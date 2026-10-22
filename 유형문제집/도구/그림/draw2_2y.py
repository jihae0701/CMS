# -*- coding: utf-8 -*-
"""공통수학2 유형서 2단원(직선의 방정식) 그림. python 그림/draw2_2y.py [파일 ...]  (KATEX_DIR 필요)
학력평가 원문 그림(HIT기출 3회, 고쟁이 044)을 같은 모양으로 새로 그렸다.
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from draw import HERE, STROKE
from draw5 import Frame, fit_shoot
from draw6 import geo, right_mark, PINK

DOT = 'stroke-dasharray="5,5" stroke-width="1.3"'


def fig_m0903():
    # 2009년 3월 고2 14번: 세 점 O(0, 0), A(6, 2), B(-2, 4)
    A, B = (6, 2), (-2, 4)
    F = Frame((-3.2, 7.4), (-0.9, 5.2), 36, 36, (20, 20, 20, 16))
    F.axes()
    F.seg((0, 0), A, STROKE)
    F.seg((0, 0), B, STROKE)
    for p in (A, B):
        F.seg((p[0], 0), p, 1.3, DOT)
        F.seg((0, p[1]), p, 1.3, DOT)
    F.pt((0, 0), "O", "rt", -5, 5)
    F.pt(A, "A", "lb", 6, -4); F.pt(B, "B", "rb", -6, -4)
    F.lab((-2, 0), "-2", "ct", 0, 6, 20); F.lab((6, 0), "6", "ct", 0, 6, 20)
    F.lab((0, 2), "2", "rc", -7, 0, 20); F.lab((0, 4), "4", "lc", 7, 0, 20)
    return F.render()


def fig_m2309a():
    # 2023년 9월 고1 14번: 직선 l(두 점 (6, 0), (0, 3)을 지남) 위의 B, C와 정사각형 ABCD, A(3, 6)
    A = (3.0, 6.0)
    u = (2 / math.sqrt(5), -1 / math.sqrt(5))          # 직선 l의 방향
    side = 9 / math.sqrt(5)
    t = (A[0] + 2 * A[1] - 6) / 5                       # 점 A에서 직선 x+2y-6=0에 내린 수선의 발 B
    B = (A[0] - t, A[1] - 2 * t)
    C = (B[0] + side * u[0], B[1] + side * u[1])
    D = (A[0] + side * u[0], A[1] + side * u[1])
    F = Frame((-1.0, 8.6), (-0.8, 7.0), 40, 40, (34, 20, 20, 16))
    F.axes()
    F.seg((-0.9, 3.45), (7.4, -0.7), STROKE)                   # l: y = 3 - x/2
    for p, q in ((A, B), (B, C), (C, D), (D, A)):
        F.seg(p, q, STROKE)
    F.pt((0, 0), "O", "rt", -5, 5)
    F.pt(A, "A", "cb", 0, -7); F.pt(B, "B", "rt", -4, 6); F.pt(C, "C", "lb", 15, -2); F.pt(D, "D", "lc", 8, 0)
    F.lab((-0.9, 3.45), "l", "rc", -6, 0, 22)
    return F.render()


def fig_m2309b():
    # 2023년 9월 고1 17번: ∠A=∠B=90°, AB=4, BC=8인 사다리꼴 ABCD, AD를 2:1로 내분하는 점 P, AC⊥BP인 점 Q
    A, B, C, D = (0, 4), (0, 0), (8, 0), (3, 4)
    P, Q = (2, 4), (1.6, 3.2)
    F = geo((-0.6, 8.6), (-0.7, 4.7), 46, (20, 20, 20, 16))
    F.poly([A, Q, D], PINK)
    for p, q in ((A, B), (B, C), (C, D), (D, A), (A, C), (B, P), (Q, D)):
        F.seg(p, q, STROKE)
    right_mark(F, A, B, D, 0.32); right_mark(F, B, A, C, 0.32); right_mark(F, Q, A, B, 0.3)
    F.pt(A, "A", "cb", 0, -7); F.pt(P, "P", "cb", 0, -7); F.pt(D, "D", "cb", 0, -7)
    F.pt(B, "B", "ct", 0, 7); F.pt(C, "C", "ct", 0, 7); F.pt(Q, "Q", "lt", 6, 6)
    return F.render()


def fig_m2409a():
    # 2024년 9월 고1 26번: l1: x-2y-2=0과 평행한 l2, A, B(l1의 절편), C, D(l2의 절편), 사각형 ADCB
    A, B, C, D = (2, 0), (0, -1), (-8, 0), (0, 4)
    F = Frame((-9.6, 7.0), (-2.6, 6.4), 30, 30, (20, 20, 36, 16))
    F.axes()
    F.seg((-3.0, -2.5), (6.4, 2.2), STROKE)                # l1: y = x/2 - 1
    F.seg((-9.4, -0.7), (4.6, 6.3), STROKE)                       # l2: y = x/2 + 4
    for p, q in ((A, D), (D, C), (C, B), (B, A)):
        F.seg(p, q, STROKE)
    F.pt((0, 0), "O", "rb", -5, -4)
    F.pt(A, "A", "ct", 2, 8); F.pt(B, "B", "lt", 6, 6); F.pt(C, "C", "ct", 0, 8); F.pt(D, "D", "rb", -6, -4)
    F.lab((6.4, 2.2), "l_{1}", "lc", 6, 0, 22); F.lab((4.6, 6.3), "l_{2}", "lc", 6, 0, 22)
    return F.render()


FIGS = (("c2_2_m0903.png", fig_m0903, 10000), ("c2_2_m2309a.png", fig_m2309a, 10500),
        ("c2_2_m2309b.png", fig_m2309b, 11500), ("c2_2_m2409a.png", fig_m2409a, 12000))

if __name__ == "__main__":
    for name, fn, wd in FIGS:
        if len(sys.argv) > 1 and name not in sys.argv[1:]:
            continue
        fit_shoot(name, fn, wd, HERE)
