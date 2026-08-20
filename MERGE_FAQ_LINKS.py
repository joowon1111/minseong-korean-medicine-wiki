from pathlib import Path
root=Path("docs/symptom-integrated")
files=["pain.md","sleep-fatigue.md","digestive.md","respiratory-rhinitis.md","autonomic-stress.md"]
marker="## 환자가 자주 묻는 치료 질문"
block="""## 환자가 자주 묻는 치료 질문

이 증상의 한약 선택 기준, 침과 한약을 함께 쓰는 이유, 치료기간과 회복신호, 안전성은  
→ [치료·경과·근거 FAQ](treatment-evidence.md)에서 이어서 봅니다.
"""
for fn in files:
    p=root/fn
    if not p.exists():
        print("SKIP:",fn); continue
    text=p.read_text(encoding="utf-8")
    if marker not in text:
        p.write_text(text.rstrip()+"\n\n"+block+"\n",encoding="utf-8")
        print("UPDATED:",fn)
    else:
        print("OK:",fn)
