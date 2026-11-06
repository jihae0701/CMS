# -*- coding: utf-8 -*-
"""공통수학2 기본서 5단원 집합의 뜻과 표현 검산: 문항마다 답을 따로(대부분 모든 경우를 직접 세어) 계산해 data05.py의 답과 맞춘다.
python verify05.py
"""
import sys, os, itertools, math, cmath
from fractions import Fraction as Fr
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sympy as sp
import data05

R = {}


def subsets(xs):
    xs = list(xs)
    for r in range(len(xs) + 1):
        for c in itertools.combinations(xs, r):
            yield set(c)


# 01 ---------------------------------------------------------------
# g302: 서로 다른 네 양수(정수에 한정하지 않고, B·C의 조건으로 a,b,c,d를 구한 뒤 확인)
found = []
for a, b, c, d in itertools.permutations([x for x in range(1, 15)], 4):
    if not (a < b < c < d):
        continue
    A = [a, b, c, d]
    B = {x + y for x in A for y in A if x != y}
    C = {x * y for x in A for y in A if x != y}
    if B == {7, 8, 9, 12, 13, 14} and C == {12, 15, 20, 27, 36, 45}:
        found.append(a * a + b * b + c * c + d * d)
R["g302"] = found[0] if len(set(found)) == 1 else None
# e5-13
R["e5-13"] = len({a * b for a in range(-1, 3) for b in range(-3, 6)})
# n1662: a+b=4, B의 원소의 합 20 → 일반 경우 + 같은 값이 생기는 경우를 모두 풀어 확인
a = sp.symbols("a")
bb = 4 - a
exprs = [25, 0, -5 * a, -5 * bb, a ** 2, bb ** 2, a * bb]
cands = set()
# 일반 경우
for s in sp.solve(sp.Eq(sum(exprs), 20), a):
    cands.add(s)
# 같은 값이 생기는 경우
for i in range(len(exprs)):
    for j in range(i + 1, len(exprs)):
        eq = sp.Eq(exprs[i], exprs[j])
        if eq is sp.true or eq is sp.false:
            continue
        for s in sp.solve(eq, a):
            cands.add(s)
good = set()
for s in cands:
    if not s.is_real:
        continue
    av, bv = sp.nsimplify(s), sp.nsimplify(4 - s)
    A = {-5, 0, av, bv}
    if len(A) != 4:
        continue
    B = {sp.simplify(x * y) for x in A for y in A}
    if sp.simplify(sum(B) - 20) == 0:
        good.add(sp.simplify(av * bv))
R["n1662"] = list(good)[0] if len(good) == 1 else good

# 02 ---------------------------------------------------------------
def nA(m):
    return math.isqrt(m)  # √m 이하의 자연수 개수
R["g301"] = sum(1 for k in range(1, 1000) if nA(k) == nA(10) + nA(20))
def ndiv(k):
    return sum(1 for d in range(1, k + 1) if k % d == 0)
R["o23"] = sum(k for k in range(1, 61) if ndiv(k) % 2 == 1 and ndiv(k) > 3)
def An(n):
    return {x for x in range(2, 100, 2) if x * x <= n}
R["n1902"] = max(n for n in range(1, 5000) if An(n) <= An(36))

# 03 ---------------------------------------------------------------
# n2775: {−1,0,1} 다음 원소 t (실수) — t²−1 ∈ A. t 후보를 방정식으로 모두 구해 집합을 만들어 확인
t = sp.symbols("t")
sets = set()
for target in [-1, 0, 1, t]:
    for s in sp.solve(sp.Eq(t ** 2 - 1, target), t):
        A = {sp.Integer(-1), sp.Integer(0), sp.Integer(1), s}
        if len(A) == 4 and all(sp.simplify(x ** 2 - 1) in A or any(sp.simplify(x ** 2 - 1 - y) == 0 for y in A) for x in A):
            sets.add(frozenset(A))
R["n2775"] = len(sets)
# o26
A = set()
todo = [2, 7]
while todo:
    v = todo.pop()
    if v in A:
        continue
    A.add(v)
    if 3 * v <= 100:
        todo.append(3 * v)
R["o26"] = sum(A)
# g340: 36의 약수 부분집합 중 조건을 만족시키는 것(공집합 제외)
D = [d for d in range(1, 37) if 36 % d == 0]
R["g340"] = sum(1 for X in subsets(D) if X and all(36 // x in X for x in X))

# 04 ---------------------------------------------------------------
sol = []
for av in [Fr(n, 2) for n in range(-40, 41)]:
    A = {1, 2 - av}
    B = {3, av - 4, 2 * av - 5}
    if A <= B:
        sol.append(av)
R["g305"] = sol[0] if len(sol) == 1 else sol
sol = []
for av in range(-20, 21):
    for bv in range(-30, 31):
        A = {3, av + 5, bv - 2}
        B = {av * av - 1, 7, 8}
        if A == B:
            sol.append(av + bv)
R["e1-3"] = sol[0] if len(set(sol)) == 1 else sol
# g306: A=(a−1, a], B=(1, 6) — 촘촘한 점으로 포함 확인
def inc306(av):
    xs = [av - 1 + (k + 1) / 400 for k in range(400)]
    return all(1 < x < 6 for x in xs)
R["g306"] = sum(av for av in range(1, 20) if inc306(av))
# n1932
def inc1932(k):
    xs = [-3 + 5 * j / 1000 for j in range(1001)]
    return all(x * x - k * x + k * k - 19 < 0 for x in xs)
R["n1932"] = sum(1 for k in range(-20, 21) if inc1932(k))

# 05 ---------------------------------------------------------------
R["o07"] = sum(1 for X in subsets(range(1, 9)) if any(x % 2 == 0 for x in X) and not (X & {2, 3, 5, 7}))
def cnt149(k):
    A = list(range(2, k + 1, 2))
    return sum(1 for X in subsets(A) if X and min(X) == 6)
R["e14-9"] = sum(k for k in range(6, 40) if cnt149(k) == 16)
def cnt08(n):
    A = set(range(3, n + 1, 3))
    return sum(1 for X in subsets(A) if 3 in X and X != A)
R["o08"] = sum(n for n in range(3, 40) if cnt08(n) == 31)
A = [d for d in range(1, 19) if 18 % d == 0]
R["g298"] = sum(1 for X in subsets(A) if X & {2, 3})

# 06 ---------------------------------------------------------------
A = {1, 2, 4}
B = {24 // n for n in range(1, 25) if 24 % n == 0}
R["o09"] = sum(1 for X in subsets(B) if A <= X)
def set_e323(k):
    P, Rr, S = (18, 24), (39, 52), (3, 4)
    out = set()
    for n in range(1, 200):
        Q = (3 * n, 4 * n)
        if math.dist(P, Q) > 10 and math.dist(Rr, Q) > 10 and math.dist(S, Q) <= k + 1e-9:
            out.add(n)
    return out
tot = 0
for k in range(1, 400):
    A = set_e323(k)
    if {1, 3} <= A and 2 ** (len(A) - 2) == 32:
        tot += k
R["e3-23"] = tot

# 07 ---------------------------------------------------------------
R["n1600"] = sum(1 for X in subsets([2, 3, 4, 5, 8, 16, 32]) if len(X) >= 3 and sum(X) % 2 == 0)
R["o29"] = sum(1 for X in subsets(range(1, 10)) if 1 <= sum(1 for x in X if x % 2) <= 4)

# 08 ---------------------------------------------------------------
R["g358"] = sum(max(X) for X in subsets(range(1, 6)) if len(X) >= 2)
sol = []
for av in range(-20, 21):
    A = [av + 2 * i for i in range(5)]
    subs = [X for X in subsets(A) if X]
    if sum(sum(X) for X in subs) == 400:
        sol.append(len(subs) - av)
R["e7-13"] = sol[0] if len(sol) == 1 else sol
R["n1771"] = sum(sum(X) for X in subsets(range(1, 11)) if len(X) in (3, 8))
A = [Fr(1, 2 ** j) for j in range(5)]
R["g344"] = sum(min(X) for X in subsets(A) if X)

# STEP 3 -----------------------------------------------------------
# g349: 궤도(묶음) 구조를 직접 만들어 ㄴ·ㄷ 확인
def f(z):
    return (z - 1) / z
def orbit(z):
    out = [z]
    w = f(z)
    while abs(w - z) > 1e-9 and len(out) < 10:
        out.append(w)
        w = f(w)
    return out
o = orbit(0.5)
g1 = all(any(abs(x - 2) < 1e-9 for x in o) for _ in [0])
om = complex(0.5, math.sqrt(3) / 2)
fixed = [om, om.conjugate()]
assert all(abs(f(z) - z) < 1e-9 for z in fixed)
# n(A)=5 → 세 원소 묶음 하나 + 고정점 둘(묶음 크기는 3 또는 1이고, 고정점은 두 개뿐)
prod5 = 1
for z in o + fixed:
    prod5 *= z
g2 = abs(prod5 - (-1)) < 1e-9
# n(A)=3인 예: 묶음 하나 → 곱 −1이므로 ㄷ 거짓
prod3 = 1
for z in o:
    prod3 *= z
g3 = abs(prod3 - 1) < 1e-9
R["g349"] = ", ".join(n for n, ok in zip("ㄱㄴㄷ", [g1, g2, g3]) if ok)
# o46
sol = []
for a_ in range(2, 100):
    for b_ in range(a_ + 1, 100):
        A = [1, a_, b_]
        B = {x * y for x in A for y in A}
        if len(B) == 5 and max(B) == 81:
            sol.append(sum(A))
R["o46"] = sol[0] if len(set(sol)) == 1 else sol
# m74
Aset = {4 * m + 11 * n for m in range(60) for n in range(30)}
R["m74"] = min(k for k in range(1, 200) if all(x in Aset for x in range(k, 200)))
# m82
A = [1, 2, 3, 4]
cnt = 0
for C in subsets(A):
    for B in subsets(C):
        if B and C and (sum(B) * sum(C)) % 2 == 0:
            cnt += 1
R["m82"] = cnt
# m80
R["m80"] = sum(1 for X in subsets(range(1, 10)) if len(X) >= 2 and all(math.gcd(x, y) == 1 for x, y in itertools.combinations(X, 2)))
# m98: 차가 4 또는 9인 두 수를 함께 갖지 않는 {1..40}의 부분집합의 최대 크기(9개씩 끊는 상태 DP)
N = 40
best = {(): 0}
for v in range(1, N + 1):
    nb = {}
    for st, val in best.items():
        # st: 최근 9개(v−9..v−1)의 선택 여부
        for take in (0, 1):
            if take:
                if len(st) >= 4 and st[-4]:
                    continue
                if len(st) >= 9 and st[-9]:
                    continue
            ns = (st + (take,))[-9:]
            if nb.get(ns, -1) < val + take:
                nb[ns] = val + take
    best = nb
R["m98"] = max(best.values())
ex = [1, 3, 6, 8, 11, 13, 14, 16, 19, 21, 24, 26, 27, 29, 32, 34, 37, 39, 40]
ok_ex = len(ex) == 19 and all(abs(x - y) not in (4, 9) for x, y in itertools.combinations(ex, 2))
# o48
best48 = 0
U = list(range(1, 17))
r0 = [x for x in U if x % 3 == 0]
r1 = [x for x in U if x % 3 == 1]
r2 = [x for x in U if x % 3 == 2]
for X1 in (r1, r2, []):
    for z in [None] + r0:
        X = list(X1) + ([z] if z else [])
        if all((x + y) % 3 for x, y in itertools.combinations(X, 2)):
            best48 = max(best48, sum(X))
R["o48"] = best48


# 대조 ---------------------------------------------------------------
def norm(v):
    return str(v).replace(" ", "")


bad = 0
items = [p for _, _, ps in data05.TYPES for p in ps] + data05.STEP3
for p in items:
    got = R.get(p["src"])
    exp = p["ans"]
    if got is None:
        print("검산 없음", p["src"], exp)
        bad += 1
        continue
    e = exp.replace(" ", "")
    if norm(got) != e:
        print("불일치", p["src"], "자료", exp, "검산", got)
        bad += 1
print("m98 예시 집합", "맞음" if ok_ex else "틀림")
print("문항", len(items), "불일치", bad)
