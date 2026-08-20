from pathlib import Path

ROOT=Path("docs/formulas")
LINKS = {'huanglian-jiedu-tang.md': [('황련', '../herbs/coptis.md'), ('치자', '../herbs/gardenia.md'), ('황금', '../herbs/scutellaria.md'), ('황백', '../herbs/phellodendron.md')], 'longdan-xiegan-tang.md': [('치자', '../herbs/gardenia.md'), ('차전자', '../herbs/plantago-seed.md'), ('시호', '../herbs/bupleurum.md'), ('황금', '../herbs/scutellaria.md')], 'pingwei-san.md': [('후박', '../herbs/magnolia-bark.md'), ('진피', '../herbs/citrus-peel.md'), ('생강', '../herbs/fresh-ginger.md')], 'xiangsha-liujunzi-tang.md': [('사인', '../herbs/amomum.md'), ('목향', '../herbs/aucklandia.md'), ('향부자', '../herbs/cyperus.md'), ('후박', '../herbs/magnolia-bark.md')], 'banxia-houpo-tang.md': [('후박', '../herbs/magnolia-bark.md'), ('자소엽', '../herbs/perilla-leaf.md'), ('생강', '../herbs/fresh-ginger.md'), ('반하', '../herbs/pinellia.md')], 'xuefu-zhuyu-tang.md': [('도인', '../herbs/peach-kernel.md'), ('홍화', '../herbs/safflower.md'), ('우슬', '../herbs/achyranthes.md'), ('시호', '../herbs/bupleurum.md')], 'buyang-huanwu-tang.md': [('홍화', '../herbs/safflower.md'), ('도인', '../herbs/peach-kernel.md'), ('우슬', '../herbs/achyranthes.md')], 'taohe-chengqi-tang.md': [('도인', '../herbs/peach-kernel.md'), ('육계', '../herbs/cinnamon-bark.md')], 'duhuo-jisheng-classic.md': [('두충', '../herbs/eucommia.md'), ('우슬', '../herbs/achyranthes.md'), ('속단', '../herbs/dipsacus.md')], 'zhenwu-tang.md': [('부자', '../herbs/aconite.md'), ('생강', '../herbs/fresh-ginger.md'), ('복령', '../herbs/poria.md')], 'wuling-san.md': [('택사', '../herbs/alisma.md'), ('복령', '../herbs/poria.md'), ('육계', '../herbs/cinnamon-bark.md')], 'bazheng-san.md': [('차전자', '../herbs/plantago-seed.md'), ('치자', '../herbs/gardenia.md')], 'shengmai-san.md': [('맥문동', '../herbs/ophiopogon.md')], 'tianwang-buxin-dan.md': [('원지', '../herbs/polygala.md'), ('백자인', '../herbs/thuja-seed.md'), ('용안육', '../herbs/longan.md'), ('단삼', '../herbs/salvia.md')], 'guipi-classic.md': [('원지', '../herbs/polygala.md'), ('용안육', '../herbs/longan.md'), ('목향', '../herbs/aucklandia.md')], 'jiawei-wendan-tang.md': [('향부자', '../herbs/cyperus.md'), ('지실', '../herbs/citrus-immature.md'), ('시호', '../herbs/bupleurum.md')], 'xiaoyao-san.md': [('시호', '../herbs/bupleurum.md'), ('박하', '../herbs/mint.md'), ('생강', '../herbs/fresh-ginger.md')], 'jiawei-xiaoyao-san.md': [('목단피', '../herbs/moutan.md'), ('치자', '../herbs/gardenia.md'), ('황금', '../herbs/scutellaria.md')], 'maxing-ganshi-tang.md': [('행인', '../herbs/apricot-kernel.md')], 'xingsu-san.md': [('행인', '../herbs/apricot-kernel.md'), ('자소엽', '../herbs/perilla-leaf.md'), ('생강', '../herbs/fresh-ginger.md')], 'jingjie-lianqiao-tang.md': [('금은화', '../herbs/honeysuckle.md'), ('우방자', '../herbs/arctium.md'), ('치자', '../herbs/gardenia.md')]}

for fn, links in LINKS.items():
    p=ROOT/fn
    if not p.exists():
        print("SKIP (file not found):", p)
        continue
    text=p.read_text(encoding="utf-8")
    marker="## 핵심 본초 연결"
    if marker in text:
        print("OK already:", fn)
        continue
    lines=["", marker, "", "이 처방을 구성하는 주요 본초를 개별 본초 페이지와 연결합니다.", ""]
    for name, href in links:
        lines.append(f"- [{name}]({href})")
    lines += ["", "→ [본초 찾기](../herbal-integrated/herbs.md)", "→ [주요 본초 비교·감별](../herbal-integrated/herb-comparisons.md)", ""]
    p.write_text(text.rstrip()+"\n"+"\n".join(lines),encoding="utf-8")
    print("UPDATED:", fn)

print("완료: 기존 처방 페이지 안에 핵심 본초 연결을 병합했습니다.")
