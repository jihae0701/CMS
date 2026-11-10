# CMS 스토리 라이트 공통수학1 4단원 단원종합문제(바꾼 13문항) 정답 독립 검산 — sympy 복소수 계산, 실제 근 대입
import sympy as sp, importlib.util, os
I = sp.I; x, t = sp.symbols("x t"); a, b, X, Y = sp.symbols("a b X Y", real=True)
R = {}
z = X + Y*I
s = sp.solve([sp.im(z + 4*I), sp.re(z + 5 - 3*I)], [X, Y]); R[1] = s[X]*s[Y]
e = sp.expand((a*b + b*I)*I + (2 + 4*I)/(1 - I) - (a - 6 + 2*a*b*I))
R[2] = sp.simplify([v[a]**3 + v[b]**3 for v in sp.solve([sp.re(e), sp.im(e)], [a, b], dict=True)][0])
zz = -1 + 2*I; w = zz**2 + 2*zz; R[3] = sp.expand(w**2 - 3*w + 4)
e = sp.expand((z + I)*(sp.conjugate(z) + I) - (12 - 6*I))
vals = {sp.expand((z + 1)*(sp.conjugate(z) + 1)).subs(v) for v in sp.solve([sp.re(e), sp.im(e)], [X, Y], dict=True)}
R[4] = vals.pop() if len(vals) == 1 else vals
e1 = sp.expand(I*z + sp.conjugate(z)); e2 = sp.expand(z - sp.conjugate(z) - 4*I)
v = sp.solve([sp.re(e1), sp.im(e1), sp.re(e2), sp.im(e2)], [X, Y], dict=True)[0]; R[5] = sp.expand(z*sp.conjugate(z)).subs(v)
R[7] = sp.nsimplify(sp.expand(((1 + I)/I)**4 + (I/(1 - I))**4))
R[9] = sum(n for n in range(1, 21) if sp.re(sp.expand(((1 + I)/(1 - I))**n + ((1 - I)/(1 + I))**n)) > 0)
res = []
for av in range(1, 50):
    for bv in range(-50, 0):
        e = sp.expand(-av + bv*I + (2*I + bv**2)*I - (-8 + 6*I))
        if e == 0: res.append(av + bv)
R[10] = res[0] if len(res) == 1 else res
res = [av for av in range(-30, 30) if av**2 + 4*av - 5 == 0 and av**2 + 8*av + 12 < 0]
R[11] = res[0] if len(res) == 1 else res
r = sp.solve(x**2 + 2*x - 1, x); R[13] = {sp.simplify(2*p**4 + 4*p**3 - 4*q + 2) for p, q in ((r[0], r[1]), (r[1], r[0]))}.pop()
ks = []
for kk in sp.solve(sp.Eq(12*t**2, 7*t - 1), t):
    ks.append(7*kk)
    rr = sp.solve(x**2 - 7*kk*x + 7*kk - 1, x); assert sp.simplify(max(rr)/min(rr) - sp.Rational(4, 3)) == 0
d = sp.Rational(max(ks) - min(ks)); R[14] = d.p + d.q
av = 2; bv = sp.Rational(av, 5); assert 5 - 7 + av == 0
R[15] = sp.expand((x - 5*av)*(x - 5*bv)).subs(x, 1)
r1 = 4 + 2*sp.sqrt(3); r2 = 4 - 2*sp.sqrt(3); av = -(r1 + r2); bv = sp.expand(r1*r2); R[17] = bv - av

sp_ = importlib.util.spec_from_file_location("s", os.path.join(os.path.dirname(os.path.abspath(__file__)), "lite_c1_04.py"))
S = importlib.util.module_from_spec(sp_); sp_.loader.exec_module(S)
bad = 0
for k, it in S.REPLACE.items():  # REPLACE에 있는 것만 대조
    exp = sp.sympify(it["ans"].replace("{", "(").replace("}", ")").replace(" over ", "/"))
    if sp.simplify(R.get(k) - exp) != 0:
        bad += 1; print("불일치", k, it["ans"], R.get(k))
print("검산", len(S.REPLACE), "불일치", bad)
