# -*- coding: utf-8 -*-
"""공통수학2 유형서 4단원(도형의 이동) 그림. python 그림/draw2_4y.py [파일 ...]  (KATEX_DIR 필요)
학력평가 원문 그림(2024년 10월 고1·2025년 10월 고1·2026년 3월 고2는 시험지 hml, 나머지는 HIT기출의 문제 그림)을
같은 모양으로 새로 그렸다(풀이용 보조선·점은 뺌).
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


FIGS = (("c2_4_m2409.png", fig_m2409, 8000), ("c2_4_m2209.png", fig_m2209, 8000), ("c2_4_m2309.png", fig_m2309, 8500),
        ("c2_4_m2321.png", fig_m2321, 7500), ("c2_4_m2410.png", fig_m2410, 7000), ("c2_4_m2510.png", fig_m2510, 7000),
        ("c2_4_m2603.png", fig_m2603, 8000))

if __name__ == "__main__":
    for name, fn, wd in FIGS:
        if len(sys.argv) > 1 and name not in sys.argv[1:]:
            continue
        fit_shoot(name, fn, wd, HERE)
