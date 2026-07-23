# Isolated divergent branch B-04

Read only the sibling `story-visual-sequence.input.json` file. Do not read any other branch task or output.

You are a generator, not a critic. Generate 4 structurally distinct ideas through the assigned constraint lens. Do not rank, score, hedge, or choose. Push beyond the first obvious answers while staying inside the fixed commercial and product-truth constraints.

Cite only allowed IDs from the input. If an idea is speculative, set hypothesis_only=true.

Write JSON only to `story-visual-sequence.output.json` with:

```json
{
  "schema_version": "1.0",
  "branch_id": "B-04",
  "frame_id": "story-visual-sequence",
  "isolation_session_id": "a unique fresh-context identifier",
  "problem_sha256": "the value from the input",
  "input_sha256": "ae9de1a6541d30dfd658cd081e07e0357e1685cb85a37682a858ed63ee78fe11",
  "observed_other_branch_ids": [],
  "ideas": [
    {
      "id": "B-04-I-01",
      "text": "one concise candidate",
      "rationale": "one concise reason",
      "hypothesis_only": false,
      "evidence_ids": []
    }
  ]
}
```
