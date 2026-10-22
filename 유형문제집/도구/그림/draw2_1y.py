# -*- coding: utf-8 -*-
"""공통수학2 유형서 1단원(평면좌표) 그림. python 그림/draw2_1y.py [파일 ...]  (KATEX_DIR 필요)
사용자가 준 학력평가 문항 사진·캡처의 그림을 같은 모양으로 새로 그렸다(2021년 3월 고2 27번, 2020년 9월 고1 2문항은 2026-10-22 원문 대조 때 추가).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from draw import HERE, STROKE
from draw5 import Frame, fit_shoot
from draw6 import geo, right_mark
import math


def fig_m0809():
    # 2008년 9월 고1 13번: 한 변 4인 정사각형 ABCD 안의 한 변 2인 정사각형 EFGH (AB ∥ EF)
    A, B, C, D = (0, 4), (0, 0), (4, 0), (4, 4)
    x0, y0 = 0.95, 1.15
    E, F_, G, H = (x0, y0 + 2), (x0, y0), (x0 + 2, y0), (x0 + 2, y0 + 2)
    F = geo((-0.45, 4.45), (-0.45, 4.45), 62, (16, 16, 16, 16))
    for p, q in ((A, B), (B, C), (C, D), (D, A), (E, F_), (F_, G), (G, H), (H, E), (A, E), (B, F_), (C, G), (D, H)):
        F.seg(p, q, STROKE)
    F.pt(A, "A", "rb", -6, -4); F.pt(B, "B", "rt", -6, 4); F.pt(C, "C", "lt", 6, 4); F.pt(D, "D", "lb", 6, -4)
    F.pt(E, "E", "lt", 11, 11); F.pt(F_, "F", "lb", 11, -11); F.pt(G, "G", "rb", -11, -11); F.pt(H, "H", "rt", -11, 11)
    F.lab((x0 / 2, 2.15), "S_{1}", "cc", 0, 0, 22)
    F.lab((2.0, y0 / 2), "S_{2}", "cc", 0, 0, 22)
    F.lab(((x0 + 2 + 4) / 2, 2.15), "S_{3}", "cc", 0, 0, 22)
    F.lab((2.0, (y0 + 2 + 4) / 2), "S_{4}", "cc", 0, 0, 22)
    return F.render()


def fig_m0911():
    # 2009년 11월 고1 21번: y=-(x-1)^2+1, y=x^2, y=x 와 정사각형 ABCD (B, D는 y=x 위, 변은 축에 평행)
    b = (3 - 5 ** 0.5) / 2
    s = 5 ** 0.5 - 2
    A, B, C, D = (b, b + s), (b, b), (b + s, b), (b + s, b + s)
    F = Frame((-0.15, 1.45), (-0.15, 1.3), 330, 330, (20, 20, 20, 16))
    F.axes()
    F.curve(lambda x: x * x, -0.1, 1.13)
    F.curve(lambda x: -(x - 1) ** 2 + 1, -0.07, 1.42)
    F.seg((-0.12, -0.12), (1.2, 1.2))
    for p, q in ((A, B), (B, C), (C, D), (D, A)):
        F.seg(p, q, STROKE)
    F.pt((0, 0), "O", "lt", 5, 5)
    F.pt(A, "A", "rb", -8, -5); F.pt(B, "B", "ct", 0, 9); F.pt(C, "C", "lt", 10, 5); F.pt(D, "D", "cb", 0, -9)
    F.lab((1.13, 1.28), "y=x^{2}", "rc", -14, 0, 20)
    F.lab((1.2, 1.2), "y=x", "lc", 10, 0, 20)
    F.lab((0.72, 0.2), "y=-(x-1)^{2}+1", "lc", 0, 0, 20)
    return F.render()


def fig_m2103():
    # 2021년 3월 고2 27번: 곡선 y=x^2-2x와 직선 y=3x+k (k=14)의 교점 P(-2, 8), Q(7, 35) (세로는 줄여 그린 개형)
    k = 14
    F = Frame((-3.2, 8.6), (-4, 40), 30, 7.2, (20, 20, 130, 16))
    F.axes()
    F.curve(lambda x: x * x - 2 * x, -2.9, 7.4)
    F.seg((-2.9, 3 * -2.9 + k), (7.9, 3 * 7.9 + k), STROKE)
    F.pt((0, 0), "O", "rt", -5, 5)
    F.pt((-2, 8), "P", "rc", -10, 0); F.pt((7, 35), "Q", "lc", 10, 4)
    F.lab((7.9, 3 * 7.9 + k), "y=3x+k", "lc", 8, 0, 20)
    F.lab((6.0, 24.0), "y=x^{2}-2x", "lc", 16, 0, 20)
    return F.render()


def fig_m2009a():
    # 2020년 9월 고1: y=ax^2 (a=1/4)와 y=x/2+1의 교점 P, Q, PQ의 중점 M, M에서 y축에 내린 수선의 발 H
    a = 0.25
    x1, x2 = 1 - 5 ** 0.5, 1 + 5 ** 0.5
    P, Qp = (x1, x1 / 2 + 1), (x2, x2 / 2 + 1)
    M, H = ((x1 + x2) / 2, (P[1] + Qp[1]) / 2), (0, (P[1] + Qp[1]) / 2)
    F = Frame((-3.3, 4.3), (-0.9, 3.9), 64, 64, (20, 44, 110, 70))
    F.axes()
    F.curve(lambda x: a * x * x, -3.3, 3.85)
    F.seg((-3.2, -0.6), (4.2, 3.1), STROKE)
    F.seg(H, M, STROKE)
    right_mark(F, H, (0, 0), M, 0.16)
    F.pt((0, 0), "O", "rt", -5, 5)
    F.pt(P, "P", "rb", -6, -4); F.pt(Qp, "Q", "rb", -4, -6); F.pt(M, "M", "lt", 4, 6); F.pt(H, "H", "rc", -8, 0)
    F.lab((3.85, a * 3.85 ** 2), "y=ax^{2}", "lc", 10, 6, 20)
    F.lab((-3.2, -0.6), "y=\\dfrac{1}{2}x+1", "lt", 4, 8, 20)
    return F.render()


def fig_m2009b():
    # 2020년 9월 고1: A(0, a) (a=sqrt7), B(-3, 0), C(1, 0), ∠ABC의 이등분선이 AC의 중점 D를 지남
    A, B, C = (0, 7 ** 0.5), (-3, 0), (1, 0)
    D = ((A[0] + C[0]) / 2, (A[1] + C[1]) / 2)
    F = Frame((-3.8, 1.9), (-0.7, 3.3), 62, 62, (20, 20, 20, 16))
    F.axes()
    for p, q in ((A, B), (B, C), (C, A)):
        F.seg(p, q, STROKE)
    E = (B[0] + (D[0] - B[0]) * 1.25, B[1] + (D[1] - B[1]) * 1.25)
    F.seg(B, E, STROKE)
    # 같은 길이 표시(AD = DC)
    for m in (((A[0] + D[0]) / 2, (A[1] + D[1]) / 2), ((D[0] + C[0]) / 2, (D[1] + C[1]) / 2)):
        ux, uy = C[0] - A[0], C[1] - A[1]; n = math.hypot(ux, uy); nx, ny = -uy / n * 0.09, ux / n * 0.09
        F.seg((m[0] - nx, m[1] - ny), (m[0] + nx, m[1] + ny), 1.6)
    # 각의 크기가 같음 표시(∠ABD = ∠DBC): 작은 점 두 개
    t1, t2 = math.atan2(A[1], 3), math.atan2(D[1], D[0] + 3)
    for th in ((t1 + t2) / 2, t2 / 2):
        X, Y = F.P(B[0] + 0.55 * math.cos(th), B[1] + 0.55 * math.sin(th))
        F.svg.append('<circle cx="%.1f" cy="%.1f" r="2.6" fill="#000"/>' % (X, Y))
    F.pt(A, "A", "lb", 6, -4); F.pt(B, "B", "ct", 0, 7); F.pt(C, "C", "ct", 4, 7)
    F.pt((0, 0), "O", "rt", -4, 6)
    return F.render()


FIGS = (("c2_1_m0809.png", fig_m0809, 9000), ("c2_1_m0911.png", fig_m0911, 11000),
        ("c2_1_m2103.png", fig_m2103, 9500), ("c2_1_m2009a.png", fig_m2009a, 11000), ("c2_1_m2009b.png", fig_m2009b, 9000))

if __name__ == "__main__":
    for name, fn, wd in FIGS:
        if len(sys.argv) > 1 and name not in sys.argv[1:]:
            continue
        fit_shoot(name, fn, wd, HERE)
