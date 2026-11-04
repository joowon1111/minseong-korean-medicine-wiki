/* Date and lookup helpers shared by the daily reading widgets. */
(function (root, factory) {
  const api = factory(typeof module === "object" && module.exports ? require("./calendar-core.js") : root.MinseongCalendar,
    typeof module === "object" && module.exports ? require("../solar-terms/calculator.js") : root.MinseongSolarTerms);
  if (typeof module === "object" && module.exports) module.exports = api;
  else root.MinseongDailyReader = api;
})(typeof window !== "undefined" ? window : globalThis, function (calendar, solarTerms) {
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
  const termYears = new Map(), termDecades = new Map(), calendarNodes = new Map();
  let termMetadata, calendarTimer;
  function loadTermEvents(year) {
    if (year < 1900 || year > 2100) return Promise.resolve(null);
    if (!termYears.has(year)) {
      function json(path) { return fetch(path, {credentials:"same-origin"}).then(r => { if(!r.ok)throw new Error("Calendar unavailable");return r.json(); }); }
      if (!termMetadata) termMetadata = json("/assets/solar-terms/de440/metadata.json?v=20261101");
      const decade = Math.floor(year / 10) * 10;
      if (!termDecades.has(decade)) termDecades.set(decade, json("/assets/solar-terms/de440/" + decade + ".json?v=20261101"));
      termYears.set(year, Promise.all([termMetadata,termDecades.get(decade)]).then(([metadata,data]) =>
        solarTerms.calculateYear(year,data.years[String(year)],metadata)).catch(error => {
          termYears.delete(year); termDecades.delete(decade); termMetadata = null; throw error;
        }));
    }
    return termYears.get(year);
  }
  function renderCalendarDate(node, date, now) {
    if (!node || !(date instanceof Date) || !Number.isFinite(date.getTime())) return;
    now = now || new Date();
    const key = date.toISOString().slice(0,10), doc = node.ownerDocument;
    node.textContent = new Intl.DateTimeFormat("ko-KR", {timeZone:"UTC",year:"numeric",month:"long",day:"numeric",weekday:"short"}).format(date);
    node.setAttribute("datetime",key); node.classList.add("daily-calendar-date");
    node.dataset.calendarDate = key;
    if (!calendar) return;
    const details = doc.createElement("span");details.className = "daily-calendar-details";details.setAttribute("data-calendar-details","");
    const lunar = calendar.lunarFor(date), moon = calendar.moonFor(date);
    function line(text,marker) { const span=doc.createElement("span");span.textContent=text;if(marker)span.setAttribute(marker,"");details.append(span);return span; }
    line(lunar ? "음력 " + lunar.year + "년 " + (lunar.intercalation?"윤":"") + lunar.month + "월 " + lunar.day + "일" : "음력: 1900–2050년 지원", "data-calendar-lunar");
    if (moon) {
      const phase=line(moon.emoji+" "+moon.label+" · 밝은 면 "+Math.round(moon.fraction*100)+"%","data-calendar-moon");
      phase.title="한국 시간 정오 기준 달 모양의 근사 계산값";
    }
    const ganji=line("만세력 계산 중…","data-calendar-pillars");node.append(details);
    const instant = key === today(now).toISOString().slice(0,10) ? now : new Date(date.getTime()+3*3600000);
    loadTermEvents(date.getUTCFullYear()).then(events => {
      if (!node.isConnected || node.dataset.calendarDate!==key || details.parentNode!==node) return;
      const result=calendar.pillarsAt(instant,events);
      ganji.textContent=result?"만세력 · "+result.year+" "+result.month+" "+result.day:"만세력: 1900–2100년 지원";
      if (!events) return;
      const boundary=events.find(e => e.termIndex%2===1 && new Date(e.milliseconds+9*3600000).toISOString().slice(0,10)===key);
      if (boundary) {
        const before=calendar.pillarsAt(new Date(boundary.milliseconds-1),events),after=calendar.pillarsAt(new Date(boundary.milliseconds+1),events);
        line(solarTerms.TERMS[boundary.termIndex][0]+" "+solarTerms.displayTime(boundary.milliseconds).time+" · "+before.month+" → "+after.month,"data-calendar-boundary");
      }
    }).catch(() => { if(details.parentNode===node)ganji.textContent="만세력 계산을 불러오지 못했습니다."; });
    calendarNodes.set(node,date);
    if (!calendarTimer && typeof window !== "undefined") calendarTimer=window.setInterval(() => {
      calendarNodes.forEach((value,element) => { if(!element.isConnected)calendarNodes.delete(element);else renderCalendarDate(element,value); });
      if(!calendarNodes.size){window.clearInterval(calendarTimer);calendarTimer=null;}
    },30000);
  }
  function titleFor(topic, item) {
    return topic === "points" ? item.name + " " + item.code + " · " + item.hanja : item.title;
  }
  function normalize(value) { return String(value || "").normalize("NFKC").toLowerCase().replace(/\s+/g, ""); }
  function reviewFor(item) {
    if (!item || typeof item.reviewQuestion !== "string" || typeof item.reviewAnswer !== "string") return null;
    const question = item.reviewQuestion.trim(), answer = item.reviewAnswer.trim();
    return question && answer ? { question: question, answer: answer } : null;
  }
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
          item.original, item.translation, item.explanation, item.note, item.review, item.reviewQuestion, item.reviewAnswer,
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
    const dateKey = date.toISOString().slice(0, 10);
    const items = (data.cards || []).filter(function (item) {
      return item.season === season && (!item.introducedOn || item.introducedOn <= dateKey);
    });
    if (!items.length) return null;
    const index = Math.floor((date.getTime() - start) / 86400000) % items.length;
    return { item: items[index], season: season, index: index, count: items.length };
  }
  const seasons = { spring: "봄", summer: "여름", autumn: "가을", winter: "겨울" };
  function solarTermFor(date, data) {
    if (!(date instanceof Date) || !Number.isFinite(date.getTime())) return null;
    const calendar = data.solarCalendar;
    if (!calendar || calendar.timezone !== "Asia/Seoul") return null;
    const key = date.toISOString().slice(0, 10);
    const dates = (calendar.years || {})[key.slice(0, 4)];
    if (!Array.isArray(dates) || dates.length !== 24) return null;
    const index = dates.indexOf(key.slice(5));
    if (index < 0) return null;
    const name = (calendar.order || [])[index];
    const item = (data.cards || []).find(function (card) { return card.solarTerm === name; });
    return item ? { item: item, date: key, sourceHref: calendar.sourceHref } : null;
  }
  function almanacFrom(value, data) {
    if (typeof value !== "string" || !/^(spring|summer|autumn|winter)-[0-9]{2,3}$/.test(value)) return null;
    return (data.cards || []).find(function (item) { return item.id === value; }) || null;
  }
  function searchAlmanac(data, season, query, topic) {
    const terms = String(query || "").trim().split(/\s+/).filter(Boolean).map(normalize);
    return (data.cards || []).filter(function (item) {
      if (season !== "all" && item.season !== season) return false;
      if (topic && topic !== "all" && item.topic !== topic) return false;
      const source = (data.sources || {})[item.source] || {};
      const text = normalize([seasons[item.season], (data.topics || {})[item.topic], item.theme, item.line, item.practice, item.story, item.solarTerm,
        item.termHanja, item.termMeaning, item.termKnowledge, item.termMedicine,
        source.original, source.translation, source.words, source.label, source.context].filter(Boolean).join(" "));
      return terms.every(function (term) { return text.includes(term); });
    });
  }
  function almanacText(item, data) {
    const source = data.sources[item.source], modern = data.modern && data.modern[item.modern];
    const lines = ["양생(養生) · " + seasons[item.season] + " · " + item.theme,
      "생활 제안 — " + item.line];
    if (item.story) lines.push("오늘의 한의학 이야기 — " + item.story);
    if (item.solarTerm && item.termMeaning) lines.push("절기의 이름과 뜻 — " + item.solarTerm + "(" + item.termHanja + ") · " + item.termMeaning,
      "알아두면 좋은 이야기 — " + item.termKnowledge, "한의학과 오늘의 생활 — " + item.termMedicine,
      "절기 자료 — " + item.termSource, "절기 날짜 자료 — " + data.solarCalendar.sourceHref);
    lines.push("오늘의 작은 실천 — " + item.practice);
    if (source) lines.push("고전 원문 — " + source.original, "원문 풀이 — " + source.translation,
      "출처 — " + source.label, source.href);
    if (modern) lines.push("현대 생활 자료 — " + modern.label, modern.href);
    if (item.relatedHref) lines.push("아카이브에서 이어 읽기 — https://wiki.minseong.co.kr" + item.relatedHref);
    return lines.join("\n\n");
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
    parseDate: parseDate, today: today, offsetFor: offsetFor, dateFor: dateFor, renderCalendarDate: renderCalendarDate,
    titleFor: titleFor, reviewFor: reviewFor, search: search, cardFrom: cardFrom, savedCards: savedCards,
    seasonalCard: seasonalCard, solarTermFor: solarTermFor, seasons: seasons, almanacFrom: almanacFrom,
    searchAlmanac: searchAlmanac, almanacText: almanacText, copyLink: copyLink };
});
