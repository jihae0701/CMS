# 공통수학2 8단원(절대부등식) 유형서 문항 정답 독립 검산 (문항 기호는 c2unit08.py의 v).
# 최댓값·최솟값은 조건을 매개변수로 풀어 넣은 촘촘한 격자로, 보기는 무작위 실수 20만 쌍과 반례로, 증명 빈칸은 sympy 항등식으로 확인한다.
import math
import numpy as np
import sympy as sp
R = []
rng = np.random.default_rng(7)
sq = np.sqrt


def chk(no, got, exp):
    if isinstance(got, str):            # ①~⑤ 같은 기호 답
        ok = got == exp
    else:
        e = float(sp.sympify(exp))
        ok = abs(float(got) - e) <= 1e-3 * max(1, abs(e))
    R.append((no, ok, got, exp))


def lin(a, b, n=400001):
    return np.linspace(a, b, n)


def mark(truth, ch="ㄱ|ㄴ|ㄷ|ㄴ, ㄷ|ㄱ, ㄴ, ㄷ", names="ㄱㄴㄷㄹㅁ"):
    s = ", ".join(names[i] for i, v in enumerate(truth) if v)
    ch = ch.split("|")
    return "①②③④⑤"[ch.index(s)] if s in ch else "?"


def always(f, pos=False, n=200000):
    lo = 1e-3 if pos else -10
    a, b, c = rng.uniform(lo, 10, (3, n))
    return bool(np.all(f(a, b, c)))


E = 1e-9
a_, b_, c_, p_, q_, x_, y_ = sp.symbols("a b c p q x y", real=True)

# 절대부등식의 뜻 ----------------------------------------------------
chk("g1-1", mark([always(lambda a, b, c: abs(a) + abs(b) > 0) and (abs(0) + abs(0) > 0),
                  always(lambda a, b, c: a * a - a + 1 > 0), always(lambda a, b, c: a * a + b * b >= a * b - E)]), "④")
xs = np.append(rng.uniform(-10, 10, 200000), [0, -2, -1, 1])
ys = np.append(rng.uniform(-10, 10, 200000), [0, 0, 0, 0])
tr = [np.all(xs - 1 > xs), np.all(xs**2 - 2 > xs), np.all(abs(xs + 2) > 0), np.all(xs**2 + 3 * ys**2 >= 2 * xs * ys - E), np.all(abs(xs + 1) > abs(xs - 1))]
chk("k5-7", "①②③④⑤"[tr.index(True)] if sum(tr) == 1 else "?", "④")
chk("s1291", mark([always(lambda a, b, c: a * a + 1 > a), always(lambda a, b, c: a * b >= a * a + b * b - E),
                   always(lambda a, b, c: (a + b)**2 >= 4 * a * b - E)], "ㄱ|ㄴ|ㄱ, ㄷ|ㄴ, ㄷ|ㄱ, ㄴ, ㄷ"), "③")

# 실수의 성질을 이용한 증명 ------------------------------------------
A, B = rng.uniform(-9, 9, (2, 200000))
g = (abs(A) + abs(B))**2 - abs(A + B)**2
ok = np.allclose(g, 2 * (abs(A * B) - A * B)) and np.all(abs(A * B) >= A * B) and np.all((abs(abs(A) + abs(B) - abs(A + B)) < 1e-9) == (A * B >= 0))
chk("g2-1", "②" if ok else "?", "②")
e1 = sp.expand((a_ * p_ + b_ * q_)**2 - (a_**2 * p_ + b_**2 * q_) - (a_**2 * p_ * (p_ - 1) + b_**2 * q_ * (q_ - 1) + 2 * a_ * b_ * p_ * q_))
e2 = sp.expand((a_**2 * p_ * (p_ - 1) + b_**2 * q_ * (q_ - 1) + 2 * a_ * b_ * p_ * q_).subs(q_, 1 - p_) - (a_ - b_)**2 * p_ * (p_ - 1))
P = rng.uniform(0, 1, 100000)
chk("m1109-17", "⑤" if e1 == 0 and e2 == 0 and np.all(P * (P - 1) <= 0) else "?", "⑤")
chk("s1298", mark([always(lambda a, b, c: abs(a + b) > abs(a - b)), always(lambda a, b, c: abs(a) + abs(b) >= abs(a - b) - E),
                   always(lambda a, b, c: abs(a - b) >= abs(a) - abs(b) - E)]), "④")
A2, B2 = rng.uniform(0, 10, (2, 200000))
big, small = np.maximum(A2, B2) + 1e-6, np.minimum(A2, B2)
cnt = sum([bool(np.all(sq(big) + sq(small) > sq(2 * (big + small)))), bool(np.all(sq(big - small) > sq(big) - sq(small))),
           always(lambda a, b, c: abs(a - b) <= abs(a) + abs(b) + E), always(lambda a, b, c: abs(a) - abs(b) <= abs(a - b) + E),
           always(lambda a, b, c: abs(abs(a) - abs(b)) <= abs(a - b) + E)])
chk("o57", cnt, 4)

# 여러 가지 절대부등식의 증명 ----------------------------------------
X, Y = sp.symbols("x y")
k = sp.Symbol("k")
sol = sp.solve(sp.Poly(sp.expand(5 * (X**2 + Y**2) - (X + 2 * Y)**2 - (4 * X**2 + Y**2 - k * X * Y)), X, Y).coeffs(), k)
assert sol == [4] or sol == {k: 4}, sol
assert sp.expand(5 * (X**2 + Y**2) - (X + 2 * Y)**2 - (2 * X - Y)**2) == 0
chk("k4-16", 4 + 2, 6)                     # (가)=4, 등호 y=2x → 1:2
A3, B3 = rng.uniform(1e-3, 3, (2, 300000))
tr = [np.all(A3**3 + B3**3 >= -A3 * B3 * (A3 + B3)), np.all(A3**3 + B3**3 >= -0.5 * A3 * B3 * (A3 + B3)), np.all(A3**3 + B3**3 >= A3 + B3),
      np.all(A3**3 + B3**3 >= 0.5 * A3 * B3 * (A3 + B3)), np.all(A3**3 + B3**3 >= A3 * B3 * (A3 + B3) - E)]
chk("연송고", "①②③④⑤"[tr.index(False)] if tr.count(False) == 1 else "?", "③")
chk("s1295", mark([always(lambda a, b, c: b / a + a / b >= 2), always(lambda a, b, c: a * a - 3 * a * b + 4 * b * b < 0),
                   always(lambda a, b, c: 3 * (a * a + b * b + c * c) >= (a + b + c)**2 - E)], "ㄱ|ㄷ|ㄱ, ㄷ|ㄴ, ㄷ|ㄱ, ㄴ, ㄷ"), "②")
Xa, Xb, Xc = rng.uniform(1e-3, 10, (3, 200000))
ok = (sp.expand((a_ + b_)**2 - 4 * a_ * b_ - (a_ - b_)**2) == 0
      and np.all(4 * Xa * Xb / (Xa + Xb) * Xc + 4 * Xb * Xc / (Xb + Xc) * Xa + 4 * Xc * Xa / (Xc + Xa) * Xb <= 2 * (Xa * Xb + Xb * Xc + Xc * Xa) + 1e-9)
      and np.all(3 * (Xa * Xb + Xb * Xc + Xc * Xa) <= (Xa + Xb + Xc)**2 + 1e-9))
chk("m0911-15", "②" if ok else "?", "②")

# 산술·기하평균, 코시 증명 --------------------------------------------
# s1299: |c| = |a x1 + b y1| 이므로 (가) |ax1+by1|/√(a²+b²), 제곱하면 ≥, 등호 OP ⊥ l ⟺ (x1, y1) ∥ (a, b) ⟺ a y1 = b x1
a0, b0, x1, y1 = rng.normal(size=(4, 100000))
lhs = (a0**2 + b0**2) * (x1**2 + y1**2); rhs = (a0 * x1 + b0 * y1)**2
chk("s1299", "②" if np.all(lhs >= rhs - 1e-9) and np.allclose(lhs - rhs, (a0 * y1 - b0 * x1)**2) else "?", "②")
G = np.meshgrid(lin(1e-3, 6, 3001), lin(1e-3, 6, 3001))
v = (G[0] + 1 / G[1]) * (G[1] + 4 / G[0])
chk("m0909-13", "⑤" if abs(v.min() - 9) < 1e-2 else "?", "⑤")   # 등호 조건 ab=1, ab=4는 산술·기하의 등호에서 바로
v = (2 * G[0] + G[1]) * (2 / G[0] + 1 / G[1])
chk("g2-7", 4 + round(v.min(), 3), 13)

# 합 또는 곱이 일정 ---------------------------------------------------
x = lin(1e-6, 4 - 1e-6); amax = (x * (4 - x)).max()
x = lin(1e-3, 30); bmin = (3 * x + 4 * 3 / x).min()
chk("g1-3", amax + bmin, 16)
r = np.exp(lin(-8, 8)); chk("k7-10", ((1 + r) * (1 + 9 / r)).min(), 16)
th = lin(0.001, 2 * math.pi - 0.001, 2000001); ab = 6 * np.cos(th) * np.sin(th)
ab = ab[(np.abs(np.cos(th)) > 1e-6) & (np.abs(np.sin(th)) > 1e-6)]
chk("s1303", ab.max() * ab.min(), -9)
x = lin(1e-6, 6 - 1e-6); y = (12 - 2 * x) / 3; i = (x * y).argmax()
chk("s1304", (x * y)[i] + x[i] + y[i], 11)

# 식의 전개 -----------------------------------------------------------
chk("g1-5", ((1 + r) * (1 + 4 / r)).min(), 9)            # a=1, b=r 꼴(동차)
t = np.exp(lin(-8, 8)); v = (t + 3 + 3 + 9 / t)          # ab=t
chk("s1308", v.min() + t[v.argmin()], 15)
b = lin(1e-4, 20); a = b + 3; v = (a + 2 / b) * (b + 8 / a); i = v.argmin()
chk("s1310", v[i] + a[i] + b[i], 23)
a = lin(1e-3, 20); chk("o42", ((a + 1 / a) * (a + 2 + 1 / a)).min(), 8)
chk("m1509-16", ((4 * G[0] + 1 / G[1]) * (1 / G[0] + 16 * G[1])).min(), 36)

# 식의 변형 -----------------------------------------------------------
a = lin(3.0001, 60); chk("고림고", ((a * a + 2 * a - 11) / (a - 3)).min(), 12)
x = lin(1.0001, 40); v = x + 4 / (x - 1); chk("o21", v.min() + x[v.argmin()], 8)
x = lin(2.0001, 40); v = x - 3 + 4 / (x - 2); chk("k10-6", v.min() + x[v.argmin()], 7)
x = lin(5.0001, 60); chk("s1317", ((x * x - 5 * x + 9) / (x - 5)).min(), 11)
x = lin(1e-4, 60); chk("s1318", (2 * x / (x * x + 7 * x + 4)).max(), "2/11")
x = lin(3.0001, 30); chk("m1209-26", (x * x + 49 / (x * x - 9)).min(), 23)

# 조건식 --------------------------------------------------------------
a = lin(1e-5, 0.8 - 1e-5); b = (4 - 5 * a) / 3; chk("g2-8", (5 / a + 3 / b).min(), 16)
a = lin(1e-4, 4 - 1e-4); b = (a - 4) / 3; chk("k3-22", (3 / a - 1 / b).min(), 3)   # a>0, b<0만 가능
b = lin(1e-5, 2.5 - 1e-5); a = 5 - 2 * b; chk("s1300", (1 / a + 1 / (2 * b)).min(), "4/5")

# 활용 ---------------------------------------------------------------
a = lin(4.0001, 60); b = a / (a - 4); chk("k4-19", (1 / (a - 4) + 1 / (b - 1)).min(), 1)
a = lin(0.01, 64); chk("m2111-14", (a * a + (32 / a)**2).min(), 64)
m = lin(1e-3, 30); chk("m1806-17", ((2 * m + 3)**2 / (2 * m)).min(), 12)
a = lin(0.05, 60); chk("m1911-16", sq(a * a + (18 / a)**2 + 36).min(), "6*sqrt(2)")

# 코시 ---------------------------------------------------------------
th = lin(0, 2 * math.pi, 2000001); a, b = sq(5) * np.cos(th), sq(5) * np.sin(th)
chk("g1-8", (a + 2 * b).max() - (a + 2 * b).min(), 10)
u = rng.normal(size=(800000, 3)); u /= np.linalg.norm(u, axis=1)[:, None]; u *= sq(12)
chk("s1327", (u[:, 0] - u[:, 1] + 2 * u[:, 2]).min(), "-6*sqrt(2)")
x = lin(-40, 40); y = (5 / 2 - x / 3) * 4; chk("s1329", (x * x + y * y).min(), 36)
chk("s1330", (a * a + 2 * a + b * b + b).max(), 10)
a = lin(0, 6); chk("g2-13", (sq(a) + sq(3 * (6 - a))).max(), "2*sqrt(6)")
x = lin(0, 1); chk("s1328", (sq(2 * x) + sq(3 * (1 - x))).max(), "sqrt(5)")
x = lin(0, 8 / 3); y = (8 - 3 * x) / 2; chk("s1305", (sq(3 * x) + sq(2 * y)).max(), 4)
zs = lin(-5, 5, 2000001); ok = 2 * (3 - zs**2) >= (1 - zs)**2 - 1e-12
chk("s1331", zs[ok].max() + zs[ok].min(), "2/3")
u = rng.normal(size=(800000, 3)); u /= np.linalg.norm(u, axis=1)[:, None]; u *= 4
chk("g2-19", (sq(2) * u[:, 0] + sq(3) * u[:, 1] + 2 * u[:, 2]).max(), 12)
#   (2x²+3y²+z²=16에서 X=√2x, Y=√3y, Z=z로 두면 2x+3y+2z=√2X+√3Y+2Z, X²+Y²+Z²=16)
th = lin(1e-6, math.pi / 2 - 1e-6); chk("g2-17", (sq(50) * (np.cos(th) + np.sin(th))).max() + 8, 18)
pts = rng.uniform(0, 3, (1500000, 2)); px, py = pts[:, 0], pts[:, 1]   # B 원점, A(0,2), C(3,0)
inside = 2 * px + 3 * py < 6
d_ab, d_bc = px[inside], py[inside]; d_ca = (6 - 2 * px[inside] - 3 * py[inside]) / sq(13)
chk("s1334", (d_ab**2 + d_bc**2 + d_ca**2).min(), "18/13")

# s1393: P(2cosθ, 2sinθ), M·N 중점, AN·BM 최댓값
th = lin(1e-6, math.pi - 1e-6)
Px, Py = 2 * np.cos(th), 2 * np.sin(th)
Mx, My = (Px - 2) / 2, Py / 2; Nx, Ny = (Px + 2) / 2, Py / 2
chk("s1393", (np.hypot(Nx + 2, Ny) * np.hypot(Mx - 2, My)).max(), 10)
r = np.exp(lin(-10, 10)); chk("s1394", ((1 + sq(r)) / sq(1 + r)).max(), "sqrt(2)")

# 고난도 --------------------------------------------------------------
G2 = np.meshgrid(lin(1e-2, 10, 2001), lin(1e-2, 10, 2001))
chk("m2011-16", (0.5 / G2[0] * (G2[1] + G2[0]**2 / G2[1])).min(), 1)
a = lin(1e-3, 10); chk("m1511-14", ((3 * a + 1 / a) / 2).min(), "sqrt(3)")
th = lin(0, math.pi, 2000001); a, b = np.cos(th), np.sin(th); m_ = np.abs(a * b) > 1e-6
chk("g3-15", ((9 * a * a + 30 * a * b + 25 * b * b) / (a * a + b * b))[m_].max(), 34)
y = lin(1e-6, 4 / sq(5) - 1e-6); x = 2 * sq(5) * (1 - y * sq(5) / 4); chk("o59", (x * y).max(), 2)
best = 1e9
for _ in range(30):
    pa, pb = rng.uniform(0, 8, (2, 300000))                        # B 원점, A(0,8), C(6,0): a=AB까지=x, b=BC까지=y
    ins = 4 * pa + 3 * pb < 24
    da, db = pa[ins], pb[ins]; dc = (24 - 4 * da - 3 * db) / 5
    best = min(best, (4 / da + 3 / db + 5 / dc).min())
chk("g3-17", best, 6)
X3 = np.exp(rng.uniform(-4, 4, (3, 400000)))
chk("g2-20", ((X3[0] + X3[1]) * (X3[1] + X3[2]) * (X3[2] + X3[0]) / X3.prod(0)).min(), 8)
n = 6
import itertools
lhs_ok = all(sum(ak / (i + 1)**2 for i, ak in enumerate(perm)) >= sum(1 / (i + 1) for i in range(n)) - 1e-12
             for perm in itertools.permutations(range(1, n + 1)))
chk("g3-20", "②" if lhs_ok else "?", "②")
xs_ = np.round(lin(-10, 10, 2000001), 6)
okx = np.abs(4 * xs_ - 3) + np.abs(xs_ + 2) + np.abs(xs_**3 - xs_) <= np.abs(3 * xs_ - 5) + 1e-9
chk("mj120", len(set(xs_[okx].tolist())), 2)
r = lin(1e-4, 40); a = sq(7 / (2 + 7 * r + 3 * r * r)); b = r * a
chk("mj111", 2 * ((a + sq(3 * a * b) + 2 * b)**2).max(), 28)
a = lin(1e-6, 1 - 1e-6); chk("mj116", (1 / (1 + a) + a / (2 - a)).min(), "2*sqrt(2)/3")
a = lin(0, 2); b = 2 - a; chk("g3-18", (1 / (a + 3) - b / (2 * a + 12)).min(), "1/6")
a = lin(1e-5, 1 - 1e-5); b = 2 - 2 * a; chk("mj114", (4 * (a - 1 / (2 * a))**2 + (2 / b - b)**2).min(), 2)
s = lin(1, 4); tt = 5 - s; v = 1 / s**2 + 1 / tt**2; chk("mj126", v.min() * v.max(), "17/50")

if __name__ == "__main__":
    bad = [r_ for r_ in R if not r_[1]]
    print("검산", len(R), "불일치", len(bad))
    for r_ in bad:
        print(r_)
