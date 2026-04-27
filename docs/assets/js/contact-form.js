/* 日和建設 - Contact form handling */
(function () {
  const form = document.getElementById("contact-form");
  if (!form) return;

  const successEl = document.getElementById("form-success");

  // Pre-select inquiry type via URL query (?type=demolition|asbestos|coating|recruit|other)
  const params = new URLSearchParams(window.location.search);
  const typeMap = {
    demolition: "解体工事",
    asbestos: "アスベスト除去",
    coating: "塗装・外壁工事",
    recruit: "採用・協力会社",
    other: "その他",
  };
  const presetType = typeMap[params.get("type")];
  if (presetType) {
    const radio = form.querySelector(`input[name="inquiry_type"][value="${presetType}"]`);
    if (radio) radio.checked = true;
  }

  function setError(field, on) {
    field.classList.toggle("is-error", on);
  }

  function validate() {
    let ok = true;
    form.querySelectorAll("[data-required]").forEach((input) => {
      const field = input.closest(".form-field") || input.closest(".form-radio-grid")?.parentElement;
      if (!field) return;
      let valid = true;
      if (input.type === "checkbox") {
        valid = input.checked;
      } else if (input.matches("input[type=radio]")) {
        valid = !!form.querySelector(`input[name="${input.name}"]:checked`);
      } else if (input.type === "email") {
        valid = !!input.value.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/);
      } else if (input.type === "tel") {
        valid = !!input.value.match(/^[0-9+\-() 　]{8,}$/);
      } else {
        valid = !!input.value.trim();
      }
      setError(field, !valid);
      if (!valid) ok = false;
    });
    return ok;
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    if (!validate()) {
      const firstErr = form.querySelector(".is-error");
      if (firstErr) firstErr.scrollIntoView({ behavior: "smooth", block: "center" });
      return;
    }
    const submitBtn = form.querySelector('button[type="submit"]');
    submitBtn.disabled = true;
    submitBtn.querySelector("span").textContent = "送信中…";

    const data = new FormData(form);
    const action = form.getAttribute("action");

    try {
      // If action is a real Formspree endpoint, send via fetch.
      // Otherwise (placeholder), simulate success after a short delay.
      const isPlaceholder = !action || action.includes("YOUR_FORM_ID");
      if (isPlaceholder) {
        await new Promise((r) => setTimeout(r, 800));
      } else {
        const resp = await fetch(action, {
          method: "POST",
          body: data,
          headers: { Accept: "application/json" },
        });
        if (!resp.ok) throw new Error("Network error");
      }
      form.style.display = "none";
      successEl.style.display = "block";
      successEl.scrollIntoView({ behavior: "smooth", block: "start" });
    } catch (err) {
      submitBtn.disabled = false;
      submitBtn.querySelector("span").textContent = "送信する";
      alert("送信に失敗しました。お手数ですが、お電話（072-239-0126）でご連絡ください。");
    }
  });

  // Live error clearing
  form.querySelectorAll("input, textarea, select").forEach((el) => {
    el.addEventListener("input", () => {
      const field = el.closest(".form-field") || el.closest(".form-radio-grid")?.parentElement;
      if (field) field.classList.remove("is-error");
    });
    el.addEventListener("change", () => {
      const field = el.closest(".form-field") || el.closest(".form-radio-grid")?.parentElement;
      if (field) field.classList.remove("is-error");
    });
  });
})();
