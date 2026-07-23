---
name: freeperrylarp1
description: Build or audit a campaign where Auralo Pheromone Perfume is the fixed $29 paid product and one newly supplied product is FREE. Use for isolated free-product intake, fresh research planning, mandatory product-marriage decisions, evidence-bounded direct-response copy, customer-facing image text, cross-campaign leakage prevention, or later prompt/build/QA phases.
---

# FreePerryLarp1

Build one evidence-bounded campaign at a time. Auralo Pheromone Perfume is the
fixed paid product. The FREE product is never a default: every run must supply
its identity, facts, evidence, reference images, offer terms, and isolation
contract again.

## Hard boundaries

- Load the bundled Auralo dossier by version and verify its hash.
- Never let a campaign override Auralo identity, price, facts, evidence type, or
  prohibited outcome claims.
- Create a new run root and campaign identifier for every FREE product.
- Resolve every FREE-product reference under that explicit run root and verify
  the file bytes against the campaign SHA-256 before accepting the campaign.
- Do not copy writer packets, accepted briefs, copy, prompts, images, or site
  data from another campaign.
- Keep prior-product entity fingerprints in the validator boundary only. Never
  include them in the writer packet.
- Freeze neutral paid-product, FREE-product, customer-language, objection, and
  purchase-trigger research before proposing any connection.
- Treat `fresh_only` and the frozen hash as contract attestations. Require a
  separate retrieval receipt before claiming that live research ran.
- Never seed neutral research with a ritual, moment, pairing, bridge, angle, or
  other preselected connection. Do not co-search the two product categories.
- Require an accepted marriage brief before any writer or prompt compiler runs.
- Allow at most two angle-repair cycles. Then stop with `ANGLE_GAP` or
  `MARRIAGE_GAP`; do not keep brainstorming.
- Reject `CROSS_CAMPAIGN_LEAK` before prompt delivery.
- Production directions may describe the current scene. Declared visible text
  must be customer-facing sales copy, never strategy diagnosis or instructions.
- A question mark, asterisk, mock-page footer, client review, or later legal
  review does not turn an unsupported claim into evidence.
- Competitor screenshots may guide layout rhythm. They do not authorize copied
  testimonials, review counts, verified-buyer badges, attraction outcomes, or
  another seller's product claims.

## Required order

1. Validate the fixed dossier and current campaign manifest.
2. Run independent fresh research for paid-product truth/desire, current
   FREE-product truth/desire, verbatim customer language, objections, and
   purchase triggers. Do not search for a connection between the products.
3. Freeze the complete research snapshot and its SHA-256.
4. Use `$freeperrylarp1-brainstorm` to generate at least four materially
   different connection hypotheses in isolated sessions.
5. Give the frozen research and exact candidate-set hash to a separate critic.
   The critic executes forced-pairing, generic-language, unsupported-assumption,
   weak-desire, interchangeability, and customer-voice challenges with
   candidate-specific tests, evidence, findings, and counterevidence.
6. Accept the highest-scoring eligible primary and strongest materially
   different backup. Candidate-owned scores and token overlap are never
   selection evidence.
7. Give the writer only the clean writer packet: all current product truth,
   all accepted customer language, objections, purchase triggers, market
   context, and one plain-English sales argument. Do not send generator frames, candidate
   rankings, critic metadata, prior-product fingerprints, or query recipes.
8. Write the complete natural sales argument before assigning page sections,
   image jobs, overlays, or prompts.
9. Require an independent copy-chief receipt bound to the finished-copy hash.
10. Map the accepted copy into page sections and image jobs, then validate all
    public copy, visible text, prompt directions, and site data against the
    claim and leakage boundaries.
11. Continue to prompt delivery only after every gate passes.

Issue 1 supplies the contract and validators. Campaign execution, installation,
image generation, lander build, deployment, and live QA remain later reviewed
phases.

## Contract command

```bash
python3 scripts/freeperrylarp1_contract.py validate-campaign \
  --campaign /absolute/path/to/campaign.json \
  --asset-root /absolute/path/to/current-run-root
```

The brainstorm sidecar accepts one schema `2.0` input containing the frozen
research snapshot, isolated candidates, and independent critic:

```bash
python3 ../freeperrylarp1-brainstorm/scripts/brainstorm_gate.py \
  --campaign /absolute/path/to/campaign.json \
  --input /absolute/path/to/brainstorm-input.json \
  --asset-root /absolute/path/to/current-run-root \
  --output /absolute/path/to/accepted-selection.json
```

Read [operating-contract.md](references/operating-contract.md) before changing
campaign schemas or completion language.
