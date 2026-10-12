# 8단원(이차부등식) 유형서 문항 정답 독립 검산 (문항 기호는 unit08.py의 v)
# 부등식은 sympy로 풀고, 매개변수는 정수·유리수 후보를 모두 대 본다.
from sympy import *
from itertools import product as iprod
import math
x, y, t = symbols('x y t', real=True)
a, b, c, k, m = symbols('a b c k m', real=True)
R = []
Rt = Rational


def chk(no, got, exp):
    R.append((no, simplify(sympify(got) - sympify(exp)) == 0, got, exp))


def chkmc(no, cond, lab):
    R.append((no, bool(cond), lab, lab))


def sol(e, v=x):
    return solve_univariate_inequality(e, v, relational=False)


def one(st):
    return st.is_FiniteSet and len(st) == 1


def ints(st, lo=-300, hi=300):
    return [n for n in range(lo, hi) if st.contains(n) == True]


def minmax(f, lo, hi):
    xs = [lo, hi] + [r for r in solve(diff(f, x), x) if lo <= r <= hi]
    v = [f.subs(x, z) for z in xs]
    return min(v), max(v)


# ---- 이차부등식의 풀이
s_ = sol(x**2 + 4*x - 5 <= 0); chk("n541", s_.inf**2 + s_.sup**2, 26)
chk("n961", sum(ints(sol(x**2 - 2*x - 8 < 0))), 5)
f = 2*(x + 1)**2; assert sol(f > 0) == Union(Interval.open(-oo, -1), Interval.open(-1, oo)) and f.subs(x, 1) == 8
chk("o40", sum(ints(sol(f <= 18))), -7)

# ---- 그래프와 이차부등식
chk("y72", sum(ints(sol((x + 3)*(x - 5) < 0))), 7)
f = x*(x - 4)/2; g = -x**2/2 + 3                       # 그림의 개형(교점 -1, 3)
assert set(solve(f - g, x)) == {-1, 3}
chk("y73", len(ints(sol(f - g <= 0))), 5)
f = (x + 2)*(x - 5); g = x - 2
chk("w1", len([n for n in ints(sol(f*g <= 0)) if n > 0]), 4)
res = []
for p in range(1, 40):
    fx = -x**2 + p*x + 2*p; A = (Rt(p, 2), fx.subs(x, Rt(p, 2))); gx = 2*p + (A[1] - 2*p)/A[0]*x
    if len(ints(sol(fx - gx > 0))) == 5:
        res.append(p)
chk("n471", min(res), 11)
f = (x + 2)*(x - 1); g = -(x - 2)**2
chk("o39", len(ints(sol(f.subs(x, 2*x) + 3*g - 9*x <= 0))), 10)

# ---- 해가 주어진 이차부등식
A_ = -1; B_, C_ = -A_, -2*A_
assert sol(A_*x**2 + B_*x + C_ > 0) == Interval.open(-1, 2)
s_ = sol(A_*x**2 + C_*x + 3*B_ < 0); chk("o16", s_.args[0].sup * s_.args[1].inf, -3)
s_ = solve([Poly(a*x**2 - x + b - a*(x + 2)*(x - Rt(3, 2)), x).coeffs()[i] for i in range(2)], [a, b], dict=True)[0]
assert s_[a] < 0 and sol(s_[a]*x**2 - x + s_[b] <= 0) == Union(Interval(-oo, -2), Interval(Rt(3, 2), oo))
chk("n157", s_[a] + s_[b], 4)
s_ = solve([a + 9 - 6, b + 3 - 8], [a, b])
chk("n310", len(ints(sol(s_[a]*x**2 + s_[b]*x + 2 >= 0))), 3)
res = [(av, bv) for av in range(1, 30) for bv in range(-30, 30) if sol(x**2 - av*x - av + 3 <= 0) == FiniteSet(bv)]
chk("n957", sum(res[0]), 3)
f = -(x + 5)*(x - 3); assert f.subs(x, 0) == 15
chk("y82", len(ints(sol(f.subs(x, x/2) > 0))), 15)
A_ = -1; B_, C_ = 2*A_, A_
assert sol(A_*x**2 + B_*x + C_ < 0) == Union(Interval.open(-oo, -1), Interval.open(-1, oo))
chkmc("n725", A_ < 0 and B_**2 - 4*A_*C_ <= 0 and sol(B_*x**2 + C_*x + A_ < 0) != EmptySet, "②")

# ---- 해를 가질 조건
good = [kv for kv in [Rt(i, 30) for i in range(-60, 30)] if sol(x**2 + (kv - 1)*x + kv**2 < 0) != EmptySet]
assert min(good) == Rt(-29, 30) and max(good) == Rt(9, 30) and Rt(1, 3) not in good
chk("n556", Rt(1, 3) - (-1), Rt(4, 3))
good = [av for av in [Rt(i, 4) for i in range(-40, 40)] if sol((av - 2)*x**2 + 2*av*x + 2*av + 3 > 0) == EmptySet]
chk("n598", max(good), -2)
res = [kv for kv in [Rt(i, 4) for i in range(-40, 40)] if one(sol(-3*x**2 + 8*kv*x + 3 - 8*kv >= 0))]
chk("n250", res[0] if len(res) == 1 else res, Rt(3, 4))
res = [(av, bv) for av in range(-10, 11) for bv in range(-10, 11)
       if all(one(sol(x**2 - 2*(kv - 1)*x + kv**2 - av*kv + bv - 1 <= 0)) for kv in range(-3, 4))]
chk("n164", res[0][0] - res[0][1] if len(res) == 1 else res, 0)

# ---- 해를 갖지 않을 조건
chk("o18", max(av for av in range(-30, 30) if sol(2*x**2 - 2*av*x + 3*av + 8 <= 0) == EmptySet), 7)
good = [kv for kv in [Rt(i, 4) for i in range(-20, 20)] if sol(x**2 + 2*(kv - 1)*x - kv**2 - kv + 4 < 0) == EmptySet]
chk("n315", max(good) + min(good), Rt(1, 2))

# ---- 모든 실수에서 성립
chk("o17", len([av for av in range(-30, 30) if sol(x**2 + 2*av*x - av + 6 >= 0) == S.Reals]), 6)
chk("n130", sum(kv for kv in range(-30, 30) if kv != 1 and sol((kv - 1)*x**2 + 2*(kv - 1)*x + 2 >= 0) == S.Reals), 5)
good = []
for av in range(-10, 15):
    d1 = expand((av - k)**2 - 4*(k**2 + 2*av))          # 모든 k에서 음수여야 함
    if sol(d1 < 0, k) == S.Reals:
        good.append(av)
chk("n209", len(good), 5)

# ---- 제한된 범위
good = [kv for kv in [Rt(i, 8) for i in range(-40, 60)]
        if all((z**2 - 4*z - 4*kv + 3) < 0 for z in [3 + Rt(j, 200) for j in range(0, 400)])]
chk("n462", min(good), 2)
good = [kv for kv in [Rt(i, 4) for i in range(-40, 40)] if minmax(-x**2 + 4*x + 3*kv - 4, 1, 5)[0] >= 0]
chk("n945", min(good), 3)
good = [av for av in [Rt(i, 4) for i in range(-60, 60)] if minmax(x**2 - av*x + av + 3, 0, 3)[0] >= 0]
chk("n728", max(good) + min(good), 3)

# ---- 근의 판별
chk("y104", len([av for av in range(-30, 30) if discriminant(x**2 - 2*av*x + av + 6, x) < 0]), 4)
res = []
for kv in range(1, 40):
    f = (x + 1)*(x - 2*kv)
    if not [r for r in solve(f - (x - 7*kv), x) if r.is_real]:
        res.append(kv)
chk("y106", sum(res), 10)

# ---- 두 이차함수와 이차부등식
res = set()
for av in [Rt(i, 2) for i in range(1, 10)]:
    bv = 4*av; f = av*x**2; g = -av*x**2 - bv*x + 2*bv
    assert sol(f + g >= 0) == Interval(-oo, 2) and solve(diff(f - g, x), x) == [-1]
    res.add(len(ints(sol(f - g <= 0))))
chk("n954", res.pop() if len(res) == 1 else res, 5)
g = -(x - 2)**2 + 3; f = expand(g + 2*(x + 3)*(x - 1))
assert sol(g >= 3) == FiniteSet(2) and sol(f < g) == Interval.open(-3, 1)
fmin = minimum(f, x); gmax = maximum(g, x)
res = [n for n in range(-50, 100) if len([kk for kk in range(-200, 200) if kk - n < fmin and kk > gmax]) == 8]
chk("n282", res[0] if len(res) == 1 else res, 35)

# ---- 활용
s_ = sol(x*(20 - x) - 96 >= 0).intersect(Interval.Ropen(10, 20)); chk("w5", s_.sup + s_.inf, 22)
s_ = sol((1000 + 10*x)*(400 - 2*x) - 448000 >= 0).intersect(Interval.open(0, 200)); chk("w6", 1000 + 10*s_.sup, 1600)
s_ = sol(40*t - 5*t**2 - 60 >= 0, t); chk("w7", s_.sup - s_.inf, 4)

# ---- 고난도
cnt = 0
for av, bv in iprod(range(1, 11), range(1, 11)):
    q = 2*x**2 + 4*av*x*y + 3*bv*y**2
    if all(sol(q.subs(y, yy) >= 0) == S.Reals for yy in (1, -1, 2)):
        cnt += 1
chk("n2512", cnt, 23)
vals = []
for kv in [Rt(i, 100) for i in range(-300, 500)]:
    e = x**2 - 2*(kv - 1)*x + 2*kv**2 - 4*kv - 2
    if discriminant(e, x) >= 0:
        vals.append(discriminant(e, x))          # (α-β)² = D
chk("o41", max(vals) + min(vals), 16)
res = []
for av in [r for r in solve(discriminant(x**2 + 2*a*x - 4*a, x), a) if r != 0]:
    bs = [bv for bv in range(-30, 30) if sol(av*x**2 + 4*x + 3*av + bv > 0) == EmptySet]
    res.append(av + max(bs))
chk("n980", max(res), 7)
aa = symbols("aa", positive=True)
f = aa*(x + 1)*(x - 3) + 4
av = solve(minimum(f, x) + 4, aa)[0]
chk("o57", f.subs({aa: av, x: 5}), 28)
# n913 ㄱㄴㄷ
s_ = solve([(a - 1)*2 - (a**2 + 2*a - 3), (a - k - 3) + 3*(a - 1)], [a, k], dict=True)
s_ = [d for d in s_ if d[a] - 1 < 0]
g1 = len(s_) == 1 and s_[0][a]*s_[0][k] == 10
g2 = not [av for av in range(-20, 21) if av != 1 and
          all(discriminant((av - 1)*x**2 + (av - kv)*x + 2*av - 3, x) >= 0 for kv in range(-30, 31))]
g3 = len([av for av in [Rt(i, 4) for i in range(-40, 40)] if av != 1 and
          one(sol((av - 1)*x**2 + 2*av - 3 <= 0))]) == 1
chkmc("n913", g1 and g2 and g3, "⑤")
cnt = 0
for av in range(-30, 60):
    st = sol(x**2 - 3*x - av < 0)
    if st != EmptySet and sum(ints(st)) == 9:
        cnt += 1
chk("n640", cnt, 6)
f = x**2 + 4*x - 12
gfun = lambda z: 2*(z*z + 4*z - 12) - abs(z*z + 4*z - 12)
ms = []
for mv in range(-60, 80):
    # a의 최솟값 = max(mx - g(x)) 를 촘촘한 점에서 근사, 정확한 경계는 두 이차식의 판별식
    ok1 = (mv - 4)**2 - 288 <= 0 or min(z*z + (4 - mv)*z + 72 for z in [i/50 for i in range(-1000, 1000)] if z <= -6 or z >= 2) >= 0
    ok2 = min(3*z*z + (12 - mv)*z + 48 for z in [i/50 for i in range(-299, 100)]) >= 0
    if ok1 and ok2:
        ms.append(mv)
chk("n495", sum(ms), 132)

# ---- 사용자 요청 추가
s_ = sol(x**2 - 2*x + 4 - (4*x - 1) >= 0); chk("y75", s_.args[1].inf - s_.args[0].sup, 4)
chk("w8", sum(av for av in range(-30, 30) if len(ints(sol(x**2 - (av + 4)*x + 4*av < 0))) == 3), 8)
gf = lambda z: ((z*z - 2*z - 8) + abs(z*z - 2*z - 8)) / 2
chk("w9", len([z for z in range(-100, 100) if gf(z) <= z + 2]), 8)
vals = []
for av in [Rt(i, 100) for i in range(1, 600)]:
    f = av*(x**2 - 4)
    if sol(expand(f - (4*x - 17)) >= 0) == S.Reals:
        vals.append(f.subs(x, 4))
chk("n817", max(vals) + min(vals), 51)
vals = [z**2 + (6*z - 2*z**2) for z in [Rt(i, 100) for i in range(-100, 400)] if 6*z - 2*z**2 >= 0]
chk("w10", max(vals) + min(vals), 9)

# ---- 사용자 요청 추가(모의고사 기출)
xs = solve(Eq(x + 1, 3), x) + solve(Eq(x + 1, 8), x)      # 교점 x=2, 7
f = -(x - 2)*(x - 7) + x + 1                                 # 위로 볼록한 대표 꼴(계수 -1)
chk("m1011", sum(ints(sol(f - x - 1 > 0))), 18)
ps = []
for pv in range(-40, 41):
    if pv == 0: continue
    fx = x**2 + pv*x + pv; A = (-Rt(pv, 2), fx.subs(x, -Rt(pv, 2))); gx = pv + (A[1] - pv)/A[0]*x
    if len(ints(sol(expand(fx - gx) <= 0))) == 10:
        ps.append(pv)
chk("m1509", max(ps) - min(ps), 38)
# m1803 ㄱㄴㄷ
st = sol(expand(x**2 - 9 - 2*0*(x - 3)) <= 0)
c1 = st == Interval(-oo, -3)
c2 = len([kv for kv in range(-30, 30) if sol(expand(x**2 - 9 - 2*kv*(x - 5)) <= 0) == EmptySet]) == 7
c3 = all(ints(sol(expand(x**2 - 9 - 2*kv*(x - av)) <= 0), -20, 20)
         for av in [Rt(i, 2) for i in range(-6, 7)] for kv in [Rt(j, 2) for j in range(-12, 13)])
chkmc("m1803", (not c1) and c2 and c3, "④")
# m1611 ㄱㄴㄷ: f>g가 항상 성립하는 (a,b) 표본에서 ㄱ, ㄴ, ㄷ 확인
ok = True
for av, bv in iprod([Rt(i, 2) for i in range(-6, 7)], [Rt(j, 2) for j in range(-20, 6)]):
    if sol(expand(x**2 - av*x + bv - (av*x + 2*bv)) > 0) == S.Reals:
        ok &= sol(x**2 - 2*av*x - bv > 0) == S.Reals and bv < 0 and (-av**2/4 + bv) > 2*bv
chkmc("m1611", ok, "⑤")
best = None
for kv in [Rt(i, 1000) for i in range(1, 4000)]:
    f = 2*(x - kv)*(x - 2*kv) + x; g = -(x - kv)**2 + x
    if sol(expand(f + g) >= 0) == S.Reals:
        best = kv
kk = symbols("kk", positive=True)
kmax = max(solve(kk**2 - 4*kk + 1, kk))
assert best <= kmax and kmax - best < Rt(1, 500)
chk("m2406", kmax, 2 + sqrt(3))
kr = sol(discriminant(k*x**2 - 8*x + 4*k - 8, x) >= 0, k)
chk("k1411", kr.sup - kr.inf, 2*sqrt(5))
good = [av for av in [Rt(i, 300) for i in range(1, 1500)] if av != 2 and
        abs(av**2 - 3*av + 3) + abs(2*av**2 - 4*av) <= 3]
chk("m2410", max(good) + min(good), Rt(10, 3))
vals = []
for kv in range(-20, 41):
    for al in range(1, 30):
        for be in range(1, 30):
            if al == be: continue
            f = Rt(1, 2)*(x - be)**2 + be                     # (가), (나)에서 꼭짓점 (β, β)
            if expand(f + x - kv).subs(x, al) == 0 and expand(f + x - kv).subs(x, be) == 0 \
               and f.subs(x, 0) <= al + be + f.subs(x, al):
                vals.append(f.subs(x, 6))
chk("m2506", prod(set(vals)), 45)

if __name__ == "__main__":
    bad = [r for r in R if not r[1]]
    print(len(R), "검산", "불일치", bad)
