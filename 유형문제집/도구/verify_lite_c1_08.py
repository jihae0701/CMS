# CMS 스토리 라이트 공통수학1 8단원 단원종합문제(바꾼 8문항) 정답 독립 검산 — 정수·격자를 직접 훑어 셈
import numpy as np, importlib.util, os
R = {}
X = np.arange(-50, 51)
f = lambda x: 0.5 * (x + 1) * (x - 4); g = lambda x: -0.5 * (x + 1) * (x - 2)   # 그림과 같은 두 그래프(만나는 점 x=-1, 3)
R[1] = int(np.sum(f(X) <= g(X) + 1e-12))
xs2 = np.linspace(-10, 10, 20001); found = []
for p in range(-30, 31):
    for q in range(-30, 31):
        if p + q != 5: continue
        sol = (2 * (xs2 - 1)**2 + p) <= ((xs2 - 1)**2 + q) + 1e-12
        if sol.any() and abs(xs2[sol].min() + 2) < 1e-6 and abs(xs2[sol].max() - 4) < 1e-6: found.append(p * p + q * q)
assert len(found) == 1; R[2] = found[0]
# 3: a=1(양수 아무거나), b=-6a, c=5a 로 놓고 ax^2-cx+b>0의 해를 격자에서 확인 -> 선지 ②(x<-1 또는 x>6)
xs = np.linspace(-20, 20, 400001); a, b, c = 2.0, -12.0, 10.0
assert np.all(((a * xs**2 + b * xs + c) < 0) == ((xs > 1) & (xs < 5)))
sol = (a * xs**2 - c * xs + b) > 0
R[3] = "②" if np.all(sol == ((xs < -1) | (xs > 6))) else "?"
xs = np.linspace(-200, 200, 400001)
R[4] = next(a for a in range(1, 100) if np.all(a * xs**2 - 4 * (a + 2) * xs + 4 * a + 18 > 0))
best = None
for a in (-2.0, 0.0):
    if abs(a) < 1e-9: continue
    if abs(a * a + 2 * a) > 1e-9: continue           # x^2-2ax-2a<=0 의 해가 한 개
    for b in np.linspace(-20, 20, 40001):
        if not np.any(a * xs**2 - 4 * xs + 3 * a + b > 0):
            best = a + b if best is None else max(best, a + b)
R[5] = round(best, 6)
R[6] = next(a for a in range(1, 100) if np.any(xs**2 + 2 * (a - 2) * xs + a + 10 <= 0))
xs1 = np.linspace(-1, 1, 200001)
R[7] = next(k for k in range(-50, 50) if np.all(xs1**2 + 4 * xs1 - 3 * k + 5 < 0))
ok = [a for a in range(-50, 51) if (16 * a * a - 4 * (3 * a * a - 2 * a + 15) >= 0) and (4 * a * a - 4 * (a + 20) < 0)]
R[9] = sum(ok)
sp_ = importlib.util.spec_from_file_location("s", os.path.join(os.path.dirname(os.path.abspath(__file__)), "lite_c1_08.py"))
S = importlib.util.module_from_spec(sp_); sp_.loader.exec_module(S)
bad = 0
for k, it in S.REPLACE.items():
    exp = it["ans"]
    got = R.get(k)
    same = (str(got) == exp) if exp in "①②③④⑤" else abs(float(got) - float(exp)) < 1e-6
    if not same: bad += 1; print("불일치", k, exp, got)
print("검산", len(S.REPLACE), "불일치", bad)
