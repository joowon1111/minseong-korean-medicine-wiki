/* Copy public canonical links only. No tracking or external publishing. */
(function () {
  "use strict";
  const ready = new WeakSet();
  function init() {
    document.querySelectorAll("[data-archive-citation]").forEach(function (root) {
      if (ready.has(root)) return;
      ready.add(root);
      const status = root.querySelector("[data-citation-status]");
      const fallback = root.querySelector("[data-citation-fallback]");
      root.querySelectorAll("[data-copy-citation]").forEach(function (button) {
        button.hidden = false;
        button.addEventListener("click", async function () {
          const text = button.dataset.copyCitation === "url" ? root.dataset.citationUrl :
            root.dataset.citationTitle + " — 민성 한의학 아카이브\n" + root.dataset.citationUrl;
          button.disabled = true;
          fallback.hidden = true;
          status.hidden = true;
          try {
            if (!navigator.clipboard || !navigator.clipboard.writeText) throw new Error("Clipboard unavailable");
            await navigator.clipboard.writeText(text);
            status.textContent = "복사했습니다.";
          } catch (_) {
            fallback.value = text;
            fallback.hidden = false;
            fallback.focus();
            fallback.select();
            status.textContent = "자동 복사가 허용되지 않았습니다. 아래 선택된 내용을 복사하세요.";
          } finally {
            status.hidden = false;
            button.disabled = false;
          }
        });
      });
    });
  }
  if (typeof document$ !== "undefined") document$.subscribe(init);
  else if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
