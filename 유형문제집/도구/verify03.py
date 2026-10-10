# 3단원(인수분해) 유형서 문항 정답 독립 검산 (문항 기호는 unit03.py의 v)
from itertools import product as iprod
from sympy import *
x, y, z, a, b, c, d, k, t, n = symbols('x y z a b c d k t n')
R = []


def chk(no, got, exp):
    R.append((no, simplify(sympify(got) - sympify(exp)) == 0, got, exp))


def chkmc(no, cond, lab):
    R.append((no, bool(cond), lab, lab))


def same(p, q):
    return expand(p - q) == 0


def syn(coeffs, r):
    """조립제법: (몫 계수, 나머지)"""
    out = [coeffs[0]]
    for cf in coeffs[1:]:
        out.append(expand(cf + r*out[-1]))
    return out[:-1], out[-1]


# ---- 인수분해 공식
Q_ = cancel((64*a**3 + 1)/(4*a + 1)); chk("n1052", Q_.subs(a, -1), 21)
e = 64*x**6 - 144*x**4*y + 108*x**2*y**2 - 27*y**3
s = [(p, q) for p in range(-9, 10) for q in range(-9, 10) if same(e, (p*x**2 + q*y)**3)]
assert len(s) == 1; chk("o01", s[0][0] - s[0][1], 7)
e = x**2 + y**2 + 4*z**2 + 2*x*y - 4*y*z - 4*z*x
s = [(p, q) for p in range(-5, 6) for q in range(-5, 6) if same(e, (x + p*y + q*z)**2)]
assert len(s) == 1; chk("w1", s[0][0] - s[0][1], 3)
e = (2*x - y)**3 - (y - 2*z)**3
s = [(p, q, r) for p in range(-5, 6) for q in range(-5, 6) for r in range(-5, 6)
     if same(e, p*(x - y + z)*(q*x**2 + y**2 + q*z**2 + r*x*y + r*y*z - 4*z*x))]
assert len(s) == 1; chk("o13", sum(s[0]), 4)
# x+y+z=3, (x+y)(y+z)(z+x)=-2 인 예(근이 복소수여도 항등식으로 성립)
X3 = expand((x + y + z)**3 - 3*(x + y)*(y + z)*(z + x))
assert same(X3, x**3 + y**3 + z**3)
chk("w2", 27 - 3*(-2), 33)

# ---- 치환
f = factor((x**2 + x)**2 - 8*(x**2 + x) + 12)
rs = [-r for r in roots(f, x, multiple=True)]; assert len(rs) == 4
chk("n1355", prod(rs), 12)
e = (x**2 + x)*(x**2 + x - 1) - 2
s = [(p, q) for p in range(-9, 10) for q in range(-9, 10) if same(e, (x - 1)*(x + p)*(x**2 + x + q))]
assert len(s) == 1; chk("n3031", sum(s[0]), 3)
e = (x + 1)*(x + 2)*(x - 3)*(x - 4) - 84
s = [(p, q, r) for p in range(-9, 10) for q in range(-9, 10) for r in range(-9, 10)
     if same(e, (x - 5)*(x + p)*(x**2 + q*x + r))]
assert len(s) == 1; p, q, r = s[0]; chk("n1037", 3*p + 2*q - r, 1)
e = (x**2 + 2*x)**2 - 18*(x**2 + 2*x + 1) + 63
cs = sorted(-r for r in roots(e, x, multiple=True)); pos = [v for v in cs if v > 0]
assert len(cs) == 4 and len(pos) == 2; chk("o04", pos[0]*pos[1], 15)

# ---- 복이차식
s = [(p, q) for p in range(-5, 6) for q in range(-5, 6) if p > q and same(x**4 - 6*x**2 + 1, (x**2 + p*x - 1)*(x**2 + q*x - 1))]
assert len(s) == 1; chk("w3", s[0][0] - s[0][1], 4)
f = x**4 + a*x**2 + b
s = solve([f.subs(x, 2), diff(f, x).subs(x, 2)], [a, b], dict=True); assert len(s) == 1
chk("o19", s[0][a] + s[0][b], 8)
e = (x - 1)**4 + (x - 1)**2 + 1
ok = [lab for lab, g in [("ㄱ", x**2 - x + 1), ("ㄴ", x**2 - 2*x + 2), ("ㄷ", x**2 - 3*x + 3)] if rem(e, g, x) == 0]
chkmc("o06", ok == ["ㄱ", "ㄷ"], "④")
e = x**5 - 2*x**4 + x**3 - 2*x**2 + x - 2
fl = factor_list(e)[1]; assert sorted(degree(g, x) for g, _ in fl) == [1, 2, 2]
tot = 0
for g, _ in fl:
    cf = Poly(g, x).all_coeffs()
    tot += -cf[1] if len(cf) == 2 else cf[1] + cf[2]
chk("n3099", tot, 4)

# ---- 상반식
e = x**4 - 3*x**3 - 2*x**2 - 3*x + 1
s = [(p, q) for p in range(-9, 10) for q in range(-9, 10) if p <= q and same(e, (x**2 + p*x + 1)*(x**2 + q*x + 1))]
assert len(s) == 1; chk("w13", s[0][0]**2 + s[0][1]**2, 17)
e = x**5 + 2*x**4 - 9*x**3 - 9*x**2 + 2*x + 1
s = [(p, q) for p in range(-9, 10) for q in range(-9, 10) if p > q and same(e, (x + 1)*(x**2 + p*x + 1)*(x**2 + q*x + 1))]
assert len(s) == 1; chk("w14", s[0][0] - s[0][1], 7)

# ---- 여러 문자
e = x**2 + 2*y**2 - 3*x*y + y - 1
s = [(p, q) for p in range(1, 9) for q in range(1, 9) if same(e, (x - p*y - 1)*(x - q*y + 1))]
assert len(s) == 1; chk("n1103", s[0][0] + 2*s[0][1], 5)
e = (x + 2)*(x - 1) + x*y + 5*y - 2*y**2
s = [(p, q) for p in range(-9, 10) for q in range(-9, 10) if same(e, (x + p*y + 2)*(x + q*y - 1))]
assert len(s) == 1; chk("n1251", sum(s[0]), 1)
ks = []
for kk in range(-30, 31):
    fl = factor_list(x**2 - 2*x*y - 3*y**2 - kk*x + y + 2)[1]
    if len(fl) == 2 or (len(fl) == 1 and fl[0][1] == 2):
        ks.append(kk)
assert ks == [3]; chk("n993", 3, 3)
e = 4*x**2 + y**2 - 3*z**2 + 4*x*y - 4*x*z - 2*y*z
s = [(p, q, r) for p in range(-5, 6) for q in range(-5, 6) for r in range(-5, 6)
     if same(e, (p*x + y + z)*(q*x + y + r*z))]
assert len(s) == 1; p, q, r = s[0]; chk("n1401", p - q + r, -3)
chk("w9", max(A + B for A in range(1, 30) for B in range(1, 30) if A*B + A + B == 23), 12)
cnt = sum(1 for A in range(1, 60) for B in range(1, 60) if A**2 + (2*B - 3)*A + B**2 - 3*B - 10 == 0)
chk("n1131", cnt, 4)
e = 2*x**2 + 15*y**2 - 11*x*y - 7*x + 17*y - 4
s = [(p, q, r) for p in range(-9, 10) for q in range(-9, 10) for r in range(-9, 10)
     if same(e, (2*x + p*y + 1)*(x + q*y + r))]
assert len(s) == 1; p, q, r = s[0]
g = -p*x**2 + 2*r*x - q
ok = [lab for lab, h in [("ㄱ", x - 1), ("ㄴ", x + 1), ("ㄷ", 5*x - 3), ("ㄹ", 5*x + 3)] if rem(g, h, x) == 0]
chkmc("n1234", ok == ["ㄱ", "ㄷ"], "①")

# ---- a^3+b^3+c^3-3abc
X_, Y_, Z_ = 2 + sqrt(3), 2 - sqrt(3), -4
chk("w4", expand(X_**3 + Y_**3 + Z_**3), -12)
# a+b+c=3√3, a²+b²+c²=9 인 실수 -> 합의 제곱 27 = 3(제곱합) 이므로 a=b=c (코시-슈바르츠 등호)
assert (3*sqrt(3))**2 == 3*9
chk("w5", 3*sqrt(3)**4, 27)

e = x**3 - 8*y**3 + 6*x*y + 1
s = [(p, q, r) for p in range(-5, 6) for q in range(-5, 6) for r in range(-5, 6)
     if same(e, (x + p*y + 1)*(x**2 + q*x*y + 4*y**2 - x + r*y + 1))]
assert len(s) == 1; chk("w10", sum(s[0]), 2)

# ---- 인수정리
fl = roots(x**3 - 2*x**2 - 5*x + 6, x, multiple=True); chk("o08", sum(v**2 for v in fl), 14)
av = solve((x**3 + a*x**2 - 4*x - 12).subs(x, -2), a)[0]
fl = factor_list(x**3 + av*x**2 - 4*x - 12)[1]; assert len(fl) == 3
chk("w11", av*prod(Poly(g, x).all_coeffs()[1] for g, _ in fl if g != x + 2), -18)
e = x**4 + 7*x**3 + 11*x**2 - x - 6
sols = [(p, q, r, s_) for p in range(-9, 10) for q in range(p, 10) for r in range(-9, 10) for s_ in range(-9, 10)
        if p*q*s_ == -6 and same(e, (x + p)*(x + q)*(x**2 + r*x + s_))]
assert len(sols) == 1; chk("n1146", sum(sols[0]), 4)
e = x**4 - 8*x**2 + 5*x + 6
sols = [(p, q, r, s_) for p in range(-9, 10) for q in range(p, 10) for r in range(-9, 10) for s_ in range(-9, 10)
        if p*q*s_ == 6 and same(e, (x + p)*(x + q)*(x**2 + r*x + s_))]
assert len(sols) == 1; chk("n1370", prod(sols[0]), -6)
fl = factor_list(2*x**3 + 7*x**2 + 7*x + 2)[1]
assert all(degree(g, x) == 1 for g, _ in fl)
L = sum(g for g, m in fl for _ in range(m))
chk("o20", sum(Poly(4*L, x).all_coeffs()), 32)

# ---- 인수분해의 조건
best = []
for C in range(1, 30):
    for A in range(1, 60):
        for B in range(1, 60):
            if rem(x**2 + A*x + 27, x + C, x) == 0 and rem(x**2 + B*x - 18, x + C, x) == 0:
                g1 = gcd(x**2 + A*x + 27, x**2 + B*x - 18)
                if same(g1, x + C):
                    best.append(A + B + C)
assert len(best) == 1; chk("m3212", best[0], 28)
vals = set()
for A, B, C in iprod(range(1, 9), repeat=3):
    if len({A, B, C}) == 3 and A*B*C == 8:
        P_ = Poly(expand((x + A)*(x + B)*(x + C)), x).all_coeffs()
        vals.add(P_[2]**2 - P_[1]**2)
assert len(vals) == 1; chk("n1059", vals.pop(), 147)
e = 8*x**4 + a*x - b
s = solve([e.subs(x, -Rational(1, 2)), diff(e, x).subs(x, -Rational(1, 2))], [a, b], dict=True)[0]
Q_ = cancel(e.subs(s)/(2*x + 1)**2); chk("n1464", Q_.subs(x, -1), Rational(11, 2))
# m3185: x+1이 인수, 나머지 이차식이 (x+1)을 인수로 갖거나 완전제곱식
e = x**3 + (2*a + 3)*x**2 + (3*a + 5)*x + a + 3
assert expand(e.subs(x, -1)) == 0
qcf, r0 = syn([1, 2*a + 3, 3*a + 5, a + 3], -1); assert r0 == 0
qq = qcf[0]*x**2 + qcf[1]*x + qcf[2]
cand = solve(qq.subs(x, -1), a) + solve(discriminant(qq, x), a)
sums = set()
for av in cand:
    E = expand(e.subs(a, av))
    for B in range(-20, 21):
        for C in range(-20, 21):
            if same(E, (x + B)*(x + C)**2):
                sums.add(av + B + C)
chk("m3185", max(sums) + min(sums), 6)

# ---- 인수분해의 활용
chk("w12", Rational(1003**3 + 27, 1003*1000 + 9), 1006)
chk("n1082", sum(1 for A in divisors(9**4 + 4) if A not in (1, 9**4 + 4)), 6)
chk("w15", (2027*2028*2029*2030 - 60) % (2027**2 + 3*2024 + 1), 20)
chk("w6", Rational(2025**3 + 1, 2025**2 - 2024), 2026)
chk("n3017", Rational(901*901 + 8, 963), 843)
X_, Y_ = sqrt(3) + 1, sqrt(3) - 1
chk("w7", expand(X_**3 - X_**2*Y_ - X_*Y_**2 + Y_**3), 8*sqrt(3))
chk("k32", max(m for m in range(4, 10000) if (m**4 + 2*m**2 - 3) % ((m - 1)*(m - 3)) == 0), 51)
# n1167: (a-b)(a²+b²-c²)=0 인 삼각형에서 보기 확인 (격자 탐색)
E = lambda A, B, C: A**3 + A*B**2 + B*C**2 - (A**2*B + B**3 + A*C**2)
tri = [(A, B, C) for A in range(1, 30) for B in range(1, 30) for C in range(1, 30)
       if A + B > C and B + C > A and C + A > B and E(A, B, C) == 0]
tri += [(3*s_, 4*s_, 5*s_) for s_ in (1, 2)]
g1 = all(A < C for A, B, C in tri if A != B)
g2 = all(A == B == C for A, B, C in tri if A == C)
g3 = all(A**2 + B**2 == C**2 for A, B, C in tri if C >= A and C >= B)
chkmc("n1167", (g1, g2, g3) == (True, True, False), "④")
e = x**3 - 8*x**2 - (k**2 - 5*k - 13)*x + k**2 - 5*k - 6
res = set()
for kv in solve(Eq((6 - k), (k + 1)), k) + [5, 0]:
    rs = roots(expand(e.subs(k, kv)), x, multiple=True)
    rs = sorted(rs)
    if len(rs) == 3 and all(v > 0 for v in rs) and rs[0] + rs[1] > rs[2] and len(set(rs)) < 3:
        res.add(prod(rs))
assert all(expand(e.subs(x, 1)) == 0 for _ in [0])
chk("n3037", res.pop(), Rational(49, 4))

# ---- 고난도
v = 65**3 - 3*65**2 + 194; m = integer_nthroot(v, 2); assert m[1]
chk("o23", log(m[0], 2), 9)
B_ = x**3 - 7*x + 6; C_ = x**3 + 2*x**2 - 5*x - 6
A_ = lcm(B_, C_); assert degree(A_, x) == 4
cf = Poly(A_, x).all_coeffs(); chk("o25", prod(cf[1:]), 42)
ns = set()
for A in range(-60, 61):
    for B in range(-60, 61):
        for N_ in range(1, 151):
            if A + 3*B == 2 and -6*A*B == N_:      # x² 계수·상수항 비교(x 계수는 자동 일치)
                assert same(x**3 + (3*A*B - 4)*x - N_, (x + 2)*(x - A)*(x - 3*B))
                ns.add(N_)
chk("k30", max(ns) + min(ns), 132)
f = x**3 + (a + 3)*x**2 + (2*a - b)*x - (5*a - b)
av = solve(f.subs(x, 1), a)[0]; f2 = expand(f.subs(a, av))
q2 = quo(f2, x - 1, x)
bs = solve(discriminant(q2, x), b) + solve(q2.subs(x, 1), b)
vals = [av + bv for bv in bs]
chk("n1323", max(vals) + min(vals), 22)
res = set()
for A in range(1, 50):
    g = gcd(x**4 + A*x**3 - 5*x**2 - A*x + 4, x**3 - 8*x + 8)
    if degree(g, x) == 2:
        res.add(g.subs(x, A))
assert len(res) == 1; chk("n2951", res.pop(), 4)
chk("o28", sum(1 for M in range(1, 200) for N_ in range(1, 200) if 2*M*N_ + 2*M + N_**2 + N_ == 132), 3)
for av in range(-10, 11):
    f = expand(x**3 + 8 - (x + 2)*(x**2 + av*x + av + 3))
    if degree(f, x) == 2 and LC(f, x) == 1:
        chk("o33", f.subs(x, av), -1)
e = (n - 3)*(n - 5)*(n - 7)*(n - 9) - 9
fl = factor_list(e)[1]
F_ = [g for g, m in fl if m == 2][0]; G_ = [g for g, m in fl if m == 1][0]
chk("o29", rem(G_, F_, n), -10)
ms = [m for m in range(1, 10000) if (m**3 + 4*m**2 + 8*m + 8) % (m**2 + 3*m + 2) == 0]
assert len(ms) == 1; chk("o36", ms[0], 2)
sol = set()
for A in range(1, 40):
    for B in range(A + 1, 40):
        for C in range(B + 1, 40):
            if A**2*(B + C) + B**2*(C + A) + C**2*(A + B) + 3*A*B*C == 310:
                sol.add(A**2 + B**2 + C**2)
assert len(sol) == 1; chk("w8", sol.pop(), 38)
# n1452: 직각삼각형(빗변 a), a=b+c/4, 내접원 반지름 4
B, C = symbols('B C', positive=True)
A = B + C/4
s = solve([A**2 - B**2 - C**2, B*C/2 - 4*(A + B + C)/2], [B, C], dict=True)
s = [u for u in s if u[B] > 0 and u[C] > 0]
assert len(s) == 1; chk("n1452", s[0][B]*s[0][C]/2, Rational(320, 3))
e = x**4 + (2*k - 1)*x**3 + (3*k - 6)*x**2 - (9*k - 4)*x - 10*k + 8
ks = set()
for A, B_, C in iprod(range(-20, 21), repeat=3):
    if len({A, B_, C}) == 3 and A < B_:
        # 상수항·x³ 계수로 k를 정해 항등식인지 확인
        kv = Rational(A + B_ + 2*C + 1, 2)
        if same(e.subs(k, kv), (x + A)*(x + B_)*(x + C)**2):
            ks.add(kv)
chk("n1243", sum(ks), 4)
best = None
for A in range(1, 40):
    for B_ in range(1, 40):
        g = A*x**2 + (A - 2*B_)*x - 9*A
        rs = roots(g, x, multiple=True)
        if not all(r.is_integer for r in rs):
            continue
        base = {1, -3} | set(rs)
        if len(base) == 3:          # (x-1)(x+3)·g 에 남은 일차식은 이 근 중 하나로 고르면 됨
            v = A**2 - B_**2 + 2*A + 2*B_ + 4
            best = v if best is None else min(best, v)
chk("n553", best, 13)

# 조립제법 표 검산 (해설의 syn 행이 실제 나눗셈과 맞는지)
import importlib.util, os
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
S = lambda v: parse_expr(str(v).replace("{", "(").replace("}", ")"),
                         transformations=standard_transformations + (implicit_multiplication_application, convert_xor))
sp = importlib.util.spec_from_file_location("u03", os.path.join(os.path.dirname(os.path.abspath(__file__)), "unit03.py"))
U = importlib.util.module_from_spec(sp); sp.loader.exec_module(U)
kk_ = symbols('k'); aa_ = symbols('a'); bb_ = symbols('b')
for it in U.ALL:
    for part in it["sol"]:
        if isinstance(part, dict) and "syn" in part:
            rows = part["syn"]
            cur = [S(v) for v in rows[0][1:]]
            for j in range(0, len(rows) - 1, 2):
                dv = S(rows[j][0])
                prods = [S(v) if v != "" else None for v in rows[j + 1][1:]]
                res_ = [S(v) if v != "" else None for v in rows[j + 2][1:]]
                qc, r0 = syn([c_ for c_ in cur if c_ is not None], dv)
                want = qc + [r0]
                got = [v for v in res_ if v is not None]
                assert all(expand(p_ - w_) == 0 for p_, w_ in zip(got, want)) and len(got) == len(want), (it["v"], j)
                pw = [expand(dv*w_) for w_ in want[:-1]]
                gp = [v for v in prods if v is not None]
                assert all(expand(p_ - w_) == 0 for p_, w_ in zip(gp, pw)) and len(gp) == len(pw), (it["v"], "곱", j)
                cur = qc
print("syn ok")
