/* Shared reading aids stay small while page-specific study tools load on demand. */
(() => {
  "use strict";
  function revealAnchor() {
    let id;
    try { id = decodeURIComponent(location.hash.slice(1)); } catch (_) { return; }
    const target = id && document.getElementById(id);
    if (!target) return;
    for (let parent = target.parentElement; parent; parent = parent.parentElement) {
      if (parent.tagName === "DETAILS") parent.open = true;
    }
  }

  function updateTable(wrap) {
    const overflowing = wrap.scrollWidth > wrap.clientWidth + 1;
    if (overflowing) {
      wrap.tabIndex = 0;
      wrap.setAttribute("role", "region");
      const caption = wrap.querySelector("caption");
      wrap.setAttribute("aria-label", caption?.textContent.trim() || "가로로 스크롤하는 표");
    } else {
      wrap.removeAttribute("tabindex");
      wrap.removeAttribute("role");
      wrap.removeAttribute("aria-label");
    }
  }

  let observer;
  function init() {
    revealAnchor();
    observer?.disconnect();
    const tables = document.querySelectorAll(".md-typeset__scrollwrap");
    if (typeof ResizeObserver !== "undefined") {
      observer = new ResizeObserver(entries => entries.forEach(entry => updateTable(entry.target)));
      tables.forEach(wrap => observer.observe(wrap));
    }
    tables.forEach(updateTable);
  }

  window.addEventListener("hashchange", revealAnchor);
  if (typeof document$ !== "undefined") document$.subscribe(init);
  else if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init, {once: true});
  else init();
})();
