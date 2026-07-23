# Issue 1 foundation validation receipt

- Issue: `blinds123/sprinkle-pants#1`
- Branch: `codex/issue-001-freeperrylarp1-foundation`
- Scope: parallel `freeperrylarp1` contract foundation only
- Fixed paid product: Auralo Pheromone Perfume, 15 ml, `$29`
- Global activation: intentionally not performed before review and human merge

## Immutable evidence

- Auralo dossier version: `auralo-pheromone-perfume-v1`
- Canonical dossier SHA-256: `375f9f95d6674261b8ca8a99e3cd7daa3887d3446812c14a2d1b430ac0f474d9`
- Auralo reference image SHA-256: `1781cd27811a984a89290722966742f5cb18084fcd78905515df1ad19fd9973d`
- Star Burst fixture campaign SHA-256: `c6bfd4f12c8d70773a351834d5e9dfe7db18642a2ac7681f75d2cdb6578db9ea`
- Cloud Travel Case fixture campaign SHA-256: `374d16fc51dc61cddec95311b375fc76e92bbc670b1e9b550c7248a81d078c64`
- Predecessor installed manifest SHA-256 observed before this change: `461bbfcdbe1487e14cd08177acafe37950b60d798757abc86e218d171e640422`

## Automated verification

All commands were run from the clean Issue 1 worktree.

| Check | Result |
| --- | --- |
| `ruff check plugins/freeperrylarp1` | PASS |
| `ruff format --check plugins/freeperrylarp1` | PASS |
| `python3 -m compileall -q plugins/freeperrylarp1` | PASS |
| `python3 -m unittest discover -s plugins/freeperrylarp1/tests -p 'test_*.py' -v` | PASS, 43 tests |
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
| `git diff --check` | PASS |

## Acceptance and non-goal ledger

| Contract item | Evidence |
| --- | --- |
| AC-1 | New files are isolated under `plugins/freeperrylarp1`; the predecessor plugin is unchanged. |
| AC-2 | Versioned dossier and reference asset are hash-verified; only enumerated fact IDs may support public claims. |
| AC-3 | Campaign input requires a fresh free-product identity, evidence ledger, fact ledger, and reference images. There are no prior-campaign defaults or examples in writer-facing assets. |
| AC-4 | Campaign validation requires an accepted, hash-bound marriage brief with exact product roles, primary and backup angles, a current-evidence buyer bridge, and a replacement-based substitution explanation. Paid/FREE restatements stop as `MARRIAGE_GAP`. |
| AC-5 | Angle repair attempts are capped at two; unresolved failures stop as `ANGLE_GAP` or `MARRIAGE_GAP`. |
| AC-6 | Validator-only prior-product registry and public/prompt scans stop strategy text, generic placeholders, and stale entities as `CROSS_CAMPAIGN_LEAK`. |
| AC-7 | Production direction is permitted only in non-visible fields; every visible-text field is treated as customer-facing copy. |
| AC-8 | Every public text leaf is exactly bound to a typed claim path, required evidence lanes, and exact cited evidence fragments. Public and prompt content share the outcome firewall; questions, asterisks, disclosures, unrelated valid IDs, and swapped fact values cannot authorize new claims. |
| AC-9 | Two unrelated-product fixtures plus negative tests prove stale-entity, missing-marriage, hidden-field, unsupported-claim, and private-strategy rejection. |
| AC-10 | This receipt records the deterministic test and validation envelope. |
| NG-1 | No predecessor-plugin files were edited. |
| NG-2 | No campaign images, landing page, or deployment were produced. |
| NG-3 | No third-party testimonial, outcome, rating, or badge was transferred into the evidence ledger. |
| NG-4 | `freeperrylarp1` was not globally installed or activated before independent review and human merge. |

Highest honestly earned state: `ISSUE_1_FOUNDATION_VALIDATED`.
