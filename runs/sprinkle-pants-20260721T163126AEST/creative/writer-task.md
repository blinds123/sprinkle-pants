# FreePerry30Days single writer pass

Read only:
- `/Users/nelsonchan/Documents/Sprinkle pants/runs/sprinkle-pants-20260721T163126AEST/creative/writer-packet.json`
- `/Users/nelsonchan/Documents/Sprinkle pants/runs/sprinkle-pants-20260721T163126AEST/creative/cast-plan.json`

Write one JSON object to `creative/writer-output.json` and then run `writer-accept`.

Required top-level keys: `schema_version`, `writer_packet_sha256`, `cast_plan_sha256`, `avatar`, `copy`, `sample_stories`, and `grounding`.

- Set `schema_version` to `1.0`.
- Set `writer_packet_sha256` to `36b944606126ca9fe8cb8dfc4fac43b7782a699404d1a829944c0889e67e4363`.
- Set `cast_plan_sha256` to `5712d8d1c354a84bab7c75539cf3783a1335134f9f46eeb074fcbf9c046cbcfd`.
- `avatar` needs `label`, `purchase_moment`, and non-empty `pains`, `desires`, `objections`, `language_cues`; every entry is `{"text":"...","research_ids":["R/X/S ID"]}`.
- `copy` needs announcement, eyebrow, headline, subheadline, primary/secondary CTA, story heading/intro, exactly 14 `story` entries with heading/body, offer heading/body/stack, final heading/body, a FAQ heading, all 10 proof-section strings, and FAQs.
- `sample_stories` must contain I-001..I-024 in order. Match each assigned name. Every item needs name, headline, complete `review_text`, context, and outcome. Do not add quotes or evidence IDs.
- `grounding.hero`, each of 14 `grounding.story` entries, and `grounding.offer` each cite at least one relevant `research_id` or `fact_id` from the packet.
- Use at least four distinct research IDs, including at least two retrieved R or X customer-voice IDs. Place every required A fact's exact public language in the relevant first-15 story body and cite it in the matching grounding entry.
- Customer-facing words must never expose framework names, research labels, production fields, or prompt instructions.
- If `offer_argument.headline_contract.required_headline` is non-empty, copy it exactly into `copy.headline`. Do not replace it with a pain-first or product-education headline. Use `secondary_hook` elsewhere in the first fold.
- Write `FREE`, never `$0` or `$0.00`, for a zero-price companion product.
- Audit every word that may be rendered inside artwork. Headings, callouts, diagrams, badges, interface labels, and offer terms may use only the packet's exact authorized facts and supplied offer terms; do not invent discounts, savings, performance results, response times, guaranteed assistance outcomes, protection, privacy/security promises, alert behavior, settings, or controls.
