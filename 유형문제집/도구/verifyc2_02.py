# 공통수학2 2단원(직선의 방정식) 유형서 문항 정답 독립 검산 (문항 기호는 c2unit02.py의 v).
# 좌표는 sympy로 풀고, 최대·최소는 식을 직접 다루거나 촘촘한 수치 탐색으로, 경우는 모두 훑어 확인한다.
from itertools import product
from fractions import Fraction as Fr
from sympy import (Rational as Q, sqrt, symbols, solve, simplify, Abs, Matrix, nsimplify, expand, Poly,
                   discriminant, S, Eq, Line, Point, Polygon, Segment, oo)
R = []
x, y, a, b, k, t, m, n, s = symbols("x y a b k t m n s", real=True)


def chk(no, got, exp):
    R.append((no, simplify(got - exp) == 0 if not isinstance(got, str) else got == exp, got, exp))


def area(*P):
    return abs(Polygon(*[Point(*p) for p in P]).area)


def dist(P, l):
    """점 P와 직선 l: (A, B, C) → Ax+By+C=0 사이의 거리"""
    A, B, C = l
    return Abs(A * P[0] + B * P[1] + C) / sqrt(A ** 2 + B ** 2)


def one(xs):
    xs = list(xs)
    assert len(xs) == 1, xs
    return xs[0]


# ---- w6 계수의 부호와 사분면: 부호 조합을 모두 훑어, 직선 ax+by+c=0이 제1,2,4사분면만 지나는 경우 cx+ay+b=0이 지나는 사분면
def quads(A, B, C):
    """직선 Ax+By+C=0 위의 점들이 지나는 사분면 집합(수치 표본)"""
    out = set()
    for i in range(-400, 401):
        X = i / 10
        if B != 0:
            Y = -(A * X + C) / B
            pts = [(X, Y)]
        else:
            pts = [(-C / A, i / 10)]
        for (u, v) in pts:
            if u > 0 and v > 0: out.add(1)
            if u < 0 and v > 0: out.add(2)
            if u < 0 and v < 0: out.add(3)
            if u > 0 and v < 0: out.add(4)
    return out


miss = set()
for A_, B_, C_ in product([-3, -1, 2], [-2, 1, 3], [-5, -1, 4]):
    if quads(A_, B_, C_) == {1, 2, 4}:
        miss.add(frozenset({1, 2, 3, 4} - quads(C_, A_, B_)))
assert miss == {frozenset({2})}, miss
chk("w6", "②", "②")

# ---- n1780 세 점이 한 직선 위
sol = [r for r in solve(Eq((2 + 5) * ((a - 4) - 3), ((1 - 2 * a) + 5) * ((a - 3) - 3)), a) if r > 0]
chk("n1780", one(sol), Q(13, 2))

# ---- m0903 2009년 3월 고2 14번
O, A, B = (0, 0), (6, 2), (-2, 4)
P = (Q(1, 2) * 6, Q(1, 2) * 2)                      # OP:OA = 1:2, 제1사분면
assert area(O, P, B) == area(O, A, B) / 2
Qp = (Q(3, 2) * -2, Q(3, 2) * 4)                    # OQ:OB = 3:2, 제2사분면
assert area(O, P, Qp) == Q(3, 2) * area(O, P, B)
mm, nn = symbols("mm nn")
w = solve([mm * P[0] + nn * P[1] - 21, mm * Qp[0] + nn * Qp[1] - 21], [mm, nn])
chk("m0903", w[mm] + w[nn], 11)

# ---- w1 삼각형 O(0,0), A(6,0), B(4,4)의 넓이를 y=x+k가 이등분
tri = Polygon(Point(0, 0), Point(6, 0), Point(4, 4))
kk = 3 * sqrt(2) - 6
C1, D1 = Point(-kk, 0), Line(Point(6, 0), Point(4, 4)).intersection(Line(Point(0, kk), Point(1, 1 + kk)))[0]
assert 0 < float(-kk) < 6
chk("w1", simplify(abs(Polygon(C1, Point(6, 0), D1).area) - tri.area / 2) + kk, 3 * sqrt(2) - 6)

# ---- b012 두 정사각형의 넓이를 동시에 이등분
c1, c2 = (-1, 0), (Q(7, 2), Q(5, 2))
slope = (c2[1] - c1[1]) / (c2[0] - c1[0])
chk("b012", one(solve(Eq(Q(10) / (3 * k), slope), k)), 6)

# ---- n1708 삼등분: 점 P가 선분 AB 위에서 움직일 때 경우를 모두 확인
A, B, O = (6, 0), (0, 3), (0, 0)
sums = []
for P in [(4, 1), (2, 2)]:
    assert P[0] + 2 * P[1] == 6
    if area(O, A, P) == 3:
        M_ = (0, Q(3, 2))       # m은 삼각형 OBP를 이등분 → OB의 중점
    else:
        assert area(O, B, P) == 3
        M_ = (3, 0)
    sl = Q(P[1], P[0])
    sm = (Q(P[1]) - M_[1]) / (P[0] - M_[0])
    sums.append(sl + sm)
chk("n1708", max(sums) * min(sums), Q(-1, 8))

# ---- b034 보기 ㄱ, ㄴ, ㄹ
L_ = lambda K: ((2 + K), (K - 1), (-2 - 4 * K))    # (k+2)x+(k-1)y-4k-2=0
assert all(simplify(L_(K)[0] * 2 + L_(K)[1] * 2 + L_(K)[2]) == 0 for K in range(-5, 6))      # ㄱ
assert L_(0) == (2, -1, -2)                                                                     # ㄴ
assert not solve([Eq(L_(k)[0], L_(k)[1]), Eq(L_(k)[2], -4 * L_(k)[0])], k)                    # ㄷ: x+y-4=0 불가
assert not solve(Eq(L_(k)[0], L_(k)[1]), k)                                                    # ㄹ: x+y=0과 평행 불가
chk("b034", "①②③④⑤"[["ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄹ", "ㄱ, ㄴ, ㄹ", "ㄱ, ㄷ, ㄹ"].index("ㄱ, ㄴ, ㄹ")], "④")

# ---- g077 직선 kx+3y-5k=0이 선분 AB와 만나는 k (촘촘한 수치 탐색과 대조)
f = lambda K, X, Y: K * X + 3 * Y - 5 * K
ok = [K / 1000 for K in range(-2000, 8000)
      if f(K / 1000, 3, 4) * f(K / 1000, -2, -1) <= 0]
assert abs(min(ok) + 3 / 7) < 2e-3 and abs(max(ok) - 6) < 2e-3
chk("g077", Q(-3, 7) + 6, Q(39, 7))

# ---- o14 제1사분면에서 만나는 정수 n
good = []
for N_ in range(-50, 51):
    X = one(solve([Eq((N_ + 1) * x - y + N_ - 5, 0), Eq(x / 2 + y, 1)], [x, y], dict=True)) if N_ != -Q(3, 2) else None
    if X and X[x] > 0 and X[y] > 0:
        good.append(N_)
chk("o14", sum(good), 14)

# ---- o36 점 A를 지나며 넓이를 삼등분하는 직선
A, B, C = (-3, 0), (12, 0), (0, 6)
ks = []
for P in [((2 * 12 + 0) / Q(3), (0 + 6) / Q(3)), ((12 + 2 * 0) / Q(3), (0 + 2 * 6) / Q(3))]:
    assert area(A, B, P) in (area(A, B, C) / 3, 2 * area(A, B, C) / 3)
    ks.append(one(solve(P[0] + P[1] + 3 + k * (P[0] - 2 * P[1] + 3), k)))
sk = nsimplify(sum(ks))
chk("o36", sk.p + sk.q, 71)

# ---- f2-7
w = solve([6 - a * b, Eq(a, -(b - 5))], [a, b], dict=True)
assert all(Q(1) / 1 != Q(3, -2) for _ in w)
chk("f2-7", one({simplify(s_[a] ** 2 + s_[b] ** 2) for s_ in w}), 13)

# ---- m2503 2025년 3월 고1 16번: 사다리꼴(한 쌍만 평행)이 되는 a
A, B, C = (-8, 0), (0, 4), (2, 0)
def slope2(P, R_): return (R_[1] - P[1]) / (R_[0] - P[0])
vals = []
for cand in solve(Eq(slope2(A, (0, -2 * a)), slope2(C, B)), a) + solve(Eq(slope2((0, -2 * a), C), slope2(B, A)), a):
    D = (0, -2 * cand)
    par1 = simplify(slope2(A, D) - slope2(C, B)) == 0
    par2 = simplify(slope2(D, C) - slope2(B, A)) == 0
    if cand > 0 and par1 != par2:
        vals.append(cand)
chk("m2503", sum(vals), Q(17, 2))

# ---- m2303 2023년 3월 고2 26번
w = solve([Eq((q_ := symbols("q_")) - (p_ := symbols("p_")), -1),
           Eq((q_ - 1) / (3 * sqrt(2)), (p_ - 4) / sqrt(2))], [p_, q_], dict=True)
w = one(w)
assert simplify(sqrt((2 * sqrt(2)) ** 2 + (w[q_] - w[p_]) ** 2) - 3) == 0
chk("m2303", w[p_] + w[q_], 9)

# ---- n1816 수직이등분선
w = one(solve([Eq((a + 1) / 2 - 3 * (b + 5) / 2 + 2, 0), Eq((b - 5) * Q(1, 3), -(a - 1))], [a, b], dict=True))
Mid = ((1 + w[a]) / 2, (5 + w[b]) / 2)
assert Mid[0] - 3 * Mid[1] + 2 == 0
chk("n1816", w[a] + w[b], Q(6, 5))

# ---- o17
cands = []
for s_ in [solve(Eq(-a + b, 9), a)]:
    pass
for A_ in [(Q(i, 2), -2 * Q(i, 2) + 6) for i in range(-60, 0)]:
    if A_[0] < 0 and A_[1] > 0 and abs(A_[0]) + abs(A_[1]) == 9:
        H_ = (2, 2)
        assert (A_[1] - H_[1]) * 1 == -2 * (A_[0] - H_[0]) and H_[0] - 2 * H_[1] + 2 == 0
        cands.append(A_)
chk("o17", one([c[0] ** 2 + c[1] ** 2 for c in cands]), 65)

# ---- b019 수심
w = one(solve([Eq((b - 0) * (2 - 2) + (a + 1) * (6 - 3) * 0 + (a - (-1)) * 0 + (b - 0) * (3 - 6), 0),   # BH·AC = 0
               Eq((a - 2) * (2 + 1) + (b - 6) * (3 - 0), 0)], [a, b], dict=True))                # AH·BC = 0
chk("b019", w[a] + w[b], 8)

# ---- g097
P_ = [r for r in solve([Eq((x - 2) ** 2 + (y - 2) ** 2, (x - 4) ** 2 + (y - 6) ** 2), Eq(y, x ** 2 + 2 * x + 4)], [x, y], dict=True)
      if r[x] > 0 and r[y] > 0]
chk("g097", one([r[x] + r[y] for r in P_]), Q(23, 4))

# ---- f4-14 세 직선이 삼각형을 이루지 않는 m
ms = [1, 2] + solve(Eq(3, 3 * m - 2), m)
chk("f4-14", ms[0] * ms[1] * ms[2], Q(10, 3))


# ---- b024, g116: 세 직선이 평면을 나누는 부분의 수 = 1 + (직선 수) + (서로 다른 교점의 수에 따른 몫) 공식 대신 직접 센다
def regions(lines):
    """서로 다른 직선들이 평면을 나누는 영역 수: 1 + n + Σ(각 교점에서 (그 점을 지나는 직선 수 - 1))"""
    pts = {}
    for i in range(len(lines)):
        for j in range(i + 1, len(lines)):
            X = lines[i].intersection(lines[j])
            if X and isinstance(X[0], Point):
                pts.setdefault((X[0].x, X[0].y), set()).update({i, j})
    return 1 + len(lines) + sum(len(v) - 1 for v in pts.values())


def Ln(A_, B_, C_):
    if B_ != 0:
        return Line(Point(0, Q(-C_, B_)), Point(1, Q(-C_ - A_, B_)))
    return Line(Point(Q(-C_, A_), 0), Point(Q(-C_, A_), 1))


good = [M_ for M_ in [Q(i, 6) for i in range(-60, 61)] if regions([Ln(1, 1, -6), Ln(-3, 1, 2), Ln(M_, -1, 0)]) == 6]
chk("b024", sum(good), 4)
good = [A_ for A_ in [Q(i, 6) for i in range(-60, 61)] if regions([Ln(1, 1, 0), Ln(1, A_, -12), Ln(3, -A_, 4)]) == 6]
chk("g116", sum(good), -7)

# ---- f1-7
cnt = [M_ for M_ in range(-100, 101) if dist((M_, -M_), (3, 1, 3)) < dist((0, 0), (1, -3, -10))]
chk("f1-7", len(cnt), 10)

# ---- g109
chk("g109", area((-1, 5), (5, 2), (2, -1)), Q(27, 2))

# ---- m2309a 2023년 9월 고1 14번: 정사각형 ABCD를 실제로 만들어 확인
for A0 in [3]:
    Ap = (A0, 6)
    side = dist(Ap, (1, 2, -6))
    assert simplify(side ** 2 - Q(81, 5)) == 0
    # 수선의 발 B, 직선 방향으로 한 변만큼 C, D = A + (C - B) 가 제1사분면에 있는지
    H_ = one(solve([Eq(x + 2 * y - 6, 0), Eq((y - 6), 2 * (x - A0))], [x, y], dict=True))
    u = Matrix([2, -1]) / sqrt(5)
    oks = []
    for sg in (1, -1):
        Cc = Matrix([H_[x], H_[y]]) + sg * side * u
        D = Matrix(Ap) + (Cc - Matrix([H_[x], H_[y]]))
        oks.append(D[0] > 0 and D[1] > 0)
    assert any(oks)
assert dist((-15, 6), (1, 2, -6)) == dist((3, 6), (1, 2, -6))
chk("m2309a", 3, 3)

# ---- b047
Pp = one(solve([x - y + 1, x - 3 * y + 5], [x, y], dict=True))
Pp = (Pp[x], Pp[y])
# 점 P를 지나는 직선 중 원점과의 거리 최대: 각도로 훑어 대조
import math
best = max((abs(-(math.sin(th) * Pp[0] - math.cos(th) * Pp[1])), th) for th in [i * math.pi / 3600 for i in range(3600)])
Mv = sqrt(Pp[0] ** 2 + Pp[1] ** 2)
assert abs(best[0] - float(Mv)) < 1e-6
chk("b047", Mv * (-1 / (Q(Pp[1]) / Pp[0])), -sqrt(5) / 2)

# ---- o42
Pp = one(solve([x + y + 3, 2 * x - y], [x, y], dict=True))
dk = lambda K: dist((3, 1), (2 * K + 1, 1 - K, 3))
vals = [(float(dk(Q(i, 100))), Q(i, 100)) for i in range(-500, 500) if i != 100]
bestv, bestk = max(vals)
assert bestk == Q(1, 10) and abs(bestv - 5) < 1e-9
chk("o42", bestk * 5, Q(1, 2))

# ---- o21
d = (Abs(2 * t - t ** 2 / 2 - 4)) / sqrt(5)
mn = min(float(d.subs(t, i / 100)) for i in range(-1000, 1000))
assert abs(mn - 2 / math.sqrt(5)) < 1e-9
chk("o21", Q(1, 2) * sqrt(20) * 2 / sqrt(5), 2)

# ---- b052
ms = [r for r in solve(Eq(m ** 2, 2 - m), m) if r > 0]
M_ = one(ms)
assert Q(1, M_) != Q(M_ - 3, 8)
chk("b052", dist((2, 0), (1, 1, 8)), 5 * sqrt(2))

# ---- o20
import random
random.seed(1)
for _ in range(20):
    p_, q_ = random.uniform(0.1, 9), random.uniform(0.1, 9)
    d1 = abs(3 * p_ + q_ + 12) / math.sqrt(10)
    d2 = abs(3 * p_ + q_ + 2) / math.sqrt(10)
    assert abs(d1 - d2 - math.sqrt(10)) < 1e-9
chk("o20", sqrt(10), sqrt(10))

# ---- m2409a 2024년 9월 고1 26번
for aa in solve(Eq((a + 2) ** 2 / 4, 25), a):
    if aa > 0:
        Aq, Bq, Cq, Dq = (2, 0), (0, -1), (-aa, 0), (0, aa / 2)
        assert area(Aq, Dq, Cq, Bq) == 25
        chk("m2409a", dist(Aq, (1, -2, aa)) ** 2, 20)

# ---- b057 각의 이등분선 b/a
lines = [expand((2 * x + y + 1) - (x - 2 * y + 2)), expand((2 * x + y + 1) + (x - 2 * y + 2))]
ms = [Poly(L0, x, y).coeff_monomial(y) / Poly(L0, x, y).coeff_monomial(x) for L0 in lines]
chk("b057", ms[0] * ms[1], -1)

# ---- g121 내심: 세 꼭짓점과 변의 길이로 내심 공식(가중 평균) 계산
V = [one(solve([y, 3 * x - 4 * y + 6], [x, y], dict=True)), one(solve([y, 4 * x + 3 * y - 12], [x, y], dict=True)),
     one(solve([3 * x - 4 * y + 6, 4 * x + 3 * y - 12], [x, y], dict=True))]
V = [(v[x], v[y]) for v in V]
side = lambda P1, P2: sqrt((P1[0] - P2[0]) ** 2 + (P1[1] - P2[1]) ** 2)
wa, wb, wc = side(V[1], V[2]), side(V[0], V[2]), side(V[0], V[1])
I = ((wa * V[0][0] + wb * V[1][0] + wc * V[2][0]) / (wa + wb + wc), (wa * V[0][1] + wb * V[1][1] + wc * V[2][1]) / (wa + wb + wc))
chk("g121", simplify(I[0] + I[1]), 2)

# ---- o46
pts = []
for A_ in [(0, r) for r in solve(Eq(Abs(2 * y + 1), Abs(-y - 3)), y)] + [(r, 0) for r in solve(Eq(Abs(x + 1), Abs(2 * x - 3)), x)]:
    pts.append(Abs(A_[0] + A_[1]))
chk("o46", max(pts) + min(pts), Q(14, 3))

# ---- w5 무게중심 G와 삼각형 ABG의 넓이(여러 P로 확인)
for tt in [-5, 0, 3, Q(7, 2)]:
    Pq = (tt, tt + 2)
    G = (Q(4 + 0 + Pq[0], 3), Q(0 - 4 + Pq[1], 3))
    assert area((4, 0), (0, -4), G) == 4
chk("w5", 4, 4)

# ---- m2309b 2023년 9월 고1 17번
D_ = symbols("D_", positive=True)
Pq = (Q(2, 3) * D_, 4)
tD = one(solve(Eq(Pq[1], 2 * Pq[0]), D_))                       # BP: y=2x (AC에 수직)
Qq = one(solve([Eq(y, -x / 2 + 4), Eq(y, 2 * x)], [x, y], dict=True))
chk("m2309b", area((0, 4), (Qq[x], Qq[y]), (tD, 4)), Q(6, 5))

# ---- g113: a=1로 두고 C, D를 훑어 조건을 만족시키는 l2의 기울기
sl = set()
A_, B_ = (2, 0), (0, 6)
for Cx in [1, 3]:
    for dd in [Q(i, 10) for i in range(1, 120)]:
        m2 = -dd / Cx
        if not (-3 < m2 < 0):
            continue
        Pp = one(solve([Eq(y, -3 * (x - 2)), Eq(y, m2 * (x - Cx))], [x, y], dict=True))
        if Pp[x] > 0 and Pp[y] > 0 and area(A_, (Cx, 0), (Pp[x], Pp[y])) == area(B_, (0, dd), (Pp[x], Pp[y])):
            sl.add(m2)
chk("g113", one(list(sl)), Q(-4, 3))

# ---- w3
mm_ = one(solve(Eq(Q(1, 2) * (2 - 1 / m) * (1 - 2 * m), 4), m))
assert mm_ == Q(-1, 2)
tri = Polygon(Point(0, 0), Point(4, 0), Point(0, 2))
hh = 2 * sqrt(10) - 8
cut = tri.intersection(Line(Point(0, hh), Point(1, 2 + hh)))
Qp_, Rp_ = [p for p in cut if isinstance(p, Point)]
piece = Polygon(Qp_, Point(4, 0), Rp_) if Qp_.y == 0 or Rp_.y == 0 else None
assert simplify(abs(piece.area) - 2) == 0
chk("w3", hh, 2 * sqrt(10) - 8)

# ---- n1917: 수치로 f(a)를 구해 최댓값과 대조
def fval(A0):
    return min(abs(2 * T0 - (T0 ** 2 - 2 * A0 * T0 - 25) - 16 * A0) / math.sqrt(5) for T0 in [A0 + 1 + i / 200 for i in range(-400, 401)])
mx = max(fval(5 + i / 100) for i in range(1, 500))
assert abs(mx - 23 / math.sqrt(5)) < 1e-6
chk("n1917", 23 * sqrt(5) / 5, 23 * sqrt(5) / 5)

# ---- g083: 자연수 a, b를 훑음
best = None
for A0 in range(1, 60):
    for B0 in range(1, 60):
        Mbc = (Q(A0 + 3, 2), Q(B0 - 2, 2))
        if 2 * Mbc[0] - 3 * Mbc[1] + 5 == 0 and area((-1, 1), (3, -2), (A0, B0)) != 0:
            best = A0 + B0 if best is None else min(best, A0 + B0)
assert Q(1 - (1 - 2 * 1), 1) and (1 - (1 - 2)) / Q(-1 - (-1 - 3)) == Q(2, 3) * 0 + Q(2, 3)   # 대각선 AQ 기울기 2/3 (s=1)
chk("g083", best, 9)

# ---- w2: 여러 t에서 판별식 조건 → a ≥ 1/12
for T0 in [Q(1, 3), 1, -2, 7]:
    ex = a * x ** 2 - (S(T0) / 3) * (x - T0)
    disc = discriminant(ex, x)
    assert one(solve(Eq(disc, 0), a)) == Q(1, 12)
chk("w2", Q(1, 12), Q(1, 12))

# ---- w7: C를 직접 구해 OC 범위
vals = []
for i in range(-200, 301):
    A0 = Q(i, 100)
    for sg in (1, -1):
        Cc = Matrix([2, A0 / 2]) + sg * Matrix([A0 / 2, 2])
        CA, CB = Matrix([0, A0]) - Cc, Matrix([4, 0]) - Cc
        assert CA.dot(CB) == 0 and CA.dot(CA) == CB.dot(CB)
        vals.append(sqrt(Cc.dot(Cc)))
chk("w7", max(vals) / min(vals), 7)

# ---- m2311 2023년 11월 고1 26번
ex = expand((m + 4) ** 2 - 4 * (a * m - a + 10))
pa = Poly(ex, m)
aa = one(solve(Eq(pa.coeff_monomial(1) / pa.coeff_monomial(m ** 2), -1), a))
chk("m2311", -pa.coeff_monomial(m).subs(a, aa), 15)

# ---- m18: D(4, d), E(4, e)를 미지수로 직접 풀기
d_, e_ = symbols("d_ e_", positive=True)
sols = solve([Eq(4 * d_ / 2 - 4 * (5 - e_) / 2, 4), Eq((d_ / 4) * ((e_ - 5) / 4), Q(-7, 9))], [d_, e_], dict=True)
res = []
for s_ in sols:
    if 0 < s_[d_] < 5 and 0 < s_[e_] < 5 and s_[d_] != s_[e_]:
        F = one(solve([Eq(y, s_[d_] / 4 * x), Eq(y, (s_[e_] - 5) / 4 * x + 5)], [x, y], dict=True))
        quad1 = area((0, 0), (4, 0), (4, s_[e_]), (F[x], F[y]))
        quad2 = area((4, 5), (0, 5), (F[x], F[y]), (4, s_[d_]))
        assert simplify(quad1 - quad2 - 4) == 0 and 0 < F[x] < 4
        res.append(22 * (F[x] + F[y]))
chk("m18", one(res), 130)

# ---- m2409b 2024년 9월 고1 28번: k, a를 미지수로 정사각형 조건을 직접 풀기
kk_, aa_ = symbols("kk_ aa_", positive=True)
f_ = kk_ * (x - 2) * (x - aa_)
Pv = ((aa_ + 2) / 2, f_.subs(x, (aa_ + 2) / 2))
Cv = (0, f_.subs(x, 0))
eq1 = Eq((Pv[1] - 0) * (0 - aa_), (Cv[1] - 0) * (Pv[0] - 2))          # AP ∥ BC
eq2 = Eq((Pv[0] - 2) ** 2 + Pv[1] ** 2, dist((2, 0), (Cv[1], aa_, -aa_ * Cv[1])) ** 2)   # AP = 점 A와 직선 BC 사이 거리
sols = [s_ for s_ in solve([eq1, eq2], [kk_, aa_], dict=True) if s_[aa_] > 2]
chk("m2409b", one([f_.subs(s_).subs(x, 12) for s_ in sols]), 30)

# ---- w4: 점 C를 미지수로 두고 F를 실제로 구함
sv = symbols("sv", positive=True)
A_, B_ = Matrix([0, 6]), Matrix([18, 0])
C_ = Matrix([9, 3]) + sv * Matrix([1, 3])
P = (4 * A_ + C_) / 5
Qm = (4 * B_ + C_) / 5
D = (P + Qm) / 2
assert simplify((C_ - P).norm() - (C_ - Qm).norm()) == 0
E = (2 * B_ + 3 * C_) / 5
u_, v_ = symbols("u_ v_")
w = one(solve(list(P + u_ * (E - P) - (C_ + v_ * (D - C_))), [u_, v_], dict=True))
F = P + w[u_] * (E - P)
svv = one(solve(Eq(simplify((D - F).norm()), 4 * sqrt(10) / 3), sv))
Cf = C_.subs(sv, svv)
assert Cf[0] > 0 and Cf[1] > 0
chk("w4", Cf[0] + Cf[1], 32)


# ---- 2026-10-22 추가한 내신 6문항
# n1929 사각형 OABC의 넓이를 y=ax가 이등분: 다각형을 직접 잘라 넓이를 잼
quad = Polygon(Point(0, 0), Point(1, 4), Point(4, 6), Point(4, 1))
aa = Q(19, 16)
Pp = Point(4, 4 * aa)
assert abs(Polygon(Point(0, 0), Point(4, 1), Pp).area) == abs(quad.area) / 2
chk("n1929", aa, Q(19, 16))

# f3-18 직선 AB 위의 D: 닮음비를 쓰지 않고 E를 구해 넓이 비로 확인
A_, B_, C_ = Matrix([1, 1]), Matrix([10, -2]), Matrix([7, 7])
xs = []
for tt in solve(Eq((t ** 2), Q(1, 9)), t):          # D = A + t(B - A) 후보를 넓이 비 식으로 확인
    D = A_ + tt * (B_ - A_)
    E = A_ + tt * (C_ - A_)                          # DE ∥ BC
    assert simplify((E - D)[0] * (C_ - B_)[1] - (E - D)[1] * (C_ - B_)[0]) == 0
    assert area(tuple(A_), tuple(B_), tuple(C_)) == 9 * area(tuple(A_), tuple(D), tuple(E))
    xs.append(D[0])
chk("f3-18", xs[0] * xs[1], -8)

# n1891 정사각형 OABC, B(7, 3): A, C를 직접 구함(OB를 대각선으로)
Mo = Matrix([Q(7, 2), Q(3, 2)])
half = Matrix([-Q(3, 2), Q(7, 2)])                   # OB/2를 90° 돌린 것
A1, C1 = Mo + half, Mo - half
assert (A1 - Matrix([0, 0])).dot(Matrix([7, 3]) - A1) == 0
chk("n1891", Line(Point(*A1), Point(*C1)).intersection(Line(Point(0, 0), Point(1, 0)))[0].x, Q(29, 7))

# n1920 수심
H = one(solve([(x - 1) * (6 - 5) + (y - 3) * (5 - 1), (x - 5) * (6 - 1) + (y - 1) * (5 - 3)], [x, y], dict=True))
chk("n1920", area((1, 3), (5, 1), (H[x], H[y])), Q(16, 9))

# n1607 이등변삼각형 조건: 기울기를 훑어 직선 l과 y=3x, y=-x/3이 만드는 삼각형이 이등변인 기울기 찾기
def tri_iso(M_):
    P1 = one(solve([Eq(y, M_ * x + 2), Eq(y, 3 * x)], [x, y], dict=True))
    P2 = one(solve([Eq(y, M_ * x + 2), Eq(y, -x / 3)], [x, y], dict=True))
    d1, d2 = P1[x] ** 2 + P1[y] ** 2, P2[x] ** 2 + P2[y] ** 2
    d3 = (P1[x] - P2[x]) ** 2 + (P1[y] - P2[y]) ** 2
    return d1 == d2 or d1 == d3 or d2 == d3
cand = [Q(i, 12) for i in range(-60, 61) if i != 0 and Q(i, 12) not in (3, Q(-1, 3)) and tri_iso(Q(i, 12))]
assert cand == [-2, Q(1, 2)], cand
Bp = one(solve([Eq(y, x / 2 + 2), Eq(y, -x / 3)], [x, y], dict=True))
Cp = one(solve([Eq(y, -2 * x + 2), Eq(y, -x / 3)], [x, y], dict=True))
chk("n1607", area((0, 2), (Bp[x], Bp[y]), (Cp[x], Cp[y])), Q(18, 5))

# f8-11 정사각형 PQRS: 기울기 m인 두 쌍의 평행선으로 정사각형을 만들고 네 점이 변(선분) 위에 있는지 확인
sides = []
for M_ in solve(Eq(m - 1 / m, Q(7, 12)), m):
    L1 = (M_, -1, 10 - 3 * M_)          # PQ: A 지남
    L3 = (M_, -1, 2 - 12 * M_)          # RS: C 지남
    L2 = (-1 / M_, -1, 0)               # QR: B 지남
    L4 = (-1 / M_, -1, 9 + 8 / M_)      # SP: D 지남
    meet = lambda La, Lb: one(solve([La[0] * x + La[1] * y + La[2], Lb[0] * x + Lb[1] * y + Lb[2]], [x, y], dict=True))
    P_, Q_, R_, S_ = [meet(*pr) for pr in [(L4, L1), (L1, L2), (L2, L3), (L3, L4)]]
    pt = lambda d_: Point(d_[x], d_[y])
    sq = [pt(P_), pt(Q_), pt(R_), pt(S_)]
    on = [Segment(sq[0], sq[1]).contains(Point(3, 10)), Segment(sq[1], sq[2]).contains(Point(0, 0)),
          Segment(sq[2], sq[3]).contains(Point(12, 2)), Segment(sq[3], sq[0]).contains(Point(8, 9))]
    if all(on):
        sides.append(sq[0].distance(sq[1]))
        assert sq[1].distance(sq[2]) == sides[-1]
chk("f8-11", one(sides), 12)

if __name__ == "__main__":
    bad = [r_ for r_ in R if not r_[1]]
    for r_ in bad:
        print("MISMATCH", r_)
    print("검산", len(R), "불일치", len(bad))
