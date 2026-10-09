import sys,re,importlib.util
from sympy import sympify,simplify,sqrt
spec=importlib.util.spec_from_file_location('u',sys.argv[1]);U=importlib.util.module_from_spec(spec);spec.loader.exec_module(U)
spec=importlib.util.spec_from_file_location('v',sys.argv[2]);V=importlib.util.module_from_spec(spec);spec.loader.exec_module(V)
ans=[it['ans'] for it in U.ITEMS if not it.get('h')]
def conv(s):
    s=s.strip().strip('$')
    if re.match(r'^[①-⑤ㄱ-ㅎ]',s): return s
    s=re.sub(r'\{([^{}]*)\}\s*over\s*\{([^{}]*)\}',r'((\1)/(\2))',s)
    s=re.sub(r'(\d+)\s*over\s*(\d+)',r'((\1)/(\2))',s)
    s=re.sub(r'sqrt\s*\{\s*([^{}]*)\}',r'sqrt(\1)',s); s=re.sub(r'root\s*\{?(\d+)\}?',r'sqrt(\1)',s)
    s=re.sub(r'(\d)\s*sqrt',r'\1*sqrt',s); s=s.replace(' ','')
    return sympify(s)
bad=0
for no,ok,got,exp in V.R:
    a=conv(ans[no-1])
    same = (a==exp) if isinstance(a,str) else simplify(a-sympify(exp))==0
    if not same or not ok: bad+=1; print('MISMATCH',no,ans[no-1],exp,got,ok)
print('문항',len(ans),'검산',len(V.R),'불일치',bad)
