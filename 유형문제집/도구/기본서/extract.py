import sys,re,json
sys.path.insert(0,__import__('os').path.dirname(__import__('os').path.abspath(__file__)))
import lib
def text(x):
    out=[]
    for m in re.finditer(r'<hp:t(?:\s[^>]*)?>(.*?)</hp:t>|<hp:script[^>]*>(.*?)</hp:script>|<hp:lineBreak/>|</hp:p>',x,re.S):
        if m.group(1) is not None: out.append(re.sub(r'<[^>]+>',' ',m.group(1)))
        elif m.group(2) is not None: out.append('$'+re.sub(r'\s+',' ',m.group(2)).strip()+'$')
        elif m.group(0)=='</hp:p>': out.append(' / ')
        else: out.append(' / ')
    t=''.join(out)
    return re.sub(r'(\s*/\s*)+',' / ',t).strip(' /').replace('&lt;','<').replace('&gt;','>').replace('&amp;','&')
def blank(p):
    q=lib.nolines(p)
    return not re.search(r'<hp:t>[^<]*\S[^<]*</hp:t>|<hp:equation|<hp:tbl|<hp:rect|<hp:pic|<hp:container|<hp:endNote|<hp:line ',q)
def run(path,tag):
    s,P=lib.paras(path)
    E=[i for i,p in enumerate(P) if '<hp:endNote ' in p]
    heads={i:text(lib.nolines(p)) for i,p in enumerate(P) if re.search(r'유형$|STEP \d$',text(lib.nolines(p)))}
    probs=[];prev_end=-1
    for k,e in enumerate(E):
        a=e
        while a-1>prev_end and not blank(P[a-1]) and (a-1) not in heads: a-=1
        b=e
        nxt=E[k+1] if k+1<len(E) else len(P)
        while b+1<nxt and not blank(P[b+1]) and (b+1) not in heads: b+=1
        q=[];note=''
        for i in range(a,b+1):
            p=lib.nolines(P[i])
            m=re.search(r'<hp:endNote .*?</hp:endNote>',p,re.S)
            if m:
                note=text(m.group(0)); p=p.replace(m.group(0),'')
            q.append(text(p))
        h=max([i for i in heads if i<a],default=None)
        probs.append(dict(file=tag,k=k+1,paras=[a,b],endnote_para=e,section=heads.get(h,''),q=' / '.join(x for x in q if x),sol=note))
        prev_end=b
    return probs
out=[]
for path,tag in [('gx/913a98b3/Contents/section0.xml','다항식의연산'),('gx/45d7db63/Contents/section0.xml','항등식'),('gx/0f284f49/Contents/section0.xml','나머지정리')]:
    out+=run(path,tag)
json.dump(out,open('gx/problems.json','w'),ensure_ascii=False,indent=1)
for p in out: print(p['file'],p['k'],p['paras'],p['section'][:20],'|',p['q'][:110])
