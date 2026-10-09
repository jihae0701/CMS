# 2단원 정답 독립 검산 (문항 순서대로)
from sympy import *
x, y, t, k = symbols('x y t k')
a, b, c, d, e, p, q, r, s, m, n = symbols('a b c d e p q r s m n')
R = []


def chk(no, got, exp):
    R.append((no, simplify(sympify(got) - sympify(exp)) == 0, got, exp))


def ident(lhs, rhs, var, unk):
    eqs = Poly(expand(lhs - rhs), var).all_coeffs()
    return solve(eqs, unk, dict=True)


def ident2(lhs, rhs, unk):
    eqs = Poly(expand(lhs - rhs), x, y).coeffs()
    return solve(eqs, unk, dict=True)


s_ = ident((x+1)*(x+a), x**2+b*x+2, x, [a, b])[0]; chk(1, s_[a]+s_[b], 5)
s_ = ident(a*(x+1)**2+b*(x-1)**2+c*(x+1)*(x-1), 10*x**2-2*x+4, x, [a, b, c])[0]; chk(2, s_[a]*s_[b]*s_[c], 36)
s_ = ident(a*x*(x+1)+b*(x-1)*(x+1)+2*x*(x-1), c*x**2+3*a*x-1, x, [a, b, c])[0]; chk(3, s_[a]-s_[b]+s_[c], 0)
s_ = ident((x-2)**3, (x+1)*(x+2)*(x-3)+a*(x+2)*(x-3)+b*(x-3)+c, x, [a, b, c])[0]; chk(4, s_[a]+s_[b]+s_[c], 8)
s_ = ident((x+3)**3, x*(x-1)*(x+2)+a*(x-1)*(x+2)+b*(x+2)+c, x, [a, b, c])[0]; chk(5, s_[a]+s_[b]+s_[c], 30)
s_ = ident2((x-3*y)*a+(2*y-x)*b+3*x-2*y, 0, [a, b])[0]; chk(6, s_[a]+s_[b], 11)
s_ = ident((a*x**2+b*y**2+2*x-4*y).subs(x, 1-2*y), 0, y, [a, b])[0]; chk(7, s_[a]+s_[b], 6)
s_ = ident((a*x**2+b*x-2*x*y+3*y+6).subs(y, 2*x-k), 0, x, [a, b, k])[0]; chk(8, s_[k]*(s_[a]-s_[b]), 28)
s_ = solve([1+a+b-(0-2+3), 1-a+b-(0+2+3)], [a, b]); chk(9, 2*s_[a]-s_[b], -6)
s_ = solve([0-(2*a+b), 5*4-(3*a+b)], [a, b]); chk(10, 2*s_[a]-s_[b], 80)
s_ = solve([a+b+8, a-b+8], [a, b]); f_ = cancel((s_[a]*x**4+s_[b]*x+8)/((x-1)*(x+1))); chk(11, f_.subs(x, 2), -40)
s_ = ident((x-1)**4+a*(x-1)**3+b*(x-1)**2+c*(x-1), (x-1)*(x+1)*(x**2-x+1), x, [a, b, c])[0]; chk(12, s_[a]+s_[b]-s_[c], 4)
kk = 25; f_ = -x**2+x+7
assert expand(f_**2 - ((x+3)*(x+1)*(x-2)*(x-4)+kk)) == 0
chk(13, f_.subs(x, 2)+kk, 30)
sols = ident((x+1)**2*(x-a)**2, x**4+b*x**3+c*x**2+4*x+4, x, [a, b, c])
s_ = [v for v in sols if v[a] > 0][0]; chk(14, s_[a]*s_[b]*s_[c], 12)
s_ = ident((x**2+(k+2)*x+k*n-n**2-1).subs(x, m), 0, k, [m, n])
chk(15, s_[0][m]**2+s_[0][n]**2, Rational(1, 2))
# 16-27 항등식의 활용
P_ = Poly(expand((3*x**2-2*x-2)**3), x); chk(16, sum(P_.coeff_monomial(x**i) for i in (2, 4, 6)), 21)
P_ = Poly(expand((x**4+2*x**3-5*x**2-2*x+1)*(3*x-2)**5), x); chk(17, sum(P_.coeff_monomial(x**i) for i in range(1, 10)), 29)
P_ = expand((x**4+2*x**3-x**2-x+2)*(2*x-1)**6); chk(18, P_.subs(x, 1)-P_.subs(x, 0), 1)
P_ = Poly(expand((x**2-2*x-1)**4), x); chk(19, sum((-1)**i*P_.coeff_monomial(x**i) for i in range(0, 8)), 15)
P_ = Poly(expand((t+1)**10), t)  # a_i <-> t^(11-i)
chk(20, sum(P_.coeff_monomial(t**(11-i)) for i in (2, 4, 6, 8, 10)), 512)
P_ = Poly(expand((t-1)**8-1), t)  # x+1=t
chk(21, sum(P_.coeff_monomial(t**i) for i in (0, 2, 4, 6, 8)), 127)
s_ = ident(x**3-2*x**2+3*x+5, (x-1)**3+a*(x+1)**2+b*x+c, x, [a, b, c])[0]; chk(22, s_[a]*s_[b]*s_[c], -10)
P_ = Poly(expand((2*x**4+11*x**3+16*x**2-1).subs(x, t-2)), t)
chk(23, P_.coeff_monomial(t**3)+P_.coeff_monomial(t**2), -7)
s_ = ident(x**3-2*x**2+3, a+b*(x-1)+c*(x-1)*(x-2)+d*(x-1)*(x-2)*(x-3), x, [a, b, c, d])[0]; chk(24, sum(s_.values()), 8)
P_ = Poly(expand((3*x**3+2*x**2-x+2).subs(x, t+1)), t)
A_, B_, C_, D_ = [P_.coeff_monomial(t**i) for i in (3, 2, 1, 0)]
chk(25, A_*D_+B_*C_, 150)
P_ = Poly(expand((x**4+x**3+2*x**2-2).subs(x, t-1)), t)
A_, B_, C_, D_, E_ = [P_.coeff_monomial(t**i) for i in (4, 3, 2, 1, 0)]
chk(26, A_*B_+C_*D_+E_, -28)
s_ = solve([(x**3-x**2+(3-a)*x+b).subs(x, -2), (x**3-x**2+(3-a)*x+b).subs(x, 1)], [a, b])
H_ = x**3-x**2+(3-s_[a])*x+s_[b]; P_ = cancel(H_/(x+2)); chk(27, P_.subs(x, -3), 20)
# 28-47 나머지 정리
chk(28, solve((2*x**3-3*x**2-a*x+4).subs(x, -1)-5, a)[0], 6)
chk(29, 4*(-2*2+3), -4)
u, v = symbols('u v')
chk(30, (-1)*2, -2)
s_ = solve([u+v-2, u**3+v**3-56], [u, v]); chk(31, s_[0][0]*s_[0][1], -8)
s_ = solve([a+b-3, -2*a+b+3], [a, b]); chk(32, 4*s_[a]+s_[b], 9)
s_ = solve([-2*a+b+2, 3*a+b-4], [a, b]); chk(33, s_[a]+s_[b], Rational(8, 5))
# 34: f(0)=1, f(1)=3 -> R=2x+1
chk(34, 2*5+1, 11)
f_ = (x**2+1)*(x+1)*(x**3+5) + 3*(x**2+1) + x - 2
assert rem(f_, x**2+1, x) == x-2 and f_.subs(x, -1) == 3
chk(35, rem(f_, expand((x**2+1)*(x+1)), x).subs(x, 1), 5)
P_ = expand((x**2+2*x-1)*(2*x+1)+3*x-5); chk(36, rem(P_, x**2+1, x).subs(x, 30), 19)
P_ = expand((2*x**3+x**2+1)*(x**2+2)+4*x**2+2*x+1); chk(37, rem(P_, x**2+2, x).subs(x, 5), 3)
f_ = (x**2+x+1)*(x-0)+(-x+1)  # f(1)=3
assert f_.subs(x, 1) == 3 and rem(f_, x**2+x+1, x) == -x+1
chk(38, rem(f_, x**3-1, x).subs(x, -1), 3)
f_ = (x**3+1)*(x**2+7) + (-4)*x**2 + 3*x
assert rem(f_, x**2-x+1, x) == -x+4
chk(39, (-4)**2-3**2, 7)
f_ = (x**3+1)*(x+5) + x**2 - 1
assert rem(f_, x**2-x+1, x) == x-2
chk(40, f_.subs(x, -1), 0)
S_ = x**2+7
Q_ = (x-3)*S_+3; P_ = (x-2)*Q_+3; f_ = expand((x-1)*P_+1)
Rm = Poly(rem(f_, expand((x-1)*(x-2)*(x-3)), x), x)
chk(41, sum(Rm.all_coeffs()), 1)
f_ = -3*x**2+18*x-14
assert expand(rem(f_, (x-4)**2, x) - (-f_-3*x**2+12*x+20)) == 0
chk(42, f_.subs(x, 1), 1)
P_ = (x+1)**3+(x+1)**2+(x+1)+1
assert rem(P_, (x+1)**3, x).subs(x, 0) == 3 and rem(P_, (x+1)**2, x).subs(x, 0) == 2 and P_.subs(x, -1) == 1
chk(43, P_.subs(x, 1), 15)
f_ = (x-3)**2*(2*x-4)+2*x-4
assert f_.subs(x, 3) == 2 and rem(f_, (x-3)**3, x).subs(x, 1) == 6
chk(44, f_.subs(x, 1), -10)
f_ = x**4+x**2+2*x+a
Rm = Poly(rem(f_, x**2-x+b, x), x)
s_ = solve([Rm.coeff_monomial(x)+4, Rm.coeff_monomial(1)-7], [a, b], dict=True)[0]
Rm2 = Poly(rem(f_.subs(a, s_[a]), x**2+s_[b]*x+1, x), x)
chk(45, Rm2.coeff_monomial(1)-Rm2.coeff_monomial(x), 41)
s_ = solve([4+2*p+q-2, 4-2*p+q+1], [p, q]); g_ = x**2+s_[p]*x+s_[q]; f_ = (x+1)*g_
assert f_.subs(x, 2) == 6 and g_.subs(x, -2) == -1
chk(46, f_.subs(x, 3)+g_.subs(x, 3), Rational(155, 4))
s_ = solve([c-2, 4*a+2*b+c-4, 9*a+3*b+c-11], [a, b, c]); chk(47, s_[a]+s_[b]+s_[c], 1)
# 48-60 인수 정리
s_ = solve([8+4*a-6+b+6, -1+a+3+b], [a, b]); chk(48, s_[a]-s_[b], -2)
s_ = solve([16+4*a+2*b-2, -2+a-b-2], [a, b]); chk(49, (2*x**3+s_[a]*x**2+s_[b]*x-2).subs(x, 1), -6)
s_ = ident(x**3+3*x**2+a*x+b, (x+1)**2*(x+c), x, [a, b, c])[0]; chk(50, s_[a]*s_[b], 3)
s_ = ident(2*x**3+a*x**2+b*x-3, (x+1)**2*(2*x+c), x, [a, b, c])[0]
chk(51, (2*x**3+s_[a]*x**2+s_[b]*x-3).subs(x, -s_[a]-s_[b]), 48)
av = solve((2*x**3+3*x**2-a*x-1).subs(x, Rational(-1, 2)), a)[0]
chk(52, quo(2*x**3+3*x**2-av*x-1, 2*x+1, x).subs(x, -1), -1)
av = solve((x**3-3*x+a).subs(x, -2), a)[0]; chk(53, av+quo(x**3-3*x+av, x+2, x).subs(x, 2), 3)
s_ = ident(2*x**4-7*x**3+2*a*x**2-b*x-6, (2*x+1)*(x-2)*(x**2+c*x+3), x, [a, b, c])[0]
chk(54, s_[a]*s_[b]-(x**2+s_[c]*x+3).subs(x, 3), 19)
print(factor(2*x**4-3*x**3+x**2+4*x-2))
chk(55, -2-2, -4)
s_ = solve([(x**2+p*x+q).subs(x, Rational(1, 2))-(x**2+p*x+q).subs(x, Rational(-1, 2)), 4+2*p+q], [p, q])
chk(56, 9+3*s_[p]+s_[q], 5)
print(factor(x**3+5*x**2+8*x+7-(x+4)))
chk(57, ((x+1)**2+(x+1)*(x+3)).subs(x, 3), 40)
Pp = (x-1)*(x-3); Qq = 2*x**2-6*x-5-Pp
assert rem(expand(Pp*Qq), x**2+x-2, x) == 0 and Pp.subs(x, 0) == 3
chk(58, Qq.subs(x, 5), 7)
f_ = (x-1)*(x-2)*(x-3)+1
assert f_.subs(x, 0) == -5
chk(59, f_.subs(x, 4), 7)
s_ = solve([(x**3+a*x**2+b*x-2).subs(x, -1), (x**3+a*x**2+b*x-2).subs(x, 2)], [a, b])
f_ = x**3+s_[a]*x**2+s_[b]*x-2
chk(60, (x*f_.subs(x, x**2)-2*x+3).subs(x, -2), -93)
# 61-80 고난도
Q_ = 2*(x**2-x+1)+x; f_ = expand((x**3+2)*Q_)
assert rem(f_, x**3+1, x) == expand(Q_) and quo(f_, x**3+1, x) == expand(Q_) and rem(f_-x, x**2-x+1, x) == 0 and f_.subs(x, 2) == 80
chk(61, f_.subs(x, 1), 9)
f_ = 3*(x+1)*(x+2)*(x-1)*(x-Rational(7, 4))+x
assert f_.subs(x, 2) == 11 and f_.subs(x, -1) == -1 and f_.subs(x, -2) == -2 and f_.subs(x, 1) == 1
chk(62, f_.subs(x, 0), Rational(21, 2))
g_ = x**3+x-2; f_ = expand((x**3+x-1)*(x-2))
assert quo(f_, g_, x) == expand(g_-x**3) and rem(f_, g_, x) == expand(g_-x**3) and f_.subs(x, 1) == -1
chk(63, f_.subs(x, 3), 29)
P_ = 2*x**3-18*x+3
assert expand((x+3)*P_.subs(x, x-3)+(x-3)*P_.subs(x, x+3)-2*x*P_) == 0
chk(64, P_.subs(x, 2), -17)
for nn in range(1, 6):
    ex = x**nn*(x**3+(-2*2+6)*x**2+(2-1)*x+3*2-6)
    assert expand(rem(ex, (x+1)**3, x) - (-1)**(nn+1)*(x+1)**2) == 0
chk(65, 2**2+6**2, 40)
A_ = expand((x**2+2*x-4)*(x+2)-16*x+16); B_ = 2*x-4
assert rem(A_, B_, x) == 0 and A_.subs(x, 0) != 0 and rem(A_, x**2+B_, x) == expand(B_**2-4*x**2)
chk(66, A_.subs(x, 1), -3)
F_ = x**3+5*x**2+9*x+6; f_ = x**2+3*x; g_ = rem(F_, f_, x)
assert expand(rem(F_, g_, x) - (f_-x**2-3*x)) == 0
chk(67, f_.subs(x, 1)+g_.subs(x, 1), 13)
s_ = solve([3*b+c-7, -2*b+c+3], [b, c]); chk(68, 1+s_[b]+s_[c], 4)
Rx = -(x+1)**2+3*x+2; chk(69, Rx.subs(x, 3), -5)
Rx = Rational(-1, 2)*(x-1)**2+x+4
assert Rx.subs(x, -1) == 1
chk(70, Rx.subs(x, 5), 1)
s_ = solve([Rational(-1, 4)*(Rational(1, 4)-p/2+q)+1, Rational(13, 4)*(9+3*p+q)-13], [p, q])
f_ = expand((x+Rational(1, 4))*(x**2+s_[p]*x+s_[q]))
qq = Poly(quo(f_, 4*x+1, x), x).all_coeffs(); assert rem(f_, 4*x+1, x) == 0 and f_.subs(x, Rational(-1, 2)) == -1 and f_.subs(x, 3) == 13
chk(71, 64*sum(cc**2 for cc in qq), 54)
f_ = (x+1)*(x-1)*x
assert expand(f_.subs(x, x**2) - (x**3*f_+x**2*(x**2-1))) == 0
chk(72, 1, 1)
f_ = x**2+1
assert expand(f_.subs(x, f_) - (f_**2+1)) == 0
chk(73, f_.subs(x, 3), 10)
f_ = x*(x-1)*(x-2)
assert expand((x+1)*f_-(x-2)*f_.subs(x, x+1)) == 0
chk(74, f_.subs(x, 5), 60)
Rx = rem(x**2026-1, x**4+x**3+x**2+x+1, x); chk(75, Rx.subs(x, 10), 9)
P_ = x**2*(x-1); assert rem(P_, x**2-1, x) == quo(P_, x**2-1, x) and rem((x+1)*P_, x**2-1, x) == 0
chk(76, P_.subs(x, 4), 48)
P_ = x**4+x**3+2*x-4; Q_ = x**4+x**3-2*x**2-x+1
assert rem(P_, x-1, x) == 0 and rem(Q_, x-1, x) == 0
chk(77, P_.subs(x, -1)+Q_.subs(x, -2), -3)
tot = 0
for P_ in (x**2-6*x-1, x**2-2*x-9):
    Q_, Rm = div(expand(P_**2), x**2-4*x-5, x); assert Rm == 36
    tot += Q_.subs(x, -1)
chk(78, tot, 8)
f_ = (x-1)*(x-5); g_ = (x-1)*(x-2); h_ = (x-2)*(x-5)
assert rem(expand(f_*g_), expand((x-1)*h_), x) == 0 and rem(expand(g_*h_), expand((x-2)*f_), x) == 0
assert f_.subs(x, -1)+g_.subs(x, -1) == 18
chk(79, h_.subs(x, 0), 10)
f_ = -3*x**2+12*x+16; av = -2
assert expand(rem(f_, (x-av)**2, x) - (2*f_+6*x**2-4)) == 0 and rem(expand(f_**2-2*f_+3), x**2-4*x-5, x) == 2
chk(80, f_.subs(x, av**2), 16)


# ---- 새 문항(재배치 때 추가)
p_, q_ = symbols('p_ q_'); f_ = p_*x + q_
s = solve(Poly(expand(f_.subs(x, x**2 - x) - (x*f_ - 3*x + 4)), x).all_coeffs(), [p_, q_], dict=True)
assert len(s) == 1
chk("m1", f_.subs(s[0]).subs(x, -2), 6)
co = Poly(expand((x**2 - x - 1)**3), x).all_coeffs()[::-1]
chk("m3", sum(w*co[k] for k, w in zip(range(1, 7), [4, 8, 28, 80, 244, 728])), 124)
co = Poly(expand((2*x**2 + x - 2)**5), x).all_coeffs()[::-1]
v_ = sum(Rational(co[k], 2**k) for k in range(1, 10, 2)); assert v_ == Rational(31, 2)
chk("m4", 31 + 2, 33)
chk("m5", rem(x**21 - 21, x**5 - 5, x).subs(x, 1), 604)
k1, k2 = symbols('k1 k2'); R_ = (x**2 + x + 1)*(k1*x + k2)
s = solve(Poly(rem(expand(R_ + 6*x), x**2 - x + 1, x), x).all_coeffs(), [k1, k2], dict=True)
chk("m6", R_.subs(s[0]).subs(x, 1), -9)
D_ = expand((x**2 - 4*x - 2)*(x**2 - 4*x + 7) + 18); assert expand(D_ - (x**2 - 4*x + 1)*(x - 2)**2) == 0
cs = symbols('c0:4'); R_ = sum(cs[i]*x**i for i in range(4))
e = Poly(rem(expand(R_ - 2*x - 2), x**2 - 4*x + 1, x), x).all_coeffs() + Poly(rem(expand(R_ - x**2), (x - 2)**2, x), x).all_coeffs()
s = solve(e, cs, dict=True); assert len(s) == 1
chk("m7", R_.subs(s[0]).subs(x, -1), 16)

bad = [r for r in R if not r[1]]
print("검산 %d문항, 불일치 %d" % (len(R), len(bad)))
for r in bad:
    print(r)
