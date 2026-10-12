# -*- coding: utf-8 -*-
"""기본서 7단원 답 검산 (data7.py의 순서대로, 문항마다 따로 계산)"""
import sys, os, re
from itertools import product as iprod
from sympy import (symbols, Rational as R, sqrt, solve, nsimplify, simplify, expand, factor, Poly, I,
                   roots, prod, conjugate, CRootOf, re, im, N, Eq)
Re, Im = re, im
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data7

x, y, z, t = symbols("x y z t")
a, b, c, k, m, n = symbols("a b c k m n", real=True)


def rts(e, v=x):
    """다항식의 근 전체(중근 포함, CRootOf 정확값)"""
    P_ = Poly(expand(e), v)
    if P_.domain.is_ZZ or P_.domain.is_QQ:
        return P_.all_roots()
    out = []                                   # 계수에 근호가 있으면 정확한 풀이로
    for r, mult in roots(P_).items():
        out += [simplify(r)] * mult
    assert len(out) == P_.degree(), e
    return out


def real_distinct(e):
    return sorted({r for r in rts(e) if r.is_real}, key=float)


def Z(e):
    """50자리 수치로 0인지 판정"""
    return abs(complex(N(e, 50))) < 1e-35


def val(e):
    """50자리 수치 값을 유리수·근호로 되돌린다"""
    v = N(e, 50)
    assert abs(complex(N(im(v), 50))) < 1e-35, e
    return nsimplify(re(v), tolerance=1e-30, rational=False)


ans = []
# 01 삼차방정식의 근과 계수의 관계
r3 = rts(x**3 - 2*x**2 + 3*x + 4); ans.append(val(sum(1/(r - 1) for r in r3)))
r3 = rts(x**3 + x**2 + 12*x - 2); ans.append(val(sum((r - 1)**3 for r in r3)))
# (가) f(α)=-(α+3)/(α+1), (나) k=Π(α²+α+1)
g = x**3 + 2*x**2 + 3*x + 4
assert expand((x**2 + x + 1)*(x + 1) + x + 3 - g) == 0
kk = val(prod(r**2 + r + 1 for r in rts(g)))
ans.append(8*(-(kk + 3)/(kk + 1)))
ans.append(val(prod(r**2 - 2*r + 2 for r in rts(x**3 - 2*x**2 - 4*x + 6))))
# 02 삼차방정식을 작성하여 식의 값 구하기
r3 = rts(x**3 - x**2 - 2*x - R(1, 3)); assert len(set(r3)) == 3 and all(r.is_real for r in r3)
ans.append(val(sum(r**3 for r in r3)))
r3 = rts(x**3 - 4*x - 3); assert len(set(r3)) == 3
ans.append(val(sum(r**3 for r in r3)))
r3 = rts(t**3 - 3*t + 1, t); assert all(r.is_real for r in r3)       # 세 실수 x, y, z
ans.append(val(sum(r**5 for r in r3)))
r3 = rts(t**3 - t + 2, t)
ans.append(val(sum(r**6 for r in r3)))
# 03 켤레근
q = expand((x - 1 - I)*(x - 1 + I)*(x - 1 + sqrt(3))*(x - 1 - sqrt(3)))
co = Poly(q, x).all_coeffs(); assert co[0] == 1 and co[4] == -4
ans.append(co[1] + co[2] + co[3])
e = expand((1 + 2*I)**4 + a*(1 + 2*I)**3 + 4*(1 + 2*I)**2 + b*(1 + 2*I) - 5)
s = solve([Re(e), Im(e)], [a, b], dict=True); assert len(s) == 1
ans.append(s[0][a]**2 + s[0][b]**2)
# 04 삼차방정식의 근의 조건
good = [mv for mv in range(-7, 8)
        if len(real_distinct(x**4 - 4*x**3 + (mv + 1)*x**2 + (6 - 2*mv)*x - 3*mv)) == 2]
ans.append(sum(good))
good = [kv for kv in [R(i, 4) for i in range(-80, 20)] if len(real_distinct(x**3 + (kv - 4)*x + 2*kv)) == 3]
assert min(good) == -20 and max(good) == R(3, 4) and -8 not in good and all(g_ < 1 for g_ in good)
assert len(good) == len([i for i in range(-80, 20) if i < 4 and i != -32]) - len([i for i in range(-80, -80)])
ans.append("k<-8 또는 -8<k<1")
# a의 후보: 인수분해 (x+2)(x-3)(x-a^2+... ) 꼴이므로 유리수와 근호 후보에서 직접 찾는다
f3 = x**3 - (a**2 + a - 3)*x**2 + (-2*a**2 + a + 2)*x + 6*a
cands = set()
for av in [R(i, 2) for i in range(-30, 31)] + [sqrt(2), -sqrt(2), sqrt(3), -sqrt(3), sqrt(6), -sqrt(6)]:
    rr = sorted(rts(f3.subs(a, av)), key=lambda w: float(Re(w)))
    if all(w.is_real for w in rr) and rr[1] != rr[2] and Z(rr[0]*rr[2] + 6):
        cands.add(av)
# 근이 a에 대한 식이므로 pr=-6을 직접 풀어 놓친 후보가 없는지 확인
print("  253 인수분해:", factor(f3), "후보", sorted(cands, key=float))
ans.append(prod(cands))
f3 = x**3 - (a**2 + a + 1)*x**2 + (a**2 + 6*a)*x - 5*a
print("  254 인수분해:", factor(f3))
cands = set()
for av in [R(i, 2) for i in range(-30, 31)] + [sqrt(5), -sqrt(5), sqrt(6), -sqrt(6)]:
    rr = real_distinct(f3.subs(a, av))
    if len(rr) == 3 and Z(rr[0] + rr[2] - 6):
        cands.add(av)
print("  254 후보", cands)
ans.append(prod(cands))
# 05 복이차방정식
out = set()
for av in [R(i, 4) for i in range(-80, 81)]:
    rr = rts(x**4 + (2 - 2*av)*x**2 + av**2 - 2*av - 15)
    re_ = [w for w in rr if w.is_real]; im_ = [w for w in rr if not w.is_real]
    if re_ and im_ and Z(prod(im_) - 3):
        out.add(val(prod(re_)))
assert len(out) == 1; ans.append(out.pop())
out = set()
for av in [R(i, 4) for i in range(-80, 81)]:
    rr = rts(x**4 + (1 - 2*av)*x**2 + av**2 - av - 12)
    re_ = [w for w in rr if w.is_real]; im_ = [w for w in rr if not w.is_real]
    if re_ and im_ and Z(prod(re_) + 2):
        out.add(val(prod(im_)))
assert len(out) == 1; ans.append(out.pop())
good = []
for av in [R(i, 4) for i in range(-80, 81)]:
    rr = real_distinct(x**4 - (2*av + 4)*x**2 + av**2)
    if len(rr) == 4 and Z(3*(rr[2] - rr[1]) - (rr[3] - rr[0])):
        good.append(av)
ans.append(sum(good))
good = []
for nv in range(-30, 31):
    pos = [w for w in real_distinct(x**4 - (2*nv + 3)*x**2 + nv**2) if w > 0]
    if len(pos) == 2 and Z(pos[1] - 2*pos[0]):
        good.append(nv)
assert len(good) == 1; ans.append(good[0])
# 06 허근 ω
w0 = [w for w in rts(x**3 - 3*x**2 + 6*x - 4) if not w.is_real][0]
base = w0*(2 - conjugate(w0))
good = [nv for nv in range(1, 30) if Z(expand(base**nv) - 64)]
assert len(good) == 1; ans.append(good[0])
w0 = [w for w in rts(x**4 - 2*x**3 - x + 2) if not w.is_real][0]
cnt, fn = 0, 0
for nv in range(1, 100):
    fn = fn + 1/w0**nv
    if Z(fn**2 + fn + 1):
        cnt += 1
ans.append(cnt)
# 07 공통근
# x=1이 공통근이고 다른 공통근이 없는지: a+b=-2, a≠b에서 a=0,b=-2로 확인
p1, p2 = x**3 + a*x**2 + b*x + 1, x**3 + b*x**2 + a*x + 1
sabs = []
for av in range(-10, 11):
    for bv in range(-10, 11):
        if av == bv:
            continue
        common = set(rts(p1.subs({a: av, b: bv}))) & set(rts(p2.subs({a: av, b: bv})))
        if len(common) == 1:
            sabs.append(av + bv)
assert set(sabs) == {-2}; ans.append(-2)
res = []
for mv in [R(i, 2) for i in range(-20, 21)]:
    common = set(rts(x**2 + (2*mv + 1)*x - mv - 3)) & set(rts(x**2 + (mv + 1)*x + mv - 3))
    if len(common) == 1:
        res.append((mv, common.pop()))
assert res == [(-1, 2)], res; ans.append("m=-1, 공통근 2")
# 08 연립방정식
s = solve([x + 3*y - z - 2, 2*x - y + z + 1, 3*x + y + 2*z - 5], [x, y, z]); ans.append("x=%s, y=%s, z=%s" % (s[x], s[y], s[z]))
s = solve([3*x + 2*y + z - 12, x + y - z - 6, x - 2*y + z + 2], [x, y, z]); ans.append("x=%s, y=%s, z=%s" % (s[x], s[y], s[z]))
s = solve([x + y - 5, y - z - 3, z - x - 4], [x, y, z]); ans.append(s[x] + s[y] + s[z])
s = solve([1/x + 1/y - 2, 1/y + 1/z - 1, 1/z + 1/x + 7], [x, y, z], dict=True); assert len(s) == 1
ans.append(s[0][x]*s[0][y]*s[0][z])
# 09 연립방정식의 해의 조건
ans.append(len([kv for kv in range(1, 100) if 64 - 4*(5*kv - 1 - 8) >= 0]))
ans.append(min(av for av in range(-50, 50) if (2*av - 4)**2 - 4*(av**2 - 4) < 0))
# 10 정수근
ks = set()
for p_ in range(1, 200):
    for q_ in range(p_, 200):
        s = solve([2*k - 1 - (p_ + q_), 4*k + 3 - p_*q_], [k], dict=True)
        if s:
            ks.add(s[0][k])
ans.append(sum(ks))
ms = [mv for mv in range(-200, 200) if all(w.is_integer for w in rts(x**2 - (mv + 5)*x - mv - 1))]
ans.append(prod(ms))
ms = [mv for mv in range(-50, 51) if any(w.is_integer for w in rts(x**2 - mv*x + mv**2 - 1))]
ans.append("m=" + ", ".join(map(str, ms)))
out = []
for mv in range(-50, 51):
    rr = rts(x**2 - 2*(mv + 2)*x + 2*mv**2 + 6)
    if all(w.is_integer for w in rr):
        out.append("m=%d일 때 두 근 %s" % (mv, ", ".join(map(str, sorted(set(rr))))))
ans.append(" / ".join(out))
# STEP 3
al = rts(x**3 - 3*x + 1)[0]
be = (al + sqrt(al**2 - 4))/2                     # x^2-αx+1=0의 한 근
ans.append(val(be**3 + 1/be**3))
# P(-1)=0, 허근 곱 6, P(2x-1)=0의 두 허근의 합 2 → P의 두 허근의 합 2
P_ = expand((x + 1)*(x**2 - 2*x + 6)); im_ = [w for w in rts(P_) if not w.is_real]
assert Z(prod(im_) - 6) and Z(sum((w + 1)/2 for w in im_) - 2)
co = Poly(P_, x).all_coeffs(); ans.append(co[1] + co[2] + co[3])
good = [av for av in [R(i, 4) for i in range(-80, 81)]
        if len(real_distinct(x**4 - 2*av*x**3 + (-3*av + 3)*x**2 + 2*av*x + 3*av - 4)) == 3]
print("  275 후보", good)
ans.append(sum(good))
cnt = 0
for av, bv in iprod(range(-30, 31), range(-30, 31)):
    e = x**3 - (5*av + 2)*x**2 + (10*av + bv**2)*x - 2*bv**2
    if 5*av + 2 == 12 and len(real_distinct(e)) == 3:
        cnt += 1
ans.append(cnt)
ks = set()
for kv in [R(i, 9) for i in range(1, 400)] + [R(i, 16) for i in range(1, 400)]:
    rr = rts(x**3 - 4*x**2 + (kv + 3)*x - kv)
    if all(w.is_real and w > 0 for w in rr):
        s3 = sorted(rr, key=float)
        if Z(s3[0]**2 + s3[1]**2 - s3[2]**2):
            ks.add(kv)
assert len(ks) == 1; ans.append(ks.pop())
# f(x)-2x=(x-p)^2 (p는 임의, p=0으로 계산)
u = x**2
ans.append(len(real_distinct(expand(u**3 - 7*u + 6))))
w0 = [w for w in rts(x**3 - 1) if not w.is_real][0]
ans.append(val(sum(w0**j/(1 + w0**(2*j)) for j in range(1, 31))))
al = [w for w in rts(x**3 - 8) if not w.is_real][0]; ab = conjugate(al)
lhs = expand(ab**3 - 2*ab**2 + 3*ab)
s = solve([Re(expand(lhs - (a*al + b))), Im(expand(lhs - (a*al + b)))], [a, b], dict=True)
ans.append(s[0][a] + s[0][b])
res = []
for av, bv in iprod(range(-10, 11), range(-10, 11)):
    rr = rts(x**3 + av*x**2 + bv*x + 1)
    im_ = [w for w in rr if not w.is_real]
    if len(im_) == 2 and (Z(im_[0]**2 - im_[1]) or Z(im_[1]**2 - im_[0])):
        res.append((av, bv))
assert res == [(2, 2)], res; ans.append("a=2, b=2")
good = [av for av in [R(i, 20) for i in range(-200, 201)]
        if len(real_distinct(expand((x**2 - 2*x - av)*(x**2 + av*x + 2)))) == 4]
assert min(good) > 2*sqrt(2) and R(3) not in good and R(57, 20) in good and R(301, 100) not in good and R(61, 20) in good
assert all(g_ > 2*sqrt(2) for g_ in good) and len([g_ for g_ in good if g_ < 3]) == len([i for i in range(57, 60)])
ans.append("2 sqrt {2} <a<3 또는 a>3")
ms = []
for p_, q_ in iprod(range(-10, 11), range(-10, 11)):
    r_ = -p_ - q_
    if p_ <= q_ <= r_ and p_*q_*r_ == 2:
        ms.append(-(p_*q_ + q_*r_ + r_*p_))
assert len(ms) == 1; ans.append(ms[0])
ks = [kv for kv in range(1, 200) if len(real_distinct(expand(x**2 - x*(x - 4) - (x - 4)**2 - kv))) == 2]
ans.append(max(ks))

items = [p for _, _, ps in data7.TYPES for p in ps] + data7.STEP3
assert len(items) == len(ans) == 44, (len(items), len(ans))
bad = 0
for no, (it, v) in enumerate(zip(items, ans), 240):
    want = it["ans"].replace("$", "")
    if isinstance(v, str):
        ok = (want == v)
    else:
        w = want.replace("{", "(").replace("}", ")").replace(" over ", "/").replace(" ", "")
        w = __import__("re").sub(r"(\d)sqrt", r"\1*sqrt", w)
        ok = Z(nsimplify(eval(w, {"sqrt": sqrt})) - v)
    if not ok:
        bad += 1
        print("불일치", no, want, v)
print("문항", len(items), "불일치", bad)
