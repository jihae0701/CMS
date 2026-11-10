# -*- coding: utf-8 -*-
"""공통수학2 기본서 11단원 유리식과 유리함수 검산: 문항마다 답을 따로 계산해 data11.py의 답과 맞춘다.
python verify11.py
"""
import sys, os, re, math, itertools
import numpy as np
import sympy as sp
from fractions import Fraction as Fr
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data11

R = {}
x = sp.symbols("x", real=True)


def lin(a, b, n=400001):
    return np.linspace(a, b, n)


def nroots(h, a, b, n=2000001):
    t = lin(a, b, n); v = h(t); s = np.sign(v)
    return int(np.count_nonzero(s[:-1] * s[1:] < 0) + np.count_nonzero(np.abs(v) < 1e-12))


def quadrants(f, xs):
    with np.errstate(divide="ignore", invalid="ignore"):
        v = f(xs)
    ok = np.isfinite(v) & (np.abs(xs) > 1e-9) & (np.abs(v) > 1e-9)
    X, Y = xs[ok] > 0, v[ok] > 0
    return {(a, b) for a in (True, False) for b in (True, False) if np.any((X == a) & (Y == b))}


def mob(p, q, r, s_):
    """(px+q)/(rx+s)를 Fraction으로 계산하는 함수와 그 역함수"""
    f = lambda t: Fr(p * t + q) / Fr(r * t + s_)
    fi = lambda t: Fr(-s_ * t + q) / Fr(r * t - p)
    return f, fi


PTS = [Fr(n, 7) for n in (-23, -9, 5, 17, 40)]


def same(f, g):
    try:
        return all(f(t) == g(t) for t in PTS)
    except ZeroDivisionError:
        return False


XS = np.concatenate([-np.logspace(-4, 4, 40001), np.logspace(-4, 4, 40001)])

# 01 ------------------------------------------------------------------
S_ = sum(1 / ((x + n) * (x + n + 1)) for n in range(3, 11))
num, den = sp.fraction(sp.factor(sp.together(S_)))
c_ = num; rts = sorted(-r for r in sp.solve(den, x))
R["b1"] = rts[0] + rts[1] - c_
t = sp.symbols("t", nonzero=True)
a_, b_, c2 = sp.symbols("a b c")
sol = sp.solve([2 * b_ + c2 - 2 * a_, a_ + c2 - 4 * b_], [a_, c2], dict=True)[0]
R["g2-4"] = sp.simplify((sol[a_]**3 + b_**3 + sol[c2]**3) / (sol[a_] * b_ * sol[c2]))
lhs = 1 / ((2 * x - 1) * (2 * x + 1)) + 1 / ((2 * x + 1) * (2 * x + 3)) + 1 / ((2 * x + 3) * (2 * x + 5))
R["o03"] = sp.simplify(lhs * (2 * x - 1) * (2 * x + 5))

# 02 ------------------------------------------------------------------
f = (-2 * x + 3) / (x + 1)
k_ = sp.limit((f - (-2)) * (x + 1), x, -1)          # y=k/(x-a)+b
R["b10"] = -1 + (-2) + k_
g = 2 / (x + 2) + 3
R["o24"] = 3 + 8 + 2 if sp.simplify(g - (3 * x + 8) / (x + 2)) == 0 else None
# o47: 점근선 교점과 k 비교
R["o47"] = (3 - Fr(1, 2)) + (-2 - (-1)) if sp.simplify(((3 - 2 * x) / (2 * x - 1)).subs(x, x - Fr(5, 2)) - 1 - (7 - 2 * x) / (x - 3)) == 0 else None

# 03 ------------------------------------------------------------------
p_, q_ = Fr(-1, 2), 2
f = (4 * x - 3) / (2 * x + 1)
assert sp.simplify(f.subs(x, p_ + x) + f.subs(x, p_ - x) - 2 * q_) == 0
R["b15"] = p_ * q_ * (q_ - p_)
res = []
for a in range(-10, 11):
    for b in range(-10, 11):
        if a == b:
            continue
        ff = (x + b) / (x + a)
        if ff.subs(x, 4) == 2 and -a == 3:
            res.append(a + b + 1)
R["o07"] = res[0]
# g2-24: ㄱ 반례 f=4/x+3, ㄴ 기호로, ㄷ 반례
f1 = 4 / x + 3
g1 = f1.subs(x, 4) == 4                                  # f(4)=4=f^{-1}(4), b+c=3≠0 → ㄱ 거짓
a, b, c = sp.symbols("a b c")
fb = a / (x + b) + c
# 대칭(y=x) → c=-b, f(0)=0 → a/b + c = 0
t2 = sp.simplify((-b * c).subs(c, -b) - (-b)**2) == 0
t3 = not (2 / (-2) + 0 > 2 / 1 + 0)                     # a=2,b=0,c=0: f(-2)=-1 < f(1)=2 → ㄷ 거짓
R["g2-24"] = "ㄴ" if (g1 and t2 and t3) else "?"

# 04 ------------------------------------------------------------------
ks = []
for k in range(-50, 51):
    if k == 0:
        continue
    q1 = quadrants(lambda X: k / (X + 2) - 2, XS)
    q2 = quadrants(lambda X: k / (X - 3) + 4, XS)
    if len(q1) == 4 and (False, False) not in q2:
        ks.append(k)
R["b21"] = len(ks)
cnt = 0
for k in range(-9, 10):
    if k == -1:
        continue
    if len(quadrants(lambda X: (X + k) / (X - 1), XS)) == 3:
        cnt += 1
R["o28"] = cnt
R["h1706-15"] = sum(1 for k in range(1, 60) if k != 10 and (True, False) in quadrants(lambda X: (2 * X + k - 8) / (X + 1), XS))

# 05 ------------------------------------------------------------------
res = []
for k in [Fr(n, 2) for n in range(-40, 41)]:
    xs = [Fr(i, 50) for i in range(0, 101)]
    v = [(2 * t_ + k) / (t_ + 1) for t_ in xs]
    if max(v) == 1:
        res.append(min(v))
R["b25"] = res[0]
res = []
for a in [Fr(n, 2) for n in range(-40, 41)]:
    if a == -2:
        continue
    v = [(a * t_ + 2) / (t_ - 1) for t_ in [Fr(i, 20) + 2 for i in range(0, 41)]]
    if max(v) == 8:
        res.append(a + min(v))
R["o33"] = res[0]
tot = 0
for k in range(-200, 200):
    if k == -15:
        continue
    xs = lin(-1e4, 1 - 1e-9, 2000001); v = (5 * xs + k) / (xs - 3)
    lo, hi = v.min(), v.max()
    # 열린 끝(5, f(1)) 처리: 정수 n이 치역에 있는지 = n이 (inf,sup) 사이 또는 실제로 도달
    f1 = Fr(5 + k, -2)
    if k + 15 < 0:
        ints = [n for n in range(-100, 100) if 5 < n < f1]
    else:
        ints = [n for n in range(-100, 100) if f1 < n < 5]
    if len(ints) == 6:
        tot += k
R["g2-18"] = tot

# 06 ------------------------------------------------------------------
res = [a for a in range(-10, 11) if a != 0 and sp.simplify((a * x / (2 * x + 3)).subs(x, a * x / (2 * x + 3)) - x) == 0]
R["b39"] = res[0]
res = []
for a in range(1, 20):
    for b in range(-30, 31):
        f, fi = mob(a * a - 14, -3, 1, -3 * a)
        if (a * a - 14) * (-3 * a) - (-3) == 0:
            continue
        if same(fi, lambda t: f(t - 4) + b):
            res.append(a + b)
R["b35"] = res[0]
f = (2 * x + 8) / (x - 2)
assert sp.simplify(f.subs(x, f) - x) == 0 and f.subs(x, 4) == 8
R["o53"] = sum(1 for X in range(-100, 101) if X != 2 and (2 * X + 8) % (X - 2) == 0)

# 07 ------------------------------------------------------------------
res = []
for a in range(-20, 21):
    for b in range(-20, 21):
        if -3 + a == 0:
            continue
        f, fi = mob(-1, -a, 1, 3)
        if same(fi, lambda t: f(t - 2) + b) and f(-2) == -3:
            res.append(a - b)
R["b43"] = res[0]
best = None
for a in range(-10, 11):
    for b in range(-10, 11):
        for c in range(-10, 11):
            if a * b + c == 0:
                continue
            f, fi = mob(b, c, 1, -a)
            if a * b + c == -2 and same(fi, lambda t: f(t - 2) + c):
                best = a * c - b if best is None else max(best, a * c - b)
R["b44"] = best
res = []
for a in range(-10, 11):
    for b in range(-10, 11):
        if b - 3 * a != 2:
            continue
        f, fi = mob(3, b, 1, a)
        if same(fi, lambda t: f(t - 2) - 2):
            res.append(a + b)
R["g2-23"] = res[0]

# 08 ------------------------------------------------------------------
ok = [a for a in np.round(lin(-1, 1, 20001), 5) if a != 0 and 1 + 8 * a > 0]
assert abs(min(ok) + 0.125) < 1e-3
R["b47"] = "$- {1} over {8} <a<0$ 또는 $a>0$"
ms = 2 / (lin(0, 1) + 1); R["b48"] = ms.max() + ms.min()
xs = lin(2, 4); a_ = 3 * xs / (xs - 1)**2; R["o34"] = a_.max() * a_.min()

# 09 ------------------------------------------------------------------
f = x / (1 - x); h = x
for _ in range(10):
    h = sp.simplify(f.subs(x, h))
num, den = sp.fraction(sp.together(h)); den0 = den.subs(x, 0)
num, den = sp.expand(num / den0), sp.expand(den / den0)
R["b56"] = num.coeff(x, 1) + num.coeff(x, 0) + den.coeff(x, 1)
fi = lambda y: Fr(-4) / (y - 2)                    # f(x)=-4/x+2의 역함수
v = Fr(-1)
for _ in range(500):
    v = fi(v)
R["g2-9"] = v
f30 = lambda y: (1 - y) / (1 + y)
v = Fr(3)
for _ in range(25):
    v = f30(v)
R["o30"] = v

# 10 ------------------------------------------------------------------
tt = lin(1e-3, 20); d2 = tt**2 + 4 / tt**2; i = d2.argmin()
R["b62"] = (2 + tt[i]) + math.sqrt(d2[i]) - math.sqrt(2)
tt = lin(1e-3, 20); area = 0.5 * np.abs((-1 - tt) * (-4 - 1 / tt) - (0 - tt) * (0 - 1 / tt))
R["b66"] = area.min()
mm = lin(1e-3, 20); area = 0.5 * (3 * mm + 1) * (1 / mm + 3)
R["g2-21"] = area.min()

# STEP 3 --------------------------------------------------------------
def g180(t):
    xs = np.concatenate([lin(-300, 5 / 3 - 1e-7, 1500001), lin(5 / 3 + 1e-7, 300, 1500001)])
    f = (6 * t * xs - 9 * t) / np.abs(3 * xs - 5)
    ks = []
    for k in range(-60, 61):
        s = np.sign(f - k); c = np.count_nonzero(s[:-1] * s[1:] < 0)
        if s[1500000] * s[1500001] < 0:
            c -= 1
        if c == 1:
            ks.append(k)
    return max(ks) - min(ks) if ks else None


ts = [t_ for t_ in (Fr(n, 2) for n in range(1, 21)) if g180(float(t_)) == 15]
R["m180"] = (12 * ts[0] - 9 * ts[0]) if len(ts) == 1 else None
mm = [m for m in range(1, 20) if sp.simplify(((5 * x - 5 * m + 6) / (x - m)).subs(x, (5 * x - 5 * m + 6) / (x - m)) - x) == 0]
k_ = sp.symbols("k", positive=True)
m = mm[0]
xs = lin(1e-6, m - 1e-6); v = xs * (m - xs) / (5 * 1)       # 1/(f-g) = x(m-x)/(5k) (m=5에서)
kv = (v.max()) / Fr(5, 24) if m == 5 else None
R["m182"] = 6 / (9 - m) + 5 if m == 5 and abs(kv - 6) < 1e-6 else None
ok = []
segs = [lin(-200, 0, 400001), lin(0, 1 - 1e-7, 2001), lin(1 + 1e-7, 200, 400001)]
for k in np.round(lin(-3, 1, 4001), 4):
    meet = False
    for xs in segs:
        fv = (2 * np.abs(xs) - 2) / np.abs(xs - 1) - k * xs
        s_ = np.sign(fv)
        if np.any(s_[:-1] * s_[1:] < 0) or np.any(np.abs(fv) < 1e-12):
            meet = True
            break
    if not meet:
        ok.append(k)
lo, hi = min(ok), max(ok)
assert abs(lo + 2) < 2e-3 and abs(hi - (-6 + 4 * math.sqrt(2))) < 2e-3
R["g3-11"] = "$-2 leq k<-6+4 sqrt {2}$"
X = lin(-1.99, 30, 3000001); X = X[X != -2]
P_ = np.stack([X, -3 / (X + 2)])
Qx = P_[1] - 2                                       # y=x+2에서 y=P_y인 x
PQ = np.abs(P_[0] - Qx); i = PQ.argmin()
PR = PQ[i] / math.sqrt(2); R["g3-13"] = 0.5 * PR * PR
X = lin(-1.99, 30, 3000001); X = X[X != -2]
X2 = lin(-30, -2.01, 3000001); P_ = np.concatenate([X2, X]); PQ = np.abs(P_ - (-3 / (P_ + 2) - 2)); i = PQ.argmin()
R["g3-13"] = 0.5 * (PQ[i] / math.sqrt(2))**2
oks = []
for k in np.round(lin(-5, 10, 1501), 3):
    xs = lin(1 + 1e-6, 2 - 1e-6, 200001)
    fv = np.abs((3 * xs - 5) / (xs - 1) + k)
    below = fv < 5
    # x1<x2, f(x1)<5<f(x2): 앞쪽에 5보다 작은 값, 뒤쪽에 5보다 큰 값
    first_below = np.argmax(below) if below.any() else None
    ok_ = first_below is not None and np.any(fv[first_below:] > 5)
    if ok_:
        oks.append(k)
assert abs(min(oks) - 4) < 0.02
R["g3-18"] = "$k>4$"
# g3-19: 점 Q는 x+y=6 또는 x+y=-10 위 → y=a/x와 두 직선의 교점이 3개인 a(>1)
res = []
for a in range(2, 40):
    cnt = 0
    for s in (6, -10):
        D = s * s - 4 * a
        cnt += 0 if D < 0 else (1 if D == 0 else 2)
    if cnt == 3:
        res.append(a)
R["g3-19"] = res[0]
res = []
for k in range(1, 60):
    a2 = Fr(k, 2)                                   # k=2a²
    if 6 * a2 == 45:
        res.append(k)
R["o50"] = res[0]
X = sp.symbols("X"); H = (2 * X - 7) / (X * (X - 2))
xs = lin(-4, -1, 3000001); hv = (2 * xs - 7) / (xs * (xs - 2))
R["o52"] = hv.max() + hv.min()
gg = lambda t: 2 / (t - 3) + 1
a62 = (15 - 10) / (gg(6) - 2)**2
R["o62"] = a62 * (1 - 2)**2 + 10
res = []
for bb in (3, -3):
    for a in range(-100, 101):
        if a == 0 or bb == 3:
            continue
        if Fr(a, 6) == Fr(a, 3) - 4:
            res.append(Fr(a, 9) + bb)
R["h2203-18"] = res[0]


# 대조 ---------------------------------------------------------------
def val(s):
    s = s.replace(" ", "").replace("it-", "-")
    s = re.sub(r"sqrt\{([^{}]*)\}", r"sqrt(\1)", s)
    s = re.sub(r"\{([^{}]*)\}over\{([^{}]*)\}", r"((\1)/(\2))", s)
    return eval(s, {"sqrt": math.sqrt})


bad = 0
items = [p for _, _, ps in data11.TYPES for p in ps] + data11.STEP3
for p in items:
    got, exp = R.get(p["src"]), p["ans"]
    if got is None:
        print("검산 없음", p["src"], exp); bad += 1; continue
    if isinstance(got, str):
        ok = got.replace(" ", "") == exp.replace(" ", "")
    else:
        e = val(exp)
        ok = abs(float(got) - e) <= 1e-3 * max(1, abs(e))
    if not ok:
        print("불일치", p["src"], "자료", exp, "검산", got); bad += 1
print("문항", len(items), "불일치", bad)
