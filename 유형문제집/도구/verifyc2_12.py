# 공통수학2 12단원(무리식과 무리함수) 유형서 문항 정답 독립 검산 (문항 기호는 c2unit12.py의 v).
# 방정식은 sympy로 풀고 제곱 전 식에 다시 넣어 확인한다. 교점 개수·사분면·최댓값은 매개변수 후보를 하나씩 넣어 센다.
import math
import numpy as np
import sympy as sp
R = []
x = sp.symbols("x", real=True)
sq = np.sqrt


def chk(no, got, exp):
    if isinstance(got, str):
        ok = got == exp
    else:
        e = float(sp.sympify(exp))
        ok = abs(float(got) - e) <= 1e-3 * max(1, abs(e))
    R.append((no, ok, got, exp))


def mark(truth, ch, names="ㄱㄴㄷㄹㅁ"):
    s = ", ".join(names[i] for i, v in enumerate(truth) if v)
    ch = ch.split("|")
    return "①②③④⑤"[ch.index(s)] if s in ch else "?"


def lin(a, b, n=400001):
    return np.linspace(a, b, n)


def roots(lhs, rhs, dom=lambda s: True):
    """lhs=rhs의 실근: 풀이 후 원래 식에 넣어 확인(제곱해서 생긴 근 제거)"""
    out = set()
    for s in sp.solve(sp.Eq(lhs, rhs), x):
        if not s.is_real:
            continue
        try:
            if dom(s) and abs(complex(sp.N(lhs.subs(x, s) - rhs.subs(x, s)))) < 1e-9:
                out.add(round(float(s), 10))
        except (TypeError, ValueError):
            pass
    return sorted(out)


# 무리식 ---------------------------------------------------------------
e = x / (sp.sqrt(x + 9) + 3) + x / (sp.sqrt(x + 9) - 3)
opts = [sp.sqrt(x + 9) - 3, sp.sqrt(x + 9), sp.sqrt(x + 9) / x, sp.sqrt(x + 9) + 3, 2 * sp.sqrt(x + 9)]
val = [abs(float((e - o).subs(x, 7))) < 1e-12 and abs(float((e - o).subs(x, 16))) < 1e-12 for o in opts]
chk("g1-20", "①②③④⑤"[val.index(True)], "⑤")
chk("g1-21", sum(1 for v in range(-50, 50) if abs(v + 3) - 3 >= 0 and 4 - abs(v - 1) >= 0), 6)
X = sp.sqrt(2)
chk("g2-32", sp.nsimplify((sp.sqrt(X + 1) + sp.sqrt(X - 1)) / (sp.sqrt(X + 1) - sp.sqrt(X - 1))), "1+sqrt(2)")
chk("o13", sum(v for v in range(-20, 20) if v - 3 >= 0 and 5 - v > 0), 7)
xs = lin(-50, 50, 100001)
chk("m1009-23", sum(1 for k in range(-100, 100) if np.all((k + 1) * xs**2 - (k + 1) * xs + 5 >= 0)), 21)
chk("k10-11", sum(1 / (math.sqrt(4 * k + 1) + math.sqrt(4 * k - 3)) for k in range(1, 13)), "3/2")
# 활용 ------------------------------------------------------------------
n_ = sp.symbols("n", positive=True)
T_, rho, L_ = 1, 1, 1
w = lambda T, r: 1 / (2 * L_) * sp.sqrt(sp.Rational(T) / r)
chk("m1306-27", sp.solve(sp.Eq(w(3, n_), w(1, 1) / 2), n_)[0], 12)
# L = 4 pi sigma T^4 R^2
chk("m1511-16", sp.Rational(1, 2)**4 * 36**2, 81)

# 평행이동·대칭이동 -----------------------------------------------------
xs = lin(-60, 2, 10001)
f = sq(-3 * (xs - 2)) + 3
dom, rng = (xs.max() == 2), f.min()
chk("k7-11", "⑤" if dom and abs(rng - 3) < 1e-12 else "?", "⑤")
def same_shape(a_abs):
    return a_abs == 2
t = [same_shape(2), same_shape(2), same_shape(8), same_shape(2)]   # ㄱ √(2x), ㄴ √(−2x), ㄷ −√(8x), ㄹ −√(−2x)
chk("k11-6", mark(t, "ㄴ, ㄷ|ㄷ, ㄹ|ㄱ, ㄴ, ㄷ|ㄱ, ㄴ, ㄹ|ㄴ, ㄷ, ㄹ"), "④")
a_, b_, c_ = sp.symbols("a b c")
# sqrt(a(x-b))-1+c == sqrt(-5x-1)+3
sol = sp.solve([sp.Eq(a_, -5), sp.Eq(-a_ * b_, -1), sp.Eq(c_ - 1, 3)], [a_, b_, c_], dict=True)[0]
chk("o37", sol[a_] + sol[b_] + sol[c_], "-6/5")

# 사분면 -----------------------------------------------------------------
def quads(xs, ys):
    ok = (np.abs(xs) > 1e-12) & (np.abs(ys) > 1e-12) & np.isfinite(ys)
    return {(u > 0, v > 0) for u, v in zip(xs[ok], ys[ok])}
xs = np.concatenate([lin(-1e4, 3, 400001), lin(-1, 3, 400001)])
ys = sq(-xs + 3) - 2
q = quads(xs, ys)
t1 = q == {(False, True), (False, False), (True, False)}
t2 = False                    # 치역 y ≥ −2
t3 = False                    # 시작점 (3, −2): x축 방향 3만큼
chk("k4-15", mark([t1, t2, t3], "ㄱ|ㄴ|ㄱ, ㄷ|ㄴ, ㄷ|ㄱ, ㄴ, ㄷ"), "①")
good = []
for a in range(-10, 10):
    xs = np.concatenate([lin(-1e4, 3, 400001), lin(-1, 3, 400001)])
    if quads(xs, sq(-2 * xs + 6) + a) >= {(True, True), (False, True), (True, False)}:
        good.append(a)
chk("숙명여고", sum(good), -3)
def nq(a):
    s0 = -a
    pts = [s0 + 1e-12] + list(lin(s0, s0 + 1e4, 200001))
    x0 = (2 - a)**2 - a if a <= 2 else None
    for c in (0.0, x0):
        if c is not None:
            pts += [c - 1e-9, c + 1e-9]
    xs = np.array([u for u in pts if u >= s0]); ys = sq(xs + a) + a - 2
    return len(quads(xs, ys))
good = [a for a in np.round(np.arange(-3, 5, 0.05), 3) if nq(a) == 2]
ok = all(a <= 0 or a >= 2 or abs(a - 1) < 1e-9 for a in good) and 0 in good and 2 in good and 1 in good and nq(1.001) == 3
chk("k3-24", "$a leq 0$ 또는 $a=1$ 또는 $a geq 2$" if ok else "?", "$a leq 0$ 또는 $a=1$ 또는 $a geq 2$")
def meet(k):
    f = -sp.sqrt(k * x + 2 * k) + 4; g = sp.sqrt(-k * x + 2 * k) - 4
    return len(roots(f, g, lambda s: k * s + 2 * k >= 0 and -k * s + 2 * k >= 0))
t1 = all(abs(float(((-(-sp.sqrt(k * (-x) + 2 * k) + 4)) - (sp.sqrt(-k * x + 2 * k) - 4)).subs(x, 1))) < 1e-12 for k in (1, 3))
t2 = meet(-1) == 1
two = [k for k in range(1, 40) if meet(k) == 2]
t3 = max(two) == 16
chk("m1803-20", mark([t1, t2, t3], "ㄱ|ㄴ|ㄱ, ㄴ|ㄱ, ㄷ|ㄱ, ㄴ, ㄷ"), "④")

# 식 구하기 ---------------------------------------------------------------
for a in range(-20, 0):
    b = -2 * a
    if abs(-math.sqrt(a * -2 + b) - 2 + 6) < 1e-12:
        chk("k4-12", -math.sqrt(a * -7 + b) - 2, -8)
for a in range(-20, 0):
    if abs(math.sqrt(a * (3 - 4)) - 2) < 1e-12:
        chk("g1-26", a + (-4 * a) + (-2), 10)
b = 4 - 1
a = [a for a in range(1, 20) if abs(math.sqrt(6 * a + 1) + b - 8) < 1e-12][0]
chk("압구정고-11", a * b, 12)

# 최대·최소 ---------------------------------------------------------------
a = 1   # f(0) = -1 + a = 0
b = [b for b in range(0, 100) if abs(-math.sqrt(b + 1) + a + 3) < 1e-12][0]
chk("k4-9", a + b, 16)
xs = lin(3, 9, 6001); ys = -sq(2 * xs - 2) + 5
chk("k8-7", ys.max() + ys.min(), 4)
xs = lin(-5, -1, 4001)
chk("k12-7", [a for a in range(1, 20) if abs((-sq(-a * xs + 1)).max() + 2) < 1e-9][0], 3)
xs = lin(-5, 3, 8001)
a = [a for a in range(3, 30) if abs((sq(a - xs) + 2).min() - 3) < 1e-9][0]
chk("g1-30", (sq(a - xs) + 2).max(), 5)
xs = lin(-3, 3, 600001); ys = sq(3 + xs) + sq(3 - xs)
chk("g3-4", ys.max() * ys.min(), "6*sqrt(2)")

# 직선 -------------------------------------------------------------------
cnt = 0
for k in range(2, 100):
    xs = lin(-1, 1, 20001); ys = sq(-2 * xs + k) - 1; ls = 1 + (xs + 1) / 2
    d = ys - ls
    if np.any(np.sign(d[:-1]) * np.sign(d[1:]) <= 0):
        cnt += 1
chk("g1-23", cnt, 10)
m_ = sp.Rational(1, 2)
r = roots(sp.sqrt(x - 1), m_ * x, lambda s: s >= 1)
assert len(r) == 1 and all(len(roots(sp.sqrt(x - 1), mm * x, lambda s: s >= 1)) == 2 for mm in (sp.Rational(49, 100),))
chk("g1-32", m_ + r[0] + math.sqrt(r[0] - 1), "7/2")
res = []
for a in range(1, 80):
    ks = [k for k in range(-20, 40) if len(roots(2 * x + k, sp.sqrt(a * (x + 3)), lambda s: s >= -3)) == 2]
    if len(ks) == 4:
        res.append(a)
chk("k2-16", len(res), 8)
def n50(k):
    return len(roots(-sp.sqrt(2 * x - 5) - 2, -k * x, lambda s: s >= sp.Rational(5, 2)))
ks = [sp.Rational(n, 40) for n in range(-60, 60)]
good = [k for k in ks if n50(k) == 2]
assert min(good) == sp.Rational(4, 5) and max(good) == sp.Rational(39, 40) and n50(1) == 1
chk("g2-50", "②", "②")
def one(k):
    xs = lin(3, 5, 20001); d = sq(3 * xs) + k - (-2 * xs + 4) / (xs - 1)
    return np.any(d <= 0) and np.any(d >= 0)
ks = np.arange(-8, 0, 0.001)
M = max(k for k in ks if one(k))
chk("m1311-27", round(M, 3)**2, 16)
tot = 0
for k in range(-20, 30):
    r = roots(5 - 2 * sp.sqrt(1 - x), -x + k, lambda s: s <= 1)
    if any(s > 0 and 5 - 2 * math.sqrt(1 - s) > 0 for s in r):
        tot += k
chk("m1903-15", tot, 15)
cnt = 0
for a in range(1, 20):
    for b in range(1, 20):
        xs = lin(1, 3, 20001); d = a * sq(xs) + b - (4 - (xs - 1) / 2)
        if np.any(d <= 0) and np.any(d >= 0):
            cnt += 1
chk("m1803-16", cnt, 5)

# 역함수와 합성 -----------------------------------------------------------
f = lambda u: sp.Rational(u + 1) / (u - 2)
k = sp.solve(sp.Eq((x + 1) / (x - 2), sp.Rational(7, 6)), x)[0]
chk("g1-27", sp.sqrt(2 * k - 4), 6)
chk("k3-21", sp.sqrt(3 * sp.Rational(-0 + 2, 0 + 1) + 3), 3)
g = lambda u: math.sqrt(2 * (u + 1) + 1)
assert abs((g(3)**2 - 1) / 2 - 4) < 1e-12        # f⁻¹(g(3)) = 3+1
chk("압구정고-6", g(3), 3)
g = lambda u: math.sqrt(3 * (2 * u) - 12)
assert abs((g(3)**2 + 12) / 3 - 6) < 1e-12
chk("m2003-16", g(3), "sqrt(6)")
def finv58(v):
    if v >= 2:
        return sp.solve(sp.Eq(sp.sqrt(1 - x) + 2, v), x)[0]
    return [s for s in sp.solve(sp.Eq((2 * x - 3) / (x - 1), v), x) if s > 1][0]
chk("o58", finv58(finv58(finv58(4))), "9/4")

# 역함수와의 교점 ---------------------------------------------------------
res = []
for a in [sp.Rational(n, 8) for n in range(-3, 5)]:
    r = roots(sp.sqrt(4 * x - 2) + a, x, lambda s: s >= sp.Rational(1, 2))
    if len(r) == 2 and abs(math.sqrt(2) * (r[1] - r[0]) - 2 * math.sqrt(6)) < 1e-9:
        res.append(a)
chk("o59", res[0], "1/4")
res = [k for k in range(-20, 20) if len(r := roots(sp.sqrt(2 * x - k) + 1, x)) == 2 and abs(math.sqrt(2) * (r[1] - r[0]) - 2 * math.sqrt(2)) < 1e-9]
chk("g2-48", res[0], 2)
r = roots(sp.sqrt(3 * x - 9) + 3, x, lambda s: s >= 3)
chk("고림고", math.sqrt(2) * (r[1] - r[0]), "3*sqrt(2)")
def n15(m):
    return len(roots(sp.sqrt(4 * x - 16) + m, x, lambda s: s >= 4))
ms = [sp.Rational(n, 20) for n in range(40, 100)]
good = [m for m in ms if n15(m) == 2]
assert min(good) == sp.Rational(61, 20) and max(good) == 4 and n15(3) == 1
chk("압구정고-15", 3 + 4, 7)
cnt = sum(1 for k in range(-30, 5) if len(roots(2 * sp.sqrt(x + 1) + k, x, lambda s: s >= -1)) == 1)
chk("경기여고", cnt, 6)
cnt = sum(1 for k in range(-30, 30) if len(roots(sp.sqrt(5 * x - k), x, lambda s: s >= 0 and 5 * s - k >= 0)) == 2)
chk("m1509-19", cnt, 7)

# 대칭인 두 점 -----------------------------------------------------------
A = roots(sp.sqrt(x + 6), x)[0]
B = roots(sp.sqrt(x + 6), -x - 4, lambda s: s >= -6)[0]
Bp = (B, -B - 4); Cp = (-B - 4, B); Ap = (A, A)
area = abs((Bp[0] - Ap[0]) * (Cp[1] - Ap[1]) - (Cp[0] - Ap[0]) * (Bp[1] - Ap[1])) / 2
chk("k8-11", area, 30)
best = 0
for k in lin(-6, 3, 90001):
    # A: sqrt(x+6) = -x+k, B: f^{-1}(x) = x^2-6 (x>=0) = -x+k
    disc = (2 * k + 1)**2 - 4 * (k * k - 6)
    if disc < 0:
        continue
    xa = [u for u in ((2 * k + 1 - math.sqrt(disc)) / 2, (2 * k + 1 + math.sqrt(disc)) / 2) if u >= -6 and -u + k >= -1e-12]
    db = 1 + 4 * (6 + k)
    xb = [u for u in ((-1 - math.sqrt(db)) / 2, (-1 + math.sqrt(db)) / 2) if u >= 0]
    if xa and xb:
        best = max(best, math.hypot(xa[0] - xb[0], (-xa[0] + k) - (-xb[0] + k)))
ratio = sp.nsimplify(round(best / math.sqrt(2), 6))
chk("k12-20", ratio.p + ratio.q, 29)
res = []
for al in [sp.Rational(n, 2) for n in range(0, 10)]:
    if 5 * (10 - 2 * al) == 20:
        P = (al, 10 - al)
        res.append(sp.Rational(P[1]**2) / P[0])
chk("능동고", res[0], "49/3")
a = sp.symbols("a", nonnegative=True)
m = sp.sqrt(sp.Rational(25, 2) / 2)
n = [s for s in sp.solve(sp.Eq((a**2 + 2 - m)**2 + (a - m)**2, sp.Rational(25, 2)), a) if s.is_real and s >= 0][0]
chk("m2311-19", m + n**2 + 2, "17/2")

# 도형 -------------------------------------------------------------------
a = sp.symbols("a", positive=True)
av = sp.solve(sp.Eq(4 * a - a, sp.sqrt(a)), a)[0]
chk("m1803-17", (3 * av)**2 / 2, "1/18")
k = sp.symbols("k", positive=True)
kv = [v for v in sp.solve(sp.Eq(k - sp.sqrt(k), 2 * sp.sqrt(k)), k) if v > 1][0]
chk("m2403-14", kv * (kv - sp.sqrt(kv)) / 2, 27)
av = [a for a in range(1, 10) if abs(6 * math.sqrt(1 + 3) / 2 - 6) < 1e-12 and abs(math.sqrt(a * (3 - 1)) - 2) < 1e-12][0]
chk("o40", av, 2)
A = roots(sp.sqrt(2 * x + 3), x)[0]
C = roots((x**2 - 3) / 2, -x + sp.Rational(5, 2), lambda s: s >= 0)[0]
Bp, Cp, Ap = (0.5, 2.0), (C, -C + 2.5), (A, A)
chk("m1411-20", abs((Bp[0] - Ap[0]) * (Cp[1] - Ap[1]) - (Cp[0] - Ap[0]) * (Bp[1] - Ap[1])) / 2, "21/8")
# g2-42: 격자 넓이 (몬테카를로가 아니라 세로 띠 적분 근사)
ys = lin(0, 6, 600001)
def xr(y):            # 오른쪽 경계: 곡선 y=sqrt(x-3) → x=y^2+3, 직선 y=-x+15 → x=15-y
    return np.minimum(ys**2 + 3, 15 - ys)
def xl(y):            # 왼쪽 경계: 곡선 y=sqrt(x)+3 → x=(y-3)^2 (y>=3), 직선 y=-x+3 → x=3-y
    return np.maximum(np.where(ys >= 3, (ys - 3)**2, -1e9), 3 - ys)
w = np.clip(xr(ys) - xl(ys), 0, None)
chk("g2-42", np.trapezoid(w, ys) if hasattr(np, "trapezoid") else np.trapz(w, ys), 36)

# 두 함수로 정의된 함수 ---------------------------------------------------
xs = lin(3 + 1e-9, 1e6, 2000001); rv = 2 + 7 / (xs - 2)
a = round(rv.max())
f2 = 1 + a
kv = [s for s in sp.solve(sp.Eq((2 * x + 3) / (x - 2), sp.Rational(40, f2)), x) if s > 3][0]
chk("m1211-18", kv, "11/2")
res = []
for c in range(-10, 20):
    for a in range(-10, 0):
        for b in range(-10, 20):
            if a + b != 1 or c - 2 < 0 or abs(math.sqrt(c - 2) + 1 - 1) > 1e-12:
                continue
            f = lambda u: a * u + b if u >= 1 else math.sqrt(c - 2 * u) + 1
            if abs(f(-1) - 3) < 1e-12 and abs(f(3) + 1) < 1e-12:
                res.append(a + 2 * b + 3 * c)
chk("k12-19", res[0], 9)

# 고난도 -----------------------------------------------------------------
xs = lin(-4, 4, 800001)
chk("m0903-29", np.trapezoid(sq(-xs + 4) + 3 - (sq(xs + 4) - 3), xs) if hasattr(np, "trapezoid") else np.trapz(sq(-xs + 4) + 3 - (sq(xs + 4) - 3), xs), 48)
tot, kk = 0, None
for xv in range(4, 100):
    hi = math.floor(2 * math.sqrt(xv) + 1e-12); lo = math.ceil(6 - math.sqrt(xv) - 1e-12)
    tot += hi - lo + 1
    if tot == 59:
        kk = xv
chk("m1809-29", kk, 18)
res = []
for a in range(-10, 20):
    b = a
    f = lambda u: -(u - a)**2 + b if u <= a else -math.sqrt(u - a) + b
    fx = [u for u in np.arange(-20, 40, 0.5) if abs(f(u) - u) < 1e-12]
    if len(fx) != 2:
        continue
    al, be = fx
    sols = set()
    for tv in (al, be):
        for u in np.arange(-50, 80, 0.25):
            if abs(f(u) - tv) < 1e-12:
                sols.add(u)
    ga = [u for u in sols if u not in (al, be)]
    if len(sols) == 3 and len(ga) == 1 and abs(al + be + ga[0] - 15) < 1e-12:
        res.append(f(al + be))
chk("m2303-20", res[0], 3)
# g3-14
def n14(k):
    c = 0
    for nn in range(0, 30):
        xs = lin(nn, nn + 1, 20001)[:-1]
        d = sq(xs - nn) - nn - (k * xs + 2)
        c += int(np.count_nonzero(np.sign(d[:-1]) * np.sign(d[1:]) < 0) + np.count_nonzero(np.abs(d) < 1e-12))
    return c
ks = np.round(np.arange(-5, 0, 0.05), 3)
good = [k for k in ks if n14(k) == 2]
assert abs(min(good) + 3) < 1e-9 and max(good) < -2 and max(good) > -2.1
chk("g3-14", (-3)**2 + (-2)**2, 13)
# m2403-30
XS = lin(-100, 200, 600001)
res = []
for a in range(-10, 20):
    for b in range(1, 8):
        g = np.where(XS <= a, np.abs(sq(np.maximum(a - XS, 0)) - b) + b, -(sq(np.maximum(XS - a, 0)) - b) + abs(b))
        def h(tv):
            d = g - tv
            return int(np.count_nonzero(np.sign(d[:-1]) * np.sign(d[1:]) < 0) + np.count_nonzero(np.abs(d) < 1e-12))
        al, be = b, 2 * b
        if h(al) * h(be) != 4:
            continue
        idx = np.where((np.abs(g - al) < 1e-9) | (np.abs(g - be) < 1e-9))[0]
        xsol = XS[idx]
        # 정확한 근: g=b → a±b², g=2b → a, a-4b²
        ex = [a - b * b, a + b * b, a, a - 4 * b * b]
        if min(ex) == -30 and max(ex) == 15:
            g150 = -(math.sqrt(150 - a) - b) + abs(b)
            res.append(g150**2)
chk("m2403-30", res[0], 36)
# m2003-30
res = []
for a in [sp.Rational(n, 2) for n in range(3, 40)]:
    f = sp.sqrt(a * x - 3) + 2
    fi = ((x - 2)**2 + 3) / a
    def h(n):
        xs = lin(2, 400, 400001)
        fv = sq(np.maximum(float(a) * xs - 3, 0)) + 2; fiv = ((xs - 2)**2 + 3) / float(a)
        gv = np.where(fv < fiv, fv, fiv); d = gv - (xs - n)
        c = int(np.count_nonzero(np.sign(d[:-1]) * np.sign(d[1:]) < 0))
        c += int(np.count_nonzero(np.abs(d) < 1e-9))
        # 접점(최솟값이 0)은 격자에서 부호가 바뀌지 않을 수 있으므로 따로 센다
        i = np.argmin(np.abs(d))
        if abs(d[i]) < 1e-6 and not (np.abs(d) < 1e-9).any() and (d[max(i - 1, 0)] > 0 and d[min(i + 1, len(d) - 1)] > 0):
            c += 1
        return c
    if h(1) == h(3) < h(2):
        res.append(a)
a = res[0]
g4 = min(math.sqrt(float(a) * 4 - 3) + 2, ((4 - 2)**2 + 3) / float(a))
q_ = sp.nsimplify(round(g4, 10))
chk("m2003-30", q_.p + q_.q, 13)

if __name__ == "__main__":
    bad = [r_ for r_ in R if not r_[1]]
    print("검산", len(R), "불일치", len(bad))
    for r_ in bad:
        print(r_)
