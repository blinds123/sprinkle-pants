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

    def candidate(
        self,
        candidate_id: str,
        hook: str,
        buyer_moment: str,
        *,
        total_bias: int = 0,
        mode: str = "wanted_premium",
    ) -> dict:
        relationship_ids = (
            ["REL-001", "REL-002"] if mode == "evidence_backed_complement" else []
        )
        return {
            "id": candidate_id,
            "relationship_mode": mode,
            "hook": hook,
            "buyer_action": (
                "Apply the scent, fasten the necklace, and leave for the evening."
            ),
            "buyer_moment": buyer_moment,
            "transaction_bridge": (
                "Choose Auralo Pheromone Perfume for $29 and receive the "
                "Star Burst Necklace FREE as the visible finishing piece."
            ),
            "product_roles": {
                "paid": "Auralo Pheromone Perfume is the $29 floral-amber scent she chooses.",
                "free": "Star Burst Necklace is the wanted visible piece included FREE.",
            },
            "substitution_test": {
                "question": "Do the scent and necklace retain distinct, material buyer roles?",
                "result": "passed",
                "evidence_ids": [
                    "AURALO-IDENTITY-001",
                    "FREE-IDENTITY-001",
                ],
            },
            "evidence_ids": [
                "AURALO-IDENTITY-001",
                "FREE-IDENTITY-001",
                *relationship_ids,
            ],
            "relationship_evidence_ids": relationship_ids,
            "scores": {
                "paid_product_desire": 4,
                "free_product_desire": 5,
                "first_touch_clarity": 5,
                "buyer_moment_specificity": 5,
                "transaction_bridge_credibility": 4,
                "evidence_fit": 5,
                "claim_integrity": 5,
                "creative_distinctiveness": 4 + total_bias,
            },
            "falsification_plan": (
                "Reject the angle if current evidence cannot support both named roles."
            ),
        }

    def payload(self, repair_cycle: int = 0) -> dict:
        return {
            "repair_cycle": repair_cycle,
            "candidates": [
                self.candidate(
                    "signature-before-words",
                    "What if your signature arrived before you said a word?",
                    "She is choosing her last details before an evening out.",
                    total_bias=0,
                ),
                self.candidate(
                    "star-bright-finish",
                    "A $29 scent with a star-bright finish included.",
                    "She is dressing for a dinner where she wants one memorable detail.",
                    total_bias=-1,
                ),
            ],
        }

    def assert_code(self, expected: str, callback) -> None:
        with self.assertRaises(contract.ContractError) as raised:
            callback()
        self.assertEqual(raised.exception.code, expected)

    def test_selects_primary_and_distinct_backup(self) -> None:
        result = brainstorm.select_angles(
            self.payload(),
            self.campaign,
            self.dossier,
        )
        self.assertEqual(result["status"], "accepted")
        self.assertEqual(
            result["decision_brief"]["primary_angle"]["id"],
            "signature-before-words",
        )
        self.assertEqual(
            result["decision_brief"]["backup_angle"]["id"],
            "star-bright-finish",
        )

    def test_low_claim_integrity_requires_repair(self) -> None:
        payload = self.payload()
        payload["candidates"][0]["scores"]["claim_integrity"] = 2
        payload["candidates"][1]["scores"]["claim_integrity"] = 2
        self.assert_code(
            "ANGLE_REPAIR_REQUIRED",
            lambda: brainstorm.select_angles(
                payload,
                self.campaign,
                self.dossier,
            ),
        )

    def test_second_failed_repair_stops_as_angle_gap(self) -> None:
        payload = self.payload(repair_cycle=2)
        payload["candidates"][0]["scores"]["evidence_fit"] = 1
        payload["candidates"][1]["scores"]["evidence_fit"] = 1
        self.assert_code(
            "ANGLE_GAP",
            lambda: brainstorm.select_angles(
                payload,
                self.campaign,
                self.dossier,
            ),
        )

    def test_repair_count_above_two_stops_immediately(self) -> None:
        self.assert_code(
            "ANGLE_GAP",
            lambda: brainstorm.select_angles(
                self.payload(repair_cycle=3),
                self.campaign,
                self.dossier,
            ),
        )

    def test_complement_candidate_requires_two_relationship_rows(self) -> None:
        payload = self.payload()
        for candidate in payload["candidates"]:
            candidate["relationship_mode"] = "evidence_backed_complement"
            candidate["relationship_evidence_ids"] = ["REL-001"]
        self.assert_code(
            "MARRIAGE_GAP",
            lambda: brainstorm.select_angles(
                payload,
                self.campaign,
                self.dossier,
            ),
        )

    def test_evidence_backed_complement_can_pass(self) -> None:
        payload = {
            "repair_cycle": 0,
            "candidates": [
                self.candidate(
                    "visible-and-close",
                    "One detail catches the light; another stays close.",
                    "She is choosing visible and close-range details before dinner.",
                    mode="evidence_backed_complement",
                ),
                self.candidate(
                    "collarbone-and-pulse",
                    "A star at the collarbone, a floral-amber scent at the wrist.",
                    "She fastens the necklace and applies scent before leaving.",
                    mode="evidence_backed_complement",
                ),
            ],
        }
        result = brainstorm.select_angles(payload, self.campaign, self.dossier)
        self.assertEqual(
            result["decision_brief"]["relationship_mode"],
            "evidence_backed_complement",
        )

    def test_generic_bridges_fail_as_marriage_gap(self) -> None:
        payload = self.payload()
        for candidate in payload["candidates"]:
            candidate["transaction_bridge"] = (
                "Put two popular choices into one easy transaction."
            )
        self.assert_code(
            "MARRIAGE_GAP",
            lambda: brainstorm.select_angles(
                payload,
                self.campaign,
                self.dossier,
            ),
        )

    def test_wording_variant_backup_requires_repair(self) -> None:
        payload = self.payload()
        payload["candidates"][1]["hook"] = payload["candidates"][0]["hook"]
        payload["candidates"][1]["buyer_moment"] = payload["candidates"][0][
            "buyer_moment"
        ]
        self.assert_code(
            "ANGLE_REPAIR_REQUIRED",
            lambda: brainstorm.select_angles(
                payload,
                self.campaign,
                self.dossier,
            ),
        )


if __name__ == "__main__":
    unittest.main()
