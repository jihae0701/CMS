# CMS 스토리 라이트 공통수학1 3단원 단원종합문제(바꾼 15문항) 정답 독립 검산 — sympy 인수분해·계수 비교·완전 탐색
import sympy as sp, importlib.util, os
x, y, a, b, c, d, k, t = sp.symbols("x y a b c d k t")
R = {}
A = sp.root(sp.expand(x**3 - y**3 - 3*x*y*(x - y)), 1); assert sp.factor(A) == (x - y)**3
assert sp.factor(sp.expand(x**3 + 8*y**3 + 6*x*y*(x + 2*y))) == (x + 2*y)**3
P = sp.Poly(sp.expand((x - y)*(x + 2*y)), x, y)
R[1] = sum(v**2 for v in P.coeffs())
q, r = sp.div(sp.expand((x**2 + x + 1)**3 + (x + 1)**3), x**2 + 2*x + 2, x); assert r == 0
Q = sp.Poly(q, x); a_, b_, c_, d_ = [Q.coeff_monomial(x**i) for i in (3, 2, 1, 0)]
R[2] = a_*d_ - b_*c_
F = sp.expand((x + 1)*(x + 2)*(x + 6)*(x + 7) - 336)
R[3] = sum(aa for aa in range(-50, 51) if F.subs(x, -aa) == 0)
sols = [aa for aa in range(-20, 21) if sp.factor_list(sp.expand((x - 1)*x*(x + 1)*(x + 2) + aa))[1][0][1] == 2]
R[4] = sols[0] if len(sols) == 1 else sols
s = sp.solve(sp.Poly(sp.expand((x + a)*(x + b)*(x**2 + 2*x + c) - ((x + 1)**4 - 6*(x + 1)**2 + 5)), x).coeffs(), [a, b, c], dict=True)
R[5] = s[0][a] + s[0][b] + s[0][c]
s = [v for v in sp.solve(sp.Poly(sp.expand((x**2 + a*x + b)*(x**2 - a*x + b) - (x**4 + x**2 + 25)), x).coeffs(), [a, b], dict=True) if v[a].is_real and v[b].is_real and v[a] > 0 and v[b] > 0]
R[6] = s[0][a]**2 + s[0][b]**2
f = sp.sqrt(x**4 + 2*x**3 + 3*x**2 + 2*x + 1); ff = sp.factor(x**4 + 2*x**3 + 3*x**2 + 2*x + 1); assert ff == (x**2 + x + 1)**2
R[7] = (x**2 + x + 1).subs(x, -2)
s = sp.solve(sp.Poly(sp.expand((x + a*y - 1)*(x + b*y + c) - (x**2 - x*y - 2*y**2 - 4*x + 5*y + 3)), x, y).coeffs(), [a, b, c], dict=True)
R[8] = s[0][a]**2 + s[0][b]**2 + s[0][c]**2
ex = sp.factor(x**3 + 3*x**2*y + x**2 + 2*x*y**2 + 3*x*y + 2*y**2)
opts = [(x + 1)*(x + y)**2, (x + 1)*(x + y)*(x + 2*y), (x + 2)*(x + y)**2, (x + 2)*(x + y)*(x + 2*y), (x + 1)*(x + 2*y)**2]
R[9] = "①②③④⑤"[[sp.expand(ex - o) == 0 for o in opts].index(True)]
s = sp.solve(sp.Poly(sp.expand((x - 1)*(x - 2)*(x + c)**2 - (x**4 + a*x**3 - 6*x**2 - 4*x + b)), x).coeffs(), [a, b, c], dict=True)
R[10] = s[0][a] + s[0][b] + s[0][c]
q, r = sp.div(x**4 + a*x**3 - 7*x**2 - 8*x + b, x**2 + 5*x + 6, x)
s = sp.solve(sp.Poly(r, x).coeffs(), [a, b], dict=True)[0]
fx = sp.factor(q.subs(s)); g = x - 1; h = x - 2; assert sp.expand(g*h - q.subs(s)) == 0
R[11] = g.subs(x, s[a]) * h.subs(x, s[b])
good = []
for kk in range(-20, 21):
    fl = sp.factor_list(x**2 + 2*y**2 + 3*x*y + kk*x + 5*y + 3, x, y)
    if sum(m for _, m in fl[1]) == 2:
        good.append(kk)
R[12] = None  # 12번(171)은 원래 문항 그대로
for aa in [sp.Rational(n, 2) for n in range(1, 21)]:
    fl = sp.factor_list(x**2 + aa*x*y - 2*y**2 + 3*y - 1, x, y)
    if sum(m for _, m in fl[1]) == 2:
        R[13] = "$a=%s$, $%s$, $%s$" % (aa, "x+2y-1", "x-y+1")
        assert sp.expand((x + 2*y - 1)*(x - y + 1) - (x**2 + aa*x*y - 2*y**2 + 3*y - 1)) == 0
A3, B3 = 2*x + y, x + y
V = sp.factor(A3**3 - 3*A3*B3**2 + 2*B3**3)
# 직접 세기: 모서리 a인 정육면체에서 세 축 방향 기둥(단면 b×b)을 뺀 부피 = 포함·배제
Vd = A3**3 - (3*A3*B3**2 - 3*B3**3 + B3**3)
assert sp.expand(V - Vd) == 0
opts = [(2*x + y)*x**2, (3*x + 2*y)*x**2, (4*x + 3*y)*x**2, (5*x + 4*y)*x**2, (6*x + 5*y)*x**2]
R[14] = "①②③④⑤"[[sp.expand(V - o) == 0 for o in opts].index(True)]
cnt = 0
for A_ in range(1, 11):
    for B_ in range(1, 11):
        for C_ in range(1, 11):
            if B_**3 - C_**3 + C_*B_**2 - B_*C_**2 == 0 and B_ + C_ < A_ + 3 and A_ < B_ + C_ and B_ < A_ + C_ and C_ < A_ + B_:
                cnt += 1
R[15] = cnt

sp_ = importlib.util.spec_from_file_location("s", os.path.join(os.path.dirname(os.path.abspath(__file__)), "lite_c1_03.py"))
S = importlib.util.module_from_spec(sp_); sp_.loader.exec_module(S)
bad = 0
for kk, it in S.REPLACE.items():
    exp, got = it["ans"], R.get(kk)
    ok = (got == exp) if isinstance(got, str) else (sp.simplify(got - sp.sympify(exp)) == 0)
    if not ok:
        bad += 1; print("불일치", kk, exp, got)
print("검산", len(S.REPLACE), "불일치", bad)
