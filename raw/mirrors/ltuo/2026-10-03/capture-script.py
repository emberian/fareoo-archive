"""One-shot, bounded mirror capture; canonical HTML is never rewritten."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.request import urlopen
from urllib.parse import urljoin, urlsplit, unquote
from datetime import datetime, timezone
import hashlib,json,re,shutil,subprocess
BASE='https://fare.tunes.org/files/cs/poof/'
WORK=Path('/Users/ember/workbox/fareoo-primary-scholar-20261003')
ROOT=Path('/Users/ember/dev/fareoo')
DEST=ROOT/'raw/mirrors/ltuo/2026-10-03'
DEST.mkdir(parents=True,exist_ok=False)
sha=lambda b:hashlib.sha256(b).hexdigest()
now=lambda:datetime.now(timezone.utc).isoformat()
raw=(WORK/'ltuo.html').read_bytes()
(DEST/'ltuo.html').write_bytes(raw)
shutil.copy2(WORK/'ltuo.headers',DEST/'ltuo.http-headers.txt')
class Links(HTMLParser):
 def __init__(self):super().__init__();self.assets=[];self.links=[];self.anchors=set()
 def handle_starttag(self,t,items):
  a=dict(items)
  for k in ['name','id']:
   if k in a:self.anchors.add(a[k])
  if t=='a' and 'href' in a:self.links.append(a['href'])
  if t in ['script','img','source','iframe']:self.assets.append(a.get('src',''))
  if t=='link':self.assets.append(a.get('href',''))
p=Links();p.feed(raw.decode())
assert len(p.assets)<=16
manifest={'canonical_url':BASE+'ltuo.html','fetched_utc':now(),'http_headers':'ltuo.http-headers.txt','canonical_html_bytes':len(raw),'canonical_html_sha256':sha(raw),'old_snapshot':{'path':'raw/html/poof-ltuo.html','sha256':sha((ROOT/'raw/html/poof-ltuo.html').read_bytes()),'identical':raw==(ROOT/'raw/html/poof-ltuo.html').read_bytes()},'assets':[],'scope':'Canonical single-file book and its directly referenced display assets only. No article/link crawl. Canonical HTML bytes unchanged.'}
for rel in dict.fromkeys(p.assets):
 assert rel and not urlsplit(rel).scheme and '..' not in Path(rel).parts
 url=urljoin(BASE,rel);entry={'local_path':rel,'requested_url':url,'fetched_utc':now()}
 try:
  with urlopen(url,timeout=30) as r:
   b=r.read(16*1024*1024+1);entry.update({'status':r.status,'source_url':r.url})
 except Exception as e:
  entry['canonical_error']=str(e)
  if rel!='scribble-common.js':raise
  url='https://raw.githubusercontent.com/racket/scribble/master/scribble-lib/scribble/scribble-common.js'
  with urlopen(url,timeout=30) as r:b=r.read(1024*1024);entry.update({'status':r.status,'source_url':r.url})
  entry['note']='Offline supplemental upstream Scribble support script; canonical same-directory script returned HTTP 404. Not claimed to be Faré\'s historical script.'
 assert len(b)<=16*1024*1024
 dest=DEST/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(b)
 entry.update({'bytes':len(b),'sha256':sha(b)})
 if rel.endswith('.css'):
  assert not re.search(r'url\s*\(|@import',b.decode()),'CSS requires further bounded asset review'
 manifest['assets'].append(entry)
missing=[];local_refs=0;relative_other=[]
for href in p.links:
 u=urlsplit(href)
 if not u.scheme and not u.netloc and u.path in ['', 'ltuo.html'] and u.fragment:
  local_refs+=1
  if unquote(u.fragment) not in p.anchors:missing.append(href)
 elif not u.scheme and not u.netloc and u.path:relative_other.append(href)
assert not missing,missing
manifest['verification']={'book_local_anchor_references':local_refs,'unique_anchor_names':len(p.anchors),'broken_book_local_anchors':missing,'direct_assets_present':len(manifest['assets']),'css_secondary_assets':0,'other_relative_navigation_links_not_crawled':sorted(set(relative_other))}
old_plain=(ROOT/'raw/html/poof-ltuo.txt').read_bytes()
plain=subprocess.check_output(['pandoc','-f','html','-t','plain','--wrap=none',str(DEST/'ltuo.html')])
(DEST/'ltuo-readable.txt').write_bytes(plain)
manifest['readable_extraction']={'path':'ltuo-readable.txt','tool':subprocess.check_output(['pandoc','--version'],text=True).splitlines()[0],'arguments':'-f html -t plain --wrap=none','bytes':len(plain),'sha256':sha(plain),'old_plain_identical':plain==old_plain,'existing_catalog':'sources/ltuo-book.md','existing_catalog_preserved':True}
sections=json.loads((WORK/'sections.json').read_text())
idx=[]
for s in sections:
 idx.append({'title':s['title'],'anchor':s['anchors'][0] if s['anchors'] else None,'canonical_url':BASE+'ltuo.html#'+s['anchors'][0] if s['anchors'] else None})
(DEST/'sections.json').write_text(json.dumps(idx,ensure_ascii=False,indent=2)+'\n')
(DEST/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
shutil.copy2(__file__,DEST/'capture-script.py')
print(json.dumps({'destination':str(DEST),'verification':manifest['verification'],'extraction':manifest['readable_extraction']},indent=2))
