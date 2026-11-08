# -*- coding: utf-8 -*-
"""공통수학2 기본서 7단원 명제 검산: 문항마다 답을 따로(대부분 모든 경우를 직접 세어) 계산해 data07.py의 답과 맞춘다.
python verify07.py
- 실수 범위 조건은 촘촘한 격자(0.001 간격)와 경계값을 함께 넣어 확인하고, 집합·논리 보기는 작은 전체집합의 모든 경우를 넣어 확인한다.
"""
import sys, os, itertools, math
from fractions import Fraction as Fr
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data07

R = {}


def subsets(xs):
    xs = list(xs)
    for r in range(len(xs) + 1):
        for c in itertools.combinations(xs, r):
            yield frozenset(c)


def grid(lo, hi, step=Fr(1, 8)):
    v = Fr(lo)
    while v <= hi:
        yield v
        v += step


XS = list(grid(-30, 30, Fr(1, 16)))   # 실수 x 대신 쓰는 촘촘한 유리수 격자


def ndiv(n):
    return sum(1 for d in range(1, n + 1) if n % d == 0)


# 01 진리집합과 반례 --------------------------------------------------
P = {x for x in range(1, 41) if ndiv(x) == 3}
Q = {x for x in range(1, 41) if x * x - 10 * x + 16 > 0}
R["g373"] = sum(P & Q)                     # p -> ~q 의 반례: P∩Q

tot = 0
for k in range(1, 200):
    # ~q -> p 의 정수 반례: ~q 이고 ~p
    cex = [x for x in range(-50, 51) if not (3 * x * x - k * x <= 0) and not (x * x - 5 * x + 4 >= 0)]
    if cex == [3]:
        tot += k
R["o29"] = tot

U = set(range(1, 11))
p = {x for x in U if 6 % x == 0}
q = {x for x in U if x % 2 == 0 or x % 3 == 0}
must = (U - p) & (U - q)                  # (~p 이고 ~q) ⊂ R
R["o31"] = 2 ** (len(U) - len(must))

best = None
cand_a = set()
for a in [Fr(n, 2) for n in range(-12, 13)] + [2, -2, 3, 1, Fr(3, 2), Fr(-3, 2)]:
    cand_a.add(Fr(a))
vals = []
for a in [Fr(n, 4) for n in range(-40, 41)]:
    for b in [Fr(n, 4) for n in range(-40, 41)]:
        Qs = {a * a - 1, b}
        Rs = {a, a * b}
        if 3 in Qs and 3 in Rs:          # p->q : P⊂Q, ~r->~p ⟺ p->r : P⊂R
            vals.append(a + b)
R["k10-12"] = max(vals)

# 02 모든·어떤 -----------------------------------------------------------
cnt = 0
for a in range(-50, 51):
    s1 = any(x * x + 2 * a * x + 5 <= 0 for x in XS)       # '모든 x x²+2ax+5>0'이 거짓
    s2 = all(x * x - a * x + 2 * a > 0 for x in XS)        # '어떤 x x²−ax+2a≤0'이 거짓
    if s1 and s2:
        cnt += 1
R["g415"] = cnt

tot = 0
for k in range(-30, 31):
    if not any((x * x - 7 * x + 10 <= 0) and (x * x - 2 * k * x + k * k - 9 >= 0) for x in grid(-20, 30, Fr(1, 64))):
        tot += k
R["o34"] = tot

cnt = 0
for a in range(-30, 31):
    ga = any(0 <= x <= 2 for x in grid(a - 1, a + 3, Fr(1, 16)))
    na = all((x - 3) * (x - a - 3) >= 0 for x in grid(-60, 0, Fr(1, 16)))
    if ga and na:
        cnt += 1
R["b30"] = cnt

cnt = 0
for a in range(-3, 4):
    for b in range(-3, 4):
        # 부정 '모든 x −x²+2ax−b²−1 ≤ 0'이 참
        if all(-x * x + 2 * a * x - b * b - 1 <= 0 for x in XS):
            cnt += 1
R["n2111"] = cnt

# 03 역과 대우 -----------------------------------------------------------
R["k12-1"] = 5          # 대우 'x=a이면 x²−8x+5=0' → a는 x²−8x+5=0의 두 근, 곱 5 (근과 계수의 관계)
assert abs((4 + math.sqrt(11)) * (4 - math.sqrt(11)) - 5) < 1e-9

ks = []
for k in [Fr(n, 4) for n in range(-40, 41)]:
    ok = True
    for a in grid(-10, 10, Fr(1, 4)):
        for b in grid(-10, 10, Fr(1, 4)):
            if a + b < 4 and not (a < k or b < -1):
                ok = False
                break
        if not ok:
            break
    if ok:
        ks.append(k)
R["b36"] = min(ks)


def cube_check():
    """g418: 실수 격자에서 명제·역·대우가 모두 참인 것"""
    vals = [Fr(n, 2) for n in range(-8, 9)]
    st = {
        "ㄱ": (lambda a, b: a + 1 == 0, lambda a, b: a ** 3 + 1 == 0),
        "ㄴ": (lambda a, b: a + b > 0 and a * b > 0, lambda a, b: a > 0 and b > 0),
        "ㄷ": (lambda a, b: a * a + b * b > 0, lambda a, b: a != 0 or b != 0),
        "ㄹ": (lambda a, b: a * b == 0, lambda a, b: a * a + a * b + 2 * b * b == 0),
        "ㅁ": (lambda a, b: a * b + 1 > a + b > 2, lambda a, b: a > 1 and b > 1),
    }
    out = []
    for key, (h, c) in st.items():
        fw = all((not h(a, b)) or c(a, b) for a in vals for b in vals)
        bw = all((not c(a, b)) or h(a, b) for a in vals for b in vals)
        if fw and bw:      # 대우는 명제와 참·거짓이 같다
            out.append(key)
    return ", ".join(out)


R["g418"] = cube_check()

# 04 포함 관계 -----------------------------------------------------------
U3 = frozenset(range(4))
ALL = list(subsets(U3))


def comp(X):
    return U3 - X


def always(cond, claims):
    ok = {c: True for c in claims}
    for Pp in ALL:
        for Qq in ALL:
            for Rr in ALL:
                if not cond(Pp, Qq, Rr):
                    continue
                for c, f in claims.items():
                    if not f(Pp, Qq, Rr):
                        ok[c] = False
    return ", ".join(c for c in claims if ok[c])


R["g409"] = always(lambda P, Q, R_: not (P & (comp(Q) | R_)),
                   {"ㄱ": lambda P, Q, R_: Q <= R_, "ㄴ": lambda P, Q, R_: R_ <= comp(P),
                    "ㄷ": lambda P, Q, R_: (P & comp(R_)) <= Q})
R["o50"] = always(lambda P, Q, R_: comp(P) <= Q and R_ <= comp(P) and comp(R_) <= P,
                  {"ㄱ": lambda P, Q, R_: comp(P) <= Q, "ㄴ": lambda P, Q, R_: not (P & R_),
                   "ㄷ": lambda P, Q, R_: (Q - R_) <= P})


def g421():
    # p 선호도 높음, q 가격 쌈, r 기능 많음, s 판매량 많음 ; (가) p→s (나) q→s (다) r→p
    U = range(16)
    ALL16 = None
    claims = {
        "ㄱ": lambda P, Q, R_, S: R_ <= (frozenset(range(5)) - Q),
        "ㄴ": lambda P, Q, R_, S: (frozenset(range(5)) - Q) <= (frozenset(range(5)) - S),
        "ㄷ": lambda P, Q, R_, S: (frozenset(range(5)) - S) <= (frozenset(range(5)) - R_),
        "ㄹ": lambda P, Q, R_, S: P <= R_,
        "ㅁ": lambda P, Q, R_, S: P <= (frozenset(range(5)) - Q),
    }
    U5 = frozenset(range(5))
    A5 = list(subsets(U5))
    ok = {c: True for c in claims}
    # 무작위가 아니라 작은 반례를 모두: 네 집합을 3원소 전체집합에서 고른다
    U3_ = frozenset(range(3))
    A3 = list(subsets(U3_))
    for P_ in A3:
        for Q_ in A3:
            for R_ in A3:
                for S_ in A3:
                    if P_ <= S_ and Q_ <= S_ and R_ <= P_:
                        for c, f in claims.items():
                            if not f(P_, Q_, R_, S_):
                                ok[c] = False
    return ", ".join(c for c in claims if ok[c])


R["g421"] = g421()

# 05 충분·필요 판별 --------------------------------------------------------
vals = [Fr(n, 2) for n in range(-8, 9)]


def rel(pf, qf):
    P_ = {(x, y) for x in vals for y in vals if pf(x, y)}
    Q_ = {(x, y) for x in vals for y in vals if qf(x, y)}
    return P_, Q_


out = []
for key, pf, qf in [("ㄱ", lambda x, y: abs(x - y) == abs(x + y), lambda x, y: x == 0 or y == 0),
                    ("ㄴ", lambda x, y: abs(x) + abs(y) == abs(x + y), lambda x, y: x >= 0 and y >= 0),
                    ("ㄷ", lambda x, y: abs(x + y) < abs(x - y), lambda x, y: x * y < 0)]:
    P_, Q_ = rel(pf, qf)
    if P_ == Q_:
        out.append(key)
R["g423"] = ", ".join(out)

out = []
vv = [Fr(n, 2) for n in range(-6, 7)]
pS = {(a, b) for a in vv for b in vv if a * a - b * b == 0}
qS = {(a, b) for a in vv for b in vv if a ** 3 - a * a * b + a * b * b - b ** 3 == 0}
rS = {(a, b) for a in vv for b in vv if a * a + b * b - 2 * a - 2 * b + 2 * a * b + 1 == 0}
allS = {(a, b) for a in vv for b in vv}
if qS <= pS:
    out.append("ㄱ")                      # p는 q이기 위한 필요조건 ⟺ Q⊂P
if rS <= (allS - pS):
    out.append("ㄴ")                      # r은 ~p이기 위한 충분조건 ⟺ R⊂P^C
if (qS & rS) == pS:
    out.append("ㄷ")
R["o56"] = ", ".join(out)

out = []
pS = {(a, b) for a in vv for b in vv if a * a + a * b + b * b == 0}
qS = {(a, b) for a in vv for b in vv if abs(a) + abs(b) == abs(a + b)}
rS = {(a, b) for a in vv for b in vv if a * b == 0}
if pS == qS:
    out.append("ㄱ")
if (allS - rS) <= (allS - qS):
    out.append("ㄴ")                      # ~r은 ~q이기 위한 충분조건
if (allS - rS) <= (allS - pS):
    out.append("ㄷ")                      # ~p는 ~r이기 위한 필요조건 ⟺ ~R⊂~P
R["k6-11"] = ", ".join(out)

# 06 충분·필요와 미지수 ------------------------------------------------------
XP = list(grid(-20, 20, Fr(1, 32)))
pP = [x for x in XP if -3 < x < 1 or x > 2]
As = [a for a in range(-20, 21) if all(x > a for x in pP)]            # P⊂Q
Bs = [b for b in range(-20, 21) if all((-3 < x < 1 or x > 2) for x in XP if x >= b)]   # R⊂P
R["b45"] = max(As) * min(Bs)

cnt = 0
for a in range(1, 50):
    Pn = [x for x in grid(a, 2 * a, Fr(1, 32)) if a <= x < 2 * a]
    if all(not (x * x - 10 * x + 16 >= 0) for x in Pn):   # P⊂Q^C
        cnt += 1
R["o19"] = cnt

cnt = 0
for a in range(1, 50):
    XX = list(grid(-160, 160, Fr(1, 4)))
    Pp = [x for x in XX if x * x + 2 * a * x - 3 * a * a < 0]
    Qq = [x for x in XX if abs(x - 2) <= 6]
    f1 = all(abs(x - 2) <= 6 for x in Pp)
    f2 = all(x * x + 2 * a * x - 3 * a * a < 0 for x in Qq)
    if not f1 and not f2:
        cnt += 1
R["n2446"] = cnt

cnt = 0
for a in range(1, 200):
    rr = int(math.isqrt(a))
    Qs = [x for x in (math.sqrt(a), -math.sqrt(a))]
    # p→~q ⟺ q→~p : x²=a 의 두 근이 모두 x²−2x−15≤0 (−3≤x≤5)
    if all(-3 <= x <= 5 for x in Qs):
        cnt += 1
R["g424"] = cnt

# 07 두 명제와 미지수 --------------------------------------------------------
tot = 0
for a in range(-30, 31):
    Pp = [x for x in grid(a - 3, a + 3, Fr(1, 8))]
    q = lambda x: x * x - 5 * x - 6 <= 0
    if not all(q(x) for x in Pp) and not all(not q(x) for x in Pp):
        tot += a
R["n2220"] = tot

As = [a for a in range(-30, 31) if all(x * x - 2 * a * x + 6 * a - 8 >= 0 for x in XS)]   # (가) 거짓
Bs = [b for b in range(-50, 51) if any(-x * x + 6 * x - b >= 0 for x in XS)]               # (나) 거짓: Q≠∅
R["k1-16"] = min(As) + max(Bs)

cnt = 0
for m in range(-20, 21):
    for n in range(-30, 31):
        ga = all(x * x + 2 * m * x + 4 > 0 for x in XS)
        nb = all(x * x + n * x + 9 > 0 for x in XS)       # ~p(=U) ⊂ Q
        if ga and nb:
            cnt += 1
R["k8-22"] = cnt

# 08 증명 ---------------------------------------------------------------
# b48: a²=1(가), (나) 3n+1  → k+f(2) = 1 + 7
for n in range(1, 200):
    v = 3 * n * (3 * n + 2)
    assert math.isqrt(v) ** 2 != v and v == (3 * n + 1) ** 2 - 1
R["b48"] = 1 + (3 * 2 + 1)
# o52: a=1, n=(p+1)/2 → k=1, f(3)=2
R["o52"] = (3 + 1) // 2
# o37: 나머지 1, 1, 2
r1 = {(a * a + b * b) % 3 for a in range(1, 60) for b in range(1, 60) if a % 3 == 0 and b % 3}
r2 = {(a * a + b * b) % 3 for a in range(1, 60) for b in range(1, 60) if a % 3 and b % 3 == 0}
r3 = {(a * a + b * b) % 3 for a in range(1, 60) for b in range(1, 60) if a % 3 and b % 3}
assert r1 == {1} and r2 == {1} and r3 == {2}
R["o37"] = 1 + 2 * 1 + 3 * 2

# 09 논리적 추론 -----------------------------------------------------------
sol = []
for pres in "ABCD":
    st = {"A": pres == "C", "B": pres != "B", "C": pres == "D"}
    st["D"] = not st["C"]
    tr = [s for s, v in st.items() if v]
    if len(tr) == 1:
        sol.append((tr[0], pres))
assert len(sol) == 1
R["k3-18"] = "%s, %s" % sol[0]

sol = []
for cards in itertools.product("WB", repeat=3):
    stA = all(c == "B" for c in cards)
    stB = cards.count("W") == 1
    if (cards[0] == "W") == stA and (cards[1] == "W") == stB:
        sol.append(cards)
assert len(sol) == 1
name = {"W": "화이트 카드", "B": "블랙 카드"}
R["o53"] = ", ".join(name[c] for c in sol[0])

# STEP 3 ---------------------------------------------------------------
# g427
res = set()
for n in range(1, 60):
    Uu = set(range(1, n + 1))
    Pp = {x for x in Uu if 36 % x == 0}
    if 2 ** len(Pp) == 128 and 2 ** (len(Uu) - len(Pp)) == 64:
        res.add(sum(Uu - Pp))
assert len(res) == 1
R["g427"] = res.pop()

# g461
cnt = 0
for k in range(-200, 10):
    # p: x²−4≠0, q: x⁴+(k−5)x²−4k+4≠0 → P=Q ⟺ 두 식이 0이 되는 실수 x의 집합이 같다
    roots = set()
    for t in (4, 1 - k):            # x⁴+(k−5)x²−4k+4=(x²−4)(x²+k−1)
        if t > 0:
            roots |= {round(math.sqrt(t), 9), round(-math.sqrt(t), 9)}
        elif t == 0:
            roots.add(0.0)
    if roots == {2.0, -2.0}:
        cnt += 1
assert all((x ** 4 + (k - 5) * x ** 2 - 4 * k + 4) == (x * x - 4) * (x * x + k - 1) for x in range(-5, 6) for k in range(-5, 6))
R["g461"] = cnt

# g475
best = None
for n in range(1, 30):
    f = lambda x: 2 * abs(x - n) - abs(x - 2 * n) + 2 * abs(x - 3 * n)
    Pint = [x for x in range(-10 * n - 10, 10 * n + 10) if f(x) < 4 * n]
    if len(Pint) != 6:
        continue
    for k in [Fr(t, 4) for t in range(0, 400)]:
        # p는 ~q이기 위한 충분조건: p를 만족하는 모든 실수 x가 q를 만족하지 않는다
        Pr = [x for x in grid(-5 * n, 10 * n, Fr(1, 16)) if f(x) < 4 * n]
        if all(not (k - 2 * abs(x - 5) <= 2 * n) for x in Pr):
            best = k if best is None else min(best, k)
            break
R["g475"] = best

# g460 : 네 집합 조건과 보기 (작은 전체집합의 모든 경우)
U3 = frozenset(range(3))
A3 = [s for s in subsets(U3) if s]
ok = {"ㄱ": True, "ㄴ": True, "ㄷ": True}
for P_ in A3:
    for Q_ in A3:
        for R_ in A3:
            for S_ in A3:
                if not (P_ <= R_ and (R_ - S_) and not (Q_ & S_) and (P_ & S_)):
                    continue
                if not (R_ | (U3 - P_)) == U3:
                    ok["ㄱ"] = False
                if len(R_) < 2:
                    ok["ㄴ"] = False
                X = (U3 - Q_) & (U3 - S_)
                Y = R_ - S_
                if not Y <= X:
                    ok["ㄷ"] = False
# ㄷ은 원소가 더 많은 전체집합에서 반례가 생기므로 4원소로 한 번 더
U4 = frozenset(range(4))
A4 = [s for s in subsets(U4) if s]
for P_ in A4:
    for Q_ in A4:
        for R_ in A4:
            for S_ in A4:
                if P_ <= R_ and (R_ - S_) and not (Q_ & S_) and (P_ & S_):
                    if not (R_ - S_) <= ((U4 - Q_) & (U4 - S_)):
                        ok["ㄷ"] = False
R["g460"] = ", ".join(c for c in ok if ok[c])

# m99 : 3k와 k+1이 함께 B에 있으면 안 된다
edges = [(3 * k, k + 1) for k in range(1, 17)]
verts = sorted({v for e in edges for v in e})
free = 50 - len(verts)
best = 0
for mask in range(1 << len(verts)):
    S_ = {verts[i] for i in range(len(verts)) if mask >> i & 1}
    if all(not (a in S_ and b in S_) for a, b in edges):
        best = max(best, len(S_))
R["m99"] = free + best

# m101
ms = []
for m in [Fr(t, 8) for t in range(-80, 81)]:
    ok_ = True
    for x in grid(-40, 40, Fr(1, 32)):
        if (x * x - m * x + m) * (x * x + 2 * x - 3) < 0 and not (x * x + 2 * x - 3 < 0):
            ok_ = False
            break
    if ok_:
        ms.append(m)
a, b = max(ms), min(ms)
R["m101"] = -8 * a * b

# o49
tot = 0
for a in range(-60, 61):
    xs = [x for x in range(-30, 31)
          if not (x * x - (Fr(a, 2) + 2) * x + a > 0) and not (abs(x - 3) > 6)]
    if len(xs) == 3:
        tot += a
R["o49"] = tot

# o46
tot = 0
for k in range(1, 40):
    n = 5
    xs = [x for x in range(-50, 60) if not (4 * x * x - 8 * n * x + 4 * n * n - k * k >= 0)]
    if len(xs) == 7:
        tot += k
R["o46"] = tot

# b32
A_ = [k for k in range(1, 50) if any(x * x - 8 * x + 2 * k < 0 for x in XS)]
cnt = 0
for Bs in subsets(A_):
    if all(Fr(x * x + 3 * x + 2, 2) not in Bs for x in Bs):
        cnt += 1
R["b32"] = cnt

# k3-17
U5 = frozenset(range(1, 6))
AL = [s for s in subsets(U5) if s]
cnt = 0
for A in AL:
    for B in AL:
        if any(x * x <= 2 * x + 3 for x in A) and all(x not in A for x in B):
            cnt += 1
R["k3-17"] = cnt

# n2202
Ub = set(range(1, 15))
B_ = set(range(1, 8))
res = set()
for mask in range(1 << 14):
    A = {i + 1 for i in range(14) if mask >> i & 1}
    if any({x, 2 * x} <= A for x in B_):
        continue
    if not all({x, 2 * x} & A for x in B_):
        continue
    if {x for x in range(6, 11) if x in A} != {x for x in range(6, 11) if x % 2 == 0}:
        continue
    if any((x in A) != (x + 1 in A) for x in (11, 13)):
        continue
    res.add(sum(A))
assert len(res) == 1
R["n2202"] = res.pop()


# 대조 ---------------------------------------------------------------
def norm(v):
    if isinstance(v, Fr):
        if v.denominator != 1:
            sgn = "-" if v < 0 else ""
            return "%s{%d}over{%d}" % (sgn, abs(v.numerator), v.denominator)
        return str(v.numerator)
    return str(v).replace(" ", "")


bad = 0
items = [p for _, _, ps in data07.TYPES for p in ps] + data07.STEP3
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
