const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");

const root = path.join(__dirname, "..");
const read = p => fs.readFileSync(path.join(root, p), "utf8");

test("core Sasang differential pages keep substantive depth", () => {
  const pages = [
    "docs/sasang-pattern-differential/soyangin-severity-map.md",
    "docs/sasang-pattern-differential/soeumin-severity-map.md",
    "docs/sasang-pattern-differential/taeeumin-exterior-vs-interior.md",
    "docs/sasang-pattern-differential/soyangin-mangeum-vs-chestheat.md",
    "docs/sasang-pattern-differential/soeumin-taeeum-vs-soeum.md",
    "docs/sasang-pattern-differential/taeyangin-haeyeok-vs-yeolgeok.md",
    "docs/sasang-pattern-differential/interview-algorithm.md",
    "docs/sasang-pattern-differential/four-constitution-map.md",
  ];
  for (const p of pages) assert.ok(read(p).length >= 2000, p);
});

test("four constitution clinical-detail pages keep substantive depth", () => {
  for (const c of ["soyangin","taeeumin","soeumin","taeyangin"]) {
    const p = `docs/sasang-clinical-detail/${c}.md`;
    assert.ok(read(p).length >= 3500, p);
  }
});

test("short-form Sasang prescription cards stay above minimum depth", () => {
  const pages = [
    "docs/sasang-formula-cards/seungyangpalmul-tang.md",
    "docs/sasang-formula-cards/baekhao-ijung-tang.md",
    "docs/sasang-formula-cards/insamgyejibujatang.md",
    "docs/sasang-formula-cards/cheongpyesagan-tang.md",
    "docs/sasang-formula-cards/hyangbujapalmul-tang.md",
    "docs/sasang-formula-cards/hyeongbangjihwang-tang.md",
    "docs/sasang-formula-cards/gwangye-buja-ijung-tang.md",
    "docs/sasang-formula-cards/cheongsimyeonja-tang.md",
    "docs/sasang-formula-cards/yanggyeoksanhwa-tang.md",
    "docs/sasang-formula-cards/gwakhyangjeonggi-san.md",
    "docs/sasang-formula-cards/hyeongbangdojeok-san.md",
    "docs/sasang-formula-cards/taeeumjowi-tang.md",
  ];
  for (const p of pages) assert.ok(read(p).length >= 2800, p);
});

function sectionLengths(content) {
  const matches = [...content.matchAll(/^##\s+(.+)$/gm)];
  return matches.map((m, i) => ({
    title: m[1],
    length: (i + 1 < matches.length ? matches[i + 1].index : content.length) - (m.index + m[0].length),
  }));
}

test("extended Sasang formula sections are not stub entries", () => {
  const configs = [
    ["docs/sasang-formula-library/soyangin-extended-formulas.md", 850],
    ["docs/sasang-formula-library/taeeumin-extended-formulas.md", 850],
    ["docs/sasang-formula-library/soeumin-extended-formulas.md", 750],
  ];
  for (const [p, min] of configs) {
    const sections = sectionLengths(read(p)).filter(x => !x.title.startsWith("공통 "));
    for (const s of sections) assert.ok(s.length >= min, `${p} :: ${s.title} (${s.length})`);
  }
});
