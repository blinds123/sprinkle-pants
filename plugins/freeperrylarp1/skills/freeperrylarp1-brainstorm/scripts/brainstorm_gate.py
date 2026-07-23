#!/usr/bin/env python3
"""Bounded, evidence-gated angle selection for FreePerryLarp1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


MAIN_SCRIPTS = Path(__file__).resolve().parents[2] / "freeperrylarp1" / "scripts"
if str(MAIN_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(MAIN_SCRIPTS))

from freeperrylarp1_contract import (  # noqa: E402
    AURALO_ID,
    AURALO_NAME,
    ContractError,
    DEFAULT_DOSSIER_PATH,
    MAX_ANGLE_REPAIR_CYCLES,
    all_evidence_ids,
    load_json,
    normalized_text,
    require_identifier,
    require_list,
    require_mapping,
    require_string,
    validate_campaign,
    validate_marriage_brief,
)


SCORE_FIELDS = {
    "paid_product_desire",
    "free_product_desire",
    "first_touch_clarity",
    "buyer_moment_specificity",
    "transaction_bridge_credibility",
    "evidence_fit",
    "claim_integrity",
    "creative_distinctiveness",
}
GATED_SCORE_FIELDS = {
    "paid_product_desire",
    "free_product_desire",
    "first_touch_clarity",
    "transaction_bridge_credibility",
    "evidence_fit",
    "claim_integrity",
}


def _candidate_brief(
    candidate: dict[str, Any],
    backup: dict[str, Any],
    campaign: dict[str, Any],
    repair_cycle: int,
) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "status": "accepted",
        "campaign_id": campaign["campaign_id"],
        "paid_product_id": AURALO_ID,
        "free_product_id": campaign["free_product"]["id"],
        "relationship_mode": candidate["relationship_mode"],
        "repair_cycles": repair_cycle,
        "primary_angle": {
            "id": candidate["id"],
            "hook": candidate["hook"],
            "buyer_action": candidate["buyer_action"],
        },
        "backup_angle": {
            "id": backup["id"],
            "hook": backup["hook"],
            "buyer_action": backup["buyer_action"],
        },
        "buyer_moment": candidate["buyer_moment"],
        "transaction_bridge": candidate["transaction_bridge"],
        "product_roles": candidate["product_roles"],
        "substitution_test": candidate["substitution_test"],
        "evidence_ids": candidate["evidence_ids"],
        "relationship_evidence_ids": candidate.get(
            "relationship_evidence_ids",
            [],
        ),
        "scorecard": candidate["scores"],
        "falsification_plan": candidate["falsification_plan"],
    }


def _validate_scores(candidate: dict[str, Any], path: str) -> int:
    scores = require_mapping(candidate.get("scores"), f"{path}.scores")
    if set(scores) != SCORE_FIELDS:
        raise ContractError(
            "ANGLE_REJECTED",
            f"{path}.scores must contain exactly the eight scorecard fields",
            details=[
                f"missing={sorted(SCORE_FIELDS - set(scores))}",
                f"extra={sorted(set(scores) - SCORE_FIELDS)}",
            ],
        )
    for field, value in scores.items():
        if not isinstance(value, int) or not 0 <= value <= 5:
            raise ContractError(
                "ANGLE_REJECTED",
                f"{path}.scores.{field} must be an integer from 0 to 5",
            )
    low_gates = sorted(field for field in GATED_SCORE_FIELDS if scores[field] < 4)
    if low_gates:
        raise ContractError(
            "ANGLE_REJECTED",
            f"{path} fails evidence/claim integrity gate",
            details=low_gates,
        )
    return sum(scores.values())


def _normalize_candidate(
    raw: Any,
    index: int,
    campaign: dict[str, Any],
    evidence_map: dict[str, str],
) -> dict[str, Any]:
    path = f"candidates[{index}]"
    candidate = require_mapping(raw, path)
    result = {
        "id": require_identifier(candidate.get("id"), f"{path}.id"),
        "relationship_mode": candidate.get("relationship_mode"),
        "hook": require_string(candidate.get("hook"), f"{path}.hook", 12),
        "buyer_action": require_string(
            candidate.get("buyer_action"),
            f"{path}.buyer_action",
            12,
        ),
        "buyer_moment": require_string(
            candidate.get("buyer_moment"),
            f"{path}.buyer_moment",
            16,
        ),
        "transaction_bridge": require_string(
            candidate.get("transaction_bridge"),
            f"{path}.transaction_bridge",
            24,
        ),
        "product_roles": require_mapping(
            candidate.get("product_roles"),
            f"{path}.product_roles",
        ),
        "substitution_test": require_mapping(
            candidate.get("substitution_test"),
            f"{path}.substitution_test",
        ),
        "evidence_ids": require_list(
            candidate.get("evidence_ids"),
            f"{path}.evidence_ids",
            2,
        ),
        "relationship_evidence_ids": require_list(
            candidate.get("relationship_evidence_ids"),
            f"{path}.relationship_evidence_ids",
            0,
        ),
        "scores": require_mapping(candidate.get("scores"), f"{path}.scores"),
        "falsification_plan": require_string(
            candidate.get("falsification_plan"),
            f"{path}.falsification_plan",
            16,
        ),
    }
    if result["relationship_mode"] not in {
        "wanted_premium",
        "evidence_backed_complement",
    }:
        raise ContractError(
            "ANGLE_REJECTED",
            f"{path}.relationship_mode is invalid",
        )
    roles = result["product_roles"]
    paid_role = require_string(roles.get("paid"), f"{path}.product_roles.paid", 16)
    free_role = require_string(roles.get("free"), f"{path}.product_roles.free", 16)
    if normalized_text(AURALO_NAME) not in normalized_text(paid_role):
        raise ContractError("MARRIAGE_GAP", f"{path} paid role does not name Auralo")
    free_name = campaign["free_product"]["public_name"]
    if normalized_text(free_name) not in normalized_text(free_role):
        raise ContractError(
            "MARRIAGE_GAP",
            f"{path} FREE role does not name the current product",
        )
    substitution = result["substitution_test"]
    require_string(
        substitution.get("question"),
        f"{path}.substitution_test.question",
        16,
    )
    if substitution.get("result") != "passed":
        raise ContractError("MARRIAGE_GAP", f"{path} substitution test did not pass")
    if normalized_text(AURALO_NAME) not in normalized_text(
        result["transaction_bridge"]
    ):
        raise ContractError("MARRIAGE_GAP", f"{path} bridge does not name Auralo")
    if normalized_text(free_name) not in normalized_text(result["transaction_bridge"]):
        raise ContractError(
            "MARRIAGE_GAP",
            f"{path} bridge does not name the current FREE product",
        )
    if any(evidence_id not in evidence_map for evidence_id in result["evidence_ids"]):
        raise ContractError("ANGLE_REJECTED", f"{path} cites unknown evidence")
    cited_lanes = {evidence_map[evidence_id] for evidence_id in result["evidence_ids"]}
    if not {"paid_product", "free_product"}.issubset(cited_lanes):
        raise ContractError(
            "ANGLE_REJECTED",
            f"{path} needs paid and FREE product evidence",
        )
    if result["relationship_mode"] == "evidence_backed_complement":
        valid_relationship = {
            evidence_id
            for evidence_id in result["relationship_evidence_ids"]
            if evidence_map.get(evidence_id) == "relationship"
        }
        if len(valid_relationship) < 2:
            raise ContractError(
                "MARRIAGE_GAP",
                f"{path} complement mode lacks two current relationship evidence rows",
            )
    result["total_score"] = _validate_scores(candidate, path)
    return result


def select_angles(
    payload: dict[str, Any],
    campaign: dict[str, Any],
    dossier: dict[str, Any],
) -> dict[str, Any]:
    validate_campaign(campaign, dossier)
    repair_cycle = payload.get("repair_cycle")
    if not isinstance(repair_cycle, int) or repair_cycle < 0:
        raise ContractError(
            "ANGLE_GAP",
            "repair_cycle must be a non-negative integer",
        )
    if repair_cycle > MAX_ANGLE_REPAIR_CYCLES:
        raise ContractError(
            "ANGLE_GAP",
            f"repair limit exceeded: {repair_cycle}>{MAX_ANGLE_REPAIR_CYCLES}",
        )
    candidates = require_list(payload.get("candidates"), "candidates", 1)
    evidence_map = all_evidence_ids(dossier, campaign)
    valid: list[dict[str, Any]] = []
    rejections: list[str] = []
    marriage_failures = 0
    for index, candidate in enumerate(candidates):
        try:
            valid.append(_normalize_candidate(candidate, index, campaign, evidence_map))
        except ContractError as error:
            rejections.append(f"candidates[{index}]={error.code}:{error.message}")
            if error.code == "MARRIAGE_GAP":
                marriage_failures += 1

    valid.sort(key=lambda row: (-row["total_score"], row["id"]))
    if len(valid) < 2:
        if not valid and marriage_failures == len(candidates):
            raise ContractError(
                "MARRIAGE_GAP",
                "no candidate materializes distinct, evidence-backed product roles",
                details=rejections,
            )
        if repair_cycle >= MAX_ANGLE_REPAIR_CYCLES:
            raise ContractError(
                "ANGLE_GAP",
                "two repair cycles ended without primary and backup angles",
                details=rejections,
            )
        raise ContractError(
            "ANGLE_REPAIR_REQUIRED",
            "fewer than two valid, materially different angles remain",
            details=rejections,
        )

    primary = valid[0]
    backup = next(
        (
            candidate
            for candidate in valid[1:]
            if normalized_text(candidate["hook"]) != normalized_text(primary["hook"])
            and normalized_text(candidate["buyer_moment"])
            != normalized_text(primary["buyer_moment"])
        ),
        None,
    )
    if backup is None:
        if repair_cycle >= MAX_ANGLE_REPAIR_CYCLES:
            raise ContractError(
                "ANGLE_GAP",
                "backup candidates are wording variants of the primary",
            )
        raise ContractError(
            "ANGLE_REPAIR_REQUIRED",
            "a meaningfully different backup angle is required",
        )

    brief = _candidate_brief(primary, backup, campaign, repair_cycle)
    receipt = validate_marriage_brief(brief, campaign, dossier)
    return {
        "status": "accepted",
        "decision_brief": brief,
        "decision_brief_sha256": receipt["sha256"],
        "primary_total_score": primary["total_score"],
        "backup_total_score": backup["total_score"],
        "rejected_candidates": rejections,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--campaign", type=Path, required=True)
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--dossier", type=Path, default=DEFAULT_DOSSIER_PATH)
    parser.add_argument("--output", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        result = select_angles(
            load_json(args.candidates),
            load_json(args.campaign),
            load_json(args.dossier),
        )
        rendered = (
            json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
        )
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(rendered, encoding="utf-8")
            print(args.output)
        else:
            print(rendered, end="")
        return 0
    except ContractError as error:
        print(
            json.dumps(error.as_dict(), indent=2, ensure_ascii=False), file=sys.stderr
        )
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
