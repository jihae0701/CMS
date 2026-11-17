# -*- coding: utf-8 -*-
"""미적분Ⅰ M 1. 함수의 극한 — C에 없던 스캔 그림 다시 그리기 (iN = 문서의 imageN).  python3 draw.py 출력폴더 [이름...]"""
import sys, math
sys.path.insert(0, '/home/user/CMS/.claude/skills/math-figure-rules'); sys.path.insert(0, '/tmp/claude-0/-home-user-CMS/7a122d51-a5b1-5def-9637-d43cb9a9b6ef/scratchpad/figw')
from mathfig import Frame, SKY, PINK
from mjcommon import odot, fdot, plot, axes2, O, run, herm
OUT = sys.argv[1]
M = (16, 16, 16, 16)


def i12():  # 13번 해설 y=|x-2|/(x-2)
    F = Frame((-0.9, 4.4), (-1.9, 1.9), 70, 70, M)
    F.axes(); O(F, 'rt', -6, 4)
    F.seg((-0.8, -1), (2, -1), 3.2); F.seg((2, 1), (4.2, 1), 3.2)
    F.dashed((2, -1), (2, 1)); F.dashed((0, 1), (2, 1))
    odot(F, (2, 1)); odot(F, (2, -1))
    F.lab((2, 0), '2', 'lt', 6, 6); F.lab((0, 1), '1', 'rc', -8, 0); F.lab((0, -1), '-1', 'lc', 8, 0)
    F.lab((3.2, 1), 'y=f(x)', 'cb', 0, -10)
    return F.render()


def i14():  # 56번 문제 f(x)=|x|, g(x)
    F = Frame((-1.6, 6.4), (-1.6, 1.8), 70, 70, M)
    axes2(F, 0, -1.6, 1.8, -1.0, 1.8); O(F, 'rt', -6, 4)
    F.seg((-1.45, 1.45), (0, 0), 3.2); F.seg((0, 0), (1.45, 1.45), 3.2)
    F.dashed((-1, 0), (-1, 1)); F.dashed((1, 0), (1, 1)); F.dashed((-1, 1), (1, 1))
    F.lab((-1, 0), '-1', 'ct', 0, 8); F.lab((1, 0), '1', 'ct', 0, 8); F.lab((0, 1), '1', 'rb', -6, -4)
    F.lab((1.2, 1.5), 'y=f(x)', 'lc', 6, 0)
    ox = 4.4
    axes2(F, ox, ox - 1.9, ox + 1.9, -1.6, 1.8); F.pt((ox, 0), 'O', 'rt', -6, 4)
    F.seg((ox - 1.8, -1), (ox, -1), 3.2); F.seg((ox, 1), (ox + 1.8, 1), 3.2)
    odot(F, (ox, 1)); odot(F, (ox, -1)); fdot(F, (ox, 0))
    F.lab((ox, 1), '1', 'rc', -8, 0); F.lab((ox, -1), '-1', 'lc', 8, 0)
    F.lab((ox + 0.9, 1), 'y=g(x)', 'cb', 0, -10)
    return F.render()


def i16():  # 58번 문제
    F = Frame((-1.9, 4.0), (-1.5, 1.9), 70, 70, M)
    F.axes(); O(F, 'rt', -6, 4)
    F.seg((-1.8, 1.8), (0, 0), 3.2); F.seg((0, 0), (1, 1), 3.2); F.seg((1, -1), (2, -1), 3.2); F.seg((2, 1), (3.8, -0.8), 3.2)
    F.dashed((0, 1), (2, 1)); F.dashed((1, 1), (1, -1)); F.dashed((2, 1), (2, -1)); F.dashed((0, -1), (1, -1))
    odot(F, (1, 1)); fdot(F, (2, 1)); fdot(F, (1, -1)); odot(F, (2, -1))
    F.lab((1, 0), '1', 'rt', -4, 6); F.lab((2, 0), '2', 'rt', -4, 6); F.lab((3, 0), '3', 'rt', -2, 6)
    F.lab((0, 1), '1', 'rc', -8, 0); F.lab((0, -1), '-1', 'rc', -8, 0)
    F.lab((2.1, 1.2), 'y=f(x)', 'lb', 4, -4)
    return F.render()


def i17():  # 59번 문제
    F = Frame((-1.6, 3.9), (-0.9, 3.9), 70, 70, M)
    F.axes(); O(F, 'rt', -6, 4)
    F.seg((-1.5, -0.5), (1, 2), 3.2); F.seg((1, 3), (2, 1), 3.2); F.seg((2, 0), (3.7, 3.4), 3.2)
    F.dashed((1, 0), (1, 3)); F.dashed((0, 3), (1, 3)); F.dashed((0, 2), (1, 2)); F.dashed((0, 1), (2, 1)); F.dashed((2, 0), (2, 1))
    fdot(F, (1, 3)); odot(F, (1, 2)); odot(F, (2, 1)); fdot(F, (2, 0))
    F.lab((-1, 0), '-1', 'cb', 0, -8); F.lab((1, 0), '1', 'ct', 0, 8); F.lab((2, 0), '2', 'ct', 0, 10)
    F.lab((0, 1), '1', 'rc', -8, -4); F.lab((0, 2), '2', 'rc', -8, 0); F.lab((0, 3), '3', 'rc', -8, 0)
    F.lab((3.3, 3.5), 'y=f(x)', 'rb', -10, 0)
    return F.render()


def i18():  # 65번 문제 f, g
    F = Frame((-1.6, 6.8), (-1.6, 2.6), 70, 70, M)
    axes2(F, 0, -1.6, 2.6, -1.6, 2.2); O(F, 'rt', -6, 4)
    f1 = herm([(-1.5, -1.8, 1.8), (-1, -1, 1.6), (0, 0.55, 0.9), (1, 1, 0.0)])
    plot(F, f1, -1.5, 1); plot(F, lambda x: -1 + 2.2 * (x - 1) ** 2 * (1 + 0.25 * (x - 1)), 1, 2.45)
    F.dashed((0, 1), (1, 1)); F.dashed((1, 1), (1, -1)); F.dashed((0, -1), (1, -1))
    F.dashed((-1, 0), (-1, -1)); F.dashed((-1, -1), (0, -1))
    odot(F, (1, 1)); fdot(F, (1, -1))
    F.lab((-1, 0), '-1', 'cb', 0, -8); F.lab((1, 0), '1', 'lt', 4, 6); F.lab((2, 0), '2', 'rt', -4, 6)
    F.lab((0, 1), '1', 'rc', -8, 0); F.lab((0, -1), '-1', 'lc', 8, 0)
    F.lab((2.0, 1.9), 'y=f(x)', 'rb', -8, 0)
    ox = 4.2
    axes2(F, ox, ox - 1.6, ox + 2.5, -1.6, 2.6); F.pt((ox, 0), 'O', 'rt', -6, 4)
    g1 = herm([(ox - 1.4, 1.8, -2.4), (ox - 1, 1, -1.6), (ox, -0.5, -1.0), (ox + 1, -1, 0.0)])
    plot(F, g1, ox - 1.4, ox + 1); F.seg((ox + 1, 1), (ox + 2.3, 2.3), 3.2)
    F.dashed((ox, 1), (ox + 1, 1)); F.dashed((ox + 1, 1), (ox + 1, -1)); F.dashed((ox, -1), (ox + 1, -1))
    F.dashed((ox + 2, 0), (ox + 2, 2)); F.dashed((ox, 2), (ox + 2, 2))
    F.dashed((ox - 1, 0), (ox - 1, 1)); F.dashed((ox - 1, 1), (ox, 1))
    fdot(F, (ox + 1, 1)); odot(F, (ox + 1, -1))
    F.lab((ox - 1, 0), '-1', 'ct', 0, 8); F.lab((ox + 1, 0), '1', 'lt', 4, 6); F.lab((ox + 2, 0), '2', 'ct', 0, 8)
    F.lab((ox, 1), '1', 'rc', -8, 0); F.lab((ox, 2), '2', 'rc', -8, 0); F.lab((ox, -1), '-1', 'rc', -8, 0)
    F.lab((ox + 1.5, 2.3), 'y=g(x)', 'rb', -10, 0)
    return F.render()


def i19():  # 78번 문제 y=x^2, P(t,t^2), Q, R (t=1.2 개형)
    t = 1.2
    P = (t, t * t); R = (0, 2.6); Q = (2.7, 0)
    F = Frame((-0.6, 3.3), (-0.5, 3.4), 80, 80, M)
    F.axes(); O(F, 'rt', -6, 4)
    F.poly([(0, 0), R, P], SKY); F.poly([(0, 0), P, Q], PINK)
    plot(F, lambda x: x * x, -0.25, 1.78)
    F.seg(R, P); F.seg(P, Q); F.seg((0, 0), P)
    F.pt(R, 'R', 'rc', -8, 0); F.pt(Q, 'Q', 'ct', 0, 8); F.pt(P, 'P', 'cb', -2, -10)
    F.lab((1.75, 3.06), 'y=x^2', 'lc', 6, 0)
    return F.render()


JOBS = {k: v for k, v in globals().items() if k[0] == 'i' and k[1:].isdigit()}
if __name__ == '__main__':
    run(JOBS, OUT, sys.argv[2:], wide=('i14', 'i18'))
