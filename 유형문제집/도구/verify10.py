# 10단원(경우의 수와 순열) 유형서 문항 정답 독립 검산 (문항 기호는 unit10.py의 v)
# 모든 경우를 직접 나열해 센다.
from itertools import permutations, product
from math import perm
R = []


def chk(no, got, exp):
    R.append((no, got == exp, got, exp))


def adj(q, cond):
    return any(cond(q[i], q[i + 1]) for i in range(len(q) - 1))


def colorings(n, edges, k):
    return sum(1 for c in product(range(k), repeat=n) if all(c[i] != c[j] for i, j in edges))


# ---- 합의 법칙
chk("n716", sum(1 for x in range(1, 10) if x % 2 == 0 or x % 3 == 0), 6)
chk("n226", sum(1 for n in range(10, 100) if n % 10 and (n // 10 + n % 10) % 2 == 0), 41)
chk("o3", sum(1 for a in range(1, 7) for b in range(1, 7) if b * b > 4 * a), 17)
# ---- 방정식·부등식
chk("n897", sum(1 for x in range(1, 201) if 200 % x == 0), 12)
chk("n692", sum(1 for x in range(1, 11) for y in range(1, 6) if 1000 * x + 2000 * y <= 10000), 20)
chk("o24", sum(1 for x in range(7) for y in range(5) for z in range(4) if 2 * x + 3 * y + 4 * z == 12), 7)
# ---- 약수
chk("n736", sum(1 for d in range(1, 541) if 540 % d == 0), 24)
chk("n162", sum(1 for a in range(1, 30) for b in range(1, 30) if (a + 1) * (b + 1) == 24), 6)
sol = [(a, b, c) for a in range(2, 20) for b in range(a + 1, 20) for c in range(b + 1, 20) if (a + 1) * (b + 1) * (c + 1) == 105]
chk("o4", sum(sol[0]) if len(sol) == 1 else sol, 12)
# ---- 곱의 법칙의 활용
chk("n150", sum(1 for a, b, c in product(range(1, 7), repeat=3) if (12 * b + 18 * a + c * a * b) % (a * b) == 0 and ((12 * b + 18 * a + c * a * b) // (a * b)) % 2 == 1), 63)
chk("n955", sum(1 for a, b, c in product(range(1, 7), repeat=3) if a * b * c % 20 == 0), 42)
# ---- 도로망
r_ = [n for n in range(1, 30) if 3 * n * (n - 1) * 2 == 72]
chk("o5", r_[0] if len(r_) == 1 else r_, 4)
E = {("A", "B"): 2, ("B", "D"): 2, ("A", "C"): 3, ("C", "D"): 1, ("B", "C"): 2}
w = lambda u, v: E.get((u, v)) or E.get((v, u)) or 0
def paths(u, seen):
    if u == "D":
        return 1
    return sum(w(u, v) * paths(v, seen | {v}) for v in "ABCD" if v not in seen and w(u, v))
chk("w1", paths("A", {"A"}), 23)
# ---- 색칠 (u10_ring: E는 모두와, A-B-C-D-A 고리 / o54: 일렬 / o53: 벤 다이어그램)
A, B, C, D, E_ = range(5)
chk("w8", colorings(5, [(A, B), (B, C), (C, D), (D, A), (A, E_), (B, E_), (C, E_), (D, E_)], 5), 420)
line = [c for c in product(range(3), repeat=5) if all(c[i] != c[i + 1] for i in range(4))]
chk("o54", sum(1 for c in line if c[0] != c[4]) - sum(1 for c in line if len(set(c)) == 2), 24)
venn = [(1, 2), (1, 4), (1, 6), (3, 2), (3, 4), (7, 2), (7, 6), (5, 4), (5, 6)]
chk("o53", sum(1 for c in product(range(3), repeat=7) if all(c[i - 1] != c[j - 1] for i, j in venn)), 84)
# ---- 순열의 수
r_ = [n for n in range(3, 30) if perm(n, 3) == 210]
chk("n346", r_[0] if len(r_) == 1 else r_, 7)
r_ = [n for n in range(2, 40) if perm(2 * n, 4) == 252 * perm(n, 2)]
chk("o7", r_[0] if len(r_) == 1 else r_, 5)
r_ = sorted({r for n in range(2, 12) for r in range(1, n + 2) if perm(n + 2, r) - perm(n + 1, 3) == r * perm(n + 1, 2)})
chk("n10", r_[0] if len(r_) == 1 else r_, 3)
# ---- 이웃
V = set("AE")
cnt = sum(1 for q in permutations("SPARKLE") if not adj(q, lambda x, y: x in V and y in V))
chk("n6", cnt // 720 if cnt % 720 == 0 else cnt, 5)
chk("n491", sum(1 for q in permutations(["m1", "m2", "e1", "e2", "o1", "o2"])
                if adj(q, lambda x, y: x[0] == y[0] == "m") and not adj(q, lambda x, y: x[0] == y[0] == "e")), 144)
chk("n548", sum(1 for q in permutations(range(1, 10)) if abs(q.index(4) - q.index(8)) == 1
                and not adj(q, lambda x, y: x % 3 == 0 and y % 3 == 0)), 28800)
chk("n593", len({q for q in permutations(["g1", "g2", "g3", "b1", "b2", "b3", "_"]) if not adj(q, lambda x, y: x[0] == y[0] == "g")}), 1440)
chk("n182", len({q for q in permutations(["s1", "s2", "s3", "s4", "s5"] + ["_"] * 5) if not adj(q, lambda x, y: x[0] == y[0] == "s")}), 720)
# ---- 위치·순서
chk("n920", sum(1 for q in permutations(["b1", "b2", "b3", "b4", "g1", "g2"]) if q[0][0] == "b" and q[-1][0] == "b"), 288)
cnt = sum(1 for q in permutations(range(1, 8)) if q[0] % 2 and q[-1] % 2)
chk("o9", cnt // 720 if cnt % 720 == 0 else cnt, 2)
P6 = ["A1", "A2", "c1", "c2", "c3", "c4"]
a = sum(1 for q in permutations(P6) if q[0][0] == "c" and q[-1][0] == "c")
b = sum(1 for q in permutations(P6) if not adj(q, lambda x, y: x[0] == y[0] == "A"))
chk("n33", b - a, 192)
def ok851(q):
    i, j = sorted((q.index("A"), q.index("B")))
    return j - i == 3 and "C" in q[i + 1:j]
chk("n851", sum(1 for q in permutations("ABCDEFG") if ok851(q)), 384)
chk("n930", sum(1 for q in permutations("ABCDEFG") if q.index("A") < q.index("B") and abs(q.index("A") - q.index("B")) > 1), 1800)
def ok3334(q):
    if q[0] % 2 == 0 or q[-1] % 2 == 0:
        return False
    i = q.index(6)
    return 0 < i < 6 and (q[i - 1] * q[i + 1]) % 2 == 0
chk("m3334", sum(1 for q in permutations(range(1, 8)) if ok3334(q)), 1008)
# ---- 교대
cnt = sum(1 for q in permutations(["b%d" % i for i in range(6)] + ["g%d" % i for i in range(4)])
          if q[0][0] == "b" and q[-1][0] == "b" and all(q[i][0] != q[i + 1][0] for i in range(1, 8)))
chk("n7", cnt // 720 if cnt % 720 == 0 else cnt, 48)
chk("o35", sum(1 for p in permutations(range(1, 10), 4) if all((p[i] + p[i + 1]) % 2 for i in range(3))), 480)
# ---- 자리 배정 (앞좌석: 운전석 F0, 옆 F1 / 뒷좌석 R0 R1 R2)
seats = ["F0", "F1", "R0", "R1", "R2"]
nb = lambda s, t: s[0] == t[0] and abs(int(s[1]) - int(t[1])) == 1
cnt = 0
for q in permutations(seats):            # 아버지, 어머니, 하니, 가족1, 가족2
    if q[0] != "F0" and q[1] != "F0":
        continue
    if nb(q[2], q[0]) or nb(q[2], q[1]):
        cnt += 1
chk("n145", cnt, 28)
p = sum(1 for q in permutations(seats) if {q[0], q[1]} == {"F0", "F1"})
qq = sum(1 for q in permutations(seats) if q[0] == "F0" or q[1] == "F0")
chk("n302", p + qq, 60)
seats = [(r, c) for r in range(4) for c in range(3)]
cnt = sum(1 for s in permutations(seats, 6)          # 남1~3, 여1~3: 남i는 여j 한 명과만 같은 줄
          if len({x[0] for x in s}) == 3 and sorted(x[0] for x in s[:3]) == sorted(x[0] for x in s[3:])
          and len({x[0] for x in s[:3]}) == 3)
pq = [(p_, q_) for p_ in range(1, 20) for q_ in range(1, 20) if 2 ** p_ * 3 ** q_ == cnt]
chk("n470", sum(pq[0]) if len(pq) == 1 else cnt, 12)
seats = [(r, c) for r in range(2) for c in range(3)]
nb2 = lambda s, t: s[0] == t[0] and abs(s[1] - t[1]) == 1
chk("n442", sum(1 for q in permutations(seats, 5) if nb2(q[0], q[1]) and all(x[0] != q[0][0] for x in q[2:])), 48)
# ---- 자연수의 개수
chk("n376", sum(1 for n in range(100, 340) if n % 2 and len(set(str(n))) == 3), 83)
chk("n836", sum(1 for p in permutations(range(7), 3) if p[0] and int("".join(map(str, p))) % 6 == 0), 39)
chk("n143", sum(1 for p in permutations(range(5)) if p[0] and int("".join(map(str, p))) % 4 == 0), 30)
chk("n184", sum(1 for p in permutations(range(5)) if p[0] and int("".join(map(str, p))) > 21000), 66)
chk("n185", sum(1 for n in range(100, 1000) if str(n).count("9") == 1 and (n // 100 + n % 10) % 2 == 0), 108)
# ---- 사전식
nums = sorted(int("".join(map(str, p))) for p in permutations(range(5)) if p[0])
chk("n745", nums[49], 30142)
chk("w2", sorted(permutations("123456")).index(tuple("342516")) + 1, 297)
# ---- 중복순열
chk("w3", min(n for n in range(1, 20) if sum(2 ** k for k in range(1, n + 1)) >= 100), 6)
chk("w4", sum(1 for _ in product(range(3), repeat=4)), 81)
chk("w5", sum(1 for p in product(range(5), repeat=4) if p[0] >= 3 and p[3] % 2 == 0), 150)
# ---- 같은 것이 있는 순열
chk("w6", len({p for p in permutations("11223") if int(p[-1]) % 2}), 18)
chk("w7", len({p for p in permutations("BANANA") if not adj(p, lambda x, y: x == y == "A")}), 12)
# ---- 교란순열
chk("w9", sum(1 for p in permutations(range(5)) if sum(p[i] == i for i in range(5)) == 1), 45)
chk("w10", sum(1 for p in permutations(range(4)) if sum(p[i] == i for i in range(4)) <= 1), 17)
# ---- 고난도
def ok26(n):
    s = str(n)
    return n % 5 == 0 and not any(int(s[i]) % 2 and int(s[i + 1]) % 2 for i in range(2))
chk("o26", sum(1 for n in range(100, 1000) if ok26(n)), 110)
cards = [1, 2, 3, 4, 0, 0, 0, 0]
S = {tuple(cards[i] for i in p) for p in permutations(range(8), 5)}
chk("o60", sum(1 for d in S if d[0] and not adj(d, lambda x, y: x == y == 0)), 168)
chk("n316", sum(1 for q in permutations(["a1", "a2", "a3", "b1", "b2", "b3", "b4"])
                if q[0][0] == "b" and q[-1][0] == "b"
                and not any(q[i][0] == q[i + 1][0] == q[i + 2][0] == "a" for i in range(5))), 1008)
def ok123(q):
    for i, x in enumerate(q):
        if x[0] == "3":
            if i == 0 or i == 6 or q[i - 1][0] != "1" or q[i + 1][0] != "1":
                return False
    return True
chk("n123", sum(1 for q in permutations(["1a", "1b", "1c", "1d", "2a", "3a", "3b"]) if ok123(q)), 432)
balls = [1, 2, 3, 4, 5, 5, 5, 5]
S = {tuple(balls[i] for i in p) for p in permutations(range(8))}
chk("n103", sum(1 for s in S if s[3] != 4 and s[4] != 5), 750)
cnt = 0
for a_ in permutations(range(1, 9), 6):
    A_ = a_[0] * 100 + a_[1] * 10 + a_[2]; B_ = a_[3] * 10 + a_[4]; C_ = a_[5]
    if (A_ + B_ + C_) % 5 == 0 and (A_ - B_ - C_) % 5 == 0:
        cnt += 1
chk("m3286", cnt, 720)
def ok11(p):
    odd = [x for x in p if x % 2]
    if odd != sorted(odd) or abs(p.index(4) - p.index(8)) != 1 or abs(p.index(2) - p.index(6)) == 1:
        return False
    ev = [x % 2 == 0 for x in p]
    return not any(ev[i] and ev[i + 1] and ev[i + 2] for i in range(6))
chk("o11", sum(1 for p in permutations(range(1, 9)) if ok11(p)), 120)
def ok449(q):
    if adj(q, lambda x, y: x[0] == y[0] == "g"):
        return False
    runs, r = [], 0
    for x in q:
        if x[0] == "m":
            r += 1
        else:
            if r:
                runs.append(r)
            r = 0
    if r:
        runs.append(r)
    return all(x % 2 == 0 for x in runs)
chk("n449", sum(1 for q in permutations(["m%d" % i for i in range(6)] + ["g1", "g2"]) if ok449(q)), 8640)

if __name__ == "__main__":
    bad = [r for r in R if not r[1]]
    for r in bad:
        print("불일치", r)
    print("검산", len(R), "불일치", len(bad))
# ---- 사용자 추가 문항(2026-10-16)
nums = sorted(int("".join(p)) for p in product("123", repeat=4))
chk("u22", nums[49], 2322)
chk("u32", sum(1 for f in product("abcd", repeat=3) if f[0] == "a" or f[1] == "b"), 28)
Xs = [-4, -2, 0, 2, 4]
chk("u33", sum(1 for f in product(Xs, repeat=5) if all(f[i] + f[4 - i] == 0 for i in range(5))), 25)
chk("u59", sum(1 for d in product("123", repeat=6) if set(d) == {"1", "2", "3"} and d[5] == d[3]), 150)
chk("u70", len({p for p in permutations("BBBBWWWWWWW") if p == p[::-1]}), 10)
