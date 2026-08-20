from pathlib import Path
root=Path("docs/symptom-integrated")
mapping={
"pain.md":["허리 삐끗","허리에서 다리까지 당김","뒷목 당김","거북목 통증","오십견","무릎 시큰","지끈거리는 두통","손발 찌릿"],
"sleep-fatigue.md":["잠이 안 옴","자꾸 깸","잠이 얕음","자고 나도 피곤","기운 없음","두근거림","긴장성 근육통"],
"digestive.md":["자주 체함","식후 더부룩","배에 가스","입맛 없음","속 울렁거림","잦은 설사","심한 변비"],
"respiratory-rhinitis.md":["재채기","맑은 콧물","코막힘","축농증 느낌","목 붓기","오래가는 기침","가래","쌕쌕거림"],
"autonomic-stress.md":["머리가 띵함","스트레스성 체기","목 이물감","손발 차가움","얼굴 붓기","다리 부종","가슴 답답 열감"]
}
marker="## 환자가 이렇게도 검색합니다"
for fn,terms in mapping.items():
    p=root/fn
    if not p.exists():
        print("SKIP:",fn); continue
    t=p.read_text(encoding="utf-8")
    if marker in t:
        print("OK:",fn); continue
    block=marker+"\n\n"+ " · ".join(terms)+"\n"
    p.write_text(t.rstrip()+"\n\n"+block+"\n",encoding="utf-8")
    print("UPDATED:",fn)
