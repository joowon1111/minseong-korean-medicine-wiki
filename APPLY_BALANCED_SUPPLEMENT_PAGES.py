from pathlib import Path
import shutil
src=Path(__file__).parent/'docs'/'conditions'
dst=Path('docs')/'conditions'
dst.mkdir(parents=True,exist_ok=True)
count=0
for p in src.glob('*.md'):
    shutil.copy2(p,dst/p.name)
    print('UPDATED:',dst/p.name)
    count+=1
print('UPDATED COUNT:',count)
