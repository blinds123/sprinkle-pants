# Paid-product desire and two-product scaffold review

Date: 2026-07-22  
Campaign: Auralo Pheromone Perfume + FREE Sprinkle Tweed Pants  
Scope: read-only review and implementation plan; no site, image, prompt, plugin, skill, or deployment changes

## Executive decision

Yes: the existing private framework and the copy jobs should change so the paid perfume receives a real desire arc. No: the page should not simply mention “pheromone perfume” more often, invent a functional relationship between scent and trousers, or try to persuade the buyer that she *needs both products*.

The correct goal is **asymmetric offer marriage**:

1. Auralo must have enough verified independent value that it does not feel like a toll charged to obtain the trousers.
2. The Sprinkle Tweed Pants should remain the high-desire premium that creates action.
3. The page must explain the transaction in one short bridge: one paid product, one wanted premium, two distinct roles, one clear offer.

This is deliberately not a 50/50 product page. Perry Belcher’s premium model allows the premium to carry a large share of the desire, including when it is not functionally related to the paid item. But the paid item still needs a credible reason to buy. The present page has the first half and not the second.

Current honest states:

- `PAID_PRODUCT_TRUTH_MISSING`
- `PAID_MARKET_VOICE_MISSING`
- `OFFER_MARRIAGE_NOT_EARNED`
- `GRAND_SLAM_NOT_PROVEN`
- the current rendered page remains a noindexed client preview, not conversion proof

Fresh verification used public/static acquisition, not the ambient in-app browser. On 2026-07-22 the deployed HTML still declared `goda-webinar-15-proof-4-v3` and `noindex,nofollow`; the live `site-data.json` SHA-256 was `03cf1d8d6a5f68e57a3f1ab4461c3c02e0268b11c3ad811f838795f8d3128fd5`. Its current strings confirm the paid-first offer line, the pants-led desire story, and the trousers-only final heading described below.

## What is structurally wrong today

This is not mainly a wording problem. It starts in the contracts.

### 1. The truth model is one-sided

The current creative contract accepts one `product_truth` ledger and requires exactly three customer-facing reasons tied to its authorized fact keys. It also says the three private reasons may cite only those keys. In this campaign, that ledger belongs to the FREE trousers. There is no equivalent `paid_product_truth` ledger for Auralo.

The writer therefore knows detailed trouser facts but, for Auralo, effectively knows only:

- product name;
- $29 price;
- its reference image;
- its role in the offer.

That is enough to state the transaction. It is not enough to write a truthful scent, format, volume, use, ingredient, longevity, emotional-outcome, or performance argument.

### 2. The research model is one-sided

The current Last30Days result is dominated by trouser and styling material. It contains useful language about statement pieces, wide-leg styling, fit, versatility, and direct requests to buy the trousers. It does not contain a sufficient Auralo or fragrance-category desire/objection lane.

That means even after adding official Auralo facts, the writer would still lack recent buyer language about why this audience wants a fragrance, what makes them hesitate, and what purchase context is relevant. Product facts and buyer voice are separate inputs; neither can substitute for the other.

### 3. The visual story jobs silently default to the companion

The current `visual-map.json` assigns:

- IMG-02 to the situation that makes the *companion* matter;
- IMG-03 to a central conclusion;
- IMG-04, IMG-07, and IMG-09 to the three reasons;
- IMG-05, IMG-06, IMG-08, IMG-10, IMG-13, and IMG-14 to singular “the product” jobs;
- only IMG-01, IMG-11, IMG-12, and IMG-15 explicitly to the offer or pair.

Because the authorized reasons and useful facts are trouser facts, every ambiguous singular-product job resolves to the trousers. The first 15 images are therefore a trouser sales story with Auralo at the opening, connection, terms, and close.

The remaining 24 illustrative cards are also trouser-led. They cannot serve as Auralo proof merely because the bottle sometimes appears in the artwork.

### 4. The HTML copy reflects the same imbalance

The current page has a clear paid-first transaction headline, but most belief-building language is about the pants:

- the hero support describes the trousers;
- the story heading is “The trousers that do the visual work”;
- the early story beats cover trouser styling, fabric, silhouette, fit, care, and occasions;
- Auralo receives one role line in “Two parts of one getting-ready moment”;
- the FAQ has no paid-product question;
- all four proof-rail headings sell trouser desire;
- the final heading is “Make the trousers the statement.”

The result is easy to understand but psychologically lopsided: **want the pants, pay through the perfume**.

## What the three teaching lenses actually imply

These are evidence-based interpretations of their public frameworks, not claims that the marketers personally reviewed this campaign.

### Perry Belcher lens: let the premium create action, but make the transaction sensible

Perry’s own funnel guide defines a premium as a gift that entices the purchase, says it does not have to be related to the paid product, and emphasizes that it must be something the market wants. He also treats identity-signalling premiums as especially powerful. That supports using the visually distinctive trousers as the wanted premium. It does **not** support inventing a functional “outfit plus attraction system.”

Implication for this offer:

- Keep the pants highly desirable.
- Do not force “you need both.”
- Verify that fragrance buyers and statement-fashion buyers overlap enough for one acquisition offer.
- Give Auralo a legitimate independent purchase reason, even if the premium remains the stronger impulse trigger.
- Judge the offer by completed-purchase economics and customer quality, not by how many people click for the FREE item.

Source: [Perry Belcher’s funnel and premium guide](https://perrybelcher.com/sales-funnel-template/).

### Russell Brunson lens: one belief sequence must lead to the transaction

ClickFunnels’ current framework material stresses that each funnel element has a conversion job, that stories and teaching points break beliefs, and that the Stack follows the belief shift. The current page creates a belief about statement trousers, then asks for money for perfume. The offer is visible, but the belief-to-transaction path is incomplete.

The correction is not a second, competing Big Domino and not a second full sales letter. It is one transaction belief:

> The paid product is worthwhile on verified grounds, the premium is genuinely desirable, and the stated purchase path is clear and credible.

The internal story can then create three subordinate beliefs and harvest them in the close. Framework names must remain private; the customer should only encounter ordinary language.

Sources: [ClickFunnels on belief, positioning, and the Stack](https://www.clickfunnels.com/blog/why-funnels-matter-more-than-product/) and [ClickFunnels on each funnel element having a job](https://www.clickfunnels.com/blog/webinar-marketing-funnel/).

### Alex Hormozi lens: repetition cannot manufacture value

Acquisition.com describes offer construction in terms of the Value Equation, offer stacking, objection removal, bonuses, guarantees, and ethical scarcity. Applied here, the paid product needs facts that support some combination of desired outcome, perceived likelihood, shorter delay, or lower effort. The premium can enhance the offer, but it cannot be the only component with articulated value.

Implication for this offer:

- one paid-product desire reason is better than five generic perfume mentions;
- a guarantee must match real policy and risk, not be invented as decoration;
- no fake scarcity or automatic countdown;
- no prohibited price comparison;
- a “Grand Slam” label is not earned until fulfilment, refund behavior, margins, buyer quality, and customer outcomes support it.

Sources: [Acquisition.com’s offer curriculum](https://www.acquisition.com/offers-oo) and [$100M Offers contents](https://shop.acquisition.com/products/100m-offers-hardcover).

## The key reframing

Do not make the template answer:

> Why does the customer need both products?

Make it answer these three questions:

1. Why is the paid product worth buying?
2. Why is the FREE premium desirable enough to increase action?
3. Why is this particular transaction clear and credible?

Only a campaign with verified joint-use evidence may answer a fourth question:

4. Why are the products better used together?

For the current campaign, question four is not earned. “Getting ready” may be a reasonable shared occasion, but it is positioning—not proof of functional complementarity.

## Required private scaffold

Add a mode-aware, two-product contract rather than a second writer or a larger persuasion catalog.

### Required offer mode

Exactly one mode must be selected before research synthesis:

- `wanted_premium`: the FREE item is principally an identity/desire incentive; functional relation is not required;
- `complementary_bundle`: each product has a distinct role in a supported shared outcome;
- `paid_led_bonus`: the paid product carries most desire and the FREE item mainly removes an objection or adds convenience.

The current Sprinkle Pants campaign should use `wanted_premium` unless new evidence earns a different mode.

### Required truth objects

```json
{
  "offer_mode": "wanted_premium",
  "paid_product_truth": [],
  "companion_product_truth": [],
  "relationship_evidence": [],
  "paid_role": "",
  "companion_role": "",
  "transaction_alignment": "",
  "unsupported_relationship_claims": []
}
```

Rules:

- both products need independent truth ledgers;
- every public product claim binds to the correct product and `fact_key`;
- product name, price, category, or a reference image alone cannot satisfy a paid-value reason;
- `relationship_evidence` is empty by default;
- empty relationship evidence forbids causal, synergistic, combined-result, “complete system,” or “works together” language;
- “pheromone” may be repeated as part of the supplied product name, but attraction, confidence, response, chemistry, or performance claims require product-specific substantiation;
- if Europe is in scope, cosmetic claims—explicit or implicit—need adequate, verifiable support and may not exceed the evidence. See [EU Regulation 655/2013](https://eur-lex.europa.eu/eli/reg/2013/655/oj/eng).

### Required research subject coverage

Keep the overall research lane compact, but make subject coverage explicit:

| Mode | Paid-product coverage | Companion coverage | Relationship coverage |
|---|---|---|---|
| `wanted_premium` | at least two buyer-voice items and one paid-category objection | at least two buyer-voice items and one purchase signal | market-overlap evidence; no joint-use claim required |
| `complementary_bundle` | at least two buyer-voice items and one objection | at least two buyer-voice items and one objection | at least one credible joint-use or shared-outcome item |
| `paid_led_bonus` | majority of selected evidence, including purchase signal and objections | at least one relevant desire or convenience item | transaction clarity only unless more is proven |

These are subject minimums inside the existing total research thresholds, not permission to double the writer packet. Irrelevant material remains quarantined.

### Required buyer-decision object

```json
{
  "central_transaction_belief": "",
  "reasons": [
    {"subject": "paid", "fact_keys": []},
    {"subject": "paid", "fact_keys": []},
    {"subject": "companion", "fact_keys": []}
  ],
  "relationship_job": {
    "type": "transaction_alignment",
    "paid_fact_keys": [],
    "companion_fact_keys": [],
    "relationship_evidence_ids": []
  }
}
```

For `wanted_premium`, the recommended three-reason allocation is two paid reasons and one companion-desire reason. The separate relationship beat explains the offer without consuming one of the three reasons. For `complementary_bundle`, use one paid reason, one companion reason, and one supported joint-use reason.

This is more robust than hard-coding “three companion facts” or forcing a universal one-one-one allocation.

## Section-by-section decision for the current frozen-image page

The present 39 images are fixed. Copy embedded in IMG-01..39 cannot be changed through HTML, and the trouser images cannot honestly be relabelled as perfume evidence. Therefore use existing text surfaces only.

| Surface | Current job | Recommended current-page job | Constraint |
|---|---|---|---|
| Announcement | state paid + FREE transaction | keep | no extra persuasion needed |
| Hero headline | state offer and price | keep paid-first | already clear |
| Hero eyebrow | generic finishing-touch language | introduce the buyer moment, not a framework label | no performance implication |
| Hero subheadline | sell trousers only | one verified Auralo value sentence, then one trouser desire sentence | blocked until paid truth exists |
| Buybox | select and transact | show paid item, FREE item, sizes, and exact terms distinctly | no second price comparison |
| New bridge after hero | absent | add exactly one compact “two roles, one offer” module | text-only; not a functional bundle claim |
| IMG-01..15 | pants-led baked story | preserve as historical creative | cannot be rebalanced without new images |
| Four proof rails | pants-led illustrative perspectives | preserve headings that match the images | do not call them Auralo proof |
| Middle offer | restate item roles | add one verified paid reason, one premium desire line, and exact terms | do not create another long Stack |
| FAQ | pants fit/care and fulfilment | add one paid-product fact question and one pairing/transaction question | blocked until facts are supplied |
| Final close | “Make the trousers the statement” | close the paid value and the premium together | blocked until paid value is supportable |
| Footer | preview disclosure | keep disclosure | illustrative cards are not customer proof |

### How many new sections?

Exactly **one** new section is justified for the current layout: the offer bridge directly after the hero. More sections would mostly repeat the same unsupported Auralo wording, lengthen the page, and separate the premium from the item being purchased.

Once verified Auralo facts exist, improve the existing hero support, middle offer, FAQ, and close. Do not add a separate perfume mini-sales-page below the trouser story. The next generation of images should solve the deeper imbalance inside the existing 15-beat structure.

### Safe bridge shape now

Until paid truth exists, only neutral role clarity is safe:

**One offer. Two distinct roles.**  
Auralo Pheromone Perfume is the $29 paid product. The Sprinkle Tweed Pants are the FREE statement pair, with cream tweed, multicoloured flecks, a braided drawcord, and fringed hems.

That is honest but not yet persuasive for Auralo. After official facts are captured, replace the first sentence after the heading with one fact-bound reason to want the paid product. Do not invent fragrance notes, bottle volume, longevity, application instructions, attraction, confidence, reactions, or “chemistry.”

## Revised 15-beat story for future campaigns

Do not change image count or placement. Version the semantic map so old accepted prompt packs are not reinterpreted retroactively.

Recommended `wanted_premium` map:

| ID | Subject | Customer-facing job |
|---|---|---|
| IMG-01 | offer | paid-first transaction and FREE reveal |
| IMG-02 | buyer | concrete occasion/problem |
| IMG-03 | paid | paid-product opportunity or desired role |
| IMG-04 | paid | first fact-bound paid reason |
| IMG-05 | paid | truthful product action or use |
| IMG-06 | paid | believable use moment |
| IMG-07 | paid | second paid reason or main objection |
| IMG-08 | companion | premium desire and identity |
| IMG-09 | companion | key product fact, fit, or selection concern |
| IMG-10 | risk | limitation, care, policy, or effort boundary |
| IMG-11 | relationship | distinct roles and transaction alignment |
| IMG-12 | terms | exact paid price, FREE item, fulfilment, returns, and warranty |
| IMG-13 | buyer | ranked moments across the purchase journey |
| IMG-14 | setup | supported application, selection, or preparation steps |
| IMG-15 | close | harvest paid value, premium desire, and next action |

For `complementary_bundle`, rebalance IMG-04..10 across paid, companion, and genuinely supported joint use. The renderer should read an explicit `subject` for every slot; ambiguous wording such as “the product” should be removed from the default visual map.

## Revised 24-card allocation for future campaigns

The count and four-rail layout may remain, but every card needs a `proof_subject`:

- `paid`
- `companion`
- `offer`

Recommended `wanted_premium` allocation:

| Rail | IDs | Future job |
|---|---|---|
| 1 | IMG-16..21 | paid-product moments, motivations, or verified proof |
| 2 | IMG-22..27 | premium desire, identity, fit, and styling |
| 3 | IMG-28..33 | decision objections spanning paid product, premium selection, and terms |
| 4 | IMG-34..39 | overall offer confidence and close |

For noindexed client previews, synthetic first-person cards must remain explicitly illustrative in the durable disclosure. They are not verified customer proof. For a production sales page, either supply authorized real-customer evidence or render these as clearly editorial “ways to wear/use/decide” cards rather than testimonial-looking proof.

## Copy framework changes by existing section

Yes, the existing frameworks should include the perfume, but by **copy job**, not mention count.

### Hero

Job: answer “what do I pay for, what do I get FREE, and why should the paid item interest me?”

- Headline: transaction.
- Supporting line one: one verified paid-product benefit or sensory/use fact.
- Supporting line two: one premium desire fact.
- CTA: paid item first, FREE item second.

### Story

Job: build the paid product’s independent value before allowing the premium to accelerate desire.

- two fact-bound paid reasons;
- one premium reason;
- one explicit but non-causal relationship beat;
- one honest risk/limitation beat;
- one terms beat.

### Proof/perspective rails

Job: answer separate questions rather than repeat the hero.

- Can I picture using or choosing the paid product?
- Can I picture wearing the premium?
- What would stop me?
- Do I understand the transaction and next step?

### FAQ

Minimum subject coverage:

1. What exactly is the paid product?
2. Why is it paired with this FREE premium?
3. What do I need to know about the premium’s size/fit/care?
4. What are shipping, returns, and any guarantee terms?
5. Is the “pheromone” wording a product name or a supported performance claim?

The fifth answer must be drafted from the merchant’s product documentation and legal review; the template must not answer it by inference.

### Close

Job: harvest one belief, not introduce a new claim.

The close should restate:

- the strongest verified reason to choose Auralo;
- the most desirable accurate trouser detail;
- the paid-first offer terms;
- the next action.

## Validator and template changes required later

This review does not implement them. A future implementation should make small, versioned changes:

1. Add `paid_product_truth`, `companion_product_truth`, `offer_mode`, and `relationship_evidence` schemas.
2. Add `PAID_PRODUCT_TRUTH_MISSING`, `PAID_MARKET_VOICE_MISSING`, and `RELATIONSHIP_NOT_EARNED` blockers.
3. Reject paid-value copy whose only support is name, price, category, or image.
4. Require subject coverage in research and the writer packet.
5. Make three-reason allocation mode-aware.
6. Add `subject` to IMG-02..15 and `proof_subject` to IMG-16..39.
7. Add exactly one `offer_bridge` component after the hero.
8. Require paid-product FAQ coverage and a paid-value statement in the close.
9. Forbid joint-benefit verbs when relationship evidence is absent.
10. Preserve the one-writer pass. Do not bolt on `brunson-perry-brain` as a second copy writer; borrow only concise congruence checks.
11. Version the layout/semantic contract rather than modifying `goda-webinar-15-proof-4-v3` in place.
12. Preserve the 220-word prompt ceiling, both-reference binding, 10/10/10/9 pack split, and source/cache/install parity checks.

## What not to do

- Do not add “pheromone,” “attraction,” or “confidence” repeatedly to create artificial desire.
- Do not say the fragrance completes the trousers, makes the outfit more attractive, changes reactions, or works synergistically without evidence.
- Do not change pants-led rail headings to fragrance headings while retaining the same images.
- Do not add a second long-form sales letter or duplicate offer stack.
- Do not create separate Perry, Brunson, and Hormozi production writers; use one writer with a compact, validated contract.
- Do not expose Big Domino, Three Secrets, Value Equation, Grand Slam Offer, objection, mechanism, or other framework labels publicly.
- Do not use false scarcity, fake social proof, unsupported guarantees, or price comparison.
- Do not call illustrative portrait cards verified customers.
- Do not upgrade `LIVE_QA_ACCEPTED` into checkout, customer, profitability, or offer proof.

## Second-, third-, and fourth-order consequences

### If the paid truth gate is added

Some Auralo runs will stop earlier. That is desirable: the current workflow hides a missing input by producing thin paid-product copy. The recovery path must ask for the current official product URL or merchant documentation, not relax the gate.

### If subject coverage is added to research

Research may become noisier or exceed the writer packet cap. Prevent this by selecting a small number of high-value paid, companion, and relationship items and retaining the 45 KB limit. Do not dump two complete raw markets into the writer.

### If the visual map changes in place

Existing 39-image runs, prompt hashes, QA receipts, and image order could become semantically invalid. Introduce a new contract version and leave prior artifacts bound to v3.

### If perfume copy is expanded before substantiation

The page risks explicit and implicit cosmetic-performance claims. EU rules require adequate, verifiable evidence and require the presentation not to exceed that evidence. The product name itself does not authorize an attraction outcome.

### If the FREE premium remains the only source of desire

Clicks may rise while paid-product satisfaction, refund rate, repeat purchase quality, and contribution margin deteriorate. The KPI hierarchy should be completed purchases, checkout completion, refunds/chargebacks, fulfilment cost, contribution margin, and repeat behavior—not CTA clicks alone.

### If the page becomes perfectly balanced

It may weaken the very premium effect that makes the offer compelling. The target is not equal word count. It is sufficient independent paid value plus strong premium desire plus clear transaction logic.

## Recommended implementation order

1. Obtain a current official Auralo product URL or merchant-approved product documentation.
2. Build the paid-product fact ledger and claim limitations.
3. Run a bounded fragrance-category research lane and identify market overlap with the trouser buyer.
4. Lock `wanted_premium` unless joint-use evidence earns `complementary_bundle`.
5. Update the schema, writer packet, and validators first.
6. Add the one text-only offer bridge and revise current HTML-only surfaces; preserve all existing images.
7. Keep the current carousel and rails explicitly pants-led because their text is baked into the images.
8. Version and rebalance the 15+24 semantic map only for future prompt/image runs.
9. Run source, cache, and installed validation plus contamination fixtures for unrelated products.
10. Build a fresh preview and rerun deterministic 390/768/1440 QA before any deployment claim.
11. Test economics and customer outcomes before calling the offer Grand Slam.

## Final recommendation

The current page should not try to prove that buyers need perfume and trousers together. It should prove three smaller things: Auralo is worth buying on verified grounds, the pants are an unusually desirable FREE premium, and the offer is straightforward.

For the current frozen-image site, add one short offer bridge and revise the hero support, middle offer, FAQ, and close only after Auralo truth is obtained. For the default plugin, make paid-product truth, dual-subject research, mode-aware reason allocation, explicit slot subjects, and relationship evidence first-class inputs. That fixes the cause instead of hiding it with more copy.
