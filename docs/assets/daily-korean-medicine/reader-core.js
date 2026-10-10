/* Date and lookup helpers shared by the daily reading widgets. */
(function (root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  else root.MinseongDailyReader = api;
})(typeof window !== "undefined" ? window : globalThis, function () {
  "use strict";
  const labels = { points: "경혈", herbs: "본초", shanghan: "상한론", sasang: "사상의학" };
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
  function search(data, topic, query, meridian) {
    const terms = String(query || "").trim().split(/\s+/).filter(Boolean).map(normalize);
    const hits = [];
    Object.keys(labels).forEach(function (key) {
      if (topic !== "all" && topic !== key) return;
      (data[key] || []).forEach(function (item, index) {
        if (key === "points" && meridian && meridian !== "all" && item.meridian !== meridian) return;
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
  return { labels: labels, parseDate: parseDate, today: today, offsetFor: offsetFor, dateFor: dateFor,
    titleFor: titleFor, search: search, cardFrom: cardFrom, copyLink: copyLink };
});
