# -*- coding: utf-8 -*-
"""유형서 11단원(조합) 그림. python 그림/draw11y.py [파일 ...]  (KATEX_DIR 필요)
- u11_par.png: n71 — 평행한 두 직선 위의 점 4개, 5개
- u11_lat43.png / u11_lat53.png / u11_lat33.png: n927·n837·n121 — 같은 간격으로 놓인 점 4×3, 5×3, 3×3
- u11_c12.png: n596 — 원 위에 일정한 간격으로 놓인 12개의 점
- u11_box7.png: 2026년 9월 고1 20번 — 1부터 7까지 적힌 7개의 상자
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from draw import HERE
from draw5 import fit_shoot
from draw6 import geo
from draw10 import poly_line, LN
from draw10y import dot


def fig_par():
    F = geo((0, 10), (0, 3), 50, (14, 14, 14, 14))
    F.seg((0, 2.6), (10, 2.6)); F.seg((0, 0.4), (10, 0.4))
    for x in (2, 4, 6, 8):
        dot(F, (x, 2.6), 5)
    for x in (1.5, 3.25, 5, 6.75, 8.5):
        dot(F, (x, 0.4), 5)
    return F.render()


def lattice(nx, ny):
    def fn():
        F = geo((-0.3, nx - 0.7), (-0.3, ny - 0.7), 70, (12, 12, 12, 12))
        for x in range(nx):
            for y in range(ny):
                dot(F, (x, y), 5.5)
        return F.render()
    return fn


def fig_c12():
    F = geo((-1.2, 1.2), (-1.2, 1.2), 140, (12, 12, 12, 12))
    X, Y = F.P(0, 0)
    F.svg.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="#000" stroke-width="%s"/>' % (X, Y, F.sx, LN))
    for k in range(12):
        a = math.pi / 2 - 2 * math.pi * k / 12
        dot(F, (math.cos(a), math.sin(a)), 5)
    return F.render()


def fig_box7():
    F = geo((0, 14), (0, 1.6), 40, (12, 12, 12, 12))
    for i in range(7):
        x = i * 2
        poly_line(F, [(x + 0.2, 0), (x + 1.8, 0), (x + 1.8, 1.4), (x + 0.2, 1.4)])
        F.lab((x + 1, 0.7), str(i + 1), "cc")
    return F.render()


FIGS = (("u11_par.png", fig_par, 9000), ("u11_lat43.png", lattice(4, 3), 9000),
        ("u11_lat53.png", lattice(5, 3), 9000), ("u11_lat33.png", lattice(3, 3), 9000),
        ("u11_c12.png", fig_c12, 9000), ("u11_box7.png", fig_box7, 10000))

if __name__ == "__main__":
    for name, fn, wd in FIGS:
        if len(sys.argv) > 1 and name not in sys.argv[1:]:
            continue
        fit_shoot(name, fn, wd, HERE)
