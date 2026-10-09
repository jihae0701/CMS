# 2단원(나머지정리) 보충 문항 정답 독립 검산 (문항 기호 c번호 = 후보 번호)
from sympy import *
x, a, b, c, k, p, q, r = symbols('x a b c k p q r')
R = []


def chk(no, got, exp):
    R.append((no, simplify(sympify(got) - sympify(exp)) == 0, got, exp))


# c2: f(x-2)=x^2+(a-4)x+3, f(3)=6
f = x**2 + a*x + b
s = solve(Poly(expand(f.subs(x, x - 2) - (x**2 + (a - 4)*x + 3)), x).all_coeffs() + [f.subs(x, 3) - 6], [a, b], dict=True)
assert len(s) == 1
chk("c2", f.subs(s[0]).subs(x, 5), Rational(106, 5))
# c3
f = x**3 + p*x**2 + q*x + 8
s = solve([f.subs(x, 3) - 5, f.subs(x, -2) - 0], [p, q], dict=True); f = f.subs(s[0])
g_r = 2*x + 3; f_r = x + 2
R1 = rem(expand(f_r**2 + g_r**2), x**2 - x - 6, x); R2 = rem(expand(f_r*g_r), x**2 - x - 6, x)
kk = expand(R1 - R2 - 12*f_r); assert kk.is_number
chk("c3", f.subs(x, kk), 3)
# c4: P(6x) mod 6x^2-5x+1=(2x-1)(3x-1): P(3)=13, P(2)=7
s = solve([a/2 + b - 13, a/3 + b - 7], [a, b])
chk("c4", s[a] - s[b], 41)
# c5: f odd, monic cubic, f(-1)=0
f = x**3 + p*x**2 + q*x + r
s = solve(Poly(expand(f + f.subs(x, -x)), x).all_coeffs() + [f.subs(x, -1)], [p, q, r], dict=True)
assert len(s) == 1
chk("c5", rem(f.subs(s[0]), x**2 - 4, x).subs(x, 5), 15)
# c6: 임의의 P에 대해 Q1(-1)+Q2(-1)=2 (두 예로 확인)
for P_ in [(x - 1)*(x + 3)*(x**2 + 5) + x, (x - 1)*(x + 3)*(2*x - 7) + x]:
    assert P_.subs(x, 1) == 1 and P_.subs(x, -3) == -3
    v = quo(P_ - 1, x - 1, x).subs(x, -1) + quo(P_ + 3, x + 3, x).subs(x, -1)
    assert v == 2
chk("c6", v, 2)
# c15: x=0, 1 대입 -> P(0)^2+P(1)^2=0, P(1)^2+P(2)^2=0 이므로 P(0)=P(1)=P(2)=0 (실계수)
P_ = 2*x*(x - 1)*(x - 2)
assert all(e.subs(x, t) == 0 for t in (0, 1) for e in [P_**2 + P_.subs(x, x + 1)**2])
Q_ = cancel((P_**2 + P_.subs(x, x + 1)**2)/(x*(x - 1)))
chk("c15", rem(Q_, P_, x).subs(x, 3), 216)
# c16
f = x**2 + x + 4; assert (f - 4).subs(x, -1) == 0 and f.subs(x, 0) == 4
chk("c16", quo(expand(f.subs(x, x**18)), x**6 - 1, x).subs(x, 1), 9)
# c18
P_ = x**7 + a*x**2 + b*x + c
s = solve(Poly(rem(P_, x**2 - x + 1, x), x).all_coeffs() + [a + b + c + 3], [a, b, c], dict=True)
assert len(s) == 1
chk("c18", P_.subs(s[0]).subs(x, 2), 120)
# c19~c22 정수 계산
chk("c19", (2026*2027*2028*2029 - 48) % (2026**2 + 3*2024 - 1), 15)
chk("c20", (2026**5 - 2026**3 + 1) % 2024, 25)
chk("c21", 10**12 % 10001, 10000)
chk("c22", sum(7**i for i in range(101)) % 6, 5)
# c26: 정수 범위 전수조사
sols = []
for A_ in range(-12, 13):
    for B_ in range(-12, 13):
        if A_ == 2 or B_ == -2 or A_ == B_:
            continue
        for K in range(-40, 41):
            P_ = expand((x - A_)*(x - B_)*(x - K) - 2*x + 3)
            if P_.subs(x, 2) == P_.subs(x, A_) and P_.subs(x, -2) == P_.subs(x, B_):
                sols.append(P_)
assert len(set(sols)) == 1
chk("c26", sols[0].subs(x, 3), 21)
# c30
f = x**3 + p*x**2 + q*x + r
s = solve([f.subs(x, 1) - 1, f.subs(x, 2) - 2, f.subs(x, 3) + 1], [p, q, r], dict=True)
chk("c30", f.subs(s[0]).subs(x, Rational(1, 2) - 1), Rational(-169, 8))
# c31: f=x^2+px+q, xf-g=(x-1)r (몫=나머지=상수 r)
f = x**2 + p*x + q; g = x*f - (x - 1)*r
s = solve([(f*g + x - 1).subs(x, 1), f.subs(x, 2) - 3, g.subs(x, 3) - 2], [p, q, r], dict=True)
assert len(s) == 1
chk("c31", (f + g).subs(s[0]).subs(x, 4), 42)
# c32: f=(x-1)(x-2)(px+q), f(0)=4, f'(0)=0
f = (x - 1)*(x - 2)*(p*x + q)
s = solve([f.subs(x, 0) - 4, diff(f, x).subs(x, 0)], [p, q], dict=True)
assert len(s) == 1
chk("c32", f.subs(s[0]).subs(x, -1), -6)
# c13: R=(x^2+x+1)(px+q), R를 x^2-x+1로 나눈 나머지 -6x, 예시 f로 다시 확인
Rx = (x**2 + x + 1)*(p*x + q)
s = solve(Poly(rem(expand(Rx), x**2 - x + 1, x) + 6*x, x).all_coeffs(), [p, q], dict=True)
assert len(s) == 1
Rx = expand(Rx.subs(s[0]))
f = expand((x**4 + x**2 + 1)*(x**3 - 2*x + 5) + Rx)
assert rem(f, x**2 + x + 1, x) == 0 and expand(rem(f, x**2 - x + 1, x) + 6*x) == 0
chk("c13", rem(f, x**4 + x**2 + 1, x).subs(x, 1), -9)
# c17: n=1~6 모두 나머지 계수 비교로 a, b가 같은지
sols = set()
for n in range(1, 7):
    rr = rem(expand(x**n*(x**2 - a*x + b)), (x - 2)**2, x) + 2**(n + 1)*(x - 2)
    s = solve(Poly(expand(rr), x).all_coeffs(), [a, b], dict=True)
    assert len(s) == 1
    sols.add((s[0][a], s[0][b]))
assert len(sols) == 1
chk("c17", sum(sols.pop()), 14)
# c33: 예시 f로 두 나머지 조건을 만족하는지 확인한 뒤 R(2)
Rx = -(x + 2)**2 + 2*x + 5
f = expand((x + 2)**2*(x - 3)*(x**2 + 7) + Rx)
assert expand(rem(f, (x + 2)**2, x) - (2*x + 5)) == 0 and f.subs(x, 3) == -14
chk("c33", rem(f, expand((x + 2)**2*(x - 3)), x).subs(x, 2), -7)

bad = [t for t in R if not t[1]]
print("검산 %d문항, 불일치 %d" % (len(R), len(bad)))
for t in bad:
    print(t)
