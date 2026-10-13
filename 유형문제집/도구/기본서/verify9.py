# -*- coding: utf-8 -*-
"""기본서 9단원 정답 검산: 문항마다 전수·sympy 계산으로 따로 풀어 data9의 답과 맞춘다.  python verify9.py"""
import math, sys, os
from fractions import Fraction as Fr
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sympy import symbols, solve, Rational as R, sqrt, nsimplify, simplify
import data9

GRID = [Fr(i, 40) for i in range(-1200, 1201)]     # -30 ~ 30, 0.025 간격
ans = []

# ---- 01
ans.append(max(k for k in range(-20, 20) if not any(abs(x + 2) + abs(x - 2) < k for x in GRID)))
f = lambda t: t*t - 2*t - 3; g = lambda t: t*t + t - 5; h = lambda t: t*t + 4*t + 3
ok = [t for t in GRID if abs(f(t) - g(t)) + abs(g(t) - h(t)) < 12]
assert all(-3 < t < 1 for t in ok) and min(ok) == Fr(-3) + Fr(1, 40) and max(ok) == 1 - Fr(1, 40)
ans.append(-3 + 1)
# ---- 02
ans.append(sum(a for a in range(-50, 50) if sum(1 for x in range(1, 100) if 3*x - 8 < 2*x - 3 < 4*x - a) == 2))
good = [a for a in [Fr(i, 20) for i in range(-200, 200)]
        if sum(1 for x in range(-50, 50) if Fr(5, 10)*(x - 1) >= Fr(3, 10)*x - Fr(9, 10) and 2*(x - 1) + a <= 3) == 5]
assert min(good) == -1 + Fr(1, 20) and max(good) == 1
ans.append("-1<a leq 1")
# ---- 03 (마지막 의자에 1~8명)
ans.append(min(x for x in range(6, 200) if 8*(x - 6) + 1 <= 7*x + 5 <= 8*(x - 6) + 8))
ans.append(max(x for x in range(3, 200) if 4*(x - 3) + 1 <= 3*x + 5 <= 4*(x - 3) + 4))
# ---- 04
cnt = 0
for k in range(-100, 100):
    s = sum(x for x in range(k - 6, k + 7) if x*x - x - 6 > 0)
    cnt += 1 <= s <= 100
ans.append(cnt)
good = [k for k in [Fr(i, 20) for i in range(1, 200)] if sum(1 for x in range(-10, 20) if abs(x - 3) < k and x*x - 3*x - 4 <= 0) == 3]
ans.append(max(good))
# ---- 05
X = [Fr(i, 400) for i in range(-400, 401)]
ans.append(4 * (max(x*x - 2*x for x in X) - min(x*x - x for x in X)))
mn, nn = symbols("m n", real=True)
sol = [s for s in solve([(mn - 3)**2 - 4*(nn - 2), (mn + 1)**2 - 4*(4 - nn)], [mn, nn])]
assert sol == [(1, 3)]
assert all(-x*x + 3*x + 2 <= x + 3 <= x*x - x + 4 for x in GRID)
ans.append(1 + 9)
# ---- 06 (반올림: m-1/2 ≤ v < m+1/2)
xs = []
for m in range(-200, 200):
    x = Fr(m - 1, 4)
    v = (x + 1)*(x - 2)
    if m - Fr(1, 2) <= v < m + Fr(1, 2):
        xs.append(x)
ans.append(sum(xs))
xs = []
for n in range(-100, 100):
    x = Fr(n + 1, 2)
    v = x*x + x - Fr(1, 2)
    if n - Fr(1, 2) <= v < n + Fr(1, 2):
        xs.append(x)
assert len(xs) == 1
ans.append(xs[0])
# ---- 07
def roots(a, b, c):
    d = b*b - 4*a*c
    if d < 0: return None
    return ((-b - math.sqrt(d))/(2*a), (-b + math.sqrt(d))/(2*a))
good = [a for a in [i/8 for i in range(-160, 160)] if (r := roots(1, 2*a, 2*a + 8)) and r[0] != r[1] and r[1] < 2]
assert min(good) == 4 + 1/8 and 4 not in good
ans.append("a>4")
ans.append(sum(a for a in range(-50, 50) if (r := roots(1, -8, a + 3)) and r[0] >= 3))
good = [k for k in [i/64 for i in range(-640, 640)] if (r := roots(2, 5, k)) and r[1] < -1]   # x=-2는 늘 근
assert min(good) == 3 + 1/64 and max(good) == 25/8
ans.append(R(3)*R(25, 8))
good = [a for a in [i/8 for i in range(-400, 200)] if (r := roots(1, -2, a)) and any(-2 < z < 2 for z in r)]
assert min(good) == -8 + 1/8 and max(good) == 1
ans.append(9)
good = [a for a in [i/8 for i in range(-400, 200)] if (r := roots(1, 4, a - 3)) and any(-3 < z < 3 for z in r)]
assert min(good) == -18 + 1/8 and max(good) == 7
ans.append(abs(-18 + 7))
# ---- STEP 3
ans.append(min(abs(x + 3) + abs(x - 2) for x in GRID))
ok = [x for x in GRID if abs(x - 1) <= abs(x - 2) < -x + 3]
ans.append(max(ok))
ok = [x for x in range(0, 401) if Fr(40, 100)*x + Fr(20, 100)*(400 - x) <= 140 and Fr(10, 100)*x + Fr(5, 100)*(400 - x) >= 25]
assert (min(ok), max(ok)) == (100, 300)
ans.append("100 rm g 이상 300 rm g 이하")
ans.append(max(x for x in range(2, 200) if 9*(x - 2) + 1 <= 7*x + 5 <= 9*(x - 2) + 9))
# 해 [1,3]∪{4}: (x-3)(x-4)≥0, (x-1)(x-4)≤0
a_, b_, c_, d_ = -7, 12, -5, 4
S = [x for x in [Fr(i, 20) for i in range(-200, 200)] if x*x + a_*x + b_ >= 0 and x*x + c_*x + d_ <= 0]
assert S == [x for x in [Fr(i, 20) for i in range(-200, 200)] if 1 <= x <= 3 or x == 4]
ans.append(a_ + b_ + c_ + d_)
ans.append(sum(k for k in range(-50, 0) if any(x*x + 2*x - 24 < 0 and x*x - 2*k*x - 3*k*k >= 0 for x in GRID)))
ks = [k for k in range(-50, 50) if sum(1 for x in range(1, 100) if x*x - 2*x - 24 <= 0 and x*x - (k + 1)*x + k <= 0) == 3]
assert len(ks) == 1
ans.append(ks[0])
ans.append(sum(a for a in range(1, 100) if sum(1 for x in range(-100, 100) if 3*x <= 2*x + 9 < 4*x + a) == 7))
tot = 0
for a in [Fr(i, 8) for i in range(-80, 160)]:
    S = [x for x in [Fr(i, 80) for i in range(-2000, 2400)] if x*x - 11*x + 24 > 0 and abs(x - a) < 2]
    if not S: continue
    # 한 구간이고 길이 2인지(격자 간격 1/80)
    if all(q - p == Fr(1, 80) for p, q in zip(S, S[1:])) and S[-1] - S[0] == 2 - Fr(2, 80):
        tot += a
ans.append(tot)
best = 0
for a in range(-10, 15):
    for b in [Fr(i, 4) for i in range(-40, 40)]:
        if all(-2 <= (a - 2)*x + b <= x*x + 2*x + 5 for x in GRID[::4]):
            best = max(best, a*a + b*b)
ans.append(best)
ks = []
for al in range(-30, 3):
    be = 6 - al
    if al >= be: continue
    k = 4 - al*be
    fa, fb = (al - 2)**2, (be - 2)**2
    if sum(1 for x in range(-200, 200) if fa < abs(2*x + k) < fb) == 2:
        ks.append(k)
assert ks == [-4], ks
ans.append(-4)
def rnd1(v):           # 소수점 아래 둘째 자리에서 반올림
    return math.floor(v*10 + Fr(1, 2)) / Fr(10)
X = [Fr(i, 1000) for i in range(1, 20001)]
ok = [x for x in X if (2*x/5 - 1) > 0 and rnd1(2*x/5 - 1) >= 2 and rnd1(abs(2*x + 1)) < 20]
assert ok[0] == Fr(7375, 1000) and ok[-1] == Fr(9474, 1000)
ans.append(10*(Fr(9475, 1000) - Fr(7375, 1000)))
ans.append(min(a for a in range(-20, 20) if 1 - 4*a < 0 or 12*a*a - 12*(a + 1)**2 < 0))
ks = []
for k in range(-20, 20):
    r = roots(1, -2*(k - 1), 2*k + 1)
    if r and all(-1 - 1e-9 <= z <= 5 + 1e-9 for z in r):
        ks.append(k)
ans.append("%s" % ", ".join(map(str, ks)))
ks = []
for k in range(1, 50):
    r = roots(1, -4, k)
    if r and r[0] < 2 < r[1]:
        ks.append(k)
ans.append(sum(ks))

items = [p for _, _, ps in data9.TYPES for p in ps] + data9.STEP3
assert len(items) == len(ans) == 32, (len(items), len(ans))
bad = 0
for no, (it, v) in enumerate(zip(items, ans), 320):
    want = it["ans"].replace("$", "")
    if isinstance(v, str):
        ok = (want == v)
    else:
        w = want.replace("{", "(").replace("}", ")").replace(" over ", "/").replace(" ", "")
        ok = simplify(nsimplify(eval(w, {"sqrt": sqrt})) - nsimplify(v)) == 0
    if not ok:
        bad += 1
        print("불일치", no, want, v)
print("문항", len(items), "불일치", bad)
