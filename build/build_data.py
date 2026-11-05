import re,html,json,sys
from html.parser import HTMLParser
ALLOW={'p','strong','b','em','i','sup','sub','br','ul','ol','li','table','thead','tbody','tr','td','th'}
class San(HTMLParser):
    def __init__(s): super().__init__(convert_charrefs=True); s.o=[]; s.skip=0
    def handle_starttag(s,t,a):
        if t in('script','style'): s.skip+=1
        elif t in ALLOW: s.o.append(f'<{t}>')
    def handle_endtag(s,t):
        if t in('script','style'): s.skip-=1
        elif t in ALLOW and t!='br': s.o.append(f'</{t}>')
    def handle_data(s,d):
        if not s.skip: s.o.append(html.escape(d,quote=False))
def san(h):
    p=San(); p.feed(h); out=''.join(p.o)
    out=re.sub(r'\s+',' ',out); out=re.sub(r'<p>\s*</p>','',out); out=out.replace('\xa0',' ')
    return out.strip()
def plain(h): return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',h))).strip()
def block(s,a,b):
    i=s.find(a); j=s.find(b,i)
    return s[i:j] if i>=0 else ''
cands=json.load(open(sys.argv[1]))
res=[]
for c in cands:
    if c['cls']=='none': continue
    s=open(f"dl/papers/{c['pid']}.html").read()
    ab=block(s,'id="ashcontent_pnlPaperAuthors"','<!-- End Authors')
    ab=re.sub(r'<sup>.*?</sup>','',ab,flags=re.S); ab=re.sub(r'<h3.*?</h3>','',ab,flags=re.S)
    authors=plain(ab)
    names=[]
    # split on ", " where next token starts a new name: use original html <strong>/commas -> approximate by splitting at sup positions
    raw=block(s,'id="ashcontent_pnlPaperAuthors"','<!-- End Authors'); raw=re.sub(r'^[^>]*>','',raw); raw=re.sub(r'<h3.*?</h3>','',raw,flags=re.S)
    parts=re.split(r'<sup>[^<]*</sup>\s*,?',raw)
    for p in parts:
        t=plain(p).strip(' ,')
        if t: names.append(t)
    if len(names)==1 and ',' in names[0] and len(names[0])>80: names=[authors]
    # first author lacks sup: split first chunk at </strong>
    m=re.search(r'<strong>(.*?)</strong>',raw,re.S)
    first=plain(m.group(1)) if m else (names[0] if names else '')
    if m and names and names[0]!=first and names[0].startswith(first):
        rest=names[0][len(first):].strip(' ,'); names=[first]+([rest] if rest else [])+names[1:]
    af=block(s,'id="ashcontent_pnlPaperAffiliations"','<!-- End Affil')
    affs=[plain(re.sub(r'<sup>.*?</sup>','',x)) for x in re.findall(r'<div><em>(.*?)</em></div>',af,re.S)]
    abs_html=block(s,'id="pnlPaperAbstract"','<!-- End Abstract'); abs_html=re.sub(r'<h3.*?</h3>','',abs_html,flags=re.S)
    abs_html=re.sub(r'^[^>]*>','',abs_html)
    dis=block(s,'id="ashcontent_pnlPaperDisclosures"','<!-- End Disc'); dis=re.sub(r'<h3.*?</h3>','',dis,flags=re.S); dis=re.sub(r'^[^>]*>','',dis)
    day,time,room=(c['meta']+['','',''])[:3]
    sess=c['session']
    res.append(dict(pid=c['pid'],no=c['abstract_no'],title=c['title'].strip(),authors=names,affils=affs,
      abstract=san(abs_html),disclosures=plain(dis),session=sess,sid=c['sid'],type=c['program'],
      day=day,time=time,room=room,tier={'title':1,'abs3+':2,'abs1-2':3}[c['cls']],n=c['n'],
      url=f"https://onlineprogram.hematology.org/paper-details.aspx?pid={c['pid']}"))
json.dump(res,open(sys.argv[2],'w'),ensure_ascii=False,indent=1)
print(len(res))
