# 한글 수식 스크립트의 대략적인 가로 폭(em) 추정 — 수정·추가한 수식의 sz 폭을 정하는 데 쓴다
import re
CMDS_W={'lim':1.35,'therefore':0.9,'because':0.9,'cdots':1.0,'cdot':0.4,'times':0.8,'le':0.8,'leq':0.8,'ge':0.8,'geq':0.8,
        'ne':0.8,'inf':1.0,'infty':1.0,'alpha':0.6,'beta':0.6,'circ':0.6,'rarrow':1.0,'larrow':1.0,'pm':0.8,'mp':0.8,
        'theta':0.5,'pi':0.55,'sum':1.0,'int':0.6,'ldots':1.0,'prime':0.3,'box':1.2}
IGN={'it','rm','bold','left','right','from','to'}
def tokenize(s):
    s=s.replace('->','→').replace('!=','≠').replace('+-','±')
    toks=re.findall(r'\{|\}|\^|_|`|~|#|&|"[^"]*"|[A-Za-z]+|\d+|\S',s)
    return toks
def parse(toks,i=0,stop=None):
    # returns list of items: each item width in em; handles over/sup/sub/sqrt
    items=[]; 
    while i<len(toks):
        t=toks[i]
        if t=='}':
            return items,i+1
        if t=='{':
            sub,i=parse(toks,i+1); items.append(sum(sub)); continue
        tl=t.lower()
        if tl=='over' and items:
            num=items.pop(); den,i=parse_one(toks,i+1); items.append(max(num,den)+0.2); continue
        if t in('^','_'):
            v,i=parse_one(toks,i+1)
            if items and t=='_' and getattr(parse,'lastlim',False):
                items[-1]=max(items[-1],v*0.7); parse.lastlim=False
            else: items.append(v*0.65)
            continue
        if tl in('sqrt','root'):
            v,i=parse_one(toks,i+1)
            if i<len(toks) and toks[i].lower()=='of':
                v,i=parse_one(toks,i+1)
            items.append(v+0.8); continue
        parse.lastlim=False
        if t=='`': items.append(0.12); i+=1; continue
        if t=='~': items.append(0.3); i+=1; continue
        if t in('#','&'): i+=1; continue
        if t.startswith('"'): items.append(0.5*len(t)-1); i+=1; continue
        if tl in IGN: i+=1; continue
        if tl=='cases': 
            i+=1; continue
        if tl in CMDS_W:
            items.append(CMDS_W[tl]); parse.lastlim=(tl=='lim'); i+=1; continue
        if re.fullmatch(r'[A-Za-z]+',t):
            items.append(0.5*len(t)); i+=1; continue
        if re.fullmatch(r'\d+',t): items.append(0.5*len(t)); i+=1; continue
        if t in '+-=<>→≠±': items.append(0.9); i+=1; continue
        if t in '(),[]|.:;\'': items.append(0.35); i+=1; continue
        if ord(t[0])>0x3000: items.append(1.0); i+=1; continue
        items.append(0.6); i+=1
    return items,i
def parse_one(toks,i):
    if i>=len(toks): return 0,i
    if toks[i]=='{':
        sub,j=parse(toks,i+1); return sum(sub),j
    it,j=parse(toks[i:i+1]); return sum(it),i+1
def em(script):
    parse.lastlim=False
    toks=tokenize(script)
    # cases/eqalign: take widest row approx -> use total/rows heuristic
    if re.search(r'cases|eqalign',script,re.I):
        rows=max(1,script.count('#'))
        items,_=parse(toks); return sum(items)/ (1+0.6*(rows))
    items,_=parse(toks); return sum(items)
