# 6단원(이차함수의 최대, 최소) 유형서 문항 정답 독립 검산 (문항 기호는 unit06.py의 v)
from sympy import *
x, y, a, b, c, k, m, p, q, t = symbols('x y a b c k m p q t', real=True)
R = []


def chk(no, got, exp):
    R.append((no, simplify(sympify(got) - sympify(exp)) == 0, got, exp))


def chkmc(no, cond, lab):
    R.append((no, bool(cond), lab, lab))


def mm(e, lo, hi, v=x):
    """[lo, hi]에서 다항식 e의 (최댓값, 최솟값): 양 끝과 범위 안의 극점"""
    e = expand(e)
    cand = [lo, hi] + [r for r in solve(diff(e, v), v) if r.is_real and lo <= r <= hi]
    vals = [simplify(e.subs(v, r)) for r in cand]
    return max(vals, key=lambda z: float(z)), min(vals, key=lambda z: float(z))


def mmf(f, lo, hi, n=4001):
    """수치 확인용 (함수 f, 실수 범위)"""
    vs = [f(lo + (hi - lo) * i / (n - 1)) for i in range(n)]
    return max(vs), min(vs)


def real_roots(e, v=x):
    return sorted({r for r in solve(expand(e), v) if r.is_real}, key=lambda z: float(z))


# ---- 이차함수의 최댓값과 최솟값
f = a*(x + 1)*(x - 5)
av = [s for s in solve(f.subs(x, 2) - 18, a) if s < 0][0]
chk("w1", f.subs({a: av, x: 3}), 16)
f = x**2 - 2*a*x + b
av = solve(diff(f, x).subs(x, 2), a)[0]
bv = solve(f.subs({a: av, x: 2}) + 5, b)[0]
r1, r2 = solve(f.subs({a: av, b: bv}), x)
chk("w4", expand(r1**2 + r2**2), 18)
e = 2*x**2 - 4*a*x + a**2 + 6*a + 1
fa = simplify(e.subs(x, solve(diff(e, x), x)[0]))
M_, m_ = mm(fa, -1, 4, a)
chk("n1174", M_ + m_, 4)
f = x**2 - 2*(a + 2)*x + a**2 + 4*a
rs = solve(f, x)
S = Rational(1, 2)*abs(rs[1] - rs[0])*f.subs(x, 0)
S = simplify(S)
M_, m_ = mm(S, 1, 4, a)
chk("n1104", M_ + m_, 74)

# ---- 제한된 범위에서의 최대·최소
for av in solve(Eq(1, 1), a) or [None]:
    pass
sol = None
for cand in solve([(a*x**2 - 6*a*x - 2*b).subs(x, 5) - 4, (a*x**2 - 6*a*x - 2*b).subs(x, 4) - 1], [a, b], dict=True):
    e = (a*x**2 - 6*a*x - 2*b).subs(cand)
    if cand[a] > 0 and mm(e, 4, 5) == (4, 1):
        sol = cand
chk("n1276", sol[a] - sol[b], Rational(11, 2))
f = (x - 1)**2 + q
qv = [s for s in solve(mm(f.subs(q, 0), -2, 3)[0] + q - 15, q)][0]
chk("o39", mm(f.subs(q, qv), -2, 3)[1], 6)
h = (-x**2 + 3*x + 5) - (2*x - 1)
al, be = real_roots(h)
M_, m_ = mm(h, al, be)
pv = [r for r in solve(diff(h, x), x)][0]
assert h.subs(x, pv) == M_
chk("o41", pv + M_, Rational(27, 4))
h = a*(x - 1)*(x - 9)
av = [s for s in solve(mm(h.subs(a, -1), 0, 6)[0]*(-a) - 8, a) if s < 0][0]
assert mm(h.subs(a, av), 0, 6)[0] == 8
chk("n1498", mm(h.subs(a, av), 0, 6)[1], Rational(-9, 2))
# w5: 임의의 x1, x2 -> min f >= max g
amin = None
for av in [Rational(i, 4) for i in range(0, 120)]:
    fmin = mm(x**2 - 6*x + av, 0, 2)[1]
    gmax = mm(-x**2 + 2*x + 5, -2, 2)[0]
    if fmin >= gmax:
        amin = av
        break
chk("w5", amin, 14)

# ---- 조건을 이용한 이차함수의 최대·최소
res = []
for s in solve([(x**2 + a*x + b).subs(x, -2) - (x**2 + a*x + b).subs(x, 4)], [a], dict=True):
    f = (x**2 + a*x + b).subs(s)
    M_, m_ = mm(f.subs(b, 0), 0, 3)
    bv = solve(M_ + m_ + 2*b - 20, b)[0]
    res.append(f.subs({b: bv, x: 1}))
chk("o55", res[0], 8)
vals = set()
for av in range(-20, 21):
    if av == 0:
        continue
    f = av*(x + 3)*(x - 5)
    if mm(f, 1, 6) == (16, -9):
        vals.add(f.subs(x, 4))
chk("n989", vals.pop() if len(vals) == 1 else vals, 7)
f = a*(x + 1)*(x - 3)
av = [s for s in solve(mm(f.subs(a, -1), -4, 4)[1]*(-a) + 63, a) if s < 0][0]
assert mm(f.subs(a, av), -4, 4)[1] == -63
chk("o46", f.subs({a: av, x: 2}), 9)
sols = []
for s in solve([m*(2 + a)*(2 - a - 4) + 18, m*a*(-a - 4) + 10], [a, m], dict=True):
    if s[a] > 0 and s[m] > 0:
        f = m*(x + a)*(x - a - 4)
        if mm(f.subs(s), 0, 3) == (-10, -18):
            sols.append(s[a] + s[m])
chk("n3107", sols[0] if len(sols) == 1 else sols, 3)
mins = set()
for kv in [Rational(-i, 100) for i in range(1, 2000)]:
    rr = real_roots(-x**2 + 4*x + kv + 8 - (3*x + 6))
    if len(rr) == 2:
        M_, m_ = mm(-x**2 + 4*x + kv + 8, rr[0], rr[1])
        if M_ == 9:
            mins.add(m_)
chk("n1488", mins.pop() if len(mins) == 1 else mins, 6)
res = []
for av in solve(Eq(1, 1), a) or []:
    pass
f = a*(x + 1)*(x - 4) - a*x - 3
for av in [Rational(-i, 4) for i in range(1, 80)]:
    M_, m_ = mm(f.subs(a, av), -1, 4)
    if M_ + m_ == 8:
        res.append(f.subs({a: av, x: 1}))
chk("o57", res[0] if len(res) == 1 else res, 11)
F = Function('F')
c0, c1, c2 = symbols('c0 c1 c2')
fq = c2*x**2 + c1*x + c0
s = solve(Poly(expand(2*fq + fq.subs(x, 4 - x) - 3*(x - 2)**2), x).all_coeffs(), [c0, c1, c2], dict=True)[0]
f = fq.subs(s)
g1 = discriminant(f, x) < 0
g2 = mm(f, 3, 4)[1] == 1
g3 = len([kv for kv in range(1, 50) if discriminant(expand(f - (2*kv*x - kv**2 - 12)), x) < 0]) == 2
chkmc("n1126", (not g1) and g2 and g3, "④")

# ---- 축에 문자가 있을 때의 최대·최소
res = set()
for av in [Rational(i, 4) for i in range(-40, 41)]:
    M_, m_ = mm(x**2 - 2*av*x - 4*av + 3, -2, 2)
    if m_ == 6:
        res.add(av + M_)
chk("o42", res.pop() if len(res) == 1 else res, 14)
pt = solve([Poly(expand(x**2 + 2*a*x - 4*a - y), a).coeffs()[0]], [x], dict=True)[0]
xv = pt[x]; yv = (x**2).subs(x, xv)
res = set()
for av in [Rational(i, 4) for i in range(-40, 41)]:
    M_, m_ = mm(x**2 + 2*av*x - 4*av, xv, yv)
    if m_ == 3:
        res.add(M_)
chk("n3000", res.pop() if len(res) == 1 else res, 4)
# n21: 구간별로 a를 풀어 확인
sol = []
f = -x**2 + 2*a*x + a
for lo_, hi_, Mexp, mexp in ((-oo, 0, f.subs(x, 0), f.subs(x, 2)), (0, 1, a**2 + a, f.subs(x, 2)),
                             (1, 2, a**2 + a, f.subs(x, 0)), (2, oo, f.subs(x, 2), f.subs(x, 0))):
    for av in solve(Mexp - mexp - 2, a):
        if av.is_real and lo_ <= av <= hi_:
            M_, m_ = mm(f.subs(a, av), 0, 2)
            if simplify(M_ - m_ - 2) == 0:
                sol.append(av)
chk("n21", sum(set(sol)), 2)
ok = [av for av in [Rational(i, 20) for i in range(-60, 61)] if sum(mm(x**2 - 4*av*x + 2*av**2, 0, 4)) == 0]
chk("n1435", max(ok)*min(ok), 2)
best = -oo
for av in [Rational(i, 30) for i in range(-60, 150)]:
    e = (x - 3*av)**2
    bv = (6 - mm(e, 0, 6)[1])/3
    best = max(best, 2*av + bv)
chk("n1393", 3*best, 19)

# ---- 범위에 문자가 있을 때의 최대·최소
ks = [kv for kv in [Rational(i, 4) for i in range(-40, 41)] if mm(x**2 + 4*x + 8, kv, kv + 1)[0] == 8]
chk("n61", sum(ks), -5)
res = set()
for av in [Rational(i, 4) for i in range(-3, 60)]:
    M_, m_ = mm(x**2 - 2*x + av, -1, av)
    if M_ == 12:
        res.add(m_)
chk("o40", res.pop() if len(res) == 1 else res, 3)
res = set()
grid = [Rational(i, 2) for i in range(-24, 13)]
for av in grid:
    for bv in grid:
        if bv > av and mm(x**2 + 6*x + 13, av, bv) == (20, 5):
            res.add(bv - av)
chk("n1338", res.pop() if len(res) == 1 else res, 3)
ss = set()
for av in [Rational(i, 4) for i in range(-24, 25)]:
    M_, m_ = mm(-x**2 - 2*x + 2, av - Rational(1, 2), av + Rational(1, 2))
    if M_ - m_ == 2:
        ss.add(av)
chk("n3043", sum(ss), -2)
best = min(2*(lambda r: r[0] - r[1])(mm(4*x*(x - kv), kv, kv + 1)) for kv in [Rational(i, 20) for i in range(-100, 101)])
chk("n2933", best, 2)
res = []
for bv in [Rational(i, 4) for i in range(1, 40)]:
    f = (x - bv)**2            # a>0이면 차는 a배
    g3 = a*(lambda r: r[0] - r[1])(mm(f, 3, 5))
    if simplify(g3 - a) != 0:
        continue
    g2 = a*(lambda r: r[0] - r[1])(mm(f, 2, 4))
    for av in solve(g2 - 3*bv, a):
        if av > 0:
            res.append(av + bv)
chk("n1108", res[0] if len(res) == 1 else res, 7)

# ---- 공통부분이 있는 함수
M_, m_ = mm((3*x - 2)**2 - 4*(3*x - 2) + 5, 0, 2)
chk("o19", M_ + m_, 18)
tM, tm = mm(x**2 - 4*x, -1, 3)                      # 치환한 t의 범위
M_, m_ = mm(t**2 - 6*t + 1, tm, tM, t)
Mf, mf = mmf(lambda v: (v*v - 4*v)**2 - 6*(v*v - 4*v) + 1, -1, 3)
assert abs(Mf - M_) < 1e-3 and abs(mf - m_) < 1e-3
chk("n1102", M_ + m_, 33)
tM, tm = mm(x**2 - 2*x + 3, -1, 2)
M_, m_ = mm(t**2 - 4*t, tm, tM, t)
kv = 10 - M_
chk("w3", m_ + kv, -6)

# ---- 이차식의 최대·최소
e = x**2 - 2*x*y + 2*y**2 - 4*y + 9
cp = solve([diff(e, x), diff(e, y)], [x, y], dict=True)[0]
assert all(v > 0 for v in hessian(e, (x, y)).eigenvals())
chk("w2", e.subs(cp), 5)
chk("o21", mm(x**2 - x*(4 - x) + 5, 0, 4)[1], 3)
ee = expand(x**2 - 2*(k + 1)*x + k**2 + 1 - (-2*x + 4))
assert simplify(discriminant(ee, x)) > 0
s1, s2 = -Poly(ee, x).all_coeffs()[1], Poly(ee, x).all_coeffs()[2]
expr = s2 - 2*s1 + 4
M_, m_ = mm(expr, 0, 3, k)
chk("n1132", M_ - m_, 4)

# ---- 활용
chk("n1095", mm((42 - 3*x)*(x + 6), 0, 14)[0], 300)
chk("n1319", mm(50*t - t**2/4, 120, 250, t)[0], 2400)
rev = 10000*(1 - x/100)*64*(1 + 2*x/100)
M_, _ = mm(rev, 0, 50)
xs = [r for r in solve(diff(rev, x), x)][0]
chk("n1069", 10000*(1 - xs/100) + M_, 727500)
per = 2*(x + (-x**2 + 5*x - 4))
lo_, hi_ = real_roots(-x**2 + 5*x - 4)
chk("o44", mm(per, lo_, hi_)[0], 10)
area = Rational(1, 2)*((-a) - a + (a - (-2 - a)))*((4 - a**2) - (a**2 + 2*a))
assert solve(x**2 + 2*x - (a**2 + 2*a), x) in ([a, -a - 2], [-a - 2, a])
chk("n1151", mm(area, -1, 0, a)[0], Rational(9, 2))
kv = [kk for kk in solve(-(real_roots(2*x**2 + 2*k*x + k**2 - 5)[0] if False else 0) + k + 1, k)]
kk = -1   # α+β=-k=1
al, be = real_roots(-x**2 + 5 - (x + kk)**2)
assert simplify(((-be**2 + 5) - (-al**2 + 5))/(be - al)) == -1
S = Rational(1, 2)*((-t**2 + 5) - (t + kk)**2)*(be - al)
chk("n711", mm(S, al, be, t)[0], Rational(27, 4))
yA = 8 - t**2/2
per = 2*t + (yA - (3 - 3*t/4)) + (yA - (3 + 3*t/4)) + sqrt((2*t)**2 + (3*t/2)**2)
per = simplify(per.subs(sqrt(25*t**2/4), 5*t/2))
tmax = [r for r in solve(yA - (3 + 3*t/4), t) if r > 0][0]
chk("n1169", mm(5*t/2 + 2*t + 10 - t**2, 0, tmax, t)[0], Rational(241, 16))

# ---- 고난도
f = x**2/2 - 2*x
xB = [r for r in solve(f - m*x, x) if r != 0][0]
xC = [r for r in solve(f - m*(x - 4), x) if r != 4][0]
S1 = Rational(1, 2)*(4 - xC)*(-f.subs(x, xC))
S2 = Rational(1, 2)*(xB - 4)*f.subs(x, xB)
mx = mm(expand(S1 - S2), 0, 2, m)[0]
chk("m3285", fraction(mx)[0]*fraction(mx)[1], 12)
best = oo
for mv in [Rational(i, 10) for i in range(20, 61)]:
    al, be = real_roots(x**2 + x - 4 - (mv*x + 4))
    best = min(best, (2*(-al) + 2*be)**2)
chk("m3335", simplify(best), 132)
sols = []
for av in [3]:
    for bv in [4]:
        pass
cands = []
for av in range(1, 13):
    for bv in range(1, 13):
        fx = av*(x - 2)**2 - 4*av
        gx = bv*(x + 1)**2 - bv
        d1, d2 = discriminant(expand(fx + 12), x), discriminant(expand(gx + 12), x)
        if not ((d1 == 0 and d2 < 0) or (d2 == 0 and d1 < 0)):
            continue
        if abs(fx.subs(x, 2) - gx.subs(x, -1)) != 8 or not (fx.subs(x, 1) + gx.subs(x, 1) > 15):
            continue
        cands.append(sum(mm(-4*fx + gx, -3, Rational(1, 2))))
chk("n1260", cands[0] if len(cands) == 1 else cands, -28)
sols = []
for av in range(-12, 13):
    if av == 0:
        continue
    for bv in range(-20, 21):
        f = x**2 + av*x + bv
        if mm(f, -100, 100)[1] != -2:
            continue
        rr = real_roots(f.subs(x, 2*x + 1))
        if sum(rr) == -4:
            sols.append(sum(mm(f, -abs(av), abs(bv))))
chk("o56", sols[0] if len(sols) == 1 else sols, 96)
vals = []
for av in [Rational(i, 4) for i in range(12, 61)]:
    f = -(x - av)**2
    if mm(f, 3, 15)[0] != 0:
        continue
    if mm(f, 3, 9)[1] == mm(f, 9, 15)[0]:
        vals.append(f.subs(x, 2))
chk("n1281", max(vals) + min(vals), -17)
best = -oo
for pv in [Rational(i, 8) for i in range(-40, 41)]:
    qv = 4 - mm(-(x - pv)**2, -2, 0)[0]
    f = -(x - pv)**2 + qv
    if all(mm(f, n, n + 1)[1] == f.subs(x, n + 1) for n in range(1, 8)):
        best = max(best, f.subs(x, 2))
chk("n1023", best, 6)
f = a*(x - 2)**2 + b
for av in (Rational(1, 1),):
    pass
sol = []
for sgn in (1, -1):
    pts = []
    ok = True
    for kv in range(0, 4):
        M_ = mm(f.subs({a: sgn*3, b: 0}), -kv**2, 3 + kv**2)[0]
    # 계수 비교로 구한 a, b가 모든 k에서 조건을 만족하는지 확인
sols = solve(Poly(expand(f.subs(x, -k**2) - 3*k**4 - 12*k**2), k).all_coeffs(), [a, b], dict=True)
good = [s for s in sols if all(mm(f.subs(s), -kv**2, 3 + kv**2)[0] == 3*kv**4 + 12*kv**2 for kv in range(0, 5))]
chk("m3313", good[0][a]**2 + good[0][b]**2, 153)
tot = 0
for pv in [Rational(i, 20) for i in range(1, 60)]:
    for Mv in range(1, 200):
        f = -4*(x - pv)**2 + Mv
        if mm(f, 0, 3) == (Mv, Mv - 25) and mm(f, 0, 6) == (Mv, -2*Mv + 41):
            tot += pv*Mv
chk("n705", tot, 102)
res = []
for av in [Rational(i, 2) for i in range(-10, 11)]:
    for cv in [Rational(i, 2) for i in range(-10, 11)]:
        if av + cv <= 0:
            continue
        f = (x + av)**2; g = -(x - cv)**2
        ks = [kv for kv in [Rational(i, 4) for i in range(-40, 41)] if mm(f, kv - 3, kv + 1)[1] == mm(g, kv - 3, kv + 1)[0]]
        if ks and min(ks) == 0 and max(ks) == 1:
            res.append(f.subs(x, 5) + g.subs(x, 3))
chk("n1045", res[0] if len(res) == 1 else res, 45)
res = []
for hv in [Rational(i, 2) for i in range(-30, 41)]:
    if hv == 0 or not (2*hv).is_integer or (2*hv) % 2 != 0:
        continue
    f = (x - hv)**2 + 4
    bad = [n for n in range(1, 40) if (lambda r: r[0]*r[1])(mm(f, n, n + 3)) != f.subs(x, n)*f.subs(x, n + 3)]
    if bad == [4, 5]:
        res.append(f.subs(x, 10))
chk("n16", res[0] if len(res) == 1 else res, 20)


def Dt(tv):
    M_, m_ = mm(x**2 - tv*x + 3*tv, tv - 3, tv + 3)
    return M_ - m_ - tv**2/2


# h(t)=M-m-t²/2 의 식을 구간별로 확인한 뒤 실근 개수를 센다
for tv in [Rational(i, 4) for i in range(-60, 61)]:
    exp_ = (-(abs(tv) - 6)**2/4 + 18) if abs(tv) <= 6 else (-(abs(tv) - 6)**2/2 + 18)
    assert Dt(tv) == exp_
ks = []
for kv in range(1, 40):
    n = 0
    n += len([r for r in solve(-(t - 6)**2/4 + 18 - kv, t) if r.is_real and 0 <= r <= 6])
    n += len([r for r in solve(-(t - 6)**2/2 + 18 - kv, t) if r.is_real and r > 6])
    tot_roots = 2*n - (1 if kv == 9 else 0)     # t=0은 한 번만 센다
    if tot_roots == 2:
        ks.append(kv)
chk("n1027", sum(ks), 54)

if __name__ == "__main__":
    bad = [r for r in R if not r[1]]
    print(len(R), "검산", "불일치", bad)
