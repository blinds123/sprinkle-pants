# FreePerryLarp Gate 2 — Implementation Plan

Date: 2026-07-22  
Authorization: approved by user  
Target source: `/Users/nelsonchan/plugins/freeperrylarp`  
Original preserved: `/Users/nelsonchan/plugins/freeperry30days`

## Objective

Create a compact successor plugin that can take Auralo Pheromone Perfume as the fixed $29 purchase and any newly supplied free physical product, research both product worlds, choose the buyer and use occasion without a confirmation pause, connect both products into one persuasive first-touch page, produce the same 39-image/four-pack workflow, build and QA the site, and target a healthy-path wall clock of 40 minutes or less.

## Non-negotiable public-copy contract

- Use the strongest supported direct statement first.
- Use high-heat questions and imagined scenes for desired outcomes when a direct performance claim is not earned.
- Do not emit the rejected generic sentence `Imagined possibilities, not guaranteed outcomes. Scent perception and individual experiences vary.`
- Do not treat a question mark or asterisk as permission to assert a false universal, chemical, biological, testimonial, inventory, scarcity, or pricing claim.
- Keep internal terms out of public copy: `offer`, `value stack`, `tripwire`, `framework`, `mechanism`, `paid product`, `companion product`, `relationship mode`, `avatar`, `Big Domino`, `ENGAGE`, `FIBS`, and `Grand Slam Offer`.
- Permit customer-facing terms such as `FREE`, `bonus`, `gift`, `bundle`, and `premium` only when transaction truth supports them.
- Render the transaction clearly: `FREE <product> with your $29 Auralo purchase`.
- Never generate named, starred, pictured, or “verified” customer reviews without real review evidence.
- Permit editorial imagination blocks such as `What if...`, `Imagine...`, and `Picture this...` without presenting them as customer experience.
- Keep competitor comments and pages as research/reference inputs, never as our customer proof.

## Persuasion model

The free product supplies the first-touch pattern interrupt. The perfume must then become desirable in its own right rather than feel like a fee required to obtain the free item.

The system will select one relationship:

- `wanted_reward`: the free item is the desired reward for purchasing Auralo; or
- `complete_ritual`: both products credibly contribute to one buyer moment.

The system may use both only when research supports a clear primary and secondary relationship.

Candidate copy will be ranked by emotional force, specificity, curiosity, product desire, transaction clarity, evidence strength, and natural language. The highest-intensity passing candidate wins.

## Research contract

Run three typed lanes:

1. Auralo demand, scent language, use moments, objections, benefit language, product facts, and evidence.
2. Free-product demand, design/fit/use language, objections, purchase signals, and exact-product facts.
3. Buyer overlap, shared use occasions, relationship evidence, and transaction language.

Reject gibberish, off-segment products, mismatched genders/recipients, unsupported claims, and evidence assigned to the wrong semantic role. Global evidence counts cannot compensate for a missing lane.

## Creative and visual contract

Keep exactly 39 images and four prompt packs sized `10/10/10/9`, with both reference products present in every pack header and every prompt capped at 220 words.

### Fifteen-slide story

1. Free-product pattern interrupt.
2. Design desire and identity.
3. Exact $29 transaction reveal.
4. Unfinished-routine tension.
5. Perfume as the invisible finishing detail.
6. Fragrance frustration/pain.
7. Desired scent experience.
8. Sensory profile and application ritual.
9. Verified perfume facts.
10. Accurately framed research context.
11. Combined buyer moment.
12. Why the free product is the reward.
13. Everything that arrives.
14. Objection and earned risk reversal.
15. Complete-transaction close.

### Four six-image rails

1. Auralo desire, ritual, and evidence.
2. Free-product desire, details, fit, and use.
3. Combined imagined moments and objections.
4. Verified proof or editorial decision support; never fabricated testimonials.

Support `legacy_39_locked` for the existing Sprinkle Pants images and `conversion_39_v5` for future image production.

## Runtime architecture

- `core.py`: schema, provenance, states, deadlines, public lexical contract.
- `research.py`: three research lanes and semantic acceptance.
- `offer.py`: internal relationship, transaction, value, objection, and economics decisions.
- `creative.py`: high-heat copy packet, rhetorical hierarchy, proof typing, 39 prompts.
- `site.py`: compatibility layouts, conversion sections, instrumentation, image import/build/local QA.
- `release.py`: Netlify create-new-site policy, deployment receipts, live QA.
- `cli.py`: thin deterministic command surface.

Keep the top-level skill concise and route detail through small phase references.

## Forty-minute contract

Target budgets:

| Phase | Target |
|---|---:|
| Intake/preflight | 2 min |
| Three-lane research | 6 min |
| Relationship/copy | 5 min |
| Review/prompt compile | 3 min |
| External images | 10 min |
| Import/build | 4 min |
| Local QA | 3 min |
| Deploy/smoke | 3 min |
| Live QA | 4 min |
| Total | 40 min |

Record active tool time, provider wait, and human wait separately. Add a `--deadline-minutes 40` run contract and fail honestly with `TIME_BUDGET_EXCEEDED` rather than reporting a false on-time completion. Optimize the default path to one research acquisition, one writer pass, one joint review, one image batch, one build, one deployment, and one live-QA collection.

## Build order

1. Scaffold plugin and skill with official creator scripts.
2. Selectively port the tested FreePerry30Days mechanics and rename the runtime package.
3. Add schemas, three-lane research, relationship engine, rhetorical candidate selection, public-copy validator, proof types, and visual contracts.
4. Add fixtures demonstrating a different free product without hardcoded pants logic.
5. Run unit tests, Ruff, skill validator, plugin validator, and deterministic canary.
6. Update the personal marketplace cachebuster, install, compare source/install trees, and rerun installed tests.
7. Keep the current deployment unchanged until a later Sprinkle Pants rerun passes the new plugin’s gates.

## Honest completion states

- `BRIEF_READY`
- `RESEARCH_PLAN_READY`
- `PAID_PRODUCT_TRUTH_MISSING`
- `PAID_RESEARCH_GAP`
- `FREE_PRODUCT_RESEARCH_GAP`
- `RELATIONSHIP_NOT_EARNED`
- `RESEARCH_ACCEPTED`
- `WRITER_READY`
- `CREATIVE_DRAFT_READY`
- `PROMPTS_COMPILED`
- `PROMPT_PACK_READY`
- `IMAGES_READY`
- `PREVIEW_BUILT`
- `QA_ACCEPTED`
- `RELEASE_PLAN_READY`
- `DEPLOYMENT_ACCEPTED`
- `LIVE_QA_ACCEPTED`
- `TIME_BUDGET_EXCEEDED`
- `CONVERSION_NOT_MEASURED`

No state may imply conversion performance without real traffic measurement.
