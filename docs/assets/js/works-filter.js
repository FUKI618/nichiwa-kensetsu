/* 日和建設 - Works filter (category & area) */
(function () {
  const grid = document.getElementById("works-grid");
  if (!grid) return;
  const empty = document.getElementById("works-empty");
  const countEl = document.getElementById("works-count");
  const cards = Array.from(grid.querySelectorAll(".card-work"));
  const filterRoot = document.querySelector(".works-filters");
  if (!filterRoot) return;

  const state = { category: "all", area: "all" };

  function apply() {
    let visible = 0;
    cards.forEach((card) => {
      const cat = card.dataset.category;
      const area = card.dataset.area;
      const match =
        (state.category === "all" || cat === state.category) &&
        (state.area === "all" || area === state.area);
      card.classList.toggle("is-hidden", !match);
      if (match) visible++;
    });
    if (empty) empty.classList.toggle("is-visible", visible === 0);
    if (countEl) countEl.querySelector("strong").textContent = String(visible);
  }

  filterRoot.querySelectorAll(".chip").forEach((chip) => {
    chip.addEventListener("click", () => {
      const group = chip.dataset.group;
      const value = chip.dataset.value;
      state[group] = value;
      filterRoot
        .querySelectorAll(`.chip[data-group="${group}"]`)
        .forEach((c) => c.setAttribute("aria-pressed", c === chip ? "true" : "false"));
      apply();
    });
  });

  apply();
})();
