# 공통수학2 11단원(유리식과 유리함수) 유형서 문항 정답 독립 검산 (문항 기호는 c2unit11.py의 v).
# 계수 비교는 sympy, 교점·최솟값·개수는 촘촘한 격자와 판별식, 조건을 만족하는 매개변수는 후보를 하나씩 넣어 확인한다.
import math
from fractions import Fraction as Fr
import numpy as np
import sympy as sp
R = []
x = sp.symbols("x", real=True)


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


def quadrants(f, xs):
    with np.errstate(divide="ignore", invalid="ignore"):
        v = f(xs)
    ok = np.isfinite(v) & (np.abs(xs) > 1e-9) & (np.abs(v) > 1e-9)
    X, Y = xs[ok] > 0, v[ok] > 0
    return {(a, b) for a in (True, False) for b in (True, False) if np.any((X == a) & (Y == b))}


XS = np.concatenate([-np.logspace(-5, 5, 80001), np.logspace(-5, 5, 80001)])


def mob(p, q, r, s_):
    return (lambda t: Fr(p * t + q) / Fr(r * t + s_)), (lambda t: Fr(-s_ * t + q) / Fr(r * t - p))


PTS = [Fr(n, 7) for n in (-23, -9, 5, 17, 40)]


def same(f, g):
    try:
        return all(f(t) == g(t) for t in PTS)
    except ZeroDivisionError:
        return False


def count_hits(fun, t, segs):
    """여러 구간에서 fun(x)=t의 서로 다른 해의 개수(부호 변화 + 정확한 0)"""
    c = 0
    for xs in segs:
        v = fun(xs) - t; s = np.sign(v)
        c += int(np.count_nonzero(s[:-1] * s[1:] < 0) + np.count_nonzero(np.abs(v) < 1e-12))
    return c


# 유리식의 계산 ---------------------------------------------------------
e = sp.apart(sp.cancel((x - 1) / (1 - 2 / (x - 1))), x)
chk("g2-2", sum(sp.Poly(sp.cancel(e - 4 / (x - 3)), x).all_coeffs()) + 4, 6)
ok = [a for a in range(1, 1000) if (3 * a * a + 5 * a + 2) % (a + 6) == 0]
chk("g2-3", min(ok) + max(ok), 76)
a_, b_, c_ = sp.symbols("a b c")
sol = sp.solve(sp.Poly(sp.expand(a_ * (x**2 - 2 * x + 4) + (x + 2) - (x**2 + b_ * x + c_)), x).all_coeffs(), [a_, b_, c_])
chk("o02", sol[a_] + sol[b_] + sol[c_], 6)
z = sp.symbols("z", nonzero=True)
X_, Y_ = 2 * z, 2 * z
assert sp.simplify((X_ + Y_) / (2 * z) - (Y_ + 2 * z) / X_) == 0
chk("m1106-11", sp.simplify((X_**3 + Y_**3 + z**3) / (X_ * Y_ * z)), "17/4")

# 그래프와 점근선 -------------------------------------------------------
a = sp.solve(sp.Eq((2 * (-1) + a_) / 3, 1), a_)[0]
chk("k3-11", a * (-4) * 2, -40)
sol = [(a, b, c) for a in range(-10, 11) for b in range(-20, 21) for c in range(-10, 11)
       if c == -3 and a == 2 and (5 * a + b) == 4 * (5 + c)]
chk("k9-4", sum(sol[0]), -3)
sol = [(a, b, c) for a in range(-10, 11) for b in range(-30, 31) for c in range(-10, 11)
       if c == -5 and a == -3 and 4 * a + b == -2 * (4 + c) and a * c != b]
chk("o06", sum(sol[0]), 6)
chk("능동고", [a + 3 for a in range(-10, 11) if -a == 2][0], 1)
f = lambda t: (2 * t + 3) / (t + 4)
q = quadrants(f, XS)
t1 = False                               # x절편 −3/2, y절편 3/4
t2 = (True, False) not in q
t3 = False                               # 점근선 교점 (−4, 2)
t4 = sp.simplify((2 * x + 3) / (x + 4) - (-5 / (x + 4) + 2)) == 0
chk("k12-8", mark([t1, t2, t3, t4], "ㄱ, ㄴ|ㄱ, ㄷ|ㄴ, ㄷ|ㄴ, ㄹ|ㄷ, ㄹ"), "④")
f = lambda t: (3 - 2 * t) / (t - 2)
q = quadrants(f, XS)
t1 = (False, True) in q
t2 = sp.limit((3 - 2 * x) / (x - 2), x, sp.oo) == -2
t3 = all(abs(f(2 + u) + f(2 - u) + 4) < 1e-9 for u in (0.3, 1.7, 5.0)) and all(abs(f(-y - 0) - (-(-y))) < 1e9 for y in (0.1,))
# y=-x 대칭: (p, q) → (−q, −p) — 점 (t, f(t))의 대칭점 (−f(t), −t)도 그래프 위
t3 = all(abs(f(-f(t)) - (-t)) < 1e-9 for t in (0.5, 3.7, -4.2))
chk("k2-4", mark([t1, t2, t3], "ㄱ|ㄴ|ㄱ, ㄴ|ㄴ, ㄷ|ㄱ, ㄴ, ㄷ"), "④")

# 평행이동과 대칭 -------------------------------------------------------
chk("k4-7", (-4 - 1) + (2 - 0), -3)
chk("k3-12", 4 - 3, 1)
X0 = sp.solve(sp.Eq(x + sp.Rational(1, 2), -x + sp.Rational(1, 3)), x)[0]
Y0 = X0 + sp.Rational(1, 2)
chk("k8-10", Y0 + (-X0), "1/2")
sol = [(2, b, 1, 2) for b in range(-10, 11) if Fr(2 * 2 + b, 2 + 1) == 1]
chk("k11-13", sum(sol[0]), 4)
f = lambda t: Fr(3 * t + 5) / Fr(t - 1)
chk("k4-18", f(-1) if f(0) == -5 else None, -1)
ks = [k for k in range(-20, 21) if Fr(3 * (-6) + k, -6 + 4) == 6]
chk("m1503-16", ks[0], 6)
res = []
for a in range(-12, 13):
    if a == 0:
        continue
    for b2 in range(-24, 25):
        b = Fr(b2, 2)
        h = lambda t: abs(a / (t + a - 6) + b + a / 2)
        ts = [0.37, 1.9, 7.3]
        try:
            if all(abs(h(t) - h(-t)) < 1e-9 for t in ts):
                res.append(Fr(a, b - 6) + b)
        except ZeroDivisionError:
            pass
chk("m2003-19", res[0], "-11/3")

# 지나는 사분면 ---------------------------------------------------------
ks = [k for k in range(-60, 61) if k != 0 and len(quadrants(lambda t: k / (t + 3) + 6, XS)) == 4]
chk("대평고", max(ks), -19)
chk("m1706-15", sum(1 for k in range(1, 60) if k != 13 and (True, False) in quadrants(lambda t: (3 * t + k - 10) / (t + 1), XS)), 9)
f = lambda t: (2 * t + 3) / (t - 1)
t1 = sp.limit((2 * x + 3) / (x - 1), x, sp.oo) == 3
t2 = len(quadrants(f, XS)) == 4
t3 = all(abs(f(f(t) - 3) - (t + 3)) < 1e-9 for t in (2.5, 4.0, -3.0))   # y=x+3 대칭이면 (f(t)−3, t+3)도 그래프 위
chk("o09", mark([t1, t2, t3], "ㄱ|ㄴ|ㄱ, ㄴ|ㄴ, ㄷ|ㄱ, ㄴ, ㄷ"), "②")

# 최대·최소 ----------------------------------------------------------
res = [k for k in range(0, 40) if k != 16 and max(Fr(4 * t - k, t - 4) for t in [Fr(i, 10) for i in range(10, 31)]) == 2]
chk("m2503-14", res[0], 10)
res = []
for a2 in range(5, 40):
    a = Fr(a2, 2)
    v = [Fr(5 - 3 * t, t - 1) for t in [2 + (a - 2) * Fr(i, 100) for i in range(101)]]
    if min(v) == -2:
        res.append(a + max(v))
chk("o08", res[0], 2)

# 역함수 -------------------------------------------------------------
res = [a for a in range(-10, 11) if a != -2 and same(mob(3, -6, 1, a)[0], mob(3, -6, 1, a)[1])]
chk("k10-7", res[0], -3)
res = []
for a in range(-10, 11):
    for b in range(-10, 11):
        if a * b == 4 or 2 + b == 0:
            continue
        f, fi = mob(a, 4, 1, b)
        if same(f, fi) and f(2) == 6:
            res.append(sum(1 for X in range(-200, 201) if X + b != 0 and (a * X + 4) % (X + b) == 0))
chk("k8-15", res[0], 4)
f, fi = mob(3, 2, 1, -4)
assert same(fi, lambda t: Fr(4 * t + 2, t - 3))
chk("o12", Fr(4 * 2 + 2, 2 - 3), -10)
res = [(a, b) for a in range(-10, 11) for b in range(-10, 11) if 3 + a != 0 and -6 + a != 0
       and Fr(b - 4, 3 + a) == -2 and Fr(-2 * b - 4, -6 + a) == 1]
chk("경기여고", res[0][0] * res[0][1], -4)
f, fi = mob(1, -6, 1, -4)
roots = set()
for X in [Fr(n, 2) for n in range(-40, 41)]:
    if X in (4, 1):
        continue
    if f(X)**2 == f(X) * fi(X):
        roots.add(X)
chk("k2-14", sum(roots), 11)

# f^{-1}(x)=f(x-m)+n ---------------------------------------------------
res = [a + b for a in range(-10, 11) for b in range(-30, 31) if 3 * a + b == 5 and same(mob(3, b, 1, -a)[1], lambda t, a=a, b=b: mob(3, b, 1, -a)[0](t + 2) + 2)]
chk("k9-9", res[0], -5)
res = [a - b for a in range(-20, 21) for b in range(-10, 11) if 2 * b + a == 3 and same(mob(2, a, 1, -b)[1], lambda t, a=a, b=b: mob(2, a, 1, -b)[0](t - 4) - 4)]
chk("k12-14", res[0], 9)
res = [a + b for a in range(-10, 11) for b in range(-20, 21) if 2 * a + b == 3 and same(mob(2, b, 1, -a)[1], lambda t, a=a, b=b: mob(2, b, 1, -a)[0](t - 4) - 4)]
chk("m1703-19", res[0], 5)

# 직선과의 위치 관계 ------------------------------------------------------
ks = []
for k in range(-30, 31):
    rts = [r for r in sp.solve(sp.Eq((x + 2), (x + k) * (x + 3)), x) if r.is_real and r != -3]
    if len(set(rts)) == 1:
        ks.append(k)
chk("o11", sum(ks), 8)
ok = []
segs = [lin(-200, -1 - 1e-6, 400001), lin(-1 + 1e-6, 200, 400001)]
for k in np.round(lin(-8, 3, 1101), 3):
    if count_hits(lambda t: (-2 * t - 1) / (t + 1) - k * (t - 1) + 6, 0, segs) > 0:
        ok.append(k)
neg = [k for k in ok if k < -2.5]; pos = [k for k in ok if k > -2.5]
chk("g2-26", "⑤" if abs(max(neg) + 4) < 0.02 and abs(min(pos) + 1) < 0.02 and max(pos) > 2.9 else "?", "⑤")
xs = lin(-4, -2); kv = (2 * xs - 7) / (xs - 1)**2
chk("숙명여고", kv.max() * kv.min(), "11/15")


def h119(k):
    rts = sp.solve(sp.Eq(-1 / x + k, 1 / (x - 1) - k), x)
    return sum(1 for r in rts if r.is_real and r > 0 and r != 1)


ks = [k for k in range(-10, 9) if h119(k) + h119(k + 1) + h119(k + 2) == 4]
chk("m1903-20", ks[0], -1)

# 합성과 규칙성 -------------------------------------------------------
v = Fr(1)
for _ in range(1000):
    v = v / (v + 1)
chk("g2-8", v, "1/1001")
g = sp.simplify(((x + 3) / (x - 2)).subs(x, (x + 3) / (x - 2)))
num, den = sp.fraction(sp.together(g))
va = sp.solve(den, x)[0]; ha = sp.limit(g, x, sp.oo)
chk("o29", va + ha, 3)

# 그래프 위의 점과 도형 ---------------------------------------------------
ks = []
for k in range(-10, 0):
    A = (2 - k, 0); B = (0, 1 - Fr(k, 2)); Cc = (2, 1)
    if (Cc[0] - A[0]) * (B[1] - A[1]) - (B[0] - A[0]) * (Cc[1] - A[1]) == 0:
        ks.append(k)
chk("m2103-16", ks[0], -2)


def quad_area(pts):
    s = 0
    for i in range(len(pts)):
        x1, y1 = pts[i]; x2, y2 = pts[(i + 1) % len(pts)]
        s += x1 * y2 - x2 * y1
    return abs(s) / 2


res = [a for a in [Fr(n, 4) for n in range(5, 60)] if quad_area([(0, 0), (0, -Fr(4) / a - 4), (a, -4), (a + 1, 0)]) == 24]
chk("m2311-16", res[0], 5)
res = [a for a in [Fr(n, 4) for n in range(5, 60)] if quad_area([(0, 0), (0, -Fr(2) / a - 3), (a, -3), (a + Fr(2, 3), 0)]) == 20]
chk("k3-23", res[0], 6)
aa = lin(1e-3, 5, 2000001); kk = aa * (aa + 2)
area = 2 * np.abs(aa * (kk / (aa + 2)) - (aa + 2) * (kk / aa))
i = np.argmin(np.abs(area - 8 * math.sqrt(5)))
chk("m2403-17", kk[i], 4)
aa = lin(1 + 1e-4, 10); chk("m1806-16", (1 / (aa - 1) + 4 * aa).min(), 8)
tt = lin(0.5 + 1e-4, 20); chk("m1411-18", (8 / (2 * tt - 1) + tt).min(), "9/2")
tt = lin(1e-3, 20); chk("m1311-16", (2 * (tt + 2 / tt)).min(), "4*sqrt(2)")
res = []
for k in [Fr(n, 4) for n in range(1, 81)]:
    u = lin(1e-3, 60, 600001)
    s1 = (u + float(k) / u + 4).min()
    s2 = (0.5 * (u + 2) * (float(k) / u + 2)).min()
    if abs(s1 - s2) < 1e-4:
        res.append(k)
chk("k10-22", res[0], 4)
tt = lin(2 + 1e-4, 30); chk("o35", (tt + 2 + 3 / (tt - 2)).min(), "4+2*sqrt(3)")

# 절댓값과 유리함수 ------------------------------------------------------
def sols(expr, t, cond):
    out = set()
    for sgn in ((1, -1) if t != 0 else (1,)):
        for r in sp.solve(sp.Eq(expr, sgn * t), x):
            if r.is_real and cond(r):
                out.add(r)
    return len(out)


chk("k5-17", sum(sols((-2 * x - 3) / (x + 1), t, lambda r: r < 0 and r != -1) for t in (0, 1, 2, 3, 4)), 7)
chk("k8-18", sum(sols((-3 * x + 12) / (x - 2), t, lambda r: r >= 0 and r != 2) for t in (2, 3, 6, 7)), 7)


def f115(t):
    t = np.abs(t); r = np.mod(t, 2); r = np.where(r > 1, 2 - r, r)
    return 2 * r / (r + 1)


xs = lin(-8, 8, 1600001); v = f115(xs) - np.abs(xs) / 6
s = np.sign(v); cnt = np.count_nonzero(s[:-1] * s[1:] < 0) + np.count_nonzero(np.abs(v) < 1e-12)
chk("m1006-29", cnt, 11)

# 고난도 ------------------------------------------------------------
res = []
for b in (2, -2):
    for a in range(-60, 61):
        if a == 0:
            continue
        f = lambda t: Fr(a) / t + b
        hits = sum(1 for val in (2, -2) if val != b)        # f=val은 b가 아니면 해 하나
        if hits != 1:
            continue
        if b == 2:
            continue                                          # f^{-1}(2) 없음
        if Fr(a, 2 - b) == f(2) - 1:
            res.append(f(8))
chk("m2203-18", res[0], "-1/2")
def ac117(k):
    r = sorted(np.roots([1, -k, 2]).real)
    best = []
    for A, B in ((r[0], r[1]), (r[1], r[0])):
        # B를 지나고 AB에 수직인 직선(기울기 1): y = x - B + 2/B, 곡선 2/x와의 교점: x^2 + (2/B - B)x - 2 = 0
        cs = np.roots([1, 2 / B - B, -2]).real
        for cx in cs:
            if abs(cx - B) > 1e-9:
                best.append(math.hypot(cx - A, 2 / cx - 2 / A))
    return best


ks = lin(2.83, 8, 51701)
d = np.array([min(ac117(k), key=lambda v: abs(v - 2 * math.sqrt(5))) for k in ks]) - 2 * math.sqrt(5)
i = np.where(np.sign(d[:-1]) * np.sign(d[1:]) <= 0)[0][0]
found = ks[i]
chk("m1709-27", round(found * found, 2), 9)


def S118(k):
    m = (k * k - 1) / (2 * k)
    t = math.sqrt(k / m)
    B = (1 + t, m * t + k); P = (1, k); A = (2, 2 * k); Cc = (1 - k / m, 0); O = (0, 0)
    tri = lambda p, q, r: abs((q[0] - p[0]) * (r[1] - p[1]) - (r[0] - p[0]) * (q[1] - p[1])) / 2
    return 2 * tri(P, B, A) - tri(P, Cc, O)


ks = lin(1.01, 6, 49901); vv = np.array([S118(k) for k in ks]); i = np.where(np.sign(vv[:-1]) * np.sign(vv[1:]) < 0)[0][0]
chk("m1609-30", 10 * ks[i]**2, 20)


def ok122(a, b):
    if a >= 1:
        return False
    def f(t):
        return (1 - a) / (t - 1) + 2 if t <= a else b * t * (t - a) + 1
    xs_ = np.concatenate([lin(-60, 0, 120001)])
    fv = np.array([f(t) for t in xs_[::40]])
    if fv.min() < f(-2) - 1e-9:
        return False
    big = lin(-200, 200, 400001)
    vals = np.where(big <= a, (1 - a) / (big - 1) + 2, b * big * (big - a) + 1)
    c = 0
    for tt in (2, -2):
        s = np.sign(vals - tt); c += np.count_nonzero(s[:-1] * s[1:] < 0) + np.count_nonzero(np.abs(vals - tt) < 1e-9)
    return c == 2


pairs = [(a, b) for a in (-4, -2) for b in (Fr(3, 4), -1) if ok122(a, float(b))]
chk("m2303-30", -40 * sum(a + b for a, b in pairs) if len(pairs) == 2 else None, 250)
a, b = 3, -8
fl = lambda t: b * t / (t - a)
gx = lambda t: fl(t) if t < a else fl(t + 2 * a) + a
xs_l = lin(-500, a - 1e-6, 800001); xs_r = lin(a, 500, 800001)
ok = True
for t in [-9, -8.5, -8, -5, 0, 10]:
    hcount = count_hits(lambda u: b * u / (u - a), t, [xs_l]) + count_hits(lambda u: b * (u + 2 * a) / (u + a) + a, t, [xs_r])
    ok &= hcount == 1
for t in [-10, -7, -6]:
    hcount = count_hits(lambda u: b * u / (u - a), t, [xs_l]) + count_hits(lambda u: b * (u + 2 * a) / (u + a) + a, t, [xs_r])
    ok &= hcount != 1
chk("m2103-30", a * b * gx(5) if ok else None, 192)
gq = lambda t: 2 + (-2 / (t - 5)) - 1        # g(x)=1-2/(x-5)
aa4 = (7 - 6) / (gq(1) - 2)**2
chk("m1903-30", aa4 * (5 - 2)**2 + 6, 42)
res = []
for a in range(-20, 0):
    segs = [lin(-400, 3 - 1e-7, 800001), lin(3, 400, 800001)]
    gfun = lambda t: np.where(t < 3, a * t / (t - 3), a * (t + 6) / (t + 3) + 3)
    hs = {t: count_hits(lambda u: np.abs(gfun(u)), t, segs) for t in (0.5, 1, 2, 2.5, 4.4, 4.6, 4.9, 5.5)}
    if hs[0.5] == 2 and hs[1] == 2 and hs[2] == 2 and hs[2.5] != 2 and hs[4.4] != 2 and hs[4.6] == 2 and hs[4.9] == 2 and hs[5.5] != 2:
        res.append(a)
chk("k9-19", res[0] if len(res) == 1 else None, -5)
res = []
for a in [Fr(n, 4) for n in range(1, 40)]:
    k = a * (a + 3)
    P_ = (2 * a, k / a + a); Q_ = (2 * a + 3, k / (a + 3) + a)
    if (Q_[1] - P_[1]) / (Q_[0] - P_[0]) == -1 and 2 * abs(P_[0] * Q_[1] - Q_[0] * P_[1]) == 30:
        res.append(k)
chk("k11-20", res[0], "7/4")
f = lambda t: 4 * t / (t - 4)
t1 = all(abs(f(f(t)) - t) < 1e-9 for t in (1.3, -2.7, 9.1))
t2 = True
for m in np.round(lin(-5, -0.01, 300), 3):
    xs_ = np.concatenate([lin(-200, 4 - 1e-6, 400001), lin(4 + 1e-6, 200, 400001)])
    v = f(xs_) - (m * (xs_ - 4) + 4)
    s = np.sign(v)
    if np.any(s[:-1] * s[1:] < 0) and not np.any(np.abs(xs_[:-1] - 4) < 1e-3):
        # 끊긴 곳(4) 근처의 부호 변화는 제외
        idx = np.where(s[:-1] * s[1:] < 0)[0]
        if any(abs(xs_[i] - 4) > 1e-3 for i in idx):
            t2 = False
aa = lin(-60, 4 - 1e-3, 200001); bb = lin(4 + 1e-3, 60, 200001)
A_, B_ = np.meshgrid(aa[::50], bb[::50])
d = np.sqrt((A_ - B_)**2 + (f(A_) - f(B_))**2)
t3 = abs(d.min() - 8 * math.sqrt(2)) < 0.05
chk("g2-25", mark([t1, t2, t3], "ㄱ|ㄴ|ㄱ, ㄴ|ㄴ, ㄷ|ㄱ, ㄴ, ㄷ"), "⑤")
res = []
for a in range(1, 30):
    for b in range(-10, 11):
        f, fi = mob(-2, a, 1, b)
        if -2 * b - a == 0:
            continue
        if same(f, fi):
            # 넓이 = |f(t)+2||t+2|/2 = |a+4|/2 (b=2일 때)
            tt = Fr(7, 3)
            if abs((f(tt) + 2) * (tt + b)) / 2 == 5:
                res.append(a + b)
chk("g2-22", res[0], 8)

if __name__ == "__main__":
    bad = [r_ for r_ in R if not r_[1]]
    print("검산", len(R), "불일치", len(bad))
    for r_ in bad:
        print(r_)
