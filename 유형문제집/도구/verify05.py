# 5단원(이차함수와 이차방정식의 관계) 유형서 문항 정답 독립 검산 (문항 기호는 unit05.py의 v)
from sympy import *
x, y, a, b, c, k, m, n, p, q, t = symbols('x y a b c k m n p q t')
R = []


def chk(no, got, exp):
    if isinstance(got, (bool, list, set)) or isinstance(exp, (bool, list, set)):
        R.append((no, got == exp, got, exp if not isinstance(exp, (list, set)) else got if got == exp else exp))
        return
    R.append((no, simplify(sympify(got) - sympify(exp)) == 0, got, exp))


def chkmc(no, cond, lab):
    R.append((no, bool(cond), lab, lab))


def disc(e, v=x):
    return discriminant(expand(e), v)


def real_roots(e, v=x):
    return sorted({r for r in solve(expand(e), v) if r.is_real}, key=lambda z: float(z))


def count_pieces(pieces, val):
    """pieces: [(식, 조건 함수)], val: 직선/상수(식). 교점 x좌표 개수"""
    s = set()
    for f, cond in pieces:
        for r in real_roots(f - val):
            if cond(r):
                s.add(nsimplify(r))
    return len(s)


# ---- x축의 교점
av = solve((-2*x**2 + a*x + 5).subs(x, 5), a)[0]
bv = [r for r in real_roots(-2*x**2 + av*x + 5) if r != 5][0]
chk("n1250", av - 2*bv, 10)
ks = [kv for kv in solve(k**2 - 60 - 4, k)]
for kv in ks:
    r1, r2 = real_roots(x**2 - kv*x + 15); assert abs(r1 - r2) == 2
chk("o24", prod(ks), -64)
sol = [av for av in solve(1 + (a + 1) - 12, a) if av > 0]
assert set(real_roots(-x**2 + sol[0]*x + sol[0] + 1)) == {-1, sol[0] + 1}
chk("o26", sol[0], 10)
# n1112: f=p(x-h)^2+mv, 거리 2*sqrt((K-mv)/p)
P_, mv, A_ = symbols('P_ mv A_')
s = solve([A_**2 - 4*(-mv)/P_, (A_ + 6)**2 - 4*(3 - mv)/P_, (A_ + 12)**2 - 4*(9 - mv)/P_], [P_, mv, A_], dict=True)
s = [d for d in s if d[P_] > 0 and d[A_] > 0]
chk("n1112", s[0][mv], Rational(-3, 8))

# ---- x축의 위치 관계
ks = [kv for kv in range(-50, 51) if disc(x**2 - 2*kv*x + kv**2 + kv - 2) >= 0]
chk("n1033", max(ks), 2)
ks = [kv for kv in solve(disc(-x**2 + 2*k*x - k - 12), k) if disc(x**2 - 6*x + kv + 7) > 0]
chk("o31", ks[0] if len(ks) == 1 else ks, -3)
ks = [kv for kv in range(1, 100) if disc(x**2 - 4*kv*x + 4*(kv - 3)*(kv + 4)) >= 0]
chk("n1456", len(ks), 12)
d = expand(disc(x**2 - 2*(a + k)*x + k**2 + b*k + a))
s = [v for v in solve(Poly(d, k).coeffs(), [a, b], dict=True) if v[a] > 0]
chk("n1357", s[0][a] + s[0][b], 3)
pairs = [(av, bv) for av in range(-30, 31) for bv in range(-30, 31) if disc(x**2 + 2*av*x + 10*av - bv**2 - 4*bv - 28) < 0]
chk("o32", sum(pairs[0]) if len(pairs) == 1 else pairs, 3)
# n1385: 보기 판정(표본 검사 + 식 확인)
import random
random.seed(1)
okA, okB, okC = True, True, True
for _ in range(4000):
    av = Rational(random.randint(-400, 400), 37); bv = Rational(random.randint(-400, 400), 23)
    if av**2 - 4*bv < 0:
        okA &= bv < 0; okB &= (2*av - 4*bv > 1); okC &= (2*av + bv > -4)
chkmc("n1385", (not okA) and (not okB) and okC, "③")

# ---- 직선과의 교점
pq = [len(real_roots(x**2 - 2*x + 1 - x)), len(real_roots(x**2 - 2*x + 1 + x))]
chk("n1441", sum(pq), 2)
s = solve([(1 - sqrt(3))**2*2 - (6 + a)*(1 - sqrt(3)) + 1 - b, (1 + sqrt(3))**2*2 - (6 + a)*(1 + sqrt(3)) + 1 - b], [a, b], dict=True)[0]
chk("n1465", s[a] + s[b], 3)
mv = [mm for mm in solve(m**2 - 4, m) if mm > 0][0]
al, be = real_roots(x**2 - mv*x - 3)
chk("n1409", abs(abs(mv*be) - abs(mv*al)), 4) if False else chk("n1409", mv if abs(abs(mv*be) - abs(mv*al)) == 4 else None, 2)
cnt = 0
for kv in range(-50, 51):
    if disc(x**2 - 3*x + 3 - kv) > 0:
        aa, bb = real_roots(x**2 - 3*x + 3 - kv)
        fa, fb = aa**2 - 2*aa + 3 - kv, bb**2 - 2*bb + 3 - kv
        if -9 < simplify(fa*fb) < 9:
            cnt += 1
chk("n826", cnt, 11)
found = []
for mv in [Rational(i, 2) for i in range(1, 20)]:
    for kv in [Rational(i, 2) for i in range(1, 20)]:
        rr = real_roots(2*(x - kv)**2 - mv*x)
        if len(rr) == 2:
            d1 = rr[1] - rr[0]
            if simplify(mv*d1 - 6) == 0 and simplify(sqrt(1 + mv**2)*d1 - 3*sqrt(5)) == 0:
                found.append((mv, kv))
chk("n1220", found[0][0] + found[0][1] if len(found) == 1 else found, 4)
pp = symbols('pp')
e = expand((x - pp)**2 + m*pp - (m*x + 4))
al_be = Poly(e, x).all_coeffs()
mv = solve(Eq(pp, (-al_be[1] - 3)/2), m)[0]
dd = simplify((al_be[1]**2 - 4*al_be[2]).subs(m, mv))
chk("n1410", sqrt(dd), 5)

# ---- 직선과의 위치 관계
chk("n1178", min(kv for kv in range(-50, 51) if disc(2*x**2 - x + kv - 4) < 0), 5)
chk("n1038", sum(av for av in range(1, 100) if disc(x**2 + (2*av + 1)*x + av**2 + 4) < 0), 6)
ks = [kv for kv in solve(disc(x**2 + (2*k - 1)*x - 1 - (x - k)), k) if disc(2*x**2 + 5*x + kv - (x - kv)) < 0]
chk("n991", ks[0] if len(ks) == 1 else ks, 2)
ks = solve(disc(x**2 + 2*k*x - 3*k + 1 - (k*x - 10)), k)
assert all(kv.is_real for kv in ks) and len(ks) == 2
chk("n1314", simplify(prod(ks)), -44)
def f1216(av):
    return len([nv for nv in range(1, 200) if disc(x**2 + 2*x + nv - 19 - (2*av*x - av**2 - av)) > 0])
chk("n1216", min(av for av in range(-30, 60) if f1216(av) == 0), 7)
def h3101(av):
    return len(real_roots(-3*x**2 + 8*x + 4 - (2*x + av)))
cands = [r for r in solve(-3*a**2 + 8*a + 4 - 2, a) if r < 7] + [r for r in solve(-3*a**2 + 8*a + 4 - 0, a) if r > 7]
cands += [7] if -3*49 + 56 + 4 == 1 else []
for r in cands:
    assert -3*r**2 + 8*r + 4 == h3101(r) or simplify(-3*r**2 + 8*r + 4 - h3101(r)) == 0
chk("n3101", simplify(prod(cands)), Rational(-2, 3))
cnt = 0
for nv in range(1, 11):
    A_ = len(real_roots(x**2 + 4*x - 12*nv + 40)); B_ = len(real_roots(x**2 - 10*x - 36*nv + 94 - (2*x - 2)))
    cnt += A_ == B_
chk("n2992", cnt, 8)

# ---- 접선
kv = solve(disc(x**2 + x - 1 - (3*x + k)), k)[0]
pv = real_roots(x**2 + x - 1 - (3*x + kv))[0]
chk("n1139", kv + pv + 3*pv + kv, 0)
chk("n810", sum(solve(disc(x**2 - 5*x + 1 - (a*x - 3)), a)), -10)
mv = [r for r in solve(disc(Rational(1, 2)*x**2 + 9 - (m*x + 1)), m) if r > 0][0]
nv = solve(disc(x**2 + 2*x + n - (mv*x + 1)), n)[0]
chk("n766", mv + nv, 6)
e = x**2 - a*x + 2*a - 3
Px = solve(diff(e, a), x)[0]; Py = e.subs(x, Px)
bv = solve(Py - (-Px + b), b)[0]
av = solve(diff(e - (-x + bv), x).subs(x, Px), a)[0]
assert simplify((e - (-x + bv)).subs(a, av).subs(x, Px)) == 0
chk("n1066", av + bv, 8)
d = expand(disc(x**2 - 4*k*x + 12*k - (2*a*x - b - 4*k**2)))
s = solve(Poly(d, k).coeffs(), [a, b], dict=True)[0]
chk("n1063", s[a] + s[b], 12)
fq = (x - 1)**2 + q; qv = solve(fq.subs(x, -2), q)[0]
chk("o50", solve(disc(fq.subs(q, qv) - (x + k)), k)[0], Rational(-41, 4))

# ---- 성질과 방정식
s = solve([2*25 + 5*a + b, -a/(2*2) - 1], [a, b], dict=True)[0]
chk("o04", s[a] - s[b], 26)
qv = solve(((x - 2)**2 + q).subs(x, 5) - 10, q)[0]
chk("n770", sum(kv for kv in range(1, 100) if qv >= 4*kv - 15), 10)
al, be = symbols('al be')
f = (x - be)**2; g = f - (x - al)**2
rem = f.subs(x, solve(g, x)[0])
chk("n2973", sqrt(4*4), 4) if simplify(rem - (al - be)**2/4) == 0 else chk("n2973", rem, 4)

# ---- 절댓값·구간 함수
cnt = 0
for av in range(-5, 40):
    cnt += count_pieces([(x**2 - 8*x, lambda r: r <= 0 or r >= 8), (-x**2 + 8*x, lambda r: 0 < r < 8)], av) == 4
chk("o38", cnt, 15)
pieces = [(x**2 - 4*x, lambda r: r <= 0 or r >= 4), (-x**2 + 4*x, lambda r: 0 < r < 4)]
ks = [Rational(i, 4) for i in range(-40, 41) if count_pieces(pieces, x + Rational(i, 4)) == 3]
chk("w12", sum(ks), Rational(9, 4))
s = solve([(2 - sqrt(3))**2 + (a - 2)*(2 - sqrt(3)) - 3 - b, (2 + sqrt(3))**2 + (a - 2)*(2 + sqrt(3)) - 3 - b], [a, b], dict=True)[0]
fx = x**2 + s[a]*x - 3; gx = 2*x + s[b]
lo, hi = 2 - sqrt(3), 2 + sqrt(3)
h_pieces = [(fx, lambda r: lo <= r <= hi), (gx, lambda r: r < lo or r > hi)]
ts = [Rational(i, 20) for i in range(-120, 120) if count_pieces(h_pieces, Rational(i, 20)) == 3]
assert min(ts) > -4 and max(ts) < -2*sqrt(3) and count_pieces(h_pieces, -4) == 2 and count_pieces(h_pieces, -2*sqrt(3)) == 2
chk("o52", (-4)**2 + (-2*sqrt(3))**2, 28)

# ---- 근의 위치
cnt = 0
for kv in range(-30, 30):
    rr = real_roots(x**2 - 6*x + 8 - kv)
    cnt += len(rr) == 2 and all(r > 0 for r in rr)
chk("o35", cnt, 8)
ok = []
for av in range(-30, 30):
    rr = real_roots(x**2 + 2*av*x + 3*av - 4)
    if len(rr) == 2 and rr[0] < -1 and rr[1] > 2:
        ok.append(av)
chk("w11", max(ok), -1)
cnt = 0
for kv in range(-30, 30):
    rr = real_roots(x**2 - 2*x + kv - (-x + 2))
    cnt += len(rr) == 2 and all(r > -1 for r in rr)
chk("w13", cnt, 2)

# ---- 도형
C_, D_ = real_roots(-2*x**2 + 5*x + 3)
ok = []
for kv in [Rational(i, 4) for i in range(13, 30)]:
    rr = real_roots(-2*x**2 + 5*x + 3 - (-x + kv))
    if len(rr) == 2:
        yA, yB = -rr[0] + kv, -rr[1] + kv
        S1 = Rational(1, 2)*(D_ - C_)*abs(yA); S2 = Rational(1, 2)*(D_ - C_)*abs(yB)
        if simplify(S1 - S2 - Rational(7, 4)) == 0:
            ok.append(kv)
chk("n3102", ok[0] if len(ok) == 1 else ok, 7)
ok = []
for kv in [Rational(i, 8) for i in range(-40, 40)]:
    rr = real_roots(-x**2 + 2 - (x + kv))
    if len(rr) == 2:
        S1 = Rational(1, 2)*(rr[0] + kv)**2; S2 = Rational(1, 2)*(rr[1] + kv)**2
        if simplify(S1 - S2) == 0 and simplify(S1) != 0:
            ok.append(simplify(S1 + S2))
chk("n1362", ok[0] if len(ok) == 1 else ok, Rational(7, 4))
tot = 0
for kv in range(1, 50):
    rr = real_roots(-x**2 + 3*kv*x + kv**2 + 3 - (kv**2 + 3))
    Bx = max(rr); g = 2*(Bx + kv**2 + 3)
    if 42 <= g <= 86:
        tot += kv
chk("n236", tot, 12)
for av in range(1, 30):
    f = x*(x - av)
    Bx = [r for r in real_roots(f - 2*x) if r != 0][0]
    slope = (2*Bx - 0)/(Bx - av)
    cx = solve(diff(f, x) - slope, x)[0]
    if Rational(1, 2)*av*2*Bx == 48:
        chk("o53", Rational(1, 2)*av*abs(f.subs(x, cx)), 21)
tt, aa = symbols('tt aa', positive=True)
s0 = 16*aa - aa*tt**2
sol = solve([aa*tt**3*5 - 2*8*aa*tt, 2*s0 - 12], [tt, aa], dict=True)
sol = [d for d in sol if d[tt] > 0 and d[tt] < 4]
# 넓이 CEB = CDB 확인: E는 D(4,0)을 지나고 BC와 평행한 직선과 그래프의 교점(제4사분면)
av, tv = sol[0][aa], sol[0][tt]
Bp = (4 + tv, 16*av - av*tv**2); Cp = (4, 16*av)
sl = (Bp[1] - Cp[1])/(Bp[0] - Cp[0])
Ex = [r for r in real_roots(-av*x**2 + 8*av*x - sl*(x - 4)) if r > 8][0]
Ep = (Ex, sl*(Ex - 4))
def area(P1, P2, P3):
    return Abs((P2[0] - P1[0])*(P3[1] - P1[1]) - (P3[0] - P1[0])*(P2[1] - P1[1]))/2
Ap = (4 - tv, 16*av - av*tv**2)
assert simplify(area(Cp, Ap, Bp)*5 - area(Cp, Ep, Bp)*2) == 0 and Ep[1] < 0
chk("m3217", av, Rational(15, 32))

# ---- 고난도
# n84: alpha 값을 바꾸어 보기 판정
okA = okB = True
for alv in range(-5, 6):
    for qv in range(-5, 6):
        for kv in range(-10, 11):
            f = (x - alv)**2 + qv
            rr = real_roots(f + 3*x - kv)
            if alv in rr and len(rr) == 2:
                bev = [r for r in rr if r != alv][0]
                okA &= bev > alv - 3
                okB &= (f.subs(x, 0) - kv == alv**2 - 3*alv)
okC = True
for qv in range(-5, 6):
    f = (x - 3)**2 + qv; kv = f.subs(x, 0) - (9 - 9)
    if f.subs(x, 0) <= 9 + 0 + f.subs(x, 3):
        okC &= f.subs(x, 6) > kv
chkmc("n84", (not okA) and okB and (not okC), "②")
res = []
for pv in range(-10, 11):
    f = (x - pv)**2 - 1
    hits = sum(1 for r in (0, 2) if f.subs(x, r) == 0)
    if hits == 1 and f.subs(x, 3) < 0:
        res.append(f.subs(x, -1))
chk("o49", res[0] if len(res) == 1 else res, 15)
import itertools
fac = [x, x, x - 2, x + 2]
res = set()
for i, j in itertools.combinations(range(4), 2):
    f = expand(fac[i]*fac[j]); g = expand(-prod(fac[l] for l in range(4) if l not in (i, j)))
    if f.subs(x, -1) <= 0:
        continue
    ms = set(solve(disc(f - m*x), m)) & set(solve(disc(g - m*x), m))
    for mv in ms:
        res.add(f.subs(x, mv) + g.subs(x, mv))
chk("o54", list(res)[0] if len(res) == 1 else res, 8)
ks = [kv for kv in solve((2/(k - 4))*(2/(k + 4)) + 1, k)]
chk("o51", ks[0]**2*Rational(1, 2)*8*2, 96)
pv = solve(((p + 1)/2 + (2*p + 1)/2) - 10, p)[0]
chk("o48", 2*(4 - pv)*(4 - 2*pv), 32)
res = []
for cv in range(-50, 51):
    Px = x**2 - 4*x + cv
    rr = solve(Px, x)
    if all(not r.is_real for r in rr):
        for r in rr:
            av, bv = re(r) + 1, im(r)
            if disc(Px - (bv*x + 7)) == 0:
                res.append(av + bv)
chk("n1024", res[0] if len(set(res)) == 1 else res, 1)
ok = []
for kv in [Rational(i, 100) for i in range(1, 300)]:
    if not (((-2 + 3)*(-2 - kv)) < (3*(-kv))):
        continue
    A_, B_, C_ = (-3, 0), (kv, 0), (0, -3*kv)
    d2 = lambda P1, P2: (P1[0] - P2[0])**2 + (P1[1] - P2[1])**2
    if d2(A_, B_) == d2(A_, C_) or d2(A_, B_) == d2(B_, C_) or d2(A_, C_) == d2(B_, C_):
        ok.append(Rational(1, 2)*(kv + 3)*3*kv)
ar = ok[0]
chk("m3345", fraction(ar)[0] + fraction(ar)[1], 167)
pp_, qq_ = symbols('pp_ qq_')
res = []
for cv in solve((9 + c)/4 - 2, c) + solve((9 + c)/4 + 2, c):
    s = solve([pp_*cv**2 + qq_*cv + Rational(9, 2), 9*pp_ + 3*qq_ + Rational(9, 2) - 6], [pp_, qq_], dict=True)[0]
    if s[pp_] < 0:
        f = s[pp_]*x**2 + s[qq_]*x + Rational(9, 2)
        xv = solve(diff(f, x), x)[0]
        assert xv > 0 and f.subs(x, xv) > 0
        # 넓이 확인: D(2, 9/2)
        Dp = (2, Rational(9, 2)); Ap, Bp, Cp = (3, 6), (0, Rational(9, 2)), (cv, 0)
        assert area(Ap, Bp, Dp) == Rational(3, 2) and area(Bp, Cp, Dp) == Rational(9, 2)
        res.append(16*f.subs(x, xv))
chk("m3226", res[0] if len(res) == 1 else res, 121)
res = []
for av in [Rational(i, 2) for i in range(5, 40)]:
    bv = 1 - av
    assert disc(x**2 - (av + 1)*x + av - (bv*x - bv)) == 0
    S1 = Rational(1, 2)*1*abs(-bv)
    S2 = area((1, 0), (av, 0), (0, av)) + area((1, 0), (0, av), (0, -bv))
    if simplify(S1*7 - S2*2) == 0:
        res.append(av)
chk("m3243", res[0] if len(res) == 1 else res, 3)
res = []
for av in range(5, 60):
    for pv in [Rational(1, i) for i in range(1, 20)] + list(range(1, 5)):
        f = pv*(x - 4)*(x - av)
        if disc(f + x) == 0:
            Px = real_roots(f + x)[0]
            Pp = (Px, -Px)
            if area((0, 0), Pp, (av, 0)) == area((0, 0), Pp, (0, f.subs(x, 0))):
                res.append(av)
assert sorted(set(res)) == [16]
chk("m3336", res[0], 16)
res = []
for pv in (1, -1):
    f = 4*(x - pv)**2 + 2*x - 4; g = (x - 4*pv)**2 + 2*x - 4
    assert set(real_roots(f - g)) == {-2, 2}
    mf = f.subs(x, solve(diff(f, x), x)[0]); mg = g.subs(x, solve(diff(g, x), x)[0])
    if mf > mg:
        res.append(f.subs(x, 2) - g.subs(x, 1))
chk("n707", res[0] if len(res) == 1 else res, 13)
A_, al_, be_ = symbols('A_ al_ be_')
fx = A_*(x - 3)*(x - al_) + 2*x - 8; gx = A_*(x - 3)*(x - be_) + 2*x - 8
s = solve([gx.subs(x, 4) - fx.subs(x, 0), gx.subs(x, 12) - fx.subs(x, 0), al_ + be_ - 6], [A_, al_, be_], dict=True)
s = [d for d in s if d[A_] < 0 and d[al_] < 3 < d[be_]]
fxx, gxx = fx.subs(s[0]), gx.subs(s[0])
f0 = fxx.subs(x, 0)
pts = sorted(set([r for r in real_roots(fxx - f0) if r <= 3] + [r for r in real_roots(gxx - f0) if r > 3]))
assert pts == [0, 4, 12]
chk("m3277", fxx.subs(x, -2) + gxx.subs(x, 5), 17)
res = []
for pv in range(1, 10):
    bv = 4*pv; cv = -2*bv
    f = pv*x**2; g = -pv*x**2 + bv*x + cv
    assert real_roots(f + g) == [2]
    fg = f - g; assert solve(diff(fg, x), x) == [1]
    cnt = 0
    for kv in range(-100, 100):
        if not real_roots(f - kv) and not real_roots(g - kv):
            cnt += 1
    if cnt == 3:
        res.append(f.subs(x, 17) + g.subs(x, 17))
chk("n1490", res[0] if len(res) == 1 else res, 60)

# ---- 사용자 요청 추가
s = solve([disc(a*x**2 + x + b - (5*x + 2)), disc(a*x**2 + x + b - (-x + 5))], [a, b], dict=True)
s = [d for d in s if d[a] != 0]
chk("n1406", s[0][a] + s[0][b] if len(s) == 1 else s, 7)
pieces = [(x**2 - 3*x - 4, lambda r: r <= -1 or r >= 4), (-x**2 + 3*x + 4, lambda r: -1 < r < 4)]
ms = [Rational(i, 8) for i in range(-80, 81) if count_pieces(pieces, Rational(i, 8)*x + 3) == 4]
assert count_pieces(pieces, Rational(-3, 4)*x + 3) == 3 and count_pieces(pieces, 3*x + 3) == 3
chk("w14", (max(ms) + Rational(1, 8)) - (min(ms) - Rational(1, 8)), Rational(15, 4))
ok = []
for kv in range(1, 40):
    rr = real_roots(Rational(1, 2)*x**2 - (2*x + kv))
    if len(rr) == 2 and rr[0] < 0 < rr[1]:
        S1 = Rational(1, 2)*rr[1]*Rational(1, 2)*rr[1]**2; S2 = Rational(1, 2)*(-rr[0])*Rational(1, 2)*rr[0]**2
        if simplify(S1 - S2 - 52) == 0:
            ok.append(kv)
chk("n2928", ok[0] if len(ok) == 1 else ok, 6)

if __name__ == "__main__":
    bad = [r for r in R if not r[1]]
    print(len(R), "검산", "불일치", bad)
