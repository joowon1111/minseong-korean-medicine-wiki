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
  for (const p of pages) assert.ok(read(p).length >= 1900, p);
});

test("four constitution clinical-detail pages keep substantive depth", () => {
  for (const c of ["soyangin","taeeumin","soeumin","taeyangin"]) {
    const p = `docs/sasang-clinical-detail/${c}.md`;
    assert.ok(Buffer.byteLength(read(p), "utf8") >= (c === "taeyangin" ? 8000 : 9000), p);
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
  for (const p of pages) assert.ok(read(p).length >= 2300, p);
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


test("every explorer disease group is represented in deep clinical-detail pages", () => {
  const expected = {
    "docs/sasang-clinical-detail/soyangin.md": ["소양상풍·얕은 표병","표병·결흉/흉격 불편","신열두통망음·배설 변화","망음·설사/복통","흉격열·리열","장관 열·이질 방향","강한 리열·이열변폐","음허오열·하소/허로"],
    "docs/sasang-clinical-detail/taeeumin.md": ["표한·한궐/통증","표한·비위담습/조위","표한·승청 저하","표한·승청과 호흡","병후체허·폐원 회복","간열·폐조","리열·양독/조열·심신","강한 리열·승기/정체"],
    "docs/sasang-clinical-detail/soeumin.md": ["태양증·울광 초기","표병·기체/두통·소화","망양초증·승양","망양 심화·부자 배합","태음병·한습/리한","태음병·구토/급성 토사","소음병·깊은 리한/장궐","리한·기체/흉복통·황달/음독"]
  };
  for (const [p, terms] of Object.entries(expected)) {
    const text = read(p);
    for (const term of terms) assert.ok(text.includes(term), p + " missing " + term);
  }
  const ty = read("docs/sasang-clinical-detail/taeyangin.md");
  assert.ok(ty.includes("외감요척병·해역"));
  assert.ok(ty.includes("내촉소장병·열격/반위"));
});

test("progression and severity layers do not regress to stubs", () => {
  for (const dir of ["sasang-progression","sasang-severity"]) {
    const base = path.join(root, "docs", dir);
    for (const name of fs.readdirSync(base)) {
      if (!name.endsWith(".md") || name === "references.md") continue;
      const text = fs.readFileSync(path.join(base, name), "utf8");
      assert.ok(Buffer.byteLength(text, "utf8") >= 2000, dir + "/" + name);
    }
  }
});
