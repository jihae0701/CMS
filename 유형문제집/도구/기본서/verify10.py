# -*- coding: utf-8 -*-
"""기본서 10단원 정답 검산: 문항마다 모든 경우를 직접 나열해 세어 data10의 답과 맞춘다.  python verify10.py"""
import sys, os
from itertools import permutations, product
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data10

ans = []


def adj(q, cond):
    return any(cond(q[i], q[i + 1]) for i in range(len(q) - 1))


def colorings(n, edges, k):
    return sum(1 for c in product(range(k), repeat=n) if all(c[i] != c[j] for i, j in edges))


# ---- 01 (g10_color1: D가 A, B, C, E와, A-B, B-C, C-E 이웃 / g10_color2: B가 A, C, D, E와, A-D, D-C 이웃)
A, B, C, D, E = range(5)
ans.append(colorings(5, [(D, A), (D, B), (D, C), (D, E), (A, B), (B, C), (C, E)], 5))
ans.append(colorings(5, [(B, A), (B, D), (B, C), (B, E), (A, D), (D, C)], 5))
# ---- 02 교란순열
ans.append(sum(1 for p in permutations(range(4)) if all(p[i] != i for i in range(4))))
ans.append(sum(1 for p in permutations(range(1, 6)) if all(p[i] != i + 1 for i in range(5))))
# ---- 03 (0 카드 두 장은 같은 숫자: 만든 수를 집합으로 센다)
cards = [0, 0, 1, 2, 3, 4]
ans.append(len({tuple(cards[i] for i in p) for p in permutations(range(6), 3) if cards[p[0]] and cards[p[2]] % 2 == 0}))
ans.append(sum(1 for p in permutations(range(5), 4) if p[0] and (10 * p[2] + p[3]) % 4 == 0))
# ---- 04
P8 = ["a1", "a2", "a3", "b1", "b2", "b3", "b4", "b5"]
ans.append(sum(1 for q in permutations(P8) if q[0][0] == "b" and q[-1][0] == "b" and not adj(q, lambda x, y: x[0] == y[0] == "a")))
P6 = ["a1", "a2", "a3", "a4", "b1", "b2"]
ans.append(sum(1 for q in permutations(P6) if q[0][0] == "a" and q[-1][0] == "a" and not adj(q, lambda x, y: x[0] == y[0] == "b")))
ans.append(len({q for q in permutations(["g1", "g2", "m1", "m2", "m3", "_"]) if not adj(q, lambda x, y: x[0] == y[0] == "g")}))
ans.append(len({q for q in permutations(["s1", "s2"] + ["_"] * 5) if not adj(q, lambda x, y: x[0] == y[0] == "s")}))
# ---- 05
seats = [(r, c) for r in range(5) for c in range(2)]
ans.append(sum(1 for a in permutations(seats, 4)                      # 남1, 남2, 여1, 여2
               if a[0][0] != a[1][0] and a[2][0] != a[3][0] and {a[0][0], a[1][0]} == {a[2][0], a[3][0]}))
seats = [("앞", 0), ("앞", 1), ("뒤", 0), ("뒤", 1), ("뒤", 2)]
ans.append(sum(1 for a in permutations(seats) if all(a[i][0] in {a[0][0], a[1][0]} for i in (2, 3, 4))))
# ---- 06
ps = sorted(permutations("12345"))
ans.append("⑴ $%d$ ⑵ $%s$" % (ps.index(tuple("31254")) + 1, "".join(ps[99])))
ws = sorted(permutations("ICEMAN"))
ans.append(ws.index(tuple("ICEMAN")) + 1)
# ---- 07 중복순열
ans.append(sum(1 for k in range(1, 5) for _ in product(".-", repeat=k)))
ans.append(sum(1 for k in range(1, 4) for _ in product("청녹적", repeat=k)))
# ---- 08 같은 것이 있는 순열
ans.append(len(set(permutations("11122"))))
ans.append(len({p for p in permutations("0111223") if p[0] != "0"}))
# ---- STEP 3
A, B, C, D, E, F = range(6)
ans.append(colorings(6, [(A, B), (B, C), (A, D), (B, E), (D, E), (D, F)], 4))
ans.append(sum(1 for p in permutations(range(5), 4) if p[0] and int("".join(map(str, p))) < 3200))
ans.append(sum(1 for p in product(range(5), repeat=3) if p[0] and p[2] % 2 == 0))
ans.append(sum(1 for t, x, y, z in product(range(1, 8), repeat=4) if x != y and y != z and max(x, y, z) < t))
ans.append(sum(1 for q in permutations(["g1", "g2", "g3", "b1", "b2", "b3", "b4"]) if all(q[i][0] != q[i + 1][0] for i in range(6))))
ans.append(len({q for q in permutations("MASTER") if all(q[i] not in "AE" or i % 2 == 1 for i in range(6))}))
ans.append(sum(1 for q in permutations(["b1", "b2", "b3", "g1", "g2", "g3"]) if q[0][0] == "b" and not adj(q, lambda x, y: x[0] == y[0] == "b")))
ans.append(sum(1 for q in permutations(["m1", "m2", "m3", "m4", "k1", "k2", "k3"]) if adj(q, lambda x, y: x[0] == y[0] == "k")))
ans.append(sum(1 for q in permutations([1, 2, 3, 4, 5]) if not adj(q, lambda x, y: x in (1, 4) and y in (1, 4))))
ans.append(sum(1 for p in permutations(range(1, 9), 4) if p[0] % 2 or p[3] % 2))
nums = sorted(n for n in range(1, 10000) if set(str(n)) <= set("0123"))
ans.append(nums[99])
ans.append(len({p for p in permutations("112345") if all(int(p[i]) % 2 or i % 2 == 1 for i in range(6))}))


def vowels_together(p):
    idx = [i for i, c in enumerate(p) if c in "aie"]
    return max(idx) - min(idx) == len(idx) - 1


ans.append(len({p for p in permutations("happiness") if vowels_together(p)}))
ans.append(sum(1 for p in permutations([1, 2, 3, 7, 8], 4) if int("".join(map(str, p))) > 6549 and int("".join(map(str, p))) % 4 == 0))
ans.append(sum(1 for q in permutations(range(3, 11)) if sum(q[:4]) == sum(q[4:])))
ans.append(sum(1 for q in permutations([1, 2, 3, 5, 9, 13]) if q[0] + q[3] < q[1] + q[4] < q[2] + q[5]))
ans.append(sum(1 for q in permutations([1, 2, 3, 4, 5, 6])
               if adj(q, lambda x, y: {x, y} == {1, 2}) and not adj(q, lambda x, y: x in (2, 3, 5) and y in (2, 3, 5))))
# 의자: 1, 3, 5번 둥근 의자, 2, 4, 6번 사각 의자
ans.append(sum(1 for q in permutations(["1a", "1b", "2a", "2b", "3a", "3b"])
               if all(i % 2 == 1 for i in range(6) if q[i][0] == "2") and not adj(q, lambda x, y: x[0] == y[0])))
seats = [(r, c) for r in range(2) for c in range(3)]
nb = lambda s, t: s[0] == t[0] and abs(s[1] - t[1]) == 1
ans.append(sum(1 for q in permutations(seats) if nb(q[0], q[1]) and nb(q[2], q[3])))
seats = [(r, c) for r in range(2) for c in range(4)]
ans.append(sum(1 for q in permutations(seats, 5) if not nb(q[0], q[1]) and q[0][0] != q[2][0]))

items = [p for _, _, ps in data10.TYPES for p in ps] + data10.STEP3
assert len(items) == len(ans) == 38, (len(items), len(ans))
bad = 0
for no, (it, v) in enumerate(zip(items, ans), 356):
    if str(v) != it["ans"]:
        bad += 1
        print("불일치", no, it["ans"], v)
print("문항", len(items), "불일치", bad)
