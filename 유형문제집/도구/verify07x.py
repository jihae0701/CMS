# 공통수학1 7단원 교체 후보 4문항 검산 (unit07x.py)
import sympy as sp
from fractions import Fraction as F
R = []
x, t, A = sp.symbols("x t a")


def chk(no, got, exp):
    R.append((no, sp.simplify(sp.sympify(got) - sp.sympify(exp)) == 0, got, exp))


def has_real(a, f):
    # x+y=..., xy=... 꼴: t^2-st+p=0 의 판별식
    return f(a) >= 0


# r390a: x+y=2a, (x+2)(y+2)=a^2+3a+12 를 직접 풀어 실수해 여부
def real_sol(sys_eqs, a):
    X, Y = sp.symbols("X Y")
    sols = sp.solve([e.subs({x: X}).subs(A, a) for e in sys_eqs], [X, Y], dict=True)
    return any(all(v.is_real for v in s.values()) for s in sols)


X, Y = sp.symbols("X Y")
ok = [a for a in range(-20, 30) if any(all(sp.im(v) == 0 for v in s.values())
       for s in sp.solve([X + Y - 2 * a, (X + 2) * (Y + 2) - (a * a + 3 * a + 12)], [X, Y], dict=True))]
chk("r390a", min(ok), 8)
ok = [a for a in range(-20, 30) if any(all(sp.im(v) == 0 for v in s.values())
       for s in sp.solve([X + Y - a, X ** 2 + Y ** 2 - (2 * a + 6)], [X, Y], dict=True))]
chk("r390b", len(ok), 9)


def real_roots(poly):
    rs = sp.Poly(poly, x, domain="QQ").real_roots()
    return sorted({round(float(r), 6) for r in rs})


# r371a: 계수 a를 넓게 훑어 실근이 {-2, 2}뿐인 경우의 a+b+c (b=-8, c=-4a는 x=±2 대입으로 강제됨)
vals = set()
for a in [sp.Rational(k, 4) for k in range(-80, 81)]:
    b, c = -8, -4 * a
    p = x ** 4 + a * x ** 3 + b * x ** 2 + c * x + 16
    if real_roots(p) == [-2.0, 2.0]:
        vals.add(a + b + c)
chk("r371a", vals.pop() if len(vals) == 1 else None, -8)
# r371b: 정수 a, b, c 전수(실근 1, 2를 가지려면 f(1)=f(2)=0 → a, c는 b로 정해짐)
best = None
for a in range(-40, 41):
    for b in range(-60, 61):
        # f(1)=0: 1+a+b+c+4=0 → c=-5-a-b ; f(2)=0 확인
        c = -5 - a - b
        if 16 + 8 * a + 4 * b + 2 * c + 4 != 0:
            continue
        p = x ** 4 + a * x ** 3 + b * x ** 2 + c * x + 4
        if real_roots(p) == [1.0, 2.0]:
            best = b if best is None else max(best, b)
chk("r371b", best, 13)

if __name__ == "__main__":
    bad = [r for r in R if not r[1]]
    print("검산", len(R), "불일치", len(bad))
    for r in bad:
        print(r)
