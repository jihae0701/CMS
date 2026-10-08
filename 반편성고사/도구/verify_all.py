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

import numpy as np, math
from fractions import Fraction as Fr
# 7: z̄=-z 인 근(실수부 0)을 갖는 k — 후보를 구하고 수치로 확인, 무작위 k 로 다른 값이 없는지 점검
Bk=lambda kv: kv**2-2*kv-8; Ck=lambda kv: kv**2+kv-6
def has_imag_root(kv):
    r=np.roots([1,float(Bk(kv)),float(Ck(kv))]); return any(abs(z_.real)<1e-9 for z_ in r)
cand={sp.nsimplify(r) for r in sp.solve(Ck(k),k)}|{sp.nsimplify(r) for r in sp.solve(Bk(k),k) if Ck(r)>0}
assert all(has_imag_root(float(c)) for c in cand)
assert not has_imag_root(-2.0)
import random; random.seed(1)
assert not any(has_imag_root(random.uniform(-20,20)) for _ in range(20000))
R[(1,7)]=sp.prod(list(cand))
def talk():
    people=[(0,i) for i in range(4)]+[(1,0),(1,1),(2,0)]
    return sum(1 for s_ in permutations(people,5) if all(not(s_[i][0]==0 and s_[i+1][0]==0) for i in range(4)))
R[(1,8)]=talk()
A=sp.Matrix(2,2,lambda i,j: 4-(i+1) if i==j else (j+1)+1)
S_=A+A**2+A**3+A**4; kv=S_[0,0]/A[0,0]; assert S_==kv*A; R[(1,9)]=kv
Bm=sp.Matrix(2,2,sp.symbols('b0:4')); Cm=sp.Matrix(2,2,sp.symbols('c0:4')); Am=sp.Matrix([[0,12],[0,0]])
eqs=list(Am*Bm)+list(Cm*Am)+list(Bm*Cm-Am)+[sum(Bm)-4, Cm[0,1]-Cm[1,1]]
sols=sp.solve(eqs, list(Bm)+list(Cm), dict=True)
R[(1,10)]={sp.simplify(sum(Cm.subs(s_))) for s_ in sols}
rooms=[r for r in [101,102,103,104,105,201,202,203,204,205] if r not in (102,204)]
c=0
for A_ in rooms:
    for B_ in rooms:
        if B_!=A_ and abs(A_-B_)==1:
            for C_ in rooms:
                if C_ not in (A_,B_) and abs(A_-C_)>4 and abs(A_-C_)!=100: c+=perm(len(rooms)-3,2)
R[(1,11)]=c
def g(kv):
    return len({-1,4,kv-1,kv+4})
ks=set()
for kv2 in range(-200,201):  # 특수값은 정수(반정수 포함 검사)
    for kv in (kv2/2,):
        if g(kv-6)+g(kv+4)==6: ks.add(kv)
R[(1,12)]=sum(ks)
u=sp.solve(2*(1-k)-4+12,k)[0]; fx=(x+1)*(x-u); gx=(x+1)*(x-3); hx=(x-3)*(x-u)
assert sp.rem(sp.expand(fx*gx),sp.expand((x+1)*hx),x)==0 and sp.rem(sp.expand(gx*hx),sp.expand((x-3)*fx),x)==0
R[(1,13)]=hx.subs(x,0)
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

# 15
res=set()
for kv in sp.solve(sp.Rational(3,2)*k**2-4*k-14,k):
    rts=sp.solve(x**2+kv*x-kv**2/2+4*kv,x)
    if len(rts)==2 and all(r.is_real for r in rts):
        for al,be in ((rts[0],rts[1]),(rts[1],rts[0])):
            if sp.simplify(al**2-kv*be-14)==0: res.add(sp.simplify(al**2+be**2))
R[(1,15)]=res
def nb(p,v):
    i=p.index(v); return (p[i-1],p[i+1]) if 0<i<len(p)-1 else None
R[(1,16)]=sum(1 for p in permutations(range(1,8)) if p[0]%2 and p[-1]%2 and nb(p,4) and sum(nb(p,4))%2==1)
bb_,cc_=sp.symbols('bb cc')
poly=x**3+(2*a+1)*x**2+(3*a+2)*x+a+2
sols=sp.solve(sp.Poly(sp.expand(poly-(x+bb_)*(x+cc_)**2),x).all_coeffs(),[a,bb_,cc_],dict=True)
vals={sp.simplify(s_[a]+s_[bb_]+s_[cc_]) for s_ in sols if all(v.is_real for v in s_.values())}
R[(1,17)]=max(vals)+min(vals)
bs,cs=sp.symbols('bs cs')
sol=sp.solve([ (bs*cs)**3+1, 2*bs*cs+bs+cs-2],[bs,cs],dict=True)
R[(1,18)]={sp.nsimplify(sp.simplify(s_[bs]**3+s_[cs]**3)) for s_ in sol if s_[bs].is_real}

R[(1,19)]=sum(1 for t_ in combinations(range(1,10),5) if 2*(t_[1]-t_[0])<t_[4]-t_[1] and (t_[1]+t_[4])%2==1)
p_,q_=sp.symbols('p q')
g_=x**2+p_*x+q_; h_=g_-2*x-3
eqs=sp.Poly(sp.expand(g_*h_-(x**4+(a-2)*x**3+b*x**2+a*x+10)),x).all_coeffs()
res=set()
for s_ in sp.solve(eqs,[p_,q_,a,b],dict=True):
    gg=g_.subs(s_); hh=h_.subs(s_)
    if all(v.is_real for v in s_.values()) and not any(r.is_real for r in sp.Poly(sp.expand(gg*hh),x).all_roots()):
        assert sp.rem(hh,gg,x)==-2*x-3
        res.add(s_[a]**2+s_[b]**2)
R[(1,20)]=res
# ---- 공수2 ----
m=sp.Rational(8-2,3-1); R[(2,1)]=1-(-1/m)*3
fmap={1:4,2:1,3:5,4:2,5:3}; inv={v:k_ for k_,v in fmap.items()}; R[(2,2)]=fmap[fmap[1]]+inv[5]
av=sp.solve(2*a-3-5,a)[0]; R[(2,3)]=sp.solve(av*x-3-13,x)[0]
R[(2,4)]=sp.solve((1+a+5)/3-3,a)[0]+sp.solve((4-2+b)/3-2,b)[0]
# 5: 변환 후 직선이 중심 지남
cx,cy=-1,4; assert sp.expand((x+1)**2+(y-4)**2-9)==x**2+y**2+2*x-8*y+8
R[(2,5)]=sp.solve(-a*(cx-2)-2-cy,a)[0]
R[(2,6)]=sum(av for av in range(-20,21) if all(abs(v-av)<=3 for v in [2+i/100 for i in range(201)]))
ok=[v/100 for v in range(-1000,1001) if all(abs(xx-1)<=5 for xx in [min(2*v/100,-v/100)+i*(abs(3*v/100))/50 for i in range(51)])]
R[(2,7)]=sp.nsimplify(max(ok)*min(ok))
R[(2,7)]=sp.nsimplify(max(ok)*min(ok))
R[(2,8)]=sp.sqrt((0-10)**2+(1-6)**2)-sp.sqrt(5)

def bij(av):
    f_=lambda v: (av+4)*v+3 if v<2 else (6-av)*v+4*av-1
    xs=[i/50 for i in range(-500,501)]; ys=[f_(v) for v in xs]
    inc=all(ys[i]<ys[i+1] for i in range(len(ys)-1)); dec=all(ys[i]>ys[i+1] for i in range(len(ys)-1))
    cont=abs(f_(2-1e-12)-f_(2))<1e-6
    return (inc or dec) and cont
R[(2,9)]=sum(1 for av in range(-50,51) if bij(av))
ks=[kv for kv in range(-30,31) if kv!=-6 and abs(max((2*xx/100+kv)/(xx/100-3) for xx in range(0,201))-4)<1e-9]; R[(2,10)]=ks[0] if len(ks)==1 else ks

best=min(math.hypot(tt+4,3)+math.hypot(4-(tt+2),5) for tt in [i/10000 for i in range(-100000,100001)])
R[(2,11)]=sp.nsimplify(round(best,6))
Ax=sp.solve(sp.Eq(3*sp.sqrt(x),x**2/9),x); Ax=max(Ax); P_=(Ax*4/9,Ax*4/9)
Bx=sp.solve(3*sp.sqrt(x)-P_[1],x)[0]; Cx=[r for r in sp.solve(x**2/9-P_[1],x) if r>0][0]; R[(2,12)]=(Cx-Bx)*(Ax-P_[1])/2
ms=[r for r in sp.solve((4*k-2)**2/(k**2+1)-2,k) if 0<r<1]
# 검증: OH:BH=3:1
mv=ms[0]; d2=(4*mv-2)**2/(mv**2+1); assert sp.simplify((20-d2)/(4-d2))==9; R[(2,13)]=mv

mm,cc=sp.symbols('mm cc',positive=True)
def foot(P,d):  # 원점을 지나는 방향 d 직선 위로 내린 수선의 발
    d=sp.Matrix(d); return d*(sp.Matrix(P).dot(d))/d.dot(d)
Ac=sp.Matrix([cc,cc]); Qp=foot(Ac,[mm,1]); Pp_=foot(Ac,[1,mm])
# 직선 PQ 와 x축의 교점 R
tt=sp.symbols('tt'); Rr=Pp_+tt*(Qp-Pp_); tsol=sp.solve(Rr[1],tt)[0]; Rr=Rr.subs(tt,tsol)
msol=[v for v in sp.solve(sp.simplify((Qp-Pp_).norm()**2-4*(Rr-Qp).norm()**2),mm) if v>1]
assert len(msol)==1; mv=msol[0]
area=sp.Abs(Pp_[0]*Qp[1]-Qp[0]*Pp_[1])/2
cv=[v for v in sp.solve(sp.simplify(area.subs(mm,mv))-16,cc) if v>0][0]
Q_=Qp.subs({mm:mv,cc:cv}); A_c=Ac.subs(cc,cv)
# 직선 AQ 와 l1: y=mv x 의 교점
ss=sp.symbols('ss'); Bp_=A_c+ss*(Q_-A_c); ssol=sp.solve(Bp_[1]-mv*Bp_[0],ss)[0]; Bp_=Bp_.subs(ss,ssol)
R[(2,14)]=sp.nsimplify(sp.sqrt(sp.simplify((Bp_-Q_).norm()**2)))
res=set()
for s_ in sp.solve([b**2-3*b],[b],dict=True):
    if s_[b]>0:
        root=sp.solve(sp.diff(x**2-2*s_[b]*x+3*s_[b],x),x)[0]; av=2*root
        # 확인: x≠a/2 에서 q 참, x=a/2 에서 q 거짓
        qf=sp.lambdify(x,x**2-2*s_[b]*x+3*s_[b])
        assert qf(float(av/2))<=0 and all(qf(float(av/2)+d)>0 for d in (-3,-0.1,0.1,3))
        res.add(av+s_[b])
R[(2,15)]=res
hh_,kk_,rr_=sp.symbols('hh kk rr',real=True)
sols=sp.solve([kk_, (hh_-rr_)+(2*rr_)/5, (4*hh_+3*kk_+26)/5-rr_],[hh_,kk_,rr_],dict=True)
res=set()
for s_ in sols:
    if s_[rr_]>0:
        AB=2*s_[rr_]; CD=2*sp.sqrt(s_[rr_]**2-s_[hh_]**2); res.add(AB*CD/2)
R[(2,16)]=res
from itertools import product as P_
R[(2,17)]=sum(1 for f_ in P_(range(1,7),repeat=6) if f_[0]>f_[1]>f_[2]>f_[3] and f_[4]<f_[5] and len(set(f_))<6)
ans18=set()
for kv in range(2,400):
    U=set(range(1,kv+1)); A_s={v for v in U if v%2==0}; B_s={v for v in U if kv%v==0}; Cs=U-(A_s|B_s)
    if len(A_s)*len(Cs)==28: ans18.add(sum(Cs))
R[(2,18)]=ans18
from itertools import combinations as C2
best=0;X=range(1,11)
for I in C2(X,2):
    for Dd in C2([v for v in X if v not in I],3):
        if all((p+1)%2==0 and (p+1)//2 in Dd for p in I) and all(q+3<=10 and q+3 not in Dd for q in Dd): best=max(best,sum(Dd))
R[(2,19)]=best

av,bv=9,4
def gfun(v): return abs(math.sqrt(av-v)-bv)+bv if v<=av else -math.sqrt(v-av)+bv+abs(bv)
def hcount(tv):
    sols=set()
    # x<=a: |sqrt(a-x)-b|+b=t -> sqrt(a-x)=b±(t-b)
    for s_ in {bv+(tv-bv), bv-(tv-bv)} if tv>=bv else set():
        if s_>=0: sols.add(round(av-s_**2,9))
    if tv<2*bv: sols.add(round(av+(2*bv-tv)**2,9)) if (2*bv-tv)>0 else None
    return len(sols), sols
assert hcount(bv)[0]==2 and hcount(2*bv)[0]==2 and hcount(5)[0]==3 and hcount(9)[0]==1 and hcount(3)[0]==1
allx=hcount(bv)[1]|hcount(2*bv)[1]; assert min(allx)==-55 and max(allx)==25
for v in hcount(bv)[1]: assert abs(gfun(v)-bv)<1e-9
for v in hcount(2*bv)[1]: assert abs(gfun(v)-2*bv)<1e-9
R[(2,20)]=round(gfun(-91)-gfun(130),9)
bad=0
for sub,M in ((1,M1),(2,M2)):
    for pr in M:
        import re as _re
        exp = sp.sympify(_re.sub(r'([\d}]) sqrt',r'\1*sqrt',pr['choices'][pr['ans']-1]).replace(' over ','/').replace('{','(').replace('}',')')) if pr['choices'] else pr['ans']
        got=R[(sub,pr['no'])]
        if isinstance(got,(set,list)): got=list(got); got=got[0] if len(got)==1 else got
        okk = (not isinstance(got,list)) and sp.simplify(sp.sympify(got)-exp)==0
        print(f"공수{sub} {pr['no']:>2}번  계산={got}  표기정답={exp}  {'OK' if okk else '<<< 불일치'}")
        bad+= (not okk)
print('불일치',bad)
