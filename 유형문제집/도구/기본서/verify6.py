# -*- coding: utf-8 -*-
"""기본서 6단원 답 검산 (data6.py의 순서대로, 문항마다 따로 계산)"""
import sys, os
from sympy import symbols, Rational as R, sqrt, solve, nsimplify, S, Max, Min, simplify
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data6

x, y, k, a, b, m, t = symbols("x y k a b m t", real=True)


def rng(f, lo, hi, n=4000):
    """구간 [lo, hi]에서 f의 최댓값, 최솟값 (꼭짓점 포함, 정확값)"""
    from sympy import diff, Poly
    pts = [S(lo), S(hi)] + [r for r in solve(diff(f, x), x) if lo <= r <= hi]
    vals = [simplify(f.subs(x, p)) for p in pts]
    return max(vals), min(vals)


ans = []
# 01
M_, m_ = None, None
kk = solve(rng(-2*x**2 + 12*x + k, 1, 4)[0] - 5, k)[0]; ans.append(rng(-2*x**2 + 12*x + kk, 1, 4)[1])
aa = [v for v in solve(sum(rng(x**2 - 2*x + a, -2, 3)) - 17, a)][0]; ans.append(aa)
kk = solve(rng(2*x**2 - 8*x + k, -2, 1)[1] + 5, k)[0]; ans.append(kk + rng(2*x**2 - 8*x + kk, -2, 1)[0])
# 02
s = solve([(a*(x - 1)**2 + b).subs(x, -3), (a*(x - 1)**2 + b).subs(x, -1) + 6], [a, b], dict=True)[0]
f = (a*(x - 1)**2 + b).subs(s); assert s[a] > 0 and rng(f, -1, 2)[0] == -6; ans.append(f.subs(x, -5))
ok = []
for av in [R(i, 4) for i in range(-40, 41) if i]:
    for kv in [solve(36*av + k + 47, k)[0]]:
        f = av*(x - 3)**2 + kv
        if abs(f.subs(x, 6)) + f.subs(x, -1) == 0 and rng(f, -3, 7)[1] == -47: ok.append(f.subs(x, 2))
assert len(set(ok)) == 1; ans.append(ok[0])
f = a*(x - 1)*(x - 5) + 4*a*x - 10; av = [v for v in solve(rng(f.subs(a, a), 0, 3)[1] + 2, a) if v > 0] if False else None
vals = [v for v in [R(i, 2) for i in range(1, 20)] if rng((a*(x - 1)*(x - 5) + 4*a*x - 10).subs(a, v), 0, 3)[1] == -2]
assert vals == [2]; ans.append(vals[0])
# 03
ms = set()
for mv in solve((-x**2 + 2*m*x - 3*m).subs(x, m) - 4, m) + solve((-x**2 + 2*m*x - 3*m).subs(x, -3) - 4, m) + solve((-x**2 + 2*m*x - 3*m).subs(x, 3) - 4, m):
    if rng(-x**2 + 2*mv*x - 3*mv, -3, 3)[0] == 4: ms.add(mv)
ans.append(sum(ms))
cands = solve((x**2 - 2*a*x + 6).subs(x, a) - 3, a) + solve((x**2 - 2*a*x + 6).subs(x, -2) - 3, a) + solve((x**2 - 2*a*x + 6).subs(x, 1) - 3, a)
good = [c for c in cands if c.is_rational and rng(x**2 - 2*c*x + 6, -2, 1)[1] == 3]; assert good == [2]; ans.append(2)
good = []
for mv in solve(m**2 + m - 6, m) + [R(7, 3)]:
    f = -x**2 - 2*mv*x + mv; vx = -mv
    mx = f.subs(x, vx) if vx <= -1 else f.subs(x, -1)
    if mx == 6: good.append(mv)
assert good == [2]; ans.append(2)
# 04
def g4(av):
    M_, m_ = rng(x**2 - 6*x + 10, av, av + 2); return M_ + m_
best = min(((g4(R(i, 10)), R(i, 10)) for i in range(-20, 60)), key=lambda z: z[0]); ans.append(best[1])
aset = set()
for av in solve(x**2 + 3*x + 2, x) + [S(-1)] + [R(i, 4) for i in range(-20, 20)]:
    if rng(x**2 - 4*x + av + 4, av, av + 3)[1] == -1: aset.add(av)
p = 1
for v in aset: p *= v
ans.append(p)
kset = set(kv for kv in [S(i) for i in range(-6, 7)] if rng(x**2 - 4*x + 5, kv, kv + 2) == (10, 2)); ans.append(sum(kset))
# 05
f = (3 + 2*x - x**2)**2 - 2*(3 + 2*x - x**2) + 2; vals = [f.subs(x, R(i, 1000)) for i in range(-1000, 1001)]; ans.append(nsimplify(max(vals) + min(vals)))
f = (x**2 + 4*x)**2 + 6*(x**2 + 4*x) - 5; vals = [f.subs(x, R(i, 500)) for i in range(0, 1001)]; ans.append(max(vals) + min(vals))
# 06
e = x**2 + 2*y**2 - 4*x - 16*y + 40; sp = solve([e.diff(x), e.diff(y)], [x, y]); ans.append(sp[x] + sp[y] + e.subs(sp))
f = 3*x**2 + (2 - x)**2; M_, m_ = rng(f, 0, 2); ans.append(M_ + m_)
import math
best = max(math.cos(th) * math.sqrt(6) + math.sin(th) * math.sqrt(3) for th in [i * 2 * math.pi / 200000 for i in range(200000)])
assert abs(best - 3) < 1e-6; ans.append(3)
vals = []
for kv in [R(i, 100) for i in range(-500, 51)]:
    r = solve(x**2 - 2*kv*x + kv**2 + 4*kv - 2, x)
    if all(ri.is_real for ri in r):
        r = r if len(r) == 2 else r * 2
        vals.append(simplify(r[0]**2 + r[1]**2))
ans.append(min(vals))
# 07
ans.append(max((2*u*(30 - 3*u)) for u in [R(i, 100) for i in range(1, 1000)]))
ans.append(max(2*(2*u + (-(4 + u)**2 + 8*(4 + u))) for u in [R(i, 100) for i in range(1, 400)]))
f = 2*x + (x**2 - 3*x - 4) - 1; M_, m_ = rng(f, -1, 4); ans.append(M_ + m_)
ans.append(30 + max(range(0, 51), key=lambda v: (30 + v)*(100 - 2*v)))
best = max(((10*u*(18 - 9*u)), u) for u in [R(i, 100) for i in range(1, 200)]); ans.append(best[0] + 10*best[1])
# STEP 3
ans.append(max(2*(2*u + (-(u)**2 + 51) - (u**2 + 1)) for u in [R(i, 100) for i in range(1, 500)]))
def S225(u):  # 사다리꼴 PRBQ 넓이 (CP=2u): PR=2√2(6-u), BQ=√2(12-u), 높이 PQ=√2u
    return (2*2**0.5*(6 - u) + 2**0.5*(12 - u)) / 2 * 2**0.5*u
ub = max((i / 1000 for i in range(1, 6000)), key=S225); assert abs(ub - 4) < 1e-9
ans.append(sqrt(2)*(12 - 4))
f = 2*x + (x**2 - 6*x + 5); M_, m_ = rng(f, 0, 5); ans.append(M_ - m_)
ans.append(max((1000 - 20*v)*(400 + 20*v) for v in range(0, 50)))
s = solve([9*a + k, a + k + 2], [a, k]); f = s[a]*(x + 3)**2 + s[k]
gmin = min(rng(f, R(i, 20), R(i, 20) + 2)[0] for i in range(-200, 100)); assert gmin == -2; ans.append(f.subs(x, -3))
fmin = (x**2 + 6*x + 12).subs(x, solve((x**2 + 6*x + 12).diff(x), x)[0]); gmax = (-x**2 - 2*x).subs(x, solve((-x**2 - 2*x).diff(x), x)[0]); ans.append(max(av for av in range(-10, 11) if fmin >= gmax + av))
# 2022.6.21 ㄷ 확인
best = max(av + bv for av, bv in [(R(i, 100), 5 - rng((x - R(i, 100))**2, 1, 2)[1]) for i in range(-300, 600)]); assert best == R(29, 4); ans.append("⑤")
sols = [f.subs(x, -2) for av in range(-10, 0) for bv in range(-10, 0) for f in [av*x**2 + bv*x + 5] if rng(f, 1, 2)[0] == 3]; assert len(set(sols)) == 1; ans.append(sols[0])
av = [v for v in solve(2*a**2 - 4*a + 4 - 10, a) if v > 0][0]; f = x**2 - 2*av*x + 2*av**2; assert rng(f, 0, 2)[1] == 10; ans.append(rng(f, 0, 2)[0])
f = (sqrt(3) - x)**2 + 2*(1 + x**2); xm = solve(f.diff(x), x)[0]; ans.append(simplify(f.subs(x, xm) / xm))
ans.append(max(R(1, 2)*(2 - u)*(3*u + 3) for u in [R(i, 1000) for i in range(1, 2000)]))
good = []
for bv in [R(i, 10) for i in range(1, 100)]:
    def g(kv, av=1):
        M_, m_ = rng(av*(x - bv)**2, kv, kv + 2); return M_ - m_
    if g(3) == 1:
        av = solve(a*(g(2) + g(6)) - 32, a)[0]; good.append(av*(6 - bv)**2)
assert len(set(good)) == 1; ans.append(good[0])
good = []
for bv in [R(i, 10) for i in range(1, 100)]:
    def g(kv):
        M_, m_ = rng((x - bv)**2, kv, kv + 2); return M_ + m_
    if g(2) == 10 and g(1) - g(4) > 0:
        av = 38 / (g(1) - g(4)); good.append(av*(7 - bv)**2)
assert len(set(good)) == 1; ans.append(good[0])
s = solve([16*a + k, 25*a + k + 9], [a, k]); f = s[a]*(x + 2)**2 + s[k]; assert s[a] < 0 and rng(f, -3, 3)[1] == -9; ans.append(f.subs(x, 1))
cnt = sum(1 for av in range(1, 20) for bv in range(1, 40) if (lambda Mm: Mm[0] <= 36 and Mm[1] >= 5)(rng((x - av)**2 + 2*bv, -2, 2))); ans.append(cnt)
good = [av for av in [R(i, 100) for i in range(-199, 800)] if rng(x**2 - 4*x + 1, -2, av)[1] == -2]; assert set(good) == {1}; ans.append(1)
good = [av for av in [R(i, 4) for i in range(1, 60)] if sum(rng(-2*x**2 + 16*x - 7, 0, av)) == 0]; ans.append(sum(good))

items = [p for _, _, ps in data6.TYPES for p in ps] + data6.STEP3
assert len(items) == len(ans) == 40, (len(items), len(ans))
bad = 0
for n, (it, v) in enumerate(zip(items, ans), 201):
    want = it["ans"]
    if want.startswith("⑤") or want.startswith("①"):
        ok = (want == v)
    else:
        w = want.replace("{", "(").replace("}", ")").replace(" over ", "/").replace("sqrt", "sqrt").replace(" ", "")
        w = w.replace("-(9)/(4)", "-9/4")
        w = __import__("re").sub(r"(\d)sqrt", r"\1*sqrt", w)
        ok = simplify(nsimplify(eval(w, {"sqrt": sqrt})) - v) == 0
    if not ok:
        bad += 1
        print("불일치", n, want, v)
print("문항", len(items), "불일치", bad)
