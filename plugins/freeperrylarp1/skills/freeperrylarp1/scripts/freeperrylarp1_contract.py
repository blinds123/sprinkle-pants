#!/usr/bin/env python3
"""Deterministic foundation contracts for FreePerryLarp1.

This module deliberately contains no campaign copy generator. It validates the
fixed paid-product dossier, one current FREE-product campaign, the mandatory
marriage brief, and the public/prompt boundary that later phases must satisfy.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable, Iterator


AURALO_ID = "auralo-pheromone-perfume-15ml"
AURALO_NAME = "Auralo Pheromone Perfume"
AURALO_PRICE_USD = 29
AURALO_DOSSIER_VERSION = "1.0.0"
EXPECTED_DOSSIER_SHA256 = (
    "375f9f95d6674261b8ca8a99e3cd7daa3887d3446812c14a2d1b430ac0f474d9"
)
MAX_ANGLE_REPAIR_CYCLES = 2
RELATIONSHIP_MODES = {"wanted_premium", "evidence_backed_complement"}
DEFAULT_DOSSIER_PATH = (
    Path(__file__).resolve().parents[1] / "assets" / "auralo-dossier.json"
)

REQUIRED_AURALO_EVIDENCE_IDS = {
    "AURALO-IDENTITY-001",
    "AURALO-SCENT-001",
    "AURALO-USE-001",
    "AURALO-PRICE-001",
}

INTERNAL_STRATEGY_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "product-marriage diagnosis",
        re.compile(
            r"\b(?:marry(?:ing)? (?:the )?products?|product marriage|"
            r"offer marriage|product relationship|relationship mode|"
            r"this pairing|pairing logic)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "generic two-product diagnosis",
        re.compile(
            r"\b(?:two random products?|random products?|both products?|"
            r"two products?|one product.{0,30}the other product|"
            r"not (?:two|separate) products?)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "abstract relationship language",
        re.compile(
            r"\b(?:belong together|complete ritual|shared moment|"
            r"coherent moment|same getting[- ]ready (?:story|decision)|"
            r"one getting[- ]ready story|sensory layer|"
            r"visible first impression)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "private marketing framework",
        re.compile(
            r"\b(?:value stack|tripwire|big domino|grand slam offer|"
            r"avatar|internal strategy|framework label|fibs|engage)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "production label",
        re.compile(
            r"\b(?:visible text(?: exact)?|text overlay instruction|"
            r"prompt instruction|production instruction|show both products?)\b",
            re.IGNORECASE,
        ),
    ),
)

GENERIC_PUBLIC_PRODUCT_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("paid-product placeholder", re.compile(r"\bpaid product\b", re.IGNORECASE)),
    (
        "free-product placeholder",
        re.compile(r"\b(?:the )?free product\b", re.IGNORECASE),
    ),
    (
        "companion-product placeholder",
        re.compile(r"\bcompanion product\b", re.IGNORECASE),
    ),
)

VISIBLE_PRODUCTION_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "camera direction",
        re.compile(
            r"\b(?:camera angle|close[- ]up shot|wide shot|hero crop|"
            r"photograph the|place the product|render the text|"
            r"use the supplied image|add an overlay)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "layout direction",
        re.compile(
            r"\b(?:left[- ]aligned headline|right[- ]hand product|"
            r"font size|design note|art direction|layout instruction)\b",
            re.IGNORECASE,
        ),
    ),
)

UNSUPPORTED_OUTCOME_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "guaranteed attraction or desire",
        re.compile(
            r"\b(?:guarantee(?:d|s)?|instant|clinically proven|scientifically proven)"
            r".{0,24}\b(?:attraction|desire|attention|compliments?)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "cannot-resist outcome",
        re.compile(
            r"\b(?:every (?:man|woman)|men|women|him|her|people)"
            r".{0,20}\b(?:cannot|can't|will not|won't|unable to)\b"
            r".{0,12}\bresist\b",
            re.IGNORECASE,
        ),
    ),
    (
        "forced social outcome",
        re.compile(
            r"\b(?:make|makes|made|force|forces)"
            r".{0,24}\b(?:men|women|him|her|people|everyone)\b"
            r".{0,24}\b(?:attract(?:ed|ion)?|flirt|desire|chase|compliment)\w*",
            re.IGNORECASE,
        ),
    ),
    (
        "pheromone outcome transfer",
        re.compile(
            r"\bpheromones?\b.{0,36}\b(?:attract|desire|flirt|chase|"
            r"compliment|irresistible)\w*",
            re.IGNORECASE,
        ),
    ),
    (
        "fabricated social proof",
        re.compile(
            r"\b(?:verified customer|verified buyer|"
            r"\d[\d,.\s]*\+?\s+(?:reviews?|customers?))\b",
            re.IGNORECASE,
        ),
    ),
)

COMMON_ENTITY_WORDS = {
    "accessory",
    "and",
    "bundle",
    "free",
    "gift",
    "item",
    "product",
    "the",
    "with",
}

PUBLIC_ROOT_KEYS = {
    "alt_text",
    "body",
    "caption",
    "copy",
    "cta",
    "customer_facing",
    "footer",
    "headline",
    "image_text",
    "site_data",
    "subheadline",
    "visible_text",
}

DIRECTION_ROOT_KEYS = {
    "negative_prompt",
    "production_direction",
    "prompt",
    "prompt_text",
    "visual_direction",
}


class ContractError(ValueError):
    """A stable machine-readable contract failure."""

    def __init__(
        self,
        code: str,
        message: str,
        *,
        details: Iterable[str] | None = None,
    ) -> None:
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message
        self.details = tuple(details or ())

    def as_dict(self) -> dict[str, Any]:
        return {
            "status": "blocked",
            "code": self.code,
            "message": self.message,
            "details": list(self.details),
        }


def load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ContractError("INVALID_JSON", f"{path}: {error}") from error
    if not isinstance(payload, dict):
        raise ContractError("INVALID_JSON", f"{path} must contain a JSON object")
    return payload


def canonical_json(payload: Any) -> str:
    return json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )


def canonical_sha256(payload: Any) -> str:
    return hashlib.sha256(canonical_json(payload).encode("utf-8")).hexdigest()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_mapping(value: Any, path: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ContractError("INVALID_CONTRACT", f"{path} must be an object")
    return value


def reject_unknown_keys(
    value: dict[str, Any],
    allowed: set[str],
    path: str,
    *,
    code: str = "INVALID_CONTRACT",
) -> None:
    unknown = sorted(set(value) - allowed)
    if unknown:
        raise ContractError(
            code,
            f"{path} contains unsupported fields",
            details=unknown,
        )


def require_list(value: Any, path: str, minimum: int = 0) -> list[Any]:
    if not isinstance(value, list) or len(value) < minimum:
        raise ContractError(
            "INVALID_CONTRACT",
            f"{path} must be a list with at least {minimum} item(s)",
        )
    return value


def require_string(value: Any, path: str, minimum: int = 1) -> str:
    if not isinstance(value, str) or len(value.strip()) < minimum:
        raise ContractError(
            "INVALID_CONTRACT",
            f"{path} must be a non-empty string",
        )
    return value.strip()


def require_identifier(value: Any, path: str) -> str:
    text = require_string(value, path)
    if not re.fullmatch(r"[a-z0-9][a-z0-9._-]{2,127}", text):
        raise ContractError(
            "INVALID_CONTRACT",
            f"{path} must be a lowercase stable identifier",
        )
    return text


def require_token(value: Any, path: str) -> str:
    text = require_string(value, path)
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{2,127}", text):
        raise ContractError(
            "INVALID_CONTRACT",
            f"{path} must be a stable token",
        )
    return text


def normalized_text(value: str) -> str:
    return re.sub(r"\s+", " ", value.replace("_", " ")).strip().casefold()


def normalized_claim_text(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.casefold()).strip()


def distinctive_tokens(*values: str) -> set[str]:
    return {
        token
        for value in values
        for token in re.findall(r"[a-z0-9]+", value.casefold())
        if len(token) >= 4 and token not in COMMON_ENTITY_WORDS
    }


def all_evidence_ids(
    dossier: dict[str, Any],
    campaign: dict[str, Any],
) -> dict[str, str]:
    result: dict[str, str] = {}
    for row in dossier["facts"]:
        result[row["evidence_id"]] = "paid_product"
    for row in campaign["evidence_ledger"]:
        result[row["evidence_id"]] = row["lane"]
    return result


def validate_dossier(
    dossier: dict[str, Any],
    *,
    asset_root: Path | None = None,
) -> dict[str, Any]:
    reject_unknown_keys(
        dossier,
        {
            "schema_version",
            "dossier_id",
            "version",
            "product",
            "facts",
            "prohibited_outcome_patterns",
            "competitor_material_policy",
        },
        "dossier",
        code="DOSSIER_INVALID",
    )
    observed_dossier_hash = canonical_sha256(dossier)
    if observed_dossier_hash != EXPECTED_DOSSIER_SHA256:
        raise ContractError(
            "DOSSIER_INVALID",
            "fixed Auralo dossier hash does not match its version",
            details=[
                f"expected={EXPECTED_DOSSIER_SHA256}",
                f"observed={observed_dossier_hash}",
            ],
        )
    if dossier.get("schema_version") != "1.0":
        raise ContractError("DOSSIER_INVALID", "schema_version must equal 1.0")
    if dossier.get("dossier_id") != AURALO_ID:
        raise ContractError("DOSSIER_INVALID", "dossier_id is not the fixed Auralo ID")
    if dossier.get("version") != AURALO_DOSSIER_VERSION:
        raise ContractError(
            "DOSSIER_INVALID",
            f"version must equal {AURALO_DOSSIER_VERSION}",
        )

    product = require_mapping(dossier.get("product"), "product")
    reject_unknown_keys(
        product,
        {"id", "public_name", "price_usd", "format", "reference_assets"},
        "product",
        code="DOSSIER_INVALID",
    )
    if product.get("id") != AURALO_ID:
        raise ContractError("DOSSIER_INVALID", "product.id cannot be overridden")
    if product.get("public_name") != AURALO_NAME:
        raise ContractError(
            "DOSSIER_INVALID", "product.public_name cannot be overridden"
        )
    if product.get("price_usd") != AURALO_PRICE_USD:
        raise ContractError("DOSSIER_INVALID", "product.price_usd must equal 29")

    assets = require_list(
        product.get("reference_assets"), "product.reference_assets", 1
    )
    for index, raw_asset in enumerate(assets):
        asset = require_mapping(raw_asset, f"product.reference_assets[{index}]")
        reject_unknown_keys(
            asset,
            {"asset_id", "path", "sha256"},
            f"product.reference_assets[{index}]",
            code="DOSSIER_INVALID",
        )
        require_token(asset.get("asset_id"), f"reference_assets[{index}].asset_id")
        relative_path = require_string(
            asset.get("path"),
            f"reference_assets[{index}].path",
        )
        expected_hash = require_string(
            asset.get("sha256"),
            f"reference_assets[{index}].sha256",
        )
        if not re.fullmatch(r"[0-9a-f]{64}", expected_hash):
            raise ContractError(
                "DOSSIER_INVALID",
                f"reference_assets[{index}].sha256 must be lowercase SHA-256",
            )
        if asset_root is not None:
            candidate = (asset_root / relative_path).resolve()
            if asset_root.resolve() not in candidate.parents:
                raise ContractError(
                    "DOSSIER_INVALID", "reference asset escapes asset root"
                )
            if not candidate.is_file():
                raise ContractError(
                    "DOSSIER_INVALID",
                    f"reference asset is missing: {relative_path}",
                )
            if file_sha256(candidate) != expected_hash:
                raise ContractError(
                    "DOSSIER_INVALID",
                    f"reference asset hash mismatch: {relative_path}",
                )

    facts = require_list(dossier.get("facts"), "facts", 1)
    observed_ids: set[str] = set()
    for index, raw_fact in enumerate(facts):
        fact = require_mapping(raw_fact, f"facts[{index}]")
        reject_unknown_keys(
            fact,
            {
                "evidence_id",
                "claim",
                "public_language",
                "scope",
                "status",
                "evidence_type",
                "source_url",
            },
            f"facts[{index}]",
            code="DOSSIER_INVALID",
        )
        evidence_id = require_string(
            fact.get("evidence_id"), f"facts[{index}].evidence_id"
        )
        if evidence_id in observed_ids:
            raise ContractError("DOSSIER_INVALID", f"duplicate fact: {evidence_id}")
        observed_ids.add(evidence_id)
        require_string(fact.get("claim"), f"facts[{index}].claim", 12)
        public_language = require_string(
            fact.get("public_language"),
            f"facts[{index}].public_language",
            12,
        )
        if fact.get("status") != "authorized":
            raise ContractError(
                "DOSSIER_INVALID",
                f"{evidence_id} is not authorized",
            )
        require_string(fact.get("evidence_type"), f"facts[{index}].evidence_type")
        source_url = require_string(
            fact.get("source_url"), f"facts[{index}].source_url"
        )
        if not (
            source_url.startswith("https://") or source_url.startswith("client://")
        ):
            raise ContractError(
                "DOSSIER_INVALID",
                f"{evidence_id} source_url must be https:// or client://",
            )
        for pattern in dossier.get("prohibited_outcome_patterns", []):
            if normalized_claim_text(pattern) in normalized_claim_text(public_language):
                raise ContractError(
                    "DOSSIER_INVALID",
                    f"authorized fact contains prohibited outcome: {evidence_id}",
                )

    if observed_ids != REQUIRED_AURALO_EVIDENCE_IDS:
        missing = sorted(REQUIRED_AURALO_EVIDENCE_IDS - observed_ids)
        extra = sorted(observed_ids - REQUIRED_AURALO_EVIDENCE_IDS)
        raise ContractError(
            "DOSSIER_INVALID",
            "Auralo evidence set differs from the fixed version",
            details=[f"missing={missing}", f"extra={extra}"],
        )

    prohibited = require_list(
        dossier.get("prohibited_outcome_patterns"),
        "prohibited_outcome_patterns",
        1,
    )
    for index, value in enumerate(prohibited):
        require_string(value, f"prohibited_outcome_patterns[{index}]", 4)

    return {
        "status": "accepted",
        "dossier_id": AURALO_ID,
        "version": AURALO_DOSSIER_VERSION,
        "sha256": observed_dossier_hash,
        "evidence_ids": sorted(observed_ids),
    }


def validate_campaign(
    campaign: dict[str, Any],
    dossier: dict[str, Any],
) -> dict[str, Any]:
    validate_dossier(dossier)
    forbidden_paid_keys = sorted(
        key
        for key in campaign
        if key in {"paid_product", "paid_product_facts", "paid_product_name"}
    )
    if forbidden_paid_keys:
        raise ContractError(
            "PAID_PRODUCT_OVERRIDE",
            "campaign contains paid-product override fields",
            details=forbidden_paid_keys,
        )
    reject_unknown_keys(
        campaign,
        {
            "schema_version",
            "campaign_id",
            "paid_product_contract",
            "free_product",
            "offer_terms",
            "evidence_ledger",
        },
        "campaign",
        code="CAMPAIGN_INVALID",
    )
    if campaign.get("schema_version") != "1.0":
        raise ContractError("CAMPAIGN_INVALID", "schema_version must equal 1.0")
    campaign_id = require_identifier(campaign.get("campaign_id"), "campaign_id")

    paid_contract = require_mapping(
        campaign.get("paid_product_contract"),
        "paid_product_contract",
    )
    if paid_contract != {
        "dossier_id": AURALO_ID,
        "dossier_version": AURALO_DOSSIER_VERSION,
    }:
        raise ContractError(
            "PAID_PRODUCT_OVERRIDE",
            "campaign must reference the fixed Auralo dossier without overrides",
        )
    free_product = require_mapping(campaign.get("free_product"), "free_product")
    reject_unknown_keys(
        free_product,
        {
            "id",
            "public_name",
            "category",
            "identity_terms",
            "facts",
            "reference_images",
        },
        "free_product",
        code="CAMPAIGN_INVALID",
    )
    free_id = require_identifier(free_product.get("id"), "free_product.id")
    if free_id == AURALO_ID:
        raise ContractError("CAMPAIGN_INVALID", "FREE product cannot reuse Auralo ID")
    free_name = require_string(
        free_product.get("public_name"), "free_product.public_name", 3
    )
    if normalized_text(free_name) == normalized_text(AURALO_NAME):
        raise ContractError("CAMPAIGN_INVALID", "FREE product cannot reuse Auralo name")
    require_string(free_product.get("category"), "free_product.category", 3)

    identity_terms = require_list(
        free_product.get("identity_terms"),
        "free_product.identity_terms",
        2,
    )
    normalized_terms: set[str] = set()
    for index, term in enumerate(identity_terms):
        normalized = normalized_text(
            require_string(term, f"free_product.identity_terms[{index}]", 3)
        )
        if normalized in COMMON_ENTITY_WORDS:
            raise ContractError(
                "CAMPAIGN_INVALID",
                f"identity term is too generic: {term}",
            )
        normalized_terms.add(normalized)
    if len(normalized_terms) != len(identity_terms):
        raise ContractError("CAMPAIGN_INVALID", "identity terms must be unique")

    facts = require_list(free_product.get("facts"), "free_product.facts", 2)
    free_fact_ids: set[str] = set()
    fact_language: list[str] = []
    for index, raw_fact in enumerate(facts):
        fact = require_mapping(raw_fact, f"free_product.facts[{index}]")
        reject_unknown_keys(
            fact,
            {
                "evidence_id",
                "claim",
                "public_language",
                "evidence_type",
                "source_url",
            },
            f"free_product.facts[{index}]",
            code="CAMPAIGN_INVALID",
        )
        evidence_id = require_string(
            fact.get("evidence_id"),
            f"free_product.facts[{index}].evidence_id",
        )
        if evidence_id in free_fact_ids or evidence_id in REQUIRED_AURALO_EVIDENCE_IDS:
            raise ContractError(
                "CAMPAIGN_INVALID", f"duplicate evidence ID: {evidence_id}"
            )
        free_fact_ids.add(evidence_id)
        fact_language.append(
            require_string(
                fact.get("claim"),
                f"free_product.facts[{index}].claim",
                10,
            )
        )
        fact_language.append(
            require_string(
                fact.get("public_language"),
                f"free_product.facts[{index}].public_language",
                10,
            )
        )
        require_string(
            fact.get("evidence_type"),
            f"free_product.facts[{index}].evidence_type",
        )
        source_url = require_string(
            fact.get("source_url"),
            f"free_product.facts[{index}].source_url",
        )
        if not (
            source_url.startswith("https://") or source_url.startswith("client://")
        ):
            raise ContractError(
                "CAMPAIGN_INVALID",
                f"free_product.facts[{index}].source_url must be https:// or client://",
            )

    identity_vocabulary = distinctive_tokens(
        free_name,
        *(str(term) for term in identity_terms),
    )
    fact_vocabulary = distinctive_tokens(*fact_language)
    if len(identity_vocabulary & fact_vocabulary) < 2:
        raise ContractError(
            "CAMPAIGN_INVALID",
            "FREE-product facts do not materialize the current product identity",
            details=sorted(identity_vocabulary - fact_vocabulary)[:8],
        )

    images = require_list(
        free_product.get("reference_images"),
        "free_product.reference_images",
        1,
    )
    for index, raw_image in enumerate(images):
        image = require_mapping(raw_image, f"free_product.reference_images[{index}]")
        reject_unknown_keys(
            image,
            {"asset_id", "path", "sha256"},
            f"free_product.reference_images[{index}]",
            code="CAMPAIGN_INVALID",
        )
        require_token(
            image.get("asset_id"),
            f"free_product.reference_images[{index}].asset_id",
        )
        require_string(
            image.get("path"),
            f"free_product.reference_images[{index}].path",
        )
        sha256 = require_string(
            image.get("sha256"),
            f"free_product.reference_images[{index}].sha256",
        )
        if not re.fullmatch(r"[0-9a-f]{64}", sha256):
            raise ContractError(
                "CAMPAIGN_INVALID",
                f"free_product.reference_images[{index}].sha256 is invalid",
            )

    offer_terms = require_mapping(campaign.get("offer_terms"), "offer_terms")
    reject_unknown_keys(
        offer_terms,
        {"paid_price_usd", "free_price_usd", "free_public_label"},
        "offer_terms",
        code="CAMPAIGN_INVALID",
    )
    if offer_terms.get("paid_price_usd") != AURALO_PRICE_USD:
        raise ContractError("CAMPAIGN_INVALID", "paid_price_usd must equal 29")
    if offer_terms.get("free_price_usd") != 0:
        raise ContractError("CAMPAIGN_INVALID", "free_price_usd must equal 0")
    if offer_terms.get("free_public_label") != "FREE":
        raise ContractError("CAMPAIGN_INVALID", "free_public_label must equal FREE")

    evidence_ledger = require_list(
        campaign.get("evidence_ledger"),
        "evidence_ledger",
        len(free_fact_ids),
    )
    observed_ledger_ids: set[str] = set()
    ledger_lanes: dict[str, str] = {}
    for index, raw_row in enumerate(evidence_ledger):
        row = require_mapping(raw_row, f"evidence_ledger[{index}]")
        reject_unknown_keys(
            row,
            {"evidence_id", "lane", "excerpt", "source_url"},
            f"evidence_ledger[{index}]",
            code="CAMPAIGN_INVALID",
        )
        evidence_id = require_string(
            row.get("evidence_id"),
            f"evidence_ledger[{index}].evidence_id",
        )
        if (
            evidence_id in observed_ledger_ids
            or evidence_id in REQUIRED_AURALO_EVIDENCE_IDS
        ):
            raise ContractError(
                "CAMPAIGN_INVALID",
                f"duplicate evidence ledger ID: {evidence_id}",
            )
        observed_ledger_ids.add(evidence_id)
        if row.get("lane") not in {"free_product", "relationship"}:
            raise ContractError(
                "CAMPAIGN_INVALID",
                f"evidence_ledger[{index}].lane must be free_product or relationship",
            )
        ledger_lanes[evidence_id] = row["lane"]
        require_string(row.get("excerpt"), f"evidence_ledger[{index}].excerpt", 8)
        source_url = require_string(
            row.get("source_url"),
            f"evidence_ledger[{index}].source_url",
        )
        if not (
            source_url.startswith("https://") or source_url.startswith("client://")
        ):
            raise ContractError(
                "CAMPAIGN_INVALID",
                f"evidence_ledger[{index}].source_url must be https:// or client://",
            )

    missing_fact_rows = sorted(free_fact_ids - observed_ledger_ids)
    if missing_fact_rows:
        raise ContractError(
            "CAMPAIGN_INVALID",
            "FREE-product facts are missing from current evidence ledger",
            details=missing_fact_rows,
        )
    wrong_fact_lanes = sorted(
        evidence_id
        for evidence_id in free_fact_ids
        if ledger_lanes.get(evidence_id) != "free_product"
    )
    if wrong_fact_lanes:
        raise ContractError(
            "CAMPAIGN_INVALID",
            "FREE-product facts must remain in the free_product evidence lane",
            details=wrong_fact_lanes,
        )

    return {
        "status": "accepted",
        "campaign_id": campaign_id,
        "free_product_id": free_id,
        "free_product_name": free_name,
        "sha256": canonical_sha256(campaign),
        "free_evidence_ids": sorted(free_fact_ids),
    }


def _angle(
    raw: Any,
    path: str,
) -> dict[str, str]:
    angle = require_mapping(raw, path)
    reject_unknown_keys(angle, {"id", "hook", "buyer_action"}, path)
    return {
        "id": require_identifier(angle.get("id"), f"{path}.id"),
        "hook": require_string(angle.get("hook"), f"{path}.hook", 12),
        "buyer_action": require_string(
            angle.get("buyer_action"),
            f"{path}.buyer_action",
            12,
        ),
    }


def _assert_no_internal_strategy(text: str, path: str) -> None:
    for label, pattern in INTERNAL_STRATEGY_PATTERNS:
        match = pattern.search(text)
        if match:
            raise ContractError(
                "CROSS_CAMPAIGN_LEAK",
                f"{path} contains {label}",
                details=[match.group(0)],
            )


def validate_marriage_brief(
    brief: dict[str, Any],
    campaign: dict[str, Any],
    dossier: dict[str, Any],
) -> dict[str, Any]:
    validate_campaign(campaign, dossier)
    reject_unknown_keys(
        brief,
        {
            "schema_version",
            "status",
            "campaign_id",
            "paid_product_id",
            "free_product_id",
            "relationship_mode",
            "repair_cycles",
            "primary_angle",
            "backup_angle",
            "buyer_moment",
            "transaction_bridge",
            "product_roles",
            "substitution_test",
            "evidence_ids",
            "relationship_evidence_ids",
            "scorecard",
            "falsification_plan",
        },
        "marriage_brief",
    )
    if brief.get("schema_version") != "1.0":
        raise ContractError("INVALID_CONTRACT", "brief schema_version must equal 1.0")
    repairs = brief.get("repair_cycles")
    if not isinstance(repairs, int) or repairs < 0:
        raise ContractError("ANGLE_GAP", "repair_cycles must be a non-negative integer")
    if repairs > MAX_ANGLE_REPAIR_CYCLES:
        raise ContractError(
            "ANGLE_GAP",
            f"angle repair limit exceeded: {repairs}>{MAX_ANGLE_REPAIR_CYCLES}",
        )
    if brief.get("status") != "accepted":
        raise ContractError("ANGLE_GAP", "marriage brief is not accepted")
    if brief.get("campaign_id") != campaign["campaign_id"]:
        raise ContractError("MARRIAGE_GAP", "marriage brief campaign_id mismatch")
    if brief.get("paid_product_id") != AURALO_ID:
        raise ContractError("MARRIAGE_GAP", "marriage brief paid product mismatch")
    free_product = campaign["free_product"]
    if brief.get("free_product_id") != free_product["id"]:
        raise ContractError("MARRIAGE_GAP", "marriage brief FREE product mismatch")

    mode = brief.get("relationship_mode")
    if mode not in RELATIONSHIP_MODES:
        raise ContractError(
            "MARRIAGE_GAP",
            "relationship_mode must be wanted_premium or evidence_backed_complement",
        )

    try:
        primary = _angle(brief.get("primary_angle"), "primary_angle")
        backup = _angle(brief.get("backup_angle"), "backup_angle")
    except ContractError as error:
        raise ContractError(
            "ANGLE_GAP",
            "marriage brief is missing a complete primary or backup angle",
            details=[error.message],
        ) from error
    if primary["id"] == backup["id"]:
        raise ContractError("ANGLE_GAP", "primary and backup angles must be distinct")
    if normalized_text(primary["hook"]) == normalized_text(backup["hook"]):
        raise ContractError("ANGLE_GAP", "backup angle cannot be a wording variant")
    _assert_no_internal_strategy(primary["hook"], "primary_angle.hook")
    _assert_no_internal_strategy(backup["hook"], "backup_angle.hook")

    require_string(brief.get("buyer_moment"), "buyer_moment", 16)
    bridge = require_string(
        brief.get("transaction_bridge"),
        "transaction_bridge",
        24,
    )
    if normalized_text(AURALO_NAME) not in normalized_text(bridge):
        raise ContractError(
            "MARRIAGE_GAP",
            "transaction_bridge must materialize Auralo by exact name",
        )
    if normalized_text(free_product["public_name"]) not in normalized_text(bridge):
        raise ContractError(
            "MARRIAGE_GAP",
            "transaction_bridge must materialize the current FREE product by exact name",
        )

    roles = require_mapping(brief.get("product_roles"), "product_roles")
    reject_unknown_keys(roles, {"paid", "free"}, "product_roles")
    paid_role = require_string(roles.get("paid"), "product_roles.paid", 16)
    free_role = require_string(roles.get("free"), "product_roles.free", 16)
    if normalized_text(AURALO_NAME) not in normalized_text(paid_role):
        raise ContractError("MARRIAGE_GAP", "paid role must name Auralo")
    if normalized_text(free_product["public_name"]) not in normalized_text(free_role):
        raise ContractError("MARRIAGE_GAP", "FREE role must name the current product")
    if normalized_text(paid_role) == normalized_text(free_role):
        raise ContractError("MARRIAGE_GAP", "product roles must be distinct")

    evidence_map = all_evidence_ids(dossier, campaign)
    evidence_ids = require_list(brief.get("evidence_ids"), "evidence_ids", 2)
    unknown = sorted(
        evidence_id
        for evidence_id in evidence_ids
        if not isinstance(evidence_id, str) or evidence_id not in evidence_map
    )
    if unknown:
        raise ContractError(
            "MARRIAGE_GAP",
            "marriage brief cites unknown or stale evidence",
            details=unknown,
        )
    cited_lanes = {evidence_map[evidence_id] for evidence_id in evidence_ids}
    if "paid_product" not in cited_lanes or "free_product" not in cited_lanes:
        raise ContractError(
            "MARRIAGE_GAP",
            "marriage brief needs current paid and FREE product evidence",
        )

    relationship_ids = require_list(
        brief.get("relationship_evidence_ids"),
        "relationship_evidence_ids",
        0,
    )
    invalid_relationship_ids = sorted(
        evidence_id
        for evidence_id in relationship_ids
        if evidence_map.get(evidence_id) != "relationship"
    )
    if invalid_relationship_ids:
        raise ContractError(
            "MARRIAGE_GAP",
            "relationship evidence IDs are invalid",
            details=invalid_relationship_ids,
        )
    if mode == "evidence_backed_complement" and len(set(relationship_ids)) < 2:
        raise ContractError(
            "MARRIAGE_GAP",
            "complement mode requires at least two current relationship evidence IDs",
        )

    substitution = require_mapping(
        brief.get("substitution_test"),
        "substitution_test",
    )
    reject_unknown_keys(
        substitution,
        {"question", "result", "evidence_ids"},
        "substitution_test",
    )
    require_string(substitution.get("question"), "substitution_test.question", 16)
    if substitution.get("result") != "passed":
        raise ContractError("MARRIAGE_GAP", "substitution test did not pass")
    substitution_evidence = require_list(
        substitution.get("evidence_ids"),
        "substitution_test.evidence_ids",
        1,
    )
    if any(evidence_id not in evidence_ids for evidence_id in substitution_evidence):
        raise ContractError(
            "MARRIAGE_GAP",
            "substitution test cites evidence outside the accepted brief",
        )

    return {
        "status": "accepted",
        "campaign_id": campaign["campaign_id"],
        "relationship_mode": mode,
        "primary_angle_id": primary["id"],
        "backup_angle_id": backup["id"],
        "repair_cycles": repairs,
        "sha256": canonical_sha256(brief),
    }


def _entity_terms(free_product: dict[str, Any]) -> set[str]:
    terms = {normalized_text(value) for value in free_product["identity_terms"]}
    full_name = normalized_text(free_product["public_name"])
    if full_name not in COMMON_ENTITY_WORDS:
        terms.add(full_name)
    return terms


def build_prior_entity_registry(
    current_campaign: dict[str, Any],
    prior_campaigns: Iterable[dict[str, Any]],
    dossier: dict[str, Any],
) -> dict[str, Any]:
    validate_campaign(current_campaign, dossier)
    current_terms = _entity_terms(current_campaign["free_product"])
    forbidden: set[str] = set()
    sources: list[dict[str, str]] = []
    for prior in prior_campaigns:
        validate_campaign(prior, dossier)
        if prior["campaign_id"] == current_campaign["campaign_id"]:
            continue
        prior_terms = _entity_terms(prior["free_product"])
        forbidden.update(term for term in prior_terms if term not in current_terms)
        sources.append(
            {
                "campaign_id": prior["campaign_id"],
                "campaign_sha256": canonical_sha256(prior),
            }
        )
    return {
        "schema_version": "1.0",
        "purpose": "validator_only_do_not_send_to_writer",
        "current_campaign_id": current_campaign["campaign_id"],
        "forbidden_entities": sorted(forbidden),
        "source_campaigns": sorted(sources, key=lambda row: row["campaign_id"]),
    }


def validate_registry(
    registry: dict[str, Any],
    campaign: dict[str, Any],
) -> list[str]:
    reject_unknown_keys(
        registry,
        {
            "schema_version",
            "purpose",
            "current_campaign_id",
            "forbidden_entities",
            "source_campaigns",
        },
        "registry",
        code="REGISTRY_INVALID",
    )
    if registry.get("schema_version") != "1.0":
        raise ContractError(
            "REGISTRY_INVALID", "registry schema_version must equal 1.0"
        )
    if registry.get("purpose") != "validator_only_do_not_send_to_writer":
        raise ContractError(
            "REGISTRY_INVALID", "registry purpose is not validator-only"
        )
    if registry.get("current_campaign_id") != campaign["campaign_id"]:
        raise ContractError("REGISTRY_INVALID", "registry campaign mismatch")
    forbidden = require_list(
        registry.get("forbidden_entities"), "forbidden_entities", 0
    )
    result: list[str] = []
    for index, value in enumerate(forbidden):
        normalized = normalized_text(
            require_string(value, f"forbidden_entities[{index}]", 3)
        )
        if normalized not in result:
            result.append(normalized)
    return result


def _content_strings(
    node: Any,
    path: tuple[str, ...] = (),
    mode: str | None = None,
) -> Iterator[tuple[str, str, str]]:
    if isinstance(node, dict):
        for key, value in node.items():
            child_mode = mode
            if key in PUBLIC_ROOT_KEYS:
                child_mode = "public"
            elif key in DIRECTION_ROOT_KEYS:
                child_mode = "direction"
            yield from _content_strings(value, path + (str(key),), child_mode)
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from _content_strings(value, path + (str(index),), mode)
    elif isinstance(node, str) and mode is not None:
        yield (".".join(path), mode, node)


def _contains_entity(text: str, entity: str) -> bool:
    normalized = normalized_text(text)
    if " " in entity:
        return entity in normalized
    return bool(re.search(rf"\b{re.escape(entity)}\b", normalized))


def _validate_claims(
    payload: dict[str, Any],
    campaign: dict[str, Any],
    dossier: dict[str, Any],
) -> None:
    claims = require_list(payload.get("claims"), "claims", 1)
    evidence_map = all_evidence_ids(dossier, campaign)
    prohibited = [
        normalized_claim_text(value) for value in dossier["prohibited_outcome_patterns"]
    ]
    for index, raw_claim in enumerate(claims):
        claim = require_mapping(raw_claim, f"claims[{index}]")
        reject_unknown_keys(
            claim,
            {"text", "evidence_ids"},
            f"claims[{index}]",
            code="PUBLIC_PAYLOAD_INVALID",
        )
        text = require_string(claim.get("text"), f"claims[{index}].text", 8)
        normalized = normalized_claim_text(text)
        matches = [
            pattern for pattern in prohibited if pattern and pattern in normalized
        ]
        if matches:
            raise ContractError(
                "CLAIM_NOT_AUTHORIZED",
                "question marks, asterisks, and disclaimers do not authorize this claim",
                details=[text],
            )
        for label, pattern in UNSUPPORTED_OUTCOME_PATTERNS:
            if pattern.search(text):
                raise ContractError(
                    "CLAIM_NOT_AUTHORIZED",
                    f"claim contains unsupported {label}",
                    details=[text],
                )
        evidence_ids = require_list(
            claim.get("evidence_ids"),
            f"claims[{index}].evidence_ids",
            1,
        )
        unknown = sorted(
            evidence_id
            for evidence_id in evidence_ids
            if not isinstance(evidence_id, str) or evidence_id not in evidence_map
        )
        if unknown:
            raise ContractError(
                "CLAIM_NOT_AUTHORIZED",
                f"claims[{index}] cites unknown evidence",
                details=unknown,
            )


def _validate_image_jobs(
    payload: dict[str, Any],
    brief_result: dict[str, Any],
    campaign: dict[str, Any],
    dossier: dict[str, Any],
) -> None:
    jobs = require_list(payload.get("image_jobs"), "image_jobs", 1)
    allowed_angles = {
        brief_result["primary_angle_id"],
        brief_result["backup_angle_id"],
    }
    observed_presence: set[str] = set()
    observed_ids: set[str] = set()
    evidence_map = all_evidence_ids(dossier, campaign)
    for index, raw_job in enumerate(jobs):
        job = require_mapping(raw_job, f"image_jobs[{index}]")
        reject_unknown_keys(
            job,
            {
                "id",
                "angle_id",
                "product_presence",
                "production_direction",
                "visible_text",
                "evidence_ids",
            },
            f"image_jobs[{index}]",
            code="PUBLIC_PAYLOAD_INVALID",
        )
        job_id = require_string(job.get("id"), f"image_jobs[{index}].id")
        if job_id in observed_ids:
            raise ContractError(
                "PUBLIC_PAYLOAD_INVALID", f"duplicate image job: {job_id}"
            )
        observed_ids.add(job_id)
        if job.get("angle_id") not in allowed_angles:
            raise ContractError(
                "ANGLE_NOT_BOUND",
                f"{job_id} is not bound to the accepted primary or backup angle",
            )
        presence = job.get("product_presence")
        if presence not in {"paid", "free", "both"}:
            raise ContractError(
                "PUBLIC_PAYLOAD_INVALID",
                f"{job_id}.product_presence must be paid, free, or both",
            )
        observed_presence.add(presence)
        evidence_ids = require_list(
            job.get("evidence_ids"),
            f"image_jobs[{index}].evidence_ids",
            1,
        )
        unknown_evidence = sorted(
            evidence_id
            for evidence_id in evidence_ids
            if not isinstance(evidence_id, str) or evidence_id not in evidence_map
        )
        if unknown_evidence:
            raise ContractError(
                "PUBLIC_PAYLOAD_INVALID",
                f"{job_id} cites unknown or stale evidence",
                details=unknown_evidence,
            )
        cited_lanes = {evidence_map[evidence_id] for evidence_id in evidence_ids}
        required_lanes = {
            "paid": {"paid_product"},
            "free": {"free_product"},
            "both": {"paid_product", "free_product"},
        }[presence]
        if not required_lanes.issubset(cited_lanes):
            raise ContractError(
                "MARRIAGE_GAP",
                f"{job_id} evidence does not support its declared product presence",
                details=sorted(required_lanes - cited_lanes),
            )
        if (
            presence == "both"
            and brief_result["relationship_mode"] == "evidence_backed_complement"
            and "relationship" not in cited_lanes
        ):
            raise ContractError(
                "MARRIAGE_GAP",
                f"{job_id} complement scene lacks current relationship evidence",
            )
        require_string(
            job.get("production_direction"),
            f"image_jobs[{index}].production_direction",
            16,
        )
        visible_text = job.get("visible_text")
        if isinstance(visible_text, str):
            require_string(visible_text, f"image_jobs[{index}].visible_text", 2)
        else:
            values = require_list(
                visible_text,
                f"image_jobs[{index}].visible_text",
                1,
            )
            for text_index, value in enumerate(values):
                require_string(
                    value,
                    f"image_jobs[{index}].visible_text[{text_index}]",
                    2,
                )
    missing_presence = {"paid", "free", "both"} - observed_presence
    if missing_presence:
        raise ContractError(
            "MARRIAGE_GAP",
            "image jobs do not materialize both independent products and a joint buyer moment",
            details=sorted(missing_presence),
        )


def validate_public_payload(
    payload: dict[str, Any],
    campaign: dict[str, Any],
    brief: dict[str, Any],
    dossier: dict[str, Any],
    registry: dict[str, Any],
) -> dict[str, Any]:
    reject_unknown_keys(
        payload,
        {
            "campaign_id",
            "marriage_brief_sha256",
            "copy",
            "claims",
            "image_jobs",
            "site_data",
        },
        "public_payload",
        code="PUBLIC_PAYLOAD_INVALID",
    )
    campaign_result = validate_campaign(campaign, dossier)
    brief_result = validate_marriage_brief(brief, campaign, dossier)
    forbidden_entities = validate_registry(registry, campaign)

    if payload.get("campaign_id") != campaign["campaign_id"]:
        raise ContractError("PUBLIC_PAYLOAD_INVALID", "payload campaign_id mismatch")
    if payload.get("marriage_brief_sha256") != brief_result["sha256"]:
        raise ContractError(
            "ANGLE_NOT_BOUND",
            "payload is not hash-bound to the accepted marriage brief",
        )

    content_rows = list(_content_strings(payload))
    if not content_rows:
        raise ContractError(
            "PUBLIC_PAYLOAD_INVALID",
            "payload contains no customer-facing or prompt content",
        )

    stale_hits: list[str] = []
    for path, mode, text in content_rows:
        for label, pattern in INTERNAL_STRATEGY_PATTERNS:
            match = pattern.search(text)
            if match:
                stale_hits.append(f"{path}: {label}: {match.group(0)}")
        for entity in forbidden_entities:
            if _contains_entity(text, entity):
                stale_hits.append(f"{path}: prior entity: {entity}")
        if mode == "public":
            for label, pattern in GENERIC_PUBLIC_PRODUCT_PATTERNS:
                match = pattern.search(text)
                if match:
                    stale_hits.append(f"{path}: {label}: {match.group(0)}")
            for label, pattern in VISIBLE_PRODUCTION_PATTERNS:
                match = pattern.search(text)
                if match:
                    stale_hits.append(f"{path}: {label}: {match.group(0)}")
    if stale_hits:
        raise ContractError(
            "CROSS_CAMPAIGN_LEAK",
            "customer/prompt content contains private, generic, production, or stale-product language",
            details=sorted(set(stale_hits)),
        )

    public_text = " ".join(text for _, mode, text in content_rows if mode == "public")
    if normalized_text(AURALO_NAME) not in normalized_text(public_text):
        raise ContractError(
            "MARRIAGE_GAP",
            "public content never materializes Auralo by exact name",
        )
    free_name = campaign_result["free_product_name"]
    if normalized_text(free_name) not in normalized_text(public_text):
        raise ContractError(
            "MARRIAGE_GAP",
            "public content never materializes the current FREE product by exact name",
        )

    for pattern in dossier["prohibited_outcome_patterns"]:
        if normalized_claim_text(pattern) in normalized_claim_text(public_text):
            raise ContractError(
                "CLAIM_NOT_AUTHORIZED",
                "public content contains a prohibited Auralo outcome",
                details=[pattern],
            )
    for label, pattern in UNSUPPORTED_OUTCOME_PATTERNS:
        match = pattern.search(public_text)
        if match:
            raise ContractError(
                "CLAIM_NOT_AUTHORIZED",
                f"public content contains unsupported {label}",
                details=[match.group(0)],
            )

    _validate_claims(payload, campaign, dossier)
    _validate_image_jobs(payload, brief_result, campaign, dossier)

    return {
        "status": "accepted",
        "campaign_id": campaign["campaign_id"],
        "marriage_brief_sha256": brief_result["sha256"],
        "payload_sha256": canonical_sha256(payload),
        "content_string_count": len(content_rows),
        "image_job_count": len(payload["image_jobs"]),
        "prior_entity_count": len(forbidden_entities),
    }


def _write_or_print(payload: dict[str, Any], output: Path | None) -> None:
    rendered = json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    if output is None:
        print(rendered, end="")
        return
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(rendered, encoding="utf-8")
    print(output)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dossier",
        type=Path,
        default=DEFAULT_DOSSIER_PATH,
        help="Fixed Auralo dossier path",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("validate-dossier")

    campaign = subparsers.add_parser("validate-campaign")
    campaign.add_argument("--campaign", type=Path, required=True)

    brief = subparsers.add_parser("validate-brief")
    brief.add_argument("--campaign", type=Path, required=True)
    brief.add_argument("--brief", type=Path, required=True)

    registry = subparsers.add_parser("build-registry")
    registry.add_argument("--campaign", type=Path, required=True)
    registry.add_argument("--prior", type=Path, action="append", default=[])
    registry.add_argument("--output", type=Path)

    public = subparsers.add_parser("validate-public")
    public.add_argument("--campaign", type=Path, required=True)
    public.add_argument("--brief", type=Path, required=True)
    public.add_argument("--registry", type=Path, required=True)
    public.add_argument("--payload", type=Path, required=True)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        dossier = load_json(args.dossier)
        asset_root = args.dossier.parent
        if args.command == "validate-dossier":
            result = validate_dossier(dossier, asset_root=asset_root)
        elif args.command == "validate-campaign":
            result = validate_campaign(load_json(args.campaign), dossier)
        elif args.command == "validate-brief":
            result = validate_marriage_brief(
                load_json(args.brief),
                load_json(args.campaign),
                dossier,
            )
        elif args.command == "build-registry":
            current = load_json(args.campaign)
            result = build_prior_entity_registry(
                current,
                (load_json(path) for path in args.prior),
                dossier,
            )
            _write_or_print(result, args.output)
            return 0
        elif args.command == "validate-public":
            result = validate_public_payload(
                load_json(args.payload),
                load_json(args.campaign),
                load_json(args.brief),
                dossier,
                load_json(args.registry),
            )
        else:  # pragma: no cover - argparse enforces the command set
            parser.error(f"unsupported command: {args.command}")
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0
    except ContractError as error:
        print(
            json.dumps(error.as_dict(), indent=2, ensure_ascii=False), file=sys.stderr
        )
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
