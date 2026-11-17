# -*- coding: utf-8 -*-
"""대수 C 4. 로그함수 — 스캔 그림 다시 그리기 (iN = 문서의 imageN)"""
import sys, math
sys.path.insert(0, '/tmp/claude-0/-home-user-CMS/7a122d51-a5b1-5def-9637-d43cb9a9b6ef/scratchpad/figw')
from dcommon import *
from mathfig import right_mark
OUT = sys.argv[1]
L2 = lambda x: math.log2(x) if x > 0 else None
L3 = lambda x: math.log(x, 3) if x > 0 else None
L4 = lambda x: math.log(x, 4) if x > 0 else None


def i2():  # 1번 y=log5 x
    f = lambda x: math.log(x, 5) if x > 0 else None
    F = Frame((-1.5, 30), (-1.3, 2.8), 11, 60, (16, 16, 30, 16))
    F.axes(); O(F, 'rt', -6, 4)
    pc(F, f, 0.002, 29, -1.3, 2.7)
    hline(F, 1, 0, 5); vline(F, 5, 0, 1); hline(F, 2, 0, 25); vline(F, 25, 0, 2)
    F.pt((5, 0), 'A', 'ct', 0, 8); F.pt((25, 0), 'B', 'ct', 0, 8)
    F.lab((0, 1), '1', 'rc', -8, 0); F.lab((0, 2), '2', 'rc', -8, 0)
    F.lab((15, f(15)), 'y=\\log_{5}x', 'cb', 0, -12)
    return F.render()


def sq11(F, coords):
    pc(F, L2, 0.03, 5.4, -1.6, 2.8)
    F.polyline([(2, 0), (2, 2), (4, 2), (4, 0)])
    F.pt((4, 2), 'A', 'lc', 8, 4); F.pt((2, 2), 'B', 'rb', -6, -2); F.pt((2, 0), 'C', 'ct', 0, 8)
    F.pt((4, 0), 'D', 'ct', 0, 8); F.pt((2, 1), 'E', 'lc', 8, 6)
    F.lab((1, 0), '1', 'ct', 0, 8); F.lab((4.6, L2(4.6)), 'y=\\log_{2}x', 'cb', 0, -12)
    if coords:
        F.lab((0, 2), '2', 'rc', -8, 0); hline(F, 2, 0, 2)


def i4():  # 11번 해설
    F = Frame((-0.6, 5.5), (-1.6, 3.1), 60, 60, (16, 16, 30, 16))
    F.axes(); O(F, 'rt', -6, 4); sq11(F, True)
    return F.render()


def i5():  # 11번 문제
    F = Frame((-0.6, 5.5), (-1.6, 3.1), 60, 60, (16, 16, 30, 16))
    F.axes(); O(F, 'rt', -6, 4); sq11(F, False)
    return F.render()


def i6():  # 12⑴ y=log3(x+1), y=log3 x
    F = Frame((-1.8, 5.5), (-2.4, 2.2), 52, 52, (16, 16, 180, 16))
    F.axes(); O(F, 'rt', -6, 4)
    pc(F, lambda x: L3(x + 1), -0.999, 5.4, -2.4, 2.1); pc(F, L3, 0.001, 5.4, -2.4, 2.1, gray=True)
    vline(F, -1, -2.4, 2.1)
    F.lab((-1, 0), '-1', 'rt', -4, 6); F.lab((1, 0), '1', 'ct', 4, 8)
    F.lab((5.4, L3(6.4)), 'y=\\log_{3}(x+1)', 'lc', 8, -4); F.lab((5.4, L3(5.4)), 'y=\\log_{3}x', 'lt', 8, 6)
    return F.render()


def i7():  # 12⑵ y=log3 3x, y=log3 x
    F = Frame((-0.6, 5.5), (-2.4, 2.4), 52, 52, (16, 16, 150, 16))
    F.axes(); O(F, 'rt', -6, 4)
    pc(F, lambda x: L3(3 * x), 0.001, 5.4, -2.4, 2.35); pc(F, L3, 0.001, 5.4, -2.4, 2.35, gray=True)
    hline(F, 1, 0, 1); vline(F, 1, 0, 1)
    F.lab((1, 0), '1', 'ct', 0, 8); F.lab((0, 1), '1', 'rc', -8, 0)
    F.lab((5.4, 2.15), 'y=\\log_{3}3x', 'lc', 8, 0); F.lab((5.4, L3(5.4)), 'y=\\log_{3}x', 'lc', 8, 0)
    return F.render()


def i8():  # 13번 해설
    f = lambda x: -L2(-x) if x < 0 else None
    g = lambda x: -L2(3 - x) + 4 if x < 3 else None
    F = Frame((-4.2, 4.2), (-2.6, 6.4), 46, 40, (230, 16, 16, 16))
    F.axes(); O(F, 'lt', 4, 4)
    pc(F, f, -4.2, -0.0005, -2.6, 6.3); pc(F, g, -4.2, 2.9999, -2.6, 6.3)
    vline(F, 3, -2.6, 6.3); hline(F, 4, 0, 2); vline(F, 2, 0, 4)
    F.lab((-1, 0), '-1', 'rt', -4, 6); F.lab((2, 0), '2', 'ct', 0, 8); F.lab((3, 0), '3', 'lt', 4, 6); F.lab((0, 4), '4', 'lt', 4, 4)
    F.lab((-0.15, 6.0), 'y=-\\log_{2}(-x)', 'rc', -8, 0); F.lab((-3.6, g(-3.6)), 'y=-\\log_{2}(3-x)+4', 'rb', 0, -8)
    return F.render()


def i9():  # 15번 해설 y=log3((x+3)/9)
    f = lambda x: L3((x + 3) / 9) if x > -3 else None
    F = Frame((-4.2, 8.6), (-3.0, 1.6), 38, 52, (16, 16, 30, 16))
    F.axes(); O(F, 'lb', 4, -4)
    pc(F, f, -2.999, 8.5, -3, 1.5); vline(F, -3, -3, 1.5)
    F.lab((-3, 0), '-3', 'rb', -4, -4); F.lab((6, 0), '6', 'ct', 0, 8); F.lab((0, -1), '-1', 'lt', 6, 4)
    F.lab((6.4, f(6.4)), 'y=\\log_{3}\\dfrac{x+3}{9}', 'cb', 0, -10)
    return F.render()


def i10():  # 17번 문제 y=2log_{1/2}(4-x)+2
    f = lambda x: 2 - 2 * L2(4 - x) if x < 4 else None
    F = Frame((-4.6, 5.4), (-4.4, 4.6), 46, 40, (16, 16, 30, 16))
    F.axes(); O(F, 'rt', -6, 4)
    pc(F, f, -4.6, 3.9999, -4.4, 4.5); vline(F, 4, -4.4, 4.5)
    F.lab((2, 0), '2', 'lt', 4, 6); F.lab((4, 0), '4', 'lt', 4, 6); F.lab((0, -2), '-2', 'rc', -8, 0)
    F.lab((-4.5, 3.4), 'y=k\\log_{1/2}(a-x)+b', 'lc', 0, 0)
    return F.render()


def i11_12(full):
    f = lambda x: 2 ** x - 1; g = lambda x: L2(x + 1) if x > -1 else None
    F = Frame((-0.9, 4.4), (-0.9, 4.4), 60, 60, (16, 16, 220, 16))
    F.axes(); O(F, 'rt', -6, 4)
    pc(F, f, -0.9, 4.4, -0.9, 4.3); pc(F, g, -0.89, 4.4, -0.9, 4.3)
    F.seg((2, 3), (3, 2)); vline(F, 2, 0, 3); vline(F, 3, 0, 2)
    right_mark(F, (2, 0), (3, 0), (2, 1)); right_mark(F, (3, 0), (4, 0), (3, 1))
    F.pt((2, 0), 'C', 'ct', 0, 8); F.pt((3, 0), 'D', 'ct', 0, 8)
    F.lab((2.45, 4.25), 'y=2^{x}-1', 'lc', 8, 0); F.lab((4.3, g(4.3)), 'y=\\log_{2}(x+1)', 'lb', 6, -6)
    if full:
        F.seg((-0.9, -0.9), (4.2, 4.2), 2.0); F.lab((3.7, 3.7), 'y=x', 'lt', 8, 6)
        F.lab((2, 3), '\\mathrm{A}(2,\\,3)', 'rc', -8, 0); F.lab((3, 2), '\\mathrm{B}(3,\\,2)', 'lt', 6, 4)
        F.seg((1.4, 3.6), (3.8, 1.2), 2.0)
    else:
        F.pt((2, 3), 'A', 'rc', -8, 0); F.pt((3, 2), 'B', 'lt', 6, 4)
    return F.render()


def i11(): return i11_12(True)
def i12(): return i11_12(False)


def i13_14(full):
    f = lambda x: 3 ** x - 3; g = lambda x: L3(x + 3) if x > -3 else None
    F = Frame((-3.2, 8.2), (-3.4, 7.2), 40, 40, (110, 16, 190, 16))
    F.axes(); O(F, 'rt', -6, 4)
    pc(F, f, -3.2, 8.2, -3.4, 7.0); pc(F, g, -2.999, 8.0, -3.4, 7.0)
    F.seg((2, 6), (6, 2)); vline(F, 2, 0, 6); vline(F, 6, 0, 2)
    right_mark(F, (2, 0), (3, 0), (2, 1)); right_mark(F, (6, 0), (7, 0), (6, 1))
    F.pt((2, 0), 'D', 'ct', 0, 8); F.pt((6, 0), 'C', 'ct', 0, 8)
    F.lab((1, 0), '1', 'rt', -2, 6); F.lab((-2, 0), '-2', 'rb', -2, -4); F.lab((0, 1), '1', 'rb', -6, -2); F.lab((0, -2), '-2', 'lt', 6, 4)
    F.lab((8.0, g(8.0)), 'y=\\log_{3}(x+3)', 'lb', 4, -8)
    if full:
        F.seg((-3.2, -3.2), (7.0, 7.0), 2.0); F.lab((7.0, 7.0), 'y=x', 'lc', 8, 0)
        F.lab((-0.2, 5.4), 'y=3^{x}-3', 'rc', 0, 0)
        F.lab((2, 6), '\\mathrm{B}(2,\\,6)', 'lb', 8, -2); F.lab((6, 2), '\\mathrm{A}(6,\\,2)', 'lt', 6, 4)
    else:
        F.pt((2, 6), 'B', 'lb', 8, -2); F.pt((6, 2), 'A', 'lt', 6, 4)
    return F.render()


def i13(): return i13_14(True)
def i14(): return i13_14(False)


def i15():  # 26번 문제
    F = Frame((-0.8, 5.4), (-0.8, 5.0), 62, 62, (16, 16, 150, 16))
    F.axes(); O(F, 'rt', -6, 4)
    pc(F, lambda x: 2 ** x, -0.8, 2.4, -0.8, 4.9); pc(F, L2, 0.5, 5.4, -0.8, 4.9)
    F.seg((-0.3, -0.6), (2.4, 4.8), 2.0); F.seg((-0.8, -0.4), (5.3, 2.65), 2.0)
    F.seg((1, 2), (2, 1)); F.seg((2, 4), (4, 2))
    F.pt((2, 1), 'A', 'ct', 2, 8); F.pt((4, 2), 'B', 'ct', 2, 8); F.pt((1, 2), 'C', 'rc', -8, -2); F.pt((2, 4), 'D', 'rb', -6, -2)
    F.lab((2.2, 4.4), 'y=nx', 'lc', 8, 0); F.lab((1.5, 2 ** 1.5), 'y=2^{x}', 'rc', -10, 0)
    F.lab((5.3, 2.65), 'y=mx', 'lb', 4, -4); F.lab((5.3, L2(5.3)), 'y=\\log_{2}x', 'lt', 4, 6)
    return F.render()


def i16():  # 41번 해설 y=(t-1)^2-9, -2≤t≤2
    f = lambda t: (t - 1) ** 2 - 9
    F = Frame((-3.4, 4.6), (-10.5, 4), 52, 22, (16, 16, 150, 16))
    F.axes('t', 'y'); O(F, 'lb', 4, -4)
    pc(F, f, -3.2, -2, -10.4, 3.9, gray=True); pc(F, f, -2, 2, -10.4, 3.9); pc(F, f, 2, 4.4, -10.4, 3.9, gray=True)
    fdot(F, (-2, 0)); fdot(F, (1, -9)); fdot(F, (2, -8))
    vline(F, 1, 0, -9); vline(F, 2, 0, -8); hline(F, -9, 0, 1); hline(F, -8, 0, 2)
    F.lab((-2, 0), '-2', 'rb', -2, -6); F.lab((1, 0), '1', 'cb', 0, -6); F.lab((2, 0), '2', 'cb', 2, -6)
    F.lab((0, -9), '-9', 'rc', -8, 0); F.lab((0, -8), '-8', 'rc', -8, 0)
    F.lab((2.7, -4.5), 'y=(t-1)^{2}-9', 'lc', 10, 0)
    return F.render()


def i17():  # 42번 해설 y=-(t-1)^2+11, 0≤t≤4
    f = lambda t: -(t - 1) ** 2 + 11
    F = Frame((-1.6, 5.0), (-1.2, 12.6), 62, 22, (16, 16, 130, 16))
    F.axes('t', 'y'); O(F, 'rt', -6, 4)
    pc(F, f, -1.6, 0, -1.2, 12.5, gray=True); pc(F, f, 0, 4, -1.2, 12.5); pc(F, f, 4, 4.5, -1.2, 12.5, gray=True)
    fdot(F, (0, 10)); fdot(F, (1, 11)); fdot(F, (4, 2))
    vline(F, 1, 0, 11); vline(F, 4, 0, 2); hline(F, 11, 0, 1); hline(F, 2, 0, 4)
    F.lab((1, 0), '1', 'ct', 0, 8); F.lab((4, 0), '4', 'ct', 0, 8)
    F.lab((0, 11), '11', 'rc', -8, 0); F.lab((0, 10), '10', 'rc', -8, 4); F.lab((0, 2), '2', 'rc', -8, 0)
    F.lab((2.6, f(2.6)), 'y=-(t-1)^{2}+11', 'lb', 10, 0)
    return F.render()


def i18():  # 52번 해설
    f = lambda x: x * (4 - x)
    F = Frame((-0.9, 5.4), (-1.3, 5.2), 54, 46, (16, 16, 120, 16))
    F.axes(); O(F, 'rt', -6, 4)
    pc(F, f, -0.35, 0, -1.3, 5.1, gray=True); pc(F, f, 0, 4, -1.3, 5.1); pc(F, f, 4, 4.3, -1.3, 5.1, gray=True)
    odot(F, (0, 0)); odot(F, (4, 0)); hline(F, 4, 0, 2)
    F.seg((-0.9, 2.2), (5.3, 2.2), 2.0)
    F.lab((4, 0), '4', 'lt', 6, 6); F.lab((0, 4), '4', 'rc', -8, 0)
    F.lab((3.2, f(3.2)), 'y=x(4-x)', 'lb', 10, -4); F.lab((5.3, 2.2), 'y=2^{k}', 'lc', 8, 0)
    return F.render()


def i19_20(sol):
    a = 6.0; b = L2(a); c = L2(b); d = L2(c)
    F = Frame((-0.9, 6.9), (-1.6, 4.0), 58, 58, (130 if sol else 40, 16, 140, 16))
    F.axes(); O(F, 'rt', -6, 4)
    pc(F, L2, 0.3, 6.8, -1.6, 3.9); F.seg((-0.9, -0.9), (3.9, 3.9), 2.0)
    for x in (a, b, c):
        vline(F, x, 0, L2(x))
    for y, x in ((b, a), (c, b), (d, c)):
        hline(F, y, 0, x)
    F.lab((a, 0), 'a', 'ct', 0, 8); F.lab((b, 0), 'b', 'ct', 0, 8); F.lab((c, 0), 'c', 'ct', 0, 8)
    F.lab((3.9, 3.9), 'y=x', 'lc', 8, 0); F.lab((6.8, L2(6.8)), 'y=\\log_{2}x', 'lc', 8, 0)
    if sol:
        F.lab((0, b), '\\log_{2}a=b', 'rc', -8, 0); F.lab((0, c), '\\log_{2}b=c', 'rc', -8, 0); F.lab((0, d), 'd', 'rc', -8, 0)
    else:
        F.lab((0, d), 'd', 'rc', -8, 0)
    return F.render()


def i19(): return i19_20(True)
def i20(): return i19_20(False)


def i21():  # 62번 해설 y=log2(2-x)-1
    f = lambda x: L2(2 - x) - 1 if x < 2 else None
    F = Frame((-3.6, 3.0), (-3.4, 1.8), 52, 52, (16, 16, 30, 16))
    F.axes(); O(F, 'rt', -6, 4)
    pc(F, f, -3.6, 1.9999, -3.4, 1.7); vline(F, 2, -3.4, 1.7)
    F.lab((2, 0), '2', 'rt', -4, 6); F.lab((-2.4, f(-2.4)), 'y=\\log_{2}(2-x)-1', 'cb', 0, -10)
    return F.render()


def i22():  # 69번 해설 y=log2 x, y=log3 x
    F = Frame((-0.6, 5.6), (-2.2, 2.6), 60, 60, (16, 16, 140, 16))
    F.axes(); O(F, 'rt', -6, 4)
    pc(F, L2, 0.2, 5.5, -2.2, 2.5); pc(F, L3, 0.1, 5.5, -2.2, 2.5)
    F.lab((1, 0), '1', 'ct', 2, 8)
    F.lab((5.5, L2(5.5)), 'y=\\log_{2}x', 'lc', 8, 0); F.lab((5.5, L3(5.5)), 'y=\\log_{3}x', 'lc', 8, 0)
    return F.render()


def i23_24(sol):
    F = Frame((-0.6, 5.4), (-1.2, 2.8), 62, 95, (60 if sol else 16, 16, 140, 16))
    F.axes(); O(F, 'rt', -6, 4)
    pc(F, L2, 0.4, 5.0, -1.2, 2.6); pc(F, L4, 0.2, 5.0, -1.2, 2.6)
    F.seg((2, 0.5), (2, 1)); F.seg((2, 1), (4, 1)); F.seg((4, 1), (4, 2))
    F.pt((2, 0.5), 'A', 'lt', 4, 4); F.pt((2, 1), 'B', 'rb', -4, -4); F.pt((4, 1), 'C', 'lt', 4, 4); F.pt((4, 2), 'D', 'rb', -4, -4)
    F.lab((1, 0), '1', 'ct', 2, 8)
    F.lab((5.0, L2(5.0)), 'y=\\log_{2}x', 'lc', 8, 0); F.lab((5.0, L4(5.0)), 'y=\\log_{4}x', 'lc', 8, 0)
    if sol:
        hline(F, 2, 0, 4); hline(F, 1, 0, 2); hline(F, 0.5, 0, 2); vline(F, 2, 0, 0.5); vline(F, 4, 0, 1)
        F.lab((2, 0), '2', 'ct', 0, 8); F.lab((4, 0), '4', 'ct', 0, 8)
        F.lab((0, 2), '2', 'rc', -8, 0); F.lab((0, 1), '1', 'rc', -8, 0); F.lab((0, 0.5), '\\dfrac{1}{2}', 'rc', -8, 6)
    return F.render()


def i23(): return i23_24(True)
def i24(): return i23_24(False)


JOBS = {k: v for k, v in globals().items() if k[0] == 'i' and k[1:].isdigit()}
if __name__ == '__main__':
    run(JOBS, OUT, sys.argv[2:])
