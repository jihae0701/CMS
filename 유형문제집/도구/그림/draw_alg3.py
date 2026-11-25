# -*- coding: utf-8 -*-
"""CLIMATH(m) 대수 3단원 '지수함수' 그림 — 올림포스 고난도 대수 02의 스캔 그림과 유형ON 0324 그림을 그림 규칙(그림규칙/math-figure-rules)대로 다시 그림 (2026-11-25).
python 도구/그림/draw_alg3.py [파일 …]   (KATEX_DIR 필요) → 도구/그림/alg3_*.png, 문서 폭은 alg3_widths.json (긴 변 약 10000 HWPUNIT, 해설 그림은 8000 안팎)
값은 문제·해설의 값을 따름(답이 드러나는 문제 그림은 개형). 원본의 색 선은 검은 선, 점선은 보조선·점근선.
"""
import os, sys, json, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "그림규칙", "math-figure-rules"))
import mathfig as M
from mathfig import Frame, dot, right_mark, DASH, SKY

def cv(F, f, x0, x1, extra="", n=400):
    """보이는 y 범위 안의 부분만 곡선으로(범위 밖은 끊음)"""
    lo, hi = F.yr
    seg = []
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        y = f(x)
        if lo <= y <= hi:
            seg.append((x, y))
        else:
            if len(seg) > 1:
                F.svg.append('<polyline points="%s" fill="none" stroke="#000" stroke-width="%s" stroke-linejoin="round" %s/>'
                             % (" ".join("%.1f,%.1f" % F.P(*p) for p in seg), M.STROKE, extra))
            seg = []
    if len(seg) > 1:
        F.svg.append('<polyline points="%s" fill="none" stroke="#000" stroke-width="%s" stroke-linejoin="round" %s/>'
                     % (" ".join("%.1f,%.1f" % F.P(*p) for p in seg), M.STROKE, extra))

def hole(F, p, r=5):
    F.svg.append('<circle cx="%.1f" cy="%.1f" r="%s" fill="#fff" stroke="#000" stroke-width="2"/>' % (F.P(*p) + (r,)))

def O(F):
    F.pt((0, 0), "O", "rt", -5, 5)

def hdash(F, y, x0, x1):
    F.dashed((x0, y), (x1, y))

def vdash(F, x, y0, y1):
    F.dashed((x, y0), (x, y1))

# ---------------------------------------------------------------- 1번 해설: y=-3^(-x+1)+2, 점근선 y=2, A(-1,-7), H
def k01s():
    f = lambda x: -3 ** (-x + 1) + 2
    F = Frame((-2.2, 3.6), (-8.2, 3.6), 52, 30, (20, 16, 120, 12)); F.axes(); O(F)
    hdash(F, 2, -2.2, 3.4); cv(F, f, -1.25, 3.4)
    A = (-1, -7); H = (-1, 2)
    dot(F, A); F.pt(A, "A", "rc", -8, 0); F.dashed(A, H); F.pt(H, "H", "rb", -6, -4)
    right_mark(F, H, (H[0], H[1] - 1), (H[0] + 1, H[1]), 0.25)
    F.lab((0, 2), "2", "lb", 6, -4); F.lab((3.4, 2), "y=2", "lb", -40, -6)
    F.lab((1.4, f(1.4)), "y=-3^{-x+1}+2", "lt", 6, 12)
    return F.render()

# ---------------------------------------------------------------- 2번 해설: y=2^x, y=4^x, y=10 안의 격자점
def k02s():
    F = Frame((-0.6, 4.6), (-0.6, 11.4), 70, 26, (20, 16, 100, 12)); F.axes(); O(F)
    cv(F, lambda x: 4 ** x, -0.6, 1.75); cv(F, lambda x: 2 ** x, -0.6, 3.45)
    F.seg((-0.6, 10), (4.5, 10)); F.lab((4.5, 10), "y=10", "lc", 6, 0)
    for x, ys in ((0, [1]), (1, [2, 3, 4]), (2, range(4, 11)), (3, [8, 9, 10])):
        for y in ys:
            dot(F, (x, y))
    for y in (2, 4, 8):
        hdash(F, y, 0, math.log2(y))
    for x in (1, 2, 3):
        vdash(F, x, 0, 2 ** x)
    vdash(F, 4, 0, 10)
    for x in (1, 2, 3, 4):
        F.lab((x, 0), str(x), "ct", 0, 6)
    for y in (1, 2, 4, 8, 10):
        F.lab((0, y), str(y), "rc", -8, 0)
    F.lab((1.66, 10.8), "y=4^x", "rb", -4, 0); F.lab((3.45, 10.8), "y=2^x", "lb", 4, 0)
    return F.render()

# ---------------------------------------------------------------- 3번 해설: f=2^(x+1)+8, g=3^(-x+1)+k (k=5로 그린 개형)
def k03s():
    k = 6.2
    f = lambda x: 2 ** (x + 1) + 8; g = lambda x: 3 ** (-x + 1) + k
    F = Frame((-2.8, 2.4), (-1.2, 15.5), 70, 34, (20, 16, 90, 12)); F.axes(); O(F)
    hdash(F, 8, -2.8, 2.2); hdash(F, k, -2.8, 2.2)
    cv(F, f, -2.8, 1.75); cv(F, g, -1.6, 2.2)
    dot(F, (0, 10)); dot(F, (0, k + 3))
    F.leader((0.06, 10), (0.7, 10.35)); F.lab((0.7, 10.35), "10", "lc", 4, 0)
    F.leader((0.06, k + 3), (0.7, 8.85)); F.lab((0.7, 8.85), "k+3", "lc", 4, 0)
    F.lab((0, 8), "8", "rt", -6, 4); F.lab((0, k), "k", "rt", -6, 4)
    F.lab((1.6, f(1.6)), "y=f(x)", "lc", 8, 0); F.lab((-1.55, g(-1.55)), "y=g(x)", "rc", -8, 0)
    return F.render()

# ---------------------------------------------------------------- 4번 문제: y=2^-x, y=-2^x, x=k, A, B, C (개형 k=1)
def k04():
    k = 1.0
    A = (k, 2 ** -k); B = (k, -2 ** k)
    m = A[1] / A[0]
    xc = next(x for x in [i / 1000 for i in range(-3000, 0)] if abs(-2 ** x - m * x) < 0.004)
    C = (xc, m * xc)
    F = Frame((-2.2, 2.2), (-2.9, 2.6), 80, 60, (20, 16, 30, 40)); F.axes(); O(F)
    cv(F, lambda x: 2 ** -x, -1.3, 2.1); cv(F, lambda x: -2 ** x, -2.1, 1.35)
    F.seg((-2.0, -2.0 * m), (2.1, 2.1 * m)); F.seg((k, -2.85), (k, 2.5))
    for p, n, a, dx, dy in ((A, "A", "lb", 6, -4), (B, "B", "lt", 6, 4), (C, "C", "rt", -6, 4)):
        dot(F, p); F.pt(p, n, a, dx, dy)
    F.lab((-0.9, 2 ** 0.9), "y=2^{-x}", "lb", 8, -2); F.lab((1.35, -2 ** 1.35), "y=-2^x", "lt", 8, 2)
    F.lab((k, -2.85), "x=k", "ct", 0, 6)
    return F.render()

# ---------------------------------------------------------------- 16번 해설: y=f(t), 한 근은 0과 1 사이, 한 근은 1보다 큼
def k16s():
    f = lambda t: 1.1 * (t - 0.45) * (t - 2.2)
    F = Frame((-1.2, 3.3), (-1.4, 2.6), 70, 70, (20, 16, 110, 12)); F.xaxis(-1.2, 3.3, "t")
    cv(F, f, -0.4, 3.0)
    F.seg((0, -0.08), (0, 0.08)); F.seg((1, -0.08), (1, 0.08))
    F.lab((0, 0), "0", "ct", 0, 8); F.lab((1, 0), "1", "ct", 0, 8)
    F.lab((2.9, f(2.9)), "y=f(t)", "lc", 8, 0)
    return F.render()

# ---------------------------------------------------------------- 24번 해설 세 그림: 원 (x-1)^2+y^2=1과 y=2^(x-m)-n
def _k24(curves, levels):
    F = Frame((-1.4, 4.6), (-3.5, 2.6), 62, 62, (20, 16, 200, 12)); F.axes(); O(F)
    t = [i / 200 * 2 * math.pi for i in range(201)]
    F.svg.append('<polyline points="%s" fill="none" stroke="#000" stroke-width="%s"/>' % (" ".join("%.1f,%.1f" % F.P(1 + math.cos(a), math.sin(a)) for a in t), M.STROKE))
    dot(F, (1, 0), 3); F.pt((1, 0), "C", "lb", 4, -4)
    ly = [2.3, 1.55, 0.8, 0.05]
    for i, (m, n, lab, yl) in enumerate(curves):
        g = lambda x, m=m, n=n: 2 ** (x - m) - n
        cv(F, g, -1.4, 4.5)
        if m == 0:
            F.lab((1.2, g(1.2)), lab, "lc", 8, 0)
        else:
            xq = m + math.log2(yl + n)                       # 곡선 위 점에서 오른쪽 빈자리로 짧은 지시선
            yy = ly[i] if len(curves) > 2 else yl + 0.7
            F.leader((xq, yl), (4.75, yy)); F.lab((4.75, yy), lab, "lc", 4, 0)
    for y in levels:
        hdash(F, y, -1.4, 4.5); F.lab((0, y), str(y), "rc", -8, 6)
    for x in (1, 2, 3):
        F.lab((x, 0), str(x), "ct", 4, 6)
    return F.render()

def k24s1():
    return _k24([(0, 0, "y=2^x", 0), (1, 1, "y=2^{x-1}-1", 1.9), (2, 1, "y=2^{x-2}-1", 1.2), (3, 1, "y=2^{x-3}-1", 0.55)], [-1])

def k24s2():
    return _k24([(0, 0, "y=2^x", 0), (1, 2, "y=2^{x-1}-2", 1.6), (2, 2, "y=2^{x-2}-2", 0.6)], [-2])

def k24s3():
    return _k24([(0, 0, "y=2^x", 0), (3, 3, "y=2^{x-3}-3", -0.6)], [-3])

# ---------------------------------------------------------------- 25번 문제·해설: 네 지수함수의 개형 (n=7로 그림)
def _k25(sol):
    b1, b2 = 2 * math.sqrt(7) / 7, 13 / 6
    F = Frame((-1.8, 1.8), (-0.3, 5.3), 80, 80, (170, 50, 190, 40)); F.axes(); O(F)
    cv(F, lambda x: 3 ** -x, -1.5, 1.8); cv(F, lambda x: 4.5 ** x, -1.8, 1.1)
    cv(F, lambda x: b1 ** x, -1.8, 1.8); cv(F, lambda x: b2 ** x, -1.8, 1.8)
    F.lab((-1.5, 3 ** 1.5), r"y=3^{-x}", "rc", -8, 4)
    F.lab((1.1, 4.5 ** 1.1), r"y=\left(\dfrac{9}{2}\right)^x", "lc", 8, 6)
    F.lab((-1.8, b1 ** -1.8), r"y=\left(\dfrac{2\sqrt{7}}{n}\right)^x", "rc", -8, 0)
    F.lab((1.8, b2 ** 1.8), r"y=\left(\dfrac{2n-1}{6}\right)^x", "lc", 8, 0)
    if sol:
        F.seg((1, -0.3), (1, 3.4)); F.lab((1, 0), "1", "lt", 4, 4)
        for (y, n, a, dx, dy) in ((3 ** -1, "A", "rt", -8, 6), (b1, "C", "lb", 8, -4), (b2, "D", "rc", -8, 0)):
            dot(F, (1, y)); F.pt((1, y), n, a, dx, dy)
        dot(F, (1, 4.5)); F.pt((1, 4.5), "B", "rc", -8, 0); F.dashed((1, 3.4), (1, 4.5))
    return F.render()

def k25(): return _k25(False)
def k25s(): return _k25(True)

# ---------------------------------------------------------------- 26번 해설: f(x)=2^x+2 (x<3), (5x+5)/(x-1) (x>=3)
def k26s():
    g = lambda x: 2 ** x + 2; h = lambda x: (5 * x + 5) / (x - 1)
    F = Frame((-1.6, 7.6), (-0.8, 12.6), 50, 30, (20, 16, 60, 12)); F.axes(); O(F)
    cv(F, g, -1.6, 3); cv(F, g, 3, 3.3, DASH); cv(F, h, 3, 7.5); cv(F, h, 1.48, 3, DASH)
    hdash(F, 2, -1.6, 7.4); hdash(F, 5, 0, 7.4); vdash(F, 1, -0.6, 12.4); vdash(F, 3, 0, 10); hdash(F, 10, 0, 3)
    dot(F, (3, 10))
    for y in (2, 3, 5, 10):
        F.lab((0, y), str(y), "rc", -8, 0)
    F.lab((1, 0), "1", "ct", 6, 6); F.lab((3, 0), "3", "ct", 0, 6)
    F.lab((6.5, h(6.5)), "y=f(x)", "lb", 0, -8)
    return F.render()

# ---------------------------------------------------------------- 27번 문제·해설: y=a^x-2, 직선 l(기울기 1), A, B (a=√2: A(2,0), B(4,2))
def _k27(sol):
    a = math.sqrt(2); f = lambda x: a ** x - 2
    F = Frame((-1.2, 5.6), (-2.6, 4.4), 60, 60, (20, 16, 40, 12)); F.axes(); O(F)
    cv(F, f, -1.2, 4.95); F.seg((-0.3, -2.3), (5.4, 3.4))
    A, B = (2, 0), (4, 2)
    dot(F, A); dot(F, B); F.pt(A, "A", "rb", -6, -6); F.pt(B, "B", "rb", -8, -2)
    F.lab((4.95, f(4.95)), "y=a^x-2", "rb", -6, -4); F.lab((5.4, 3.4), "l", "lc", 6, 0)
    if sol:
        H = (4, 0); F.seg(B, H); F.pt(H, "H", "lt", 4, 4); right_mark(F, H, A, B, 0.3)
    return F.render()

def k27(): return _k27(False)
def k27s(): return _k27(True)

# ---------------------------------------------------------------- 39번 문제: f=-2^(x-1)+7, g=4^(x-1)+1, A, B, C
def k39():
    f = lambda x: -2 ** (x - 1) + 7; g = lambda x: 4 ** (x - 1) + 1
    xa = 2.0
    F = Frame((-1.2, 3.6), (-0.8, 8.2), 80, 40, (20, 16, 110, 12)); F.axes(); O(F)
    cv(F, f, -1.2, 3.55); cv(F, g, -1.2, 2.45)
    A, B, C = (xa, f(xa)), (0, f(0)), (0, g(0))
    for p in (A, B, C):
        dot(F, p)
    F.seg(A, B); F.seg(B, C); F.seg(C, A)
    F.pt(A, "A", "lb", 6, -2); F.pt(B, "B", "rc", -8, -6); F.pt(C, "C", "rc", -8, 4)
    F.lab((2.4, g(2.4)), "y=g(x)", "lb", 4, 0); F.lab((3.4, f(3.4)), "y=f(x)", "lc", 6, 0)
    return F.render()

# ---------------------------------------------------------------- 47번 해설: y=(|n+1|+|n-2|)/6 의 그래프와 정수 n에서의 점
def k47s():
    f = lambda x: (abs(x + 1) + abs(x - 2)) / 6
    F = Frame((-4.2, 5.2), (-0.6, 1.9), 52, 130, (20, 16, 40, 30)); F.axes("n"); O(F)
    F.polyline([(-4.0, f(-4)), (-1, 0.5), (2, 0.5), (5.0, f(5))], DASH)
    hdash(F, 1, -4.2, 5.0); F.lab((0, 1), "1", "lb", 6, -4)
    for n in range(-3, 5):
        dot(F, (n, f(n)))
        if n:
            F.lab((n, 0), str(n), "ct", 0, 6)
    F.lab((0, 0.5), "\\dfrac{1}{2}", "rt", -6, 8); F.lab((-2, 5 / 6), "\\dfrac{5}{6}", "rt", -10, 10); F.lab((4, 7 / 6), "\\dfrac{7}{6}", "lt", 10, 6)
    F.lab((4.9, f(4.9)), "y=f(n)", "rb", -6, -6)
    return F.render()

# ---------------------------------------------------------------- 49번 해설: y=2^x+2, y=4^(-x+2)+5, y=n
def k49s():
    f = lambda x: 2 ** x + 2; g = lambda x: 4 ** (-x + 2) + 5
    F = Frame((-2.2, 4.4), (-0.6, 10.4), 60, 34, (20, 16, 130, 36)); F.axes(); O(F)
    cv(F, f, -2.2, 3.0); cv(F, g, 0.4, 4.3)
    hdash(F, 2, -2.2, 4.2); hdash(F, 5, -2.2, 4.2); hdash(F, 6, 0, 2); vdash(F, 2, 0, 6)
    F.seg((-2.2, 4), (4.3, 4)); F.lab((4.3, 4), "y=n", "lc", 6, 0)
    for y in (2, 3, 5, 6):
        F.lab((0, y), str(y), "rc", -8, 0)
    F.lab((2, 0), "2", "ct", 0, 6)
    F.lab((2.9, f(2.9)), "y=2^x+2", "lc", 8, 0); F.lab((3.0, 5.6), "y=4^{-x+2}+5", "lb", 6, -2)
    return F.render()

# ---------------------------------------------------------------- 56번 문제: y=2^x, y=10×2^-x, 선분 A_nB_n
def k56():
    f = lambda x: 2 ** x; g = lambda x: 10 * 2 ** -x
    F = Frame((-0.8, 4.4), (-0.8, 5.8), 90, 64, (20, 16, 150, 12)); F.axes(); O(F)
    cv(F, f, -0.8, 2.5); cv(F, g, 0.8, 4.3)
    L = {1: (("lt", 6, 4), ("lt", 6, 4)), 2: (("rb", -6, -2), ("lb", 6, -2)), 3: (("rc", -8, 0), ("lc", 8, 0)), 4: (("lb", 6, -2), ("rb", -6, -2))}
    for n in (1, 2, 3, 4):
        a, b = math.log2(n), math.log2(10 / n)
        F.seg((a, n), (b, n)); dot(F, (a, n)); dot(F, (b, n))
        (aa, adx, ady), (ba, bdx, bdy) = L[n]
        F.pt((a, n), "A_%d" % n, aa, adx, ady); F.pt((b, n), "B_%d" % n, ba, bdx, bdy)
    F.lab((0, 1), "1", "rb", -8, -2)
    F.lab((2.5, f(2.5)), "y=2^x", "lc", 6, 0); F.lab((4.3, g(4.3)), "y=10\\times2^{-x}", "lb", 4, -4)
    return F.render()

# ---------------------------------------------------------------- 60번 문제: y=2^x, x=n, x=2n, A, B, C, D, E, F (n=1.3으로 그린 개형)
def k60():
    n = 1.3; A, B = (n, 2 ** n), (2 * n, 2 ** (2 * n))
    F = Frame((-0.8, 3.4), (-1.2, 7.6), 110, 56, (20, 16, 90, 40)); F.axes(); O(F)
    cv(F, lambda x: 2 ** x, -0.8, 2.85)
    F.seg((n, -1.1), (n, 6.6)); F.seg((2 * n, -1.1), (2 * n, 6.6))
    C, D, E, Fp = (n, 0), (2 * n, 0), (0, A[1]), (0, B[1])
    F.seg(E, A); F.seg(Fp, B)
    for p in (A, B):
        dot(F, p)
    F.pt(A, "A", "lt", 6, 2); F.pt(B, "B", "lt", 8, 0); F.pt(C, "C", "lt", 6, 4); F.pt(D, "D", "lt", 6, 4)
    F.pt(E, "E", "rc", -8, 0); F.pt(Fp, "F", "rc", -8, 0)
    for v, p, q in ((C, (n, 1), (0, 0)), (D, (2 * n, 1), (0, 0)), (E, (1, A[1]), (0, 0)), (Fp, (1, B[1]), (0, 0))):
        right_mark(F, v, p, (v[0] - 1 if v[1] == 0 else v[0], v[1] if v[1] == 0 else v[1] - 1), 0.14)
    F.lab((n, -1.1), "x=n", "ct", 0, 6); F.lab((2 * n, -1.1), "x=2n", "ct", 0, 6)
    F.lab((2.85, 2 ** 2.85), "y=2^x", "lc", 8, 0)
    return F.render()

# ---------------------------------------------------------------- 61번 문제·해설: y=2^x, y=4^-x, y=-x^2+2
def _k61(sol):
    p = lambda x: -x * x + 2
    def root(fn, a, b):
        for _ in range(80):
            c = (a + b) / 2
            if (fn(a) - p(a)) * (fn(c) - p(c)) <= 0: b = c
            else: a = c
        return (a + b) / 2
    x1 = root(lambda x: 2 ** x, 0, 1.4); x2 = root(lambda x: 4 ** -x, -1.4, 0)
    A, B = (x1, 2 ** x1), (x2, 4 ** -x2)
    F = Frame((-2.0, 2.0), (-0.9, 3.0), 150, 150, (150, 16, 120, 30)); F.axes(); O(F)
    cv(F, p, -1.7, 1.7); cv(F, lambda x: 2 ** x, -2.0, 1.55); cv(F, lambda x: 4 ** -x, -0.78, 2.0)
    dot(F, A); dot(F, B); F.pt(A, "A", "lb", 6, -4); F.pt(B, "B", "rb", -6, -4)
    F.lab((0, 1), "1", "rt", -6, 4)
    F.lab((1.55, 2 ** 1.55), "y=2^x", "lc", 6, 0); F.lab((-0.78, 4 ** 0.78), "y=4^{-x}", "rc", -6, 0); F.lab((-1.62, p(-1.62)), "y=-x^2+2", "rc", -8, 0)
    if sol:
        cv(F, lambda x: 2 ** -x, -1.55, 2.0, DASH)
        A2 = (-x1, A[1]); dot(F, A2); F.pt(A2, "A'", "rb", -6, -4)
        F.dashed(A2, A); vdash(F, x1, 0, A[1]); vdash(F, -x1, 0, A[1]); vdash(F, x2, 0, B[1]); hdash(F, B[1], x2, 0)
        F.lab((x1, 0), "x_1", "ct", 0, 6); F.lab((-x1, 0), "-x_1", "rt", 2, 6); F.lab((x2, 0), "x_2", "ct", 0, 32)
        F.lab((0, B[1]), "y_2", "lb", 6, -2); F.lab((0, A[1]), "y_1", "lt", 6, 4); F.lab((0, 2), "2", "rb", -6, -4)
    return F.render()

def k61(): return _k61(False)
def k61s(): return _k61(True)

# ---------------------------------------------------------------- 유형ON 0324: y=n^x, y=2^x, x=1, x=2, 사다리꼴 ABDC (n=3)
def on324():
    n = 3
    F = Frame((-1.4, 2.6), (-0.8, 10.2), 120, 34, (20, 16, 70, 34)); F.axes(); O(F)
    A, B, C, D = (1, n), (1, 2), (2, n * n), (2, 4)
    F.poly([A, B, D, C], SKY)
    cv(F, lambda x: n ** x, -1.4, 2.08); cv(F, lambda x: 2 ** x, -1.4, 2.5)
    F.seg((1, -0.6), (1, 10)); F.seg((2, -0.6), (2, 10)); F.seg(A, C); F.seg(B, D)
    for q, nm, a, dx, dy in ((A, "A", "rb", -6, -2), (B, "B", "lt", 6, 4), (C, "C", "rb", -8, 0), (D, "D", "lt", 6, 4)):
        F.pt(q, nm, a, dx, dy)
    F.lab((1, -0.6), "x=1", "ct", -6, 6); F.lab((2, -0.6), "x=2", "ct", 6, 6)
    F.lab((2.08, n ** 2.08), "y=n^x", "lc", 6, 0); F.lab((2.5, 2 ** 2.5), "y=2^x", "lc", 6, 0)
    return F.render()


# ---------------------------------------------------------------- 모의 2023 고2 6월 18번: y=2^(x+1), y=2^(-x+1), A, B, C, y=k, y=2k (개형 k=1.35)
def m2306():
    k = 1.35; L = math.log2(k)
    A, B, C = (-1, 1), (1, 1), (0, 2)
    D, E, Fp, G = (L - 1, k), (1 - L, k), (L, 2 * k), (-L, 2 * k)
    F = Frame((-1.9, 1.9), (-0.4, 3.4), 110, 110, (20, 16, 90, 12)); F.axes(); O(F)
    F.poly([A, B, E, D], SKY); F.poly([C, Fp, G], SKY)
    cv(F, lambda x: 2 ** (x + 1), -1.9, 0.75); cv(F, lambda x: 2 ** (-x + 1), -0.75, 1.9)
    F.seg((-1.9, k), (1.9, k)); F.seg((-1.9, 2 * k), (1.9, 2 * k)); F.seg(A, B); F.seg(G, C); F.seg(C, Fp)
    for q, nm, a, dx, dy in ((A, "A", "rt", -6, 4), (B, "B", "lt", 6, 4), (C, "C", "lt", 6, 2), (D, "D", "rb", -6, -4), (E, "E", "lb", 6, -4), (Fp, "F", "lb", 6, -4), (G, "G", "rb", -6, -4)):
        dot(F, q); F.pt(q, nm, a, dx, dy)
    F.lab((1.9, k), "y=k", "lb", -30, -6); F.lab((1.9, 2 * k), "y=2k", "lb", -40, -6)
    F.lab((0.75, 2 ** 1.75), "y=2^{x+1}", "lc", 6, 0); F.lab((-0.75, 2 ** 1.75), "y=2^{-x+1}", "rc", -6, 0)
    return F.render()


# ---------------------------------------------------------------- 워크북: 모의 2023 고2 6월 18번 숫자 변형 — y=3^(x+1), y=3^(-x+1), A(-1,1), B(1,1), C(0,3), y=k, y=3k (개형 k=1.45)
def w2306():
    k = 1.45; L = math.log(k, 3)
    A, B, C = (-1, 1), (1, 1), (0, 3)
    D, E, Fp, G = (L - 1, k), (1 - L, k), (L, 3 * k), (-L, 3 * k)
    F = Frame((-1.9, 1.9), (-0.5, 5.6), 110, 62, (20, 16, 90, 12)); F.axes(); O(F)
    F.poly([A, B, E, D], SKY); F.poly([C, Fp, G], SKY)
    cv(F, lambda x: 3 ** (x + 1), -1.9, 0.55); cv(F, lambda x: 3 ** (-x + 1), -0.55, 1.9)
    F.seg((-1.9, k), (1.9, k)); F.seg((-1.9, 3 * k), (1.9, 3 * k)); F.seg(A, B); F.seg(G, C); F.seg(C, Fp)
    for q, nm, a, dx, dy in ((A, "A", "rt", -6, 4), (B, "B", "lt", 6, 4), (C, "C", "lt", 6, 2), (D, "D", "rb", -6, -4), (E, "E", "lb", 6, -4), (Fp, "F", "lb", 6, -4), (G, "G", "rb", -6, -4)):
        dot(F, q); F.pt(q, nm, a, dx, dy)
    F.lab((1.9, k), "y=k", "lb", -30, -6); F.lab((1.9, 3 * k), "y=3k", "lb", -40, -6)
    F.lab((0.55, 3 ** 1.55), "y=3^{x+1}", "lc", 6, 0); F.lab((-0.55, 3 ** 1.55), "y=3^{-x+1}", "rc", -6, 0)
    return F.render()


FIGS = {"alg3_w2306.png": w2306, "alg3_m2306.png": m2306, "alg3_k01s.png": k01s, "alg3_k02s.png": k02s, "alg3_k03s.png": k03s, "alg3_k04.png": k04, "alg3_k16s.png": k16s,
        "alg3_k24s1.png": k24s1, "alg3_k24s2.png": k24s2, "alg3_k24s3.png": k24s3, "alg3_k25.png": (k25, 13000), "alg3_k25s.png": (k25s, 13000),
        "alg3_k26s.png": k26s, "alg3_k27.png": k27, "alg3_k27s.png": k27s, "alg3_k39.png": k39, "alg3_k47s.png": k47s,
        "alg3_k49s.png": k49s, "alg3_k56.png": k56, "alg3_k60.png": k60, "alg3_k61.png": k61, "alg3_k61s.png": k61s, "alg3_on324.png": on324}

if __name__ == "__main__":
    wf = os.path.join(HERE, "alg3_widths.json")
    W = json.load(open(wf)) if os.path.exists(wf) else {}
    for name in sys.argv[1:] or FIGS:
        fn, w = FIGS[name] if isinstance(FIGS[name], tuple) else (FIGS[name], None)   # 25번은 긴 함수식 이름표 넷이라 폭 13000(넓은 그림 예외)
        W[name] = M.fit_shoot(name, fn, w, HERE)
    json.dump(W, open(wf, "w"), indent=1, sort_keys=True)
