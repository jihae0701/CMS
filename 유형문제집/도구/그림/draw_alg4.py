# -*- coding: utf-8 -*-
"""CLIMATH(m) 대수 4단원 '로그함수' 그림 — 올림포스 고난도 대수 02의 로그함수 문항 스캔 그림, 유형ON 0335·0341, 모의 2023 고2 9월 18번을
그림 규칙(그림규칙/math-figure-rules)대로 다시 그림 (2026-11-26).
python 도구/그림/draw_alg4.py [파일 …]   (KATEX_DIR 필요) → 도구/그림/alg4_*.png, 문서 폭은 alg4_widths.json
값은 문제·해설의 값을 따름(답이 드러나는 문제 그림은 개형). 원본의 굵은 곡선 조각은 보통 굵기, 점선은 보조선·점근선.
"""
import os, sys, json, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "그림규칙", "math-figure-rules"))
sys.path.insert(0, HERE)
import mathfig as M
from mathfig import Frame, dot, right_mark, DASH, SKY
from draw_alg3 import cv, O, hdash, vdash

L2 = lambda x: math.log2(x)
LG = lambda b: (lambda x: math.log(x) / math.log(b))

def circle(F, c, r, extra=""):
    t = [i / 240 * 2 * math.pi for i in range(241)]
    F.svg.append('<polyline points="%s" fill="none" stroke="#000" stroke-width="%s" %s/>'
                 % (" ".join("%.1f,%.1f" % F.P(c[0] + r * math.cos(a), c[1] + r * math.sin(a)) for a in t), M.STROKE, extra))

def pts(F, L):
    for p, n, a, dx, dy in L:
        dot(F, p); F.pt(p, n, a, dx, dy)

# ---------------------------------------------------------------- 9번 해설: y=log2(x-2), y=log3(-x+m) (개형 m=6)
def k09s():
    m = 6
    F = Frame((-6.6, 7.6), (-2.4, 3.4), 42, 42, (20, 16, 20, 12)); F.axes(); O(F)
    cv(F, lambda x: L2(x - 2), 2.02, 7.5); cv(F, lambda x: math.log(-x + m, 3), -6.6, 5.98)
    dot(F, (3, 0)); F.lab((3, 0), "3", "ct", -4, 6)
    dot(F, (m - 1, 0)); F.leader((m - 1, 0), (4.3, -1.0)); F.lab((4.3, -1.0), "m-1", "rt", -2, 0)
    F.lab((-6.5, 0.9), r"y=\log_3(-x+m)", "lc", 0, 0)
    F.lab((7.5, L2(5.5)), r"y=\log_2(x-2)", "rb", 0, -10)
    return F.render()

# ---------------------------------------------------------------- 10번 해설: y=log_a x, y=log_2a x (a=2), y=x-2, A(4,2)
def k10s():
    F = Frame((-0.6, 6.4), (-1.6, 3.4), 70, 70, (20, 16, 130, 12)); F.axes(); O(F)
    cv(F, L2, 0.33, 6.2); cv(F, LG(4), 0.11, 6.2)
    F.seg((0.5, -1.5), (5.1, 3.1))
    A = (4, 2); dot(F, A); F.pt(A, "A", "rb", -6, -4); hdash(F, 2, 0, 4)
    F.lab((0, 2), "2", "rc", -8, 0); F.lab((1, 0), "1", "lt", 12, 6); F.lab((2, 0), "2", "ct", 4, 6)
    F.lab((5.1, 3.1), "y=x-2", "lc", 6, 0); F.lab((6.2, L2(6.2)), r"y=\log_a x", "lc", 6, 0); F.lab((6.2, LG(4)(6.2)), r"y=\log_{2a} x", "lc", 6, 0)
    return F.render()

# ---------------------------------------------------------------- 12번 해설: y=(t-1)^2-3 (-1<=t<=4)
def k12s():
    f = lambda t: (t - 1) ** 2 - 3
    F = Frame((-2.0, 5.0), (-4.0, 7.0), 56, 28, (20, 16, 170, 12)); F.axes("t"); O(F)
    cv(F, f, -1, 4); cv(F, f, -1.65, -1, DASH); cv(F, f, 4, 4.3, DASH)
    for p in ((-1, 1), (4, 6), (1, -3)):
        dot(F, p)
    hdash(F, 1, -1, 0); vdash(F, -1, 0, 1); hdash(F, 6, 0, 4); vdash(F, 4, 0, 6); hdash(F, -3, 0, 1)
    F.lab((0, 1), "1", "lb", 4, -2); F.lab((0, 6), "6", "rc", -8, 0); F.lab((0, -3), "-3", "rc", -8, 0)
    F.lab((-1, 0), "-1", "ct", -6, 6); F.lab((4, 0), "4", "ct", 0, 6)
    F.lab((3.5, f(3.5)), "y=(t-1)^2-3", "lc", 12, 0)
    return F.render()

# ---------------------------------------------------------------- 13번 해설: f = 2^(x+1) (x<0), log4(x+1)+2 (x>=0)
def k13s():
    g1 = lambda x: 2 ** (x + 1); g2 = lambda x: math.log(x + 1, 4) + 2
    F = Frame((-7.6, 3.6), (-1.6, 4.3), 50, 50, (20, 16, 120, 12)); F.axes(); O(F)
    cv(F, g1, -7.6, 0); cv(F, g2, 0, 3.5)
    cv(F, g1, 0, 1.1, DASH); cv(F, g2, -0.985, 0, DASH)
    F.seg((-7.6, 1), (3.5, 1), 1.5); F.seg((-7.6, 3), (3.5, 3), 1.5)
    F.lab((3.5, 1), "y=1", "lc", 6, 0); F.lab((3.5, 3), "y=3", "lc", 6, 8)
    F.lab((0, 1), "1", "lb", 4, -2); F.lab((0, 2), "2", "rb", -4, -2); F.lab((0, 3), "3", "lb", 4, -4)
    F.lab((1.1, g1(1.1)), "y=2^{x+1}", "lc", 6, 0); F.lab((-7.5, g1(-7.5)), "y=f(x)", "lb", 0, -4)
    F.lab((-0.99, -1.05), r"y=\log_4(x+1)+2", "rc", -6, 0)
    return F.render()

# ---------------------------------------------------------------- 14번: f=a^x+1, g=log_a(x-1), A, B, C (a^2=√5)
def _k14(sol):
    a = 5 ** 0.25; s = a * a + 1
    f = lambda x: a ** x + 1; g = lambda x: math.log(x - 1, a)
    F = Frame((-1.4, 6.2), (-1.4, 6.2), 50, 50, (20, 16, 110, 12)); F.axes(); O(F)
    cv(F, f, -1.4, 3.1); cv(F, g, 1.03, 6.1); F.seg((-1.2, -1.2), (5.6, 5.6), 1.5)
    A, B, C = (2, 0), (2, s), (s, 2)
    F.seg(A, B); F.seg((1.2, s + 0.8), (s + 1.6, 2 - 1.6))
    pts(F, ((A, "A", "ct", 4, 6), (B, "B", "rb", -6, -4), (C, "C", "lb", 6, -4)))
    if sol:
        hdash(F, s, 0, 2); hdash(F, 2, 0, s); vdash(F, s, 0, 2)
        F.lab((0, s), "a^2+1", "rc", -6, 0); F.lab((0, 2), "2", "rc", -6, 0); F.lab((s, 0), "a^2+1", "ct", 4, 6)
        F.seg(A, C)
    F.lab((3.1, f(3.1)), "y=f(x)", "rb", -4, -4); F.lab((5.6, 5.6), "y=x", "lc", 6, 0); F.lab((6.1, g(6.1)), "y=g(x)", "lc", 6, 0)
    return F.render()
def k14(): return _k14(False)
def k14s(): return _k14(True)

# ---------------------------------------------------------------- 15번 해설: f=log2 x+1, g=2^(x-1), (1,1), (2,2)
def k15s():
    f = lambda x: L2(x) + 1; g = lambda x: 2 ** (x - 1)
    F = Frame((-0.8, 3.4), (-0.9, 3.4), 80, 80, (20, 16, 120, 12)); F.axes(); O(F)
    cv(F, f, 0.25, 3.3); cv(F, g, -0.8, 2.75); F.seg((-0.6, -0.6), (3.0, 3.0), 1.5)
    for p in ((1, 1), (2, 2)):
        dot(F, p); hdash(F, p[1], 0, p[0]); vdash(F, p[0], 0, p[1])
    F.lab((1, 0), "1", "ct", 0, 6); F.lab((2, 0), "2", "ct", 0, 6); F.lab((0, 1), "1", "rc", -8, 0); F.lab((0, 2), "2", "rc", -8, 0)
    F.lab((2.75, g(2.75)), "y=g(x)", "rc", -6, -6); F.lab((3.0, 3.0), "y=x", "lc", 6, 0); F.lab((3.3, f(3.3)), "y=f(x)", "lc", 6, 0)
    return F.render()

# ---------------------------------------------------------------- 19번 해설: y=log_{1/4} x, y=log2 x-2, A(4,0), B(1,0), C(2^{4/3}, -2/3)
def k19s():
    F = Frame((-0.9, 5.8), (-2.6, 2.0), 66, 66, (40, 16, 200, 12)); F.axes(); O(F)
    cv(F, lambda x: -L2(x) / 2, 0.11, 5.7); cv(F, lambda x: L2(x) - 2, 0.17, 5.7)
    c = 2 ** (4 / 3); A, B, C = (4, 0), (1, 0), (c, -2 / 3)
    F.seg(A, B); F.seg(B, C); F.seg(C, A)
    pts(F, ((A, "A", "cb", 0, -6), (B, "B", "rb", -4, -4), (C, "C", "ct", 0, 8)))
    hdash(F, -2 / 3, 0, c)
    F.lab((0, -2 / 3), r"-\frac{2}{3}", "rc", -6, 0); F.lab((c, 0), r"2^{\genfrac{}{}{}{2}{4}{3}}", "cb", 0, -6)
    F.lab((0.11, -L2(0.11) / 2), r"y=\log_{\genfrac{}{}{}{2}{1}{4}} x", "lc", 8, 4); F.lab((5.7, L2(5.7) - 2), r"y=\log_2 x-2", "lc", 6, 0)
    return F.render()

# ---------------------------------------------------------------- 20번: f=(x+2)(x-5)/2, g=-(x-1)(x-10)/2
def _k20(sol):
    f = lambda x: (x + 2) * (x - 5) / 2; g = lambda x: -(x - 1) * (x - 10) / 2
    F = Frame((-3.4, 12.6), (-7.4, 12.6), 26, 26, (20, 16, 90, 12)); F.axes(); O(F)
    cv(F, f, -3.4, 8.4); cv(F, g, -0.2, 11.8)
    vdash(F, 7, 0, 9); F.lab((7, 0), "7", "ct", 4, 6)
    F.lab((0, -5), "-5", "rc", -6, 0)
    for x, t in ((-2, "-2"), (1, "1"), (5, "5"), (10, "10")):
        F.lab((x, 0), t, "ct", -4 if x < 0 else 4, 6)
    if sol:
        hdash(F, -5, 0, 11); vdash(F, 3, -5, 0); vdash(F, 11, -5, 0)
        F.lab((3, 0), "3", "cb", 0, -6); F.lab((11, 0), "11", "cb", 0, -6)
    F.lab((8.4, f(8.4)), "y=f(x)", "lc", 6, 0); F.lab((11.8, g(11.8)), "y=g(x)", "lc", 6, 0)
    return F.render()
def k20(): return _k20(False)
def k20s(): return _k20(True)

# ---------------------------------------------------------------- 23번: y=mx, y=log2 x, A(2,1), B(4,2) (해설: C, D 수선의 발)
def _k23(sol):
    F = Frame((-0.6, 6.2), (-1.4, 3.0), 70, 70, (20, 16, 140, 12)); F.axes(); O(F)
    cv(F, L2, 0.36, 6.0); F.seg((-0.6, -0.3), (6.0, 3.0))
    A, B = (2, 1), (4, 2)
    pts(F, ((A, "A", "rb", -6, -4), (B, "B", "rb", -4, -6)))
    if sol:
        C, D = (2, 0), (4, 0)
        F.seg(A, C, 1.5); F.seg(B, D, 1.5)
        right_mark(F, C, (2, 1), (3, 0), 0.22); right_mark(F, D, (4, 1), (5, 0), 0.22)
        F.pt(C, "C", "ct", 0, 8); F.pt(D, "D", "ct", 0, 8)
    F.lab((6.0, 3.0), "y=mx", "lc", 6, 0); F.lab((6.0, L2(6.0)), r"y=\log_2 x", "lc", 6, 6)
    return F.render()
def k23(): return _k23(False)
def k23s(): return _k23(True)

# ---------------------------------------------------------------- 30번 해설: y=log_a(x+1/2), y=log_a(x+b) (b=3/2), 정삼각형 ACB
def k30s():
    a = 2 ** (2 / math.sqrt(3))
    F = Frame((-1.9, 3.6), (-2.3, 2.6), 80, 80, (20, 16, 150, 12)); F.axes(); O(F)
    cv(F, lambda x: math.log(x + 0.5, a), -0.44, 2.9); cv(F, lambda x: math.log(x + 1.5, a), -1.45, 2.2)
    A, B, C = (0.5, 0), (0, -math.sqrt(3) / 2), (-0.5, 0)
    F.seg(A, B); F.seg(B, C)
    pts(F, ((A, "A", "lt", 6, 4), (B, "B", "lt", 6, 4), (C, "C", "rb", -4, -4)))
    F.lab((0.5, 0), r"\frac{1}{2}", "lt", 28, 2)
    F.leader((1.0, math.log(2.5, a)), (1.5, 2.3)); F.lab((1.5, 2.3), r"y=\log_a(x+b)", "lc", 4, 0)
    F.leader((1.2, math.log(1.7, a)), (1.5, -0.9)); F.lab((1.5, -0.9), r"y=\log_a\left(x+\frac12\right)", "lc", 4, 0)
    return F.render()

# ---------------------------------------------------------------- 37번 해설: y=a^x, y=x, y=log_a x (개형 a=2), A(1,0), B(1,a), C(a,1)
def k37s():
    F = Frame((-1.2, 3.6), (-1.2, 3.6), 70, 70, (20, 16, 120, 12)); F.axes(); O(F)
    cv(F, lambda x: 2 ** x, -1.2, 1.75); cv(F, L2, 0.21, 3.5); F.seg((-1.0, -1.0), (3.2, 3.2), 1.5)
    F.seg((1, -1.0), (1, 3.5), 1.5); F.seg((0.4, 2.6), (3.0, 0.0))
    A, B, C, H = (1, 0), (1, 2), (2, 1), (1.5, 1.5)
    pts(F, ((A, "A", "lt", 6, 4), (B, "B", "rb", -6, -2), (C, "C", "lb", 6, -2)))
    right_mark(F, A, (1, 1), (2, 0), 0.2); right_mark(F, H, (1, 2), (2, 2), 0.2)
    F.lab((1.75, 2 ** 1.75), "y=a^x", "lc", 6, 0); F.lab((3.2, 3.2), "y=x", "lc", 6, 0); F.lab((3.5, L2(3.5)), r"y=\log_a x", "lc", 6, 0)
    return F.render()

# ---------------------------------------------------------------- 44번: 기울기 -1인 직선 l, y=log2 x, y=log4 x (a=2+2√2)
def _k44(sol):
    a = 2 + 2 * math.sqrt(2); ya, yb = L2(a), math.log(a + 1, 4)
    F = Frame((-0.6, 8.6), (-1.4, 3.6), 46, 70, (120 if sol else 20, 16, 130, 12)); F.axes(); O(F)
    cv(F, L2, 0.36, 8.4); cv(F, LG(4), 0.15, 8.4)
    k = a + ya; F.seg((k - 3.5, 3.5), (k - (-0.9), -0.9))
    A, B = (a, ya), (a + 1, yb)
    pts(F, ((A, "A", "cb", 0, -8), (B, "B", "lb", 6, 2)))
    F.lab((1, 0), "1", "ct", 2, 6); F.lab((k - 3.5, 3.5), "l", "rc", -6, 0)
    if sol:
        C = (a, yb); F.seg(A, C, 1.5); F.seg(C, B, 1.5); right_mark(F, C, (a, ya), (a + 1, yb), 0.18)
        hdash(F, ya, 0, a); hdash(F, yb, 0, a); vdash(F, a, 0, yb); vdash(F, a + 1, 0, yb)
        F.lab((0, ya), r"\log_2 a", "rc", -6, 0); F.lab((0, yb), r"\log_4(a+1)", "rc", -6, 0)
        F.lab((a, 0), "a", "ct", -4, 6); F.lab((a + 1, 0), "a+1", "ct", 6, 6); F.pt(C, "C", "rt", -6, 4)
    F.lab((8.4, L2(8.4)), r"y=\log_2 x", "lc", 6, 0); F.lab((8.4, math.log(8.4, 4)), r"y=\log_4 x", "lc", 6, 0)
    return F.render()
def k44(): return _k44(False)
def k44s(): return _k44(True)

# ---------------------------------------------------------------- 50번: y=log_a x, 기울기 4/3인 직선 l, A, B, C, D (a=2)
def k50():
    F = Frame((-0.8, 6.6), (-2.7, 3.4), 60, 60, (20, 16, 130, 12)); F.axes(); O(F)
    cv(F, L2, 0.17, 6.4)
    l = lambda x: 4 / 3 * x - 5 / 3; F.seg((-0.5, l(-0.5)), (3.3, l(3.3)))
    A, B, C, D = (0.5, -1), (2, 1), (1.25, 0), (0, -5 / 3)
    pts(F, ((A, "A", "lt", 6, 2), (B, "B", "lt", 6, 4), (C, "C", "lt", 4, 4), (D, "D", "rc", -6, 0)))
    F.lab((3.3, l(3.3)), "l", "lb", 4, -2); F.lab((6.4, L2(6.4)), r"y=\log_a x", "lc", 6, 0)
    return F.render()

# ---------------------------------------------------------------- 53번: 4x-3y-5=0, y=log2 x, y=log2(x-3)+4, A, B, C, D, 삼각형 OBC
def k53():
    F = Frame((-0.8, 9.2), (-2.8, 7.6), 44, 44, (20, 16, 240, 12)); F.axes(); O(F)
    cv(F, L2, 0.15, 9.0); cv(F, lambda x: L2(x - 3) + 4, 3.02, 9.0)
    l = lambda x: (4 * x - 5) / 3; F.seg((-0.1, l(-0.1)), (6.2, l(6.2)))
    A, B, C, D = (0.5, -1), (2, 1), (3.5, 3), (5, 5)
    F.seg((0, 0), B, 1.5); F.seg((0, 0), C, 1.5)
    pts(F, ((A, "A", "lt", 6, 2), (B, "B", "lt", 10, 6), (C, "C", "lt", 6, 2), (D, "D", "lt", 6, 2)))
    F.lab((6.2, l(6.2)), "4x-3y-5=0", "cb", 0, -6)
    F.lab((9.0, L2(9.0)), r"y=\log_2 x", "lc", 6, 0); F.lab((9.0, L2(6.0) + 4), r"y=\log_2(x-3)+4", "lc", 6, 0)
    return F.render()

# ---------------------------------------------------------------- 54번 해설: 0<=x<=2에서 f, 0<=x<=6에서 f
def f54(x):
    k = min(int(x // 2), 2); t = x - 2 * k
    return (2 ** t - 1 if t < 1 else L2(t) + 1) + 2 * k
def k54s1():
    F = Frame((-0.5, 2.7), (-0.5, 2.7), 110, 110, (20, 16, 60, 12)); F.axes(); O(F)
    cv(F, f54, 0, 2); cv(F, lambda x: L2(x + 1), 0, 1, DASH); F.seg((-0.3, -0.3), (2.5, 2.5), 1.5)
    for p in ((1, 1), (2, 2)):
        dot(F, p); hdash(F, p[1], 0, p[0]); vdash(F, p[0], 0, p[1])
    F.lab((1, 0), "1", "ct", 0, 6); F.lab((2, 0), "2", "ct", 0, 6); F.lab((0, 1), "1", "rc", -8, 0); F.lab((0, 2), "2", "rc", -8, 0)
    F.leader((0.55, f54(0.55) + 0.02), (0.35, 1.9)); F.lab((0.35, 1.9), "y=f(x)", "cb", 0, -2); F.lab((2.5, 2.5), "y=x", "lc", 6, 0)
    return F.render()
def k54s2():
    F = Frame((-0.5, 6.8), (-0.5, 6.8), 46, 46, (20, 16, 80, 12)); F.axes(); O(F)
    cv(F, f54, 0, 6, n=1200); F.seg((-0.3, -0.3), (6.6, 6.6), 1.5); F.seg((6, 0), (6, 6))
    for i in range(1, 7):
        hdash(F, i, 0, i); vdash(F, i, 0, i)
        F.lab((i, 0), str(i), "ct", 0, 6); F.lab((0, i), str(i), "rc", -8, 0)
    F.lab((6.6, 6.6), "y=x", "lc", 6, 0); F.lab((6, 6), "y=f(x)", "lc", 10, 14)
    return F.render()

# ---------------------------------------------------------------- 55번: y=a^x, y=log_a x (a=4), y=-x+5, A(1,4), B(4,1) (해설: 외접원, 외심 C)
def _k55(sol):
    F = Frame((-1.2, 5.6), (-1.4, 5.6), 56, 56, (20, 16, 130, 12)); F.axes(); O(F)
    cv(F, lambda x: 4 ** x, -1.2, 1.22); cv(F, LG(4), 0.07, 5.5); F.seg((-0.4, 5.4), (5.6, -0.6))
    A, B = (1, 4), (4, 1)
    if sol:
        C, H = (1.7, 1.7), (2.5, 2.5)
        F.seg((-0.8, -0.8), (4.4, 4.4), 1.5); circle(F, C, math.hypot(1.7, 1.7))
        F.seg((0, 0), A, 1.5); F.seg((0, 0), B, 1.5)
        dot(F, C); F.pt(C, "C", "lt", 6, 2); F.pt(H, "H", "lb", 8, -2); right_mark(F, H, (2, 3), (3, 3), 0.2)
        F.lab((4.4, 4.4), "y=x", "lc", 6, 0)
    else:
        F.poly([(0, 0), A, B], SKY); F.seg((0, 0), A, 1.5); F.seg((0, 0), B, 1.5)
    pts(F, ((A, "A", "lb", 6, -2), (B, "B", "lb" if sol else "lt", 10 if sol else 4, -6 if sol else 6)))
    F.lab((1.22, 4 ** 1.22), "y=a^x", "lc", 6, 0); F.lab((5.5, math.log(5.5, 4)), r"y=\log_a x", "lc", 6, 0)
    F.lab((5.6, -0.6), "y=-x+5", "rc", -10, 6)
    return F.render()
def k55(): return _k55(False)
def k55s(): return _k55(True)

# ---------------------------------------------------------------- 58번: y=|log2(x-1)|, y=k, y=2k, A, B, C, D, E (k=1)
def k58():
    F = Frame((-0.6, 7.0), (-0.7, 3.4), 56, 56, (20, 16, 140, 12)); F.axes(); O(F)
    cv(F, lambda x: abs(L2(x - 1)), 1.13, 6.9)
    F.seg((0, 1), (6.9, 1), 1.5); F.seg((0, 2), (6.9, 2), 1.5)
    A, B, C, D, E = (1.5, 1), (3, 1), (1.25, 2), (5, 2), (0, 1)
    pts(F, ((A, "A", "rt", -4, 4), (B, "B", "lt", 4, 4), (C, "C", "rb", -4, -4), (D, "D", "rb", -4, -4), (E, "E", "rc", -6, 0)))
    F.lab((6.9, 1), "y=k", "lc", 6, 0); F.lab((6.9, 2), "y=2k", "lc", 6, 0); F.lab((6.9, 3.05), r"y=|\log_2(x-1)|", "rc", 0, 0)
    return F.render()

# ---------------------------------------------------------------- 유형ON 0335: y=log_a x, 원 (x-5/4)^2+y^2=13/16 (a=4)
def on335():
    F = Frame((-0.5, 4.6), (-1.5, 1.5), 100, 100, (20, 16, 20, 12)); F.axes(); O(F)
    cv(F, LG(4), 0.12, 3.7); circle(F, (1.25, 0), math.sqrt(13) / 4)
    P, Q = (2, 0.5), (0.5, -0.5)
    pts(F, ((P, "P", "rb", -4, -4), (Q, "Q", "rc", -8, 4)))
    F.lab((3.7, math.log(3.7, 4)), r"y=\log_a x", "rb", 0, -8)
    F.lab((2.05, -1.1), r"\left(x-\frac{5}{4}\right)^2+y^2=\frac{13}{16}", "lc", 0, 0)
    return F.render()

# ---------------------------------------------------------------- 유형ON 0341: y=log_a x, y=log_b x (a=1/4, b=(2/3)^{3/2}), 정사각형 두 개
def on341():
    a, b = 0.25, (2 / 3) ** 1.5
    F = Frame((-0.2, 1.6), (-0.6, 1.3), 260, 260, (20, 16, 110, 12)); F.axes(); O(F)
    cv(F, LG(a), 0.12, 1.55); cv(F, LG(b), 0.32, 1.55)
    p, q = 0.5, 2 / 3
    F.polyline([(0, p), (p, p), (p, 0)]); F.polyline([(0, q), (q, q), (q, 0)])
    pts(F, (((p, p), "P", "rt", -6, 6), ((q, q), "Q", "lb", 4, -4)))
    F.pt((p, 0), "A", "ct", 0, 6); F.pt((q, 0), "B", "ct", 0, 6); F.lab((1, 0), "1", "cb", 4, -6)
    F.lab((0.48, LG(b)(0.48)), r"y=\log_b x", "lc", 10, 0); F.lab((1.55, LG(a)(1.55)), r"y=\log_a x", "lc", 6, 0)
    return F.render()

# ---------------------------------------------------------------- 모의 2023 고2 9월 18번: y=log2 x, y=log2(x-p)+q, (4,2), A, B, C, D, y=3 (개형 p=2.6)
def m2309():
    p = 2.6; q = 2 - L2(4 - p)
    g = lambda x: L2(x - p) + q
    F = Frame((-0.6, 11.4), (-1.8, 5.0), 40, 48, (20, 16, 240, 12)); F.axes(); O(F)
    cv(F, L2, 0.3, 11.2); cv(F, g, p + 0.02, 11.2)
    F.seg((0, 3), (11.2, 3), 1.5)
    xb = p + 2 ** -q; xd = p + 2 ** (3 - q)
    pts(F, (((1, 0), "A", "ct", -2, 6), ((xb, 0), "B", "ct", 4, 6), ((8, 3), "C", "lt", 4, 6), ((xd, 3), "D", "cb", -4, -6)))
    dot(F, (4, 2)); F.lab((4, 2), "(4,\\,2)", "lt", 6, 4)
    F.lab((0, 3), "y=3", "lb", 6, -4); F.lab((11.2, L2(11.2)), r"y=\log_2 x", "lc", 6, 0); F.lab((11.2, g(11.2)), r"y=\log_2(x-p)+q", "lc", 6, 0)
    return F.render()


FIGS = {"alg4_k09s.png": k09s, "alg4_k10s.png": k10s, "alg4_k12s.png": k12s, "alg4_k13s.png": k13s, "alg4_k14.png": k14, "alg4_k14s.png": k14s,
        "alg4_k15s.png": k15s, "alg4_k19s.png": k19s, "alg4_k20.png": k20, "alg4_k20s.png": k20s, "alg4_k23.png": k23, "alg4_k23s.png": k23s,
        "alg4_k30s.png": k30s, "alg4_k37s.png": k37s, "alg4_k44.png": k44, "alg4_k44s.png": k44s, "alg4_k50.png": k50, "alg4_k53.png": k53,
        "alg4_k54s1.png": k54s1, "alg4_k54s2.png": k54s2, "alg4_k55.png": k55, "alg4_k55s.png": k55s, "alg4_k58.png": k58,
        "alg4_on335.png": on335, "alg4_on341.png": on341, "alg4_m2309.png": m2309}

if __name__ == "__main__":
    wf = os.path.join(HERE, "alg4_widths.json")
    W = json.load(open(wf)) if os.path.exists(wf) else {}
    for name in sys.argv[1:] or FIGS:
        fn, w = FIGS[name] if isinstance(FIGS[name], tuple) else (FIGS[name], None)
        W[name] = M.fit_shoot(name, fn, w, HERE)
    json.dump(W, open(wf, "w"), indent=1, sort_keys=True)
