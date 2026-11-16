# -*- coding: utf-8 -*-
"""미적분Ⅰ 8. 정적분 — 스캔 그림 다시 그리기.  python3 draw.py 출력폴더 [이름...]"""
import sys, math
sys.path.insert(0, '/home/user/CMS/.claude/skills/math-figure-rules'); sys.path.insert(0, '..')
from mathfig import Frame, DASH, GREEN
from mjcommon import plot, O, run
OUT = sys.argv[1]
M = (16, 16, 16, 16)
YEL = '#fff3bf'


def i3():   # 13번 해설 ⑴
    F = Frame((-1.6, 3.6), (-1.6, 1.8), 90, 90, M)
    F.poly([(-1, 0), (-1, -1), (0, 0)], YEL); F.poly([(0, 0), (1, 1), (2, 0)], YEL)
    F.axes(); O(F, 'lt', 4, 6)
    F.seg((-1.4, -1.4), (1, 1), 3.2); F.seg((1, 1), (3.4, -1.4), 3.2)
    F.seg((-1, 0), (-1, -1), 2.0)
    F.dashed((0, 1), (1, 1)); F.dashed((1, 0), (1, 1))
    F.lab((-1, 0), '-1', 'cb', 0, -6); F.lab((1, 0), '1', 'ct', 0, 6); F.lab((2, 0), '2', 'lb', 6, -4); F.lab((0, 1), '1', 'rc', -8, 0)
    F.lab((1.3, 1.3), 'y=f(x)', 'lc', 8, 0)
    return F.render()


def i4():   # 14번 해설 ⑴ |x-1|
    F = Frame((-0.9, 3.8), (-0.6, 2.8), 90, 90, M)
    F.poly([(0, 0), (0, 1), (1, 0), (3, 2), (3, 0)], YEL)
    F.axes(); O(F, 'rt', -6, 4)
    F.polyline([(-0.8, 1.8), (1, 0), (3.55, 2.55)])
    F.seg((3, 0), (3, 2), 2.0); F.dashed((0, 2), (3, 2))
    F.lab((1, 0), '1', 'ct', 0, 6); F.lab((3, 0), '3', 'ct', 0, 6); F.lab((0, 1), '1', 'rc', -8, 0); F.lab((0, 2), '2', 'rc', -8, 0)
    F.lab((1.6, 2.5), 'y=|x-1|', 'cc')
    return F.render()


def i5():   # 14번 해설 ⑵ |x-x²|
    f = lambda x: abs(x - x * x)
    F = Frame((-1.4, 2.8), (-0.6, 2.9), 100, 100, M)
    n = 60
    F.poly([(0, 0)] + [(2 * i / n, f(2 * i / n)) for i in range(n + 1)] + [(2, 0)], GREEN)
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, f, -1.1, 2.12)
    F.seg((2, 0), (2, 2), 2.0); F.dashed((0, 2), (2, 2))
    F.lab((1, 0), '1', 'ct', 0, 6); F.lab((2, 0), '2', 'ct', 0, 6); F.lab((0, 2), '2', 'rc', -8, 0)
    F.lab((0.4, 2.6), 'y=|x-x^{2}|', 'lc', 6, 0)
    return F.render()


def i7():   # 25번 문제 f(x)=(x+1)(x-1)(x-2)
    f = lambda x: (x + 1) * (x - 1) * (x - 2)
    F = Frame((-1.7, 3.0), (-2.4, 3.3), 80, 70, M)
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, f, -1.3, 2.55)
    F.lab((-1, 0), '-1', 'rb', -4, -4); F.lab((1, 0), '1', 'rt', -4, 6); F.lab((2, 0), '2', 'lt', 4, 6); F.lab((0, 2), '2', 'lb', 6, -4)
    F.lab((2.55, f(2.55)), 'y=f(x)', 'rc', -12, 0)
    return F.render()


def i8():   # 26·27번 y=f(x): (-1, 0)→(1, 1)→(2, 0)
    F = Frame((-2.2, 3.4), (-1.0, 1.9), 90, 90, M)
    F.axes(); O(F, 'rt', -6, 4)
    F.polyline([(-2.0, -0.5), (1, 1), (2.8, -0.8)])
    F.dashed((0, 1), (1, 1)); F.dashed((1, 0), (1, 1))
    F.lab((-1, 0), '-1', 'ct', -4, 6); F.lab((1, 0), '1', 'ct', 0, 6); F.lab((2, 0), '2', 'lt', 4, 6); F.lab((0, 1), '1', 'rc', -8, 0)
    F.lab((1, 1), 'y=f(x)', 'lb', 10, -6)
    return F.render()


def i9():   # 27번 문제 x³-6x²+9x-3
    f = lambda x: x ** 3 - 6 * x * x + 9 * x - 3
    F = Frame((-0.9, 4.6), (-3.8, 2.6), 80, 60, M)
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, f, -0.1, 4.25)
    F.dashed((0, 1), (1, 1)); F.dashed((1, 0), (1, 1)); F.dashed((3, 0), (3, -3)); F.dashed((0, -3), (3, -3))
    F.lab((1, 0), '1', 'ct', 0, 6); F.lab((3, 0), '3', 'cb', 0, -6); F.lab((0, 1), '1', 'rc', -8, 0); F.lab((0, -3), '-3', 'rc', -8, 0)
    F.lab((4.25, f(4.25)), 'y=f(x)', 'rc', -12, 0)
    return F.render()


def i10():  # y=f(x): x<0이면 6x+18, x≥0이면 18
    F = Frame((-4.4, 4.4), (-5.0, 22.5), 60, 12, M)
    F.axes(); O(F, 'lt', 4, 4)
    F.polyline([(-3.7, -4.2), (0, 18), (4.0, 18)])
    F.lab((-3, 0), '-3', 'rb', -6, -4); F.lab((0, 18), '18', 'rc', -8, -8)
    F.lab((4.0, 18), 'y=f(x)', 'rb', 0, -8)
    return F.render()


JOBS = {k: v for k, v in globals().items() if k[0] == 'i' and k[1:].isdigit()}
if __name__ == '__main__':
    run(JOBS, OUT, sys.argv[2:])
