# CMS 스토리 라이트 공통수학1 7단원 단원종합문제(바꾼 11문항) 정답 독립 검산 — sympy로 방정식을 직접 풀어 셈
import sympy as sp, importlib.util, os
x, y, t, a, b, c, d, k = sp.symbols("x y t a b c d k")
R = {}
def real_roots(p):
    return sorted(set(r for r in sp.Poly(p, x).all_roots() if r.is_real))
r = real_roots(x**4 + 2*x**3 - 6*x**2 + 2*x + 1); R[2] = len(r) + max(r)
r = real_roots(sp.expand((x + 1)*(x + 2)*(x - 3)*(x - 4) - 84)); assert len(r) == 2; R[3] = r[1] - r[0]
ks = []
for kv in [sp.Rational(n, 100) for n in range(-400, 401) if n != 0] + [sp.sqrt(3), -sp.sqrt(3)]:
    if len(real_roots(sp.expand(x**4 - (4*kv**2 - 6)*x**2 + 9))) == 2: ks.append(kv)
assert sorted(ks, key=float) == [-sp.sqrt(3), sp.sqrt(3)]; R[4] = sp.prod(ks)
s = 0
for n in range(-40, 41):
    av = sp.Rational(n, 4)
    if len(real_roots(x**3 + av*x**2 + 2*(av - 1)*x + av - 1)) == 2: s += av
R[7] = s
al, be, ga = sp.symbols("al be ga"); rs = sp.solve(x**3 - x**2 - 4*x + 2, x)
R[8] = sp.nsimplify(sp.N(sp.expand((rs[0] + rs[1])*(rs[1] + rs[2])*(rs[2] + rs[0])), 30), rational=True)
P = sp.expand((x - 2 - sp.sqrt(3))*(x - 2 + sp.sqrt(3))*(x - 2*sp.I)*(x + 2*sp.I)); co = sp.Poly(P, x).all_coeffs()
assert all(cc.is_rational for cc in co); R[9] = co[1]*co[2] - co[3]*co[4]
w = sp.Rational(-1, 2) + sp.sqrt(3)/2*sp.I; av = sp.symbols("av", real=True)
e = sp.expand((w**10 - w**20 + w**30 + av)**2); e = sp.simplify(e)
sol = [v for v in sp.solve(sp.im(e), av) if sp.re(e).subs(av, v) < 0]; R[10] = sol[0]
sols = sp.solve([4*x**2 - y**2, x**2 - 2*y + y**2 - 12], [x, y]); nat = [p for p in sols if all(q.is_integer and q > 0 for q in p)]
assert len(nat) == 1; R[12] = sum(nat[0])
sols = sp.solve([x + y - 6, (x - 2)*(2 - y) - 24], [x, y]); R[13] = max(p[0] - p[1] for p in sols)
ok = [n for n in range(-20, 21) if any(all(q.is_real for q in p) for p in sp.solve([x + y - 2*n, (x + 1)*(y + 1) - 7 - n*n], [x, y]))]
R[14] = min(ok)
xs, ys = sp.symbols("xs ys", positive=True)
sols = sp.solve([xs**2 + ys**2 - 208, (xs + 4)*(ys + 4) - xs*ys - 96], [xs, ys]); R[15] = set(abs(p[0] - p[1]) for p in sols).pop()
sp_ = importlib.util.spec_from_file_location("s", os.path.join(os.path.dirname(os.path.abspath(__file__)), "lite_c1_07.py"))
S = importlib.util.module_from_spec(sp_); sp_.loader.exec_module(S)
bad = 0
for i, v in S.REPLACE.items():
    if sp.simplify(sp.nsimplify(R.get(i)) - sp.sympify(v["ans"])) != 0: bad += 1; print("불일치", i, v["ans"], R.get(i))
print("검산", len(S.REPLACE), "불일치", bad)
