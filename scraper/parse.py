import re,html,json,glob,os,sys
from html.parser import HTMLParser
def txt(s):
    s=re.sub(r'<br\s*/?>','\n',s); s=re.sub(r'</p>|</div>','\n',s); s=re.sub(r'<[^>]+>','',s); s=html.unescape(s)
    return re.sub(r'[ \t\r\f\v]+',' ',re.sub(r'\n\s*\n+','\n\n',s)).strip()
def between(s,start,end):
    i=s.find(start); 
    if i<0: return ''
    j=s.find(end,i+len(start)); return s[i+len(start):j if j>0 else None]
out=[]
for f in sorted(glob.glob(sys.argv[1]+'/*.html')):
    s=open(f).read(); pid=os.path.basename(f)[:-5]
    m=re.search(r'<main.*?</main>',s,re.S).group(0)
    sess_a=re.search(r'id="ashcontent_lnkSessionTitle" href="session-details\.aspx\?sid=(\d+)">(.*?)</a>',m,re.S)
    meta=re.findall(r'session-meta-item">(.*?)</div>',m,re.S)
    prog=txt(between(m,'session-program','</div>')).replace('">','').replace('Program:','').strip()
    paper_block=m[m.find('>PAPER<'):]
    title=txt(between(paper_block,'<h2 class="session-title">','</h2>'))
    authors=txt(between(m,'id="ashcontent_pnlPaperAuthors"','id="ashcontent_pnlPaperAffiliations"'))
    affs=txt(between(m,'id="ashcontent_pnlPaperAffiliations"','id="pnlPaperAbstract"'))
    abstract=txt(between(m,'id="pnlPaperAbstract"','id="ashcontent_pnlPaperDisclosures"'))
    discl=txt(between(m,'id="ashcontent_pnlPaperDisclosures"','Begin New Search'))
    kw=txt(between(m,'id="ashcontent_pnlSessionKeywords"','</div>'))
    num=re.match(r'(\d+)\s+(.*)',title,re.S)
    out.append(dict(pid=pid,sid=sess_a and sess_a.group(1),session=sess_a and txt(sess_a.group(2)),program=prog,
        meta=[txt(x) for x in meta],abstract_no=num and num.group(1),title=num.group(2).strip() if num else title,
        authors_raw=authors,affils_raw=affs,abstract=abstract,disclosures=discl,keywords=kw))
json.dump(out,open(sys.argv[2],'w'),ensure_ascii=False,indent=1)
print(len(out))
