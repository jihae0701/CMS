# CMS 스토리 라이트 공통수학1 11단원 단원종합문제(바꾼 5문항) 정답 독립 검산 — 모든 경우를 직접 나열해 셈
import itertools as it, importlib.util, os
R = {}
R[1] = sum(1 for c in it.combinations(range(8), 5) if 0 in c or 1 in c)          # 0=회장, 1=부회장
R[2] = sum(1 for c in it.combinations(range(1, 10), 4) if sum(c) % 2 == 0)
R[3] = sum(1 for q in it.permutations(range(1, 9), 5) if q[2] == 5 and all(q[k] < q[k + 1] for k in range(4)))
pts = [(x, 0) for x in range(5)] + [(x, 1) for x in range(5)]
def para(q):
    a, b, c, d = q                                  # 꼭짓점 순서 a-b-c-d 가 평행사변형: a+c = b+d, 세 점이 한 직선 위에 있지 않음
    if (a[0] + c[0], a[1] + c[1]) != (b[0] + d[0], b[1] + d[1]): return False
    cr = (b[0] - a[0]) * (d[1] - a[1]) - (b[1] - a[1]) * (d[0] - a[0])
    return cr != 0
shapes = set()
for c in it.combinations(pts, 4):
    if any(para(q) for q in it.permutations(c)): shapes.add(c)
R[4] = len(shapes)
cnt = 0
people = ["B%d" % i for i in range(6)] + ["G1", "G2"]
for five in it.combinations(people, 5):
    if sum(1 for p in five if p[0] == "G") == 1: cnt += 1
R[6] = cnt
sp_ = importlib.util.spec_from_file_location("s", os.path.join(os.path.dirname(os.path.abspath(__file__)), "lite_c1_11.py"))
S = importlib.util.module_from_spec(sp_); sp_.loader.exec_module(S)
bad = 0
for k, v in S.REPLACE.items():
    if str(R.get(k)) != v["ans"]: bad += 1; print("불일치", k, v["ans"], R.get(k))
print("검산", len(S.REPLACE), "불일치", bad)
