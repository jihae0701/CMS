# -*- coding: utf-8 -*-
"""공통수학2 기본서 1단원 평면좌표 검산: 문항마다 답을 따로 계산해 data01.py의 답과 맞춘다.
python verify01.py
- 좌표 문제는 sympy로 직접 풀고, 최솟값·최댓값은 촘촘한 수치 탐색으로도 다시 확인한다.
"""
import sys, os, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from sympy import *
import data01

x, y, t, a, b, c = symbols("x y t a b c", real=True)


def dist(P, Q):
    return sqrt((P[0] - Q[0]) ** 2 + (P[1] - Q[1]) ** 2)


def inner(P, Q, m, n):
    return ((m * Q[0] + n * P[0]) / (m + n), (m * Q[1] + n * P[1]) / (m + n))


def outer(P, Q, m, n):
    return ((m * Q[0] - n * P[0]) / (m - n), (m * Q[1] - n * P[1]) / (m - n))


R = {}
# 001: A(0), B(4)
A, B = 0, 4
P_, Q_ = Rational(3 * 4 + 0, 4), Rational(3 * 4 - 0, 2)
ok = [Rational(2 * Q_ + A, 3) == B, Rational(2 * Q_ - P_, 1) == A, (A + Q_) / 2 == P_]
R["001"] = "".join("ㄱㄴㄷ"[i] for i in range(3) if ok[i])
# 003: A..G = 0..6
pt = dict(zip("ABCDEFG", range(7)))
ok = [Rational(5 * 6 + 2 * 0, 7) == pt["E"], Rational(2 * 3 - 2, 1) == pt["F"], Rational(2 * 4 - 3 * 3, -1) == pt["B"]]
R["003"] = "".join("ㄱㄴㄷ"[i] for i in range(3) if ok[i])
# 007: C on line AB with 2AB = 3BC
A, B = (3, 3), (6, 9)
sols = []
for s in (Rational(-2, 3), Rational(2, 3)):        # C = B + s(B-A)
    C = (B[0] + s * (B[0] - A[0]), B[1] + s * (B[1] - A[1]))
    assert 2 * dist(A, B) == 3 * dist(B, C)
    sols.append(C[0] + C[1])
R["007"] = sum(sols)
# 011: C on extension (not on segment), 3AB = 2BC
A, B = (-1, 2), (3, -2)
v = 0
for s in (Rational(3, 2), Rational(-3, 2)):
    C = (B[0] + s * (B[0] - A[0]), B[1] + s * (B[1] - A[1]))
    # 선분 AB 위가 아님: C = A + u(B-A)에서 u<0 또는 u>1
    u = 1 + s
    assert u < 0 or u > 1
    v += C[0] * C[1]
R["011"] = v
# 012, 014
Pt = inner((2, 4), (-2, -5), t, 1 - t)
R["012"] = solve([Pt[0] > 0, Pt[1] > 0, t > 0, t < 1], t)
Pt = inner((-4, -1), (3, 4), t, 1 - t)
r = solve([Pt[0] < 0, Pt[1] > 0, t > 0, t < 1], t)
R["014"] = r
# 015
A, B, C = (2, 10), (-8, -14), (10, 4)
R["015"] = inner(B, C, dist(A, B), dist(A, C))
# 016: O, A(1,2), B(5,4)
O, A, B = (0, 0), (1, 2), (5, 4)
R["016"] = inner(O, B, dist(A, O), dist(A, B))
# 017
O, A, B = (0, 0), (3, 4), (1, 0)
x17 = radsimp(outer(O, B, dist(A, O), dist(A, B))[0])
assert simplify(x17 - (5 + 2 * sqrt(5))) == 0
R["017"] = 5 * 2
# 018
A, B, C = (-1, 2), (3, 5), (-3, -3)
r18 = dist(B, A) / dist(B, C)
R["018"] = numer(r18) ** 2 + denom(r18) ** 2
# 038
A, B, C = (6, 1), (-1, 2), (2, 3)
s = solve([dist((x, y), A) ** 2 - dist((x, y), B) ** 2, dist((x, y), A) ** 2 - dist((x, y), C) ** 2], [x, y], dict=True)[0]
R["038"] = s[x] + s[y] + dist((s[x], s[y]), A)
# 039
A, B, C = (7, 1), (5, -3), (-1, 5)
s = solve([dist((x, y), A) ** 2 - dist((x, y), B) ** 2, dist((x, y), A) ** 2 - dist((x, y), C) ** 2], [x, y], dict=True)[0]
R["039"] = dist((s[x], s[y]), A)


def incenter(A, B, C):
    la, lb, lc = dist(B, C), dist(C, A), dist(A, B)
    s = la + lb + lc
    return (simplify((la * A[0] + lb * B[0] + lc * C[0]) / s), simplify((la * A[1] + lb * B[1] + lc * C[1]) / s))


R["042"] = incenter((0, 0), (6, 0), (3, 4))
I = incenter((0, 0), (2, 2 * sqrt(3)), (4, 0))
R["043"] = simplify(I[0] ** 2 + I[1] ** 2)
R["044"] = Rational(5 + 4 + 0, 3) + Rational(-4 + 6 - 2, 3)
A, B, C = (1, 2), (2, 4), (3, 3)
Pp, Qp, Rp = outer(A, B, 2, 1), outer(B, C, 2, 1), outer(C, A, 2, 1)
R["047"] = (Rational(Pp[0] + Qp[0] + Rp[0], 3), Rational(Pp[1] + Qp[1] + Rp[1], 3))
# 051: M(0), B(-2), C(2), D(1)
s = solve([x ** 2 + y ** 2 - 15, (x - 1) ** 2 + y ** 2 - 12], [x, y], dict=True)[0]
R["051"] = expand((s[x] + 2) ** 2 + s[y] ** 2 - (s[x] - 2) ** 2 - s[y] ** 2)
# 052: G at origin, |a|=4,|b|=6,|c|=8, a+b+c=0 -> |b-c|^2 = 2|b|^2+2|c|^2-|a|^2 ... 직접: b.c = (|a|^2-|b|^2-|c|^2)/2
bc = Rational(16 - 36 - 64, 2)
R["052"] = sqrt(36 + 64 - 2 * bc)
# 056
s = solve([x ** 2 + y ** 2 - 9, (x - 6) ** 2 + y ** 2 - 25], [x, y], dict=True)
R["056"] = radsimp(sqrt((s[0][x] - 4) ** 2 + s[0][y] ** 2))
# 058
s = solve([x ** 2 + y ** 2 - 25, (x - 9) ** 2 + y ** 2 - 49], [x, y], dict=True)[0]
R["058"] = 9 - 2 * s[x]
# 048
f = sum(dist((x, y), Pp_) ** 2 for Pp_ in [(4, 0), (-1, 1), (3, 5)])
s = solve([diff(f, x), diff(f, y)], [x, y], dict=True)[0]
R["048"] = s[x] + s[y]
# 062
f = (t - 0) ** 2 + (t - 2 - 1) ** 2 + (t + 1) ** 2 + (t - 2) ** 2
tt = solve(diff(f, t), t)[0]
R["062"] = (tt, tt - 2)
# 065, 067: 수치 탐색과 공식
import math
g = lambda u: math.sqrt(u * u + 2 * u + 26) + math.sqrt(u * u - 6 * u + 10)
assert abs(min(g(-10 + i / 1000) for i in range(30000)) - math.sqrt(52)) < 1e-5
R["065"] = 2 * sqrt(13)
A, B = (3, 6), (-1, 3)
h = lambda u: abs(math.hypot(u - 3, 6) - math.hypot(u + 1, 3))
assert abs(max(h(-200 + i / 100) for i in range(40000)) - 5) < 1e-3
R["068"] = dist(A, B)
# 070, 072
R["070"] = dist((0, 40), (40, -10))
R["072"] = dist((-10, 30), (50, 0))
best = min(math.hypot(px - 0, 30 - 20) + math.hypot(qx - px, 30) + math.hypot(40 - qx, 10)
           for px in [i / 10 for i in range(401)] for qx in [j / 10 for j in range(401)])
assert abs(best - math.sqrt(4100)) < 1e-3
# 078
u = symbols("u", positive=True)
cand = [r for r in solve((u - 16) ** 2 + (u - 40) ** 2 - 36 * u, u) if r > 40]
R["078"] = cand[0]
# 080: A(0,h), B(-h,0), C(h,0)
hh, d = symbols("h d", positive=True)
R["080"] = solve(Eq((d ** 2 + hh ** 2) + (hh + d) * (hh - d), 100), hh ** 2) or [50]
R["080"] = 50 if simplify((d ** 2 + hh ** 2) + (hh + d) * (hh - d) - 2 * hh ** 2) == 0 else None
# STEP 3
av, bv = symbols("a_v b_v", real=True)
X, Y, Z = (3 * av + 2 * bv) / 5, (2 * av + bv) / 3, (3 * av - bv) / 2
vals = {"X": X.subs({av: 1, bv: 5}), "Y": Y.subs({av: 1, bv: 5}), "Z": Z.subs({av: 1, bv: 5})}
R["002"] = "<".join(sorted(vals, key=lambda k: vals[k]))
A, B = (-3, 4), (1, -2)
P_ = (B[0] + Rational(1, 2) * (B[0] - A[0]), B[1] + Rational(1, 2) * (B[1] - A[1]))
R["008"] = P_[0] - P_[1]
m, n = symbols("m n", positive=True)
AB = 1
R["020"] = simplify((1 / (m / (m + n)) + 1 / (m / (m - n))) * AB)
O, A, B = (0, 0), (2, 1), (1, 5)
G = (Rational(3, 3), Rational(6, 3))
area = Rational(abs(2 * 5 - 1 * 1), 2)
R["045"] = G[0] + G[1] + 2 * area / 3
f = sum(dist((x, y), Pp_) ** 2 for Pp_ in [(2, 6), (0, 2), (4, -2)])
s = solve([diff(f, x), diff(f, y)], [x, y], dict=True)[0]
R["049"] = f.subs(s)
s = solve([x ** 2 + y ** 2 - 36, (x - 6) ** 2 + y ** 2 - 16], [x, y], dict=True)[0]
R["053"] = simplify((s[x] - 2) ** 2 + s[y] ** 2 + (s[x] - 4) ** 2 + s[y] ** 2)
# 059: D=0, B(-k,0), C(3k,0), A(p,q)
k, p, q = symbols("k p q", real=True)
lhs = 3 * ((p + k) ** 2 + q ** 2) + (p - 3 * k) ** 2 + q ** 2
P4, Q3 = 4, 3
assert expand(lhs - P4 * ((p ** 2 + q ** 2) + Q3 * k ** 2)) == 0
R["059"] = P4 + Q3
# 060: 무작위 삼각형 몇 개로 k, l 확인
import random
kk, ll = 4, 9
for _ in range(5):
    A, B, C = [(random.random() * 9, random.random() * 9) for _ in range(3)]
    G = ((A[0] + B[0] + C[0]) / 3, (A[1] + B[1] + C[1]) / 3)
    d2 = lambda P, Q: (P[0] - Q[0]) ** 2 + (P[1] - Q[1]) ** 2
    assert abs(d2(A, B) + d2(A, C) + kk * d2(B, C) - ll * (d2(B, G) + d2(C, G))) < 1e-9
R["060"] = kk + ll
g2 = lambda u: math.sqrt(u * u - 2 * u + 2) + math.sqrt(u * u - 4 * u + 5)
assert abs(min(g2(-5 + i / 1000) for i in range(10000)) - math.sqrt(5)) < 1e-5
R["067"] = sqrt(5)
R["066"] = 8 ** 2 + 8 ** 2
R["069"] = sqrt(9 ** 2 + 17 ** 2)
best = min(math.hypot(6, 10 - py) + math.hypot(2, py - ry) + math.hypot(2, ry - qy) + math.hypot(8, qy + 8)
           for py in [i / 4 for i in range(-40, 61)] for ry in [i / 4 for i in range(-40, 61)] for qy in [i / 4 for i in range(-40, 61)])
assert abs(best - 18 * math.sqrt(2)) < 0.05, best
R["073"] = 18 * sqrt(2)


# ---- 외분점을 뺀 뒤 넣은 문항
A, B = (2, 2), (5, 8)
C = inner(A, B, Integer(1), Integer(2))
assert simplify(2 * dist(A, B) - 3 * dist(B, C)) == 0
R["009"] = C
P3, P5 = sqrt(3), sqrt(5)
vals = {"a": (P5 + 2 * P3) / 3, "b": (P5 + 3 * P3) / 4, "c": (3 * P5 + 2 * P3) / 5}
R["005"] = "<".join(sorted(vals, key=lambda k: float(vals[k])))
s = solve([dist((x, y), (2, 0)) ** 2 - dist((x, y), (0, 4)) ** 2, dist((x, y), (2, 0)) ** 2 - dist((x, y), (4, 1)) ** 2], [x, y], dict=True)[0]
R["040"] = s[x] * s[y]
for _ in range(5):
    A, B, C = [(random.random() * 9, random.random() * 9) for _ in range(3)]
    G = ((A[0] + B[0] + C[0]) / 3, (A[1] + B[1] + C[1]) / 3)
    d2 = lambda P, Q: (P[0] - Q[0]) ** 2 + (P[1] - Q[1]) ** 2
    assert abs(d2(A, B) + d2(B, C) + d2(C, A) - 3 * (d2(G, A) + d2(G, B) + d2(G, C))) < 1e-9
R["050"] = 3
xx = solve(diff((x - 4) ** 2 + 4 + x ** 2, x), x)[0]
R["054"] = "%s:%s" % (xx, 5 - xx)
kk = symbols("kk", positive=True)
k7 = solve(81 * kk + 49 * 3 * kk - 4 * kk * (36 + 3 * kk ** 2), kk)
R["057"] = 4 * [r for r in k7 if r > 0][0]
s = solve([x ** 2 + y ** 2 - 5, (x - 1) ** 2 + y ** 2 - 8], [x, y], dict=True)
assert any(t[x] == -1 and t[y] == 2 for t in s)
A = (-1, 2)
assert A[0] ** 2 + A[1] ** 2 == 5 and (A[0] - 1) ** 2 + A[1] ** 2 == 8
B, C, D = (-2, 0), (2, 0), (1, 0)
d2 = lambda P, Q: (P[0] - Q[0]) ** 2 + (P[1] - Q[1]) ** 2
ok = [len({d2(A, B), d2(B, D), d2(A, D)}) < 3, d2(A, C) - d2(A, B) == 8, Rational(1, 2) * 4 * 2 == 4]
R["055"] = "".join("ㄱㄴㄷ"[i] for i in range(3) if ok[i])

# ---------------------------------------------------------------- 고쟁이(g)·무장해제(m) 문항
# g027: 이등변삼각형이 되는 정수 k (세 점이 한 직선 위에 있으면 뺀다)
kk_ = symbols("k")
A, C = (-1, -1), (2, -2)
d2 = lambda P, Q: expand((P[0] - Q[0]) ** 2 + (P[1] - Q[1]) ** 2)
ks = set()
for k_ in range(-50, 51):
    B = (0, -k_)
    ab, bc, ca = d2(A, B), d2(B, C), d2(C, A)
    col = (B[0] - A[0]) * (C[1] - A[1]) - (B[1] - A[1]) * (C[0] - A[0]) == 0
    if not col and (ab == bc or bc == ca or ca == ab):
        ks.add(k_)
R["g027"] = sum(ks)
# g028
A, B, C = (0, 1), (1, 0), (8, 1)
s = solve([d2((x, y), A) - d2((x, y), B), d2((x, y), A) - d2((x, y), C)], [x, y], dict=True)[0]
Pc = (s[x], s[y]); Q = (2 * Pc[0] - B[0], 2 * Pc[1] - B[1])
assert Q[0] > 0 and Q[1] > 0 and d2(Pc, Q) == d2(Pc, A)
S_ = abs((B[0] - A[0]) * (Q[1] - A[1]) - (B[1] - A[1]) * (Q[0] - A[0])) / 2
R["g028"] = Pc[0] * Pc[1] * S_
# g024: 수치로 최소 시각 확인
f = lambda t_: (960 - 40 * t_) ** 2 + (720 - 40 * t_) ** 2
tm = min((f(i / 100), i / 100) for i in range(0, 5000))[1]
assert abs(tm - 21) < 1e-9
R["g024"] = (21, sqrt(f(21)))
# g045
f = lambda t_: (2 * t_ + t_) ** 2 + (2 * t_ - (10 - 2 * t_)) ** 2
tm = min((f(i / 1000), i / 1000) for i in range(0, 10000))[1]
assert abs(tm - 1.6) < 1e-9
R["g045"] = Rational(8, 5) * 60 + sqrt(f(Rational(8, 5)))
# g032: 수직선
A_ = 0; D_ = 5; B_ = Rational(3 * D_ + 2 * A_, 5); C_ = 2 * B_ - A_; E_ = Rational(2 * D_ + B_, 3)
assert len({A_, B_, C_, D_, E_}) == 5
R["g032"] = (E_ - A_) / abs(C_ - E_)
# g049: 모든 (a, b, m, n)을 직접 찾는다
areas = []
for a_ in range(1, 6):
    for b_ in range(1, 6):
        ok = False
        for m_ in range(1, 40):
            for n_ in range(1, 40):
                if Rational(-2 * m_ + a_ * n_, m_ + n_) == 0 and Rational(-2 * m_ + b_ * n_, m_ + n_) == 0:
                    ok = True
        if ok:
            A = (a_, b_); B = (-2, 1); C = (1, -2)
            areas.append(abs((B[0] - A[0]) * (C[1] - A[1]) - (B[1] - A[1]) * (C[0] - A[0])) / Rational(2))
R["g049"] = max(areas) - min(areas)
# g043
A, B, C = (-4, 1), (4, 7), (16, 1)
R["g043"] = sum(inner(B, C, dist(A, B), dist(A, C)))
# g036
s = solve([(2 + a + b) / 3 - 5, (-1 + 2 - 4) / Rational(3) - a * b], [a, b], dict=True)
R["g036"] = simplify(s[0][a] ** 2 + s[0][b] ** 2)
assert all(simplify(t_[a] ** 2 + t_[b] ** 2 - R["g036"]) == 0 for t_ in s)
# m08: 평행사변형 좌표로 확인 (B 원점, C(12,0))
s = solve([x ** 2 + y ** 2 - 64, (x + 12) ** 2 + y ** 2 - 256], [x, y], dict=True)[0]   # A(x,y), D=A+C
A = (s[x], s[y]); C = (12, 0)
R["m08"] = simplify(dist(A, C))
# m13: 수치 탐색 (변 AB, AC 모두)
A, B, C = (0, sqrt(3)), (-1, 0), (1, 0)
best = None
for side in (B, C):
    for i in range(0, 4001):
        u = Rational(i, 4000)
        P_ = (A[0] + u * (side[0] - A[0]), A[1] + u * (side[1] - A[1]))
        v = float(d2(B, P_) + d2(C, P_))
        if best is None or v < best[0] - 1e-12:
            best = (v, P_)
R["m13"] = simplify(abs(best[1][1]) * 2 / 2)
# g037: 수직선 A(0), B(2), C(5)
xx = solve(diff(x ** 2 + (x - 2) ** 2 + (x - 5) ** 2, x), x)[0]
r_ = (xx - 2) / (5 - xx)
R["g037"] = numer(r_) + denom(r_)
# g046
AC = 2 * sqrt(3) * 2 / sqrt(3)
mm, nn = symbols("mm nn", positive=True)
r_ = solve(AC * (mm - 1) / (mm + 1) - Rational(4, 5), mm)[0]          # m/n
# A가 CR을 (m-n):n으로 내분 → CA:AR = (m-n):n
R["g046"] = simplify(AC * 1 / (r_ - 1))
# g048
s = solve([(a - 8) ** 2 + b ** 2 - 80], [b], dict=True)
sol = []
for a_ in [Rational(i, 100) for i in range(1, 2000)]:
    pass
A, B = (0, 4), (8, 0)
s = solve([(a - 8) ** 2 + b ** 2 - 80, ((5 * a + 16) / 9 - a) ** 2 + ((5 * b + 8) / 9 - b) ** 2 - Rational(64, 9)], [a, b], dict=True)
s = [t_ for t_ in s if t_[a] > 0 and t_[b] > 0]
assert len(s) == 1
Cc = (s[0][a], s[0][b]); Pp = inner(A, Cc, 1, 2); Qq = inner(B, Cc, 1, 2)
G = ((Cc[0] + Pp[0] + Qq[0]) / 3, (Cc[1] + Pp[1] + Qq[1]) / 3)
assert d2(Cc, G) == Rational(64, 9)
R["g048"] = Cc[0] + Cc[1]
# g051: 좌표로 삼각형을 만들어 확인 (G 원점)
s = solve([x ** 2 + y ** 2 - 12, (x + (-x)) ** 2], [x, y], dict=True)
# B=(p,q), C=(r,s), A=-(B+C), |A|=4√2, |B|=2√3, |C|=2√5
p_, q_, r2, s2 = symbols("p_ q_ r2 s2", real=True)
sol = solve([p_ ** 2 + q_ ** 2 - 12, r2 ** 2 + s2 ** 2 - 20, (p_ + r2) ** 2 + (q_ + s2) ** 2 - 32, q_], [p_, q_, r2, s2], dict=True)
sv = sol[0]
B = (sv[p_], sv[q_]); C = (sv[r2], sv[s2]); A = (-B[0] - C[0], -B[1] - C[1])
R["g051"] = simplify(abs((B[0] - A[0]) * (C[1] - A[1]) - (B[1] - A[1]) * (C[0] - A[0])) / 2)
# g050
s = solve([x ** 2 + y ** 2 - 40, (x - 6) ** 2 + y ** 2 - 52], [x, y], dict=True)
A = [(t_[x], t_[y]) for t_ in s if t_[y] > 0][0]
ok = [d2(A, (3, 0)) == 37]
ps = [p for p in [Rational(i, 1000) for i in range(1, 6000)] if d2(A, (p, 0)) == 40]
r_ = ps[0] / (6 - ps[0]); ok.append(len(ps) == 1 and numer(r_) - denom(r_) == 3)
ps = [p for p in [Rational(i, 1000) for i in range(1, 6000)] if d2(A, (p, 0)) == 45]
r_ = ps[0] / (6 - ps[0]); ok.append(len(ps) == 1 and numer(r_) + 2 * denom(r_) == 7)
R["g050"] = "".join("ㄱㄴㄷ"[i] for i in range(3) if ok[i])

# n01: 직사각형 (예: P(√5, 2), a=√5+2√3, b=2+√13) — 존재 확인 후 PD
a_, b_ = sqrt(5) + 2 * sqrt(3), 2 + sqrt(13)
P_ = (sqrt(5), 2)
A, B, C, D = (0, 0), (a_, 0), (a_, b_), (0, b_)
assert [simplify(dist(P_, Q)) for Q in (A, B, C)] == [3, 4, 5]
R["n01"] = simplify(dist(P_, D))
# m192v: 격자점 전수
pts = [(i, j) for i in range(5) for j in range(5)]
cnt = 0
for u_, v_ in itertools.combinations(pts, 2):
    ok = all(((2 * u_[k] + v_[k]) % 3 == 0) and ((u_[k] + 2 * v_[k]) % 3 == 0) for k in (0, 1))
    cnt += ok
R["m192v"] = cnt
# m04: 임의의 삼각형 여러 개로 비 확인
import random
random.seed(1)
for _ in range(5):
    A, B, C = [(Rational(random.randint(-9, 9)), Rational(random.randint(-9, 9))) for _ in range(3)]
    if (B[0] - A[0]) * (C[1] - A[1]) - (B[1] - A[1]) * (C[0] - A[0]) == 0:
        continue
    G = ((A[0] + B[0] + C[0]) / 3, (A[1] + B[1] + C[1]) / 3)
    mid = lambda P, Q: ((P[0] + Q[0]) / 2, (P[1] + Q[1]) / 2)
    L_, M_, N_ = mid(B, C), mid(C, A), mid(A, B)
    r_ = (d2(A, B) + d2(B, C) + d2(C, A)) / (d2(G, L_) + d2(G, M_) + d2(G, N_))
    assert r_ == 12
R["m04"] = 12

# 고쟁이로 바꾼 문항(2026-10-19)
# g026: B, C를 직접 잡아 확인 (P 중심, 반지름 √13인 원 위 지름 양 끝)
Pc = (-1, -1); A = (2, 1)
B = (-1 + sqrt(13), -1); C = (-1 - sqrt(13), -1)
assert simplify(d2(Pc, A) - d2(Pc, B)) == 0
R["g026"] = simplify(d2(A, B) + d2(A, C))
# g031
vals = {"P": sqrt(2), "Q": sqrt(3), "A": (sqrt(2) + sqrt(3)) / 2, "B": (3 * sqrt(2) + sqrt(3)) / 4, "C": (sqrt(2) + 3 * sqrt(3)) / 4}
R["g031"] = "".join(sorted(vals, key=lambda k: float(vals[k])))
# g033
Pt = ((1 - t) * 1 + t * (-5), (1 - t) * (-3) + t * 1)
r = solve([Pt[0] < 0, Pt[1] < 0, t > 0, t < 1], t)
assert r.as_set() == Interval.open(Rational(1, 6), Rational(3, 4))
R["g033"] = Rational(1, 6) + Rational(3, 4)
# g025: 정삼각형을 직접 만든다
A = Matrix([3, 5]); G = Matrix([-1, 2])
M_ = G + (G - A) / 2
u = (M_ - A); perp = Matrix([-u[1], u[0]]) / u.norm()
half = u.norm() / sqrt(3)
B = M_ + perp * half; C = M_ - perp * half
assert simplify((A - B).norm() - (B - C).norm()) == 0 and simplify((A - C).norm() - (B - C).norm()) == 0
R["g025"] = simplify(3 * (B - C).norm())
# g021
f_ = sum((x - p[0]) ** 2 + (y - p[1]) ** 2 for p in ((1, -1), (-3, 4), (5, 6)))
s_ = solve([diff(f_, x), diff(f_, y)], [x, y], dict=True)[0]
R["g021"] = s_[x] + s_[y] + f_.subs(s_)
# g022: 촘촘한 수치 탐색 + 선분 길이
g_ = lambda X, Y: math.sqrt(X * X + Y * Y + 6 * X - 4 * Y + 13) + math.sqrt(X * X + Y * Y - 2 * X - 8 * Y + 17)
import math
mn = min(g_(-4 + i * 0.05, j * 0.05) for i in range(120) for j in range(120))
assert abs(mn - math.sqrt(20)) < 1e-6
R["g022"] = sqrt(20)
# g029: 좌표로
kk2 = symbols("kk2", positive=True)
s_ = solve([(x + kk2) ** 2 + y ** 2 - 25, (x - 3 * kk2) ** 2 + y ** 2 - 9, x ** 2 + y ** 2 - 15], [x, y, kk2], dict=True)
R["g029"] = simplify(4 * [q for q in s_ if q[kk2] > 0][0][kk2])
# g030: 임의의 삼각형으로 비 확인
k30 = None
for (ax_, ay_, c_) in ((1, 2, 1), (3, 5, 2), (-2, 7, 3)):
    A = (ax_, ay_); B = (-3 * c_, 0); C = (c_, 0); D = (0, 0)
    r_ = Rational(3 * d2(A, D) + d2(B, D), d2(A, B) + 3 * d2(A, C))
    assert k30 is None or r_ == k30
    k30 = r_
R["g030"] = k30

# 넓이의 비(2026-10-19)
def area(P, Q, T):
    return abs((Q[0] - P[0]) * (T[1] - P[1]) - (Q[1] - P[1]) * (T[0] - P[0])) / Rational(2)
# g042
A, B, C = (-3, 1), (-1, 5), (2, -1)
Pp = inner(A, C, dist(B, A), dist(B, C))
G = ((A[0] + B[0] + C[0]) / Rational(3), (A[1] + B[1] + C[1]) / Rational(3))
R["g042"] = simplify(area(A, B, C) / area(B, Pp, G))
# g053: 여러 볼록사각형으로 확인
for (A, B, C, D) in (((1, 2), (0, 0), (4, 0), (3, 3)), ((-1, 4), (0, 0), (6, 0), (5, 6))):
    A = tuple(map(Rational, A)); D = tuple(map(Rational, D))
    sA, sD = area(A, B, C), area(D, B, C)
    E = inner(A, D, 3, 1)
    rat = area(E, B, C)
    assert rat == (sA + 3 * sD) / 4
R["g053"] = (2 + 3 * 3) / Rational(4)
# m10: 이등변이 아닌 삼각형으로도 확인
for (A, B, C) in (((0, 9), (-4, 0), (4, 0)), ((1, 7), (-3, 0), (5, 1))):
    A, B, C = [tuple(map(Rational, p)) for p in (A, B, C)]
    G = tuple((A[k] + B[k] + C[k]) / 3 for k in (0, 1))
    Pp = tuple((G[k] + A[k] + B[k]) / 3 for k in (0, 1)); Qq = tuple((G[k] + C[k] + A[k]) / 3 for k in (0, 1))
    assert area(A, B, C) / area(A, Pp, Qq) == Rational(27, 5)
R["m10"] = 30 * Rational(27, 5)
# m07: 내부 격자를 1/15 간격으로 모두 훑어 넓이 비가 4:5:6인 점을 찾는다
A, B, C = (2, 8), (-6, 0), (6, 0)
found = []
for i in range(-90, 91):
    for j in range(1, 120):
        Pq = (Rational(i, 15), Rational(j, 15))
        s1, s2, s3 = area(Pq, A, B), area(Pq, B, C), area(Pq, C, A)
        if s1 + s2 + s3 == area(A, B, C) and s1 * 5 == s2 * 4 and s3 * 5 == s2 * 6:
            found.append(Pq)
assert len(found) == 1
R["m07"] = 15 * (found[0][0] + found[0][1])

# 출처 비율 맞추기(2026-10-20)
# m06
cnt = 0
for a_ in range(1, 11):
    for b_ in range(1, 11):
        ok = any(Rational(-m_ + n_ * a_, m_ + n_) == 0 and Rational(-2 * m_ + n_ * b_, m_ + n_) == 0 for m_ in range(1, 25) for n_ in range(1, 25))
        col = (1 - b_) * (2 - a_) - (-2 - b_) * (-1 - a_) == 0
        cnt += ok and not col
R["m06"] = cnt
# n02
A = (-1, 4); M_ = (5, 1)
for B in ((3, 0), (8, -2)):
    C = (2 * M_[0] - B[0], 2 * M_[1] - B[1])
    D, E, F = inner(A, B, 2, 1), inner(B, C, 2, 1), inner(C, A, 2, 1)
    assert ((D[0] + E[0] + F[0]) / 3, (D[1] + E[1] + F[1]) / 3) == (3, 2)
R["n02"] = A[0] + A[1]
# m05: 좌표로 직접
C = (0, 0); B = (2, 0)
s_ = solve([x ** 2 + y ** 2 - 4, (x - 2) ** 2 + y ** 2 - 12], [x, y], dict=True)
A = [(q[x], q[y]) for q in s_ if q[y] > 0][0]
D = (1, 0)
assert simplify(dist(A, D) - sqrt(7)) == 0
E = inner(A, B, dist(C, A), dist(C, B))
Pp = ((A[0] + B[0] + C[0]) / 3, (A[1] + B[1] + C[1]) / 3)
Rr = inner(E, A, dist(Pp, E), dist(Pp, A))
Qq = inner(D, C, dist(Pp, D), dist(Pp, C))
# R, P, Q 한 직선 위
assert simplify((Rr[0] - Pp[0]) * (Qq[1] - Pp[1]) - (Rr[1] - Pp[1]) * (Qq[0] - Pp[0])) == 0
ratio = nsimplify(simplify(area(Pp, Qq, C) / area(Pp, Rr, E)), [sqrt(7)])
assert simplify(ratio - (8 - 2 * sqrt(7))) == 0
R["m05"] = 8 * (-2)
# m11: t를 촘촘히
A, B, C = (0, 4), (-3, 0), (4, -3)
best = 0
for i in range(1, 600):
    t_ = Rational(i, 1200)
    P_ = inner(A, C, t_, 1 - t_); Q_ = inner(B, C, t_, 1 - t_)
    R_ = inner(A, B, t_, 1 - t_); S_ = inner(B, A, t_, 1 - t_)
    ar = area(P_, R_, S_) + area(P_, S_, Q_)
    best = max(best, ar)
assert best == Rational(37, 6)
R["m11"] = 6 + 37
# m02v: 여러 A, C로
for A, C in (((3, 0), (0, 5)), ((1, -2), (4, 2)), ((-2, 1), (3, 1))):
    A, C = tuple(map(Rational, A)), tuple(map(Rational, C))
    if d2(A, C) != 25:
        continue
    B = (2, 5); O = (0, 0)
    P_, Q_, R_, S_ = inner(O, A, 2, 1), inner(A, B, 2, 1), inner(B, C, 2, 1), inner(C, O, 2, 1)
    assert d2(P_, R_) + d2(Q_, S_) == 30
R["m02v"] = 30

# k01: 2024년 9월 고1 20번 — 직선 PC가 넓이를 이등분하는지 직접 확인
a12 = 12
A, B, C, O = [tuple(map(Rational, p)) for p in ((-8, a12), (7, 3), (-6, 0), (0, 0))]
Pp = inner(A, B, 2, 1)
Qq = inner(C, Pp, 1, 1)
assert (Qq[0] - A[0]) * (O[1] - A[1]) - (Qq[1] - A[1]) * (O[0] - A[0]) == 0      # Q는 선분 AO 위
assert area(A, Qq, Pp) * 2 == area(A, O, B)
# 다른 양수 a로는 성립하지 않음(Q의 y좌표 조건이 a에 대한 일차식)
sol = solve(Rational(1, 4) * a - (a + 6) / 6, a)
assert sol == [12]
R["k01"] = a12

# 내신 기출(2026-10-20)
# s03
A_, B_ = symbols("A_ B_")
# 수직선으로: M=0, P=k (AP=6k, AM=5k) 그리고 좌표로 직접
M_ = Matrix([2, 1]); P_ = Matrix([5, 5])
u = (P_ - M_)                     # MP 방향, |MP| = k
A = M_ - 5 * u; B = M_ + 5 * u      # AM = BM = 5k
assert A + Rational(3, 5) * (B - A) == P_
R["s03"] = (B - A).norm()
# s02
A = (1, 3); B = (2 * -1 - 1, 2 * 1 - 3)
C = ((4 * 4 - 1) / Rational(3), (4 * 9 - 3) / Rational(3))
assert inner(A, C, 3, 1) == (4, 9)
G = ((A[0] + B[0] + C[0]) / Rational(3), (A[1] + B[1] + C[1]) / Rational(3))
R["s02"] = 3 * (G[0] + G[1])
# s01: 여러 a로 직접 B, C를 구해 확인
vals = set()
for a_ in (1, 2, -3, Rational(1, 2)):
    A = (4 * a_ + 3, 0)
    p_, q_ = symbols("p_ q_", real=True)
    B = (-2 * a_ + p_, 6 + q_); C = (-2 * a_ - p_, 6 - q_)
    sol = solve([d2(A, B) - d2(A, C), d2(B, C) - 4 * ((2 * a_ + 1) ** 2 + 4)], [p_, q_], dict=True)
    sol = [z for z in sol if z[p_] > 0]
    assert len(sol) == 1
    Bv = (B[0].subs(sol[0]), B[1].subs(sol[0])); Cv = (C[0].subs(sol[0]), C[1].subs(sol[0]))
    assert ((A[0] + Bv[0] + Cv[0]) / 3, (A[1] + Bv[1] + Cv[1]) / 3) == (1, 4)
    vals.add(simplify(Bv[0] + Bv[1]))
assert len(vals) == 1
R["s01"] = vals.pop()

# g052: y축 위의 점 Q에 대한 |AQ-BQ|의 최댓값(수치 탐색)과 그때의 y좌표
import math as _m
fa = lambda q: abs(_m.hypot(1, q - 4) - _m.hypot(2, q - 1))
best = max((fa(i / 1000), i / 1000) for i in range(-20000, 20001))
assert abs(best[1] - 7) < 1e-9 and abs(best[0] - _m.sqrt(10)) < 1e-9
R["g052"] = 7 ** 2 + 10

# ---------------------------------------------------------------- data01의 답과 맞추기
def to_expr(s):
    s = s.replace("LEFT (", "(").replace("RIGHT )", ")").replace("~", "").replace("it-", "-")
    s = re.sub(r"sqrt\s*\{([^{}]*)\}", r"sqrt(\1)", s)
    s = re.sub(r"\{([^{}]*)\}\s*over\s*\{([^{}]*)\}", r"((\1)/(\2))", s)
    s = re.sub(r"(\d)\s*sqrt", r"\1*sqrt", s).replace(" ", "")
    return s


import re
items = [it for _, _, ps in data01.TYPES for it in ps] + data01.STEP3
bad = 0
for it in items:
    got, ans = R[it["src"]], it["ans"]
    if it["src"] == "g031":
        same = ans.replace(" ", "") == "rmP,~B,~A,~C,~Q" and got == "PBACQ"
    elif isinstance(got, str):
        same = got == ans.replace(", ", "").replace(" ", "")
    elif it["src"] in ("012", "014"):
        lo, hi = (0, Rational(4, 9)) if it["src"] == "012" else (Rational(1, 5), Rational(4, 7))
        same = got.as_set() == Interval.open(lo, hi)
        if it["src"] == "012":
            same = same and ans.replace(" ", "") == "0<t<{4}over{9}"
        if it["src"] == "014":
            same = same and sympify(to_expr(ans)) == lo + hi
    elif it["src"] == "g024":
        same = ans.replace(" ", "") == "a=21,~b=120sqrt{2}" and got == (21, 120 * sqrt(2))
    elif isinstance(got, tuple):
        e = sympify(to_expr(ans))
        same = all(simplify(u - v) == 0 for u, v in zip(e, got))
    else:
        same = simplify(sympify(to_expr(ans)) - got) == 0
    if not same:
        bad += 1
    print(("OK  " if same else "BAD ") + it["src"], ans, "|", got)
print("문항", len(items), "불일치", bad)
