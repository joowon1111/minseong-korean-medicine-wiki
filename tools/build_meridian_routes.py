"""Render editable route overview SVGs from the reviewed meridian manifest."""
from pathlib import Path
import html
import json

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'docs/assets/meridian-routes'
STYLE = '''text{font-family:system-ui,"Noto Sans KR",sans-serif;fill:#29424a}.skin{fill:#f9efe5;stroke:#b18a72;stroke-width:1.8}.landmark{fill:none;stroke:#c7ad95;stroke-width:2}.guide{fill:none;stroke:#95a7aa;stroke-width:1.3;stroke-dasharray:5 5}.route{fill:none;stroke:#087d80;stroke-width:4;stroke-linecap:round;stroke-linejoin:round;marker-end:url(#arrow)}.point circle{fill:#087d80;stroke:white;stroke-width:2}.point.end circle{fill:#ba552f}.point text{font-size:15px;font-weight:700;fill:#08676b}.point.end text{fill:#a04422}.point:hover circle,.point:focus circle,.point:target circle{fill:#bf4129;stroke:#783627;stroke-width:3}.point:focus{outline:2px solid #087d80}.callout{fill:none;stroke:#799097;stroke-width:1}.small{font-size:13px;fill:#546b73}'''

def text(x, y, content, size=16, cls=''):
    return f'<text x="{x}" y="{y}" font-size="{size}" class="{cls}">{html.escape(content)}</text>'

def path(d, cls='landmark'):
    return f'<path class="{cls}" d="{d}"/>'

def body(view):
    if view == 'side':
        return (path('M246 105 Q274 70 307 99 Q331 139 307 182 L299 210 L320 235 Q338 293 311 362 L313 410 Q333 440 319 477 L311 557 L305 674 L310 713 Q286 731 236 721 L235 708 L272 681 L267 565 L244 463 L244 402 L234 338 L227 262 L249 211 L251 187 L232 171 L233 154 L217 150 L234 133 Z','skin')
            + path('M243 128 L253 130 M267 246 Q248 303 259 352 L270 457 M258 709 L306 709')
            + '<ellipse class="landmark" cx="295" cy="141" rx="10" ry="17"/>'
            + text(45,116,'옆면',16))
    head='<ellipse class="skin" cx="270" cy="135" rx="44" ry="57"/>'
    trunk=path('M249 185 L248 210 L185 230 L209 282 L211 348 L193 427 L186 466 Q224 488 270 475 Q315 488 354 466 L347 427 L329 348 L331 282 L355 230 L292 210 L291 185 Z','skin')
    arm=path('M188 234 Q166 275 151 344 L121 466 L113 487 L94 499 L80 529 L74 545 Q74 551 82 548 L96 525 L91 551 Q92 559 99 553 L104 531 L103 557 Q103 567 107 562 L113 550 L114 529 L116 545 Q121 551 122 541 L124 519 L125 502 L140 517 Q154 520 148 507 L132 487 L145 474 L177 360 L211 258 Z','skin')
    leg=path('M187 460 Q214 480 254 475 L249 543 L246 610 L241 674 L254 707 L248 722 L181 723 L180 709 L195 676 L190 607 L181 546 Z','skin')
    b=head+trunk+arm+f'<g transform="translate(540 0) scale(-1 1)">{arm}</g>'+leg+f'<g transform="translate(540 0) scale(-1 1)">{leg}</g>'
    if view=='front':
        b+=path('M240 224 Q255 230 270 227 Q285 230 300 224 M252 135 L262 135 M278 135 L288 135 M267 140 L264 149 L275 149 M256 162 Q270 169 284 162')
        b+='<circle class="landmark" cx="270" cy="382" r="5"/>'
    else:
        b+=path('M270 218 L270 449','guide')+path('M239 244 L211 271 L245 320 Z M301 244 L329 271 L295 320 Z M200 489 Q219 500 248 489 M292 489 Q321 500 340 489')
    b+=path('M198 540 L239 540 M301 540 L342 540 M197 682 L238 682 M302 682 L343 682')
    return b+text(45,116,'앞면' if view=='front' else '뒷면',16)

def render(route):
    code=route['code']; inset=code in ('BL','GV')
    bits=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 800" role="img" aria-labelledby="title desc"><title id="title">{html.escape(route["title"])} · 시작혈부터 마지막혈까지</title><desc id="desc">{html.escape(route["summary"]+". "+route["note"])}</desc><style>{STYLE}</style><defs><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 Z" fill="#087d80"/></marker></defs><rect width="960" height="800" rx="18" fill="white"/>',text(30,39,route['title']+' '+code,25),text(30,69,'시작혈 → 지나가는 부위 → 마지막혈',16),body(route['view'])]
    bits.extend(path(d,'route') for d in route['tracks'])
    if inset:
        bits+=['<rect x="540" y="87" width="386" height="152" rx="12" fill="#f5f8f8"/>','<ellipse class="skin" cx="720" cy="147" rx="39" ry="47"/>',path('M696 135 L711 135 M724 135 L739 135 M718 142 L715 151 L724 151 M706 166 Q720 172 734 166')]
        if code=='BL':
            bits+=[text(553,108,'얼굴 쪽 시작혈',14),path('M712 135 L660 122 L477 88 L302 84','guide')]
        else:
            bits+=[text(553,108,'윗입술 안쪽 종점',14),path('M711 179 L729 179 L729 197 L711 197 Z'),path('M720 174 L720 185'),path('M275 78 L491 90 L660 185 L720 185','guide')]
    points=route['points'];left=sorted([p for p in points if p['x']<520],key=lambda p:p['y'])
    previous=65
    for point in left:
        yy=max(previous+30,point['y']);previous=yy
        end=point['code']==route['last']; cx=point['x'];cy=point['y'];px=38 if cx<=270 else 422
        endx=100 if px==38 else 412
        name=point['name']+' '+point['code']
        bits.append(f'<a id="{point["code"]}" class="point'+(' end' if end else '')+f'" href="/{point["path"][:-3]}/" target="_top" aria-label="{html.escape(name)} 상세 도해"><title>{html.escape(name)}</title>{path(f"M{cx} {cy} L{endx} {yy-5}","callout")}<circle cx="{cx}" cy="{cy}" r="6"/>{text(px,yy,point["code"])}</a>')
    if inset:
        p=next(p for p in points if p['x']>=520)
        bits.append(f'<a id="{p["code"]}" class="point'+(' end' if code=='GV' else '')+f'" href="/{p["path"][:-3]}/" target="_top" aria-label="{html.escape(p["name"])} 상세 도해"><circle cx="{p["x"]}" cy="{p["y"]}" r="6"/>{text(783,p["y"]+5,p["name"]+" "+p["code"],15)}</a>')
    top=272 if inset else 147
    first,last=points[0],points[-1]
    for i,(p,label,color) in enumerate([(first,'체표 첫 혈','#087d80'),(last,'체표 마지막 혈','#ba552f')]):
        yy=top+i*70
        bits+=[f'<rect x="540" y="{yy-24}" width="386" height="62" rx="10" fill="#f5f8f8"/>',text(553,yy-3,label,13),f'<a href="/{p["path"][:-3]}/" target="_top">'+text(553,yy+22,p['name']+' '+p['code'],20)+'</a>']
    yy=top+156
    for i,station in enumerate(route['stations']):
        bits += [f'<circle cx="552" cy="{yy-5}" r="4" fill="#087d80"/>',text(568,yy,station,15)]
        if i<3:bits.append(path(f'M552 {yy+7} L552 {yy+30}','guide'))
        yy+=51
    bits += [text(540,yy+7,'경혈 코드·이름을 누르면 상세 위치로 이동합니다.',13,'small'),text(30,762,'한쪽 경맥의 체표 흐름을 펼친 교육용 개요 · 내부 장부·깊이·자침 방향은 표시하지 않음',14,'small'),text(30,786,'민성 한의학 아카이브 · 정확한 위치는 연결된 361경혈 도해와 본문에서 확인',12,'small'),'</svg>']
    return ''.join(bits)

def main():
    ASSETS.mkdir(parents=True,exist_ok=True)
    data=json.loads((ROOT/'data/meridian_routes.json').read_text(encoding='utf-8'))
    for route in data['routes']:
        (ASSETS/(route['code'].lower()+'.svg')).write_text(render(route),encoding='utf-8')
    print(f'Rendered {len(data["routes"])} meridian route diagrams')

if __name__=='__main__':
    main()
