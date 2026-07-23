# FreePerryLarp single writer pass

Read only:
- `/Users/nelsonchan/Documents/Sprinkle pants/runs/sprinkle-pants-freeperrylarp-20260722T172700AEST/creative/writer-packet.json`
- `/Users/nelsonchan/Documents/Sprinkle pants/runs/sprinkle-pants-freeperrylarp-20260722T172700AEST/creative/cast-plan.json`

Write one JSON object to `creative/writer-output.json` and then run `writer-accept`.

Required top-level keys: `schema_version`, `writer_packet_sha256`, `cast_plan_sha256`, `avatar`, `copy`, `scenario_cards`, and `grounding`.

- Set `schema_version` to `1.0`.
- Set `writer_packet_sha256` to `592cfbd79f99b45462b2a0c9db9dffafce01d98dd9210f5f26382ce86ed812ae`.
- Set `cast_plan_sha256` to `3d224bf85ec827c86ae71e96fa0a6aa1bb5d6fa120b2a9af6f046ce6c221e1d4`.
- `avatar` needs `label`, `purchase_moment`, and non-empty `pains`, `desires`, `objections`, `language_cues`; every entry is `{"text":"...","research_ids":["R/X/S ID"]}`.
- `copy` needs announcement, eyebrow, headline, subheadline, primary/secondary CTA, bridge heading/body, 5-10 ranked `desire_questions`, story heading/intro, exactly 14 `story` entries with heading/body, transaction heading/body/stack, final heading/body, a FAQ heading, all 12 proof-section strings, and FAQs.
- `desire_questions` must use maximum-heat What if, Could, Imagine, or Picture this language. Put the strongest line first. Questions may end with an asterisk, but the asterisk never authorizes a universal, chemical, biological, or guaranteed result.
- `scenario_cards` must contain I-001..I-024 in order. Every item needs id, headline, complete `scene_text`, context, and outcome. Use direct second-person editorial scenes; do not add names, stars, quotes, review labels, or evidence IDs.
- `grounding.hero`, each of 14 `grounding.story` entries, and `grounding.offer` each cite at least one relevant `research_id` or `fact_id` from the packet.
- Use at least four distinct research IDs, including at least two retrieved R or X customer-voice IDs. Place every required A fact's exact public language in the relevant first-15 story body and cite it in the matching grounding entry.
- Customer-facing words must never expose framework names, research labels, production fields, or prompt instructions.
- The four proof rails separately build Auralo desire, free-product desire, their shared moment, and decision confidence. They are editorial scenes—not testimonials.
- If `offer_argument.headline_contract.required_headline` is non-empty, copy it exactly into `copy.headline`. Do not replace it with a pain-first or product-education headline. Use `secondary_hook` elsewhere in the first fold.
- Write `FREE`, never `$0` or `$0.00`, for a zero-price companion product.
- Never print the rejected generic sentence about imagined possibilities or scent perception varying.
- Audit every word that may be rendered inside artwork. Headings, callouts, diagrams, badges, interface labels, and transaction terms may use only the packet's exact authorized facts and supplied terms; do not invent discounts, savings, performance results, response times, guaranteed assistance outcomes, protection, privacy/security promises, alert behavior, settings, or controls.
