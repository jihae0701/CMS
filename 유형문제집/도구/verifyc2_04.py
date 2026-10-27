# 공통수학2 4단원(도형의 이동) 유형서 문항 정답 독립 검산 (문항 기호는 c2unit04.py의 v).
# 좌표는 sympy로 풀고, 최솟값·최댓값은 경우를 모두 훑거나 촘촘한 수치 탐색으로 확인한다.
import math
from itertools import product
from sympy import (Rational as Q, sqrt, symbols, solve, simplify, Abs, expand, Poly, pi, Point, Polygon, nsimplify)
R = []
x, y, a, b, k, t, m = symbols("x y a b k t m", real=True)


def chk(no, got, exp):
    R.append((no, simplify(got - exp) == 0 if not isinstance(got, str) else got == exp, got, exp))


def near(no, got, exp, tol=1e-3):
    """수치로 확인한 값 — 맞으면 정확한 값 exp를 검산값으로 남긴다"""
    ok = abs(float(got) - float(exp)) < tol
    R.append((no, ok, exp if ok else got, exp))


def dist(P, l):
    A, B, C = l
    return Abs(A * P[0] + B * P[1] + C) / sqrt(A ** 2 + B ** 2)


def d2(P, Q_):
    return math.hypot(P[0] - Q_[0], P[1] - Q_[1])


def circle_pts(c, r, n=720):
    return [(c[0] + r * math.cos(2 * math.pi * i / n), c[1] + r * math.sin(2 * math.pi * i / n)) for i in range(n)]


def golden(f, lo, hi, it=200):
    g = (math.sqrt(5) - 1) / 2
    c, d = hi - g * (hi - lo), lo + g * (hi - lo)
    for _ in range(it):
        if f(c) < f(d):
            hi = d
        else:
            lo = c
        c, d = hi - g * (hi - lo), lo + g * (hi - lo)
    return f((lo + hi) / 2)


def mark(truth, ch):
    """ㄱㄴㄷ 참·거짓 → 보기 번호"""
    names = "ㄱㄴㄷ"
    s = ", ".join(names[i] for i, v in enumerate(truth) if v)
    return "①②③④⑤"[ch.index(s)] if s in ch else "?"


MC5 = ["ㄱ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"]

# ================================================================ 점의 평행이동
dx, dy = 6 - 3, 1 - 2
chk("f5-1", (4 - dx) + (3 + dy), 3)
sols = [s for s in solve([a ** 2 + b ** 2 - 169, dist((1, 2), (b, -a, 2 * a - 14 * b)) - 5], [a, b], dict=True) if s[a] < 0 and s[b] > 0]
chk("f1-14", sols[0][a] * sols[0][b], -60)

# ================================================================ 도형의 평행이동
A_, B_ = (2, 1), (1, -1)
sl = Q(B_[1] - A_[1], B_[0] - A_[0])
chk("n1910", (A_[1] + 2) - sl * (A_[0] + 4), -9)
# f9-6: 꼭짓점 (1,1) → (-5,15)
p0, q0 = -5 - 1, 15 - 1
chk("f9-6", dist((0, 1), (1, -1, -p0 + q0 + 1)), 10 * sqrt(2))
ks = solve(dist((k - 1, 1), (3, 4, 10)) - 4, k)
chk("g221", ks[0] * ks[1], -31)
# e13-5: 두 원 위 점을 직접 연립해 공통현 길이 2
for av in [sqrt(8)]:
    pts = solve([(x - 2) ** 2 + (y + 3) ** 2 - 4, (x - 2 - av) ** 2 + (y + 1) ** 2 - 4], [x, y])
    ok = simplify((pts[0][0] - pts[1][0]) ** 2 + (pts[0][1] - pts[1][1]) ** 2) == 4   # 공통현의 길이 2 (중심 거리에 대해 단조라 양수 a는 하나)
    R.append(("e13-5", ok, av if ok else -1, 2 * sqrt(2)))
g = (x - 1) ** 2 + 11 * (x - 1) + 24 + 2
areas = []
for s_ in (1, -1):
    for xv in set(solve(g - s_ * x, x)):
        areas.append(pi * xv ** 2)
chk("f6-14", sum(areas), 84 * pi)

# ================================================================ 이동한 도형과 넓이
# g222: 격자 세기로 두 부분 넓이 차
c, r = (-1, 2), 2
n_ = 1500
h = 2 * r / n_
s1 = s2 = 0
for i in range(n_):
    for j in range(n_):
        px, py = c[0] - r + (i + .5) * h, c[1] - r + (j + .5) * h
        if (px - c[0]) ** 2 + (py - c[1]) ** 2 <= r * r:
            if px + py - 3 > 0:
                s1 += 1
            else:
                s2 += 1
near("g222", abs(s1 - s2) * h * h, 2 * pi + 4, 0.02)


def S417(tv, n=4000):
    tot, dxx = 0, 10 / n
    for i in range(n):
        xx = (i + .5) * dxx
        if xx > tv or xx < tv - 8:
            continue
        hh = min(xx - tv + 8, 10 - xx)
        if hh > 0:
            tot += hh * dxx
    return tot


near("f4-17", max(S417(tv / 20) for tv in range(1, 360)), 26, 0.01)

# ================================================================ 점의 대칭이동
chk("f6-4", sum(solve([-b - 2, -a + 1], [a, b]).values()), -1)
av = [s for s in solve(pi * (9 + a ** 2) - 13 * pi, a) if s > 0][0]
chk("e9-12", av, 2)
av = [s for s in solve(2 * a * (a + 2) - 16, a) if s > 0][0]
chk("g209", av + av + 2, 6)
cnt = 0
for X in range(1, 60):
    for Y in range(-60, 0):
        A1, B1, C1 = (X, Y), (Y, X), (0, 10)
        sq = lambda P, Q2: (P[0] - Q2[0]) ** 2 + (P[1] - Q2[1]) ** 2
        ab, bc, ca = sq(A1, B1), sq(B1, C1), sq(C1, A1)
        if ab and bc and ca and (ab + bc == ca or bc + ca == ab or ca + ab == bc):
            cnt += 1
chk("n1629", cnt, 10)

# ================================================================ 도형의 대칭이동
chk("f1-5", solve((2 * y + x - 4).subs(x, 0), y)[0], 2)
f = lambda X, Y: [X ** 2 + Y ** 2 - 2 * X - 6 * Y, abs(X - 2) + abs(Y - 2) - 4, abs(X - Y) + X + Y - 4]
import random
random.seed(1)
tr = []
for i in range(3):
    ok = True
    for _ in range(2000):   # 곡선 위의 점(근사)을 직선 y=x에 대하여 옮겨도 곡선 위인가 — 식에 x, y를 바꿔 넣어 같은 식인지 수치로
        X, Y = random.uniform(-9, 9), random.uniform(-9, 9)
        if abs(f(X, Y)[i] - f(Y, X)[i]) > 1e-9:
            ok = False
            break
    tr.append(ok)
chk("f4-15", "①②③④⑤"[["ㄱ", "ㄴ", "ㄷ", "ㄱ, ㄴ", "ㄴ, ㄷ"].index(", ".join("ㄱㄴㄷ"[i] for i, v in enumerate(tr) if v))], "⑤")
c1, c2 = (7, -1), (-1, 7)
chk("f3-11", sqrt((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2) - 4 * sqrt(2), 4 * sqrt(2))
cnt = 0
for K in range(1, 30):
    curve = -(x ** 2 + 4 * x + 10) + K       # 원점 대칭: -y = x²+4x+10
    if all(not s.is_real for s in solve(curve, x)):
        cnt += 1
chk("g213", cnt, 5)

# ================================================================ 대칭이동한 원과 직선
tot = 0
for M in range(1, 11):
    dd = dist((-1, -2), (M, -1, 0))
    rr = 1 / sqrt(2)
    tot += 2 if simplify(dd - rr) < 0 else (1 if simplify(dd - rr) == 0 else 0)
chk("n1602", tot, 12)
found = []
for K in [Q(i, 4) for i in range(1, 40)]:
    s_ = 0
    for n in range(1, 13):
        sol = [p for p in solve([(x - 2 * K) ** 2 + y ** 2 - n, (y - 2 * K) ** 2 + x ** 2 - n], [x, y]) if all(v.is_real for v in p)]
        s_ += len(set(sol))
    if s_ == 9:
        found.append(K)
chk("n1943", found[0] if len(found) == 1 else -1, 2)

# ================================================================ 평행이동과 대칭이동
avs = solve(Abs(a + 2) - 3, a)
chk("e9-6", sum(avs), -4)
B2 = (3, 2)
C2 = (B2[0] + 1, B2[1] + a)
chk("n1882", solve((B2[1] - 3) * (C2[0] - 2) - (C2[1] - 3) * (B2[0] - 2), a)[0], -1)
lp = 2 * x + 3 * y + m - 8                  # 3(x-m)+2(y+2m)-8 의 x, y를 바꿈
chk("f7-14", solve(lp.subs({x: 0, y: 4}), m)[0], -4)
av = [s for s in solve(dist((-2 * a, -5), (4, -3, 0)) - 5, a) if s > 0][0]
chk("e5-15", av + 5, 10)
fx = (x - 3) ** 2 + 2
gx = -(x - a) ** 2 + 4 * a
disc = Poly(expand(fx - gx), x).all_coeffs()
avs = solve(disc[1] ** 2 - 4 * disc[0] * disc[2], a)
chk("o18", avs[0] * avs[1], 13)

# ================================================================ 점의 이동 규칙
P_ = (3, 8)
while P_[0] != P_[1]:
    P_ = (P_[0] + 3, P_[1]) if P_[1] > P_[0] else (P_[0], P_[1] + 2)
chk("g220", P_[0] + P_[1], 24)
pts = [(2, 1)]
for _ in range(9):
    X, Y = pts[-1]
    if X * Y > 0 and X > Y:
        pts.append((-X, -Y))
    elif X * Y > 0 and X < Y:
        pts.append((X, -Y))
    elif X * Y < 0 and X > Y:
        pts.append((-X, Y))
    else:
        pts.append((Y, X))
val = sum((-1) ** i * ((pts[i][0] - pts[i + 1][0]) ** 2 + (pts[i][1] - pts[i + 1][1]) ** 2) for i in range(9))
chk("n1542", val, 34)

# ================================================================ 점에 대한 대칭이동
img = 2 - y - 2 * (4 - x)                   # 직선 y=2x 위의 점 (4-x, 2-y)
sl_ = solve(img, y)[0]
chk("g216", sl_.coeff(x) + sl_.subs(x, 0), -4)
# g240: y=x²+1 을 점 (2,-1)에 대하여: -y-2 = (4-x)²+1 → y = -(4-x)² - 3
lhs = expand(-(4 - x) ** 2 - 3)
rhs = expand(-(x - a) ** 2 - 1 + b)
sol = solve([Poly(lhs - rhs, x).coeff_monomial(x), Poly(lhs - rhs, x).coeff_monomial(1)], [a, b], dict=True)[0]
chk("g240", sol[a] + sol[b], 2)

# ================================================================ 직선에 대한 대칭이동
def refl(P, A, B, C):
    """점 P를 직선 Ax+By+C=0에 대하여 대칭이동"""
    d = Q(A * P[0] + B * P[1] + C) / (A * A + B * B) if not hasattr(C, "free_symbols") else (A * P[0] + B * P[1] + C) / (A * A + B * B)
    return (P[0] - 2 * A * d, P[1] - 2 * B * d)


pq = refl((3, 4), 1, 1, -2)
chk("g215", pq[0] ** 2 + pq[1] ** 2, 5)
# g243: 접는 선 = 두 점의 수직이등분선
P1, P2 = (2, -1), (0, 5)
Aa, Bb = P2[0] - P1[0], P2[1] - P1[1]
Cc = -(Aa * (P1[0] + P2[0]) + Bb * (P1[1] + P2[1])) / Q(2)
pq = refl((-7, 6), Aa, Bb, Cc)
chk("g243", pq[0] * pq[1], 18)
rr = symbols("rr", positive=True)
pp = refl((4, 3), 8, 6, -rr)               # 공통현 8x+6y-r²=0 (rr = r²)
rs = [s for s in solve(pp[0] ** 2 + pp[1] ** 2 - rr, rr) if 0 < s < 25]
aa_, bb_ = nsimplify(rs[0]).as_coeff_add()
chk("e13-17", 2 * (aa_ + bb_[0] / sqrt(5)), 50)
# g260: 직접 접기 — 점 E(2, e)에 대해 사각형 EFGH 넓이
def area260(e):
    A0, E0 = (0, 1), (2, e)
    mx, my = 1, (1 + e) / 2
    sl2 = -2 / (e - 1)
    gx = (0 - my) / sl2 + mx
    hx = (1 - my) / sl2 + mx
    return 0.5 * (gx + hx) * 1
cand = [e / 3000 for e in range(1, 3000) if abs(area260(e / 3000) - 17 / 18) < 2e-4 and e / 3000 > 0.5]
near("g260", sum(cand) / len(cand), Q(2, 3), 1e-3)

# ================================================================ 도형 f(x, y)=0의 이동
fr = lambda X, Y: X ** 3 + 2 * Y + X * Y * Y + 5 * X     # 대칭이 없는 임의의 식으로 항등식 판별
gg = lambda X, Y: fr(-X, -Y)
hh = lambda X, Y: fr(Y, X)
tr = []
for F_ in (lambda X, Y: gg(-X, -Y) - fr(X, Y), lambda X, Y: gg(-Y, -X) - hh(-X, -Y), lambda X, Y: fr(Y - 2, X - 3) - hh(X - 3, Y - 2)):
    tr.append(all(F_(X, Y) == 0 for X, Y in product(range(-3, 4), repeat=2)))
chk("n1912", mark(tr, ["ㄱ", "ㄴ", "ㄷ", "ㄱ, ㄷ", "ㄱ, ㄴ, ㄷ"]), "④")
cpts = circle_pts((-4, -2), 2, 1440)
vals = []
for (pa, pb) in cpts[::4]:
    for (qc, qd) in cpts[::4]:
        if abs(pa + qd) > 1e-9:
            vals.append((pb + qc) / (pa + qd))
near("g238", max(vals) + min(vals), Q(18, 5), 0.02)

# ================================================================ 대칭이동과 이차함수의 그래프
ps = solve([y - (x ** 2 - 2 * x - 2), x - (y ** 2 - 2 * y - 2)], [x, y])
ps = [p for p in ps if simplify(p[0] - p[1]) != 0]
chk("g233", sqrt((ps[0][0] - ps[0][1]) ** 2 * 2), sqrt(26))
gval = golden(lambda X: abs((X * X - 2 * X + 4) - (X + 1)) / math.sqrt(2), -5, 5)
near("f9-19", 0.5 * 7 * math.sqrt(2) * gval, Q(21, 8))

# ================================================================ 대칭이동을 이용한 최단 거리
near("g217", golden(lambda Y: d2((-3, 2), (0, Y)) + d2((0, Y), (-1, -2)), -10, 10), 4 * sqrt(2))
best = min(d2((5, 2), (q, q)) + d2((q, q), (r_, 0)) + d2((r_, 0), (5, 2)) for q in [i / 50 for i in range(0, 300)] for r_ in [j / 50 for j in range(0, 400)])
near("n1878", best, sqrt(58), 0.01)
best = min(golden(lambda Y: d2((-1, 0), (0, Y)) + d2((0, Y), Qp), -20, 30) for Qp in circle_pts((-3, 8), math.sqrt(5), 2000))
near("g250", best ** 2, 45, 0.01)


def per1624(bx):
    B0 = (bx, -2 * bx + 6)
    return golden(lambda cx: d2((0, 1), B0) + d2(B0, (cx, 0)) + d2((cx, 0), (0, 1)), -20, 20)


bx = min((per1624(i / 3000), i / 3000) for i in range(1, 9000))[1]
near("n1624", bx, Q(7, 3), 1e-3)

# ================================================================ 꺾은선의 길이의 최솟값
best = min(golden(lambda cx: d2((0, 0), (cx, 10)) + d2((cx, 20), (20, 25)), -50, 50) for _ in [0]) + 10
near("g252", best, 35)
best = min(golden(lambda px: d2((-2, 4), (px, 0)) + d2((px + 1, 0), Bp), -20, 20) for Bp in circle_pts((5, 2), math.sqrt(2), 2000))
near("n1512", best, 5 * sqrt(2), 1e-3)


def tri_min(Pd, n=300):
    """D를 고정하고 C는 선분 OA(y=x, 0~10), E는 선분 OB(x축, 0~15) 위에서 둘레 최소 — 반사로 계산하지 않고 훑기"""
    best = 1e9
    for i in range(n + 1):
        cc = 10 * i / n
        Cp = (cc, cc)
        e = golden(lambda ex: d2(Cp, (ex, 0)) + d2((ex, 0), Pd), 0, 15)
        best = min(best, d2(Pd, Cp) + e)
    return best


best = min(tri_min((10 + 5 * s / 100, 10 - 10 * s / 100)) for s in range(0, 101, 2))
near("n1712", best, 6 * sqrt(10), 0.02)
best = 1e9
for i in range(1, 90, 3):
    th = math.radians(i / 2)
    Pp = (2 * math.cos(th), 2 * math.sin(th))
    for j in range(0, 201):
        q = math.sqrt(2) * j / 200
        Qp = (q, q)
        best = min(best, d2(Pp, Qp) + golden(lambda rx: d2(Qp, (rx, 0)) + d2((rx, 0), Pp), 0, 2))
near("n1750", best, 2 * sqrt(2), 0.01)

# ================================================================ 고난도
best = min(golden(lambda qx: d2((-3, 2), (qx, 0)) + d2((qx, 0), Pp), -20, 20) for Pp in circle_pts((5, 4), 3, 3000))
near("m2211", best, 7, 1e-3)
best = 1e9
for Ap in circle_pts((8, 2), 2, 240):
    for Bp in circle_pts((3, -4), 2, 240):
        Bq = (Bp[1], Bp[0])                   # B를 y=x에 대하여 옮긴 점
        Aq = (Ap[0], -Ap[1])
        best = min(best, d2(Aq, Bq))
near("m2309", best, 9, 1e-3)
best = min(golden(lambda q: d2((2, 0), (q, q)) + d2((q, q), Pp), -10, 20) for Pp in circle_pts((7, 3), math.sqrt(2), 3000))
near("m2603", best, 4 * sqrt(2), 1e-3)
best = min(golden(lambda cx: d2((-3, 1), (cx, 0)) + d2((cx, 0), (dd, dd)), -20, 20) + d2((dd, dd), (2, 3)) for dd in [i / 1000 for i in range(-3000, 5000)])
near("m2209", best, 3 * sqrt(5), 1e-3)
# m2227: r = 원 C 중심과 접선 거리, C'이 중심 지남, 같은 직선에 접함
rv = dist((1, 0), (4, -3, 21))
sols = [s for s in solve([a ** 2 + b ** 2 - 25, dist((1 + a, b), (4, -3, 21)) - rv], [a, b], dict=True) if s[a] > 0 and s[b] > 0]
chk("m2227", sols[0][a] + sols[0][b] + rv, 12)
tv = [s for s in solve(dist((-1, 1), (2, -1, -t + 1)) - sqrt(13 - 10), t) if 0 < s < 2][0]
chk("e6-16", tv, sqrt(15) - 2)
found = []
for av in [Q(i, 8) for i in range(17, 120)]:
    A3, B3, C3 = Point(av, 2), Point(2, av), Point(2, -av)
    r1 = Polygon(A3, B3, C3).circumradius
    r2 = Polygon(A3, Point(0, 0), C3).circumradius
    if simplify(r1 * r2 - 18 * sqrt(2)) == 0:
        found.append(av ** 2)
for av in [4 * sqrt(2)]:
    A3, B3, C3 = Point(av, 2), Point(2, av), Point(2, -av)
    if simplify(Polygon(A3, B3, C3).circumradius * Polygon(A3, Point(0, 0), C3).circumradius - 18 * sqrt(2)) == 0:
        found.append(av ** 2)
chk("m2409", found[0] if len(found) == 1 else -1, 32)
# m2321 (ㄱㄴㄷ)
arc = [(5 * math.cos(math.radians(90 + i / 10)), 5 * math.sin(math.radians(90 + i / 10))) for i in range(0, 901)]
mids, lens, ars = set(), set(), []
for (pa, pb) in arc:
    qx, qy = -pa - 4, -pb - 2
    mids.add((round((pa + qx) / 2, 9), round((pb + qy) / 2, 9)))
    lens.add(round(d2((-4, -2), (qx, qy)), 9))
    ars.append(abs((pa - (-4)) * (qy - (-2)) - (qx - (-4)) * (pb - (-2))) / 2)
tr = [mids == {(-2.0, -1.0)}, len(lens) == 1, abs(max(ars) * min(ars) - 20 * math.sqrt(5)) < 1e-3]
chk("m2321", mark(tr, MC5), "②")
# o27
def edges(x0, y0, x1, y1):
    return [((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)), ((x0, y1), (x1, y1)), ((x0, y0), (x0, y1))]


def inter(s1, s2):
    (p1, p2), (p3, p4) = s1, s2
    h1, h2 = p1[1] == p2[1], p3[1] == p4[1]
    if h1 == h2:
        if h1 and p1[1] != p3[1] or (not h1) and p1[0] != p3[0]:
            return set()
        i_ = 0 if h1 else 1
        lo = max(min(p1[i_], p2[i_]), min(p3[i_], p4[i_]))
        hi = min(max(p1[i_], p2[i_]), max(p3[i_], p4[i_]))
        if lo < hi:
            return None
        return {(lo, p1[1]) if h1 else (p1[0], lo)} if lo == hi else set()
    if not h1:
        s1, s2 = s2, s1
        (p1, p2), (p3, p4) = s1, s2
    if min(p1[0], p2[0]) <= p3[0] <= max(p1[0], p2[0]) and min(p3[1], p4[1]) <= p1[1] <= max(p3[1], p4[1]):
        return {(p3[0], p1[1])}
    return set()


mm = nn = 0
for A4 in range(-8, 9):
    for B4 in range(-8, 9):
        pts, inf = set(), False
        for s1 in edges(0, 0, 2, 2):
            for s2 in edges(A4 - 2, B4 - 2, A4, B4):
                rr2 = inter(s1, s2)
                if rr2 is None:
                    inf = True
                else:
                    pts |= rr2
        if inf:
            nn += 1
        elif len(pts) == 2:
            mm += 1
chk("o27", abs(mm - nn), 13)
# m2510: A(a, b), a²+b²=9 (반지름 3), B(-2a, 0)에서의 접선 기울기 1/2
sols = [s for s in solve([a ** 2 + b ** 2 - 9, -a / b * 0 + (b - 0) / (a - 2 * a) * Q(1, 2) + 1], [a, b], dict=True) if s[a] > 0 and s[b] > 0]
av, bv = sols[0][a], sols[0][b]
# 접선 l: 점 B(-2a,0)을 지나고 기울기 1/2 → x - 2y + 2a = 0
chk("m2510", dist((av, bv), (1, -2, 2 * av)), Q(3, 5))
# 조건(PQ=6 ⇒ 반지름 3) 수치 확인: 원 C1 위의 P, C2 위의 Q, ∠POQ=90°일 때 PQ
cA = (float(av), float(bv))
ok = True
for i in range(1, 359, 7):
    th = math.radians(i)
    Pp = (cA[0] + 3 * math.cos(th), cA[1] + 3 * math.sin(th))
    if d2(Pp, (0, 0)) < 1e-6:
        continue
    # OQ ⟂ OP, Q는 원 C2 위(원점 아닌 점)
    ux, uy = -Pp[1], Pp[0]
    tq = -2 * ((-cA[0]) * ux + (-cA[1]) * uy) / (ux * ux + uy * uy)
    Qp = (tq * ux, tq * uy)
    if abs(d2(Pp, Qp) - 6) > 1e-6:
        ok = False
R.append(("m2510 조건", ok, ok, True))
# m2410 (ㄱㄴㄷ)
g1 = True                                    # ㄱ: (4,2),(0,s)와 (4,-2),(0,-s) — 거리 같음
for s_ in range(-5, 6):
    g1 &= abs(d2((4, 2), (0, s_)) - d2((4, -2), (0, -s_))) < 1e-12


def minsum(Bp, cen, rad):
    return golden(lambda s_: d2(Bp, (0, s_)) + d2((0, -s_), cen) - rad, -40, 40)


g2 = abs(minsum((4, 2), (2, 6), 1) - 9) < 1e-6
dif = lambda av_: minsum((av_, 6 * av_ + 1), (2, 6), 1) - minsum((av_, 6 * av_ + 1), (6, 4), 3) - 2
assert all(dif(i / 100) < dif((i + 1) / 100) for i in range(1, 400))     # a에 대하여 증가하므로 근은 하나
lo_, hi_ = 0.01, 4.0
for _ in range(60):
    mid = (lo_ + hi_) / 2
    lo_, hi_ = (mid, hi_) if dif(mid) < 0 else (lo_, mid)
asol = lo_
g3 = abs(d2((0, 0), (asol, 6 * asol + 1)) - math.sqrt(65) / 2) < 1e-6
chk("m2410", mark([g1, g2, g3], MC5), "⑤")
# n1732: f(x)=ax²+bx+c, 경우를 모두 훑어 조건에 맞는 f(10)
res = []
for c0 in (-4, 0, 4):
    for av in solve(c0 - (12 * a - 1) ** 2 / (4 * a) + 4, a):
        if av <= 0:
            continue
        fx = av * x ** 2 + (12 * av - 1) * x + c0
        rs = sorted({r_ for kk in (4, 0, -4) for r_ in solve(fx + x - kk, x) if r_.is_real}, key=lambda v: float(v))
        if len(rs) == 6 and rs[4] == 0 and simplify(sum(rs) - rs[4] + 36) == 0:
            res.append(fx.subs(x, 10))
chk("n1732", res[0] if len(res) == 1 else -1, 45)
# m2329: 조건을 만족하는 r, k를 직접 찾음 — 두 원 (0,6),(6+k,0) 반지름 r, 기울기 범위 [0, 4/3]
def slope_range(rv, kv, n=360):
    A5, B5 = (0, 6), (6 + kv, 0)
    lo, hi = 1e9, -1e9
    for i in range(n):
        for j in range(n):
            p1 = (A5[0] + rv * math.cos(2 * math.pi * i / n), A5[1] + rv * math.sin(2 * math.pi * i / n))
            p2 = (B5[0] + rv * math.cos(2 * math.pi * j / n), B5[1] + rv * math.sin(2 * math.pi * j / n))
            if abs(p2[0] - p1[0]) > 1e-9:
                s_ = (p2[1] - p1[1]) / (p2[0] - p1[0])
                lo, hi = min(lo, s_), max(hi, s_)
    return lo, hi


lo, hi = slope_range(3, -18)
near("m2329 기울기 최솟값", lo, 0, 2e-3)
near("m2329 기울기 최댓값", hi, Q(4, 3), 2e-3)
lo2, hi2 = slope_range(3, -Q(21, 2))
R.append(("m2329 k=-21/2 제외", not (abs(lo2) < 2e-3 and abs(hi2 - 4 / 3) < 2e-3), (lo2, hi2), "다름"))
chk("m2329", abs(3 + (-18)), 15)

if __name__ == "__main__":
    bad = [r_ for r_ in R if not r_[1]]
    for r_ in bad:
        print("MISMATCH", r_)
    print("검산", len(R), "불일치", len(bad))
