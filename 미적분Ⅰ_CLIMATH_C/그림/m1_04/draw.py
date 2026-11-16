# -*- coding: utf-8 -*-
"""미적분Ⅰ 4. 도함수의 활용(1) — 스캔 그림 다시 그리기.  python3 draw.py 출력폴더 [이름...]"""
import sys, math
sys.path.insert(0, '/home/user/CMS/.claude/skills/math-figure-rules'); sys.path.insert(0, '..')
from mathfig import Frame, DASH, SKY, dot, right_mark, dim_arc, roots
from mjcommon import odot, fdot, plot, O, run
OUT = sys.argv[1]
M = (16, 16, 16, 16)
PINK = '#ffd9e6'


def i3():   # 10번 해설 ⑴ y=x²-3x+4, 원점에서 그은 접선 y=-7x, y=x
    F = Frame((-3.0, 3.8), (-2.2, 16.8), 70, 22, (100, 16, 200, 16))
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, lambda x: x * x - 3 * x + 4, -2.6, 3.4)
    F.seg((-2.3, 16.1), (0.28, -1.96), 2.0); F.seg((-1.9, -1.9), (3.6, 3.6), 2.0)
    F.dashed((-2, 0), (-2, 14)); F.dashed((-2, 14), (0, 14)); F.dashed((2, 0), (2, 2)); F.dashed((0, 2), (2, 2))
    fdot(F, (0, 0))
    F.lab((-2, 0), '-2', 'ct', 0, 8); F.lab((2, 0), '2', 'ct', 0, 8); F.lab((0, 14), '14', 'lc', 8, 0); F.lab((0, 2), '2', 'rc', -8, 0)
    F.lab((3.4, 3.4 * 3.4 - 3 * 3.4 + 4), 'y=x^{2}-3x+4', 'lc', 6, 0)
    F.lab((3.6, 3.6), 'y=x', 'lc', 6, 0); F.lab((-2.3, 16.1), 'y=-7x', 'rc', -8, 0)
    return F.render()


def i4():   # 10번 해설 ⑵ y=x³+2x, (0, 2)에서 그은 접선 y=5x+2
    F = Frame((-1.8, 1.9), (-5.0, 7.0), 70, 35, (16, 40, 120, 16))
    F.axes(); O(F, 'lt', 4, 4)
    plot(F, lambda x: x ** 3 + 2 * x, -1.45, 1.45); F.seg((-1.38, -4.9), (0.95, 6.75), 2.0)
    F.dashed((-1, 0), (-1, -3)); F.dashed((-1, -3), (0, -3))
    fdot(F, (0, 2)); fdot(F, (-1, -3))
    F.lab((-1, 0), '-1', 'cb', 0, -8); F.lab((0, 2), '2', 'rc', -8, 0); F.lab((0, -3), '-3', 'lc', 8, 0)
    F.lab((1.45, 1.45 ** 3 + 2.9), 'y=x^{3}+2x', 'lc', 8, 0); F.lab((0.95, 6.75), 'y=5x+2', 'cb', 0, -8)
    return F.render()


def i5():   # 13번 해설 y=|x-1/2|
    F = Frame((-0.5, 1.6), (-0.4, 1.1), 200, 200, (16, 70, 110, 16))
    F.axes(); O(F, 'rt', -6, 4)
    F.polyline([(-0.4, 0.9), (0.5, 0), (1.45, 0.95)], 'stroke-width="3.2" stroke-linejoin="round"')
    F.dashed((0, 0.5), (1, 0.5)); F.dashed((1, 0), (1, 0.5))
    F.lab((0.5, 0), '\\dfrac{1}{2}', 'ct', 0, 8); F.lab((1, 0), '1', 'ct', 0, 8); F.lab((0, 0.5), '\\dfrac{1}{2}', 'rc', -8, 6)
    F.lab((0.5, 0.85), 'y=\\left|x-\\dfrac{1}{2}\\right|', 'cc')
    return F.render()


def i7():   # 22번 문제 f(x)=(x-3)²
    F = Frame((-1.0, 6.2), (-1.5, 11.5), 60, 18, M)
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, lambda x: (x - 3) ** 2, -0.25, 6.25)
    F.lab((3, 0), '3', 'ct', 0, 8); F.lab((0, 9), '9', 'rc', -8, 0)
    F.lab((6.25, 3.25 ** 2), 'y=f(x)', 'rc', -12, 0)
    return F.render()


def i8():   # 27번 문제 y=x³-5x, A(1,-4) 접선 y=-2x-2, B(-2, 2)
    F = Frame((-2.9, 2.9), (-5.2, 5.2), 70, 35, (16, 16, 130, 16))
    F.axes(); O(F, 'lb', 6, -4)
    plot(F, lambda x: x ** 3 - 5 * x, -2.62, 2.65); F.seg((-2.6, 3.2), (1.6, -5.2), 2.0)
    fdot(F, (1, -4)); fdot(F, (-2, 2))
    F.pt((1, -4), 'A', 'rc', -10, 4); F.pt((-2, 2), 'B', 'rc', -10, 0)
    F.lab((2.65, 2.65 ** 3 - 13.25), 'y=x^{3}-5x', 'lc', 6, 0)
    return F.render()


def i9():   # 33번 해설 y=x²+2, A(1,-1), B(-1,3), C(3,11)
    F = Frame((-2.0, 4.0), (-2.5, 13.0), 70, 17, (40, 16, 16, 16))
    A, B, C = (1, -1), (-1, 3), (3, 11)
    F.poly([A, B, C], SKY)
    F.axes(); O(F, 'rb', -6, -4)
    plot(F, lambda x: x * x + 2, -1.75, 3.25)
    F.seg(A, B, 2.0); F.seg(A, C, 2.0); F.seg(B, C, 2.0)
    F.polyline([(-1, -1), (3, -1), (3, 11), (-1, 11), (-1, -1)], DASH + ' stroke-width="1.5"')
    for p in (A, B, C):
        fdot(F, p)
    F.pt(A, 'A', 'ct', 0, 8); F.pt(B, 'B', 'rb', -8, -6); F.pt(C, 'C', 'lc', 10, 0)
    F.lab((1, 0), '1', 'cb', 0, -6); F.lab((3, 0), '3', 'lb', 6, -4); F.lab((-1, 0), '-1', 'rb', -6, -4)
    F.lab((0, 11), '11', 'lb', 6, -4); F.lab((0, 3), '3', 'rc', -8, -6); F.lab((-1, -1), '-1', 'rc', -8, 0)
    F.lab((3.25, 3.25 ** 2 + 2), 'y=x^{2}+2', 'rc', -12, 0)
    return F.render()


# 37번: 극솟값·극댓값·극솟값이 있는 사차함수 개형
def q37(x):
    return 1.2 * (x ** 4 / 4 + 0.2 * x ** 3 / 3 - 1.195 * x * x - 0.24 * x) + 1.7


def q37p(x):
    return 1.2 * (x + 1.6) * (x + 0.1) * (x - 1.5)


A37 = roots(lambda x: q37(x) - 0.55, -3, -1.6, 0)[0]
B37 = roots(lambda x: q37(x) - 0.55, 1.5, 3, 0)[0]
C37 = 2.25


def solve(f, lo, hi):
    for _ in range(60):
        m = (lo + hi) / 2
        if (f(lo) > 0) == (f(m) > 0):
            lo = m
        else:
            hi = m
    return (lo + hi) / 2


def i10():  # 37번 해설: 평균값 정리
    F = Frame((-2.6, 2.7), (-0.9, 4.1), 90, 90, M)
    F.axes(); O(F, 'lt', 4, 4)
    plot(F, q37, -2.35, 2.32)
    a, c = A37, C37
    k = (q37(c) - q37(a)) / (c - a)
    L = lambda x: q37(a) + k * (x - a)
    F.seg((-2.55, L(-2.55)), (2.55, L(2.55)), 2.0)
    al = [solve(lambda x: q37p(x) - k, -2.0, -1.0), solve(lambda x: q37p(x) - k, -0.9, 0.5), solve(lambda x: q37p(x) - k, 0.6, 2.0)]
    for i, t in enumerate(al):
        F.seg((t - 0.45, q37(t) - 0.45 * k), (t + 0.45, q37(t) + 0.45 * k), 1.5)
        F.dashed((t, 0), (t, q37(t)))
        F.lab((t, 0), '\\alpha_{%d}' % (i + 1), 'ct', 0, 8)
    F.lab((al[0] + 0.45, q37(al[0]) + 0.45 * k), 'l_{1}', 'lc', 4, 4); F.lab((al[1] - 0.2, q37(al[1]) - 0.2 * k), 'l_{2}', 'rb', -4, -4)
    F.lab((al[2] + 0.45, q37(al[2]) + 0.45 * k), 'l_{3}', 'lc', 4, 0)
    F.dashed((a, 0), (a, q37(a))); F.dashed((c, 0), (c, q37(c)))
    F.lab((a, 0), 'a', 'ct', 0, 8); F.lab((c, 0), 'c', 'ct', 0, 8)
    F.lab((2.32, q37(2.32)), 'y=f(x)', 'rc', -12, 0)
    return F.render()


def i11():  # 37번 해설: 롤의 정리
    F = Frame((-2.6, 2.7), (-0.9, 4.1), 90, 90, M)
    F.axes(); O(F, 'lt', 4, 4)
    plot(F, q37, -2.35, 2.32)
    a, b = A37, B37
    F.seg((-2.55, q37(a)), (2.55, q37(a)), 2.0)
    for i, t in enumerate((-1.6, -0.1, 1.5)):
        F.seg((t - 0.4, q37(t)), (t + 0.4, q37(t)), 1.5)
        F.dashed((t, 0), (t, q37(t)))
        F.lab((t, 0), '\\beta_{%d}' % (i + 1), 'ct', 0, 8)
    F.dashed((a, 0), (a, q37(a))); F.dashed((b, 0), (b, q37(b)))
    F.lab((a, 0), 'a', 'ct', 0, 8); F.lab((b, 0), 'b', 'ct', 0, 8)
    F.lab((2.32, q37(2.32)), 'y=f(x)', 'rc', -12, 0)
    return F.render()


def i12():  # 37번 문제
    F = Frame((-2.6, 2.7), (-0.9, 4.1), 90, 90, M)
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, q37, -2.35, 2.32)
    a, b, c = A37, B37, C37
    F.dashed((a, 0), (a, q37(a))); F.dashed((a, q37(a)), (c, q37(a))); F.dashed((c, 0), (c, q37(c)))
    F.lab((a, 0), 'a', 'ct', 0, 8); F.lab((b, 0), 'b', 'ct', 0, 8); F.lab((c, 0), 'c', 'ct', 0, 8)
    F.lab((2.32, q37(2.32)), 'y=f(x)', 'rc', -12, 0)
    return F.render()


def i13():  # 42번 문제: x=1에서 y=1에 접함
    F = Frame((-3.2, 2.3), (-1.0, 4.4), 70, 70, (16, 16, 100, 16))
    f = lambda x: 1 + 0.35 * (x - 1) ** 2 * (x + 2.5)
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, f, -2.95, 2.12); F.seg((-3.1, 1), (2.2, 1), 2.0)
    F.dashed((1, 0), (1, 1))
    F.lab((1, 0), '1', 'ct', 0, 8); F.lab((0, 1), '1', 'rt', -6, 6)
    F.lab((2.2, 1), 'y=1', 'lc', 8, 0); F.lab((2.12, f(2.12)), 'y=f(x)', 'rc', -12, 0)
    return F.render()


def i14():  # 43번 문제 f(x)=(x+1)(x-1)(x-4)+x+2, y=x+2
    f = lambda x: (x + 1) * (x - 1) * (x - 4) + x + 2
    F = Frame((-2.3, 5.4), (-4.0, 8.3), 55, 40, (16, 30, 150, 16))
    F.axes(); O(F, 'lt', 4, 4)
    plot(F, f, -1.42, 4.1); F.seg((-2.2, -0.2), (5.2, 7.2), 2.0)
    for p in [(-1, 1), (1, 3), (4, 6)]:
        fdot(F, p)
    F.dashed((1, 0), (1, 3)); F.dashed((4, 0), (4, 6))
    F.pt((-1, 1), 'A', 'rb', -8, -4); F.pt((1, 3), 'B', 'lb', 8, -2); F.pt((4, 6), 'C', 'rb', -10, -4)
    F.lab((-1, 0), '-1', 'ct', -8, 8); F.lab((1, 0), '1', 'ct', 0, 8); F.lab((4, 0), '4', 'ct', 8, 8); F.lab((0, 2), '2', 'rc', -8, -4)
    F.lab((5.2, 7.2), 'y=x+2', 'lt', 4, 8); F.lab((4.1, f(4.1)), 'y=f(x)', 'lc', 10, 0)
    return F.render()


g48 = lambda x: -0.5 * x * x + 6 * x


def i15():  # 48번 해설: P(5, 35/2)에서 접선이 OB와 평행
    F = Frame((-1.0, 13.0), (-1.5, 20.5), 26, 26, (50, 30, 150, 16))
    P, B = (5, 17.5), (12, 12); H = (11.25, 11.25)
    F.poly([(0, 0), P, B], SKY)
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, g48, 0, 12)
    F.seg((0, 0), B, 2.0); F.seg((0, 0), P, 2.0); F.seg(P, B, 2.0)
    F.seg((-0.9, 11.6), (8.0, 20.5), 2.0)
    F.dashed((0, 18), (6, 18)); F.dashed((12, 0), B)
    F.seg(P, H, 1.5); right_mark(F, H, P, (0, 0), 0.8)
    dim_arc(F, P, H, 'h', -1)
    fdot(F, P); fdot(F, B)
    F.pt(P, 'P', 'rc', -12, 0); F.pt(B, '\\mathrm{B}(12,\\ 12)', 'lc', 10, 0)
    F.lab((12, 0), '12', 'ct', -14, 8); F.lab((0, 18), '18', 'rc', -8, 0)
    F.lab((6.6, 18.2), 'y=-\\dfrac{1}{2}x^{2}+6x', 'lb', 10, -4)
    return F.render()


def i16():  # 48번 문제
    F = Frame((-1.0, 13.0), (-1.5, 20.5), 26, 26, (50, 30, 150, 16))
    P, B = (3, g48(3)), (12, 12)
    F.poly([(0, 0), P, B], PINK)
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, g48, 0, 12)
    F.seg((0, 0), B, 2.0); F.seg((0, 0), P, 2.0); F.seg(P, B, 2.0)
    F.dashed((12, 0), B)
    fdot(F, P); fdot(F, B)
    F.pt(P, 'P', 'rc', -12, -4); F.pt(B, '\\mathrm{B}(12,\\ 12)', 'lc', 10, 0)
    F.lab((12, 0), '12', 'ct', -14, 8)
    F.lab((6.6, 18.2), 'y=-\\dfrac{1}{2}x^{2}+6x', 'lb', 10, -4)
    return F.render()


JOBS = {k: v for k, v in globals().items() if k[0] == 'i' and k[1:].isdigit()}
if __name__ == '__main__':
    run(JOBS, OUT, sys.argv[2:], wide=())
