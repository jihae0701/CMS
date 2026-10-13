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
sol6=sp.solve([x+y-2, x**2-3*x+2*y-10],[x,y],dict=True); R[(1,6)]=max(s_[x]**2+s_[y]**2 for s_ in sol6)

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
zc=(1-sp.I)/(1+sp.I); s9=sp.expand(sp.simplify(sum(n*zc**n for n in range(1,21)))); R[(1,9)]=sp.re(s9)+sp.im(s9)
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

vals19=[]
for ai in range(1,1201):
    av=ai/100
    for ki in range(-300,1201):
        kv=ki/100
        f_=lambda xx:(xx-kv)**2+1
        mn=f_(min(max(kv,0),av)); mx=max(f_(0),f_(av))
        if abs(mn-1)<1e-9 and abs(mx-10)<1e-9: vals19.append(av+kv)
R[(1,19)]=round(max(vals19)*min(vals19),6)
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
R[(2,3)]=sum(sp.solve((3-a)**2+(a-1)**2-10,a))
R[(2,4)]=sp.solve((1+a+5)/3-3,a)[0]+sp.solve((4-2+b)/3-2,b)[0]
# 5: 변환 후 직선이 중심 지남
cx,cy=-1,4; assert sp.expand((x+1)**2+(y-4)**2-9)==x**2+y**2+2*x-8*y+8
R[(2,5)]=sp.solve(-a*(cx-2)-2-cy,a)[0]
R[(2,6)]=sum(av for av in range(-20,21) if all(abs(v-av)<=3 for v in [2+i/100 for i in range(201)]))
from itertools import combinations as _cmb
U_=set(range(1,13)); A_={d for d in U_ if 12%d==0}; B_={d for d in U_ if d%2==0}
R[(2,7)]=sum(1 for r_ in range(13) for X_ in map(set,_cmb(sorted(U_),r_))
             if (A_-B_)|X_==X_ and not X_-(A_|B_) and len(X_-B_)==len(X_&B_))
import numpy as _np
_th=_np.linspace(0,2*_np.pi,1441); _B=_np.stack([6+_np.cos(_th),2+_np.sin(_th)],1); _ps=_np.linspace(0,12,1201)
R[(2,8)]=sp.nsimplify(round(min(_np.min(_np.hypot(_B[:,0]-q_,_B[:,1]-q_))+_np.min(_np.hypot(_ps-8,2)+_np.hypot(_ps-q_,q_))
                                 for q_ in _np.linspace(0,10,2001)),3))

m9=sp.symbols('m9'); P9=sp.solve([x+2*y-4,2*x-y-3],[x,y])
ms9=sp.solve((P9[y]-m9*P9[x])**2-(m9**2+1),m9)          # 원점과의 거리 1 (x=2 는 거리 2)
yi9=[P9[y]-mm*P9[x] for mm in ms9]; R[(2,9)]=abs(yi9[0]-yi9[1])*P9[x]/2
ks=[kv for kv in range(-30,31) if kv!=-6 and abs(max((2*xx/100+kv)/(xx/100-3) for xx in range(0,201))-4)<1e-9]; R[(2,10)]=ks[0] if len(ks)==1 else ks

f11=lambda t: -t+2 if t<=2 else 2*t-4          # 그림의 꺾은선 (0,2)-(2,0)-(4,4)
r11=set()
for k_ in range(0,400001):                        # 구간 [0,4]를 촘촘히 훑어 부호 변화·근 찾기
    t0,t1=k_/100000,(k_+1)/100000
    d0,d1=f11(f11(t0))-f11(t0),f11(f11(t1))-f11(t1) if t1<=4 else None
    if abs(d0)<1e-12: r11.add(round(t0,6))
    elif d1 is not None and d0*d1<0: r11.add(round((t0+t1)/2,4))
R[(2,11)]=sp.nsimplify(round(sum(r11),3))
Ax=sp.solve(sp.Eq(3*sp.sqrt(x),x**2/9),x); Ax=max(Ax); P_=(Ax*4/9,Ax*4/9)
Bx=sp.solve(3*sp.sqrt(x)-P_[1],x)[0]; Cx=[r for r in sp.solve(x**2/9-P_[1],x) if r>0][0]; R[(2,12)]=(Cx-Bx)*(Ax-P_[1])/2
k13,a13=sp.symbols('k13 a13',positive=True)
f13=k13*(x-2)*(x-a13); P13=((2+a13)/2,f13.subs(x,(2+a13)/2))
a13v=[v for v in sp.solve(sp.simplify(-f13.subs(x,0)/a13-P13[1]/(P13[0]-2)),a13) if v>2]; assert len(a13v)==1
m13=(-f13.subs(x,0)/a13).subs(a13,a13v[0]); AP13=sp.sqrt((P13[0]-2)**2+P13[1]**2).subs(a13,a13v[0])
AQ13=sp.Abs(m13*(2-a13v[0]))/sp.sqrt(m13**2+1)
k13v=sp.solve(sp.simplify(AP13*AQ13)-32,k13); R[(2,13)]=[f13.subs({a13:a13v[0],k13:kv}).subs(x,8) for kv in k13v][0]
res14=set()
for c_ in (4,0,-4):                                   # 중심은 x+y=4,0,-4 와 y=f(x)의 교점
    for s_ in sp.solve([b+1-10*a, c_-b**2/(4*a)+4],[a,b],dict=True):
        av_,bv_=float(s_[a]),float(s_[b])
        if av_<=0: continue
        rts=sorted(set(_np.round([z.real for d_ in (4,0,-4) for z in _np.roots([av_,bv_+1,c_-d_]) if abs(z.imag)<1e-12],9)))
        if len(rts)==6 and abs(rts[-1])<1e-9 and abs(sum(rts[:-1])+30)<1e-6: res14.add(round(36*av_+6*bv_+c_,9))
R[(2,14)]=res14
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
R[(2,17)]=sp.nsimplify(round(min(aa*(2*aa/(aa-3))/2 for aa in [3+i/10000 for i in range(1,600000)]),6))
ans18=set()
for av in [i/4 for i in range(-40,41)]:
    for bv in [i/4 for i in range(-40,41)]:
        f_=lambda v: (av+2)*v+bv if v<1 else v*v-2*av*v+av*av+5
        xs=[i/100 for i in range(0,2001)]; ys=[f_(v) for v in xs]
        if abs(ys[0]-2)<1e-12 and all(ys[i]<ys[i+1] for i in range(len(ys)-1)) and abs((av+2)+bv-f_(1))<1e-12:
            ans18.add(f_(4))
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
