# -*- coding: utf-8 -*-
"""기본서 12단원 정답 검산: 행렬을 직접 계산해(sympy) data12의 답과 맞춘다.  python verify12.py
- 조건만 주어진 문항(04, STEP 3 A²+A³)은 조건을 만족시키는 행렬을 실제로 만들어 계산하거나, 다항식의 나머지로 확인한다.
- ㄱㄴㄷ은 반례를 계산하고, 참인 명제는 조건을 만족시키는 행렬을 여러 개 만들어 확인한다."""
import sys, os, random
from itertools import product
from sympy import Matrix, Rational, eye, zeros, symbols, solve, expand, rem, sqrt, I, simplify, nsimplify
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data12
from data12 import M

E, O = eye(2), zeros(2)
ans = []


def total(A):
    return simplify(sum(A))


def mstr(A):
    return M(*[tuple(int(A[i, j]) for j in range(A.cols)) for i in range(A.rows)])


def frac(v):
    v = nsimplify(v)
    return str(v) if v.q == 1 else "{%d} over {%d}" % (v.p, v.q)


def eform(A):
    """kE 꼴이면 '-E', '-2E' 등"""
    k = A[0, 0]
    assert A == k * E
    return {1: "E", -1: "-E"}.get(k, "%dE" % k)


def choose(truth, ch):
    pick = ", ".join(l for l, t in zip("ㄱㄴㄷ", truth) if t)
    return "①②③④⑤"[ch.index(pick)]


def ch_of(it):
    return next(p["ch"] for p in it["q"] if isinstance(p, dict) and "ch" in p)


# 01
k = symbols("k")
a = lambda i, j, kk: 2 * i + j + kk
kv = solve(a(1, 2, k) + a(2, 2, k) - 8, k)[0]
ans.append(sum(a(1, j, kv) for j in (1, 2, 3)))
ans.append((2 * 2 + 1 - 3) + (1 - 2 * 2))
# 02
A = Matrix([[1, 2], [0, 1]]); B = A - Matrix([[1, 0], [1, -1]])
ans.append(total(A * A - A * B))
P1, P2 = Matrix([[4, 2], [1, 3]]), Matrix([[0, 2], [5, -1]])
A, B = (P1 + P2) / 2, (P1 - P2) / 4
ans.append((A * B + B * A)[1, 0])
x, y = symbols("x y")
A, B = Matrix([[4, 3], [1, 2]]), Matrix([[1, 2], [x, y]])
sol = solve(list(A * A + B * B - A * B - B * A), [x, y], dict=True)
assert len(sol) == 1
ans.append(sol[0][x] + sol[0][y])
S = Matrix([[5, 0], [Rational(3, 2), 1]]) + Matrix([[-4, 0], [Rational(-1, 2), 0]])     # (A+B)^2
ans.append(total(S * S))
# 03
A = Matrix(2, 2, lambda i, j: i - j)
n1 = next(n for n in range(1, 20) if A ** n == E)
s = zeros(2)
for n in range(1, 2027):
    s += A ** (n % 4 or 4)
ans.append("⑴ $%d$ ⑵ $%d$" % (n1, total(s)))
A = Matrix([[1, 0], [1, 1]])
ans.append(next(n for n in range(1, 30) if sum((A ** n).LUsolve(Matrix([3, 8]))) == 2))
# 04: A+B=-E, AB=E인 실제 행렬(A는 120° 회전, B=-E-A)
R = lambda t: Matrix([[t[0], -t[1]], [t[1], t[0]]])
A = R((Rational(-1, 2), sqrt(3) / 2)); B = -E - A
assert simplify(A * B - E) == O
s = sum((simplify(A ** n + B ** n) for n in range(1, 101)), zeros(2))
ans.append(eform(simplify(s)))
A = R((Rational(1, 2), sqrt(3) / 2)); B = E - A       # A+B=E, AB=E (60° 회전)
assert simplify(A * B - E) == O
ans.append("⑴ $%s$ ⑵ $%s$ ⑶ $%s$" % tuple(eform(simplify(A ** n + B ** n)) for n in (2, 3, 100)))
# 05
a_, x_, z_, y_, w_ = symbols("a x z y w")
A = Matrix([[1, 1], [a_, a_]]); B = Matrix([[x_, z_], [y_, w_]])
eqs = list(B * Matrix([1, -1])) + list(A * B - 2 * A) + list(B * A - 4 * B)
vals = set()
for s_ in solve(eqs, [a_, x_, z_, y_, w_], dict=True):
    Bs = B.subs(s_)
    if Bs != O:
        C = (A + Bs).subs(s_)
        vals.add(simplify(C[0, 1] + C[1, 0]))
assert len(vals) == 1, vals
ans.append(vals.pop())
v = 2 * Matrix([4, 3]) - Matrix([2, 1])                      # A(4,3)=A²(2,1)=(2A-E)(2,1)
p_, q_, r_, s2 = symbols("p q r s")
A = Matrix([[p_, q_], [r_, s2]])
cond = list(A * A - 2 * A + E) + list(A * Matrix([2, 1]) - Matrix([4, 3]))
for s_ in solve(cond, [p_, q_, r_, s2], dict=True):            # 실제 행렬로도 확인
    assert list(A.subs(s_) * Matrix([4, 3])) == list(v)
ans.append(v[0] - v[1])
# 06
A, B = Matrix([[3000, 1200], [3500, 1000]]), Matrix([[3, 3], [4, 5]])
AB = A * B
assert AB[0, 0] < AB[1, 0] and AB[0, 1] < AB[1, 1]
ans.append("⑴ $" + mstr(AB) + "$ ⑵ 두 사람 모두 편의점 $rm P$")
A, B = Matrix([[450, 350], [400, 500]]), Matrix([[8000, 9000], [10000, 12000]])
tgt = 450 * 9000 + 350 * 12000
ij = [(i, j) for i in range(2) for j in range(2) if (A * B)[i, j] == tgt]
assert ij == [(0, 1)]
ans.append(10 * (ij[0][0] + 1) + ij[0][1] + 1)
# 07
it7 = data12.TYPES[6][2]


def rnd(lo=-3, hi=3):
    return Matrix(2, 2, lambda i, j: random.randint(lo, hi))


random.seed(1)
N = Matrix([[1, 1], [-1, -1]])
t1 = not (N * N == O and N != O)
A0, B0, C0 = Matrix([[1, 0], [0, 0]]), Matrix([[0, 0], [1, 0]]), O
t2 = not (A0 != O and A0 * B0 == A0 * C0 and B0 != C0)
t3 = True
for _ in range(200):
    A = rnd(); B = A * A - 2 * A + 3 * E       # A와 교환되는 B
    assert A * B == B * A
    t3 &= all(A ** n * B == B * A ** n for n in range(1, 6))
ans.append(choose((t1, t2, t3), ch_of(it7[0])))
u1 = True
for _ in range(300):
    A, B = rnd(), rnd()
    if (A + B) * (A - B) == A * A - B * B:
        u1 &= (A + B) ** 2 == A * A + 2 * A * B + B * B
A0, B0 = Matrix([[1, -1], [0, -1]]), Matrix([[1, 2], [0, -1]])
u2 = not (A0 * A0 == B0 * B0 and A0 != B0 and A0 != -B0)
J = Matrix([[0, -1], [1, 0]])
u3 = J * J + E == O
ans.append(choose((u1, u2, u3), ch_of(it7[1])))
# 08
p, q = symbols("p q")
A = Matrix([[2, 3], [1, 1]])
sp = solve(list(A * A - p * A - q * E), [p, q], dict=True)[0]
ans.append("⑴ $p=%d$, $q=%d$ ⑵ $%s$" % (sp[p], sp[q], mstr(A ** 3 - 2 * A ** 2 + 5 * A - 6 * E)))
a, b = symbols("a b")
A = Matrix([[a, b], [1, -3]])
sab = solve(list(A * A + A - 6 * E), [a, b], dict=True)
assert len(sab) == 1
A = A.subs(sab[0])
ans.append("⑴ $%d$ ⑵ $%s$" % (sab[0][a] + sab[0][b], mstr(A ** 3 + 2 * A ** 2 - 3 * A - 6 * E)))

# STEP 3
s3 = solve([3 + a + b + 6 - 13, 3 - a + b - 6 - 15], [a, b])
ans.append(s3[a] * s3[b])
shapes = {"A": (1, 3), "B": (3, 2), "C": (2, 1)}


def defined(w):
    r, c = shapes[w[0]]
    for ch in w[1:]:
        r2, c2 = shapes[ch]
        if c != r2:
            return False
        c = c2
    return True


ans.append(sum(defined(w) for w in ("AB", "BC", "CA", "ABC", "CBA")))
A = Matrix([[x, 2], [-2, 3]]); B = Matrix([[-4, -3 * x + 1], [-4, x + 5]])
xs = [v for v in solve((A * B - B * A)[1, 0], x) if (A * B - B * A).subs(x, v) == O]
assert len(xs) == 1
ans.append(xs[0])
av = [v for v in solve(3 - 2 * a, a) if 2 - 7 * v != 0]       # (3-2a)y=2-7a에 해가 없을 조건
for v in av:
    assert Matrix([[v, 3], [1, 2]]).det() == 0
ans.append(frac(av[0]))
al = Rational(-1, 2) + sqrt(3) / 2 * I
assert simplify(al ** 3 - 1) == 0
A = Matrix([[al, 2], [-1, al]])
ans.append(simplify(expand(sum(A * A))))
P1, P2 = Matrix([[1, -1], [4, 5]]), Matrix([[1, -1], [2, 3]])
A, B = (P1 + P2) / 2, (P1 - P2) / 2
ans.append(total(A * A - B * B))
A = Matrix([[-2, 5], [-1, 2]])
ans.append(next(n for n in range(1, 50) if A ** n + A == Matrix([[-1, 5], [-1, 3]])))
X = Matrix([[3, 1], [1, 2]])          # 열이 (3p,q)/p, (p,2q)/q 꼴: A·diag(p,q)·X = [[2,4],[-3,5]]
AD = Matrix([[2, 4], [-3, 5]]) * X.inv()      # A·diag(p,q)
v = AD * Matrix([1, 1])
ans.append(frac(v[0] * v[1]))
A = Matrix([[0, -1], [1, 0]])
ans.append(sum(1 for m in range(1, 41) for n in range(1, m) if A ** m == A ** n))
A = Matrix([[-1, 0], [2, 3]])
ans.append(solve(list(A * A - 2 * A + k * E), k)[0] if isinstance(solve(list(A * A - 2 * A + k * E), k), list) else solve(list(A * A - 2 * A + k * E), k)[k])
t = symbols("t")
r_ = rem(t ** 4 + t ** 5, t ** 3 + t ** 2 + 3 * t + 3, t)       # A^3+A^2+3A+3E=O로 낮춘 나머지
assert expand(r_ - (9 * t + 9)) == 0
ans.append(9 * 0 + 9 * 2)
it_last = data12.STEP3[11]
Z = Matrix([[0, 1], [1, 0]])
v1 = not (Z * Z == E and Z != E and Z != -E)
v2 = True
for _ in range(100):
    th = random.choice([Matrix([[1, 0], [0, -1]]), Matrix([[0, 1], [1, 0]]), Matrix([[1, 2], [0, -1]]), Matrix([[-1, 0], [3, 1]])])
    Bm = random.choice([Matrix([[1, 0], [0, 0]]), Matrix([[1, 1], [0, 0]]), Matrix([[0, 0], [2, 1]]), E, O])
    assert th * th == E and Bm * Bm == Bm
    v2 &= (th * Bm * th) ** 3 == th * Bm * th
v3 = True
for _ in range(100):
    A = rnd()
    if A.det() == 0:
        continue
    B = A.inv()                        # BA=E인 B (확인용으로만 역행렬 사용)
    if A * (A + B) == 2 * E:
        v3 &= A == B
ans.append(choose((v1, v2, v3), ch_of(it_last)))
P_, Q_ = Matrix([[220, 210], [250, 230]]), Matrix([[Rational(2, 5), Rational(3, 5)], [Rational(1, 2), Rational(1, 2)]])
kk = 250 * Rational(2, 5) + 230 * Rational(1, 2)
ij = [(i, j) for i in range(2) for j in range(2) if (P_ * Q_)[i, j] == kk]
assert ij == [(1, 0)]
ans.append(10 * 2 + 1 + kk)

items = [p for _, _, ps in data12.TYPES for p in ps] + data12.STEP3
assert len(items) == len(ans), (len(items), len(ans))
bad = 0
for no, (it, v) in enumerate(zip(items, ans), 428):
    if str(v) != it["ans"]:
        bad += 1
        print("불일치", no, it["ans"], v)
print("문항", len(items), "불일치", bad)
