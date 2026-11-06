# 공통수학2 6단원(집합의 연산) 유형서 문항 정답 독립 검산 (문항 기호는 c2unit06.py의 v).
# 집합 등식·ㄱㄴㄷ는 작은 전체집합의 모든 부분집합으로 확인하고, 개수·최댓값은 경우를 모두 훑는다.
import itertools, math
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
            yield frozenset(c)


def mark(truth, ch, names="ㄱㄴㄷㄹ"):
    s = ", ".join(names[i] for i, v in enumerate(truth) if v)
    return "①②③④⑤"[ch.index(s)] if s in ch else "?"


MC_BOGI = ["ㄱ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"]
MC_B2 = ["ㄱ", "ㄴ", "ㄱ, ㄴ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"]
MC_B3 = ["ㄱ", "ㄴ", "ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"]
U4 = frozenset(range(4))
ALL4 = list(subsets(U4))
cp = lambda X: U4 - X

U = frozenset(range(1, 6))
chk("o11", sum(1 for A in subsets(U) for B in subsets(U) if len(A) == len(B) == 2 and len(A | B) == 3), 60)
U = frozenset(range(1, 7))
chk("n1893", sum(1 for A in subsets(U) for B in subsets(U) if B - A == B and (U - A) & (U - B) == {1}), 32)
A, B = {1, 3, 5, 7, 9}, {2, 4, 5, 9}
chk("n1570", sum((A - B) | (B - A)), 17)
U = set(range(-4, 5)); A = {v for v in U if -3 < v <= 2}; B = {v for v in U if 1 <= v < 4}
chk("o13", len(U - (A - B)), 6)
U = set(range(1, 101)); A = {v for v in U if v % 2 == 0}; B = {v for v in U if v % 3 == 0}
chk("o22", len(A | (U - B)), 83)
U = set(range(1, 21)); A = {v for v in U if v % 5 == 0}; B = {v for v in U if 20 % v == 0}
chk("n2370", mark([A | B == {5, 10, 20}, B - A == {1, 2, 4}, len((U - A) & (U - B)) == 13], MC_BOGI), "④")
# n1772: U는 (가)에서 정해짐 — U 후보를 {1..9}의 상위집합으로 두고 B까지 모두 훑음
sols = set()
A = frozenset({4, 5, 6, 7})
for extra in subsets([1, 2, 3, 8, 9]):
    Uu = A | extra
    for Bb in subsets(Uu):
        if (Uu - A) | (Uu - Bb) != {1, 3, 5}:
            continue
        if all(len((A | {x}) - Bb) == 1 for x in Uu):
            sols.add(sum(Bb))
chk("n1772", sols.pop() if len(sols) == 1 else None, 21)
U = frozenset(range(1, 11))
As = set()
for A in subsets(U):
    for B in subsets(U):
        if B - A == {4, 5} and U - (A | B) == {6, 7}:
            As.add(A)
chk("o36", 2 ** len(As.pop()) if len(As) == 1 else None, 64)
U = frozenset(range(1, 9))
vals = set()
for A in subsets(U):
    for B in [frozenset(b) for b in subsets(U)]:
        if A - B != {1, 2}:
            continue
        # C는 A−C={1,5,8}을 만족시키는 아무 집합: 결과는 C와 무관함을 확인
        for Cc in [U - {1, 5, 8}, (U - A) | (A - {1, 5, 8})]:
            if A - Cc == {1, 5, 8}:
                vals.add(sum(A & (U - (B & Cc))))
chk("e10-22", vals.pop() if len(vals) == 1 else None, 16)
sol = set()
for a in [F(n, 3) for n in range(-30, 31)]:
    A = {2, 6, 2 * a - 1, 3 * a}
    if len(A) != 4:
        continue
    for b in [F(n, 2) for n in range(-20, 21)]:
        B = {6, a, b - 1, b}
        if len(B) == 4 and A & B == {1, 3, 6}:
            sol.add(sum(A | B))
chk("o12", sol.pop() if len(sol) == 1 else None, 16)
# g330: p, q를 유리수 격자에서 훑어 조건을 만족시키는 경우의 합을 모음
res = set()
xs = sp.symbols("x")
for pn in range(-24, 25):
    for qn in range(-24, 25):
        p_, q_ = F(pn, 2), F(qn, 2)
        if p_ == q_:
            continue
        def roots(b, c):
            d = b * b - 4 * c
            if d < 0:
                return set()
            r = sp.sqrt(sp.Rational(d.numerator, d.denominator))
            return {sp.nsimplify((-sp.Rational(b.numerator, b.denominator) + r) / 2), sp.nsimplify((-sp.Rational(b.numerator, b.denominator) - r) / 2)}
        A = {sp.Integer(-1), sp.Integer(2)} | roots(p_, q_)
        B = {sp.Integer(-1), sp.Integer(2)} | roots(q_, p_)
        if len(A | B) == 5 and len(A & B) == 3:
            res.add(sp.simplify(sum(A | B)))
chk("g330", res.pop() if len(res) == 1 else None, 1)
ok_a = []
for j in range(-400, 401):
    a = F(j, 40)
    # A=(a−2, a+2), B=(−∞, 2a−5] ∪ [a²−a−1, ∞): 서로소인지 확인
    if 2 * a - 5 <= a - 2 and a + 2 <= a * a - a - 1:
        ok_a.append(a)
chk("g311", max(ok_a), 3)
# 성질·법칙 ---------------------------------------------------------------
def holds(cond, concl):
    return all(concl(A, B) for A in ALL4 for B in ALL4 if cond(A, B) and A and B)
c = lambda A, B: A & B == B
chk("n1909", mark([holds(c, lambda A, B: A <= B), holds(c, lambda A, B: cp(A) <= cp(B)), holds(c, lambda A, B: A | B == U4)], ["ㄱ", "ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"]), "②")
c = lambda A, B: cp(A | B) == cp(B)
chk("n2376", mark([all(B <= A for A in ALL4 for B in ALL4 if c(A, B)), all(A & B == A for A in ALL4 for B in ALL4 if c(A, B)),
                   all(cp(B) <= cp(A) for A in ALL4 for B in ALL4 if c(A, B)), all(B - A == frozenset() for A in ALL4 for B in ALL4 if c(A, B))],
                  ["ㄴ", "ㄱ, ㄹ", "ㄴ, ㄷ", "ㄷ, ㄹ", "ㄴ, ㄷ, ㄹ"]), "③")
chk("g281", sum({1, 3, 5} | {1, 2, 5, 7}), 18)
U = frozenset(range(1, 11))
As = {A for A in subsets(U) for B in subsets(U) if (U - A) & B == {6, 8} and (U - A) & (U - B) == {4, 7, 10}}
chk("g283", sum(As.pop()) if len(As) == 1 else None, 20)
st = [lambda A, B, C: ((A | B) & (A & cp(B))) | (cp(A) & B) == cp(A & B),
      lambda A, B, C: (A - B) & (A - C) == A - (B | C),
      lambda A, B, C: (A - cp(B)) - C == A - (cp(B) - C),
      lambda A, B, C: ((A | B) & (cp(A) | B)) & ((cp(B) & C) | cp(B | C)) == U4]
chk("g315", sum(1 for f in st if all(f(A, B, C) for A in ALL4 for B in ALL4 for C in ALL4)), 1)
U = set(range(1, 51)); A = {v for v in U if v % 6 == 0}; B = {v for v in U if v % 4 == 0}
chk("m2203x2", sum(1 for X in subsets(A) if not (B & X)), 16)
A = {v for v in range(1, 16) if v % 2}; B = {pow(7, n, 10) for n in range(1, 20)}
chk("g334", sum(1 for X in subsets(A) if B <= X), 16)
U = frozenset(range(1, 10)); A = frozenset({1, 3}); B = frozenset({2, 4, 6})
chk("n1841", sum(1 for X in subsets(U) if len(X | A) == 5 and len(X - B) == 3), 52)
U = frozenset(range(1, 7))
chk("g339", sum(1 for A in subsets(U) for B in subsets(U) if len(A) < 5 and A & B == {6}), 232)
N_ = 600
def mult(k):
    return frozenset(range(k, N_ + 1, k))
chk("g285", mark([mult(2) | mult(4) == mult(2), mult(2) & mult(3) == mult(6), mult(2) & (mult(3) | mult(4)) == mult(2) | mult(6)], ["ㄱ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"]), "②")
chk("n1564", sum(1 for n in range(1, 31) if mult(n) & mult(2) == mult(2 * n) and not (mult(n) - mult(3))), 5)
U = set(range(1, 21))
An = lambda n: {v for v in U if v % n == 0}
Bm = lambda m: {v for v in U if v % m == 2}
p_ = [v for v in U if all(v in Bm(m) for m in range(3, 60))]
q_ = min(m for m in range(3, 60) if len(Bm(m)) == 2)
r_ = min(n for n in range(3, 60) if len((U - An(n)) & (Bm(4) | Bm(6))) == 6)
chk("e10-12", p_[0] + q_ + r_ if len(p_) == 1 else None, 19)
Sab = lambda A, B: len(cp(A) | B)
g1 = all(Sab(A, B) == Sab(B, A) for A in ALL4 for B in ALL4 if not (A & B))
g2 = all(Sab(B, A) - Sab(A, B) == len(A & B) - len(A | B) for A in ALL4 for B in ALL4 if A <= B)
g3 = all(len(A) <= len(B) for A in ALL4 for B in ALL4 if Sab(A, B) >= Sab(B, A))
chk("g323", mark([g1, g2, g3], MC_B3), "④")
PS = lambda X: frozenset(subsets(X))
g1 = all(PS(A) <= PS(B) for A in ALL4 for B in ALL4 if A <= B)
g2 = all(PS(A & B) == PS(A) & PS(B) for A in ALL4 for B in ALL4)
g3 = all(PS(A | B) == PS(A) | PS(B) for A in ALL4 for B in ALL4)
chk("g347", mark([g1, g2, g3], ["ㄱ", "ㄴ", "ㄱ, ㄴ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"]), "③")
chk("o19", 42 - 23, 19)
sol = set()
for mb in range(0, 51):        # 두 서비스를 모두 이용하는 남자
    for wb in range(0, 41):
        m1, w1 = 50 - mb, 40 - wb
        if (m1 + w1) + 2 * (mb + wb) == 115 and w1 == m1 + 15:
            sol.add(mb)
chk("n1938", sol.pop() if len(sol) == 1 else None, 25)
vals = [(30 - 2 * t) for t in range(0, 31) if 20 + 10 - t <= 30 and t <= 10]
chk("n1915", max(vals) * min(vals), 300)
best = 0
for ab in range(0, 26):
    for ba in range(0, 26):
        for out in range(0, 26):
            if 11 + ab + ba + out == 25 and ab >= 1:
                best = max(best, ba)
chk("e13-13", best, 13)
# g332: 영역 개수를 모두 훑음(세 집합의 7영역 + 바깥)
best = None
for x in range(0, 28):
    for r12 in range(0, 31):
        for r13 in range(0, 31 - r12):
            r23 = 30 - r12 - r13
            r1 = 33 - r12 - r13 - x
            r2 = 32 - r12 - r23 - x
            r3 = 27 - r13 - r23 - x
            if min(r1, r2, r3) < 0:
                continue
            if r1 + r2 + r3 + 30 + x <= 50:
                best = x if best is None else min(best, x)
chk("g332", best, 6)
# 고난도 ---------------------------------------------------------------
A = frozenset({1, 2, 4, 6, 8}); U = frozenset(range(1, 9))
cnt = 0
for a in range(2, 9):
    for b in range(a + 1, 9):
        B = frozenset({1, a, b})
        if sum(1 for Cc in subsets(U) if A | Cc == B | Cc) == 16:
            cnt += 1
chk("g360", cnt, 12)
U6 = frozenset(range(1, 7))
SS = lambda X: sum(X)
g1 = all(A <= B for A in subsets(U6) for B in subsets(U6) if SS(A) < SS(B))
g2 = all(SS(A) + SS(B) == 21 for A in subsets(U6) for B in [U6 - A])
g3 = sum(1 for B in subsets(U6) if 7 <= SS(B)) == 50
chk("g355", mark([g1, g2, g3], MC_B3), "④")
vals = set()
for k in range(1, 30):
    for m in range(1, k + 1):
        Uu = set(range(1, k + 1)); A = {d for d in Uu if m % d == 0}
        if 4 in A or 7 in A or not {4, 7} <= Uu:
            continue
        for r in range(len(A) + 1):
            for ab in itertools.combinations(sorted(A), r):
                B = set(ab) | {4, 7}
                if len(A | (Uu - B)) == 7 and sum(A) == sum(B):
                    vals.add(sum(Uu - (A | B)))
chk("m2203x1", vals.pop() if len(vals) == 1 else None, 22)
# m2311x: 원소 5개를 8개 영역에 넣는 모든 경우
ok1 = ok2 = True
prods = set()
for asg in itertools.product(range(8), repeat=5):
    cnt_ = [asg.count(r) for r in range(8)]
    nA = sum(cnt_[r] for r in range(8) if r & 1); nB = sum(cnt_[r] for r in range(8) if r & 2); nC = sum(cnt_[r] for r in range(8) if r & 4)
    if cnt_[6] + cnt_[7] != 2 or cnt_[2] + cnt_[6] != 1 or cnt_[4] + cnt_[6] != 2:
        continue
    if cnt_[7] == 0:
        ok1 = False
    if cnt_[7] == 2 and nC != 4:
        ok2 = False
    prods.add(nA * nB * nC)
chk("m2311x", mark([ok1, ok2, max(prods) + min(prods) == 42], MC_BOGI), "⑤")
ivs = [(k - 1, k + 1) for k in range(1, 10)]
g1 = True   # [0,2]∩[1,3]∩[2,4] = {2}
g2 = all(max(ivs[l][0], ivs[m][0]) <= min(ivs[l][1], ivs[m][1]) for l in range(9) for m in range(9) if abs(l - m) <= 2)
pts = []
for lo, hi in sorted(ivs, key=lambda t: t[1]):
    if not any(lo <= p <= hi for p in pts):
        pts.append(hi)
chk("m2011x1", mark([g1, g2, len(pts) == 4], MC_B2), "③")
best = None
for a in range(1, 21):
    for b in range(1, 21):
        Uu = set(range(1, 21)); A = {v for v in Uu if v % a == 0}; B = {v for v in Uu if b % v == 0}
        if {3, 6} <= A & B and len(B - A) == 2:
            s_ = sum(A - B)
            best = s_ if best is None else min(best, s_)
chk("m2410-27", best, 27)
sol = []
for k in range(2, 200):
    Uu = set(range(1, k + 1)); A = {v for v in Uu if v % 2 == 0}; B = {v for v in Uu if k % v == 0}
    Cc = Uu - (A | B)
    if len(A) * len(Cc) == 15:
        sol.append(math.prod(Cc))
chk("m2403-28", sol[0] if len(sol) == 1 else None, 189)
X = range(1, 11)
best = 0
for AB in itertools.combinations(X, 2):
    for BA in itertools.combinations([v for v in X if v not in AB], 3):
        sAB, sBA = set(AB), set(BA)
        if not all(F(p + 2, 3) in sBA for p in sAB):
            continue
        need = {q + 3 for q in sBA}
        if any(v > 10 for v in need) or need & sBA:
            continue
        best = max(best, sum(BA))
chk("m2603-19", best, 12)
U = [1, 2, 4, 8, 16, 32]
best = None
for asg in itertools.product(range(4), repeat=6):   # 0: 바깥, 1: A만, 2: B만, 3: 둘 다
    A = {u for u, r in zip(U, asg) if r & 1}; B = {u for u, r in zip(U, asg) if r & 2}
    BmA = B - A
    if not (2 <= len(BmA) <= 4) or len(A | B) != 5:
        continue
    if sum(set(U) - BmA) == 6 * sum(BmA):
        best = sum(A) if best is None else min(best, sum(A))
chk("m2211x", best, 22)
P = {2, 3, 5, 7, 11, 13}; Uu = set(range(1, 16))
cnt = 0
for r in range(0, 16):
    for Xs in itertools.combinations(sorted(Uu), r):
        Xs = set(Xs)
        if len(Xs - P) * len(Xs | (Uu - P)) != 11:
            continue
        if sp.divisor_count(math.prod(Xs)) == 16:
            cnt += 1
chk("m2503-29", cnt, 38)
# m2011x2: 조건을 만족시키는 A, B를 모두 비트로 만들고 짝을 훑음
def valid(mask, mod):
    el = [i + 1 for i in range(20) if mask >> i & 1]
    return all((x + y) % mod for x, y in itertools.combinations(el, 2))
As, Bs = [], []
for c in itertools.combinations(range(20), 8):
    m = sum(1 << i for i in c)
    s_ = sum(i + 1 for i in c)
    if valid(m, 9):
        As.append((s_, m))
    if valid(m, 10):
        Bs.append((s_, m))
As.sort(reverse=True); Bs.sort()
best = None
for sa, ma in As:
    if best is not None and sa - Bs[0][0] <= best:
        break
    for sb, mb in Bs:
        if best is not None and sa - sb <= best:
            break
        if bin(ma & mb).count("1") == 1:
            best = sa - sb if best is None else max(best, sa - sb)
            break
chk("m2011x2", best, 63)
# m2410-30: 구한 f, g가 조건을 모두 만족시키는지 확인
xx = sp.symbols("x", real=True)
f = sp.Rational(1, 4) * (xx - 2) ** 2 - sp.Rational(5, 4)
g = -sp.Rational(1, 2) * (xx - 1) ** 2 + 1
Xs = set(sp.solve(f - 1, xx)) | set(sp.solve(f + 1, xx))
Ys = set(sp.solve(g - 1, xx)) | set(sp.solve(g + 1, xx))
okc = len(Xs & Ys) == 3 and len(Xs | Ys) == 4 and sum(Xs & Ys) == 3 and sum(Xs | Ys) == 8 and f.subs(xx, 2) < f.subs(xx, 1)
# 다른 경우(n(X)=3)는 f(2)<f(1)에 맞지 않음을 확인
f2 = sp.Rational(1, 2) * (xx - 1) ** 2 - 1
okc = okc and not (f2.subs(xx, 2) < f2.subs(xx, 1))
chk("m2410-30", f.subs(xx, 7) - g.subs(xx, 9) if okc else None, 36)

# 2026 중간 17개교 등 추가 문항 ----------------------------------------------
chk("j1-5", sum(1 for X in subsets([1, 2, 3, 4, 5, 6]) if not (X & {2, 3, 4})), 8)
A, B = {-1, 0, 1}, {2, 3}
P = {x + y for x in A for y in A}; Q = {x * y for x in A for y in B}
chk("j12-18", len(Q - P), 2)
U = frozenset(range(1, 9)); vals = set()
for Aa in subsets(U):
    if Aa - (U - {8}) or 8 in Aa:
        pass
    for Cc in subsets(U):
        if U - (Aa | Cc) != {8} or Cc - Aa != {1, 6}:
            continue
        for Bb in subsets(Aa):
            if Aa - Bb == {2, 7} and Bb - Cc == {5}:
                vals.add(sum(Aa - (Bb - Cc)))
chk("j16-9", vals.pop() if len(vals) == 1 else None, 16)
xs = sp.symbols("x")
def rset(e):
    return {sp.nsimplify(r) for r in sp.solve(e, xs) if r.is_real}
def froots(b, c):   # x²+bx+c=0의 실근(수치)
    d = b * b - 4 * c
    if d < 0:
        return set()
    r = math.sqrt(d)
    return {round((-b + r) / 2, 9), round((-b - r) / 2, 9)}
res = set()
for an in range(-80, 81):
    for bn in range(-80, 81):
        a_, b_ = an / 4, bn / 4
        A_ = froots(-a_, b_); B_ = froots(-a_, b_ + 1)
        if (A_ - B_) | (B_ - A_) == {1.0, 2.0, 3.0}:
            res.add(a_ + b_)
chk("j3-17", res.pop() if len(res) == 1 else None, 7)
ok = [a_ for a_ in range(-40, 41) if len(froots(4, a_) ^ froots(a_, 4)) == 2]
chk("j10-16", min(ok), -5)
U = set(range(1, 101))
forced = all(A == U4 for A in ALL4 for B in ALL4 if (A | B) == U4 and B & cp(B - A) == B)
chk("e4-9", 100 if forced else None, 100)
U = frozenset(range(1, 7)); A, B = frozenset({1, 3, 5}), frozenset({2, 5})
chk("j14-4", sum(1 for Cc in subsets(U) if Cc != U and A | Cc == B | Cc), 7)
U = set(range(1, 51)); An = lambda n: {v for v in U if v % n == 0}
chk("j10-7", sum(k for k in range(1, 101) if 2 ** len(An(3) & (An(4) | An(k))) == 256), 17)
U = set(range(1, 19)); res = []
for k in range(1, 60):
    Ak = {x for x in U for y in U if x * (y - k) == 30}; Bk = {d for d in U if k % d == 0}
    if len(Ak) * len(U - (Ak | Bk)) == 36:
        res.append(sum(Ak - Bk))
chk("j16-15", res[0] if len(res) == 1 else None, 30)
chk("e6-20", (100 - 25) - (50 + 40 - (100 - 25)), 60)
res = {a + i for a in range(15) for b in range(15) for i in range(min(a, b) + 1) if 2 ** a + 2 ** b == 2 ** 10 and (2 ** a + 2 ** b) * 8 == 2 ** (a + b - i)}
chk("j2-19", res.pop() if len(res) == 1 else None, 14)
A = frozenset({2, 4, 6, 8, 10, 12}); best = 0
for X in subsets(range(1, 15)):
    if 2 ** len(A | X) == 2 ** len(A) + 2 ** len(X):
        best = max(best, sum(A & X))
chk("j11-13", best, 40)
prods = []
for asg in itertools.product(range(4), repeat=10):   # 0 바깥, 1 A만, 2 B만, 3 둘 다
    if asg.count(1) != asg.count(2) or asg.count(1) != asg.count(3):
        continue
    A_ = [i + 1 for i, r in enumerate(asg) if r & 1]; B_ = [i + 1 for i, r in enumerate(asg) if r & 2]
    uni = sum(i + 1 for i, r in enumerate(asg) if r)
    if 55 - uni == 4 * uni:
        prods.append(sum(A_) * sum(B_))
chk("j14-11", max(prods) - min(prods), 63)
U = set(range(1, 9)); A = {x for x in U if x * x - 9 * x + 20 > 0}; B = {x for x in U if x ** 3 - 18 * x * x + 87 * x - 110 == 0}; Ac = U - A
cnt = 0
for X in subsets(sorted(U)):
    Cc = {abs(p - q) for p in Ac for q in X if p != q}
    if len(A & (B | X)) == 3 and len(Cc) == 4:
        cnt += 1
chk("j8-24", cnt, 47)
def kcount(x):   # x∈A_k인 정수 k의 개수(구간 [x−1, x+1]의 정수)
    return math.floor(x + 1) - math.ceil(x - 1) + 1
pts = [F(n, 7) for n in range(-70, 71)]
Xm = {m: {p for p in pts if kcount(p) == m} for m in range(0, 8)}
g1 = not Xm[0] and not Xm[1]
g2 = all(not Xm[m] for m in range(4, 8))
g3 = all((sum(k for k in range(math.ceil(p - 1), math.floor(p + 1) + 1))) % 2 == 1 for m in range(8) for p in Xm[m])
chk("j1-15", mark([g1, g2, g3], ["ㄱ", "ㄷ", "ㄱ, ㄴ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"]), "③")

# 기본서에서 옮긴 문항(2026-11-06) --------------------------------------------------
U = frozenset(range(1, 11)); sol = set()
rest = U - {5, 7, 3, 9, 10}
for AmB in subsets(rest):
    A = AmB | {5, 7}; B = (rest - AmB) | {5, 7}
    if sum(A) == 2 * sum(B):
        sol.add(math.prod(B))
chk("g308", sol.pop() if len(sol) == 1 else None, 70)
tot = F(0)
for j in range(-400, 401):
    av = F(j, 8)
    lo, hi = max(F(2), av), min(F(3), av + 1)
    if lo == hi:
        tot += av
chk("e11-22", tot, 4)
U = frozenset(range(1, 10)); A, B = frozenset({1, 2, 3, 4}), frozenset({3, 4, 5, 6})
chk("e1-14", sum(1 for X in subsets(U) if A - X == B - X and len((X - A) & (X - B)) >= 1), 28)
M_ = lambda k: frozenset(range(k, 2001, k))
chk("e12-13", sum(k for k in range(2, 100) if (M_(4) & M_(6)) <= M_(k)), 27)
sol = set()
for bb in range(0, 25):
    for gg in range(0, 33):
        if (24 - bb + 32 - gg) + 2 * (bb + gg) == 64 and 32 - gg == 24 - bb + 4:
            sol.add(gg)
chk("n2812", sol.pop() if len(sol) == 1 else None, 6)

if __name__ == "__main__":
    bad = [r for r in R if not r[1]]
    print("검산", len(R), "불일치", len(bad))
    for r in bad:
        print(r)
