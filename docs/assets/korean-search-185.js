(() => {
  "use strict";

  const INDEX_URL = "/assets/korean-search-index.json";
  const RESULT_LIMIT = 12;
  let docs = null;
  let loading = null;

  const normalize = (s) =>
    String(s || "")
      .normalize("NFKC")
      .toLowerCase()
      .replace(/[·ㆍ,./()[\]{}:;'"!?_\-–—]+/g, " ")
      .replace(/\s+/g, " ")
      .trim();

  const compact = (s) => normalize(s).replace(/\s+/g, "");

  const patientAliases = new Map([
    ["잠이안와요", ["불면", "불면증", "수면", "잠"]],
    ["자주깨요", ["불면", "수면", "잠"]],
    ["새벽에깨요", ["불면", "수면"]],
    ["코막힘", ["비염", "알레르기비염", "코막힘"]],
    ["코가막혀요", ["비염", "알레르기비염", "코막힘"]],
    ["허리통증", ["요통", "허리통증"]],
    ["허리가아파요", ["요통", "허리통증"]],
    ["체했어요", ["소화불량", "더부룩함"]],
    ["명치답답함", ["소화불량", "명치답답함"]],
  ]);

  async function loadIndex() {
    if (docs) return docs;
    if (!loading) {
      loading = fetch(INDEX_URL, { cache: "no-cache" })
        .then((r) => {
          if (!r.ok) throw new Error(`index ${r.status}`);
          return r.json();
        })
        .then((data) => {
          docs = Array.isArray(data) ? data : [];
          return docs;
        })
        .catch((err) => {
          console.error("[Minseong Search 185] index load failed", err);
          docs = [];
          return docs;
        });
    }
    return loading;
  }

  function queryTerms(raw) {
    const n = normalize(raw);
    const c = compact(raw);
    const terms = new Set(n.split(" ").filter(Boolean));
    terms.add(n);
    terms.add(c);
    for (const extra of patientAliases.get(c) || []) {
      terms.add(normalize(extra));
      terms.add(compact(extra));
    }
    return [...terms].filter((x) => x.length >= 1);
  }

  function scoreDoc(doc, raw) {
    const qn = normalize(raw);
    const qc = compact(raw);
    const title = normalize(doc.title);
    const titleC = compact(doc.title);
    const keys = (doc.keywords || []).map(normalize);
    const keysC = (doc.keywords || []).map(compact);
    const text = normalize(doc.text);
    const textC = compact(doc.text);
    const terms = queryTerms(raw);

    let score = Number(doc.boost || 0);

    // 대표 페이지를 최우선으로: 제목 exact > 제목 prefix > 제목 포함 > keyword > 본문
    if (title === qn || titleC === qc) score += 1200;
    if (title.startsWith(qn) || titleC.startsWith(qc)) score += 650;
    if (title.includes(qn) || titleC.includes(qc)) score += 420;
    if (keys.includes(qn) || keysC.includes(qc)) score += 340;

    for (const term of terms) {
      const tc = term.replace(/\s+/g, "");
      if (!term) continue;
      if (title.includes(term) || titleC.includes(tc)) score += 160;
      if (keys.some((k) => k.includes(term)) || keysC.some((k) => k.includes(tc))) score += 110;
      if (text.includes(term) || textC.includes(tc)) score += 18;
    }

    // 아무 관련도 없는 문서는 제외
    const matched =
      title.includes(qn) || titleC.includes(qc) ||
      keys.includes(qn) || keysC.includes(qc) ||
      terms.some((t) => text.includes(t) || textC.includes(t.replace(/\s+/g, "")));

    return matched ? score : 0;
  }

  function search(data, raw) {
    return data
      .map((doc) => ({ doc, score: scoreDoc(doc, raw) }))
      .filter((x) => x.score > 0)
      .sort((a, b) => b.score - a.score || a.doc.title.localeCompare(b.doc.title, "ko"))
      .slice(0, RESULT_LIMIT);
  }

  function ensurePanel(searchRoot) {
    let panel = document.getElementById("ms-ksearch-panel");
    if (panel) return panel;

    panel = document.createElement("div");
    panel.id = "ms-ksearch-panel";
    panel.className = "ms-ksearch-panel";
    panel.setAttribute("aria-live", "polite");
    searchRoot.appendChild(panel);
    return panel;
  }

  function escapeHtml(s) {
    return String(s || "").replace(/[&<>"']/g, (m) => ({
      "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;"
    }[m]));
  }

  function render(panel, raw, results) {
    if (!raw.trim()) {
      panel.hidden = true;
      panel.innerHTML = "";
      document.documentElement.classList.remove("ms-ksearch-active");
      return;
    }

    document.documentElement.classList.add("ms-ksearch-active");
    panel.hidden = false;

    if (!results.length) {
      panel.innerHTML = `
        <div class="ms-ksearch-head">민성 한국어 검색</div>
        <div class="ms-ksearch-empty">
          <strong>${escapeHtml(raw)}</strong>에 대한 자체 검색 결과가 없습니다.
          <span>아래 기본 검색 결과도 함께 확인할 수 있습니다.</span>
        </div>`;
      return;
    }

    const items = results.map(({ doc }) => `
      <a class="ms-ksearch-item" href="${escapeHtml(doc.url)}">
        <span class="ms-ksearch-title">${escapeHtml(doc.title)}</span>
        <span class="ms-ksearch-snippet">${escapeHtml(doc.snippet || "")}</span>
      </a>`).join("");

    panel.innerHTML = `
      <div class="ms-ksearch-head">
        <span>민성 한국어 검색</span>
        <small>${results.length}개 우선 표시</small>
      </div>
      <div class="ms-ksearch-list">${items}</div>
      <div class="ms-ksearch-foot">환자 표현·제목·태그·본문을 통합 검색합니다. 기본 MkDocs 검색은 보조로 유지됩니다.</div>`;
  }

  function install() {
    const input = document.querySelector(".md-search__input");
    const searchRoot = document.querySelector(".md-search");
    if (!input || !searchRoot) return false;

    if (input.dataset.msKsearch185 === "1") return true;
    input.dataset.msKsearch185 = "1";

    const panel = ensurePanel(searchRoot);
    let seq = 0;

    const run = async () => {
      const current = ++seq;
      const raw = input.value || "";
      if (!raw.trim()) {
        render(panel, "", []);
        return;
      }
      const data = await loadIndex();
      if (current !== seq) return;
      render(panel, raw, search(data, raw));
    };

    input.addEventListener("input", run);
    input.addEventListener("focus", run);

    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") {
        panel.hidden = true;
        document.documentElement.classList.remove("ms-ksearch-active");
      }
    });

    // Material instant navigation에서도 재설치 가능
    if (typeof document$ !== "undefined" && document$?.subscribe) {
      document$.subscribe(() => setTimeout(install, 0));
    }

    loadIndex();
    return true;
  }

  // Material의 검색 결과 DOM을 기다리지 않는다.
  // 검색 입력 자체가 생기면 즉시 독립 패널을 연결한다.
  if (!install()) {
    const observer = new MutationObserver(() => {
      if (install()) observer.disconnect();
    });
    observer.observe(document.documentElement, { childList: true, subtree: true });
  }
})();