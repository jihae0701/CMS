# CMS 스토리 라이트 공통수학1 5단원 단원종합문제(바꾼 7문항) 정답 독립 검산
import sympy as sp, importlib.util, os
x, a, b, k = sp.symbols("x a b k"); R = {}
s = sp.solve([(a - 2) + (a - 1) - a, (a - 2)*(a - 1) + b], [a, b], dict=True)[0]
r = sp.solve(x**2 + s[b]*x - s[a], x); R[2] = s[a] + s[b] + sum(r)
ks = [kk for kk in sp.solve(sp.discriminant(x**2 + k*x - k + 3, x), k) if sp.discriminant(x**2 - 3*x + kk + 5, x) > 0]; R[3] = ks[0] if len(ks) == 1 else ks
r1 = 2 - sp.sqrt(3); s = [v for v in sp.solve([sp.expand(-2*r1**2 + a*r1 + 4 - r1 - b)], [a, b], dict=True)]
# 유리수 조건: 무리수 부분, 유리수 부분 각각 0
e = sp.expand(-2*r1**2 + a*r1 + 4 - r1 - b); s = sp.solve([e.coeff(sp.sqrt(3)), e.subs(sp.sqrt(3), 0)], [a, b]); R[4] = s[a] + s[b]
f = lambda t: t*t - 4*t
xs = sorted(sp.solve(f(x) + 2*x - 3, x)); A = (xs[0], f(xs[0])); B = (xs[1], f(xs[1]))
C = [v for v in sp.solve(f(x) - A[1], x) if v != A[0]][0]; D = [v for v in sp.solve(f(x) - B[1], x) if v != B[0]][0]
P = [A, (D, B[1]), B, (C, A[1])]; R[5] = abs(sum(P[i][0]*P[(i+1) % 4][1] - P[(i+1) % 4][0]*P[i][1] for i in range(4)))/2
av = sp.solve(sp.discriminant(3*x**2 - 12*x + a, x), a)[0]; bv = sp.solve(sp.discriminant(3*x**2 - 12*x + av + 9*x - b, x), b)[0]; R[6] = av*bv
av = -8; R[9] = min(1 + av + bb for bb in range(-100, 200) if sp.discriminant(x**2 + av*x + bb - 2*x + 4, x) < 0)
fx = -(x - 1)*(x - 3); r = sp.solve(fx.subs(x, (x - a)/2), x); R[10] = sp.solve(sp.expand(r[0]*r[1] - a**2 - 13*a), a)[0]
sp_ = importlib.util.spec_from_file_location("s", os.path.join(os.path.dirname(os.path.abspath(__file__)), "lite_c1_05.py"))
S = importlib.util.module_from_spec(sp_); sp_.loader.exec_module(S)
bad = 0
for kk, it in S.REPLACE.items():
    exp = sp.sympify(it["ans"].replace("{", "(").replace("}", ")").replace(" over ", "/"))
    if sp.simplify(R.get(kk) - exp) != 0: bad += 1; print("불일치", kk, it["ans"], R.get(kk))
print("검산", len(S.REPLACE), "불일치", bad)
