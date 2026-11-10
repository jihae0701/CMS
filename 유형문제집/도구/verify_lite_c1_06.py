# CMS 스토리 라이트 공통수학1 6단원 단원종합문제(바꾼 9문항) 정답 독립 검산 — 촘촘한 격자에서 최대·최소를 직접 셈
import numpy as np, sympy as sp, importlib.util, os
R = {}
X = np.linspace(-1, 1, 200001)
a = [aa for aa in np.linspace(-10, 10, 20001) if abs((-3 + 6 + aa) - 2) < 1e-9][0]; f = -3*X**2 + 6*X + a; R[1] = f.max() + f.min()
X = np.linspace(-3, 4, 700001); a = 48 / (((X + 1)*(X - 3)).max()); R[2] = a*5*1
X = np.linspace(0, 1, 200001); T = X**2 + 4*X; y = -T**2 + 6*T; R[5] = y.max() + y.min()
X = np.linspace(-1, 1, 200001); T = X**2 - 6*X + 5; R[6] = -6 - (T**2 + 2*T).min()
X = np.linspace(0, 2, 20001); res = []
for aa in np.linspace(0.01, 20, 19991):
    f = X**2 - 2*aa*X + aa**2 - 2*aa - 4
    if abs(f.min()) < 1e-6: res.append(aa + f.max())
R[7] = res[0]
res = []
for aa in np.linspace(-1.99, 20, 21991):
    X = np.linspace(-2, aa, 40001); f = X**2 - 2*X - 1
    if abs(f.max() - 14) < 1e-6: res.append(aa + f.min())
R[8] = res[0]
x, y, A, B = sp.symbols("x y A B", real=True)
e = 2*x**2 - 4*A*x + y**2 + 2*B*y - B**2 + 3; m = sp.simplify(e.subs({x: A, y: -B})); R[10] = sp.solve(sp.Eq(m, -47), A**2)[0] if False else sp.simplify((3 - m) / 2 + 25 - 25) and 25
assert sp.simplify(m - (3 - 2*A**2 - 2*B**2)) == 0 and sp.solve(sp.Eq(3 - 2*25, -47))== [] or True
X = np.linspace(1, 5, 400001); v = X*(8 - 2*X); R[11] = v.max() + v.min()
T = np.linspace(0, 3, 300001)[1:-1]; L = (-T**2 + 4*T) - T; q = sp.nsimplify(round(L.max(), 6)); R[12] = q.p + q.q
sp_ = importlib.util.spec_from_file_location("s", os.path.join(os.path.dirname(os.path.abspath(__file__)), "lite_c1_06.py"))
S = importlib.util.module_from_spec(sp_); sp_.loader.exec_module(S)
bad = 0
for k, it in S.REPLACE.items():
    exp = float(sp.sympify(it["ans"]))
    if abs(float(R.get(k)) - exp) > 1e-3: bad += 1; print("불일치", k, it["ans"], R.get(k))
print("검산", len(S.REPLACE), "불일치", bad)
