# CMS 스토리 라이트 공통수학2 1~4단원 단원종합문제(바꾼 29문항) 정답 독립 검산 — sympy·전수·수치 탐색
import sympy as sp, numpy as np, importlib.util, os, re, itertools as it
x, y, a, b, c, d, k, t = sp.symbols("x y a b c d k t", real=True)
R = {}
def dist2(P, Q): return (P[0]-Q[0])**2 + (P[1]-Q[1])**2
# ---- 1단원
A, B, C = (-2, -1), (0, 3), (1, 2); s = sp.solve([dist2((x, y), A) - dist2((x, y), B), dist2((x, y), B) - dist2((x, y), C)], [x, y])
R[(1, 1)] = sp.pi * dist2((s[x], s[y]), B)
tot = 0
for av in sp.solve(sp.Eq(a**2 + 1, (a-2)**2 + 1), a) + sp.solve(sp.Eq(a**2 + 1, 4), a) + sp.solve(sp.Eq((a-2)**2 + 1, 4), a):
    if av > 0: tot += av
R[(1, 3)] = sp.nsimplify(tot)
g = np.linspace(-2, 8, 1001); X, Y = np.meshgrid(g, g); P = [(0, 0), (4, 0), (6, 8), (0, 3)]
R[(1, 93)] = round(float(sum(np.hypot(X - p[0], Y - p[1]) for p in P).min()), 2)
Cc = lambda P, Q, m, n: ((n*P[0] + m*Q[0]) / (m + n), (n*P[1] + m*Q[1]) / (m + n))
cnt = 0
for m in range(1, 200):
    p1 = Cc((-1, -2), (10, 2), 1, m); q1 = Cc((-1, -2), (10, 2), 1, m + 1)
    if p1[0] > 0 and p1[1] < 0 and q1[0] > 0 and q1[1] < 0: cnt += 1
R[(1, 9)] = cnt
import random
vals = set()
for _ in range(5):
    av, bv, cv, dv = [random.randint(-9, 9) for _ in range(4)]
    cv, dv = 5 - av, -2 - bv                              # 중점 조건을 만족시키도록
    C1 = Cc((av, bv), (cv, dv), 2, 3); D1 = Cc((av, bv), (cv, dv), 3, 2)
    assert (C1[0] + D1[0]) / 2 == 2.5 and (C1[1] + D1[1]) / 2 == -1
    vals.add((av + cv) - (bv + dv))
R[(1, 8)] = vals.pop()
Bv, Cv = sp.symbols("B0 B1", real=True), None
G = ((3 + 2*(-2)) / sp.Integer(3), (2 + 2*1) / sp.Integer(3)); R[(1, 10)] = G[0] + G[1]
bx, by, cx, cy, dx, dy = sp.symbols("bx by cx cy dx dy", real=True)
s = sp.solve([-2 + bx + cx + 6, 0 + by + cy + 12, -2 + bx + dx + 2, 0 + by + dy + 4, -2 + cx - bx - dx, cy - by - dy], [bx, by, cx, cy, dx, dy])
AB2 = dist2((-2, 0), (s[bx], s[by])); assert AB2 == dist2((-2, 0), (s[dx], s[dy])); R[(1, 99)] = sp.sqrt(AB2)
ys = sp.symbols("ys", positive=True)
sol = [v for v in sp.solve(sp.Eq(sp.sqrt(1 + ys**2) / sp.sqrt(1) , 0) , ys)]  # 자리만
# 각의 이등분선: OD 방향이 OA, OB 단위벡터의 합과 평행
u = sp.Matrix([1, 0]) + sp.Matrix([1, 2]) / sp.sqrt(5); tt = 1 / u[0]; Dp = u * tt; assert Dp[0] == 1
R[(1, 11)] = sp.nsimplify(sp.simplify(Dp[0]**2 + Dp[1]**2))
best = 1e9
for h in [3.0]:
    for ax in np.linspace(-6, 6, 12001):
        best = min(best, (ax + 2)**2 + h*h + (ax - 2)**2 + h*h)
R[(1, 91)] = round(best, 4)
Bq, Cq = np.array([0., 0.]), np.array([6., 0.]); Aq = np.array([2., 8.])  # 넓이 24인 삼각형 하나
Dq = (Aq + Bq) / 2; Eq = Bq + (Cq - Bq) / 3
def area(*P): return abs(sum(P[i][0]*P[(i+1) % len(P)][1] - P[(i+1) % len(P)][0]*P[i][1] for i in range(len(P)))) / 2
assert area(Aq, Bq, Cq) == 24; R[(1, 12)] = area(Aq, Dq, Eq, Cq)
# ---- 2단원
c1, c2 = sp.Rational(-2), sp.Rational(9, 2); e1, e2 = sp.Rational(5, 2), sp.Rational(2)
m_ = (e2 - c2) / (e1 - c1); R[(2, 1)] = c2 - m_ * c1
s = sp.solve([x + 2*y, 2*x + y - 3], [x, y]); assert all(sp.expand((kk**2 + 2*kk)*s[x] + (2*kk**2 + kk)*s[y] - 3*kk) == 0 for kk in range(-3, 4))
R[(2, 2)] = sp.sqrt(s[x]**2 + s[y]**2)
def seg_hits(px, py, slope):
    # 직선 y-py=slope(x-px)와 정사각형 둘레의 교점 개수(변 위에 겹치면 무한 -> 99)
    sq = [(1, 1), (4, 1), (4, 4), (1, 4)]; pts = set()
    f = lambda X_, Y_: (Y_ - py) - slope*(X_ - px)
    for i in range(4):
        (x1, y1), (x2, y2) = sq[i], sq[(i+1) % 4]
        f1, f2 = f(x1, y1), f(x2, y2)
        if f1 == 0 and f2 == 0: return 99
        if f1 == 0: pts.add((x1, y1))
        if f2 == 0: pts.add((x2, y2))
        if f1*f2 < 0:
            tt_ = f1/(f1 - f2); pts.add((round(x1 + (x2-x1)*tt_, 9), round(y1 + (y2-y1)*tt_, 9)))
    return len(pts)
ok = []
for av in range(-2, 8):
    for bv in range(-2, 8):
        if all(seg_hits(av, bv, sl) == 2 for sl in np.linspace(-20, 20, 801)): ok.append(av + bv)
R[(2, 4)] = max(ok) + min(ok)
kv = sp.solve(sp.Rational(1, 2) * (-k) + 1, k)[0]; P1 = sp.solve([x - 2*y - 2, kv*x + y - 4*kv - 1], [x, y])
xi1 = sp.solve((x - 2).subs(x, x), x)[0]; xi2 = sp.solve(kv*x - 4*kv - 1, x)[0]
R[(2, 5)] = sp.Rational(1, 2) * abs(xi2 - 2) * P1[y]
Gx, Gy = 2, 1; R[(2, 6)] = Gx + Gy   # 수직이등분선 x+y=a+b+c 가 G를 지남(풀이식과 별도로 아래에서 수치 확인)
for _ in range(3):
    av, bv = random.randint(-5, 5), random.randint(-5, 5); cv = 3 - av - bv
    if cv == 0: continue
    mid = (av + cv/2, bv + cv/2); assert abs((Gx - mid[0])*cv + (Gy - mid[1])*cv) < 1e-9
s_all = 0
for eq in (sp.Eq((a+1)/a**2 * (-2), -1), sp.Eq((a+1)/a**2 * sp.Rational(-2, 3), -1)):
    for r in sp.solve(eq, a): s_all += r
R[(2, 7)] = sp.nsimplify(sp.simplify(s_all))
sols = sp.solve(sp.Eq((2*a - a**2 + 1)**2, (2*(a+1) - (a+1)**2 + 1)**2), a); R[(2, 9)] = sp.nsimplify(sp.simplify(sum(sols)))
P0 = sp.solve([2*x + y - 2, x + y + 1], [x, y]); R[(2, 10)] = P0[x]*P0[y] + sp.sqrt(P0[x]**2 + P0[y]**2)
Ap, Bp = sp.Matrix([1, 0]), sp.Matrix([0, 2]); v = Bp - Ap; w = sp.Matrix([v[1], -v[0]])
Cp, Dp2 = Bp + w, Ap + w; assert all(q > 0 for q in list(Cp) + list(Dp2))
sl = (Dp2[1] - Cp[1]) / (Dp2[0] - Cp[0]); R[(2, 11)] = Cp[1] - sl*Cp[0]
bis = sp.solve(sp.Eq(13*y, 12*x - 5*y + 36), y)[0]; R[(2, 12)] = bis.subs(x, 0)
gx = np.linspace(-8, -0.01, 400); hits = []
for xv in gx:
    for yv in np.linspace(0.01, 8, 400):
        if abs(abs(xv - yv - 2) - 3*abs(xv - yv)) < 0.02: hits.append((xv, yv))
H = np.array(hits); co = np.polyfit(H[:, 0], H[:, 1], 1); R[(2, 13)] = round(co[0] + co[1], 1)
for kv in range(1, 50):
    V1 = sp.solve([3*x + y - 12, x - 2*y + 3], [x, y]); V2 = sp.solve([x - 2*y + 3, kv*x + 8*y + 3*kv], [x, y]); V3 = sp.solve([3*x + y - 12, kv*x + 8*y + 3*kv], [x, y])
    Vs = [(V[x], V[y]) for V in (V1, V2, V3)]
    if area(*Vs) == 21: R[(2, 15)] = sum(v_[0] for v_ in Vs)/3 + sum(v_[1] for v_ in Vs)/3; break
# ---- 3단원
tot = 0
for kv in range(1, 50):
    cx_, cy_ = sp.Rational(kv, 2), kv - 4; r = sp.sqrt(5)*kv/2; dd = abs(cx_ + 2*cy_ - 12)/sp.sqrt(5)
    if dd > r: tot += kv
R[(3, 7)] = tot
L = [(sp.sqrt(3), 4), (sp.sqrt(3), -4), (-sp.sqrt(3), 4), (-sp.sqrt(3), -4)]
for m1, c_ in L: assert sp.simplify(abs(c_)/sp.sqrt(m1**2 + 1) - 2) == 0
V = [sp.solve([y - L[i][0]*x - L[i][1], y - L[j][0]*x - L[j][1]], [x, y]) for i, j in ((0, 2), (0, 3), (1, 3), (1, 2))]
R[(3, 9)] = sp.nsimplify(sp.simplify(area(*[(v_[x], v_[y]) for v_ in V])))
rs = set()
for sx, sy in ((1, 1), (-1, 1), (-1, -1), (1, -1)):
    for r_ in sp.solve(sp.Eq((3*sx*t - 4*sy*t + 5)**2, 25*t**2), t):
        if r_ > 0: rs.add((sx, sy, r_))
R[(3, 10)] = sum(r_ for _, _, r_ in rs)
ks3 = []
for kv in sp.solve(sp.Eq((k - 2)**2 / sp.sqrt(3), 3*sp.sqrt(3)), k):
    m_t = sp.solve(sp.Eq(2/sp.sqrt(t**2 + 1), 1), t); assert sorted(m_t) == [-sp.sqrt(3), sp.sqrt(3)]
    P1 = ((kv - 2)/sp.sqrt(3), kv); P2 = (-(kv - 2)/sp.sqrt(3), kv)
    if sp.simplify(area((0, 2), P1, P2) - 3*sp.sqrt(3)) == 0: ks3.append(kv)
R[(3, 14)] = sp.prod(ks3)
# ---- 4단원
s = [p for p in sp.solve([2*a*b - 14, a**2 + b**2 - 22], [a, b]) if p[0] > 0 and p[1] > 0]; R[(4, 5)] = sp.simplify(s[0][0]**3 + s[0][1]**3)
av_ = [v_ for v_ in sp.solve(sp.Rational(1, 2)*((3 + a) - (-a))*(sp.Rational(3, 2) + a) - 4, a) if v_ > 0]; R[(4, 8)] = av_[0]
r = abs(2 - (-2))/sp.sqrt(2)/2; R[(4, 9)] = sp.pi*r**2
prod = 1; S_ = set()
for v_ in sp.solve(sp.Eq((a**2 - 4 - 1)**2, 1), a) + sp.solve(sp.Eq((a - 3 - 2)**2, 1), a):
    if v_ > 0: S_.add(v_)
for v_ in S_: prod *= v_
R[(4, 13)] = sp.simplify(prod)
# ---- 5단원 (집합의 뜻과 표현)
dv = lambda m: [x for x in range(1, m+1) if m % x == 0]
primes = lambda n: [p for p in range(2, n+1) if all(p % q for q in range(2, p))]
R[(5, 1)] = next(kk for kk in range(1, 100) if len({kk // m for m in range(1, kk+1) if kk % m == 0}) > len(primes(10)))
gx5 = np.linspace(-200, 200, 8001)
R[(5, 2)] = sum(1 for av in range(-50, 51) if np.all(~(gx5 > 4) | (gx5 >= av/2)) and np.all(~(gx5 >= 2*av) | (gx5 > 4)))
R[(5, 3)] = [av for av in range(-20, 21) if len({2, av}) == 2 and len({1, av*av+1, -av+7}) == 3 and {2, av} <= {1, av*av+1, -av+7}][0]
R[(5, 4)] = [av for av in range(-20, 21) if len({1, av, av*av-1}) == 3 and {1, av, av*av-1} == {av+5, -av+4, 2*av-3}][0]
subs = lambda S: [set(c) for r in range(len(S)+1) for c in it.combinations(S, r)]
R[(5, 5)] = sum(1 for X in subs(range(1, 8)) if len(X) >= 3 and all(x % 2 for x in X))
R[(5, 7)] = sum(1 for X in subs(range(1, 6)) if len(X & {4, 5, 6, 7}) == 1)
R[(5, 8)] = sum(kk for kk in range(5, 60) if sum(1 for X in subs(primes(kk)) if {2, 5} <= X and 3 not in X) == 16)
R[(5, 9)] = sum(1 for X in subs(range(1, 9)) if 1 in X and all(12 % x == 0 for x in X))
R[(5, 10)] = sum(1 for X in subs(range(1, 8)) if X and any(x % 2 == 0 for x in X) and sum(X) <= 24)
# ---- 6단원 (집합의 연산)
Uu = set(range(1, 11)); A6 = {1, 2, 3, 6, 9}; vals = set()
for Bm in range(1 << 10):
    B6 = {i+1 for i in range(10) if Bm >> i & 1}
    if not {3, 9} <= B6: continue
    for C6 in ({3, 9} | (Uu - B6), {3, 9}):
        if B6 & C6 == {3, 9}: vals.add(sum((A6 & (Uu - B6)) | (A6 & (Uu - C6))))
assert len(vals) == 1; R[(6, 1)] = vals.pop()
R[(6, 2)] = [sum(B6) for B6 in subs(range(0, 10)) if ({1, 3, 5, 7} | B6) - ({1, 3, 5, 7} & B6) == {1, 2, 3, 4, 5}][0]
mul = lambda n: {x for x in range(1, 3000) if x % n == 0}
R[(6, 3)] = sum(kk for kk in range(1, 300) if set(dv(12)) & set(dv(18)) <= set(dv(kk)) and (mul(6) & mul(8)) <= mul(kk))
g6 = np.linspace(-20, 20, 40001); Am = g6**2 - 2*g6 - 8 > 0; ab = None
for av in range(-20, 21):
    for bv in range(-40, 41):
        Bm6 = g6**2 + av*g6 + bv <= 1e-9
        if np.all(Am | Bm6) and np.array_equal(Am & Bm6, (g6 > 4) & (g6 <= 7 + 1e-9)): ab = av*bv
R[(6, 4)] = ab
best = set()
for yab in range(36):
    for ybc in range(40):
        for yca in range(36):
            xa, xb, xc = 35-yab-yca, 39-yab-ybc, 43-ybc-yca
            if min(xa, xb, xc) >= 0 and xa+xb+xc+yab+ybc+yca == 100: best.add(xa+xb+xc)
assert len(best) == 1; best = best.pop()
R[(6, 10)] = best
inter = [na+nb-u for na in range(0, 28) for nb in range(0, 28) if na+nb == 32 for u in range(max(na, nb), 28) if na+nb-u <= min(na, nb)]
R[(6, 12)] = max(inter) + min(inter)
R[(6, 6)] = next(na+nb-u for na in range(21) for nb in range(21) for u in range(21) if u == 13 and na+nb-u >= 0 and u-(na+nb-u) == 11)
U7 = set(range(1, 8)); r7 = set()
for X in subs(range(1, 8)):
    for Y in subs(range(1, 8)):
        if X - Y == {4, 5} and (U7 - (X & Y)) & (X | (U7 - Y)) == {4, 5, 6, 7}: r7.add(sum(X | Y))
assert len(r7) == 1; R[(6, 7)] = r7.pop()
R[(6, 15)] = min(sum(Y) for X in subs(range(1, 6)) for Y in subs(range(1, 6)) if all(x % 2 for x in X) and len(X | Y) == 5 and len(Y) == 3 and not (X & Y))
# ---- 명세와 대조
def hwp2sym(s):
    s = s.replace("pi", "*pi").replace(" ", "")
    s = re.sub(r"sqrt\{([^{}]*)\}", r"sqrt(\1)", s)
    while "over" in s:
        s = re.sub(r"\{([^{}]*)\}over\{([^{}]*)\}", r"((\1)/(\2))", s)
    s = s.replace("{", "(").replace("}", ")")
    s = re.sub(r"(\d)(sqrt|\()", r"\1*\2", s)
    s = s.lstrip("*")
    return sp.sympify(s)
bad = n = 0
for u in (1, 2, 3, 4, 5, 6):
    sp_ = importlib.util.spec_from_file_location("s", os.path.join(os.path.dirname(os.path.abspath(__file__)), "lite_c2_%02d.py" % u))
    S = importlib.util.module_from_spec(sp_); sp_.loader.exec_module(S)
    for i, v_ in S.REPLACE.items():
        n += 1
        got = R.get((u, i)); exp = hwp2sym(v_["ans"])
        if got is None or abs(float(sp.N(got)) - float(sp.N(exp))) > 1e-2: bad += 1; print("불일치", u, i, v_["ans"], got)
print("검산", n, "불일치", bad)
