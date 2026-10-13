# -*- coding: utf-8 -*-
"""기본서 9단원(연립부등식) 그림. python 그림/draw9.py [파일 ...]  (KATEX_DIR 필요)
- g9_roots.png: 개념 — 이차방정식의 근의 위치(a>0): ⑴ 두 근이 모두 p보다 큼 ⑵ 모두 p보다 작음 ⑶ 두 근 사이에 p ⑷ 두 근이 모두 p, q 사이
- g9_tri.png: 06 유제(고등수매씽 1511) — AB=BC=12인 직각이등변삼각형 안의 직사각형 PQBR (P의 위치는 개형)
- g9_ocba.png: STEP 3(2020년 9월 고1) — y=-x²+2kx+k²+4의 그래프와 사각형 OCBA (그림은 k=1.5)
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from draw import HERE
from draw5 import Frame, roots, fit_shoot
from draw8 import ARROW, xaxis
from draw6 import geo, right_mark, dim_arc
from draw import STROKE

DASH = 'stroke-dasharray="5,4"'


def fig_roots():
    F = Frame((0, 22.6), (-1.75, 2.75), 46, 46, (10, 10, 10, 10))
    F.svg.append(ARROW)
    for c, ps, cap, ax in ((2.6, (-1.8,), "⑴", True), (8.3, (1.8,), "⑵", True),
                           (14.0, (0.35,), "⑶", False), (19.7, (-1.8, 1.8), "⑷", True)):
        f = lambda t, c=c: 0.75 * (t - c) ** 2 - 0.75
        xaxis(F, c - 2.4, c + 2.8)
        F.curve(f, roots(f, c - 3, c, 2.5)[0], roots(f, c, c + 3, 2.5)[0])
        F.lab((c - 1, 0), r"\alpha", "rt", -3, 4); F.lab((c + 1, 0), r"\beta", "lt", 3, 4)
        if ax:
            F.seg((c, -0.75), (c, 2.3), 1.3, DASH)
        for d, nm in zip(ps, "pq"):
            p = c + d
            F.seg((p, 0), (p, f(p)), 1.3, DASH)
            F.lab((p, 0), nm, "ct", 0, 6) if f(p) > 0 else F.lab((p, 0), nm, "cb", 0, -5)
        F.lab((c, -1.25), cap, "ct", 0, 0)
    return F.render()


def fig_tri():
    F = geo((-2, 14), (-3.2, 13), 16, (80, 22, 30, 16))
    A, B, C = (0, 12), (0, 0), (12, 0)
    P, Q, R = (5, 7), (0, 7), (5, 0)
    for p, q in ((A, B), (B, C), (C, A)):
        F.seg(p, q, STROKE)
    F.seg(Q, P); F.seg(P, R)
    right_mark(F, B, A, C, 0.75); right_mark(F, Q, A, P, 0.75); right_mark(F, R, P, C, 0.75)
    dim_arc(F, B, A, "12", -1, 46, cut=True)
    dim_arc(F, B, C, "12", 1, 30, cut=True)
    F.pt(A, "A", "cb", 0, -6); F.pt(B, "B", "rt", -6, 4); F.pt(C, "C", "lc", 7, 0)
    F.pt(P, "P", "lb", 5, -3); F.pt(Q, "Q", "rc", -6, 0); F.pt(R, "R", "lb", 20, -3)
    return F.render()


def fig_ocba():
    k = 1.5
    f = lambda t: -t * t + 2 * k * t + k * k + 4
    F = Frame((-2.3, 6.0), (-1.6, 9.8), 34, 21, (20, 12, 70, 12))
    F.axes()
    F.curve(f, roots(f, -4, k, -1.3)[0], roots(f, k, 8, -1.3)[0])
    yA = k * k + 4
    F.seg((-2.1, yA), (5.6, yA), 1.6)
    F.seg((2 * k, yA), (2 * k, 0), 1.6)
    right_mark(F, (2 * k, 0), (2 * k, yA), (0, 0), 0.32)
    F.pt((0, 0), "O", "rt", -4, 4)
    F.pt((0, yA), "A", "rb", -4, -3); F.pt((2 * k, yA), "B", "lb", 4, -3); F.pt((2 * k, 0), "C", "ct", 0, 5)
    return F.render()


FIGS = (("g9_roots.png", fig_roots, 21000), ("g9_tri.png", fig_tri, 9000), ("g9_ocba.png", fig_ocba, 9000))

if __name__ == "__main__":
    for name, fn, wd in FIGS:
        if len(sys.argv) > 1 and name not in sys.argv[1:]:
            continue
        fit_shoot(name, fn, wd, HERE)
