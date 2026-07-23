# Issue 1 foundation validation receipt

- Issue: `blinds123/sprinkle-pants#1`
- Branch: `codex/issue-001-freeperrylarp1-foundation`
- Scope: parallel `freeperrylarp1` contract foundation only
- Plugin version: `0.2.0`
- Fixed paid product: Auralo Pheromone Perfume, 15 ml, `$29`
- Global activation: intentionally not performed before review and human merge

## Immutable evidence

- Auralo dossier version: `auralo-pheromone-perfume-v1`
- Canonical dossier SHA-256: `375f9f95d6674261b8ca8a99e3cd7daa3887d3446812c14a2d1b430ac0f474d9`
- Auralo reference image SHA-256: `1781cd27811a984a89290722966742f5cb18084fcd78905515df1ad19fd9973d`
- Star Burst fixture campaign SHA-256: `cc76c070c4aad746fe8953cf200e71d2c8f6d3d5007289a11e154bb73d7be901`
- Star Burst fixture reference SHA-256: `03a2ee50ce977a252fc6ea0119b41ba5755f863205fe17b2a123024a0b842864`
- Cloud Travel Case fixture campaign SHA-256: `bc721c231a13d608be339e3775ecf77d278e6cd3936dd379e3dbd668e72cbd01`
- Cloud Travel Case fixture reference SHA-256: `90cc9e73a202b5a31fa967d0e31e4e468251d9c4fc3eddd994a8121727b49d45`
- Predecessor installed manifest SHA-256 observed before this change: `461bbfcdbe1487e14cd08177acafe37950b60d798757abc86e218d171e640422`

## Automated verification

All commands were run from the clean Issue 1 worktree.

| Check | Result |
| --- | --- |
| `ruff check plugins/freeperrylarp1` | PASS |
| `ruff format --check plugins/freeperrylarp1` | PASS |
| `python3 -m compileall -q plugins/freeperrylarp1` | PASS |
| `python3 -m unittest discover -s plugins/freeperrylarp1/tests -p 'test_*.py' -v` | PASS, 64 tests |
| Repository validator | PASS |
| Plugin manifest validator | PASS |
| Main skill validator | PASS |
| Brainstorm skill validator | PASS |
| `validate-dossier` CLI | PASS |
| `validate-campaign` CLI, Star Burst | PASS |
| `validate-campaign` CLI, Cloud Travel Case | PASS |
| Paid/FREE restatement canary | `MARRIAGE_GAP` |
| Unrelated valid evidence claim canary | `CLAIM_NOT_AUTHORIZED` |
| Swapped `$29` / `15 ml` fact canary | `CLAIM_NOT_AUTHORIZED` |
| Generic paid/FREE prompt placeholder canary | `CROSS_CAMPAIGN_LEAK` |
| Unsupported prompt-outcome canary | `CLAIM_NOT_AUTHORIZED` |
| Reversed use-instruction fragment canary | `CLAIM_NOT_AUTHORIZED` |
| Cross-product fact-ownership canary | `CLAIM_NOT_AUTHORIZED` |
| Inverted `$29`/FREE offer-role canary | `CLAIM_NOT_AUTHORIZED` |
| Relationship-scope price/partial-owner canary | `CLAIM_NOT_AUTHORIZED` |
| Partial-name identity-swap canary | `CLAIM_NOT_AUTHORIZED` |
| Fabricated five-star proof canary | `CLAIM_NOT_AUTHORIZED` |
| Traversal FREE-reference path canary | `CAMPAIGN_ASSET_INVALID` |
| Missing FREE-reference file canary | `CAMPAIGN_ASSET_INVALID` |
| Mismatched FREE-reference hash canary | `CAMPAIGN_ASSET_INVALID` |
| Ritual/moment-seeded research query canary | `RESEARCH_CONTAMINATION` |
| Both-products-in-one-neutral-query canary | `RESEARCH_CONTAMINATION` |
| Prior FREE-product language in research canary | `CROSS_CAMPAIGN_LEAK` |
| Candidate-owned score canary | `ANGLE_REPAIR_REQUIRED` |
| Reused generator/critic session canary | `CRITIC_NOT_INDEPENDENT` |
| Missing executed challenge canary | `CHALLENGE_NOT_EXECUTED` |
| Wrong candidate-set hash canary | `CANDIDATE_SET_HASH_MISMATCH` |
| Page/image mapping before accepted copy canary | `COPY_NOT_FINAL` |
| Finished-copy hash mismatch canary | `COPY_HASH_MISMATCH` |
| Writer self-review canary | `COPY_REVIEW_NOT_INDEPENDENT` |
| Wrong clean-writer-packet hash canary | `WRITER_PACKET_MISMATCH` |
| Generic AI pairing glue canary | `CROSS_CAMPAIGN_LEAK` |
| Incomplete image mapping canary | `PAGE_MAPPING_INVALID` |
| Image job with non-copy source path canary | `COPY_NOT_FINAL` |
| `git diff --check` | PASS |

## Acceptance and non-goal ledger

| Contract item | Evidence |
| --- | --- |
| AC-1 | New files are isolated under `plugins/freeperrylarp1`; the predecessor plugin is unchanged. |
| AC-2 | Versioned dossier and reference asset are hash-verified; only enumerated fact IDs may support public claims. |
| AC-3 | Campaign input requires a fresh free-product identity, evidence ledger, fact ledger, and reference images. References must exist under an explicit campaign asset root, remain inside that root, avoid symlinks, and match their declared SHA-256. There are no prior-campaign defaults or examples in writer-facing assets. |
| AC-4 | Neutral paid/FREE/customer/objection/purchase-trigger research is frozen before ideation. At least four isolated generators produce materially different connections; a different critic session scores and challenges all candidates. The accepted marriage brief is bound to the research, candidate set, critic, and clean writer packet hashes. Candidate self-scores, token overlap, paid/FREE restatements, and inferred relationship evidence cannot select the result. |
| AC-5 | Angle repair attempts are capped at two; unresolved failures stop as `ANGLE_GAP` or `MARRIAGE_GAP`. |
| AC-6 | The validator-only prior-product registry now guards research and candidate inputs before writer-packet creation as well as public/prompt outputs. Strategy text, generic AI glue, generic placeholders, and stale entities stop as `CROSS_CAMPAIGN_LEAK`. |
| AC-7 | Production direction is permitted only in non-visible fields; every visible-text field is treated as customer-facing copy. Each image job is bound to exact finished-copy paths after independent copy review. |
| AC-8 | Every public text leaf is exactly bound to a typed claim path, required evidence lanes, and exact cited evidence fragments whose co-occurring factual order and product ownership must be preserved. Paid facts and `$29` stay attached to Auralo; FREE facts and the `FREE` label stay attached to the exact current FREE product. Relationship scope cannot carry commercial markers, partial product ownership, or unanchored cross-lane identity assignments. Public and prompt content share the outcome and fabricated-proof firewalls; questions, asterisks, disclosures, unrelated valid IDs, swapped fact values, scope laundering, role inversions, reversed instructions, and rating decoration cannot authorize new claims. |
| AC-9 | Two unrelated-product fixtures plus adversarial tests prove neutral-research contamination, prior-product research leakage, candidate self-scoring, critic reuse, skipped challenge, candidate-hash drift, generic AI glue, premature mapping, stale-entity, missing-marriage, hidden-field, unsupported-claim, and private-strategy rejection. |
| AC-10 | This receipt records the deterministic test and validation envelope. |
| NG-1 | No predecessor-plugin files were edited. |
| NG-2 | No campaign images, landing page, or deployment were produced. |
| NG-3 | No third-party testimonial, outcome, rating, or badge was transferred into the evidence ledger. |
| NG-4 | `freeperrylarp1` was not globally installed or activated before independent review and human merge. |

Highest honestly earned state: `ISSUE_1_FOUNDATION_VALIDATED`.
