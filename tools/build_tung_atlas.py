"""Render original educational Tung point SVGs from cited location records."""
from pathlib import Path
import html
import json

ROOT = Path(__file__).resolve().parents[1]

def path(d, cls='landmark'):
    return f'<path class="{cls}" d="{d}"/>'

def text(x,y,value,size=16):
    return f'<text x="{x}" y="{y}" font-size="{size}">{html.escape(value)}</text>'

def anatomy(shape):
    if shape=='forearm-ulnar':
        return path('M206 145 Q258 105 309 145 L300 532 L222 532 Z','skin')+path('M268 152 L268 509','bone')+path('M231 142 Q270 119 293 151 M224 520 L298 520')+text(220,91,'팔꿈치 끝',16)+text(211,563,'손목 주름',15)+text(91,338,'자뼈 가장자리',14)
    if shape=='lowerleg-front':
        return path('M179 146 Q262 121 348 146 L329 307 L311 562 L217 562 L199 308 Z','skin')+path('M258 218 L260 532 M318 225 L298 530','bone')+'<ellipse class="landmark" cx="260" cy="176" rx="29" ry="35"/>'+path('M244 215 L271 215 M226 541 L307 541')+text(315,206,'외슬안',14)+text(80,377,'정강뼈',15)+text(227,596,'발목 방향',15)
    if shape=='lowerleg-lateral':
        return path('M171 149 Q240 111 302 156 Q354 244 321 341 L287 526 Q283 552 261 557 L204 557 L179 333 Z','skin')+path('M255 187 L260 534','bone')+path('M182 174 Q231 198 283 175')+'<circle class="landmark" cx="260" cy="537" r="12"/>'+text(190,91,'무릎 가쪽',16)+text(71,364,'앞 · 정강이',14)+text(333,364,'뒤 · 종아리',14)+text(229,590,'바깥 복사뼈',14)
    if shape=='thigh-medial':
        return path('M173 137 Q257 110 341 137 L318 478 Q311 544 291 561 L217 561 Q194 536 189 478 Z','skin')+path('M198 173 Q237 309 221 476 M320 184 Q285 319 290 482')+path('M227 531 Q254 513 288 533')+text(217,91,'몸통 방향',16)+text(205,597,'무릎 안쪽',16)
    if shape in ('hand','palm'):
        outline='M255 570 L254 488 Q199 453 157 381 L101 302 Q88 280 105 270 Q124 260 144 290 L198 337 Q215 345 216 307 L200 144 Q199 122 217 121 Q236 121 239 145 L255 280 L258 94 Q258 69 277 69 Q297 69 297 95 L304 279 L317 121 Q319 99 338 104 Q355 107 353 132 L350 296 L372 205 Q379 183 397 191 Q414 200 407 224 L385 386 Q383 449 350 489 L352 570 Z'
        lines='M226 303 L285 474 M291 302 L309 474 M336 315 L329 474 M380 337 L348 474 M178 374 L260 483'
        return path(outline,'skin')+path(lines,'bone')+path('M257 500 L350 500')+(path('M221 355 Q272 376 264 468 M253 333 Q307 370 376 351') if shape=='palm' else '')+text(75,228,'엄지 쪽',14)+text(276,597,'손목',14)
    if shape=='finger':
        return path('M178 550 L175 160 Q177 110 234 110 Q293 113 295 160 L297 550 Z','skin')+path('M179 255 Q235 270 293 255 M179 320 Q235 335 294 320 M183 530 Q235 541 291 530')+text(190,92,'검지 손끝',15)+text(70,340,'엄지 쪽',15)+text(185,575,'손바닥 방향',15)+text(355,326,'첫 마디',14)
    if shape=='forearm':
        return path('M175 110 Q265 90 355 110 L320 526 L208 526 Z','skin')+path('M188 135 L343 135 M210 520 L320 520 M238 150 L244 495 M300 150 L287 495','bone')+text(212,87,'팔꿈치',16)+text(230,559,'손목 뒤 주름',15)
    if shape=='upperarm':
        return path('M160 510 L165 235 Q170 126 265 125 Q360 126 365 235 L370 510 Z','skin')+path('M190 193 Q264 148 340 194 M265 170 L265 485','bone')+path('M198 225 Q265 338 335 225 M165 493 Q265 518 368 493')+text(230,101,'어깨 가쪽',16)+text(235,545,'팔꿈치',15)
    if shape=='foot':
        return path('M290 573 Q267 506 230 392 Q206 325 180 217 Q166 161 182 131 Q198 106 219 127 L232 166 Q226 110 247 106 Q269 105 274 161 Q274 115 294 119 Q314 126 314 175 Q319 142 338 150 Q357 159 351 197 Q363 173 379 191 Q395 220 376 266 L388 348 Q394 421 370 503 L370 573 Z','skin')+path('M220 210 L281 430 M257 209 L300 430 M296 220 L319 430 M333 244 L337 430 M372 270 L355 430','bone')+path('M281 520 L378 520 M185 140 Q203 125 220 153 M239 127 Q251 120 263 137')+text(80,98,'엄지발가락',14)+text(290,600,'발목 방향',15)
    if shape=='lowerleg':
        return path('M171 167 Q242 132 313 167 Q351 219 327 318 L286 548 L186 548 L176 341 Q142 252 171 167 Z','skin')+path('M206 190 Q255 170 295 191 L250 520','bone')+path('M180 209 Q225 222 287 205 M194 529 L273 529')+text(206,124,'무릎 안쪽',16)+text(179,582,'안쪽 복사 윗모서리',14)
    if shape=='thigh':
        return path('M147 130 Q249 104 352 130 L341 450 Q336 515 310 567 L190 567 Q157 519 151 450 Z','skin')+path('M250 150 L250 480','bone')+path('M162 245 Q180 391 204 464 M333 239 Q314 385 294 464')+'<ellipse class="landmark" cx="250" cy="520" rx="34" ry="39"/>'+path('M188 551 L312 551')+text(218,90,'몸통 방향',16)+text(207,599,'무릎 앞면',16)
    raise ValueError('Unknown anatomy view: '+shape)

STYLE='''text{font-family:system-ui,"Noto Sans KR",sans-serif;fill:#29424a}.skin{fill:#f9efe5;stroke:#b18a72;stroke-width:2}.bone{fill:none;stroke:#dfcbb5;stroke-width:9;stroke-linecap:round}.landmark{fill:none;stroke:#ba9c83;stroke-width:2}.callout{fill:none;stroke:#879b9c;stroke-width:1.3}.point circle{fill:#087d80;stroke:white;stroke-width:3}.point text{font-weight:700;fill:#08676b}.point:hover circle,.point:focus circle,.point:target circle{fill:#bd4c23;stroke:#7f3218}.point:hover text,.point:target text{fill:#9e3c18}.point:focus{outline:2px solid #087d80}'''

def render(region):
    title='동씨침법 · '+region['title']
    title_size = 17 if len(title)>30 else 21
    out=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 660" role="img" aria-labelledby="title desc"><title id="title">{html.escape(title)}</title><desc id="desc">{html.escape(region["view"]+". "+region["note"])}</desc><style>{STYLE}</style><rect width="720" height="660" rx="18" fill="white"/>',text(24,34,title,title_size),text(24,61,region['view'],14),anatomy(region['shape'])]
    for i,p in enumerate(sorted(region['points'],key=lambda p:p['y'])):
        yy=160+i*65
        href='/tung-acupuncture/'+region['id']+'/#'+p['id']
        out.append(f'<a id="{p["id"]}" class="point" href="{href}" target="_top" aria-label="{html.escape(p["name"])} 위치와 임상 설명"><title>{html.escape(p["name"]+" "+p["han"])}</title>{path(f"M{p["x"]} {p["y"]} L470 {yy}","callout")}<circle cx="{p["x"]}" cy="{p["y"]}" r="8"/>{text(486,yy+5,p["name"]+" "+p["han"],19)}</a>')
    out += [text(24,627,'점·이름을 누르면 해당 혈 설명으로 이동 · 교육용 위치 개요',14),text(24,649,'민성 한의학 아카이브 · 출처별 위치 기준은 본문 참조 · 자침 깊이·방향 표시 아님',12),'</svg>']
    return ''.join(out)

def main():
    data=json.loads((ROOT/'data/tung_acupuncture.json').read_text(encoding='utf-8'))
    output=ROOT/'docs/assets/tung-atlas';output.mkdir(parents=True,exist_ok=True)
    for region in data['regions']:
        (output/(region['id']+'.svg')).write_text(render(region),encoding='utf-8')
    print(f'Rendered {len(data["regions"])} Tung atlas diagrams')

if __name__=='__main__':main()
