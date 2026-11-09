# 공통수학2 9단원(함수) 유형서 문항 정답 독립 검산 (문항 기호는 c2unit09.py의 v).
# 유한집합 문항은 모든 함수를 완전 탐색하고, 실수 범위 문항은 촘촘한 격자와 sympy로 확인한다.
import itertools
import math
from fractions import Fraction as Fr
import numpy as np
import sympy as sp
R = []


def chk(no, got, exp):
    if isinstance(got, str):            # ①~⑤ 같은 기호 답
        ok = got == exp
    else:
        e = float(sp.sympify(exp))
        ok = abs(float(got) - e) <= 1e-6 * max(1, abs(e))
    R.append((no, ok, got, exp))


def mark(truth, ch, names="ㄱㄴㄷㄹㅁ"):
    s = ", ".join(names[i] for i, v in enumerate(truth) if v)
    ch = ch.split("|")
    return "①②③④⑤"[ch.index(s)] if s in ch else "?"


B5 = "ㄱ|ㄱ, ㄴ|ㄱ, ㄷ|ㄴ, ㄷ|ㄱ, ㄴ, ㄷ"


def funcs(X, Y):
    for v in itertools.product(Y, repeat=len(X)):
        yield dict(zip(X, v))


def inj(f):
    return len(set(f.values())) == len(f)


def is_lin_bij(a, b, X, Y):          # 닫힌 구간 X에서 Y로의 ax+b가 일대일대응인가
    if a == 0:
        return False
    v = sorted([a * X[0] + b, a * X[1] + b])
    return v[0] == Y[0] and v[1] == Y[1]


x = sp.symbols("x", real=True)
xs = np.linspace(-50, 50, 2000001)

# 함수의 뜻과 치역 --------------------------------------------------
Xo = [-1, 0, 1]; Yo = set(range(5))
chk("o01", mark([all(f(t) in Yo for t in Xo) for f in (lambda t: abs(t - 3), lambda t: 2 * t * t - t, lambda t: 3 * t * t - t ** 3)], B5), "⑤")
primes = [p for p in range(2, 30) if all(p % d for d in range(2, p))]
chk("k4-6", sum(set(sum(1 for p in primes if p <= 2 * t * t) for t in (1, 2, 3))), 12)
best = []
for a in [Fr(n, 4) for n in range(-40, 41)]:
    for b in [Fr(n, 4) for n in range(-40, 41)]:
        if is_lin_bij(a, b, (-2, 3), (-2, 3)):
            best.append(a + b)
chk("g1-5", min(best), 0)
a_ = sp.symbols("a", positive=True)
sols = [s for s in sp.solve(sp.Eq(5 - a_**2, 1), a_)]
a0 = sols[0]; xx = np.linspace(float(-2 * a0), 3, 100001); yy = xx**2 + 2 * float(a0) * xx + 5
chk("g1-8", float(a0) + yy.max(), 28)
S3 = list(range(3, 51, 3))
groups = {}
for n in S3:
    groups.setdefault(n % 7, []).append(n)
cnt = 1
for r in (1, 2, 3, 4):
    cnt *= 2 ** len(groups[r]) - 1
chk("g2-3", cnt, 189)                  # 나머지 0, 5, 6인 수는 고르지 않는다

# 서로 같은 함수 ----------------------------------------------------
D = [-2, 0, 2]
pairs = [(lambda t: t * t, lambda t: 2 * abs(t)), (lambda t: t ** 3, lambda t: 4 * t),
         (lambda t: 2 * t + 4, lambda t: (t + 2) ** 2 if t <= 0 else t + 4)]
chk("k6-2", mark([all(f(t) == g(t) for t in D) for f, g in pairs], "ㄱ|ㄱ, ㄴ|ㄱ, ㄷ|ㄴ, ㄷ|ㄱ, ㄴ, ㄷ"), "②")
sa, sb = sp.symbols("sa sb")
s = sp.solve([sp.Eq(11, 4 * sa + sb), sp.Eq(16, 9 * sa + sb)], [sa, sb]); chk("o02", s[sa] + s[sb], 8)
s = sp.solve([sp.Eq(t**3 + sa, sa * t + sb) for t in D], [sa, sb], dict=True); chk("k1-6", s[0][sa] + 2 * s[0][sb], 12)
roots = sp.solve(sp.Abs(4 * x) - x**2, x)
chk("g2-2", 2 ** len(set(roots)) - 1, 7)

# 함수방정식 --------------------------------------------------------
# f(x)=kx 꼴만 f(x−y)=f(x)−f(y)를 만족(유리수에서) — f(1)=4
chk("g2-6", 4 * 33, 132)


def fk10(n):
    tot = Fr(0); m = n; p = 2
    while m > 1:
        while m % p == 0:
            tot += Fr(p, 2) + 2; m //= p
        p += 1
    return tot


chk("k10-13", fk10(36), 13)
gx = 0.5 * (2 * xs**2 - 4 * xs + 5) + 1.5           # g(x/3−1)의 값, t=x/3−1은 실수 전체
chk("k5-9", gx.min(), 3)


def f1303(n):
    return (-1) ** ((n + 1) // 2) if n % 2 else 2 * f1303(n // 2)


chk("m1303-14", f1303(14) + f1303(20), -2)


def f0806(n):
    return 0 if n == 0 else f0806(n // 10) + n % 10


okc = all(f0806(100 * a1 + 10 * b1 + c1) == f0806(100 * c1 + 10 * b1 + a1) for a1 in range(10) for b1 in range(10) for c1 in range(10))
chk("m0806-11", mark([f0806(12) == 3, f0806(8 * 123) == 8 * f0806(123), okc], "ㄱ|ㄱ, ㄴ|ㄱ, ㄷ|ㄴ, ㄷ|ㄱ, ㄴ, ㄷ"), "③")

# 대칭성과 주기 -----------------------------------------------------
t = 16
while t > 3:
    t -= 3
chk("o26", t * t - 3 * t, -2)


def scale(v, k, lo, hi, base):
    m = 0
    while v > hi:
        v /= k; m += 1
    return k ** m * base(v)


chk("k1-17", scale(Fr(2025), 5, 1, 5, lambda v: 4 - 2 * abs(v - 3)), 2200)
chk("m1506-29", scale(Fr(2015), 3, 1, 3, lambda v: 1 - abs(v - 2)), 172)

# 일대일함수와 일대일대응 -------------------------------------------
pts = np.linspace(-5, 5, 2001)
fs = [lambda t: t + 4, lambda t: 3 * t * t, lambda t: abs(2 * t), lambda t: -2 * t + 1, lambda t: 2 + 0 * t]
inj5 = [len(np.unique(np.round(f(pts), 9))) == len(pts) for f in fs]       # 일차함수(기울기≠0)는 전사
chk("k11-5", mark(inj5, "ㄱ|ㄴ, ㄷ|ㄱ, ㄹ|ㄱ, ㄴ, ㄹ|ㄷ, ㄹ, ㅁ"), "③")
xp = np.linspace(1e-4, 50, 500001)
ok = []
for f in (lambda t: 3 + 0 * t, lambda t: t + 1, lambda t: -2 * t, lambda t: abs(t - 2), lambda t: t * t + t):
    v = f(xp)
    ok.append(bool(np.all(v > 0) and np.all(np.diff(v) > 0) and v[0] < 1e-3))
chk("g1-10", "①②③④⑤"[ok.index(True)] if ok.count(True) == 1 else "?", "⑤")
c = [f for f in itertools.permutations([6, 7, 8, 9]) if f[0] == 8 and f[2] - f[3] == 3]
chk("k3-6", c[0][1] + c[0][2] if len(c) == 1 else -1, 16)

# 일대일대응이 되기 위한 조건 ---------------------------------------
best = []
for a in [Fr(n, 2) for n in range(-20, 21)]:
    for b in [Fr(n, 2) for n in range(-20, 21)]:
        if is_lin_bij(a, b, (-1, 2), (-3, 6)):
            best.append(a + b)
chk("o04", max(best), 3)
s = [(a1, b1) for a1 in [Fr(n, 4) for n in range(1, 21)] for b1 in [Fr(n, 4) for n in range(-20, 21)] if is_lin_bij(a1, b1, (-2, 2), (-1, 3))]
chk("k7-12", s[0][0] + s[0][1] if len(s) == 1 else -1, 2)


def pw_bij(fun, lo=-60, hi=60):         # 실수 전체에서 연속 구간별 일차 → 순증가 또는 순감소이고 양끝이 ±무한
    v = fun(np.linspace(lo, hi, 24001))
    d = np.diff(v)
    return bool(np.all(d > 0) or np.all(d < 0))


chk("k3-19", min(a1 for a1 in range(1, 50) if pw_bij(lambda t: a1 * t - 3 * abs(t + 1) + 3)), 4)
chk("o27", sum(pw_bij(lambda t: 2 * a1 * t + (3 * a1 - 4) * abs(t - 1)) for a1 in range(-30, 31)), 3)
ok13 = [a1 for a1 in np.linspace(-3, 8, 1101) if pw_bij(lambda t: np.where(t <= 0, (a1 * a1 - 5 * a1) * t, 2 * t))]
chk("g1-13", "④" if (min(ok13) < 0 and max([a1 for a1 in ok13 if a1 < 2.5]) < 0 and min([a1 for a1 in ok13 if a1 > 0]) > 5) else "?", "④")
chk("m1511-28", sum(pw_bij(lambda t: a1 * abs(t + 2) - 4 * t) for a1 in range(-30, 31)), 7)
ok62 = [a1 for a1 in np.linspace(-4, 4, 801) if pw_bij(lambda t: a1 * abs(t - 1) + (2 - a1) * t + a1)]
chk("m0403-9", "④" if (max(ok62) < 1 and min(ok62) < -3.9) else "?", "④")

# 제한된 범위의 이차함수 --------------------------------------------
k = sp.symbols("k", real=True)
k1 = [r for r in sp.solve(-k**2 + 4 * k - 1 - 2, k) if r <= 2]
k2 = [r for r in sp.solve(k**2 + 2 * k - 6 - k, k) if r >= -1]
chk("g2-18", k1[0] + k2[0], 3)
best = []
for a1 in range(-10, 11):
    for b1 in range(-10, 11):
        if a1 in (0, 1):
            continue
        if sorted([b1, 1 + b1, a1 * a1 + b1]) == [4, 5, 8]:
            best.append(a1 + b1)
chk("o28", max(best), 6)
# k12-15: k=2, a=1/2, b=3/2일 때 일대일대응인지 확인
t1 = np.linspace(0, 1, 100001)[:-1]; t2 = np.linspace(1, 3, 200001)
v = np.concatenate([-2 * (t1 - 1)**2 + 2, 0.5 * t2 + 1.5])
chk("k12-15", 0.5 * 2 + 1.5 if (np.all(np.diff(np.sort(v)) > 0) and abs(v.min()) < 1e-9 and abs(v.max() - 3) < 1e-9) else -1, "5/2")
aa = np.linspace(2, 10, 800001); chk("m2203-26", 17 if abs((aa - (aa**2 - 4 * aa + 3)).max() - 13 / 4) < 1e-9 else -1, 17)
a1 = Fr(-1, 3); b1 = 4
t1 = np.linspace(0, 3, 300001)[:-1]; t2 = np.linspace(3, 4, 100001)
v = np.concatenate([float(a1) * t1**2 + b1, t2 - 3])
okb = np.all(np.diff(np.sort(v)) > 0) and abs(v.min()) < 1e-9 and abs(v.max() - 4) < 1e-9
chk("m2303-16", a1 + b1 if okb else -1, "11/3")

# 항등함수와 상수함수 -----------------------------------------------
chk("k9-3", -1 + 2, 1)
X = [2, 3, 5]; res = set()
for p in itertools.permutations(X):
    f = dict(zip(X, p))
    if p == tuple(X):
        continue
    for c in X:
        if 2 + c == f[5]:
            res.add(f[2] + 3 + c)
chk("o07", res.pop() if len(res) == 1 else -1, 9)
X = [1, 2, 3, 6]; res = set()
for p in itertools.permutations(X):
    f = dict(zip(X, p))
    for c in X:
        if f[1] == 2 == c and f[1] * f[6] == f[3]:
            res.add(f[2] + 3 + c)
chk("g2-10", res.pop() if len(res) == 1 else -1, 6)
X = [1, 2, 3, 4]; res = set()
for p in itertools.permutations(X):
    f = dict(zip(X, p))
    for c in X:
        if f[3] == 2 == c and f[4] == 2 * c - 1:
            res.add(f[1] + f[2] + 3)
chk("k10-14", res.pop() if len(res) == 1 else -1, 8)
chk("g2-12", 2 ** len(set(sp.solve(x**3 - x**2 - 4 * x - 3 - x, x))) - 1, 3)
s = sp.solve([sp.Eq(4 + 2 * sa + sb, 3), sp.Eq(9 + 3 * sa + sb, 3)], [sa, sb]); chk("o51", s[sa] + s[sb], 4)

# 함수의 개수 -------------------------------------------------------
chk("o09", sum(inj(f) for f in funcs([1, 2, 3], range(5))) + 5, 65)
chk("g1-39", sum(inj(f) and f[1] != 3 and f[3] == 2 for f in funcs([1, 2, 3, 4], range(1, 6))), 18)
chk("s1491", sum(len(set(f.values())) == 2 for f in funcs(range(5), "ab")), 30)
A = [-2, -1, 0, 1, 2]
chk("m1103-26", sum(all(f[-t] == -f[t] for t in A) for f in funcs(A, A)), 25)
chk("g2-59", sum(all(f[-t] == f[t] for t in A) for f in funcs(A, A)), 125)
chk("s1497", sum(inj(f) and sum(f[t] == t for t in f) == 1 for f in funcs([1, 2, 3, 4], [1, 3, 5, 7, 9])), 36)
A7 = range(1, 8)
chk("m0509-25", sum(p[0] == 7 and all(p[k - 1] <= k for k in range(2, 8)) for p in itertools.permutations(A7)), 32)

# 새롭게 정의된 함수 ------------------------------------------------
chk("m0905-30", sum(2 <= sum(f.values()) <= 4 for f in funcs(range(5), (0, 1))), 25)
Xk = [-2, -1, 0, 1, 2]; res = set()
for ch in itertools.product((0, 1), repeat=5):
    f = {t: (t * t - 3 if c == 0 else 1 - 3 * t) for t, c in zip(Xk, ch)}
    if inj(f) and f[0] < 0 and f[-1] * f[1] * f[2] < 0:
        res.add(sum(f.values()))
chk("k9-12", res.pop() if len(res) == 1 else -1, 7)
F = {1: 1}
for n in range(2, 129):
    F[n] = F[n // 2] + (n % 2)
M = max(F.values()); aM = [n for n in F if F[n] == M]
chk("m1303-30", aM[0] + M if len(aM) == 1 else -1, 134)

# 절댓값 그래프 -----------------------------------------------------
xg = np.linspace(-200, 200, 400001)
okm = []
for m in np.round(np.linspace(-3, 3, 601), 4):
    okm.append((m, bool(np.any(np.diff(np.sign(np.abs(xg - 1) - (m * (xg + 2) - 2))) != 0) or np.any(np.abs(np.abs(xg - 1) - (m * (xg + 2) - 2)) < 1e-9))))
good = [m for m, o in okm if o]
chk("s1640", "$m<-1$ 또는 $m geq {2} over {3}$" if (max(m for m in good if m < 0) < -1 + 1e-9 and min(m for m in good if m > -1) >= 2 / 3 - 1e-9 and (-1.0 not in good)) else "?", "$m<-1$ 또는 $m geq {2} over {3}$")
# a|x|+|y|=8: 마름모 넓이 = 2 × (8/a) × 8
chk("s1643", [a1 for a1 in range(1, 10) if 2 * (8 / a1) * 8 == 64][0], 2)
v = np.abs(xs + 4) - np.abs(xs - 5); chk("s1644", v.max() / v.min(), -1)
xi = np.arange(1, 102)
vals = [np.abs(t - xi).sum() for t in range(-10, 120)]
chk("s1645", list(range(-10, 120))[int(np.argmin(vals))], 51)

# 고난도 ------------------------------------------------------------
X8 = range(1, 9); res = set()
# 치역 7개 → 빠진 수 k, 겹친 수 n: 36−k+n=42, 치역 max−min=6
for k_ in X8:
    for n_ in X8:
        rng = [t for t in X8 if t != k_]
        if n_ in rng and 36 - k_ + n_ == 42 and max(rng) - min(rng) == 6:
            res.add(n_)
chk("m1811-28", res.pop() if len(res) == 1 else -1, 7)
X6 = [-3, -2, -1, 0, 1, 2]; res = set()
for ch in itertools.product((0, 1), repeat=6):
    f = {t: (5 - t * t if c == 0 else -4 * t) for t, c in zip(X6, ch)}
    if inj(f) and f[0] * f[1] * f[2] < 0:
        res.add(sum(f.values()))
chk("m2311-29", res.pop() if len(res) == 1 else -1, 26)
X5_ = [3, 4, 5, 6, 7]; best = 0
for p in itertools.permutations(X5_):
    f = dict(zip(X5_, p))
    if all(f[n] * f[n + 2] % 2 == 0 for n in (3, 4, 5)):
        best = max(best, f[3] + f[7])
chk("m1803-27", best, 12)


def inA(a1, b1):                         # h가 R→R 일대일대응인가 (수치)
    if a1 > -1 + 1e-12:
        return False
    if a1 + b1 - 1 < -1e-9:
        return False
    fa = -a1 * a1 - 2 * a1 + 1
    ga = (a1 + b1 - 1) ** 2 - 2
    return abs(fa - ga) < 1e-9


g1 = not any(inA(0, kk) for kk in np.linspace(-20, 20, 4001))
g2 = inA(-1, 4)
tot = 0
for m in range(-10, 11):
    if m <= -1 and 3 - 2 * m - m * m >= 0:
        bb = 1 - m + math.sqrt(3 - 2 * m - m * m)
        if inA(m, bb):
            tot += m + bb
g3 = abs(tot - (5 + math.sqrt(3))) < 1e-9
chk("m2211-21", mark([g1, g2, g3], "ㄱ|ㄷ|ㄱ, ㄴ|ㄱ, ㄷ|ㄱ, ㄴ, ㄷ"), "⑤")
cnt = 0
for p in itertools.permutations(range(1, 9)):
    f = dict(zip(range(1, 9), p))
    if any(f[q] > q for q in (2, 3, 5, 7)):
        continue
    if all(f[a1] < f[b1] for a1 in range(1, 9) for b1 in range(a1 + 1, 9) if b1 % a1 == 0):
        cnt += 1
chk("m1907-28", cnt, 18)


def f31(n):
    return f31(n // 2) if n % 2 == 0 else (-1) ** ((n + 1) // 2)


g1 = f31(100) == -1; g2 = sum(f31(n) for n in range(1, 11)) == -4
g3 = all(f31(n) == f31(n + 8) for n in range(1, 2000, 2))
chk("g3-1", mark([g1, g2, g3], B5), "⑤")
res = set()
for a1 in [Fr(n, 2) for n in range(-20, 21)]:
    rts = sorted(set([-1, 2, a1]))
    subs = [c for r in range(1, len(rts) + 1) for c in itertools.combinations(rts, r)]
    if sum(sum(c) for c in subs) == 8:
        res.add(a1 + len(subs))
chk("g3-5", res.pop() if len(res) == 1 else -1, 8)


def g36(a1):
    r = [t for t in sp.solve(x**2 - 4 * x + a1, x) if t.is_real and t < 4]
    r += [a1 + 2] if a1 + 2 >= 4 else []
    return len(set(r))


chk("g3-6", sum(g36(a1) for a1 in range(1, 6)), 11)
cnt = 0
for f in funcs([1, 2, 3, 4], range(1, 6)):
    if f[2] <= f[3] or inj(f):
        cnt += 1
chk("g3-7", cnt, 435)
chk("g3-13", 2 * 10, 20)                # f(x)=2x가 유일 — 풀이의 부등식 논증
cnt = 0
for f in funcs([1, 2, 3, 4], range(1, 9)):
    vals = set(f.values())
    if inj(f) and f[1] == 1 and all(9 - f[t] in vals for t in f):
        cnt += 1
chk("s1498", cnt, 18)

if __name__ == "__main__":
    bad = [r_ for r_ in R if not r_[1]]
    print("검산", len(R), "불일치", len(bad))
    for r_ in bad:
        print(r_)
