# -*- coding: utf-8 -*-
"""공통수학2 기본서 4단원 도형의 이동 검산: 문항마다 답을 따로 계산해 data04.py의 답과 맞춘다.
python verify04.py
- 좌표 문제는 sympy로 풀고, 최솟값·최댓값·개수는 촘촘한 수치 탐색이나 직접 이동(시뮬레이션)으로도 다시 확인한다.
"""
import sys, os
import math as _m
import itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sympy import *
import data04

x, y, t, a, b, c, k, m, n, r, h, s = symbols("x y t a b c k m n r h s", real=True)
R = {}


def dist(P, Q):
    return sqrt((P[0] - Q[0]) ** 2 + (P[1] - Q[1]) ** 2)


def ndist(P, Q):
    return _m.hypot(P[0] - Q[0], P[1] - Q[1])


def pdist(P, L):
    return Abs(L[0] * P[0] + L[1] * P[1] + L[2]) / sqrt(L[0] ** 2 + L[1] ** 2)


def refl_line(P, L):
    """점 P를 직선 L: Ax+By+C=0에 대하여 대칭이동"""
    A_, B_, C_ = L
    d = (A_ * P[0] + B_ * P[1] + C_) / (A_ ** 2 + B_ ** 2)
    return (P[0] - 2 * A_ * d, P[1] - 2 * B_ * d)


def clip(poly, A_, B_, C_):
    """볼록다각형 poly에서 A x + B y + C <= 0 인 부분 (Sutherland–Hodgman)"""
    out = []
    for i in range(len(poly)):
        P, Q = poly[i], poly[(i + 1) % len(poly)]
        fp, fq = A_ * P[0] + B_ * P[1] + C_, A_ * Q[0] + B_ * Q[1] + C_
        if fp <= 0:
            out.append(P)
        if (fp < 0 < fq) or (fq < 0 < fp):
            tt = fp / (fp - fq)
            out.append((P[0] + tt * (Q[0] - P[0]), P[1] + tt * (Q[1] - P[1])))
    return out


def halfplanes(poly):
    """반시계 볼록다각형의 변 → 안쪽이 <=0 인 반평면들"""
    hs = []
    for i in range(len(poly)):
        P, Q = poly[i], poly[(i + 1) % len(poly)]
        # 반시계이면 안쪽은 왼쪽: (Q-P) x (X-P) >= 0 → -(...) <= 0
        A_, B_ = (Q[1] - P[1]), -(Q[0] - P[0])
        C_ = -(A_ * P[0] + B_ * P[1])
        hs.append((A_, B_, C_))
    return hs


def inter(p1, p2):
    q = p1
    for hp in halfplanes(p2):
        q = clip(q, *hp)
        if not q:
            return []
    return q


def area(poly):
    return abs(sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1]
                   for i in range(len(poly)))) / 2


def ccw(poly):
    sa = sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1] for i in range(len(poly)))
    return poly if sa > 0 else poly[::-1]


# ================================================================ 01 도형의 평행이동
# g225: y=x²+2ax+2a² → y=x²+a²-a 의 평행이동 (a, -a), 원 x²+(y-5)²=9와 옮긴 원의 공통현 2
sol = []
for A0 in [Rational(i, 4) for i in range(1, 60)]:
    c1 = x ** 2 + (y - 5) ** 2 - 9
    c2 = (x - A0) ** 2 + (y - 5 + A0) ** 2 - 9
    P2 = solve([c1, c2], [x, y])
    P2 = [p for p in P2 if p[0].is_real]
    if len(P2) == 2 and simplify(dist(P2[0], P2[1]) - 2) == 0:
        sol.append(A0)
R["g225"] = sol[0] if len(sol) == 1 else None

# n1814(2022년 3월 고2 27번 꼴): 원 (x-3)²+(y+2)²=r²과 (a, b)만큼 평행이동한 원, 직선 12x-5y+6=0에 모두 접함, 두 원 위의 점 사이 거리 최솟값 5
r0 = pdist((3, -2), (12, -5, 6))
cands = []
for A0 in range(1, 40):
    for B0 in range(1, 40):
        if simplify(pdist((3 + A0, -2 + B0), (12, -5, 6)) - r0) == 0 and simplify(sqrt(A0 ** 2 + B0 ** 2) - 2 * r0 - 5) == 0:
            cands.append(r0 ** 2 + A0 + B0)
R["n1814"] = cands[0] if len(set(cands)) == 1 else None

# o22: 원 (x+2)²+(y+4)²=16을 (1, 2)만큼 평행이동한 원과 직선 y=3x+n이 만나는 정수 n의 합
R["o22"] = sum(N for N in range(-60, 61) if pdist((-1, -2), (3, -1, N)) <= 4)

# ================================================================ 02 평행이동한 도형의 공통부분
# n1713: 삼각형 OAB(O, (8,0), (0,8))와 삼각형 OCD(O, (0,-8), (-8,0))를 (t, t)만큼 옮긴 것의 공통부분 넓이 최댓값
T1 = ccw([(0.0, 0.0), (8.0, 0.0), (0.0, 8.0)])
best = 0
for i in range(1, 8000):
    tt = i / 1000
    T2 = ccw([(tt, tt), (tt, tt - 8), (tt - 8, tt)])
    q = inter(T1, T2)
    if q:
        best = max(best, area(q))
assert abs(best - 64 / 3) < 1e-4
# 정확히: 공통부분은 정사각형 [0,t]x[0,t]에서 두 꼭짓점 쪽 직각삼각형을 뺀 꼴. 넓이 t² - (2t-8)²(t>4) → 최대 t=16/3에서 64/3
R["n1713"] = Rational(64, 3)

# g261: T1 = 삼각형 (0,0),(0,2),(-2,0)을 x축 방향 t, T2 = 삼각형 (0,0),(0,-2),(2,0)을 y축 방향 2t, 공통부분이 육각형인 t 범위 a<t<1, 그때 넓이 최댓값 M
hexes = []
for i in range(1, 2000):
    tt = i / 1000
    A1 = ccw([(tt, 0.0), (tt, 2.0), (tt - 2, 0.0)])
    A2 = ccw([(0.0, 2 * tt), (0.0, 2 * tt - 2), (2.0, 2 * tt)])
    q = inter(A1, A2)
    # 겹치는 꼭짓점 정리
    qq = []
    for p in q:
        if not qq or ndist(p, qq[-1]) > 1e-9:
            qq.append(p)
    if len(qq) > 1 and ndist(qq[0], qq[-1]) < 1e-9:
        qq.pop()
    if len(qq) == 6:
        hexes.append((tt, area(qq)))
lo = min(h_[0] for h_ in hexes)
Mx = max(h_[1] for h_ in hexes)
assert abs(lo - 2 / 3) < 2e-3 and max(h_[0] for h_ in hexes) < 1 and abs(Mx - 8 / 7) < 1e-5
f_ = t * 2 * t - (3 * t - 2) ** 2                      # 직사각형 t×2t에서 두 직각이등변삼각형 뺌
tm = solve(diff(f_, t), t)[0]
R["g261"] = Rational(2, 3) + f_.subs(t, tm)

# ================================================================ 03 점의 대칭이동
# g230: 제2사분면의 점 P(a, b)는 y=-2x+3 위, Q=y=x 대칭, R=원점 대칭, 넓이 45
res = []
for A0 in solve(Abs(3 * a ** 2 - 12 * a + 9) - 45, a):
    if A0.is_real and A0 < 0:
        B0 = -2 * A0 + 3
        P_, Q_, R_ = (A0, B0), (B0, A0), (-A0, -B0)
        ar = Abs((Q_[0] - P_[0]) * (R_[1] - P_[1]) - (Q_[1] - P_[1]) * (R_[0] - P_[0])) / 2
        assert simplify(ar - 45) == 0
        res.append(A0 + B0)
R["g230"] = res[0]

# n1922(2024년 9월 고1 27번 꼴): A(a, 2) (a>2), B=y=x 대칭, C=B의 x축 대칭, r1 r2 = 6√2


def circumR(P, Q, S):
    A_, B_, C_ = dist(Q, S), dist(P, S), dist(P, Q)
    ar = Abs((Q[0] - P[0]) * (S[1] - P[1]) - (Q[1] - P[1]) * (S[0] - P[0])) / 2
    return A_ * B_ * C_ / (4 * ar)


ap = symbols("ap", positive=True)
A_, B_, C_ = (ap, 2), (2, ap), (2, -ap)
eq = simplify(circumR(A_, B_, C_) * circumR(A_, (0, 0), C_))
sols = [v for v in solve(eq - 6 * sqrt(2), ap) if v > 2]
R["n1922"] = sols[0] ** 2

# o23: 제1사분면 A(a, b), B=y=x 대칭, C=원점 대칭, a-b=1, 넓이 7
res = []
for A0 in range(1, 30):
    B0 = A0 - 1
    if B0 > 0:
        P_, Q_, R_ = (A0, B0), (B0, A0), (-A0, -B0)
        ar = abs((Q_[0] - P_[0]) * (R_[1] - P_[1]) - (Q_[1] - P_[1]) * (R_[0] - P_[0])) / 2
        if ar == 7:
            res.append(A0 ** 2 + B0 ** 2)
R["o23"] = res[0] if len(res) == 1 else None

# ================================================================ 04 도형의 대칭이동
# f9-21: x²+(y-a)²=n을 y=x 대칭한 원과 y=x의 교점 개수 합 f_1+...+f_21=7인 a (보기 2, 4, 6, 8, 10)
good = []
for A0 in range(1, 20):
    tot = 0
    for N in range(1, 22):
        d2 = Rational(A0 ** 2, 2)
        tot += 2 if N > d2 else (1 if N == d2 else 0)
    if tot == 7:
        good.append(A0)
R["f9-21"] = good[0] if len(good) == 1 else None

# n1899: x²+y²+6x-10y+26=0을 y=x 대칭한 원이 y=mx+2에 접하는 m의 합
R["n1899"] = sum(solve(pdist((5, -3), (m, -1, 2)) ** 2 - 8, m))

# g255: (x-2)²+y²=16 위 P → x축 방향 -2 → y=x 대칭 = Q, A(1, -√3), B(3, √3), 삼각형 ABQ 넓이 최대 S, 그때 P의 x좌표 a
best = (-1, None)
for i in range(72000):
    th = 2 * _m.pi * i / 72000
    P_ = (2 + 4 * _m.cos(th), 4 * _m.sin(th))
    Q_ = (P_[1], P_[0] - 2)
    A1, B1 = (1, -_m.sqrt(3)), (3, _m.sqrt(3))
    ar = abs((B1[0] - A1[0]) * (Q_[1] - A1[1]) - (B1[1] - A1[1]) * (Q_[0] - A1[0])) / 2
    if ar > best[0]:
        best = (ar, P_[0])
assert abs(best[0] + best[1] - float(12 + 2 * sqrt(3))) < 1e-4
R["g255"] = 2 * (sqrt(3) + 4) + 4

# ================================================================ 05 점의 이동 규칙
# g227: (5, 2)에서 출발, xy>0일 때 x>y면 y=x 대칭, x<=y면 (x+4, y-6), xy<0이면 x축 대칭, xy=0이면 멈춤
P_ = (5, 2)
cnt = 0
while P_[0] * P_[1] != 0:
    X, Y = P_
    if X * Y > 0:
        P_ = (Y, X) if X > Y else (X + 4, Y - 6)
    else:
        P_ = (X, -Y)
    cnt += 1
    assert cnt < 1000
R["g227"] = P_[0] + P_[1] + cnt

# g257: P는 x축·y축·원점 대칭을 차례로, Q는 y=x·y축·y=x·x축 대칭을 차례로 반복, 2000번 중 일치 횟수
fP = [lambda p: (p[0], -p[1]), lambda p: (-p[0], p[1]), lambda p: (-p[0], -p[1])]
fQ = [lambda p: (p[1], p[0]), lambda p: (-p[0], p[1]), lambda p: (p[1], p[0]), lambda p: (p[0], -p[1])]
P_, Q_ = (1, 2), (1, 2)
same = 0
for i in range(2000):
    P_ = fP[i % 3](P_)
    Q_ = fQ[i % 4](Q_)
    same += P_ == Q_
R["g257"] = same

# ================================================================ 06 점에 대한 대칭이동
# m63: A(5, -2)를 지나는 기울기 m(m<0) 직선 l을 점 (2, 1)에 대칭 후 x축 대칭한 l'. l'이 A를 지날 때 m=p, l'⊥l일 때 m=q
def img63(P):                                 # 점 (2, 1)에 대칭 → x축 대칭
    Q0 = (4 - P[0], 2 - P[1])
    return (Q0[0], -Q0[1])


P1, P2 = img63((5, -2)), img63((6, -2 + m))      # 직선 l 위의 두 점의 상
slope_ = simplify((P2[1] - P1[1]) / (P2[0] - P1[0]))
p_ = [v for v in solve(P1[1] + slope_ * (5 - P1[0]) + 2, m) if v < 0][0]   # l'이 A(5, -2)를 지남
q_ = [v for v in solve(slope_ * m + 1, m) if v < 0][0]                     # l' ⊥ l
R["m63"] = p_ + q_

# m64: 제2사분면 P(a, 1), Q = x+y=2 대칭, R = (1, 1) 대칭, 넓이 4
res = []
for A0 in solve(Abs((1 - a) ** 2) - 4, a):
    if A0 < 0:
        P_ = (A0, 1)
        Q_ = refl_line(P_, (1, 1, -2))
        R_ = (2 - A0, 1)
        ar = Abs((Q_[0] - P_[0]) * (R_[1] - P_[1]) - (Q_[1] - P_[1]) * (R_[0] - P_[0])) / 2
        assert simplify(ar - 4) == 0
        res.append(A0)
R["m64"] = res[0]

# ================================================================ 07 직선에 대한 대칭이동
# g241: (x+3)²+(y+2)²=9를 y=mx+n에 대칭 → x²+y²+2x-12y+k=0
K = solve(9 - (1 + 36 - k), k)[0]
M_ = solve(Eq(m * 4, -1), m)[0]                # 두 중심 (-3,-2), (-1,6) 이은 직선(기울기 4)에 수직
N_ = solve(Eq(2, M_ * (-2) + n), n)[0]          # 중점 (-2, 2)를 지남
assert refl_line((-3, -2), (M_, -1, N_)) == (-1, 6)
R["g241"] = K * M_ * N_

# f5-19: A(3, m+1)을 y=x-2 대칭 → B, B를 x축 대칭 → C, 세 점이 (x-a)²+(y-b)²=2m²-5m+2 위
res = []
for M0 in range(1, 30):
    A_ = (Rational(3), Rational(M0 + 1))
    B_ = refl_line(A_, (1, -1, -2))
    C_ = (B_[0], -B_[1])
    sol_ = solve([(A_[0] - a) ** 2 + (A_[1] - b) ** 2 - (B_[0] - a) ** 2 - (B_[1] - b) ** 2,
                  (B_[0] - a) ** 2 + (B_[1] - b) ** 2 - (C_[0] - a) ** 2 - (C_[1] - b) ** 2], [a, b], dict=True)
    for s_ in sol_:
        if simplify((A_[0] - s_[a]) ** 2 + (A_[1] - s_[b]) ** 2 - (2 * M0 ** 2 - 5 * M0 + 2)) == 0:
            res.append(s_[a] + s_[b] + M0)
R["f5-19"] = res[0] if len(res) == 1 else None

# m47: 중심 (6, 1), 반지름 1인 원을 y=2x+k에 대칭한 원 위의 모든 점이 x>=0, y>=0 → a<=k<=b
ks = [K0 / 100 for K0 in range(-2000, 2000)
      if (lambda C0: C0[0] >= 1 and C0[1] >= 1)(refl_line((6, 1), (2, -1, K0 / 100)))]
assert abs(min(ks) + 11) < 1e-9 and abs(max(ks) + 4.75) < 1e-9
R["m47"] = Rational(-19, 4) - (-11)

# ================================================================ 08 도형 f(x, y)=0의 이동
# g237: f(x,y)=0은 (2,0),(0,-2),(4,-2) 삼각형, f(y+1, -x-3)=0 위 (c, d), f 위 (a, b), (d-b)/(c-a)의 최대+최소
T = [(2, 0), (0, -2), (4, -2)]
Tp = [(-Y0 - 3, X0 - 1) for X0, Y0 in T]        # (X, Y)가 T 위이면 (x, y)=(-Y-3, X-1)


def boundary(poly, nn=200):
    pts = []
    for i in range(len(poly)):
        P, Q = poly[i], poly[(i + 1) % len(poly)]
        for j in range(nn):
            pts.append((P[0] + (Q[0] - P[0]) * j / nn, P[1] + (Q[1] - P[1]) * j / nn))
    return pts


sl = [(q[1] - p[1]) / (q[0] - p[0]) for p in boundary(T) for q in boundary(Tp) if abs(q[0] - p[0]) > 1e-12]
assert abs(max(sl) - 1 / 3) < 1e-9 and abs(min(sl) + 5) < 1e-9
R["g237"] = Rational(1, 3) + (-5)

# o31: f(x,y)=y-x² (-1<=x<=1, 0<=y<=1). f(x-2, y+2)=0, f(x-2, 2-y)=0 과 x=1, x=3으로 둘러싸인 넓이
upper = 2 - (x - 2) ** 2
lower = (x - 2) ** 2 - 2
R["o31"] = integrate(upper - lower, (x, 1, 3))
assert integrate(x ** 2, (x, -1, 0)) == Rational(1, 3)

# ================================================================ 09 대칭이동과 곡선 위의 두 점
# g258: y=x²-2x+2 위 A, B가 y=-x/2+12에 대하여 대칭
res = []
for p1 in range(-20, 21):
    for p2 in range(-20, 21):
        if p1 < p2:
            A_, B_ = (Rational(p1), Rational(p1 ** 2 - 2 * p1 + 2)), (Rational(p2), Rational(p2 ** 2 - 2 * p2 + 2))
            if refl_line(A_, (1, 2, -24)) == (Rational(B_[0]), Rational(B_[1])):
                res.append(dist(A_, B_))
assert len(res) == 1
R["g258"] = res[0]

# o17: A(1, 5), B(3, 5)의 y=x 대칭 A', B', C(a, -a²), (삼각형 ABC 넓이) = 2(삼각형 A'B'C 넓이), a≠5인 모든 a의 합
def tri(P, Q, S):
    return Abs((Q[0] - P[0]) * (S[1] - P[1]) - (Q[1] - P[1]) * (S[0] - P[0])) / 2


sols = solve(tri((1, 5), (3, 5), (a, -a ** 2)) - 2 * tri((5, 1), (5, 3), (a, -a ** 2)), a)
sols = [v for v in sols if v.is_real and v != 5]
R["o17"] = simplify(sum(sols))

# ================================================================ 10 대칭이동을 이용한 최단 거리
# b070(Basecamp 1단원 070): 40×30 직사각형, A(0, 20), B(40, 10), P는 y=30 위, Q는 x축 위
best = min(ndist((0, 20), (px, 30)) + ndist((px, 30), (qx, 0)) + ndist((qx, 0), (40, 10))
           for px in [i / 10 for i in range(0, 401)] for qx in [j / 10 for j in range(0, 401)])
assert abs(best - 10 * _m.sqrt(41)) < 0.05
R["b1-070"] = dist((0, 40), (40, -10))

# n1730(2022년 11월 고1 15번 꼴): A(4, 1), B(1, 5), x축 위 P, BQ=√5인 Q, AP+PQ 최소일 때 삼각형 APQ 넓이
Ap = (4, -1)
Pp = (Rational(7, 2), 0)                          # 직선 A'B와 x축의 교점
assert simplify((Pp[1] - Ap[1]) * (5 - Ap[1]) ** -1 - (Pp[0] - Ap[0]) * (1 - Ap[0]) ** -1) == 0
uB = ((Pp[0] - 1) / dist(Pp, (1, 5)), (Pp[1] - 5) / dist(Pp, (1, 5)))
Qp = (1 + sqrt(5) * uB[0], 5 + sqrt(5) * uB[1])
R["n1730"] = simplify(tri((4, 1), Pp, Qp))
# 수치로 최솟값 위치 확인
bb = min((ndist((4, 1), (px, 0)) + ndist((px, 0), (1, 5)) - _m.sqrt(5), px) for px in [i / 1000 for i in range(-5000, 10000)])
assert abs(bb[1] - 3.5) < 2e-3

# n1813(2023년 9월 고1 16번 꼴): C1:(x-1)²+(y-9)²=1, C2:(x+3)²+(y-4)²=1, y축 위 P, y=x 위 Q, AP+PQ+QB 최솟값
D_ = (-1, 9)       # C1 중심의 y축 대칭
E_ = (4, -3)       # C2 중심의 y=x 대칭
R["n1813"] = dist(D_, E_) - 2
# 수치 확인: P(0, p), Q(q, q)
bb = min(ndist(D_, (0, pp)) + ndist((0, pp), (qq, qq)) + ndist((qq, qq), (-3, 4)) - 2
         for pp in [i / 20 for i in range(-40, 200)] for qq in [j / 20 for j in range(-100, 100)])
assert abs(bb - 11) < 0.02

# k01v(2026년 3월 고2 14번 변형): 원 (x-9)²+(y-5)²=2 위 P, y=x 위 Q, A(11, 3), AQ+QP 최솟값
bb = min(ndist((11, 3), (qq, qq)) + min(ndist((qq, qq), (9 + _m.sqrt(2) * _m.cos(th), 5 + _m.sqrt(2) * _m.sin(th)))
                                         for th in [2 * _m.pi * i / 360 for i in range(360)])
         for qq in [j / 50 for j in range(250, 500)])
assert abs(bb - 5 * _m.sqrt(2)) < 0.01
R["k01v"] = dist((11, 3), (5, 9)) - sqrt(2)

# n1601: P(6, 2), A(a, a), B(a+2, a-1), PA+PB 최소 (a=p/5, 최솟값 q), 2x-y+4=0을 (p, q²) 평행이동 → 2x-y-r=0
bb = min((ndist((6, 2), (aa, aa)) + ndist((6, 2), (aa + 2, aa - 1)), aa) for aa in [i / 10000 for i in range(0, 80000)])
p_ = 5 * Rational(18, 5)
assert abs(bb[1] - 3.6) < 1e-3 and abs(bb[0] - _m.sqrt(13)) < 1e-6
q2 = 13
rr = solve(Eq(2 * (x - p_) - (y - q2) + 4, 2 * x - y - r), r)[0]
R["n1601"] = p_ + q2 + rr

# ================================================================ 11 꺾은선의 길이의 최솟값
# g254: y=x 위 A, B (AB=2√2, B가 오른쪽), C(1, -1), D(7, 1), 사각형 ACDB 둘레 최솟값
bb = min(ndist((aa, aa), (1, -1)) + ndist((1, -1), (7, 1)) + ndist((7, 1), (aa + 2, aa + 2)) + 2 * _m.sqrt(2)
         for aa in [i / 10000 for i in range(-30000, 50000)])
assert abs(bb - float(2 * sqrt(2) + 4 * sqrt(10))) < 1e-6
R["g254"] = 2 * sqrt(2) + 4 * sqrt(10)

# f2-18: P(12, 0), Q(0, 5), 길이 5√2인 RS가 반직선 y=-x (x>=-5) 위, 사각형 PQRS 둘레 최솟값 (R이 S보다 왼쪽 위)
bb = min(13 + 5 * _m.sqrt(2) + ndist((0, 5), (rx, -rx)) + ndist((rx + 5, -rx - 5), (12, 0))
         for rx in [i / 1000 for i in range(-5000, 20000)])
assert abs(bb - (26 + 5 * _m.sqrt(2))) < 1e-5
R["f2-18"] = 26 + 5 * sqrt(2)

# k03v(2022년 9월 고1 17번 변형): A(2, 4), B(-5, 1), x축 위 C, y=x 위 D, AD+CD+BC 최솟값
bb = min(ndist((2, 4), (dd, dd)) + ndist((dd, dd), (cc, 0)) + ndist((cc, 0), (-5, 1))
         for dd in [i / 100 for i in range(-300, 400)] for cc in [j / 100 for j in range(-500, 400)])
assert abs(bb - 3 * _m.sqrt(10)) < 1e-3
R["k03v"] = dist((4, 2), (-5, -1))

# o28: A(5, 1), B(5, -1), y=x 위 P, y=-x 위 Q (x좌표 0~5), 사각형 APQB 둘레 최솟값
bb = min(ndist((5, 1), (pp, pp)) + ndist((pp, pp), (qq, -qq)) + ndist((qq, -qq), (5, -1)) + 2
         for pp in [i / 200 for i in range(1, 1000)] for qq in [j / 200 for j in range(1, 1000)])
assert abs(bb - 12) < 1e-3
R["o28"] = 12

# b073(Basecamp 1단원 073): A(6, 10), B(8, -8), y축 위 P, Q, x=2 위 R, AP+PR+RQ+QB 최솟값
bb = min(ndist((6, 10), (0, pp)) + ndist((0, pp), (2, rr_)) + ndist((2, rr_), (0, qq)) + ndist((0, qq), (8, -8))
         for pp in [i / 20 for i in range(-100, 260)] for rr_ in [i / 20 for i in range(-200, 200, 2)] for qq in [j / 20 for j in range(-200, 100, 2)])
assert abs(bb - 18 * _m.sqrt(2)) < 0.05
R["b1-073"] = dist((-6, 10), (12, -8))

# ================================================================ STEP 3
# f7-16(2023년 3월 고2 29번 꼴): 원 (x-5)²+(y-1)²=r² 위 P, Q. P의 y=x 대칭 (x1, y1), Q의 x축 방향 k 평행이동 (x2, y2), 기울기 최소 0, 최대 3/4
res = []
for K0 in range(-40, 41):
    for R0 in range(1, 10):
        dx, dy = 1 - (5 + K0), 5 - 1                 # 두 중심 (1, 5), (5+k, 1)
        ok = lambda M0: (M0 * dx - dy) ** 2 <= 4 * R0 ** 2 * (1 + M0 ** 2) + 1e-12
        ms = [M0 / 400 for M0 in range(-4000, 4001) if ok(M0 / 400)]
        if ms and abs(min(ms)) < 1e-9 and abs(max(ms) - 0.75) < 1e-9 and ok(-10) is False and ok(10) is False:
            res.append(abs(R0 + K0))
R["f7-16"] = res[0] if len(set(res)) == 1 else None

# k02v(2025년 10월 고1 21번 변형): C1 중심 A(제1사분면), O를 지남, C2 = 원점 대칭, ∠POQ=90°일 때 PQ=10, B에서의 접선 기울기 2 → A와 l 사이 거리
A_ = (2 * sqrt(5), sqrt(5))
rad = dist(A_, (0, 0))
assert rad == 5
# PQ가 일정하게 10인지 수치로 확인
for th in [0.3, 1.1, 2.0, 4.0]:
    P_ = (float(A_[0]) + 5 * _m.cos(th), float(A_[1]) + 5 * _m.sin(th))
    # Q: C2 위, OP ⊥ OQ → Q = s(-P_y, P_x)
    for sg in (1, -1):
        ss = symbols("ss", real=True)
        Qe = (sg * ss * -P_[1], sg * ss * P_[0])
        for sv in solve((Qe[0] + float(A_[0])) ** 2 + (Qe[1] + float(A_[1])) ** 2 - 25, ss):
            if abs(sv) > 1e-9:
                Q_ = (float(Qe[0].subs(ss, sv)), float(Qe[1].subs(ss, sv)))
                assert abs(ndist(P_, Q_) - 10) < 1e-6
B_ = (-2 * A_[0], 0)
C2 = (-A_[0], -A_[1])
slope_tan = -1 / ((B_[1] - C2[1]) / (B_[0] - C2[0]))
assert simplify(slope_tan - 2) == 0
R["k02v"] = simplify(pdist(A_, (2, -1, -2 * B_[0])))

# g253: 반지름 4, 중심각 60°인 부채꼴 BOA의 호 위 P, OA·OB 위 Q, R, 삼각형 PQR 둘레 최솟값
best = 1e9
for i in range(1, 60):
    th = _m.radians(i)
    P_ = (4 * _m.cos(th), 4 * _m.sin(th))          # OA는 x축, OB는 60°
    P1 = (P_[0], -P_[1])
    P2 = (4 * _m.cos(_m.radians(120) - th), 4 * _m.sin(_m.radians(120) - th))
    best = min(best, ndist(P1, P2))
    assert abs(ndist(P1, P2) - 4 * _m.sqrt(3)) < 1e-9
R["g253"] = 4 * sqrt(3)

# m58: 사분원 x²+y²=16 위 A, B, C (각 22.5°, 45°, 52.5°), OA 위 D, OC 위 E, 삼각형 BED 둘레 최소일 때 원점과 직선 D1E1 사이 거리
B1 = (4, 0)                                   # B를 OA(22.5°)에 대칭
B2 = (4 * _m.cos(_m.radians(60)), 4 * _m.sin(_m.radians(60)))   # B를 OC(52.5°)에 대칭
d_ = abs(B1[0] * B2[1] - B1[1] * B2[0]) / ndist(B1, B2)
assert abs(d_ - 2 * _m.sqrt(3)) < 1e-12
# 교점 D1, E1이 각각 선분 OA, OC 위에 있는지
for ang in (22.5, 52.5):
    u_ = (_m.cos(_m.radians(ang)), _m.sin(_m.radians(ang)))
    # 직선 B1B2와 반직선 su_의 교점
    A_m = [[u_[0], -(B2[0] - B1[0])], [u_[1], -(B2[1] - B1[1])]]
    det = A_m[0][0] * A_m[1][1] - A_m[0][1] * A_m[1][0]
    s_ = (B1[0] * A_m[1][1] - A_m[0][1] * B1[1]) / det
    assert 0 < s_ < 4
R["m58"] = 2 * sqrt(3)

# n1901: x²+y²=10과 (1, 3)만큼 평행이동한 원의 내부의 공통부분 넓이 aπ-b√3 → 6a+b
cnt_in = 0
NN = 1200
for i in range(NN):
    for j in range(NN):
        X0 = -3.2 + 6.4 * (i + 0.5) / NN
        Y0 = -3.2 + 9.4 * (j + 0.5) / NN
        if X0 * X0 + Y0 * Y0 < 10 and (X0 - 1) ** 2 + (Y0 - 3) ** 2 < 10:
            cnt_in += 1
num_area = cnt_in * (6.4 / NN) * (9.4 / NN)
ex = Rational(20, 3) * pi - 5 * sqrt(3)               # 두 중심 사이 거리 √10 = 반지름 → 정삼각형 두 개, 부채꼴 120°
assert abs(num_area - float(ex)) < 0.02
R["n1901"] = 6 * Rational(20, 3) + 5

# m65: A(4, a) (a>4), B(2, 1), y=x 대칭 A', B', AB와 A'B'의 교점 P, 삼각형 APA' : BPB' = 9 : 4
res = []
for A0 in [Rational(i, 2) for i in range(9, 60)]:
    A_, B_ = (4, A0), (2, 1)
    Ap_, Bp_ = (A0, 4), (1, 2)
    L1 = Line(Point(*A_), Point(*B_))
    L2 = Line(Point(*Ap_), Point(*Bp_))
    I = L1.intersection(L2)
    if I and isinstance(I[0], Point):
        P_ = (I[0].x, I[0].y)
        if simplify(tri(A_, P_, Ap_) * 4 - tri(B_, P_, Bp_) * 9) == 0:
            res.append(A0)
R["m65"] = res[0] if len(res) == 1 else None

# g259: 한 변 6인 정사각형 ABCD(A(0,6), B(0,0), C(6,0), D(6,6)), E(2,6), F(6,2), BE·BF로 접은 A', C', A'C' = q√2/p
Ap_ = refl_line((0, 6), (3, -1, 0))
Cp_ = refl_line((6, 0), (1, -3, 0))
val = nsimplify(dist(Ap_, Cp_) / sqrt(2))
R["g259"] = val.p + val.q

# m67: 중심 (3, 7), 반지름 2√2 원을 y=-x 대칭 후 (a, a) 평행이동, 공통현 2√6
sols = []
for A0 in range(-40, 41):
    C2 = (-7 + A0, -3 + A0)
    d_ = dist((3, 7), C2)
    if d_ < 4 * sqrt(2) and simplify(2 * sqrt(8 - (d_ / 2) ** 2) - 2 * sqrt(6)) == 0:
        sols.append(A0)
R["m67"] = sum(sols)

# m68: y=2x+1을 직선 l에 대칭한 직선의 기울기가 2, x²+(y-3)²=1을 l에 대칭한 원 (x-a)²+(y-b)²=r², a²+b²+r² 최솟값
best = 1e9
for slope in (2, -0.5):
    for i in range(-4000, 4000):
        icpt = i / 200
        L = (slope, -1, icpt)
        img = refl_line((0, 3), L)
        # 직선 y=2x+1의 상 기울기 확인
        p1, p2 = refl_line((0, 1), L), refl_line((1, 3), L)
        assert abs((p2[1] - p1[1]) / (p2[0] - p1[0]) - 2) < 1e-9
        best = min(best, img[0] ** 2 + img[1] ** 2 + 1)
assert abs(best - 2.8) < 1e-3
R["m68"] = Rational(9, 5) + 1

# ---------------------------------------------------------------- data04의 답과 맞추기
import re          # sympy의 re를 덮는다


def to_expr(s_):
    s_ = s_.replace("LEFT (", "(").replace("RIGHT )", ")").replace("~", "").replace("it-", "-")
    s_ = re.sub(r"sqrt\s*\{([^{}]*)\}", r"sqrt(\1)", s_)
    s_ = re.sub(r"\{([^{}]*)\}\s*over\s*\{([^{}]*)\}", r"((\1)/(\2))", s_)
    s_ = re.sub(r"(\d)\s*sqrt", r"\1*sqrt", s_)
    s_ = re.sub(r"(\d|\))\s*pi", r"\1*pi", s_)
    s_ = re.sub(r"(\d)\s*\(", r"\1*(", s_).replace(" ", "")
    return s_


items = [it for _, _, ps in data04.TYPES for it in ps] + data04.STEP3
bad = 0
for it in items:
    got, ans = R.get(it["src"]), it["ans"]
    same = got is not None and simplify(sympify(to_expr(ans)) - got) == 0
    if not same:
        bad += 1
    print(("OK  " if same else "BAD ") + it["src"], ans, "|", got)
print("문항", len(items), "불일치", bad)
