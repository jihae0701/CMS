# -*- coding: utf-8 -*-
"""기본서 10단원(경우의 수와 순열) 그림. python 그림/draw10.py [파일 ...]  (KATEX_DIR 필요)
- g10_color1.png: 01 대표문제 — 영역 5개(D가 A, B, C, E와 이웃)
- g10_color2.png: 01 유제 — 영역 5개(B가 A, C, D, E와 이웃, E는 B와만 이웃)
- g10_chair6.png / g10_chair7.png: 04 — 나란히 놓인 의자 6개 / 7개(위에서 본 모양)
- g10_ride5.png: 05 대표문제 — 한 줄에 2개씩 5줄인 놀이기구 의자
- g10_ride23.png: 05 유제 — 앞줄 2개, 뒷줄 3개인 놀이기구 의자
- g10_stairs.png: STEP 3 — 크기가 같은 정사각형 6개를 계단 모양으로 붙인 도형
- g10_trisq.png: STEP 3 — 정삼각형 1개와 일렬로 붙은 정사각형 3개
- g10_grid24.png: STEP 3 — 8칸(2×4)으로 나누어진 직사각형
- g10_grid23.png: STEP 3 — 1열, 2열, 3열에 2칸씩인 빈칸 6개
- g10_round.png: STEP 3 — 둥근 의자와 사각 의자가 교대로 3개씩(위에서 본 모양)
- g10_seat23.png: STEP 3 — 2열로 3개씩인 좌석 6개
- g10_seat24.png: STEP 3 — 2열로 4개씩인 좌석 8개
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from draw import HERE
from draw5 import fit_shoot
from draw6 import geo

LN = 2.0


def poly_line(F, pts, wd=LN):
    F.svg.append('<polygon points="%s" fill="none" stroke="#000" stroke-width="%s" stroke-linejoin="round"/>'
                 % (" ".join("%.1f,%.1f" % F.P(*p) for p in pts), wd))


def rrect(F, x, y, w, h, r=0.12, wd=LN, fill="none"):
    """수학 좌표 (x, y)가 왼쪽 아래인 둥근 직사각형"""
    X, Y = F.P(x, y + h)
    W, H = w * F.sx, h * F.sy
    F.svg.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%.1f" fill="%s" stroke="#000" stroke-width="%s"/>'
                 % (X, Y, W, H, r * F.sx, fill, wd))


def seat(F, x, y, s=1.0):
    """위에서 본 의자: 앉는 판(둥근 사각형)과 위쪽 등받이"""
    rrect(F, x, y, s, s * 0.82, 0.14)
    rrect(F, x - 0.04 * s, y + s * 0.82, s * 1.08, s * 0.22, 0.08, fill="#d6ecfb")


def text(F, p, t, anc="cc", dx=0, dy=0):
    F.lab(p, r"\text{%s}" % t, anc, dx, dy)


def fig_color1():
    F = geo((0, 10), (0, 5), 40, (12, 12, 12, 12))
    poly_line(F, [(0, 0), (10, 0), (10, 5), (0, 5)])
    a = lambda y: 1.8 + (5 - y) * 0.28           # A와 나머지의 경계 (위 1.8 → 아래 3.2)
    e = lambda y: 8.2 - (5 - y) * 0.24           # 나머지와 E의 경계 (위 8.2 → 아래 7.0)
    F.seg((a(5), 5), (a(0), 0)); F.seg((e(5), 5), (e(0), 0))
    F.seg((a(2.2), 2.2), (e(2.2), 2.2))
    F.seg((5.3, 5), (5.05, 2.2))
    for p, n in (((1.1, 2.5), "A"), ((3.6, 3.6), "B"), ((6.7, 3.6), "C"), ((5.1, 1.1), "D"), ((8.9, 2.5), "E")):
        F.pt(p, n, "cc", 0, 0)
    return F.render()


def fig_color2():
    F = geo((0, 10), (0, 5), 40, (12, 12, 12, 12))
    poly_line(F, [(0, 0), (10, 0), (10, 5), (0, 5)])
    a = lambda y: 2.2 + (5 - y) * 0.2
    F.seg((a(5), 5), (a(0), 0))
    F.seg((a(2.4), 2.4), (10, 2.4))
    F.seg((7.3, 5), (10, 3.3))
    F.seg((6.6, 2.4), (6.6, 0))
    for p, n in (((1.3, 2.5), "A"), ((5.0, 3.7), "B"), ((9.2, 4.45), "E"), ((4.6, 1.2), "D"), ((8.3, 1.2), "C")):
        F.pt(p, n, "cc", 0, 0)
    return F.render()


def chairs(n):
    def fn():
        F = geo((0, n * 1.5 - 0.5), (0, 1.05), 44, (14, 14, 14, 14))
        for i in range(n):
            seat(F, i * 1.5, 0)
        return F.render()
    return fn


def fig_ride5():
    F = geo((-1.6, 2.6), (0, 8.4), 40, (14, 14, 14, 14))
    for r in range(5):
        y = 6.8 - r * 1.7
        seat(F, 0, y); seat(F, 1.3, y)
        text(F, (-0.35, y + 0.5), "%d줄" % (r + 1), "rc")
    return F.render()


def fig_ride23():
    F = geo((-1.8, 4.3), (0, 3.4), 44, (14, 14, 14, 14))
    for i in range(2):
        seat(F, 0.65 + i * 1.4, 1.9)
    for i in range(3):
        seat(F, i * 1.4, 0)
    text(F, (-0.35, 2.4), "앞줄", "rc"); text(F, (-0.35, 0.5), "뒷줄", "rc")
    return F.render()


def fig_stairs():
    F = geo((0, 3), (0, 3), 66, (12, 12, 12, 12))
    for c, r in ((0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (0, 2)):
        poly_line(F, [(c, r), (c + 1, r), (c + 1, r + 1), (c, r + 1)])
    return F.render()


def fig_trisq():
    F = geo((0, 3), (0, 1 + math.sqrt(3) / 2), 70, (12, 12, 12, 12))
    for c in range(3):
        poly_line(F, [(c, 0), (c + 1, 0), (c + 1, 1), (c, 1)])
    poly_line(F, [(1, 1), (2, 1), (1.5, 1 + math.sqrt(3) / 2)])
    return F.render()


def fig_grid24():
    F = geo((0, 4), (0, 2), 60, (12, 12, 12, 12))
    for c in range(4):
        for r in range(2):
            poly_line(F, [(c, r), (c + 1, r), (c + 1, r + 1), (c, r + 1)])
    return F.render()


def fig_grid23():
    F = geo((0, 3), (-0.55, 2), 66, (12, 12, 12, 12))
    for c in range(3):
        for r in range(2):
            poly_line(F, [(c, r), (c + 1, r), (c + 1, r + 1), (c, r + 1)])
        text(F, (c + 0.5, -0.3), "%d열" % (c + 1))
    return F.render()


def fig_round():
    F = geo((0, 8.6), (0, 1.1), 40, (14, 14, 14, 14))
    for i in range(6):
        x = i * 1.5
        if i % 2 == 0:
            X, Y = F.P(x + 0.55, 0.55)
            F.svg.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="#000" stroke-width="%s"/>'
                         % (X, Y, 0.55 * F.sx, LN))
        else:
            rrect(F, x, 0, 1.1, 1.1, 0.06)
    return F.render()


def seat_rows(ncol):
    def fn():
        F = geo((-1.6, ncol * 1.4 - 0.4), (0, 3.2), 44, (14, 14, 14, 14))
        for r, y in ((1, 1.9), (2, 0)):
            for i in range(ncol):
                seat(F, i * 1.4, y)
            text(F, (-0.35, y + 0.5), "%d열" % r, "rc")
        return F.render()
    return fn


FIGS = (("g10_color1.png", fig_color1, 9000), ("g10_color2.png", fig_color2, 9000),
        ("g10_chair6.png", chairs(6), 9500), ("g10_chair7.png", chairs(7), 10000),
        ("g10_ride5.png", fig_ride5, 5200), ("g10_ride23.png", fig_ride23, 9000),
        ("g10_stairs.png", fig_stairs, 9000), ("g10_trisq.png", fig_trisq, 9000),
        ("g10_grid24.png", fig_grid24, 9000), ("g10_grid23.png", fig_grid23, 9000),
        ("g10_round.png", fig_round, 9000), ("g10_seat23.png", seat_rows(3), 9000),
        ("g10_seat24.png", seat_rows(4), 9000))

if __name__ == "__main__":
    for name, fn, wd in FIGS:
        if len(sys.argv) > 1 and name not in sys.argv[1:]:
            continue
        fit_shoot(name, fn, wd, HERE)
