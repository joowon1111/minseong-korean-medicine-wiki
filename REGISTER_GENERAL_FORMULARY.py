from pathlib import Path
import yaml
p=Path('mkdocs.yml')
cfg=yaml.safe_load(p.read_text(encoding='utf-8-sig'))
cats={'비위·소화': [('평위산', 'pingwei-san.md'), ('향사육군자탕', 'xiangsha-liujunzi-tang.md'), ('향사양위탕', 'xiangsha-yangwei-tang.md'), ('불환금정기산', 'buhuanjin-zhengqi-san.md'), ('인삼양위탕', 'renshen-yangwei-tang.md'), ('보화환', 'baohe-wan.md'), ('위령탕', 'weiling-tang.md')], '담음·현훈·불면': [('이진탕', 'erchen-tang.md'), ('반하백출천마탕', 'banxia-baizhu-tianma-tang.md'), ('도담탕', 'daotan-tang.md'), ('가미온담탕', 'jiawei-wendan-tang.md'), ('천왕보심단', 'tianwang-buxin-dan.md'), ('산조인탕', 'suanzaoren-tang.md')], '간울·기체·활혈': [('소요산', 'xiaoyao-san.md'), ('가미소요산', 'jiawei-xiaoyao-san.md'), ('분심기음', 'fenxin-qiyin.md'), ('오약순기산', 'wuyao-shunqi-san.md'), ('혈부축어탕', 'xuefu-zhuyu-tang.md')], '외감·호흡·청열': [('삼소음', 'renshen-suyin.md'), ('형개연교탕', 'jingjie-lianqiao-tang.md'), ('연교패독산', 'lianqiao-baidu-san.md'), ('맥문동탕', 'maidong-tang.md')], '한열·비위조화': [('반하사심탕', 'banxia-xiexin-tang.md'), ('오적산', 'wujisan.md')], '보익·음양': [('자음강화탕', 'ziyin-jianghuo-tang.md'), ('청심연자음', 'qingxin-lianzi-yin.md'), ('육미지황환', 'liu wei dihuang wan.md'), ('팔미지황환', 'bawei-dihuang-wan.md')]}
found=False
for top in cfg['nav']:
    if isinstance(top,dict) and '본초·방제' in top:
        items=top['본초·방제']
        items[:]=[x for x in items if not (isinstance(x,dict) and '일반 방제 임상 지도' in x)]
        idx=next((i for i,x in enumerate(items) if isinstance(x,dict) and '방제 찾기' in x),0)
        nav=['herbal-integrated/general-formulary.md']
        for cat,ls in cats.items():
            nav.append({cat:[{n:'formulas/'+fn} for n,fn in ls]})
        items.insert(idx+1,{'일반 방제 임상 지도':nav})
        found=True
        break
if not found: raise SystemExit('본초·방제 nav를 찾지 못했습니다.')
r=yaml.safe_dump(cfg,allow_unicode=True,sort_keys=False,width=1000)
yaml.safe_load(r)
p.write_text(r,encoding='utf-8')
print('일반 방제 28개 NAV 등록: OK')
