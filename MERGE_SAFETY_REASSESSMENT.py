from pathlib import Path
root=Path("docs/symptom-integrated")
files=["pain.md","sleep-fatigue.md","digestive.md","respiratory-rhinitis.md","autonomic-stress.md"]
marker="## 안전성과 재평가"
block="""## 안전성과 재평가

치료 전에 위험신호·복용약·기저질환을 확인하고, 치료 후에는 증상 강도뿐 아니라 **실제 기능과 생활 변화**를 같은 기준으로 다시 봅니다.

→ [치료 안전성·회복신호·근거](treatment-evidence.md)
"""
for fn in files:
    p=root/fn
    if not p.exists():
        print("SKIP:",fn); continue
    t=p.read_text(encoding="utf-8")
    if marker not in t:
        p.write_text(t.rstrip()+"\n\n"+block+"\n",encoding="utf-8")
        print("UPDATED:",fn)
    else:
        print("OK:",fn)
