from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
CONTRACT_SCRIPTS = PLUGIN_ROOT / "skills" / "freeperrylarp1" / "scripts"
if str(CONTRACT_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(CONTRACT_SCRIPTS))

CONTRACT_PATH = CONTRACT_SCRIPTS / "freeperrylarp1_contract.py"
BRAINSTORM_PATH = (
    PLUGIN_ROOT
    / "skills"
    / "freeperrylarp1-brainstorm"
    / "scripts"
    / "brainstorm_gate.py"
)
DOSSIER_PATH = (
    PLUGIN_ROOT / "skills" / "freeperrylarp1" / "assets" / "auralo-dossier.json"
)
CAMPAIGN_PATH = PLUGIN_ROOT / "tests" / "fixtures" / "star-burst-campaign.json"
SECOND_CAMPAIGN_PATH = PLUGIN_ROOT / "tests" / "fixtures" / "travel-case-campaign.json"
ASSET_ROOT = CAMPAIGN_PATH.parent

CONTRACT_SPEC = importlib.util.spec_from_file_location(
    "freeperrylarp1_contract",
    CONTRACT_PATH,
)
assert CONTRACT_SPEC and CONTRACT_SPEC.loader
contract = importlib.util.module_from_spec(CONTRACT_SPEC)
CONTRACT_SPEC.loader.exec_module(contract)
sys.modules["freeperrylarp1_contract"] = contract

BRAINSTORM_SPEC = importlib.util.spec_from_file_location(
    "brainstorm_gate",
    BRAINSTORM_PATH,
)
assert BRAINSTORM_SPEC and BRAINSTORM_SPEC.loader
brainstorm = importlib.util.module_from_spec(BRAINSTORM_SPEC)
BRAINSTORM_SPEC.loader.exec_module(brainstorm)


class BrainstormGateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.dossier = json.loads(DOSSIER_PATH.read_text(encoding="utf-8"))
        self.campaign = json.loads(CAMPAIGN_PATH.read_text(encoding="utf-8"))
        self.second_campaign = json.loads(
            SECOND_CAMPAIGN_PATH.read_text(encoding="utf-8")
        )

    def research_snapshot(self) -> dict:
        return {
            "schema_version": "1.0",
            "campaign_id": self.campaign["campaign_id"],
            "session_id": "fresh-research-session-001",
            "fresh_only": True,
            "status": "frozen",
            "created_at": "2026-07-23T06:00:00Z",
            "queries": [
                {
                    "id": "Q-PAID-001",
                    "lane": "paid_product",
                    "target_product_id": contract.AURALO_ID,
                    "query": "Auralo perfume format scent notes and use instructions",
                },
                {
                    "id": "Q-FREE-001",
                    "lane": "free_product",
                    "target_product_id": self.campaign["free_product"]["id"],
                    "query": "Star Burst Necklace design details and buyer questions",
                },
                {
                    "id": "Q-VOICE-001",
                    "lane": "customer_voice",
                    "target_product_id": "market",
                    "query": "exact words fragrance and jewellery shoppers use before buying",
                },
                {
                    "id": "Q-OBJECTION-001",
                    "lane": "objection",
                    "target_product_id": "market",
                    "query": "why fragrance and jewellery shoppers hesitate before purchase",
                },
                {
                    "id": "Q-TRIGGER-001",
                    "lane": "purchase_trigger",
                    "target_product_id": "market",
                    "query": "what makes fragrance and jewellery shoppers decide to buy",
                },
            ],
            "records": [
                {
                    "id": "R-PAID-FACT-001",
                    "lane": "paid_product",
                    "kind": "product_fact",
                    "target_product_id": contract.AURALO_ID,
                    "source_family": "official",
                    "source_url": "https://example.com/auralo-format",
                    "text": "The product page identifies a floral-amber perfume in a 15 ml bottle.",
                    "verbatim": False,
                },
                {
                    "id": "R-PAID-VOICE-001",
                    "lane": "paid_product",
                    "kind": "customer_language",
                    "target_product_id": contract.AURALO_ID,
                    "source_family": "forum",
                    "source_url": "https://example.net/fragrance-voice",
                    "text": "I want a scent that feels special without making the purchase complicated.",
                    "verbatim": True,
                },
                {
                    "id": "R-FREE-FACT-001",
                    "lane": "free_product",
                    "kind": "product_fact",
                    "target_product_id": self.campaign["free_product"]["id"],
                    "source_family": "official",
                    "source_url": "https://example.com/star-burst-details",
                    "text": "The necklace has a radiating pendant on a gold-tone chain.",
                    "verbatim": False,
                },
                {
                    "id": "R-FREE-VOICE-001",
                    "lane": "free_product",
                    "kind": "customer_language",
                    "target_product_id": self.campaign["free_product"]["id"],
                    "source_family": "social",
                    "source_url": "https://example.org/necklace-voice",
                    "text": "I buy jewellery when the shape gives a plain outfit one clear focal point.",
                    "verbatim": True,
                },
                {
                    "id": "R-CUSTOMER-001",
                    "lane": "customer_voice",
                    "kind": "customer_language",
                    "target_product_id": "market",
                    "source_family": "forum",
                    "source_url": "https://example.net/buyer-language",
                    "text": "Show me exactly what I get and why it is worth choosing today.",
                    "verbatim": True,
                },
                {
                    "id": "R-OBJECTION-001",
                    "lane": "objection",
                    "kind": "objection",
                    "target_product_id": "market",
                    "source_family": "forum",
                    "source_url": "https://example.net/buyer-objections",
                    "text": "A free extra feels weak when the page never makes the extra desirable.",
                    "verbatim": True,
                },
                {
                    "id": "R-TRIGGER-001",
                    "lane": "purchase_trigger",
                    "kind": "purchase_trigger",
                    "target_product_id": "market",
                    "source_family": "social",
                    "source_url": "https://example.org/purchase-language",
                    "text": "Clear details and a useful bonus make the decision easier.",
                    "verbatim": True,
                },
                {
                    "id": "R-CONTEXT-001",
                    "lane": "context",
                    "kind": "market_context",
                    "target_product_id": "market",
                    "source_family": "editorial",
                    "source_url": "https://example.edu/category-context",
                    "text": "Shoppers compare personal accessories by detail, occasion, and price clarity.",
                    "verbatim": False,
                },
            ],
        }

    def candidate(self, index: int) -> dict:
        situations = [
            "choosing a personal treat before a dinner she has been looking forward to",
            "refreshing a simple outfit before meeting friends after work",
            "buying a small birthday reward without wanting a complicated decision",
            "choosing a travel-friendly scent and one visible detail for a weekend away",
        ]
        arguments = [
            (
                "Make the $29 bottle worth choosing for its scent and compact format, "
                "then make the necklace a genuinely wanted extra by showing its exact focal design."
            ),
            (
                "Lead with a clear after-work self-purchase: a named floral-amber scent "
                "for $29, with a visible starburst piece that saves a second decision."
            ),
            (
                "Turn a birthday self-gift into an easy value decision by proving the "
                "perfume and necklace separately before stating the FREE transaction."
            ),
            (
                "Use compactness and exact product detail to sell a weekend-away choice: "
                "the 15 ml scent earns the purchase and the necklace earns its place as the reward."
            ),
        ]
        hooks = [
            "A $29 scent worth choosing. A necklace worth wanting.",
            "Two clear reasons to say yes before the evening starts.",
            "Make the birthday treat feel complete without hiding the terms.",
            "Pack the scent. Wear the detail. See every term first.",
        ]
        customer_ids = ["R-PAID-VOICE-001", "R-FREE-VOICE-001"]
        evidence_ids = [
            "AURALO-IDENTITY-001",
            "AURALO-SCENT-001",
            "FREE-IDENTITY-001",
            "FREE-FORM-001",
            "R-PAID-VOICE-001",
            "R-FREE-VOICE-001",
            "R-OBJECTION-001",
            "R-TRIGGER-001",
        ]
        return {
            "id": f"connection-{index + 1}",
            "generator_session_id": f"generator-session-{index + 1}",
            "observed_other_candidate_ids": [],
            "relationship_mode": "wanted_premium",
            "sales_argument": arguments[index],
            "hook": hooks[index],
            "buyer_action": (
                "Choose the scent for its own merits, inspect the necklace, then decide on the $29 transaction."
            ),
            "buyer_situation": situations[index],
            "buyer_bridge": {
                "shared_avatar": "A detail-conscious self-purchaser who wants clear value before buying.",
                "occasion_or_desire": situations[index],
                "reason_to_act": (
                    "She can judge the scent and necklace separately, then see the exact $29 and FREE terms."
                ),
                "evidence_ids": [
                    "R-PAID-VOICE-001",
                    "R-FREE-VOICE-001",
                    "R-OBJECTION-001",
                ],
            },
            "transaction_bridge": (
                "Choose Auralo Pheromone Perfume for $29 and receive the "
                "Star Burst Necklace FREE after both items have earned desire separately."
            ),
            "product_roles": {
                "paid": "Auralo Pheromone Perfume is the $29 floral-amber scent that earns the purchase.",
                "free": "Star Burst Necklace is the exact visible piece made desirable before it is labelled FREE.",
            },
            "substitution_test": {
                "question": "If either named product is replaced, does the specific reason to choose this transaction change?",
                "reason": (
                    "Replacing Auralo Pheromone Perfume removes the evidenced scent and format; "
                    "replacing Star Burst Necklace removes the evidenced starburst focal design."
                ),
                "evidence_ids": [
                    "AURALO-IDENTITY-001",
                    "FREE-IDENTITY-001",
                    "R-PAID-VOICE-001",
                    "R-FREE-VOICE-001",
                ],
            },
            "evidence_ids": evidence_ids,
            "customer_language_evidence_ids": customer_ids,
            "relationship_evidence_ids": [],
        }

    def critic(self, snapshot: dict, candidates: list[dict]) -> dict:
        research_receipt = contract.validate_neutral_research_snapshot(
            snapshot,
            self.campaign,
            self.dossier,
            asset_root=ASSET_ROOT,
        )
        authorized = contract.all_evidence_ids(self.dossier, self.campaign)
        normalized = [
            brainstorm._normalize_candidate(
                candidate,
                index,
                self.campaign,
                authorized,
                research_receipt,
            )
            for index, candidate in enumerate(candidates)
        ]
        candidate_set_sha256 = contract.canonical_sha256(normalized)
        score_rows = []
        challenge_rows = []
        for index, candidate in enumerate(candidates):
            score_rows.append(
                {
                    "candidate_id": candidate["id"],
                    "paid_product_desire": 5 if index == 0 else 4,
                    "free_product_desire": 5 if index in {0, 1} else 4,
                    "first_touch_clarity": 5 if index < 2 else 4,
                    "buyer_situation_specificity": 5 - min(index, 1),
                    "transaction_credibility": 5 if index == 0 else 4,
                    "evidence_fit": 5 if index < 2 else 4,
                    "claim_integrity": 5,
                    "creative_distinctiveness": 5 - index,
                }
            )
            challenge_rows.append(
                {
                    "candidate_id": candidate["id"],
                    "verdict": "eligible",
                    "evidence_ids": [
                        "R-PAID-VOICE-001",
                        "R-FREE-VOICE-001",
                        "R-OBJECTION-001",
                    ],
                    "checks": {
                        field: {
                            "status": "pass",
                            "finding": f"{field} was tested against the cited current evidence.",
                        }
                        for field in sorted(brainstorm.CHALLENGE_FIELDS)
                    },
                }
            )
        return {
            "schema_version": "1.0",
            "critic_session_id": "independent-critic-session-001",
            "research_snapshot_sha256": research_receipt["sha256"],
            "candidate_set_sha256": candidate_set_sha256,
            "evaluated_candidate_ids": [candidate["id"] for candidate in candidates],
            "scores": score_rows,
            "challenges": challenge_rows,
            "primary_candidate_id": "connection-1",
            "backup_candidate_id": "connection-2",
            "selection_reason": (
                "The first connection has the strongest independent desire, evidence, and transaction clarity."
            ),
            "rejected_assumptions": [
                "The products do not need to be used together to make the transaction persuasive."
            ],
            "second_order_consequences": [
                "Each product needs its own proof and page space before the transaction statement."
            ],
            "third_order_consequences": [
                "Image jobs must follow accepted copy rather than inventing a reusable scene recipe."
            ],
            "unresolved_evidence_gaps": [],
        }

    def payload(self, repair_cycle: int = 0) -> dict:
        snapshot = self.research_snapshot()
        candidates = [self.candidate(index) for index in range(4)]
        return {
            "schema_version": "2.0",
            "repair_cycle": repair_cycle,
            "research_snapshot": snapshot,
            "prior_entity_registry": contract.build_prior_entity_registry(
                self.campaign,
                [],
                self.dossier,
                asset_root=ASSET_ROOT,
            ),
            "candidates": candidates,
            "critic": self.critic(snapshot, candidates),
        }

    def assert_code(self, expected: str, callback) -> None:
        with self.assertRaises(contract.ContractError) as raised:
            callback()
        self.assertEqual(raised.exception.code, expected)

    def select(self, payload: dict) -> dict:
        return brainstorm.select_angles(
            payload,
            self.campaign,
            self.dossier,
            asset_root=ASSET_ROOT,
        )

    def test_selects_primary_and_distinct_backup_after_independent_challenge(
        self,
    ) -> None:
        result = self.select(self.payload())
        self.assertEqual(result["status"], "accepted")
        self.assertEqual(result["research_state"], "NEUTRAL_RESEARCH_FROZEN")
        self.assertEqual(result["challenged_candidate_count"], 4)
        self.assertEqual(
            result["decision_brief"]["primary_angle"]["id"], "connection-1"
        )
        self.assertEqual(result["decision_brief"]["backup_angle"]["id"], "connection-2")
        self.assertNotIn("scorecard", result["decision_brief"])
        self.assertNotIn("falsification_plan", result["decision_brief"])
        packet_text = json.dumps(result["writer_packet"]).casefold()
        for forbidden in (
            "scores",
            "scorecard",
            "frame_id",
            "relationship_mode",
            "critic_session",
            "generator_session",
            "research query",
        ):
            self.assertNotIn(forbidden, packet_text)
        self.assertEqual(
            result["writer_packet_sha256"],
            result["decision_brief"]["writer_packet_sha256"],
        )

    def test_research_query_cannot_be_seeded_with_ritual_or_moment(self) -> None:
        payload = self.payload()
        payload["research_snapshot"]["queries"][2]["query"] = (
            "shared getting-ready ritual moment for perfume and necklace"
        )
        self.assert_code("RESEARCH_CONTAMINATION", lambda: self.select(payload))

    def test_research_query_cannot_search_both_products_together(self) -> None:
        payload = self.payload()
        payload["research_snapshot"]["queries"][2]["query"] = (
            "Auralo Pheromone Perfume Star Burst Necklace customer language"
        )
        self.assert_code("RESEARCH_CONTAMINATION", lambda: self.select(payload))

    def test_prior_free_product_language_cannot_enter_research_or_writer_packet(
        self,
    ) -> None:
        payload = self.payload()
        payload["prior_entity_registry"] = contract.build_prior_entity_registry(
            self.campaign,
            [self.second_campaign],
            self.dossier,
            asset_root=ASSET_ROOT,
        )
        payload["research_snapshot"]["records"][7]["text"] = (
            "Shoppers discussed a quilted shell while comparing accessories."
        )
        self.assert_code("CROSS_CAMPAIGN_LEAK", lambda: self.select(payload))

    def test_candidate_self_scores_are_rejected_and_cannot_control_selection(
        self,
    ) -> None:
        payload = self.payload()
        payload["candidates"][0]["scores"] = {
            field: 5 for field in brainstorm.SCORE_FIELDS
        }
        self.assert_code("ANGLE_REPAIR_REQUIRED", lambda: self.select(payload))

    def test_critic_must_be_independent_from_generators(self) -> None:
        payload = self.payload()
        payload["critic"]["critic_session_id"] = "generator-session-1"
        self.assert_code("CRITIC_NOT_INDEPENDENT", lambda: self.select(payload))

    def test_every_falsification_challenge_must_be_executed(self) -> None:
        payload = self.payload()
        payload["critic"]["challenges"][0]["checks"].pop("forced_pairing")
        self.assert_code("CHALLENGE_NOT_EXECUTED", lambda: self.select(payload))

    def test_failed_forced_pairing_challenge_removes_candidate(self) -> None:
        payload = self.payload()
        row = payload["critic"]["challenges"][0]
        row["checks"]["forced_pairing"] = {
            "status": "fail",
            "finding": "The connection depends on a forced use-together assumption.",
        }
        row["verdict"] = "rejected"
        payload["critic"]["primary_candidate_id"] = "connection-2"
        payload["critic"]["backup_candidate_id"] = "connection-3"
        result = self.select(payload)
        self.assertEqual(
            result["decision_brief"]["primary_angle"]["id"], "connection-2"
        )

    def test_critic_cannot_choose_a_preferred_lower_ranked_candidate(self) -> None:
        payload = self.payload()
        payload["critic"]["primary_candidate_id"] = "connection-3"
        self.assert_code("CRITIC_SELECTION_INVALID", lambda: self.select(payload))

    def test_second_failed_repair_stops_as_angle_gap(self) -> None:
        payload = self.payload(repair_cycle=2)
        payload["candidates"] = payload["candidates"][:3]
        self.assert_code("ANGLE_GAP", lambda: self.select(payload))

    def test_candidate_wording_variants_require_repair(self) -> None:
        payload = self.payload()
        for candidate in payload["candidates"][1:]:
            candidate["sales_argument"] = payload["candidates"][0]["sales_argument"]
        self.assert_code("ANGLE_REPAIR_REQUIRED", lambda: self.select(payload))

    def test_critic_hash_cannot_point_at_a_different_candidate_set(self) -> None:
        payload = self.payload()
        payload["critic"]["candidate_set_sha256"] = "0" * 64
        self.assert_code("CANDIDATE_SET_HASH_MISMATCH", lambda: self.select(payload))

    def test_complement_needs_explicit_dual_product_language_from_two_families(
        self,
    ) -> None:
        payload = self.payload()
        for candidate in payload["candidates"]:
            candidate["relationship_mode"] = "evidence_backed_complement"
            candidate["relationship_evidence_ids"] = ["R-REL-001", "R-REL-002"]
            candidate["evidence_ids"].extend(["R-REL-001", "R-REL-002"])
        snapshot = payload["research_snapshot"]
        snapshot["records"].extend(
            [
                {
                    "id": "R-REL-001",
                    "lane": "relationship",
                    "kind": "explicit_dual_product_language",
                    "target_product_id": "both",
                    "source_family": "forum",
                    "source_url": "https://example.net/direct-language",
                    "text": (
                        "I considered Auralo Pheromone Perfume and Star Burst Necklace in the same purchase."
                    ),
                    "verbatim": True,
                    "explicit_dual_product": True,
                },
                {
                    "id": "R-REL-002",
                    "lane": "relationship",
                    "kind": "explicit_dual_product_language",
                    "target_product_id": "both",
                    "source_family": "social",
                    "source_url": "https://example.org/direct-language",
                    "text": (
                        "Auralo Pheromone Perfume and Star Burst Necklace were both named in my decision."
                    ),
                    "verbatim": True,
                    "explicit_dual_product": True,
                },
            ]
        )
        payload["critic"] = self.critic(snapshot, payload["candidates"])
        result = self.select(payload)
        self.assertEqual(
            result["decision_brief"]["relationship_mode"],
            "evidence_backed_complement",
        )


if __name__ == "__main__":
    unittest.main()
