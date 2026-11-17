# -*- coding: utf-8 -*-
"""미적분Ⅰ M 4. 도함수의 활용(1) — C에 없던 스캔 그림 다시 그리기 (iN = 문서의 imageN).  python3 draw.py 출력폴더 [이름...]"""
import sys, math
sys.path.insert(0, '/home/user/CMS/.claude/skills/math-figure-rules'); sys.path.insert(0, '/tmp/claude-0/-home-user-CMS/7a122d51-a5b1-5def-9637-d43cb9a9b6ef/scratchpad/figw')
from mathfig import Frame, SKY, PINK
from mjcommon import odot, fdot, plot, axes2, O, run, herm
OUT = sys.argv[1]
M = (16, 16, 16, 16)

from mathfig import dot


def cubes(F, ab=False):
    plot(F, lambda x: x ** 3 + 2, -1.75, 1.32); plot(F, lambda x: x ** 3 - 2, -1.08, 1.75)
    F.seg((-1.45, -4.35), (1.45, 4.35))
    F.lab((0, 2), '2', 'rb', -6, -4); F.lab((0, -2), '-2', 'lt', 6, 4)
    F.lab((1.32, 1.32 ** 3 + 2), 'y=x^3+2', 'lc', 8, 0); F.lab((1.75, 1.75 ** 3 - 2), 'y=x^3-2', 'lc', 8, 0)
    if ab:
        dot(F, (1, 3)); dot(F, (-1, -3)); F.pt((1, 3), 'A', 'rb', -6, -4); F.pt((-1, -3), 'B', 'lt', 6, 4)


def i6():   # 12번 문제
    F = Frame((-2.0, 3.9), (-4.5, 4.9), 50, 40, M)
    F.axes(); O(F, 'rt', -6, 4); cubes(F)
    return F.render()


def i5():   # 12번 해설
    F = Frame((-2.0, 3.9), (-4.5, 4.9), 50, 40, M)
    F.axes(); O(F, 'rt', -6, 4); cubes(F, True)
    return F.render()


def i7():   # 13번 문제 y=x^4, 원 C 중심 (0, 5/4)
    r = math.sqrt(17) / 4
    F = Frame((-1.5, 1.9), (-0.4, 2.6), 90, 90, M)
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, lambda x: x ** 4, -1.27, 1.27)
    F.svg.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="#000" stroke-width="2"/>' % (F.P(0, 1.25) + (r * F.sx,)))
    dot(F, (0, 1.25)); dot(F, (1, 1))
    F.pt((0, 1.25), 'C', 'rc', -8, 0); F.lab((0.75, 2.05), 'C', 'lb', 4, 0); F.lab((1, 1), '(1,~1)', 'lc', 10, 4)
    F.lab((1.27, 1.27 ** 4), 'y=x^4', 'lc', 8, 0)
    return F.render()


def i13():  # 42번 해설 y=x^2-4x+6, P(3,3), 접선 y=2x-3 과 직선 y=2x-5
    F = Frame((-0.6, 6.9), (-1.3, 6.4), 60, 60, M)
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, lambda x: x * x - 4 * x + 6, 0, 4.45)
    F.seg((0.85, -1.3), (4.6, 6.2), 2.0); F.seg((1.85, -1.3), (5.0, 5.0), 3.2)
    dot(F, (3, 3)); F.pt((3, 3), 'P', 'rb', -8, -2)
    F.lab((0.9, 5.6), 'y=x^2-4x+6', 'lc', 0, 0); F.lab((5.0, 5.0), 'y=2x-5', 'lc', 8, 0)
    return F.render()


def i18():  # 53번 문제 f(x)=x^3-5/2x^2+ax+2 (a=-2/3), 접선 l, m
    a = -2 / 3
    f = lambda x: x ** 3 - 2.5 * x * x + a * x + 2
    F = Frame((-1.4, 3.9), (-2.4, 3.2), 70, 70, M)
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, f, -0.85, 2.95)
    F.seg((-1.2, a * -1.2 + 2), (3.8, a * 3.8 + 2), 2.0); F.seg((1.0, (a + 2) * 1.0 - 4), (3.7, (a + 2) * 3.7 - 4), 2.0)
    dot(F, (0, 2)); dot(F, (2, f(2)))
    F.pt((0, 2), 'A', 'lb', 6, -4); F.pt((2, f(2)), 'B', 'rt', -6, 6)
    F.lab((3.8, a * 3.8 + 2), 'l', 'lc', 6, 0); F.lab((3.7, (a + 2) * 3.7 - 4), 'm', 'lc', 6, 0)
    F.lab((2.95, f(2.95)), 'y=f(x)', 'lc', 8, 0)
    return F.render()


def i19():  # 57번 해설 y=4x^2+5, y=|2a||x-1|
    F = Frame((-2.0, 6.6), (-0.6, 11.5), 55, 30, M)
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, lambda x: 4 * x * x + 5, -1.2, 1.2)
    F.seg((-1.6, 10.4), (1, 0), 3.2); F.seg((1, 0), (3.0, 8.0), 3.2)
    F.seg((-1.9, 4.06), (1, 0), 2.0); F.seg((1, 0), (3.3, 3.22), 2.0)
    F.lab((1, 0), '1', 'ct', 0, 8)
    F.lab((1.2, 4 * 1.2 ** 2 + 5), 'y=4x^2+5', 'lc', 8, 0); F.lab((3.0, 8.0), 'y=|2a||x-1|', 'lc', 8, 0)
    return F.render()


def i20():  # 59번 해설 y=g(x), 접선과 평행한 직선
    g = lambda x: 1.25 * x * x + 9 * x + 12 if x < -2 else 3 - x * x
    F = Frame((-5.0, 3.9), (-5.2, 4.2), 50, 50, M)
    F.axes(); O(F, 'lb', 6, -4)
    plot(F, g, -4.9, 1.95, n=300)
    F.seg((-4.6, -5.2), (0.1, 4.2), 2.0); F.seg((-3.7, -5.2), (1.0, 4.2), 2.0)
    c = -2.8
    F.dashed((-4, 0), (-4, -4)); F.dashed((c, 0), (c, g(c))); F.dashed((-1, 0), (-1, 2))
    F.lab((-4, 0), '-4', 'cb', -4, -8); F.lab((-2, 0), '-2', 'cb', 6, -8); F.lab((c, 0), 'c', 'ct', -6, 8); F.lab((-1, 0), '-1', 'ct', 8, 8)
    F.lab((1.3, g(1.3)), 'y=g(x)', 'lc', 10, 0)
    return F.render()


JOBS = {k: v for k, v in globals().items() if k[0] == 'i' and k[1:].isdigit()}
if __name__ == '__main__':
    run(JOBS, OUT, sys.argv[2:])
