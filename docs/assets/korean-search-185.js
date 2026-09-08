(() => {
  "use strict";

  const INDEX_URL = "/assets/korean-search-index.json";
  const RESULT_LIMIT = 12;
  let docs = null;
  let loading = null;
  let closeSearch = () => {};

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

  // Match concrete patient phrases inside longer questions, not isolated particles
  // such as "안". These expand document search; they do not select a prescription.
  const patientPhrases = [
    [/피곤(?:해요|하고|해서|합니다)|기운이?없(?:어요|고|어서|습니다)/, ["피로", "기력저하"]],
    [/잠(?:이|도)?안(?:와요|오고|와서|옵니다)|자주깨(?:요|고|서)/, ["불면", "수면"]],
    [/소화(?:가|도)?안(?:돼요|되고|돼서|됩니다)|속(?:이|도)?더부룩(?:해요|하고|해서)/, ["소화불량"]],
    [/밥(?:을|도)?못(?:먹(?:어요|고|어서)|드(?:세요|시고|셔서))|입맛이?없(?:어요|고|어서)/, ["식욕저하"]],
  ];

  async function loadIndex() {
    if (docs) return docs;
    if (!loading) {
      loading = fetch(INDEX_URL, { cache: "no-cache" })
        .then((r) => {
          if (!r.ok) throw new Error(`index ${r.status}`);
          return r.json();
        })
        .then((data) => {
          if (!Array.isArray(data)) throw new Error('invalid index');
          docs = data.filter(validDoc).map(prepareDoc);
          if (docs.length !== data.length) console.error('[Minseong Search 185] invalid rows skipped');
          return docs;
        })
        .catch((err) => {
          console.error("[Minseong Search 185] index load failed", err);
          // A temporary failure must not disable search until the next page load.
          loading = null;
          return [];
        });
    }
    return loading;
  }

  function validDoc(doc) {
    // The index contains only root-relative internal links, never executable URLs.
    return doc && typeof doc === 'object' && typeof doc.title === 'string' &&
      typeof doc.url === 'string' && /^\/(?!\/)/.test(doc.url) &&
      !/[\\\x00-\x20\x7f]/.test(doc.url) &&
      (doc.keywords == null || Array.isArray(doc.keywords)) &&
      (doc.text == null || typeof doc.text === 'string') &&
      Number.isFinite(Number(doc.boost || 0));
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
    let symptomPhrase = false;
    for (const [pattern, extras] of patientPhrases) {
      if (!pattern.test(c)) continue;
      symptomPhrase = true;
      for (const extra of extras) terms.add(extra);
    }
    if (symptomPhrase && /부모님|어머니|아버지|어르신/.test(c)) {
      terms.add("어르신");
      terms.add("노인");
    }
    if (symptomPhrase && c.includes("수술후")) terms.add("수술후");
    if (symptomPhrase) {
      // In a recognized sentence, these particles otherwise match unrelated titles
      // (e.g. "안" matches every "안내"). Keep the complete original query.
      for (const particle of ["안", "못", "후", "도"]) terms.delete(particle);
    }
    return [...terms].filter((x) => x.length >= 1);
  }

  function prepareDoc(doc) {
    const title = normalize(doc.title);
    const titleC = title.replace(/\s+/g, "");
    const keys = (doc.keywords || []).map(normalize);
    const keysC = keys.map((key) => key.replace(/\s+/g, ""));
    const text = normalize(doc.text);
    const textC = text.replace(/\s+/g, "");
    return { doc, title, titleC, keys, keysC, text, textC };
  }

  function scoreDoc(prepared, query) {
    const { doc, title, titleC, keys, keysC, text, textC } = prepared;
    const { qn, qc, terms } = query;

    let score = Number(doc.boost || 0);

    // 대표 페이지를 최우선으로: 제목 exact > 제목 prefix > 제목 포함 > keyword > 본문
    if (title === qn || titleC === qc) score += 1200;
    if (title.startsWith(qn) || titleC.startsWith(qc)) score += 650;
    if (title.includes(qn) || titleC.includes(qc)) score += 420;
    if (keys.includes(qn) || keysC.includes(qc)) score += 340;

    let termMatched = false;
    for (const [term, tc] of terms) {
      if (!term) continue;
      if (title.includes(term) || titleC.includes(tc)) {
        score += 160;
        termMatched = true;
      }
      if (keys.some((k) => k.includes(term)) || keysC.some((k) => k.includes(tc))) {
        score += 110;
        termMatched = true;
      }
      if (text.includes(term) || textC.includes(tc)) {
        score += 18;
        termMatched = true;
      }
    }

    // 아무 관련도 없는 문서는 제외
    const matched =
      title.includes(qn) || titleC.includes(qc) ||
      keys.includes(qn) || keysC.includes(qc) ||
      termMatched;

    return matched ? score : 0;
  }

  function search(data, raw) {
    const query = { qn: normalize(raw), qc: compact(raw),
      terms: queryTerms(raw).map((term) => [term, term.replace(/\s+/g, '')]) };
    return data
      .map((prepared) => ({ doc: prepared.doc, score: scoreDoc(prepared, query) }))
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
    panel.hidden = true;
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
      <div class="ms-ksearch-foot">증상 표현·제목·태그·본문에서 검색한 결과입니다.</div>`;
  }

  function install() {
    const input = document.querySelector(".md-search__input");
    const searchRoot = document.querySelector(".md-search");
    if (!input || !searchRoot) return false;

    if (input.dataset.msKsearch185 === "1") return true;
    closeSearch();
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

    closeSearch = () => {
      ++seq;
      panel.hidden = true;
      document.documentElement.classList.remove("ms-ksearch-active");
    };

    return true;
  }

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") closeSearch();
  });

  // Subscribe once, rather than once for every new search input.
  if (typeof document$ !== "undefined" && document$?.subscribe) {
    document$.subscribe(() => setTimeout(install, 0));
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
