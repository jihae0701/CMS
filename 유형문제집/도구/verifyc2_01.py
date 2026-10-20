# 공통수학2 1단원(평면좌표) 유형서 문항 정답 독립 검산 (문항 기호는 c2unit01.py의 v).
# 좌표는 sympy로 풀고, 최솟값은 식을 직접 최소화하거나 촘촘한 수치 탐색으로, 개수·경우는 모두 훑어 확인한다.
from itertools import product
from sympy import Rational as Q, sqrt, symbols, solve, simplify, Abs, Matrix, nsimplify, minimum, Interval, expand
R = []
x, y, a, b, k, t, p, q, r = symbols("x y a b k t p q r", real=True)


def chk(no, got, exp):
    R.append((no, simplify(got - exp) == 0 if not isinstance(got, str) else got == exp, got, exp))


def d2(P, S):
    return (P[0] - S[0]) ** 2 + (P[1] - S[1]) ** 2


def div(P, S, m, n):
    """선분 PS를 m:n으로 내분하는 점"""
    from sympy import S as _S
    return (_S(m * S[0] + n * P[0]) / (m + n), _S(m * S[1] + n * P[1]) / (m + n))


def area(P, S, T):
    return Abs((S[0] - P[0]) * (T[1] - P[1]) - (S[1] - P[1]) * (T[0] - P[0])) / 2


def one(xs):
    assert len(xs) == 1, xs
    return xs[0]


def mark(truth, ch):
    pick = ", ".join(l for l, v in zip("ㄱㄴㄷㄹ", truth) if v)
    return "①②③④⑤"[ch.index(pick)]


BOGI = ["ㄱ", "ㄴ", "ㄱ, ㄴ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"]

# ---- 두 점 사이의 거리
chk("f9-1", sqrt(d2((-2, 4), (4, 2))), 2 * sqrt(10))
chk("g002", sum(solve(d2((4, -1), (0, 1)) - 4 * d2((0, 1), (1, a)), a)), 2)
# 수직선: 정수가 아닌 점까지 0.001 간격으로 훑어 길이를 잰다
pts = [i / 1000 for i in range(-10000, 10001) if abs(i / 1000 + 1) + abs(i / 1000 - 2) <= 7 + 1e-12]
chk("g019", nsimplify(round(max(pts) - min(pts), 6)), 7)
# ---- 두 점에서 같은 거리에 있는 점
xa = one(solve(d2((a, 0), (2, -1)) - d2((a, 0), (-3, 4)), a))
chk("g003", Abs(xa), 2)
sol = one(solve([b - (2 * a - 3), d2((a, b), (5, -2)) - d2((a, b), (2, 3))], [a, b], dict=True))
chk("g004", sol[a] + sol[b], 0)
px = one(solve(d2((a, 0), (4, 1)) - d2((a, 0), (-3, 2)), a))
py = one(solve(d2((0, b), (4, 1)) - d2((0, b), (-3, 2)), b))
chk("g023", sqrt(d2((px, 0), (0, py))), 10 * sqrt(2) / 7)
# ---- 삼각형의 모양
A, B, C = (-1, 1), (1, 4), (4, 2)
ab, bc, ca = d2(A, B), d2(B, C), d2(C, A)
shape = [ab == bc == ca, ab + ca == bc, ab == ca, ca == bc, ab == bc and ab + bc == ca]
chk("g005", "①②③④⑤"[shape.index(True)] if shape.count(True) == 1 else "?", "⑤")
s = [z for z in solve([d2((p, q), (-1, 1)) - d2((p, q), (1, -1)), d2((p, q), (-1, 1)) - 8], [p, q], dict=True) if z[p] > 0 and z[q] > 0]
chk("g006", one([z[p] + z[q] for z in s]), 2 * sqrt(3))
ks = []
for kv in range(-100, 101):
    A, B, C = (-1, 2), (1, kv), (3, 0)
    if area(A, B, C) == 0:
        continue
    if len({d2(A, B), d2(B, C), d2(C, A)}) < 3:
        ks.append(kv)
chk("w1", sum(ks), 4)
# ---- 삼각형의 외심
def circum(A, B, C):
    z = one(solve([d2((x, y), A) - d2((x, y), B), d2((x, y), A) - d2((x, y), C)], [x, y], dict=True))
    return (z[x], z[y])


O = circum((7, 1), (5, -3), (-1, 5))
chk("b039", sqrt(d2(O, (7, 1))), 5)
O = circum((2, 0), (0, 4), (4, 1))
chk("b040", O[0] * O[1], 5)
# 정삼각형: 외심이 원점, A(4, 3) → 나머지 두 꼭짓점은 A를 원점 중심으로 120°, 240° 돌린 점
import sympy
rot = Matrix([[sympy.cos(2 * sympy.pi / 3), -sympy.sin(2 * sympy.pi / 3)], [sympy.sin(2 * sympy.pi / 3), sympy.cos(2 * sympy.pi / 3)]])
vA = Matrix([4, 3]); vB = rot * vA; vC = rot * vB
S = simplify(area(tuple(vA), tuple(vB), tuple(vC)))
fr = nsimplify(S / sqrt(3))
chk("f2-13", fr.q + fr.p, 79)
# ---- 두 점 사이의 거리의 활용
f = d2((-1, 1), (t, t - 2)) + d2((1, 3), (t, t - 2))
chk("g020", min(f.subs(t, v) for v in solve(f.diff(t), t)), 20)
g = lambda av: float(sqrt(av ** 2 - 2 * av + 2) + sqrt(av ** 2 - 4 * av + 5))
mn = min(g(i / 2000) for i in range(-4000, 8000))     # 수치 최솟값이 √5와 같은지
chk("b067", sqrt(5) if abs(mn - 5 ** 0.5) < 1e-6 else nsimplify(mn), sqrt(5))
f = d2((0, 4 - 2 * t), (3 - t, 0))
chk("f3-17", one(solve(f.diff(t), t)) * 60, 132)
f = d2((2 * t, 2 * t), (-t, 10 - 2 * t))
tm = one(solve(f.diff(t), t))
chk("g045", tm * 60 + sqrt(f.subs(t, tm)), 102)
# ---- 선분의 내분점
P = div((1, -8), (4, -2), 2, 1)
chk("f3-3", P[0] - P[1], 7)
z = one(solve([div((a, 2), (2, b), 2, 1)[0] - 1, div((a, 2), (2, b), 2, 1)[1] - 4], [a, b], dict=True))
chk("f2-4", z[a] + z[b], 4)
Av, Bv = 0, 4
Pv = div((Av, 0), (Bv, 0), 3, 1)[0]
Qv = 2 * Av - Bv
chk("g012", Q(abs(Pv - Qv)) / abs(Bv - Av), Q(7, 4))
P = div((5, 3), (-4, 6), 2, 1)
chk("f8-14", area((1, 1), (5, 3), P), 10)
# 중점 M(2, 1), 3:2 내분점 P(5, 5) → A, B를 직접 구한다
z = solve([(x + p) / 2 - 2, (y + q) / 2 - 1, (3 * p + 2 * x) / 5 - 5, (3 * q + 2 * y) / 5 - 5], [x, y, p, q], dict=True)
z = one(z)
chk("f9-5", sqrt(d2((z[x], z[y]), (z[p], z[q]))), 50)
# ---- 선분의 내분점의 위치
from sympy import reduce_inequalities, And
Pk = div((3, -1), (-2, 5), k, 1 - k)
sol = reduce_inequalities([Pk[0] > 0, Pk[1] > 0, k > 0, k < 1], k)
lo, hi = sorted({v for v in [arg.rhs for arg in sol.args] + [arg.lhs for arg in sol.args] if v.is_number})
chk("f7-4", lo * hi, Q(1, 10))
P = div((2, 2), (10, 4), 1, k)
chk("g014", one([v for v in solve(P[1] - (2 * P[0] - 4), k) if v > 0]), 6)
vA = 1; vB = Q(3, 2); tB = Q(270) / vB
Rp, Qp, Pp = 30, 270, 30 + vA * tB
fr = Q(Pp - Rp) / (Qp - Pp)
chk("g038", fr.p - fr.q, 2)
# ---- 삼각형의 무게중심
z = one(solve([(2 + a - 1) / 3 - 3, (3 - 1 + b) / 3 - 2], [a, b], dict=True))
chk("f9-3", z[a] + z[b], 12)
# A(u, v), C(2-u, 4-v) (중점 (1, 2)), 무게중심 원점 → B
u, v = symbols("u v")
Bx = -(u + 2 - u); By = -(v + 4 - v)
chk("f6-7", Bx + By, -6)
A, B, C = (-1, 1), (2, 5), (5, -3)
D, E, F = div(A, B, 1, 2), div(B, C, 1, 2), div(C, A, 1, 2)
chk("g018", (D[0] + E[0] + F[0]) / 3 + (D[1] + E[1] + F[1]) / 3, 3)
# 세 넓이가 같은 내부의 점: 직접 연립
O_, A_, B_ = (0, 0), (2, 1), (1, 5)
tot = area(O_, A_, B_)
z = [w for w in solve([((A_[0] - x) * (O_[1] - y) - (A_[1] - y) * (O_[0] - x)) / 2 - tot / 3,
                       ((B_[0] - x) * (A_[1] - y) - (B_[1] - y) * (A_[0] - x)) / 2 - tot / 3], [x, y], dict=True)]
z = one(z)
chk("b045", z[x] + z[y] + 2 * area((z[x], z[y]), A_, B_), 6)
# 임의의 B, C 한 쌍을 만들어 조건을 맞춘다: xB+xC=6, yB+yC=0
for Bt in [(1, 2), (-4, 7)]:
    Ct = (6 - Bt[0], 0 - Bt[1])
    M, N = ((3 + Bt[0]) / Q(2), (-1 + Bt[1]) / Q(2)), ((3 + Ct[0]) / Q(2), (-1 + Ct[1]) / Q(2))
    assert M[0] + N[0] == 6 and M[1] + N[1] == -1
    G = ((3 + Bt[0] + Ct[0]) / Q(3), (-1 + Bt[1] + Ct[1]) / Q(3))
chk("g039", G[0] + G[1], Q(8, 3))
# ---- 평행사변형과 마름모
z = one(solve([(1 + 3) - (b + 5), (a - 2) - (0 + 4)], [a, b], dict=True))
chk("g017a", z[a] + z[b], 5)
z = [w for w in solve([(1 + q) - (p + 6), (-1 + r) - 10, d2((1, -1), (p, 6)) - d2((1, -1), (6, 4))], [p, q, r], dict=True)
     if w[p] > 0 and w[q] > 0 and w[r] > 0]
w = one(z)
# 마름모인지(네 변이 같음) 확인
Av, Bv, Cv, Dv = (1, -1), (w[p], 6), (w[q], w[r]), (6, 4)
assert len({d2(Av, Bv), d2(Bv, Cv), d2(Cv, Dv), d2(Dv, Av)}) == 1
chk("g017b", w[p] + w[q] + w[r], 20)
# ---- 각의 이등분선과 내심


def incenter(A, B, C):
    la, lb, lc = sqrt(d2(B, C)), sqrt(d2(C, A)), sqrt(d2(A, B))
    s_ = la + lb + lc
    return ((la * A[0] + lb * B[0] + lc * C[0]) / s_, (la * A[1] + lb * B[1] + lc * C[1]) / s_)


A, B, C = (-1, 2), (3, 5), (-3, -3)
ratio = sqrt(d2(B, A)) / sqrt(d2(B, C))        # AD:DC = BA:BC
D = div(A, C, sqrt(d2(B, A)), sqrt(d2(B, C)))
fr = nsimplify(area(D, A, B) / area(D, B, C))
chk("b018", fr.p ** 2 + fr.q ** 2, 5)
I = incenter((0, 0), (6, 0), (3, 4))
chk("b042", simplify(I[0] + I[1]), Q(9, 2))
I = incenter((0, 0), (2, 2 * sqrt(3)), (4, 0))
chk("b043", simplify(I[0] ** 2 + I[1] ** 2), Q(16, 3))
# ---- 중선정리 (좌표로 직접)
# g016: B(x1, y1), C = 3G - A - B → AB²=58, AC²=10
x1, y1 = symbols("x1 y1")
Cx, Cy = 12 - 6 - x1, 3 - 3 - y1
zs = solve([d2((6, 3), (x1, y1)) - 58, d2((6, 3), (Cx, Cy)) - 10], [x1, y1], dict=True)
chk("g016", one(list({simplify(sqrt(d2((z[x1], z[y1]), (Cx.subs(z), Cy.subs(z))))) for z in zs})), 8)
# b052: G 원점, A, B, C 합 0, |A|=4, |B|=6, |C|=8 → BC
# A = -(B+C)이므로 |B+C|² = 16, |B|²=36, |C|²=64 → B·C = (16-100)/2, |B-C|² = 100 - 2B·C
BC2 = 100 - (16 - 100)
chk("b052", sqrt(BC2), 2 * sqrt(46))
z = [w for w in solve([x ** 2 + y ** 2 - 5, (x - 1) ** 2 + y ** 2 - 8], [x, y], dict=True) if w[y] > 0]
w = one(z)
A, B, C, D = (w[x], w[y]), (-2, 0), (2, 0), (1, 0)
t1 = len({d2(A, B), d2(B, D), d2(D, A)}) < 3
t2 = d2(A, C) - d2(A, B) == 8
t3 = area(A, B, C) == 4
chk("b055", mark([t1, t2, t3], BOGI), "④")
# ---- 중선정리의 확장
z = [w for w in solve([x ** 2 + y ** 2 - 15, (x + t) ** 2 + y ** 2 - 25, (x - 3 * t) ** 2 + y ** 2 - 9], [x, y, t], dict=True) if w[t] > 0]
chk("g029", one(list({4 * w[t] for w in z})), 4 * sqrt(2))
s_ = symbols("s", positive=True)
lhs = 3 * (x ** 2 + y ** 2) + 9 * s_ ** 2
rhs = (x + 3 * s_) ** 2 + y ** 2 + 3 * ((x - s_) ** 2 + y ** 2)
chk("g030", simplify(lhs / rhs), Q(3, 4))
# ---- 거리의 제곱의 합의 최솟값
f = d2((x, y), (1, -1)) + d2((x, y), (-3, 4)) + d2((x, y), (5, 6))
z = one(solve([f.diff(x), f.diff(y)], [x, y], dict=True))
chk("g021", z[x] + z[y] + f.subs(z), 62)
kk = 3     # AB:BC = 2:3 → A(-2), B(0), C(3)
f = (x + 2) ** 2 + x ** 2 + (x - 3) ** 2
xm = one(solve(f.diff(x), x))
fr = Q(xm - 0) / (3 - xm)
chk("g037", fr.p + fr.q, 9)
# ---- 삼각형의 넓이의 비
A, B, C = (2, 3), (7, 1), (4, 5)
cands = []
for lam in [Q(2, 5), -Q(2, 5)]:
    D = (A[0] + lam * (B[0] - A[0]), A[1] + lam * (B[1] - A[1]))
    E = (A[0] + lam * (C[0] - A[0]), A[1] + lam * (C[1] - A[1]))
    if D[0] > A[0] and area(A, B, C) / area(A, D, E) == Q(25, 4):
        cands.append(D[0] + D[1])
chk("g035", one(cands), Q(31, 5))
Av, Bv = Q(0), Q(4)
Pv = div((Av, 0), (Bv, 0), 3, 1)[0]
Qv = one(solve((2 * x + 1 * Av) / 3 - Bv, x))
Cpt = (1, 5)       # 직선 밖의 점
t1 = (Av + Qv) / 2 == Pv
t2 = 3 * (Bv - Av) == 2 * (Qv - Av)
t3 = area((Av, 0), (Bv, 0), Cpt) / area((Pv, 0), (Qv, 0), Cpt) == Q(4, 3)
chk("g040", mark([t1, t2, t3], BOGI), "⑤")
# ---- 고난도
O_, A_, B_ = (0, 0), (6, 2), (-2, 4)
P = [(lam * 6, lam * 2) for lam in [Q(1, 2), -Q(1, 2)] if lam > 0][0]
assert area(O_, P, B_) == area(O_, A_, B_) / 2
Qs = [(m * -2, m * 4) for m in [Q(3, 2), -Q(3, 2)] if m * -2 < 0 and m * 4 > 0]
Qp = one(Qs)
assert area(O_, P, Qp) == Q(3, 2) * area(O_, P, B_)
chk("g044v", sqrt(d2(P, Qp)), sqrt(61))
A, B, C = (0, 6), (-3, 0), (6, 0)
sg = lambda P, S, T: ((S[0] - P[0]) * (T[1] - P[1]) - (S[1] - P[1]) * (T[0] - P[0])) / 2   # 부호 있는 넓이
tot = sg(A, B, C)      # 내부의 점이면 세 삼각형도 같은 방향(같은 부호)
w = one(solve([sg((x, y), A, B) - tot / 6, sg((x, y), B, C) - 2 * tot / 6], [x, y], dict=True))
Pp = (w[x], w[y])
assert [area(Pp, A, B), area(Pp, B, C), area(Pp, C, A)] == [abs(tot) / 6, 2 * abs(tot) / 6, 3 * abs(tot) / 6]
chk("w2", Pp[0] + Pp[1], Q(3, 2))
sq = symbols("sq", positive=True)
res = []
for z in solve([x ** 2 + y ** 2 - 10, (x - sq) ** 2 + y ** 2 - 18, x ** 2 + (y - sq) ** 2 - 2], [x, y, sq], dict=True):
    if 0 < z[x] < z[sq] and 0 < z[y] < z[sq]:
        res.append(z[sq] ** 2)
chk("w3", one(res), 16)
# w4: 임의의 삼각형 두 개로 넓이비 확인
for A, B, C in [((0, 0), (5, 1), (2, 7)), ((-3, 2), (4, -1), (1, 6))]:
    G = ((A[0] + B[0] + C[0]) / Q(3), (A[1] + B[1] + C[1]) / Q(3))
    cen = lambda U, V, W: ((U[0] + V[0] + W[0]) / Q(3), (U[1] + V[1] + W[1]) / Q(3))
    Pp, Qp, Rp = cen(G, B, C), cen(G, C, A), cen(G, A, B)
    rat = area(A, B, C) / area(Pp, Qp, Rp)
    assert rat == 9
chk("w4", 4 * rat, 36)
# b060: 임의의 삼각형 세 개로 k, l을 풀어 확인
kk_, ll_ = symbols("kk ll")
eqs = []
for A, B, C in [((0, 5), (-2, 0), (3, 0)), ((1, 1), (6, 2), (2, 7)), ((0, 0), (4, 0), (1, 3))]:
    G = ((A[0] + B[0] + C[0]) / Q(3), (A[1] + B[1] + C[1]) / Q(3))
    eqs.append(d2(A, B) + d2(A, C) + kk_ * d2(B, C) - ll_ * (d2(B, G) + d2(C, G)))
z = one(solve(eqs, [kk_, ll_], dict=True))
chk("b060", z[kk_] + z[ll_], 13)
# g041: 임의의 삼각형
A, B, C = (1, 4), (0, 0), (5, 1)
D = div(B, C, 1, 3)
E = (B[0] - 2 * (C[0] - B[0]), B[1] - 2 * (C[1] - B[1]))      # B가 EC를 2:1로 내분 → EB = 2BC
assert div(E, C, 2, 1) == (Q(B[0]), Q(B[1]))
F = (2 * A[0] - B[0], 2 * A[1] - B[1])
chk("g041", area(F, E, B) / area(A, B, D), 16)
# f6-16: a를 풀어 직선 PC가 넓이를 이등분하는지 직접 확인
av = symbols("av", positive=True)
A, B, C, O_ = (-8, 3), (12, av), (9, 0), (0, 0)
P = div(A, B, 1, 3)
# 직선 PC와 선분 OB의 교점 Q = (12m, av m): 세 점 P, Q, C가 한 직선 → 행렬식 0
m = symbols("m")
Qp = (12 * m, av * m)
col = (Qp[0] - P[0]) * (C[1] - P[1]) - (Qp[1] - P[1]) * (C[0] - P[0])
# 넓이 조건은 부호를 피하려고 수치로 확인: 후보 a에서 직선 PC가 넓이를 반으로 나누는지
av0 = Q(45, 11)
Pn = div(A, (12, av0), 1, 3)
mm = one([w for w in solve(((12 * m) - Pn[0]) * (0 - Pn[1]) - ((av0 * m) - Pn[1]) * (9 - Pn[0]), m) if 0 < w < 1])
Qn = (12 * mm, av0 * mm)
assert area(Pn, (12, av0), Qn) == area(A, O_, (12, av0)) / 2
# a가 하나뿐인지: 넓이 이등분 조건 BQ:BO = 2:3 → m = 1/3, 세 점이 한 직선 → a
a_sol = one(solve((((12 * Q(1, 3)) - P[0]) * (C[1] - P[1]) - ((av * Q(1, 3)) - P[1]) * (C[0] - P[0])), av))
chk("f6-16", 11 * a_sol, 45)
# g053: A, D의 높이 4/c, 6/c (c = BC)
c = 3
A, D, B, C = (Q(1), Q(4, c)), (Q(2), Q(6, c)), (0, 0), (c, 0)
assert area(A, B, C) == 2 and area(D, B, C) == 3
E = div(A, D, 3, 1)
chk("g053", area(E, B, C), Q(11, 4))
B, C = (0, 0), (6, 0)
z = [w for w in solve([x ** 2 + y ** 2 - 40, (x - 6) ** 2 + y ** 2 - 52], [x, y], dict=True) if w[y] > 0]
A = (one(z)[x], one(z)[y])
def Pmn(m_, n_):
    return div(B, C, m_, n_)
t1 = d2(A, Pmn(1, 1)) == 37
# ㄴ, ㄷ: 서로소인 m:n을 훑는다
from math import gcd
pairs = [(m_, n_) for m_ in range(1, 60) for n_ in range(1, 60) if gcd(m_, n_) == 1]
ab_ = [(m_, n_) for m_, n_ in pairs if d2(A, Pmn(m_, n_)) == d2(A, B)]
t2 = all(m_ - n_ == 3 for m_, n_ in ab_) and len(ab_) > 0
ap_ = [(m_, n_) for m_, n_ in pairs if d2(A, Pmn(m_, n_)) == 45]
t3 = all(m_ + 2 * n_ == 7 for m_, n_ in ap_) and len(ap_) > 0
chk("g050", mark([t1, t2, t3], ["ㄱ", "ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"]), "③")
areas = []
for av_, bv_ in product(range(1, 6), repeat=2):
    # y축이 선분 AB를, x축이 선분 AC를 같은 m:n으로 내분하는 자연수 m, n이 있는지 (내분점의 x좌표, y좌표가 0)
    okk = any(div((av_, bv_), (-2, 1), m_, n_)[0] == 0 and div((av_, bv_), (1, -2), m_, n_)[1] == 0
              for m_ in range(1, 30) for n_ in range(1, 30))
    if okk:
        areas.append(area((av_, bv_), (-2, 1), (1, -2)))
chk("g049", max(areas) - min(areas), 12)
# f7-17: a를 여러 값으로 두고 B를 직접 구한다
for aval in [Q(1), Q(-2), Q(1, 3)]:
    xb, yb = symbols("xb yb")
    A = (4 * aval, 1)
    xc, yc = 0 * 3 - A[0] - xb, 9 - A[1] - yb
    zs = solve([d2(A, (xb, yb)) - d2(A, (xc, yc)), d2((xb, yb), (xc, yc)) - 36 * (4 * aval ** 2 + 1)], [xb, yb], dict=True)
    zs = [w for w in zs if w[xb] > xc.subs(w)]
    w = one(zs)
    val = 3 * w[xb] + w[yb]
    assert simplify(val - 13) == 0, (aval, val)
chk("f7-17", val, 13)
# g051: G를 원점, B, C를 놓고 A = -(B+C)
xb, yb, xc_, yc_ = symbols("xb yb xc yc", real=True)
B = (2 * sqrt(3), 0)
zs = solve([xc_ ** 2 + yc_ ** 2 - 20, (B[0] + xc_) ** 2 + yc_ ** 2 - 32], [xc_, yc_], dict=True)
w = [w for w in zs if w[yc_] > 0][0]
C = (w[xc_], w[yc_])
A = (-(B[0] + C[0]), -(B[1] + C[1]))
chk("g051", simplify(area(A, B, C)), 6 * sqrt(15))

if __name__ == "__main__":
    bad = [r_ for r_ in R if not r_[1]]
    for r_ in bad:
        print("MISMATCH", r_)
    print("검산", len(R), "불일치", len(bad))
