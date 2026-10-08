"""Validate content and produce standalone offline pages. Python 3, no dependencies."""
from pathlib import Path
import json,re,shutil
root=Path(__file__).resolve().parent
content={name:json.loads((root/'content'/f'{name}.json').read_text(encoding='utf-8')) for name in ['quiz','exercises','rules']}
assert content['quiz'], 'Το κουίζ δεν μπορεί να είναι κενό.'
for q in content['quiz']:
 assert len(q['options'])==4 and type(q['correctIndex']) is int and 0<=q['correctIndex']<4
 assert all(isinstance(q[k],str) and q[k] for k in ['question','hint','explanation'])
for q in content['exercises']:assert q['question'] and q['answer']
for s in content['rules']:
 assert s['title']
 for b in s['blocks']:
  assert b['type'] in ['text','table']
  if b['type']=='table':assert all(len(row)==len(b['headers']) for row in b['rows'])
out=root/'offline';out.mkdir(exist_ok=True)
css=(root/'assets/style.css').read_text(encoding='utf-8')
data=json.dumps(content,ensure_ascii=False).replace('<','\\u003c')
for name in ['index','exercises','rules']:
 html=(root/f'{name}.html').read_text(encoding='utf-8')
 html=html.replace('<link rel="stylesheet" href="assets/style.css">',f'<style>{css}</style>')
 html=html.replace('<script defer src="assets/loader.js"></script>',f'<script>window.QUIZ_CONTENT={data};</script>')
 scripts=['loader','quiz' if name=='index' else 'content']
 html=re.sub(r'<script defer src="assets/(?:quiz|content).js"></script>','',html)
 html=html.replace('</body>', ''.join('<script>'+(root/'assets'/f'{s}.js').read_text(encoding='utf-8')+'</script>' for s in scripts)+'</body>')
 (out/f'{name}.html').write_text(html,encoding='utf-8')
shutil.copy(root/'English-Grammar-60-Exercises.pdf',out)
shutil.copy(out/'index.html',out/'English-Grammar-Quiz.html')
# A standalone quiz download keeps external navigation pointed at the hosted pages.
shutil.copy(out/'index.html',root/'English-Grammar-Quiz.html')
print(f'Έτοιμη offline έκδοση: {out}')
