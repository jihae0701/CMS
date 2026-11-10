# CMS 스토리 라이트 공통수학1 2단원 단원 종합 문제(바꾼 12문항) 정답 독립 검산 — 조건을 만족하는 다항식을 직접 만들어 계산
import sympy as sp, importlib.util, os
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
x, t = sp.symbols("x t")
R = {}
# 1: f(2)=8, f(-2)=-2 인 아무 다항식(일차식)으로
f = sp.interpolate([(2, 8), (-2, -2)], x)
R[1] = sp.expand(f.subs(x, x/2 - 2) + f.subs(x, 2 - x/2)).subs(x, 8)
f = sp.interpolate([(sp.Rational(1, 2), 2), (0, 7)], x)
R[2] = sp.rem(sp.expand((x + 1) * f.subs(x, 2*x)), 4*x - 1, x)
f2, g2 = sp.symbols("f2 g2"); s = sp.solve([f2 + 2*g2, f2 - g2 + 1], [f2, g2])
F = sp.interpolate([(2, s[f2]), (5, 1)], x); G = sp.interpolate([(2, s[g2]), (7, 3)], x)
R[3] = sp.rem(sp.expand(3*x*F.subs(x, 2*x) - 6*x*G.subs(x, 2*x)), x - 1, x)
fx = sp.expand((1 + 2*x**2 - 4*x - 3) / 2); gx = 1 - fx
assert sp.expand(fx**2 - gx**2 - (2*x**2 - 4*x - 3)) == 0
R[4] = sp.rem(sp.expand(fx.subs(x, x + 1) * gx.subs(x, x - 1)), x - 2, x)
f = sp.expand(x*(x - 1)*(x - 2)*(x + 5) + sp.interpolate([(0, 1), (1, 3), (2, 3)], x))
assert sp.rem(f, x**2 - x, x) == 2*x + 1 and f.subs(x, 2) == 3
rr = sp.rem(f, x*(x - 1)*(x - 2), x)
opts = [3*x + 1, 3*x + 2, -x**2 + 3*x - 1, -x**2 + 3*x, -x**2 + 3*x + 1]
R[5] = "①②③④⑤"[[sp.expand(rr - o) == 0 for o in opts].index(True)]
p, q = sp.symbols("p q"); s = sp.solve([1 + p + q - 1 - 2, 8 + 4*p + 2*q - 1 - 1], [p, q])
f = x**3 + s[p]*x**2 + s[q]*x - 1; Rx = sp.rem(f, x**2 - 2*x, x)
R[6] = Rx.subs(x, f.subs(x, 3))
a, b = sp.symbols("a b"); f = x**2 + a*x + b
s = sp.solve([f.subs(x, sp.Rational(1, 2)) - f.subs(x, -sp.Rational(1, 2)), f.subs(x, 2)], [a, b])
R[7] = f.subs(s).subs(x, 3)
f = sp.expand((x**2 - 16)*(x**2 - 1))          # 짝함수이고 f(4)=f(1)=0
assert sp.rem(sp.expand(f.subs(x, x + 2)), x**2 - x - 2, x) == 0
R[8] = sp.rem(sp.expand(f.subs(x, 2*x - 2) + f.subs(x, 2*x + 3) + 2*x), x - sp.Rational(1, 2), x)
f = sp.expand((x + 1)*(x - 2)*(x**2 + 3) + sp.interpolate([(-1, 2), (2, 0)], x))
assert sp.rem(sp.expand(x**2*f), x + 1, x) == 2 and sp.rem(sp.expand(x**2*f.subs(x, x + 1)), x - 1, x) == 0
R[9] = sp.rem(f, (x + 1)*(x - 2), x)
s = sp.solve(sp.Poly(sp.rem(3*x**3 + 7*x**2 + 3*a*x + b, sp.expand((3*x - 2)**2), x), x).all_coeffs(), [a, b])
R[10] = s[a] + s[b]
P = sp.Poly(sp.expand((t + 2)**4 + 4*(t + 2)**2 - (t + 2) - 2), t)
A_, B_, C_, D_, E_ = [P.coeff_monomial(t**k) for k in (4, 3, 2, 1, 0)]
R[11] = A_*D_ - B_*C_ + E_
R[17] = (9**10 + 9**11 + 9**12) % 80

sp_ = importlib.util.spec_from_file_location("s", os.path.join(os.path.dirname(os.path.abspath(__file__)), "lite_c1_02.py"))
S = importlib.util.module_from_spec(sp_); sp_.loader.exec_module(S)
bad = 0
for k, it in S.REPLACE.items():
    exp, got = it["ans"], R.get(k)
    if isinstance(got, str):
        ok = got == exp
    else:
        e = parse_expr(exp.replace("{", "(").replace("}", ")").replace(" over ", "/"), local_dict={"x": x},
                       transformations=standard_transformations + (implicit_multiplication_application,))
        ok = sp.simplify(got - e) == 0
    if not ok:
        bad += 1; print("불일치", k, exp, got)
print("검산", len(S.REPLACE), "불일치", bad)
