const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

class FakeElement {
  constructor(tag = "div") {
    this.tagName = tag.toUpperCase();
    this.value = "";
    this.disabled = false;
    this.textContent = "";
    this._innerHTML = "";
    this.children = [];
    this.listeners = {};
    this.focused = false;
  }
  append(child) { this.children.push(child); }
  addEventListener(type, fn) { (this.listeners[type] ||= []).push(fn); }
  dispatch(type) { for (const fn of this.listeners[type] || []) fn({ target: this }); }
  focus() { this.focused = true; }
  set innerHTML(value) { this._innerHTML = value; if (value === "") this.children = []; }
  get innerHTML() { return this._innerHTML; }
}

function boot() {
  const ids = ["sx-constitution","sx-axis","sx-stage","sx-results","sx-summary","sx-reset"];
  const elements = Object.fromEntries(ids.map(id => [id, new FakeElement(id === "sx-reset" ? "button" : "div")]));
  const document = {
    getElementById: id => elements[id] || null,
    createElement: tag => new FakeElement(tag),
  };
  const script = fs.readFileSync(path.join(__dirname, "../docs/assets/sasang-explorer.js"), "utf8");
  vm.runInNewContext(script, { document, console, Set, String });
  return elements;
}

test("Sasang explorer filters constitution, axis and stage, then resets", () => {
  const e = boot();
  e["sx-constitution"].value = "소양인";
  e["sx-constitution"].dispatch("change");

  assert.equal(e["sx-axis"].disabled, false);
  assert.deepEqual(
    e["sx-axis"].children.map(x => x.value),
    ["", "소양상풍·표병", "표병·결흉/흉격 불편", "신열두통망음·배설 변화", "망음·설사/복통", "흉격열·리열", "장관 열·이질", "강한 리열·이열변폐", "음허오열·하소/허로"]
  );

  e["sx-axis"].value = "흉격열·리열";
  e["sx-axis"].dispatch("change");
  assert.equal(e["sx-stage"].disabled, false);
  assert.ok(e["sx-stage"].children.some(x => x.value === "흉격열·리열"));

  e["sx-stage"].value = "흉격열·리열";
  e["sx-stage"].dispatch("change");
  assert.match(e["sx-results"].innerHTML, /양격산화탕/);
  assert.match(e["sx-results"].innerHTML, /감별 포인트/);
  assert.match(e["sx-summary"].textContent, /학습용 연결/);

  e["sx-reset"].dispatch("click");
  assert.equal(e["sx-constitution"].value, "");
  assert.equal(e["sx-axis"].disabled, true);
  assert.equal(e["sx-stage"].disabled, true);
  assert.equal(e["sx-results"].innerHTML, "");
  assert.equal(e["sx-constitution"].focused, true);
});

test("Explorer exposes eight major disease groups for three constitutions and preserves Taeyangin evidence limits", () => {
  for (const constitution of ["소양인","태음인","소음인","태양인"]) {
    const e = boot();
    e["sx-constitution"].value = constitution;
    e["sx-constitution"].dispatch("change");
    assert.equal(e["sx-axis"].disabled, false);
    assert.ok(e["sx-axis"].children.length >= 2, constitution);
  }
});

test("Explorer includes learning-only notice and responsive mobile CSS", () => {
  const page = fs.readFileSync(path.join(__dirname, "../docs/sasang-explorer/index.md"), "utf8");
  const css = fs.readFileSync(path.join(__dirname, "../docs/assets/sasang-explorer.css"), "utf8");
  assert.match(page, /학습·문서 탐색용 도구입니다/);
  assert.match(page, /진단하거나 개인별 처방을 추천하지 않습니다/);
  assert.match(css, /grid-template-columns:repeat\(3,minmax\(0,1fr\)\) auto/);
  assert.match(css, /@media\(max-width:760px\)/);
  assert.match(css, /\.sasang-explorer__controls\{grid-template-columns:1fr\}/);
});
