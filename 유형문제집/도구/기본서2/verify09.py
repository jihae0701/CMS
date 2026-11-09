# -*- coding: utf-8 -*-
"""공통수학2 기본서 9단원 함수 검산: 문항마다 답을 따로(모든 경우를 세거나 촘촘한 격자로) 계산해 data09.py의 답과 맞춘다.
python verify09.py
"""
import sys, os, re, math, itertools
import numpy as np
from fractions import Fraction as Fr
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data09

R = {}
rng = np.random.default_rng(3)


def lin(a, b, n=200001):
    return np.linspace(a, b, n)


# 01 ------------------------------------------------------------------
ok = [a for a in np.round(lin(-5, 5, 10001), 4) if all(-3 <= a * x - a - 1 <= 2 for x in (0, 2))]
assert abs(min(ok) + 2) < 1e-9 and abs(max(ok) - 2) < 1e-9
R["b26"] = "-2 leq a leq 2"

best = None
y = lambda x: abs(x + 2) + 2 * abs(x - 3)
for a in np.round(lin(-6, 6, 1201), 2):
    for b in np.round(lin(-6, 6, 1201), 2):
        if b < a:
            continue
        xs = np.linspace(a, b, 301)
        v = y(xs)
        lo = min(v.min(), min(y(a), y(b)))
        if 3 >= a and 3 <= b:
            lo = 5
        if abs(lo - 5) < 1e-6 and abs(max(v.max(), y(a), y(b)) - 13) < 1e-6:
            best = a + b if best is None else min(best, a + b)
R["g2-8"] = best

tot = Fr(0)
for num in range(-400, 401):
    a = Fr(num, 16)
    if all(a * x * x + 2 * (a + 1) * x + 3 in (-1, 3, 5) for x in (-2, 0, 2)):
        tot += a
R["b27"] = tot

# 02 ------------------------------------------------------------------
sa = set()
for a in [Fr(n, 4) for n in range(-40, 41)]:
    if a == -1:
        continue
    for b in range(-10, 11):
        if all(x**3 == 2 * x**3 - x * x + b * x for x in (-1, a)):
            sa.add(a)
R["b29"] = sum(sa)

sol = [(a, b) for a in range(-10, 11) for b in range(-10, 11)
       if all(2 * x * x - 4 * x + 3 == a * abs(x - 1) + b for x in (0, 1, 2))]
assert len(sol) == 1
R["b32"] = 2 * sol[0][0] - sol[0][1]

vals = set()
for a in [Fr(n, 4) for n in range(-40, 41)]:
    if a in (0, 1):
        continue
    for b in range(-10, 11):
        for c in range(-10, 11):
            if all(b * abs(x - 1) + c == (x - 1)**2 + 4 for x in (0, 1, a)):
                vals.add(b * abs(a - 1) + c + b * c)
assert len(vals) == 1
R["o25"] = vals.pop()

# 03 ------------------------------------------------------------------
f = lambda x: x * x + x                      # 조건을 만족시키는 함수(검산: 식 확인)
assert all(f(x + y) == f(x) + f(y) + 2 * x * y for x in range(-5, 6) for y in range(-5, 6)) and f(1) == 2
R["b2"] = f(5)

f = lambda x: -3 * x**3 - 3
for x in (-3, -2, -0.5, 0.5, 2, 3):
    assert abs(f(-x) / x**2 - x * f(1 / x) - 6 * x) < 1e-9
R["g2-7"] = f(2)


def fac(n):
    out, p = [], 2
    while n > 1:
        while n % p == 0:
            out.append(p); n //= p
        p += 1
    return out


R["g2-4"] = sum(fac(240)) - (len(fac(240)) - 1)

# 04 ------------------------------------------------------------------
def f23(x):
    x = x - 2 * math.floor((x + 1) / 2)          # 주기 2로 [−1, 1)로
    return (x + 1)**2 if x <= 0 else (-x + 1)**2
R["b23"] = f23(121 / 2)

def f767(x):
    x = x - 4 * math.floor((x + 2) / 4)
    return -abs(x) + 1
xs = lin(-40, 40, 800001) + 1e-7
cnts = {}
for n in range(1, 20):
    d = np.array([f767(v) for v in xs[::10]]) - xs[::10] / n
    cnts[n] = int(np.sum(d[:-1] * d[1:] < 0))
R["g2-5"] = [n for n in cnts if cnts[n] == 7][0]

def f1506(x):
    k = 0
    while x > 4:
        x /= 2; k += 1
    while x < 2:
        x *= 2; k -= 1
    return 2**k * (1 - abs(x - 3))
R["h1506-29"] = f1506(100)

# 05 ------------------------------------------------------------------
a, b = 8, -2
assert 2 * (-3) + b == -a and 2 * 5 + b == a
R["b33"] = a * a + b * b

bs = []
for b in range(-5, 6):
    a = b + Fr(5, 4)                              # 이어짐 조건
    if 2 * a - 1 > 0:
        bs.append(b)
R["b37"] = min(bs)

R["o05"] = sum(1 for a in range(-20, 21) if (a + 5) * (4 - 2 * a) > 0 and (a + 5) * 1 - 1 == (4 - 2 * a) * 1 + 3 * a)

ks = [k for k in np.round(lin(-6, 6, 1201), 2)
      if np.all(np.diff(np.abs(2 * lin(-5, 5, 2001) - 1) - k * lin(-5, 5, 2001) + 1) > 0)
      or np.all(np.diff(np.abs(2 * lin(-5, 5, 2001) - 1) - k * lin(-5, 5, 2001) + 1) < 0)]
assert min(k for k in ks if k > 0) > 2 and max(k for k in ks if k < 0) < -2 and 2.01 in ks and -2.01 in ks
R["b44"] = "k<-2~또는~k>2"

# 06 ------------------------------------------------------------------
R["b54"] = 2 - (-1)
a = Fr(1, 3); b = 1
assert a * 9 + b == 4
R["o50"] = a * 1 + b
av = lin(3, 10, 700001)
R["h2203-26"] = (av - (av**2 - 6 * av + 5)).max()

# 07 ------------------------------------------------------------------
res = []
for f in itertools.permutations((2, 4, 8)):
    F = dict(zip((2, 4, 8), f))
    for c in (2, 4, 8):
        if F[2] == 4 == c and F[2] * F[8] == F[4] and F != {2: 2, 4: 4, 8: 8}:
            res.append(F[4] + 8 + c)
assert len(set(res)) == 1
R["b55"] = res[0]

sol = [(a, b) for a in range(-10, 11) for b in range(-10, 11) if 2 == 1 + a + b == 4 + 2 * a + b]
R["g2-13"] = sol[0][0] * sol[0][1]

xs = lin(-10, 10, 2000001)
fx = np.where(xs < 2, np.abs(3 * xs - 2), 4)
fixed = xs[np.abs(fx - xs) < 2e-5]
groups = []
for x in fixed:
    if not groups or x - groups[-1][-1] > 1e-3:
        groups.append([x])
    else:
        groups[-1].append(x)
assert len(groups) == 3
R["o32"] = sum(np.mean(g) for g in groups)

# 08 ------------------------------------------------------------------
R["b69"] = sum(1 for p in itertools.permutations(range(1, 7)) if all(p[a - 1] + p[6 - a] == 7 for a in range(1, 7)))
R["b74"] = sum(1 for p in itertools.permutations(range(1, 8), 4) if (p[0] + p[1] + p[2]) % 2)
R["o03"] = sum(1 for f in itertools.product(range(1, 6), repeat=5) if f[0] < f[2] < f[4] and f[1] < f[3])
R["h0509-25"] = sum(1 for p in itertools.permutations(range(1, 9)) if p[0] == 8 and all(p[k - 1] <= k for k in range(2, 9)))

# 09 ------------------------------------------------------------------
# b67: X를 몇 가지 집합(유한 표본)으로 바꾸어 보기 판정
samples = [set(), {0}, set(range(-5, 6)), {1, 2, 3}, {-1, 3}]
dom = range(-6, 7)
fA = lambda A, x: 1 if x in A else 3
t1 = fA(set(range(-100, 101)), -1) + fA(set(range(-100, 101)), 3) == 2
t2 = all({fA(X, x) for x in dom} == {1} for X in samples)
t3 = all(fA(X | Y, x) == fA(X, x) + fA(Y, x) for X in samples for Y in samples for x in dom)
t4 = all(fA(set(dom) - X, x) == 4 - fA(X, x) for X in samples for x in dom)
R["b67"] = ", ".join(n for n, v in zip("ㄱㄴㄷㄹ", (t1, t2, t3, t4)) if v)

ks = set()
for vals in itertools.combinations(range(1, 9), 7):
    if max(vals) - min(vals) == 6:
        for k in vals:
            if sum(vals) + k == 40:
                ks.add(k)
assert len(ks) == 1
R["g2-9"] = ks.pop()

def digit(n):
    return 0 if n == 0 else digit(n // 10) + n % 10
R["h1211-20"] = sum(1 for n in range(100, 1000) if digit(n) == 6)

# STEP 3 --------------------------------------------------------------
ns = set()
for vals in itertools.combinations(range(1, 8), 6):
    if sum(v % 2 for v in vals) == 3:
        for n in vals:
            if sum(vals) + n == 23:
                ns.add(n)
assert len(ns) == 1
R["o47"] = ns.pop()

A = {x: x * x - 6 * x + 4 for x in range(1, 7)}
B = {x: -x * x + 8 * x - 8 for x in range(1, 7)}
sums = set()
for ch in itertools.product((0, 1), repeat=6):
    v = [B[x] if c else A[x] for x, c in zip(range(1, 7), ch)]
    if len(set(v)) == 6:
        sums.add(sum(v))
assert len(sums) == 1
R["o48"] = sums.pop()

R["o56"] = sum(1 for f in itertools.product(range(1, 6), repeat=5)
               if len({f[0], f[1], f[2]}) == 3 and len(set(f)) < 5)

# g3-22: 칸토어 계단 꼴 — (가)(나)(다)로 정해지는 함숫값을 재귀로 계산
def cantor(x, depth=40):
    if depth == 0:
        return 0.5
    if x <= 1 / 3:
        return cantor(3 * x, depth - 1) / 2 if x > 0 else 0.0
    if x >= 2 / 3:
        return 1 - cantor(1 - x, depth - 1)
    return 0.5
R["g3-22"] = cantor(14 / 15)

c = 0
for f in itertools.product(range(1, 7), repeat=6):
    F = dict(zip(range(1, 7), f))
    if F[5] == 5 and all(F[m] < F[n] for m in range(1, 7) for n in (2 * m, 2 * m + 1) if n <= 6):
        c += 1
R["b77"] = c

xs = lin(-30, 30, 6001)
cnt = 0
for a in range(-10, 11):
    for b in range(-10, 11):
        v = xs * xs - np.abs(a * xs * xs - a * xs + b)
        d = np.diff(v)
        if (np.all(d > 0) or np.all(d < 0)) and abs(v[-1]) > 10:   # 양 끝으로 한없이 커지거나 작아지는 일대일대응
            cnt += 1
R["m132"] = cnt

# m133: f(x)=c^x 꼴과 f=1 로 보기 확인 (ㅁ은 f=1이 반례)
# m133: 조건을 만족시키는 함수 f(x)=c^x (c>0)와 f(x)=1로 보기를 확인한다(ㄱ~ㄹ은 해설의 대입으로 증명, ㅁ은 f=1이 반례).
fs = [lambda x, c=c: c**x for c in (0.5, 1.0, 2.0, 3.0)]
pts = rng.uniform(-3, 3, (200, 2))
tv = [all(abs(f(0) - 1) < 1e-12 for f in fs),
      all(abs(f(a) - 1 / f(-a)) < 1e-9 for f in fs for a, _ in pts),
      all(abs(f(a - b) - f(a) / f(b)) < 1e-9 for f in fs for a, b in pts),
      all(f(a) > 0 for f in fs for a, _ in pts),
      all(len({round(f(x), 9) for x in (0, 1, 2)}) == 3 for f in fs)]
R["m133"] = ", ".join(n for n, v in zip("ㄱㄴㄷㄹㅁ", tv) if v)

for a in [Fr(n, 2) for n in range(1, 30)]:
    f = lambda x: abs(x - a) - a if x >= 0 else -(abs(-x - a) - a)
    if f(-5) + f(15) == 0:
        R["m141"] = a

R["m146"] = sum(1 for n in range(1, 101) if bin(n).count("1") == 3)

res = set()
for g in itertools.permutations(range(1, 5)):
    G = dict(zip(range(1, 5), g))
    if G[2] != 1:
        continue
    H = {x: max(x, G[x]) for x in range(1, 5)}
    if len(set(H.values())) == 2:
        res.add(G[4] + H[1])
assert len(res) == 1
R["m148"] = res.pop()

def cnt150(t, k):
    f = lambda x: (x - 1)**2 + 5
    g = lambda x: 11 - abs(x - t)
    c = []
    if k >= 5:
        r = math.sqrt(k - 5); c += [1 - r, 1 + r]
    if k <= 11:
        c += [t - (11 - k), t + (11 - k)]
    pts = []
    for x in c:
        if abs(min(f(x), g(x)) - k) < 1e-9 and all(abs(x - y) > 1e-7 for y in pts):
            pts.append(x)
    return len(pts)
ks = set()
for k in range(1, 12):
    cands = list(np.linspace(-15, 15, 3001))
    if k >= 5:
        r = math.sqrt(k - 5)
        cands += [x0 + s * (11 - k) for x0 in (1 - r, 1 + r) for s in (1, -1)]
    if any(cnt150(t, k) == 3 for t in cands):
        ks.add(k)
R["m150"] = sum(ks)


# 대조 ---------------------------------------------------------------
def val(s):
    s = s.replace(" ", "").replace("it-", "-")
    s = re.sub(r"sqrt\{([^{}]*)\}", r"sqrt(\1)", s)
    s = re.sub(r"\{([^{}]*)\}over\{([^{}]*)\}", r"((\1)/(\2))", s)
    return eval(s, {"sqrt": math.sqrt})


bad = 0
items = [p for _, _, ps in data09.TYPES for p in ps] + data09.STEP3
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
