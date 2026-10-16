# -*- coding: utf-8 -*-
"""유형서 11단원(조합) 그림. python 그림/draw11y.py [파일 ...]  (KATEX_DIR 필요)
- u11_par.png: n71 — 평행한 두 직선 위의 점 4개, 5개
- u11_lat43.png / u11_lat53.png / u11_lat33.png: n927·n837·n121 — 같은 간격으로 놓인 점 4×3, 5×3, 3×3
- u11_c12.png: n596 — 원 위에 일정한 간격으로 놓인 12개의 점
- u11_box7.png: 2026년 9월 고1 20번 — 1부터 7까지 적힌 7개의 상자
- u11_g44.png / u11_cube.png / u11_zig.png / u11_arch.png: 최단 거리 — 4×4 도로망과 P, 정육면체 24개의 직육면체(4×3×2), 비스듬한 도로망과 C, D, ㄷ자 도로망과 P
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



def fig_g44():
    F = geo((0, 4), (0, 4), 60, (44, 44, 44, 44))
    for k in range(5):
        F.seg((k, 0), (k, 4)); F.seg((0, k), (4, k))
    for q in ((0, 0), (4, 4), (1, 2)):
        dot(F, q, 5)
    F.pt((0, 0), "A", "rc", -14, 10); F.pt((4, 4), "B", "lc", 14, 0); F.pt((1, 2), "P", "rb", -10, -10)
    return F.render()


def fig_cube():
    a, b, c = 4, 2, 3                       # 가로, 깊이, 높이
    ox, oy = 0.55, 0.45                     # 깊이 방향 한 칸의 비스듬한 이동
    F = geo((0, a + b * ox), (0, c + b * oy), 60, (44, 44, 44, 44))
    P = lambda x, y, z: (x + z * ox, y + z * oy)
    for x in range(a + 1):
        F.seg(P(x, 0, 0), P(x, c, 0)); F.seg(P(x, c, 0), P(x, c, b))
    for y in range(c + 1):
        F.seg(P(0, y, 0), P(a, y, 0)); F.seg(P(a, y, 0), P(a, y, b))
    for z in range(b + 1):
        F.seg(P(0, c, z), P(a, c, z)); F.seg(P(a, 0, z), P(a, c, z))
    dot(F, P(0, 0, 0), 5); dot(F, P(a, c, b), 5)
    F.pt(P(0, 0, 0), "A", "rc", -14, 8); F.pt(P(a, c, b), "B", "lc", 14, 0)
    return F.render()


ZIG = ({0: (0, 4), 1: (0, 4), 2: (2, 4), 3: (2, 6), 4: (3, 6)},           # j가 같은 선: i의 범위
       {0: (0, 1), 1: (0, 1), 2: (0, 3), 3: (0, 4), 4: (0, 4), 5: (3, 4), 6: (3, 4)})   # i가 같은 선: j의 범위


def fig_zig():
    Q = lambda i, j: (i + j, 0.8 * (j - i))
    F = geo((0, 10), (-3.2, 0.8), 60, (44, 44, 44, 44))
    for j, (lo, hi) in ZIG[0].items():
        F.seg(Q(lo, j), Q(hi, j))
    for i, (lo, hi) in ZIG[1].items():
        F.seg(Q(i, lo), Q(i, hi))
    for n, ij, anc, dx, dy in (("A", (0, 0), "rc", -14, 0), ("B", (6, 4), "lc", 14, 0), ("C", (4, 0), "ct", 0, 14), ("D", (4, 4), "lb", 10, -10)):
        dot(F, Q(*ij), 5); F.pt(Q(*ij), n, anc, dx, dy)
    return F.render()


def fig_arch():
    F = geo((0, 5), (0, 3), 60, (44, 44, 44, 44))
    for x in (0, 1, 3, 4, 5):
        F.seg((x, 0), (x, 3))
    F.seg((2, 2), (2, 3))
    for y in (0, 1):
        F.seg((0, y), (1, y)); F.seg((3, y), (5, y))
    for y in (2, 3):
        F.seg((0, y), (5, y))
    for q in ((0, 0), (5, 0), (2, 3)):
        dot(F, q, 5)
    F.pt((0, 0), "A", "rc", -14, 8); F.pt((5, 0), "B", "lc", 14, 8); F.pt((2, 3), "P", "cb", 0, -14)
    return F.render()


FIGS = (("u11_par.png", fig_par, 9000), ("u11_lat43.png", lattice(4, 3), 9000),
        ("u11_lat53.png", lattice(5, 3), 9000), ("u11_lat33.png", lattice(3, 3), 9000),
        ("u11_c12.png", fig_c12, 9000), ("u11_box7.png", fig_box7, 10000),
        ("u11_g44.png", fig_g44, 9000), ("u11_cube.png", fig_cube, 9000), ("u11_zig.png", fig_zig, 10000),
        ("u11_arch.png", fig_arch, 9000))

if __name__ == "__main__":
    for name, fn, wd in FIGS:
        if len(sys.argv) > 1 and name not in sys.argv[1:]:
            continue
        fit_shoot(name, fn, wd, HERE)
