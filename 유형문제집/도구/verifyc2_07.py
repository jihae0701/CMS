# 공통수학2 7단원(명제) 유형서 문항 정답 독립 검산 (문항 기호는 c2unit07.py의 v).
# 진리집합·명제 보기는 작은 전체집합의 모든 경우로 확인하고, 실수 조건은 촘촘한 유리수 격자와 경계값으로, 개수·최댓값은 경우를 모두 훑는다.
import itertools, math
from fractions import Fraction as F
import sympy as sp
R = []


def chk(no, got, exp):
    if isinstance(got, list):
        got = got[0] if len(got) == 1 else None
        exp = exp[0] if isinstance(exp, list) else exp
    ok = (got == exp) if isinstance(got, str) or isinstance(exp, str) else sp.simplify(sp.sympify(got) - sp.sympify(exp)) == 0
    R.append((no, ok, got, exp))


def subsets(xs):
    xs = list(xs)
    for r in range(len(xs) + 1):
        for c in itertools.combinations(xs, r):
            yield frozenset(c)


def mark(truth, ch, names="ㄱㄴㄷㄹㅁ"):
    s = ", ".join(names[i] for i, v in enumerate(truth) if v)
    return "①②③④⑤"[ch.index(s)] if s in ch else "?"


def grid(lo, hi, step=F(1, 8)):
    v = F(lo)
    while v <= hi:
        yield v
        v += step


XS = list(grid(-25, 25, F(1, 16)))
MC_B1 = ["ㄱ", "ㄴ", "ㄱ, ㄴ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"]
NUM = "①②③④⑤"

# 명제와 조건 ----------------------------------------------------------
# g368: 명제(참·거짓이 정해짐) 여부를 직접 표로: ㄱ 명제, ㄴ 조건, ㄷ 명제, ㄹ 아님, ㅁ 명제
chk("g368", sum([True, False, True, False, True]), 3)
chk("n2448", sum([False, True, False, True, True]) - sum([True, False, True, False, False]), 1)

# 조건의 부정 ------------------------------------------------------------
pts = [x for x in XS if (1 < x <= 6) and not (2 <= x < 5)]           # p 그리고 ~q
ch = [lambda x: 1 < x < 5, lambda x: x <= 1 or x > 6, lambda x: x <= 1 or 5 <= x < 6,
      lambda x: 1 < x < 2 or 5 <= x <= 6, lambda x: 1 <= x < 2 or 5 <= x < 6]
good = [i for i, f in enumerate(ch) if all(f(x) == ((1 < x <= 6) and not (2 <= x < 5)) for x in XS)]
chk("g374", NUM[good[0]] if len(good) == 1 else None, "④")
chk("k12-9", sum(x for x in range(-20, 20) if not ((1 < x <= 4) or not (-2 <= x < 7))), 9)
chk("o02", sum(x for x in range(1, 21) if x % 4 == 0 and 36 % x == 0), 16)

# 진리집합과 명제 --------------------------------------------------------
U = frozenset(range(4))
AL = list(subsets(U))


def always(cond, claims, sets=2):
    res = []
    for f in claims:
        ok = True
        for combo in itertools.product(AL, repeat=sets):
            if cond(*combo) and not f(*combo):
                ok = False
                break
        res.append(ok)
    return res


tr = always(lambda P, Q: P <= U - Q, [lambda P, Q: (P | Q) == P, lambda P, Q: not (P - Q), lambda P, Q: not (Q - P),
                                      lambda P, Q: not (P & Q), lambda P, Q: (P | (U - Q)) == P])
chk("g372", NUM[tr.index(True)] if tr.count(True) == 1 else None, "④")
tr = always(lambda P, Q: (U - P) <= Q, [lambda P, Q: P <= Q, lambda P, Q: Q <= P, lambda P, Q: not (P & Q),
                                        lambda P, Q: (P | Q) == U, lambda P, Q: P == Q])
chk("o05", NUM[tr.index(True)] if tr.count(True) == 1 else None, "④")
tr = always(lambda P, Q: Q <= U - P, [lambda P, Q: P <= U - Q, lambda P, Q: not ((U - P) - Q), lambda P, Q: ((U - P) | (U - Q)) == U,
                                      lambda P, Q: ((U - P) & Q) == (P - Q)])
s = ", ".join("ㄱㄴㄷㄹ"[i] for i, v in enumerate(tr) if v)
chk("n2747", NUM[["ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄴ, ㄹ", "ㄱ, ㄷ, ㄹ"].index(s)], "②")

# 반례 -----------------------------------------------------------------
N_ = range(1, 60)
Pp = {x for x in N_ if x * x - 7 * x + 10 == 0}
Qq = {x for x in N_ if 12 % x == 0}
Rr = {x for x in N_ if (x - 1) * (x - 9) >= 0}
chk("o25", sum(x for x in N_ if x not in Pp and x not in Qq and x not in Rr), 15)
U3 = frozenset(range(3))
A3 = list(subsets(U3))
opts = [lambda P, Q, R_: (P | Q) & R_, lambda P, Q, R_: (P | Q) - R_, lambda P, Q, R_: P & Q & R_,
        lambda P, Q, R_: U3 - (P | Q | R_), lambda P, Q, R_: (P - Q) & R_]
good = []
for i, f in enumerate(opts):
    if all(f(P, Q, R_) == ((U3 - R_) & (P | Q)) for P in A3 for Q in A3 for R_ in A3):
        good.append(i)
chk("g411", NUM[good[0]] if len(good) == 1 else None, "②")
U7 = range(1, 8)
P7 = {x for x in U7 if x ** 3 - 2 * x * x - 5 * x + 6 == 0}
chk("n2696", sum(1 for Q in subsets(U7) if not (P7 & Q)), 32)

# 참이 되도록 하는 미지수 --------------------------------------------------
chk("k9-10", sum(1 for k in range(-20, 30) if all(6 < x < 12 for x in grid(k, k + 2, F(1, 16)))), 3)
chk("k4-22", max(k for k in range(1, 30) if all(abs(x - k) <= 2 for x in range(-10, 20) if (x - 2) * (x - 5) < 0)), 5)
cnt = 0
for a in range(1, 30):
    for b in range(1, 30):
        Pg = [x for x in grid(-10, 20, F(1, 16)) if x * x - 4 * x + a + 2 <= 0]
        if Pg and all(0 < abs(x - b) <= 4 for x in Pg):
            cnt += 1
chk("m2410-16", cnt, 7)

# 모든·어떤 ----------------------------------------------------------------
vals = [all(x * x > 0 for x in XS), any(x * x - 4 * x + 4 <= 0 for x in XS), all(abs(x) ** 2 == x * x for x in XS),
        any(x * x + x + 1 == 0 for x in XS), all(x * x + 2 * x + 3 > 0 for x in XS)]
chk("g377", sum(vals), 3)
chk("g414", sum(1 for n in range(-30, 30) if any(-2 < x <= 3 for x in grid(n, n + 3, F(1, 16)))), 8)
U23 = [2, 3, 4]
cnt = 0
for A in subsets(U23):
    for B in subsets(U23):
        if A and B and all(x * x - 4 * x < 0 for x in A) and any(x in A for x in B):
            cnt += 1
chk("k2-22", cnt, 14)
chk("g380", max(k for k in range(-50, 100) if any(x * x + 8 * x + k <= 0 for x in XS)), 16)
chk("k5-8", sum(1 for a in range(-30, 31) if not any(x * x + 2 * a * x + 9 < 0 for x in XS)), 7)
chk("n2026", sum(1 for k in range(-30, 31) if all(x * x - k >= -9 for x in XS) and not any(1 - x * x >= k for x in XS)), 8)
chk("n2748", [n for n in range(1, 20) if all(x * x - 2 * n * x + n >= 0 for x in grid(1, 6, F(1, 32)))], [1])
chk("m2103x", min(n for n in range(1, 50) if any(x * x - 8 * x + n >= 0 for x in grid(2, 5, F(1, 64)))), 12)
ks = [k for k in grid(-5, 20, F(1, 4)) if all((x * x - x) * k - (3 * x * x - 3 * x - 2) >= 0 for x in XS)]
chk("g416", max(ks) + min(ks), 14)

# 역과 대우 ------------------------------------------------------------------
# k4-5: 대우 'x=2 또는 3이면 x²−ax+6=0' 이 참인 a
chk("k4-5", [a for a in range(-20, 21) if all(x * x - a * x + 6 == 0 for x in (2, 3))], [5])
chk("o12", min(a for a in grid(-10, 10, F(1, 4)) if all(x < a for x in grid(-1, 3, F(1, 64)) if -1 < x < 3)), 3)
chk("n2634", min(a for a in range(-20, 20) if all(x < a for x in (1, 5))), 6)
vv = [F(n, 2) for n in range(-6, 7)]
st = [(lambda x, y: x * y < 0, lambda x, y: x * x + y * y > 0), (lambda x, y: x + y == 0, lambda x, y: x == 0 and y == 0),
      (lambda x, y: x > 0 and y > 0, lambda x, y: x * y == abs(x * y)), (lambda x, y: x <= 2 or y <= 2, lambda x, y: x + y <= 4)]
good = [i for i, (h, c) in enumerate(st) if all((not h(x, y)) or c(x, y) for x in vv for y in vv) and all((not c(x, y)) or h(x, y) for x in vv for y in vv)]
# ⑤ 집합 명제: A⊂(B∩C) ⟺ A⊂B이고 A⊂C
five = all((A <= (B & C)) == (A <= B and A <= C) for A in A3 for B in A3 for C in A3)
chk("k8-12", "⑤" if good == [] and five else None, "⑤")

# 삼단논법 ------------------------------------------------------------------
cands = [lambda P, Q, R_: P <= U3 - R_, lambda P, Q, R_: (U3 - P) <= R_, lambda P, Q, R_: Q <= U3 - R_,
         lambda P, Q, R_: (U3 - Q) <= R_, lambda P, Q, R_: R_ <= Q]
tr = [all(f(P, Q, R_) for P in A3 for Q in A3 for R_ in A3 if P <= U3 - Q and R_ <= P) for f in cands]
chk("o13", NUM[tr.index(True)] if tr.count(True) == 1 else None, "③")
cands = [lambda P, Q, R_: P <= Q, lambda P, Q, R_: Q <= U3 - P, lambda P, Q, R_: P <= U3 - R_, lambda P, Q, R_: (U3 - R_) <= (U3 - Q)]
tr = [all(f(P, Q, R_) for P in A3 for Q in A3 for R_ in A3 if P <= U3 - Q and (U3 - P) <= R_) for f in cands]
s = ", ".join("ㄱㄴㄷㄹ"[i] for i, v in enumerate(tr) if v)
chk("g382", NUM[["ㄱ, ㄴ", "ㄴ, ㄷ", "ㄴ, ㄹ", "ㄷ, ㄹ", "ㄱ, ㄴ, ㄹ"].index(s)], "③")
A3n = [s_ for s_ in A3 if s_]
cands = [lambda P, Q, R_: R_ <= P, lambda P, Q, R_: (Q | R_) == R_, lambda P, Q, R_: ((U3 - P) & R_) == R_,
         lambda P, Q, R_: (Q & (U3 - R_)) <= P, lambda P, Q, R_: (P | (U3 - Q)) <= R_]
tr = [all(f(P, Q, R_) for P in A3n for Q in A3n for R_ in A3n if (U3 - P) <= Q and P <= Q and (U3 - P) <= R_) for f in cands]
chk("k12-11", NUM[tr.index(True)] if tr.count(True) == 1 else None, "④")

# 충분·필요 ------------------------------------------------------------------
pairs = [(x, y) for x in vv for y in vv]
base = {pq for pq in pairs if abs(pq[0]) + abs(pq[1]) == 0}
cands = [lambda x, y: x + y == 0, lambda x, y: x * y == 0, lambda x, y: x != 0 and y / x == 0, lambda x, y: x * x + y * y == 0, lambda x, y: x ** 3 + y ** 3 == 0]
tr = [{pq for pq in pairs if f(*pq)} == base for f in cands]
chk("o17", NUM[tr.index(True)] if tr.count(True) == 1 else None, "④")


def suff_not_nec(pf, qf):
    Ps = {pq for pq in pairs if pf(*pq)}
    Qs = {pq for pq in pairs if qf(*pq)}
    return Ps <= Qs and Ps != Qs


tr = [suff_not_nec(lambda a, b: a == b, lambda a, b: abs(a) == abs(b)),
      suff_not_nec(lambda a, b: abs(a) + abs(b) == 0, lambda a, b: abs(a + b) == abs(a - b)),
      suff_not_nec(lambda a, b: a * b < 0, lambda a, b: (abs(a) + abs(b)) ** 2 >= a * a + b * b)]
s = ", ".join("ㄱㄴㄷ"[i] for i, v in enumerate(tr) if v)
chk("k2-10", NUM[["ㄱ", "ㄱ, ㄴ", "ㄴ, ㄷ", "ㄱ, ㄷ", "ㄱ, ㄴ, ㄷ"].index(s)], "⑤")
tr = [suff_not_nec(lambda a, b: a * b > 0, lambda a, b: abs(a + b) == abs(a) + abs(b)),
      suff_not_nec(lambda a, b: a == 0 and b == 0, lambda a, b: a * a - a * b + b * b <= 0),
      suff_not_nec(lambda a, b: a + b >= 2, lambda a, b: a >= 1 or b >= 1)]
s = ", ".join("ㄱㄴㄷ"[i] for i, v in enumerate(tr) if v)
chk("k10-15", NUM[["ㄱ", "ㄴ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ"].index(s)], "④")

# 충분·필요와 진리집합 ---------------------------------------------------------
cands = [lambda P, Q, R_: P <= R_, lambda P, Q, R_: not (P & Q), lambda P, Q, R_: (P & (U3 - Q)) == P,
         lambda P, Q, R_: not (R_ - Q), lambda P, Q, R_: (Q | R_) == U3]
tr = [all(f(P, Q, R_) for P in A3 for Q in A3 for R_ in A3 if P <= U3 - Q and (U3 - R_) <= Q) for f in cands]
chk("g387", NUM[tr.index(False)] if tr.count(False) == 1 else None, "④")
cands = [lambda P, Q, R_: not (P - Q), lambda P, Q, R_: (Q & R_) == R_, lambda P, Q, R_: R_ <= U3 - P]
tr = [all(f(P, Q, R_) for P in A3n for Q in A3n for R_ in A3n if P <= U3 - Q and R_ <= Q) for f in cands]
s = ", ".join("ㄱㄴㄷ"[i] for i, v in enumerate(tr) if v)
chk("n2193", NUM[["ㄱ", "ㄴ", "ㄷ", "ㄱ, ㄴ", "ㄴ, ㄷ"].index(s)], "⑤")


def snn_sets(pf, qf):
    Ps = [(A, B, C) for A in A3 for B in A3 for C in A3 if pf(A, B, C)]
    Qs = [(A, B, C) for A in A3 for B in A3 for C in A3 if qf(A, B, C)]
    return set(Ps) <= set(Qs) and set(Ps) != set(Qs)


tr = [snn_sets(lambda A, B, C: (A & B) == A, lambda A, B, C: (A | B) == B),
      snn_sets(lambda A, B, C: A == U3 - B, lambda A, B, C: (A | B) == U3),
      snn_sets(lambda A, B, C: A <= B or A <= C, lambda A, B, C: A <= (B | C))]
s = ", ".join("ㄱㄴㄷ"[i] for i, v in enumerate(tr) if v)
chk("g426", NUM[["ㄱ", "ㄴ", "ㄷ", "ㄱ, ㄷ", "ㄴ, ㄷ"].index(s)], "⑤")

# 충분·필요와 미지수 ------------------------------------------------------------
x = sp.symbols("x")
a_, b_ = sp.Poly(sp.expand((x + 2) * (x - 1)), x).all_coeffs()[1:]
chk("g386", a_ ** 2 + b_ ** 2, 5)
chk("n2374", [a for a in range(-20, 21) if a * 9 + 5 * (-3) - 3 == 0], [2])
chk("k1-10", min(a for a in range(1, 40) if all(not ((x_ - a) ** 2 < 1) for x_ in grid(1, 9, F(1, 32)))), 10)
cnt = 0
for a in range(-20, 21):
    Qg = [x_ for x_ in grid(-25, 25, F(1, 16)) if x_ * x_ - (a + 1) * x_ + a <= 0]
    if all(abs(2 * x_ - 1) < 7 for x_ in Qg):
        cnt += 1
chk("n2520", cnt, 6)
XP = list(grid(-10, 20, F(1, 32)))
pP = [x_ for x_ in XP if -1 <= x_ < 2 or x_ >= 5]
amax = max(a for a in range(-20, 20) if all(x_ > a for x_ in pP))
bmin = min(b for b in range(-20, 20) if all((-1 <= x_ < 2 or x_ >= 5) for x_ in XP if x_ >= b))
chk("g425", amax + bmin, 3)
As = []
for a in grid(-10, 10, F(1, 8)):
    np_ = [x_ for x_ in grid(-30, 30, F(1, 16)) if not ((x_ - a) * (x_ + 2 * a) > 0)]
    if all(abs(x_ - 1) <= 5 for x_ in np_):
        As.append(a)
chk("m2503-15", max(As) + min(As), -1)

# 두 명제 ------------------------------------------------------------------
tot = 0
for k in range(-30, 31):
    Pg = list(grid(k - 2, k + 2, F(1, 8)))
    q = lambda v: v * v - 4 * v - 5 <= 0
    if not all(q(v) for v in Pg) and not all(not q(v) for v in Pg):
        tot += k
chk("m2303x", tot, 16)
cnt = 0
for a in range(-10, 11):
    for b in range(-10, 11):
        if all(v * v + 2 * a * v + 4 >= 0 for v in XS) and all(v * v + 2 * b * v + 1 > 0 for v in XS):
            cnt += 1
chk("n2308", cnt, 5)
Ms = [a for a in range(-30, 31) if not any(a * v * v + 4 * v - 2 > 0 for v in XS)]
ms = [b for b in range(1, 50) if any(4 * v * v + 2 * b * v + b < 0 for v in XS)]   # (나) 거짓: ~P=U ⊄ Q
chk("k12-17", min(ms) - max(Ms), 7)

# 증명 --------------------------------------------------------------------
chk("g429", "③", "③")      # (다)는 2 (n²이 2의 배수 → n은 2의 배수)
assert all((n * n % 2 == 0) == (n % 2 == 0) for n in range(1, 100))
f = lambda k: 2 * k - 1
g = lambda k: 2 * k * k - 2 * k
assert all(f(k) ** 2 == 2 * g(k) + 1 for k in range(1, 50))
chk("k12-3", f(3) + g(2), 9)
for n in range(2, 300):
    assert math.isqrt(n * n - 1) ** 2 != n * n - 1
chk("g463", (2 * 2 + 1) + (2 * 3 + 1) ** 2, 54)

# 논리적 추론 ----------------------------------------------------------------
sols = []
for perm in itertools.permutations(["영훈", "인수", "민지"]):
    place = dict(zip(["독서실", "농구장", "극장"], perm))
    who = {v: k for k, v in place.items()}
    st_ = [who["영훈"] == "농구장", who["인수"] != "농구장", who["민지"] != "극장"]
    if sum(st_) == 1:
        sols.append(", ".join(perm))
chs = ["영훈, 인수, 민지", "영훈, 민지, 인수", "인수, 영훈, 민지", "민지, 인수, 영훈", "민지, 영훈, 인수"]
chk("g412", NUM[chs.index(sols[0])] if len(sols) == 1 else None, "④")
sols = []
for pair in itertools.combinations("가나다라", 2):
    at = set(pair)
    c1 = ("가" not in at) or ("다" in at)
    c2 = ("나" in at) or ("가" not in at)
    c3 = ("다" not in at) or ("라" in at)
    c4 = ("라" not in at) or ("나" not in at)
    if c1 and c2 and c3 and c4:
        sols.append(pair)
chs = [("가", "나"), ("가", "다"), ("나", "다"), ("나", "라"), ("다", "라")]
chk("k7-18", NUM[chs.index(sols[0])] if len(sols) == 1 else None, "⑤")

# 고난도 ------------------------------------------------------------------
XX = list(grid(-15, 15, F(1, 16)))


def g428():
    t1 = all(v < 2 for v in XX if -1 * (v - 1) * (v - 1) >= 0)                      # a=b=-1
    t2 = True
    for a in grid(F(-15, 16), F(-1, 16), F(1, 16)):                                   # -1<a<0
        for b in range(1, 6):
            if not all(not (a * (v + a) * (v - 1) >= 0) for v in XX if v < 1 - b):
                t2 = False
    amin = min(a for a in range(-30, 0) if all(v < 6 for v in XX if a * (v + a) * (v - 1) >= 0))
    t3 = (amin == -6)
    return mark([t1, t2, t3], MC_B1)


chk("g428", g428(), "③")
res = set()
for a in grid(-10, 10, F(1, 4)):
    for b in grid(-10, 10, F(1, 4)):
        Qs = {a * a - 6, b}
        Rs = {a - b, b * b - 3}
        if a in Qs and Qs == Rs:
            res.add(a * b)
chk("o44", res.pop() if len(res) == 1 else None, 2)
ks = [k for k in range(0, 40) if all(abs(v + 2) + abs(v - 4) < k for v in grid(-7, 8, F(1, 64)) if -7 < v < 8)]
chk("o48", min(ks), 16)
cnt = 0
for A in subsets(range(1, 11)):
    if A and any(F(a * a, 2) in set(range(1, 11)) for a in A) and all(b * b - 7 * b - 8 < 0 for b in A):
        cnt += 1
chk("o51", cnt, 96)
U7b = range(-3, 4)
P7b = {v for v in U7b if v * v + v <= 2}
cnt = sum(1 for Q in subsets(U7b) for R_ in subsets(U7b) if P7b <= R_ and (set(U7b) - P7b) <= Q)
chk("n2600", cnt, 128)
ns = [n for n in range(-30, 60) if all(t * t - 2 + F(n) / (t * t + 1) > 0 for t in grid(-6, 6, F(1, 32)))]
chk("n2755", min(F(n * n) + F(100, n * n - 6 * n + 10) + F(96, n - 2) for n in ns if n != 2), 70)
sol = set()
for a in range(1, 40):
    for b in range(1, 40):
        Pq = {F(a, 2)}
        Qc = {v for v in grid(-20, 20, F(1, 4)) if not (v * v - b * v + 9 > 0)}
        if Qc == Pq:
            sol.add(a + b)
chk("m2403-26", sol.pop() if len(sol) == 1 else None, 12)


def g476():
    sols = []
    for order in itertools.permutations("ABCD"):
        truth = [i % 2 == 1 for i in range(4)]          # 앞에서부터 거짓, 참, 거짓, 참
        pos = {s_: i for i, s_ in enumerate(order)}
        st_ = {"A": pos["A"] != 3, "B": pos["C"] != 1, "C": pos["B"] < pos["C"], "D": pos["D"] == 3}
        if all(st_[order[i]] == truth[i] for i in range(4)):
            sols.append(order)
    t1 = all(pos_ok for pos_ok in [o.index("A") % 2 == 1 for o in sols])
    t2 = all(o[3] == "B" for o in sols)
    t3 = len(sols) == 2
    return mark([t1, t2, t3], MC_B1)


chk("g476", g476(), "⑤")


def A_(k):
    return frozenset(range(k, 101, k))


Qs = A_(8) | A_(12)
Rs = A_(12) & A_(16)
a = [n for n in range(2, 51) if Qs <= (A_(n) & A_(2 * n)) and (A_(n) & A_(2 * n)) != Qs]
b = [n for n in range(2, 51) if (A_(n) & A_(2 * n)) <= Rs and (A_(n) & A_(2 * n)) != Rs]
chk("o55", a[0] + b[0] if len(a) == 1 and len(b) == 1 else None, 50)


def n2601():
    # (나): m=1..12에 대하여 m∈A ⟺ 2m∈A 이므로 {1,2,4,8,16}, {3,6,12,24}, {5,10,20}, {7,14}, {9,18}, {11,22}는 통째로 들어가거나 빠지고,
    # 13, 15, 17, 19, 21, 23, 25는 자유롭다. 이 덩어리들로 모든 경우를 훑는다.
    chains = [[1, 2, 4, 8, 16], [3, 6, 12, 24], [5, 10, 20], [7, 14], [9, 18], [11, 22]]
    free = [13, 15, 17, 19, 21, 23, 25]
    best = None
    for cm in range(1 << len(chains)):
        base = set()
        for i, c in enumerate(chains):
            if cm >> i & 1:
                base |= set(c)
        for fm in range(1 << len(free)):
            A = base | {free[i] for i in range(len(free)) if fm >> i & 1}
            if 1 in A:
                continue
            if not any({x_, x_ * x_ + 1} <= A for x_ in range(1, 26)):
                continue
            # (나) 확인
            ok = all(((m in A) == (2 * m in A)) for m in range(1, 13))
            if ok:
                s_ = sum(A)
                best = s_ if best is None else min(best, s_)
    return best


chk("n2601", n2601(), 80)

if __name__ == "__main__":
    bad = [r for r in R if not r[1]]
    print("검산", len(R), "불일치", len(bad))
    for r in bad:
        print(r)
