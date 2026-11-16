# -*- coding: utf-8 -*-
"""공통수학2 유형서 12단원(무리식과 무리함수) 완성본(2026-11-16)에 붙여 넣은 스캔 그림을 그림 규칙대로 다시 그림.  python draw2_12y.py [파일 ...]
(번호는 미주 644부터로 맞춘 뒤 번호)
- c2y12_659  : 659번 문제 y=−√(ax+b)+c (시작점 (−2, 1), y절편 −1 → y=−√(2x+4)+1)
- c2y12_662p : 662번 문제 y=a/(x+b)+c (점근선 x=1, y=2, 점 (0, 3))
- c2y12_662s : 662번 해설 y=√(−x−1)+2 (시작점 (−1, 2))
- c2y12_672  : 672번 해설 f(x)=14/(x+3)−2, y=√(x+64/9), y=√(x−k), y=√(x−4) (경계 두 곡선은 점선, 개형 k=−2)
- c2y12_677  : 677번 해설 y=−√(−2x+1)+2 (끝점 (1/2, 2))
- c2y12_678  : 678번 해설 y=−√(2x+4)+3 (시작점 (−2, 3))
- c2y12_693  : 693번 문제 y=√x 위의 P(a, b), Q(c, d)와 직선 PQ (개형 b=1.5, d=3.1)
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from draw import HERE, STROKE
from draw5 import Frame, fit_shoot
from draw10y import dot

DASH = 'stroke-dasharray="5,4"'


def fn(F, f, x0, x1, extra="", n=400):
    pts = [(x0 + (x1 - x0) * i / n, f(x0 + (x1 - x0) * i / n)) for i in range(n + 1)]
    F.svg.append('<polyline points="%s" fill="none" stroke="#000" stroke-width="%s" stroke-linejoin="round" %s/>'
                 % (" ".join("%.1f,%.1f" % F.P(*p) for p in pts), STROKE, extra))


def dash(F, p, q):
    F.seg(p, q, 1.5, DASH)


def sq(v):
    return math.sqrt(max(v, 0))


def y659():
    f = lambda x: -sq(2 * x + 4) + 1
    F = Frame((-3.0, 4.0), (-3.4, 2.0), 50, 50, (16, 12, 200, 12)); F.axes()
    fn(F, f, -2, 3.6)
    dash(F, (-2, 1), (-2, 0)); dash(F, (-2, 1), (0, 1))
    F.pt((0, 0), "O", "rt", -4, 4)
    F.lab((-2, 0), "-2", "rt", -4, 4); F.lab((0, 1), "1", "lb", 6, -2); F.lab((0, -1), "-1", "rt", -6, 2)
    F.lab((3.6, f(3.6)), r"y=-\sqrt{ax+b}+c", "lc", 8, 0)
    return F.render()


def y662p():
    f = lambda x: 2 - 1 / (x - 1)
    F = Frame((-2.4, 4.6), (-1.4, 5.6), 46, 46, (200, 12, 16, 12)); F.axes()
    dash(F, (1, 5.4), (1, -1.2)); dash(F, (-2.2, 2), (4.4, 2))
    fn(F, f, -2.2, 1 - 1 / 3.4); fn(F, f, 1 + 1 / 3.2, 4.4)
    F.pt((0, 0), "O", "rt", -4, 4)
    F.lab((1, 0), "1", "lt", 4, 4); F.lab((0, 3), "3", "rb", -5, -4); F.lab((0, 2), "2", "rb", -5, -3)
    F.lab((-2.2, f(-2.2)), r"y=\dfrac{a}{x+b}+c", "rc", -8, 0)
    return F.render()


def y662s():
    f = lambda x: sq(-x - 1) + 2
    F = Frame((-5.6, 2.2), (-1.0, 4.6), 46, 46, (16, 12, 16, 12)); F.axes()
    fn(F, f, -5.4, -1)
    dash(F, (-1, 2), (-1, 0)); dash(F, (-1, 2), (0, 2))
    F.pt((0, 0), "O", "lt", 4, 4)
    F.lab((-1, 0), "-1", "ct", 0, 6); F.lab((0, 2), "2", "lc", 6, 0)
    return F.render()


def y672():
    f = lambda x: 14 / (x + 3) - 2
    F = Frame((-8.0, 9.0), (-6.8, 5.6), 36, 50, (180, 34, 150, 12)); F.axes()
    dash(F, (-3, 5.4), (-3, -6.6)); dash(F, (-7.8, -2), (8.8, -2))
    fn(F, f, -3 + 14 / 7.4, 8.8); fn(F, f, -7.8, -3 - 14 / 4.6)
    fn(F, lambda x: sq(x + 64 / 9), -64 / 9, 7.6, DASH)
    fn(F, lambda x: sq(x + 2), -2, 7.6)
    fn(F, lambda x: sq(x - 4), 4, 8.8, DASH)
    dot(F, (4, 0), 4); dot(F, (0, 8 / 3), 4)
    F.pt((0, 0), "O", "lt", 4, 4)
    F.lab((-3, 0), "-3", "rt", -4, 4); F.lab((4, 0), "4", "rb", -2, -6); F.lab((0, -2), "-2", "lt", 5, 3)
    F.lab((0, 8 / 3), r"\dfrac{8}{3}", "rt", -10, 2)
    F.lab((7.6, sq(7.6 + 64 / 9)), r"y=\sqrt{x+\dfrac{64}{9}}", "lc", 6, -22)
    F.lab((7.6, sq(9.6)), r"y=\sqrt{x-k}", "lc", 6, 10)
    F.lab((8.8, sq(4.8)), r"y=\sqrt{x-4}", "lc", 6, 14)
    F.lab((-8.0, 5.2), r"y=\dfrac{-2x+8}{x+3}", "rc", -4, 0); F.seg((-7.9, 5.1), (-0.45, f(-0.45)), 1.2)
    return F.render()


def y677():
    f = lambda x: -sq(-2 * x + 1) + 2
    F = Frame((-4.4, 1.6), (-1.6, 3.0), 56, 56, (16, 12, 16, 30)); F.axes()
    fn(F, f, -4.2, 0.5)
    dash(F, (0.5, 2), (0.5, 0)); dash(F, (0.5, 2), (0, 2))
    F.pt((0, 0), "O", "rt", -4, 4)
    F.lab((0.5, 0), r"\dfrac{1}{2}", "lt", 4, 4); F.lab((0, 2), "2", "rc", -6, 0)
    return F.render()


def y678():
    f = lambda x: -sq(2 * x + 4) + 3
    F = Frame((-3.0, 6.0), (-2.4, 4.0), 46, 46, (16, 12, 16, 12)); F.axes()
    fn(F, f, -2, 5.8)
    dash(F, (-2, 3), (-2, 0)); dash(F, (-2, 3), (0, 3))
    F.pt((0, 0), "O", "rt", -4, 4)
    F.lab((-2, 0), "-2", "rt", -4, 4); F.lab((0, 3), "3", "lc", 6, 0)
    return F.render()


def y693():
    b, d = 1.5, 3.1
    a, c = b * b, d * d
    m = (d - b) / (c - a)
    F = Frame((-0.8, 11.4), (-0.8, 4.4), 40, 60, (40, 12, 16, 12)); F.axes()
    fn(F, sq, 0, 11.2)
    F.seg((-0.7, b + m * (-0.7 - a)), (11.2, b + m * (11.2 - a)), 2.0)
    for (x, y) in ((a, b), (c, d)):
        dot(F, (x, y), 4); dash(F, (x, y), (x, 0)); dash(F, (x, y), (0, y))
    F.pt((0, 0), "O", "rt", -4, 4)
    F.lab((a, 0), "a", "ct", 0, 6); F.lab((c, 0), "c", "ct", 0, 6); F.lab((0, b), "b", "rc", -6, 0); F.lab((0, d), "d", "rc", -6, 0)
    F.pt((a, b), "P", "rb", -2, -8); F.pt((c, d), "Q", "lt", 6, 8)
    F.lab((3.6, 3.75), r"y=\sqrt{x}", "cc", 0, 0); F.seg((3.9, 3.5), (4.6, sq(4.6) + 0.08), 1.2)
    return F.render()


FIGS = [("c2y12_659.png", y659, 10000), ("c2y12_662p.png", y662p, 10000), ("c2y12_662s.png", y662s, 9000),
        ("c2y12_672.png", y672, 15000), ("c2y12_677.png", y677, 9000), ("c2y12_678.png", y678, 9000), ("c2y12_693.png", y693, 10000)]

if __name__ == "__main__":
    for name, fnc, wd in FIGS:
        if len(sys.argv) > 1 and name not in sys.argv[1:]:
            continue
        print(name, fit_shoot(name, fnc, wd, HERE))
