# -*- coding: utf-8 -*-
"""대수 C 3. 지수함수 — 스캔 그림 다시 그리기 (iN = 문서의 imageN).  python3 draw.py 출력폴더 [이름...]"""
import sys, math
sys.path.insert(0, '/tmp/claude-0/-home-user-CMS/7a122d51-a5b1-5def-9637-d43cb9a9b6ef/scratchpad/figw')
from dcommon import *
OUT = sys.argv[1]
M = (16, 16, 16, 16)


def i2():  # 4⑴ y=2^(2x-4)+5, 2≤x≤4
    f = lambda x: 2 ** (2 * x - 4) + 5
    F = Frame((-0.8, 5.2), (-2.5, 25), 52, 9, (16, 16, 170, 16))
    F.axes(); O(F, 'rt', -6, 4)
    pc(F, f, -0.8, 2, -3, 24.5, dash=True); pc(F, f, 2, 4, -3, 24.5); pc(F, f, 4, 4.4, -3, 24.5, dash=True)
    hline(F, 5, -0.8, 5.1)
    fdot(F, (2, 6)); fdot(F, (4, 21))
    vline(F, 2, 0, 6); vline(F, 4, 0, 21); hline(F, 21, 0, 4); hline(F, 6, 0, 2)
    F.lab((2, 0), '2', 'ct', 0, 8); F.lab((4, 0), '4', 'ct', 0, 8)
    F.lab((0, 21), '21', 'rc', -8, 0); F.lab((0, 6), '6', 'rb', -8, -2); F.lab((5.1, 5), 'y=5', 'rb', 0, -6)
    F.lab((4.2, 23.5), 'y=2^{2x-4}+5', 'lc', 10, 0)
    return F.render()


def i3():  # 4⑵ y=3(2/3)^x, -1≤x≤1
    f = lambda x: 3 * (2 / 3) ** x
    F = Frame((-1.7, 2.8), (-0.6, 5.4), 70, 52, (16, 16, 200, 16))
    F.axes(); O(F, 'rt', -6, 4)
    pc(F, f, -1.7, -1, -1, 5.3, dash=True); pc(F, f, -1, 1, -1, 5.3); pc(F, f, 1, 2.7, -1, 5.3, dash=True)
    fdot(F, (-1, 4.5)); fdot(F, (1, 2))
    vline(F, -1, 0, 4.5); hline(F, 4.5, -1, 0); vline(F, 1, 0, 2); hline(F, 2, 0, 1)
    F.lab((-1, 0), '-1', 'ct', 0, 8); F.lab((1, 0), '1', 'ct', 0, 8)
    F.lab((0, 4.5), '\\dfrac{9}{2}', 'lc', 8, 0); F.lab((0, 3), '3', 'lb', 6, -2); F.lab((0, 2), '2', 'rc', -8, 0)
    F.lab((2.0, f(2.0)), 'y=2^{x}\\times3^{-x+1}', 'lb', 6, -8)
    return F.render()


def i5():  # 7번 해설 y=3^x, x1<x2
    f = lambda x: 3 ** x
    F = Frame((-2.6, 1.9), (-0.6, 4.6), 52, 52, (16, 16, 80, 16))
    F.axes(); O(F, 'rt', -6, 4)
    pc(F, f, -2.6, 1.6, -1, 4.4)
    vline(F, 0.35, 0, f(0.35)); vline(F, 0.95, 0, f(0.95))
    F.lab((0.35, 0), 'x_{1}', 'ct', 0, 8); F.lab((0.95, 0), 'x_{2}', 'ct', 0, 8)
    F.lab((0, 1), '1', 'rb', -6, -2); F.lab((1.3, f(1.3)), 'y=3^{x}', 'lc', 10, 0)
    return F.render()


def i6():  # 12⑴
    f = lambda x: 5 * 3 ** (x + 2) + 1; g = lambda x: 5 * 3 ** x
    F = Frame((-5.2, 1.3), (-1, 9.5), 46, 30, M)
    F.axes(); O(F, 'rt', -6, 4)
    pc(F, f, -5.2, 0, -1, 9.3); pc(F, g, -5.2, 1.3, -1, 9.3, dash=True); hline(F, 1, -5.2, 1.2)
    F.lab((0, 5), '5', 'lc', 6, 0); F.lab((0, 1), '1', 'lt', 6, 4)
    F.lab((-2.1, f(-2.1)), 'y=5\\times3^{x+2}+1', 'rc', -10, 0)
    F.lab((-4.5, 0.2), 'y=5\\times3^{x}', 'ct', 0, 12)
    return F.render()


def i7():  # 12⑵ y=3^(-x-1)-1 (y=3^-x 점선)
    f = lambda x: 3 ** (-x - 1) - 1; g = lambda x: 3 ** (-x)
    F = Frame((-2.6, 2.6), (-1.9, 3.9), 56, 56, M)
    F.axes(); O(F, 'rt', -6, 4)
    pc(F, f, -2.6, 2.6, -2, 3.8); pc(F, g, -2.6, 2.6, -2, 3.8, dash=True); hline(F, -1, -2.6, 2.6)
    F.lab((-1, 0), '-1', 'ct', -4, 8); F.lab((0, -1), '-1', 'rt', -6, 4); F.lab((0, 1), '1', 'lb', 6, -2)
    F.leader((0, -2 / 3), (0.7, -0.45)); F.lab((0.7, -0.45), '-\\dfrac{2}{3}', 'lb', 2, 0)
    F.lab((1.7, g(1.7)), 'y=3^{-x}', 'lb', 0, -8); F.lab((1.6, -1), 'y=3^{-x-1}-1', 'ct', 0, 10)
    return F.render()


def i8():  # 12⑶ y=-3^(x-2)+2 (y=-3^x 점선)
    f = lambda x: -3 ** (x - 2) + 2; g = lambda x: -3 ** x
    F = Frame((-3.2, 3.4), (-3.3, 3.0), 50, 50, (16, 16, 200, 16))
    F.axes(); O(F, 'rt', -6, 4)
    pc(F, f, -3.2, 3.4, -3.3, 2.9); pc(F, g, -3.2, 3.4, -3.3, 2.9, dash=True); hline(F, 2, -3.2, 3.3)
    F.lab((0, 2), '2', 'lb', 6, -2); F.lab((0, -1), '-1', 'lc', 8, 0)
    F.leader((0, 17 / 9), (-1.0, 1.0)); F.lab((-1.0, 1.0), '\\dfrac{17}{9}', 'rt', -2, 0)
    F.lab((3.0, -2.6), 'y=-3^{x-2}+2', 'lc', 14, 0); F.lab((0.9, g(0.9)), 'y=-3^{x}', 'lc', 10, 0)
    return F.render()


def i9():  # 12⑷ y=-(1/3)^(x-1)-2 (y=-(1/3)^x 점선)
    f = lambda x: -(1 / 3) ** (x - 1) - 2; g = lambda x: -(1 / 3) ** x
    F = Frame((-2.2, 3.6), (-6.2, 0.9), 62, 34, (16, 16, 30, 16))
    F.axes(); O(F, 'rt', -6, 4)
    pc(F, f, -2.2, 3.6, -6.1, 0.8); pc(F, g, -2.2, 3.6, -6.1, 0.8, dash=True); hline(F, -2, -2.2, 3.5)
    F.lab((0, -1), '-1', 'rt', -6, 2); F.lab((0, -2), '-2', 'rt', -6, 4); F.lab((0, -5), '-5', 'rc', -8, 0)
    F.lab((1.2, -0.95), 'y=-\\left(\\dfrac{1}{3}\\right)^{x}', 'lc', 0, 0)
    F.lab((0.9, -4.3), 'y=-\\left(\\dfrac{1}{3}\\right)^{x-1}-2', 'lc', 0, 0)
    return F.render()


def i10():  # 15⑴
    f = lambda x: 2 ** (x + 3) + 1; g = lambda x: 2 ** x
    F = Frame((-5.2, 3.6), (-0.8, 10.2), 40, 30, M)
    F.axes(); O(F, 'rt', -6, 4)
    pc(F, f, -5.2, 3.6, -1, 10); pc(F, g, -5.2, 3.6, -1, 10); hline(F, 1, -5.2, 3.5)
    F.lab((0, 9), '9', 'lc', 6, 0); F.lab((0, 1), '1', 'rb', -6, -2)
    F.lab((-1.4, f(-1.4)), 'y=2^{x+3}+1', 'rc', -10, 0); F.lab((3.0, g(3.0)), 'y=2^{x}', 'rc', -8, 0)
    return F.render()


def i11():  # 15⑵
    f = lambda x: (1 / 4) ** x; g = lambda x: 4 ** (-x - 2) - 2
    F = Frame((-2.2, 2.6), (-2.7, 2.3), 66, 66, (16, 16, 30, 16))
    F.axes(); O(F, 'rt', -6, 4)
    pc(F, f, -2.2, 2.6, -2.7, 2.2); pc(F, g, -2.2, 2.6, -2.7, 2.2); hline(F, -2, -2.2, 2.5)
    F.lab((0, 1), '1', 'lb', 6, -2); F.lab((0, -2), '-2', 'rt', -6, 4)
    F.leader((0, -31 / 16), (-0.7, -1.1)); F.lab((-0.7, -1.1), '-\\dfrac{31}{16}', 'rb', -2, 0)
    F.lab((0.8, 1.1), 'y=\\left(\\dfrac{1}{4}\\right)^{x}', 'lc', 0, 0)
    F.lab((0.8, -1.25), 'y=4^{-x-2}-2', 'lc', 0, 0)
    return F.render()


def i12():  # 15⑶
    f = lambda x: 2 ** x; g = lambda x: -2 ** (x + 2) - 1
    F = Frame((-3.2, 2.2), (-6.2, 3.2), 54, 34, (16, 16, 120, 16))
    F.axes(); O(F, 'rt', -6, 4)
    pc(F, f, -3.2, 2.2, -6.2, 3.1); pc(F, g, -3.2, 2.2, -6.2, 3.1); hline(F, -1, -3.2, 2.1)
    F.lab((0, 1), '1', 'rb', -6, -2); F.lab((0, -1), '-1', 'lt', 6, 4); F.lab((0, -5), '-5', 'lc', 8, 0)
    F.lab((1.5, f(1.5)), 'y=2^{x}', 'rc', -8, 0); F.lab((0.5, -4.0), 'y=-2^{x+2}-1', 'lc', 8, 0)
    return F.render()


def i13():  # 15⑷
    f = lambda x: (1 / 3) ** x; g = lambda x: -(1 / 3) ** (x - 1) + 2
    F = Frame((-1.3, 3.6), (-1.9, 2.9), 62, 62, (16, 16, 230, 16))
    F.axes(); O(F, 'rt', -6, 4)
    pc(F, f, -1.3, 3.6, -1.9, 2.8); pc(F, g, -1.3, 3.6, -1.9, 2.8); hline(F, 2, -1.3, 3.5)
    F.lab((0, 2), '2', 'lb', 6, -2); F.lab((0, 1), '1', 'rc', -8, 0); F.lab((0, -1), '-1', 'rc', -8, 0)
    F.lab((3.6, 0.35), 'y=\\left(\\dfrac{1}{3}\\right)^{x}', 'lc', 8, 0)
    F.lab((3.6, 1.55), 'y=-\\left(\\dfrac{1}{3}\\right)^{x-1}+2', 'lc', 8, 0)
    return F.render()


def i14():  # 17번 문제 y=f(x)=3^(x+1)-2
    f = lambda x: 3 ** (x + 1) - 2
    F = Frame((-3.4, 1.6), (-2.9, 3.2), 54, 54, M)
    F.axes(); O(F, 'lt', 4, 4)
    pc(F, f, -3.4, 1.6, -3, 3.1); hline(F, -2, -3.4, 1.5)
    F.lab((0, 1), '1', 'rb', -6, -2); F.lab((0, -2), '-2', 'rt', -6, 4)
    F.lab((0.35, f(0.35)), 'y=f(x)', 'lc', 10, 0)
    return F.render()


def i15():  # 35번 해설 y=(t-8)^2-34, 2≤t≤16
    f = lambda t: (t - 8) ** 2 - 34
    F = Frame((-1.5, 19.5), (-38, 40), 15, 4.2, (40, 16, 190, 16))
    F.axes('t', 'y'); O(F, 'rt', -6, 4)
    pc(F, f, -0.6, 2, -38, 39, dash=True); pc(F, f, 2, 16, -38, 39); pc(F, f, 16, 16.8, -38, 39, dash=True)
    fdot(F, (2, 2)); fdot(F, (16, 30))
    hline(F, 30, 0, 16); vline(F, 16, 0, 30); hline(F, -34, 0, 8); vline(F, 8, -34, 0)
    F.lab((2, 0), '2', 'lt', 2, 6); F.lab((8, 0), '8', 'cb', 0, -8); F.lab((16, 0), '16', 'lt', 6, 6)
    F.lab((0, 30), '30', 'rc', -8, 0); F.lab((0, 2), '2', 'rb', -8, -2); F.lab((0, -34), '-34', 'rc', -8, 0)
    F.lab((12.5, f(12.5)), 'y=(t-8)^{2}-34', 'lc', 12, 0)
    return F.render()


def i16():  # 37번 해설 y=(t-1)^2+2, 1/2≤t≤4
    f = lambda t: (t - 1) ** 2 + 2
    F = Frame((-0.7, 5.0), (-0.8, 12.8), 62, 18, (16, 16, 16, 60))
    F.axes('t', 'y'); O(F, 'rt', -6, 4)
    pc(F, f, -0.7, 0.5, 0, 12.6, gray=True); pc(F, f, 0.5, 4, 0, 12.6); pc(F, f, 4, 4.4, 0, 12.6, gray=True)
    fdot(F, (0.5, 2.25)); fdot(F, (1, 2)); fdot(F, (4, 11))
    vline(F, 0.5, 0, 2.25); vline(F, 1, 0, 2); vline(F, 4, 0, 11); hline(F, 11, 0, 4); hline(F, 2, 0, 1)
    F.lab((0.5, 0), '\\dfrac{1}{2}', 'ct', -4, 6); F.lab((1, 0), '1', 'ct', 4, 8); F.lab((4, 0), '4', 'ct', 0, 8)
    F.lab((0, 11), '11', 'rc', -8, 0); F.lab((0, 2), '2', 'rc', -8, 0)
    F.lab((3.0, f(3.0)), 'y=(t-1)^{2}+2', 'rc', -12, 0)
    return F.render()


def i17():  # 57번 문제 y=2^x, y=x 계단
    f = lambda x: 2 ** x
    a = 0.25; b = f(a); c = f(b); d = f(c)
    F = Frame((-0.9, 5.6), (-0.9, 5.6), 54, 54, (16, 16, 70, 16))
    F.axes(); O(F, 'rt', -6, 4)
    pc(F, f, -0.9, 5.6, -1, 5.5); F.seg((-0.9, -0.9), (5.4, 5.4))
    for x, y in [(a, b), (b, c), (c, d)]:
        hline(F, y, 0, y); vline(F, x, 0, y)
    vline(F, d, 0, d)
    for x, t in [(a, 'a'), (b, 'b'), (c, 'c'), (d, 'd')]:
        F.lab((x, 0), t, 'ct', 0, 8)
    F.lab((0, 1), '1', 'rc', -8, 0)
    F.lab((2.4, f(2.4)), 'y=2^{x}', 'rc', -8, 0); F.lab((5.2, 5.2), 'y=x', 'lc', 8, 0)
    return F.render()


def i18():  # 59번 해설
    f = lambda x: (1 / 4) ** (x - 1) - 4; g = lambda x: (1 / 4) ** (x - 1) - 6
    F = Frame((-0.6, 4.4), (-7.0, 1.6), 62, 34, M)
    F.axes(); O(F, 'lb', 4, -4)
    pc(F, f, -0.6, 4.4, -7, 1.5); pc(F, g, -0.6, 4.4, -7, 1.5); hline(F, -4, -0.6, 4.3); hline(F, -6, -0.6, 4.3)
    F.lab((0, -4), '-4', 'rb', -6, -2); F.lab((0, -6), 'n', 'rt', -6, 4)
    F.lab((2.0, f(2.0)), 'y=\\left(\\dfrac{1}{4}\\right)^{x-1}-4', 'lb', 8, -6)
    F.lab((2.0, g(2.0)), 'y=\\left(\\dfrac{1}{4}\\right)^{x-1}+n', 'lb', 8, -6)
    return F.render()


def i19():  # 62번 해설 y=(t-3)^2-9+k (k=-9), 3≤t≤9
    f = lambda t: (t - 3) ** 2 - 18
    F = Frame((-1.6, 11), (-21, 24), 30, 9, (80, 16, 260, 16))
    F.axes('t', 'y'); O(F, 'rt', -6, 4)
    pc(F, f, -1.2, 3, -21, 23, dash=True); pc(F, f, 3, 9, -21, 23); pc(F, f, 9, 9.6, -21, 23, dash=True)
    fdot(F, (3, -18)); fdot(F, (9, 18))
    hline(F, 18, 0, 9); vline(F, 9, 0, 18); hline(F, -18, 0, 3); vline(F, 3, -18, 0)
    F.lab((3, 0), '3', 'cb', 0, -8); F.lab((9, 0), '9', 'lt', 6, 6)
    F.lab((0, 18), '27+k', 'rc', -8, 0); F.lab((0, -18), '-9+k', 'rc', -8, 0)
    F.lab((9.4, 6), 'y=(t-3)^{2}-9+k', 'lc', 6, 0)
    return F.render()


def i20():  # 65번 문제 곡선 y=f(x)와 직선 y=g(x)
    A, B, D = -2.5, -0.4, 2.6
    f = lambda x: -0.25 * (x - A) * (x - B) * (x - D)
    m = f(0) / (-A); g = lambda x: m * (x - A)
    c = bisect(lambda x: f(x) - g(x), 1.0, 2.5)
    F = Frame((-3.3, 3.4), (-1.6, 2.4), 60, 60, (16, 40, 16, 16))
    F.axes(); O(F, 'lt', 4, 4)
    pc(F, f, -3.3, 3.4, -1.6, 2.35); pc(F, g, -3.3, 3.4, -1.6, 2.35, wd=2.0)
    vline(F, c, 0, f(c))
    F.lab((A, 0), 'a', 'rt', -2, 6); F.lab((B, 0), 'b', 'rt', -4, 6); F.lab((c, 0), 'c', 'ct', 0, 8); F.lab((D, 0), 'd', 'lt', 4, 6)
    F.lab((-3.15, 2.2), 'y=f(x)', 'lc', 10, 0); F.lab((3.1, g(3.1)), 'y=g(x)', 'rb', 0, -10)
    return F.render()


def sq(F, lab_axes):
    f4 = lambda x: 4 ** x; f2 = lambda x: 2 ** x
    pc(F, f4, -1.6, 1.3, -0.5, 5.4); pc(F, f2, -1.6, 2.45, -0.5, 5.4)
    e = math.log2(3)
    F.polyline([(1, 4), (2, 4), (2, 3), (1, 3), (1, 4)])
    F.pt((1, 4), 'A', 'rb', -6, -4); F.pt((2, 4), 'D', 'lb', 4, -4); F.pt((1, 3), 'B', 'rt', -6, 4)
    F.pt((2, 3), 'C', 'lt', 6, 4); F.pt((e, 3), 'E', 'ct', 0, 8)
    F.lab((0, 1), '1', 'rb', -6, -2)
    F.lab((1.2, f4(1.2)), 'y=4^{x}', 'rc', -8, 0); F.lab((2.4, f2(2.4)), 'y=2^{x}', 'lc', 8, 0)
    if lab_axes:
        hline(F, 4, 0, 1); hline(F, 3, 0, 1); vline(F, 1, 0, 3); vline(F, 2, 0, 3)
        F.lab((0, 4), '4^{a}', 'rc', -8, 0); F.lab((0, 3), '4^{a}-1', 'rc', -8, 0)
        F.lab((1, 0), 'a', 'ct', 0, 8); F.lab((2, 0), 'a+1', 'ct', 0, 8)


def i21():  # 68번 해설
    F = Frame((-1.6, 2.9), (-0.6, 5.5), 70, 52, (16, 16, 70, 16))
    F.axes(); O(F, 'rt', -6, 4); sq(F, True)
    return F.render()


def i22():  # 68번 문제
    F = Frame((-1.6, 2.9), (-0.6, 5.5), 70, 52, (16, 16, 70, 16))
    F.axes(); O(F, 'rt', -6, 4); sq(F, False)
    return F.render()


JOBS = {k: v for k, v in globals().items() if k[0] == 'i' and k[1:].isdigit()}
if __name__ == '__main__':
    run(JOBS, OUT, sys.argv[2:])
