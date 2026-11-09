# 공통수학2 10단원(합성함수와 역함수) 유형서 문항 정답 독립 검산 (문항 기호는 c2unit10.py의 v).
# 유한집합 문항은 모든 함수를 완전 탐색하고, 실수 범위 문항은 촘촘한 격자·sympy로 확인한다.
import itertools
import math
from fractions import Fraction as Fr
import numpy as np
import sympy as sp
R = []
P = itertools.permutations


def chk(no, got, exp):
    if isinstance(got, str):
        ok = got == exp
    else:
        e = float(sp.sympify(exp))
        ok = abs(float(got) - e) <= 1e-6 * max(1, abs(e))
    R.append((no, ok, got, exp))


def mark(truth, ch, names="ㄱㄴㄷㄹㅁ"):
    s = ", ".join(names[i] for i, v in enumerate(truth) if v)
    ch = ch.split("|")
    return "①②③④⑤"[ch.index(s)] if s in ch else "?"


def lin(a, b, n=400001):
    return np.linspace(a, b, n)


def nroots(h, a, b, n=4000001):
    x = lin(a, b, n); v = h(x); s = np.sign(v)
    return int(np.count_nonzero(s[:-1] * s[1:] < 0) + np.count_nonzero(np.abs(v) < 1e-12))


def bij_pw(fun, lo=-80, hi=80):
    v = fun(lin(lo, hi, 32001)); d = np.diff(v)
    return bool(np.all(d > 0) or np.all(d < 0))


def inv_dict(f):
    return {v: k for k, v in f.items()}


x = sp.symbols("x", real=True)

# 합성함수의 함숫값 ----------------------------------------------------
f = lambda t: 2 * t + 5; g = lambda t: t * t + 1
chk("k7-4", f(g(-1)) + g(f(-2)), 11)
f = lambda t: t + 3; g = lambda t: 5 * t - 4
chk("o10", g(f(2)) + f(f(2)), 29)
v = 2 * (lin(1, 4) - 1) ** 2 - 4 * (lin(1, 4) - 1) + 8
chk("o37", v.max() + v.min(), 20)
ks = [k for k in np.round(lin(-20, 20, 40001), 3) if abs((-(abs(k) - 4) ** 2 + 4 if abs(k) - 4 >= 0 else (abs(k) - 4) ** 2 + 4) - 3) < 1e-9]
chk("m0803-26", max(ks) - min(ks), 10)
S = 0
for a in [Fr(n, 2) for n in range(-40, 41)]:
    gg = lambda t: 2 * t - 6 if t < a else t * t
    if gg(1 + a) + gg(4) + a == 57:
        S += a
chk("m1911-28", 10 * S * S, 40)
res = set()
for a in range(-10, 11):
    for b in range(-10, 11):
        if all((a * t - 3 * a) ** 2 + 2 * (a * t - 3 * a) + b == t for t in (2, 3)):
            res.add(a + b)
chk("m2111-27", res.pop() if len(res) == 1 else -1, 4)
a, b = sp.symbols("a b")
eq = sp.Poly(sp.expand(a * (x ** 2 + 3) + b - 9 * (a * x + b) ** 2 - sp.Rational(1, 3)), x).coeffs()
sol = [s_ for s_ in sp.solve(eq, [a, b], dict=True) if s_[a] != 0 and s_[a].is_real and s_[b].is_real]
chk("k1-14", 40 * sol[0][a] + sol[0][b], "40/9")

# 합성함수와 치환 ------------------------------------------------------
chk("k3-20", 6 * Fr(5, 3) + 1, 11)                 # f(5/3)=3
chk("o14", 4 * 2 ** 2 - 4, 12)                      # h=2(g-1)=4x²-4
h = lambda t: t / 2 - 1
ok = all(abs(h(-(2 * t - 6) + 4) - (-t + 4)) < 1e-12 for t in (-3, 0, 1.5, 7))
chk("k11-8", "④" if ok else "?", "④")
xs = [t for t in [Fr(n, 4) for n in range(-40, 41)] if 2 * t - 4 == 2]
chk("k9-7", (-xs[0] + 5) / 4, "1/2")

# 교환법칙과 일차함수 --------------------------------------------------
ks = [k for k in range(-20, 21) if all(3 * (-t + k) + 2 == -(3 * t + 2) + k for t in (0, 1))]
chk("g1-18", ks[0], -2)
res = set()
for a in [Fr(n, 2) for n in range(-10, 11)]:
    if a == 0:
        continue
    for b in [Fr(n, 2) for n in range(-10, 11)]:
        ff = lambda t: a * t + b
        if ff(ff(0)) == -1 and ff(1) == -1:
            res.add(ff(-3))
chk("k3-9", res.pop() if len(res) == 1 else -1, 7)
ab = [(a, b) for a in range(-5, 6) for b in range(-10, 11) if a ** 3 == 8 and (a * a + a + 1) * b == 21]
a, b = ab[0]
xx = lin(-3, -1.5, 3000001); l1 = a * xx + b; l2 = a * a * xx + a * b + b
area = np.trapezoid(np.clip(np.minimum(0, l2) - l1, 0, None), xx)
chk("o35", area, "9/8")

# 반복합성 ------------------------------------------------------------
def itr(fd, t, n):
    for _ in range(n):
        t = fd[t]
    return t


F = {t: t * t % 7 for t in range(1, 7)}
chk("k7-15", itr(F, 2, 2025) + itr(F, 5, 1201), 8)
F = {0: 1, 1: 2, 2: 3, 3: 1}
chk("k11-18", itr(F, 1, 100) + itr(F, 0, 102), 5)
X3 = [1, 2, 3]; res = set()
for p in P(X3):
    fd = dict(zip(X3, p))
    if fd[1] == 3 and all(itr(fd, t, 3) == t for t in X3):
        gd = inv_dict(fd); res.add(itr(gd, 2, 10) + itr(gd, 3, 11))
chk("m0803-14", float(res.pop()), 5)
res = set()
for a in range(-6, 6):
    fd = {1: 1, 2: 4, 3: 3 + a, 4: 4 + a}
    if sorted(fd.values()) == [1, 2, 3, 4]:
        gd = inv_dict(fd); res.add(a + itr(gd, 2, 10) + itr(gd, 2, 11))
chk("m1511-19", float(res.pop()), 6)

# (f∘f)(x)=x와 일대일대응 ----------------------------------------------
X4 = [1, 2, 3, 4]; good = []
for p in P(X4):
    fd = dict(zip(X4, p))
    if all(fd[fd[t]] == t for t in X4) and any(fd[t] == 2 * t for t in X4):
        good.append(fd)
t1 = all(fd[3] == inv_dict(fd)[3] for fd in good)
t2 = all(fd[2] == 4 for fd in good if fd[1] == 3)
t3 = len(good) == 4
chk("m1603-20", mark([t1, t2, t3], "ㄱ|ㄴ|ㄱ, ㄴ|ㄱ, ㄷ|ㄱ, ㄴ, ㄷ"), "⑤")
X6 = range(1, 7)
chk("m1010-11", float(sum(1 for p in P(X6) if (lambda fd: fd[fd[1]] == 1 and fd[2] - fd[1] == 2)(dict(zip(X6, p))))), 36)
X5 = [1, 2, 3, 4, 5]
chk("k12-21", sum(1 for p in P(X5) if (lambda fd: all(fd[fd[t]] == t for t in X5) and any(fd[t] == t + 3 for t in X5))(dict(zip(X5, p)))), 7)
c = 0
for v_ in itertools.product(X5, repeat=5):
    if v_[0] < v_[1] < v_[2] and len(set(v_)) < 5:
        c += 1
chk("k4-23", c, 230)

# 합성함수의 방정식 ---------------------------------------------------
f164 = lambda t: np.abs(2 * t - 4)
g1 = f164(f164(1)) == 0
g2 = nroots(lambda t: f164(t) - t, 0, 4) == 2
pre = lambda c: {Fr(4 + sg * c, 2) for sg in (1, -1) if 0 <= Fr(4 + sg * c, 2) <= 4}   # |2x-4|=c인 x
ts = [t for t in [Fr(n, 3) for n in range(0, 13)] if abs(2 * t - 4) == t]          # f(t)=t
roots = set().union(*[pre(t) for t in ts])
g3 = sum(roots) == 8 and all(abs(2 * abs(2 * r_ - 4) - 4) == abs(2 * r_ - 4) for r_ in roots)
chk("m1706-20", mark([g1, g2, g3], "ㄱ|ㄱ, ㄴ|ㄱ, ㄷ|ㄴ, ㄷ|ㄱ, ㄴ, ㄷ"), "⑤")
ff = lambda t: t ** 2 - 2 * t - 4
chk("o38", sum(sp.solve(ff(ff(x)) - ff(x), x)), 4)


def roots_pw(fx, pieces):
    """조각별 다항식 f에 대하여 f(f(a))=f(a)의 실근 집합"""
    out = set()
    for cond_a, fa in pieces:
        for r in sp.solve(sp.Eq(fx(fa), fa), x):
            if r.is_real and cond_a(r):
                out.add(sp.nsimplify(r))
    return out


def mkf(br, l1, l2):
    return lambda t: sp.Piecewise((l1(t), t < br), (l2(t), True))


f206 = mkf(2, lambda t: 2 * t + 2, lambda t: t ** 2 - 7 * t + 16)
A = roots_pw(f206, [(lambda r: r < 2, 2 * x + 2), (lambda r: r >= 2, x ** 2 - 7 * x + 16)])
chk("m2111-28", sum(A), 6)
f118 = mkf(3, lambda t: 3 * t + 1, lambda t: t ** 2 - 8 * t + 18)
A = roots_pw(f118, [(lambda r: r < 3, 3 * x + 1), (lambda r: r >= 3, x ** 2 - 8 * x + 18)])
chk("k1-18", sum(A), "95/6")
cnt = 0
for a in range(-30, 31):
    rts = set()
    for r in sp.solve((x ** 2 + 2 * x + a - x) * (x ** 2 + 2 * x + a + x - 2), x):
        if r.is_real:
            rts.add(r)
    if len(rts) == 2:
        cnt += 1
chk("m1903-21a", cnt, 4)

# 역함수의 함숫값 ----------------------------------------------------
chk("k12-5", [t for t in range(-10, 11) if 3 * t - 5 == 4][0], 3)
chk("k6-5", 3 * 3 - 5, 4)
fi = lambda y: (2 - y) / 3; gi = lambda y: (y + 3) / 2
chk("o19", fi(-1) + gi(5), 5)                      # (f⁻¹∘g)⁻¹∘f⁻¹ = g⁻¹
fx = lambda t: (-3 * t - 2) / 2                    # g∘f=3x+5, g=-2x+3
gfun = lambda t: -2 * t + 3; gi = lambda y: (3 - y) / 2
chk("k8-19", gfun(fx(gi(2))), "13/2")
gi12 = [t for t in range(-30, 31) if -t + 1 == -12][0]
m_ = [r for r in sp.solve(x ** 2 - 2 * x + 5 - gi12, x) if r >= 1]
chk("k7-17", m_[0], 4)
chk("k5-18", 2 * 1 + 5, 7)
res = set()
for p in P(X5):
    fd = dict(zip(X5, p)); fid = inv_dict(fd)
    if fd[1] + 2 * fd[3] == 12 and fid[1] - fid[3] == 2:
        res.add(fd[4] + fid[4])
chk("m2203-14", float(res.pop()), 6)
t_ = [t for t in sp.solve(-2 * x ** 2 + 1 + 2, x)][0]
chk("m2311-15", t_ ** 2 + 1, "5/2")

# 역함수가 존재하기 위한 조건 ------------------------------------------
ok = [a for a in range(-30, 31) if bij_pw(lambda t: (a - 3) * t + (4 * a + 3) * np.abs(t - 2))]
chk("k4-14", ok[0] if len(ok) == 1 else -99, -1)
bs = [2 * a - 2 for a in np.round(lin(-3, 4, 7001), 4) if (a + 1) * (2 - a) > 0]
chk("k5-19", min(bs) + max(bs), -2)
ok = [a for a in np.round(lin(-8, 6, 1401), 2) if bij_pw(lambda t: np.where(t >= 0, (a + 4) * t + 3, 2 * (a - 2) * t + 3))]
chk("k11-9", "⑤" if (max(a for a in ok if a < 0) < -4 + 1e-9 and min(a for a in ok if a > -4) > 2 - 1e-9 and abs(max(a for a in ok if a < 0) + 4.01) < 1e-6) else "?", "⑤")
best = None
for a in range(-10, 11):
    for b in range(-20, 21):
        if bij_pw(lambda t: np.where(t < 2, a * (t - 2) ** 2 + b, -2 * t + 10), -40, 40):
            ok_range = abs(b - 6) < 1e-9
            if ok_range:
                best = a + b if best is None else min(best, a + b)
chk("m1806-14", best, 7)

# 역함수 구하기 -------------------------------------------------------
fA = lambda t: 3 * t - 2; gA = lambda y: (y + 2) / 3
cand = lambda y: gA(y) / 4 - 0.5
chk("k8-16", "①" if all(abs(cand(fA(4 * t + 2)) - t) < 1e-12 for t in (-2, 0, 1.3, 5)) else "?", "①")
fi = lambda y: y + 4; gi = lambda y: (3 - y) / 3
aa = fi(gi(1)) - fi(gi(0)); bb = fi(gi(0))
chk("k10-5", aa * bb, "-5/3")
f57 = lambda t: 2 * abs(t + 1) + abs(t - 3)
a_, b_, c_, d_ = -5, 8, Fr(1, 3), Fr(1, 3)
ok = all(abs(f57(y + a_) - y) < 1e-9 for y in (4, 5.5, 7.9)) and all(abs(f57(c_ * y + d_) - y) < 1e-9 for y in (8, 10, 31))
chk("o57", (a_ + b_ + c_ + d_) if ok else -99, "11/3")

# 역함수의 그래프와 교점 -----------------------------------------------
r = [t for t in sp.solve(5 * x - 2 - x, x)][0]
chk("k3-13", 2 * r, 1)
kk = [k for k in [Fr(n, 100) for n in range(0, 1000)]
      if len([t for t in sp.solve(x ** 2 / 3 - 2 * x + k - x, x) if t.is_real and t >= 3]) == 2]
chk("k8-9", max(kk) + Fr(1, 100) - min(kk), "3/4")   # 위끝은 열린 끝(27/4 제외) — 격자 한 칸 보정
kk = [k for k in [Fr(n, 80) for n in range(0, 160)]
      if len([t for t in sp.solve((x - k) ** 2 + 1 - x, x) if t.is_real and t >= k]) == 2]
chk("m1609-17", max(kk), 1)
xx = lin(-2, 12, 1400001); fv = np.where(xx < 4, 2 * xx + 2, xx / 4 + 9)
chk("k7-22", 2 * np.trapezoid(fv - xx, xx), 84)
xx = lin(-0.5, 5, 1100001); fv = np.where(xx <= 1, 3 * xx + 1, xx / 4 + 15 / 4)
chk("o46", 2 * np.trapezoid(fv - xx, xx), "33/2")

# 고난도 --------------------------------------------------------------
Xm = [-2, -1, 0, 1, 2]; res = set()
for p in P(Xm):
    fd = dict(zip(Xm, p)); fid = inv_dict(fd)
    if fd[fd[-1]] + fid[-2] == 4 and all(fd[k] * fd[k - 2] <= 0 for k in (0, 1)):
        res.add(6 * fd[0] + 5 * fd[1] + 2 * fd[2])
chk("m2211-27", res.pop() if len(res) == 1 else -1, 13)


def g208_ok(p, q, r_):
    """f=px²+qx+r_ (p>0)일 때 g가 실수 전체 일대일대응인가 (수치)"""
    xs_ = lin(-2, 1, 3001); fv_ = p * xs_ ** 2 + q * xs_ + r_
    d = np.diff(fv_)
    mono = np.all(d > 0) or np.all(d < 0)
    return mono and abs(min(fv_[0], fv_[-1]) + 3) < 1e-9 and abs(max(fv_[0], fv_[-1]) - 6) < 1e-9


# ㄱ: 조건을 만족시키는 여러 f에서 f(-2)+f(1)=3 / ㄴ: g(0)=-1, g(1)=-3 → 꼭짓점 5/2 / ㄷ: 꼭짓점 -2 → g(0)=1
samples = []
for p in [Fr(n, 4) for n in range(1, 13)]:
    for vtx in [Fr(n, 4) for n in range(-30, 31)]:
        for top in (True, False):
            # f(-2), f(1)이 (6,-3) 또는 (-3,6)인 이차함수 p(x-vtx)²+k
            f_m2 = 6 if top else -3
            k_ = f_m2 - p * (-2 - vtx) ** 2
            if abs(p * (1 - vtx) ** 2 + k_ - (-3 if top else 6)) < 1e-12 and g208_ok(float(p), float(-2 * p * vtx), float(p * vtx * vtx + k_)):
                samples.append((p, vtx, k_))
t1 = len(samples) > 0 and all(p * (-2 - v) ** 2 + k + p * (1 - v) ** 2 + k == 3 for p, v, k in samples)
pp, qq = sp.symbols("pp qq")
s2 = sp.solve([pp + qq - 1 + 3, 4 * pp - 2 * qq - 1 - 6], [pp, qq])
t2 = sp.Rational(-s2[qq], 2 * s2[pp]) == sp.Rational(5, 2)
t3 = sp.Integer(1) * ((0 + 2) ** 2 - 3) == 1
chk("m1903-21b", mark([t1, t2, t3], "ㄱ|ㄴ|ㄱ, ㄴ|ㄱ, ㄷ|ㄱ, ㄴ, ㄷ"), "⑤")
X7 = range(1, 8); res = set()
for p in P(X7):
    fd = dict(zip(X7, p)); fid = inv_dict(fd)
    if all(fd[fd[t]] + fid[t] == 2 * t for t in (1, 2, 6)) and fd[3] + fd[5] == 10 and fd[6] != 6:
        res.add(fd[4] * (fd[6] + fd[7]))
chk("m1811-30", res.pop() if len(res) == 1 else -1, 50)
res = set()
for p in P(X7):
    fd = dict(zip(X7, p))
    if all(fd[fd[t]] == fd[t] - 2 * t for t in (1, 2, 3)):
        res.add(fd[2] + fd[3] + fd[4])
chk("m1703-28", res.pop() if len(res) == 1 else -1, 17)
S9 = [n for n in range(1, 101) if n % 9 == 0]
cnt = sum(1 for r_ in range(1, 8) for Xs in itertools.combinations(S9, r_) if sorted(t % 7 for t in Xs) == list(range(7)))
chk("m1611-29", cnt, 16)
tot = 0
for a in range(-10, 11):
    if a == 0:
        continue
    gv = a * lin(-300, 300, 600001) ** 2 - 2 * a * lin(-300, 300, 600001) + abs(3 * a) - 9
    if np.all((gv <= -1 + 1e-12) | (gv >= 6 - 1e-12)):
        tot += a
chk("k3-16", tot, 24)
X9 = range(1, 10); res = set()
for p in P(X9):
    fd = dict(zip(X9, p))
    if fd[2] != 9 or not fd[4] < fd[6]:
        continue
    gd = inv_dict(fd)
    if len({fd[t] + gd[t] for t in X9}) == 1:
        res.add(fd[fd[8]] + gd[4])
chk("k12-22", res.pop() if len(res) == 1 else -1, 9)
Xk = [2, 3, 5, 7]; res = set()
for p in P(Xk):
    fd = dict(zip(Xk, p)); fid = inv_dict(fd)
    if fd[2] + fd[7] == fd[3] and fid[7] + fid[3] == 7:
        res.add(5 * fd[5] + fd[fd[3]])
chk("k6-15", res.pop() if len(res) == 1 else -1, 42)
pr = [2, 3, 5, 7, 11, 13, 17, 19]
chk("mj156", sum(1 for p in P(pr, 5) if sum(p[c - 1] - p[c + 2] == 10 for c in (1, 2)) == 1), 464)
c = 0
for v_ in itertools.product(range(1, 7), repeat=6):
    fd = dict(zip(range(1, 7), v_))
    if all(fd[fd[t]] == fd[t] for t in fd) and len(set(v_)) == 3 and all(v_.count(y) == 2 for y in set(v_)):
        c += 1
chk("mj153", c, 120)
c = 0
for v_ in itertools.product(X4, repeat=4):
    fd = dict(zip(X4, v_))
    if fd[4] == 3 and all(fd[a] <= fd[b] for a in X4 for b in X4 if fd[a] <= b):
        c += 1
chk("mj158", c, 8)

if __name__ == "__main__":
    bad = [r_ for r_ in R if not r_[1]]
    print("검산", len(R), "불일치", len(bad))
    for r_ in bad:
        print(r_)
