# -*- coding: utf-8 -*-
"""미적분Ⅰ 9. 정적분으로 정의된 함수 — 스캔 그림 다시 그리기.  python3 draw.py 출력폴더 [이름...]"""
import sys, math
sys.path.insert(0, '/home/user/CMS/.claude/skills/math-figure-rules'); sys.path.insert(0, '..')
from mathfig import Frame
from mjcommon import plot, O, run, odot, fdot
OUT = sys.argv[1]
M = (16, 16, 16, 16)


def i5():
    F = Frame((-2.6, 1.9), (-1.6, 3.6), 90, 90, M)
    F.axes(); O(F, 'lt', 4, 6)
    plot(F, lambda x: 2 - 2 * (x + 2) ** 2, -2, -1)
    plot(F, lambda x: -math.sqrt(max(0, -x)), -1, 0)
    F.seg((0, 1), (1, 3), 3.2)
    F.dashed((-2, 0), (-2, 2)); F.dashed((-2, 2), (1, 2)); F.dashed((-1, -1), (-1, 1)); F.dashed((-1, 1), (0, 1))
    F.dashed((0, 3), (1, 3)); F.dashed((1, 0), (1, 3)); F.dashed((-1, -1), (0, -1))
    for p in [(-2, 2), (-1, 1), (0, 1), (1, 2)]:
        fdot(F, p)
    for p in [(-1, 0), (-1, -1), (0, 0), (1, 3)]:
        odot(F, p)
    F.lab((-2, 0), '-2', 'ct', 0, 6); F.lab((-1, 0), '-1', 'ct', -8, 6); F.lab((1, 0), '1', 'ct', 0, 6)
    F.lab((0, 1), '1', 'rb', -6, -4); F.lab((0, 2), '2', 'rb', -6, -4); F.lab((0, 3), '3', 'rc', -8, 0); F.lab((0, -1), '-1', 'lc', 8, 0)
    F.lab((1, 3), 'y=f(x)', 'cb', 0, -10)
    return F.render()


def i6():   # 34번 문제 f(x)=(x-3)(x-7) 꼴
    f = lambda x: 0.25 * (x - 3) * (x - 7)
    F = Frame((-1.4, 10.6), (-1.6, 6.6), 45, 45, M)
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, f, -0.25, 9.6)
    F.lab((3, 0), '3', 'rt', -4, 6); F.lab((7, 0), '7', 'lt', 4, 6)
    F.lab((9.6, f(9.6)), 'y=f(x)', 'rc', -12, 0)
    return F.render()


JOBS = {k: v for k, v in globals().items() if k[0] == 'i' and k[1:].isdigit()}
if __name__ == '__main__':
    run(JOBS, OUT, sys.argv[2:])
