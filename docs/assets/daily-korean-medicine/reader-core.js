/* Date and lookup helpers shared by the daily reading widgets. */
(function (root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  else root.MinseongDailyReader = api;
})(typeof window !== "undefined" ? window : globalThis, function () {
  "use strict";
  const labels = { points: "경혈", herbs: "본초", shanghan: "상한론", sasang: "사상의학" };
  const chapters = { "taiyang-upper": "태양 상편", "taiyang-middle": "태양 중편", "taiyang-lower": "태양 하편",
    yangming: "양명", shaoyang: "소양", taiyin: "태음", shaoyin: "소음", jueyin: "궐음", huoluan: "곽란", recovery: "차후노복" };
  function chapterFor(item) {
    const match = String(item.href || "").match(/\/classics\/shanghanlun\/clauses\/([^/]+)\//);
    return match && chapters[match[1]] ? match[1] : null;
  }
  function clauseFrom(value, data) {
    if (typeof value !== "string" || !/^[1-9]\d{0,2}$/.test(value.trim())) return null;
    const number = Number(value.trim());
    const index = (data.shanghan || []).findIndex(function (item) { return item.title.startsWith(number + "조 ·"); });
    return index < 0 ? null : { topic: "shanghan", index: index };
  }
  function parseDate(value) {
    if (typeof value !== "string" || !/^\d{4}-\d{2}-\d{2}$/.test(value)) return null;
    const parts = value.split("-").map(Number);
    if (parts[0] < 1000) return null;
    const date = new Date(Date.UTC(parts[0], parts[1] - 1, parts[2]));
    return Number.isFinite(date.getTime()) && date.toISOString().slice(0, 10) === value ? date : null;
  }
  function today(now) {
    const values = {};
    new Intl.DateTimeFormat("en-CA", { timeZone: "Asia/Seoul", year: "numeric", month: "2-digit", day: "2-digit" })
      .formatToParts(now || new Date()).forEach(function (part) { values[part.type] = part.value; });
    return parseDate(values.year + "-" + values.month + "-" + values.day);
  }
  function offsetFor(value, now) {
    const date = parseDate(value);
    return date ? Math.round((date - today(now)) / 86400000) : null;
  }
  function dateFor(offset, now) {
    const date = new Date(today(now).getTime() + offset * 86400000);
    return Number.isInteger(offset) && Number.isFinite(date.getTime()) ? date : null;
  }
  function titleFor(topic, item) {
    return topic === "points" ? item.name + " " + item.code + " · " + item.hanja : item.title;
  }
  function normalize(value) { return String(value || "").normalize("NFKC").toLowerCase().replace(/\s+/g, ""); }
  function search(data, topic, query, meridian, chapter) {
    const terms = String(query || "").trim().split(/\s+/).filter(Boolean).map(normalize);
    const hits = [];
    Object.keys(labels).forEach(function (key) {
      if (topic !== "all" && topic !== key) return;
      (data[key] || []).forEach(function (item, index) {
        if (key === "points" && meridian && meridian !== "all" && item.meridian !== meridian) return;
        if (key === "shanghan" && chapter && chapter !== "all" && chapterFor(item) !== chapter) return;
        const title = titleFor(key, item);
        const text = normalize([title, item.meridian, item.location, (item.traditional || []).join(" "), item.summary,
          item.original, item.translation, item.explanation, item.note, item.review,
          (item.related || []).map(function (link) { return link.label; }).join(" ")].filter(Boolean).join(" "));
        if (terms.every(function (term) { return text.includes(term); })) hits.push({ topic: key, index: index, title: title });
      });
    });
    return hits;
  }
  function cardFrom(value, data) {
    const match = typeof value === "string" && value.match(/^(points|herbs|shanghan|sasang)-([1-9]\d{0,3})$/);
    if (!match) return null;
    const index = Number(match[2]) - 1;
    return data[match[1]] && data[match[1]][index] ? { topic: match[1], index: index } : null;
  }
  function savedCards(raw, data) {
    let values;
    try { values = JSON.parse(raw); } catch (_) { return []; }
    if (!Array.isArray(values)) return [];
    return Array.from(new Set(values.filter(function (value) { return cardFrom(value, data); }))).slice(0, 200);
  }
  function seasonalCard(date, data) {
    if (!(date instanceof Date) || !Number.isFinite(date.getTime())) return null;
    const month = date.getUTCMonth(), year = date.getUTCFullYear();
    const season = month >= 2 && month <= 4 ? "spring" : month >= 5 && month <= 7 ? "summer" : month >= 8 && month <= 10 ? "autumn" : "winter";
    const startMonth = {spring: 2, summer: 5, autumn: 8, winter: 11}[season];
    const start = Date.UTC(season === "winter" && month < 2 ? year - 1 : year, startMonth, 1);
    const items = (data.cards || []).filter(function (item) { return item.season === season; });
    if (!items.length) return null;
    const index = Math.floor((date.getTime() - start) / 86400000) % items.length;
    return { item: items[index], season: season, index: index, count: items.length };
  }
  async function copyLink(href, fallback, status) {
    try {
      await navigator.clipboard.writeText(href);
      fallback.hidden = true;
      status.textContent = "링크를 복사했습니다.";
    } catch (_) {
      fallback.value = href;
      fallback.hidden = false;
      fallback.focus();
      fallback.select();
      status.textContent = "아래 주소를 선택해 복사하세요.";
    }
  }
  return { labels: labels, chapters: chapters, chapterFor: chapterFor, clauseFrom: clauseFrom,
    parseDate: parseDate, today: today, offsetFor: offsetFor, dateFor: dateFor,
    titleFor: titleFor, search: search, cardFrom: cardFrom, savedCards: savedCards,
    seasonalCard: seasonalCard, copyLink: copyLink };
});
