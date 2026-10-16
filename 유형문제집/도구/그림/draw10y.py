# -*- coding: utf-8 -*-
"""유형서 10단원(경우의 수와 순열) 그림. python 그림/draw10y.py [파일 ...]  (KATEX_DIR 필요)
- u10_road.png: w1 — 네 지점 A, B, C, D를 잇는 도로망(A-B 2, B-D 2, A-C 3, C-D 1, B-C 2)
- u10_ring.png: w8 — 가운데 영역 E와 그 둘레의 네 영역 A, B, C, D(차례로 이웃)
- u10_venn.png: o53 — 세 원이 만드는 7개의 영역(번호 1~7)
- u10_strip.png: o54 — 일렬로 놓인 5개의 영역 A~E
- u10_boat.png: n470 — 한 줄에 3개씩 4줄인 보트 좌석
- u10_marble.png: 검은 구슬 4개, 흰 구슬 7개의 좌우 대칭 배열
- u10_vr.png: n442 — 한 줄에 3개씩 2줄인 체험 기구 의자
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from draw import HERE
from draw5 import fit_shoot
from draw6 import geo
from draw10 import poly_line, rrect, seat, text, LN


def bez(F, p, c, q, wd=LN):
    (x1, y1), (cx, cy), (x2, y2) = F.P(*p), F.P(*c), F.P(*q)
    F.svg.append('<path d="M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" fill="none" stroke="#000" stroke-width="%s"/>'
                 % (x1, y1, cx, cy, x2, y2, wd))


def roads(F, p, q, n, spread):
    """p, q를 잇는 길 n개: 가운데 선분과 양쪽으로 휜 곡선"""
    mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
    dx, dy = q[0] - p[0], q[1] - p[1]
    L = math.hypot(dx, dy)
    nx, ny = -dy / L, dx / L
    offs = [spread * (k - (n - 1) / 2) for k in range(n)]
    for o in offs:
        bez(F, p, (mx + nx * o * 2, my + ny * o * 2), q)


def dot(F, p, r=4.5):
    X, Y = F.P(*p)
    F.svg.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#000"/>' % (X, Y, r))


def fig_road():
    F = geo((0, 10), (0, 6), 40, (40, 40, 40, 40))
    A, B, C, D = (0, 3), (5, 6), (5, 0), (10, 3)
    roads(F, A, B, 2, 0.45); roads(F, B, D, 2, 0.45); roads(F, A, C, 3, 0.4); roads(F, C, D, 1, 0.4); roads(F, B, C, 2, 0.5)
    for p in (A, B, C, D):
        dot(F, p)
    F.pt(A, "A", "rc", -12, 0); F.pt(B, "B", "cb", 0, -9); F.pt(C, "C", "ct", 0, 9); F.pt(D, "D", "lc", 12, 0)
    return F.render()


def fig_ring():
    F = geo((0, 8), (0, 6), 44, (12, 12, 12, 12))
    poly_line(F, [(0, 0), (8, 0), (8, 6), (0, 6)])
    c = (4, 3)
    for corner in ((0, 0), (8, 0), (8, 6), (0, 6)):
        F.seg(corner, (c[0] + (corner[0] - 4) * 0.42, c[1] + (corner[1] - 3) * 0.42))
    X, Y = F.P(*c)
    w, h = 4 * 0.84 * F.sx, 3 * 0.84 * F.sy
    F.svg.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="#fff" stroke="#000" stroke-width="%s"/>'
                 % (X - w / 2, Y - h / 2, w, h, LN))
    for p, n in (((4, 5.3), "A"), ((7.2, 3), "B"), ((4, 0.7), "C"), ((0.8, 3), "D"), ((4, 3), "E")):
        F.pt(p, n, "cc", 0, 0)
    return F.render()


def fig_venn():
    F = geo((-3.3, 3.3), (-3.0, 3.4), 40, (12, 12, 12, 12))
    r = 1.85
    cs = [(0, 1.05), (-0.95, -0.55), (0.95, -0.55)]
    for x, y in cs:
        X, Y = F.P(x, y)
        F.svg.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="#000" stroke-width="%s"/>' % (X, Y, r * F.sx, LN))
    for p, n in (((0, 0), "1"), ((-0.95, 0.55), "2"), ((0, 2.1), "3"), ((0.95, 0.55), "4"),
                 ((1.85, -1.1), "5"), ((0, -1.15), "6"), ((-1.85, -1.1), "7")):
        F.lab(p, n, "cc")
    return F.render()


def fig_strip():
    F = geo((0, 10), (0, 1.6), 40, (12, 12, 12, 12))
    for i, n in enumerate("ABCDE"):
        poly_line(F, [(2 * i, 0), (2 * i + 2, 0), (2 * i + 2, 1.6), (2 * i, 1.6)])
        F.pt((2 * i + 1, 0.8), n, "cc", 0, 0)
    return F.render()


def seat_grid(rows, cols, labels):
    def fn():
        F = geo((-1.6 if labels else 0, cols * 1.4 - 0.4), (0, rows * 1.9 - 0.7), 44, (14, 14, 14, 14))
        for r in range(rows):
            y = (rows - 1 - r) * 1.9
            for i in range(cols):
                seat(F, i * 1.4, y)
            if labels:
                text(F, (-0.35, y + 0.5), "%d줄" % (r + 1), "rc")
        return F.render()
    return fn



def fig_marble():
    F = geo((-0.6, 10.6), (-0.6, 0.6), 60, (8, 8, 8, 8))
    for i, c in enumerate("WWWBBWBBWWW"):
        X, Y = F.P(i, 0)
        F.svg.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="#000" stroke-width="2"/>'
                     % (X, Y, 0.42 * F.sx, "#000" if c == "B" else "#fff"))
    return F.render()


FIGS = (("u10_road.png", fig_road, 9500), ("u10_ring.png", fig_ring, 9000), ("u10_venn.png", fig_venn, 9000),
        ("u10_strip.png", fig_strip, 10000), ("u10_boat.png", seat_grid(4, 3, True), 7300),
        ("u10_vr.png", seat_grid(2, 3, False), 9000), ("u10_marble.png", fig_marble, 10000))

if __name__ == "__main__":
    for name, fn, wd in FIGS:
        if len(sys.argv) > 1 and name not in sys.argv[1:]:
            continue
        fit_shoot(name, fn, wd, HERE)
