# 11단원(조합) 유형서 문항 정답 독립 검산 (문항 기호는 unit11.py의 v). 모든 경우를 직접 나열해 센다.
from itertools import permutations, combinations, product
from math import comb, perm
import math
R = []


def chk(no, got, exp):
    R.append((no, got == exp, got, exp))


def one(xs):
    return xs[0] if len(xs) == 1 else xs


def col(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]) == 0


# ---- 조합의 수
chk("n5", sum(n for n in range(1, 12) if comb(11, n - 1) + comb(11, n) == 66), 12)
chk("n286", one([n for n in range(4, 40) if 12 * comb(n, 3) == 5 * perm(n - 1, 3)]), 5)
chk("n962", one([n for n in range(2, 40) if 2 * perm(n, 2) == comb(n + 1, 3)]), 11)
chk("n504", one([n for n in range(2, 40) if comb(n + 1, n - 1) == perm(n, 2) - 2 * comb(n, n - 1)]), 7)
chk("o16", one([n for n in range(3, 7) if comb(7, 8 - n) == comb(7, 2 * n - 5)]), 4)
chk("o39", one([n for n in range(2, 15) if comb(16 - n, 2) == 3 * comb(n, 2)]), 6)
# ---- 포함·불포함
chk("n454", sum(1 for s in combinations("abcdef", 3) if "a" in s), 10)
chk("n133", sum(1 for s in combinations(range(1, 10), 4) if 6 in s), 56)
chk("n335", one([n for n in range(3, 30) if sum(1 for s in combinations(range(4 + n), 3) if any(x < 4 for x in s) and any(x >= 4 for x in s)) == 70]), 5)
chk("n719", one([n for n in range(3, 40) if comb(2 * n, 3) == 9 * comb(n, 3)]), 14)
# ---- 적어도
chk("n782", sum(1 for s in combinations(["g%d" % i for i in range(4)] + ["b%d" % i for i in range(3)], 2) if sum(x[0] == "g" for x in s) == 1), 12)
st = ["a%d" % i for i in range(4)] + ["b%d" % i for i in range(3)] + ["c%d" % i for i in range(2)]
chk("n750", sum(1 for s in combinations(st, 5) if {x[0] for x in s} == {"a", "b", "c"}), 98)
chk("o59", sum(1 for s in combinations(range(10), 4) if sum(x < 4 for x in s) >= 2), 115)
chk("n645", sum(1 for a in combinations(range(5), 3) for b in combinations(range(5), 3) if len(set(a) & set(b)) <= 2), 90)
# ---- 수를 택하는 조합
chk("n397", sum(1 for s in combinations(range(1, 10), 3) if math.prod(s) % 2 == 0), 74)
chk("o21", sum(1 for s in combinations(range(1, 10), 3) if sum(s) % 2), 40)
chk("o38", sum(1 for s in combinations(range(1, 10), 4) if math.prod(s) % 2 == 0), 121)
chk("o19", sum(1 for s in combinations(range(1, 11), 4) if max(s) - min(s) == 7), 45)
chk("n54", sum(1 for p in permutations(range(1, 10), 3) if sum(p) % 2 == 0), 264)
# ---- 조건을 만족시키는 자연수
chk("n731", sum(1 for p in permutations(range(1, 10), 3) if all(a + b != 10 for a, b in combinations(p, 2))), 336)
chk("n105", sum(1 for p in permutations(range(1, 10), 3) if all(abs(a - b) != 4 for a, b in combinations(p, 2))), 300)
chk("n604", sum(1 for p in permutations(range(10), 3) if p[0] and int("".join(map(str, p))) % 6 == 0), 115)
# ---- 뽑아서 나열
P = ["m%d" % i for i in range(5)] + ["f%d" % i for i in range(3)]
c = 0
for q in permutations(P, 4):
    if sum(x[0] == "m" for x in q) == 2:
        fi = [i for i, x in enumerate(q) if x[0] == "f"]
        if fi[1] - fi[0] == 1:
            c += 1
chk("o18", c, 360)
def ok641(q):
    if not {"A", "B", "C"} <= set(q):
        return False
    return not any(q[i] in "ABC" and q[i + 1] in "ABC" for i in range(5))
chk("n641", sum(1 for q in permutations("ABCDEFGHI", 6) if ok641(q)), 2880)
def ok345(q):
    return ("A" in q or "B" in q) and q[2] == "C" and q[0] not in "AB" and q[4] not in "AB"
chk("n345", sum(1 for q in permutations("ABCDEFGHI", 5) if ok345(q)), 540)
chk("n611", sum(1 for p in permutations(range(8), 4) if p[0] and p[0] + p[3] == 6), 150)
def cnt206(n):
    return sum(1 for q in permutations(range(n)) if q.index(0) < q.index(1) and q.index(0) < q.index(2))
chk("n206", one([n for n in range(3, 9) if cnt206(n) == 240]), 6)
st = ["a1", "a2", "a3", "b1", "b2", "c1"]
chk("m3183", sum(1 for q in permutations(st, 5) if not any(q[i][0] == q[i + 1][0] == "a" for i in range(4))), 252)
# ---- 크기순
chk("n755", sum(1 for s in combinations(range(1, 10), 3) if any(x % 3 == 0 for x in s)), 64)
chk("o41", sum(1 for p in permutations(range(1, 10), 6) if {2, 4, 6, 8} <= set(p) and [v for v in p if v % 2 == 0] == [2, 4, 6, 8]), 300)
# ---- 직선과 삼각형
pts = [(x, 1) for x in range(4)] + [(x, 0) for x in range(5)]
chk("n71", sum(1 for t in combinations(pts, 3) if not col(*t)), 70)
def lines(pts):
    return len({frozenset(p for p in pts if col(a, b, p)) for a, b in combinations(pts, 2)})
L43 = [(x, y) for x in range(4) for y in range(3)]
chk("n927", lines(L43), 35)
L53 = [(x, y) for x in range(5) for y in range(3)]
chk("n837", lines(L53) + sum(1 for t in combinations(L53, 3) if not col(*t)), 464)
Q = [(math.cos(2 * math.pi * k / 12), math.sin(2 * math.pi * k / 12)) for k in range(12)]
def acute(t):
    for i in range(3):
        A, B, C_ = Q[t[i]], Q[t[(i + 1) % 3]], Q[t[(i + 2) % 3]]
        if (B[0] - A[0]) * (C_[0] - A[0]) + (B[1] - A[1]) * (C_[1] - A[1]) < 1e-9:
            return False
    return True
chk("n596", sum(1 for t in combinations(range(12), 3) if acute(t)), 40)
L33 = [(x, y) for x in range(3) for y in range(3)]
par = 0
for qd in combinations(L33, 4):
    a, b, c_, d = qd
    for (p1, p2), (p3, p4) in (((a, b), (c_, d)), ((a, c_), (b, d)), ((a, d), (b, c_))):
        if (p1[0] + p2[0], p1[1] + p2[1]) == (p3[0] + p4[0], p3[1] + p4[1]) and not col(p1, p2, p3):
            par += 1
            break
area1 = sum(1 for t in combinations(L33, 3) if abs((t[1][0] - t[0][0]) * (t[2][1] - t[0][1]) - (t[1][1] - t[0][1]) * (t[2][0] - t[0][0])) == 2)
truth = (lines(L33) == 20, par == 21, area1 == 27)
chk("n121", {(True, False, False): "①"}.get(truth, truth), "①")
# ---- 분할과 분배
chk("n31", sum(1 for s in range(1 << 9) if bin(s).count("1") in (4, 5)), 252)
c = 0
for f in product(range(3), repeat=9):
    k = [f.count(i) for i in range(3)]
    if min(k) > 0 and len(set(k)) == 3:
        c += 1
chk("n386", c, 12096)
P8 = ["a1", "a2", "a3", "b1", "b2", "b3", "c1", "c2"]
def pairings(lst):
    if not lst:
        yield []
        return
    for i in range(1, len(lst)):
        for rest in pairings(lst[1:i] + lst[i + 1:]):
            yield [(lst[0], lst[i])] + rest
chk("o43", sum(1 for pp in pairings(P8) if all(x[0] != y[0] for x, y in pp)), 36)
c = 0
for sn in product(range(3), repeat=7):
    for dl in product(range(3), repeat=5):
        s_ = [sn.count(i) for i in range(3)]
        d_ = [dl.count(i) for i in range(3)]
        if 1 in s_ and min(d_) >= 1 and all(s_[i] + d_[i] == 4 for i in range(3)):
            c += 1
fac = {}
x = c
for pr in (2, 3, 5, 7):
    while x % pr == 0:
        fac[pr] = fac.get(pr, 0) + 1
        x //= pr
chk("n215", sum(fac.values()) if x == 1 and len(fac) == 4 else c, 8)
# ---- 같은 것이 있을 때
chk("n17", len({tuple(sorted(s)) for s in combinations("AABBCCDD", 4)}), 19)
S = set()
for p in permutations("AABBCCDD", 4):
    S.add((tuple(sorted(p[:2])), tuple(sorted(p[2:]))))
chk("n410", len(S), 72)
c = 0
for soap in combinations(range(5), 3):
    for sp in permutations(range(5), 4):
        if set(soap) | set(sp) == set(range(5)):
            c += 1
chk("n56", c, 720)
S = set()
for p in permutations("RRRBBYYG"):
    hands = tuple(tuple(sorted(p[2 * i:2 * i + 2])) for i in range(4))
    if all(h[0] != h[1] for h in hands):
        S.add(hands)
chk("o44", len(S), 48)
# ---- 두 사람이 고르기
M_, S_ = ["m%d" % i for i in range(4)], ["s%d" % i for i in range(3)]
opts = [a + b for a in combinations(M_, 2) for b in combinations(S_, 1)]
chk("n86", sum(1 for a in opts for b in opts if len(set(a) & set(b)) == 1), 162)
subj = ["g", "e", "p1", "p2", "p3", "p4"]
opts = [s for s in combinations(subj, 3) if "g" in s or "e" in s]
chk("n301", sum(1 for a in opts for b in opts if len(set(a) & set(b)) == 1), 108)
# ---- 고난도
chk("o23", sum(1 for a in range(1, 21) for b in range(1, 21) for c_ in range(1, 21)
               if len({a, b, c_}) == 3 and (a * b * c_) % 2 and a < b < 16 < c_), 56)
chk("o45", sum(1 for x in product(range(1, 10), repeat=5) if x[0] < x[1] < x[2] <= 5 <= x[3] < x[4]), 100)
choc = 3 ** 4
candy = sum(1 for c_ in product(range(3), repeat=3) if sum(c_) == 2)
cookie = sum(1 for f in product(range(3), repeat=6) if len(set(f)) == 3)
tot = choc * candy * cookie
fac = {}
x = tot
for pr in (2, 3, 5):
    while x % pr == 0:
        fac[pr] = fac.get(pr, 0) + 1
        x //= pr
chk("n516", sum(v * v for v in fac.values()) if x == 1 else tot, 74)
c = 0
for cars in combinations(range(5), 2):
    for asg in product(range(2), repeat=8):        # 사람 8명(어른 0~2, 어린이 3~7)이 두 케이블카 중 하나
        n0, n1 = asg.count(0), asg.count(1)
        if n0 > 5 or n1 > 5 or n0 == 0 or n1 == 0:
            continue
        if any(not any(asg[i] == k for i in range(3)) for k in (0, 1)):
            continue
        c += 1
chk("n320", c, 1500)
c = 0
for f in product(range(5), repeat=6):             # 책 6권(동화 0~2, 시집 3~5) → 학생 0,1(1학년), 2,3,4(2학년)
    if any(f[i] < 2 for i in range(3)):
        continue
    if len(set(f)) != 5:
        continue
    if any(sum(1 for i in range(3, 6) if f[i] == s) >= 2 for s in range(5)):
        continue
    c += 1
chk("m3303", c, 216)
T_, Mu = ["t%d" % i for i in range(4)], ["u%d" % i for i in range(3)]
opts = [s for s in combinations(T_ + Mu, 4) if any(x[0] == "t" for x in s) and any(x[0] == "u" for x in s)]
chk("n321", sum(1 for a in opts for b in opts if len(set(a) & set(b)) == 2), 594)
c = 0
for f in product(range(7), repeat=5):
    k = [f.count(i) for i in range(7)]
    if max(k) > 2:
        continue
    if not all(any(k[j] == 2 for j in (n, n + 1, n + 2)) for n in range(5)):
        continue
    two = [i for i in range(7) if k[i] == 2]
    if any(k[j] for a, b in combinations(two, 2) for j in range(a + 1, b)):
        continue
    c += 1
chk("m3337", c, 300)
c = 0
for pairs in product(list(combinations("ABCD", 2)), repeat=5):
    act = {s: {d for d in range(5) if s in pairs[d]} for s in "ABCD"}
    if all(len(act[s]) >= 2 for s in "ABCD") and not act["A"] & act["B"] and len(act["B"] & act["C"]) == 1:
        c += 1
chk("m3278", c, 450)

if __name__ == "__main__":
    bad = [r for r in R if not r[1]]
    for r in bad:
        print("불일치", r)
    print("검산", len(R), "불일치", len(bad))
