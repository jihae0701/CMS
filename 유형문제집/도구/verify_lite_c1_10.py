# CMS 스토리 라이트 공통수학1 10단원 단원종합문제(바꾼 8문항) 정답 독립 검산 — 모든 경우를 직접 나열해 셈
import itertools as it, importlib.util, os
R = {}
R[1] = sum(1 for a, b in it.permutations(range(1, 6), 2) if 9 - 12 * a + 5 * b < 0)
R[2] = sum(1 for d in range(1, 1501) if 1500 % d == 0 and d % 5 == 0)
R[3] = sum(1 for n in range(10, 100) if (n // 10 + n % 10) % 2 == 1)
def cnt4(n):
    P = ["B%d" % i for i in range(n)] + ["G1", "G2"]
    c = 0
    for q in it.permutations(P):
        i, j = q.index("G1"), q.index("G2")
        if abs(i - j) == 2: c += 1
    return c
R[4] = next(n for n in range(1, 7) if cnt4(n) == 192)
R[5] = sum(1 for q in it.permutations(["B", "S1", "S2", "D1", "D2"]) if q.index("B") < q.index("D1") and q.index("B") < q.index("D2"))
R[6] = sum(1 for q in it.permutations(range(1, 10), 3) if all((q[k] - q[k + 1]) % 2 for k in range(2)))
R[7] = sum(1 for q in it.permutations(range(6), 4) if q[0] != 0 and q[3] % 2 == 0)
R[9] = sorted("".join(q) for q in it.permutations("abcde")).index("daebc") + 1
sp_ = importlib.util.spec_from_file_location("s", os.path.join(os.path.dirname(os.path.abspath(__file__)), "lite_c1_10.py"))
S = importlib.util.module_from_spec(sp_); sp_.loader.exec_module(S)
bad = 0
for k, v in S.REPLACE.items():
    if str(R.get(k)) != v["ans"]: bad += 1; print("불일치", k, v["ans"], R.get(k))
print("검산", len(S.REPLACE), "불일치", bad)
