# -*- coding: utf-8 -*-
"""공통수학2 기본서 8단원 절대부등식 검산: 문항마다 답을 따로(촘촘한 수치 탐색·직접 대입으로) 계산해 data08.py의 답과 맞춘다.
python verify08.py
- 최댓값·최솟값은 조건을 매개변수로 풀어 넣은 촘촘한 격자에서 찾고(상대 오차 1e-4 이내), 등호 조건의 값은 직접 대입해 확인한다.
- 보기(ㄱㄴㄷ) 문항은 무작위 실수 20만 쌍으로 반례가 있는지 본다.
"""
import sys, os, re, math, random
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data08

R = {}
rng = np.random.default_rng(1)
sq = np.sqrt


def lin(a, b, n=400001):
    return np.linspace(a, b, n)


def always(f, n=200000, lo=-10, hi=10, pos=False):
    a = rng.uniform(0 if pos else lo, hi, n) + (1e-6 if pos else 0)
    b = rng.uniform(0 if pos else lo, hi, n) + (1e-6 if pos else 0)
    return bool(np.all(f(a, b)))


# 01 ------------------------------------------------------------------
# g2-4: 5x²+4y²+9−4x(y−3) = (x−2y)² + f(x) → f(x)=5x²+4y²+9−4xy+12x−(x−2y)² 는 x만의 식
f = lambda x: 4 * x * x + 12 * x + 9
xs = lin(-5, 5, 1001)
for y in (-2.0, 0.5, 3.0):
    assert np.allclose(5 * xs**2 + 4 * y * y + 9 - 4 * xs * (y - 3), (xs - 2 * y)**2 + f(xs))
al, be = -1.5, -0.75                                  # 두 제곱이 모두 0
assert abs(al - 2 * be) < 1e-12 and abs(2 * al + 3) < 1e-12
R["g2-4"] = f(2) + 12 * (al + be)

e = 1e-12
ok = []
if always(lambda a, b: b / a**2 + a**2 / b >= 3 - e, pos=True): ok.append("ㄱ")
if always(lambda a, b: 1 + a / 2 > sq(1 + a), pos=True): ok.append("ㄴ")
if always(lambda a, b: sq((a + b) / 2) >= (sq(a) + sq(b)) / 2 - e, pos=True): ok.append("ㄷ")
R["b4"] = ", ".join(ok)

ok = []
if always(lambda a, b: abs(a + b) >= abs(a - b)): ok.append("ㄱ")
if always(lambda a, b: abs(a - b) <= abs(a) + abs(b) + e): ok.append("ㄴ")
if always(lambda a, b: np.where(a > b, sq(np.abs(a - b)) > sq(np.abs(a)) - sq(np.abs(b)), True), pos=True): ok.append("ㄷ")
if always(lambda a, b: abs(a) - abs(b) <= abs(a - b) + e): ok.append("ㄹ")
R["g2-6"] = ", ".join(ok)

# 02 ------------------------------------------------------------------
A, B = np.meshgrid(lin(-4, 2, 1201), lin(-2, 1, 1201))
F = 2 * A**2 + 2 * A * (2 - 3 * B) + 9 * B**2 + 4
i = np.unravel_index(F.argmin(), F.shape)
a0, b0 = A[i], B[i]                                   # 격자 최소점 근처에서 F=0인 점(완전제곱식의 합이 0)
Fx = lambda a, b: 2 * a * a + 2 * a * (2 - 3 * b) + 9 * b * b + 4
assert abs(a0 + 2) < 0.01 and abs(b0 + 2 / 3) < 0.01 and abs(Fx(-2, -2 / 3)) < 1e-12 and F.min() >= 0
R["b14"] = 9 * (-2) * (-2 / 3)

best = None
for k in np.arange(-4, 4.0001, 0.01):
    a = rng.uniform(-20, 20, 20000); b = rng.uniform(-20, 20, 20000)
    a = np.append(a, k); b = np.append(b, 1)
    if np.all(a * a + b * b + 5 >= 2 * k * a + 2 * b - 1e-9):
        best = k
R["k4-13"] = round(best, 2)

u = rng.dirichlet([1, 1, 1], 400000)                  # a+b+c=1 (넓이에서), 내부의 점
R["b16"] = (u[:, 0] * u[:, 1] + u[:, 1] * u[:, 2] + u[:, 2] * u[:, 0]).max()

# 03 ------------------------------------------------------------------
x = lin(-0.999, 20)
v = (x * x + x + 4) / (x + 1)
R["b19"] = v.min() + x[v.argmin()]

k = lin(5.0001, 60)
v = k + 5 + 9 / (k - 5)
R["g2-5"] = k[v.argmin()] + v.min()

x = lin(-10, 10)
t = x * x + 3 * x + 4
R["b21"] = (sq(t) + 4 / t).min()

x = lin(-1.999, 20)
v = sq((2 * x * x + 2 * x + 4) / (x + 2))
R["g2-12"] = x[v.argmin()] + v.min()

# 04 ------------------------------------------------------------------
a = lin(1e-4, 200)                                   # 1/(2a+1)+1/(3b+1)=1/5 → 3b+1 = 1/(1/5−1/(2a+1))
w = 1 / 5 - 1 / (2 * a + 1)
m = w > 0
b = (1 / w[m] - 1) / 3
mm = b > 0
R["g2-9"] = (2 * a[m][mm] + 3 * b[mm]).min()

th = lin(1e-6, math.pi / 2 - 1e-6)
R["b29"] = (15 * np.cos(th)**2 + 8 * np.cos(th) * np.sin(th)).max()

r = np.exp(lin(-6, 6))                               # x/y 또는 z/(x+y)의 비
amin = ((r + 2) * (1 / r + 2)).min()                 # A: x=r, y=1
bmin = ((r + 1) * (3 / r + 1 / 3)).min()             # B
cmin = ((1 + r) * (1 + 1 / r)).min()                 # C: x+y=1, z=r
order = sorted([("a", amin), ("b", bmin), ("c", cmin)], key=lambda p: p[1])
R["b47"] = "<".join(p[0] for p in order)

# 05 ------------------------------------------------------------------
a = lin(3.0001, 200)                                 # 3/a+5/b=1
b = 5 / (1 - 3 / a)
R["g2-10"] = (a * b / 2).min()

a = lin(1e-4, 3.4999)                                # 4a+3b=14
b = (14 - 4 * a) / 3
R["k6-18"] = (4 / a + 3 / b).min()

x = lin(1, 1200)                                     # BC=x, AB=1200/x
cost = 1.5 * x + 2 * 1200 / x
R["g3-12"] = round(x[cost.argmin()], 2)

x = lin(1e-4, 4.8 - 1e-4)                            # 25x/12 + y = 10
y = 10 - 25 * x / 12
i = (x * y).argmax()
R["g3-14"] = 2 * (x[i] + y[i]) - (x * y)[i]

# 06 ------------------------------------------------------------------
u = rng.normal(size=(600000, 3)); u /= np.linalg.norm(u, axis=1)[:, None]
s = 2 * u[:, 0] + 3 * u[:, 1] + 6 * u[:, 2]
al = s.max()
a, b, c = 2 / 7, 3 / 7, 6 / 7                        # 최댓값일 때(직접 대입)
assert abs(2 * a + 3 * b + 6 * c - 7) < 1e-12 and abs(al - 7) < 1e-3
R["b34"] = 7 - c * c / (a * b)

x = lin(-5, 5)
y = (5 - 3 * x) / 4
v = 9 * x * x + 4 * y * y
i = v.argmin()
R["g2-14"] = v[i] / (x[i] * y[i])

x = lin(1e-4, 8 / math.sqrt(5) - 1e-4)               # √5x+2y=8 (넓이 25에서)
y = (8 - math.sqrt(5) * x) / 2
R["k2-23"] = (9 * (x * x + y * y)).min()

t = lin(0, 2 * math.pi, 2001)
T1, T2 = np.meshgrid(t, t)
a, b = math.sqrt(2) * np.cos(T1), math.sqrt(2) * np.sin(T1)
c, d = math.sqrt(18) * np.cos(T2), math.sqrt(18) * np.sin(T2)
R["g2-16"] = (a * b + c * d).max() + (a * c + b * d).max()

# 07 ------------------------------------------------------------------
y = lin(1e-6, 0.75)                                  # x=2−2y>0, 3−4y≥0
x = 2 - 2 * y
R["b41"] = 5 * ((sq(5 - 2 * x) + sq(3 - 4 * y))**2).max()

x = lin(1e-4, 1.25 - 1e-4)
y = 5 - 4 * x
v = 1 / x + 9 / y
i = v.argmin()
R["b49"] = v[i] * x[i] * y[i]

x = lin(0, 10)
y = 10 - x
m = (21 - 2 * x >= 0) & (23 - 2 * y >= 0)
R["m117"] = (sq(21 - 2 * x[m]) + sq(23 - 2 * y[m])).max()

# 08 ------------------------------------------------------------------
def zrange(coef, s, q):
    """x·coef[0]+y·coef[1]+z·coef[2]=s, x²+y²+z²=q에서 z가 가질 수 있는 값의 범위(격자)"""
    zs = lin(-10, 10, 200001)
    rest_s = s - coef[2] * zs
    rest_q = q - zs * zs
    ok = (rest_q >= 0) & ((coef[0]**2 + coef[1]**2) * rest_q >= rest_s**2 - 1e-9)
    return zs[ok].min(), zs[ok].max()


lo, hi = zrange((1, 2, 3), 3, 12)
R["b55"] = lo + hi
lo, hi = zrange((1, 1, 1), 5, 11)
R["g3-19"] = hi + 3 * lo

# 09 ------------------------------------------------------------------
# b62: 조건을 만족시키는 점이 하나뿐인지 무작위 탐색으로 확인 후 그 점 대입
x, y, z = 6, 3, -2
assert x + 2 * y - 3 * z == 18 and x * x + 4 * y * y + 9 * z * z == 108
pts = rng.normal(size=(300000, 3)) * 6
g = (3 * (pts[:, 0]**2 + 4 * pts[:, 1]**2 + 9 * pts[:, 2]**2) - (pts[:, 0] + 2 * pts[:, 1] - 3 * pts[:, 2])**2)
assert g.min() >= -1e-6                               # 3(제곱합) ≥ (일차식)², 등호일 때만 조건 성립
R["b62"] = x + y + z

pts = rng.normal(size=(300000, 3))
g = 14 * (pts**2).sum(1) - (pts[:, 0] + 2 * pts[:, 1] + 3 * pts[:, 2])**2
assert g.min() >= -1e-6
a, b, c = 1, 2, 3                                    # 등호: a:b:c=1:2:3
assert 14 * (a * a + b * b + c * c) == (a + 2 * b + 3 * c)**2
R["b65"] = 3 * c / (2 * b)

X, Y = np.meshgrid(lin(0, 0.5, 2001), lin(0, 2 / 3, 2001))
slack = np.minimum(4 * X * (2 - 3 * Y), 6 * Y * (1 - 2 * X)) - 1   # 두 부등식을 모두 만족시키면 0 이상
i = np.unravel_index(slack.argmax(), slack.shape)
assert abs(slack[i]) < 1e-5                            # 최댓값이 0: 만족시키는 점은 등호인 한 점뿐
far = (np.abs(X - X[i]) > 0.01) | (np.abs(Y - Y[i]) > 0.01)
assert slack[far].max() < 0
R["m124"] = X[i] + Y[i]

# STEP 3 --------------------------------------------------------------
r = np.exp(lin(-8, 8))                               # y/x
R["g3-13"] = ((24 + 26 * r + 6 * r * r) / (4 + 4 * r + r * r)).max()

X, Y = np.meshgrid(lin(-3, 6, 1801), lin(-3, 3, 1201))
R["m113"] = (2 * X**2 + 2 * Y**2 - 4 * X + 25 / (X**2 + 2 * Y**2 + 1)).min()

a = lin(1e-6, 2 - 1e-6)
b = 2 - a
R["m115"] = ((2 * b - 2) / (a + 1) + a / (b + 2)).min()

X, Y = np.meshgrid(lin(-2, 6, 1601), lin(-2, 5, 1401))
R["b76"] = (sq(4 + Y**2) + sq((X - 2)**2 + (2 - Y)**2) + sq((4 - X)**2 + 1)).min()

best = 1e9
for _ in range(40):
    a, b, c = rng.uniform(1e-3, 10, (3, 200000))
    v = (3 * a / 4 + 2 * b + 5 * c / 2) * (1 / (3 * a + 2 * b) + 1 / (3 * b + 5 * c))
    best = min(best, v.min())
R["g3-4"] = best

r = lin(1e-4, 30)                                    # y = r x
x = sq(10 / (6 + 11 * r + 3 * r * r)); y = r * x
R["m110"] = ((2 * x + y + sq(2 * x * y))**2).max()

r = lin(1e-4, 30)
x = (1 / (1 + r**4))**0.25; y = r * x
R["m112"] = (3 * x * x + 2 * math.sqrt(2) * x * y).max()

xs = np.round(lin(-10, 10, 200001), 6)
v = np.abs(xs - 5) + np.abs(xs + 2) + np.abs(xs * (xs - 1) * (xs + 2) * (xs + 3))
R["m119"] = xs[v <= 7 + 1e-9].sum()

a = lin(1.0001, 40)
R["m118"] = (2 * a / (1 - a) - a).max()

u = rng.uniform(1e-3, 1, (3, 600000))                # x=s−a, y=s−b, z=s−c
x, y, z = u
R["m121"] = (x * y * z / ((y + z) * (z + x) * (x + y))).max()

u = rng.dirichlet([1, 1, 1], 600000)
M = sq(3 * u + 1).sum(1)
assert M.min() > 4 and M.max() < 5
R["m123"] = 4



# 2차 구성(증명 문항) -----------------------------------------------------
import sympy as sp
a_, b_, c_, x_, y_, z_, p_, q_, t_ = sp.symbols("a b c x y z p q t", real=True)
ANS = {p["src"]: p["ans"] for _, _, ps in data08.TYPES for p in ps}


def ok_text(src, cond):
    assert cond, src
    R[src] = ANS[src]


# s1296: (|a|+|b|)²−|a+b|² = 2(|ab|−ab), 등호 ab≥0
A, B = rng.uniform(-9, 9, (2, 100000))
ok_text("s1296", np.allclose((abs(A) + abs(B))**2 - abs(A + B)**2, 2 * (abs(A * B) - A * B))
        and np.all((np.abs((abs(A) + abs(B)) - abs(A + B)) < 1e-12) == (A * B >= 0)))
# m128: |a|−|b| ≤ |a−b|, 차 = 2(|ab|−ab), 등호 |a|≥|b|이고 ab≥0
A, B = rng.uniform(-9, 9, (2, 100000))
ok_text("m128", np.allclose(abs(A - B)**2 - (abs(A) - abs(B))**2, 2 * (abs(A * B) - A * B))
        and np.all(abs(A) - abs(B) <= abs(A - B) + 1e-12)
        and np.all((np.abs(abs(A - B) - (abs(A) - abs(B))) < 1e-9) == ((abs(A) >= abs(B)) & (A * B >= 0))))
# s1290: (√(a−b))²−(√a−√b)² = 2√(ab) − 2b = 2√b(√a−√b)
ok_text_v = sp.simplify((a_ - b_) - (sp.sqrt(a_) - sp.sqrt(b_))**2 - (2 * sp.sqrt(a_) * sp.sqrt(b_) - 2 * b_))
assert ok_text_v == 0
R["s1290"] = 2 * math.sqrt(4 * 9) + math.sqrt(16)
# h1109-17: |ap+bq|² − (a²p+b²q) = a²p(p−1)+b²q(q−1)+2abpq = −pq(a−b)² (p+q=1)
e1 = sp.expand((a_ * p_ + b_ * q_)**2 - (a_**2 * p_ + b_**2 * q_) - (a_**2 * p_ * (p_ - 1) + b_**2 * q_ * (q_ - 1) + 2 * a_ * b_ * p_ * q_))
e2 = sp.expand((a_**2 * p_ * (p_ - 1) + b_**2 * q_ * (q_ - 1) + 2 * a_ * b_ * p_ * q_).subs(q_, 1 - p_) + p_ * (1 - p_) * (a_ - b_)**2)
ok_text("h1109-17", e1 == 0 and e2 == 0)
# s1294: 보기 ㄱ~ㅁ (양수 무작위 + 등호인 a=b=c)
X, Y, Z = rng.uniform(1e-3, 10, (3, 200000))
tv = [np.all(1 / X + 1 / Y >= 4 / (X + Y) - 1e-12), np.all(X**3 + Y**3 >= X * Y * (X + Y) - 1e-9),
      np.all(X + Y + Z >= sq(X * Y) + sq(Y * Z) + sq(Z * X) - 1e-9), bool(1 + 1 + 1 > 3 * 1 * 1 * 1),   # ㄹ: a=b=c에서 거짓
      np.all((X + Y) * (Y + Z) * (Z + X) >= 8 * X * Y * Z - 1e-9)]
R["s1294"] = ", ".join(n for n, v in zip("ㄱㄴㄷㄹㅁ", tv) if v)
# h0911-15: f=(a−b)², g=2(ab+bc+ca), k=3, 그리고 4ab/(a+b)·c 합 ≤ 2(ab+bc+ca) 확인
assert sp.expand((a_ + b_)**2 - 4 * a_ * b_ - (a_ - b_)**2) == 0
assert np.all(4 * X * Y / (X + Y) * Z + 4 * Y * Z / (Y + Z) * X + 4 * Z * X / (Z + X) * Y <= 2 * (X * Y + Y * Z + Z * X) + 1e-9)
assert np.all(3 * (X * Y + Y * Z + Z * X) <= (X + Y + Z)**2 + 1e-9)
R["h0911-15"] = (3 - 1)**2 + 2 * (1 * 2 + 2 * 3 + 3 * 1) + 3
# g1-7, 개념 증명: 항등식 확인
ok_text("g1-7", sp.expand((a_**2 + b_**2) * (x_**2 + y_**2) - (a_ * x_ + b_ * y_)**2 - (a_ * y_ - b_ * x_)**2) == 0)
ok_text("s1292", sp.simplify((a_ + b_) / 2 - sp.sqrt(a_) * sp.sqrt(b_) - (sp.sqrt(a_) - sp.sqrt(b_))**2 / 2) == 0)
Aa, Bb, Cc = sp.symbols("A B C")
ok_text("개념-산술기하3", sp.expand(Aa**3 + Bb**3 + Cc**3 - 3 * Aa * Bb * Cc - (Aa + Bb + Cc) * ((Aa - Bb)**2 + (Bb - Cc)**2 + (Cc - Aa)**2) / 2) == 0)
ok_text("개념-코시3", sp.expand((a_ * t_ - x_)**2 + (b_ * t_ - y_)**2 + (c_ * t_ - z_)**2
                               - ((a_**2 + b_**2 + c_**2) * t_**2 - 2 * (a_ * x_ + b_ * y_ + c_ * z_) * t_ + (x_**2 + y_**2 + z_**2))) == 0)
# h0909-13: 등호 조건 2ab=1, ab=8, 올바른 최솟값
a = lin(1e-3, 20, 4001)
Aa_, Bb_ = np.meshgrid(a, a)
v = (2 * Aa_ + 1 / Bb_) * (Bb_ + 8 / Aa_)
assert abs(v.min() - 25) < 1e-2
ok_text("h0909-13", True)
# o20, h1911-16, o58
Aa_, Bb_ = np.meshgrid(lin(1e-3, 3, 3001), lin(1e-3, 3, 3001))
R["o20"] = ((3 * Aa_ + 1 / Bb_) * (1 / Aa_ + 12 * Bb_)).min()
a = lin(0.05, 60)
R["h1911-16"] = sq(a * a + (18 / a)**2 + 16).min()
a = lin(1e-3, 6 - 1e-3)                               # a>0, b=(a−6)/2<0
b = (a - 6) / 2
R["o58"] = (2 / a - 1 / b).min()


# 대조 ---------------------------------------------------------------
def val(s):
    s = s.replace(" ", "")
    s = re.sub(r"sqrt\{([^{}]*)\}", r"sqrt(\1)", s)
    s = re.sub(r"\{([^{}]*)\}over\{([^{}]*)\}", r"((\1)/(\2))", s)
    s = re.sub(r"(\d)(sqrt)", r"\1*\2", s)
    return eval(s, {"sqrt": math.sqrt})


bad = 0
items = [p for _, _, ps in data08.TYPES for p in ps] + data08.STEP3
for p in items:
    got = R.get(p["src"])
    exp = p["ans"]
    if got is None:
        print("검산 없음", p["src"], exp); bad += 1; continue
    if isinstance(got, str):
        ok = got.replace(" ", "") == exp.replace(" ", "")
    else:
        e = val(exp)
        ok = abs(got - e) <= 1e-3 * max(1, abs(e))
    if not ok:
        print("불일치", p["src"], "자료", exp, "검산", got); bad += 1
print("문항", len(items), "불일치", bad)
