/* Daily study streams for the archive. Data is fetched from this site's curated JSON only. */
(function () {
  "use strict";

  const dataUrl = "/assets/daily-korean-medicine/data.json?v=20261007-03";
  let dataPromise;
  let dayOffset = 0;

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
  "/herbs/mint/": "B00261",
  "/herbs/pinellia/": "B00132",
  "/herbs/platycodon/": "B00076",
  "/herbs/poria/": "B00356",
  "/herbs/rehmannia-root-fresh/": "B00050",
  "/herbs/schisandra/": "B00211",
  "/herbs/scutellaria/": "B00072",
  "/herbs/white-peony/": "B00026",
  "/herbs/codonopsis/": "B00021",
  "/herbs/sarsaparilla/": "B00015"
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

  function renderTopic(root, topic, data, date) {
    const epoch = absoluteDay(date);
    const items = data[topic];
    const index = topic === "points"
      ? dayOfYear(date) % items.length
      : ((epoch % items.length) + items.length) % items.length;
    const item = items[index];

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
      setOptional(root, "[data-topic-note]", "");
      setOptional(root, "[data-topic-edition]", "");
      setLink(root, "[data-topic-reference]", item.reference, "표준 경혈 위치 자료 확인 ↗");
    } else if (topic === "herbs") {
      setText(root, "[data-topic-count]", "오늘의 본초 " + (index + 1) + " / " + items.length);
      setText(root, "[data-topic-title]", item.title);
      setText(root, "[data-topic-summary]", item.summary);
      setLink(root, "[data-topic-link]", item.href, "본초 문서에서 더 읽기 →");
      setOptional(root, "[data-topic-original]", "");
      setOptional(root, "[data-topic-translation]", "");
      setOptional(root, "[data-topic-note]", "");
      setOptional(root, "[data-topic-edition]", "");
      const catalogRecord = typeof item.href === "string" ? hkbuHerbReferences[item.href] : "";
      const providedCatalogUrl = typeof item.reference === "string" && item.reference.startsWith("https://sys01.lib.hkbu.edu.hk/cmed/mmid/detail.php?pid=")
        ? item.reference
        : "";
      const catalogUrl = providedCatalogUrl || (catalogRecord
        ? "https://sys01.lib.hkbu.edu.hk/cmed/mmid/detail.php?lang=cht&pid=" + encodeURIComponent(catalogRecord)
        : "");
      setLink(root, "[data-topic-hkbu-reference]", catalogUrl, "약재 사진·한자 주치 정보(HKBU) ↗");
      const otherReference = providedCatalogUrl ? "" : item.reference;
      setLink(root, "[data-topic-reference]", otherReference, item.referenceLabel || "본초 출전·자료 확인 ↗");
    } else {
      const label = topic === "shanghan" ? "오늘의 상한론 조문 " : "오늘의 동의수세보원 구절 ";
      setText(root, "[data-topic-count]", label + (index + 1) + " / " + items.length);
      setText(root, "[data-topic-title]", item.title);
      setText(root, "[data-topic-summary]", item.originalLabel || "");
      setOptional(root, "[data-topic-original]", item.original);
      setOptional(root, "[data-topic-translation]", item.translation ? "아카이브 풀이 — " + item.translation : "");
      setOptional(root, "[data-topic-note]", item.note ? "읽는 포인트 — " + item.note : "");
      setOptional(root, "[data-topic-edition]", item.edition ? "출전·판본 — " + item.edition : "");
      setLink(root, "[data-topic-link]", item.href, "관련 원문·해설 보기 →");
      setLink(root, "[data-topic-reference]", item.reference, "원문 자료 확인 ↗");
    }

    const dateNode = root.querySelector("[data-topic-date]");
    if (dateNode) {
      dateNode.textContent = formatDate(date);
      dateNode.setAttribute("datetime", date.toISOString().slice(0, 10));
    }
  }

  function renderAll() {
    const widgets = document.querySelectorAll("[data-daily-km-topics]");
    if (!widgets.length) return;
    const date = kstDate(dayOffset);
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

  function init() {
    if (!document.querySelector("[data-daily-km-topics]")) return;
    renderAll();
  }

  window.addEventListener("daily-km-offset", function (event) {
    const value = event.detail && Number(event.detail.offset);
    if (Number.isFinite(value)) {
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
