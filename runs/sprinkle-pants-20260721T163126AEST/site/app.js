"use strict";

const LAYOUT_CONTRACT = "goda-webinar-15-proof-4-v3";
const HERO_IDS = Array.from({ length: 15 }, (_, index) => `IMG-${String(index + 1).padStart(2, "0")}`);
const TESTIMONIAL_ZONES = [
  ["testimonial_rail_one", "testimonial-rail-one"],
  ["testimonial_rail_two", "testimonial-rail-two"],
  ["testimonial_rail_three", "testimonial-rail-three"],
  ["testimonial_rail_four", "testimonial-rail-four"],
];
const scrollBehavior = () => window.matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth";

const byId = (id) => document.getElementById(id);
const make = (tag, className, text) => {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
};

function moneyOrFree(value) {
  const amount = Number(value);
  if (Number.isFinite(amount) && amount === 0) return "FREE";
  return `$${value}`;
}

function imageElement(job, eager = false) {
  const image = make("img");
  image.src = job.image;
  image.alt = job.alt || "Campaign image";
  image.loading = eager ? "eager" : "lazy";
  image.decoding = "async";
  if (eager) image.fetchPriority = "high";
  return image;
}

function testimonialCard(job, story, index) {
  const card = make("article", "testimonial-card");
  card.dataset.proofIndex = String(index);
  card.setAttribute("aria-label", `${story.name}. ${story.headline}. ${story.review_text}`);
  const figure = make("figure", "testimonial-image");
  figure.dataset.imageSlot = job.id;
  figure.append(imageElement(job));
  const accessibleCopy = make(
    "span",
    "sr-only testimonial-accessible-copy",
    `${story.name}. ${story.headline}. ${story.review_text}`,
  );
  card.append(figure, accessibleCopy);
  return card;
}

function faqItem(item, index) {
  const wrap = make("article", "faq-item");
  const button = make("button");
  button.type = "button";
  button.setAttribute("aria-expanded", "false");
  button.setAttribute("aria-controls", `faq-answer-${index}`);
  button.append(make("span", "", item.question));
  button.append(make("span", "faq-symbol", "+"));
  const answer = make("div", "faq-answer", item.answer);
  answer.id = `faq-answer-${index}`;
  answer.hidden = true;
  button.addEventListener("click", () => {
    const open = button.getAttribute("aria-expanded") === "true";
    button.setAttribute("aria-expanded", String(!open));
    button.lastElementChild.textContent = open ? "+" : "−";
    answer.hidden = open;
  });
  wrap.append(button, answer);
  return wrap;
}

function setText(id, value) {
  const target = byId(id);
  if (target) target.textContent = value || "";
}

function validateLayoutData(data, jobs) {
  const expectedIds = Array.from({ length: 39 }, (_, index) => `IMG-${String(index + 1).padStart(2, "0")}`);
  if (data.visual_jobs.length !== 39 || expectedIds.some((id) => !jobs.has(id))) {
    throw new Error("Layout contract requires one job for every IMG-01 through IMG-39 slot");
  }
  if (HERO_IDS.some((id) => jobs.get(id)?.zone !== "hero_carousel")) {
    throw new Error("IMG-01 through IMG-15 must form the ordered hero carousel");
  }
  TESTIMONIAL_ZONES.forEach(([zone]) => {
    if (data.visual_jobs.filter((job) => job.zone === zone).length !== 6) {
      throw new Error(`${zone} must contain exactly six testimonial images`);
    }
  });
  if (data.copy.story.length !== 14 || data.sample_stories.length !== 24) {
    throw new Error("Layout contract requires 14 hero-carousel story beats and 24 testimonial stories");
  }
}

function renderHeroCarousel(data, jobs) {
  const track = byId("hero-track");
  const thumbs = byId("hero-thumbs");
  const media = document.querySelector("[data-gallery]");
  const counter = byId("hero-counter");
  const heroJobs = HERO_IDS.map((id) => jobs.get(id));
  let activeIndex = 0;
  let scrollFrame = 0;

  heroJobs.forEach((job, index) => {
    const slide = make("figure", "hero-slide");
    slide.dataset.imageSlot = job.id;
    slide.dataset.heroSlide = String(index + 1);
    slide.dataset.webinarBeat = String(index + 1);
    slide.setAttribute("role", "group");
    slide.setAttribute("aria-label", `Offer image ${index + 1} of 15`);
    slide.append(imageElement(job, index === 0));
    const caption = index === 0
      ? `${data.copy.headline}. ${data.copy.subheadline}`
      : `${data.copy.story[index - 1].heading}. ${data.copy.story[index - 1].body}`;
    slide.append(make("figcaption", "sr-only", caption));
    track.append(slide);

    const thumb = make("button", "hero-thumb");
    thumb.type = "button";
    thumb.dataset.galleryThumb = String(index + 1);
    thumb.setAttribute("aria-label", `Show offer image ${index + 1}`);
    thumb.setAttribute("aria-current", index === 0 ? "true" : "false");
    thumb.style.backgroundImage = `url(${JSON.stringify(job.image)})`;
    thumb.addEventListener("click", () => goTo(index));
    thumbs.append(thumb);
  });

  const update = (index) => {
    activeIndex = Math.max(0, Math.min(heroJobs.length - 1, index));
    counter.textContent = `${activeIndex + 1} / ${heroJobs.length}`;
    [...thumbs.children].forEach((thumb, thumbIndex) => {
      thumb.setAttribute("aria-current", thumbIndex === activeIndex ? "true" : "false");
    });
    byId("hero-previous").disabled = activeIndex === 0;
    byId("hero-next").disabled = activeIndex === heroJobs.length - 1;
  };
  const goTo = (index) => {
    const target = Math.max(0, Math.min(heroJobs.length - 1, index));
    track.scrollTo({ left: target * track.clientWidth, behavior: scrollBehavior() });
    update(target);
  };

  byId("hero-previous").addEventListener("click", () => goTo(activeIndex - 1));
  byId("hero-next").addEventListener("click", () => goTo(activeIndex + 1));
  media.addEventListener("keydown", (event) => {
    if (event.key === "ArrowLeft") {
      event.preventDefault();
      goTo(activeIndex - 1);
    }
    if (event.key === "ArrowRight") {
      event.preventDefault();
      goTo(activeIndex + 1);
    }
  });
  track.addEventListener("scroll", () => {
    cancelAnimationFrame(scrollFrame);
    scrollFrame = requestAnimationFrame(() => {
      const width = Math.max(track.clientWidth, 1);
      update(Math.round(track.scrollLeft / width));
    });
  }, { passive: true });
  update(0);
}

function bindRailControls() {
  document.querySelectorAll("[data-rail-previous],[data-rail-next]").forEach((button) => {
    const targetId = button.dataset.railPrevious || button.dataset.railNext;
    const direction = button.dataset.railPrevious ? -1 : 1;
    button.addEventListener("click", () => {
      const rail = byId(targetId);
      const card = rail?.querySelector(".testimonial-card");
      if (!rail || !card) return;
      const gap = Number.parseFloat(getComputedStyle(rail).columnGap || getComputedStyle(rail).gap || "0");
      rail.scrollBy({ left: direction * (card.getBoundingClientRect().width + gap), behavior: scrollBehavior() });
    });
  });
}

function bindCheckout(data) {
  const drawer = byId("checkout-drawer");
  const panel = drawer.querySelector(".drawer-panel");
  const drawerOffer = byId("drawer-offer");
  let returnFocus = null;
  const focusable = () => [...panel.querySelectorAll("button:not([disabled]),a[href],[tabindex]:not([tabindex='-1'])")]
    .filter((node) => node.getClientRects().length > 0);
  const closeDrawer = () => {
    drawer.hidden = true;
    document.body.classList.remove("drawer-open");
    if (returnFocus?.isConnected) returnFocus.focus();
    returnFocus = null;
  };
  data.copy.offer_stack.forEach((item) => drawerOffer.append(make("p", "", item)));
  document.querySelectorAll("[data-preview-checkout]").forEach((button) => {
    button.textContent = data.copy.primary_cta;
    button.addEventListener("click", () => {
      returnFocus = button;
      drawer.hidden = false;
      document.body.classList.add("drawer-open");
      drawer.querySelector(".drawer-close").focus();
    });
  });
  document.querySelectorAll("[data-close-checkout]").forEach((button) => button.addEventListener("click", closeDrawer));
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && !drawer.hidden) {
      event.preventDefault();
      closeDrawer();
      return;
    }
    if (event.key !== "Tab" || drawer.hidden) return;
    const controls = focusable();
    if (!controls.length) return;
    const first = controls[0];
    const last = controls[controls.length - 1];
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    } else if (!panel.contains(document.activeElement)) {
      event.preventDefault();
      first.focus();
    }
  });
}

function bindAnchorNavigation() {
  document.querySelectorAll('a[href^="#"]').forEach((link) => {
    link.addEventListener("click", (event) => {
      const hash = link.getAttribute("href");
      const target = hash ? document.querySelector(hash) : null;
      if (!target) return;
      event.preventDefault();
      const headerHeight = document.querySelector(".site-header")?.getBoundingClientRect().height || 0;
      const top = hash === "#top" ? 0 : Math.max(0, target.getBoundingClientRect().top + window.scrollY - headerHeight - 16);
      history.replaceState(null, "", hash);
      window.scrollTo({ top, behavior: "auto" });
    });
  });
}

async function render() {
  if (document.documentElement.dataset.layoutContract !== LAYOUT_CONTRACT) {
    throw new Error("Layout contract marker mismatch");
  }
  const response = await fetch("site-data.json", { cache: "no-store" });
  if (!response.ok) throw new Error(`site-data.json returned ${response.status}`);
  const data = await response.json();
  const jobs = new Map(data.visual_jobs.map((job) => [job.id, job]));
  validateLayoutData(data, jobs);
  const offer = data.campaign.offer;
  const priceLine = `${offer.paid_name} ${moneyOrFree(offer.paid_price_usd)} + ${offer.companion_name} ${moneyOrFree(offer.companion_price_usd)}`;

  setText("announcement", data.copy.announcement);
  setText("header-cta", data.copy.primary_cta);
  setText("secondary-cta", data.copy.secondary_cta);
  setText("eyebrow", data.copy.eyebrow);
  setText("hero-heading", data.copy.headline);
  setText("hero-subheadline", data.copy.subheadline);
  setText("hero-offer-heading", data.copy.offer_heading);
  setText("hero-offer-body", data.copy.offer_body);
  setText("offer-heading", data.copy.offer_heading);
  setText("offer-body", data.copy.offer_body);
  setText("final-heading", data.copy.final_heading);
  setText("final-body", data.copy.final_body);
  setText("price-line", priceLine);
  setText("faq-heading", data.copy.faq_heading);
  setText("drawer-heading", data.copy.final_heading);
  setText("drawer-body", data.copy.final_body);
  setText("social-kicker", data.copy.proof_sections.social_kicker);
  setText("social-heading", data.copy.proof_sections.social_heading);
  setText("recognition-kicker", data.copy.proof_sections.recognition_kicker);
  setText("recognition-heading", data.copy.proof_sections.recognition_heading);
  setText("recognition-body", data.copy.proof_sections.recognition_body);
  setText("compliments-kicker", data.copy.proof_sections.compliments_kicker);
  setText("compliments-heading", data.copy.proof_sections.compliments_heading);
  setText("wall-kicker", data.copy.proof_sections.wall_kicker);
  setText("wall-heading", data.copy.proof_sections.wall_heading);
  setText("wall-body", data.copy.proof_sections.wall_body);

  renderHeroCarousel(data, jobs);

  const trustItems = [offer.shipping, offer.returns, offer.warranty];
  trustItems.forEach((item) => byId("trust-strip").append(make("li", "", item)));
  trustItems.forEach((item) => byId("final-trust").append(make("li", "", item)));
  data.copy.offer_stack.forEach((item) => byId("offer-stack").append(make("li", "", item)));
  data.copy.faq.forEach((item, index) => byId("faq-list").append(faqItem(item, index)));

  const railByZone = new Map(TESTIMONIAL_ZONES.map(([zone, id]) => [zone, byId(id)]));
  data.visual_jobs.filter((job) => job.phase === "proof").forEach((job, index) => {
    const rail = railByZone.get(job.zone);
    if (!rail) throw new Error(`Unmapped testimonial zone: ${job.zone}`);
    rail.append(testimonialCard(job, data.sample_stories[index], index));
  });

  bindRailControls();
  bindCheckout(data);
  bindAnchorNavigation();
  document.body.dataset.renderComplete = "true";
}

render().catch((error) => {
  document.body.dataset.renderError = error.message;
  const message = make("p", "render-error", "Page data could not be loaded. Serve this folder with a local HTTP server and refresh.");
  document.body.prepend(message);
});
