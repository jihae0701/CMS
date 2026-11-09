# -*- coding: utf-8 -*-
"""공통수학2 기본서 10단원 합성함수와 역함수 검산: 문항마다 답을 따로(모든 경우를 세거나 촘촘한 격자로) 계산해 data10.py의 답과 맞춘다.
python verify10.py   (도구/verify10.py는 공통수학1 10단원 검산이라 이름이 같아도 다른 파일)
"""
import sys, os, re, math, itertools
import numpy as np
from fractions import Fraction as Fr
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data10

R = {}
P = itertools.permutations


def lin(a, b, n=400001):
    return np.linspace(a, b, n)


def count_roots(h, a, b, n=2000001):
    """[a, b]에서 h(x)=0의 서로 다른 근의 개수(부호 바뀜 + 격자 위의 정확한 0)"""
    x = lin(a, b, n); v = h(x)
    z = np.abs(v) < 1e-12
    s = np.sign(v)
    ch = np.count_nonzero((s[:-1] * s[1:] < 0))
    return ch + np.count_nonzero(z)


# 01 ------------------------------------------------------------------
tot = 0
for a in range(-5, 6):
    for b in range(-8, 9):
        if all(a * x ** 3 - b * x - 2 * a + b in (0, 1) for x in (0, 1)):
            tot += a + b
R["b2"] = tot
ok = [a for a in [Fr(n, 100) for n in range(1, 501)] if -a <= -2 and a * a - 2 <= a]
R["g1-17"] = ok[0] if len(ok) == 1 else None
f33 = lambda x: x * x - 3 * x - 2 if x <= -1 else x + 3
g33 = lambda x: -x + 1
R["o33"] = f33(g33(-2)) + f33(g33(3))

# 02 ------------------------------------------------------------------
# f(t)=at+b를 두 점에서 정함
f5 = lambda t: 4 * ((3 * t - 1) / 2) - 6
R["b5"] = "$f(3x-1)=18x-14$" if all(abs(f5(3 * x - 1) - (18 * x - 14)) < 1e-9 for x in (-2, 0, 1.5, 3)) else None
xs = np.array([-3., -1., 0., 2., 5.]); t = (xs + 1) / 2; rhs = 2 * (xs ** 2 + 2 * xs) + 1
a, b, c = np.linalg.solve(np.vstack([t[:3] ** 2, t[:3], np.ones(3)]).T, rhs[:3])
assert np.allclose(a * t ** 2 + b * t + c, rhs)
R["o13"] = a * a + b * b + c * c
h = lambda t: (t + 1) / 3 + 4          # h(3x-1)=x+4
assert all(abs(h(3 * x - 1) - (x + 4)) < 1e-9 for x in (-1, 0, 2))
R["g1-30"] = "$h^{-1} (x)=3x-13$" if all(abs(h(3 * y - 13) - y) < 1e-9 for y in (-2, 0, 7)) else None

# 03 ------------------------------------------------------------------
res = set()
for a in range(-20, 21):
    b = 4 - 3                         # g(1)=4
    if all(-a * (3 * x + b) + 4 == 3 * (-a * x + 4) + b for x in (0, 1)):
        res.add(a * b)
R["b10"] = res.pop()
res = [a for a in [Fr(n, 4) for n in range(-40, 41)] if all(2 * (3 * x + 1) + a == 3 * (2 * x + a) + 1 for x in (0, 1))]
R["o12"] = 2 * res[0] + res[0]
vals = set()
for a in [Fr(n, 2) for n in range(-10, 11)]:
    for b in [Fr(n, 2) for n in range(-10, 11)]:
        f = lambda x: a * x + b
        if all(f(f(x)) == x and f(3 * x + 1) == 3 * f(x) + 1 for x in (0, 1, 2)):
            vals.add(f(2))
R["o45"] = sum(vals)

# 04 ------------------------------------------------------------------
def it(f, x, n):
    for _ in range(n):
        x = f(x)
    return x


R["b30"] = it(lambda x: x + 1 if x <= 1 else -2 * x + 4, Fr(3, 2), 100)
R["b32"] = it(lambda x: 2 * x - 5 if x >= 0 else 2 * x + 5, 4, 200)
F53 = lambda x: x + 3 if x % 2 else x // 2
R["o53"] = sum(a for a in range(1, 3000) if F53(F53(F53(a))) == 27)

# 05 ------------------------------------------------------------------
X4 = [1, 2, 3, 4]; res = set()
for p in P(X4):
    f = dict(zip(X4, p))
    if f[f[1]] == 4 and f[f[3]] == 3:
        res.add(2 * f[1] + 4 * f[3])
R["b26"] = res.pop() if len(res) == 1 else None
# g1-18: 일대일대응 f, g (값이 필요한 곳만): f(6)=8, g(3)=4, f(g(5))=8 → g(5)=6, f(g(3))=f(4)=9
R["g1-18"] = 9 + 6
X5 = [1, 2, 3, 4, 5]; res = set()
for p in P(X5):
    f = dict(zip(X5, p))
    if f[3] == 1 and f[f[3]] == 4 and f[f[f[3]]] == 3 and f[2] < f[5]:
        res.add(it(lambda x: f[x], 4, 100))
R["b29"] = res.pop() if len(res) == 1 else None

# 06 ------------------------------------------------------------------
R["b63"] = count_roots(lambda x: np.abs(np.abs(x - 2) - 2) - np.abs(x) / 5, -30, 30, 6000001)
R["o36"] = sum(1 + s * d for d in (Fr(2, 9), Fr(4, 9)) for s in (1, -1)
               if 3 * abs(3 * abs(1 + s * d - 1) - 1) == 1)
fb = lambda x: np.interp(x, [0, 1, 2], [0, 2, 0]); gb = lambda x: np.interp(x, [0, 1, 2], [1, 0, 2])
R["b61"] = count_roots(lambda x: gb(fb(x)) - 1, 0, 2, 2000001)

# 07 ------------------------------------------------------------------
f48 = lambda x: -2 * x + 6; g48 = lambda x: x - 8
fi = lambda y: (6 - y) / 2; gi = lambda y: y + 8
fgi_inv = lambda y: g48(fi(y))       # (f∘g⁻¹)⁻¹ = g∘f⁻¹
H = lambda x: f48(fgi_inv(f48(x)))
a = H(1) - H(0); b = H(0)
R["b48"] = a + b
res = [(a, b) for a in [Fr(n, 2) for n in range(-10, 11)] for b in [Fr(n, 2) for n in range(-10, 11)]
       if all(a * (-Fr(1, 2) * x + b) + 3 == x for x in (0, 1))]
R["o40"] = res[0][0] + res[0][1]
X3 = [1, 2, 3]; res = set()
for pf in P(X3):
    for pg in P(X3):
        f = dict(zip(X3, pf)); g = dict(zip(X3, pg))
        fi_ = {v: k for k, v in f.items()}; gi_ = {v: k for k, v in g.items()}
        fg = {x: f[g[x]] for x in X3}; fgi_ = {v: k for k, v in fg.items()}
        if f[1] == 3 and g[2] == 3 and fgi_[1] == 2 and fi_[g[1]] == 2:
            res.add(f[2] + g[3] + f[gi_[1]])
R["o44"] = res.pop() if len(res) == 1 else None

# 08 ------------------------------------------------------------------
def bij_pw(fun, lo=-80, hi=80):
    v = fun(lin(lo, hi, 32001)); d = np.diff(v)
    return bool(np.all(d > 0) or np.all(d < 0))


R["o42"] = sum(bij_pw(lambda x: np.where(x < 2, (a + 3) * x - 2, (2 - a) * x + 4 * a)) for a in range(-30, 31))
R["g1-31"] = sum(bij_pw(lambda x: a * np.abs(x) + 3 * x - 1) for a in range(-30, 31))
aa = lin(-1, 5); R["o23"] = (aa - (aa ** 2 + 2 * aa + 5)).max()

# 09 ------------------------------------------------------------------
# b43: f(x)=2x+1(아무 일대일 함수로 시험) → g, y=3g((x−1)/2)−1의 역함수가 2f((x+1)/3)+1과 같은지
for fA, gA in ((lambda x: 2 * x + 1, lambda y: (y - 1) / 2), (lambda x: x ** 3, lambda y: np.cbrt(y))):
    k = lambda x: 3 * gA((x - 1) / 2) - 1
    cand = lambda x: 2 * fA((x + 1) / 3) + 1
    assert all(abs(cand(k(x)) - x) < 1e-9 for x in (-3.0, 0.5, 2.0, 7.0))
R["b43"] = "$y=2f LEFT ( {x+1} over {3} RIGHT ) +1$"
fA = lambda x: 3 * x - 2; gA = lambda y: (y + 2) / 3
inv = lambda y: (gA(y) - 5) / 4            # y=f(4x+5)의 역함수
a = inv(1) - inv(0); b = inv(0) - a * 0
a = (inv(3) - inv(0)) / (gA(3) - gA(0)); b = inv(0) - a * gA(0)
R["o20"] = a + b
f41 = lambda t: 5 * (3 * t + 2) + 6
R["o41"] = [Fr(n, 3) for n in range(-30, 31) if f41(Fr(n, 3)) == -4][0]

# 10 ------------------------------------------------------------------
best = None
for a in [Fr(n, 4) for n in range(0, 40)]:
    D = 16 - 8 * a
    if D <= 0:
        continue
    r1, r2 = 2 - math.sqrt(D) / 2, 2 + math.sqrt(D) / 2
    if r1 >= 1 and abs(math.sqrt(2) * (r2 - r1) - 2) < 1e-9:
        best = a
R["b78"] = best
r = np.roots([1, -5, 6]); r = sorted(x for x in r if x >= 2 - 1e-9)
R["o21"] = math.sqrt(2) * (r[1] - r[0])
x = lin(0, 2, 2000001); fv = np.where(x <= 1, x / 2, 1.5 * x - 1)
R["b85"] = 2 * np.trapezoid(x - fv, x)

# STEP 3 --------------------------------------------------------------
X6 = range(1, 7)
R["m159"] = sum(all(p[p[p[x - 1] - 1] - 1] == x for x in X6) for p in P(X6))
roots = []
for xv in [Fr(n, 2) for n in range(3, 40)]:
    fx = xv * xv - 3 * xv + 3
    # f⁻¹(x): x ≥ 3/4에서 f(y)=x, y ≥ 3/2
    yv = (3 + math.sqrt(4 * float(xv) - 3)) / 2
    if abs(float(fx) ** 2 - float(fx) - (float(fx) * yv - yv)) < 1e-9:
        roots.append(xv)
R["m174"] = sum(roots)
n = 0; best = 0
for p in P(X5):
    f = dict(zip(X5, p))
    if f[4] != 1 or sum(f[f[f[a]]] == a for a in X5) != 3:
        continue
    n += 1
    bs = [b for b in X5 if f[f[b]] == b]
    if len(bs) == 2:
        best = max(best, sum(bs))
R["m152"] = n + best
X7 = range(1, 8); res = set()
for p in P(X7):
    f = dict(zip(X7, p))
    if all(f[f[x]] == 2 * f[x] - 3 * x for x in (2, 3, 4)):
        res.add(f[2] + f[3] + f[4])
R["m160"] = res.pop() if len(res) == 1 else None
U = range(1, 6); cnt = 0
for mask in itertools.product((0, 1, 2), repeat=5):        # 0: X만, 1: Y만, 2: 둘 다 → X∪Y=U
    Xs = [u for u, m in zip(U, mask) if m in (0, 2)]; Ys = [u for u, m in zip(U, mask) if m in (1, 2)]
    if Xs and len(Xs) == len(Ys):
        cnt += sum(all(y > x for x, y in zip(Xs, q)) for q in P(Ys))
R["m157"] = cnt
best = 0
for p in P(X5):
    f = dict(zip(X5, p)); fi_ = {v: k for k, v in f.items()}
    if f[1] + f[3] == 7 and fi_[1] - fi_[3] == 3:
        best = max(best, f[4] + fi_[2])
R["o58"] = best
res = set()
for p in P(X7):
    f = dict(zip(X7, p)); fi_ = {v: k for k, v in f.items()}
    if all(f[f[x]] + fi_[x] == 2 * x for x in (1, 2, 6)) and f[3] + f[4] == 8 and f[6] != 6:
        res.add(f[5] * (f[6] + f[7]))
R["b102"] = res.pop() if len(res) == 1 else None
fg = lambda x: 1.5 * np.abs(x) - 0.5 * x - 1
R["g3-2"] = count_roots(lambda x: fg(fg(fg(x))) - fg(x) - 1, -20, 20, 4000001)
c = 0
for v in itertools.product(X5, repeat=5):
    f = dict(zip(X5, v))
    if f[5] == 4 and f[f[1]] == 1 and f[f[f[5]]] == 3:
        c += 1
R["g3-18"] = c
S = [n for n in range(1, 61) if n % 4 == 0]
cnt = 0
for r in range(1, 6):
    for Xs in itertools.combinations(S, r):
        if sorted(x % 5 for x in Xs) == [0, 1, 2, 3, 4]:
            cnt += 1
R["h1611-29"] = cnt


# 대조 ---------------------------------------------------------------
def val(s):
    s = s.replace(" ", "").replace("it-", "-")
    s = re.sub(r"sqrt\{([^{}]*)\}", r"sqrt(\1)", s)
    s = re.sub(r"\{([^{}]*)\}over\{([^{}]*)\}", r"((\1)/(\2))", s)
    return eval(s, {"sqrt": math.sqrt})


bad = 0
items = [p for _, _, ps in data10.TYPES for p in ps] + data10.STEP3
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
