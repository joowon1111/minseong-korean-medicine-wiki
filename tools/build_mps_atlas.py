"""Render original, linked educational muscle anatomy and MPS concept SVGs.

Shapes summarize relationships, not insertion paths or fixed trigger-point maps.
Sources and clinical scope live in data/mps_atlas.json and the linked pages.
"""
from pathlib import Path
import html
import json

ROOT = Path(__file__).resolve().parents[1]
STYLE = '''text{font-family:system-ui,"Noto Sans KR",sans-serif;fill:#243f4b}.bone{fill:#eee5d6;stroke:#b09c7c;stroke-width:2}.skin{fill:#faf3eb;stroke:#cab6a4;stroke-width:2}.line{fill:none;stroke:#b09c7c;stroke-width:2}.muscle{fill:#60b6b0;stroke:#176f70;stroke-width:2}.fiber{fill:none;stroke:#d6f0e9;stroke-width:1.5;pointer-events:none}.nerve{fill:none;stroke:#d6a137;stroke-width:5;stroke-linecap:round}.link:hover .muscle,.link:focus .muscle,.link:target .muscle{fill:#e2a17b;stroke:#a54b28}.link:hover .button,.link:focus .button,.link:target .button{fill:#d7edea}.link:focus{outline:2px solid #176f70}.button{fill:#edf7f4;stroke:#6ba8a3;stroke-width:1.5}.small{fill:#536974}'''
def p(d,c='bone'):return f'<path class="{c}" d="{d}"/>'
def t(x,y,s,size=15,anchor='start'):return f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}">{html.escape(s)}</text>'
def rect(x,y,w,h,fill,rx=12):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"/>'
def ellipse(x,y,rx,ry,c='bone'):return f'<ellipse class="{c}" cx="{x}" cy="{y}" rx="{rx}" ry="{ry}"/>'
def header(title,desc):return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 680" role="img" aria-labelledby="title desc"><title id="title">{html.escape(title)}</title><desc id="desc">{html.escape(desc)}</desc><style>{STYLE}</style>'+rect(0,0,960,680,'#fff',20)+t(28,43,title,27)+t(28,74,desc,15)
def scapula():
 return p('M65 95 L179 77 Q206 103 188 129 L109 266 Q77 218 65 95 Z')+p('M69 117 L175 99 L202 90','line')+p('M198 120 Q223 107 227 134 L226 288 L211 291 L202 151 Z')+t(12,312,'肩甲骨 · 견갑골',13)
def neck_base():
 return ellipse(120,52,51,52,'skin')+p('M89 94 L85 171 Q60 186 13 198 L10 308 L230 308 L227 198 Q175 187 156 171 L152 94 Z','skin')+p('M120 110 L120 284','bone')+p('M44 218 L98 210 L72 287 Z')+p('M142 211 L198 218 L171 287 Z')+t(113,338,'뒤쪽',14,'middle')
def lumbar_base():
 return p('M36 65 Q121 88 204 65 L211 269 Q177 290 157 310 L83 310 Q65 290 30 267 Z','skin')+p('M108 83 L131 83 L140 270 L100 270 Z')+p('M24 257 Q57 229 99 253 L107 308 L84 323 L33 293 Z')+p('M143 253 Q183 229 216 257 L207 293 L155 323 L133 308 Z')+p('M25 72 L106 98 M134 98 L216 72','bone')+t(4,52,'제12갈비뼈',13)+t(156,344,'장골능',13)
def hip_base():
 return p('M38 67 Q106 9 195 50 L201 119 L165 169 L135 234 L81 222 L51 160 Z')+p('M166 157 Q204 152 210 184 L200 330 L176 330 L170 211 L141 191 Z')+t(9,23,'장골',13)+t(164,355,'대퇴골',13)
def thigh_base():
 return p('M51 47 Q120 29 190 47 L180 244 Q175 294 161 326 L84 326 Q67 296 61 244 Z','skin')+p('M113 65 L132 65 L136 269 L110 269 Z')+ellipse(123,291,22,26)+p('M122 314 L123 345','bone')+t(165,297,'슬개골',12)+t(20,20,'고관절 쪽',13)
def calf_base():
 return p('M62 25 Q120 5 179 25 Q210 98 178 192 L148 322 L92 322 L62 191 Q35 97 62 25 Z','skin')+p('M71 28 Q120 47 171 28','bone')+p('M104 318 L102 344 L141 347 L142 318 Z')+t(93,374,'발꿈치뼈',13)
def forearm_base(front=False):
 return p('M64 30 Q120 6 176 30 L160 258 L151 284 L170 325 Q172 347 155 347 L115 316 L77 326 Q63 323 71 300 L83 272 L65 178 Z','skin')+p('M88 46 L102 258 M157 45 L136 258','bone')+p('M82 269 L157 269','line')+t(93,7,'팔꿈치',13)+t(172,274,'손목',12)
def jaw_base():
 return p('M40 164 Q17 125 30 72 Q46 18 113 20 Q183 15 198 78 L195 114 L218 137 L197 146 L200 175 L212 180 L199 191 Q198 224 164 230 L151 288 L63 285 L73 230 Q45 218 40 164 Z','skin')+p('M84 161 L104 206 L185 204 L170 226 L91 234 L64 174 Z')+p('M79 145 L164 143','bone')+ellipse(75,151,11,15)+p('M182 115 L193 116','line')+t(108,319,'턱뼈',13)+t(160,10,'얼굴 앞 →',13)

def anatomy(id):
 """Return background, linked muscle shape, fibers, and panel view label."""
 if id=='masseter':
  return jaw_base(),p('M88 147 L151 146 L160 210 L108 219 Z','muscle'),p('M100 155 L119 207 M119 155 L133 207 M139 155 L147 204','fiber'),'옆쪽 · 턱 가쪽'
 if id=='temporalis':
  return jaw_base(),p('M46 114 Q23 58 77 35 Q143 15 178 76 L161 122 L140 179 L126 183 L119 130 Z','muscle'),p('M56 67 L132 165 M94 47 L134 161 M152 67 L138 158','fiber'),'옆쪽 · 관자 부위'
 if id=='upper-trapezius':
  return neck_base(),p('M116 87 L115 176 Q78 193 30 201 L48 218 Q103 205 120 163 Q138 205 195 218 L213 201 Q169 194 127 176 L125 87 Z','muscle'),p('M118 112 Q105 175 45 207 M123 112 Q139 180 198 207','fiber'),'뒤쪽 · 표층'
 if id=='levator-scapulae':
  return neck_base()+t(161,110,'C1–C4',12),p('M138 104 L153 110 L178 212 L158 214 L136 135 Z','muscle'),p('M144 116 L167 206','fiber'),'뒤쪽 · 승모근 생략'
 if id=='suboccipitals':
  bg=ellipse(120,51,86,53,'skin')+p('M51 155 L189 155 M57 212 L182 212 M120 184 L120 272','bone')+t(196,158,'C1',13)+t(190,217,'C2',13)+t(75,23,'뒤통수뼈',13)
  shape=p('M115 151 L97 100 L112 104 Z M125 151 L128 104 L143 100 Z M113 208 L61 88 L88 102 Z M126 208 L153 102 L180 88 Z M57 151 L42 78 L62 85 Z M183 151 L178 86 L196 79 Z M117 210 L54 158 L72 151 Z M124 210 L167 151 L186 158 Z','muscle')
  return bg,shape,'','뒤쪽 · 심층 확대'
 if id in ('supraspinatus','infraspinatus','rhomboids'):
  bg=scapula()
  if id=='supraspinatus':return bg,p('M70 103 Q118 74 175 83 L217 112 L204 124 L170 103 L73 117 Z','muscle'),p('M80 104 L205 114 M83 110 L204 118','fiber'),'뒤쪽 · 가시 위'
  if id=='infraspinatus':return bg,p('M74 131 L170 110 L208 130 L205 145 L179 148 L111 249 Z','muscle'),p('M83 143 L202 137 M96 178 L196 140 M113 220 L189 143','fiber'),'뒤쪽 · 가시 아래'
  return bg+p('M23 68 L23 267','bone'),p('M27 99 L65 106 L70 134 L26 125 Z M27 137 L72 144 L96 229 L27 188 Z','muscle'),p('M34 109 L64 118 M32 152 L76 170 M33 170 L84 194','fiber'),'뒤쪽 · 승모근 생략'
 if id=='pectoralis-minor':
  bg=p('M49 56 L50 289','bone')+''.join(p(f'M54 {y} Q132 {y-25} 205 {y+12}','bone') for y in (120,155,190,225))+p('M71 55 Q128 39 194 69','bone')+p('M192 78 L179 102 L192 112 L204 89 Z')+t(6,164,'3–5',12)+t(4,186,'갈비뼈',12)+t(138,29,'부리돌기',12)
  return bg,p('M86 156 L189 97 L166 151 L116 234 L84 220 L100 192 L83 187 L103 166 Z','muscle'),p('M94 160 L179 111 M106 193 L179 117 M107 224 L178 124','fiber'),'앞쪽 · 대흉근 생략'
 if id=='ecrb':return forearm_base(),p('M88 44 Q137 79 127 159 L119 226 L122 272 L135 308 L126 312 L111 273 L108 226 Q78 142 84 74 Z','muscle'),p('M92 64 Q116 136 113 218','fiber'),'뒤쪽 · 손등 방향'
 if id=='pronator-teres':return forearm_base(True),p('M161 49 L155 79 L96 174 L84 165 L128 74 L139 53 Z','muscle'),p('M148 67 L94 158','fiber'),'앞쪽 · 손바닥 방향'
 if id=='quadratus-lumborum':return lumbar_base(),p('M149 101 L188 86 L185 241 L155 250 L142 228 L151 209 L141 187 L150 168 L140 142 Z','muscle'),p('M159 112 L164 233 M178 106 L176 231','fiber'),'뒤쪽 투영 · 후복벽'
 if id=='multifidus':return lumbar_base(),p('M114 106 L90 166 L110 151 L84 210 L106 194 L75 257 L94 270 L118 222 L104 238 L122 184 L110 198 L124 146 Z M128 106 L143 165 L134 151 L156 211 L138 192 L171 257 L152 270 L128 222 L141 238 L126 184 L138 198 L123 146 Z','muscle'),p('M87 254 L119 192 M155 252 L130 192','fiber'),'뒤쪽 · 척추 가까운 심층'
 if id=='gluteus-medius':return hip_base(),p('M44 75 Q107 19 192 56 L193 92 Q191 129 184 179 L168 180 Q128 127 44 75 Z','muscle'),p('M57 75 L175 168 M106 52 L179 166 M168 53 L183 168','fiber'),'가쪽 · 대둔근 생략'
 if id=='gluteus-minimus':return hip_base(),p('M77 103 Q126 62 193 92 L194 132 L183 182 L167 180 Q123 139 77 103 Z','muscle'),p('M91 103 L176 170 M133 89 L179 167 M176 99 L183 166','fiber'),'가쪽 · 중둔근 생략'
 if id=='piriformis':
  bg=p('M20 69 L60 77 L78 179 L50 218 L19 153 Z')+p('M74 49 Q157 26 209 73 L198 149 L151 187 L104 170 L76 116 Z')+p('M181 174 Q215 164 218 204 L209 325 L184 325 L180 221 L146 199 Z')+p('M93 160 Q118 209 111 314','nerve')+t(22,35,'천골',13)+t(9,344,'노랑: 좌골신경 개요',12)
  return bg,p('M43 105 L47 140 L186 195 L198 180 L118 135 Z','muscle'),p('M51 119 L186 184','fiber'),'뒤쪽 · 대둔근 생략'
 if id=='rectus-femoris':return thigh_base(),p('M121 51 Q97 112 99 175 Q100 230 116 266 L132 266 Q148 222 147 174 Q145 103 127 51 Z','muscle'),p('M121 83 L121 251 M130 89 L130 245','fiber'),'앞쪽 · 고관절도 지남'
 if id=='vastus-medialis':return thigh_base(),p('M144 109 Q173 151 172 223 Q172 257 148 278 L139 263 Q157 229 140 179 Z','muscle'),p('M155 178 L160 218 L148 262 M158 238 L146 262','fiber'),'앞쪽 · 안쪽 부분'
 if id=='gastrocnemius':return calf_base(),p('M77 29 Q49 74 67 147 Q83 186 108 200 L111 273 L104 324 L132 324 L130 270 L134 199 Q172 179 177 134 Q185 69 162 30 L130 43 L122 147 L115 45 Z','muscle'),p('M86 46 Q68 108 111 178 M150 49 Q172 110 133 177 M120 216 L117 313','fiber'),'뒤쪽 · 표층 두 갈래'
 if id=='soleus':return calf_base(),p('M74 69 Q47 137 78 209 L108 272 L106 324 L133 324 L132 270 L164 208 Q190 134 164 71 L140 83 L102 84 Z','muscle'),p('M84 98 L111 241 M155 97 L130 242 M120 266 L119 315','fiber'),'뒤쪽 · 비복근 생략'
 raise ValueError(id)

def render_region(region):
 out=[header(region['title']+' · 근육 해부 도해','근육이나 이름을 눌러 기능·신경지배·MPS 평가로 이동합니다.')]
 n=len(region['muscles']);w=904/n
 for i,m in enumerate(region['muscles']):
  x=28+i*w
  out.append(rect(x+4,99,w-8,479,'#f7f9f8'))
  bg,shape,fibers,label=anatomy(m['id']);scale=min(0.95,(w-20)/240);tx=x+(w-240*scale)/2
  out.append(t(x+w/2,128,label,13,'middle'))
  out.append(f'<g transform="translate({tx:.2f} 155) scale({scale:.3f})">{bg}</g>')
  out.append(f'<a id="{m["id"]}" class="link" href="/clinical-anatomy/mps-{region["id"]}/#{m["id"]}" target="_top" aria-label="{m["name"]} 해부와 평가"><title>{html.escape(m["name"]+" · "+m["en"])}</title><g transform="translate({tx:.2f} 155) scale({scale:.3f})">{shape}{fibers}</g><rect class="button" x="{x+12:.2f}" y="532" width="{w-24:.2f}" height="34" rx="8"/>{t(x+w/2,555,m["name"]+' →',17,"middle")}</a>')
 out += [t(28,613,'초록: 해당 근육·근육군  |  베이지: 뼈·체표 윤곽  |  근육층은 패널별로 분리',15),t(28,642,'관계를 단순화한 자체 제작 도해 · 고정 유발점·자침 깊이·경로를 나타내지 않습니다.',14),t(28,666,'민성 한의학 아카이브 · 해부 출처와 평가 기준은 연결된 본문 참조',12),'</svg>']
 return ''.join(out)

def layers():
 out=[header('근육·근막 · 조직층을 나누어 보기','왼쪽은 피부에서 근육까지의 개념 단면, 오른쪽은 근육 내부 결합조직의 확대 개요입니다.')]
 out.append(rect(28,110,440,450,'#f7f9f8'));out.append(rect(490,110,442,450,'#f7f9f8'))
 for y,h,color,label in [(166,28,'#d6ad92','피부'),(194,74,'#f2dfac','피하조직 · 얕은근막'),(268,16,'#c0d8da','깊은근막'),(293,21,'#86babc','근외막'),(314,168,'#d3e8de','골격근')]:
  out.append(rect(49,y,195,h,color,2));out.append(t(263,y+h/2+6,label,16))
 for y in range(330,475,22):out.append(p(f'M61 {y} L231 {y}','fiber'))
 out.append(t(49,142,'층별 구조',20));out.append(t(49,524,'부위마다 두께·연결 방식이 다릅니다.',15))
 out.append(ellipse(689,302,142,142,'muscle'))
 for x,y in [(634,261),(731,256),(673,358)]:
  out.append(f'<circle cx="{x}" cy="{y}" r="45" fill="#f9eedb" stroke="#628f97" stroke-width="5"/>')
  for dx,dy in [(-14,-13),(14,-13),(0,15)]:out.append(f'<circle cx="{x+dx}" cy="{y+dy}" r="12" fill="#bc8273" stroke="#fff" stroke-width="3"/>')
 out.append(t(518,142,'근육 내부 · 확대',20))
 out.append(t(518,484,'근외막: 근육 전체를 감쌈',16));out.append(t(518,513,'근주막: 근섬유 다발을 감쌈',16));out.append(t(518,542,'근내막: 개별 근섬유를 감쌈',16))
 out += [t(28,601,'근막·근육·힘줄은 이어져 있지만, 통증의 원인 조직은 진찰에서 구분합니다.',17),t(28,632,'신경·혈관은 여러 층 사이를 지나갑니다. 이 그림에서는 생략했습니다.',15),t(28,661,'자체 제작 개념도 · 실제 조직 두께·주행을 나타내지 않음 · 본문에 해부 출처 수록',13),'</svg>']
 return ''.join(out)

def trigger_concept():
 out=[header('MPS · 긴장대와 통증을 읽는 방법','촉진 부위와 환자가 실제로 느낀 통증 부위를 구분하여 기록합니다.')]
 out.append(rect(28,105,904,233,'#f7f9f8'))
 out.append(ellipse(280,218,192,77,'muscle'))
 for y in range(174,269,16):out.append(p(f'M121 {y} Q280 {y+10} 440 {y}','fiber'))
 out.append(p('M107 215 Q279 233 458 215','nerve'))
 out.append('<circle cx="294" cy="223" r="17" fill="#c75f35" stroke="white" stroke-width="3"/>')
 out.append(t(526,158,'긴장대 · taut band',20));out.append(t(526,189,'띠처럼 만져지는 근육 부위',16));out.append(t(526,231,'과민점 · hypersensitive spot',20));out.append(t(526,262,'긴장대 안에서 특히 민감한 곳',16));out.append(t(526,305,'평소의 익숙한 증상인지 확인',18))
 for i,(label,desc,kind) in enumerate([('국소 통증','누른 곳 가까이 아픔','local'),('퍼지는 통증','같은 근육 안으로 퍼짐','spread'),('연관통','근육 밖의 다른 곳에서 느낌','referred')]):
  x=28+i*306;out.append(rect(x,358,292,221,'#faf7f1'));out.append(t(x+18,389,label,19));out.append(ellipse(x+115,465,81,38,'muscle'))
  if kind=='spread':out.append('<ellipse cx="'+str(x+124)+'" cy="465" rx="53" ry="19" fill="#e8ad82" opacity=".9"/>')
  else:out.append('<circle cx="'+str(x+98)+'" cy="465" r="11" fill="#c75f35"/>')
  if kind=='referred':out.append('<ellipse cx="'+str(x+247)+'" cy="456" rx="24" ry="31" fill="#e8ad82"/>')
  out.append(t(x+18,551,desc,15))
 out += [t(28,612,'위치·범위는 개인마다 달라집니다. 이 도해는 고정된 통증 지도가 아닙니다.',16),t(28,642,'통증 양상 + 움직임·기능 + 신경학적 소견을 함께 해석합니다.',16),t(28,666,'자체 제작 개념도 · 국제 TrP Delphi 합의 및 DC/TMD의 용어 구분을 참고',12),'</svg>']
 return ''.join(out)

def main():
 data=json.loads((ROOT/'data/mps_atlas.json').read_text())
 folder=ROOT/'docs/assets/mps-atlas';folder.mkdir(parents=True,exist_ok=True)
 for r in data['regions']:(folder/(r['id']+'.svg')).write_text(render_region(r))
 (folder/'tissue-layers.svg').write_text(layers())
 (folder/'trigger-pain.svg').write_text(trigger_concept())
 print(f'Rendered {len(data["regions"])+2} original MPS atlas diagrams')
if __name__=='__main__':main()
