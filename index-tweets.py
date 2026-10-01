#!/usr/bin/env python3
"""Index the OO-relevant tweets of @Ngnghm from raw/ngnghm.jsonl into sources/tweets-oo.md.

Threads by in_reply_to / quoted where both ends are his (the file holds only his tweets, so a
referenced id present in the file is his). Relevance is a keyword match on the lower-cased text
(the lists below); every kept tweet is quoted verbatim with its id, URL and date. The index
prints counts so the final report can say how many tweets had arrived and how many were kept.
Re-runnable; overwrites sources/tweets-oo.md. Never calls scry."""
import json, os, re, sys, collections, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, 'raw', 'ngnghm.jsonl')
OUT = os.path.join(HERE, 'sources', 'tweets-oo.md')

OO = [r'\boo\b', r'\boop\b', r'object[- ]orient', r'\bobjects?\b', r'prototyp', r'inherit', r'mixin',
      r'\bclass(es)?\b', r'\bclos\b', r'smalltalk', r'\bself\b.*\bsuper\b', r'\bsuper\b', r'conflat',
      r'specification', r'\btarget\b', r'modular', r'extensib', r'incremental', r'fix(ed)?[- ]?point',
      r'\by combinator', r'\bc3\b', r'\bc4\b', r'lineari[sz]', r'multiple dispatch', r'generic function',
      r'method combination', r'late binding', r'open recursion', r'lambda,? the ultimate', r'\bltuo\b',
      r'\bpoof\b', r'jsonnet', r'\bnix\b', r'typeclass', r'\btrait', r'flavors?\b', r'metaobject',
      r'\bmop\b', r'subtyp', r'subclass', r'encapsulation', r'message passing', r'alan kay', r'simula',
      r'bracha', r'cook\b', r'delegation', r'\bself language', r'\bexpression problem']
HOU = [r'houyhnhnm', r'hunam', r'ngnghm', r'orthogonal persist', r'persisten', r'live upgrade',
       r'schema', r'migrat', r'first-class implementation', r'semantic tower', r'reflect', r'meta-?level',
       r'metaprogram', r'kernel\b', r'platform', r'application', r'division of labou?r', r'point of view',
       r'turtle', r'full abstraction', r'pclsr', r'transaction', r'atomic section', r'capabilit',
       r'\bdomain', r'urbit', r'nock', r'erlang', r'build system', r'\basdf\b', r'gerbil', r'scheme\b',
       r'\blisp\b', r'racket', r'\bdsl', r'macro']
oo_re = re.compile('|'.join(OO)); hou_re = re.compile('|'.join(HOU))

def load():
    rows = []
    if not os.path.exists(RAW): return {}
    for line in open(RAW):
        line = line.strip()
        if not line: continue
        try: rows.append(json.loads(line))
        except json.JSONDecodeError: pass
    # dedupe by id, keep last
    byid = {}
    for r in rows: byid[r['tweet_id']] = r
    return byid

def main():
    byid = load()
    ids = set(byid)
    def his(x): return x and x not in ('', 'None', 'null', '0') and x in ids
    # thread roots: follow in_reply_to while it is his
    def root(tid):
        seen = set(); cur = tid
        while True:
            seen.add(cur); p = byid[cur].get('in_reply_to')
            if his(p) and p not in seen: cur = p
            else: return cur
    rel = {}
    for tid, r in byid.items():
        t = (r.get('text') or '').lower()
        tags = []
        if oo_re.search(t): tags.append('OO')
        if hou_re.search(t): tags.append('HOU')
        if tags: rel[tid] = tags
    # include whole threads that contain a relevant tweet
    threads = collections.defaultdict(list)
    for tid in byid: threads[root(tid)].append(tid)
    keep_roots = {root(t) for t in rel}
    kept = sorted(keep_roots, key=lambda r: -int(r))
    n_kept = sum(len(threads[r]) for r in kept)
    dates = [r.get('ts', '') for r in byid.values() if r.get('ts')]
    with open(OUT, 'w') as f:
        f.write('# @Ngnghm tweets relevant to OO foundations and Houyhnhnm computing\n\n')
        f.write(f'- Source: scry twitter archive, drip-fetched by `fetch-ngnghm.py` into `raw/ngnghm.jsonl` (never pulled by this indexer)\n')
        f.write(f'- Indexed: {datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%MZ")} by `index-tweets.py`\n')
        f.write(f'- Arrived: {len(byid)} tweets (of 7,346 archived); date range {min(dates) if dates else "-"} .. {max(dates) if dates else "-"}\n')
        f.write(f'- Kept: {n_kept} tweets in {len(kept)} threads ({len(rel)} matched a keyword; a thread is kept whole if any tweet in it matched)\n')
        f.write('- Tags: OO = object-orientation keywords; HOU = Houyhnhnm/persistence/platform keywords. Text is verbatim from the archive; `complete=false` means the archive marks the text as possibly truncated.\n\n')
        f.write('Threads are newest-first; within a thread, oldest-first (reply order). `→ id` = in_reply_to; `⟳ id` = quoted.\n\n---\n\n')
        for rt in kept:
            members = sorted(threads[rt], key=lambda t: int(t))
            f.write(f'## thread {rt} ({len(members)} tweets)\n\n')
            for tid in members:
                r = byid[tid]; tags = ','.join(rel.get(tid, [])) or '-'
                refs = []
                if his(r.get('in_reply_to')): refs.append(f'→ {r["in_reply_to"]}')
                elif r.get('in_reply_to') not in (None, '', 'None', 'null', '0'): refs.append(f'→ (not his) {r["in_reply_to"]}')
                if his(r.get('quoted')): refs.append(f'⟳ {r["quoted"]}')
                elif r.get('quoted') not in (None, '', 'None', 'null', '0'): refs.append(f'⟳ (not his) {r["quoted"]}')
                f.write(f'- **{tid}** · {r.get("ts","")} · https://x.com/Ngnghm/status/{tid} · [{tags}] {" ".join(refs)} complete={r.get("complete")} likes={r.get("likes")}\n')
                text = (r.get('text') or '').replace('\n', '\n  > ')
                f.write(f'  > {text}\n\n')
    print(f'arrived={len(byid)} matched={len(rel)} kept={n_kept} threads={len(kept)} -> {OUT}')

if __name__ == '__main__':
    main()
