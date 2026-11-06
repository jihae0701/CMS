# 공통수학2 5단원(집합의 뜻과 표현) 유형서 문항 정답 독립 검산 (문항 기호는 c2unit05.py의 v).
# 집합은 원소를 직접 만들어 세고, 실수 조건은 방정식을 풀어 후보를 모두 확인한다.
import itertools, math
from fractions import Fraction as Fr
from fractions import Fraction as F
import sympy as sp
R = []


def chk(no, got, exp):
    ok = (got == exp) if isinstance(got, str) or isinstance(exp, str) else sp.simplify(sp.sympify(got) - sp.sympify(exp)) == 0
    R.append((no, ok, got, exp))


def subsets(xs):
    xs = list(xs)
    for r in range(len(xs) + 1):
        for c in itertools.combinations(xs, r):
            yield set(c)


def mark(truth, ch, names="ㄱㄴㄷㄹ"):
    s = ", ".join(names[i] for i, v in enumerate(truth) if v)
    return "①②③④⑤"[ch.index(s)] if s in ch else "?"


E0 = frozenset()
# n1743: 원소의 개수 — 파이썬 집합으로 직접
t = [len({E0}) == 0, len({0}) == 1, len({1}) < len({2}), len({E0, 1}) - len(E0) == 2]
chk("n1743", mark(t, ["ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄹ", "ㄱ, ㄷ, ㄹ", "ㄴ, ㄷ, ㄹ"]), "③")
A = {1, 2, 3}
t = [frozenset({1, 3}) in A, 2 in A, E0 in A, {3} <= A]
chk("e14-5", mark(t, ["ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄴ, ㄹ", "ㄷ, ㄹ"]), "④")
# e10-4
sol = []
for j in range(-80, 81):
    a = Fr(j, 4)
    B = {a, a + 1}
    X = {x + y for x in A for y in B}
    Y = {x - y for x in A for y in B}
    if X == Y:
        sol.append(a)
chk("e10-4", sol[0] if len(sol) == 1 else None, sp.Rational(-1, 2))
# e2-12
tot = 0
for a in range(1, 100):
    A2 = {1, 2, 3, 4, a}
    if len(A2) != 5:
        continue
    if len({x - y for x in A2 for y in {1, 3, 5}}) == 9:
        tot += a
chk("e2-12", tot, 11)
chk("g265", len({0, 1}) + len([x for x in range(-10, 11) if abs(x) <= 5]) + len([d for d in range(1, 13) if 12 % d == 0]), 19)
# o24
sq = [n * n for n in range(1, 40)]
res = set()
for A4 in itertools.combinations(sq, 4):
    B4 = {math.isqrt(v) for v in A4}
    if sum(set(A4) & B4) == 13:
        res.add(sum(B4))
chk("o24", res.pop() if len(res) == 1 else None, 18)
A3 = {2 * n * n + 1 for n in range(1, 4)}
chk("g300", sum({a % 5 for a in A3}), 7)
# o44
D = [d for d in range(1, 19) if 18 % d == 0]
chk("o44", sum(1 for X in subsets(D) if X and all(18 // x in X for x in X)), 7)
# o25: 집합 A={a}가 조건을 만족시키려면 a²−4a+k=0 — 해의 개수가 1인 k
x = sp.symbols("x")
ks = [kk for kk in [sp.Rational(n, 4) for n in range(-40, 81)] if len(set(sp.solve(x ** 2 - 4 * x + kk, x)) & set(sp.S.Reals.intersect(sp.FiniteSet(*sp.solve(x ** 2 - 4 * x + kk, x))))) == 1]
chk("o25", ks[0] if len(ks) == 1 else None, 4)
# g269
t = [0 in set(), set() <= {0}, False, {1} <= {1}]   # ㄷ: 1은 집합이 아니므로 '1⊂{1,2,3}'은 성립하지 않음
chk("g269", mark(t, ["ㄱ, ㄴ", "ㄴ, ㄷ", "ㄴ, ㄹ", "ㄷ, ㄹ", "ㄱ, ㄴ, ㄹ"]), "③")
a, b = sp.symbols("a b")
s = sp.solve([1 - a + b, 9 + 3 * a + b], [a, b])
chk("g272", s[a] * s[b], 6)
sol = [(av, bv) for av in range(1, 30) for bv in range(1, 30) if {-1, av * av - av} <= {2, bv * bv - 2 * bv}]
chk("f4-5", sol[0][0] * sol[0][1] if len(sol) == 1 else None, 2)
ks = [Fr(j, 100) for j in range(1, 2000) if -Fr(j, 100) <= -2 and 3 * Fr(j, 100) <= 12]
chk("o05", max(ks) + min(ks), 6)
sol = [av for av in range(-20, 21) if {1, av * av - av} == {2, av * av - 3}]
chk("g304", sol[0] if len(sol) == 1 else None, 2)
sol = [(av, bv) for av in range(-30, 31) for bv in range(-30, 31) if {1, 12, av} == {1, 5, av + bv}]
chk("g271", sol[0][0] * sol[0][1] if len(sol) == 1 else None, 35)
chk("f4-12", sum(1 for X in subsets([1, 3, 5, 7, 9]) if len(X) >= 3), 16)
A7 = [v for v in range(-2, 5)]
chk("g295", sum(1 for X in subsets(A7) if {0, 4} <= X and -1 not in X), 16)
chk("g296", sum(1 for X in subsets(range(1, 10)) if sum(1 for v in X if v % 2) == 3 and sum(1 for v in X if v % 2 == 0) >= 2), 110)
Af = {2, 4}
Bf = {2, 4, 6, 8}
chk("f4-8", sum(1 for X in subsets(Bf) if Af <= X), 4)
chk("e11-18", sum(1 for X in subsets(range(1, 11)) if len(X) >= 2 and sum(X) % 2 == 1 and math.prod(X) % 2 == 1), 11)
chk("n1682", sum(1 for X in subsets(range(3, 16)) if X and math.prod(X) % 2 == 1 and sum(X) % 2 == 0 and 3 not in X and 15 not in X), 15)
chk("n1894", sum(max(X) for X in subsets([1, 3, 5, 7]) if len(X) >= 2), 67)
sol = [xv for xv in range(-50, 100) if len({1, 2, xv, 4, 5}) == 5 and sum(sum(c) for c in itertools.combinations([1, 2, xv, 4, 5], 2)) == 120]
chk("g358", sol[0] if len(sol) == 1 else None, 18)
# 고난도 ---------------------------------------------------------------
res = set()
for av in range(1, 200):
    for bv in range(av + 1, 200):
        if (av + bv) % 5:
            continue
        A_ = {av, bv, bv - av, (av + bv) // 5}
        r = [math.isqrt(v) for v in (av, bv, av + bv, 4 * av + 4 * bv)]
        if any(rr * rr != v for rr, v in zip(r, (av, bv, av + bv, 4 * av + 4 * bv))):
            continue
        B_ = set(r)
        if max(B_) == 10:
            res.add(sum(A_ - B_))
chk("g303", res.pop() if len(res) == 1 else None, 32)
# n2761: f(a)=2a²−1, n(A)=1,2 — 원소 후보를 방정식으로 구해 모든 집합을 확인
f = lambda v: sp.nsimplify(2 * v * v - 1)
cands = set()
for e in [2 * x * x - 1 - x]:
    cands |= set(sp.solve(e, x))
fx = 2 * x * x - 1
cands |= set(sp.solve(fx - 1, x)) | set(sp.solve(fx + sp.Rational(1, 2), x)) | set(sp.solve(sp.expand((2 * fx * fx - 1) - x), x))
cands = {sp.nsimplify(c) for c in cands if c.is_real}
sets = set()
for r in (1, 2):
    for c in itertools.combinations(sorted(cands, key=lambda v: float(v)), r):
        Sx = set(c)
        if all(any(sp.simplify(f(v) - w) == 0 for w in Sx) for v in Sx):
            sets.add(frozenset(Sx))
chk("n2761", len(sets), 6)
A81 = [v for v in range(1, 21) if all(p in (2, 3, 5) for p in sp.primefactors(v))]
chk("m81", sum(1 for X in subsets(A81) if {v for v in A81 if v % 4 == 0} <= X and X & {v for v in A81 if v % 3 == 0 and v != 12}), 496)
# m2303x: {0}⊂A, a∈A → a²−2∈A, n(A)=4
fx2 = x * x - 2
c2 = set()
for tg in [-2, 0, 2]:
    c2 |= set(sp.solve(fx2 - tg, x))
c2 |= set(sp.solve(fx2 - x, x))
c2 = {sp.nsimplify(v) for v in c2 if v.is_real} - {-2, 0, 2}
cnt = 0
for tv in c2:
    A_ = {sp.Integer(-2), sp.Integer(0), sp.Integer(2), tv}
    if all(any(sp.simplify(v * v - 2 - w) == 0 for w in A_) for v in A_):
        cnt += 1
chk("m2303x", cnt, 3)
cnt = 0
for av in range(1, 11):
    for bv in range(1, 11):
        A_ = [av, bv, 5, 8, 9, 10]
        if len(set(A_)) != 6:
            continue
        fk = lambda k: sum(1 for X in subsets(A_) if X and min(X) == k)
        if fk(av) == 2 * fk(bv):
            cnt += 1
chk("e12-20", cnt, 7)
# m87: 상한 6×3+3×7+2×10=59, 예 B={1,6}, C={2,3,5}에서 6개가 모두 다름 — 정수 예를 모두 훑어 최댓값 확인
best = 0
for b1 in range(1, 7):
    B_ = {b1, 7 - b1}
    if len(B_) != 2:
        continue
    for c in itertools.combinations(range(1, 10), 3):
        if sum(c) != 10:
            continue
        D_ = {3 + bb + cc for bb in B_ for cc in c}
        best = max(best, sum(D_))
chk("m87", best if best == 6 * 3 + 3 * 7 + 2 * 10 else None, 59)
best_n, best_s = 0, 0
for mask in range(1 << 19):
    A_ = [i + 1 for i in range(19) if mask >> i & 1]
    s_ = set(A_)
    if any(2 * v in s_ for v in A_):
        continue
    sm = sum(A_)
    if sm % 2:
        continue
    if len(A_) > best_n or (len(A_) == best_n and sm > best_s):
        best_n, best_s = len(A_), sm
chk("m88", best_s, 148)

# 2026 중간 17개교 등 추가 문항 ----------------------------------------------
chk("j2-1", mark([True, False, False, True], ["ㄱ, ㄴ", "ㄱ, ㄹ", "ㄷ, ㄹ", "ㄱ, ㄴ, ㄷ", "ㄴ, ㄷ, ㄹ"]), "②")   # 집합의 뜻(기준이 분명한 것)
A3 = {2, 3, 4}
PA = set(frozenset(x) for x in subsets(A3))
chk("j12-9", mark([True, {frozenset(), frozenset(A3)} <= PA, all(math.prod(X) % 2 == 0 for X in PA if len(X) >= 2)],
                  ["ㄱ", "ㄴ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄱ, ㄴ, ㄷ"]), "⑤")
A_ = {2 ** k for k in (1, 2, 3)}
chk("j6-7", len({x - y for x in A_ for y in A_}), 7)
sol = [a for a in [F(n, 2) for n in range(-40, 41)] if {3, a} <= {-a, 2 * a - 1, a * a + 3}]
chk("j9-8", sol[0] if len(sol) == 1 else None, 0)
sol = {a + b for a in range(-20, 21) for b in range(-20, 21) if {a, 1, 7} == {-2, b, 2 * a + 5}}
chk("j6-4", sol.pop() if len(sol) == 1 else None, 5)
best = 0
for a in range(10, 100):
    D = [d for d in range(1, a + 1) if a % d == 0]
    if len(D) == 3:
        best = max(best, math.prod(D))
chk("j3-13", best, 343)
chk("j5-6", sum(1 for X in subsets(range(1, 10)) if len(X) == 3 and 3 in X), 28)
pr = [p_ for p_ in range(2, 17) if all(p_ % q for q in range(2, p_))]
chk("j9-7", sum(1 for X in subsets(pr) if X), 63)
sol = [(a, b) for a in range(-20, 21) for b in range(-30, 31) if {3, a + 5, b - 2} == {a * a - 1, 7, 8}]
chk("e1-3", sol[0][0] + sol[0][1] if len(sol) == 1 else None, 12)
chk("n1902", max(n for n in range(1, 5000) if {x for x in range(2, 100, 2) if x * x <= n} <= {2, 4, 6}), 63)
sol = [a for a in range(-20, 21) if 16 * (5 * a + 20) == 400]
chk("e7-13", 31 - sol[0] if len(sol) == 1 else None, 30)
S_ = [(x, y) for x in range(-5, 6) for y in range(-5, 6) if x * x + y * y == 25]
def right(P, Q, R):
    v = lambda a, b: (b[0] - a[0], b[1] - a[1])
    dot = lambda u, w: u[0] * w[0] + u[1] * w[1]
    return dot(v(P, Q), v(P, R)) == 0 or dot(v(Q, P), v(Q, R)) == 0 or dot(v(R, P), v(R, Q)) == 0
chk("j7-20", sum(1 for t3 in itertools.combinations(S_, 3) if right(*t3)), 60)

if __name__ == "__main__":
    bad = [r for r in R if not r[1]]
    print("검산", len(R), "불일치", len(bad))
    for r in bad:
        print(r)
