# -*- coding: utf-8 -*-
"""미적분Ⅰ 7. 부정적분 — 스캔 그림 다시 그리기.  python3 draw.py 출력폴더 [이름...]"""
import sys, math
sys.path.insert(0, '/home/user/CMS/.claude/skills/math-figure-rules'); sys.path.insert(0, '..')
from mathfig import Frame, DASH
from mjcommon import plot, O, run, table, UP, DN
OUT = sys.argv[1]
M = (16, 16, 16, 16)
MX, MN = '\\text{극대}', '\\text{극소}'


def i4():   # 30번 해설
    return table([['x', '\\cdots', '0', '\\cdots', '2', '\\cdots'], ["f'(x)", '+', '0', '-', '0', '+'], ['f(x)', UP, MX, DN, MN, UP]], [80] + [78] * 5)


def i6():   # 31번 해설
    return table([['x', '\\cdots', '0', '\\cdots', '4', '\\cdots'], ["f'(x)", '+', '0', '-', '0', '+'], ['f(x)', UP, MX, DN, MN, UP]], [80] + [78] * 5)


def para(z0, z1, k, xr, yr, sx, sy, lab_end, Oanc=('rt', -6, 4)):
    f = lambda x: k * (x - z0) * (x - z1)
    F = Frame(xr, yr, sx, sy, M)
    F.axes(); O(F, *Oanc)
    a, b = lab_end
    plot(F, f, a, b)
    return F, f, b


def i5():   # 30번 문제 f'(x)=x(x-2) 꼴
    F, f, b = para(0, 2, 1.2, (-1.0, 3.2), (-1.6, 2.6), 90, 70, (-0.55, 2.6), ('rt', -6, 4))
    F.lab((2, 0), '2', 'lt', 6, 6); F.lab((b, f(b)), "y=f'(x)", 'rc', -12, 0)
    return F.render()


def i7():   # 33번 문제
    F, f, b = para(0, 2, 1.2, (-1.0, 3.2), (-1.6, 2.6), 90, 70, (-0.55, 2.6), ('rt', -6, 4))
    F.lab((2, 0), '2', 'lt', 6, 6); F.lab((b, f(b)), "y=f'(x)", 'rc', -12, 0)
    return F.render()


def i8():   # 34번 문제 f'(x)=-(x-1)(x-3) 꼴
    f = lambda x: -1.2 * (x - 1) * (x - 3)
    F = Frame((-0.9, 4.4), (-2.6, 1.9), 80, 70, M)
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, f, 0.3, 3.7)
    F.lab((1, 0), '1', 'rt', -4, 6); F.lab((3, 0), '3', 'lt', 4, 6); F.lab((2.6, f(2.6)), "y=f'(x)", 'lb', 14, -6)
    return F.render()


def i9():   # 41번 문제 f'(x)=x(x-3) 꼴
    f = lambda x: 0.8 * x * (x - 3)
    F = Frame((-1.0, 4.4), (-2.6, 4.2), 80, 70, M)
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, f, -1.0, 3.95)
    F.lab((3, 0), '3', 'lt', 6, 6); F.lab((3.95, f(3.95)), "y=f'(x)", 'rc', -12, 0)
    return F.render()


def i10():  # 43번 문제 f'(x)=|x|
    F = Frame((-3.0, 3.6), (-1.2, 3.6), 70, 70, M)
    F.axes(); O(F, 'rt', -6, 4)
    F.polyline([(-2.8, 2.8), (0, 0), (2.8, 2.8)])
    F.dashed((-2, 0), (-2, 2)); F.dashed((2, 0), (2, 2)); F.dashed((-2, 2), (2, 2))
    F.lab((-2, 0), '-2', 'ct', 0, 6); F.lab((2, 0), '2', 'ct', 0, 6); F.lab((0, 2), '2', 'rb', -6, -4)
    F.lab((2.8, 2.8), "y=f'(x)", 'rc', -12, -14)
    return F.render()


JOBS = {k: v for k, v in globals().items() if k[0] == 'i' and k[1:].isdigit()}
if __name__ == '__main__':
    run(JOBS, OUT, sys.argv[2:], natural=('i4', 'i6'))
