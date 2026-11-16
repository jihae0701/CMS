# -*- coding: utf-8 -*-
"""미적분Ⅰ 3. 미분계수와 도함수 — 스캔 그림 다시 그리기.  python3 draw.py 출력폴더 [이름...]"""
import sys, math
sys.path.insert(0, '/home/user/CMS/.claude/skills/math-figure-rules'); sys.path.insert(0, '..')
from mathfig import Frame, DASH
from mjcommon import odot, fdot, plot, O, run, herm
OUT = sys.argv[1]
M = (16, 16, 16, 16)
g6 = lambda x: x - 0.13 * x * x


def i3():   # 6번 해설: f(a), f(b) 표시
    F = Frame((-1.4, 3.6), (-1.6, 2.9), 80, 80, (70, 16, 16, 16))
    F.axes(); O(F, 'lt', 4, 4)
    F.seg((-1.3, -1.3), (2.75, 2.75), 2.0); plot(F, g6, -1.0, 3.4)
    a, b = 1.0, 2.5
    for t in (a, b):
        F.dashed((t, 0), (t, g6(t))); F.dashed((0, g6(t)), (t, g6(t)))
    F.lab((a, 0), 'a', 'ct', 0, 8); F.lab((b, 0), 'b', 'ct', 0, 8)
    F.lab((0, g6(a)), 'f(a)', 'rc', -8, 0); F.lab((0, g6(b)), 'f(b)', 'rc', -8, 0)
    F.lab((2.75, 2.75), 'y=x', 'lc', 8, 0); F.lab((3.4, g6(3.4)), 'y=f(x)', 'rb', 0, -14)
    return F.render()


def i4():   # 6번 문제
    F = Frame((-1.4, 3.6), (-1.6, 2.9), 80, 80, M)
    F.axes(); O(F, 'lt', 4, 4)
    F.seg((-1.3, -1.3), (2.75, 2.75), 2.0); plot(F, g6, -1.0, 3.4)
    for t in (1.0, 2.5):
        F.dashed((t, 0), (t, g6(t)))
    F.lab((1.0, 0), 'a', 'ct', 0, 8); F.lab((2.5, 0), 'b', 'ct', 0, 8)
    F.lab((2.75, 2.75), 'y=x', 'lc', 8, 0); F.lab((3.4, g6(3.4)), 'y=f(x)', 'rb', 0, -14)
    return F.render()


def i7():   # 15번 문제
    F = Frame((-4.9, 3.9), (-3.4, 0.9), 60, 60, M)
    F.axes(); O(F, 'lb', 6, -6)
    F.seg((-4.7, -1.6), (-3, -3.1), 3.2)
    g = herm([(-3, -3.1, 3.4), (-2, -1, 1.5), (-0.9, -0.06, 0), (0, -1, -1.6), (1, -2, -0.2)])
    plot(F, g, -3, 1); F.seg((1, -1), (2, -1), 3.2); F.seg((2, -1), (3.3, -2.8), 3.2)
    F.dashed((-4, 0), (-4, -1.6 - 1.5 * 0.7 / 1.7)); F.dashed((-3, 0), (-3, -3.1))
    F.dashed((-2, 0), (-2, -1)); F.dashed((-2, -1), (1, -1)); F.dashed((1, 0), (1, -2)); F.dashed((2, 0), (2, -1)); F.dashed((3, 0), (3, -1 - 1.8 / 1.3))
    fdot(F, (-2, 0)); fdot(F, (1, -1)); odot(F, (-2, -1)); odot(F, (1, -2))
    for x in (-4, -3, -2, -1, 1, 2, 3):
        F.lab((x, 0), str(x), 'cb', 0, -8)
    F.lab((3.3, -2.8), 'y=f(x)', 'rt', 10, 6)
    return F.render()


def i8():   # 17번 문제 (-2, 5)
    F = Frame((-2.6, 5.9), (-2.6, 2.7), 60, 85, M)
    F.axes(); O(F, 'rt', -6, 4)
    F.seg((-2, 1), (-1, 0), 3.2); F.seg((-1, 1), (0, 2), 3.2); plot(F, lambda x: 2 * (x - 1) ** 2, 0, 2)
    F.seg((2, 2), (3, 2), 3.2); F.seg((3, 2), (5, -2), 3.2)
    F.dashed((-2, 0), (-2, 1)); F.dashed((-2, 1), (0, 1)); F.dashed((-1, 0), (-1, 1)); F.dashed((0, 2), (2, 2))
    F.dashed((2, 0), (2, 2)); F.dashed((3, 0), (3, 2)); F.dashed((5, 0), (5, -2)); F.dashed((0, -2), (5, -2))
    fdot(F, (-1, 1)); fdot(F, (2, 1))
    for p in [(-2, 1), (-1, 0), (2, 2), (5, -2)]:
        odot(F, p)
    for x in (-2, -1, 1, 2, 3):
        F.lab((x, 0), str(x), 'ct', 0, 8)
    F.lab((4, 0), '4', 'ct', 8, 8); F.lab((5, 0), '5', 'cb', 0, -8)
    F.lab((0, 1), '1', 'rt', -8, 6); F.lab((0, 2), '2', 'rc', -8, 0); F.lab((0, -2), '-2', 'rc', -8, 0)
    F.lab((3.6, 1.6), 'y=f(x)', 'lc', 6, 0)
    return F.render()


def i10():  # 31번 해설 f'(x)=3/2(x²-1), x≠-1, 0
    F = Frame((-1.9, 1.9), (-2.3, 2.6), 80, 80, M)
    F.axes(); O(F, 'lt', 4, 4)
    fp = lambda x: 1.5 * (x * x - 1)
    plot(F, fp, -1.62, 1.62)
    odot(F, (-1, 0)); odot(F, (0, -1.5))
    F.lab((-1, 0), '-1', 'rt', -6, 6); F.lab((1, 0), '1', 'lt', 6, 6); F.lab((0, -1.5), '-\\dfrac{3}{2}', 'rt', -8, 4)
    F.lab((1.62, fp(1.62)), "y=f'(x)", 'rc', -12, 0)
    return F.render()


def i11():  # 31번 문제
    F = Frame((-2.6, 2.6), (-1.9, 2.4), 70, 70, M)
    F.axes(); O(F, 'rb', -6, -4)
    f = lambda x: 0.5 * (x ** 3 - 3 * x)
    plot(F, f, -2.25, -1); plot(F, lambda x: f(x) - 1, -1, 0); plot(F, f, 0, 2.35)
    F.dashed((-1, 0), (-1, 1)); F.dashed((-1, 1), (0, 1)); F.dashed((1, 0), (1, -1)); F.dashed((0, -1), (1, -1))
    fdot(F, (-1, 1)); fdot(F, (0, 0)); odot(F, (-1, 0)); odot(F, (0, -1))
    F.lab((-1, 0), '-1', 'ct', 0, 8); F.lab((1, 0), '1', 'cb', 0, -8); F.lab((0, 1), '1', 'lc', 8, 0); F.lab((0, -1), '-1', 'rc', -8, 0)
    F.lab((2.35, f(2.35)), 'y=f(x)', 'rc', -12, 0)
    return F.render()


JOBS = {k: v for k, v in globals().items() if k[0] == 'i' and k[1:].isdigit()}
if __name__ == '__main__':
    run(JOBS, OUT, sys.argv[2:], wide=())
