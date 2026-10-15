# -*- coding: utf-8 -*-
"""기본서 11단원(조합) 그림. python 그림/draw11.py [파일 ...]  (KATEX_DIR 필요)
- g11_lattice.png: 05 대표문제 — 좌표평면 위의 9개의 점 (x, y = 1, 2, 3)
- g11_seg.png: 05 유제 — 한 점에서 만나는 두 선분 AB(점 5개), CD(점 4개) 위의 8개의 점
- g11_oct.png / g11_dec.png: 05 — 원주를 8등분, 10등분한 점 P₁~P₈, P₁~P₁₀
- g11_sq17.png: 05 대표문제 — 합동인 정사각형 17개(위 4, 가운데 6, 아래 7, 오른쪽 맞춤)
- g11_sq19.png: 05 유제 — 합동인 정사각형 19개(3×5 직사각형 오른쪽 아래에 2×2)
- g11_bracket.png: STEP 3 — 8개 학급의 대진표(3팀 쪽: 1 대 (2), 5팀 쪽: (2) 대 (1 대 (2)))
- g11_grid33.png: STEP 3 — 제1열~제3열의 3×3 빈칸
- g11_tetra.png: STEP 3 — 정사면체의 세 모서리에 5개씩 찍은 점
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from draw import HERE
from draw5 import fit_shoot
from draw6 import geo
from draw10 import poly_line, text, LN
from draw10y import dot

DASH = 'stroke-dasharray="5,4"'


def fig_lattice():
    F = geo((-0.5, 4.0), (-0.5, 4.0), 60, (24, 18, 18, 24))
    F.axes()
    for k in (1, 2, 3):
        F.seg((k, 0), (k, 3), 1.2, DASH); F.seg((0, k), (3, k), 1.2, DASH)
        F.lab((k, 0), str(k), "ct", 0, 6); F.lab((0, k), str(k), "rc", -7, 0)
    for x in (1, 2, 3):
        for y in (1, 2, 3):
            dot(F, (x, y), 5)
    F.lab((0, 0), r"\mathrm{O}", "rt", -4, 4)
    return F.render()


def fig_seg():
    F = geo((0, 10), (0, 6), 44, (40, 26, 40, 26))
    A, B = (0, 1), (10, 3.5)
    X = (5, 1 + 2.5 * 0.5)
    C = (3.2, 5.6)
    D = (X[0] + (X[0] - C[0]) * 0.55, X[1] + (X[1] - C[1]) * 0.55)
    F.seg(A, B); F.seg(C, D)
    for t in (0, 0.25, 0.5, 0.75, 1):
        dot(F, (A[0] + (B[0] - A[0]) * t, A[1] + (B[1] - A[1]) * t), 5)
    for t in (0, 1 / 3, 1):
        p = (C[0] + (X[0] - C[0]) * t, C[1] + (X[1] - C[1]) * t)
        dot(F, p, 5)
    dot(F, D, 5)
    F.pt(A, "A", "rc", -12, 0); F.pt(B, "B", "lc", 12, 0); F.pt(C, "C", "rb", -8, -6); F.pt(D, "D", "lt", 8, 6)
    return F.render()


def circle_pts(n):
    def fn():
        F = geo((-1.5, 1.5), (-1.5, 1.5), 120, (16, 16, 16, 16))
        X, Y = F.P(0, 0)
        F.svg.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="#000" stroke-width="%s"/>' % (X, Y, F.sx, LN))
        for k in range(n):
            a = math.pi / 2 - 2 * math.pi * k / n
            p = (math.cos(a), math.sin(a))
            dot(F, p, 5)
            F.lab((1.28 * p[0], 1.28 * p[1]), r"\mathrm{P}_{%d}" % (k + 1), "cc")
        return F.render()
    return fn


def squares(cells, s):
    def fn():
        xs = [x for x, y in cells]; ys = [y for x, y in cells]
        F = geo((min(xs), max(xs) + 1), (min(ys), max(ys) + 1), s, (12, 12, 12, 12))
        for x, y in cells:
            poly_line(F, [(x, y), (x + 1, y), (x + 1, y + 1), (x, y + 1)])
        return F.render()
    return fn


SQ17 = [(x, 2) for x in range(3, 7)] + [(x, 1) for x in range(1, 7)] + [(x, 0) for x in range(0, 7)]
SQ19 = [(x, y) for x in range(3) for y in range(5)] + [(x, y) for x in (3, 4) for y in range(2)]


def fig_bracket():
    F = geo((-0.6, 7.6), (-0.9, 4.6), 52, (12, 12, 12, 12))
    def tie(x1, y1, x2, y2, top):
        F.seg((x1, y1), (x1, top)); F.seg((x2, y2), (x2, top)); F.seg((x1, top), (x2, top))
        return ((x1 + x2) / 2, top)
    for x in range(8):
        poly_line(F, [(x - 0.32, -0.8), (x + 0.32, -0.8), (x + 0.32, -0.1), (x - 0.32, -0.1)])
    L = [(x, -0.1) for x in range(8)]
    a = tie(*L[1], *L[2], 0.9)                 # 왼쪽: 1 대 (2)
    left = tie(*L[0], *a, 1.9)
    b = tie(*L[3], *L[4], 0.9)                 # 오른쪽: (2) 대 (1 대 (2))
    c = tie(*L[6], *L[7], 0.9)
    d = tie(*L[5], *c, 1.9)
    right = tie(*b, *d, 2.9)
    top = tie(*left, *right, 4.0)
    F.seg(top, (top[0], 4.5))
    return F.render()


def fig_grid33():
    F = geo((-1.4, 3), (0, 3.7), 60, (14, 12, 14, 12))
    for c in range(3):
        for r in range(3):
            poly_line(F, [(c, r), (c + 1, r), (c + 1, r + 1), (c, r + 1)])
        text(F, (c + 0.5, 3.35), "제%d열" % (c + 1))
    for r in range(3):
        text(F, (-0.2, 2.5 - r), "제%d행" % (r + 1), "rc")
    return F.render()


def fig_tetra():
    F = geo((0, 8), (0, 8.2), 44, (12, 12, 12, 12))
    T, P, Q, R = (4.2, 8.0), (0.3, 1.6), (5.4, 0.2), (7.7, 2.6)
    for p, q in ((T, P), (T, Q), (T, R), (P, Q), (Q, R)):
        F.seg(p, q)
    F.seg(P, R, LN, DASH)
    for E in (P, Q, R):
        for k in range(1, 6):
            t = k / 6
            dot(F, (T[0] + (E[0] - T[0]) * t, T[1] + (E[1] - T[1]) * t), 5)
    return F.render()


FIGS = (("g11_lattice.png", fig_lattice, 9000), ("g11_seg.png", fig_seg, 9500),
        ("g11_oct.png", circle_pts(8), 9000), ("g11_dec.png", circle_pts(10), 9000),
        ("g11_sq17.png", squares(SQ17, 60), 10000), ("g11_sq19.png", squares(SQ19, 60), 9000),
        ("g11_bracket.png", fig_bracket, 10000), ("g11_grid33.png", fig_grid33, 9000),
        ("g11_tetra.png", fig_tetra, 9000))

if __name__ == "__main__":
    for name, fn, wd in FIGS:
        if len(sys.argv) > 1 and name not in sys.argv[1:]:
            continue
        fit_shoot(name, fn, wd, HERE)
