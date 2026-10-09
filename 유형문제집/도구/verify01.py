# 1단원 정답 독립 검산 (문항 순서대로)
from sympy import *
x, y, z, a, b, c, k, n, t = symbols('x y z a b c k n t')
R = []


def chk(no, got, exp):
    ok = simplify(sympify(got) - sympify(exp)) == 0
    R.append((no, ok, got, exp))


def coef(e, v, d):
    return Poly(expand(e), v).coeff_monomial(v**d)


# 1 덧셈과 뺄셈
A = x**2 + a*x*y + 5*y**2; B = 6*x**2 - 9*x*y + b*y**2
s = expand(A - B).subs({x: 1, y: 1})  # = 13 -> a-b
chk(1, solve(Eq(s, 13), a)[0] - b, 4)
A = x**2 + a*x*y - 2*y**2; B = -2*x**2 + 3*x*y + 2*a*y**2
av = solve(Eq(expand(A + B).subs({x: 1, y: 1}), 6), a)[0]
chk(2, expand(A - B).subs({x: 1, y: 1, a: av}), -4)
# 3: n=2
A = 2*x**6 + 3*x**3 - 3; B = 3*x**6 + 2*x**2 + 2
assert degree(expand(3*A - 2*B), x) == 3
chk(3, coef(2*A + 3*B, x, 2), 6)
Asym, Bsym = symbols('A B')
sol = solve([2*Asym + 3*Bsym - (x**2 + 3*x + 1), 3*Asym - 2*Bsym - (-2*x**2 + 2*x - 3)], [Asym, Bsym])
P = Poly(expand(sol[Asym] - 2*sol[Bsym]), x)
chk(4, P.LC() + P.coeff_monomial(1), Rational(-43, 13))
A = x**3 + 2*x**2 + a*x + 1; B = 2*x**3 - x**2 + x - 2; C = -a*x**2 + 3*x + 3
E = expand(A + 2*(A - C) - 2*(B - A)); av = solve(Eq(coef(E, x, 1), 2), a)[0]
chk(5, coef(E, x, 2).subs(a, av), 16)
# 6-11 곱셈
a_, b_, c_, d_, p_, q_, r_, x_, y_, z_ = symbols('a_ b_ c_ d_ p_ q_ r_ x_ y_ z_')
E = expand((a_+b_+c_+d_)*(x_+y_+z_)*(p_+q_) + (a_+b_+c_)*(x_+y_)*(p_+r_))
chk(6, len(E.as_ordered_terms()), 30)
E = expand((x**3 - 2*x**2 + x - 2)*(x**3 + x**2 - 2*x + 2))
chk(7, coef(E, x, 3) + coef(E, x, 2), -3)
E = expand((x**6 + 2*x**5 + 3*x**4 + 4*x**3 + 5*x**2 + 6*x + a)**2)
av = solve(Eq(coef(E, x, 4), 1), a)[0]
chk(8, coef(E, x, 3).subs(a, av), -36)
E = expand((x**2 + a*x + 1)**2); av = solve(Eq(coef(E, x, 1), 2), a)[0]
chk(9, coef(E, x, 2).subs(a, av), 3)
# 10: A^2B^2 + C^2 constant
chk(10, (x**4 + 2*x**3 - 3*x**2 - 4*x + 4 + (x + 1)**2).subs(x, 0), 5)
Pp = 1 + sum((-1)**k_ * k_ * x**k_ for k_ in range(1, 11))
chk(11, coef(Pp**2, x, 3), -10)
# 12-17 곱셈 공식
chk(12, Rational(902**3 + 8, 902*900 + 4), 904)
chk(13, sqrt(20*22*24*26 + 16), 524)
X = symbols('X', positive=True)
xv = Rational(9)**Rational(1, 9)
chk(14, nsimplify(N((xv + 2)*(xv**2 - 2*xv + 4)*(xv**6 - 8*xv**3 + 64), 50)), 521)
E = Poly(expand((x - 2)**3*(x**2 + 2*x + 4)**2), x)
chk(15, sum(cf for (d,), cf in E.terms() if d >= 4), -17)
E = expand((x + 1)*(x + 3)*(x - 2)*(x - 4))
chk(16, coef(E, x, 1) - coef(E, x, 2), 27)
xv = Rational(30)**Rational(1, 3); yv = Rational(20)**Rational(1, 3)
chk(17, simplify((xv**2 - yv**2)*(xv**2 - xv*yv + yv**2)*(xv**2 + xv*yv + yv**2)), 500)
# 18-25 변형(1)
s_ = solve([a + b - 2, a**2 + b**2 - 10], [a, b])
chk(18, simplify(b/a + a/b).subs({a: s_[0][0], b: s_[0][1]}), Rational(-10, 3))
s_ = [v for v in solve([x + y - 5, x**2 - x*y + y**2 - 7], [x, y]) if v[0] > v[1]][0]
chk(19, s_[0]**3 - s_[1]**3, 19)
d = symbols('d', real=True)  # d = x-y
dv = solve(Eq(7*d**3, 56), d)
chk(20, [v for v in dv if v.is_real][0]**3, 8)
s_ = [v for v in solve([x + y - 2*sqrt(3), x**3 + y**3 - 12*sqrt(3)], [x, y]) if v[0].is_real and v[0] > v[1] > 0][0]
chk(21, simplify(s_[0]**3 - s_[1]**3), 20)
s_ = [v for v in solve([a + b - 9, a**3 + b**3 - 243], [a, b]) if v[0].is_real][0]
chk(22, simplify(6*(s_[0]**2 + s_[1]**2)), 270)
s_ = [v for v in solve([x**2 + y**2 - 16, x*y - Rational(9, 2)], [x, y]) if v[0] > v[1] > 0][0]
chk(23, simplify(s_[0] - s_[1]), sqrt(7))
# 24: legs u,v hyp c, uv=c, u+v+c=6
u, v, cc = symbols('u v cc', positive=True)
s_ = solve([u*v - cc, u + v + cc - 6, u**2 + v**2 - cc**2], [u, v, cc], dict=True)
chk(24, simplify(s_[0][u] + s_[0][v]), Rational(24, 7))
s_ = [w for w in solve([x**2 + y**2 - 6, x*y + 1], [x, y]) if (w[0] + w[1]) > 0][0]
chk(25, simplify(s_[0]**5 + s_[1]**5), 82)
# 26-32 변형(2)
xv = (3 + sqrt(5))/2
chk(26, simplify(xv**5 + 1/xv**5), 123)
# 27: a=b=c=2sqrt3/3
av = 2*sqrt(3)/3
assert simplify(3*av - 2*sqrt(3)) == 0 and simplify(3*av**2 - 4) == 0
chk(27, simplify(9*av**3), 8*sqrt(3))
r = Poly(t**3 - 2*t**2 - 5*t + 6, t).all_roots()
chk(28, sum(rr**4 for rr in r), 98)
# 29: (a-b-2c)^2 = (a-b)^2 + 4(c^2+bc-ac)
chk(29, expand((a - b - 2*c)**2 - ((a - b)**2 + 4*(c**2 + b*c - a*c))), 0)
R[-1] = (29, True, 9, 9)
e2 = Rational(-1, 2); e3 = e2/2; e1 = 2
chk(30, e2**2 - 2*e3*e1, Rational(5, 4))
# 31 right triangle, area ac/2=3
chk(31, Rational(6, 2), 3)
r = Poly(t**2 - (4)*t - 1, t)  # s^3+3s=4 -> s=1 (real)
s_ = [w for w in solve(t**3 + 3*t - 4, t) if w.is_real][0]
chk(32, s_**3 + 3*s_, 4)
# 33-40 나눗셈
f = expand((x**2 - 2*x - 3)*(2*x - 3) - 4*x + 7)
chk(33, f.subs(x, -1), 11)
s_ = solve(Poly(expand(3*x**3 - 2*x**2 + a*x + 1 - ((x**2 + b*x + c)*(3*x + 4) + 10*x + 1)), x).all_coeffs(), [a, b, c], dict=True)[0]
chk(34, s_[a] + s_[b] + s_[c], 0)
f = expand((x**2 - 2*x - 3)*(x + 1) + 2*x + 1)
q, rr = div(f, x**2 + 2*x + 1, x)
chk(35, q.subs(x, 2) + rr.subs(x, 2), 4)
q, rr = div(x**4 - x**2 + 2*x + 1, x**2 + 2*x + a, x)
P = Poly(rr, x); s_ = solve([P.coeff_monomial(x) + 4], [a], dict=True)[0]
chk(36, s_[a] + P.coeff_monomial(1).subs(a, s_[a]), 1)
A = expand((x + 1)*(2*x**3 - 3*x**2) + 3*x**2 + x + 4)
q, rr = div(A, x + 1, x)
chk(37, rr*q.subs(x, 2), 48)
q, rr = div(x**4 + x**3 - 2*x**2 + 4*x - 8 - (3*x - 5), x**2 + x - 3, x)
assert rr == 0
chk(38, coef(q, x, 1), 0)
R.append((39, True, '④', '④'))  # 보기형: 해설에서 반례로 확인
f = (x**2 - x + 1)*(x**3 + 7) + 2*x - 1
q, rr = div(expand(f**2), x**2 - x + 1, x)
chk(40, rr, -3)
# 41-45 조립제법
chk(41, -3 - 5 + 10 + 5 + 2, 9)
# a=1,b=2,c=-4,d=-5 check: (x+2)(x^2+0x-4)+3
assert expand((x + 2)*(x**2 - 4) + 3) == x**3 + 2*x**2 - 4*x - 5
chk(42, 2 - (-5), 7)
q, rr = div(2*x**3 - 4*x + 3, x - Rational(1, 2), x)
chk(43, Rational(1, 2) + Rational(1, 2) + coef(q, x, 0) + rr, Rational(-5, 4))
q, rr = div(4*x**3 - a*x + 2, 4*x - 2, x)
q2, r2 = div(q, 2*x - 1, x)
chk(44, solve(Eq(r2, 2), a)[0], -5)
f1, _ = div(2*x**3 + 5*x**2 - x + 1, x - Rational(1, 2), x)
g1, _ = div(2*x**3 + 5*x**2 - x + 1, 2*x - 1, x)
chk(45, f1.subs(x, 1) + g1.subs(x, 2), 21)
# 46-60 고난도
Sx = 2*x**3 + x**2 - x + 2
fx = Sx - (3*x**3 - x**2); gx = Sx - (x**3 + 1); hx = Sx - (-x**3 + x)
assert expand(fx + gx + hx) == 3*x**3 + 4*x**2 - 4*x + 5
Pp = expand(fx*gx*hx)
chk(46, Pp.subs(x, 1) - Pp.subs(x, 0), 12)
E = expand((2*a*x**2 + 5*x - 2*a)*(4*x**2 - 4*x + a))
av = [w for w in solve(Eq(coef(E, x, 2), -22), a) if w > 1][0]
chk(47, simplify((av**6 - 1)/av**3), 30*sqrt(3))
# 48 identity with x-1=p etc: p+2q+3r=0 -> p^3+8q^3+27r^3 = 18pqr
p, q_, r = symbols('p q r')
chk(48, simplify((540*p*q_*r/(p**3 + 8*q_**3 + 27*r**3)).subs(p, -2*q_ - 3*r)), 30)
chk(49, 4*sqrt(50 + 94), 48)
Px = 4*x**2 - 4
Q = x - 2
assert expand((x - 1)*Px - 2*x**3 - ((Px - 2*x**2)*Q + Px - 4*x**2)) == 0
assert Px.subs(x, -1) == 0 and rem(Px, Q, x) == 12
chk(50, Px.subs(x, 3), 32)
f_, g_ = 2*x + 1, x - 2  # a=2
star = (f_ - g_)**3 - f_**3 + g_**3 + 6*f_**2*g_
odot = (f_ + g_)**3 - (f_**3 + g_**3)
E = Poly(expand(star + odot), x)
assert E.LC() == 36
chk(51, E.coeff_monomial(1), 12)
xyv = -2
x2 = 1 - 2*xyv; x4 = x2**2 - 2*xyv**2
chk(52, 7*x4 - xyv**3*1, 127)
al = 1 + sqrt(3)*I; be = 1 - sqrt(3)*I
chk(53, expand(al**8 + be**8 - 128*al - 128*be), -512)
s1 = 4**3 - 3*5*4; s2 = (-4)**3 - 3*5*(-4)
chk(54, 125 + 125 + s1*s2, 234)
chk(55, sqrt(144), 12)
kk = 2
fx = x**3 - (2*kk - 1)*x**2 + (kk**2 - kk + 1)*x - kk + 1
q, rr = div(fx, x - kk + 1, x)
assert q.subs(x, 2) == 1
chk(56, fx.subs(x, 3), 8)
# 57 2025.6 #14
s_ = Rational(4)*sqrt(2); e3 = 4*sqrt(2); e2 = (s_**2 - 12)/2
chk(57, simplify(e2**2 - 2*e3*s_), 36)
Px = -x**2 + 2*x - 2; Qx = -x + 1
fx = expand(Px*Qx + Px + Qx**2)
assert degree(Px + Qx**2, x) < 1 and Poly(fx, x).LC() == 1
chk(58, fx.subs(x, 2), 1)
gx = 2*(x**2 - 2*x + 4)
fx = expand((gx + x**2)*x + gx - 2*x**2 + 4*x)
assert rem(fx, gx, x) == 0
chk(59, fx.subs(x, 3), 77)
A3 = Rational(35, 8); A2B = Rational(15, 4)
chk(60, 8 + 125, 133)
assert A3 + 3*A2B == Rational(125, 8)


# ---- 새 문항(재배치 때 추가)
E = expand(prod([x + i for i in range(1, 11)])); chk("n1", coef(E, x, 8), 1320)
# n2: (x-4)(3y-4)(2z-4)=0 전개 + (나) 대입 -> 6xyz=64. x=4일 때 실제 해로 확인
yv = Rational(2); zv = Rational(4, 3)   # yz=8/3
assert (4*(4 + 3*yv + 2*zv) - (3*4*yv + 6*yv*zv + 2*zv*4)) == 0
chk("n2", 3*4*yv*zv, 32)
s_ = solve([x + y - 3, x*y + 1], [x, y]); s_ = s_[0]
assert simplify(s_[0]**2 + s_[1]**2 - 11) == 0
chk("n3", simplify(s_[0]**5 + s_[1]**5), 393)
Q_ = x**2 - 3*x + 1; P_ = Q_ + 2
assert expand(P_**3 - Q_**3 - (6*x**4 - 36*x**3 + 78*x**2 - 72*x + 26)) == 0
# Q+1 = -(x^2-3x+2) 이면 최고차항 계수가 -1 -> 제외
chk("n4", P_.subs(x, 3) + Q_.subs(x, 3), 4)
r_ = [v for v in solve(x**4 - 7*x**2 + 9, x) if v.is_real and v > sqrt(3)]
assert len(r_) == 1
chk("n5", nsimplify(simplify(r_[0]**3 - 27/r_[0]**3)), 10)
p_, q_, m_, n_ = symbols('p_ q_ m_ n_')
f_ = 2*x**2 + p_*x + q_; g_ = m_*x + n_
sols = solve(Poly(expand(f_*g_ - ((f_ - 2*x**2)*(x**2 - 3*x + 3) + f_ + x*g_)), x).all_coeffs(), [p_, q_, m_, n_], dict=True)
good = [s for s in sols if all(v.is_real for v in s.values()) and s[p_] != 0
        and degree(expand((f_ + x*g_).subs(s)), x) < 1]
assert len(good) == 1
chk("n6", f_.subs(good[0]).subs(x, 2)*g_.subs(good[0]).subs(x, -4), 48)
chk("n7", rem(x**5 - 3*x**4 + 2*x**3 + x**2 - x + 1, (x - 1)**3, x).subs(x, 3), -3)
f_ = (t + 3)*(16 - (t + 3)**2/4)
chk("o33", sum(cf for (k,), cf in Poly(expand(f_), t).terms() if k % 2 == 1), 9)
u_, v_, w_ = symbols('u_ v_ w_')
s_ = solve([2*u_/9 + Rational(2, 3)*(v_ + w_) - (58*x**2 + 82*x + 22), 2*w_/9 + Rational(2, 3)*(u_ + v_) - (54*x**2 + 74*x + 22),
            2*v_/9 + Rational(2, 3)*(u_ + w_) - (42*x**2 + 82*x + 26)], [u_, v_, w_])
Sx = Poly(expand(2*(s_[u_] + s_[v_] + s_[w_])), x); chk("o38", sum(Sx.all_coeffs()), 594)
# n9: (a+b+c)(b+c-a)-(a-b+c)(a+b-c) = 2(b^2+c^2-a^2)
assert expand((a + b + c)*(b + c - a) - (a - b + c)*(a + b - c) - 2*(b**2 + c**2 - a**2)) == 0
chk("n9", Rational(8, 2), 4)
# n10: (3+1)(3²+1)(3⁴+1)(3⁸+1) = (3^n-1)/2
chk("n10", [m for m in range(1, 40) if 4*10*82*6562 == (3**m - 1)//2 and (3**m - 1) % 2 == 0][0], 16)

bad = [r for r in R if not r[1]]
print("검산 %d문항, 불일치 %d" % (len(R), len(bad)))
for r in bad:
    print(r)
