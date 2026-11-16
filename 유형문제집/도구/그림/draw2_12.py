# -*- coding: utf-8 -*-
"""공통수학2 기본서 12단원(무리식과 무리함수) 완성본(2026-11-16)에 붙여 넣은 스캔 그림을 그림 규칙대로 다시 그림.  python draw2_12.py [파일 ...]
- c2b12_c1 : 개념 ⑴ y=√(ax)의 그래프 (a<0, a>0)
- c2b12_c2 : 개념 ⑵ y=−√(ax)의 그래프 (a<0, a>0)
- c2b12_470a : 470번 해설 y=√(x+4)−3, y=√(−x+4)+3
- c2b12_470b : 470번 해설 두 곡선과 x=−4, x=4로 둘러싸인 도형 — S₁(하늘)을 S₂(하늘) 자리로 옮기면 가로 8, 세로 6인 직사각형(연두)
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from draw import HERE, STROKE
from draw5 import Frame, fit_shoot
from draw10y import dot

SKY, GREEN, PINK = "#d6ecfb", "#dcf3d2", "#ffd9e6"
DASH = 'stroke-dasharray="5,4"'


def fn(F, f, x0, x1, extra="", n=300):
    pts = [(x0 + (x1 - x0) * i / n, f(x0 + (x1 - x0) * i / n)) for i in range(n + 1)]
    F.svg.append('<polyline points="%s" fill="none" stroke="#000" stroke-width="%s" stroke-linejoin="round" %s/>'
                 % (" ".join("%.1f,%.1f" % F.P(*p) for p in pts), STROKE, extra))


def dash(F, p, q):
    F.seg(p, q, 1.5, DASH)


def tagbox(F, p, text, fill):
    """a<0, a>0 이름표: 연한 색 둥근 상자"""
    X, Y = F.P(*p)
    F.svg.append('<rect x="%.1f" y="%.1f" width="76" height="34" rx="16" fill="%s" stroke="#000" stroke-width="1.2"/>' % (X - 38, Y - 17, fill))
    F.lab(p, text, "cc", 0, 0)


def c1():
    F = Frame((-4.6, 4.6), (-0.7, 3.4), 40, 40, (16, 12, 16, 12)); F.axes()
    fn(F, lambda x: math.sqrt(-0.8 * x), -4.4, 0); fn(F, lambda x: math.sqrt(0.8 * x), 0, 4.4)
    F.pt((0, 0), "O", "rt", -4, 4)
    tagbox(F, (-3.4, 2.95), "a<0", SKY); tagbox(F, (3.4, 2.95), "a>0", PINK)
    return F.render()


def c2():
    F = Frame((-4.6, 4.6), (-3.4, 1.3), 40, 40, (16, 12, 16, 12)); F.axes()
    fn(F, lambda x: -math.sqrt(-0.8 * x), -4.4, 0); fn(F, lambda x: -math.sqrt(0.8 * x), 0, 4.4)
    F.pt((0, 0), "O", "lb", 6, -4)
    tagbox(F, (-3.4, -2.95), "a<0", SKY); tagbox(F, (3.4, -2.95), "a>0", PINK)
    return F.render()


f470 = lambda x: math.sqrt(x + 4) - 3
g470 = lambda x: math.sqrt(-x + 4) + 3


def b470a():
    F = Frame((-5.4, 7.6), (-4.0, 6.8), 36, 40, (200, 12, 150, 30)); F.axes()
    fn(F, f470, -4, 6.4); fn(F, g470, -5.2, 4)
    dot(F, (-4, -3), 4); dot(F, (4, 3), 4)
    dash(F, (-4, -3), (-4, 0)); dash(F, (-4, -3), (0, -3)); dash(F, (4, 3), (4, 0)); dash(F, (4, 3), (0, 3))
    F.pt((0, 0), "O", "rt", -4, 4)
    F.lab((-4, 0), "-4", "cb", 0, -6); F.lab((4, 0), "4", "rb", -3, -4); F.lab((5, 0), "5", "lb", 3, -4)
    F.lab((0, 5), "5", "rt", -6, 4); F.lab((0, 3), "3", "rc", -6, 0); F.lab((0, -1), "-1", "lt", 6, 4); F.lab((0, -3), "-3", "lc", 6, 0)
    F.lab((-4, -3), r"y=\sqrt{x+4}-3", "rc", -10, 0); F.lab((4, 3), r"y=\sqrt{-x+4}+3", "lb", 8, -6)
    return F.render()


def b470b():
    F = Frame((-6.0, 7.4), (-4.8, 6.8), 40, 40, (190, 12, 190, 30))
    xs = [-4 + 8 * i / 200 for i in range(201)]
    F.poly([(-4, 3)] + [(x, g470(x)) for x in xs] + [(4, 3)], SKY)                       # S1
    F.poly([(-4, -3)] + [(x, f470(x)) for x in xs] + [(4, -3)], SKY)                     # S2
    F.poly([(-4, 3), (4, 3)] + [(x, f470(x)) for x in reversed(xs)], GREEN)              # 직사각형에서 S2를 뺀 부분
    F.axes()
    fn(F, f470, -4, 6.0); fn(F, g470, -4.0, 4)
    for x in (-4, 4):
        F.seg((x, -4.4), (x, 6.6), 1.6)
    for y in (3, -3):
        F.seg((-5.6, y), (6.0, y), 1.6)
    F.pt((0, 0), "O", "rb", -4, -4)
    F.lab((-4, 0), "-4", "lb", 4, -4); F.lab((4, 0), "4", "rb", -4, -4); F.lab((5, 0), "5", "lt", 3, 4)
    F.lab((0, 3), "3", "lb", 5, -3); F.lab((0, -3), "-3", "lt", 5, 3)
    F.lab((-2.6, 4.25), "S_{1}", "cc"); F.lab((-2.0, -2.45), "S_{2}", "cc")
    F.svg.append('<path d="M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" fill="none" stroke="#000" stroke-width="1.3" marker-end="url(#ar)"/>'
                 % (F.P(-3.1, 4.0) + F.P(-4.9, 0.6) + F.P(-2.6, -2.35)))
    F.lab((6.0, 3), "y=3", "lc", 6, 0); F.lab((6.0, -3), "y=-3", "lc", 6, 0)
    F.lab((-4, -4.4), "x=-4", "ct", 0, 6); F.lab((4, -4.4), "x=4", "ct", 0, 6)
    F.lab((6.0, f470(6.0)), r"y=\sqrt{x+4}-3", "lb", 2, -10); F.lab((-4, g470(-4)), r"y=\sqrt{-x+4}+3", "rc", -10, 0)
    return F.render()


FIGS = [("c2b12_c1.png", c1, 10000), ("c2b12_c2.png", c2, 10000), ("c2b12_470a.png", b470a, 13000), ("c2b12_470b.png", b470b, 14000)]

if __name__ == "__main__":
    for name, fnc, wd in FIGS:
        if len(sys.argv) > 1 and name not in sys.argv[1:]:
            continue
        print(name, fit_shoot(name, fnc, wd, HERE))
