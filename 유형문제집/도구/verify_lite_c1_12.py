# CMS 스토리 라이트 공통수학1 12단원 단원종합문제(바꾼 4문항) 정답 독립 검산 — sympy 행렬로 직접 계산
import sympy as sp, importlib.util, os
R = {}
a, b, k = sp.symbols("a b k")
sol = sp.solve([a**2 - a, b - 5 + a, b - a**2 - 3], [a, b], dict=True)
assert len(sol) == 1; R[1] = sol[0][a]**2 + sol[0][b]**2
A = sp.Matrix([[k, k + 1], [2 * k, 0]]); B = sp.Matrix([[-1, k], [0, 1]]); X = sp.Matrix(2, 2, sp.symbols("x0:4"))
Xs = sp.solve(list(3 * (X - 2 * B) + A - (X - A)), list(X), dict=True)[0]
R[4] = sp.solve(sum(X.subs(Xs)) + 10, k)[0]
A, B = sp.Matrix(2, 2, sp.symbols("p0:4")), sp.Matrix(2, 2, sp.symbols("q0:4"))
s = sp.solve(list(A + 2 * B - sp.Matrix([[1, 2], [-1, 0]])) + list(A - B - sp.Matrix([[-2, -1], [5, 0]])), list(A) + list(B), dict=True)[0]
R[5] = (A.subs(s) * B.subs(s))[1, 0]
M = sp.Matrix([[1, 1], [-1, 1]])**16
assert M[0, 1] == 0 and M[1, 0] == 0 and M[0, 0] == M[1, 1]; R[6] = M[0, 0]
sp_ = importlib.util.spec_from_file_location("s", os.path.join(os.path.dirname(os.path.abspath(__file__)), "lite_c1_12.py"))
S = importlib.util.module_from_spec(sp_); sp_.loader.exec_module(S)
bad = 0
for i, v in S.REPLACE.items():
    if str(R.get(i)) != v["ans"]: bad += 1; print("불일치", i, v["ans"], R.get(i))
print("검산", len(S.REPLACE), "불일치", bad)
