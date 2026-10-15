# -*- coding: utf-8 -*-
"""기본서 11단원 정답 검산: 문항마다 모든 경우를 직접 나열해 세어 data11의 답과 맞춘다.  python verify11.py"""
import sys, os, math
from itertools import permutations, product, combinations
from math import comb
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data11

ans = []


def dist(n, k, lo=0):
    return [c for c in product(range(n + 1), repeat=k) if sum(c) == n and min(c) >= lo]


def col3(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]) == 0


M, K = ["m%d" % i for i in range(5)], ["k%d" % i for i in range(4)]
S = list(combinations(M + K, 4))
a1 = sum(1 for s in S if "m0" in s and "m1" in s)
a2 = sum(1 for s in S if "k0" not in s and "k1" not in s)
a3 = sum(1 for s in S if any(x[0] == "m" for x in s))
ans.append("⑴ $%d$ ⑵ $%d$ ⑶ $%d$" % (a1, a2, a3))
ans.append(sum(1 for s in combinations(["b%d" % i for i in range(4)] + ["g%d" % i for i in range(5)], 4) if sum(x[0] == "b" for x in s) >= 2))
ans.append(sum(1 for r in dist(4, 3, 1) for b in dist(5, 3) if all(r[i] + b[i] <= 4 for i in range(3))))
ans.append(sum(1 for r in dist(3, 5) for b in dist(6, 5) if max(r) <= 1 and all(1 <= r[i] + b[i] <= 3 for i in range(5))))
x1 = sum(1 for p in permutations(range(1, 7)) if p[1] < p[2] < p[4] and p[0] > p[3])
x2 = sum(1 for a in range(10) for b in range(10) for c in range(10) if 0 < c < b < a and 500 < 100 * a + 10 * b + c < 700)
ans.append("⑴ $%d$ ⑵ $%d$" % (x1, x2))
y = [sum(1 for a in range(1, 10) for b in range(10) for c in range(10) if f(a, b, c))
     for f in (lambda a, b, c: a < b < c, lambda a, b, c: a > b > c, lambda a, b, c: a > b >= c)]
ans.append("⑴ $%d$ ⑵ $%d$ ⑶ $%d$" % tuple(y))
rows = [(0, i) for i in range(4)] + [(1, i) for i in range(5)]
cnt = 0
for t in permutations(range(9), 3):
    pos = [rows[i] for i in t]
    if {p[0] for p in pos} != {0, 1}:
        continue
    if any(pos[a][0] == pos[b][0] and abs(pos[a][1] - pos[b][1]) == 1 for a in range(3) for b in range(a + 1, 3)):
        continue
    cnt += 1
ans.append(cnt)          # N = cnt × 6!
P = ["T", "b1", "b2", "b3", "g1", "g2", "g3", "g4"]
ans.append(sum(1 for s in permutations(P, 5) if "T" in s and sum(x[0] == "b" for x in s) >= 2
               and not any(s[i][0] == s[i + 1][0] == "b" for i in range(4))))
ans.append(sum(1 for s in combinations(range(1, 13), 3) if sum(s) % 3 == 0))
ans.append(sum(1 for s in combinations(range(1, 31, 2), 2) if sum(s) % 3 == 0))
pts = [(x, y) for x in range(1, 4) for y in range(1, 4)]
lines = {frozenset(p for p in pts if col3(a, b, p)) for a, b in combinations(pts, 2)}
ans.append("⑴ $%d$ ⑵ $%d$" % (len(lines), sum(1 for t in combinations(pts, 3) if not col3(*t))))
AB = [(t, 0) for t in range(5)]                         # 두 선분: AB 위 5점, CD 위 4점, 교점 (2, 0) 공유
CD = [(2, 0), (2, 1), (2, 2), (2, -1)]
P8 = list(set(AB + CD))
ans.append(sum(1 for t in combinations(P8, 3) if not col3(*t)))


def tri_types(n):
    Q = [(math.cos(2 * math.pi * k / n), math.sin(2 * math.pi * k / n)) for k in range(n)]
    r = o = a = 0
    for t in combinations(range(n), 3):
        d = []
        for i in range(3):
            A, B, C_ = Q[t[i]], Q[t[(i + 1) % 3]], Q[t[(i + 2) % 3]]
            d.append((B[0] - A[0]) * (C_[0] - A[0]) + (B[1] - A[1]) * (C_[1] - A[1]))
        if any(abs(v) < 1e-9 for v in d):
            r += 1
        elif any(v < 0 for v in d):
            o += 1
        else:
            a += 1
    return comb(n, 3), r, o, a


ans.append("⑴ $%d$ ⑵ $%d$ ⑶ $%d$ ⑷ $%d$" % tri_types(8))
ans.append("⑴ $%d$ ⑵ $%d$ ⑶ $%d$" % tri_types(10)[:3])


def rects(cells, square=True):
    cells = set(cells)
    n = 0
    for x1 in range(10):
        for x2 in range(x1, 10):
            for y1 in range(10):
                for y2 in range(y1, 10):
                    if (square or x2 - x1 != y2 - y1) and all((x, y) in cells for x in range(x1, x2 + 1) for y in range(y1, y2 + 1)):
                        n += 1
    return n


ans.append(rects([(x, 2) for x in range(3, 7)] + [(x, 1) for x in range(1, 7)] + [(x, 0) for x in range(0, 7)]))
ans.append(rects([(x, y) for x in range(3) for y in range(5)] + [(x, y) for x in (3, 4) for y in range(2)], square=False))
fr = list("abcdefghi")
g1 = len({frozenset([frozenset(s1), frozenset(s2), frozenset(set(fr) - set(s1) - set(s2))])
          for s1 in combinations(fr, 2) for s2 in combinations(sorted(set(fr) - set(s1)), 3)})
g2 = len({frozenset([frozenset(s1), frozenset(s2), frozenset(set(fr) - set(s1) - set(s2))])
          for s1 in combinations(fr, 2) for s2 in combinations(sorted(set(fr) - set(s1)), 2)})
g3 = len({frozenset([frozenset(s1), frozenset(s2), frozenset(set(fr) - set(s1) - set(s2))])
          for s1 in combinations(fr, 3) for s2 in combinations(sorted(set(fr) - set(s1)), 3)}) * 6
ans.append("⑴ $%d$ ⑵ $%d$ ⑶ $%d$" % (g1, g2, g3))
ans.append(sum(1 for f in product(range(2, 6), repeat=6) if len(set(f)) == 2 and all(f.count(v) == 3 for v in set(f))))
# STEP 3
ans.append(10 * 9 + 9 * 8 + (8 - 2))
ans.append(sum(1 for s in combinations(range(8), 3) if any(x < 4 for x in s)))
ans.append(sum(1 for r in dist(3, 5) for b in dist(6, 5) if max(r) < 3 and all(1 <= r[i] + b[i] <= 3 for i in range(5))))
ans.append([n for n in range(5, 40) if sum(1 for s in permutations(range(n), 4) if sum(x < 3 for x in s) == 2) == 1512][0])
ans.append(sum(1 for p in permutations(range(1, 7), 4) if sum(p) % 3 == 0))
c = 0
for d in product(range(5), repeat=3):
    for ch in dist(3, 5):
        got = [0] * 5
        for x in d:
            got[x] += 1
        if all(got[i] + ch[i] > 0 for i in range(5)):
            c += 1
ans.append(c)
bars = set()
for pos in combinations(range(7), 4):
    s = tuple(1 if i in pos else 0 for i in range(7))
    bars.add(min(s, s[::-1]))
ans.append(len(bars))
f = lambda n: sum(1 for s in combinations(range(1, n + 1), 3) if s[1] - s[0] > 1 and s[2] - s[1] > 1)
ans.append(f(10) + f(14))
ans.append(sum(1 for s in combinations(range(1, 9), 3) if sum(1 for x in range(1, 9, 2) if x not in s) <= 3))
c = 0
for digs in combinations(range(10), 4):
    if sum(digs) % 2 == 0:
        continue
    for arr in permutations(list(digs) + ["*"]):
        if arr[0] != 0:
            c += 2                                    # 특수 문자 2가지
ans.append(c // 120)
grid = 0
for p in permutations(range(1, 10)):
    c1, c2, c3 = p[0:3], p[3:6], p[6:9]
    if all(x % 2 for x in c1) and all(x % 2 == 0 for x in c3) and all(list(c) == sorted(c) for c in (c1, c2, c3)):
        grid += 1
ans.append(grid)
c = sum(1 for p in permutations([1, 2, 3, 4, 10, 11, 12, 13]) if sum(p[:4]) < sum(p[4:]))
ans.append(c // 24)
ans.append(math.factorial(8) // 8)        # 대진표 모양의 대칭(두 팀씩 묶인 곳 3곳)으로 나눔
ans.append(sum(1 for t in combinations([(e, k) for e in range(3) for k in range(5)], 3) if len({e for e, k in t}) > 1))
rooms = [(f_, r) for f_ in (2, 3) for r in range(4)]
ans.append(sum(1 for q in permutations(rooms, 5) if q[0][0] == q[1][0] and abs(q[0][1] - q[1][1]) == 1))
c = 0
for s in product("HT", repeat=14):
    pr = [s[i] + s[i + 1] for i in range(13)]
    if pr.count("HH") == 0 and pr.count("TT") == 9 and pr.count("HT") == 2 and pr.count("TH") == 2:
        c += 1
ans.append(c)

items = [p for _, _, ps in data11.TYPES for p in ps] + data11.STEP3
assert len(items) == len(ans) == 34, (len(items), len(ans))
bad = 0
for no, (it, v) in enumerate(zip(items, ans), 394):
    if str(v) != it["ans"]:
        bad += 1
        print("불일치", no, it["ans"], v)
print("문항", len(items), "불일치", bad)
