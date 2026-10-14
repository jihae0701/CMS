# 9단원(연립부등식) 유형서 문항 정답 독립 검산 (문항 기호는 unit09.py의 v)
# 부등식은 유리수 격자·정수 전수로 직접 확인하고, 매개변수는 후보를 모두 대 본다.
from fractions import Fraction as F
import math
R = []


def chk(no, got, exp):
    R.append((no, got == exp, got, exp))


def chkmc(no, cond, lab):
    R.append((no, bool(cond), lab, lab))


def ints(cond, lo=-300, hi=300):
    return [x for x in range(lo, hi) if cond(x)]


G = [F(i, 16) for i in range(-800, 801)]       # -50 ~ 50, 1/16 간격


def ends(cond, grid=G):
    S = [x for x in grid if cond(x)]
    return (min(S), max(S)) if S else None


# ---- 연립일차부등식의 풀이
chk("n1", sum(ints(lambda x: 2*x < x + 3 and 3*x + 2 >= x + 4)), 3)
chk("n112", len(ints(lambda x: x - 3 < 3*x - 1 < 2*x + 3)), 4)
chk("o12", len(ints(lambda x: -x - 22 < 5*x - 4 <= 2*x + 23)), 12)
# ---- 해가 주어진 연립일차부등식
ab = [(a, b) for a in range(-15, 16) for b in range(-15, 16)
      if ints(lambda x: -2*x >= x + a and 4*x - 3 >= 3*(x - b)) == [-3]
      and not [z for z in G if -2*z >= z + a and 4*z - 3 >= 3*(z - b) and z != -3]]
chk("n831", ab[0][0] * ab[0][1] if len(ab) == 1 else None, 18)
chk("n524", max(a for a in range(-50, 50) if not [z for z in G if 2*z - 3 <= -z + 6 <= 3*z + a]), -7)
ab = [(a, b) for a in range(-20, 21) for b in range(-20, 21)
      if ends(lambda z: 6*z - a > 4*z + 1 and 5*z + 6 < 3*z + b) == (-1 + F(1, 16), 2 - F(1, 16))]
chk("o33", ab[0][0] + ab[0][1] if len(ab) == 1 else None, 7)
chk("o34", min(a for a in range(-50, 50) if [z for z in G if 5*z - 2 >= 8 and 4*z + 1 > 6*z - a]), 4)
ok = [a for a in [F(i, 16) for i in range(-160, 161)] if len(ints(lambda x: a*x - 1 <= 4*x - 3 < -x + 15, -2000, 2000)) == 2]
chk("n547", max(ok), 3)
# ---- 연립일차부등식의 활용
best = 0
for b in range(1, 200):
    a = 4*b + 11
    if 5*(b - 3) + 1 <= a <= 5*(b - 3) + 5:
        best = max(best, a + b)
chk("o54", best, 136)
chk("n558", sum(x for x in range(1, 100) if 7*(x - 1) + 1 <= 5*x + 12 <= 7*(x - 1) + 6), 24)
# ---- 절댓값 기호가 하나인 부등식
f = lambda n: len(ints(lambda x: abs(2*x + 6) <= 8*n - 6, -1000, 1000))
chk("n252", f(7) + f(8), 110)
e = ends(lambda z: abs(3*z - 1) < z + 3); chk("n400", e[0] - F(1, 16) + e[1] + F(1, 16), F(3, 2))
chk("n549", len([k for k in range(-20, 60) if len(ints(lambda x: x >= 1 and abs(2*x - 8) <= k - 3)) == 7]), 2)
bad = [z for z in G if not (2*abs(z - 2) - 1 < 3*abs(2*z + 1))]
chk("n276", min(bad) + max(bad), F(-3, 2))      # 해가 아닌 구간 [a, b]의 양 끝
# ---- 절댓값 기호가 두 개인 부등식
e = ends(lambda z: abs(z + 2) + abs(z - 4) <= 8); chk("o14", e[0] + e[1], 2)
bad = [z for z in G if not (3*abs(z + 2) + abs(z - 4) >= 10)]
chk("n8", (max(bad) + F(1, 16)) - (min(bad) - F(1, 16)), 3)
e = ends(lambda z: abs(3*z) < abs(z - 8)); chk("n575", e[0] - F(1, 16) + e[1] + F(1, 16), -2)
nm = [(n, max(ints(lambda x: abs(x - 1) + abs(x - n) < n + 5))) for n in range(1, 60)
      if len(ints(lambda x: abs(x - 1) + abs(x - n) < n + 5)) == 15]
chk("n729", nm[0][0] + nm[0][1] if len(nm) == 1 else None, 24)
A = [F(i, 300) for i in range(1, 1500) if i != 600]
okA = [a for a in A if abs(a*a - 3*a + 3) + abs(2*a*a - 4*a) <= 3]
chk("m2410", min(okA) + max(okA), F(10, 3))
# ---- 절댓값 기호를 포함한 부등식과 이차부등식
e = ends(lambda z: abs(z + 1) + abs(z - 2) <= 5)        # [-2, 3] -> a(x+2)(x-3), (b+c)/a
chk("o38", -(e[0] + e[1]) + e[0] * e[1], -7)        # a(x-r1)(x-r2): b/a=-(r1+r2), c/a=r1r2
e = ends(lambda z: abs(z) + abs(z - 2) <= 4); chk("n768", (e[0] + e[1]) / 2, 1)
# ---- 연립이차부등식의 풀이
chk("o19", len(ints(lambda x: x*x + 2*x - 3 <= 0 and 2*x*x - 3*x - 5 < 0)), 2)
chk("n222", len(ints(lambda x: x*x - 2*x - 8 <= 0 and x*x - 6*x + 9 > 0)), 6)
S = [z for z in G if 2*z*z + z - 2 <= z*z + 3*z + 6 <= -2*z]; chk("n570", S[0] if len(S) == 1 else None, -2)
ok = [a for a in range(-20, 30) if [z for z in G if 2*z*z + 1 <= 3*z < -z*z + a] == [z for z in G if F(1, 2) <= z < 1]]
chk("n880", ok[0] if len(ok) == 1 else None, 4)
# ---- 해가 주어진 연립이차부등식
ab = [(a, b) for a in range(-20, 21) for b in range(-20, 21)
      if [z for z in G if z*z + 4*z + a > 0 and z*z + b*z - 8 <= 0] == [z for z in G if 1 < z <= 4]]
chk("o42", ab[0][0] + ab[0][1] if len(ab) == 1 else None, -7)
chk("n207", max(a for a in range(-30, 30)
                if [z for z in G if z*z - 3*z - 10 < 0 and z*z - (a + 1)*z + 2*a - 2 > 0] == [z for z in G if 2 < z < 5]), -1)
r = [(a, b) for a in range(-10, 0) for b in range(-10, 10)
     if [z for z in G if z*z - 2*a*z < 0 and z*z - (a + 2)*z + 2*a > 0] == [z for z in G if b*b - 15 < z < b]]
chk("n769", r[0][0] + r[0][1] if len(r) == 1 else None, -6)
ok = [a for a in [F(i, 8) for i in range(-80, 200)]
      if [z for z in G if z*z - 4*z - 12 <= 0 and z*z + (1 - a)*z - a > 0] == [z for z in G if -2 <= z < -1]]
chk("n636", min(ok), 6)
# ---- 정수인 해의 개수
ok = [a for a in [F(i, 16) for i in range(33, 400)] if len(ints(lambda x: x*x - 10*x - 24 < 0 and (x - 2)*(x - a) >= 0)) == 9]
chk("o20", max(ok), 7)
chk("n281", sum(a for a in range(-40, 40) if len(ints(lambda x: x*x - x - 12 < 0 and (x - 2*a)*(x - a - 2) <= 0)) == 2), -2)
ok = [a for a in [F(i, 16) for i in range(-400, 400)] if len(ints(lambda x: 2*x*x - 3*x - 14 <= 0 and (x + a)*(x - 1) > 0)) == 2]
chk("n167", min(ok), 2)
ok = [a for a in [F(i, 16) for i in range(-400, 400)] if len(ints(lambda x: x*x - 7*x - 8 < 0 and (x - 1)*(x - a) >= 0)) == 5]
chk("n294", max(ok), 5)
# ---- 절댓값 기호를 포함한 연립부등식
ks = [k for k in range(-40, 40) if sum(ints(lambda x: abs(x - k) <= 6 and x*x - x - 12 > 0)) == 9]
chk("n292", ks[0] if len(ks) == 1 else None, 1)
ok = [k for k in [F(i, 16) for i in range(1, 400)] if len(ints(lambda x: x*x - 5*x - 6 < 0 and abs(2*x - 4) >= k)) == 3]
chk("o46", max(ok), 4)
chk("m3343", sum(a for a in range(1, 60) if len(ints(lambda x: abs(x - a) <= 2 and x*x + (a*a - 5)*x - 5*a*a <= 0, -4000, 4000)) == 5), 6)
chk("n929", sum(n for n in range(1, 100) if len(ints(lambda x: abs(x - 1) <= n and x*x - 4*x - 12 > 0)) <= 4), 21)
# ---- 해가 존재할 조건
chk("n597", sum(k for k in range(-30, 30) if not [z for z in G if z*z - 4*z - 12 > 0 and z*z - 2*k*z + k*k - 4 <= 0]), 10)
chk("o44", len([a for a in range(-30, 30) if not [z for z in G if 5*z*z - (4*a + 3)*z + 2*a*a + 4*a <= 3*z*z + z < 4*z*z - 12]]), 6)
ok = [a for a in [F(i, 64) for i in range(-320, 320)] if [z for z in G if z*z - 6*z + 8 <= 0 and a*z + 1 >= 0]]
chk("n79", min(ok), F(-1, 2))
# ---- 항상 성립하는 연립부등식
X = [F(i, 8) for i in range(-400, 401)]
ok = [a for a in [F(i, 4) for i in range(-40, 120)] if all(2*z + 1 <= 2*z + a <= z*z - 2*z + 24 for z in X)]
chk("m3253", min(ok) + max(ok), 21)
# g(x) <= -5x+9가 모든 x에서 성립하려면 일차항 계수가 같아야 하므로 a+2=-5 (a=-6이면 x가 클 때 성립하지 않음)
assert not all(-z*z - 4*z + 3 <= -4*z + 5 <= -5*z + 9 for z in X)
bs = [b for b in [F(i, 16) for i in range(-160, 320)] if all(-z*z - 4*z + 3 <= -5*z + b <= -5*z + 9 for z in X)]
chk("n42", -7 + (max(bs) - min(bs)), F(-5, 4))
Xr = [F(i, 64) for i in range(-128, 65)]
chk("w7", max(z*z + z + 3 for z in Xr) - min(-z*z + z + 3 for z in Xr), 8)
# ---- 연립이차부등식의 활용
chk("w5", sum(x for x in range(1, 14) if 14 - x > x and x*(14 - x) >= 40), 15)
ok = [z for z in [F(i, 64) for i in range(1, 640)] if z + (z + 1) > z + 2 and (z + 2)**2 > z*z + (z + 1)**2]
chk("w6", min(ok) - F(1, 64) + max(ok) + F(1, 64), 4)
xs = []
for m in range(-300, 300):
    z = F(m + 1, 3)
    v = z*z - z
    if m - F(1, 2) <= v < m + F(1, 2):
        xs.append(z)
chk("w8", sum(xs), 4)
# ---- 근의 부호·근의 분리 (실근을 직접 구함)


def roots(a, b, c):
    d = b*b - 4*a*c
    if d < 0:
        return None
    return sorted([(-b - math.sqrt(d)) / (2*a), (-b + math.sqrt(d)) / (2*a)])


ok = [a for a in [F(i, 8) for i in range(-200, 200)] if (r := roots(1, 2*(a - 1), a + 5)) and r[1] < 0]
chk("w2", min(ok), 4)
chk("w3", len([a for a in range(-30, 30) if (r := roots(1, -4, a*a - 2*a - 8)) and r[0] < 0 < r[1]]), 5)
chk("w9", len([a for a in range(1, 11) if (r := roots(1, -2*(a - 3), a + 3)) and r[0] > 0]), 5)
chk("w10", len([a for a in range(-30, 30) if (r := roots(1, a*a - 4*a - 5, a - 3)) and r[0] < 0 < r[1] and r[1] > -r[0]]), 3)
chk("w4", len([a for a in range(-50, 50) if (r := roots(1, -2*a, a + 12)) and r[0] != r[1] and r[0] > 1]), 8)
ok = [m for m in [F(i, 96) for i in range(-300, 300)] if (r := roots(1, m - 3, m)) and 0 < r[0] and r[1] < 2]
chk("w11", min(ok) - F(1, 96) + max(ok), F(5, 3))
# ---- 고난도
d = [z for z in [F(i, 40) for i in range(-400, 400)] if abs(z) + abs(z - 1) <= 5]     # a=0, b=1 (d=1, c=1/2)
pq = max(d) - F(1, 2)                       # q/p
chk("n87", pq.numerator * pq.denominator, 10)
chk("o58", len([a for a in range(1, 11) if ints(lambda x: x*x - 10*x + 21 > 0 and abs(x - a) < 1)]), 5)
nn = [n for n in range(3, 60) if len(ints(lambda x: (x - F(1, n))**2 > F(1, n)**2 and abs(x - F(1, n)) <= n)) == 21]
chk("n88", nn[0] if len(nn) == 1 else None, 11)
chk("n842", len(ints(lambda x: (x + 3)*abs(x - 1) <= 3*abs(x + 1) and 2*abs(F(x) - F(3, 2)) < -x*x - x + 15)), 4)
# o55: a, b 결정 후 복소수 계산(제곱근은 주치로)
e = ends(lambda z: abs(z - 4) <= 5)
import cmath
a_, b_ = 4, -1
z = (cmath.sqrt(a_) / cmath.sqrt(b_)) * cmath.sqrt(b_ / a_) + cmath.sqrt(a_ * b_) / (cmath.sqrt(-a_) * cmath.sqrt(b_))
val = (z - 1)**10 + 1j * z**10
chk("o55", (e == (-1, 9)) and round(val.real) == 31 and abs(val.imag) < 1e-9 and 31, 31)
ok = [p for p in [F(i, 400) for i in range(101, 800)]
      if sum(1 for x in (1, 2, 3) if x*x - (4*p - 1)*x >= 0 and x*x - (p*p + p + 2)*x + p**3 + 2*p < 0) >= 2]
chk("n106", 48 * F(1, 4) * max(ok) if min(ok) == F(101, 400) else None, 6)
cnt = sum(1 for a in range(-60, 61) for b in range(-60, 61)
          if abs(a*b) <= 30 and len(ints(lambda x: x*x - 2*a*x + a*a - 1 <= 0 and x*x - 2*b*x + b*b - 4 > 0, -100, 100)) == 2)
chk("n628", cnt, 24)
# m3247: (a, b)를 격자로 훑어 해가 x<p 꼴인 경우를 모아 ㄱ, ㄴ, ㄷ 확인
Z = [F(i, 8) for i in range(-160, 161)]


def sol_left(a, b):
    S = [z for z in Z if a*z*z + (a + b)*z + a + b + 1 < 0 and (a + b)*z*z + (a + b + 1)*z + a < 0]
    if not S or S[0] != Z[0]:
        return None
    p = S[-1]
    return p if S == [z for z in Z if z <= p] else None


cases = [(a, b, sol_left(a, b)) for a in [F(i, 4) for i in range(-16, 17)] for b in [F(i, 4) for i in range(-16, 17)]]
cases = [c for c in cases if c[2] is not None and c[2] < Z[-1] - 1]
g1 = all(abs(p - (-1 - F(1, 8))) <= F(1, 8) for a, b, p in cases if a == -1) and any(a == -1 for a, b, p in cases)
g2 = all(b > 0 for a, b, p in cases)
g3 = all(a**3 <= -1 for a, b, p in cases)
chkmc("m3247", g1 and g2 and not g3, "②")

if __name__ == "__main__":
    bad = [r for r in R if not r[1]]
    for r in bad:
        print("불일치", r)
    print("검산", len(R), "불일치", len(bad))
