# FreePerryLarp Gate 1 — Evidence Audit and First Plan

Date: 2026-07-22 (Australia/Sydney)  
Status: `GATE_1_RESEARCH_COMPLETE`  
Implementation status: `NOT_STARTED`  
Approval required before Gate 2: **yes**

## Scope and honesty boundary

This is a research-backed design review and a proposed first plan. It does **not** claim that Perry Belcher, Russell Brunson, or Alex Hormozi reviewed this plugin, endorsed the recommendations, or predicted that they will convert. Their public teachings are used only as clearly identified strategic lenses. Conversion can be established only by measured traffic and experiments.

No `freeperrylarp` plugin has been created. The existing `freeperry30days` source, installation, current Sprinkle Pants page, images, checkout mode, and Netlify deployment have not been modified in Gate 1.

## Executive verdict

The existing plugin is technically disciplined but commercially under-modelled for a two-product offer. Its strongest assets are deterministic release mechanics, prompt-pack constraints, image ordering, source/install parity, preview safety, and multi-viewport QA. Those should be selectively ported rather than rewritten.

The largest conversion problem is not simply “too little copy.” The page has no formal model for why a buyer should want the paid perfume and the premium pants in the same transaction. The current story and proof system disproportionately sells the pants, while the buyer pays for the perfume. Adding more generic sections would make the page longer without resolving that mismatch.

The recommended upgrade is a truth-gated, dual-product system that:

1. researches and proves each product separately;
2. earns an explicit relationship between them;
3. leads with one transaction-aligned promise;
4. uses one connected Hook → Story → Offer progression rather than many disconnected frameworks;
5. treats proof as a typed, evidence-backed asset rather than generated testimonials;
6. measures the funnel before calling it optimized.

## What the evidence says

### Plugin health

- Source: `/Users/nelsonchan/plugins/freeperry30days`
- Installed copy: `/Users/nelsonchan/.codex/plugins/cache/personal/freeperry30days/0.4.0+codex.20260721231545`
- Source/install parity: `PASS`
- Compared file count: `29 / 29`
- Tree SHA-256: `4a6ca3e9695477d162ce38f0b12848f25dcbb81bbeacea40c87d03046674f7b7`
- Unit tests: `43 passed`
- Ruff: `PASS`
- Quick validator: `PASS`
- Plugin validator: `PASS`

This means the release core is worth preserving. The redesign should focus on the campaign model, research gates, offer logic, copy/proof contracts, and page semantics.

### Current campaign truth and research gaps

The current campaign contains authorized pants facts but has no `paid_product_truth` ledger and no `relationship` evidence object for the perfume-plus-pants transaction. The research query plan is almost entirely pants-focused.

The research sufficiency gate passes by counts even though accepted evidence contains off-segment and unusable material, including a J.Jill linen top, a car-showroom phrase, a men's-pants item, and a malformed sentence. This proves the current gate can be count-rich but meaning-poor.

Relevant files:

- `/Users/nelsonchan/Documents/Sprinkle pants/campaigns/sprinkle-pants-20260721T163126AEST/campaign.json`
- `/Users/nelsonchan/Documents/Sprinkle pants/runs/sprinkle-pants-20260721T163126AEST/research/query-plan.json`
- `/Users/nelsonchan/Documents/Sprinkle pants/runs/sprinkle-pants-20260721T163126AEST/research/brief.json`

### Current page findings

The live and local page bytes match. The page is a noindex client preview with a dry-run checkout. It clearly introduces the $29 perfume in the main headline, but most of the subsequent desire, stories, image rails, and final close sell the pants. On mobile, the header CTA says `GET IT FREE`, even though the transaction is a $29 perfume purchase.

The page includes 24 first-person sample-story cards. A footer disclosure does not neutralize the customer-review impression created much earlier on the page. The production system must not convert fictional or illustrative stories into apparent customer proof.

The page has no conversion instrumentation, so neither “optimized” nor “high converting” is presently proven.

### Fresh Last30Days research receipt

- Topic: `OpenAI Codex plugin and skill architecture for deterministic ecommerce landing-page workflows`
- Evidence items: `210`
- Raw research SHA-256: `c0d0047a8aa709028e2b2443152d82a8e9084355d905fd5754a4c81d1dc93b4e`
- Query-plan SHA-256: `5a018e32c72a9d6cac9f83a928383253dd80df0c46300d11493a85452ad035ab`
- Raw report: `/Users/nelsonchan/Documents/Sprinkle pants/research/freeperrylarp/openai-codex-plugin-and-skill-architecture-for-deterministic-ecommerce-landing-page-workflows-raw-freeperrylarp-gate1.md`
- Query plan: `/Users/nelsonchan/Documents/Sprinkle pants/research/freeperrylarp/last30days-plan.json`

The LLM reranker and “fun judge” returned HTTP 400, so the run used the local fallback. Instagram was partial after an HTTP 500. These limits are recorded rather than hidden. The useful cross-source signal was a preference for reusable workflows, explicit checkpoints, deterministic validation, and verification over disconnected prompt collections. Engagement around several architecture-specific items was weak, so those items are directional rather than authoritative.

### Protocol findings

Official Codex guidance supports a small manifest, progressive-disclosure skills, deterministic scripts for repeatable work, and creator scaffolds for new plugins and skills. The current online manual shows a `hooks` manifest field, while the installed local plugin-creator specification rejects that field. Gate 2 should follow the local installed validator unless a minimal isolated canary proves the newer contract is supported. Hooks are unnecessary for the proposed workflow.

Sources:

- OpenAI, [Plugins in Codex](https://help.openai.com/en/articles/20001256-plugins-in-codex/)
- OpenAI, [Codex for every role and workflow](https://openai.com/index/codex-for-every-role-tool-workflow/)
- OpenAI, [Open-sourcing Codex orchestration with Symphony](https://openai.com/index/open-source-codex-orchestration-symphony/)
- OpenAI, [skill-creator sample](https://github.com/openai/codex/blob/main/codex-rs/skills/src/assets/samples/skill-creator/SKILL.md)

## The marketer-lens synthesis

These are interpretations of public teachings, not simulated quotes or claimed participation.

### Perry Belcher lens

The first purchase should be low-risk and logically framed. A premium can be a wanted incentive even when it is not functionally required, but the paid item must still identify a real market and carry enough perceived value to support the transaction. The page needs to make the risk/reward exchange obvious and test the earliest funnel bottleneck.

Implication: do not invent a functional reason the buyer “needs both.” Choose and support one relationship mode:

- `wanted_premium`: the pants are a highly desired reward for buying the perfume; or
- `complementary_bundle`: both contribute to one credible use occasion.

### Russell Brunson lens

The page needs one macro Hook → Story → Offer sequence. The story should carry the buyer from their present state to the offer, not become a decorative biography or a collection of unrelated frameworks.

Implication: use one Big Domino, one buyer-as-hero story bridge, and transaction-aligned calls to action. ENGAGE and FIBS can guide internal drafting, but those labels must never appear in public copy.

### Alex Hormozi lens

Increase the perceived dream outcome and confidence while reducing delay and effort, but only with supported facts. Stack what the buyer actually receives, answer real objections, and use genuine risk reversal.

Implication: do not call the result a “Grand Slam Offer” until paid-product truth, credible economics, proof, and measured response support it. A disclaimer does not make unsupported product-performance, scarcity, testimonial, or guarantee claims safe.

### Combined decision

The three lenses converge on a shorter and more coherent sales argument, not maximum page length:

> **One desired outcome → one reason the paid product matters → one honest reason the premium belongs → one transparent transaction → one supported close.**

## Proposed page changes

### Current page with existing images frozen

Use compatibility mode `legacy_39_locked`:

- Keep all 39 current images and their ordering.
- Add one compact, text-first `offer_bridge` directly after the hero.
- Give the paid perfume a concise reason-to-buy section before deep pants desire.
- Explain the premium relationship without claiming that both products are necessary.
- Replace ambiguous `GET IT FREE` CTAs with transaction-aligned wording such as `GET THE $29 PERFUME + PANTS BONUS`, subject to verified terms.
- Replace apparent testimonials with either verified customer proof or clearly adjacent-labelled editorial scenarios.
- Bring material terms and disclosures close to the claims they qualify.
- Rewrite the final close around the complete transaction, not “make the trousers the statement.”

### Future campaigns

Use compatibility mode `conversion_39_v5`. Preserve the 39-image production/import contract, but change its semantic allocation:

- Story rail 1–15: reveal, buyer moment, paid-product reason, paid truth, paid use, premium desire, relationship, evidence, stack, terms, objection, order, close.
- Proof rail 1: paid-product desire and evidence.
- Proof rail 2: companion-product desire, fit, and use.
- Proof rail 3: relationship and credible scenarios.
- Proof rail 4: verified proof, decision support, and terms. If verified proof is absent, render editorial evidence/scenarios—never simulated customer testimonials.

This maintains the existing image workflow while preventing all four rails from becoming repetitive fictional reviews.

## Research and truth model changes

Every campaign should have three research lanes:

1. `paid_product`: demand, mechanisms, objections, proof, claims, compliance, and offer terms;
2. `companion_product`: demand, fit/use questions, objections, proof, and claims;
3. `relationship`: buyer overlap, purchase occasion, vocabulary overlap, and evidence for `wanted_premium` or `complementary_bundle`.

Required machine gates:

- dual product-truth ledgers;
- source-backed commercial terms;
- subject quotas by lane, not global counts;
- semantic-role checks for context, voice, objection, and purchase signal;
- gibberish, off-segment, and unrelated-product rejection;
- relationship evidence threshold;
- claim-to-source mapping;
- proof-mode declaration;
- earned urgency, guarantee, and scarcity checks.

Proposed honest states:

- `PAID_PRODUCT_TRUTH_MISSING`
- `PAID_RESEARCH_GAP`
- `COMPANION_RESEARCH_GAP`
- `RELATIONSHIP_NOT_EARNED`
- `PRODUCTION_PROOF_MISSING`
- `URGENCY_NOT_EARNED`
- `ECONOMICS_NOT_VALIDATED`
- `CONVERSION_NOT_MEASURED`

## Proposed plugin architecture

Create `/Users/nelsonchan/plugins/freeperrylarp` from the current creator scaffold, then selectively port tested FreePerry30Days mechanics. Do not clone the old tree wholesale.

Suggested runtime modules:

- `core.py`: campaign schema, state machine, provenance;
- `research.py`: three-lane research and semantic acceptance;
- `offer.py`: relationship mode, value stack, economics, objections, risk reversal;
- `creative.py`: connected narrative, claim-safe copy, proof typing;
- `prompts.py`: 39-job map, four packs, references, compactness guard;
- `site.py`: compatibility layouts and transparent CTAs;
- `qa.py`: semantic, compliance, responsive, and checkout checks;
- `release.py`: install parity, deployment, live QA, receipts.

Suggested small referenced contracts:

- intake and dual-product truth;
- research acceptance;
- offer relationship and economics;
- copy and proof modes;
- page architecture;
- prompt/image production;
- QA and release.

Suggested templates/assets:

- paid-product truth ledger;
- companion-product truth ledger;
- relationship evidence record;
- claims matrix;
- offer economics record;
- experiment plan;
- `legacy_39_locked` and `conversion_39_v5` visual maps.

Keep the top-level skill concise. Route into phase runbooks and deterministic scripts so the agent does not have to hold the whole workflow in context.

## 40-minute feasibility

The existing plugin advertises a 34-minute target and a 46-minute maximum. The strict “40 minutes or less” outcome cannot be guaranteed because research services, image generation, user downloads, Netlify, and live-browser review are external-latency surfaces.

A healthy-path target can be engineered and measured:

| Phase | Budget |
|---|---:|
| Intake and preflight | 2 min |
| Three-lane research and truth gates | 6 min |
| Offer synthesis and one writer pass | 5 min |
| Review and prompt-pack compile | 3 min |
| External image production/download | 10 min |
| Import, build, and checkout wiring | 4 min |
| Local QA | 3 min |
| Deploy and smoke test | 3 min |
| Live QA and host receipt | 4 min |
| **Healthy-path total** | **40 min** |

The workflow must record machine time, external waiting time, and human waiting time separately. “Under 40 minutes” becomes a measured service-level target after repeated successful runs, never an unconditional completion claim.

## Material concerns to resolve before implementation

1. **Production proof:** the current 24 illustrative first-person stories cannot remain as apparent testimonials in a production page.
2. **Disclaimer misconception:** a footer disclaimer does not authorize unsupported claims, fake reviews, fake urgency, or misleading scarcity.
3. **Paid-product truth:** the perfume lacks a campaign-level truth ledger and product-specific claim evidence.
4. **Research acceptance:** current count gates accept irrelevant and malformed evidence.
5. **Offer relationship:** the perfume-plus-pants relationship has not yet been earned by evidence.
6. **Commercial terms:** shipping, returns, warranty, price, and checkout destination need source provenance.
7. **CTA truth:** `GET IT FREE` conflicts with a $29 paid transaction.
8. **Checkout scope:** the current site is a dry-run noindex preview. The default remains dry-run until the user explicitly authorizes a live purchase endpoint.
9. **Measurement:** there is no CTA, size, checkout-open, checkout-completion, or drop-off instrumentation.
10. **Urgency:** no fake countdown, stock, or deadline may be generated. Urgency requires a verifiable source.
11. **Forty-minute promise:** treat it as a healthy-path target until instrumented runs demonstrate it.
12. **Regression risk:** wholesale copying or rewriting could break currently accepted prompt, release, and live-QA mechanics.
13. **Protocol drift:** online and locally installed manifest-hook rules currently differ; local validation wins unless a canary proves otherwise.
14. **Page bloat:** more storytelling and more sections can lower scanability if they do not advance the transaction.
15. **Cosmetics claims:** attraction, pheromone, performance, and outcome claims require product-specific support; the product name alone is not evidence.
16. **Traffic context:** the first-touch default should be declared as cold social/TikTok traffic, but remain configurable.
17. **Image compatibility:** current imagery should be preserved through `legacy_39_locked`; semantic reallocation applies only to future campaigns.
18. **Attribution honesty:** the three marketer roles are analytical lenses, not real reviewers or endorsements.
19. **Preservation:** the original plugin and current deployment must remain untouched until the successor passes parity and release gates.
20. **Installation:** a fresh task/app restart may be required before a newly installed plugin is available in the active skill list.

## First implementation plan — proposed, not yet authorized

### Phase 1: Scaffold and freeze contracts

- Create `freeperrylarp` from the official local plugin scaffold.
- Pin an inventory and hashes for source materials selected from FreePerry30Days.
- Add compatibility contracts and fail-closed state names.
- Verify the original source/install tree remains unchanged.

Exit: scaffold validates; no campaign build attempted.

### Phase 2: Truth, research, and offer engine

- Add dual truth ledgers and the three research lanes.
- Replace count-only research acceptance with subject and semantic-role gates.
- Add relationship modes, claim mapping, commercial-term provenance, proof modes, and honest failure states.
- Unit-test the current bad evidence as rejection fixtures.

Exit: irrelevant evidence, unsupported pairing, and missing paid truth fail closed.

### Phase 3: Creative and page contracts

- Add the connected narrative and transaction-alignment validator.
- Implement `legacy_39_locked` and `conversion_39_v5`.
- Remove production reliance on illustrative testimonials.
- Add proof typing, local disclosure placement, transparent CTAs, offer bridge, and complete-transaction close.
- Preserve four prompt packs, 10/10/10/9 split, reference images, and 220-word maximum.

Exit: deterministic fixtures pass semantic, truth, prompt, and responsive contracts.

### Phase 4: Measurement, release, and parity

- Add privacy-conscious funnel event hooks and an experiment plan.
- Preserve WebP import, dry-run checkout default, Netlify fresh-site behavior, 390/768/1440 QA, host review, and exact site-ID receipts.
- Validate source, cache, and installed parity; test from a fresh task.

Exit: plugin is installed and callable, with no completion state above what evidence earns.

### Phase 5: Pilot and timing proof

- Run one fixture campaign and then the Sprinkle Pants campaign in compatibility mode.
- Do not alter the current live page until the new output passes side-by-side semantic, visual, checkout, and release review.
- Record active time versus provider/human wait time.
- Promote only if all validators pass; otherwise retain the original deployment and report the exact blocker.

Exit: evidence-backed pilot receipt and measured timing, not a prediction.

## Approval gate

Gate 1 is ready for review. If approved, Gate 2 begins with a new scaffold and tests; it will not touch the existing live page. The default assumptions are:

- cold social/TikTok first-touch traffic;
- current images frozen in `legacy_39_locked` mode;
- dry-run/noindex checkout behavior until explicit live-checkout authorization;
- verified proof only in production;
- no unsupported perfume, urgency, scarcity, or guarantee claims;
- original `freeperry30days` preserved as rollback.

