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
    if isinstance(got, str):
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
