# -*- coding: utf-8 -*-
"""공통수학2 기본서 2단원 직선의 방정식 검산: 문항마다 답을 따로 계산해 data02.py의 답과 맞춘다.
python verify02.py
- 좌표 문제는 sympy로 직접 풀고, 범위·최댓값·최솟값·개수는 촘촘한 수치 탐색으로도 다시 확인한다.
"""
import sys, os, re
import math as _m
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sympy import *
import data02

x, y, t, a, b, c, k, m, p, q, r = symbols("x y t a b c k m p q r", real=True)


def dist(P, Q):
    return sqrt((P[0] - Q[0]) ** 2 + (P[1] - Q[1]) ** 2)


def inner(P, Q, mm, nn):
    return ((mm * Q[0] + nn * P[0]) / (mm + nn), (mm * Q[1] + nn * P[1]) / (mm + nn))


def line_through(P, Q):
    """ax+by+c=0 계수"""
    return (Q[1] - P[1], P[0] - Q[0], Q[0] * P[1] - P[0] * Q[1])


def pdist(P, L):
    return Abs(L[0] * P[0] + L[1] * P[1] + L[2]) / sqrt(L[0] ** 2 + L[1] ** 2)


def meet(L1, L2):
    s = solve([L1[0] * x + L1[1] * y + L1[2], L2[0] * x + L2[1] * y + L2[2]], [x, y], dict=True)
    return (s[0][x], s[0][y])


def area(*Ps):
    s = 0
    for i in range(len(Ps)):
        s += Ps[i][0] * Ps[(i + 1) % len(Ps)][1] - Ps[(i + 1) % len(Ps)][0] * Ps[i][1]
    return Abs(s) / 2


def clip_area(poly, a_, b_, c_):
    """다각형 중 a x + b y + c <= 0 인 부분의 넓이(수치)"""
    out = []
    n = len(poly)
    f = lambda P: a_ * P[0] + b_ * P[1] + c_
    for i in range(n):
        P, Q = poly[i], poly[(i + 1) % n]
        fp, fq = f(P), f(Q)
        if fp <= 0:
            out.append(P)
        if fp * fq < 0:
            s = fp / (fp - fq)
            out.append((P[0] + s * (Q[0] - P[0]), P[1] + s * (Q[1] - P[1])))
    if len(out) < 3:
        return 0.0
    s = 0.0
    for i in range(len(out)):
        s += out[i][0] * out[(i + 1) % len(out)][1] - out[(i + 1) % len(out)][0] * out[i][1]
    return abs(s) / 2


R = {}

# ================================================================ 유형 01 넓이를 이등분하는 직선
# m17: O, A(4,0), B(3,4), 직선 y=x+k가 넓이 이등분
# y=x+k (-4<k<0)는 OA와 (-k, 0), AB(4x+y=16)와 ((16-k)/5, (16+4k)/5)에서 만난다 → 점 A 쪽 삼각형 넓이 4
sol = [v for v in solve(Eq((4 + k) * (16 + 4 * k) / 5 / 2, 4), k) if -4 < v < 0]
assert len(sol) == 1
kk = sol[0]
assert abs(clip_area([(0, 0), (4, 0), (3, 4)], 1, -1, float(kk)) - 4) < 1e-9     # x - y + k <= 0 쪽(위)
R["m17"] = kk

# o36: A(-3,0), B(12,0), C(0,6), x+y+3+k(x-2y+3)=0 이 넓이를 삼등분하는 직선 중 하나
A, B, C = (-3, 0), (12, 0), (0, 6)
tot = float(area(A, B, C))
ks = []
for v in solve(Eq((1 + k) * x + (1 - 2 * k) * y + 3 + 3 * k, 0).subs({x: 8, y: 2}), k) + \
         solve(Eq((1 + k) * x + (1 - 2 * k) * y + 3 + 3 * k, 0).subs({x: 4, y: 4}), k):
    ks.append(v)
for v in ks:
    s = clip_area([A, B, C], float(1 + v), float(1 - 2 * v), float(3 + 3 * v))
    assert min(abs(s - tot / 3), abs(s - 2 * tot / 3)) < 1e-9
# 정점이 A이므로 다른 삼등분 직선은 없다(넓이 삼등분하는 직선은 BC의 삼등분점을 지남)
S36 = sum(ks)
assert S36 == Rational(64, 7)
R["o36"] = 64 + 7

# g079: 정사각형 OABC, A(-1,3), C 제1사분면 → O를 지나 넓이 3등분하는 두 직선의 기울기의 곱
A = (S(-1), S(3))
C = (S(3), S(1))
B = (A[0] + C[0], A[1] + C[1])
D = inner(A, B, 2, 1)
E = inner(B, C, 1, 2)
sq = [(0, 0), C, B, A]
for P_ in (D, E):
    s = clip_area(sq, float(P_[1]), float(-P_[0]), 0.0)
    assert min(abs(s - 10 / 3), abs(s - 20 / 3)) < 1e-9
R["g079"] = (D[1] / D[0]) * (E[1] / E[0])

# ================================================================ 유형 02 정점을 지나는 직선
# s04: 2x+y-4=0, mx-y+2m-1=0 이 제1사분면에서 만나는 m 범위 alpha<m<beta
X = solve([2 * x + y - 4, m * x - y + 2 * m - 1], [x, y], dict=True)[0]
rng = solve([X[x] > 0, X[y] > 0], m)
lo, hi = Rational(1, 4), Rational(5, 2)
assert rng.as_set() == Interval.open(lo, hi)
R["s04"] = lo + hi

# g076: 사각형 ABCD와 직선 mx-y-3m-1=0 이 만나는 m ≥ p 또는 m ≤ q
quad = [(-1, 5), (-3, 3), (2, 3), (4, 5)]


def hits(mv):
    vals = [mv * X_ - Y_ - 3 * mv - 1 for X_, Y_ in quad]
    return min(vals) <= 0 <= max(vals)


ok = [i / 100 for i in range(-3000, 3001) if hits(i / 100)]
assert all(hits(v) for v in (6, 7, 100, -Rational(2, 3), -1, -50)) and not hits(5.99) and not hits(-0.66)
assert not any(-0.66 < v < 6 for v in ok)
R["g076"] = 6 * Rational(-2, 3)

# o33: y=2x^2-12x+17 (1<=x<=4)와 (k+3)x-(2k+1)y-k+2=0 이 만나는 음의 정수 k의 최댓값
def meets(kv):
    for i in range(0, 30001):
        xv = 1 + 3 * i / 30000
        yv = 2 * xv * xv - 12 * xv + 17
        if i:
            if (f0 > 0) != ((kv + 3) * xv - (2 * kv + 1) * yv - kv + 2 > 0) or abs((kv + 3) * xv - (2 * kv + 1) * yv - kv + 2) < 1e-12:
                return True
        f0 = (kv + 3) * xv - (2 * kv + 1) * yv - kv + 2 > 0
    return False


neg = [kv for kv in range(-1, -40, -1) if meets(kv)]
R["o33"] = max(neg)

# ================================================================ 유형 03 두 직선의 평행
# k02: y=x/2+4 (A, B), y=ax-2a (C, D), 사각형 ADCB가 사다리꼴인 a의 합
A, B, C, D = (S(-8), S(0)), (S(0), S(4)), (S(2), S(0)), (S(0), -2 * a)
sl = lambda P, Q: (Q[1] - P[1]) / (Q[0] - P[0])
s1 = solve(Eq(sl(A, B), sl(D, C)), a)
s2 = solve(Eq(sl(A, D), sl(B, C)), a)
vals = [v for v in s1 + s2 if v > 0]
R["k02"] = sum(vals)

# k03: A(0,1), B(0,4), C(√2,p), D(3√2,q), CD 기울기 음수, AB=CD, AD∥BC
sols = solve([Eq((q - p) ** 2 + 8, 9), Eq((q - 1) / (3 * sqrt(2)), (p - 4) / sqrt(2))], [p, q], dict=True)
sols = [s for s in sols if s[q] - s[p] < 0]
assert len(sols) == 1
R["k03"] = sols[0][p] + sols[0][q]

# ================================================================ 유형 04 두 직선의 수직
# k04: 사다리꼴 ABCD, ∠A=∠B=90°, AB=4, BC=8, P는 AD를 2:1로 내분, AC⊥BP → 삼각형 AQD
B_, A_, C_ = (S(0), S(0)), (S(0), S(4)), (S(8), S(0))
D_ = (t, S(4))
P_ = inner(A_, D_, 2, 1)
tv = [v for v in solve(Eq(((C_[1] - A_[1]) / (C_[0] - A_[0])) * (P_[1] / P_[0]), -1), t) if v > 0][0]
Q_ = meet(line_through(A_, C_), line_through(B_, (P_[0].subs(t, tv), P_[1])))
R["k04"] = area(A_, Q_, (tv, 4))

# g088: (k^2+2k-3)x+(k+3)y=2, (k-4)x+(k-1)y=-1 수직
ks = [v for v in solve(Eq((k ** 2 + 2 * k - 3) * (k - 4) + (k + 3) * (k - 1), 0), k)]
ks = [v for v in ks if not (v ** 2 + 2 * v - 3 == 0 and v + 3 == 0)]   # 첫 식이 직선이 아닌 경우 제외
R["g088"] = sum(ks)

# g089: 마름모 ABCD, A(-2,1), B(p,4), C(q,8), D(1,r) (p,q,r>0)
sols = solve([Eq(-2 + q, p + 1), Eq(1 + 8, 4 + r), Eq((8 - 1) * (r - 4), -(q + 2) * (1 - p))], [p, q, r], dict=True)
sols = [s for s in sols if all(v > 0 for v in s.values())]
assert len(sols) == 1
s_ = sols[0]
Aa, Bb, Cc, Dd = (-2, 1), (s_[p], 4), (s_[q], 8), (1, s_[r])
assert dist(Aa, Bb) == dist(Bb, Cc) == dist(Cc, Dd) == dist(Dd, Aa)
R["g089"] = s_[p] * s_[q] * s_[r]

# ================================================================ 유형 05 세 직선의 위치 관계
# s05: y=x, y=2x-3, y=mx-2 가 삼각형을 이루지 않는 m의 곱
ms = [1, 2] + solve(Eq(3, 3 * m - 2), m)
R["s05"] = Mul(*ms)
# s06: x+2y-3=0, 3x-4y-12=0, ax+y+1=0 직각삼각형
P0 = meet((1, 2, -3), (3, -4, -12))
avs = []
for v in solve(Eq((-a) * Rational(-1, 2), -1), a) + solve(Eq((-a) * Rational(3, 4), -1), a):
    assert v * P0[0] + P0[1] + 1 != 0
    avs.append(v)
R["s06"] = sum(avs)

# o39: mx-6y+4m=0, y=-x+1, y=2x-2 로 둘러싸인 부분이 예각삼각형인 정수 m의 개수
def acute(mv):
    L = [(mv, -6, 4 * mv), (1, 1, -1), (2, -1, -2)]
    try:
        V = [meet(L[i], L[j]) for i, j in ((0, 1), (1, 2), (2, 0))]
    except Exception:
        return False
    if len(set(V)) < 3:
        return False
    for i in range(3):
        P0_, P1_, P2_ = V[i], V[(i + 1) % 3], V[(i + 2) % 3]
        d = (P1_[0] - P0_[0]) * (P2_[0] - P0_[0]) + (P1_[1] - P0_[1]) * (P2_[1] - P0_[1])
        if d <= 0:
            return False
    return True


R["o39"] = sum(1 for mv in range(-300, 301) if acute(mv))

# ================================================================ 유형 06 점과 직선 사이의 거리
# k05: A(a,6), 직선 l: (6,0),(0,3), 정사각형 ABCD 넓이 81/5 (B, C는 l 위, D는 제1사분면)
L = line_through((6, 0), (0, 3))
av = [v for v in solve(Eq(pdist((a, 6), L) ** 2, Rational(81, 5)), a) if v > 0]
assert len(av) == 1
R["k05"] = av[0]

# g108: A(1,-1), B(10,2), C(7,a), G(6,b) 무게중심, G와 AB 거리 √10, a>0
L = line_through((1, -1), (10, 2))
sols = solve([Eq((1 + 10 + 7) / 3, 6), Eq((-1 + 2 + a) / 3, b), Eq(pdist((6, b), L) ** 2, 10)], [a, b], dict=True)
sols = [s for s in sols if s[a] > 0]
assert len(sols) == 1
R["g108"] = sols[0][a] + sols[0][b]

# s07: A(t,1)을 지나고 원점에서 거리 t인 직선 l, m: x=t, x축으로 둘러싸인 넓이 6/5 (0<t<1)
kk = (1 - t ** 2) / (2 * t)
assert simplify(pdist((0, 0), (kk, -1, 1 - kk * t)) ** 2 - t ** 2).subs(t, Rational(1, 3)) == 0
x0 = t - 1 / kk                                                       # l의 x절편
f_ = Abs(t - x0) * 1 / 2
tv = [v for v in solve(Eq(simplify(1 / kk / 2), Rational(6, 5)), t) if 0 < v < 1]
assert len(tv) == 1 and simplify(f_.subs(t, tv[0]) - Rational(6, 5)) == 0
R["s07"] = tv[0]

# ================================================================ 유형 07 거리의 최대·최소
# g106: 원점과 k(x+y)-x+3y+4=0 사이 거리의 최댓값 b (k=a)
dk = 4 / sqrt((k - 1) ** 2 + (k + 3) ** 2)
best = max((float(dk.subs(k, i / 1000)), i / 1000) for i in range(-10000, 10001))
assert abs(best[1] + 1) < 1e-9 and abs(best[0] - 2 ** 0.5) < 1e-9
R["g106"] = (-1) ** 2 + 2

# s08: 마름모 A(-4,0), B(0,-3), C(4,0), D(0,3), P(5,3) → 최댓값 × 최솟값
quad = [(-4, 0), (0, -3), (4, 0), (0, 3)]
ds = []
for i in range(4):
    P0_, P1_ = quad[i], quad[(i + 1) % 4]
    for j in range(20001):
        s = j / 20000
        X_ = P0_[0] + s * (P1_[0] - P0_[0]); Y_ = P0_[1] + s * (P1_[1] - P0_[1])
        ds.append(_m.hypot(X_ - 5, Y_ - 3))
assert abs(max(ds) - 3 * 10 ** 0.5) < 1e-6 and abs(min(ds) - 3) < 1e-6
R["s08"] = 9 * sqrt(10)

# ================================================================ 유형 08 평행한 두 직선 사이의 거리
# k06: l1: x-2y-2=0, l2 ∥ l1 (y절편 양수), 사각형 ADCB 넓이 25 → d^2
cv = [v for v in solve(Eq((c + 2) ** 2 / 4, 25), c) if v > 0]
assert area((2, 0), (0, cv[0] / 2), (-cv[0], 0), (0, -1)) == 25
R["k06"] = ((cv[0] + 2) / sqrt(5)) ** 2

# o55: m>3, a>b, y=mx+a, y=mx+b 가 직사각형 O(0,0),A(3,0),B(3,6),C(0,6)의 넓이를 삼등분, 거리 2√6/5
rect = [(0, 0), (3, 0), (3, 6), (0, 6)]
mv = sqrt(24)
av, bv = 3 - mv, 3 - 2 * mv
for cc in (av, bv):
    s = clip_area(rect, float(mv), -1.0, float(cc))              # mx - y + c <= 0 : 직선 위쪽(왼쪽)
    assert min(abs(s - 6), abs(s - 12)) < 1e-9
assert simplify(Abs(av - bv) / sqrt(mv ** 2 + 1) - 2 * sqrt(6) / 5) == 0
# 거리 조건은 m에 대해 m/√(m²+1) = 2√6/5 하나뿐 (m>3)
assert [v for v in solve(Eq(m ** 2 / (m ** 2 + 1), Rational(24, 25)), m) if v > 3] == [mv]
R["o55"] = mv * (av - bv)

# ================================================================ 유형 09 각의 이등분선과 내심
# m22: x+2y+1=0, 2x-y-3=0 의 각의 이등분선
bis = [(1, -3, -4), (3, 1, -2)]
cands = {"ㄱ": (1, -3, -4), "ㄴ": (1, -2, -5), "ㄷ": (2, 1, 1), "ㄹ": (3, 1, -2)}
got = ""
for name, Lc in cands.items():
    # 직선 위의 두 점에서 두 직선까지 거리가 같은지
    pts = [(xv, Rational(-(Lc[0] * xv + Lc[2]), Lc[1])) for xv in (0, 7)]
    if all(pdist(P_, (1, 2, 1)) == pdist(P_, (2, -1, -3)) for P_ in pts):
        got += name
R["m22"] = got

# m15: y=0, x/6+y/8=1, -x/4+y/3=1 로 둘러싸인 삼각형의 내심
Ls = [(0, 1, 0), (4, 3, -24), (-3, 4, -12)]
V = [meet(Ls[0], Ls[1]), meet(Ls[1], Ls[2]), meet(Ls[2], Ls[0])]
sides = [dist(V[1], V[2]), dist(V[2], V[0]), dist(V[0], V[1])]
I = (sum(sides[i] * V[i][0] for i in range(3)) / sum(sides), sum(sides[i] * V[i][1] for i in range(3)) / sum(sides))
assert len({simplify(pdist(I, L_)) for L_ in Ls}) == 1
R["m15"] = simplify(I[0] + I[1])

# o43: y=x, y=7x 의 각의 이등분선 l(기울기 양수), m; x=1과의 교점 A, B → 삼각형 AOB 넓이
# |x-y|/√2 = |7x-y|/√50 → y=2x, y=-x/2
for sl_ in (2, Rational(-1, 2)):
    P_ = (1, sl_)
    assert pdist(P_, (1, -1, 0)) == pdist(P_, (7, -1, 0))
R["o43"] = area((0, 0), (1, 2), (1, Rational(-1, 2)))

# ================================================================ STEP 3
# a1620: 한 변 2인 정육각형 ABCDEF, A, B는 x축 위, C는 y축 위 → 직선 EF: y=ax+b, a^2+b^2
s3 = sqrt(3)
vals = set()
for sg in (1, -1):                       # 꼭짓점이 시계/반시계 방향
    for up in (1, -1):                   # x축 위쪽/아래쪽
        ang = [0, 60, 120, 180, 240, 300]
        P0 = [0, 0]
        V = [(0, 0)]
        for i in range(5):
            th = rad(sg * ang[i])
            P0 = [P0[0] + 2 * cos(th), P0[1] + up * 2 * sin(th)]
            V.append(tuple(P0))
        shift = -V[2][0]                 # C가 y축 위
        V = [(v[0] + shift, v[1]) for v in V]
        E_, F_ = V[4], V[5]
        av = (F_[1] - E_[1]) / (F_[0] - E_[0])
        bv = E_[1] - av * E_[0]
        vals.add(simplify(av ** 2 + bv ** 2))
assert len(vals) == 1
R["a1620"] = vals.pop()

# a1891: 정사각형 OABC, B(7,3) → 직선 AC의 x절편
Mx = (Rational(7, 2), Rational(3, 2))
A = (Mx[0] + Rational(3, 2), Mx[1] - Rational(7, 2))
C = (Mx[0] - Rational(3, 2), Mx[1] + Rational(7, 2))
assert dist((0, 0), A) == dist(A, (7, 3)) == dist((7, 3), C) == dist(C, (0, 0))
L = line_through(A, C)
R["a1891"] = -L[2] / L[0]

# k07: O, A(6,2), B(-2,4), P는 직선 OA 위(제1사분면), Q는 직선 OB 위(제2사분면)
# △OPB = ½△OAB, △OPQ = 3/2 △OPB → 직선 PQ: mx+ny=21
P_ = (3, 1)
Q_ = (-3, 6)
assert area((0, 0), P_, (-2, 4)) == area((0, 0), (6, 2), (-2, 4)) / 2
assert area((0, 0), P_, Q_) == Rational(3, 2) * area((0, 0), P_, (-2, 4))
L = line_through(P_, Q_)
sc = Rational(21, -L[2])
R["k07"] = L[0] * sc + L[1] * sc

# k08: (a,a)를 지나고 y=x^2-4x+10에 접하는 두 직선이 수직 → 기울기의 합
disc = expand((m + 4) ** 2 - 4 * (a * m - a + 10))            # x^2-(m+4)x+am-a+10=0
cf = Poly(disc, m).all_coeffs()
av = solve(Eq(cf[2] / cf[0], -1), a)[0]
R["k08"] = -cf[1].subs(a, av) / cf[0]

# k09: f(x)=k(x-2)(x-a), 꼭짓점 P, C(0,2ak), A, P에서 직선 BC에 내린 수선의 발 Q, R, APRQ 정사각형 → f(12)
kk = symbols("kk", positive=True)
fx = kk * (x - 2) * (x - a)
Pv = ((a + 2) / 2, fx.subs(x, (a + 2) / 2))
Cv = (0, fx.subs(x, 0))
Bv = (a, 0)
# AP ∥ BC, AP = (A와 직선 BC 사이 거리)
eq1 = Eq((Pv[1] - 0) / (Pv[0] - 2), (Cv[1] - 0) / (0 - a))
sola = [v for v in solve(eq1, a) if v.is_real is not False]
sola = [v for v in sola if (v - 2) != 0]
assert sola == [6]
Lbc = line_through(Bv, Cv)
eq2 = Eq(dist((2, 0), Pv).subs(a, 6) ** 2, (pdist((2, 0), Lbc) ** 2).subs(a, 6))
kv = solve(eq2, kk)
assert kv == [Rational(1, 2)]
R["k09"] = fx.subs({a: 6, kk: Rational(1, 2), x: 12})

# m14: A(0,4), B(20,0), C(a,b) 제1사분면, AC=BC, P, Q는 AC, BC를 1:4로 내분, CD는 ∠ACB의 이등분선,
#      선분 PQ 위의 점 D에 대하여 CD는 ∠ACB의 이등분선, E는 BC를 3:2로 내분, PE∩CD=F, DF=4√26/5 → a+b
A, B = (0, 4), (20, 0)
M_ = (10, 2)
# C는 AB의 수직이등분선 위: 기울기 5
s = symbols("s", positive=True)
C = (10 + s, 2 + 5 * s)
Pp = inner(A, C, 1, 4)
Ee = inner(B, C, 3, 2)
Qq = inner(B, C, 1, 4)
D_ = ((Pp[0] + Qq[0]) / 2, (Pp[1] + Qq[1]) / 2)           # CA=CB이므로 이등분선은 PQ의 중점을 지난다
F_ = meet(line_through(Pp, Ee), line_through(C, M_))
sv = [v for v in solve(Eq(dist(D_, F_) ** 2, Rational(16 * 26, 25)), s) if v > 0]
assert len(sv) == 1
R["m14"] = (C[0] + C[1]).subs(s, sv[0])

# m16: 한 변 6인 정사각형 ABCD, E, F는 AB, BC의 중점, G=AF∩DE, H는 G에서 BD에 내린 수선의 발 → GH
A, B, C, D = (0, 6), (0, 0), (6, 0), (6, 6)
E, F = (0, 3), (3, 0)
G = meet(line_through(A, F), line_through(D, E))
R["m16"] = pdist(G, line_through(B, D))

# m20: L(2,1), M(4,-1), N(a,b)는 AB, BC, CA의 중점, BN ⊥ LM, G와 직선 LM 거리 4√2, G 제1사분면 → ab
Lm, Mm, Nm = (2, 1), (4, -1), (a, b)
# A = L+N-M, B = L+M-N, C = M+N-L
Av = (Lm[0] + Nm[0] - Mm[0], Lm[1] + Nm[1] - Mm[1])
Bv = (Lm[0] + Mm[0] - Nm[0], Lm[1] + Mm[1] - Nm[1])
Cv = (Mm[0] + Nm[0] - Lm[0], Mm[1] + Nm[1] - Lm[1])
G = ((Av[0] + Bv[0] + Cv[0]) / 3, (Av[1] + Bv[1] + Cv[1]) / 3)
eqs = [Eq((Nm[1] - Bv[1]) * (Mm[1] - Lm[1]) + (Nm[0] - Bv[0]) * (Mm[0] - Lm[0]), 0),
       Eq(pdist(G, line_through(Lm, Mm)) ** 2, 32)]
sols = solve(eqs, [a, b], dict=True)
sols = [s_ for s_ in sols if G[0].subs(s_) > 0 and G[1].subs(s_) > 0]
assert len(sols) == 1
R["m20"] = sols[0][a] * sols[0][b]

# g100: kx-y=0, x+ky=0 (k<0)이 x+2y-10=0과 만나는 점 A, B, ∠AOB 이등분선이 AB를 수직이등분 → k+S
kv = symbols("kv", negative=True)
Av = meet((kv, -1, 0), (1, 2, -10))
Bv = meet((1, kv, 0), (1, 2, -10))
sol = [v for v in solve(Eq(dist((0, 0), Av) ** 2, dist((0, 0), Bv) ** 2), kv) if v < 0]
# OA=OB(이등변)이면 이등분선이 AB를 수직이등분한다
assert len(sol) == 1
R["g100"] = sol[0] + area((0, 0), tuple(v.subs(kv, sol[0]) for v in Av), tuple(v.subs(kv, sol[0]) for v in Bv))

# g119: 기울기 음수, (1,2)를 지나는 l1의 삼각형 OAB 넓이 4, l1에 수직이고 넓이 이등분하는 l2의 y절편
mv = [v for v in solve(Eq((1 - 2 / m) * (2 - m) / 2, 4), m) if v < 0]
assert mv == [-2]
tri = [(0, 0), (2, 0), (0, 4)]
# l2: y = x/2 + h  →  x/2 - y + h = 0
h = symbols("h")
hv = [v for v in solve(Eq(((4 - h) ** 2) / 5, 2), h) if 0 < v < 4]
assert len(hv) == 1 and abs(clip_area(tri, 0.5, -1.0, float(hv[0])) - 2) < 1e-9
R["g119"] = hv[0]

# k01은 1단원. 2단원 STEP 3에 넣은 a1891도 위에서 확인.

# ================================================================ 모의고사 변형(기본서에 넣는 것, 원문은 유형서로)
# k02v: y=x/3+2 (A, B), y=ax-3a (C, D), 사각형 ADCB가 사다리꼴인 a의 합
A, B, C, D = (S(-6), S(0)), (S(0), S(2)), (S(3), S(0)), (S(0), -3 * a)
vals = [v for v in solve(Eq(sl(A, B), sl(D, C)), a) + solve(Eq(sl(A, D), sl(B, C)), a) if v > 0]
assert len(vals) == 2
R["k02v"] = sum(vals)

# k03v: A(0,1), B(0,6), C(2,p), D(6,q), CD 기울기 음수, AB=CD, AD∥BC
sols = solve([Eq((q - p) ** 2 + 16, 25), Eq((q - 1) / 6, (p - 6) / 2)], [p, q], dict=True)
sols = [s_ for s_ in sols if s_[q] - s_[p] < 0]
assert len(sols) == 1
R["k03v"] = sols[0][p] + sols[0][q]

# k04v: 사다리꼴 ABCD, ∠A=∠B=90°, AB=3, BC=6, P는 AD를 3:1로 내분, AC⊥BP → 삼각형 AQD
A_, B_, C_ = (S(0), S(3)), (S(0), S(0)), (S(6), S(0))
P_ = inner(A_, (t, S(3)), 3, 1)
tv = [v for v in solve(Eq(sl(A_, C_) * (P_[1] / P_[0]), -1), t) if v > 0][0]
Q_ = meet(line_through(A_, C_), line_through(B_, (P_[0].subs(t, tv), P_[1])))
R["k04v"] = area(A_, Q_, (tv, 3))

# k05v: A(a,5) (a>0), 직선 l: (4,0),(0,2), 정사각형 ABCD 넓이 49/5 (B, C는 l 위, D는 제1사분면)
L = line_through((4, 0), (0, 2))
av = [v for v in solve(Eq(pdist((a, 5), L) ** 2, Rational(49, 5)), a) if v > 0]
assert len(av) == 1
# D가 제1사분면에 오도록 잡을 수 있는지 확인
Av = Matrix([av[0], 5]); n_ = Matrix([L[0], L[1]]) / sqrt(L[0] ** 2 + L[1] ** 2)
Bv = Av - n_ * (n_.dot(Av) + L[2] / sqrt(L[0] ** 2 + L[1] ** 2))
u_ = Matrix([-n_[1], n_[0]]) * sqrt(Rational(49, 5))
assert any((Av + sg * u_)[0] > 0 and (Av + sg * u_)[1] > 0 for sg in (1, -1))
R["k05v"] = av[0]

# k06v: l1: 2x-y-4=0, l2 ∥ l1 (y절편 양수), 사각형 ADCB 넓이 36 → d^2
cv = [v for v in solve(Eq((c + 4) ** 2 / 4, 36), c) if v > 0]
assert area((2, 0), (0, cv[0]), (-cv[0] / 2, 0), (0, -4)) == 36
R["k06v"] = (pdist((0, cv[0]), (2, -1, -4))) ** 2

# k07v: O, A(8,4), B(-3,6), △OPB = 1/4 △OAB, △OPQ = 2 △OPB → 직선 PQ: mx+ny=30
P_ = (S(2), S(1))
Q_ = (S(-6), S(12))
assert area((0, 0), P_, (-3, 6)) == area((0, 0), (8, 4), (-3, 6)) / 4
assert area((0, 0), P_, Q_) == 2 * area((0, 0), P_, (-3, 6))
L = line_through(P_, Q_)
sc = Rational(30, -L[2])
R["k07v"] = L[0] * sc + L[1] * sc

# k08v: (a,a)를 지나고 y=x^2-2x+5에 접하는 두 직선이 수직 → 기울기의 합
disc = expand((m + 2) ** 2 - 4 * (5 + a * m - a))
cf = Poly(disc, m).all_coeffs()
av = solve(Eq(cf[2] / cf[0], -1), a)[0]
assert av ** 2 - 2 * av + 5 > av            # 점이 포물선 아래쪽에 있어 접선이 두 개
R["k08v"] = -cf[1].subs(a, av) / cf[0]

# k09v: f(x)=k(x-1)(x-a) (k>0, a>1), APRQ 정사각형 → f(10)
fx = kk * (x - 1) * (x - a)
Pv = ((a + 1) / 2, fx.subs(x, (a + 1) / 2))
Cv = (0, fx.subs(x, 0))
Bv = (a, 0)
sola = [v for v in solve(Eq((Pv[1] - 0) / (Pv[0] - 1), (Cv[1] - 0) / (0 - a)), a) if v != 1]
assert sola == [3]
Lbc = line_through(Bv, Cv)
kv = solve(Eq((dist((1, 0), Pv) ** 2).subs(a, 3), (pdist((1, 0), Lbc) ** 2).subs(a, 3)), kk)
assert kv == [1]
R["k09v"] = fx.subs({a: 3, kk: 1, x: 10})

# ================================================================ 추가 5문항(2026-10-21)
# k10v: 2024년 9월 고1 20번 변형 — A(-6,a), B(5,6), C(-3,0), P는 AB를 3:1로 내분, 직선 PC가 △AOB 넓이 이등분
av_ = symbols("av_", positive=True)
A, B, C = (S(-6), av_), (S(5), S(6)), (S(-3), S(0))
P_ = inner(A, B, 3, 1)
Q_ = meet(line_through(C, P_), line_through((0, 0), A))
sarea = lambda P0, P1, P2: ((P1[0] - P0[0]) * (P2[1] - P0[1]) - (P2[0] - P0[0]) * (P1[1] - P0[1])) / 2
sol = [v for v in solve(Eq(sarea(A, Q_, P_) ** 2, (sarea((0, 0), A, B) / 2) ** 2), av_) if v > 0]
sol = [v for v in sol if simplify(Abs(sarea(A, Q_, P_)) - Abs(sarea((0, 0), A, B)) / 2).subs(av_, v) == 0
       and 0 < (Q_[1] / A[1]).subs(av_, v) < 1]
assert len(sol) == 1
# Q가 선분 AO 위, C는 삼각형 밖
Qv = tuple(v.subs(av_, sol[0]) for v in Q_)
assert -6 < Qv[0] < 0
R["k10v"] = sol[0]

# a1838: A(0,3)을 지나는 직선과 B(n,0)을 지나는 직선이 C에서 수직, 무게중심 G(13,4) → 자연수 n
nn = symbols("nn", positive=True)
Cv = (39 - nn, 12 - 3)
ns = [v for v in solve(Eq((Cv[1] - 3) * (Cv[1] - 0) + (Cv[0] - 0) * (Cv[0] - nn), 0), nn) if v.is_integer]
assert ns == [21]
R["a1838"] = ns[0]

# g107: 직선 l이 y=-x/2+3, y=-x/2-1과 각각 A, B에서 수직으로 만남, △OAB 넓이 2 → 직선 AB의 y절편의 곱
kvals = solve(Eq(Abs(k) * 4 / 5, 2), k)
for kv_ in kvals:
    A_ = meet((2, -1, kv_), (1, 2, -6)); B_ = meet((2, -1, kv_), (1, 2, 2))
    assert area((0, 0), A_, B_) == 2
R["g107"] = Mul(*kvals)

# o40: O(0,0), A(2,-1), 제1사분면의 B, 삼각형 OAB의 내심=외심(정삼각형) → 직선 OB의 기울기
sols = solve([Eq(x ** 2 + y ** 2, 5), Eq((x - 2) ** 2 + (y + 1) ** 2, 5)], [x, y], dict=True)
sols = [s_ for s_ in sols if s_[x] > 0 and s_[y] > 0]
assert len(sols) == 1
R["o40"] = radsimp(sols[0][y] / sols[0][x])

# m21: A(0,a), B(3,0), AC=BC인 직각이등변삼각형 ABC, -1<=a<=2 → OC의 최댓값/최솟값
vals = []
for i in range(0, 30001):
    av2 = -1 + 3 * i / 30000
    Nx, Ny = 1.5, av2 / 2
    for sg in (1, -1):
        Cx, Cy = Nx + sg * av2 / 2, Ny + sg * 1.5
        # 확인: CA=CB, CA ⊥ CB
        assert abs((Cx) ** 2 + (Cy - av2) ** 2 - (Cx - 3) ** 2 - Cy ** 2) < 1e-9
        assert abs((0 - Cx) * (3 - Cx) + (av2 - Cy) * (0 - Cy)) < 1e-9
        vals.append(_m.hypot(Cx, Cy))
assert abs(max(vals) / min(vals) - 5) < 1e-9
R["m21"] = 5

# ---------------------------------------------------------------- data02의 답과 맞추기
import re          # sympy의 re를 덮는다


def to_expr(s):
    s = s.replace("LEFT (", "(").replace("RIGHT )", ")").replace("~", "").replace("it-", "-")
    s = re.sub(r"sqrt\s*\{([^{}]*)\}", r"sqrt(\1)", s)
    s = re.sub(r"\{([^{}]*)\}\s*over\s*\{([^{}]*)\}", r"((\1)/(\2))", s)
    s = re.sub(r"(\d)\s*sqrt", r"\1*sqrt", s).replace(" ", "")
    return s


items = [it for _, _, ps in data02.TYPES for it in ps] + data02.STEP3
bad = 0
for it in items:
    got, ans = R[it["src"]], it["ans"]
    if isinstance(got, str):
        same = got == ans.replace(", ", "").replace(" ", "")
    else:
        same = simplify(sympify(to_expr(ans)) - got) == 0
    if not same:
        bad += 1
    print(("OK  " if same else "BAD ") + it["src"], ans, "|", got)
print("문항", len(items), "불일치", bad)
