# -*- coding: utf-8 -*-
"""공통수학2 기본서 9단원(함수) 해설 그림 — 사용자 최종본(2026-11-14)에 붙여 넣은 스캔 그림을 그림 규칙대로 다시 그리고,
323번(절댓값 기호를 포함한 식의 그래프 8개)의 그래프를 모두 그린다.  python draw2_9.py [파일 ...]  (KATEX_DIR 필요)
- c2b9_323_1.png ~ c2b9_323_8.png : 323번 (1)~(8) 그래프 (한 칸씩, 해설에서 두 개씩 나란히)
- c2b9_314.png : 314번 f(x)=x²−5x+a (0≤x≤6), 치역 −1/4~b
- c2b9_327.png : 327번 |x|+2|y|=2(마름모)와 점 (1, 1)을 지나는 직선, m=0·m=−1 사이(경계 제외)
- c2b9_329.png : 329번 일대일대응 f(x)=ax+b, (−2, −7)~(3, 3)
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from draw import HERE, STROKE
from draw5 import Frame, fit_shoot
from draw10y import dot

PINK, SKY = "#ffd9e6", "#d6ecfb"
DASH = 'stroke-dasharray="5,4"'


def gline(F, pts, extra=""):
    d = " ".join("%.1f,%.1f" % F.P(*p) for p in pts)
    F.svg.append('<polyline points="%s" fill="none" stroke="#000" stroke-width="%s" stroke-linejoin="round" %s/>' % (d, STROKE, extra))


def dash(F, p, q):
    F.seg(p, q, 1.5, DASH)


def panel(xr, yr, s=30):
    return Frame(xr, yr, s, s, (34, 12, 18, 12))


def tag(F, n):
    X, Y = F.P(F.xr[0], F.yr[1])
    F.labels.append((X - 30, Y - 2, r"\text{(%d)}" % n, 21, "lt"))


def f1():
    F = panel((-1.2, 4.6), (-1.0, 4.4)); F.axes(); tag(F, 1)
    gline(F, [(-0.25, 3.25), (2, 1), (4.4, 3.4)])
    dash(F, (2, 1), (2, 0)); dash(F, (2, 1), (0, 1))
    F.pt((0, 0), "O", "rt", -4, 4); F.lab((2, 0), "2", "ct", 0, 6); F.lab((0, 1), "1", "rc", -6, 0); F.lab((0, 3), "3", "rc", -8, 12)
    return F.render()


def f2():
    F = panel((-1.4, 3.2), (-1.0, 4.4)); F.axes(); tag(F, 2)
    gline(F, [(-1.3, 1), (1, 1), (2.6, 4.2)])
    dash(F, (1, 1), (1, 0))
    F.pt((0, 0), "O", "rt", -4, 4); F.lab((1, 0), "1", "ct", 0, 6); F.lab((0, 1), "1", "rb", -6, -8)
    return F.render()


def f3():
    F = panel((-1.0, 4.8), (-4.4, 2.2)); F.axes(); tag(F, 3)
    gline(F, [(4.4, 1.4), (1, -2), (3.3, -4.3)])
    dash(F, (1, -2), (1, 0)); dash(F, (1, -2), (0, -2))
    F.pt((0, 0), "O", "rt", -4, 4); F.lab((1, 0), "1", "cb", 0, -6); F.lab((3, 0), "3", "lt", 4, 6); F.lab((0, -2), "-2", "rc", -6, 0)
    return F.render()


def f4():
    F = panel((-1.0, 4.8), (-1.0, 3.6)); F.axes(); tag(F, 4)
    gline(F, [(-0.9, 2), (1, 2), (2, 0), (3, 2), (4.5, 2)])
    dash(F, (1, 2), (1, 0)); dash(F, (3, 2), (3, 0))
    F.pt((0, 0), "O", "rt", -4, 4); F.lab((1, 0), "1", "ct", 0, 6); F.lab((2, 0), "2", "ct", 0, 6); F.lab((3, 0), "3", "ct", 0, 6)
    F.lab((0, 2), "2", "rb", -6, -4)
    return F.render()


def f5():
    F = panel((-2.4, 2.6), (-1.0, 3.6)); F.axes(); tag(F, 5)
    xs = [-2.0 + 4.0 * i / 400 for i in range(401)]
    gline(F, [(x, abs(x * x - 1)) for x in xs])
    F.pt((0, 0), "O", "rt", -4, 4); F.lab((-1, 0), "-1", "ct", 0, 6); F.lab((1, 0), "1", "ct", 0, 6); F.lab((0, 1), "1", "lb", 6, -4)
    return F.render()


def f6():
    F = panel((-2.4, 2.6), (-1.8, 3.6)); F.axes(); tag(F, 6)
    xs = [-2.1 + 4.2 * i / 400 for i in range(401)]
    gline(F, [(x, x * x - 1) for x in xs])
    F.pt((0, 0), "O", "rt", -4, 4); F.lab((-1, 0), "-1", "rt", -4, 6); F.lab((1, 0), "1", "lt", 4, 6); F.lab((0, -1), "-1", "lt", 6, 4)
    return F.render()


def f7():
    F = panel((-5.2, 6.2), (-5.0, 6.2), 20); F.axes(); tag(F, 7)
    gline(F, [(4, 0), (0, 4), (-4, 0), (0, -4), (4, 0)])
    F.pt((0, 0), "O", "rt", -4, 4); F.lab((4, 0), "4", "lt", 4, 6); F.lab((-4, 0), "-4", "rt", -4, 6)
    F.lab((0, 4), "4", "lb", 6, -4); F.lab((0, -4), "-4", "lt", 6, 4)
    return F.render()


def f8():
    F = panel((-5.4, 6.0), (-2.6, 3.0), 26); F.axes(); tag(F, 8)
    for sx in (1, -1):
        gline(F, [(sx * 5.0, 1.5), (sx * 2, 0), (sx * 5.0, -1.5)])
    F.pt((0, 0), "O", "rt", -4, 4); F.lab((2, 0), "2", "cb", -8, -8); F.lab((-2, 0), "-2", "cb", 10, -8)
    return F.render()


def f314():
    f = lambda x: x * x - 5 * x + 6
    F = Frame((-0.9, 7.8), (-2.6, 15.6), 40, 18, (60, 12, 24, 34))
    F.poly([(0, -0.25), (6, -0.25), (6, 12), (0, 12)], SKY)
    F.axes()
    F.curve(f, 0, 6)
    xs = [-0.6 + 0.6 * i / 40 for i in range(41)]
    F.svg.append('<polyline points="%s" fill="none" stroke="#000" stroke-width="%s" %s/>' % (" ".join("%.1f,%.1f" % F.P(x, f(x)) for x in xs), STROKE, DASH))
    xs = [6 + 0.5 * i / 40 for i in range(41)]
    F.svg.append('<polyline points="%s" fill="none" stroke="#000" stroke-width="%s" %s/>' % (" ".join("%.1f,%.1f" % F.P(x, f(x)) for x in xs), STROKE, DASH))
    dash(F, (0, 12), (6, 12)); dash(F, (6, 12), (6, 0)); dash(F, (0, -0.25), (2.5, -0.25)); dash(F, (2.5, -0.25), (2.5, 0))
    F.pt((0, 0), "O", "rb", -6, -4)
    F.lab((0, 6), "a", "rc", -8, 0); F.lab((0, 12), "b", "rc", -8, 0); F.lab((6, 0), "6", "ct", 0, 6)
    F.lab((2.5, 0), r"\dfrac{5}{2}", "cb", 0, -8); F.lab((0, -0.25), r"-\dfrac{1}{4}", "rt", -8, 2)
    F.lab((5.9, 14.6), "f(x)=x^{2}-5x+a", "rc", -6, 0)
    return F.render()


def f327():
    F = Frame((-2.8, 3.2), (-1.8, 2.6), 60, 60, (16, 14, 120, 12))
    F.poly([(1, 1), (-2.6, 1), (-2.6, 2.4), (-0.4, 2.4)], PINK)       # m=−1과 m=0 사이(왼쪽 위)
    F.poly([(1, 1), (3.1, 1), (3.1, -1.1)], PINK)                       # m=−1과 m=0 사이(오른쪽 아래)
    F.axes()
    gline(F, [(2, 0), (0, 1), (-2, 0), (0, -1), (2, 0)])
    F.seg((-2.6, 1), (3.1, 1), 1.5, DASH)
    F.seg((-0.4, 2.4), (3.1, -1.1), 1.5, DASH)
    dot(F, (1, 1), 4)
    F.pt((0, 0), "O", "rt", -4, 4)
    F.lab((2, 0), "2", "lt", 4, 6); F.lab((-2, 0), "-2", "rt", -4, 6); F.lab((0, 1), "1", "lb", 6, -4); F.lab((0, -1), "-1", "lt", 6, 4)
    F.lab((1, 1), "(1,~1)", "lb", 4, -6)
    F.lab((3.1, 1), "m=0", "lc", 6, 0); F.lab((3.1, -1.1), "m=-1", "lc", 6, 0)
    return F.render()


def f329():
    F = Frame((-3.0, 4.6), (-8.2, 4.4), 34, 22, (40, 12, 30, 16))
    F.poly([(-2, -7), (3, -7), (3, 3), (-2, 3)], SKY)
    F.axes()
    dash(F, (-2, -7), (3, -7)); dash(F, (3, -7), (3, 3)); dash(F, (3, 3), (-2, 3)); dash(F, (-2, 3), (-2, -7))
    gline(F, [(-2, -7), (3, 3)])
    dot(F, (-2, -7), 5); dot(F, (3, 3), 5)
    F.pt((0, 0), "O", "rt", -4, 4)
    F.lab((-2, 0), "-2", "rt", -4, 6); F.lab((3, 0), "3", "lt", 4, 6); F.lab((0, 3), "3", "lb", 6, -4); F.lab((0, -7), "-7", "lt", 6, 4)
    return F.render()


FIGS = [("c2b9_323_%d.png" % (k + 1), fn, 5600) for k, fn in enumerate((f1, f2, f3, f4, f5, f6, f7, f8))] + \
       [("c2b9_314.png", f314, 10000), ("c2b9_327.png", f327, 10000), ("c2b9_329.png", f329, 8800)]

if __name__ == "__main__":
    for name, fn, wd in FIGS:
        if len(sys.argv) > 1 and name not in sys.argv[1:]:
            continue
        print(name, fit_shoot(name, fn, wd, HERE))
