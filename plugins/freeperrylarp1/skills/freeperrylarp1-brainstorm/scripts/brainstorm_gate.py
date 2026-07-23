#!/usr/bin/env python3
"""Neutral-research, isolated-generation, and independent-critic gate."""

from __future__ import annotations

import argparse
import json
import re
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
    GENERIC_AI_COPY_PATTERNS,
    MAX_ANGLE_REPAIR_CYCLES,
    all_evidence_ids,
    canonical_sha256,
    load_json,
    normalized_text,
    reject_unknown_keys,
    require_identifier,
    require_list,
    require_mapping,
    require_sha256,
    require_string,
    require_token,
    validate_campaign,
    validate_marriage_brief,
    validate_neutral_research_snapshot,
    validate_registry,
)


SCORE_FIELDS = {
    "paid_product_desire",
    "free_product_desire",
    "first_touch_clarity",
    "buyer_situation_specificity",
    "transaction_credibility",
    "evidence_fit",
    "claim_integrity",
    "creative_distinctiveness",
}
GATED_SCORE_FIELDS = {
    "paid_product_desire",
    "free_product_desire",
    "first_touch_clarity",
    "transaction_credibility",
    "evidence_fit",
    "claim_integrity",
}
CHALLENGE_FIELDS = {
    "forced_pairing",
    "generic_ai_language",
    "unsupported_assumption",
    "weak_paid_desire",
    "weak_free_desire",
    "interchangeability",
    "customer_voice_fit",
}
CHALLENGE_CONCEPT_PATTERNS = {
    "forced_pairing": re.compile(
        r"\b(?:forced|independent|together|depend|relationship)\b",
        re.IGNORECASE,
    ),
    "generic_ai_language": re.compile(
        r"\b(?:generic|language|copy|phrase|wording)\b",
        re.IGNORECASE,
    ),
    "unsupported_assumption": re.compile(
        r"\b(?:assumption|support|evidence|prove)\b",
        re.IGNORECASE,
    ),
    "weak_paid_desire": re.compile(
        r"\b(?:auralo|paid|scent|perfume|desire)\b",
        re.IGNORECASE,
    ),
    "weak_free_desire": re.compile(
        r"\b(?:free|necklace|bonus|desire|wanted)\b",
        re.IGNORECASE,
    ),
    "interchangeability": re.compile(
        r"\b(?:replace|replacement|swap|interchange|substitut)\w*\b",
        re.IGNORECASE,
    ),
    "customer_voice_fit": re.compile(
        r"\b(?:customer|buyer|voice|language|words)\b",
        re.IGNORECASE,
    ),
}
GENERIC_CHALLENGE_PATTERNS = (
    re.compile(
        r"\bpassed after (?:looking at|reviewing) (?:the )?cited evidence\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:was )?tested against (?:the )?cited current evidence\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:reviewed current evidence|no issue found|appears acceptable)\b",
        re.IGNORECASE,
    ),
)
COUNTEREVIDENCE_CHALLENGES = {
    "forced_pairing",
    "unsupported_assumption",
    "interchangeability",
}
MINIMUM_CANDIDATES = 4


def _contains_forbidden_entity(text: str, entity: str) -> bool:
    normalized = normalized_text(text)
    if " " in entity:
        return entity in normalized
    return f" {entity} " in f" {normalized} "


def _normalize_candidate(
    raw: Any,
    index: int,
    campaign: dict[str, Any],
    authorized_evidence: dict[str, str],
    research_receipt: dict[str, Any],
) -> dict[str, Any]:
    path = f"candidates[{index}]"
    candidate = require_mapping(raw, path)
    reject_unknown_keys(
        candidate,
        {
            "id",
            "generator_session_id",
            "observed_other_candidate_ids",
            "relationship_mode",
            "sales_argument",
            "hook",
            "buyer_action",
            "buyer_situation",
            "buyer_bridge",
            "transaction_bridge",
            "product_roles",
            "substitution_test",
            "evidence_ids",
            "customer_language_evidence_ids",
            "relationship_evidence_ids",
        },
        path,
        code="ANGLE_REJECTED",
    )
    session_id = require_token(
        candidate.get("generator_session_id"),
        f"{path}.generator_session_id",
    )
    observed = require_list(
        candidate.get("observed_other_candidate_ids"),
        f"{path}.observed_other_candidate_ids",
        0,
    )
    if observed:
        raise ContractError(
            "CROSS_CANDIDATE_LEAK",
            f"{path} observed another generator candidate",
            details=[str(value) for value in observed],
        )

    relationship_mode = candidate.get("relationship_mode")
    if relationship_mode not in {"wanted_premium", "evidence_backed_complement"}:
        raise ContractError("ANGLE_REJECTED", f"{path}.relationship_mode is invalid")

    sales_argument = require_string(
        candidate.get("sales_argument"),
        f"{path}.sales_argument",
        40,
    )
    for label, pattern in GENERIC_AI_COPY_PATTERNS:
        match = pattern.search(sales_argument)
        if match:
            raise ContractError(
                "GENERIC_COPY",
                f"{path}.sales_argument contains {label}",
                details=[match.group(0)],
            )

    evidence_ids = [
        require_token(value, f"{path}.evidence_ids[{item_index}]")
        for item_index, value in enumerate(
            require_list(candidate.get("evidence_ids"), f"{path}.evidence_ids", 5)
        )
    ]
    if len(set(evidence_ids)) != len(evidence_ids):
        raise ContractError("ANGLE_REJECTED", f"{path}.evidence_ids must be unique")
    research_record_ids = set(research_receipt["record_ids"])
    allowed_ids = set(authorized_evidence) | research_record_ids
    if any(evidence_id not in allowed_ids for evidence_id in evidence_ids):
        raise ContractError("ANGLE_REJECTED", f"{path} cites unknown evidence")
    product_evidence = {
        evidence_id: authorized_evidence[evidence_id]
        for evidence_id in evidence_ids
        if evidence_id in authorized_evidence
    }
    if not {"paid_product", "free_product"}.issubset(set(product_evidence.values())):
        raise ContractError(
            "ANGLE_REJECTED",
            f"{path} needs authorized paid and FREE product evidence",
        )
    research_evidence_ids = [
        evidence_id
        for evidence_id in evidence_ids
        if evidence_id in research_record_ids
    ]
    if len(research_evidence_ids) < 3:
        raise ContractError(
            "ANGLE_REJECTED",
            f"{path} must reason from at least three frozen research records",
        )

    customer_language_ids = [
        require_token(value, f"{path}.customer_language_evidence_ids[{item_index}]")
        for item_index, value in enumerate(
            require_list(
                candidate.get("customer_language_evidence_ids"),
                f"{path}.customer_language_evidence_ids",
                2,
            )
        )
    ]
    if not set(customer_language_ids).issubset(
        set(research_receipt["customer_language_ids"]) & set(evidence_ids)
    ):
        raise ContractError(
            "ANGLE_REJECTED",
            f"{path} does not preserve current customer language",
        )

    relationship_ids = [
        require_token(value, f"{path}.relationship_evidence_ids[{item_index}]")
        for item_index, value in enumerate(
            require_list(
                candidate.get("relationship_evidence_ids"),
                f"{path}.relationship_evidence_ids",
                0,
            )
        )
    ]
    if relationship_mode == "wanted_premium" and relationship_ids:
        raise ContractError(
            "MARRIAGE_GAP",
            f"{path} cannot promote inferred similarity to relationship evidence",
        )
    if relationship_mode == "evidence_backed_complement":
        valid_relationship_ids = set(research_receipt["explicit_relationship_ids"])
        if len(set(relationship_ids)) < 2 or not set(relationship_ids).issubset(
            valid_relationship_ids
        ):
            raise ContractError(
                "MARRIAGE_GAP",
                f"{path} needs two explicit dual-product research records",
            )
        if research_receipt["relationship_source_family_count"] < 2:
            raise ContractError(
                "MARRIAGE_GAP",
                f"{path} needs explicit dual-product support from two source families",
            )

    buyer_bridge = require_mapping(
        candidate.get("buyer_bridge"), f"{path}.buyer_bridge"
    )
    reject_unknown_keys(
        buyer_bridge,
        {"shared_avatar", "occasion_or_desire", "reason_to_act", "evidence_ids"},
        f"{path}.buyer_bridge",
        code="MARRIAGE_GAP",
    )
    require_string(
        buyer_bridge.get("shared_avatar"),
        f"{path}.buyer_bridge.shared_avatar",
        16,
    )
    require_string(
        buyer_bridge.get("occasion_or_desire"),
        f"{path}.buyer_bridge.occasion_or_desire",
        16,
    )
    require_string(
        buyer_bridge.get("reason_to_act"),
        f"{path}.buyer_bridge.reason_to_act",
        16,
    )
    bridge_ids = [
        require_token(value, f"{path}.buyer_bridge.evidence_ids[{item_index}]")
        for item_index, value in enumerate(
            require_list(
                buyer_bridge.get("evidence_ids"),
                f"{path}.buyer_bridge.evidence_ids",
                3,
            )
        )
    ]
    if not set(bridge_ids).issubset(evidence_ids):
        raise ContractError(
            "MARRIAGE_GAP",
            f"{path}.buyer_bridge cites evidence outside the candidate",
        )
    if not set(bridge_ids).intersection(customer_language_ids):
        raise ContractError(
            "MARRIAGE_GAP",
            f"{path}.buyer_bridge ignores preserved customer language",
        )

    roles = require_mapping(candidate.get("product_roles"), f"{path}.product_roles")
    reject_unknown_keys(roles, {"paid", "free"}, f"{path}.product_roles")
    paid_role = require_string(roles.get("paid"), f"{path}.product_roles.paid", 16)
    free_role = require_string(roles.get("free"), f"{path}.product_roles.free", 16)
    free_name = campaign["free_product"]["public_name"]
    if normalized_text(AURALO_NAME) not in normalized_text(paid_role):
        raise ContractError("MARRIAGE_GAP", f"{path} paid role does not name Auralo")
    if normalized_text(free_name) not in normalized_text(free_role):
        raise ContractError(
            "MARRIAGE_GAP",
            f"{path} FREE role does not name the current product",
        )

    transaction_bridge = require_string(
        candidate.get("transaction_bridge"),
        f"{path}.transaction_bridge",
        24,
    )
    if normalized_text(AURALO_NAME) not in normalized_text(transaction_bridge):
        raise ContractError("MARRIAGE_GAP", f"{path} bridge does not name Auralo")
    if normalized_text(free_name) not in normalized_text(transaction_bridge):
        raise ContractError(
            "MARRIAGE_GAP",
            f"{path} bridge does not name the current FREE product",
        )

    substitution = require_mapping(
        candidate.get("substitution_test"),
        f"{path}.substitution_test",
    )
    reject_unknown_keys(
        substitution,
        {"question", "reason", "evidence_ids"},
        f"{path}.substitution_test",
        code="MARRIAGE_GAP",
    )
    question = require_string(
        substitution.get("question"),
        f"{path}.substitution_test.question",
        16,
    )
    if not any(
        token in normalized_text(question)
        for token in ("replace", "replacement", "swap", "substitute", "remove")
    ):
        raise ContractError(
            "MARRIAGE_GAP",
            f"{path} substitution test does not test replacement or removal",
        )
    substitution_reason = require_string(
        substitution.get("reason"),
        f"{path}.substitution_test.reason",
        24,
    )
    if normalized_text(AURALO_NAME) not in normalized_text(substitution_reason):
        raise ContractError(
            "MARRIAGE_GAP",
            f"{path} substitution reason does not name Auralo",
        )
    if normalized_text(free_name) not in normalized_text(substitution_reason):
        raise ContractError(
            "MARRIAGE_GAP",
            f"{path} substitution reason does not name the current FREE product",
        )
    substitution_ids = [
        require_token(value, f"{path}.substitution_test.evidence_ids[{item_index}]")
        for item_index, value in enumerate(
            require_list(
                substitution.get("evidence_ids"),
                f"{path}.substitution_test.evidence_ids",
                3,
            )
        )
    ]
    if not set(substitution_ids).issubset(evidence_ids):
        raise ContractError(
            "MARRIAGE_GAP",
            f"{path} substitution test cites evidence outside the candidate",
        )

    return {
        "id": require_identifier(candidate.get("id"), f"{path}.id"),
        "generator_session_id": session_id,
        "relationship_mode": relationship_mode,
        "sales_argument": sales_argument,
        "hook": require_string(candidate.get("hook"), f"{path}.hook", 12),
        "buyer_action": require_string(
            candidate.get("buyer_action"),
            f"{path}.buyer_action",
            12,
        ),
        "buyer_situation": require_string(
            candidate.get("buyer_situation"),
            f"{path}.buyer_situation",
            16,
        ),
        "buyer_bridge": {
            "shared_avatar": buyer_bridge["shared_avatar"].strip(),
            "occasion_or_desire": buyer_bridge["occasion_or_desire"].strip(),
            "reason_to_act": buyer_bridge["reason_to_act"].strip(),
            "evidence_ids": bridge_ids,
        },
        "transaction_bridge": transaction_bridge,
        "product_roles": {"paid": paid_role, "free": free_role},
        "substitution_test": {
            "question": question,
            "reason": substitution_reason,
            "evidence_ids": substitution_ids,
        },
        "evidence_ids": evidence_ids,
        "product_evidence_ids": sorted(product_evidence),
        "research_evidence_ids": research_evidence_ids,
        "customer_language_evidence_ids": customer_language_ids,
        "relationship_evidence_ids": relationship_ids,
    }


def _critic_scores(
    critic: dict[str, Any],
    candidate_ids: set[str],
) -> dict[str, dict[str, Any]]:
    rows = require_list(critic.get("scores"), "critic.scores", len(candidate_ids))
    result: dict[str, dict[str, Any]] = {}
    for index, raw_row in enumerate(rows):
        path = f"critic.scores[{index}]"
        row = require_mapping(raw_row, path)
        candidate_id = require_identifier(
            row.get("candidate_id"), f"{path}.candidate_id"
        )
        if candidate_id not in candidate_ids or candidate_id in result:
            raise ContractError(
                "CRITIC_COVERAGE_GAP", f"{path} candidate coverage is invalid"
            )
        if set(row) != {"candidate_id", *SCORE_FIELDS}:
            raise ContractError(
                "CRITIC_COVERAGE_GAP",
                f"{path} must contain the independent score fields exactly",
            )
        scores: dict[str, int] = {}
        for field in SCORE_FIELDS:
            value = row.get(field)
            if not isinstance(value, int) or not 0 <= value <= 5:
                raise ContractError(
                    "CRITIC_COVERAGE_GAP",
                    f"{path}.{field} must be an integer from 0 to 5",
                )
            scores[field] = value
        result[candidate_id] = {
            "scores": scores,
            "total": sum(scores.values()),
            "score_eligible": all(scores[field] >= 4 for field in GATED_SCORE_FIELDS),
        }
    if set(result) != candidate_ids:
        raise ContractError("CRITIC_COVERAGE_GAP", "critic omitted candidate scores")
    return result


def _critic_challenges(
    critic: dict[str, Any],
    candidates: dict[str, dict[str, Any]],
    evidence_lanes: dict[str, str],
    required_research_ids: set[str],
    customer_language_ids: set[str],
    objection_ids: set[str],
) -> dict[str, dict[str, Any]]:
    rows = require_list(critic.get("challenges"), "critic.challenges", len(candidates))
    result: dict[str, dict[str, Any]] = {}
    seen_finding_templates: set[str] = set()
    for index, raw_row in enumerate(rows):
        path = f"critic.challenges[{index}]"
        row = require_mapping(raw_row, path)
        reject_unknown_keys(
            row,
            {"candidate_id", "verdict", "evidence_ids", "checks"},
            path,
            code="CRITIC_COVERAGE_GAP",
        )
        candidate_id = require_identifier(
            row.get("candidate_id"), f"{path}.candidate_id"
        )
        if candidate_id not in candidates or candidate_id in result:
            raise ContractError(
                "CRITIC_COVERAGE_GAP", f"{path} candidate coverage is invalid"
            )
        evidence_ids = [
            require_token(value, f"{path}.evidence_ids[{item_index}]")
            for item_index, value in enumerate(
                require_list(row.get("evidence_ids"), f"{path}.evidence_ids", 2)
            )
        ]
        if len(set(evidence_ids)) != len(evidence_ids):
            raise ContractError(
                "CHALLENGE_NOT_EXECUTED",
                f"{path}.evidence_ids must be unique",
            )
        if not set(evidence_ids).issubset(evidence_lanes):
            raise ContractError(
                "CHALLENGE_NOT_EXECUTED",
                f"{path} cites evidence outside the frozen complete evidence",
            )
        if not required_research_ids.issubset(evidence_ids):
            raise ContractError(
                "CHALLENGE_NOT_EXECUTED",
                f"{path} did not consult every frozen research record",
                details=sorted(required_research_ids - set(evidence_ids)),
            )
        checks = require_mapping(row.get("checks"), f"{path}.checks")
        if set(checks) != CHALLENGE_FIELDS:
            raise ContractError(
                "CHALLENGE_NOT_EXECUTED",
                f"{path} must execute every challenge",
                details=[
                    f"missing={sorted(CHALLENGE_FIELDS - set(checks))}",
                    f"extra={sorted(set(checks) - CHALLENGE_FIELDS)}",
                ],
            )
        normalized_checks: dict[str, dict[str, Any]] = {}
        seen_tests: set[str] = set()
        seen_findings: set[str] = set()
        all_pass = True
        for field in sorted(CHALLENGE_FIELDS):
            check = require_mapping(checks[field], f"{path}.checks.{field}")
            reject_unknown_keys(
                check,
                {
                    "status",
                    "test",
                    "finding",
                    "evidence_ids",
                    "counterevidence_ids",
                },
                f"{path}.checks.{field}",
                code="CHALLENGE_NOT_EXECUTED",
            )
            status = check.get("status")
            if status not in {"pass", "fail"}:
                raise ContractError(
                    "CHALLENGE_NOT_EXECUTED",
                    f"{path}.checks.{field}.status must be pass or fail",
                )
            test = require_string(
                check.get("test"),
                f"{path}.checks.{field}.test",
                24,
            )
            finding = require_string(
                check.get("finding"),
                f"{path}.checks.{field}.finding",
                24,
            )
            combined = f"{test} {finding}"
            if not CHALLENGE_CONCEPT_PATTERNS[field].search(combined):
                raise ContractError(
                    "CHALLENGE_NOT_EXECUTED",
                    f"{path}.checks.{field} does not execute its named test",
                )
            if candidate_id.casefold() not in combined.casefold():
                raise ContractError(
                    "CHALLENGE_NOT_EXECUTED",
                    f"{path}.checks.{field} is not bound to {candidate_id}",
                )
            generic_match = next(
                (
                    pattern.search(combined)
                    for pattern in GENERIC_CHALLENGE_PATTERNS
                    if pattern.search(combined)
                ),
                None,
            )
            if generic_match:
                raise ContractError(
                    "CHALLENGE_NOT_EXECUTED",
                    f"{path}.checks.{field} contains a reusable boilerplate result",
                    details=[generic_match.group(0)],
                )
            normalized_test = normalized_text(test)
            normalized_finding = normalized_text(finding)
            finding_template = normalized_text(
                re.sub(
                    re.escape(candidate_id),
                    "",
                    finding,
                    flags=re.IGNORECASE,
                )
            )
            if normalized_test in seen_tests or normalized_finding in seen_findings:
                raise ContractError(
                    "CHALLENGE_NOT_EXECUTED",
                    f"{path}.checks.{field} reuses another challenge result",
                )
            seen_tests.add(normalized_test)
            seen_findings.add(normalized_finding)
            if finding_template in seen_finding_templates:
                raise ContractError(
                    "CHALLENGE_NOT_EXECUTED",
                    f"{path}.checks.{field} reuses a finding from another candidate",
                )
            seen_finding_templates.add(finding_template)

            check_evidence_ids = [
                require_token(
                    value,
                    f"{path}.checks.{field}.evidence_ids[{item_index}]",
                )
                for item_index, value in enumerate(
                    require_list(
                        check.get("evidence_ids"),
                        f"{path}.checks.{field}.evidence_ids",
                        2,
                    )
                )
            ]
            counterevidence_ids = [
                require_token(
                    value,
                    f"{path}.checks.{field}.counterevidence_ids[{item_index}]",
                )
                for item_index, value in enumerate(
                    require_list(
                        check.get("counterevidence_ids"),
                        f"{path}.checks.{field}.counterevidence_ids",
                        0,
                    )
                )
            ]
            if len(set(check_evidence_ids)) != len(check_evidence_ids):
                raise ContractError(
                    "CHALLENGE_NOT_EXECUTED",
                    f"{path}.checks.{field}.evidence_ids must be unique",
                )
            if len(set(counterevidence_ids)) != len(counterevidence_ids):
                raise ContractError(
                    "CHALLENGE_NOT_EXECUTED",
                    f"{path}.checks.{field}.counterevidence_ids must be unique",
                )
            if not set(check_evidence_ids).issubset(evidence_ids):
                raise ContractError(
                    "CHALLENGE_NOT_EXECUTED",
                    f"{path}.checks.{field} cites evidence not consulted by the critic",
                )
            if not set(counterevidence_ids).issubset(check_evidence_ids):
                raise ContractError(
                    "CHALLENGE_NOT_EXECUTED",
                    f"{path}.checks.{field} counterevidence is not in its evidence set",
                )
            check_lanes = {
                evidence_lanes[evidence_id] for evidence_id in check_evidence_ids
            }
            if field in {
                "forced_pairing",
                "unsupported_assumption",
                "interchangeability",
            } and not {"paid_product", "free_product"}.issubset(check_lanes):
                raise ContractError(
                    "CHALLENGE_NOT_EXECUTED",
                    f"{path}.checks.{field} must test both product lanes",
                )
            if field == "weak_paid_desire" and "paid_product" not in check_lanes:
                raise ContractError(
                    "CHALLENGE_NOT_EXECUTED",
                    f"{path}.checks.{field} lacks paid-product evidence",
                )
            if field == "weak_free_desire" and "free_product" not in check_lanes:
                raise ContractError(
                    "CHALLENGE_NOT_EXECUTED",
                    f"{path}.checks.{field} lacks FREE-product evidence",
                )
            if field in {"generic_ai_language", "customer_voice_fit"} and not (
                set(check_evidence_ids) & customer_language_ids
            ):
                raise ContractError(
                    "CHALLENGE_NOT_EXECUTED",
                    f"{path}.checks.{field} lacks preserved customer language",
                )
            if field in COUNTEREVIDENCE_CHALLENGES and not (
                set(counterevidence_ids) & objection_ids
            ):
                raise ContractError(
                    "CHALLENGE_NOT_EXECUTED",
                    f"{path}.checks.{field} lacks objection counterevidence",
                )
            normalized_checks[field] = {
                "status": status,
                "test": test,
                "finding": finding,
                "evidence_ids": check_evidence_ids,
                "counterevidence_ids": counterevidence_ids,
            }
            all_pass = all_pass and status == "pass"
        expected_verdict = "eligible" if all_pass else "rejected"
        if row.get("verdict") != expected_verdict:
            raise ContractError(
                "CHALLENGE_NOT_EXECUTED",
                f"{path}.verdict does not match executed challenge results",
            )
        result[candidate_id] = {
            "verdict": expected_verdict,
            "evidence_ids": evidence_ids,
            "checks": normalized_checks,
        }
    if set(result) != set(candidates):
        raise ContractError(
            "CRITIC_COVERAGE_GAP", "critic omitted candidate challenges"
        )
    return result


def _writer_packet(
    primary: dict[str, Any],
    campaign: dict[str, Any],
    dossier: dict[str, Any],
    research_snapshot: dict[str, Any],
    research_receipt: dict[str, Any],
) -> dict[str, Any]:
    all_records = research_snapshot["records"]
    customer_language = [
        {
            "id": record["id"],
            "text": record["text"],
            "target_product_id": record["target_product_id"],
            "source_family": record["source_family"],
        }
        for record in all_records
        if record["kind"] == "customer_language"
    ]
    objections = [
        {"id": record["id"], "text": record["text"]}
        for record in all_records
        if record["kind"] == "objection"
    ]
    purchase_triggers = [
        {"id": record["id"], "text": record["text"]}
        for record in all_records
        if record["kind"] == "purchase_trigger"
    ]
    market_context = [
        {"id": record["id"], "text": record["text"]}
        for record in all_records
        if record["kind"] == "market_context"
    ]
    return {
        "schema_version": "1.0",
        "campaign_id": campaign["campaign_id"],
        "research_snapshot_sha256": research_receipt["sha256"],
        "paid_product_truth": {
            "id": AURALO_ID,
            "public_name": AURALO_NAME,
            "price_public": "$29",
            "facts": [
                {
                    "evidence_id": row["evidence_id"],
                    "public_language": row["public_language"],
                }
                for row in dossier["facts"]
            ],
        },
        "free_product_truth": {
            "id": campaign["free_product"]["id"],
            "public_name": campaign["free_product"]["public_name"],
            "public_label": "FREE",
            "facts": [
                {
                    "evidence_id": row["evidence_id"],
                    "public_language": row["public_language"],
                }
                for row in campaign["free_product"]["facts"]
            ],
        },
        "customer_language": customer_language,
        "objections": objections,
        "purchase_triggers": purchase_triggers,
        "market_context": market_context,
        "plain_english_sales_argument": primary["sales_argument"],
        "writer_job": {
            "sequence": [
                f"Make {AURALO_NAME} desirable on its evidenced merits.",
                (
                    f"Make {campaign['free_product']['public_name']} desirable "
                    "on its evidenced merits."
                ),
                "State the $29 and FREE transaction clearly.",
                "Write the complete natural sales argument before assigning sections or images.",
            ],
            "public_boundaries": [
                "Use only current product truth and current customer evidence.",
                "Do not publish private planning metadata or production directions.",
                "Do not invent proof, outcomes, reviews, urgency, or product behavior.",
            ],
        },
    }


def _candidate_brief(
    primary: dict[str, Any],
    backup: dict[str, Any],
    campaign: dict[str, Any],
    repair_cycle: int,
    research_receipt: dict[str, Any],
    candidate_set_sha256: str,
    critic: dict[str, Any],
    generator_session_ids: list[str],
    writer_packet_sha256: str,
) -> dict[str, Any]:
    return {
        "schema_version": "2.0",
        "status": "accepted",
        "campaign_id": campaign["campaign_id"],
        "paid_product_id": AURALO_ID,
        "free_product_id": campaign["free_product"]["id"],
        "relationship_mode": primary["relationship_mode"],
        "repair_cycles": repair_cycle,
        "primary_angle": {
            "id": primary["id"],
            "hook": primary["hook"],
            "buyer_action": primary["buyer_action"],
        },
        "backup_angle": {
            "id": backup["id"],
            "hook": backup["hook"],
            "buyer_action": backup["buyer_action"],
        },
        "sales_argument": primary["sales_argument"],
        "buyer_moment": primary["buyer_situation"],
        "buyer_bridge": primary["buyer_bridge"],
        "transaction_bridge": primary["transaction_bridge"],
        "product_roles": primary["product_roles"],
        "substitution_test": {
            **primary["substitution_test"],
            "result": "passed",
        },
        "evidence_ids": primary["product_evidence_ids"],
        "research_evidence_ids": primary["research_evidence_ids"],
        "customer_language_evidence_ids": primary["customer_language_evidence_ids"],
        "relationship_evidence_ids": primary["relationship_evidence_ids"],
        "relationship_source_family_count": research_receipt[
            "relationship_source_family_count"
        ],
        "research_snapshot_sha256": research_receipt["sha256"],
        "candidate_set_sha256": candidate_set_sha256,
        "critic_receipt_sha256": canonical_sha256(critic),
        "writer_packet_sha256": writer_packet_sha256,
        "generator_session_ids": generator_session_ids,
        "critic_session_id": critic["critic_session_id"],
    }


def select_angles(
    payload: dict[str, Any],
    campaign: dict[str, Any],
    dossier: dict[str, Any],
    *,
    asset_root: Path,
) -> dict[str, Any]:
    validate_campaign(campaign, dossier, asset_root=asset_root)
    reject_unknown_keys(
        payload,
        {
            "schema_version",
            "repair_cycle",
            "research_snapshot",
            "prior_entity_registry",
            "candidates",
            "critic",
        },
        "brainstorm_payload",
        code="ANGLE_REJECTED",
    )
    if payload.get("schema_version") != "2.0":
        raise ContractError(
            "ANGLE_REJECTED", "brainstorm payload schema_version must equal 2.0"
        )
    repair_cycle = payload.get("repair_cycle")
    if not isinstance(repair_cycle, int) or repair_cycle < 0:
        raise ContractError("ANGLE_GAP", "repair_cycle must be a non-negative integer")
    if repair_cycle > MAX_ANGLE_REPAIR_CYCLES:
        raise ContractError(
            "ANGLE_GAP",
            f"repair limit exceeded: {repair_cycle}>{MAX_ANGLE_REPAIR_CYCLES}",
        )

    research_snapshot = require_mapping(
        payload.get("research_snapshot"),
        "research_snapshot",
    )
    research_receipt = validate_neutral_research_snapshot(
        research_snapshot,
        campaign,
        dossier,
        asset_root=asset_root,
    )
    registry = require_mapping(
        payload.get("prior_entity_registry"),
        "prior_entity_registry",
    )
    forbidden_entities = validate_registry(registry, campaign)
    pre_writer_text = json.dumps(
        {
            "research_snapshot": research_snapshot,
            "candidates": payload.get("candidates"),
        },
        ensure_ascii=False,
    )
    prior_hits = sorted(
        entity
        for entity in forbidden_entities
        if _contains_forbidden_entity(pre_writer_text, entity)
    )
    if prior_hits:
        raise ContractError(
            "CROSS_CAMPAIGN_LEAK",
            "research or connection hypotheses contain a prior FREE-product entity",
            details=prior_hits,
        )
    authorized_evidence = all_evidence_ids(dossier, campaign)
    raw_candidates = require_list(
        payload.get("candidates"),
        "candidates",
        1,
    )
    if len(raw_candidates) < MINIMUM_CANDIDATES:
        code = (
            "ANGLE_GAP"
            if repair_cycle >= MAX_ANGLE_REPAIR_CYCLES
            else "ANGLE_REPAIR_REQUIRED"
        )
        raise ContractError(
            code,
            f"at least {MINIMUM_CANDIDATES} materially different connection hypotheses are required",
        )
    normalized_candidates: list[dict[str, Any]] = []
    rejections: list[str] = []
    for index, candidate in enumerate(raw_candidates):
        try:
            normalized_candidates.append(
                _normalize_candidate(
                    candidate,
                    index,
                    campaign,
                    authorized_evidence,
                    research_receipt,
                )
            )
        except ContractError as error:
            rejections.append(f"candidates[{index}]={error.code}:{error.message}")

    if len(normalized_candidates) < MINIMUM_CANDIDATES:
        code = (
            "ANGLE_GAP"
            if repair_cycle >= MAX_ANGLE_REPAIR_CYCLES
            else "ANGLE_REPAIR_REQUIRED"
        )
        raise ContractError(
            code,
            f"fewer than {MINIMUM_CANDIDATES} valid connection hypotheses remain",
            details=rejections,
        )
    candidate_ids = [candidate["id"] for candidate in normalized_candidates]
    if len(set(candidate_ids)) != len(candidate_ids):
        raise ContractError("ANGLE_REJECTED", "candidate IDs must be unique")
    generator_sessions = [
        candidate["generator_session_id"] for candidate in normalized_candidates
    ]
    if len(set(generator_sessions)) != len(generator_sessions):
        raise ContractError(
            "ISOLATION_NOT_AVAILABLE",
            "every connection hypothesis needs a unique generator session",
        )
    distinct_arguments = {
        normalized_text(candidate["sales_argument"])
        for candidate in normalized_candidates
    }
    distinct_situations = {
        normalized_text(candidate["buyer_situation"])
        for candidate in normalized_candidates
    }
    if len(distinct_arguments) < MINIMUM_CANDIDATES or len(distinct_situations) < 3:
        code = (
            "ANGLE_GAP"
            if repair_cycle >= MAX_ANGLE_REPAIR_CYCLES
            else "ANGLE_REPAIR_REQUIRED"
        )
        raise ContractError(
            code,
            "candidate set contains wording variants instead of materially different connections",
        )

    candidate_set_sha256 = canonical_sha256(normalized_candidates)
    critic = require_mapping(payload.get("critic"), "critic")
    reject_unknown_keys(
        critic,
        {
            "schema_version",
            "critic_session_id",
            "research_snapshot_sha256",
            "candidate_set_sha256",
            "evaluated_candidate_ids",
            "scores",
            "challenges",
            "primary_candidate_id",
            "backup_candidate_id",
            "selection_reason",
            "rejected_assumptions",
            "second_order_consequences",
            "third_order_consequences",
            "unresolved_evidence_gaps",
        },
        "critic",
        code="CRITIC_COVERAGE_GAP",
    )
    if critic.get("schema_version") != "1.0":
        raise ContractError(
            "CRITIC_COVERAGE_GAP", "critic schema_version must equal 1.0"
        )
    critic_session = require_token(
        critic.get("critic_session_id"),
        "critic.critic_session_id",
    )
    if critic_session in set(generator_sessions):
        raise ContractError(
            "CRITIC_NOT_INDEPENDENT",
            "critic session cannot be a generator session",
        )
    if (
        require_sha256(
            critic.get("research_snapshot_sha256"),
            "critic.research_snapshot_sha256",
        )
        != research_receipt["sha256"]
    ):
        raise ContractError(
            "RESEARCH_HASH_MISMATCH",
            "critic did not read the frozen neutral research snapshot",
        )
    if (
        require_sha256(
            critic.get("candidate_set_sha256"),
            "critic.candidate_set_sha256",
        )
        != candidate_set_sha256
    ):
        raise ContractError(
            "CANDIDATE_SET_HASH_MISMATCH",
            "critic did not read the exact candidate set",
        )
    evaluated = [
        require_identifier(value, f"critic.evaluated_candidate_ids[{index}]")
        for index, value in enumerate(
            require_list(
                critic.get("evaluated_candidate_ids"),
                "critic.evaluated_candidate_ids",
                len(candidate_ids),
            )
        )
    ]
    if set(evaluated) != set(candidate_ids) or len(evaluated) != len(candidate_ids):
        raise ContractError(
            "CRITIC_COVERAGE_GAP", "critic did not evaluate every candidate"
        )
    candidate_map = {candidate["id"]: candidate for candidate in normalized_candidates}
    scores = _critic_scores(critic, set(candidate_ids))
    evidence_lanes = {
        **authorized_evidence,
        **research_receipt["record_lanes"],
    }
    challenges = _critic_challenges(
        critic,
        candidate_map,
        evidence_lanes,
        set(research_receipt["record_ids"]),
        set(research_receipt["customer_language_ids"]),
        set(research_receipt["objection_ids"]),
    )
    require_string(critic.get("selection_reason"), "critic.selection_reason", 24)
    for field in (
        "rejected_assumptions",
        "second_order_consequences",
        "third_order_consequences",
    ):
        rows = require_list(critic.get(field), f"critic.{field}", 1)
        for index, value in enumerate(rows):
            require_string(value, f"critic.{field}[{index}]", 12)
    gaps = require_list(
        critic.get("unresolved_evidence_gaps"),
        "critic.unresolved_evidence_gaps",
        0,
    )
    if gaps:
        raise ContractError(
            "MARRIAGE_GAP",
            "critic found unresolved evidence gaps",
            details=[str(value) for value in gaps],
        )

    eligible = [
        candidate_map[candidate_id]
        for candidate_id in candidate_ids
        if scores[candidate_id]["score_eligible"]
        and challenges[candidate_id]["verdict"] == "eligible"
    ]
    eligible.sort(key=lambda row: (-scores[row["id"]]["total"], row["id"]))
    if len(eligible) < 2:
        code = (
            "ANGLE_GAP"
            if repair_cycle >= MAX_ANGLE_REPAIR_CYCLES
            else "ANGLE_REPAIR_REQUIRED"
        )
        raise ContractError(
            code,
            "independent challenge left fewer than two eligible connections",
        )
    primary = eligible[0]
    backup = next(
        (
            candidate
            for candidate in eligible[1:]
            if normalized_text(candidate["sales_argument"])
            != normalized_text(primary["sales_argument"])
            and normalized_text(candidate["buyer_situation"])
            != normalized_text(primary["buyer_situation"])
        ),
        None,
    )
    if backup is None:
        code = (
            "ANGLE_GAP"
            if repair_cycle >= MAX_ANGLE_REPAIR_CYCLES
            else "ANGLE_REPAIR_REQUIRED"
        )
        raise ContractError(
            code, "independent critic found no materially different backup"
        )
    if critic.get("primary_candidate_id") != primary["id"]:
        raise ContractError(
            "CRITIC_SELECTION_INVALID",
            "critic primary is not the highest-scoring eligible connection",
        )
    if critic.get("backup_candidate_id") != backup["id"]:
        raise ContractError(
            "CRITIC_SELECTION_INVALID",
            "critic backup is not the strongest materially different eligible connection",
        )

    writer_packet = _writer_packet(
        primary,
        campaign,
        dossier,
        research_snapshot,
        research_receipt,
    )
    writer_packet_sha256 = canonical_sha256(writer_packet)
    brief = _candidate_brief(
        primary,
        backup,
        campaign,
        repair_cycle,
        research_receipt,
        candidate_set_sha256,
        critic,
        generator_sessions,
        writer_packet_sha256,
    )
    receipt = validate_marriage_brief(
        brief,
        campaign,
        dossier,
        asset_root=asset_root,
    )
    return {
        "status": "accepted",
        "research_state": research_receipt["status"],
        "research_snapshot_sha256": research_receipt["sha256"],
        "candidate_set_sha256": candidate_set_sha256,
        "critic_receipt_sha256": canonical_sha256(critic),
        "writer_packet": writer_packet,
        "writer_packet_sha256": writer_packet_sha256,
        "decision_brief": brief,
        "decision_brief_sha256": receipt["sha256"],
        "primary_critic_total": scores[primary["id"]]["total"],
        "backup_critic_total": scores[backup["id"]]["total"],
        "challenged_candidate_count": len(challenges),
        "rejected_candidates": rejections,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--campaign", type=Path, required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--dossier", type=Path, default=DEFAULT_DOSSIER_PATH)
    parser.add_argument("--asset-root", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        result = select_angles(
            load_json(args.input),
            load_json(args.campaign),
            load_json(args.dossier),
            asset_root=args.asset_root,
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
