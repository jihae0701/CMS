# 7단원(여러 가지 방정식) 유형서 문항 정답 독립 검산 (문항 기호는 unit07.py의 v)
# 방정식은 근을 직접 구해(수치 근은 50자리) 조건을 확인하고, 매개변수는 정수·유리수 후보를 모두 대 본다.
from sympy import *
from itertools import product as iprod
x, y, t = symbols('x y t')
a, b, c, k, m, n = symbols('a b c k m n', real=True)
R = []


def chk(no, got, exp):
    R.append((no, simplify(sympify(got) - sympify(exp)) == 0, got, exp))


def chkmc(no, cond, lab):
    R.append((no, bool(cond), lab, lab))


def rts(e, v=x):
    """중근 포함 모든 근(정확값이 어려우면 CRootOf)"""
    return Poly(expand(e), v).all_roots()


def Z(e):
    return abs(complex(N(e, 40))) < 1e-25


def nreal(e, v=x):
    """서로 다른 실근의 개수"""
    return len({r for r in rts(e, v) if r.is_real})


def val(e):
    v = N(e, 40)
    assert abs(complex(N(im(v), 40))) < 1e-25, e
    return nsimplify(re(v), tolerance=1e-20, rational=False)


# ---- 고차방정식의 풀이
chk("o04", sum({r for r in rts(x**4 - 5*x**3 + 20*x - 16) if r.is_real and r > 0}), 7)
chk("n918", sum({r for r in rts(x**4 - 3*x**3 + 2*x**2 + 2*x - 4) if r.is_real}), 1)
av = solve((x**3 + a*x**2 + x + 10).subs(x, -2), a)[0]
rr = rts(x**3 + av*x**2 + x + 10); rr.remove(-2)
chk("n917", val(sum(rr)), 2)
# ---- 치환
chk("n329", val(sum({r for r in rts((x**2 - 3*x)*(x**2 - 3*x - 6) - 27) if r.is_real})), 3)
ks = {val(r**2 + 5*r) for r in rts((x**2 + 4*x + 3)*(x**2 + 6*x + 8) - 120) if not r.is_real}
assert len(ks) == 1; chk("n229", ks.pop(), -16)
ks = {val(r**4 - 12*r**3 + 36*r**2) for r in rts((x**2 - 6*x + 2)*(x**2 - 6*x + 4) - 99) if not r.is_real}
assert len(ks) == 1; chk("n2927", ks.pop(), 169)
chk("n1468", val(sum({r for r in rts(x**4 - 2*x**3 - x**2 + 2*x + 1) if r.is_real})), 1)
pos = sorted({r for r in rts(x**4 - 7*x**2 + 9) if r.is_real and r > 0}, key=float); assert len(pos) == 2
chk("w1", val(sum(pos)**2), 13)
# ---- 근과 계수
im2 = [r for r in rts(x**3 - 5*x**2 + 11*x - 7) if not r.is_real]
chk("n115", val((im2[0] - 2)*(im2[1] - 2)), 3)
r3 = rts(x**3 + x**2 + x - 3)
chk("n543", val((r3[0]-r3[1])**2 + (r3[1]-r3[2])**2 + (r3[2]-r3[0])**2 + 3*r3[0]*r3[1]*r3[2]), 5)
f = x**3 + k*x**2 + (k + 2)*x - 2*k - 3
kv = solve(-f.subs(x, 4) + 15, k)[0]            # (α-4)(β-4)(γ-4) = -f(4)
r3 = rts(f.subs(k, kv)); assert Z(prod([r - 4 for r in r3]) + 15)
chk("n726", val(sum(1/r for r in r3)), Rational(1, 3))
r3 = rts(x**3 - x + 6)
pr = [r3[0]*r3[1], r3[1]*r3[2], r3[2]*r3[0]]
cub = expand((x - pr[0])*(x - pr[1])*(x - pr[2]))
co = [val(cc) for cc in Poly(cub, x).all_coeffs()]
chk("o26", co[1] + co[2] + co[3], -35)
# ---- 켤레근
s = solve([re(expand((x**3 - k*x**2 + 8*k*x - 32).subs(x, 4*I))), im(expand((x**3 - k*x**2 + 8*k*x - 32).subs(x, 4*I)))], k)
kv = s[k] if isinstance(s, dict) else s[0][0]
al = [r for r in rts(x**3 - kv*x**2 + 8*kv*x - 32) if r.is_real][0]
chk("o24", kv + al, 4)
e = expand((x**3 + a*x**2 - b*x - 10).subs(x, 1 - 2*I))
s = solve([re(e), im(e)], [a, b], dict=True)[0]
chk("n277", -s[b]/s[a], Rational(-9, 4))
e = expand((x**4 + x**3 + k*x**2 + 9*x - 18).subs(x, 3*I))
kv = solve([re(e), im(e)], k)
kv = kv[k] if isinstance(kv, dict) else kv[0]
rr = [r for r in rts(x**4 + x**3 + kv*x**2 + 9*x - 18) if r.is_real]
chk("n902", sum(rr) + kv, 6)
# n1342: 유리수 계수 → (x²-4x+1)(x²+c), c 여러 값에서 ㄱ·ㄴ·ㄷ 확인
ok = True
for cv in [Rational(i, 3) for i in range(-30, 31) if i]:
    P4 = expand((x**2 - 4*x + 1)*(x**2 + cv))
    co = Poly(P4, x).all_coeffs()
    av_, bv_ = co[2], co[3]
    ok &= (av_ - bv_ == 5*cv + 1)
    rr = rts(P4)
    if cv < 0:
        ok &= (len({r for r in rr if r.is_real}) == 4)
    else:
        ok &= (len({r for r in rr if r.is_real}) == 2 and len({r for r in rr if not r.is_real}) == 2)
chkmc("n1342", ok, "⑤")
# ---- 고차방정식의 근의 조건
cnt = [av for av in range(1, 100) if nreal(x**3 + 5*x**2 + (14 - av)*x + av - 20) == 1
       and len({r for r in rts(x**3 + 5*x**2 + (14 - av)*x + av - 20) if not r.is_real}) == 2]
chk("n140", len(cnt), 10)
cnt = [av for av in range(1, 100) if nreal(x**3 - (av + 5)*x**2 + 7*av*x - 2*av**2) == 3]
chk("n234", len(cnt), 2)
cnt = [mv for mv in range(-50, 51) if nreal(x**3 - 2*(mv + 1)*x**2 + 4*(mv + 1)*x - 8) == 1]
chk("m3333", len(cnt), 4)
ks = []
for kv in sorted({Rational(i, 4) for i in range(-80, 81)}):
    if nreal(x**3 - 2*(kv - 1)*x**2 + (2*kv - 5)*x + 4*kv - 6) == 2:
        ks.append(kv)
chk("n666", sum(ks), Rational(7, 2))
sols = []
for av_, bv_, cv_ in iprod(range(-6, 7), repeat=3):
    rr = rts(x**4 + av_*x**3 + bv_*x**2 + cv_*x + 1)
    if {r for r in rr if r.is_real} == {-1, 1}:
        sols.append((av_, bv_, cv_))
assert sols == [(0, -2, 0)], sols
chk("d2", sum(sols[0]), -2)
# ---- 복이차
s = []
for av_ in [Rational(i, 2) for i in range(-40, 41)]:
    rr = sorted({r for r in rts(x**4 - (2*av_ - 1)*x**2 + 16) if r.is_real}, key=float)
    if len(rr) == 4 and Z(rr[0]**2 + rr[1]**2 - 17):
        s.append(av_)
assert s == [9]; chk("n144", s[0], 9)
cnt = [kv for kv in range(1, 100) if all(r.is_real for r in rts(x**4 - 10*x**2 + 2*kv - 15))]
chk("o28", len(cnt), 13)
s = set()
for av_ in [Rational(i, 4) for i in range(-60, 61)]:
    rr = rts(x**4 - (2*av_ + 3)*x**2 + av_**2 + 3*av_)
    if any(r.is_real for r in rr) and any(not r.is_real for r in rr) and any(r.is_integer for r in rr):
        s.add(av_)
chk("n935", sum(s), -5)
# ---- ω
w = [r for r in rts(x**3 - 1) if not r.is_real][0]; wb = conjugate(w)
chk("n274", val((1/w - 2)*(1/wb - 2)), 7)
chk("o25", val((2*w**3 + w)*(2*wb**3 + wb)), 3)
w = [r for r in rts(x**3 + 1) if not r.is_real][0]; wb = conjugate(w)
A_ = val((1 - w)/w**2 + w**2/(1 - w)); B_ = val(w + 1/w + wb + 1/wb)
assert A_ == -2 and B_ == 2
chk("d3", A_*B_, -4)
w = [r for r in rts(x**3 - 1) if not r.is_real][0]
base = (w**3 + 2*w**2 + w + 1)/(w**4 + w**3 - w)
cnt = 0
for nv in range(1, 56):
    z = N(base**nv, 40)
    if abs(im(z)) < 1e-25 and re(z) < 0:
        cnt += 1
chk("n788", cnt, 9)
w = [r for r in rts(x**3 - 5*x**2 + 9*x - 5) if not r.is_real][0]
sol = [nv for nv in range(1, 30) if Z(((w**2 - 5)/w)**(2*nv) - 256)]
assert len(sol) == 1; chk("n187", sol[0], 4)
w = [r for r in rts(x**3 + 1) if not r.is_real][0]
ns = set()
for av_ in range(1, 12):
    for bv_ in range(1, 12):
        nv = val(a*b - (a*w + b)*(a*w**2 - b)).subs({a: av_, b: bv_}) if False else val(av_*bv_ - (av_*w + bv_)*(av_*w**2 - bv_))
        if nv.is_integer and 1 <= nv <= 100:
            ns.add(nv)
chk("n122", len(ns), 9)
w = [r for r in rts(x**3 - 1) if not r.is_real][0]; wb = conjugate(w)
g1 = Z((1 + w)**2 - w); g2 = Z((1 + w**2)**10 - 1/wb)
g3 = all(Z((w*(wb + 1))**(3*nv) - (-1)**nv) for nv in range(1, 12))
chkmc("n973", g1 and g2 and g3, "⑤")
# ---- 연립이차방정식의 풀이
S_ = solve([2*x - y - 1, 3*x**2 - 6*x - y**2 + 16], [x, y], dict=True)
S_ = [d for d in S_ if d[x] > 0]; assert len(S_) == 1
chk("n721", S_[0][x] + S_[0][y], 8)
S_ = solve([x**2 - 2*x*y - 3*y**2, x**2 - x*y + 2*y**2 - 16], [x, y], dict=True)
vals = [d[x] - d[y] for d in S_]
chk("n37", max(vals)*min(vals), -16)
S_ = solve([3*x**2 - 2*x*y - y**2 - 8, x**2 + 2*x*y - 3*y**2 - 4], [x, y], dict=True)
pv = {simplify(d[x]*d[y]) for d in S_}
assert len(pv) == 1; chk("n876", pv.pop(), Rational(5, 8))
S_ = solve([y**2 + (x - 3)*y - x + 2, x**2 - 3*x + y + 1], [x, y], dict=True)
chk("n701", max(d[x]**2 + d[y]**2 for d in S_), 10)
# ---- 연립이차방정식의 해의 조건
def nsol(eqs, cond=None):
    S_ = solve(eqs, [x, y], dict=True)
    return [d for d in S_ if d[x].is_real and d[y].is_real]
kk = [kv for kv in range(-60, 10) if len(nsol([2*x + y - 8, x**2 - 3*y - kv])) == 1]
assert kk == [-33]; d = nsol([2*x + y - 8, x**2 - 3*y + 33])[0]
chk("n971", d[x] + d[y] - 33, -22)
kk = [kv for kv in range(-10, 11) if len(nsol([x - y - kv, x**2 + x*y + y**2 - 4])) == 1]
chk("n868", prod(kk), -16)
kk = [kv for kv in range(0, 40) if len(nsol([x - y - 4, x**2 - x*y + y**2 - kv])) == 1]
assert kk == [12]; d = nsol([x - y - 4, x**2 - x*y + y**2 - 12])[0]
chk("o31", 12*(d[x]**2 + d[y]**2), 96)
good = [kv for kv in [sqrt(Rational(i, 25)) for i in range(0, 400)] if nsol([x - kv*y - 1, x**2 + 4*x + 4*y**2 - 1])]
chk("n163", min(5*g**2 for g in good), 16)
aa = [av_ for av_ in range(-10, 11) if nsol([x + y - 2*av_, (x + 1)*(y + 1) - 5 - av_**2])]
chk("d1", min(aa), 2)
S_ = solve([x + y - 1, 2*x**2 - y**2 - 4*x - 2], [x, y], dict=True)
res = []
for d in S_:
    av_, bv_ = d[x]**2 + d[y]**2, 3*d[x] + d[y]
    if av_ > 0 and bv_ > 0:
        res.append(av_*bv_ - d[x]*d[y])
assert len(res) == 1; chk("o30", res[0], 97)
# ---- 공통근
ks = [kv for kv in range(-20, 21) if set(rts(x**2 - 3*x + kv)) & set(rts(x**2 + kv*x - 3))]
chk("w2", sum(ks), -1)
e = expand((x**3 - a*x**2 - 7*x - b).subs(x, 1 - 2*I))
s = solve([re(e), im(e)], [a, b], dict=True)[0]
rr = [r for r in rts(x**3 - s[a]*x**2 - 7*x - s[b]) if r.is_real]
kv = solve((x**2 + k*x + 5).subs(x, rr[0]), k)[0]
chk("n840", s[a] + s[b] + 6*kv, 7)
# ---- 부정방정식
cnt = [(xv, yv) for xv in range(-50, 51) for yv in range(-50, 51) if xv*yv - 2*xv - 3*yv == 1]
chk("w5", len(cnt), 4)
pairs = [(xv, yv) for xv in range(1, 100) for yv in range(1, 100) if xv**2 - yv**2 == 24]
chk("w9", sum(xv*yv for xv, yv in pairs), 40)
G_ = x**2 + 2*x*y + 2*y**2 - 4*y + 4
S_ = solve([diff(G_, x), diff(G_, y)], [x, y], dict=True)[0]
assert G_.subs(S_) == 0 and hessian(G_, (x, y)).det() > 0           # 최솟값 0인 점이 유일한 실수 해
chk("w6", S_[x]*S_[y], -4)
F_ = x**2 - 4*x*y + 5*y**2 + 2*x - 8*y + 5
S_ = solve([diff(F_, x), diff(F_, y)], [x, y], dict=True)[0]
assert F_.subs(S_) == 0 and hessian(F_, (x, y)).det() > 0
chk("w7", S_[x]*S_[y], 6)
# ---- 활용
S_ = [d for d in solve([x**2 + y**2 - 52, x*y - 24], [x, y], dict=True) if d[x] > 0 and d[y] > 0]
chk("o32", abs(S_[0][x] - S_[0][y]), 2)
sv = [r for r in rts(x**2*(x + 3) - 112) if r.is_real and r > 0]
assert sv == [4]; chk("w8", 2*16 + 4*4*7, 144)
S_ = solve([3*a + 6*b - 42, sqrt(3)/4*a**2 + 3*sqrt(3)/2*b**2 - 33*sqrt(3)], [a, b], dict=True)
S_ = [d for d in S_ if d[a] > 0 and d[b] > 0 and not (3*d[a]).is_integer]
assert len(S_) == 1; chk("n577", S_[0][a] + S_[0][b], Rational(62, 5))
# ---- 고난도
ks = []
for kv in [Rational(i, 8) for i in range(-80, 81)]:
    rr = sorted({r for r in rts(x**3 - 6*x**2 + (kv + 8)*x - 2*kv) if r.is_real}, key=float)
    if len(rr) == 3 and Z(2*rr[0] + rr[1] - 2*rr[2]):
        ks.append(kv)
assert ks == [Rational(15, 4)]; chk("m3275", ks[0], Rational(15, 4))
f = x**3 + k*x**2 + (k + 4)*x - 6*k - 1
kv = solve(f.subs(x, 1) - 8, k)[0]
chk("o49", val(sum(r**2 for r in rts(f.subs(k, kv)))), -5)
ks = [kv for kv in range(-30, 31) if nreal((x**2 + kv*x)**2 + kv*(x**2 + kv*x) + kv - 1) == 2]
chk("n821", len(ks), 3)
res = set()
for av_ in [Rational(i, 2) for i in range(-40, 0)]:
    fx = x**3 + av_*x**2 + x - av_ + 2
    zs = [r for r in rts(fx) if not r.is_real]
    if zs and Z((zs[0] - conjugate(zs[0]))**2 + 4):
        res.add(val(sum({(r + 4)/3 for r in rts(fx)})))
assert len(res) == 1; chk("o50", res.pop(), 5)
ks = [kv for kv in range(1, 40) if nreal((2*x**2 + kv*x)**2 + 10*(2*x**2 + kv*x) + 16) == 2]
chk("m3193", sum(ks), 18)
res = set()
for av_ in [Rational(i, 2) for i in range(-20, 21)]:
    rr = rts(x**4 - (2*av_**2 - 2*av_ - 3)*x**2 + av_**4 - 2*av_**3 - 3*av_**2)
    re_ = sorted({r for r in rr if r.is_real}, key=float); im_ = [r for r in rr if not r.is_real]
    if len(re_) == 2 and len(set(im_)) == 2 and len(rr) == 4 and Z(re_[0]**3*re_[1] + re_[0]*re_[1]**3 + 32):
        res.add(val(av_ + im_[0]*im_[1]))
assert len(res) == 1; chk("o29", res.pop(), 5)
res = set()
for kv in [Rational(i, 2) for i in range(-30, 31)]:
    rr = rts(x**3 - kv*x**2 + 2*kv*x - 8)
    re_ = [r for r in rr if r.is_real]; im_ = [r for r in rr if not r.is_real]
    if len(re_) == 1 and len(im_) == 2 and Z(im_[0]**2 + im_[1]**2 - 11 + 2*kv):
        res.add(kv + re_[0])
assert len(res) == 1; chk("o45", res.pop(), 7)
res = set()
for av_ in [sqrt(Rational(i, 3)) for i in range(1, 40)] + [-sqrt(Rational(i, 3)) for i in range(1, 40)]:
    bv_ = 2*av_**2
    rr = rts(x**3 + av_*x**2 + bv_*x - 2*av_*bv_) if False else None
    rr = [av_, -av_ + sqrt(3)*av_*I, -av_ - sqrt(3)*av_*I]
    assert all(Z((x**3 + av_*x**2 + bv_*x - 2*av_*bv_).subs(x, r)) for r in rr)
    for al_, be_, ga_ in [(rr[0], rr[1], rr[2]), (rr[0], rr[2], rr[1]), (rr[1], rr[0], rr[2]), (rr[2], rr[0], rr[1]), (rr[1], rr[2], rr[0]), (rr[2], rr[1], rr[0])]:
        if Z((2*al_ + be_ - ga_)**2 + 36):
            res.add(val(al_**2 + be_**2 + ga_**2))
assert len(res) == 1; chk("n173", res.pop(), -4)
best = None
for av_ in [Rational(i, 10) for i in range(-50, 81)]:
    rr = rts(x**4 - (2*av_ + 1)*x**3 + 6*(av_ + 2)*x**2 - 4*(av_ + 3)*x)
    re_ = sorted({r for r in rr if r.is_real}, key=float); im_ = list({r for r in rr if not r.is_real})
    if len(re_) == 2 and len(im_) == 2:
        v_ = val(re_[0]**2 + re_[1]**2 - im_[0]**2 - im_[1]**2)
        best = v_ if best is None or v_ > best else best
chk("o52", best, 29)
dd = symbols('dd', positive=True)
sol_d = [s_ for s_ in solve(3*sqrt(dd - 9) + sqrt(2)*sqrt(dd - 2) - 7, dd) if s_ > 9]
assert sol_d == [10]; chk("o53", 3*sol_d[0] - 11, 19)
res = set()
for pv_, qv_ in iprod(range(-6, 7), range(1, 7)):
    for one_pos in (0, 1):
        r_ = [1, pv_ + qv_*I, pv_ - qv_*I] if one_pos == 0 else [pv_ + qv_*I, 1, pv_ - qv_*I]
        if Z((2*r_[0] + 2*r_[1] - r_[2])**2 + 81):
            res.add(val((4 + r_[0])*(4 + r_[1])*(4 + r_[2])))
assert len(res) == 1; chk("m3256", res.pop(), 65)
cnt = 0
for av_ in range(-20, 21):
    if av_ == 0:
        continue
    for bv_ in range(-20, 21):
        rr = rts(av_*x**3 - bv_*x**2 + (5*av_ + bv_)*x - 6*av_)
        if len(set(rr)) == 3 and all(r.is_integer for r in rr):
            cnt += 1
chk("n475", cnt, 22)
ns = []
for nv in range(1, 41):
    rr = rts(x**4 - 2*(2*nv + 1)*x**2 + (2*nv - 1)**2)
    if len(set(rr)) == 4 and all(r.is_integer for r in rr):
        ns.append(nv)
chk("n863", sum(ns), 60)

# ---- 추가 문항
ks = [kv for kv in range(-30, 6) if len(set(rts((x + 1)*(x - kv)*(x**2 + 4*x - kv)))) == 4
      and all(r.is_real for r in rts((x + 1)*(x - kv)*(x**2 + 4*x - kv)))]
chk("n14", len(ks), 6)
ks = []
for kv in range(-60, 61):
    S_ = solve([3*x**2 + kv*x*y - 3*y**2 + 3, 6*x**2 - 5*x*y + 2*y**2 - 1], [x, y], dict=True)
    S_ = [d for d in S_ if d[x].is_real and d[y].is_real]
    if S_ and all((d[y]/d[x]).is_integer for d in S_):
        ks.append(kv)
chk("n823", max(ks) + min(ks), 30)
S_ = solve([x**2 - x*y - 2*y**2 + 2*x + 5*y - 3, x**2 + x*y + y**2 - 1], [x, y], dict=True)
assert len(S_) == 4
chk("n846", sum(d[x]*d[y] for d in S_), Rational(-89, 49))
sols = [(xv, yv) for xv in range(-30, 31) for yv in range(-30, 31) if xv**2 - xv*yv + yv**2 == 3]
chk("w10", max(xv + yv for xv, yv in sols), 3)
S_ = [d for d in solve([4*a + 4*b - 120, a**2 - b**2 - 180], [a, b], dict=True) if d[a] > d[b] > 0]
chk("y44", S_[0][a], 18)
S_ = [d for d in solve([x**2 + y**2 - 208, (x + 4)*(y + 4) - x*y - 96], [x, y], dict=True) if d[x] > 0 and d[y] > 0]
assert {abs(d[x] - d[y]) for d in S_} == {4}; chk("y45", 4, 4)
S_ = [d for d in solve([8 - b + a - 10, a**2 - 4*b**2/2 - 7], [a, b], dict=True) if 2 < d[a] < 6 and 0 < d[b] < 4]
chk("n622", sum(d[a] for d in S_), 8)

chk("w11", val(sum({r for r in rts(x**4 - 5*x**3 + 8*x**2 - 5*x + 1) if r.is_real})), 4)

if __name__ == "__main__":
    bad = [r for r in R if not r[1]]
    print(len(R), "검산", "불일치", bad)
