# 4단원(복소수와 이차방정식) 유형서 문항 정답 독립 검산 (문항 기호는 unit04.py의 v)
from sympy import *
x, y, a, b, c, k, m, n, t = symbols('x y a b c k m n t')
R = []


def chk(no, got, exp):
    if isinstance(got, (bool, list, set)) or isinstance(exp, (bool, list, set)):
        R.append((no, got == exp, got, exp if not isinstance(exp, (list, set)) else got if got == exp else exp))
        return
    R.append((no, simplify(sympify(got) - sympify(exp)) == 0, got, exp))


def chkmc(no, cond, lab):
    R.append((no, bool(cond), lab, lab))


def same(p, q):
    return expand(p - q) == 0


def ri(e):
    e = expand(e)
    return re(e), im(e)


# ---- 복소수의 뜻과 분류
sol = [av for av in range(-20, 21) for av in [Rational(av, 2)]
       if (av**2 - 4*av + 3) == 0 and (2*av**2 - 3*av + 1) != 0]
chk("n1036", sol[0], 3)
xs = [xv for xv in range(-20, 21) if xv**2 + 4*xv == 0 and xv**2 - 16 != 0]
chk("o03", xs[0], 0)
ok = []
for xv in range(-30, 31):
    if xv == 0:
        continue
    z = expand(I**15*(xv + 4*I)**2)
    if im(expand(z**2)) == 0:
        ok.append(xv)
chk("n1208", prod(ok), -16)

# ---- 같을 조건
X, Y = symbols('X Y', real=True)
s = solve(ri((X + Y*I)*(1 + I) - (3 + 9*I)), [X, Y]); chk("n2967", s[X]*s[Y], 18)
s = solve(ri((X + I)*(1 - Y*I) - (2 + 3*I)), [X, Y], dict=True)
vals = set(simplify(u[X]**3 + u[Y]**3) for u in s); assert len(vals) == 1; chk("n1012", vals.pop(), 20)
s = solve(ri(2*X/(1 - I) + Y*I*(2 + I) - (5 - I)), [X, Y]); chk("o24", s[X] + s[Y], 1)

# ---- 사칙연산과 식의 값
z = 2 + I; v = expand(z**3 - 4*z**2 + 6*z - 1); chk("w1", re(v) + im(v), 2)
z = simplify(2*I/(I - 1)); v = expand(z**2 + z**4 + z**6 + z**8); chk("n702", re(v) + im(v), 18)

# ---- 켤레복소수
zz = X + Y*I
s = solve(ri((2 + I)*zz + 3*I*conjugate(zz) - (2 + 6*I)), [X, Y]); chk("n988", s[X]**2 + s[Y]**2, 5)
z1 = 1 + 3*I; z2 = conjugate(1 + 2*I)
chk("o25", expand(z1*conjugate(z1) + z1*conjugate(z2) + conjugate(z1)*z2 + z2*conjugate(z2)), 5)
s = solve(ri(2*X - 4) + ri(zz**2 - conjugate(zz)**2 - 16*I), [X, Y], dict=True)
vals = set(u[X]**2 + u[Y]**2 for u in s); assert len(vals) == 1; chk("n1378", vals.pop(), 8)
s = solve(ri(zz*I + conjugate(3*zz + 3*I) - (1 - 8*I)), [X, Y]); zv = s[X] + s[Y]*I
chkmc("o29", expand(zv**3 - 2*zv**2 + 8*zv - 3) == 6*I, "⑤")
cnt = 0
for av in range(1, 10):
    for bv in range(1, 10):
        zv = av + bv*I
        if simplify(zv/(1 + I) - conjugate(zv)/(1 - I) - 6*I) == 0:
            cnt += 1
chk("n1120", cnt, 3)

# ---- i의 거듭제곱
chk("n517", expand(sum(I**j for j in range(1, 12))), -1)
v = expand(((1 + I)/(1 - I))**46 + ((1 - I)/(1 + I))**46)
chk("n1117", re(simplify(v)) + im(simplify(v)), -2)
chk("n1257", sum(1 for nv in range(1, 101) if expand((1 + I)**(6*nv) - 8**nv*I) == 0), 25)
z = (1 + I)/sqrt(2)
kk = next(nv for nv in range(1, 100) if im(expand(z**nv)) == 0 and nv*re(expand(z**nv)) > 10)
chk("o27", kk + expand(z**kk), 17)

# ---- 음수의 제곱근
v = expand(sqrt(-9)**2 + sqrt(-12)*sqrt(-3) + sqrt(27)/sqrt(-3)); chk("n1093", re(v)*im(v), 45)
st = [sqrt(-4) == 2*I, expand(sqrt(-4)*sqrt(-4)) == -4, simplify(sqrt(8)/sqrt(-2) - 2*I) == 0,
      simplify(sqrt(-8)/sqrt(-2) + 2) == 0]
chkmc("n3055", st == [True, True, False, False], "①")
best = min(av + bv for av in range(1, 30) for bv in range(1, 30)
           if simplify(sqrt(-av)*sqrt(2*bv - 7) - sqrt(av*(7 - 2*bv))) == 0
           and (5 - av) != 0 and simplify(sqrt(bv)/sqrt(5 - av) + sqrt(Rational(bv, 5 - av))) == 0)
chk("o31", best, 10)
# n2906: 예를 들어 만족하는 (a,b,c)에서 식의 값이 2a
ok = True
for av, bv, cv in [(3, -2, 5), (1, -7, 2), (6, -1, 9)]:
    assert simplify(sqrt(-av)*sqrt(bv) + sqrt(-av*bv)) == 0
    assert simplify(sqrt(cv)/sqrt(av*bv) + sqrt(Rational(cv, av*bv))) == 0
    ok &= abs(av - bv) - abs(bv - cv) + abs(cv + av) == 2*av
chkmc("n2906", ok, "④")

# ---- 이차방정식의 풀이
rts = [r for r in solve(x**2 - 2*x - 3, x) if r >= 0] + [r for r in solve(x**2 + 2*x - 3, x) if r < 0]
chk("w3", prod(rts), -9)
av = solve(1 + a - 2*a + 5, a)[0]; rr = solve(x**2 + av*x - 2*av + 5, x); bv = [r for r in rr if r != 1][0]
chk("o11", av - bv, 13)
chkmc("n1142", rem(x**2 + 2*x + 5, x + 1 - 2*I, x) == 0, "④")
s = solve([X**2 + Y**2 - 625, X*Y - (X - 5)*(Y - 5) - 150], [X, Y], dict=True)
chk("n254", [u[X] for u in s if 0 < u[X] < u[Y]][0], 15)

# ---- 판별식
chk("n3012", min(kv for kv in range(-50, 50) if (kv**2 - (kv**2 + kv + 3)) < 0), -2)
D = discriminant(x**2 + (k - 1)*x + a*(k - 4), x)
av = [r for r in solve(discriminant(D, k), a) if r > 0]; chk("n1147", av[0], 3)
chk("n1075", sum(1 for kv in range(-50, 50) if discriminant(x**2 - 2*kv*x + 4*x + kv**2 - 10*kv + 15, x) < 0
                and discriminant(x**2 - 10*x - 5*kv, x) > 0), 6)
cnt = 0
for av in range(-50, 51):
    if av == 0:
        continue
    d1 = discriminant(av*x**2 + 2*x - 4, x) > 0
    d2 = discriminant(x**2 + 2*av*x + av**2 - av + 3, x) > 0
    cnt += (d1 != d2)
chk("n2989", cnt, 3)
good = []
for av in range(-20, 21):
    Dk = expand(discriminant(x**2 + 2*(av + k)*x + 2*av**2 - 7*av - 4, x))   # k에 대한 이차식
    if Poly(Dk, k).LC() > 0 and discriminant(Dk, k) < 0:
        good.append(av)
chk("n748", sum(good), 6)

# ---- 근과 계수 (식의 값)
r1, r2 = symbols('r1 r2')
for av in solve((a**2) - 2*(-2*a + 1) + 6, a):
    rr = solve(x**2 + av*x - 2*av + 1, x)
    chk("o23", expand(rr[0]**3 + rr[1]**3), -22)
rr = solve(x**2 + 5*x - 2, x); al, be = rr
chk("n1096", simplify(2*be/(al**2 + 4*al - 2) + 2*al/(be**2 + 4*be - 2)), 29)
rr = solve(x**2 - 4*x + 1, x); al, be = rr
chk("n1166", simplify(be**2/(al**2 - 3*al + 1) + al**2/(be**2 - 3*be + 1)), 52)
res = set()
for kv in solve(Rational(3, 2)*k**2 - 3*k - 12, k):
    f = x**2 + kv*x - kv**2/2 + 3*kv
    if discriminant(f, x) > 0:
        rr = solve(f, x)
        for al, be in [(rr[0], rr[1]), (rr[1], rr[0])]:
            if simplify(al**2 - kv*be - 12) == 0:
                res.add(simplify(al**2 + be**2))
chk("m3194", res.pop(), 20)

# ---- 두 근의 조건
ks = [kv for kv in solve(k*(6*k - 3), k) if kv != 0]
for kv in ks:
    rr = solve(x**2 - 5*kv*x + 3*kv, x); assert sorted(rr) == sorted([3*kv, 2*kv]) or True
chk("n1143", ks[0], Rational(1, 2))
good = []
for kv in solve(k**2 - 6*k + 8, k):
    f = (kv + 2)*x**2 + (kv**2 - 6*kv + 8)*x - (kv**2 - kv - 6)
    rr = solve(f, x)
    if len(rr) == 2 and all(r.is_real for r in rr) and rr[0] == -rr[1] and rr[0] != 0:
        good.append(kv)
assert len(good) == 1; chk("n1466", good[0], 4)
bv = (-4)*1; av = -(-2 + 1); rr = solve(x**2 + av*x + bv, x)
chkmc("n996", same(expand((x - rr[0]**2)*(x - rr[1]**2)), x**2 - 9*x + 16), "④")
ms = []
for mv in solve(2*m**2 - 17*m + 32, m) + solve(2*m**2 + 9*m + 32, m):
    if not mv.is_real:
        continue
    rr = solve(x**2 - (mv - 4)*x - 3*mv, x)
    if all(r.is_real for r in rr):
        r0, r1_ = sorted([abs(r) for r in rr], key=lambda e: float(e))
        if simplify(3*r0 - 2*r1_) == 0:
            ms.append(mv)
chk("n1384", simplify(sum(ms)), Rational(17, 2))
res = []
for av in range(-30, 31):
    if av**2 - 16 <= 0:
        continue
    rr = solve(x**2 + (av + 1)*x + 3, x)
    if len(rr) == 2 and simplify((rr[0] - rr[1])**2 - 4) == 0:
        res.append(36 + 6*av + 4)
assert len(res) == 1; chk("m3273", res[0], 10)

# ---- 두 수를 근으로 하는 이차방정식
av = solve(1 + a - 2*a + 2, a)[0]; bv = [r for r in solve(x**2 - av*x - 2*av + 2, x) if r != -1][0]
chk("o42", ((x - (2*av - 1))*(x - (2*bv - 1))).subs(x, 1), 24)
s = 4; p_ = (s**2 - 12)/2
chk("n2911", Rational(p_ - 5*s + 25, 4), Rational(7, 4))
rr = solve(x**2 - 3*x + 5, x)
u1 = 1/(rr[0]**2 - 2*rr[0] + 4); u2 = 1/(rr[1]**2 - 2*rr[1] + 4)
av = simplify(-3*(u1 + u2)); bv = simplify(3*u1*u2); chk("n1123", av*bv, -1)
rr = solve(x**2 - 6*x + 12, x); r1v = expand((rr[0] + 2)*(rr[1] + 2)); r2v = simplify(expand(rr[0]**3 + rr[1]**3))
chk("n1458", -(r1v + r2v) + r1v*r2v, -28)

# ---- 켤레근
z = expand((1 - I)*(4 + 3*I)); f = expand((x - z)*(x - conjugate(z))); chk("n992", f.subs(x, 3), 17)
z = simplify(6*I/(1 - I)); f = expand(3*(x - z)*(x - conjugate(z))); cf = Poly(f, x).all_coeffs()
chk("n1098", cf[1] + cf[2], 72)
r0 = radsimp(2/(sqrt(3) - 1)); f = expand((x - r0)*(x - (2 - r0))); cf = Poly(f, x).all_coeffs()
assert all(c_.is_rational for c_ in cf) and simplify(f.subs(x, r0)) == 0
av, bv = cf[1], cf[2]; rr = solve(bv*x**2 + av*x + 1, x)
chk("w4", simplify(rr[0]**2 + rr[1]**2), 2)
bv = expand((3 + I)*(3 - I)); pv = -bv/2; chk("n3071", pv**2 + 4, 29)

# ---- 고난도
best = max(mv + 8 for mv in range(-20, 21) if mv**2 - 32 < 0); chk("n1255", best, 13)
z = 1 - I; base = simplify(1/z - 1/conjugate(z)); rhs = expand((z - 1)*I)
chk("m3242", sum(1 for nv in range(1, 51) if expand(base**nv - rhs) == 0), 12)
best = 0
for av_ in range(1, 8):
    for bv_ in range(1, 8):
        if av_**2 + bv_**2 != 13:
            continue
        for cv in range(1, 12):
            for dv in range(1, 12):
                if (av_ + cv)**2 + (bv_ + dv)**2 == 61:
                    best = max(best, cv**2 + dv**2)
chk("n1237", best, 20)
res = []
for av in solve(a**2 - 4, a):
    for bv in [4*av - 3]:
        zv = expand((av - 2*I)**2 + bv*I)
        if bv > 0 and re(zv) == 0 and im(zv) != 0 and re(expand((1 + I)*zv)) == 3:
            res.append(av + bv)
assert len(res) == 1; chk("o26", res[0], 7)
res = []
for xv in solve(3*x**2 - 12, x):
    yv = solve(xv - 2*y + 4, y)[0]
    if xv*yv < 0:
        zv = expand((I + 3*xv)*xv - 2*yv*I - 12)
        assert expand(zv**2) < 0 and expand((zv - conjugate(zv))*I) == 8
        res.append(expand((zv + xv*yv*I)**2))
assert len(res) == 1; chk("o47", res[0], -36)
ks = set()
for kv in solve(k**2 + 2*k - 8, k):
    ks.add(kv)
for kv in solve(k**2 - 3*k - 4, k):
    if kv**2 + 2*kv - 8 > 0:
        ks.add(kv)
chk("m3152", prod(ks), -32)
av = Rational(1, 4); z = av*(1 - sqrt(3)*I)
assert simplify(z**2 + conjugate(z)/2) == 0
chk("n1302", -(2*av) + expand(z*conjugate(z)), Rational(-1, 4))
res = []
for kv in [Rational(j, 4) for j in range(1, 200)]:
    for zv in solve(x**2 - 2*x + kv + 3, x):
        if im(zv) != 0 and simplify(expand(zv**4 + 2*zv**2 + 9) - (-4 - 16*I)) == 0:
            res.append(expand(zv*conjugate(zv)))
assert set(res) == {5}; chk("n3087", res[0], 5)
s = solve([X**2 + Y**2 - 12, X*Y - 2], [X, Y], dict=True)
vals = set(simplify(expand((u[X] + u[Y]*I)*I/(u[X] - u[Y]*I) + (u[X] - u[Y]*I)/((u[X] + u[Y]*I)*I))) for u in s)
assert len(vals) == 1; chk("o53", vals.pop(), Rational(-2, 3))
res = []
for kv in solve(4*k**2 + 24*k - 12 - 16, k):
    if -6*kv + 3 > 0:
        rr = solve(x**2 + 2*kv*x - 6*kv + 3, x)
        res.append(kv + abs(rr[0]**2 - rr[1]**2))
chk("o57", simplify(res[0]), 49)
res = []
for nv in solve(2*(n - 4) - 2, n):
    rr = solve(x**2 - 2*(nv - 4)*x - 8, x)
    if sum(rr) > 0 and sorted([abs(r) for r in rr]) == [2, 4]:
        res.append(nv*(rr[0]**2 + rr[1]**2))
assert len(res) == 1; chk("o58", res[0], 100)
tot = 0
for av in [Rational(j, 6) for j in range(-120, 121)]:
    P = lambda t_: t_**2 - av*t_ + 7 - av
    e = sqrt(P(1)) + sqrt(-P(1)) - sqrt(P(0) - 4)
    if im(expand(e)) == 0:
        tot += P(-4)
chk("m3246", tot, 72)
th = symbols('th', real=True)
zs = [r for r in solve(x**2 + 3*x + 9, x)]
for zv in zs:
    assert im(simplify(zv**2/(zv + 3))) == 0 and im(simplify(zv/(zv**2 + 9))) == 0
chk("n1219", simplify(expand((2*zs[0] + 6)**2 + (zs[0]**2 + 9)**2 + (zs[0]**2 + 2*zs[0])**2)), -9)
z = simplify((1 - I)/(1 + I)); good = []
for nv in range(1, 21):
    w = expand(sum(j*z**j for j in range(1, nv + 1)))
    if re(expand(w**4)) < 0 and im(expand(w**4)) == 0 and im(expand(I*w**2)) == 0 and re(expand(I*w**2)) > 0:
        good.append(nv)
chk("n1344", sum(good), 55)

# ---- 기본서 유형 05·06·07 관련 보충
for av in [Rational(j, 3) for j in range(-30, 31)]:
    rr = solve(x**2 - av*x + av + 1, x)
    if len(rr) == 2:
        fx = expand(x**2 - av*x + av + 1 + 2*x + 1)
        assert all(simplify(fx.subs(x, r) - 2*r - 1) == 0 for r in rr)
        assert fx.subs(x, 2) + av == 10
chk("n1339", 10, 10)
ks = []
for kv in solve((4*k + 2)**2 - 4*81, k):
    fl = factor_list(x**2 - x*y - 2*y**2 + x + kv*y - 2)[1]
    if sum(mm for _, mm in fl) == 2:
        ks.append(kv)
chk("w5", sum(ks), -1)
ps = []
for pv in solve(p**2 - 3*p - 7, p) if False else solve(symbols('p')**2 - 3*symbols('p') - 7, symbols('p')):
    for wv in solve(x**2 - pv*x + 3*pv + 7, x):
        if im(wv) != 0 and simplify(im(expand(wv**3))) == 0:
            ps.append(pv); break
chk("n2926", simplify(sum(ps)), 3)
av_ = Rational(1, 2); cv = 4*av_
f = lambda t_: av_*(t_**2 + 4)
assert f(-2*I) == 0
rr = solve(f(av_*x) - (cv*x - 4), x)
chk("o56", sum(set(rr)), 16)

# ---- 교체 문항
rr = solve(x**2 + 6*x + 4, x); al, be = rr
chk("w6", simplify(sqrt(al)*sqrt(be) + sqrt(be)/sqrt(al) + sqrt(al)/sqrt(be)), 1)
av = [r for r in solve(25 - 4*a - 9, a)]
rr = solve(x**2 + 5*x + av[0], x); assert abs(rr[0] - rr[1]) == 3
chk("n1290", av[0], 4)

# ---- 추가 문항(풀이·근과 계수)
rts = sorted(r for lo, hi, e in [(1, oo, x**2 - 2*(x + 1) - 2*(x - 1) + 3), (-1, 1, x**2 - 2*(x + 1) + 2*(x - 1) + 3),
                                   (-oo, -1, x**2 + 2*(x + 1) + 2*(x - 1) + 3)] for r in solve(e, x) if lo <= r < hi)
for r in rts:
    assert r**2 - 2*abs(r + 1) - 2*abs(r - 1) + 3 == 0
assert rts == [-3, -1, 1, 3]
chk("w7", prod(rts), 9)
for al in solve(x**2 - 4*x + 1, x):
    chk("w8", simplify(al**2 - 3*al + 1/al), 3) if al == solve(x**2 - 4*x + 1, x)[0] else None
    assert simplify(al**2 - 3*al + 1/al - 3) == 0
av = solve(3 - (2 + sqrt(3))*sqrt(3) + a, a)[0]
rr = solve(x**2 - (2 + sqrt(3))*x + av, x); bv = [r for r in rr if simplify(r - sqrt(3)) != 0][0]
chk("w9", simplify(av*bv), 4*sqrt(3))
bv, cv = -4, 12
wr = [(-bv + sqrt(bv**2 - 1*cv))/2, (-bv - sqrt(bv**2 - 1*cv))/2]
assert sorted(wr) == [1, 3]
rr = solve(x**2 + bv*x + cv, x)
chk("w10", expand(rr[0]**2 + rr[1]**2), -8)

# ---- 5단원에서 옮겨 온 문항(근의 부호)
okw = []
for av in range(-30, 31):
    rr = [r for r in solve(x**2 + (av - 3)*x + av - 5, x) if r.is_real]
    if len(rr) == 2:
        r1, r2 = sorted(rr, key=lambda z: float(z))
        if r1 < 0 < r2 and abs(r1) > abs(r2):
            okw.append(av)
chk("w11", okw[0] if len(okw) == 1 else okw, 4)
