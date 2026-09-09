"""Build original, non-anatomical concept diagrams for the acupuncture science pages."""
from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / 'docs/assets/acupuncture-science'
INK = '#172d43'
TEAL = '#087f8c'
BLUE = '#4465aa'


def label(x, y, lines, size=21, color=INK, anchor='middle', weight=400):
    return ''.join(f'<text x="{x}" y="{y+i*30}" font-size="{size}" fill="{color}" text-anchor="{anchor}" font-weight="{weight}">{escape(t)}</text>' for i, t in enumerate(lines))


def box(x, y, w, h, title, sub=(), tone='teal'):
    fill, stroke = ('#e9f7f5', TEAL) if tone == 'teal' else ('#eef2fb', BLUE) if tone == 'blue' else ('#fff5e7', '#ad7220')
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{fill}" stroke="{stroke}" stroke-width="2"/>' + label(x+w/2, y+38, [title], 25, stroke, weight=700) + label(x+w/2, y+72, sub, 21)


def arrow(path, color=TEAL, dashed=False):
    dash = ' stroke-dasharray="8 6"' if dashed else ''
    return f'<path d="{path}" fill="none" stroke="{color}" stroke-width="3"{dash} marker-end="url(#arrow-{color[1:]})"/>'


def save(name, title, desc, body, height, footer):
    markers=''.join(f'<marker id="arrow-{c[1:]}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 Z" fill="{c}"/></marker>' for c in (TEAL, BLUE))
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 {height}" width="960" height="{height}" role="img" aria-labelledby="title desc" lang="ko">
<title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc>
<defs>{markers}</defs>
<g font-family="Noto Sans KR,Malgun Gothic,Apple SD Gothic Neo,sans-serif">
<rect width="960" height="{height}" rx="18" fill="#f8fafc"/>
{label(36,46,[title],30,anchor='start',weight=700)}
{body}
{label(36,height-28,[footer],19,'#526477',anchor='start')}
</g></svg>'''
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/name).write_text(svg+'\n',encoding='utf-8')


def main():
    body=box(40,85,400,106,'조직 자극',['피부 · 근육 · 근막'])+box(520,85,400,106,'국소 반응',['기계적 변형 · 생화학 신호'])
    body+=arrow('M440 138 H520')+arrow('M240 191 V245')
    body+=box(40,245,400,106,'체성감각 입력',['말초 감각신경'])
    body+=box(520,245,400,106,'척수 · 뇌의 통합',['통각 전달 · 감각 · 주의 · 정서'],'blue')+arrow('M440 298 H520')
    body+=box(40,415,400,106,'통증조절 경로',['분절성 · 하행성 조절'],'blue')+box(520,415,400,106,'자율신경 반사',['교감 · 부교감 출력'],'blue')
    body+=arrow('M650 351 V383 H240 V415',BLUE)+arrow('M790 351 V415',BLUE)
    body+=box(40,585,880,108,'임상효과는 별도로 비교·평가',['통증 · 기능 · 삶의 질 · 지속효과 · 이상반응'],'amber')
    body+=label(480,559,['기전 관찰과 환자 결과를 연결해 연구'],21,'#526477')
    save('overview.svg','침 자극을 연구하는 네 가지 층위','조직 자극은 국소 반응과 감각 입력에 연결된다. 척수와 뇌의 통합은 통증조절과 자율신경 반사에 연결되며 임상효과는 별도 평가한다.',body,760,'원본 개념도 · 화살표는 기능적 관계이며 모든 단계의 작동이나 임상효과를 보증하지 않습니다.')

    body=box(40,90,400,112,'국소조직의 변형',['침과 조직의 물리적 상호작용'])
    body+=box(520,90,400,112,'국소 생화학 반응',['ATP · 아데노신 등'])+arrow('M440 146 H520')
    body+=box(40,270,400,112,'감각신경 말단',['Aβ · Aδ · C 등'])+arrow('M240 202 V270')
    body+=box(520,270,400,112,'아데노신 A1 수용체',['국소 항통각 기전 연구'])+arrow('M720 202 V270')
    body+=box(40,450,880,112,'몸통·팔다리: 일차감각 뉴런 → 척수',['세포체: 후근신경절(DRG) · 통각 처리: 척수 후각'])+arrow('M240 382 V450')
    body+=label(480,609,['감각 입력(구심성)과 근육으로 가는 운동 출력(원심성)을 구분'],22)
    body+=label(480,646,['얼굴 감각은 주로 삼차신경계 경로로 전달'],22)
    save('peripheral.svg','말초조직에서 신경계로','조직 자극의 감각 경로와 국소 아데노신 반응을 구분한 개념도. DRG는 일차감각 뉴런의 세포체 위치이며 시냅스 중계핵이 아니다.',body,720,'원본 개념도 · 본문의 사람·동물 연구 구분을 함께 읽습니다. 실제 자침 경로가 아닙니다.')

    body=box(60,95,380,110,'뇌의 감각·인지·정서 처리',['시상 · 감각피질 · 관련 네트워크'],'blue')
    body+=box(540,95,360,110,'뇌간 조절 네트워크',['PAG · RVM · 청반 등'],'blue')+arrow('M440 150 H540',BLUE)
    body+=box(280,325,400,115,'척수 후각',['국소 회로 · 통각 전달 조절'])
    body+=arrow('M340 325 V245 H230 V205')+label(105,278,['상행 입력'],21,TEAL,anchor='start')
    body+=arrow('M720 205 V385 H680',BLUE)+label(755,277,['하행 조절'],21,BLUE,anchor='start')+label(755,311,['억제 · 촉진'],21,BLUE,anchor='start')
    body+=box(60,525,380,108,'통각 입력',['조직 상태 · 유해 자극'])+box(520,525,380,108,'침의 감각 입력',['부위 · 조직층 · 자극량'])
    body+=arrow('M250 525 V480 H390 V440')+arrow('M710 525 V480 H570 V440')
    save('pain-modulation.svg','상행 통각 처리와 하행성 조절','통각 입력과 침의 감각 입력이 척수 회로에서 상호작용한다. 상행 입력은 뇌로 전달되고 뇌간의 하행 경로는 척수 전달을 억제하거나 촉진한다.',body,700,'원본 개념도 · 중간 핵·시냅스를 생략한 기능적 관계입니다. 효과 크기를 뜻하지 않습니다.')

    body=box(40,90,400,106,'연구 조건 A',['실제 침 · 특정 자극 설정'])+box(520,90,400,106,'연구 조건 B',['가짜침 · 통상치료 등 비교 조건'],'blue')
    body+=label(480,242,['같은 시점·같은 방법으로 두 조건을 비교'],23)
    body+=box(40,285,400,150,'영상·생리 지표',['BOLD · 연결성 · 감각지도','신경전도 등'])+box(520,285,400,150,'임상 결과',['통증 · 기능 · 감각 증상','치료 종료 후 지속효과'],'blue')
    body+=box(40,510,880,128,'두 결과의 관계를 분석',['함께 변하는가?  어떤 결과를 예측하는가?','상관관계와 인과적 매개를 구분'],'amber')
    body+=arrow('M240 435 V510')+arrow('M720 435 V510',BLUE)
    save('brain-evidence.svg','뇌영상과 임상 결과를 함께 읽기','연구 조건을 비교하고 영상·생리 지표와 환자의 임상 결과를 각각 측정한다. 두 결과의 상관관계만으로 치료의 인과적 매개가 입증되지는 않는다.',body,710,'원본 연구 개념도 · 뇌의 실제 위치나 활성화 지도를 표시한 그림이 아닙니다.')

    body=label(40,97,['일반적인 기능적 연결'],23,TEAL,anchor='start',weight=700)
    body+=box(40,120,880,97,'체성감각 입력',['피부 · 근육 등의 감각신경'])
    body+=box(40,265,880,97,'중추 통합 → 자율신경 출력',['척수 · 뇌간 · 상위 중추 → 장기별 반응'],'blue')+arrow('M480 217 V265')
    body+=label(40,419,['특정 조건에서 검증한 생쥐 실험: Liu 등, 2021'],23,'#ad7220',anchor='start',weight=700)
    body+=box(40,447,400,110,'뒷다리 저강도 전침',['PROKR2 표지 감각뉴런'],'amber')
    body+=box(520,447,400,110,'미주신경–부신 축',['내독소 염증 모델의 반응'],'amber')+arrow('M440 502 H520')
    body+=label(480,610,['부위 · 강도 · 신경 분포에 따른 회로의 차이를 검증'],22)
    body+=box(40,653,880,104,'사람의 임상 연구',['HRV · 혈압 등 생리 지표 + 증상 · 장기 기능을 평가'],'blue')
    save('autonomic.svg','체성–자율신경 반사: 회로와 임상 연구','일반 체성감각 입력의 중추 통합과 자율신경 출력을 보여준다. 생쥐의 특정 미주신경–부신 실험과 사람의 HRV·임상 평가를 별도로 구분한다.',body,830,'원본 개념도 · 생쥐 회로의 인과 검증과 사람의 질환별 치료 효과는 구분합니다.')
    print(f'Built 5 original SVG concept diagrams in {OUT}')


if __name__ == '__main__':
    main()
