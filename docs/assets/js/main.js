/* 日和建設 - Main behaviors */
(function () {
  const NW = window.NW;
  if (!NW) return;

  document.addEventListener("DOMContentLoaded", function () {
    initHeader();
    initMobileNav();
    initSmoothScroll();
    initRevealAnimations();
    initCountUps();
    initVoicesCarousel();
    initFAQ();
    initToTop();
    initFooterYear();
    const hero = document.querySelector(".hero");
    if (hero) {
      hero.classList.add("js-anim");
      requestAnimationFrame(() => {
        requestAnimationFrame(() => hero.classList.add("is-loaded"));
      });
    }
  });

  /* ---------- Header scroll state ---------- */
  function initHeader() {
    const header = document.querySelector(".site-header");
    if (!header) return;
    const update = () => {
      if (window.scrollY > 24) header.classList.add("is-scrolled");
      else header.classList.remove("is-scrolled");
    };
    update();
    window.addEventListener("scroll", update, { passive: true });
  }

  /* ---------- Mobile nav ---------- */
  function initMobileNav() {
    const btn = document.querySelector(".menu-btn");
    const nav = document.querySelector(".mobile-nav");
    if (!btn || !nav) return;
    const close = () => {
      btn.setAttribute("aria-expanded", "false");
      nav.classList.remove("is-open");
      document.body.style.overflow = "";
    };
    btn.addEventListener("click", () => {
      const open = btn.getAttribute("aria-expanded") === "true";
      if (open) {
        close();
      } else {
        btn.setAttribute("aria-expanded", "true");
        nav.classList.add("is-open");
        document.body.style.overflow = "hidden";
      }
    });
    nav.querySelectorAll("a").forEach((a) => a.addEventListener("click", close));
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") close();
    });
  }

  /* ---------- Smooth scroll w/ header offset ---------- */
  function initSmoothScroll() {
    const headerH = () => (window.matchMedia("(max-width:1023px)").matches ? 64 : 84);
    document.querySelectorAll('a[href^="#"]').forEach((a) => {
      a.addEventListener("click", (e) => {
        const id = a.getAttribute("href");
        if (!id || id === "#" || id.length < 2) return;
        const target = document.querySelector(id);
        if (!target) return;
        e.preventDefault();
        const top = target.getBoundingClientRect().top + window.scrollY - headerH() - 8;
        window.scrollTo({ top, behavior: NW.prefersReducedMotion() ? "auto" : "smooth" });
      });
    });
  }

  /* ---------- Reveal observers ---------- */
  function initRevealAnimations() {
    NW.observeReveal(".reveal");
    NW.observeReveal(".reveal-stagger");
    NW.observeReveal(".reasons-list");
    NW.observeReveal(".kpi-grid");
  }

  /* ---------- KPI count-up ---------- */
  function initCountUps() {
    const els = document.querySelectorAll(".kpi__num[data-target]");
    if (!els.length) return;
    if (!("IntersectionObserver" in window)) {
      els.forEach((el) => (el.textContent = NW.formatNum(parseInt(el.dataset.target, 10))));
      return;
    }
    const obs = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          const el = entry.target;
          const target = parseInt(el.dataset.target, 10);
          const duration = 1600;
          NW.animateCount(el, target, duration);
          obs.unobserve(el);
        });
      },
      { threshold: 0.4 }
    );
    els.forEach((el) => obs.observe(el));
  }

  /* ---------- Voices carousel ---------- */
  function initVoicesCarousel() {
    const track = document.querySelector(".voices-track");
    const prev = document.querySelector(".voices-btn.prev");
    const next = document.querySelector(".voices-btn.next");
    if (!track) return;
    const step = () => {
      const card = track.querySelector(".voice-card");
      if (!card) return 320;
      const gap = parseInt(getComputedStyle(track).gap || "24", 10);
      return card.getBoundingClientRect().width + gap;
    };
    next && next.addEventListener("click", () => track.scrollBy({ left: step(), behavior: "smooth" }));
    prev && prev.addEventListener("click", () => track.scrollBy({ left: -step(), behavior: "smooth" }));

    let auto = null;
    const start = () => {
      stop();
      if (NW.prefersReducedMotion()) return;
      auto = setInterval(() => {
        const max = track.scrollWidth - track.clientWidth - 4;
        if (track.scrollLeft >= max) track.scrollTo({ left: 0, behavior: "smooth" });
        else track.scrollBy({ left: step(), behavior: "smooth" });
      }, 7000);
    };
    const stop = () => { if (auto) { clearInterval(auto); auto = null; } };
    track.addEventListener("mouseenter", stop);
    track.addEventListener("mouseleave", start);
    track.addEventListener("focusin", stop);
    track.addEventListener("touchstart", stop, { passive: true });
    start();
  }

  /* ---------- FAQ accordion ---------- */
  function initFAQ() {
    const items = document.querySelectorAll(".faq-q");
    items.forEach((q) => {
      q.addEventListener("click", () => {
        const expanded = q.getAttribute("aria-expanded") === "true";
        q.setAttribute("aria-expanded", expanded ? "false" : "true");
      });
    });
  }

  /* ---------- To top ---------- */
  function initToTop() {
    const btn = document.querySelector(".to-top");
    if (!btn) return;
    const update = () => {
      if (window.scrollY > 900) btn.classList.add("is-visible");
      else btn.classList.remove("is-visible");
    };
    update();
    window.addEventListener("scroll", update, { passive: true });
    btn.addEventListener("click", () => {
      window.scrollTo({ top: 0, behavior: NW.prefersReducedMotion() ? "auto" : "smooth" });
    });
  }

  /* ---------- Footer year ---------- */
  function initFooterYear() {
    const el = document.querySelector("[data-current-year]");
    if (el) el.textContent = String(new Date().getFullYear());
  }
})();
