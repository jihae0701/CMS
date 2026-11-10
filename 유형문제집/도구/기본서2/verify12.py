# -*- coding: utf-8 -*-
"""공통수학2 기본서 12단원 무리식과 무리함수 검산: 문항마다 답을 따로 계산해 data12.py의 답과 맞춘다.
python verify12.py
"""
import sys, os, re, math
import numpy as np
import sympy as sp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data12

R = {}
x, t = sp.symbols("x t", real=True)
sq = np.sqrt


def lin(a, b, n=400001):
    return np.linspace(a, b, n)


def nsol(expr_l, expr_r, dom, var=x):
    """expr_l=expr_r의 실근(정의역 조건 dom)을 정확히 센다: 제곱 전 식으로 다시 확인"""
    sols = sp.solve(sp.Eq(expr_l, expr_r), var)
    out = []
    for s in sols:
        s = sp.nsimplify(s)
        if s.is_real and dom(s) and abs(float(expr_l.subs(var, s) - expr_r.subs(var, s))) < 1e-9:
            out.append(s)
    return sorted(set(out), key=float)


def quadrants(xs, ys):
    ok = (np.abs(xs) > 1e-9) & (np.abs(ys) > 1e-9) & np.isfinite(ys)
    X, Y = xs[ok] > 0, ys[ok] > 0
    return {(a, b) for a in (True, False) for b in (True, False) if np.any((X == a) & (Y == b))}


# 01 ------------------------------------------------------------------
cnt = 0
for a in range(-50, 51):
    xs = lin(-100, 100, 200001)
    if np.all(a * xs**2 - 2 * a * xs + 6 >= -1e-12):
        cnt += 1
R["o36"] = cnt
ok = all(int(2 * n / (math.sqrt(n * n + 2 * n) - n)) == 2 * n for n in range(1, 200))
R["g2-33"] = "$2n$" if ok else "?"
def l_(n):
    return math.hypot(1, math.sqrt(2 * (n + 1) + 1)) - math.hypot(1, math.sqrt(2 * (n + 1) - 1))
m, s = 0, 0.0
while s <= 2 * math.sqrt(2):
    m += 1; s += l_(m)
R["g2-35"] = m

# 02 ------------------------------------------------------------------
xs = lin(-20, -3, 1001)
for a in range(-10, 11):
    for mm in range(-10, 11):
        for n in range(-10, 11):
            if np.allclose(a * sq(-(xs - mm)) - 6 + n, sq(-4 * xs - 12)):
                R["b5"] = a + mm + n
a_, b_, c_ = sp.symbols("a b c")
# y=sqrt(a(x-b)+1)+1 -> y축 대칭: sqrt(a(-x-b)+1)+1 == sqrt(-4x-1)+c
sol = sp.solve([sp.Eq(-a_, -4), sp.Eq(-a_ * b_ + 1, -1), sp.Eq(1, c_)], [a_, b_, c_], dict=True)[0]
R["o16"] = sol[a_] + sol[b_] + sol[c_]
xs = lin(-50, 3, 1001)
for a in range(-10, 11):
    for b in range(-10, 11):
        if np.allclose(2 * sq(-(xs - a)) + b, sq(-4 * xs + 12) + 5):
            R["g1-24"] = a + b

# 03 ------------------------------------------------------------------
xs = lin(-50, 1, 2000001)
cand = []
for a in np.linspace(0.01, 3, 2991):
    pass
a = math.sqrt(2) / 2
q = quadrants(xs, 1 - a * sq(2 - 2 * xs))
assert len(q) == 2
for a in (0.5, 0.8, 1.0):
    assert len(quadrants(xs, 1 - a * sq(2 - 2 * xs))) == 3
R["b13"] = a if False else math.sqrt(2) / 2
# o46: 사분면 개수를 a에 따라 조사
a46 = (9 - math.sqrt(17)) / 2
def nq46(a):
    s0 = -a / 2
    xs = [s0 + 1e-14 * max(1, abs(s0))] + list(lin(s0, s0 + 1e4, 200001))
    x0 = ((4 - a)**2 - a) / 2 if a <= 4 else None          # x절편
    for c in (0.0, x0):
        if c is not None:
            xs += [c - 1e-11, c + 1e-11]
    xs = np.array([u for u in xs if u >= s0])
    ys = sq(2 * xs + a) + a - 4
    ok = (xs != 0) & (np.abs(ys) > 1e-13)
    return len({(u > 0, v > 0) for u, v in zip(xs[ok], ys[ok])})
good = [a for a in np.round(np.arange(-3, 7, 0.05), 3) if nq46(a) == 2]
assert all(a <= 0 or a >= 4 for a in good) and min(a for a in good if a >= 4) == 4 and max(a for a in good if a <= 0) == 0
assert nq46(a46) == 2 and nq46(a46 + 1e-4) == 3 and nq46(a46 - 1e-4) == 3
R["o46"] = "$a leq 0$ 또는 $a= {9- sqrt {17}} over {2}$ 또는 $a geq 4$"
# g2-37
okA = okB = okC = True
for k in (-3, -1, -0.2, 0.3, 2):
    d = lin(-1 / k, -1 / k + 50, 200001) if k > 0 else lin(-1 / k - 50, -1 / k, 200001)
    y = 4 - sq(k * d + 1)
    okA &= abs(y.max() - 4) < 1e-9
    if k < 0:
        okC &= (False, True) not in {(a > 0, b > 0) for a, b in zip(d[np.abs(d) > 1e-9], y[np.abs(d) > 1e-9]) if abs(b) > 1e-9} if False else not np.any((d > 1e-9) & (y < -1e-9))
okB = False   # k>0이면 정의역은 x >= -1/k
R["g2-37"] = ", ".join(n for n, v in zip("ㄱㄴㄷ", (okA, okB, okC)) if v)

# 04 ------------------------------------------------------------------
for a in range(-20, 0):
    b = -4 * a
    if abs(-math.sqrt(b) + 2 + 2) < 1e-12:
        R["b12"] = -math.sqrt(a * -5 + b) + 2
a, b = -2, 1
assert math.isclose(math.sqrt(a * 2 + 4), 0)
R["o15"] = a + math.sqrt(a * b + 4) + b
s_ = [r for r in sp.solve(sp.Eq(sp.sqrt(6 - 2 * x), 2 * x), x) if r <= 3]
R["g1-31"] = s_[0]

# 05 ------------------------------------------------------------------
for a in range(-10, 30):
    xs = lin(-3, 2, 5001)
    if a - 2 >= 0 and abs((sq(a - xs) - 1).max() - 2) < 1e-9:
        R["b20"] = (sq(a - xs) - 1).min()
xs = lin(2, 200, 200001); fv = 5 - sq(3 * xs - 6)
aa, bb = 2, fv.max()
xs = lin(aa, bb, 200001)
R["b21"] = (3 - sq(6 - xs)).max()
best = None
for h in np.linspace(1e-6, math.sqrt(2) - 1e-6, 2000001)[::50]:
    pass
hs = lin(1e-9, math.sqrt(2) - 1e-9, 2000001)
per = 2 * (hs + (4 - 2 * hs**2)); i = per.argmax()
l_, S_ = per[i], hs[i] * (4 - 2 * hs[i]**2)
R["g3-20"] = 8 * S_ / l_

# 06 ------------------------------------------------------------------
def cnt26(k):
    return len(nsol(-sp.sqrt(2 * x + 4) + 1, -x + k, lambda s: s >= -2))
ks = [sp.Rational(n, 8) for n in range(-24, 8)]
good = [k for k in ks if cnt26(k) == 2]
assert min(good) == sp.Rational(-11, 8) and max(good) == -1 and cnt26(sp.Rational(-3, 2)) == 1
R["b26"] = "$- {3} over {2} <k leq -1$"
def hit27(m):
    return len(nsol(sp.sqrt(2 * x - 4) + 1, m * x + 1, lambda s: s >= 2)) > 0
ms = [sp.Rational(n, 16) for n in range(-8, 16)]
good = [m for m in ms if hit27(m)]
assert min(good) == 0 and max(good) == sp.Rational(1, 2)
R["b27"] = "$0 leq m leq {1} over {2}$"
def n52(k):
    r1 = nsol(2 * sp.sqrt(x), 2 * x + k, lambda s: s >= 0)
    r2 = nsol(sp.sqrt(-2 * x), 2 * x + k, lambda s: s < 0)
    return len(r1) + len(r2)
ks = [sp.Rational(n, 40) for n in range(-20, 40)]
good = [k for k in ks if n52(k) == 3]
assert min(good) == sp.Rational(1, 40) and max(good) == sp.Rational(19, 40) and n52(0) != 3 and n52(sp.Rational(1, 2)) != 3
R["g2-52"] = sp.Rational(0) + sp.Rational(1, 2)

# 07 ------------------------------------------------------------------
fi = lambda u: u * u - 2 * u + 2
for a in range(-5, 6):
    for b in range(-5, 6):
        if a > -3 and all(abs(fi(math.sqrt(u + a) + b) - u) < 1e-9 for u in (3, 5, 10, 17)) and all(math.sqrt(u + a) + b >= 1 for u in (3, 5)):
            R["b30"] = fi(b - a)
# o57: f(x) 일대일대응 -> a=2
a = 2
R["o57"] = sp.solve(sp.sqrt(2 * x - 4) + 1 - 2, x)[0] + sp.solve(-sp.sqrt(a - x) + 1 + 2, x)[0]
xs = lin(-3 + 1e-9, 1e6, 2000001)
fv = sq(xs + 3) - 1; gv = (2 * fv + 4) / (fv + 3)
assert gv.min() > 1 and gv.min() < 1 + 1e-3 and gv.max() < 2 and gv.max() > 1.99
R["g2-44"] = "$" + data12.C("1<y<2", "y") + "$"

# 08 ------------------------------------------------------------------
k = sp.symbols("k")
for kv in [sp.Rational(n, 4) for n in range(-8, 9)]:
    r = nsol(sp.sqrt(4 * x - 3) + kv, x, lambda s: s >= sp.Rational(3, 4))
    if len(r) == 2 and sp.simplify(sp.sqrt(2) * (r[1] - r[0]) - 2 * sp.sqrt(6)) == 0:
        R["b35"] = kv
tot = 0
for kv in range(-30, 30):
    r = nsol(sp.sqrt(4 * x - kv) - 2, x, lambda s: s >= sp.Rational(kv, 4) and s >= -2)
    if len(r) == 2:
        tot += kv
R["b40"] = tot
for n in range(1, 20):
    f = sp.sqrt(x + n * n) - n
    r = nsol(f, -x + 4 * n + 6, lambda s: s >= 0)
    if len(r) == 1:
        a = r[0]; b = f.subs(x, a)
        if sp.simplify(sp.sqrt(2) * abs(a - b) - 22 * sp.sqrt(2)) == 0:
            R["g2-49"] = n

# 09 ------------------------------------------------------------------
a_, b_ = sp.symbols("a b", real=True)
sols = sp.solve([sp.Eq(b_, sp.sqrt(13 - 4 * a_)), sp.Eq(a_, sp.sqrt(13 - 4 * b_))], [a_, b_], dict=True)
off = [s for s in sols if s[a_] != s[b_]]
R["b43"] = off[0][a_] + off[0][b_]
A_, B_ = off[0], off[1]
R["b46"] = abs(A_[a_] * B_[b_] - A_[b_] * B_[a_]) / 2
best = 0
for kv in lin(-4, 2, 600001)[::10]:
    xa = (2 * kv - 1 - math.sqrt(max((2 * kv - 1)**2 - 4 * (kv * kv - 4), 0))) / 2   # sqrt(x+4)=-x+k 의 근(작은 쪽)
    cands = np.roots([1, -(2 * kv + 1), kv * kv - 4])
    pts = [c.real for c in cands if abs(c.imag) < 1e-12 and c.real >= -4 and -c.real + kv >= -1e-12]
    cb = np.roots([1, 1, -4 - kv]); ptb = [c.real for c in cb if abs(c.imag) < 1e-12 and c.real >= 0]
    if pts and ptb:
        xa, xb = pts[0], ptb[0]
        best = max(best, math.hypot(xa - xb, (-xa + kv) - (-xb + kv)))
R["g2-57"] = best

# 10 ------------------------------------------------------------------
xs = lin(3 + 1e-9, 1e6, 2000001); rv = (2 * xs + 3) / (xs - 2)
for a in range(0, 20):
    if a > rv.max() - 1e-3 and a < rv.max() + 1e-3:
        f2 = math.sqrt(3 - 2) + a
        k_ = sp.solve(sp.Eq((2 * x + 3) / (x - 2), sp.Rational(30, int(f2))), x)
        R["b41"] = [v for v in k_ if v > 3][0]
kk = sp.symbols("kk", positive=True)
a0 = sp.Rational(3)   # 임의의 양수 a로 계산해도 k는 같다
A = (a0, sp.sqrt(a0)); B = (a0, sp.sqrt(kk * a0)); C_ = (kk * a0, sp.sqrt(kk * a0)); D = (kk * a0, sp.sqrt(kk * kk * a0))
OAB = (B[1] - A[1]) * a0 / 2
BCD = (C_[0] - B[0]) * (D[1] - C_[1]) / 2
R["o55"] = [v for v in sp.solve(sp.Eq(BCD, sp.sqrt(2) * OAB), kk) if v > 1][0]
a = sp.symbols("a", positive=True)
R["g2-38"] = sp.solve(sp.Eq(3 * sp.sqrt(a), sp.Rational(9, 2) * a - a), a)[0]

# STEP3 ---------------------------------------------------------------
def hit47(m):
    r = nsol(sp.sqrt(2 * x - x**2), m * x + m - 1, lambda s: 0 <= s <= 2)
    return len(r) > 0
ms = [sp.Rational(n, 12) for n in range(-6, 24)]
good = [m for m in ms if hit47(m)]
assert min(good) == sp.Rational(4, 12) and max(good) == sp.Rational(16, 12)
R["b47"] = "${1} over {3} leq m leq {4} over {3}$"
cnt = 0
for a in range(3, 100000):
    v = 7 - math.sqrt(math.sqrt(3 * a - 5) + 2)
    if v >= 1 - 1e-12 and abs(v - round(v)) < 1e-9:
        cnt += 1
R["m188"] = cnt
xs = lin(-4, 7, 2000001); fv = sq(21 - 3 * xs) + sq(12 + 3 * xs)
R["m190"] = fv.max() / fv.min()
# m195: 몇 개의 (a, b)에서 교점 수를 세어 조건과 대조
def n195(a, b):
    f = sp.sqrt(a * x + b)
    pts = set()
    # y=x 위
    for r in nsol(f, x, lambda s: a * s + b >= 0):
        pts.add((round(float(r), 9), round(float(r), 9)))
    # (p,q),(q,p): q=f(p), p=f(q)
    p, q = sp.symbols("p q", real=True)
    for s in sp.solve([sp.Eq(q**2, a * p + b), sp.Eq(p**2, a * q + b)], [p, q], dict=True):
        if s[p].is_real and s[q].is_real and s[p] >= 0 and s[q] >= 0:
            pts.add((round(float(s[p]), 9), round(float(s[q]), 9)))
    return len(pts)
ok195 = True
for a in (-2, -4, 3):
    for b in (sp.Rational(a * a * 3, 4), sp.Rational(a * a * 3, 4) + sp.Rational(1, 4), a * a, a * a + 1, 1):
        exp3 = a < 0 and sp.Rational(3, 4) * a * a < b <= a * a
        ok195 &= ((n195(a, b) == 3) == exp3)
assert ok195
R["m195"] = "$a<0$, ${3} over {4} a^{2} <b leq a^{2}$"
xs = lin(-1e6, -2 - 1e-9, 2000001); rv = (3 * xs - 1) / (xs + 1)
a = round(rv.max())
fi6 = sp.solve(sp.Eq((3 * x - 1) / (x + 1), 6), x)[0]
fb = sp.Rational(-21) / fi6
R["m198"] = sp.solve(sp.Eq(sp.sqrt(x + 2) + a, fb), x)[0]
a2 = sp.symbols("a2")
aa = sp.solve(sp.Eq(a2 * (2 - sp.Rational(3, 4))**2 + sp.Rational(1, 8), -3), a2)[0]
fq = sp.expand(aa * (x - sp.Rational(3, 4))**2 + sp.Rational(1, 8))
A2, B2, C2 = [fq.coeff(x, i) for i in (2, 1, 0)]
g = lambda u: A2 * sp.sqrt(-u + B2) + C2
c1 = g(-1) < 0                                   # 제3사분면
c2 = False                                       # 정의역 x <= B2
al, be = sorted(sp.solve(fq, x))
vals = [g(al), g(be)]
c3 = sp.simplify(max(vals) - min(vals) - (sp.sqrt(10) - 2 * sp.sqrt(2))) == 0
R["m199"] = ", ".join(n for n, v in zip("ㄱㄴㄷ", (c1, c2, c3)) if v)
f = lambda u: (u - 3) / (u + 1)
def fn(n, u):
    v = sp.Rational(u)
    for _ in range(n):
        v = f(v)
    return v
R["m202"] = fn(1010, 2) + fn(2016, 2)
# o60
res = []
XS = lin(-60, 60, 120001)
for a in range(-10, 11):
    for b in range(-6, 7):
        fx = lambda u: np.sqrt(np.maximum(u - a, 0)) - b
        g_ = np.where(XS < a, -(np.sqrt(np.maximum(a - XS, 0)) - b) + abs(b), np.abs(fx(XS)) + b)
        def h(tv):
            d = g_ - tv
            return int(np.count_nonzero(np.sign(d[:-1]) * np.sign(d[1:]) < 0) + np.count_nonzero(np.abs(d) < 1e-12))
        if sum(1 for tv in range(-20, 21) if h(tv + 1e-7) == 3 or h(tv) == 3) == 0:
            continue
        T3 = [tv for tv in range(-20, 21) if h(tv) == 3]
        if len(T3) != 2:
            continue
        T2 = [tv for tv in np.arange(-20, 21, 0.5) if h(tv) == 2]
        xsol = [XS[i] for i in range(len(XS)) if any(abs(g_[i] - tv) < 2e-3 for tv in T2)]
        if xsol and abs(min(xsol) + 4) < 0.05:
            res.append(a + b)
R["o60"] = res[0] if len(set(res)) == 1 else res
# o61
def fA(a):
    return len(nsol(sp.sqrt(2 + x), x + a, lambda s: s >= -2))
def gB(a):
    return len(nsol(sp.sqrt(2 - x), x + a, lambda s: s <= 2))
As = [sp.Rational(n, 8) for n in range(-40, 40)]
A1 = [a for a in As if fA(a) == 1]
c1 = all((a == sp.Rational(9, 4) or a < 2) == (a in A1) for a in As)
c2 = all(((fA(a) + gB(a)) == 2) == (a == sp.Rational(9, 4) or -2 < a < 2) for a in As)
c3 = all(((fA(a) + gB(a)) == 3) == (2 <= a < sp.Rational(9, 4)) for a in As)
R["o61"] = ", ".join(n for n, v in zip("ㄱㄴㄷ", (c1, c2, c3)) if v)
# g3-17
res = []
for n in range(1, 30):
    a = math.sqrt(2 * n - 2) + 3
    xl = lin(-200, 2, 400001); xr = lin(2 + 1e-9, 2000, 2000001)
    fl = sq(-xl + 2 * n) + 3; fr = -4 / (xr + n) + a
    meet = np.any(np.sign(fl - 2 * xl)[:-1] * np.sign(fl - 2 * xl)[1:] <= 0) or np.any(np.sign(fr - 2 * xr)[:-1] * np.sign(fr - 2 * xr)[1:] <= 0)
    if not meet:
        res.append((2 * a - 3 * n)**2)
R["g3-17"] = res[0] if len(res) == 1 else res


# 대조 ---------------------------------------------------------------
def val(s):
    s = s.replace(" ", "").replace("it-", "-")
    s = re.sub(r"sqrt\{([^{}]*)\}", r"sqrt(\1)", s)
    s = re.sub(r"(\d)(sqrt)", r"\1*\2", s)
    s = re.sub(r"\{([^{}]*)\}over\{([^{}]*)\}", r"((\1)/(\2))", s)
    return eval(s, {"sqrt": math.sqrt})


bad = 0
items = [p for _, _, ps in data12.TYPES for p in ps] + data12.STEP3
for p in items:
    got, exp = R.get(p["src"]), p["ans"]
    if got is None:
        print("검산 없음", p["src"], exp); bad += 1; continue
    if isinstance(got, str):
        ok = got.replace(" ", "") == exp.replace(" ", "").replace("it-", "-")
    elif isinstance(got, list):
        ok = False
    else:
        e = val(exp)
        ok = abs(float(got) - e) <= 1e-3 * max(1, abs(e))
    if not ok:
        print("불일치", p["src"], "자료", exp, "검산", got); bad += 1
print("문항", len(items), "불일치", bad)
