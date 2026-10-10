"""Validate JSON and rebuild offline HTML. Python 3; no dependencies."""
from pathlib import Path
import json,re,shutil
root=Path(__file__).resolve().parent
content={p.stem:json.loads(p.read_text(encoding='utf-8')) for p in (root/'content').glob('*.json')}
for name,items in content.items():
 assert items,name
 if name.endswith('quiz'):
  for q in items:assert len(q['options'])==4 and len(set(q['options']))==4 and 0<=q['correctIndex']<4 and q['hint'] and q['explanation']
 elif name.endswith('exercises'):
  for q in items:assert q['question'] and q['answer']
 elif name.endswith('rules'):
  for s in items:
   for b in s['blocks']:
    if b['type']=='table':assert all(len(row)==len(b['headers']) for row in b['rows'])
out=root/'offline'
if out.exists():shutil.rmtree(out)
out.mkdir()
css=(root/'assets/style.css').read_text(encoding='utf-8')
data=json.dumps(content,ensure_ascii=False).replace('<','\\u003c')
for p in root.glob('*.html'):
 if p.name in ['English-Grammar-Quiz.html','Junior-English-Quiz.html']:continue
 html=p.read_text(encoding='utf-8').replace('<link rel="stylesheet" href="assets/style.css">',f'<style>{css}</style>')
 html=html.replace('<script defer src="assets/loader.js"></script>',f'<script>window.QUIZ_CONTENT={data};</script>')
 scripts=re.findall(r'<script defer src="assets/(\w+).js"></script>',html)
 html=re.sub(r'<script defer src="assets/\w+.js"></script>','',html)
 if scripts:html=html.replace('</body>','<script>'+(root/'assets/loader.js').read_text()+'</script>'+''.join('<script>'+(root/'assets'/f'{s}.js').read_text()+'</script>' for s in scripts)+'</body>')
 (out/p.name).write_text(html,encoding='utf-8')
for p in root.glob('*.pdf'):shutil.copy(p,out)
shutil.copy(out/'tenses.html',root/'English-Grammar-Quiz.html');shutil.copy(out/'tenses.html',out/'English-Grammar-Quiz.html')
print('Validated content and built',len(list(out.glob('*.html'))),'offline pages.')
