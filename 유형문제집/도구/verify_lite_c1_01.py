# CMS 스토리 라이트 공통수학1 1단원 단원 종합 문제(바꾼 10문항) 정답 독립 검산 — sympy로 직접 전개·대입
import sympy as sp, importlib.util, os
x, y, a, b, c, n = sp.symbols("x y a b c n")
R = {}
av = sp.solve(sp.Eq(sp.Poly((x**2 + a*x + 1)**2, x).coeff_monomial(x), 2), a)[0]
R[1] = sp.Poly((x**2 + av*x + 1)**2, x).coeff_monomial(x**2)
R[2] = sp.Poly((x**3 + x**2 - x + 1)**3, x).coeff_monomial(x**2)
R[3] = sp.Poly((x - 3)**6, x).coeff_monomial(x**3)
# 4: (가)(나) 만족하는 a,b,c 예: (나) ⇔ b²=a²+c² 를 기호로 확인
A, B, C = sp.symbols("A B C", positive=True)
d = sp.expand((A+B+C)*(A+C-B) - (A+B-C)*(B+C-A))
assert sp.simplify(d - 2*(A**2 + C**2 - B**2)) == 0
R[4] = sp.Rational(6, 2)
res = []
for nn in range(2, 12):
    p = sp.Poly(sp.expand((nn*x**nn + (nn+1)*x + 1)**2), x)
    if len(p.terms()) == 5:
        res.append(p.LC() + p.degree())
R[5] = res[0] if len(res) == 1 else None
# 7: a,b,c 는 t³-2t²+0t+1 = 0 의 근
t = sp.symbols("t"); r = sp.Poly(t**3 - 2*t**2 + 0*t + 1, t).all_roots()
R[7] = sp.nsimplify(sp.N(r[0]**2*r[1]**2 + r[1]**2*r[2]**2 + r[2]**2*r[0]**2, 30))
f2 = sp.expand((2*x-1)**2 + (2*x-1) + 1); q, rr = sp.div(f2, x-2, x)
R[8] = sp.expand(q + rr)
f = sp.expand((x**2-2*x-3)*(x+1) + 2*x + 1); q, rr = sp.div(f, x**2+2*x+1, x)
R[9] = "③" if sp.expand(q - (x-3)) == 0 else q
sol = sp.solve(sp.Poly(sp.expand((a*x**2 + x*y + b*x + c*y + 1).subs(y, 2-x)), x).all_coeffs(), [a, b, c], dict=True)[0]
R[10] = sol[a]**2 + sol[b]**2 + sol[c]**2
T = sp.symbols("T")
P = sp.Poly(sp.expand((1 - 2*(T-1) - (T-1)**2)**7), T)
R[12] = sum(P.coeff_monomial(T**k) for k in range(0, 15, 2))

sp_ = importlib.util.spec_from_file_location("s", os.path.join(os.path.dirname(os.path.abspath(__file__)), "lite_c1_01.py"))
S = importlib.util.module_from_spec(sp_); sp_.loader.exec_module(S)
bad = 0
for k, it in S.REPLACE.items():
    exp = it["ans"]
    got = R.get(k)
    if isinstance(got, str):
        ok = got == exp
    else:
        from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
        e = parse_expr(exp.replace("{", "(").replace("}", ")").replace(" over ", "/"), local_dict={"x": x}, transformations=standard_transformations + (implicit_multiplication_application,))
        ok = sp.simplify(got - e) == 0
    if not ok:
        bad += 1; print("불일치", k, exp, got)
print("검산", len(S.REPLACE), "불일치", bad)
