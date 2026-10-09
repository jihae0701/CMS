import sys,re,importlib.util
from sympy import sympify,simplify,sqrt
spec=importlib.util.spec_from_file_location('u',sys.argv[1]);U=importlib.util.module_from_spec(spec);spec.loader.exec_module(U)
spec=importlib.util.spec_from_file_location('v',sys.argv[2]);V=importlib.util.module_from_spec(spec);spec.loader.exec_module(V)
items=[it for it in U.ITEMS if not it.get('h')]
ans={it.get('v',i):it['ans'] for i,it in enumerate(items,1)}
def conv(s):
    s=s.strip().strip('$')
    if re.match(r'^[①-⑤ㄱ-ㅎ]',s): return s
    s=re.sub(r'\{([^{}]*)\}\s*over\s*\{([^{}]*)\}',r'((\1)/(\2))',s)
    s=re.sub(r'(\d+)\s*over\s*(\d+)',r'((\1)/(\2))',s)
    s=re.sub(r'sqrt\s*\{\s*([^{}]*)\}',r'sqrt(\1)',s); s=re.sub(r'root\s*\{?(\d+)\}?',r'sqrt(\1)',s)
    s=re.sub(r'(\d)\s*sqrt',r'\1*sqrt',s); s=s.replace(' ','')
    return sympify(s)
bad=0; seen=set()
for no,ok,got,exp in V.R:
    if no not in ans: continue          # 최종 책에서 뺀 문항
    seen.add(no)
    a=conv(ans[no])
    same = (a==exp) if isinstance(a,str) else simplify(a-sympify(exp))==0
    if not same or not ok: bad+=1; print('MISMATCH',no,ans[no],exp,got,ok)
miss=[k for k in ans if k not in seen]
if miss: bad+=len(miss); print('검산 없음',miss)
print('문항',len(ans),'검산',len(seen),'불일치',bad)
