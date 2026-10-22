# -*- coding: utf-8 -*-
"""공통수학2 기본서 3단원 원의 방정식 검산: 문항마다 답을 따로 계산해 data03.py의 답과 맞춘다.
python verify03.py
- 좌표 문제는 sympy로 풀고, 개수·최대·최소·범위는 촘촘한 수치 탐색으로도 다시 확인한다.
"""
import sys, os, re
import math as _m
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sympy import *
import data03

x, y, t, a, b, c, k, m, n, r, h, s = symbols("x y t a b c k m n r h s", real=True)
R = {}


def dist(P, Q):
    return sqrt((P[0] - Q[0]) ** 2 + (P[1] - Q[1]) ** 2)


def pdist(P, L):
    return Abs(L[0] * P[0] + L[1] * P[1] + L[2]) / sqrt(L[0] ** 2 + L[1] ** 2)


def ndist_line(P, L):
    return abs(L[0] * P[0] + L[1] * P[1] + L[2]) / _m.hypot(L[0], L[1])


# ================================================================ 유형 01 원의 방정식
# s09: y=x^2과 y=2mx-n의 교점 A, B를 지름으로 하는 원의 넓이 34π, m, n은 0이 아닌 정수, m≠n → 중심 좌표의 합
res = set()
for mv in range(-20, 21):
    for nv in range(-200, 201):
        if mv == 0 or nv == 0 or mv == nv or mv * mv - nv <= 0:
            continue
        if (mv * mv - nv) * (1 + 4 * mv * mv) == 34:          # (AB/2)^2 = (m^2-n)(1+4m^2) = 34
            res.add(mv + 2 * mv * mv - nv)
assert res == {4}
# 직접 확인: m=-2, n=2
xs = solve(x ** 2 + 4 * x + 2, x)
A_, B_ = [(xv, xv ** 2) for xv in xs]
assert simplify(dist(A_, B_) ** 2 / 4 - 34) == 0
R["s09"] = 4

# k11v: A(1,-7), 무게중심 (1,1), 외심 원점 → 넓이 (q/p)√39, p+q
A_ = (1, -7)
M_ = (Rational(3 * 1 - 1, 2), Rational(3 * 1 + 7, 2))                  # A + 2M = 3G
Rr = 50
L = (M_[0], M_[1], -(M_[0] ** 2 + M_[1] ** 2))                       # OM ⊥ BC, BC는 M을 지남
sol = solve([x ** 2 + y ** 2 - Rr, L[0] * x + L[1] * y + L[2]], [x, y], dict=True)
Bv, Cv = (sol[0][x], sol[0][y]), (sol[1][x], sol[1][y])
G = ((A_[0] + Bv[0] + Cv[0]) / 3, (A_[1] + Bv[1] + Cv[1]) / 3)
assert simplify(G[0] - 1) == 0 and simplify(G[1] - 1) == 0
Sarea = Abs((Bv[0] - A_[0]) * (Cv[1] - A_[1]) - (Cv[0] - A_[0]) * (Bv[1] - A_[1])) / 2
Sarea = simplify(Sarea)
assert simplify(Sarea - Rational(120, 13) * sqrt(39)) == 0
R["k11v"] = 13 + 120

# ================================================================ 유형 02 좌표축에 접하는 원
# g151: 중심이 y=x^2-x-3 위, 두 축에 동시에 접하는 모든 원의 넓이의 합
areas = 0
for sg in (1, -1):
    for av in solve(Eq(sg * a, a ** 2 - a - 3), a):
        assert av != 0
        areas += av ** 2
R["g151"] = simplify(areas) * pi

# b092: (2x-y+3)+k(x-2y)=0 중 원점에서 거리 최대인 직선 l, 중심이 l 위이고 두 축에 접하는 원의 반지름의 합
P0 = solve([2 * x - y + 3, x - 2 * y], [x, y])
P0 = (P0[x], P0[y])
# 거리 최대: l ⊥ OP0, P0를 지남 → l: P0x*x + P0y*y - (P0x^2+P0y^2) = 0
Ll = (P0[0], P0[1], -(P0[0] ** 2 + P0[1] ** 2))
# 이 직선이 실제로 주어진 꼴로 나타나는지(k 존재)
kk_ = solve([Eq((2 + k) * Ll[1], (-1 - 2 * k) * Ll[0])], k)
assert kk_
best = max((float(pdist((0, 0), (2 + kv, -1 - 2 * kv, 3))), kv) for kv in [i / 100 for i in range(-3000, 3001)])
assert abs(best[0] - float(sqrt(P0[0] ** 2 + P0[1] ** 2))) < 1e-3
rs = []
for sg in (1, -1):
    for av in solve(Eq(Ll[0] * a + Ll[1] * sg * a + Ll[2], 0), a):
        rs.append(Abs(av))
R["b092"] = sum(rs)

# s10: f(x)=ax^2+b, 중심이 그래프 위, y=3x/4와 x축에 동시에 접하는 원이 오직 1개, 넓이 π → a/b
found = set()
for av in (Rational(9, 2), Rational(-9, 2)):
    bv = Rational(9, 4) / av
    cnt = []
    for sl in (Rational(1, 3), -3):                                     # 각의 이등분선 y=x/3, y=-3x
        roots = [rv for rv in solve(av * x ** 2 + bv - sl * x, x) if rv.is_real]
        for rv in roots:
            cy = sl * rv
            if cy != 0:
                cnt.append((rv, cy))
    assert len(set(cnt)) == 1 and Abs(cnt[0][1]) == 1
    found.add(av / bv)
assert found == {9}
R["s10"] = 9

# ================================================================ 유형 03 점이 나타내는 도형
# g160: A(0,0), B(8,0), AP = 3BP → 삼각형 ABP 넓이 최대
circ = expand(x ** 2 + y ** 2 - 9 * ((x - 8) ** 2 + y ** 2))
cx = solve(diff(circ, x), x)[0]
rad2 = simplify(-(circ.subs({x: cx, y: 0})) / (-8))
assert cx == 9 and rad2 == 9
R["g160"] = Rational(1, 2) * 8 * 3

# b031: A(1,1), B(-2,-2), ∠ACB의 이등분선이 원점을 지남 → C와 직선 AB 거리 최대
# 원점은 선분 AB 위 → CA:CB = OA:OB = 1:2
best = 0
for i in range(0, 72000):
    th = 2 * _m.pi * i / 72000
    Cx, Cy = 2 + 2 * _m.sqrt(2) * _m.cos(th), 2 + 2 * _m.sqrt(2) * _m.sin(th)
    if abs(Cx - Cy) < 1e-9:
        continue
    ca, cb = _m.hypot(Cx - 1, Cy - 1), _m.hypot(Cx + 2, Cy + 2)
    assert abs(cb - 2 * ca) < 1e-9
    best = max(best, abs(Cx - Cy) / _m.sqrt(2))
assert abs(best - 2 * _m.sqrt(2)) < 1e-6
R["b031"] = 2 * sqrt(2)

# o20: x^2+y^2=4 밖의 점 P, ∠APB=60° → OP=4 → 둘레 8π
R["o20"] = 2 * pi * 4

# ================================================================ 유형 04 두 원의 교점
# g193: (x+1)^2+(y-2)^2=10, (x-2)^2+(y+1)^2=k, AB=2√2 → 모든 양수 k의 합
ks = []
for kv in range(1, 200):
    o1, o2 = (-1, 2), (2, -1)
    d_ = _m.hypot(3, 3)
    r1, r2 = _m.sqrt(10), _m.sqrt(kv)
    if abs(r1 - r2) < d_ < r1 + r2:
        aa = (r1 ** 2 - r2 ** 2 + d_ ** 2) / (2 * d_)
        hh = _m.sqrt(r1 ** 2 - aa ** 2)
        if abs(2 * hh - 2 * _m.sqrt(2)) < 1e-9:
            ks.append(kv)
assert ks == [4, 52]
R["g193"] = sum(ks)

# b077: x^2+y^2-2x-2y-7=0이 x^2+y^2-6x-2ay+a^2+8=0의 둘레를 이등분 → a의 곱
avs = solve(Eq(4 * 3 + (2 * a - 2) * a - a ** 2 - 15, 0), a)
for av in avs:
    d_ = sqrt((3 - 1) ** 2 + (av - 1) ** 2)
    assert 3 - 1 < d_ < 3 + 1                                           # 두 원이 두 점에서 만남
R["b077"] = Mul(*avs)

# o24: x^2+y^2=m, (x-3)^2+(y-3)^2=n, AB=2√n, m+n=30 → 둘레의 합
mv_, nv_ = symbols("mv_ nv_", positive=True)
sol = solve([Eq(36 - 18 - mv_ + nv_, 0), Eq(mv_ + nv_, 30)], [mv_, nv_], dict=True)[0]
R["o24"] = simplify(2 * pi * (sqrt(sol[mv_]) + sqrt(sol[nv_])))

# ================================================================ 유형 05 원 위의 점까지의 거리
# g157: (4,0),(10,0)을 지나고 반지름 5, 중심 제1사분면 → OP 정수인 P 개수
Cc = (7, 4)
cnt = 0
for kv in range(0, 30):
    d_ = _m.hypot(7, 4)
    if d_ - 5 < kv < d_ + 5:
        cnt += 2
    elif abs(kv - (d_ - 5)) < 1e-12 or abs(kv - (d_ + 5)) < 1e-12:
        cnt += 1
R["g157"] = cnt

# s11: l1, l2 수직 교점 P(지름 AB 원 위), Q는 (x-8)^2+(y-2)^2=4 위 → PQ 최댓값
best = 0
for mi in range(-4000, 4001):
    mv = mi / 100
    Psol = solve([mv * (x - 1) - (y - 1), (x - 7) + mv * (y - 9)], [x, y]) if mi % 400 == 0 else None
    if Psol:
        Px, Py = float(Psol[x]), float(Psol[y])
        best = max(best, _m.hypot(Px - 8, Py - 2) + 2)
assert best <= 12 + 1e-9
# 최댓값 12는 P(0,8)에서: m=-7
Ps = solve([-7 * (x - 1) - (y - 1), (x - 7) - 7 * (y - 9)], [x, y])
assert Ps == {x: 0, y: 8}
R["s11"] = dist((0, 8), (8, 2)) + 2

# o29: x^2+(y-4)^2=7/4 위 P(a,b), y=x^2/2 위 제1사분면 Q(c,d), PQ 최소 → ac+bd
best = min(((cv * cv + (cv * cv / 2 - 4) ** 2), cv) for cv in [i / 10000 for i in range(1, 60000)])
cq = sqrt(6)
assert abs(best[1] - float(cq)) < 1e-3
Q_ = (cq, 3)
dq = dist((0, 4), Q_)
P_ = (0 + (cq - 0) * sqrt(Rational(7, 4)) / dq, 4 + (3 - 4) * sqrt(Rational(7, 4)) / dq)
R["o29"] = simplify(P_[0] * Q_[0] + P_[1] * Q_[1])

# ================================================================ 유형 06 원과 직선의 위치 관계
# g179: x^2+y^2-4x-12y+20=0과 y=k|x|가 서로 다른 두 점에서만 → a<k<b, ab
def count_g179(kv):
    pts = set()
    for sg in (1, -1):                       # x>=0: y=kx, x<=0: y=-kx
        for xv in solve(x ** 2 + (sg * kv * x) ** 2 - 4 * x - 12 * sg * kv * x + 20, x):
            if xv.is_real and (sg * xv >= 0):
                pts.add((round(float(xv), 9), round(float(sg * kv * xv), 9)))
    return len(pts)
ok = [kv for kv in [Rational(i, 20) for i in range(-60, 121)] if count_g179(kv) == 2]
assert min(ok) > Rational(1, 2) and max(ok) < 2 and Rational(11, 20) in ok and Rational(39, 20) in ok
assert count_g179(Rational(1, 2)) != 2 and count_g179(2) != 2
R["g179"] = Rational(1, 2) * 2

# o25: 중심 A(3,4), xy=0과 만나는 점의 개수가 홀수 → 반지름의 합
def count_axes(rv):
    pts = set()
    for xv in solve((x - 3) ** 2 + 16 - rv ** 2, x):
        if xv.is_real:
            pts.add((float(xv), 0.0))
    for yv in solve(9 + (y - 4) ** 2 - rv ** 2, y):
        if yv.is_real:
            pts.add((0.0, float(yv)))
    return len(pts)
odd = [rv for rv in [Rational(i, 10) for i in range(1, 120)] if count_axes(rv) % 2 == 1]
assert odd == [3, 4, 5]
R["o25"] = sum(odd)

# s12: A(k,3k), B(2k,4k), x^2+y^2=2 위의 P 중 AP=BP인 P가 하나 → k의 곱
kv_ = solve(Eq(Abs(5 * k) / sqrt(2), sqrt(2)), k)
R["s12"] = Mul(*kv_)

# k12v: A(0,3), B(4,3), C(t,0), D(0,t), 선분 CD 위에 ∠APB=90°인 P → t의 최댓값-최솟값
def exists(tv):
    for i in range(0, 4001):
        u = i / 4000
        Px, Py = tv * (1 - u), tv * u
        if abs((Px - 2) ** 2 + (Py - 3) ** 2 - 4) < 1e-3 * tv and (abs(Px) + abs(Py - 3) > 1e-6) and (abs(Px - 4) + abs(Py - 3) > 1e-6):
            return True
    return False
ts = [tv for tv in [i / 100 for i in range(100, 1000)] if exists(tv)]
assert abs(min(ts) - (5 - 2 * _m.sqrt(2))) < 0.02 and abs(max(ts) - (5 + 2 * _m.sqrt(2))) < 0.02
R["k12v"] = 4 * sqrt(2)

# ================================================================ 유형 07 현의 길이
# g170: (x+2)^2+(y+3)^2=25, y=kx와 교점 P,Q, PQ 최소일 때 삼각형 APQ 둘레
d_ = sqrt(13)
R["g170"] = 10 + 2 * sqrt(25 - d_ ** 2)

# o37: 원 C가 y=0, 3x-4y=0과 만나 생기는 현의 길이 모두 2, A(4,1) 위 → 넓이 합 q/p π
tot = 0
for sl in (Rational(1, 3), -3):
    for hv in solve(Eq((4 - h) ** 2 + (1 - sl * h) ** 2, (sl * h) ** 2 + 1), h):
        if hv.is_real:
            kc = sl * hv
            rr = kc ** 2 + 1
            assert simplify(pdist((hv, kc), (3, -4, 0)) ** 2 - (rr - 1)) == 0
            tot += rr
assert tot == Rational(550, 81)
R["o37"] = 81 + 550

# m33: x^2+(y-1)^2=1과 y=mx-m+1, S1=S2 → m의 합
Qs = solve([x ** 2 + (y - 1) ** 2 - 1, y + x - 1], [x, y], dict=True)
ms = []
for q_ in Qs:
    if q_[x] == 0:
        continue
    ms.append(simplify((q_[y] - 1) / (q_[x] - 1)))
R["m33"] = simplify(sum(ms))

# ================================================================ 유형 08 원 위의 점과 직선 사이의 거리
# s13: (x+2)^2+(y+1)^2=2, A(-1,5), B(3,1), 넓이 최소인 P의 x좌표
best = min((ndist_line((-2 + _m.sqrt(2) * _m.cos(2 * _m.pi * i / 36000), -1 + _m.sqrt(2) * _m.sin(2 * _m.pi * i / 36000)), (1, 1, -4)), i) for i in range(36000))
th = 2 * _m.pi * best[1] / 36000
assert abs(-2 + _m.sqrt(2) * _m.cos(th) + 1) < 1e-3
R["s13"] = -1

# s14: x^2+y^2=2 위 A, y=x+4 위 B, C, 정삼각형 ABC 넓이 최대 M, 최소 m → Mm
d_ = pdist((0, 0), (1, -1, 4))
hmin, hmax = d_ - sqrt(2), d_ + sqrt(2)
area_ = lambda hh: hh ** 2 / sqrt(3)
R["s14"] = simplify(area_(hmax) * area_(hmin))

# m32: A(17,0), B(5,12), C(5,5), 중심 C 반지름 r인 원이 삼각형 OAB와 세 점에서만 → r의 곱
def seg_pts(P, Q, rv):
    out = []
    dx, dy = Q[0] - P[0], Q[1] - P[1]
    fx, fy = P[0] - 5, P[1] - 5
    A2, B2, C2 = dx * dx + dy * dy, 2 * (fx * dx + fy * dy), fx * fx + fy * fy - rv * rv
    D = B2 * B2 - 4 * A2 * C2
    if D < -1e-9:
        return out
    D = max(D, 0)
    for sg in (1, -1):
        u = (-B2 + sg * _m.sqrt(D)) / (2 * A2)
        if -1e-9 <= u <= 1 + 1e-9:
            out.append((round(P[0] + u * dx, 6), round(P[1] + u * dy, 6)))
    return out
def count_tri(rv):
    pts = set()
    for P, Q in (((0, 0), (17, 0)), ((17, 0), (5, 12)), ((5, 12), (0, 0))):
        pts.update(seg_pts(P, Q, rv))
    return len(pts)
cands = [35 / 13, 7 / _m.sqrt(2), 5, 7, 5 * _m.sqrt(2), 13]
hits = [rv for rv in cands if count_tri(rv) == 3]
# 구간 안쪽은 짝수 개
for lo, hi in zip([0] + cands, cands + [20]):
    mid = (lo + hi) / 2
    assert count_tri(mid) != 3
assert len(hits) == 2 and abs(hits[0] - 7 / _m.sqrt(2)) < 1e-9 and abs(hits[1] - 5 * _m.sqrt(2)) < 1e-9
R["m32"] = 35

# ================================================================ 유형 09 원의 접선
# k13v: A(0,4), B(8,0), P는 AB를 1:3 내분, x^2+y^2-2ax-2by=0이 직선 AB와 P에서만 → 16(a+b)
P_ = (2, 3)
sol = solve([Eq(b - 3, 2 * (a - 2)), Eq(a ** 2 + b ** 2, (a - 2) ** 2 + (b - 3) ** 2)], [a, b], dict=True)[0]
# 접하는지 확인
assert simplify(pdist((sol[a], sol[b]), (1, 2, -8)) - sqrt(sol[a] ** 2 + sol[b] ** 2)) == 0
R["k13v"] = 16 * (sol[a] + sol[b])

# k14v: y=x^2-4x+3 위 A, B, AB 지름 원 넓이 18π, A를 지나고 기울기 -1인 직선이 원에 접 → AB의 y절편
kv = solve(Eq(25 - 4 * (3 - k), 36), k)[0]
xs = solve(x ** 2 - 5 * x + 3 - kv, x)
Pts = [(xv, xv + kv) for xv in xs]
assert simplify(dist(*Pts) - 6 * sqrt(2)) == 0
for xv in xs:
    assert simplify(xv ** 2 - 4 * xv + 3 - (xv + kv)) == 0
R["k14v"] = kv

# g167: y=-x^2/2와 x^2+(y-2)^2=4에 동시에 접하는 직선(기울기≠0)의 기울기의 곱
sols = solve([Eq(a ** 2, 2 * b), Eq((b - 2) ** 2, 4 * (a ** 2 + 1))], [a, b], dict=True)
slopes = [s_[a] for s_ in sols if s_[a] != 0]
R["g167"] = Mul(*slopes)

# ================================================================ 유형 10 원 밖의 점에서 그은 접선
# g163: (1,k)에서 (x-3)^2+(y+1)^2=9에 그은 두 접선 수직 → 양수 k
kv = [v for v in solve(Eq(4 + (k + 1) ** 2, 18), k) if v > 0][0]
R["g163"] = kv

# m28: P(p,q) 제1사분면, x^2+y^2=1 접선 l1, l2, 삼각형 PAB 넓이 2√2/3, 기울기 곱 1/2 → pq
dd = symbols("dd", positive=True)
d2 = [v for v in solve(Eq((dd ** 2 - 1) ** 3 / dd ** 4, Rational(8, 9)), dd) if v.is_real][0] ** 2
assert d2 == 3
p2 = solve(Eq((3 - x - 1) / (x - 1), Rational(1, 2)), x)[0]
R["m28"] = sqrt(p2 * (3 - p2))

# s15: y=-x-2 위 P에서 (x-1)^2+(y-1)^2=4에 그은 두 접선의 기울기 곱 3 → P의 x좌표 (>3)
tv = symbols("tv")
quad = expand((m - m * tv - tv - 3) ** 2 - 4 * (m ** 2 + 1))
cf = Poly(quad, m).all_coeffs()
tsol = [v for v in solve(Eq(cf[2] / cf[0], 3), tv) if v > 3]
R["s15"] = tsol[0]

# ================================================================ STEP 3
# k15v: x^2+y^2=9 위 A(a,b), B(-b,-a), AP=BP, AQ=BQ인 P, Q, 사각형 APBQ 넓이 6 → ab
# P, Q = 직선 y=-x와 원의 교점(지름 6), AB = 2 → 2(a+b)^2 = 4 → ab = ((a+b)^2-9)/2
R["k15v"] = (2 - 9) / S(2)
# 수치 확인
for i in range(1, 3600):
    th = 2 * _m.pi * i / 3600
    av, bv = 3 * _m.cos(th), 3 * _m.sin(th)
    if abs(2 * (av + bv) ** 2 - 4) < 1e-4:
        P1, P2 = (3 / _m.sqrt(2), -3 / _m.sqrt(2)), (-3 / _m.sqrt(2), 3 / _m.sqrt(2))
        A_, B_ = (av, bv), (-bv, -av)
        assert abs(_m.hypot(A_[0] - P1[0], A_[1] - P1[1]) - _m.hypot(B_[0] - P1[0], B_[1] - P1[1])) < 1e-6
        assert abs(av * bv + 3.5) < 1e-3

# k16v: y=x+4, y=-x+4에 모두 접하고 (2,0)을 지나는 두 원의 중심 사이 거리
cs = solve(Eq((4 - c) ** 2, 2 * (4 + c ** 2)), c)
hs = [v for v in solve(Eq((h - 2) ** 2 + 16, h ** 2 / 2), h) if v.is_real]
assert hs == []
R["k16v"] = simplify(Abs(cs[0] - cs[1]))

# k19v: y=x+2 위 P(0,2), Q(a,a+2), R(b,b+2) (0<a<b), 삼각형 OPR 넓이 4√2, C1:C2 넓이비 1:9 → a+b
bv = solve(Eq(Rational(1, 2) * sqrt(2) * b * sqrt(2), 4 * sqrt(2)), b)[0]                 # PR = √2 b, O와 직선 거리 √2
av = solve(Eq(sqrt(2) * a * 3, sqrt(2) * (bv - a)), a)[0]                                 # QR = 3 PQ
R["k19v"] = simplify(av + bv)

# k21v: x^2+y^2=65, A1(1,8), A2(4,7), B(-8,1), B를 지나고 A1B, A2B에 수직인 직선과 원의 교점 C1, C2
def other(Ai):
    slope = -(Ai[0] + 8) / S(Ai[1] - 1)
    sols = solve([x ** 2 + y ** 2 - 65, y - 1 - slope * (x + 8)], [x, y], dict=True)
    return [(s_[x], s_[y]) for s_ in sols if (s_[x], s_[y]) != (-8, 1)][0]
C1, C2 = other((1, 8)), other((4, 7))
R["k21v"] = C1[1] ** 2 + C2[0] ** 2

# k20v: C1 (x+4)^2+(y-1)^2=9, C2 (x-6)^2+(y-2)^2=4, l: y=x-1, 수선의 발 H1H2 최대 M, 최소 m → Mm
t1 = (-4 + 1) / sqrt(2)                       # 직선 l 방향 (1,1)/√2 위로의 사영
t2 = (6 + 2) / sqrt(2)
Mv, mv = (t2 - t1) + 3 + 2, (t2 - t1) - 3 - 2
assert mv > 0
R["k20v"] = simplify(Mv * mv)

# k17v: 반지름 2, x축과 y=mx에 접, 삼각형 ROP 넓이 54 → 60m
hv = [v for v in solve(Eq(h ** 3 / 4, 54), h) if v.is_real][0]
mvs = [v for v in solve(Eq((hv * m - 2) ** 2, 4 * (m ** 2 + 1)), m) if v > 0]
# R의 y좌표 확인: P(h,0), Q는 C(h,2)에서 y=mx에 내린 수선의 발
mq = mvs[0]
Qx = (hv + 2 * mq) / (1 + mq ** 2)
Q_ = (Qx, mq * Qx)
Ry = (Q_[1] - 0) / (Q_[0] - hv) * (0 - hv)
assert simplify(Rational(1, 2) * hv * Ry - 54) == 0
R["k17v"] = 60 * mq

# m34: 3x+4y+5=0, 4x-3y+15=0에 접하고 (-1,-3)을 지나는 큰 원 → p+q+r
cands = []
for hv in solve(Eq((h + 1) ** 2 + (-7 * h - 20 + 3) ** 2, (5 * (h + 3)) ** 2), h):
    kv = -7 * hv - 20
    rv = Abs(5 * (hv + 3))
    assert simplify(pdist((hv, kv), (3, 4, 5)) - rv) == 0 and simplify(pdist((hv, kv), (4, -3, 15)) - rv) == 0
    cands.append((rv, hv, kv))
for hv in solve(Eq((h + 1) ** 2 + ((h + 10) / 7 + 3) ** 2, ((3 * h + 4 * (h + 10) / 7 + 5) / 5) ** 2), h):
    if hv.is_real:
        kv = (hv + 10) / 7
        rv = Abs(3 * hv + 4 * kv + 5) / 5
        cands.append((rv, hv, kv))
assert len(cands) == 2
rv, hv, kv = max(cands, key=lambda z: z[0])
R["m34"] = -2 * hv - 2 * kv + hv ** 2 + kv ** 2 - rv ** 2

# k18v: l1 3x+y+3=0, l2 x-3y-9=0, A, B, C, 제1사분면 P, 외접원 위 Q (무게중심), 넓이 3배 → P의 좌표 합
A_ = solve([3 * x + y + 3, x - 3 * y - 9], [x, y]); A_ = (A_[x], A_[y])
B_, C_ = (-1, 0), (9, 0)
Oc = solve([(x - A_[0]) ** 2 + (y - A_[1]) ** 2 - (x - B_[0]) ** 2 - (y - B_[1]) ** 2,
            (x - A_[0]) ** 2 + (y - A_[1]) ** 2 - (x - C_[0]) ** 2 - (y - C_[1]) ** 2], [x, y])
rr = (Oc[x] - B_[0]) ** 2 + (Oc[y] - B_[1]) ** 2
SABC = Rational(1, 2) * 10 * Abs(A_[1])
Py = 3 * SABC * 2 / 10
res = []
for qx in solve((x - Oc[x]) ** 2 + (Py / 3 - Oc[y]) ** 2 - rr, x):
    px = 3 * qx - 8
    if px > 0:
        res.append(px + Py)
assert len(res) == 1
R["k18v"] = res[0]

# m30: 원 (x-k+1)^2+(y-2k+1)^2=k^2/9 위 P, 3x-4y-1=0까지 PH 자연수인 P가 10개 → k의 합
def countP(kv):
    d_ = Rational(abs(3 * (kv - 1) - 4 * (2 * kv - 1) - 1), 5)
    rv = Rational(kv, 3)
    lo, hi = d_ - rv, d_ + rv
    tot = 0
    for nv in range(1, 200):
        if lo < nv < hi:
            tot += 2
        elif nv == lo or nv == hi:
            tot += 1
    return tot
ks = [kv for kv in range(1, 60) if countP(kv) == 10]
assert ks == [7, 8]
R["m30"] = sum(ks)

# o36: 중심이 y=x^2 위, y=x+3에 접, 반지름 같은 네 원, 중심의 x좌표 곱 5 → y좌표 합
sv = [v for v in solve(Eq(9 - s ** 2, 5), s) if v > 0][0]
roots = solve(x ** 2 - x - 3 - sv, x) + solve(x ** 2 - x - 3 + sv, x)
assert len(set(roots)) == 4 and all(rv.is_real for rv in roots)
assert simplify(Mul(*roots) - 5) == 0
R["o36"] = simplify(sum(rv ** 2 for rv in roots))

# m36: l: y=m(x-1) (m<0), x^2+y^2=r^2와 제2·4사분면 교점 A, B, P=l∩y축, Q: P를 지나 x축 평행, 제1사분면
#      ∠BAQ=45°, AP:BP=2:5 → r^2  (수치로 풀고 확인)
import itertools
def m36_err(mv, rv):
    sols_ = sorted([((-(-2 * mv * mv)) + sg * _m.sqrt((2 * mv * mv) ** 2 - 4 * (1 + mv * mv) * (mv * mv - rv * rv))) / (2 * (1 + mv * mv)) for sg in (1, -1)])
    xa, xb = sols_[0], sols_[1]
    A_, B_ = (xa, mv * (xa - 1)), (xb, mv * (xb - 1))
    P_ = (0, -mv)
    Q_ = (_m.sqrt(rv * rv - mv * mv), -mv)
    ap, bp = _m.hypot(A_[0] - P_[0], A_[1] - P_[1]), _m.hypot(B_[0] - P_[0], B_[1] - P_[1])
    v1, v2 = (B_[0] - A_[0], B_[1] - A_[1]), (Q_[0] - A_[0], Q_[1] - A_[1])
    ang = _m.degrees(_m.acos((v1[0] * v2[0] + v1[1] * v2[1]) / (_m.hypot(*v1) * _m.hypot(*v2))))
    return ap / bp - 2 / 5, ang - 45, A_, B_
# AP:BP=2:5에서 x좌표 비 |xa|:xb = 2:5
best = None
for i in range(1, 4000):
    mv = -i / 400
    # r을 AP:BP 조건으로 정한다: xa = -2u, xb = 5u, 근과 계수: xa+xb = 2m^2/(1+m^2), xa*xb = (m^2-r^2)/(1+m^2)
    u = 2 * mv * mv / (1 + mv * mv) / 3
    rr2 = mv * mv + 10 * u * u * (1 + mv * mv)
    e1, e2, A_, B_ = m36_err(mv, _m.sqrt(rr2))
    if best is None or abs(e2) < best[0]:
        best = (abs(e2), mv, rr2, A_, B_)
assert best[0] < 0.05 and abs(best[2] - 45) < 0.5
# 정확한 값: m=-3, r^2=45
e1, e2, A_, B_ = m36_err(-3, _m.sqrt(45))
assert abs(e1) < 1e-9 and abs(e2) < 1e-9 and A_[0] < 0 < A_[1] and B_[0] > 0 > B_[1]
R["m36"] = 45


# ---------------------------------------------------------------- data03의 답과 맞추기
import re          # sympy의 re를 덮는다


def to_expr(s_):
    s_ = s_.replace("LEFT (", "(").replace("RIGHT )", ")").replace("~", "").replace("it-", "-")
    s_ = re.sub(r"sqrt\s*\{([^{}]*)\}", r"sqrt(\1)", s_)
    s_ = re.sub(r"\{([^{}]*)\}\s*over\s*\{([^{}]*)\}", r"((\1)/(\2))", s_)
    s_ = re.sub(r"(\d)\s*sqrt", r"\1*sqrt", s_)
    s_ = re.sub(r"(\d|\))\s*pi", r"\1*pi", s_)
    s_ = re.sub(r"(\d)\s*\(", r"\1*(", s_).replace(" ", "")
    return s_


items = [it for _, _, ps in data03.TYPES for it in ps] + data03.STEP3
bad = 0
for it in items:
    got, ans = R[it["src"]], it["ans"]
    same = simplify(sympify(to_expr(ans)) - got) == 0
    if not same:
        bad += 1
    print(("OK  " if same else "BAD ") + it["src"], ans, "|", got)
print("문항", len(items), "불일치", bad)
