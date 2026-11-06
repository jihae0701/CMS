# -*- coding: utf-8 -*-
"""공통수학2 기본서 6단원 집합의 연산 검산: 문항마다 답을 따로(대부분 모든 경우를 직접 세어) 계산해 data06.py의 답과 맞춘다.
python verify06.py
- 집합 등식·ㄱㄴㄷ는 작은 전체집합의 모든 부분집합을 넣어 확인하고, 개수 문제는 경우를 모두 센다.
"""
import sys, os, itertools, math
from fractions import Fraction as Fr
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sympy as sp
import data06

R = {}


def subsets(xs):
    xs = list(xs)
    for r in range(len(xs) + 1):
        for c in itertools.combinations(xs, r):
            yield frozenset(c)


U4 = frozenset(range(4))
ALL4 = list(subsets(U4))


def comp(X, U=U4):
    return U - X


# 01 ---------------------------------------------------------------
k = sp.symbols("k")
Aex = [k - 1, sp.Integer(1), k ** 2 - 3 * k - 3]
Bex = [sp.Integer(-3), k ** 2 - 2 * k + 1, 2 * k + 5]
cands = set()
for e in Aex + Bex:
    for target in (-3, 1):
        if e.free_symbols:
            cands |= set(sp.solve(sp.Eq(e, target), k))
good = []
for kv in cands:
    A = {sp.simplify(e.subs(k, kv)) for e in Aex}
    B = {sp.simplify(e.subs(k, kv)) for e in Bex}
    if len(A) == 3 and len(B) == 3 and A & B == {-3, 1}:
        good.append(kv)
R["g309"] = max(good) - min(good)
sol = []
for a in [Fr(n, 2) for n in range(-40, 41)]:
    A = {1, 3, a, a * a}
    B = {3, a + 1, 2 * a - 3}
    if B - A == {6, 7}:
        sol.append(sum(A))
R["o32"] = sol[0] if len(set(sol)) == 1 else sol
x = sp.symbols("x")
Aset = set(sp.solve(3 * x ** 3 - 2 * x ** 2 - x, x))
res = set()
a_, b_ = sp.symbols("a b")
for r1 in Aset:
    for r2 in list(Aset) + [sp.Symbol("t")]:
        pass
# B는 이차방정식의 해집합: 근 두 개(같을 수도) — 근을 A의 원소와 임의의 수로 두고 조건 확인
for r in Aset:
    for s in list(Aset) + [sp.Rational(n, 3) for n in range(-30, 31)]:
        B = {r, s}
        if len(Aset | B) == 3 and len(Aset & B) == 1:
            av, bv = -(r + s), r * s
            if av * bv > 0:
                res.add(av + bv)
R["n2853"] = list(res)[0] if len(res) == 1 else res

# 02 ---------------------------------------------------------------
U = frozenset(range(1, 9))
sol = set()
for A in subsets(U):
    for B in [frozenset(Bb) for Bb in subsets(U)]:
        if A & B == {3} and (U - A) & (U - B) == {7, 8} and B & ((U - A) | (U - B)) == {4, 5, 6}:
            sol.add(sum(A | (U - B)))
R["e1-7"] = list(sol)[0] if len(sol) == 1 else sol
U = frozenset(range(1, 11))
sol = set()
rest = U - {5, 7, 3, 9, 10}
for AmB in subsets(rest):
    A = AmB | {5, 7}
    B = (rest - AmB) | {5, 7}
    if sum(A) == 2 * sum(B):
        sol.add(math.prod(B))
R["g308"] = list(sol)[0] if len(sol) == 1 else sol
X = range(1, 13)
sol = set()
for AB in itertools.combinations(X, 3):
    for BA in itertools.combinations([v for v in X if v not in AB], 4):
        sAB, sBA = set(AB), set(BA)
        ok = all(Fr(p + 2, 2) in sBA for p in sAB)
        ok = ok and all(q + 2 <= 12 and q + 2 not in sBA for q in sBA)
        if ok:
            sol.add(sum(sBA))
R["n1515"] = list(sol)[0] if len(sol) == 1 else sol

# 03 ---------------------------------------------------------------
def holds(cond, concl, n=3):
    """작은 전체집합 위의 모든 부분집합 (A,B,C)에서 cond → concl"""
    ok = True
    for A in ALL4:
        for B in ALL4:
            for C in (ALL4 if n == 3 else [frozenset()]):
                if cond(A, B, C) and not concl(A, B, C):
                    return False
    return ok
c316 = lambda A, B, C: A and B and C and (A & (C | comp(A))) == frozenset() and (((A - C) | (B - C)) | (C - comp(A | B))) == B
g = [holds(c316, lambda A, B, C: A & comp(C) == A),
     holds(c316, lambda A, B, C: (A & comp(C)) | (comp(A) & B) == B),
     holds(c316, lambda A, B, C: comp(C) & (B | C) == B)]
R["g316"] = ", ".join(n for n, ok in zip("ㄱㄴㄷ", g) if ok)
c38 = lambda A, B, C: A != B and ((A & B) | (A & comp(B))) & B == A
g = [holds(c38, lambda A, B, C: B - A != frozenset(), 2),
     holds(c38, lambda A, B, C: comp(A) <= comp(B), 2),
     holds(c38, lambda A, B, C: comp(A) | B == U4, 2)]
R["o38"] = ", ".join(n for n, ok in zip("ㄱㄴㄷ", g) if ok)
# e4-9: 작은 전체집합에서 A=U가 강제되는지 확인 → n(A)=n(U)=100
forced = all(A == U4 for A in ALL4 for B in ALL4 if (A | B) == U4 and B & comp(B - A) == B)
R["e4-9"] = 100 if forced else None

# 04 ---------------------------------------------------------------
ok = all((B & (A | B)) & (A - (A & comp(C))) == A & B & C for A in ALL4 for B in ALL4 for C in ALL4)
R["n1764"] = "A cap B cap C" if ok else None
st = [lambda A, B: A | frozenset() == frozenset(), lambda A, B: B & comp(B) == B, lambda A, B: A | (A & B) == A,
      lambda A, B: A - comp(B) == A & B, lambda A, B: (A | B) & comp(A - B) == A, lambda A, B: comp(A - comp(B)) & A == A - B]
R["e11-17"] = sum(1 for f in st if all(f(A, B) for A in ALL4 for B in ALL4))
ok = all((A & comp(B)) | comp(A | B) == comp(B) for A in ALL4 for B in ALL4)
R["o15"] = "B^{C}" if ok else None

# 05 ---------------------------------------------------------------
U = frozenset(range(1, 11))
A, B = frozenset({1, 3, 5, 7, 9}), frozenset({3, 6, 9})
R["g338"] = sum(1 for C in subsets(U) if A | C == B | C)
tot = Fr(0)
A = {1, 3, 4, 5}
xs = [1, 3, 4, 5, 7]
kc = {Fr(2 * a - x_) for a in A for x_ in xs}
for kv in sorted(kc):
    B = {Fr(x_ + kv, 2) for x_ in xs}
    I = {Fr(a) for a in A} & B
    if 2 ** (4 - len(I)) == 2:
        tot += kv
R["n2809"] = tot
U = frozenset(range(1, 10))
A, B = frozenset({1, 2, 3, 4}), frozenset({3, 4, 5, 6})
R["e1-14"] = sum(1 for X in subsets(U) if A - X == B - X and len((X - A) & (X - B)) >= 1)

# 06 ---------------------------------------------------------------
N = 2000
def mult(k_, N=N):
    return frozenset(range(k_, N + 1, k_))
A945 = mult(9) & mult(15)
mmin = min(m for m in range(1, 200) if mult(m) <= A945)
nmax = max(n for n in range(1, 200) if (mult(18) | mult(45)) <= mult(n))
R["g311"] = mmin + nmax
R["e12-13"] = sum(k_ for k_ in range(2, 100) if (mult(4) & mult(6)) <= mult(k_))
sol = []
for k_ in range(2, 200):
    U = set(range(1, k_ + 1))
    A = {v for v in U if v % 2 == 0}
    B = {v for v in U if k_ % v == 0}
    Cc = U - (A | B)
    if len(A) * len(Cc) == 12:
        sol.append(math.prod(Cc))
R["n1916"] = sol[0] if len(sol) == 1 else sol

# 07 ---------------------------------------------------------------
a, b = sp.Rational(-1, 2), -4
def inA318(v):
    return a * v * v + b * v - 6 < 0
ok = True
for j in range(-4000, 4001):
    v = sp.Rational(j, 100)
    inB = -6 <= v <= 3
    if not (inA318(v) or inB):
        ok = False
    if (inA318(v) and inB) != (-2 < v <= 3):
        ok = False
R["g318"] = sp.Rational(-9, 2) if ok else None
def setA341():
    return {v for v in range(-100, 101) if v * v < 2 * v + 3}
def setB341(k_):
    return {v for v in range(-100, 101) if 4 * v * v + (2 - 2 * k_) * v > k_}
Ac = set(range(-100, 101)) - setA341()
R["g341"] = min(k_ for k_ in range(1, 100) if 2 ** len(Ac - setB341(k_)) >= 100)
tot = Fr(0)
for j in range(-400, 401):
    av = Fr(j, 8)
    # A=[2,3], B=[a, a+1] — 교집합이 한 점인지(구간의 길이로 판정)
    lo, hi = max(Fr(2), av), min(Fr(3), av + 1)
    if lo == hi:
        tot += av
R["e11-22"] = tot

# 08 ---------------------------------------------------------------
U = set(range(1, 101))
def op(X, Y):
    return (X | Y) & ((U - X) | (U - Y))
A, B, C = {v for v in U if v % 3 == 0}, {v for v in U if v % 4 == 0}, {v for v in U if v % 5 == 0}
R["g353"] = len(op(op(A, B), C))
def oc(X, Y):
    return (X & Y) | comp(X | Y)
g1 = all(oc(A, B) == oc(B, A) for A in ALL4 for B in ALL4)
g2 = all(oc(oc(A, B), C) == oc(A, oc(B, C)) for A in ALL4 for B in ALL4 for C in ALL4)
def rep(A, n):
    X = A
    for _ in range(n - 1):
        X = oc(X, A)
    return X
g3 = all(rep(A, 99) == A for A in ALL4)
R["g348"] = ", ".join(n for n, ok in zip("ㄱㄴㄷ", [g1, g2, g3]) if ok)
ok = True
for A1 in ALL4:
    for A2 in ALL4:
        for A3 in ALL4:
            seq = [None, A1, A2, A3]
            for kk in range(4, 8):
                seq.append(seq[kk - 1] & (seq[kk - 2] | seq[kk - 3]))
            if seq[7] != A3 & (A1 | A2):
                ok = False
R["m75"] = "A_{3} cap (A_{1} cup A_{2} )" if ok else None

# 09 ---------------------------------------------------------------
# g330: 각 음식점이 만족시키는 기준 집합을 영역 개수로 두고 정수해를 모두 찾음
sol = set()
for r123 in range(0, 46):
    for r12 in range(0, 46):
        for r13 in range(0, 46):
            r23 = 25 - r12 - r13
            if r23 < 0:
                continue
            r1 = 36 - r12 - r13 - r123
            r2 = 25 - r12 - r23 - r123
            r3 = 23 - r13 - r23 - r123
            if min(r1, r2, r3) < 0:
                continue
            if r1 + r2 + r3 + r12 + r13 + r23 + r123 + 4 == 45:
                sol.add(r123)
R["g330"] = list(sol)[0] if len(sol) == 1 else sol
nU, nA, nB = 100, 50, 40
nAB_union = nU - 25
R["e6-20"] = (nA - (nA + nB - nAB_union)) + (nB - (nA + nB - nAB_union))
sol = set()
for bb in range(0, 25):
    for gg in range(0, 33):
        b1, g1_ = 24 - bb, 32 - gg
        if (b1 + g1_) + 2 * (bb + gg) == 64 and g1_ == b1 + 4:
            sol.add(gg)
R["n2812"] = list(sol)[0] if len(sol) == 1 else sol

# 10 ---------------------------------------------------------------
U = range(1, 11)
sums = [sum(set(A) & set(B)) for A in itertools.combinations(U, 5) for B in itertools.combinations(U, 7)]
R["g327"] = max(sums) + min(sums)
vals = []
for x_ in range(0, 15):
    for y_ in range(0, 20):
        c_only = 54 - 9 - x_ - y_
        if c_only >= 0:
            vals.append(c_only)
R["n1695"] = max(vals) + min(vals)
prods = set()
for assign in itertools.product(range(8), repeat=6):   # 영역 번호: 비트 1=A, 2=B, 4=C
    cnt = [assign.count(r) for r in range(8)]
    nA_ = sum(cnt[r] for r in range(8) if r & 1)
    nB_ = sum(cnt[r] for r in range(8) if r & 2)
    nC_ = sum(cnt[r] for r in range(8) if r & 4)
    if cnt[6] + cnt[7] == 2 and cnt[2] + cnt[6] == 2 and cnt[4] + cnt[6] == 2 and cnt[7] == 1:
        prods.add(nA_ * nB_ * nC_)
R["e7-15"] = max(prods) - min(prods)
R["o43"] = max(xx for xx in range(1, 26) if 2 * xx >= 7 and xx >= 7 and 3 * xx - 7 <= 25)

# STEP 3 -----------------------------------------------------------
vals = set()
for kk in range(1, 30):
    for m in range(1, kk + 1):
        U = set(range(1, kk + 1))
        A = {d for d in U if m % d == 0}
        if 5 in A or 8 in A or not {5, 8} <= U:
            continue
        for r in range(len(A) + 1):
            for AB in itertools.combinations(sorted(A), r):
                B = set(AB) | {5, 8}
                if len(A | (U - B)) == 8 and sum(B) == sum(A) + 3:
                    vals.add(sum(U - (A | B)))
R["e9-20"] = sum(vals)
sol = set()
for others in itertools.combinations([v for v in range(1, 14) if v != 12], 4):
    if sum(others) != 13:
        continue
    A = set(others) | {12}
    for kn in range(1, 200):
        for kd in range(1, 30):
            kv = Fr(kn, kd)
            B = {kv * v for v in A}
            if any(bv.denominator != 1 for bv in B):
                continue
            B = {int(bv) for bv in B}
            I = A & B
            if 12 in I and len(I) == 2 and sum(A | B) == 157 and len(B) == 5:
                sol.add(max(B))
R["g352"] = list(sol)[0] if len(sol) == 1 else sol
sol = set()
for A in itertools.combinations(range(1, 40), 5):
    if not {4, 6, 8} <= set(A):
        continue
    for kk in range(1, 40):
        B = {Fr(v + kk, 2) for v in A}
        if any(bv.denominator != 1 for bv in B):
            continue
        B = {int(bv) for bv in B}
        As = set(A)
        if len(B) == 5 and As & B == {4, 6, 8} and sum((As - B) | (B - As)) == 24:
            sol.add(sum(B))
R["g354"] = list(sol)[0] if len(sol) == 1 else sol
S4 = frozenset("abcd")
PS = list(subsets(S4))
cnt = 0
for mask in range(1, 1 << 16):
    X = {PS[i] for i in range(16) if mask >> i & 1}
    if all((S4 - A) in X for A in X) and all((A & B) in X and (A | B) in X for A in X for B in X):
        cnt += 1
R["m77"] = cnt
# e4-15: 구간 [k−1, k+1] (k=1..18)을 모두 찌르는 최소 점 개수(구간 찌르기 — 끝점 순 탐욕이 최적)
ivs = sorted([(kk - 1, kk + 1) for kk in range(1, 19)], key=lambda t: t[1])
pts = []
for lo, hi in ivs:
    if not any(lo <= p_ <= hi for p_ in pts):
        pts.append(hi)
R["e4-15"] = len(pts)
# m97: 비율 100명 기준 — 안 쓴 사람 집합이 겹치지 않게 만들 수 있는지, 하한 계산
miss = [10, 12, 30, 45]
R["m97"] = max(0, 100 - sum(miss))
A = {d for d in range(1, 37) if 36 % d == 0}
B = {v for v in range(1, 100) if (v - 6) ** 2 * (v * v - 22 * v + 57) < 0}
tot = 0
for X in subsets(A):   # (가)에서 X⊂A이므로 A의 부분집합만 보면 된다(아래에서 다시 확인)
    X = set(X)
    if (X - A) <= (A - X) and ((A - B) | X) == X:
        tot += len(X)
R["n1798"] = tot
pairs = [(1, 24), (2, 12), (3, 8), (4, 6)]
tot = Fr(0)
for p_, q_ in itertools.combinations(pairs, 2):
    A = set(p_) | set(q_)
    av = Fr(40 - sum(A), 4)
    B = {(Fr(v) + av) / 2 for v in A}
    if len({Fr(v) for v in A} | B) == 7:
        tot += av
R["e10-15"] = tot


# 대조 ---------------------------------------------------------------
def norm(v):
    if isinstance(v, (Fr,)) or (hasattr(v, "is_Rational") and getattr(v, "is_Rational", False) and not getattr(v, "is_Integer", True)):
        v = Fr(str(v))
        if v.denominator != 1:
            sgn = "-" if v < 0 else ""
            return "%s{%d}over{%d}" % (sgn, abs(v.numerator), v.denominator)
        return str(v.numerator)
    return str(v).replace(" ", "")


bad = 0
items = [p for _, _, ps in data06.TYPES for p in ps] + data06.STEP3
for p in items:
    got = R.get(p["src"])
    exp = p["ans"].replace(" ", "")
    if got is None:
        print("검산 없음", p["src"], p["ans"])
        bad += 1
        continue
    if norm(got) != exp:
        print("불일치", p["src"], "자료", p["ans"], "검산", got, norm(got))
        bad += 1
print("문항", len(items), "불일치", bad)
