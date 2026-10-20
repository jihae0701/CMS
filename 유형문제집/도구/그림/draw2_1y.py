# -*- coding: utf-8 -*-
"""공통수학2 유형서 1단원(평면좌표) 그림. python 그림/draw2_1y.py [파일 ...]  (KATEX_DIR 필요)
사용자가 준 학력평가 문항 캡처의 그림을 같은 모양으로 새로 그렸다.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from draw import HERE, STROKE
from draw5 import Frame, fit_shoot
from draw6 import geo


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


FIGS = (("c2_1_m0809.png", fig_m0809, 9000), ("c2_1_m0911.png", fig_m0911, 11000))

if __name__ == "__main__":
    for name, fn, wd in FIGS:
        if len(sys.argv) > 1 and name not in sys.argv[1:]:
            continue
        fit_shoot(name, fn, wd, HERE)
