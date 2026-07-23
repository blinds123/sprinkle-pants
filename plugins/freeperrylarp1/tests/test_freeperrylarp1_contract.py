from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = (
    PLUGIN_ROOT / "skills" / "freeperrylarp1" / "scripts" / "freeperrylarp1_contract.py"
)
DOSSIER_PATH = (
    PLUGIN_ROOT / "skills" / "freeperrylarp1" / "assets" / "auralo-dossier.json"
)
CAMPAIGN_PATH = PLUGIN_ROOT / "tests" / "fixtures" / "star-burst-campaign.json"
SECOND_CAMPAIGN_PATH = PLUGIN_ROOT / "tests" / "fixtures" / "travel-case-campaign.json"
ASSET_ROOT = CAMPAIGN_PATH.parent

SPEC = importlib.util.spec_from_file_location("freeperrylarp1_contract", CONTRACT_PATH)
assert SPEC and SPEC.loader
contract = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(contract)


class ContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.dossier = json.loads(DOSSIER_PATH.read_text(encoding="utf-8"))
        self.campaign = json.loads(CAMPAIGN_PATH.read_text(encoding="utf-8"))
        self.second_campaign = json.loads(
            SECOND_CAMPAIGN_PATH.read_text(encoding="utf-8")
        )

    def brief(
        self,
        *,
        mode: str = "wanted_premium",
        repair_cycles: int = 0,
    ) -> dict:
        relationship_ids = (
            ["R-REL-001", "R-REL-002"] if mode == "evidence_backed_complement" else []
        )
        evidence_ids = [
            "AURALO-IDENTITY-001",
            "AURALO-SCENT-001",
            "FREE-IDENTITY-001",
            "FREE-FORM-001",
        ]
        research_evidence_ids = [
            "R-PAID-VOICE-001",
            "R-FREE-VOICE-001",
            "R-OBJECTION-001",
            *relationship_ids,
        ]
        return {
            "schema_version": "2.0",
            "status": "accepted",
            "campaign_id": self.campaign["campaign_id"],
            "paid_product_id": contract.AURALO_ID,
            "free_product_id": self.campaign["free_product"]["id"],
            "relationship_mode": mode,
            "repair_cycles": repair_cycles,
            "research_snapshot_sha256": "1" * 64,
            "candidate_set_sha256": "2" * 64,
            "critic_receipt_sha256": "3" * 64,
            "writer_packet_sha256": "4" * 64,
            "generator_session_ids": [
                "generator-session-1",
                "generator-session-2",
                "generator-session-3",
                "generator-session-4",
            ],
            "critic_session_id": "independent-critic-session",
            "primary_angle": {
                "id": "signature-before-words",
                "hook": "What if your signature arrived before you said a word?",
                "buyer_action": "Apply the scent, fasten the necklace, and step into the evening.",
            },
            "backup_angle": {
                "id": "finish-worth-remembering",
                "hook": "A $29 scent with a star-bright finish included.",
                "buyer_action": "Choose the floral-amber scent and wear the starburst at your collarbone.",
            },
            "sales_argument": (
                "Make Auralo worth choosing for its evidenced scent and compact format, "
                "then make the Star Burst Necklace independently desirable before "
                "stating the clear $29 and FREE transaction."
            ),
            "buyer_moment": "She is choosing the last details before leaving for an evening out.",
            "buyer_bridge": {
                "shared_avatar": (
                    "A style-led self-purchaser preparing for an evening out."
                ),
                "occasion_or_desire": (
                    "She wants separate scent and jewellery finishing choices "
                    "before an evening out."
                ),
                "reason_to_act": (
                    "The $29 scent purchase adds the wanted visible necklace "
                    "choice before the evening."
                ),
                "evidence_ids": [
                    "R-PAID-VOICE-001",
                    "R-FREE-VOICE-001",
                    "R-OBJECTION-001",
                ],
            },
            "transaction_bridge": (
                "Choose Auralo Pheromone Perfume for $29 and receive the "
                "Star Burst Necklace FREE as separate scent and jewellery "
                "finishing choices before an evening out."
            ),
            "product_roles": {
                "paid": "Auralo Pheromone Perfume is the $29 floral-amber scent she chooses.",
                "free": "Star Burst Necklace is the wanted visible piece included FREE.",
            },
            "substitution_test": {
                "question": (
                    "If either product is replaced, does the evidence-backed "
                    "buyer reason materially change?"
                ),
                "result": "passed",
                "reason": (
                    "Replacing Auralo Pheromone Perfume or the Star Burst Necklace "
                    "removes the separate scent and jewellery finishing choices "
                    "before an evening out."
                ),
                "evidence_ids": [
                    "AURALO-IDENTITY-001",
                    "FREE-IDENTITY-001",
                    "R-PAID-VOICE-001",
                ],
            },
            "evidence_ids": evidence_ids,
            "research_evidence_ids": research_evidence_ids,
            "customer_language_evidence_ids": [
                "R-PAID-VOICE-001",
                "R-FREE-VOICE-001",
            ],
            "relationship_evidence_ids": relationship_ids,
            "relationship_source_family_count": 2 if relationship_ids else 0,
        }

    def registry(self, prior_campaigns: list[dict] | None = None) -> dict:
        return contract.build_prior_entity_registry(
            self.campaign,
            prior_campaigns or [],
            self.dossier,
            asset_root=ASSET_ROOT,
        )

    def payload(
        self,
        brief: dict | None = None,
        registry: dict | None = None,
    ) -> dict:
        accepted_brief = brief or self.brief()
        payload = {
            "campaign_id": self.campaign["campaign_id"],
            "marriage_brief_sha256": contract.canonical_sha256(accepted_brief),
            "copy": {
                "headline": (
                    "Scent and jewellery: separate finishing choices before "
                    "an evening out."
                ),
                "subheadline": (
                    "Get Auralo Pheromone Perfume for $29 and receive the "
                    "Star Burst Necklace FREE."
                ),
                "body": (
                    "Auralo Pheromone Perfume brings a floral-amber scent in a "
                    "15 ml bottle. The Star Burst Necklace adds a radiating "
                    "pendant on a gold-tone chain."
                ),
                "cta": "Choose Auralo for $29",
                "footer": (
                    "Promotional lifestyle scenes are creative representations. "
                    "Product details and purchase terms appear on this mock page."
                ),
            },
            "claims": [
                {
                    "claim_id": "CLAIM-001",
                    "public_path": "copy.headline",
                    "scope": "relationship",
                    "text": (
                        "Scent and jewellery: separate finishing choices before "
                        "an evening out."
                    ),
                    "evidence_ids": [
                        "AURALO-SCENT-001",
                        "FREE-IDENTITY-001",
                        "REL-001",
                    ],
                    "evidence_bindings": [
                        {
                            "evidence_id": "AURALO-SCENT-001",
                            "fragments": ["Scent"],
                        },
                        {
                            "evidence_id": "FREE-IDENTITY-001",
                            "fragments": ["jewellery"],
                        },
                        {
                            "evidence_id": "REL-001",
                            "fragments": [
                                "separate finishing choices",
                                "before an evening out",
                            ],
                        },
                    ],
                },
                {
                    "claim_id": "CLAIM-002",
                    "public_path": "copy.subheadline",
                    "scope": "offer",
                    "text": (
                        "Get Auralo Pheromone Perfume for $29 and receive the "
                        "Star Burst Necklace FREE."
                    ),
                    "evidence_ids": [
                        "AURALO-PRICE-001",
                        "FREE-IDENTITY-001",
                    ],
                    "evidence_bindings": [
                        {
                            "evidence_id": "AURALO-PRICE-001",
                            "fragments": [
                                "Auralo Pheromone Perfume",
                                "$29",
                            ],
                        },
                        {
                            "evidence_id": "FREE-IDENTITY-001",
                            "fragments": ["Star Burst Necklace"],
                        },
                    ],
                },
                {
                    "claim_id": "CLAIM-003",
                    "public_path": "copy.body",
                    "scope": "multi_product_fact",
                    "text": (
                        "Auralo Pheromone Perfume brings a floral-amber scent in a "
                        "15 ml bottle. The Star Burst Necklace adds a radiating "
                        "pendant on a gold-tone chain."
                    ),
                    "evidence_ids": [
                        "AURALO-IDENTITY-001",
                        "AURALO-SCENT-001",
                        "FREE-IDENTITY-001",
                        "FREE-FORM-001",
                    ],
                    "evidence_bindings": [
                        {
                            "evidence_id": "AURALO-IDENTITY-001",
                            "fragments": [
                                "Auralo Pheromone Perfume",
                                "15 ml",
                                "bottle",
                            ],
                        },
                        {
                            "evidence_id": "AURALO-SCENT-001",
                            "fragments": ["floral-amber scent"],
                        },
                        {
                            "evidence_id": "FREE-IDENTITY-001",
                            "fragments": [
                                "Star Burst Necklace",
                                "radiating pendant",
                            ],
                        },
                        {
                            "evidence_id": "FREE-FORM-001",
                            "fragments": ["gold-tone chain"],
                        },
                    ],
                },
                {
                    "claim_id": "CLAIM-004",
                    "public_path": "copy.cta",
                    "scope": "paid_fact",
                    "text": "Choose Auralo for $29",
                    "evidence_ids": ["AURALO-PRICE-001"],
                    "evidence_bindings": [
                        {
                            "evidence_id": "AURALO-PRICE-001",
                            "fragments": ["Auralo", "$29"],
                        }
                    ],
                },
                {
                    "claim_id": "CLAIM-005",
                    "public_path": "copy.footer",
                    "scope": "disclosure",
                    "text": (
                        "Promotional lifestyle scenes are creative representations. "
                        "Product details and purchase terms appear on this mock page."
                    ),
                    "evidence_ids": [],
                    "evidence_bindings": [],
                },
                {
                    "claim_id": "CLAIM-006",
                    "public_path": "image_jobs.0.visible_text",
                    "scope": "paid_fact",
                    "text": "Meet Auralo Pheromone Perfume",
                    "evidence_ids": ["AURALO-IDENTITY-001"],
                    "evidence_bindings": [
                        {
                            "evidence_id": "AURALO-IDENTITY-001",
                            "fragments": ["Auralo Pheromone Perfume"],
                        }
                    ],
                },
                {
                    "claim_id": "CLAIM-007",
                    "public_path": "image_jobs.1.visible_text",
                    "scope": "free_fact",
                    "text": "Your Star Burst Necklace is FREE",
                    "evidence_ids": ["FREE-IDENTITY-001"],
                    "evidence_bindings": [
                        {
                            "evidence_id": "FREE-IDENTITY-001",
                            "fragments": ["Star Burst Necklace"],
                        }
                    ],
                },
                {
                    "claim_id": "CLAIM-008",
                    "public_path": "image_jobs.2.visible_text.0",
                    "scope": "paid_fact",
                    "text": "Auralo Pheromone Perfume — $29",
                    "evidence_ids": ["AURALO-PRICE-001"],
                    "evidence_bindings": [
                        {
                            "evidence_id": "AURALO-PRICE-001",
                            "fragments": [
                                "Auralo Pheromone Perfume",
                                "$29",
                            ],
                        }
                    ],
                },
                {
                    "claim_id": "CLAIM-009",
                    "public_path": "image_jobs.2.visible_text.1",
                    "scope": "free_fact",
                    "text": "Star Burst Necklace — FREE",
                    "evidence_ids": ["FREE-IDENTITY-001"],
                    "evidence_bindings": [
                        {
                            "evidence_id": "FREE-IDENTITY-001",
                            "fragments": ["Star Burst Necklace"],
                        }
                    ],
                },
            ],
            "image_jobs": [
                {
                    "id": "IMG-01",
                    "angle_id": "signature-before-words",
                    "product_presence": "paid",
                    "copy_source_paths": ["copy.body", "copy.cta"],
                    "evidence_ids": ["AURALO-IDENTITY-001"],
                    "production_direction": (
                        "Editorial bottle still life with believable window light "
                        "and accurate proportions."
                    ),
                    "visible_text": "Meet Auralo Pheromone Perfume",
                },
                {
                    "id": "IMG-02",
                    "angle_id": "finish-worth-remembering",
                    "product_presence": "free",
                    "copy_source_paths": ["copy.body", "copy.subheadline"],
                    "evidence_ids": ["FREE-IDENTITY-001"],
                    "production_direction": (
                        "Editorial necklace still life matching the supplied "
                        "current-product reference."
                    ),
                    "visible_text": "Your Star Burst Necklace is FREE",
                },
                {
                    "id": "IMG-03",
                    "angle_id": "signature-before-words",
                    "product_presence": "both",
                    "copy_source_paths": ["copy.headline", "copy.subheadline"],
                    "evidence_ids": [
                        "AURALO-IDENTITY-001",
                        "FREE-IDENTITY-001",
                    ],
                    "production_direction": (
                        "Believable evening preparation scene with the current "
                        "bottle and necklace each clearly identifiable."
                    ),
                    "visible_text": [
                        "Auralo Pheromone Perfume — $29",
                        "Star Burst Necklace — FREE",
                    ],
                },
            ],
        }
        copy_sha256 = contract.canonical_sha256(payload["copy"])
        copy_paths = [f"copy.{key}" for key in payload["copy"]]
        payload.update(
            {
                "writer_packet_sha256": accepted_brief["writer_packet_sha256"],
                "copy_sha256": copy_sha256,
                "copy_review": {
                    "schema_version": "1.0",
                    "status": "accepted",
                    "copy_sha256": copy_sha256,
                    "writer_session_id": "writer-session-001",
                    "reviewer_session_id": "copy-chief-session-001",
                    "checks": {
                        field: {
                            "status": "pass",
                            "finding": f"{field} passed against the complete finished copy.",
                            "copy_paths": copy_paths,
                        }
                        for field in sorted(contract.COPY_REVIEW_CHECKS)
                    },
                },
                "page_mapping": {
                    "schema_version": "1.0",
                    "copy_sha256": copy_sha256,
                    "sections": [
                        {
                            "id": "complete-sales-argument",
                            "copy_paths": copy_paths,
                            "image_job_ids": [
                                job["id"] for job in payload["image_jobs"]
                            ],
                        }
                    ],
                },
            }
        )
        return payload

    def assert_code(self, expected: str, callback) -> None:
        with self.assertRaises(contract.ContractError) as raised:
            callback()
        self.assertEqual(raised.exception.code, expected)

    def test_fixed_dossier_and_reference_hash_pass(self) -> None:
        result = contract.validate_dossier(
            self.dossier,
            asset_root=DOSSIER_PATH.parent,
        )
        self.assertEqual(result["status"], "accepted")
        self.assertEqual(
            set(result["evidence_ids"]),
            contract.REQUIRED_AURALO_EVIDENCE_IDS,
        )

    def test_paid_product_override_is_rejected(self) -> None:
        changed = copy.deepcopy(self.campaign)
        changed["paid_product"] = {"public_name": "Something else"}
        self.assert_code(
            "PAID_PRODUCT_OVERRIDE",
            lambda: contract.validate_campaign(
                changed,
                self.dossier,
                asset_root=ASSET_ROOT,
            ),
        )

    def test_hidden_campaign_fields_are_rejected(self) -> None:
        changed = copy.deepcopy(self.campaign)
        changed["prior_campaign_copy"] = "stale material"
        self.assert_code(
            "CAMPAIGN_INVALID",
            lambda: contract.validate_campaign(
                changed,
                self.dossier,
                asset_root=ASSET_ROOT,
            ),
        )

    def test_stale_facts_cannot_be_relabelled_as_a_new_free_product(self) -> None:
        changed = copy.deepcopy(self.campaign)
        changed["free_product"]["id"] = "new-unrelated-item"
        changed["free_product"]["public_name"] = "New Unrelated Item"
        changed["free_product"]["identity_terms"] = [
            "folding handle",
            "insulated chamber",
        ]
        self.assert_code(
            "CAMPAIGN_INVALID",
            lambda: contract.validate_campaign(
                changed,
                self.dossier,
                asset_root=ASSET_ROOT,
            ),
        )

    def test_fixed_dossier_price_override_is_rejected(self) -> None:
        changed = copy.deepcopy(self.dossier)
        changed["product"]["price_usd"] = 19
        self.assert_code(
            "DOSSIER_INVALID",
            lambda: contract.validate_dossier(changed),
        )

    def test_fixed_dossier_claim_change_requires_versioned_hash_update(self) -> None:
        changed = copy.deepcopy(self.dossier)
        changed["facts"][0]["public_language"] = "Changed without a version update."
        self.assert_code(
            "DOSSIER_INVALID",
            lambda: contract.validate_dossier(changed),
        )

    def test_current_free_product_contract_passes(self) -> None:
        result = contract.validate_campaign(
            self.campaign,
            self.dossier,
            asset_root=ASSET_ROOT,
        )
        self.assertEqual(result["free_product_name"], "Star Burst Necklace")
        self.assertEqual(result["status"], "accepted")

    def test_free_product_reference_cannot_escape_asset_root(self) -> None:
        changed = copy.deepcopy(self.campaign)
        changed["free_product"]["reference_images"][0]["path"] = (
            "../../archive/sprinkle-pants.png"
        )
        changed["free_product"]["reference_images"][0]["sha256"] = "f" * 64
        self.assert_code(
            "CAMPAIGN_ASSET_INVALID",
            lambda: contract.validate_campaign(
                changed,
                self.dossier,
                asset_root=ASSET_ROOT,
            ),
        )

    def test_free_product_reference_must_exist(self) -> None:
        changed = copy.deepcopy(self.campaign)
        changed["free_product"]["reference_images"][0]["path"] = (
            "assets/missing-reference.png"
        )
        changed["free_product"]["reference_images"][0]["sha256"] = "0" * 64
        self.assert_code(
            "CAMPAIGN_ASSET_INVALID",
            lambda: contract.validate_campaign(
                changed,
                self.dossier,
                asset_root=ASSET_ROOT,
            ),
        )

    def test_free_product_reference_hash_must_match_bytes(self) -> None:
        changed = copy.deepcopy(self.campaign)
        changed["free_product"]["reference_images"][0]["sha256"] = "f" * 64
        self.assert_code(
            "CAMPAIGN_ASSET_INVALID",
            lambda: contract.validate_campaign(
                changed,
                self.dossier,
                asset_root=ASSET_ROOT,
            ),
        )

    def test_two_unrelated_free_products_remain_isolated(self) -> None:
        first = contract.validate_campaign(
            self.campaign,
            self.dossier,
            asset_root=ASSET_ROOT,
        )
        second = contract.validate_campaign(
            self.second_campaign,
            self.dossier,
            asset_root=ASSET_ROOT,
        )
        self.assertEqual(first["free_product_name"], "Star Burst Necklace")
        self.assertEqual(second["free_product_name"], "Cloud Travel Case")

        first_registry = contract.build_prior_entity_registry(
            self.campaign,
            [self.second_campaign],
            self.dossier,
            asset_root=ASSET_ROOT,
        )
        second_registry = contract.build_prior_entity_registry(
            self.second_campaign,
            [self.campaign],
            self.dossier,
            asset_root=ASSET_ROOT,
        )
        self.assertIn("quilted shell", first_registry["forbidden_entities"])
        self.assertNotIn("radiating pendant", first_registry["forbidden_entities"])
        self.assertIn("radiating pendant", second_registry["forbidden_entities"])
        self.assertNotIn("quilted shell", second_registry["forbidden_entities"])

    def test_plugin_contract_surface_has_no_prior_pants_vocabulary(self) -> None:
        forbidden = ("pants", "tweed", "drawcord", "fringe")
        surfaced: list[str] = []
        roots = [
            PLUGIN_ROOT / ".codex-plugin",
            PLUGIN_ROOT / "skills",
        ]
        for root in roots:
            for path in root.rglob("*"):
                if not path.is_file() or path.suffix.lower() not in {
                    ".json",
                    ".md",
                    ".py",
                    ".yaml",
                }:
                    continue
                text = path.read_text(encoding="utf-8").casefold()
                for term in forbidden:
                    if term in text:
                        surfaced.append(f"{path.relative_to(PLUGIN_ROOT)}:{term}")
        self.assertEqual(surfaced, [])

    def test_free_product_requires_fresh_facts(self) -> None:
        changed = copy.deepcopy(self.campaign)
        changed["free_product"]["facts"] = []
        self.assert_code(
            "INVALID_CONTRACT",
            lambda: contract.validate_campaign(
                changed,
                self.dossier,
                asset_root=ASSET_ROOT,
            ),
        )

    def test_wanted_premium_marriage_brief_passes(self) -> None:
        result = contract.validate_marriage_brief(
            self.brief(),
            self.campaign,
            self.dossier,
            asset_root=ASSET_ROOT,
        )
        self.assertEqual(result["relationship_mode"], "wanted_premium")

    def test_complement_mode_requires_two_relationship_rows(self) -> None:
        changed = self.brief(mode="evidence_backed_complement")
        changed["relationship_evidence_ids"] = ["R-REL-001"]
        self.assert_code(
            "MARRIAGE_GAP",
            lambda: contract.validate_marriage_brief(
                changed,
                self.campaign,
                self.dossier,
                asset_root=ASSET_ROOT,
            ),
        )

    def test_angle_repair_limit_stops(self) -> None:
        self.assert_code(
            "ANGLE_GAP",
            lambda: contract.validate_marriage_brief(
                self.brief(repair_cycles=3),
                self.campaign,
                self.dossier,
                asset_root=ASSET_ROOT,
            ),
        )

    def test_missing_primary_angle_stops_as_angle_gap(self) -> None:
        changed = self.brief()
        changed.pop("primary_angle")
        self.assert_code(
            "ANGLE_GAP",
            lambda: contract.validate_marriage_brief(
                changed,
                self.campaign,
                self.dossier,
                asset_root=ASSET_ROOT,
            ),
        )

    def test_generic_transaction_bridge_stops(self) -> None:
        changed = self.brief()
        changed["transaction_bridge"] = (
            "Put these two choices into one easy transaction before heading out."
        )
        self.assert_code(
            "MARRIAGE_GAP",
            lambda: contract.validate_marriage_brief(
                changed,
                self.campaign,
                self.dossier,
                asset_root=ASSET_ROOT,
            ),
        )

    def test_paid_and_free_restatement_is_not_a_marriage_bridge(self) -> None:
        changed = self.brief()
        changed["transaction_bridge"] = (
            "Auralo Pheromone Perfume is the paid item and the "
            "Star Burst Necklace is the FREE item."
        )
        changed["buyer_moment"] = (
            "The customer sees the two items on the same checkout page."
        )
        changed["substitution_test"] = {
            "question": "Are these simply the two named items in this transaction?",
            "result": "passed",
            "evidence_ids": ["AURALO-IDENTITY-001"],
        }
        self.assert_code(
            "MARRIAGE_GAP",
            lambda: contract.validate_marriage_brief(
                changed,
                self.campaign,
                self.dossier,
                asset_root=ASSET_ROOT,
            ),
        )

    def test_public_payload_passes_with_current_products_and_angles(self) -> None:
        brief = self.brief()
        result = contract.validate_public_payload(
            self.payload(brief),
            self.campaign,
            brief,
            self.dossier,
            self.registry(),
            asset_root=ASSET_ROOT,
        )
        self.assertEqual(result["image_job_count"], 3)
        self.assertEqual(result["status"], "accepted")
        self.assertEqual(result["copy_sha256"], self.payload(brief)["copy_sha256"])
        self.assertIn("page_mapping_sha256", result)

    def test_page_and_image_mapping_cannot_precede_finished_copy(self) -> None:
        brief = self.brief()
        payload = self.payload(brief)
        payload["page_mapping"]["copy_sha256"] = "0" * 64
        self.assert_code(
            "COPY_NOT_FINAL",
            lambda: contract.validate_public_payload(
                payload,
                self.campaign,
                brief,
                self.dossier,
                self.registry(),
                asset_root=ASSET_ROOT,
            ),
        )

    def test_copy_hash_must_match_the_complete_finished_argument(self) -> None:
        brief = self.brief()
        payload = self.payload(brief)
        payload["copy_sha256"] = "0" * 64
        self.assert_code(
            "COPY_HASH_MISMATCH",
            lambda: contract.validate_public_payload(
                payload,
                self.campaign,
                brief,
                self.dossier,
                self.registry(),
                asset_root=ASSET_ROOT,
            ),
        )

    def test_copy_chief_must_be_independent_from_the_writer(self) -> None:
        brief = self.brief()
        payload = self.payload(brief)
        payload["copy_review"]["reviewer_session_id"] = payload["copy_review"][
            "writer_session_id"
        ]
        self.assert_code(
            "COPY_REVIEW_NOT_INDEPENDENT",
            lambda: contract.validate_public_payload(
                payload,
                self.campaign,
                brief,
                self.dossier,
                self.registry(),
                asset_root=ASSET_ROOT,
            ),
        )

    def test_writer_packet_hash_must_match_the_selected_clean_packet(self) -> None:
        brief = self.brief()
        payload = self.payload(brief)
        payload["writer_packet_sha256"] = "0" * 64
        self.assert_code(
            "WRITER_PACKET_MISMATCH",
            lambda: contract.validate_public_payload(
                payload,
                self.campaign,
                brief,
                self.dossier,
                self.registry(),
                asset_root=ASSET_ROOT,
            ),
        )

    def test_generic_ai_pairing_glue_is_rejected_before_delivery(self) -> None:
        brief = self.brief()
        payload = self.payload(brief)
        payload["copy"]["headline"] = (
            "Auralo Pheromone Perfume and Star Burst Necklace are better together."
        )
        self.assert_code(
            "CROSS_CAMPAIGN_LEAK",
            lambda: contract.validate_public_payload(
                payload,
                self.campaign,
                brief,
                self.dossier,
                self.registry(),
                asset_root=ASSET_ROOT,
            ),
        )

    def test_page_mapping_must_cover_every_image_job_exactly_once(self) -> None:
        brief = self.brief()
        payload = self.payload(brief)
        payload["page_mapping"]["sections"][0]["image_job_ids"].pop()
        self.assert_code(
            "PAGE_MAPPING_INVALID",
            lambda: contract.validate_public_payload(
                payload,
                self.campaign,
                brief,
                self.dossier,
                self.registry(),
                asset_root=ASSET_ROOT,
            ),
        )

    def test_image_jobs_must_derive_from_finished_copy_paths(self) -> None:
        brief = self.brief()
        payload = self.payload(brief)
        payload["image_jobs"][0]["copy_source_paths"] = ["strategy.primary_angle"]
        self.assert_code(
            "COPY_NOT_FINAL",
            lambda: contract.validate_public_payload(
                payload,
                self.campaign,
                brief,
                self.dossier,
                self.registry(),
                asset_root=ASSET_ROOT,
            ),
        )

    def test_internal_strategy_visible_text_is_rejected(self) -> None:
        brief = self.brief()
        payload = self.payload(brief)
        payload["image_jobs"][2]["visible_text"] = (
            "One getting-ready story, not two random products"
        )
        self.assert_code(
            "CROSS_CAMPAIGN_LEAK",
            lambda: contract.validate_public_payload(
                payload,
                self.campaign,
                brief,
                self.dossier,
                self.registry(),
                asset_root=ASSET_ROOT,
            ),
        )

    def test_internal_strategy_in_prompt_direction_is_rejected(self) -> None:
        brief = self.brief()
        payload = self.payload(brief)
        payload["image_jobs"][0]["production_direction"] = (
            "Use the value stack framework to show both products."
        )
        self.assert_code(
            "CROSS_CAMPAIGN_LEAK",
            lambda: contract.validate_public_payload(
                payload,
                self.campaign,
                brief,
                self.dossier,
                self.registry(),
                asset_root=ASSET_ROOT,
            ),
        )

    def test_generic_product_placeholders_in_prompt_direction_are_rejected(
        self,
    ) -> None:
        brief = self.brief()
        payload = self.payload(brief)
        payload["image_jobs"][0]["production_direction"] = (
            "Place the paid product beside the free product in soft window light."
        )
        self.assert_code(
            "CROSS_CAMPAIGN_LEAK",
            lambda: contract.validate_public_payload(
                payload,
                self.campaign,
                brief,
                self.dossier,
                self.registry(),
                asset_root=ASSET_ROOT,
            ),
        )

    def test_unsupported_outcome_in_prompt_direction_is_rejected(self) -> None:
        brief = self.brief()
        payload = self.payload(brief)
        payload["image_jobs"][0]["production_direction"] = (
            "Editorial scene implying pheromones attract everyone nearby."
        )
        self.assert_code(
            "CLAIM_NOT_AUTHORIZED",
            lambda: contract.validate_public_payload(
                payload,
                self.campaign,
                brief,
                self.dossier,
                self.registry(),
                asset_root=ASSET_ROOT,
            ),
        )

    def test_prior_product_terms_are_validator_only_and_block_delivery(self) -> None:
        prior = copy.deepcopy(self.campaign)
        prior["campaign_id"] = "prior-trouser-campaign"
        prior["free_product"]["id"] = "sprinkle-trousers"
        prior["free_product"]["public_name"] = "Sprinkle Tweed Pants"
        prior["free_product"]["category"] = "clothing"
        prior["free_product"]["identity_terms"] = [
            "flecked tweed",
            "drawcord waist",
            "fringed hem",
        ]
        prior["free_product"]["facts"][0]["claim"] = (
            "The supplied reference shows flecked tweed trousers."
        )
        prior["free_product"]["facts"][0]["public_language"] = (
            "Flecked tweed gives the trousers their textured finish."
        )
        prior["free_product"]["facts"][1]["claim"] = (
            "The supplied reference shows a drawcord waist and fringed hem."
        )
        prior["free_product"]["facts"][1]["public_language"] = (
            "A drawcord waist and fringed hem finish the trousers."
        )
        prior["evidence_ledger"][0]["excerpt"] = (
            "The supplied reference shows flecked tweed trousers."
        )
        prior["evidence_ledger"][1]["excerpt"] = (
            "The supplied reference shows a drawcord waist and fringed hem."
        )
        registry = self.registry([prior])
        self.assertEqual(
            registry["purpose"],
            "validator_only_do_not_send_to_writer",
        )
        brief = self.brief()
        payload = self.payload(brief)
        payload["copy"]["body"] += " Finished with a flecked tweed texture."
        self.assert_code(
            "CROSS_CAMPAIGN_LEAK",
            lambda: contract.validate_public_payload(
                payload,
                self.campaign,
                brief,
                self.dossier,
                registry,
                asset_root=ASSET_ROOT,
            ),
        )

    def test_current_product_terms_are_not_treated_as_prior_leaks(self) -> None:
        prior = copy.deepcopy(self.campaign)
        prior["campaign_id"] = "older-star-campaign"
        registry = self.registry([prior])
        self.assertEqual(registry["forbidden_entities"], [])

    def test_question_and_asterisk_do_not_authorize_outcome_claim(self) -> None:
        brief = self.brief()
        payload = self.payload(brief)
        payload["claims"][0].update(
            {
                "scope": "paid_fact",
                "text": "Guaranteed attraction*?",
                "evidence_ids": ["AURALO-IDENTITY-001"],
            }
        )
        payload["copy"]["headline"] = "Guaranteed attraction*?"
        self.assert_code(
            "CLAIM_NOT_AUTHORIZED",
            lambda: contract.validate_public_payload(
                payload,
                self.campaign,
                brief,
                self.dossier,
                self.registry(),
                asset_root=ASSET_ROOT,
            ),
        )

    def test_reworded_question_does_not_bypass_outcome_gate(self) -> None:
        brief = self.brief()
        payload = self.payload(brief)
        payload["claims"][0].update(
            {
                "scope": "paid_fact",
                "text": "Could pheromones make everyone flirt with you*?",
                "evidence_ids": ["AURALO-IDENTITY-001"],
            }
        )
        payload["copy"]["headline"] = "Could pheromones make everyone flirt with you*?"
        self.assert_code(
            "CLAIM_NOT_AUTHORIZED",
            lambda: contract.validate_public_payload(
                payload,
                self.campaign,
                brief,
                self.dossier,
                self.registry(),
                asset_root=ASSET_ROOT,
            ),
        )

    def test_unrelated_valid_evidence_cannot_authorize_new_claim(self) -> None:
        brief = self.brief()
        payload = self.payload(brief)
        unsupported = "Auralo Pheromone Perfume eliminates anxiety."
        payload["copy"]["headline"] = unsupported
        payload["claims"][0].update(
            {
                "scope": "paid_fact",
                "text": unsupported,
                "evidence_ids": ["AURALO-IDENTITY-001"],
                "evidence_bindings": [
                    {
                        "evidence_id": "AURALO-IDENTITY-001",
                        "fragments": ["Auralo Pheromone Perfume"],
                    }
                ],
            }
        )
        self.assert_code(
            "CLAIM_NOT_AUTHORIZED",
            lambda: contract.validate_public_payload(
                payload,
                self.campaign,
                brief,
                self.dossier,
                self.registry(),
                asset_root=ASSET_ROOT,
            ),
        )

    def test_valid_evidence_values_cannot_be_swapped_into_false_claim(self) -> None:
        brief = self.brief()
        payload = self.payload(brief)
        unsupported = "Auralo Pheromone Perfume is a 29 ml perfume for $15."
        payload["copy"]["headline"] = unsupported
        payload["claims"][0].update(
            {
                "scope": "paid_fact",
                "text": unsupported,
                "evidence_ids": [
                    "AURALO-IDENTITY-001",
                    "AURALO-PRICE-001",
                ],
                "evidence_bindings": [
                    {
                        "evidence_id": "AURALO-IDENTITY-001",
                        "fragments": [
                            "Auralo Pheromone Perfume",
                            "15 ml",
                        ],
                    },
                    {
                        "evidence_id": "AURALO-PRICE-001",
                        "fragments": ["$29"],
                    },
                ],
            }
        )
        self.assert_code(
            "CLAIM_NOT_AUTHORIZED",
            lambda: contract.validate_public_payload(
                payload,
                self.campaign,
                brief,
                self.dossier,
                self.registry(),
                asset_root=ASSET_ROOT,
            ),
        )

    def test_evidence_fragments_cannot_reverse_a_use_instruction(self) -> None:
        brief = self.brief()
        payload = self.payload(brief)
        unsupported = "Apply pulse points to two or three drops."
        payload["copy"]["headline"] = unsupported
        payload["claims"][0].update(
            {
                "scope": "paid_fact",
                "text": unsupported,
                "evidence_ids": ["AURALO-USE-001"],
                "evidence_bindings": [
                    {
                        "evidence_id": "AURALO-USE-001",
                        "fragments": [
                            "Apply",
                            "pulse points",
                            "two",
                            "three",
                            "drops",
                        ],
                    }
                ],
            }
        )
        self.assert_code(
            "CLAIM_NOT_AUTHORIZED",
            lambda: contract.validate_public_payload(
                payload,
                self.campaign,
                brief,
                self.dossier,
                self.registry(),
                asset_root=ASSET_ROOT,
            ),
        )

    def test_valid_facts_cannot_be_assigned_to_the_wrong_product(self) -> None:
        brief = self.brief()
        payload = self.payload(brief)
        unsupported = (
            "Auralo Pheromone Perfume is jewellery and "
            "Star Burst Necklace is a floral-amber scent."
        )
        payload["copy"]["headline"] = unsupported
        payload["claims"][0].update(
            {
                "scope": "multi_product_fact",
                "text": unsupported,
                "evidence_ids": [
                    "AURALO-SCENT-001",
                    "FREE-IDENTITY-001",
                ],
                "evidence_bindings": [
                    {
                        "evidence_id": "AURALO-SCENT-001",
                        "fragments": [
                            "Auralo Pheromone Perfume",
                            "floral-amber scent",
                        ],
                    },
                    {
                        "evidence_id": "FREE-IDENTITY-001",
                        "fragments": [
                            "Star Burst Necklace",
                            "jewellery",
                        ],
                    },
                ],
            }
        )
        self.assert_code(
            "CLAIM_NOT_AUTHORIZED",
            lambda: contract.validate_public_payload(
                payload,
                self.campaign,
                brief,
                self.dossier,
                self.registry(),
                asset_root=ASSET_ROOT,
            ),
        )

    def test_paid_and_free_offer_roles_cannot_be_inverted(self) -> None:
        brief = self.brief()
        payload = self.payload(brief)
        unsupported = (
            "Get Star Burst Necklace for $29 and receive Auralo Pheromone Perfume FREE."
        )
        payload["copy"]["headline"] = unsupported
        payload["claims"][0].update(
            {
                "scope": "offer",
                "text": unsupported,
                "evidence_ids": [
                    "AURALO-IDENTITY-001",
                    "AURALO-PRICE-001",
                    "FREE-IDENTITY-001",
                ],
                "evidence_bindings": [
                    {
                        "evidence_id": "AURALO-IDENTITY-001",
                        "fragments": ["Auralo Pheromone Perfume"],
                    },
                    {
                        "evidence_id": "AURALO-PRICE-001",
                        "fragments": ["$29"],
                    },
                    {
                        "evidence_id": "FREE-IDENTITY-001",
                        "fragments": ["Star Burst Necklace"],
                    },
                ],
            }
        )
        self.assert_code(
            "CLAIM_NOT_AUTHORIZED",
            lambda: contract.validate_public_payload(
                payload,
                self.campaign,
                brief,
                self.dossier,
                self.registry(),
                asset_root=ASSET_ROOT,
            ),
        )

    def test_relationship_scope_cannot_launder_price_or_partial_owner(self) -> None:
        brief = self.brief()
        payload = self.payload(brief)
        unsupported = "Before an evening out, Star Burst is a $29 perfume."
        payload["copy"]["headline"] = unsupported
        payload["claims"][0].update(
            {
                "scope": "relationship",
                "text": unsupported,
                "evidence_ids": [
                    "AURALO-IDENTITY-001",
                    "AURALO-PRICE-001",
                    "FREE-IDENTITY-001",
                    "REL-001",
                ],
                "evidence_bindings": [
                    {
                        "evidence_id": "AURALO-IDENTITY-001",
                        "fragments": ["perfume"],
                    },
                    {
                        "evidence_id": "AURALO-PRICE-001",
                        "fragments": ["$29"],
                    },
                    {
                        "evidence_id": "FREE-IDENTITY-001",
                        "fragments": ["Star Burst"],
                    },
                    {
                        "evidence_id": "REL-001",
                        "fragments": ["before an evening out"],
                    },
                ],
            }
        )
        self.assert_code(
            "CLAIM_NOT_AUTHORIZED",
            lambda: contract.validate_public_payload(
                payload,
                self.campaign,
                brief,
                self.dossier,
                self.registry(),
                asset_root=ASSET_ROOT,
            ),
        )

    def test_relationship_scope_rejects_partial_name_identity_swap(self) -> None:
        brief = self.brief()
        payload = self.payload(brief)
        unsupported = "Before an evening out, Star Burst is perfume."
        payload["copy"]["headline"] = unsupported
        payload["claims"][0].update(
            {
                "scope": "relationship",
                "text": unsupported,
                "evidence_ids": [
                    "AURALO-IDENTITY-001",
                    "FREE-IDENTITY-001",
                    "REL-001",
                ],
                "evidence_bindings": [
                    {
                        "evidence_id": "AURALO-IDENTITY-001",
                        "fragments": ["perfume"],
                    },
                    {
                        "evidence_id": "FREE-IDENTITY-001",
                        "fragments": ["Star Burst"],
                    },
                    {
                        "evidence_id": "REL-001",
                        "fragments": ["before an evening out"],
                    },
                ],
            }
        )
        self.assert_code(
            "CLAIM_NOT_AUTHORIZED",
            lambda: contract.validate_public_payload(
                payload,
                self.campaign,
                brief,
                self.dossier,
                self.registry(),
                asset_root=ASSET_ROOT,
            ),
        )

    def test_star_rating_decoration_requires_evidence_and_is_rejected(self) -> None:
        brief = self.brief()
        payload = self.payload(brief)
        unsupported = "★★★★★ Auralo is a 15 ml pheromone-inspired floral-amber perfume."
        payload["copy"]["headline"] = unsupported
        payload["claims"][0].update(
            {
                "scope": "paid_fact",
                "text": unsupported,
                "evidence_ids": ["AURALO-IDENTITY-001"],
                "evidence_bindings": [
                    {
                        "evidence_id": "AURALO-IDENTITY-001",
                        "fragments": [
                            "Auralo is a 15 ml pheromone-inspired floral-amber perfume."
                        ],
                    }
                ],
            }
        )
        self.assert_code(
            "CLAIM_NOT_AUTHORIZED",
            lambda: contract.validate_public_payload(
                payload,
                self.campaign,
                brief,
                self.dossier,
                self.registry(),
                asset_root=ASSET_ROOT,
            ),
        )

    def test_claim_scope_cannot_launder_relationship_evidence(self) -> None:
        brief = self.brief()
        payload = self.payload(brief)
        payload["claims"][0]["scope"] = "paid_fact"
        self.assert_code(
            "CLAIM_NOT_AUTHORIZED",
            lambda: contract.validate_public_payload(
                payload,
                self.campaign,
                brief,
                self.dossier,
                self.registry(),
                asset_root=ASSET_ROOT,
            ),
        )

    def test_every_public_text_field_requires_exact_claim_grounding(self) -> None:
        brief = self.brief()
        payload = self.payload(brief)
        payload["copy"]["body"] += " This extra sentence is not grounded."
        self.assert_code(
            "CLAIM_NOT_AUTHORIZED",
            lambda: contract.validate_public_payload(
                payload,
                self.campaign,
                brief,
                self.dossier,
                self.registry(),
                asset_root=ASSET_ROOT,
            ),
        )

    def test_unknown_claim_evidence_is_rejected(self) -> None:
        brief = self.brief()
        payload = self.payload(brief)
        payload["claims"][0]["evidence_ids"] = ["STALE-CLAIM-999"]
        self.assert_code(
            "CLAIM_NOT_AUTHORIZED",
            lambda: contract.validate_public_payload(
                payload,
                self.campaign,
                brief,
                self.dossier,
                self.registry(),
                asset_root=ASSET_ROOT,
            ),
        )

    def test_production_instruction_cannot_be_visible_copy(self) -> None:
        brief = self.brief()
        payload = self.payload(brief)
        payload["image_jobs"][0]["visible_text"] = (
            "Close-up shot: place the product on the right"
        )
        self.assert_code(
            "CROSS_CAMPAIGN_LEAK",
            lambda: contract.validate_public_payload(
                payload,
                self.campaign,
                brief,
                self.dossier,
                self.registry(),
                asset_root=ASSET_ROOT,
            ),
        )

    def test_payload_must_be_bound_to_accepted_brief_hash(self) -> None:
        brief = self.brief()
        payload = self.payload(brief)
        payload["marriage_brief_sha256"] = "0" * 64
        self.assert_code(
            "ANGLE_NOT_BOUND",
            lambda: contract.validate_public_payload(
                payload,
                self.campaign,
                brief,
                self.dossier,
                self.registry(),
                asset_root=ASSET_ROOT,
            ),
        )

    def test_image_jobs_must_cover_paid_free_and_joint_moment(self) -> None:
        brief = self.brief()
        payload = self.payload(brief)
        payload["image_jobs"] = payload["image_jobs"][:2]
        self.assert_code(
            "MARRIAGE_GAP",
            lambda: contract.validate_public_payload(
                payload,
                self.campaign,
                brief,
                self.dossier,
                self.registry(),
                asset_root=ASSET_ROOT,
            ),
        )

    def test_image_jobs_must_cite_evidence_for_declared_products(self) -> None:
        brief = self.brief()
        payload = self.payload(brief)
        payload["image_jobs"][2]["evidence_ids"] = ["AURALO-IDENTITY-001"]
        self.assert_code(
            "MARRIAGE_GAP",
            lambda: contract.validate_public_payload(
                payload,
                self.campaign,
                brief,
                self.dossier,
                self.registry(),
                asset_root=ASSET_ROOT,
            ),
        )

    def test_public_copy_must_materialize_both_exact_product_names(self) -> None:
        brief = self.brief()
        payload = self.payload(brief)
        payload["copy"] = {
            "headline": "A finish worth remembering.",
            "body": "Choose your evening details.",
        }
        payload["image_jobs"][1]["visible_text"] = "Your necklace is FREE"
        payload["image_jobs"][2]["visible_text"] = ["Scent — $29", "Necklace — FREE"]
        self.assert_code(
            "MARRIAGE_GAP",
            lambda: contract.validate_public_payload(
                payload,
                self.campaign,
                brief,
                self.dossier,
                self.registry(),
                asset_root=ASSET_ROOT,
            ),
        )


if __name__ == "__main__":
    unittest.main()
