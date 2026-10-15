# 12단원(행렬) 유형서 문항 정답 독립 검산 (문항 기호는 unit12.py의 v). sympy로 행렬을 직접 계산한다.
# 조건만 주어진 문항은 연립방정식을 풀거나 정수 범위를 모두 훑고, ㄱㄴㄷ은 반례 계산과 무작위 행렬로 확인한다.
import random
from sympy import Matrix, Rational, eye, zeros, symbols, solve, sqrt, simplify, prod, divisors, nsimplify
R = []
E, O = eye(2), zeros(2)
x, y, a, b, c, d, k, p, q, r, s = symbols("x y a b c d k p q r s")


def chk(no, got, exp):
    R.append((no, got == exp, got, exp))


def one(xs):
    assert len(xs) == 1, xs
    return xs[0]


def mul(X, Y):
    return (X[0] * Y[0] + X[1] * Y[2], X[0] * Y[1] + X[1] * Y[3], X[2] * Y[0] + X[3] * Y[2], X[2] * Y[1] + X[3] * Y[3])


def rnd():
    return Matrix(2, 2, lambda i, j: random.randint(-3, 3))


def mark(truth, ch):
    pick = ", ".join(l for l, t in zip("ㄱㄴㄷㄹ", truth) if t)
    return "①②③④⑤"[ch.index(pick)]


random.seed(7)
# ---- 행렬의 성분
xs = solve(4 + 0 + 3 - (8 + 3 + 2 * x), x)
chk("n539", 1 + (3 * one(xs) - 1) + 8, 2)
A = Matrix(2, 2, lambda i, j: (lambda D: 2 if D > 0 else (1 if D == 0 else 0))((i + 1 + 4 * (j + 1)) ** 2 - 36))
chk("n722", sum(A), 5)
A = Matrix(2, 2, lambda i, j: 2 * (i + 1) - (j + 1) if i >= j else -(2 * (j + 1) - (i + 1)))
chk("n401", A[0, 1] + A[1, 1], -1)
A = Matrix([[2, -1], [-3, 1]])
B = Matrix(2, 2, lambda i, j: (-1) ** (i + j) * A[j, i])
chk("o12", B[0, 1] + B[1, 1], 4)
# ---- 서로 같은 행렬
so = one(solve(list(Matrix([[a * x - 3 * b, -1], [2 * a * x + 9 * b, 1]]) - Matrix([[-7, 2 * a - 5 * b], [1, -a + 3 * b]])), [a, b, x], dict=True))
chk("n366", so[a] + so[b] + so[x], 1)
vals = {simplify(z[x] ** 3 + z[y] ** 3) for z in solve([x + y - 8, x * y - 8], [x, y], dict=True)}
chk("n943", one(list(vals)), 320)
vals = {simplify(z[a] * z[b]) for z in solve([a ** 2 - (32 - b ** 2), -b - (a - 6)], [a, b], dict=True)}
chk("o13", one(list(vals)), 2)
L = Matrix([[2, x], [5, y]]) * Matrix([[y, 3], [x, y]])
Rm = Matrix([[1, 9], [x * y, y ** 2]]) - Matrix([[-2, 2], [-5 * y, -15]])
so = [z for z in solve(list(L - Rm), [x, y], dict=True) if z[y].is_real and z[y] < 0]
chk("n813", one([z[x] - z[y] for z in so]), Rational(-3, 2))
# ---- 덧셈, 뺄셈, 실수배
so = one(solve(list(2 * Matrix([[a, 2 * a], [-1, 3 * a]]) + 3 * Matrix([[-2, 1], [b, b / 2]]) - Matrix([[x, 7], [10, y]])), [a, b, x, y], dict=True))
chk("n853", so[x] + so[y], 8)
so = one(solve(list(x * Matrix([[1, -2], [-2, 1]]) + y * Matrix([[3, -4], [-4, 3]]) - 2 * E), [x, y], dict=True))
chk("n589", so[x] + so[y], -2)
A = Matrix([[3, -2], [1, 0]]) - 3 * E
B = A - Matrix([[1, 0], [-3, 2]])
chk("n658", sum(A - 2 * B), 4)
S, D = Matrix([[5, 5], [2, -2]]), Matrix([[1, 5], [-4, 6]])
A, B = (S + D) / 2, (S - D) / 2
T = 3 * A + 2 * B
chk("o15", T[0, 1] - T[1, 1], 17)
# ---- 곱셈
chk("n161", sum(Matrix([[1, 2, 3], [3, 6, 9], [15, 30, 45]]) * Matrix([2, 4, 4])), 418)
so = one(solve(list(Matrix([[-1, a], [c, -2]]) * Matrix([[4, b], [2, 3]])), [a, b, c], dict=True))
chk("n417", so[a] + so[b] + so[c], 9)
A = Matrix([[a, 0], [0, b]]); B = Matrix([[2, 3], [1, 0]]); C = Matrix([[2, 9], [1, -2]])
so = one(solve(list(A * B - A - B - C), [a, b], dict=True))
chk("n287", so[a] + so[b], 6)
f = sum(Matrix([[x, 1], [1, 2]]) * Matrix([[-x, 3], [4, -2]]))
chk("o18", max(f.subs(x, Rational(t, 100)) for t in range(-500, 501)), 10)
# ---- 교환법칙
A = Matrix([[9, -1], [2, 3]]); B = Matrix([[2, a], [1, -1]])
av = one(solve(list(A * B - B * A), [a], dict=True))[a]
chk("n910", av + sum((B ** 2).subs(a, av)), 4)
A = Matrix([[1, x], [3, -1]]); B = Matrix([[1, 2], [-3, y]])
so = one(solve(list(A * B - B * A), [x, y], dict=True))
chk("o17", so[x] + 2 * so[y], 4)
A = Matrix([[a, -2], [2, -1]]); B = Matrix([[a + 2, 1], [-a, 0]])
chk("n833", one([v for v in range(-20, 21) if (A * B - B * A).subs(a, v) == 8 * Matrix([[0, 1], [1, 0]])]), 1)
best = None
for xv in range(-30, 31):
    for yv in range(-30, 31):
        A = Matrix([[-3, xv * yv - xv], [3, 0]]); B = Matrix([[1, yv], [-1, 0]])
        if (A + B) * (A - B) == A * A - B * B:
            best = xv * yv if best is None else max(best, xv * yv)
chk("n484", best, 4)
# ---- 곱셈에 대한 성질
AB, B = Matrix([[4, 1], [2, 3]]), Matrix([[1, -1], [0, 2]])
chk("o22", sum(AB * B - 3 * B), 2)
# n798: B를 일반 행렬로 두고 (가), (나)를 만족시키는 B를 실제로 구해 AB를 계산
B = Matrix([[p, q], [r, s]])
sols = solve(list((B + 2 * E) ** 2 + B ** 2 - 10 * E), [p, q, r, s], dict=True)
ks = set()
for z in sols:
    Bz = B.subs(z)
    if all(v.is_number for v in Bz):
        P = (Bz + 2 * E) * Bz
        if P[0, 1] == 0 and P[1, 0] == 0 and P[0, 0] == P[1, 1]:
            ks.add(P[0, 0])
chk("n798", one(list(ks)), 3)
N_ = Matrix([[3, 3], [1, 5]]) - 2 * E       # (k-1)B
kk = one(solve(list((N_ / (k - 1)) ** 2 - N_ / (k - 1)), [k], dict=True))[k]
chk("n300", kk, 5)
# ---- 거듭제곱
chk("n878", sum(Matrix([[1, 1], [1, 0]]) ** 8), 89)
A, B = Matrix([[1, 0], [-1, 1]]), Matrix([[1, 0], [-5, -1]])
chk("n727", one([n for n in range(1, 300) if sum(A ** n * B) == -100]), 95)
def powsum(X, n):
    P, T = (1, 0, 0, 1), (0, 0, 0, 0)
    for _ in range(n):
        P = mul(P, X)
        T = tuple(u + w for u, w in zip(T, P))
    return T


chk("n295", one([v for v in range(-50, 51) if sum(powsum((1, 0, v, -1), 100)) == 800]), 14)
A = Matrix([[2, 2], [-1, -2]])
chk("n825", sum(sum((A ** n for n in range(1, 9)), zeros(2))), 75)
A = Matrix([[1, -1], [1, 1]])
S = sum((A ** n for n in range(1, 9)), zeros(2))
chk("o32", S[0, 1] + S[1, 1], 30)
# ---- 거듭제곱이 kE
T = (Matrix([[4, 5], [1, 3]]) - Matrix([[4, 2], [-2, 3]])) ** 10
chk("o21", one([kk for kk in range(1, 30) if sum(T) == 2 * 3 ** kk]), 10)
# n923: A²=A+E, 모든 성분의 합 3인 A를 실제로 만들어 확인 (A=(a b; c d), a+d=1, ad-bc=-1)
A = Matrix([[0, 1], [1, 1]])
assert A ** 2 == A + E and sum(A) == 3
A2 = Matrix([[3, 5], [-1, -2]])      # A²=A+E인 다른 행렬로도 A⁷=13A+8E
assert A2 ** 2 == A2 + E and A2 ** 7 == 13 * A2 + 8 * E
chk("n923", one(list({sum(A ** 7)})), 55)
A, B = Matrix([[2, -1], [3, -1]]), Matrix([[3, -1], [7, -3]])
best = None
for n in range(1, 40):
    Sn = A ** n + B ** n
    if Sn[0, 1] == 0 and Sn[1, 0] == 0 and Sn[0, 0] == Sn[1, 1] and Sn[0, 0] > 0:
        best = n + Sn[0, 0] if best is None else min(best, n + Sn[0, 0])
chk("n425", best, 15)
A = Matrix([[1, -3], [1, -2]])
tot = 0
P = E
for n in range(1, 200):
    P = P * (A ** n + E)
    if n >= 4 and P == 128 * E:
        tot += n
chk("n324", tot, 44)
# ---- 열로 이루어진 행렬과의 곱
Am = Matrix([[a, b], [c, d]])
z = one(solve(list(Am * Matrix([1, 0]) - Matrix([2, 3])) + list(Am * Matrix([0, 2]) - Matrix([-4, 2])), [a, b, c, d], dict=True))
chk("n660", sum(Am.subs(z) * Matrix([1, 3])), 2)
z = solve(list(Am ** 2 * Matrix([2, 1]) - Matrix([2, 1])) + list(Am ** 3 * Matrix([2, 1]) - Matrix([1, 3])), [a, b, c, d], dict=True)
vals = {sum(Am.subs(w) * Matrix([4, -3])) for w in z if all(v.is_real for v in w.values())}
chk("n792", one(list(vals)), 6)
z = solve(list(Am * Matrix([2, 3]) - Matrix([3, 4])) + list(Am ** 2 * Matrix([2, 3]) - Matrix([5, 7])), [a, b, c, d], dict=True)
chk("n816", one([prod(Am.subs(w)) for w in z]), 30)
# n75: A(A+E)=E, A²(1;3)=(-3;10)를 만족시키는 A를 실제로 구해 계산
z = solve(list(Am * (Am + E) - E) + list(Am ** 2 * Matrix([1, 3]) - Matrix([-3, 10])), [a, b, c, d], dict=True)
vals = set()
for w in z:
    Aw = Am.subs(w)
    v = (Aw + E).LUsolve(Aw * Matrix([2, 6]))
    vals.add(simplify(v[0] + v[1]))
chk("n75", one(list(vals)), 14)
# ---- 실생활
T = Matrix([[Rational(7, 10), Rational(3, 10)], [Rational(1, 10), Rational(9, 10)]])
v = Matrix([[60, 40]]) * T * T
chk("n947", 10 * (v[1] - v[0]), 248)
P, Q = Matrix([[2000, 2200], [3000, 3200]]), Matrix([[350, 290], [850, 540]])
P2 = Matrix([[2000 * Rational(11, 10), 2200 * Rational(105, 100)], [3000 * Rational(12, 10), 3200 * Rational(11, 10)]])
X = P + Q - P2
chk("n488", max(X) - min(X), 100)
# ---- 참, 거짓


def ex_counter(cond, concl, n=4000, three=False):
    """정수 행렬을 무작위로 만들어 cond이면 concl인지 본다. 반례가 있으면 False"""
    for _ in range(n):
        Ms = [rnd() for _ in range(3)]
        if cond(*Ms) and not concl(*Ms):
            return False
    return True


A0, B0, C0 = Matrix([[1, 0], [0, 0]]), O, Matrix([[0, 0], [0, 1]])
t1 = not (A0 * B0 == A0 * C0 and A0 != O and B0 != C0)
t2 = ex_counter(lambda A, B, C: A * B + B * C == B * (A + C), lambda A, B, C: A * A * B == B * A * A)
t3 = ex_counter(lambda A, B, C: (A + 2 * B) ** 2 == (A - 2 * B) ** 2, lambda A, B, C: A * B + B * A == O)
chk("n100", mark((t1, t2, t3), ["ㄱ", "ㄴ", "ㄷ", "ㄱ, ㄴ", "ㄴ, ㄷ"]), "⑤")
fs = lambda M_: sum(M_)
u1 = ex_counter(lambda A, B, C: True, lambda A, B, C: fs(A + B) == fs(A) + fs(B))
u2 = fs(Matrix([[1, 0], [0, 0]]) * Matrix([[0, 0], [1, 0]])) == fs(Matrix([[1, 0], [0, 0]])) * fs(Matrix([[0, 0], [1, 0]]))   # 반례이면 False
u3 = ex_counter(lambda A, B, C: True, lambda A, B, C: fs(3 * A) == 3 * fs(A) and fs(-2 * A) == -2 * fs(A))
u4 = ex_counter(lambda A, B, C: True, lambda A, B, C: fs(2 * A - 5 * B) == 2 * fs(A) - 5 * fs(B))
chk("n730", mark((u1, u2, u3, u4), ["ㄱ", "ㄱ, ㄷ", "ㄱ, ㄴ, ㄹ", "ㄱ, ㄷ, ㄹ", "ㄴ, ㄷ, ㄹ"]), "④")
t_ = symbols("t", real=True)
A = Matrix([[t_, 2], [0, 1 - t_]])
D2 = A * A - A
w1 = [z[t_] for z in solve(list(D2 - 2 * E), [t_], dict=True) if z[t_] > 0] == [2]
w2 = solve(list(D2 + E), [t_], dict=True) == []
w3 = solve(sum(D2 * D2) - 72, [t_], dict=True) == []
chk("n624", mark((w1, w2, w3), ["ㄱ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"]), "②")
# ---- A²=pB+qE
z = one(solve(list(Matrix([[1, -1], [-2, 3]]) ** 2 - p * Matrix([[3, -2], [-4, 7]]) - q * E), [p, q], dict=True))
chk("n308", z[p] + z[q], -1)
z = one(solve(list(Matrix([[1, 2], [3, 4]]) ** 2 - p * Matrix([[2, k], [3, 5]]) - q * E), [p, q, k], dict=True))
chk("n232", z[k], 2)
# ---- 고난도
A = Matrix([[4, 3], [-7, -5]])
K = sum((A ** (2 * m) for m in range(1, 1014)), zeros(2))
v = K * Matrix([1, -2])
chk("n146", v[0] + v[1], 1)
A = Matrix([[0, p], [-p, 0]]); B = Matrix([[q, r], [r, s]])
z = one(solve(list(A + 2 * B - Matrix([[2, -1], [-7, 8]])), [p, q, r, s], dict=True))
chk("o25", sum((B - A * A).subs(z)), 19)
chk("o29", one([av for av in range(1, 60) if sum(Matrix([[av, av - 3], [0, 3]]) ** 12) == 2 ** 25]), 4)
S1, S2 = Matrix([[1, 4], [a, -4]]), Matrix([[3, 5], [b, -2]])
A = S2 - S1; B = S1 - A
z = one(solve(list(A * B), [a, b], dict=True))
chk("m3332", z[a] + z[b], 16)
b11, b12, b21, b22, c11, c12, c21, c22 = symbols("b11 b12 b21 b22 c11 c12 c21 c22")
A = Matrix([[0, 0], [6, 0]]); B = Matrix([[b11, b12], [b21, b22]]); C = Matrix([[c11, c12], [c21, c22]])
z = solve(list(A * B) + list(C * A) + [sum(B) - 3, c11 - c21] + list(B * C - A), [b11, b12, b21, b22, c11, c12, c21, c22], dict=True)
chk("m3182", one(list({sum(C.subs(w)) for w in z})), 4)
cnt = 0
for av in range(-30, 31):
    for bv in range(-30, 31):
        for cv in range(-30, 31):
            X = (2 * av + 3, bv, -cv, 1 - av)
            if mul(X, X) == (1, 0, 0, 1):
                cnt += 1
chk("n515", cnt, 16)
cnt = 0
for av in range(1, 60):
    for bv in divisors(24 * 60):
        for cv in divisors(24 * 60):
            X = (av, bv, -cv, av - 10)
            if mul(X, X) == (1, 0, 0, 1):
                cnt += 1
chk("o33", cnt, 8)
# m3316: A의 성분을 훑지 않고, 조건을 식으로 풀어 a12³+a21³의 값을 모은다
a11, a12, a21, a22 = symbols("a11 a12 a21 a22")
A = Matrix([[a11, a12], [a21, a22]]); B = A * A
vals = set()
# (가)(나): 위치마다 a, b 중 정확히 하나가 0 → 각 위치에서 어느 쪽이 0인지 16가지를 모두 풀어 본다
from itertools import product as iprod
for pick in iprod((0, 1), repeat=4):
    eqs = []
    for (i, j), w in zip(((0, 0), (0, 1), (1, 0), (1, 1)), pick):
        eqs.append(A[i, j] if w == 0 else B[i, j])
    T = A + B
    eqs2 = eqs + [sum(T) + 1, prod(T) + 8]
    for z in solve(eqs2, [a11, a12, a21, a22], dict=True):
        if len(z) < 4 or not all(v.is_real for v in z.values()):
            continue
        Az, Bz = A.subs(z), B.subs(z)
        if Az == O or Bz == O:
            continue
        if all(Az[i, j] * Bz[i, j] == 0 and simplify(Az[i, j] + Bz[i, j]) != 0 for i in range(2) for j in range(2)):
            vals.add(simplify(z[a12] ** 3 + z[a21] ** 3))
chk("m3316", one(list(vals)), 45)
