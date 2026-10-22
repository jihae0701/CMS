# 공통수학2 3단원(원의 방정식) 유형서 문항 정답 독립 검산 (문항 기호는 c2unit03.py의 v).
# 좌표는 sympy로 풀고, 개수·최대·최소는 경우를 모두 훑거나 촘촘한 수치 탐색으로 확인한다.
import math
from sympy import (Rational as Q, sqrt, symbols, solve, simplify, Abs, nsimplify, expand, Poly, pi,
                   discriminant, S, Eq, Point, Polygon, Circle, Line, Segment, atan, tan, factor)
R = []
x, y, a, b, c, k, t, m, n, r = symbols("x y a b c k t m n r", real=True)


def chk(no, got, exp):
    R.append((no, simplify(got - exp) == 0 if not isinstance(got, str) else got == exp, got, exp))


def dist(P, l):
    """점 P와 직선 l: (A, B, C) → Ax+By+C=0 사이의 거리"""
    A, B, C = l
    return Abs(A * P[0] + B * P[1] + C) / sqrt(A ** 2 + B ** 2)


def area(*P):
    return abs(Polygon(*[Point(*p) for p in P]).area)


def circ(expr):
    """x²+y²+Ax+By+C=0 → (중심, 반지름²)"""
    p = Poly(expand(expr), x, y)
    A, B, C = p.coeff_monomial(x), p.coeff_monomial(y), p.coeff_monomial(1)
    return (-A / 2, -B / 2), A ** 2 / 4 + B ** 2 / 4 - C


def mark(truth):
    """ㄱㄴㄷ 참·거짓 → 원문 5지선다 ① ㄱ ② ㄷ ③ ㄱ, ㄴ ④ ㄱ, ㄷ ⑤ ㄱ, ㄴ, ㄷ (2023년 9월 20번)"""
    tbl = {(1, 0, 0): "①", (0, 0, 1): "②", (1, 1, 0): "③", (1, 0, 1): "④", (1, 1, 1): "⑤"}
    return tbl.get(tuple(int(v) for v in truth), "?")


def mark2(truth):
    """2022년 3월 고2 19번 보기: ① ㄱ ② ㄴ ③ ㄱ, ㄴ ④ ㄱ, ㄷ ⑤ ㄱ, ㄴ, ㄷ"""
    tbl = {(1, 0, 0): "①", (0, 1, 0): "②", (1, 1, 0): "③", (1, 0, 1): "④", (1, 1, 1): "⑤"}
    return tbl.get(tuple(int(v) for v in truth), "?")


# ================================================================ 원의 방정식
O_, r2 = circ(x ** 2 + y ** 2 - 4 * x + 10 * y - 1)
chk("f3-4", O_[0] + O_[1] + r2, 27)

# o10: 중심이 제1사분면인 원이 되는 정수 k
good = []
for K in range(-30, 31):
    (cx, cy), rr = circ(x ** 2 + y ** 2 + 2 * (K - 5) * x - 2 * (K + 2) * y + K ** 2 - 6 * K + 30)
    if rr > 0 and cx > 0 and cy > 0:
        good.append(K)
chk("o10", sum(good), 9)

# n1622: 원이 제1, 4사분면을 모두 지나고 제2, 3사분면은 지나지 않는 자연수 k (원 위의 점을 촘촘히 훑음)
cnt = 0
for K in range(1, 40):
    (cx, cy), rr = circ(x ** 2 + y ** 2 - 8 * x - 2 * (K - 1) * y + 2 * K ** 2 - 14 * K + 28)
    if rr <= 0:
        continue
    R0 = math.sqrt(float(rr))
    q = set()
    for i in range(3600):
        th = 2 * math.pi * i / 3600
        X, Y = float(cx) + R0 * math.cos(th), float(cy) + R0 * math.sin(th)
        if abs(X) < 1e-9 or abs(Y) < 1e-9:
            continue
        q.add((X > 0, Y > 0))
    if (True, True) in q and (True, False) in q and (False, True) not in q and (False, False) not in q:
        cnt += 1
chk("n1622", cnt, 2)

# n1642: 원과 직선의 두 교점을 지름의 양 끝점으로 하는 원의 중심
X = solve([x ** 2 + y ** 2 + 9 * x - 6 * y + 3, 2 * x - y + 2], [x, y])
chk("n1642", (X[0][0] + X[1][0]) / 2 + (X[0][1] + X[1][1]) / 2, Q(1, 2))

# ================================================================ 세 점을 지나는 원
A0, B0, C0 = (1, 5), (2, 4), (-1, 1)
cen = solve([(x - A0[0]) ** 2 + (y - A0[1]) ** 2 - (x - B0[0]) ** 2 - (y - B0[1]) ** 2,
             (x - A0[0]) ** 2 + (y - A0[1]) ** 2 - (x - C0[0]) ** 2 - (y - C0[1]) ** 2], [x, y])
G = (Q(A0[0] + B0[0] + C0[0], 3), Q(A0[1] + B0[1] + C0[1], 3))
chk("f1-6", sqrt((cen[x] - G[0]) ** 2 + (cen[y] - G[1]) ** 2), sqrt(5) / 3)

s_ = solve([X0 ** 2 + Y0 ** 2 + a * X0 + b * Y0 + c for X0, Y0 in ((0, 3), (2, 1), (2, -3))], [a, b, c])
chk("o16", abs(s_[a]) + abs(s_[b]) + abs(s_[c]), 21)

# ================================================================ 좌표축에 접하는 원
rs = solve((3 - r) ** 2 + (2 - r) ** 2 - r ** 2, r)          # 중심 (r, r)
chk("n1591", sum(v ** 2 for v in rs) * pi, 74 * pi)

# f9-18: 중심 (t, f(t))가 제2사분면, |t|=|f(t)|
ts = [T for T in solve(t ** 2 - t - 4 + t, t) if T < 0]       # 제2사분면이면 f(t) = -t
T = ts[0]
cx, cy, rr = T, -T, -T
e = expand((x - cx) ** 2 + (y - cy) ** 2 - rr ** 2)
pe = Poly(e, x, y)
chk("f9-18", pe.coeff_monomial(x) + pe.coeff_monomial(y) + pe.coeff_monomial(1), 4)

# n1666: 중심이 원 (x+2)²+(y+2)²=16 위, 두 좌표축에 동시에 접함
cs = [(X0, X0) for X0 in solve((x + 2) ** 2 * 2 - 16, x)] + [(X0, -X0) for X0 in solve((x + 2) ** 2 + (-x + 2) ** 2 - 16, x)]
cs = [p for p in cs if p[0] != 0]
chk("n1666", sum(p[0] ** 2 for p in cs) * pi, 32 * pi)

# n1586: 두 축과 직선 3x-4y-12=0에 접하는 원
rad = []
for sx, sy in ((1, 1), (-1, 1), (-1, -1), (1, -1)):
    for R0 in solve(Abs(3 * sx * r - 4 * sy * r - 12) - 5 * r, r):
        if R0 > 0:
            rad.append(R0)
chk("n1586", len(rad) * sum(rad), 48)

# n1749: 중심 (a, -a), 반지름 |a|, 직선 3x+4y-12=0에 접함 → 접점 A, B
pts = []
for A1 in solve(Abs(3 * a - 4 * a - 12) - 5 * Abs(a), a):
    C1 = Point(A1, -A1)
    L = Line(Point(0, 3), Point(4, 0))
    pts.append(L.projection(C1))
chk("n1749", pts[0].distance(pts[1]), 7)

# ================================================================ 점이 나타내는 도형
cP, rP = circ(expand(9 * ((x + 3) ** 2 + y ** 2) - ((x - 3) ** 2 + y ** 2)) / 8)
chk("f2-10", 2 * pi * sqrt(rP), Q(9, 2) * pi)

cP, rP = circ(expand(((x + 3) ** 2 + y ** 2) - 9 * ((x - 1) ** 2 + y ** 2)) / -8)
top = (cP[0], cP[1] + sqrt(rP))                               # 제1사분면 위의 점
assert top[0] > 0 and top[1] > 0
chk("o12", Q(1, 2) * 4 * top[1], 3)

# o14: C1 반지름 2(직선 x=2와 중심 (4, 6) 사이 거리), C2 중심 (4t, 6t), 반지름 2t
tt = [T for T in solve(Abs(4 * t - 2) - 2 * t, t) if 0 < T < 1]
chk("o14", 2 + 2 * tt[0], Q(8, 3))

# ================================================================ 두 원의 교점을 지나는 도형
c1 = (x - 3) ** 2 + (y - 5) ** 2 - r ** 2
c2 = (x - 1) ** 2 + (y - 3) ** 2 - 4
chord = expand(c1 - c2)
rr = [v for v in solve(chord.subs({x: 1, y: 3}), r) if v > 0]
chk("n1619", rr[0], 2 * sqrt(3))

f1 = x ** 2 + y ** 2 + 2 * x - 2 * y - 3
f2 = x ** 2 + y ** 2 - 6 * x - 4 * y + 9
P2 = solve([f1, f2], [x, y])
cen = solve([(x - P2[0][0]) ** 2 + (y - P2[0][1]) ** 2 - (x - P2[1][0]) ** 2 - (y - P2[1][1]) ** 2,
             (x - P2[0][0]) ** 2 + (y - P2[0][1]) ** 2 - (x - 1) ** 2 - (y - 4) ** 2], [x, y])
chk("o05", sqrt((cen[x] - 1) ** 2 + (cen[y] - 4) ** 2), sqrt(37))

AB = solve([(x - 3) ** 2 + y ** 2 - 10, (x + 3) ** 2 + (y - 2) ** 2 - 18], [x, y])
chk("g191", sum((p[1] - 2) / (p[0] + 3) for p in AB), -Q(6, 7))

# ================================================================ 원 위의 점까지의 거리
th = symbols("th", real=True)
vals = []
for i in range(7200):
    T = 2 * math.pi * i / 7200
    X0, Y0 = 3 * math.cos(T), 3 + 3 * math.sin(T)
    vals.append((X0 - 8) ** 2 + (Y0 - 3) ** 2 + X0 ** 2 + (Y0 - 9) ** 2)
chk("n1541", int(round(max(vals) + min(vals))), 236)
chk("n1541", 2 * (25 + (5 + 3) ** 2) + 2 * (25 + (5 - 3) ** 2), 236)   # 중선정리: 2(AC²+PC²), C(4, 6)

ns = []
for N in [Q(i, 4) for i in range(1, 200)]:
    d0 = sqrt(10)
    M_, m_ = d0 + sqrt(N), Abs(d0 - sqrt(N))
    if simplify(M_ * m_ - 5) == 0:
        ns.append(N)
chk("o21", sum(ns), 20)

# g155: PA²+PB²=10 → a²+b²=4, (a-3)²+(b+4)²의 최댓값
vals = [(2 * math.cos(2 * math.pi * i / 7200) - 3) ** 2 + (2 * math.sin(2 * math.pi * i / 7200) + 4) ** 2 for i in range(7200)]
chk("g155", int(round(max(vals))), 49)
chk("g155", (sqrt(3 ** 2 + 4 ** 2) + 2) ** 2, 49)

# ================================================================ 원과 직선의 위치 관계
# o07: 직선 y=m(x+3)+1이 원 x²+y²=2와 만나지 않고 x²+y²=8과 만남, m>0
ok = [M0 for M0 in [Q(i, 1000) for i in range(1, 3000)]
      if dist((0, 0), (M0, -1, 3 * M0 + 1)) > sqrt(2) and dist((0, 0), (M0, -1, 3 * M0 + 1)) <= 2 * sqrt(2)]
lo_ = [v for v in solve((3 * m + 1) ** 2 - 2 * (m ** 2 + 1), m) if v > 0][0]    # 경계(열림)
hi_ = [v for v in solve((3 * m + 1) ** 2 - 8 * (m ** 2 + 1), m) if v > 0][0]    # 경계(닫힘)
assert min(ok) > lo_ and min(ok) - lo_ < Q(2, 1000) and max(ok) == hi_
chk("o07", hi_ / lo_, 7)

chk("n1748", max(A1 for A1 in range(-30, 31) if dist((1, A1), (4, -3, 5 * A1 - 2)) <= 3)
    - min(A1 for A1 in range(-30, 31) if dist((1, A1), (4, -3, 5 * A1 - 2)) <= 3), 14)


def f_o17(M0):
    d = dist((5, 5), (4, -M0, 0))
    return 2 if d < sqrt(5) else (1 if simplify(d - sqrt(5)) == 0 else 0)


acc, nmin = 0, None
for N in range(1, 30):
    acc += f_o17(N)
    if acc == 12 and nmin is None:
        nmin = N
chk("o17", nmin, 8)

# 2023년 11월 고1 16번: 선분 CD(C(2t, 0), D(0, t)) 위에 ∠APB=90° → 원 (x-3)²+(y-4)²=4와 선분 CD가 만남
def meets(T):
    P_, Q_ = (2 * T, 0.0), (0.0, T)
    best = 1e9
    for i in range(2001):
        s = i / 2000
        X0, Y0 = P_[0] * (1 - s) + Q_[0] * s, P_[1] * (1 - s) + Q_[1] * s
        best = min(best, abs(math.hypot(X0 - 3, Y0 - 4) - 2))
    return best < 2e-3


Ts = [T / 1000 for T in range(1, 12000) if meets(T / 1000)]
assert abs(max(Ts) - min(Ts) - float(2 * sqrt(5))) < 0.01
tv = solve(Abs(3 + 8 - 2 * t) / sqrt(5) - 2, t)           # 직선 x+2y=2t가 원에 접할 때(접점이 제1사분면에 있음은 위 탐색으로 확인)
chk("m2311", max(tv) - min(tv), 2 * sqrt(5))

# n1715v: 두 원 (x+3)²+y²=9, (x-1)²+y²=1과 직선 x+√3y-n=0의 교점이 0보다 큰 짝수 개인 정수 n
def npts(N):
    s = set()
    for cx, R0 in ((-3, 3), (1, 1)):
        for p in solve([(x - cx) ** 2 + y ** 2 - R0 ** 2, x + sqrt(3) * y - N], [x, y]):
            s.add((nsimplify(p[0]), nsimplify(p[1])))
    return len(s)


chk("n1715v", len([N for N in range(-20, 21) if npts(N) > 0 and npts(N) % 2 == 0]), 10)

# ================================================================ 현의 길이
chk("f3-12", 2 * sqrt(49 - dist((4, 3), (1, 0, -1)) ** 2), 4 * sqrt(10))

K = [K0 for K0 in solve(Q(1, 2) * 2 * sqrt(9 + k ** 2 - 9) * 3 - 15, k) if K0 > 0]
d0 = dist((4, K[0]), (3, -4, 4 * K[0] + 3))
chk("f9-13", K[0] if d0 == 3 else -1, 5)

mm = solve(Abs(-2 * m) / sqrt(m ** 2 + 1) - sqrt(9 - Q(81, 16)), m)
chk("n1809", mm[0] ** 2, 63)

# f2-19v: 직선 k(x-5)-(y-1)=0과 원 (x-2)²+(y-5)²=169, 현 AB의 최솟값과 그때의 k
best = None
for i in range(-4000, 4001):
    K0 = i / 400
    L = (K0, -1, -5 * K0 + 1)
    d = float(dist((2, 5), L))
    ln = 2 * math.sqrt(169 - d * d)
    if best is None or ln < best[0]:
        best = (ln, K0)
chk("f2-19v", int(round(best[0] * best[1])), 18)
chk("f2-19v", 2 * sqrt(169 - 25) * Q(3, 4), 18)

# ================================================================ 원 위의 점과 직선 사이의 거리
chk("m2209a", dist((3, 2), (2, -1, 8)) - sqrt(5), 7 * sqrt(5) / 5)

chk("f7-11", Q(1, 2) * sqrt(20) * (dist((2, 0), (1, -2, 7)) + sqrt(5)), 14)

# n1648: 호 AB 위 제3사분면 P, 삼각형 PAB 넓이 최대 (수치)
A1, B1 = (-math.sqrt(2), 2 * math.sqrt(2)), (2 * math.sqrt(2), math.sqrt(2))
best = 0
for i in range(36000):
    T = 2 * math.pi * i / 36000
    X0, Y0 = math.sqrt(10) * math.cos(T), math.sqrt(10) * math.sin(T)
    if X0 < 0 and Y0 < 0:
        best = max(best, abs((B1[0] - A1[0]) * (Y0 - A1[1]) - (B1[1] - A1[1]) * (X0 - A1[0])) / 2)
assert abs(best - float(5 * sqrt(2) + 5)) < 1e-6
chk("n1648", Q(1, 2) * sqrt(20) * (sqrt(10) + dist((0, 0), (1, 3, -5 * sqrt(2)))), 5 * sqrt(2) + 5)

# n1836: 점 (3, 4)를 지나고 원점과의 거리가 최대인 직선 3x+4y-25=0, 원 (x-8)²+(y-4)²=9 위의 점까지 거리가 자연수
cnt = 0
d = dist((8, 4), (3, 4, -25))           # 3
lo, hi = d - 3, d + 3                    # 0, 6
for N in range(1, 10):
    if lo < N < hi:
        cnt += 2
    elif N == lo or N == hi:
        cnt += 1
chk("n1836", cnt, 11)

# n1706: 삼각형 PAB 넓이가 자연수인 P의 개수 (A(-1, 0), B(1, 2), 원 (x+2)²+(y-4)²=2)
d = dist((-2, 4), (1, -1, 1))
lo, hi = Q(1, 2) * 2 * sqrt(2) * (d - sqrt(2)), Q(1, 2) * 2 * sqrt(2) * (d + sqrt(2))
cnt = sum(2 if lo < N < hi else (1 if N in (lo, hi) else 0) for N in range(1, 30))
chk("n1706", cnt, 8)

# ================================================================ 원의 접선
L1 = (3, 4, -25)
cc, rr = circ(x ** 2 + y ** 2 - 2 * x + 14 * y + k)
chk("f1-9", solve(dist(cc, L1) ** 2 - rr, k)[0], -50)

# f2-15: l1: y=3x+10 (제4사분면 지나지 않음), l2: x+3y=10
P_ = solve([y - 3 * x - 10, x + 3 * y - 10], [x, y])
chk("f2-15", area((-Q(10, 3), 0), (10, 0), (P_[x], P_[y])), Q(80, 3))

aa = []
for kk in (5, -5):                                  # 기울기 2인 접선 y=2x±5
    aa += solve(discriminant(x ** 2 + a * x + 1 - 2 * x - kk, x), a)
chk("o08", sum(aa), 4)

# 2024년 3월 고2 19번: A(0, 6), B(9, 0), P(6, 2), 원 x²+y²-2ax-2by=0이 직선 AB와 P에서만 만남
s_ = solve([36 + 4 - 12 * a - 4 * b, 3 * (a - 6) - 2 * (b - 2)], [a, b])   # 중심-P ⊥ AB(방향 (3, -2))
chk("m2403", s_[a] + s_[b], Q(22, 9))

# n1710: x²+y²=9, A(-3, 0), 2AH=HB
pa = [p for p in solve([x ** 2 + y ** 2 - 9, 2 * (x + 3) - (9 / x - x)], [x, y]) if p[0] > 0 and p[1] > 0][0]
chk("n1710", Q(1, 2) * (9 / pa[0] + 3) * pa[1], 12 * sqrt(2))

# 2024년 10월 고1 19번: y=-x²+6x 위 A, B, AB를 지름으로 하는 원 넓이 8π, A에서 기울기 1인 접선
best = None
for kk in [Q(i, 4) for i in range(1, 60)]:
    xs = solve(x ** 2 - 7 * x + kk, x)               # 직선 AB: y=-x+k (기울기 -1)
    if len(xs) == 2 and all(v.is_real for v in xs):
        d = sqrt(2) * Abs(xs[1] - xs[0])
        if simplify(d - 4 * sqrt(2)) == 0:
            best = kk
chk("m2410b", best, Q(33, 4))

# ================================================================ 원 밖의 점에서 그은 접선
# 두 접선이 수직 → 중심과 그 점 사이 거리 = 반지름 × √2
chk("n1579", [A1 for A1 in solve((a - 2) ** 2 - 16, a) if A1 > 0][0], 6)

ms = solve((2 * m + 3) ** 2 - 4 * (m ** 2 + 1), m)    # 기울기 접선 하나 + x=-1
xb = solve(ms[0] * (x + 1) + 5, x)[0]
chk("n1644", xb - (-1), 12)

ms = solve((2 * m - 4) ** 2 - 2 * (m ** 2 + 1), m)
ys = [-2 * M0 + 4 for M0 in ms]
chk("n1665", Q(1, 2) * Abs(ys[0] - ys[1]) * 2, 12)

ms = solve((-7 * t - 2) ** 2 - 9 * (t ** 2 + 1), t)
chk("f3-16", sum(ms), -Q(7, 10))

ms = solve((3 * m + 4) ** 2 - 5 * (m ** 2 + 1), m)     # 점 (-3, 4)에서 x²+y²=5에 그은 접선
ys = [M0 * (1 + 3) + 4 for M0 in ms]
chk("f4-11", Q(1, 2) * Abs(ys[0] - ys[1]) * 4, 40)

chk("n1774", Q(10, 1) / 5, 2)                            # (OA²)/OC: 직각삼각형 OAC에서 OM = OA²/OC
# 다시 확인: 접점 A, B 좌표를 구해 직선 AB와 원점 사이 거리
T_ = solve([x ** 2 + y ** 2 - 10, 3 * x + 4 * y - 10], [x, y])
chk("n1774", Line(Point(*T_[0]), Point(*T_[1])).distance(Point(0, 0)), 2)

# ================================================================ 고난도
# 2024년 10월 고1 26번: 두 직선 y=2x+6, y=-2x+6에 접하고 (2, 0)을 지나는 원 → 중심은 y축 위 또는 y=6 위
cents = []
cy = symbols("cy", real=True)
for v in solve((cy - 6) ** 2 / 5 - (4 + cy ** 2), cy):      # 중심 (0, cy)
    cents.append((0, v))
cx_ = symbols("cx", real=True)
for v in solve((2 * cx_) ** 2 / 5 - ((cx_ - 2) ** 2 + 36), cx_):   # 중심 (cx, 6)
    if v.is_real:
        cents.append((v, 6))
chk("m2410c", sqrt((cents[0][0] - cents[1][0]) ** 2 + (cents[0][1] - cents[1][1]) ** 2) if len(cents) == 2 else -1, 5)

# 2024년 10월 고1 15번: A(a, b), B(b, a) on x²+y²=4, 사각형 APBQ 넓이 2√2 → |AB|=√2
sol = solve([a ** 2 + b ** 2 - 4, 2 * (a - b) ** 2 - 2], [a, b])
chk("m2410a", sol[0][0] * sol[0][1], Q(3, 2))

# 2026년 3월 고2 17번: 원 (x-3)²+(y-3)²=9, y=mx, OH:BH=√3:1
best = None
for M0 in solve(9 * (m - 1) ** 2 / (m ** 2 + 1) - Q(9, 2), m):
    if 0 < M0 < 1:
        best = M0
chk("m2603", best, 2 - sqrt(3))

# 2023년 9월 고1 20번 (ㄱㄴㄷ)
P_ = lambda M, N: (0, Q(4 * M, M + N))
Q_ = lambda M, N: (Q(4 * M, M + N), 4)
R_ = lambda M, N: (4, Q(4 * N, M + N))
s_ = Point(0, 2) == Point(*P_(1, 1))
ok2 = True
for M0, N0 in ((1, 2), (2, 3), (3, 1), (1, 5)):
    C_ = Circle(Point(*P_(M0, N0)), Point(*Q_(M0, N0)), Point(*R_(M0, N0)))
    ok2 = ok2 and C_.encloses_point(Point(Q(4 * M0, M0 + N0), 0)) is False and simplify(
        C_.center.distance(Point(Q(4 * M0, M0 + N0), 0)) - C_.radius) == 0
# ㄷ: x축과 만나는 두 점 사이 거리 3일 때 PQ
s3 = symbols("s3", positive=True)                         # s3 = 4m/(m+n), 0<s3<4
P3, Q3, R3 = Point(0, s3), Point(s3, 4), Point(4, 4 - s3)
C3 = Circle(P3, Q3, R3)
xs = solve((x - C3.center.x) ** 2 + C3.center.y ** 2 - C3.radius ** 2, x)
cand = [v for v in solve(Abs(xs[1] - xs[0]) - 3, s3) if 0 < v < 4]
ok3 = all(simplify(P3.subs(s3, v).distance(Q3.subs(s3, v)) - 5 * sqrt(2) / 2) == 0 for v in cand) and len(cand) > 0
chk("m2309c", mark((s_, ok2, ok3)), "⑤")

# 2022년 9월 고1 28번: 중심 (c, 2), 삼각형 ROP 넓이 c³/4 = 16 → c = 4, m = tan 2θ (tan θ = 2/c)
cc = [v for v in solve(c ** 3 / 4 - 16, c) if v.is_real][0]
tn = 2 / cc
chk("m2209b", 60 * (2 * tn / (1 - tn ** 2)), 80)
# 직접 확인: 원 (x-4)²+(y-2)²=4와 y=4x/3 접함, P(4, 0), Q, R
assert simplify(dist((4, 2), (4, -3, 0)) - 2) == 0
Qp = Line(Point(0, 0), Point(3, 4)).projection(Point(4, 2))
Rp = Line(Point(4, 0), Qp).intersection(Line(Point(0, 0), Point(0, 1)))[0]
assert simplify(area((0, 0), (4, 0), (Rp.x, Rp.y)) - 16) == 0

# 2022년 3월 고2 19번
L1_, L2_ = Line(Point(-1, 0), Point(0, -2)), Line(Point(4, 0), Point(0, -2))
A_ = L1_.intersection(L2_)[0]
B_, C_ = Point(-1, 0), Point(4, 0)
g1 = simplify(L1_.slope * L2_.slope + 1) == 0
circ_ = Circle(A_, B_, C_)
# Q = (P+B+C)/3, 넓이 PBC = 3 × 넓이 ABC → P의 y좌표 = 3 × |A의 y| = 6, Q의 y = 2
Qs = [p for p in circ_.intersection(Line(Point(0, 2), Point(1, 2))) if p.y > 0]
cands = []
for Qq in Qs:
    Pp = Point(3 * Qq.x - B_.x - C_.x, 3 * Qq.y)
    if Pp.x > 0 and Pp.y > 0:
        cands.append(Pp)
g2 = len(cands) == 1 and simplify((cands[0].y + 0) / 3 - 2) == 0
g3 = len(cands) == 1 and simplify(cands[0].x + cands[0].y - 10) == 0
chk("m2203", mark2((g1, g2, g3)), "③")

# n1604: 중심이 제2사분면, x=0, 3x+4y=0에서 현의 길이 4, A(1, 3) 지남
tot = 0
for sgn in (1, -1):
    # 두 직선까지의 거리가 같음: |x| = |3x+4y|/5
    for cxv in solve((x - 1) ** 2 + ((-2 * x if sgn == 1 else x / 2) - 3) ** 2 - (x ** 2 + 4), x):
        cyv = -2 * cxv if sgn == 1 else cxv / 2
        if cxv < 0 and cyv > 0:
            tot += (cxv ** 2 + 4)
chk("n1604", (lambda v: v.q + v.p)(nsimplify(tot)), 49)

# 2020년 9월 고1 27번: 직선 y=x-2 방향으로의 정사영 (중심 사이 거리 4√2, 반지름 2, 1)
u = (1 / sqrt(2), 1 / sqrt(2))
s1 = -6 * u[0]
s2 = 5 * u[0] - 3 * u[1]
chk("m2009", (Abs(s2 - s1) + 3) * (Abs(s2 - s1) - 3), 23)

# 2024년 3월 고2 21번: 수치 구성(m=2, Q(8, 4), P(4, 8), A(20/3, 20/3), B=l1∩AQ)
M0 = 2
Pq = Point(4, 8)
Qq = Point(8, 4)
Ap = Point(Q(20, 3), Q(20, 3))
assert simplify(Line(Point(0, 0), Point(1, M0)).distance(Ap) - Ap.distance(Pq)) == 0
assert simplify(Line(Point(0, 0), Point(M0, 1)).distance(Ap) - Ap.distance(Qq)) == 0
Rr = Line(Pq, Qq).intersection(Line(Point(0, 0), Point(1, 0)))[0]
assert Pq.distance(Qq) == Qq.distance(Rr) and area((0, 0), (4, 8), (8, 4)) == 24
Bb = Line(Point(0, 0), Point(1, M0)).intersection(Line(Ap, Qq))[0]
chk("m2421", Bb.distance(Qq), 3 * sqrt(5))
# 조건만으로 m이 하나로 정해지는지: 대칭인 접점 P, Q(직선 y=x 대칭), PQ=QR이면 Q=(2k, k) 꼴이 아니어도 확인
for M1 in (Q(3, 2), 3, 4):
    qx = symbols("qx", positive=True)
    Qa = Point(qx, qx / M1)
    Pa = Point(qx / M1, qx)
    Ra = Line(Pa, Qa).intersection(Line(Point(0, 0), Point(1, 0)))[0]
    assert simplify(Pa.distance(Qa) - Qa.distance(Ra)) != 0

# n1773: (x+2)²+(y-4)²=10, 원점에서 그은 접선 y=3x, y=-x/3, 직선 y=mx+10, 이등변삼각형 OAB
ms = solve((-2 * m - 4) ** 2 - 10 * (m ** 2 + 1), m)
assert set(ms) == {3, -Q(1, 3)}
# 두 접선이 수직이므로 직각이등변삼각형 → OA = OB, 직선 l은 각의 이등분선에 수직
best = []
for mm_ in [Q(i, 100) for i in range(1, 1000)]:
    A1 = solve([y - 3 * x, y - mm_ * x - 10], [x, y])
    B1 = solve([y + x / 3, y - mm_ * x - 10], [x, y])
    if not A1 or not B1:
        continue
    OA = sqrt(A1[x] ** 2 + A1[y] ** 2)
    OB = sqrt(B1[x] ** 2 + B1[y] ** 2)
    if simplify(OA - OB) == 0:
        best.append(area((0, 0), (A1[x], A1[y]), (B1[x], B1[y])))
chk("n1773", best[0] if best else -1, 80)

# 2021년 9월 고1 19번: P(-1, -3), Q(a, a-2), R(b, b-2), 넓이 3√2, 넓이비 1:4
d0 = dist((0, 0), (1, -1, -2))                           # 원점과 직선 y=x-2 사이 거리 √2
PR = 2 * 3 * sqrt(2) / d0                                 # 6
bb = -1 + PR / sqrt(2)
# PQ : QR = 1 : 2
aa_ = -1 + (bb + 1) / 3
chk("m2109", aa_ + bb, 4 * sqrt(2) - 2)

# 2025년 3월 고2 28번: |OA| = r + 2, P2Q2 = (1+r) P1Q1 = 4 P1Q1 → r = 3
rr = 3
OA = rr + 2
th0 = math.asin(rr / OA)
mval = math.tan(math.pi / 4 - th0)
fr = nsimplify(mval, tolerance=1e-12)
assert fr == Q(1, 7)
chk("m2503b", fr.p + fr.q, 8)
# 넓이 4배 직접 확인 (수치)
Ax = OA / math.sqrt(2)
P1 = (Ax - rr / math.sqrt(2),) * 2
P2 = (Ax + rr / math.sqrt(2),) * 2


def meet_tangent(Pp):
    # 점 Pp에서의 접선(방향 (1, -1))과 y = mval x의 교점
    s = (Pp[1] - mval * Pp[0]) / (mval + 1)
    return (Pp[0] + s, Pp[1] - s)


Q1, Q2 = meet_tangent(P1), meet_tangent(P2)
ar = lambda U, V, W: abs((V[0] - U[0]) * (W[1] - U[1]) - (V[1] - U[1]) * (W[0] - U[0])) / 2
assert abs(ar((Ax, Ax), Q2, P2) - 4 * ar((Ax, Ax), P1, Q1)) < 1e-9

# 2023년 9월 고1 29번: B+C = (2, 4), |B| = |C| = √26
Mx, My = 1, 2
half = sqrt(26 - (Mx ** 2 + My ** 2))
h = dist((-5, -1), (1, 2, -5))
ar_ = Q(1, 2) * 2 * half * h
fr = nsimplify(ar_ / sqrt(105))
chk("m2309d", fr.p + fr.q, 17)

# 2022년 9월 고1 29번: A1(3, √91), A2(7, √51), B(-10, 0), C1·C2는 지름의 반대쪽 끝
A1 = Point(3, sqrt(91))
A2 = Point(7, sqrt(51))
Bp = Point(-10, 0)
cir = Circle(Point(0, 0), 10)
C1 = [p for p in cir.intersection(Line(Bp, Bp + Point(-(A1.y - Bp.y), A1.x - Bp.x))) if p != Bp][0]
C2 = [p for p in cir.intersection(Line(Bp, Bp + Point(-(A2.y - Bp.y), A2.x - Bp.x))) if p != Bp][0]
chk("m2209c", C1.y ** 2 + C2.x ** 2, 140)

# 2024년 9월 고1 30번: f(x) = a(x-b)²; 원의 중심은 두 각의 이등분선 y=x/2, y=-2x 위
found = []
for A0 in [Q(i, 8) for i in range(-40, 41) if i != 0]:
    for B0 in [Q(j, 4) for j in range(-40, 41)]:
        f = A0 * (x - B0) ** 2
        xs = set()
        for line in (x / 2, -2 * x):
            for v in solve(f - line, x):
                if v.is_real:
                    xs.add(v)
        xs = [v for v in xs if v != 0] + ([0] if 0 in xs else [])
        if len(set(xs)) != 3:
            continue
        x1, x2, x3 = xs
        if x1 * x2 * x3 > 0 and simplify((f.subs(x, x1) + f.subs(x, x2) + f.subs(x, x3)) / 3 + Q(7, 3)) == 0:
            found.append(f.subs(x, 4) * f.subs(x, 6))
chk("m2409c", found[0] if len(set(found)) == 1 else -1, 144)

if __name__ == "__main__":
    bad = [r_ for r_ in R if not r_[1]]
    for r_ in bad:
        print("MISMATCH", r_)
    print("검산", len(R), "불일치", len(bad))
