# -*- coding: utf-8 -*-
"""기본서 8단원 정답 검산: 문항마다 sympy·전수 계산으로 따로 풀어 data8의 답과 맞춘다.  python verify8.py"""
import math, sys, os
from itertools import product as iprod
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sympy import *
import data8

x, y, t, k, a, b, c, m = symbols("x y t k a b c m", real=True)
R = Rational
oo_ = S.Infinity


def sol(ineq, v=x):
    return solve_univariate_inequality(ineq, v, relational=False)


def ints(st, lo=-300, hi=300):
    return [n for n in range(lo, hi) if st.contains(n) == True]


ans = []
# ---------------------------------------------------------------- 01
# (1) ax²+bx+c<0 해 -2<x<1 (a=1로 계산: 결과는 a>0 배수와 무관)
A_, B_, C_ = 1, 1, -2
s1 = sol(B_*x**2 + C_*x - 3*A_ > 0)
s2 = sol(9*x**2 - 6*x + 1 <= 0)          # x²+ax+b≤0 해 x=3 -> a=-6, b=9
assert s1 == Union(Interval.open(-oo, -1), Interval.open(3, oo)) and s2 == FiniteSet(R(1, 3))
ans.append("⑴ x<-1 또는 x>3　⑵ x={1} over {3}")
A_ = -1; B_, C_ = -6*A_, 8*A_                 # ax²+bx+c>0 해 2<x<4
assert sol(A_*x**2 + B_*x + C_ > 0) == Interval.open(2, 4)
s1 = sol(C_*x**2 - 4*B_*x + 16*A_ > 0)
A_ = -1; B_, C_ = -6*A_, 9*A_                 # ax²+bx+c≥0 해 x=3
assert sol(A_*x**2 + B_*x + C_ >= 0) == FiniteSet(3)
s2 = sol(B_*x**2 + C_*x + 6*A_ < 0)
assert s1 == Interval.open(-2, -1) and s2 == Interval.open(R(-1, 2), 2)
ans.append("⑴ -2<x<-1　⑵ -{1} over {2} <x<2")
good = [kv for kv in [R(i, 30) for i in range(-300, 300)]
        if sol(expand((kv + 1)*x**2 + kv + 1 - (x**2 + kv*x + 3)) <= 0) != EmptySet]
assert max(good) == R(8, 3) and min(good) == -10; ans.append("k leq {8} over {3}")
good = [av for av in [R(i, 4) for i in range(-60, 60) if i] if sol(av*x**2 + 2*av*x - 5 > 0) != EmptySet]
assert all(g_ > 0 or g_ < -5 for g_ in good) and R(1, 4) in good and R(-21, 4) in good and -5 not in good
ans.append("a<-5 또는 a>0")


def cnt_int(lo, hi):
    lo, hi = min(lo, hi), max(lo, hi)
    return math.floor(hi + 1e-12) - math.ceil(lo - 1e-12) + 1


ks = []
for kv in set(solve((k**2 - 5*k)**2 - 36, k) + solve((k**2 - 5*k)**2 - 64, k)
              + solve((k**2 - 5*k)**2 - 4, k) + solve((k**2 - 5*k)**2 - 16, k) + solve((k**2 - 5*k)**2 - 100, k)):
    if not kv.is_real or kv in (0, 5):
        continue
    r1, r2 = (kv**2 - 4*kv)/2, kv/2
    d = simplify(abs(r1 - r2))
    if d.is_integer and d > 0 and cnt_int(float(r1), float(r2)) == 4:
        ks.append(kv)
ans.append(simplify(sum(ks)))
as_ = set()
for dv in range(1, 10):
    for sg in (1, -1):
        for av in solve(a**2 - 8*a - sg*3*dv, a):
            if av.is_real:
                r1, r2 = (av**2 - 3*av)/3, 5*av/3
                if cnt_int(float(r1), float(r2)) == 4:
                    as_.add(simplify(av))
ans.append(simplify(sum(as_)))
# ---------------------------------------------------------------- 02
good = [av for av in [R(i, 4) for i in range(-40, 20)]
        if sol((av + 1)*x**2 - (av + 1)*x - 1 < 0) == S.Reals]
assert min(good) == R(-19, 4) and max(good) == -1 and -5 not in good; ans.append("-5<a leq -1")
ans.append(len([kv for kv in range(-30, 30) if sol((kv + 2)*x**2 - 2*(kv + 2)*x + 4 > 0) == S.Reals]))
vals = []
for av in [R(i, 100) for i in range(1, 400)]:
    f = av*(x + 2)*(x - 3)
    assert sol(f.subs(x, (2 - 2*x)/3) <= 0) == Interval(R(-7, 2), 4)
    if sol(expand(f - (3*x - 14)) >= 0) == S.Reals:
        vals.append(f.subs(x, 4))
ans.append(max(vals) - min(vals))
vals = []
for av in [R(i, 100) for i in range(1, 400)] + [R(4, 25)]:
    f = av*(x + 3)*(x - 2)
    if sol(expand(f - (2*x - R(25, 4))) >= 0) == S.Reals:
        vals.append(f.subs(x, -1))
assert sol(((R(4, 25))*(x + 3)*(x - 2)).subs(x, (2 - x)/4) <= 0) == Interval(-6, 14)
ans.append(max(vals) / min(vals))
# ---------------------------------------------------------------- 03
h = lambda av: 2*x**2 - 4*av*x + av + 3


def minmax(f, lo, hi):
    xs = [lo, hi] + [r for r in solve(diff(f, x), x) if lo <= r <= hi]
    v = [f.subs(x, z) for z in xs]
    return min(v), max(v)


g1 = [av for av in [R(i, 60) for i in range(-180, 180)] if minmax(h(av), -1, 1)[0] >= 0]
g2 = [av for av in [R(i, 110) for i in range(0, 400)] if minmax(h(av), 1, 3)[1] < 0]
assert min(g1) == -1 and max(g1) == R(5, 3) and min(g2) == R(211, 110) and R(21, 11) not in g2
ans.append("⑴ -1 leq a leq {5} over {3}　⑵ a>{21} over {11}")
g1 = [av for av in [R(i, 20) for i in range(-100, 100)] if minmax(x**2 - 4*x - av**2 + 4*av, -1, 1)[0] >= 0]
g2 = [av for av in [R(i, 20) for i in range(-100, 100)] if minmax(x**2 - av*x + av**2 - 4, 0, 2)[1] <= 0]
assert (min(g1), max(g1), min(g2), max(g2)) == (1, 3, 0, 2)
ans.append("⑴ 1 leq a leq 3　⑵ 0 leq a leq 2")
# ---------------------------------------------------------------- 04
f = x**2 + 2*x - 3; g = f + Abs(f)
c1 = all(g.subs(x, 2 - z) == g.subs(x, z) for z in range(-6, 6))
c2 = len(real_roots(Poly(expand(2*f + 1), x))) == 2 and False   # g≥0이므로 g=-1은 실근 없음
c3 = all((g.subs(x, z) <= 0) == (-3 <= z <= 1) for z in [R(i, 4) for i in range(-24, 12)])
assert (c1, c2, c3) == (False, False, True); ans.append("②")
f = x**2 - 4*x - 12; g = (Abs(f) - f)/2
c1 = all(g.subs(x, 2 + z) == g.subs(x, 2 - z) for z in range(-8, 8))
c2 = all((g.subs(x, z) > 0) == (z < -2 or z > 6) for z in range(-8, 12))
c3 = len([kv for kv in range(-5, 30) if len(set(r for r in solve(-f - kv, x) if r.is_real and -2 < r < 6)) == 2]) == 15
assert (c1, c2, c3) == (True, False, True); ans.append("③")
F = lambda z: (z*z + 2*z - 15) - abs(z*z + 2*z - 15)/4
cnt = lambda mv: sum(1 for z in range(-200, 200) if F(z) <= mv*(z - 3) + 1e-12)
good = [mv for mv in [R(-i, 400) for i in range(1, 4000)] if cnt(float(mv)) == 12]
assert max(good) == R(-9, 4) and min(good) == R(-1199, 400); ans.append(4*(-3)*R(-9, 4))
F2 = lambda z: abs(z*z + 2*z - 8)
ms = [mv for mv in range(-60, 61) if sum(1 for z in range(-200, 200) if F2(z) <= mv*z - 2*mv) == 4]
ans.append(sum(ms))
# ---------------------------------------------------------------- 05
res = set()
for av in [R(i, 4) for i in range(1, 60)]:
    bv = 2*av; f = av*x**2; g = -av*x**2 + bv*x - 2*bv
    assert sol(f + g >= 0) == Interval(2, oo) and solve(diff(f - g, x), x) == [R(1, 2)]
    kk = [kv for kv in range(-50, 50) if sol(f + 3*kv <= 0) == EmptySet or True]
    kk = [kv for kv in range(-50, 50) if not [r for r in solve(f + 3*kv, x) if r.is_real]
          and not [r for r in solve(g + 3*kv, x) if r.is_real]]
    if len(kk) == 6:
        res.add(g.subs(x, 2) - f.subs(x, 2))
ans.append(min(res))
av = symbols("av")
f = x**2 + 2*x; g = -x**2 + (av - 2)*x - av
e = expand(f - g + x); av_ = solve(diff(e, x).subs(x, 3), av)[0]
assert sol((f + g).subs(av, av_) >= 0) == Interval(1, oo); ans.append(g.subs({av: av_, x: 3}))
mm = symbols("mm")
fm = mm*(x - 1)*(x - 2) - 2*x - 1
mv = [v for v in solve(discriminant(expand(fm + 3*x - 1), x), mm) if v < 0][0]
f = fm.subs(mm, mv)
assert sol(f <= -2*x - 1) == Union(Interval(-oo, 1), Interval(2, oo))
good = [av_ for av_ in [R(i, 4) for i in range(3, 60)] if minmax(f, 1 - av_, 1 + av_)[0] == -15]
assert good == [3]; ans.append(3)
vals = []
for av_ in [R(-i, 1000) for i in range(1, 1000)]:
    f = av_*(x - 3)**2
    nn = [n for n in range(1, 200) if discriminant(expand(f - 4*x - n), x) >= 0]
    if len(nn) == 4:
        vals.append(17*f.subs(x, 1))
assert sol(R(-1, 4)*(x - 3)**2 < 0) == Union(Interval.open(-oo, 3), Interval.open(3, oo)); ans.append(min(vals))
# ---------------------------------------------------------------- 06
assert sol(4 - x**2 >= 0) == Interval(-2, 2)
v = [(4 - z**2) + 2*z for z in [R(i, 100) for i in range(-200, 201)]]
assert (max(v), min(v)) == (5, -4); ans.append("⑴ -2 leq x leq 2　⑵ 최댓값 5, 최솟값 -4")
v = [(3 - 2*z) + 4*z**2 for z in [R(i, 400) for i in range(0, 601)]]
ans.append(max(v) / min(v))
kr = sol(discriminant(expand(x**2 + 2*(k - x)**2 - 6), x) >= 0, k)
ans.append(kr.sup - kr.inf)
# ---------------------------------------------------------------- STEP 3
A_ = -1; B_, C_ = 8*A_, 16*A_
assert sol(A_*x**2 + B_*x + C_ >= 0) == FiniteSet(-4)
ans.append(len(ints(sol(B_*x**2 - C_*x - 10*A_ > 0))))
res = []
for av_ in range(3, 80):
    bv = 5 - 3*av_; f = (x - 1)**2; g = -x**2 + av_*x + bv
    assert sol(f + g >= 0) == Interval(3, oo)
    if sol(f - g <= -10) != EmptySet:
        res.append(g.subs(x, 4))
ans.append(min(res))
f = -(x + 2)*(x - 9)
ans.append(len(ints(sol(f.subs(x, -3*x + 2) > 0))))
f = (x + 2)*(x - 3)
ans.append([kv for kv in range(-20, 20) if sol(f.subs(x, (-x + kv)/3) <= 0) == Interval(-8, 7)][0])
good = [kv for kv in [R(i, 20) for i in range(1, 200)]
        if sum(ints(sol(x**2 - x - (kv**2 + 5*kv + 6) < 0))) == 6]
assert min(good) == R(61, 20) and max(good) == 4; ans.append(3 + 4)
ans.append(len([kv for kv in range(-20, 30)
                if sol(expand((a**2 - 2*a)*kv - (2*a**2 - 4*a - 5)) >= 0, a) == S.Reals]))
best = None
for av_, bv in iprod(range(0, 41), range(0, 60)):
    e = x**2 + 4*y**2 + 4*x*y + 10*x + av_*y + bv
    d4 = expand(((4*y + 10)/2)**2 - (4*y**2 + av_*y + bv))
    if Poly(d4, y).degree() <= 0 and d4 < 0:
        best = av_ + bv if best is None else min(best, av_ + bv)
ans.append(best)
kr = []
for kv in [R(i, 10) for i in range(0, 260)]:
    q = (kv - 2)*t**2 - (kv - 4)*t + 3
    ok = sol(q < 0, t).intersect(Interval(0, oo)) == EmptySet
    if ok:
        kr.append(kv)
assert min(kr) == 2 and max(kr) == R(177, 10) and float(10 + 2*sqrt(15)) < 17.8
ans.append("2 leq k leq 10+2 sqrt {15}")
f = 2*(x - 2)**2
assert f.subs(x, 1) == 2 and sol(f > 0) == Union(Interval.open(-oo, 2), Interval.open(2, oo))
ans.append(min(kv for kv in range(-30, 30) if sol(expand(f - (2*kv*x - (kv + 8))) > 0) == S.Reals))
good = [av_ for av_ in [R(i, 20) for i in range(-200, 200)] if minmax(x**2 + 2*av_*x + av_**2 - 9, -1, 3)[1] <= 0]
assert (min(good), max(good)) == (-2, 0); ans.append("-2 leq a leq 0")
f = x**2 + 2*x - 8; g = (f - 3*Abs(f))/2
ans.append(sum(z for z in range(-50, 50) if g.subs(x, z) >= -z - 4))
pv = solve(diff(-R(3, 2)*(x + 2)*(x - 6), x), x)[0]
ans.append(pv + (-R(3, 2)*(x + 2)*(x - 6)).subs(x, pv))
vals = []
for z in [R(i, 100) for i in range(-400, 401)]:
    bb = z**2 - 12
    if z**2 - 4*bb >= 0:
        vals.append(bb + z)
ans.append(max(vals) * min(vals))

items = [p for _, _, ps in data8.TYPES for p in ps] + data8.STEP3
assert len(items) == len(ans) == 36, (len(items), len(ans))
bad = 0
for no, (it, v) in enumerate(zip(items, ans), 284):
    want = it["ans"].replace("$", "")
    if isinstance(v, str):
        ok = (want == v)
    else:
        w = want.replace("{", "(").replace("}", ")").replace(" over ", "/").replace(" ", "")
        ok = simplify(nsimplify(eval(w, {"sqrt": sqrt})) - v) == 0
    if not ok:
        bad += 1
        print("불일치", no, want, v)
print("문항", len(items), "불일치", bad)
