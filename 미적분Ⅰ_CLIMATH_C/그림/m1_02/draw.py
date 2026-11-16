# -*- coding: utf-8 -*-
"""미적분Ⅰ 2. 함수의 연속 — 스캔 그림 다시 그리기.  python3 draw.py 출력폴더 [이름...]"""
import sys, math
sys.path.insert(0, '/home/user/CMS/.claude/skills/math-figure-rules'); sys.path.insert(0, '..')
from mathfig import Frame, DASH
from mjcommon import odot, fdot, plot, axes2, O, run
OUT = sys.argv[1]
M = (16, 16, 16, 16)


def i3():   # 1⑴ y=x-2
    F = Frame((-1.4, 3.4), (-2.9, 1.5), 70, 70, M)
    F.axes(); O(F, 'rb', -6, -4)
    F.seg((-1.0, -3.0 + 0.0), (3.0, 1.0), 3.2)
    F.lab((2, 0), '2', 'lt', 2, 6); F.lab((0, -2), '-2', 'lc', 10, 4)
    F.lab((2.9, 0.9), 'y=f(x)', 'rb', -14, -6)
    return F.render()


def i4():   # 1⑵ √x (x≥0), x (x<0)
    F = Frame((-1.9, 3.4), (-1.9, 2.4), 70, 70, M)
    F.axes(); O(F, 'lt', 4, 4)
    F.seg((-1.8, -1.8), (0, 0), 3.2); plot(F, lambda x: math.sqrt(x), 0, 3.2)
    F.lab((3.2, math.sqrt(3.2)), 'y=f(x)', 'rb', 0, -12)
    return F.render()


def i5():   # 1⑶ |x|/x, f(0)=0
    F = Frame((-2.4, 2.6), (-1.9, 1.9), 70, 70, M)
    F.axes(); O(F, 'rt', -6, 4)
    F.seg((0, 1), (2.2, 1), 3.2); F.seg((-2.2, -1), (0, -1), 3.2)
    odot(F, (0, 1)); odot(F, (0, -1)); fdot(F, (0, 0))
    F.lab((0, 1), '1', 'rc', -10, 0); F.lab((0, -1), '-1', 'lc', 10, 0)
    F.lab((1.2, 1), 'y=f(x)', 'cb', 0, -10)
    return F.render()


def i6():   # 1⑷ x-[x]
    F = Frame((-2.0, 2.0), (-0.9, 1.9), 90, 90, M)
    F.axes(); O(F, 'rt', -6, 4)
    F.seg((-1.45, 0.55), (-1, 1), 3.2); F.seg((-1, 0), (0, 1), 3.2); F.seg((0, 0), (1, 1), 3.2); F.seg((1, 0), (1.45, 0.45), 3.2)
    F.dashed((-1, 1), (1, 1)); F.dashed((-1, 0), (-1, 1)); F.dashed((1, 0), (1, 1))
    for p in [(-1, 0), (0, 0), (1, 0)]:
        fdot(F, p)
    for p in [(-1, 1), (0, 1), (1, 1)]:
        odot(F, p)
    F.lab((-1.75, 0.55), '\\cdots', 'cc'); F.lab((1.75, 0.55), '\\cdots', 'cc')
    F.lab((-1, 0), '-1', 'ct', 0, 10); F.lab((1, 0), '1', 'ct', 0, 10); F.lab((0, 1), '1', 'rb', -6, -4)
    F.lab((0.15, 1.45), 'y=f(x)', 'lc', 0, 0)
    return F.render()


def i7():   # 2번 문제
    F = Frame((-2.6, 2.9), (-1.6, 1.8), 80, 80, M)
    F.axes(); O(F, 'lt', 4, 4)
    F.seg((-2, 1), (-1, 0), 3.2); plot(F, lambda x: x * x - 1, -1, 1); F.seg((1, 1), (2, 0), 3.2)
    F.dashed((-2, 0), (-2, 1)); F.dashed((-2, 1), (1, 1)); F.dashed((-1, 0), (-1, 1)); F.dashed((1, 0), (1, 1))
    for p in [(-1, 1), (0, 0), (1, 1)]:
        fdot(F, p)
    for p in [(-2, 1), (-1, 0), (0, -1), (1, 0), (2, 0)]:
        odot(F, p)
    F.lab((-2, 0), '-2', 'ct', 0, 10); F.lab((-1, 0), '-1', 'ct', -8, 10); F.lab((1, 0), '1', 'ct', 8, 10); F.lab((2, 0), '2', 'ct', 0, 10)
    F.lab((0, 1), '1', 'lb', 6, -4); F.lab((0, -1), '-1', 'rt', -6, 6)
    F.lab((-2, 1), 'y=f(x)', 'lb', -10, -12)
    return F.render()


def i9():   # 4번 문제 [-1, 3]
    F = Frame((-1.6, 3.9), (-2.6, 2.7), 70, 70, M)
    F.axes(); O(F, 'rb', -6, -4)
    F.seg((-1, -1), (0, 0), 3.2)
    plot(F, lambda x: -2 * (1 - math.sqrt(max(0, 1 - x * x))), 0, 1)
    plot(F, lambda x: (x - 1) ** 2, 1, 2); plot(F, lambda x: 1 + math.sqrt(max(0, x - 2)), 2, 3)
    F.dashed((-1, 0), (-1, -1)); F.dashed((-1, -1), (0, -1)); F.dashed((1, 0), (1, -2)); F.dashed((0, -2), (1, -2))
    F.dashed((2, 0), (2, 1)); F.dashed((0, 1), (2, 1)); F.dashed((3, 0), (3, 2)); F.dashed((0, 2), (3, 2))
    for p in [(-1, -1), (1, 0), (2, 0), (3, 2)]:
        fdot(F, p)
    for p in [(1, -2), (2, 1)]:
        odot(F, p)
    F.lab((-1, 0), '-1', 'cb', 0, -8); F.lab((1, 0), '1', 'lt', 4, 6); F.lab((2, 0), '2', 'ct', 0, 10); F.lab((3, 0), '3', 'ct', 0, 10)
    F.lab((0, 1), '1', 'rc', -8, 0); F.lab((0, 2), '2', 'rc', -8, 0); F.lab((0, -1), '-1', 'lc', 8, 0); F.lab((0, -2), '-2', 'rc', -8, 0)
    F.lab((3, 2), 'y=f(x)', 'cb', 0, -14)
    return F.render()


def i10():  # 5번 문제
    F = Frame((-1.6, 3.6), (-1.7, 2.6), 70, 70, M)
    F.axes(); O(F, 'lt', 4, 4)
    F.seg((-1.4, -1.4), (0, 0), 3.2)
    plot(F, lambda x: 1 + 0.9 * math.sqrt(max(0, 1 - (x - 1) ** 2)), 0, 2)
    F.seg((2, -1), (3.4, -1), 3.2)
    F.dashed((0, 1), (2, 1)); F.dashed((2, 1), (2, -1)); F.dashed((0, -1), (2, -1))
    fdot(F, (0, 1)); fdot(F, (2, -1)); odot(F, (0, 0)); odot(F, (2, 1))
    F.lab((2, 0), '2', 'lb', 6, -4); F.lab((0, 1), '1', 'rc', -8, 0); F.lab((0, -1), '-1', 'rc', -8, 0)
    F.lab((1.9, 1.75), 'y=f(x)', 'lb', 4, 0)
    return F.render()


def i12():  # 10번 해설 y=3, x²-1, y=3
    F = Frame((-3.6, 3.9), (-1.7, 3.9), 60, 60, M)
    F.axes(); O(F, 'lt', 4, 4)
    F.seg((-3.4, 3), (-2, 3), 3.2); plot(F, lambda x: x * x - 1, -2, 2); F.seg((2, 3), (3.4, 3), 3.2)
    F.dashed((-2, 0), (-2, 3)); F.dashed((2, 0), (2, 3)); F.dashed((-2, 3), (2, 3))
    F.lab((-2, 0), 'a', 'ct', 0, 8); F.lab((2, 0), 'b', 'ct', 0, 8); F.lab((-1, 0), '-1', 'rt', -4, 6); F.lab((1, 0), '1', 'lt', 4, 6)
    F.lab((0, 3), '3', 'rb', -6, -4); F.lab((0, -1), '-1', 'rt', -6, 6)
    F.lab((2.4, 3), 'y=f(x)', 'lb', 0, -8)
    return F.render()


def i13():  # 18번 문제 f, g
    F = Frame((-2.4, 8.2), (-1.9, 2.0), 70, 70, M)
    axes2(F, 0, -2.3, 2.6, -1.8, 1.9); O(F, 'lt', 4, 4)
    F.seg((-2.2, 1), (-1, 1), 3.2); F.seg((-1, -1), (1, 1), 3.2); F.seg((1, -1), (2.2, -1), 3.2)
    F.dashed((-1, 1), (1, 1)); F.dashed((-1, 1), (-1, -1)); F.dashed((1, 1), (1, -1)); F.dashed((-1, -1), (1, -1))
    fdot(F, (-1, -1)); fdot(F, (1, 1)); odot(F, (-1, 1)); odot(F, (1, -1))
    F.lab((-1, 0), '-1', 'rb', -4, -4); F.lab((1, 0), '1', 'lb', 4, -4); F.lab((0, 1), '1', 'rb', -6, -4); F.lab((0, -1), '-1', 'lt', 6, 6)
    F.lab((1.1, 1.6), 'y=f(x)', 'lc', 0, 0)
    ox = 5.6
    axes2(F, ox, ox - 2.3, ox + 2.5, -1.8, 1.9); F.pt((ox, 0), 'O', 'rb', -6, -4)
    F.seg((ox - 2.2, -1), (ox - 1, -1), 3.2); plot(F, lambda x: -(x - ox) ** 2, ox - 1, ox + 1); F.seg((ox + 1, 1), (ox + 2.2, 1), 3.2)
    F.dashed((ox - 1, 0), (ox - 1, -1)); F.dashed((ox - 1, -1), (ox + 1, -1)); F.dashed((ox + 1, -1), (ox + 1, 1)); F.dashed((ox, 1), (ox + 1, 1))
    fdot(F, (ox - 1, 0)); fdot(F, (ox + 1, -1)); odot(F, (ox - 1, -1)); odot(F, (ox + 1, 1))
    F.lab((ox - 1, 0), '-1', 'rb', -6, -4); F.lab((ox + 1, 0), '1', 'lb', 6, -4); F.lab((ox, 1), '1', 'rb', -6, -4); F.lab((ox, -1), '-1', 'rt', -6, 6)
    F.lab((ox + 1.1, 1.6), 'y=g(x)', 'lc', 0, 0)
    return F.render()


def i14():  # 19번 문제 f, g
    F = Frame((-1.6, 7.6), (-1.5, 2.3), 70, 70, M)
    axes2(F, 0, -1.5, 3.0, -1.4, 2.2); O(F, 'rt', -6, 4)
    plot(F, lambda x: x * x, -1.35, 1); F.seg((1, 1), (2.9, -0.9), 3.2)
    F.dashed((0, 1), (1, 1)); F.dashed((1, 0), (1, 1))
    fdot(F, (1, 0)); odot(F, (1, 1))
    F.lab((1, 0), '1', 'ct', 0, 10); F.lab((2, 0), '2', 'cb', 6, -6); F.lab((0, 1), '1', 'rc', -8, 0)
    F.lab((1.2, 1.55), 'y=f(x)', 'lc', 0, 0)
    ox = 4.6
    axes2(F, ox, ox - 1.3, ox + 2.9, -1.4, 2.2); F.pt((ox, 0), 'O', 'lt', 4, 4)
    F.seg((ox - 1.2, -1.2), (ox + 1, 1), 3.2)
    plot(F, lambda x: -1 + 2 * (x - ox - 2) ** 2, ox + 1, ox + 2)
    plot(F, lambda x: 1 + 1.6 * (x - ox - 2) ** 2, ox + 2, ox + 2.85)
    F.dashed((ox, 1), (ox + 2, 1)); F.dashed((ox + 1, 0), (ox + 1, 1)); F.dashed((ox + 2, 1), (ox + 2, -1)); F.dashed((ox, -1), (ox + 2, -1))
    fdot(F, (ox + 2, -1)); odot(F, (ox + 2, 1))
    F.lab((ox + 1, 0), '1', 'ct', -6, 10); F.lab((ox + 2, 0), '2', 'lt', 6, 6); F.lab((ox, 1), '1', 'rc', -8, 0); F.lab((ox, -1), '-1', 'rc', -8, 0)
    F.lab((ox + 2.85, 1 + 1.6 * 0.85 ** 2), 'y=g(x)', 'rc', -12, 0)
    return F.render()


def i15():  # 20번 해설 ⑴ x²-x
    F = Frame((-1.9, 2.6), (-0.9, 3.1), 80, 80, M)
    F.axes(); O(F, 'lb', 4, -4)
    f = lambda x: x * x - x
    plot(F, f, -1, 1); plot(F, f, -1.55, -1, 3.2, DASH); plot(F, f, 1, 2.3, 3.2, DASH)
    F.dashed((-1, 0), (-1, 2)); F.dashed((-1, 2), (0, 2)); F.dashed((0.5, 0), (0.5, -0.25)); F.dashed((0, -0.25), (0.5, -0.25))
    fdot(F, (-1, 2)); fdot(F, (1, 0))
    F.lab((-1, 0), '-1', 'ct', 0, 8); F.lab((1, 0), '1', 'ct', 4, 8); F.lab((0, 2), '2', 'lc', 8, 0)
    F.lab((0.5, 0), '\\dfrac{1}{2}', 'cb', 6, -14); F.lab((0, -0.25), '-\\dfrac{1}{4}', 'rt', -6, 2)
    F.lab((2.2, 2.9), 'y=f(x)', 'rc', -14, 0)
    return F.render()


def i16():  # 20번 해설 ⑵ (x+1)/(x-1)
    F = Frame((-2.1, 6.2), (-2.1, 4.4), 55, 55, M)
    F.axes(); O(F, 'lt', 4, 4)
    f = lambda x: 1 + 2 / (x - 1)
    plot(F, f, 2, 5); plot(F, f, 1.48, 2, 3.2, DASH); plot(F, f, 5, 6.0, 3.2, DASH)
    plot(F, f, -2.0, 0.55, 3.2, DASH)
    F.dashed((1, -2.0), (1, 4.3)); F.dashed((-2.0, 1), (6.0, 1))
    F.dashed((2, 0), (2, 3)); F.dashed((0, 3), (2, 3)); F.dashed((5, 0), (5, 1.5)); F.dashed((0, 1.5), (5, 1.5))
    fdot(F, (2, 3)); fdot(F, (5, 1.5))
    F.lab((-1, 0), '-1', 'ct', 0, 8); F.lab((1, 0), '1', 'lt', 4, 6); F.lab((2, 0), '2', 'ct', 0, 8); F.lab((5, 0), '5', 'ct', 0, 8)
    F.lab((0, 3), '3', 'rc', -8, 0); F.lab((0, 1.5), '\\dfrac{3}{2}', 'rc', -8, -10); F.lab((0, 1), '1', 'rt', -6, 4); F.lab((0, -1), '-1', 'lc', 8, 0)
    F.lab((2.2, 3.9), 'y=f(x)', 'lc', 0, 0)
    return F.render()


def i17():  # 22번 해설 1/x, f(0)=0
    F = Frame((-3.1, 3.4), (-2.2, 2.4), 60, 110, M)
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, lambda x: 1 / x, 0.37, 3.2); plot(F, lambda x: 1 / x, -3.0, -0.38)
    F.dashed((1, 0), (1, 1)); F.dashed((0, 1), (1, 1)); F.dashed((2, 0), (2, 0.5)); F.dashed((0, 0.5), (2, 0.5))
    F.dashed((-1, 0), (-1, -1)); F.dashed((-1, -1), (0, -1))
    fdot(F, (0, 0))
    F.lab((1, 0), '1', 'ct', 0, 8); F.lab((2, 0), '2', 'ct', 0, 8); F.lab((-1, 0), '-1', 'cb', 0, -6)
    F.lab((0, 1), '1', 'rc', -8, 0); F.lab((0, 0.5), '\\dfrac{1}{2}', 'rc', -8, -6); F.lab((0, -1), '-1', 'lc', 8, 0)
    F.lab((0.55, 2.4), 'y=f(x)', 'lc', 6, 0)
    return F.render()


def i18():  # 22번 문제 [-2, 3]
    F = Frame((-2.6, 3.8), (-3.6, 1.8), 70, 70, M)
    F.axes(); O(F, 'rb', -6, -4)
    plot(F, lambda x: -1 + (x + 1) ** 2, -2, -1); plot(F, lambda x: -math.cos(math.pi * (x + 1) / 2), -1, 1)
    plot(F, lambda x: 1 - 3 * (x - 1) ** 2, 1, 2); plot(F, lambda x: -3 + (x - 2) ** 2, 2, 3)
    F.dashed((-1, 0), (-1, -1)); F.dashed((0, 1), (1, 1)); F.dashed((1, 0), (1, 1)); F.dashed((2, 0), (2, -3))
    F.dashed((0, -2), (3, -2)); F.dashed((0, -3), (2, -3)); F.dashed((3, 0), (3, -2))
    for p in [(-2, 0), (-1, 0), (2, -2), (3, -2)]:
        fdot(F, p)
    for p in [(-1, -1), (2, -3)]:
        odot(F, p)
    F.lab((-2, 0), '-2', 'cb', 0, -8); F.lab((-1, 0), '-1', 'cb', 0, -8); F.lab((1, 0), '1', 'ct', 0, 8); F.lab((2, 0), '2', 'cb', 0, -8); F.lab((3, 0), '3', 'cb', 0, -8)
    F.lab((0, 1), '1', 'rc', -8, 0); F.lab((0, -1), '-1', 'lc', 8, 0); F.lab((0, -2), '-2', 'rc', -8, 0); F.lab((0, -3), '-3', 'rc', -8, 0)
    F.lab((1.2, 1.4), 'y=f(x)', 'lc', 0, 0)
    return F.render()


def i19():  # 28번 문제
    F = Frame((-1.9, 2.9), (-1.8, 2.6), 70, 70, M)
    F.axes(); O(F, 'rt', -6, 4)
    F.seg((-1.6, 2.6), (0, 1), 3.2); F.seg((0, -1), (2.6, 1.6), 3.2)
    fdot(F, (0, 0)); odot(F, (0, 1)); odot(F, (0, -1))
    F.lab((0, 1), '1', 'lc', 10, 0); F.lab((0, -1), '-1', 'rc', -10, 0)
    F.lab((2.6, 1.6), 'y=f(x)', 'rb', -6, -14)
    return F.render()


def i20():  # 32번 문제 f, g
    F = Frame((-2.6, 7.6), (-2.1, 2.4), 70, 70, M)
    axes2(F, 0, -2.4, 1.6, -0.9, 2.3); O(F, 'rt', -6, 4)
    F.seg((-2.3, -1.3), (1.2, 2.2), 3.2)
    F.lab((-1, 0), '-1', 'rt', -4, 6); F.lab((0, 1), '1', 'lc', 10, 4)
    F.lab((-1.5, -0.5), 'y=f(x)', 'rc', -12, 0)
    ox = 5.2
    axes2(F, ox, ox - 2.1, ox + 2.2, -2.0, 2.2); F.pt((ox, 0), 'O', 'lt', 4, 4)
    F.seg((ox - 2.0, 2.0), (ox - 1, 1), 3.2); F.seg((ox - 1, -1), (ox + 1, 1), 3.2); F.seg((ox + 1, -1), (ox + 2.0, -2.0), 3.2)
    F.dashed((ox - 1, 1), (ox + 1, 1)); F.dashed((ox - 1, -1), (ox + 1, -1)); F.dashed((ox - 1, 1), (ox - 1, -1)); F.dashed((ox + 1, 1), (ox + 1, -1))
    fdot(F, (ox - 1, 0)); fdot(F, (ox + 1, 0))
    for p in [(ox - 1, 1), (ox - 1, -1), (ox + 1, 1), (ox + 1, -1)]:
        odot(F, p)
    F.lab((ox - 1, 0), '-1', 'rt', -6, 6); F.lab((ox + 1, 0), '1', 'lt', 6, 6); F.lab((ox, 1), '1', 'rb', -6, -4); F.lab((ox, -1), '-1', 'lt', 6, 6)
    F.lab((ox + 1.1, 1.7), 'y=g(x)', 'lc', 0, 0)
    return F.render()


def i21():  # 33번 문제 f, g
    F = Frame((-2.0, 7.4), (-0.9, 2.3), 70, 70, M)
    axes2(F, 0, -1.9, 3.1, -0.8, 2.2); O(F, 'rt', -6, 4)
    F.seg((-1.8, 1.8), (0, 0), 3.2); F.seg((0, 0), (1, 0), 3.2); F.seg((1, 0), (2.8, 1.8), 3.2)
    F.dashed((-1, 1), (2, 1)); F.dashed((-1, 0), (-1, 1)); F.dashed((2, 0), (2, 1))
    F.lab((-1, 0), '-1', 'ct', 0, 8); F.lab((1, 0), '1', 'ct', 0, 8); F.lab((2, 0), '2', 'ct', 0, 8); F.lab((0, 1), '1', 'rb', -6, -4)
    F.lab((2.8, 1.8), 'y=f(x)', 'rb', -16, -6)
    ox = 4.8
    axes2(F, ox, ox - 1.4, ox + 2.6, -0.8, 2.2); F.pt((ox, 0), 'O', 'rt', -6, 4)
    F.seg((ox - 1.3, 0), (ox, 0), 3.2); F.seg((ox, 1), (ox + 1, 0), 3.2); F.seg((ox + 1, 1), (ox + 2.5, 1), 3.2)
    F.dashed((ox, 1), (ox + 1, 1)); F.dashed((ox + 1, 0), (ox + 1, 1))
    fdot(F, (ox, 1)); fdot(F, (ox + 1, 1)); odot(F, (ox, 0)); odot(F, (ox + 1, 0))
    F.lab((ox + 1, 0), '1', 'ct', 0, 8); F.lab((ox, 1), '1', 'rc', -8, 0)
    F.lab((ox + 1.3, 1.5), 'y=g(x)', 'lc', 0, 0)
    return F.render()


def i22():  # 37번 문제 [0, 6]
    F = Frame((-0.6, 6.9), (-1.6, 2.6), 60, 60, M)
    F.axes(); O(F, 'rt', -6, 4)
    F.polyline([(0, 1), (1, 0), (2, 1)], 'stroke-width="3.2" stroke-linejoin="round"')
    F.polyline([(2, 1), (3, -1), (4, 0)], 'stroke-width="3.2" stroke-linejoin="round"')
    F.polyline([(4, 0), (5, 1), (6, 0)], 'stroke-width="3.2" stroke-linejoin="round"')
    F.dashed((0, 2), (4, 2)); F.dashed((2, 0), (2, 2)); F.dashed((4, 0), (4, 2)); F.dashed((2, 1), (5, 1)); F.dashed((5, 0), (5, 1))
    F.dashed((3, 0), (3, -1)); F.dashed((0, -1), (3, -1))
    for p in [(0, 1), (2, 2), (4, 2), (6, 0)]:
        fdot(F, p)
    for p in [(2, 1), (4, 0)]:
        odot(F, p)
    for x in (1, 2, 4, 5, 6):
        F.lab((x, 0), str(x), 'ct', 0, 10)
    F.lab((3, 0), '3', 'cb', 0, -8)
    F.lab((0, 1), '1', 'rc', -8, 0); F.lab((0, 2), '2', 'rc', -8, 0); F.lab((0, -1), '-1', 'rc', -8, 0)
    F.lab((5.2, 1.4), 'y=f(x)', 'lc', 0, 0)
    return F.render()


def i23():  # 40번 해설 0<x<1
    F = Frame((-2.6, 3.3), (-0.9, 3.6), 60, 60, M)
    F.axes('n'); O(F, 'rt', -6, 4)
    plot(F, lambda t: 0.5 ** t, -1.75, 3.1)
    F.lab((0, 1), '1', 'rt', -6, 6)
    F.lab((-1.75, 0.5 ** -1.75), 'y=x^{n}', 'rc', -8, 0)
    return F.render()


def i24():  # 40번 해설 x>1
    F = Frame((-3.3, 2.6), (-0.9, 3.6), 60, 60, (16, 16, 70, 16))
    F.axes('n'); O(F, 'rt', -6, 4)
    plot(F, lambda t: 2 ** t, -3.1, 1.75)
    F.lab((0, 1), '1', 'lt', 6, 6)
    F.lab((1.75, 2 ** 1.75), 'y=x^{n}', 'lc', 10, 0)
    return F.render()


def i25():  # 41번 문제
    F = Frame((-1.0, 4.6), (-0.9, 5.9), 60, 60, M)
    F.axes(); O(F, 'lt', 4, 4)
    F.seg((-0.8, -0.4), (2, 1), 3.2); F.seg((2, 4), (4.4, 5.2), 3.2)
    F.dashed((2, 0), (2, 4)); F.dashed((0, 4), (2, 4)); F.dashed((0, 1), (2, 1))
    fdot(F, (2, 4)); odot(F, (2, 1))
    F.lab((2, 0), '2', 'ct', 0, 8); F.lab((0, 1), '1', 'rc', -8, 0); F.lab((0, 4), '4', 'rc', -8, 0)
    F.lab((3.0, 4.5), 'y=f(x)', 'lt', 6, 10)
    return F.render()


def i26():  # 42번 해설 a=f(4), b=f(1)
    F = Frame((-1.0, 5.2), (-0.9, 6.4), 60, 60, M)
    F.axes(); O(F, 'lt', 4, 4)
    F.seg((-0.8, -0.4), (2, 1), 3.2); F.seg((2, 4), (5.0, 5.5), 3.2)
    F.dashed((2, 0), (2, 4)); F.dashed((0, 4), (2, 4)); F.dashed((0, 1), (2, 1))
    F.dashed((4, 0), (4, 5)); F.dashed((0, 5), (4, 5)); F.dashed((1, 0), (1, 0.5)); F.dashed((0, 0.5), (1, 0.5))
    fdot(F, (2, 4)); odot(F, (2, 1))
    F.lab((1, 0), '1', 'ct', 0, 8); F.lab((2, 0), '2', 'ct', 0, 8); F.lab((4, 0), '4', 'ct', 0, 8)
    F.lab((0, 1), '1', 'rc', -8, -2); F.lab((0, 0.5), 'b', 'rc', -8, 4); F.lab((0, 4), '4', 'rc', -8, 0); F.lab((0, 5), 'a', 'rc', -8, 0)
    F.lab((2.6, 5.3), 'y=f(x)', 'lc', 0, 0)
    return F.render()


JOBS = {k: v for k, v in globals().items() if k[0] == 'i' and k[1:].isdigit()}
if __name__ == '__main__':
    run(JOBS, OUT, sys.argv[2:], wide=('i13', 'i14', 'i20', 'i21'))
