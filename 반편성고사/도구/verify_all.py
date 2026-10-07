import sys; sys.path.insert(0,'..')
from problems import M1, M2
import sympy as sp
from itertools import combinations, permutations, product
from math import perm
x,y,a,b,k,t=sp.symbols('x y a b k t')
R={}
# ---- 공수1 ----
s=sp.solve([a-b-3, a**3-b**3-63],[a,b]); R[(1,1)]={sp.simplify(u*v) for u,v in s}
A=sp.Matrix(2,2,lambda i,j:2*(i+1)-(j+1)); B=sp.Matrix(2,2,lambda i,j:(i+1)*(j+1)); R[(1,2)]=sum(A+2*B)
R[(1,3)]=sum(r for r in sp.solve(x**3-4*x**2+x+6) if r>0)
R[(1,4)]=sum(v for v in range(-50,51) if v*v-2*v-8>=0 and v*v-36<0)
# P(1)=5,P(-3)=-3, R=ax+b
s=sp.solve([a+b-5,-3*a+b+3],[a,b]); R[(1,5)]=2*s[a]+s[b]
kk=[r for r in sp.solve(k**2-3-6) if r>0][0]; AB=sp.Matrix([[1,2],[kk,3]])*sp.Matrix([[kk,2],[-1,1]]); assert AB[0,1]==4 and AB[1,0]==6; R[(1,6)]=AB[0,0]+AB[1,1]
xr,yr=sp.symbols('xr yr',real=True); z=xr+sp.I*yr
sol=[s_ for s_ in sp.solve([sp.re(sp.expand(z**2-6*sp.conjugate(z))),sp.im(sp.expand(z**2-6*sp.conjugate(z)))],[xr,yr],dict=True) if s_[yr]!=0]
R[(1,7)]={sp.simplify(s_[xr]**2+s_[yr]**2) for s_ in sol}
sol=sp.solve([x**2-4*x*y+3*y**2, x**2-2*y**2-21],[x,y],dict=True); R[(1,8)]={sp.nsimplify(s_[x]+s_[y]) for s_ in sol if s_[x].is_real and s_[x]>0 and s_[y]>0}
def clubs():
    S=[('S',i) for i in range(4)]+[('M',i) for i in range(2)]
    sets=[set(c) for c in combinations(S,3) if any(e[0]=='S' for e in c) and any(e[0]=='M' for e in c)]
    return sum(1 for p in sets for q in sets if len(p-q)>=1)
R[(1,9)]=clubs()
res=[]
for av in range(-60,61):
    cnt=sum(1 for v in range(-400,401) if v*v-4*v-5>=0 and (v+av)*(v-av+4)<0)
    if cnt==6: res.append(av)
R[(1,10)]=sum(res)
def books():
    items=['F0','F1','P0','P1','P2','P3']; c=0
    for asg in product(range(5),repeat=6):
        got=[[] for _ in range(5)]; ok=True
        for it,sx in zip(items,asg):
            if it[0]=='F' and sx<2: ok=False;break
            got[sx].append(it)
        if ok and all(got) and all(sum(1 for e in g if e[0]=='P')<=1 for g in got): c+=1
    return c
R[(1,11)]=books()
def g(kv):
    return len({-1,4,kv-1,kv+4})
ks=set()
for kv2 in range(-200,201):  # 특수값은 정수(반정수 포함 검사)
    for kv in (kv2/2,):
        if g(kv-6)+g(kv+4)==6: ks.add(kv)
R[(1,12)]=sum(ks)
rooms=[r for r in [101,102,103,104,105,201,202,203,204,205] if r not in (102,204)]
c=0
for A_ in rooms:
    for B_ in rooms:
        if B_!=A_ and abs(A_-B_)==1:
            for C_ in rooms:
                if C_ not in (A_,B_) and abs(A_-C_)>4 and abs(A_-C_)!=100: c+=perm(len(rooms)-3,2)
R[(1,13)]=c
# 14: f=(x-2)^2-6, count real roots of f(x)(f(x)+2f(t))=0 over t grid
f=lambda v:(v-2)**2-6
def nroots(tv):
    rs=set()
    for eq in (sp.Poly((x-2)**2-6,x), sp.Poly((x-2)**2-6+2*f(tv),x)):
        for r in sp.roots(eq).keys():
            if r.is_real: rs.add(sp.nsimplify(r))
    return len(rs)
ts=[tv for tv in [sp.Rational(n,4) for n in range(-40,41)] if nroots(tv)==3]
assert ts==[-1,5], ts
R[(1,14)]=f(8)
s=sp.solve(a/6-sp.Rational(3,2),a)[0]; r=sp.solve(x**2-s*x+6); R[(1,15)]=sp.simplify(r[0]**2+r[1]**2)
r2=3-sp.I; aa=-(r2+sp.conjugate(r2)); bb=sp.expand(r2*sp.conjugate(r2)); R[(1,16)]=aa**2+bb**2
seats=[11,12,21,22,31,32,41,42]
R[(1,17)]=sum(1 for p in permutations(seats,4) if p[0]%2==0 and p[1]<=22 and p[2]>=31 and p[3]>=31)
D=sp.discriminant(x**2+(a-2)*x+3*a-3,x); R[(1,18)]=sum(sp.solve(D,a))
bs,cs=sp.symbols('bs cs')
sol=sp.solve([ (bs*cs)**3+1, 2*bs*cs+bs+cs-2],[bs,cs],dict=True)
R[(1,19)]={sp.nsimplify(sp.simplify(s_[bs]**3+s_[cs]**3)) for s_ in sol if s_[bs].is_real}
u=sp.solve(2*(1-k)-4+12,k)[0]; fx=(x+1)*(x-u); gx=(x+1)*(x-3); hx=(x-3)*(x-u)
assert sp.rem(sp.expand(fx*gx),sp.expand((x+1)*hx),x)==0 and sp.rem(sp.expand(gx*hx),sp.expand((x-3)*fx),x)==0
R[(1,20)]=hx.subs(x,0)
# ---- 공수2 ----
m=sp.Rational(8-2,3-1); R[(2,1)]=1-(-1/m)*3
fmap={1:4,2:1,3:5,4:2,5:3}; inv={v:k_ for k_,v in fmap.items()}; R[(2,2)]=fmap[fmap[1]]+inv[5]
av=sp.solve(2*a-3-5,a)[0]; R[(2,3)]=sp.solve(av*x-3-13,x)[0]
R[(2,4)]=sp.solve((1+a+5)/3-3,a)[0]+sp.solve((4-2+b)/3-2,b)[0]
# 5: 변환 후 직선이 중심 지남
cx,cy=-1,4; assert sp.expand((x+1)**2+(y-4)**2-9)==x**2+y**2+2*x-8*y+8
R[(2,5)]=sp.solve(-a*(cx-2)-2-cy,a)[0]
R[(2,6)]=sum(av for av in range(-20,21) if all(abs(v-av)<=3 for v in [2+i/100 for i in range(201)]))
s=sp.solve([a/5+b-3,a/3+b-1],[a,b]); assert s[a]<0; R[(2,7)]=s[a]+s[b]
th=sp.symbols('th'); P=(-1+2*sp.cos(th),2+2*sp.sin(th)); area=sp.Abs((4-1)*(P[1]+3)-(1+3)*(P[0]-1))/2
import math
R[(2,8)]=sp.nsimplify(max(float(area.subs(th,v*2*math.pi/20000)) for v in range(20000)),tolerance=1e-4)
kv=sp.solve(16*k*sp.sqrt(2*k)-64,k)[0]; A_=(kv,sp.sqrt(2*kv)); B_=(9*kv,sp.sqrt(18*kv)); R[(2,9)]=sp.sqrt((B_[0]-A_[0])**2+(B_[1]-A_[1])**2)
ok=[v/100 for v in range(-1000,1001) if all(abs(xx-1)<=5 for xx in [min(2*v/100,-v/100)+i*(abs(3*v/100))/50 for i in range(51)])]
R[(2,10)]=sp.nsimplify(max(ok)*min(ok))
R[(2,11)]=sp.sqrt((0-10)**2+(1-6)**2)-sp.sqrt(5)
ks=[kv for kv in range(-30,31) if kv!=-6 and abs(max((2*xx/100+kv)/(xx/100-3) for xx in range(0,201))-4)<1e-9]; R[(2,12)]=ks[0] if len(ks)==1 else ks
Ax=sp.solve(sp.Eq(3*sp.sqrt(x),x**2/9),x); Ax=max(Ax); P_=(Ax*4/9,Ax*4/9)
Bx=sp.solve(3*sp.sqrt(x)-P_[1],x)[0]; Cx=[r for r in sp.solve(x**2/9-P_[1],x) if r>0][0]; R[(2,13)]=(Cx-Bx)*(Ax-P_[1])/2
ms=[r for r in sp.solve((4*k-2)**2/(k**2+1)-2,k) if 0<r<1]
# 검증: OH:BH=3:1
mv=ms[0]; d2=(4*mv-2)**2/(mv**2+1); assert sp.simplify((20-d2)/(4-d2))==9; R[(2,14)]=mv
av=2; bv=sp.sqrt(2*5+6)+av; assert sp.sqrt(2*(-3)+6)+av==2; R[(2,15)]=av+bv
A_={d for d in range(1,13) if 12%d==0}; B_={2,3,5,7}; R[(2,16)]=sum((A_|B_)-(A_&B_))
xt=sp.Rational(2); yt=-1; assert xt**2+yt**2==5; D=sp.discriminant(x**2+a*x+a-8-(2*x-5),x); R[(2,17)]=sp.solve(D,a)
Pp=(12/3,6/3); Ap=(2,1); Bp=(6,-2)
vals=[(Pp[0]-(Ap[0]+(Bp[0]-Ap[0])*i/10000))**2+(Pp[1]-(Ap[1]+(Bp[1]-Ap[1])*i/10000))**2 for i in range(10001)]
R[(2,18)]=round(max(vals)+min(vals),6)
fu={kk_: pow(7,kk_,10) for kk_ in range(1,10)}
best=0
from itertools import combinations as C2
for n in range(2,10):
    for As in C2(range(1,10),n):
        S=set(As)
        if all(fu[a_] in S and fu[fu[a_]]==3 for a_ in S) and all(fu[p]<=fu[q] for p in S for q in S if p<q): best=max(best,sum(S))
R[(2,19)]=best
best=0;X=range(1,11)
for I in C2(X,2):
    for Dd in C2([v for v in X if v not in I],3):
        if all((p+1)%2==0 and (p+1)//2 in Dd for p in I) and all(q+3<=10 and q+3 not in Dd for q in Dd): best=max(best,sum(Dd))
R[(2,20)]=best
bad=0
for sub,M in ((1,M1),(2,M2)):
    for pr in M:
        import re as _re
        exp = sp.sympify(_re.sub(r'(\d) sqrt',r'\1*sqrt',pr['choices'][pr['ans']-1]).replace(' over ','/').replace('{','(').replace('}',')')) if pr['choices'] else pr['ans']
        got=R[(sub,pr['no'])]
        if isinstance(got,(set,list)): got=list(got); got=got[0] if len(got)==1 else got
        okk = (not isinstance(got,list)) and sp.simplify(sp.sympify(got)-exp)==0
        print(f"공수{sub} {pr['no']:>2}번  계산={got}  표기정답={exp}  {'OK' if okk else '<<< 불일치'}")
        bad+= (not okk)
print('불일치',bad)
