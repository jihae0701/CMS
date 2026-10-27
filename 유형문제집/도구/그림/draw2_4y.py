# -*- coding: utf-8 -*-
"""공통수학2 유형서 4단원(도형의 이동) 그림. python 그림/draw2_4y.py [파일 ...]  (KATEX_DIR 필요)
학력평가 원문 그림(2024년 10월 고1·2025년 10월 고1·2026년 3월 고2는 시험지 hml, 나머지는 HIT기출의 문제 그림)을
같은 모양으로 새로 그렸다(풀이용 보조선·점은 뺌).
내신·고쟁이·올림포스 그림(2026-10-27 사용자 지시 '원본 그대로'): 내신은 학교 시험지 hwp의 그림, 고쟁이·올림포스는 책 쪽 그림을 보고 그림.
n1629는 시험지의 그림이 한글 그리기 개체라 꺼낼 수 없어 문제 조건(직선 y=x, 제4사분면의 A, 대칭점 B, C(0, 10))대로 그림.
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from draw import HERE
from draw5 import LN, fit_shoot
from draw6 import geo
from draw2_3y import circ, dot, DOT, THIN


def toward(c, r, p):
    """중심 c, 반지름 r인 원 위에서 점 p 쪽(r>0) 또는 반대쪽(r<0)의 점"""
    dx, dy = p[0] - c[0], p[1] - c[1]
    n = math.hypot(dx, dy)
    return (c[0] + r * dx / n, c[1] + r * dy / n)


def fig_m2409():
    # 2024년 9월 고1 27번: A(a, 2), B(2, a), C(2, -a), a=4√2; 원 O(반지름 6)와 삼각형 AOC의 외접원
    a = 4 * math.sqrt(2)
    A, B, C = (a, 2), (2, a), (2, -a)
    F = geo((-6.6, 9.4), (-7.6, 8.6), 22, (20, 20, 60, 14))
    F.axes()
    circ(F, (0, 0), 6)
    circ(F, ((a + 2) / 2, (2 - a) / 2), 3 * math.sqrt(2))
    F.seg((-6.4, -6.4), (8.0, 8.0), LN)
    for p, q in ((B, C), (B, A), (A, C), ((0, 0), A), ((0, 0), C)):
        F.seg(p, q, LN)
    F.pt((0, 0), "O", "rb", -4, -4)
    F.pt(A, "A", "lb", 4, -2); F.pt(B, "B", "cb", 0, -6); F.pt(C, "C", "ct", 0, 7)
    F.lab((8.0, 8.0), "y=x", "lc", 4, 0, 20)
    return F.render()


def fig_m2209():
    # 2022년 9월 고1 17번: A(2, 3), B(-3, 1), x축 위의 점 C, 직선 y=x 위의 점 D
    A, B, C, D = (2.0, 3.0), (-3.0, 1.0), (-1.6, 0.0), (1.6, 1.6)
    F = geo((-4.2, 4.6), (-2.0, 4.0), 46, (20, 20, 50, 14))
    F.axes()
    F.seg((-1.9, -1.9), (3.6, 3.6), LN)
    F.seg(B, C, LN); F.seg(C, D, LN); F.seg(D, A, LN)
    F.pt((0, 0), "O", "lt", 4, 5)
    F.pt(A, "A", "cb", 0, -6); F.pt(B, "B", "cb", -2, -6); F.pt(C, "C", "ct", 0, 7); F.pt(D, "D", "lt", 4, 3)
    F.lab((3.6, 3.6), "y=x", "lc", 4, 0, 20)
    return F.render()


def fig_m2309():
    # 2023년 9월 고1 16번: C1 (x-8)²+(y-2)²=4, C2 (x-3)²+(y+4)²=4, x축 위의 P, y=x 위의 Q
    c1, c2 = (8.0, 2.0), (3.0, -4.0)
    P, Q = (5.4, 0.0), (-1.2, -1.2)
    A = toward(c1, -2, P)
    B = toward(c2, -2, Q)
    F = geo((-3.4, 11.4), (-6.8, 5.4), 20, (20, 20, 40, 14))
    F.axes()
    circ(F, c1, 2); circ(F, c2, 2)
    F.seg((-3.2, -3.2), (5.0, 5.0), LN)
    F.seg(A, P, LN); F.seg(P, Q, LN); F.seg(Q, B, LN)
    F.pt((0, 0), "O", "lt", 4, 5)
    F.pt(A, "A", "lb", 3, -3); F.pt(B, "B", "lt", 3, 3); F.pt(P, "P", "ct", 2, 7); F.pt(Q, "Q", "rb", -5, -2)
    F.lab((c1[0] + 2.1, c1[1]), "C_{1}", "lc", 4, 0, 20); F.lab((c2[0] + 2.1, c2[1] - 0.3), "C_{2}", "lc", 4, 0, 20)
    F.lab((5.0, 5.0), "y=x", "lc", 4, 0, 20)
    return F.render()


def fig_m2321():
    # 2023년 3월 고2 21번: 사분원의 호 x²+y²=25 (x≤0, y≥0), 호 위의 점 P, A(4, 2)
    F = geo((-6.4, 5.6), (-1.4, 6.2), 30, (20, 20, 20, 14))
    F.axes()
    F.curve(lambda x: math.sqrt(max(25 - x * x, 0)), -5, 0)
    P = (-5 * math.cos(math.radians(62)), 5 * math.sin(math.radians(62)))
    dot(F, P); dot(F, (4, 2))
    F.seg((0, 2), (4, 2), THIN, DOT); F.seg((4, 0), (4, 2), THIN, DOT)
    F.pt((0, 0), "O", "rt", -5, 5)
    F.pt(P, "P", "rb", -4, -3); F.pt((4, 2), "A", "lb", 4, -3)
    F.lab((-5, 0), "-5", "ct", 0, 6, 20); F.lab((4, 0), "4", "ct", 0, 6, 20)
    F.lab((0, 5), "5", "lc", 5, -2, 20); F.lab((0, 2), "2", "rc", -5, 0, 20)
    F.lab((-4.3, 3.0), "C", "rc", -5, 0, 22)
    return F.render()


def fig_m2410():
    # 2024년 10월 고1 21번: C1 (x-2)²+(y-6)²=1, C2 (x-6)²+(y-4)²=9
    F = geo((-0.6, 10.2), (-0.6, 8.4), 26, (24, 20, 24, 14))
    F.axes()
    circ(F, (2, 6), 1); circ(F, (6, 4), 3)
    F.pt((0, 0), "O", "rt", -5, 5)
    F.lab((2.6, 7.0), "C_{1}", "lb", 2, -2, 22); F.lab((7.6, 7.0), "C_{2}", "lb", 2, -2, 22)
    return F.render()


def fig_m2510():
    # 2025년 10월 고1 21번: 원점을 지나는 원 C1(중심 A, 제1사분면)과 원점에 대하여 대칭인 원 C2 (a=3/√5, b=6/√5)
    a, b = 3 / math.sqrt(5), 6 / math.sqrt(5)
    F = geo((-5.0, 5.4), (-6.0, 6.4), 24, (20, 20, 30, 14))
    F.axes()
    circ(F, (a, b), 3); circ(F, (-a, -b), 3)
    F.pt((0, 0), "O", "lt", 3, 5)
    F.lab((a + 2.2, b + 2.1), "C_{1}", "lb", 2, -2, 20)
    F.lab((-a - 2.3, -b - 2.1), "C_{2}", "rt", -2, 2, 20)
    return F.render()


def fig_m2603():
    # 2026년 3월 고2 14번: 원 C (x-7)²+(y-3)²=2, A(2, 0), 직선 y=x 위의 점 Q, 원 C 위의 점 P
    c, r = (7.0, 3.0), math.sqrt(2)
    Q = (3.6, 3.6)
    P = toward(c, r, (Q[0], Q[1] + 0.9))
    F = geo((-0.6, 9.4), (-0.8, 6.8), 34, (20, 20, 50, 14))
    F.axes()
    circ(F, c, r)
    F.seg((-0.4, -0.4), (6.0, 6.0), LN)
    F.seg((2, 0), Q, LN); F.seg(Q, P, LN)
    F.pt((0, 0), "O", "lt", 4, 5)
    F.pt((2, 0), "A", "ct", 0, 7); F.pt(Q, "Q", "rb", -5, -3); F.pt(P, "P", "cb", -3, -6)
    F.lab((c[0] + 1.1, c[1] + 1.2), "C", "lb", 3, -2, 22)
    F.lab((6.0, 6.0), "y=x", "lc", 4, 0, 20)
    return F.render()



def poly_line(F, pts, wd=None, extra=""):
    for p, q in zip(pts, pts[1:]):
        F.seg(p, q, wd or LN, extra)


def refl_pt(p, a, b):
    """점 p를 두 점 a, b를 지나는 직선에 대하여 대칭이동"""
    dx, dy = b[0] - a[0], b[1] - a[1]
    t = ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / (dx * dx + dy * dy)
    f = (a[0] + t * dx, a[1] + t * dy)
    return (2 * f[0] - p[0], 2 * f[1] - p[1])


def fig_n1629():
    # 백영고 2025 2학기 중간 논술형 2: 제4사분면의 격자점 A, 직선 y=x에 대한 대칭점 B, C(0, 10)
    A, B, C = (6.0, -4.0), (-4.0, 6.0), (0.0, 10.0)
    F = geo((-6.4, 9.4), (-6.4, 11.6), 17, (24, 20, 50, 20))
    F.axes()
    F.seg((-6.0, -6.0), (8.4, 8.4), LN)
    F.seg(A, B, LN); F.seg(B, C, LN); F.seg(C, A, LN)
    for p in (A, B, C):
        dot(F, p)
    F.pt((0, 0), "O", "rt", -4, 5)
    F.pt(A, "A", "lc", 6, 0); F.pt(B, "B", "rc", -6, 0); F.pt(C, "C", "lc", 7, 2)
    F.lab((0, 10), "10", "rc", -6, 2, 20)
    F.lab((8.4, 8.4), "y=x", "lc", 4, 0, 20)
    return F.render()


def fig_n1624():
    # 백영고 2025 2학기 중간: A(0, 1), 직선 l: y=-2x+6 위의 점 B, x축 위의 점 C
    A, B, C = (0.0, 1.0), (1.4, 3.2), (2.0, 0.0)
    F = geo((-0.9, 4.6), (-2.4, 8.4), 38, (20, 20, 30, 26))
    F.axes()
    F.seg((-0.5, 7.0), (4.0, -2.0), LN)
    F.seg(A, B, LN); F.seg(B, C, LN); F.seg(C, A, LN)
    F.pt((0, 0), "O", "rt", -4, 5)
    F.pt(A, "A", "rc", -6, 0); F.pt(B, "B", "lb", 4, -3); F.pt(C, "C", "ct", 0, 7)
    F.lab((0, 6), "6", "rc", -5, 0, 20); F.lab((3, 0), "3", "lb", 3, -3, 20)
    F.lab((4.0, -2.0), "l", "rt", -4, 2, 22)
    return F.render()


def fig_n1712():
    # 수리고 2025 2학기 중간: O, 직선 y=x 위의 A(10, 10), x축 위의 B(15, 0), 세 변 위의 C, D, E
    A, B = (10.0, 10.0), (15.0, 0.0)
    C, D, E = (5.2, 5.2), (12.6, 4.8), (6.6, 0.0)
    F = geo((-1.6, 18.4), (-1.6, 13.0), 16, (20, 20, 50, 14))
    F.axes()
    F.seg((-1.4, -1.4), (12.6, 12.6), LN)
    F.seg(A, B, LN)
    F.seg(C, D, LN); F.seg(D, E, LN); F.seg(E, C, LN)
    F.pt((0, 0), "O", "lt", 4, 5)
    F.pt(A, "A", "rb", -4, -4); F.pt(B, "B", "ct", 0, 7); F.pt(C, "C", "rb", -5, -3)
    F.pt(D, "D", "lc", 6, 0); F.pt(E, "E", "ct", 0, 7)
    F.lab((12.6, 12.6), "y=x", "lc", 4, 0, 20)
    return F.render()


def fig_n1750():
    # 안양고 2025 2학기 중간: 원 x²+y²=4, A(2, 0), B(√2, √2), 호 AB 위의 P, 선분 OB 위의 Q, 선분 OA 위의 R
    r2 = math.sqrt(2)
    B = (r2, r2)
    P = (2 * math.cos(math.radians(30)), 2 * math.sin(math.radians(30)))
    Q, R = (0.75, 0.75), (1.25, 0.0)
    F = geo((-4.4, 3.2), (-2.8, 3.0), 50, (20, 20, 30, 30))
    F.axes()
    circ(F, (0, 0), 2)
    F.seg((-2.6, -2.6), (2.7, 2.7), LN)
    F.seg(P, Q, LN); F.seg(Q, R, LN); F.seg(R, P, LN)
    F.pt((0, 0), "O", "lt", 4, 5)
    F.pt((2, 0), "A", "lb", 4, -3); F.pt(B, "B", "rb", -3, -5); F.pt(P, "P", "lb", 5, -2)
    F.pt(Q, "Q", "rb", -5, -3); F.pt(R, "R", "ct", 0, 7)
    F.lab((2, 0), "2", "lt", 4, 5, 20); F.lab((-2, 0), "-2", "rt", -3, 5, 20)
    F.lab((0, 2), "2", "lb", 4, -3, 20); F.lab((0, -2), "-2", "lt", 4, 4, 20)
    F.lab((-1.35, 1.85), "x^{2}+y^{2}=4", "rb", 0, 0, 20)
    F.lab((-2.6, -2.6), "y=x", "lt", 6, 0, 20)
    return F.render()


def fig_n1912():
    # 평촌고 2025 2학기 중간: 방정식 f(x, y)=0이 나타내는 도형(계단 모양)
    pts = [(3, 0), (3, 1), (4, 1), (4, 2), (5, 2), (5, 0), (3, 0)]
    F = geo((-0.9, 7.0), (-0.9, 3.2), 46, (20, 20, 30, 14))
    F.axes()
    F.seg((0, 2), (4, 2), THIN, DOT); F.seg((3, 1), (3, 2), THIN, DOT)
    poly_line(F, pts, 3.0)
    F.seg((4.8, 0), (4.8, 0.2), 1.6); F.seg((4.8, 0.2), (5, 0.2), 1.6)
    F.pt((0, 0), "O", "lt", 4, 6)
    F.lab((0, 2), "2", "rc", -6, 0, 20); F.lab((3, 0), "3", "ct", 0, 7, 20); F.lab((5, 0), "5", "ct", 0, 7, 20)
    F.lab((4.6, 2.5), "f(x,~y)=0", "cb", 0, -2, 20)
    return F.render()


def fig_g220():
    # 고쟁이 220: 점 A(3, 8)에서 출발하여 점 B에서 멈춤
    A, B = (3.0, 8.0), (12.0, 12.0)
    F = geo((-0.8, 14.0), (-0.8, 13.6), 14, (20, 20, 20, 26))
    F.axes()
    F.seg((0, 8), A, THIN, DOT); F.seg((3, 0), A, THIN, DOT)
    dot(F, A); dot(F, B)
    F.pt((0, 0), "O", "rt", -4, 5)
    F.pt(A, "A", "cb", 0, -6); F.pt(B, "B", "lc", 6, 0)
    F.lab((0, 8), "8", "rc", -5, 0, 20); F.lab((3, 0), "3", "ct", 0, 6, 20)
    return F.render()


def fig_g250():
    # 고쟁이 250: A(-1, 0), 원 (x+3)²+(y-8)²=5, y축 위의 P, 원 위의 Q
    c, r = (-3.0, 8.0), math.sqrt(5)
    P = (0.0, 3.6)
    Q = toward(c, r, (0.4, 6.0))
    F = geo((-16.0, 2.4), (-1.0, 11.0), 26, (20, 20, 20, 20))
    F.axes()
    circ(F, c, r); dot(F, c)
    F.seg(c, (0, 8), THIN, DOT); F.seg(c, (-3, 0), THIN, DOT)
    F.seg((-1, 0), P, LN); F.seg(P, Q, LN)
    dot(F, (-1, 0)); dot(F, P); dot(F, Q)
    F.pt((0, 0), "O", "lt", 4, 5)
    F.pt((-1, 0), "A", "rb", -4, -4); F.pt(P, "P", "lc", 6, 0); F.pt(Q, "Q", "lc", 6, 2)
    F.lab((-3, 0), "-3", "ct", 0, 6, 20); F.lab((-1, 0), "-1", "ct", 0, 6, 20); F.lab((0, 8), "8", "lc", 5, 0, 20)
    F.lab((-5.4, 5.6), "(x+3)^{2}+(y-8)^{2}=5", "rt", 0, 0, 20)
    return F.render()


def fig_g252():
    # 고쟁이 252: 폭 10 m인 도로(회색)를 사이에 두고 건물 A(아래), B(위)
    A, B = (0.0, 0.0), (20.0, 25.0)
    F = geo((-12.0, 26.0), (-3.0, 28.0), 9, (60, 16, 40, 14))
    F.poly([(-10, 10), (25, 10), (25, 20), (-10, 20)], "#bbbbbb")
    F.seg(A, (0, 10), LN); F.seg(B, (20, 20), LN); F.seg(A, B, LN)
    for p, sgn in (((0, 10), -1), ((20, 20), 1)):
        k = 0.9
        F.seg((p[0], p[1] + sgn * k), (p[0] + k, p[1] + sgn * k), 1.6); F.seg((p[0] + k, p[1] + sgn * k), (p[0] + k, p[1]), 1.6)
    for p in (A, B):
        X, Y = F.P(*p)
        F.svg.append('<rect x="%.1f" y="%.1f" width="14" height="14" fill="#fff" stroke="#000" stroke-width="1.6"/>' % (X - 7, Y - 7))
    F.pt(A, "A", "rc", -10, 0); F.pt(B, "B", "rc", -10, 0)
    F.lab((-10, 15), "10\\,\\mathrm{m}", "rc", -4, 0, 20)
    F.lab((0, 5), "10\\,\\mathrm{m}", "rc", -5, 0, 20); F.lab((20, 22.5), "5\\,\\mathrm{m}", "lc", 5, 0, 20)
    F.lab((10, 12.5), "5\\sqrt{41}\\,\\mathrm{m}", "lt", 10, 22, 20)
    return F.render()


def fig_g260():
    # 고쟁이 260: 직사각형 ABCD(AB=1, BC=2)를 접어 점 A가 변 CD 위의 E로
    e = 2 / 3
    G, H = ((e * e + 3) / 4, 0.0), ((e * e - 2 * e + 5) / 4, 1.0)
    Fp = refl_pt((0.0, 0.0), G, H)
    off = 3.4
    F = geo((-0.5, 6.0), (-0.6, 1.4), 80, (20, 16, 24, 14))
    poly_line(F, [(0, 0), (2, 0), (2, 1), (0, 1), (0, 0)])
    dot(F, (2, e))
    for p, n, an in (((0, 1), "A", "rc"), ((0, 0), "B", "rc"), ((2, 0), "C", "lc"), ((2, 1), "D", "lc"), ((2, e), "E", "lc")):
        F.pt(p, n, an, -6 if an == "rc" else 6, 0)
    F.lab((2.7, 0.5), "\\Rightarrow", "cc", 0, 0, 30)
    S = lambda p: (p[0] + off, p[1])
    F.seg(S((0, 1)), S(H), THIN, DOT); F.seg(S((0, 1)), S((0, 0)), THIN, DOT); F.seg(S((0, 0)), S(G), THIN, DOT)
    poly_line(F, [S(H), S((2, 1)), S((2, 0)), S(G), S(H)])
    poly_line(F, [S(G), S(Fp), S((2, e))])
    for p, n, an, dx, dy in (((0, 1), "A", "rc", -6, 0), ((0, 0), "B", "rc", -6, 0), ((2, 0), "C", "lc", 6, 0), ((2, 1), "D", "lc", 6, 0),
                             ((2, e), "E", "lc", 6, 0), (H, "H", "cb", 0, -6), (G, "G", "rt", -2, 5), (Fp, "F", "ct", 0, 7)):
        F.pt(S(p), n, an, dx, dy)
    return F.render()


def fig_o27():
    # 올림포스 고난도 공통수학2 03 27번: 정사각형 OABC와 O, P(-2, 0), Q(-2, -2), R(0, -2)
    F = geo((-3.0, 3.4), (-3.0, 3.2), 40, (20, 20, 20, 26))
    F.axes()
    poly_line(F, [(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)])
    poly_line(F, [(0, 0), (-2, 0), (-2, -2), (0, -2), (0, 0)])
    F.pt((0, 0), "O", "lt", 4, 5)
    F.pt((2, 0), "A", "lb", 4, -3); F.pt((2, 2), "B", "lb", 4, -3); F.pt((0, 2), "C", "lb", 4, -3)
    F.pt((-2, 0), "P", "rb", -4, -3); F.pt((-2, -2), "Q", "rt", -4, 3); F.pt((0, -2), "R", "lt", 4, 4)
    F.lab((2, 0), "2", "lt", 4, 5, 20); F.lab((0, 2), "2", "rc", -5, 0, 20)
    F.lab((-2, 0), "-2", "lt", 3, 5, 20); F.lab((0, -2), "-2", "lb", 5, -4, 20)
    return F.render()

FIGS = (("c2_4_m2409.png", fig_m2409, 8000), ("c2_4_m2209.png", fig_m2209, 8000), ("c2_4_m2309.png", fig_m2309, 8500),
        ("c2_4_m2321.png", fig_m2321, 7500), ("c2_4_m2410.png", fig_m2410, 7000), ("c2_4_m2510.png", fig_m2510, 7000),
        ("c2_4_m2603.png", fig_m2603, 8000),
        ("c2_4_n1629.png", fig_n1629, 7000), ("c2_4_n1624.png", fig_n1624, 5000), ("c2_4_n1712.png", fig_n1712, 8000),
        ("c2_4_n1750.png", fig_n1750, 7000), ("c2_4_n1912.png", fig_n1912, 7000), ("c2_4_g220.png", fig_g220, 6000),
        ("c2_4_g250.png", fig_g250, 9500), ("c2_4_g252.png", fig_g252, 8000), ("c2_4_g260.png", fig_g260, 9000),
        ("c2_4_o27.png", fig_o27, 6000))

if __name__ == "__main__":
    for name, fn, wd in FIGS:
        if len(sys.argv) > 1 and name not in sys.argv[1:]:
            continue
        fit_shoot(name, fn, wd, HERE)
