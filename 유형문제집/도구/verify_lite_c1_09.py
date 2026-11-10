# CMS 스토리 라이트 공통수학1 9단원 단원종합문제(바꾼 8문항) 정답 독립 검산 — 촘촘한 격자·정수를 직접 훑어 셈
import numpy as np, importlib.util, os
R = {}
I = np.arange(-100, 101)
R[1] = sum(a for a in range(1, 200) if np.sum(np.abs(4 * I - a) <= a) == 2)
xs = np.linspace(-20, 20, 4000001)
ok = 2 * np.abs(xs + 1) - np.abs(xs - 1) >= 3
a = xs[ok & (xs < 0)].max(); b = xs[ok & (xs > 0)].min()
R[2] = round(a * b, 3)
R[3] = int(np.sum((2 * I - 6 <= -I**2 + I) & (-I**2 + I <= -2 * I**2 + 5 * I + 12)))
res = None
for A in np.arange(0.5, 30, 0.5):
    s = xs[(xs**2 - 2 * A * xs < 0) & (xs**2 - (A - 2) * xs - 2 * A > 0)]
    if len(s) == 0: continue
    lo, hi = s.min(), s.max()
    if abs(lo**2 - 24 - hi) < 1e-3: res = A + lo
R[5] = round(res, 3)
cnt = 0
for k in range(1, 100):
    if np.any((xs**2 + 2 * xs - 24 <= 0) & (xs**2 - 3 * k * xs - 4 * k * k > 0)): cnt += 1
R[6] = cnt
ks = [k for k in np.arange(0.01, 5, 0.01) if np.sum((I**2 + I - 6 < 0) & (np.abs(I + 1) <= k + 1e-12)) == 3]
R[7] = (round(min(ks), 2), round(max(ks), 2))          # [1, 2) 이면 (1.0, 1.99)
R[8] = sum(n for n in range(1, 200) if np.sum((I**2 - 8 * I - 48 <= 0) & (np.abs(2 * I - 4) > n)) == 3)
R[9] = sum(1 for a in range(1, 100) if a + a + 3 > a + 6 and (a + 6)**2 > a * a + (a + 3)**2)
sp_ = importlib.util.spec_from_file_location("s", os.path.join(os.path.dirname(os.path.abspath(__file__)), "lite_c1_09.py"))
S = importlib.util.module_from_spec(sp_); sp_.loader.exec_module(S)
EXP = {7: (1.0, 1.99)}
bad = 0
for k, it in S.REPLACE.items():
    got = R.get(k)
    same = got == EXP[k] if k in EXP else abs(float(got) - float(it["ans"])) < 1e-3
    if not same: bad += 1; print("불일치", k, it["ans"], got)
print("검산", len(S.REPLACE), "불일치", bad)
