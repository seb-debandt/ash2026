import json,re,html,glob,os
def plain(h): return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',h))).strip()
d=json.load(open('dl/final.json'))
mine={}
for x in d: mine.setdefault(x['sid'],[]).append(x['pid'])
S={}
for f in glob.glob('dl/sessions/*.html'):
    sid=os.path.basename(f)[:-5]; s=open(f).read()
    title=plain(re.search(r'<h2 class="session-title">(.*?)</h2>',s,re.S).group(1))
    prog=plain(re.search(r'class="session-program">(.*?)</div>',s,re.S).group(1)).replace('Program:','').strip()
    meta=[plain(x) for x in re.findall(r'session-meta-item">(.*?)</div>',s,re.S)][:3]
    order=[]
    for p in re.findall(r"paper-details\.aspx\?pid=(\d+)",s):
        if p not in order: order.append(p)
    desc=''
    m=re.search(r'SESSION DESCRIPTION</h3>(.*?)</div>',s,re.S)
    if m: desc=plain(m.group(1))
    S[sid]=dict(sid=sid,title=title,type=prog,day=meta[0] if meta else '',time=meta[1] if len(meta)>1 else '',room=meta[2] if len(meta)>2 else '',
        total=len(order),papers=[p for p in order if p in mine.get(sid,[])],desc=desc[:600])
print(len(S))
for v in sorted(S.values(),key=lambda v:(v['day'],v['time'])):
    print(v['sid'],v['day'][:9],v['time'],'|',v['type'][:22],'|',v['room'][:28],'|',len(v['papers']),'/',v['total'],'|',v['title'][:70])
json.dump(S,open('dl/sessions.json','w'),ensure_ascii=False)
