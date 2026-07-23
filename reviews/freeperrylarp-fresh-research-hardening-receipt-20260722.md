# FreePerryLarp Fresh-Research Hardening Receipt

Date: 2026-07-22 (Australia/Sydney)

## Installed release

- Plugin: `freeperrylarp@personal`
- Version: `0.1.0+codex.20260722064807`
- Source: `/Users/nelsonchan/plugins/freeperrylarp`
- Installed cache: `/Users/nelsonchan/.codex/plugins/cache/personal/freeperrylarp/0.1.0+codex.20260722064807`
- Enabled: yes

## Fresh-only contract

- Every `init` creates a random research-session ID and a `research_not_before` timestamp.
- Every `research-plan` binds the Last30Days plan and official-reference plan to that session and records both plan hashes.
- `research-run` executes Last30Days from the current plan and writes the raw artifact only inside the current run.
- `research-ingest` rejects external raw JSON, missing receipts, raw-hash drift, plan-hash drift, another run's session ID, pre-session generation timestamps, and a stale research range.
- Official free-product evidence must use the current session ID, current competitor-plan hash, a post-session capture time, `fresh_research: true`, and `reused_prior_facts: false`.
- Exa recovery must use the current session ID, current recovery-plan hash, and a post-session generation time.
- Campaign input rejects embedded prior research fields such as evidence, buyer language, research briefs, source counts, and prior research artifacts.
- Current product identity, official URL, reference image, and supplied comments remain allowed as query seeds. They do not become retrieved evidence or authorized product facts by themselves.
- Free-product facts become usable only after exact mapping to the new current-session official-reference capture.

## Verification

- Source skill validation: pass
- Source plugin validation: pass
- Source tests: 45 passed (`Ran 45 tests in 33.858s — OK`)
- Installed-cache skill validation: pass
- Installed-cache plugin validation: pass
- Installed-cache tests: 45 passed (`Ran 45 tests in 32.114s — OK`)
- Negative coverage proves rejection of external old raw research, missing current receipts, mismatched research sessions, and stale generation timestamps.
- Execution coverage proves `research-run` launches the current plan, produces an in-run artifact, binds its receipt, and refuses a second retrieval in the same run so a new campaign run is required.
- Actual Sprinkle Pants canary: the installed plugin initialized the supplied pants campaign with fresh session `a67f54e173004872a856eec72e958552` and freshness boundary `2026-07-22T06:50:23Z`, then rejected the older FreePerry30Days pants raw artifact with exit code 2: `Last30Days research must be generated inside this run; prior or external raw artifacts are forbidden`.

## Source/cache parity

- Included files per tree: 30
- Source SHA-256: `c88031133ebc691f8d8d8408f88836a5f584e65bf6ca33d78cc3108278499fc5`
- Installed-cache SHA-256: `c88031133ebc691f8d8d8408f88836a5f584e65bf6ca33d78cc3108278499fc5`
- Result: `BYTE_PARITY=PASS`
- Hash scope excludes generated `__pycache__` directories and `.pyc` files.

## Honest boundary

This release hardens the plugin. It does not claim that the new plugin has already rerun the Sprinkle Pants campaign. The next real pants workflow must start a new run and retrieve its own current Last30Days, official-reference, and any bounded Exa evidence before copy or prompts can advance.
