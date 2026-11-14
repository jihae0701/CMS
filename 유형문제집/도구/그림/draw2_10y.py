# -*- coding: utf-8 -*-
"""공통수학2 유형서 10단원(합성함수와 역함수) 완성본(2026-11-14)에 붙여 넣은 스캔 그림을 그림 규칙대로 다시 그림.  python draw2_10y.py [파일 ...]  (KATEX_DIR 필요)
- c2y10_528 : 528번 문제 X→X 대응 1→4, 2→1, 3→2, 4→3
- c2y10_542 : 542번 해설 X→X 대응 1→3, 2→4, 3→5, 4→1, 5→2
- c2y10_558p / c2y10_558s : 558번 문제·해설 y=f(x), y=g(x), y=x와 점선(개형: a=1, b=2, c=3, d=4.4, f(x)=1.4+0.4x+0.2x², g(x)=f⁻¹(x)−1)
- c2y10_568 : 568번 해설 f(x)=−(x−1)²+2 (x≤1 실선, x>1 점선)
- c2y10_577p / c2y10_577s : 577번 문제 y=f(x), y=g(x) / 해설 y=f⁻¹(x), y=g⁻¹(x) (0≤x≤6 모눈)
- c2y10_587 : 587번 문제 y=f(x) (f(1)=2, f(2)=3, f(3)=6, f(4)=3, f(5)=2, f(6)=3, f(7)=6, f(8)=7, f(9)=6, f(10)=3, f(11)=2, f(12)=0)
- c2y10_589 : 589번 해설 y=f(x), y=g(x), y=h(x)와 삼각형 PQR (a=1)
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from draw import HERE, STROKE
from draw5 import Frame, fit_shoot
from draw10y import dot

DASH = 'stroke-dasharray="5,4"'
GRID = 'stroke-dasharray="3,3" stroke-opacity="0.55"'
PINK = "#ffd9e6"


def pl(F, pts, extra=""):
    F.svg.append('<polyline points="%s" fill="none" stroke="#000" stroke-width="%s" stroke-linejoin="round" %s/>'
                 % (" ".join("%.1f,%.1f" % F.P(*p) for p in pts), STROKE, extra))


def fn(F, f, x0, x1, extra="", n=300):
    pl(F, [(x0 + (x1 - x0) * i / n, f(x0 + (x1 - x0) * i / n)) for i in range(n + 1)], extra)


def dash(F, p, q):
    F.seg(p, q, 1.5, DASH)


def O(F, anc="rt", dx=-4, dy=4):
    F.pt((0, 0), "O", anc, dx, dy)


# ---------------------------------------------------------------- 대응 그림
ARW = ('<defs><marker id="am" viewBox="0 0 13 10" refX="12" refY="5" markerWidth="7.8" markerHeight="6" orient="auto">'
       '<path d="M13,5 L0.5,0.3 L2.5,5 L0.5,9.7 z" fill="#000"/></marker></defs>')


def mapping(n, f, nameX="X", nameY="X", fname="f"):
    gap = 1.0
    top = (n - 1) * gap
    F = Frame((-0.9, 4.9), (-0.9, top + 1.9), 46, 46, (12, 12, 12, 12))
    F.svg.append(ARW)
    for cx in (0, 4):
        cy, rx, ry = top / 2, 0.75, top / 2 + 0.75
        X, Y = F.P(cx, cy)
        F.svg.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="none" stroke="#000" stroke-width="2.0"/>' % (X, Y, rx * F.sx, ry * F.sy))
    for k in range(1, n + 1):
        y = top - (k - 1) * gap
        F.lab((0, y), str(k), "cc", 0, 0); F.lab((4, y), str(k), "cc", 0, 0)
    for k, v in f.items():
        y0, y1 = top - (k - 1) * gap, top - (v - 1) * gap
        (X0, Y0), (X1, Y1) = F.P(0.3, y0), F.P(3.7, y1)
        F.svg.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#000" stroke-width="1.5" marker-end="url(#am)"/>' % (X0, Y0, X1, Y1))
    yt = top + 1.3
    F.lab((0, yt), nameX, "cc", 0, 0, 23); F.lab((4, yt), nameY, "cc", 0, 0, 23)
    (X0, Y0), (X1, Y1) = F.P(0.7, yt), F.P(3.3, yt)
    F.svg.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#000" stroke-width="1.5" marker-end="url(#am)"/>' % (X0, Y0, X1, Y1))
    F.lab((2, yt), fname, "cb", 0, -6)
    return F.render()


def f528():
    return mapping(4, {1: 4, 2: 1, 3: 2, 4: 3})


def f542():
    return mapping(5, {1: 3, 2: 4, 3: 5, 4: 1, 5: 2})


# ---------------------------------------------------------------- 558
A_, B_, C_, D_ = 1.0, 2.0, 3.0, 4.4
f558 = lambda x: 1.4 + 0.4 * x + 0.2 * x * x
fi558 = lambda y: (-0.4 + math.sqrt(0.16 + 0.8 * (y - 1.4))) / 0.4
g558 = lambda x: fi558(x) - 1


def f558base(sol):
    F = Frame((-0.7, 6.0), (-0.9, 5.6), 50, 50, (16, 12, 110, 12)); F.axes()
    fn(F, f558, -0.65, 3.2)
    fn(F, g558, 1.62, 5.7)
    F.seg((-0.5, -0.5), (5.4, 5.4), 2.0)
    # 세로 점선
    for x, y in ((A_, B_), (B_, C_), (C_, D_), (D_, D_)):
        dash(F, (x, 0), (x, y))
    # 가로 점선 (해설: y축부터, 문제: 그래프에서부터)
    for y, x0, x1 in ((A_, A_, C_), (B_, A_, D_), (C_, B_, C_), (D_, C_, D_)):
        dash(F, (0 if sol else x0, y), (x1, y))
    F.lab((5.4, 5.4), "y=x", "lc", 4, 0)
    F.lab((3.2, f558(3.2)), "y=f(x)", "rc", -10, 0)
    F.lab((5.7, g558(5.7)), "y=g(x)", "lc", 6, 0)
    for v, s in ((A_, "a"), (B_, "b"), (C_, "c"), (D_, "d")):
        F.lab((v, 0), s, "ct", 6 if v == B_ else 0, 6)
        if sol:
            F.lab((0, v), s, "rc", -6, 0)
    return F


def f558p():
    F = f558base(False); O(F, "rb", -5, -5)
    return F.render()


def f558s():
    F = f558base(True); O(F, "lt", 4, 4)
    return F.render()


# ---------------------------------------------------------------- 568
def f568():
    f = lambda x: -(x - 1) ** 2 + 2
    F = Frame((-1.2, 3.6), (-2.8, 3.0), 50, 40, (16, 12, 80, 12)); F.axes()
    fn(F, f, -0.95, 1); fn(F, f, 1, 3.0, DASH)
    dash(F, (1, 2), (1, 0)); dash(F, (1, 2), (0, 2))
    F.pt((0, 0), "O", "lt", 4, 4)
    F.lab((1, 0), "1", "lt", 4, 4); F.lab((0, 2), "2", "rb", -5, -3)
    F.lab((1.6, f(1.6)), "y=f(x)", "lb", 6, -6)
    return F.render()


# ---------------------------------------------------------------- 577
def grid6(F):
    for k in range(1, 7):
        F.seg((k, 0), (k, 6), 1.2, GRID); F.seg((0, k), (6, k), 1.2, GRID)
    for k in range(1, 7):
        F.lab((k, 0), str(k), "ct", 0, 6); F.lab((0, k), str(k), "rc", -6, 0)
    O(F, "rt", -4, 4)


def f577p():
    F = Frame((-0.6, 7.0), (-0.6, 7.0), 40, 40, (16, 12, 110, 12)); F.axes(); grid6(F)
    pl(F, [(0, 0), (2, 1), (4, 5), (6, 6)]); pl(F, [(0, 6), (2, 5), (4, 1), (6, 0)])
    F.lab((6, 6), "y=f(x)", "lb", 4, -4); F.lab((6, 0.6), "y=g(x)", "lb", 10, -4)
    F.seg((6.15, 0.75), (5.55, 0.3), 1.2)
    return F.render()


def f577s():
    F = Frame((-0.6, 7.0), (-0.6, 7.0), 40, 40, (16, 12, 130, 12)); F.axes(); grid6(F)
    pl(F, [(0, 0), (1, 2), (5, 4), (6, 6)]); pl(F, [(0, 6), (1, 4), (5, 2), (6, 0)])
    F.lab((6, 6), "y=f^{-1}(x)", "lb", 4, -4); F.lab((6, 1.6), "y=g^{-1}(x)", "lb", 10, -4)
    F.seg((6.15, 1.75), (5.55, 1.1), 1.2)
    return F.render()


# ---------------------------------------------------------------- 587
P587 = [(0, 0, 2.6), (1, 2, 1.4), (2, 3, 0), (3, 6, 0), (4, 3, -2.2), (5, 2, 0), (6, 3, 2.0), (7, 6, 2.0), (8, 7, 0),
        (9, 6, -2.0), (10, 3, 0), (11, 2, -1.4), (12, 0, -2.6)]


def h587(x):
    if x <= 0:
        return 2.6 * x
    if x >= 12:
        return -2.6 * (x - 12)
    k = min(int(x), 11)
    x0, y0, m0 = P587[k]; x1, y1, m1 = P587[k + 1]
    t = x - x0
    return (2 * t ** 3 - 3 * t ** 2 + 1) * y0 + (t ** 3 - 2 * t ** 2 + t) * m0 + (-2 * t ** 3 + 3 * t ** 2) * y1 + (t ** 3 - t ** 2) * m1


def f587():
    F = Frame((-0.6, 13.4), (-1.3, 8.0), 30, 30, (16, 12, 30, 12)); F.axes()
    for k in range(1, 12):
        F.seg((k, 0), (k, P587[k][1]), 1.2, GRID)
    for y, x1 in ((2, 11), (3, 10), (6, 9), (7, 8)):
        F.seg((0, y), (x1, y), 1.2, GRID)
    fn(F, h587, -0.35, 12.35, n=1200)
    O(F, "rb", -5, -3)
    for k in range(1, 12):
        F.lab((k, 0), str(k), "ct", 0, 6)
    F.lab((12, 0), "12", "lb", 3, -4)
    for y in (2, 3, 6, 7):
        F.lab((0, y), str(y), "rc", -6, 0)
    F.lab((8, 7), "y=f(x)", "cb", 0, -8)
    return F.render()


# ---------------------------------------------------------------- 589 (a=1)
def f589():
    F = Frame((-0.9, 6.0), (-2.9, 3.6), 54, 50, (40, 12, 110, 12))
    F.poly([(2, 2), (4, 2), (3, 0)], PINK)
    F.axes()
    pl(F, [(1.2, 3.4), (2, 2), (4, 2), (4.7, 3.4)])        # f
    pl(F, [(-0.8, -2), (2, -2), (4, 2), (5.8, 2)])          # g
    pl(F, [(-0.8, 2), (2, 2), (4, -2), (5.8, -2)])          # h
    dash(F, (2, -2), (2, 2)); dash(F, (4, -2), (4, 2))
    O(F, "rt", -4, 4)
    F.lab((2, 0), "2a", "rt", -4, 6); F.lab((4, 0), "4a", "lt", 4, 6)
    F.lab((0, 2), "2a", "rb", -5, -4); F.lab((0, -2), "-2a", "rt", -5, 4)
    F.pt((2, 2), "R", "rt", -6, 6); F.pt((4, 2), "P", "lt", 6, 6); F.pt((3, 0), "Q", "lc", 12, 0)
    F.lab((3, 1.25), "3a", "cb", 0, 0); F.seg((3, 1.2), (3, 0.12), 1.2)
    F.lab((4.7, 3.4), "y=f(x)", "lc", 6, 0); F.lab((5.8, 2), "y=g(x)", "lb", -40, -6); F.lab((5.8, -2), "y=h(x)", "lt", -40, 6)
    return F.render()


FIGS = [("c2y10_528.png", f528, 6000), ("c2y10_542.png", f542, 6000), ("c2y10_558p.png", f558p, 10000),
        ("c2y10_558s.png", f558s, 10000), ("c2y10_568.png", f568, 8000), ("c2y10_577p.png", f577p, 9000),
        ("c2y10_577s.png", f577s, 9500), ("c2y10_587.png", f587, 13000), ("c2y10_589.png", f589, 10000)]

if __name__ == "__main__":
    for name, fnc, wd in FIGS:
        if len(sys.argv) > 1 and name not in sys.argv[1:]:
            continue
        print(name, fit_shoot(name, fnc, wd, HERE))
