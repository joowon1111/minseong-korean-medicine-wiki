/* Daily study streams for the archive. Data is fetched from this site's curated JSON only. */
(function () {
  "use strict";

  const dataUrl = "/assets/daily-korean-medicine/data.json?v=20261010-yangsheng-more";
  let dataPromise, yangshengPromise;
  const reader = window.MinseongDailyReader;
  let dayOffset = reader.offsetFor(new URL(window.location.href).searchParams.get("date")) || 0;

  const hkbuHerbReferences = {
  "/herbs/amomum/": "B00254",
  "/herbs/angelica/": "B00049",
  "/herbs/angelica-pubescens/": "B00052",
  "/herbs/arctium/": "B00251",
  "/herbs/astragalus-tonic-guide/": "B00071",
  "/herbs/atractylodes/": "B00032",
  "/herbs/barley-malt/": "B00193",
  "/herbs/chuanxiong/": "B00047",
  "/herbs/cinnamon-twig/": "B00138",
  "/herbs/citrus-peel/": "B00162",
  "/herbs/coptis/": "B00070",
  "/herbs/dioscorea/": "B00007",
  "/herbs/forsythia/": "B00190",
  "/herbs/fresh-ginger/": "B00012",
  "/herbs/fritillaria/": "B00043",
  "/herbs/gastrodia/": "B00003",
  "/herbs/ginseng/": "B00002",
  "/herbs/honeysuckle/": "B00305",
  "/herbs/jujube-fruit/": "B00171",
  "/herbs/licorice/": "B00129",
  "/herbs/aconite/": "B00058",
  "/herbs/bupleurum/": "B00038",
  "/herbs/ephedra/": "B00278",
  "/herbs/ophiopogon/": "B00084",
  "/herbs/mint/": "B00261",
  "/herbs/pinellia/": "B00132",
  "/herbs/platycodon/": "B00076",
  "/herbs/poria/": "B00356",
  "/herbs/rehmannia-root-fresh/": "B00050",
  "/herbs/schisandra/": "B00211",
  "/herbs/scutellaria/": "B00072",
  "/herbs/white-peony/": "B00026",
  "/herbs/codonopsis/": "B00021",
};

  function loadData() {
    if (!dataPromise) {
      dataPromise = fetch(dataUrl, { credentials: "same-origin" }).then(function (response) {
        if (!response.ok) throw new Error("Daily study data unavailable");
        return response.json();
      }).then(function (data) {
        ["points", "herbs", "shanghan", "sasang"].forEach(function (key) {
          if (!Array.isArray(data[key]) || data[key].length === 0) {
            throw new Error("Daily study data is incomplete");
          }
        });
        return data;
      });
    }
    return dataPromise;
  }

  function kstDate(offset) {
    const parts = new Intl.DateTimeFormat("en-CA", {
      timeZone: "Asia/Seoul",
      year: "numeric",
      month: "2-digit",
      day: "2-digit"
    }).formatToParts(new Date());
    const values = {};
    parts.forEach(function (part) {
      if (part.type !== "literal") values[part.type] = part.value;
    });
    return new Date(Date.UTC(
      Number(values.year),
      Number(values.month) - 1,
      Number(values.day) + offset
    ));
  }

  function absoluteDay(date) {
    return Math.floor(Date.UTC(date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate()) / 86400000);
  }

  function dayOfYear(date) {
    return Math.floor((Date.UTC(date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate()) - Date.UTC(date.getUTCFullYear(), 0, 1)) / 86400000);
  }

  function formatDate(date) {
    return new Intl.DateTimeFormat("ko-KR", {
      timeZone: "UTC",
      year: "numeric",
      month: "long",
      day: "numeric"
    }).format(date);
  }

  function setText(root, selector, value) {
    const node = root.querySelector(selector);
    if (node) node.textContent = value || "";
  }

  function setLink(root, selector, href, label) {
    const node = root.querySelector(selector);
    if (!node) return;
    const validInternal = typeof href === "string" && href.startsWith("/") && !href.startsWith("//");
    const validExternal = typeof href === "string" && href.startsWith("https://");
    if (!validInternal && !validExternal) {
      node.hidden = true;
      return;
    }
    node.href = href;
    node.textContent = label;
    node.hidden = false;
    if (validExternal) {
      node.target = "_blank";
      node.rel = "noopener";
    } else {
      node.removeAttribute("target");
      node.removeAttribute("rel");
    }
  }

  function setOptional(root, selector, value) {
    const node = root.querySelector(selector);
    if (!node) return;
    node.textContent = value || "";
    node.hidden = !value;
  }

  function loadAlmanac() {
    if (!yangshengPromise) yangshengPromise = fetch("/assets/daily-korean-medicine/yangsheng.json?v=20261010-yangsheng-more", {credentials: "same-origin"})
      .then(function (response) { if (!response.ok) throw new Error("Almanac unavailable"); return response.json(); })
      .then(function (data) {
        if (!Array.isArray(data.cards) || !data.cards.length || !data.sources || !data.modern ||
            data.cards.some(function (item) { return !item.id || !item.line || !item.practice || !data.sources[item.source]; }) ||
            new Set(data.cards.map(function (item) { return item.id; })).size !== data.cards.length) {
          throw new Error("Almanac incomplete");
        }
        return data;
      });
    return yangshengPromise;
  }

  function renderAlmanacContent(root, item, data) {
    const source = data.sources[item.source];
    setText(root, "[data-yangsheng-season]", reader.seasons[item.season]);
    setText(root, "[data-yangsheng-theme]", item.theme);
    setText(root, "[data-yangsheng-line]", item.line);
    setOptional(root, "[data-yangsheng-practice]", "오늘의 작은 실천 — " + item.practice);
    setText(root, "[data-yangsheng-original]", source.original);
    setText(root, "[data-yangsheng-translation]", "원문 풀이 — " + source.translation);
    setOptional(root, "[data-yangsheng-words]", source.words ? "말뜻 — " + source.words : "");
    setText(root, "[data-yangsheng-context]", source.context);
    setLink(root, "[data-yangsheng-source]", source.href, source.label + " ↗");
    setLink(root, "[data-yangsheng-archive]", source.archiveHref, source.archiveLabel + " →");
    const guide = item.modern && data.modern[item.modern];
    setLink(root, "[data-yangsheng-modern]", guide ? guide.href : "", guide ? "오늘의 생활 자료 · " + guide.label + " ↗" : "");
  }

  function renderTopic(root, topic, data, date, chosenIndex) {
    const epoch = absoluteDay(date);
    const items = data[topic];
    const index = Number.isInteger(chosenIndex) ? chosenIndex : topic === "points"
      ? dayOfYear(date) % items.length
      : ((epoch % items.length) + items.length) % items.length;
    const item = items[index];
    setLink(root, "[data-topic-hkbu-reference]", "", "");
    setOptional(root, "[data-topic-explanation]", item.explanation ? "해설 — " + item.explanation : "");
    const related = root.querySelector("[data-topic-related]");
    if (related) {
      related.replaceChildren();
      (item.related || []).forEach(function (link) {
        if (typeof link.href !== "string" || !link.href.startsWith("/") || link.href.startsWith("//")) return;
        const anchor = document.createElement("a");
        anchor.href = link.href;
        anchor.textContent = link.label + " →";
        related.append(anchor);
      });
      related.hidden = !related.childElementCount;
    }

    if (topic === "points") {
      setText(root, "[data-topic-count]", "올해의 경혈 " + (index + 1) + " / " + items.length);
      setText(root, "[data-topic-title]", item.name + " " + item.code + " · " + item.hanja);
      const details = [
        item.meridian,
        "위치: " + item.location,
        item.traditional && item.traditional.length
          ? "전통 자료의 주치 예: " + item.traditional.join(" · ")
          : ""
      ].filter(Boolean).join("\n");
      setText(root, "[data-topic-summary]", details);
      setLink(root, "[data-topic-link]", item.href, "경혈 위치·설명 보기 →");
      setOptional(root, "[data-topic-original]", "");
      setOptional(root, "[data-topic-translation]", "");
      setOptional(root, "[data-topic-note]", item.note ? "확인할 점 — " + item.note : "");
      setOptional(root, "[data-topic-edition]", "");
      setLink(root, "[data-topic-reference]", item.reference, "표준 경혈 위치 자료 확인 ↗");
    } else if (topic === "herbs") {
      setText(root, "[data-topic-count]", "오늘의 본초");
      setText(root, "[data-topic-title]", item.title);
      setText(root, "[data-topic-summary]", item.summary);
      setLink(root, "[data-topic-link]", item.href, "본초 문서에서 더 읽기 →");
      setOptional(root, "[data-topic-original]", "");
      setOptional(root, "[data-topic-translation]", "");
      setOptional(root, "[data-topic-note]", item.note ? "확인할 점 — " + item.note : "");
      setOptional(root, "[data-topic-edition]", "");
      const catalogRecord = typeof item.href === "string" ? hkbuHerbReferences[item.href] : "";
      const providedCatalogUrl = typeof item.reference === "string" && item.reference.startsWith("https://sys01.lib.hkbu.edu.hk/cmed/mmid/detail.php?pid=")
        ? item.reference
        : "";
      const catalogSearch = typeof item.title === "string"
        ? (item.title.match(/[\u3400-\u4DBF\u4E00-\u9FFF\uF900-\uFAFF]+/) || [])[0]
        : "";
      const catalogUrl = providedCatalogUrl || (catalogRecord
        ? "https://sys01.lib.hkbu.edu.hk/cmed/mmid/detail.php?lang=cht&pid=" + encodeURIComponent(catalogRecord)
        : "https://sys01.lib.hkbu.edu.hk/cmed/mmid/index.php?sort=name_pinyin&lang=cht&qry=" + encodeURIComponent(catalogSearch || item.title || ""));
      setLink(root, "[data-topic-hkbu-reference]", catalogUrl, providedCatalogUrl || catalogRecord
        ? "약재 사진·한자 주치 정보(HKBU) ↗"
        : "HKBU 약재 사진·한자 주치 정보 검색 ↗");
      const otherReference = providedCatalogUrl || item.reference === item.href ? "" : item.reference;
      setLink(root, "[data-topic-reference]", otherReference, item.referenceLabel || "본초 출전·자료 확인 ↗");
    } else {
      const label = topic === "shanghan" ? "오늘의 상한론 조문 " : "원문·풀이 ";
      setText(root, "[data-topic-count]", label + (index + 1) + " / " + items.length);
      setText(root, "[data-topic-title]", item.title);
      setText(root, "[data-topic-summary]", item.originalLabel || "");
      setOptional(root, "[data-topic-original]", item.original);
      setOptional(root, "[data-topic-translation]", item.translation ? "아카이브 풀이 — " + item.translation : "");
      setOptional(root, "[data-topic-note]", item.note ? "읽는 포인트 — " + item.note : "");
      setOptional(root, "[data-topic-edition]", item.edition ? "출전·판본 — " + item.edition : "");
      setLink(root, "[data-topic-link]", item.href, "관련 원문·해설 보기 →");
      setLink(root, "[data-topic-reference]", item.reference, item.referenceLabel || "원문 자료 확인 ↗");
    }

    const reviews = {
      points: "경락과 위치를 자신의 말로 설명해 보세요.",
      herbs: "약용 부위와 처방 안에서 맡는 역할을 함께 떠올려 보세요.",
      shanghan: "조문에서 빠뜨리면 안 되는 증후와 조건을 짚어 보세요.",
      sasang: "평소 소증과 현재 병증, 비슷한 처방의 갈림점을 구분해 보세요."
    };
    setText(root, "[data-topic-review]", "복습 포인트 — " + (item.review || reviews[topic]));
    const quiz = { points: "acupoints", herbs: "herbs", shanghan: "shanghanlun", sasang: "sasang" };
    setLink(root, "[data-topic-quiz]", "/learning/" + quiz[topic] + "/", reader.labels[topic] + " 학습·퀴즈 →");

    const dateNode = root.querySelector("[data-topic-date]");
    if (dateNode) {
      dateNode.textContent = formatDate(date);
      dateNode.setAttribute("datetime", date.toISOString().slice(0, 10));
    }
  }

  function renderYangsheng(date) {
    const roots = document.querySelectorAll("[data-daily-yangsheng]");
    if (!roots.length) return;
    loadAlmanac().then(function (data) {
      // Ignore an older date's pending render when the reader moves quickly.
      if (date.getTime() !== kstDate(dayOffset).getTime()) return;
      const selected = reader.seasonalCard(date, data);
      if (!selected || !data.sources[selected.item.source]) throw new Error("Almanac incomplete");
      roots.forEach(function (root) {
        renderAlmanacContent(root, selected.item, data);
        const node = root.querySelector("[data-yangsheng-date]");
        node.textContent = formatDate(date);
        node.setAttribute("datetime", date.toISOString().slice(0, 10));
        root.querySelector("[data-yangsheng-error]").hidden = true;
      });
    }).catch(function () {
      roots.forEach(function (root) { root.querySelector("[data-yangsheng-error]").hidden = false; });
    });
  }

  const almanacReady = new WeakSet();
  function initAlmanacBrowser() {
    document.querySelectorAll("[data-almanac-library]").forEach(function (root) {
      if (almanacReady.has(root)) return;
      almanacReady.add(root);
      const query = root.querySelector("[data-almanac-query]"), season = root.querySelector("[data-almanac-season]");
      const results = root.querySelector("[data-almanac-results]"), status = root.querySelector("[data-almanac-status]");
      const more = root.querySelector("[data-almanac-more]"), preview = root.querySelector("[data-almanac-preview]");
      const previous = root.querySelector("[data-almanac-previous]"), next = root.querySelector("[data-almanac-next]");
      const copyStatus = root.querySelector("[data-almanac-copy-status]");
      const linkFallback = root.querySelector("[data-almanac-link-fallback]"), textFallback = root.querySelector("[data-almanac-text-fallback]");
      const todayButton = document.querySelector("[data-yangsheng-find]");
      let selected = null, limit = 12, copyVersion = 0;
      loadAlmanac().then(function (data) {
        if (!root.isConnected) return;
        function hits() { return reader.searchAlmanac(data, season.value, query.value); }
        function clearCopy() { copyVersion += 1; copyStatus.textContent = ""; linkFallback.hidden = true; textFallback.hidden = true; }
        function renderResults(reset) {
          if (reset) limit = 12;
          const items = hits();
          status.textContent = items.length ? items.length + "개 중 " + Math.min(limit, items.length) + "개 표시"
            : "일치하는 문구가 없습니다. 계절이나 검색어를 바꿔 보세요.";
          results.replaceChildren();
          items.slice(0, limit).forEach(function (item) {
            const li = document.createElement("li"), button = document.createElement("button");
            const tag = document.createElement("span"), line = document.createElement("strong");
            button.type = "button";
            button.setAttribute("aria-pressed", String(selected && selected.id === item.id || false));
            tag.textContent = reader.seasons[item.season] + " · " + item.theme;
            line.textContent = item.line;
            button.append(tag, line);
            button.addEventListener("click", function () { showItem(item, true); });
            li.append(button); results.append(li);
          });
          more.hidden = items.length <= limit;
        }
        function showItem(item, focus) {
          selected = item;
          preview.hidden = false;
          renderAlmanacContent(preview, item, data);
          setText(preview, "[data-almanac-title]", reader.seasons[item.season] + " · " + item.theme);
          const items = hits(), position = items.findIndex(function (hit) { return hit.id === item.id; });
          previous.disabled = position <= 0; next.disabled = position < 0 || position >= items.length - 1;
          setText(preview, "[data-almanac-position]", "현재 조건의 문구 " + (position + 1) + " / " + items.length);
          clearCopy(); renderResults(false);
          const url = new URL(window.location.href);
          url.searchParams.set("almanac", item.id);
          window.history.replaceState(null, "", url);
          if (focus) {
            preview.querySelector("[data-almanac-title]").focus({preventScroll: true});
            preview.scrollIntoView({block: "nearest", behavior: "auto"});
          }
        }
        function updateSearch() {
          selected = null; preview.hidden = true; clearCopy();
          const url = new URL(window.location.href);
          url.searchParams.delete("almanac");
          window.history.replaceState(null, "", url);
          renderResults(true);
        }
        function move(direction) {
          if (!selected) return;
          const items = hits(), position = items.findIndex(function (item) { return item.id === selected.id; });
          if (position >= 0 && items[position + direction]) showItem(items[position + direction], true);
        }
        query.disabled = false; season.disabled = false;
        query.addEventListener("input", updateSearch); season.addEventListener("change", updateSearch);
        more.addEventListener("click", function () {
          const firstNew = limit;
          limit += 12; renderResults(false);
          if (more.hidden) {
            const button = results.querySelectorAll("button")[firstNew];
            if (button) button.focus();
          }
        });
        previous.addEventListener("click", function () { move(-1); }); next.addEventListener("click", function () { move(1); });
        async function copySelection(asText) {
          if (!selected) return;
          clearCopy();
          const version = copyVersion;
          const url = new URL("/daily-korean-medicine/", window.location.origin);
          url.searchParams.set("almanac", selected.id);
          const value = asText ? reader.almanacText(selected, data) : url.href;
          try {
            await navigator.clipboard.writeText(value);
            if (version !== copyVersion) return;
            copyStatus.textContent = asText ? "생활 제안·실천·고전 원문과 출처를 복사했습니다." : "문구 링크를 복사했습니다.";
          } catch (_) {
            if (version !== copyVersion) return;
            const fallback = asText ? textFallback : linkFallback;
            fallback.value = value; fallback.hidden = false; fallback.focus(); fallback.select();
            copyStatus.textContent = asText ? "아래 내용을 선택해 복사하세요." : "아래 주소를 선택해 복사하세요.";
          }
        }
        root.querySelector("[data-almanac-share]").addEventListener("click", function () { copySelection(false); });
        root.querySelector("[data-almanac-copy]").addEventListener("click", function () { copySelection(true); });
        if (todayButton) {
          todayButton.disabled = false;
          todayButton.addEventListener("click", function () {
            const current = reader.seasonalCard(kstDate(dayOffset), data);
            if (!current) return;
            root.open = true; query.value = ""; season.value = "all"; limit = 12;
            showItem(current.item, true);
          });
        }
        const requested = new URL(window.location.href).searchParams.get("almanac");
        const item = reader.almanacFrom(requested, data);
        if (item) { root.open = true; season.value = item.season; showItem(item, false); }
        renderResults(true);
        if (requested && !item) { root.open = true; status.textContent = "이 문구 링크를 찾을 수 없습니다. 아래 목록에서 골라 읽어 보세요."; }
      }).catch(function () {
        status.textContent = "문구 자료를 불러오지 못했습니다. 위 기본 문구나 고전 해설에서 읽을 수 있습니다.";
      });
    });
  }

  function renderAll() {
    const widgets = document.querySelectorAll("[data-daily-km-topics]");
    if (!widgets.length) return;
    const date = kstDate(dayOffset);
    renderYangsheng(date);
    loadData().then(function (data) {
      widgets.forEach(function (widget) {
        widget.querySelectorAll("[data-daily-topic]").forEach(function (root) {
          const topic = root.getAttribute("data-daily-topic");
          if (data[topic]) renderTopic(root, topic, data, date);
        });
        widget.querySelectorAll("[data-topic-date]").forEach(function (node) {
          node.textContent = formatDate(date);
          node.setAttribute("datetime", date.toISOString().slice(0, 10));
        });
      });
    }).catch(function () {
      widgets.forEach(function (widget) {
        const note = widget.querySelector("[data-daily-data-error]");
        if (note) note.hidden = false;
      });
    });
  }

  const browserReady = new WeakSet();
  function initBrowser() {
    document.querySelectorAll("[data-daily-browser]").forEach(function (root) {
      if (browserReady.has(root)) return;
      browserReady.add(root);
      const query = root.querySelector("[data-daily-query]");
      const topic = root.querySelector("[data-daily-filter]");
      const results = root.querySelector("[data-daily-results]");
      const status = root.querySelector("[data-daily-results-status]");
      const more = root.querySelector("[data-daily-more]");
      const preview = root.querySelector("[data-daily-preview]");
      const meridian = root.querySelector("[data-daily-meridian]");
      const meridianLabel = root.querySelector("[data-daily-meridian-label]");
      const chapter = root.querySelector("[data-daily-chapter]");
      const chapterLabel = root.querySelector("[data-daily-chapter-label]");
      const clauseJump = root.querySelector("[data-daily-clause-jump]");
      const clauseNumber = root.querySelector("[data-daily-clause-number]");
      const clauseStatus = root.querySelector("[data-daily-clause-status]");
      const previous = root.querySelector("[data-daily-previous-card]");
      const next = root.querySelector("[data-daily-next-card]");
      const savedOnly = root.querySelector("[data-daily-saved-only]");
      const saveButton = root.querySelector("[data-daily-save-card]");
      const saveStatus = root.querySelector("[data-daily-save-status]");
      const savedKey = "minseong-daily-saved-v1";
      let saved = [], persistent = true;
      let selected, limit = 24;
      loadData().then(function (data) {
        try { saved = reader.savedCards(window.localStorage.getItem(savedKey), data); }
        catch (_) { persistent = false; }
        savedOnly.disabled = false;
        function selectedId() { return selected && selected.topic + "-" + (selected.index + 1); }
        function updateSaved() {
          setText(root, "[data-daily-saved-count]", "보관한 카드 " + saved.length + "개");
          if (!persistent) saveStatus.textContent = "이 환경에서는 새로고침 전까지만 보관됩니다.";
          const active = saved.includes(selectedId());
          saveButton.textContent = active ? "보관 해제" : "이 카드 보관";
          saveButton.setAttribute("aria-pressed", String(active));
        }
        updateSaved();
        Array.from(new Set(data.points.map(function (item) { return item.meridian; }))).forEach(function (name) {
          const option = document.createElement("option");
          option.value = name;
          option.textContent = name;
          meridian.append(option);
        });
        meridian.disabled = false;
        Object.keys(reader.chapters).forEach(function (key) {
          const items = data.shanghan.filter(function (item) { return reader.chapterFor(item) === key; });
          if (!items.length) return;
          const option = document.createElement("option");
          option.value = key;
          option.textContent = reader.chapters[key] + " · " + items[0].title.split("조")[0] + "–" + items[items.length - 1].title.split("조")[0] + "조";
          chapter.append(option);
        });
        chapter.disabled = false;
        clauseNumber.disabled = false;
        clauseJump.querySelector("button").disabled = false;
        function matchingCards() {
          return reader.search(data, topic.value, query.value, meridian.value, chapter.value).filter(function (hit) {
            return !savedOnly.checked || saved.includes(hit.topic + "-" + (hit.index + 1));
          });
        }
        function neighbors() {
          const hits = matchingCards().filter(function (hit) { return selected && hit.topic === selected.topic; });
          const position = hits.findIndex(function (hit) { return hit.index === selected.index; });
          return { hits: hits, position: position };
        }
        function updateNavigation() {
          const list = neighbors();
          previous.disabled = list.position <= 0;
          next.disabled = list.position < 0 || list.position >= list.hits.length - 1;
          setText(preview, "[data-daily-preview-position]", "현재 조건의 " + reader.labels[selected.topic] + " " + (list.position + 1) + " / " + list.hits.length);
        }
        function showCard(key, index, focus) {
          selected = { topic: key, index: index };
          preview.className = "daily-km-topic daily-km-topic-" + key;
          preview.hidden = false;
          renderTopic(preview, key, data, kstDate(0), index);
          setText(preview, "[data-preview-topic]", reader.labels[key] + " · 찾아본 카드");
          setText(preview, "[data-topic-count]", (index + 1) + " / " + data[key].length);
          root.querySelector("[data-daily-copy-fallback]").hidden = true;
          root.querySelector("[data-daily-share-status]").textContent = "";
          updateNavigation();
          updateSaved();
          const url = new URL(window.location.href);
          url.searchParams.set("card", key + "-" + (index + 1));
          window.history.replaceState(null, "", url);
          if (focus) {
            preview.querySelector("[data-topic-title]").focus({preventScroll: true});
            preview.scrollIntoView({block: "nearest", behavior: "auto"});
          }
        }
        function renderResults(reset) {
          if (reset) limit = 24;
          const hits = matchingCards();
          status.textContent = hits.length ? hits.length + "개 중 " + Math.min(limit, hits.length) + "개 표시" : "일치하는 카드가 없습니다. 다른 이름이나 용어로 찾아보세요.";
          if (!hits.length && savedOnly.checked) status.textContent = saved.length
            ? "보관한 카드 중 조건에 맞는 카드가 없습니다. 주제나 검색어를 바꿔 보세요."
            : "아직 보관한 카드가 없습니다. 카드에서 ‘이 카드 보관’을 눌러 모아 보세요.";
          results.replaceChildren();
          hits.slice(0, limit).forEach(function (hit) {
            const li = document.createElement("li");
            const button = document.createElement("button");
            button.type = "button";
            const tag = document.createElement("span");
            tag.textContent = reader.labels[hit.topic];
            const title = document.createElement("strong");
            title.textContent = hit.title;
            button.append(tag, title);
            button.addEventListener("click", function () { showCard(hit.topic, hit.index, true); });
            li.append(button);
            results.append(li);
          });
          more.hidden = hits.length <= limit;
        }
        query.disabled = false;
        topic.disabled = false;
        function updateSearch() {
          clauseStatus.textContent = "";
          preview.hidden = true;
          selected = null;
          const url = new URL(window.location.href);
          url.searchParams.delete("card");
          window.history.replaceState(null, "", url);
          renderResults(true);
        }
        query.addEventListener("input", updateSearch);
        savedOnly.addEventListener("change", updateSearch);
        saveButton.addEventListener("click", function () {
          if (!selected) return;
          const id = selectedId(), active = saved.includes(id);
          if (!active && saved.length >= 200) {
            saveStatus.textContent = "200개까지 보관할 수 있습니다. 기존 카드의 보관을 해제한 뒤 추가하세요.";
            return;
          }
          saved = active ? saved.filter(function (value) { return value !== id; }) : saved.concat(id);
          try { window.localStorage.setItem(savedKey, JSON.stringify(saved)); }
          catch (_) { persistent = false; }
          saveStatus.textContent = active ? "카드 보관을 해제했습니다." : "카드를 보관했습니다. ‘보관한 카드만’에서 다시 읽을 수 있습니다.";
          updateSaved();
          if (active && savedOnly.checked) { updateSearch(); savedOnly.focus(); }
          else { renderResults(false); updateNavigation(); }
        });
        function updateFilterVisibility() {
          meridianLabel.hidden = topic.value !== "points";
          if (topic.value !== "points") meridian.value = "all";
          chapterLabel.hidden = topic.value !== "shanghan";
          clauseJump.hidden = topic.value !== "shanghan";
          if (topic.value !== "shanghan") chapter.value = "all";
        }
        topic.addEventListener("change", function () { updateFilterVisibility(); updateSearch(); });
        meridian.addEventListener("change", updateSearch);
        chapter.addEventListener("change", updateSearch);
        clauseJump.addEventListener("submit", function (event) {
          event.preventDefault();
          const card = reader.clauseFrom(clauseNumber.value, data);
          if (!card) {
            clauseStatus.textContent = "1부터 398까지의 조문 번호를 입력하세요.";
            return;
          }
          query.value = "";
          savedOnly.checked = false;
          chapter.value = reader.chapterFor(data.shanghan[card.index]) || "all";
          renderResults(true);
          clauseStatus.textContent = reader.chapters[chapter.value] + "의 " + clauseNumber.value + "조를 열었습니다.";
          showCard(card.topic, card.index, true);
        });
        function moveCard(direction) {
          if (!selected) return;
          const list = neighbors();
          const hit = list.hits[list.position + direction];
          if (list.position >= 0 && hit) showCard(hit.topic, hit.index, true);
        }
        previous.addEventListener("click", function () { moveCard(-1); });
        next.addEventListener("click", function () { moveCard(1); });
        more.addEventListener("click", function () { limit += 24; renderResults(false); });
        root.querySelector("[data-daily-share-card]").addEventListener("click", function () {
          if (!selected) return;
          const url = new URL("/daily-korean-medicine/", window.location.origin);
          url.searchParams.set("card", selected.topic + "-" + (selected.index + 1));
          reader.copyLink(url.href, root.querySelector("[data-daily-copy-fallback]"), root.querySelector("[data-daily-share-status]"));
        });
        const card = reader.cardFrom(new URL(window.location.href).searchParams.get("card"), data);
        if (card) {
          root.open = true;
          topic.value = card.topic;
          showCard(card.topic, card.index, false);
        }
        updateFilterVisibility();
        renderResults(true);
      }).catch(function () {
        status.textContent = "카드 자료를 불러오지 못했습니다. 아래 주제별 문서에서 읽을 수 있습니다.";
      });
    });
  }

  function init() {
    if (!document.querySelector("[data-daily-km-topics]")) return;
    renderAll();
    initBrowser();
    initAlmanacBrowser();
  }

  window.addEventListener("daily-km-offset", function (event) {
    const value = event.detail && Number(event.detail.offset);
    if (Number.isInteger(value)) {
      dayOffset = value;
      renderAll();
    }
  });

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init, { once: true });
  } else {
    init();
  }
  if (typeof document$ !== "undefined") {
    document$.subscribe(init);
  }
})();
