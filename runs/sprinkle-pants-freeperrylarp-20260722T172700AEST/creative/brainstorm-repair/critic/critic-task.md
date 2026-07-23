# Independent critic

Read only `critic-input.json`. Use a fresh context that generated none of the branches.

Evaluate every idea. Cluster by underlying strategic angle, not wording. Flag attractive traps with a concrete reason. Evidence fit and claim integrity are gates: an unsupported or hypothesis-only conversion idea cannot be primary. Select one primary and one backup, then deepen the top 2 into one implementation brief.

Write JSON only to `critic-output.json` with:

```json
{
  "schema_version": "1.0",
  "critic_session_id": "unique fresh-context identifier",
  "evaluated_branch_ids": ["B-01"],
  "evaluated_idea_ids": ["B-01-I-01"],
  "scores": [{"idea_id":"B-01-I-01","novelty":0,"evidence_fit":0,"buyer_force":0,"cross_product_fit":0,"implementation_fit":0,"claim_integrity":0,"consequence_resilience":0,"trap":"omit or explain"}],
  "clusters": [{"label":"underlying angle","idea_ids":["B-01-I-01"]}],
  "primary_idea_id": "...",
  "backup_idea_id": "...",
  "decision_brief": {"selected_idea_ids":[],"primary_hook":"...","product_relationship":"...","page_argument":"...","section_sequence":["..."],"proof_jobs":["..."],"visual_jobs":["..."],"objection_order":["..."],"public_copy_rules":["..."],"evidence_ids":[],"falsification_plan":"..."},
  "second_order_consequences": ["..."],
  "third_order_consequences": ["..."],
  "rejected_assumptions": ["..."],
  "unresolved_evidence_gaps": []
}
```
