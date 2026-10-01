#!/usr/bin/env python3
"""Drip-fetch every archived tweet of @Ngnghm (author_id 3399611914) from scry into raw/ngnghm.jsonl.
Scry lets ~1.3 MB/day of X rows leave per account, so this runs for days: newest first, pages of
120 tweets, sleeping out every 429 by its retry_after. Re-runnable: it resumes below the oldest
tweet_id already on disk. State: raw/ngnghm.jsonl (one tweet per line, newest first within a page)."""
import json, os, sys, time, urllib.request
KEY = open(os.path.expanduser('~/.scry-key')).read().strip()
AUTHOR = 3399611914
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'raw', 'ngnghm.jsonl')
LOG = os.path.join(HERE, 'raw', 'fetch.log')
PAGE = 120
COLS = ["toString(tweet_id) AS tweet_id", "argMax(original_timestamp, version) AS ts",
        "argMax(text, version) AS text", "argMax(text_is_complete, version) AS complete",
        "toString(argMax(in_reply_to_tweet_id, version)) AS in_reply_to",
        "toString(argMax(quoted_tweet_id, version)) AS quoted", "argMax(like_count, version) AS likes"]
def log(msg):
    line = time.strftime('%Y-%m-%d %H:%M:%S ') + msg
    print(line, file=sys.stderr); open(LOG, 'a').write(line + '\n')
def query(sql, secs=90):
    req = urllib.request.Request('https://scry.io/v1/scry/query', method='POST', data=json.dumps({'sql': sql}).encode(),
        headers={'Authorization': 'Bearer ' + KEY, 'Content-Type': 'application/json', 'x-scry-max-seconds': str(secs)})
    while True:
        try:
            with urllib.request.urlopen(req, timeout=secs + 30) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            body = e.read().decode()
            try: err = json.loads(body)['error']
            except Exception: err = {'code': str(e.code), 'message': body[:300]}
            if e.code == 429:
                wait = int(err.get('retry_after_seconds') or 900) + 30
                log(f'429 {err.get("code")}: sleeping {wait}s'); time.sleep(wait); continue
            log(f'HTTP {e.code} {err.get("code")}: {err.get("message","")[:300]}')
            if e.code >= 500: time.sleep(120); continue
            raise SystemExit(1)
        except (urllib.error.URLError, TimeoutError) as e:
            log(f'network: {e}; sleeping 120s'); time.sleep(120)
def oldest_on_disk():
    if not os.path.exists(OUT): return None
    ids = [json.loads(l)['tweet_id'] for l in open(OUT) if l.strip()]
    return min(ids, key=int) if ids else None
os.makedirs(os.path.dirname(OUT), exist_ok=True)
last = oldest_on_disk()
log(f'start; resuming below {last}' if last else 'start; fresh')
total = 0
while True:
    bound = f' AND tweet_id < {last}' if last else ''
    sql = (f"SELECT {', '.join(COLS)} FROM twitter.tweets WHERE author_id = {AUTHOR} AND tweet_id IN "
           f"(SELECT tweet_id FROM twitter.tweets_by_author WHERE author_id = {AUTHOR}{bound}) "
           f"GROUP BY tweet_id ORDER BY tweet_id DESC LIMIT {PAGE}")
    res = query(sql)
    names = [c['name'] for c in res['columns']]
    rows = [dict(zip(names, r)) for r in res['rows']]
    if not rows:
        log(f'done: nothing below {last}; total this run {total}'); break
    with open(OUT, 'a') as f:
        for r in rows: f.write(json.dumps(r, ensure_ascii=False) + '\n')
    total += len(rows); last = rows[-1]['tweet_id']
    log(f'+{len(rows)} (oldest now {rows[-1]["ts"]}); partial={res.get("deadline_partial")} truncated={res.get("truncated")}')
    time.sleep(20)
