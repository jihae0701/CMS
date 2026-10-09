import re
def top_spans(x):
    start=x.index('>',x.index('<hs:sec'))+1
    out=[];depth=0;st=0
    for m in re.finditer(r'<hp:p\b[^>]*?(/?)>|</hp:p>',x[start:]):
        t=m.group(0);pos=m.start()+start
        if t.startswith('</'):
            depth-=1
            if depth==0: out.append((st,m.end()+start))
        elif not t.endswith('/>'):
            if depth==0: st=pos
            depth+=1
    return out
def nolines(p): return re.sub(r'<hp:linesegarray>.*?</hp:linesegarray>','',p,flags=re.S)
def paras(path):
    s=open(path,encoding='utf8').read()
    return s,[s[a:b] for a,b in top_spans(s)]
