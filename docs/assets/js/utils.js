/* 日和建設 - Utilities (no module bundler, attached to window.NW) */
(function () {
  const NW = (window.NW = window.NW || {});

  NW.prefersReducedMotion = function () {
    return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  };

  /**
   * IntersectionObserver-based reveal helper.
   * Adds `is-inview` once when threshold is met. Won't unset.
   * @param {string} selector
   * @param {object} options - threshold, rootMargin
   */
  NW.observeReveal = function (selector, options) {
    const els = document.querySelectorAll(selector);
    if (!("IntersectionObserver" in window) || NW.prefersReducedMotion()) {
      els.forEach((el) => el.classList.add("is-inview"));
      return;
    }
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-inview");
            observer.unobserve(entry.target);
          }
        });
      },
      Object.assign({ threshold: 0.18, rootMargin: "0px 0px -80px 0px" }, options || {})
    );
    els.forEach((el) => observer.observe(el));
  };

  /** Animate a number from 0 to target over duration ms. */
  NW.animateCount = function (el, target, duration) {
    if (NW.prefersReducedMotion()) {
      el.textContent = NW.formatNum(target);
      return;
    }
    const start = performance.now();
    const easeOut = (t) => 1 - Math.pow(1 - t, 3);
    function tick(now) {
      const t = Math.min(1, (now - start) / duration);
      const v = Math.round(target * easeOut(t));
      el.textContent = NW.formatNum(v);
      if (t < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  };

  NW.formatNum = function (n) {
    if (n >= 1000) return n.toLocaleString("en-US");
    return String(n);
  };
})();
