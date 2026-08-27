from pathlib import Path
import shutil,sys,yaml
p=Path("mkdocs.yml")
if not p.exists(): print("ERROR: mkdocs.yml 없음");sys.exit(1)
t=p.read_text(encoding="utf-8-sig")
shutil.copy2(p,"_backup_mkdocs_184.yml")
line="  - javascripts/korean-search-fallback.js"
if "javascripts/korean-search-fallback.js" not in t:
    if "extra_javascript:" in t:
        t=t.replace("extra_javascript:","extra_javascript:\n"+line,1)
    else:
        anchor="extra_css:\n"
        i=t.find(anchor)
        if i>=0:
            # insert before extra_css
            t=t[:i]+"extra_javascript:\n"+line+"\n"+t[i:]
        else:
            t="extra_javascript:\n"+line+"\n"+t
p.write_text(t,encoding="utf-8")
print("mkdocs.yml: Korean fallback JS 연결 완료")
