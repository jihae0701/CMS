# -*- coding: utf-8 -*-
"""미적분Ⅰ M 3. 미분계수와 도함수 — C에 없던 스캔 그림 다시 그리기 (iN = 문서의 imageN).  python3 draw.py 출력폴더 [이름...]"""
import sys, math
sys.path.insert(0, '/home/user/CMS/.claude/skills/math-figure-rules'); sys.path.insert(0, '/tmp/claude-0/-home-user-CMS/7a122d51-a5b1-5def-9637-d43cb9a9b6ef/scratchpad/figw')
from mathfig import Frame, SKY, PINK
from mjcommon import odot, fdot, plot, axes2, O, run, herm
OUT = sys.argv[1]
M = (16, 16, 16, 16)


def i8():   # 46번 문제 f(x)=x (x<2), 2x-6 (x≥2) / g(x)=|2x-4|
    F = Frame((-1.0, 9.9), (-2.6, 4.6), 55, 55, M)
    axes2(F, 0, -1.0, 3.9, -2.6, 2.9); O(F, 'rt', -6, 4)
    F.seg((-0.8, -0.8), (2, 2), 3.2); F.seg((2, -2), (3.4, 0.8), 3.2)
    F.dashed((0, 2), (2, 2)); F.dashed((2, 2), (2, -2)); F.dashed((0, -2), (2, -2))
    odot(F, (2, 2)); fdot(F, (2, -2))
    F.lab((2, 0), '2', 'lt', 4, 6); F.lab((3, 0), '3', 'rb', -2, -4); F.lab((0, 2), '2', 'rc', -8, 0); F.lab((0, -2), '-2', 'rc', -8, 0)
    F.lab((3.1, 2.5), 'y=f(x)', 'rb', 0, 0)
    ox = 5.0
    axes2(F, ox, ox - 0.8, ox + 4.9, -0.8, 4.6); F.pt((ox, 0), 'O', 'rt', -6, 4)
    F.seg((ox - 0.15, 4.3), (ox + 2, 0), 3.2); F.seg((ox + 2, 0), (ox + 4.15, 4.3), 3.2)
    F.dashed((ox, 4), (ox + 4, 4)); F.dashed((ox + 4, 0), (ox + 4, 4))
    F.lab((ox + 2, 0), '2', 'ct', 0, 8); F.lab((ox + 4, 0), '4', 'ct', 0, 8); F.lab((ox, 4), '4', 'rc', -8, 0)
    F.lab((ox + 3.2, 4.4), 'y=g(x)', 'rb', 0, 0)
    return F.render()


def i9():   # 49번 문제
    F = Frame((-1.3, 6.9), (-1.9, 2.6), 60, 60, M)
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, lambda x: 2 - 2 * x * x, -1.2, 1)
    F.polyline([(1, 0), (2, 1), (3, -1), (5, -1), (6.6, 1.6)])
    F.dashed((1, 0), (1, 1)); F.dashed((0, 1), (4, 1)); F.dashed((2, 0), (2, 1)); F.dashed((3, 0), (3, -1)); F.dashed((0, -1), (3, -1))
    F.dashed((4, 1), (4, -1)); F.dashed((5, 0), (5, -1))
    odot(F, (1, 0)); fdot(F, (1, 1)); odot(F, (4, -1)); fdot(F, (4, 1))
    for x in (1, 2, 4):
        F.lab((x, 0), str(x), 'ct', 0 if x != 1 else 8, 8)
    F.lab((3, 0), '3', 'cb', 6, -6); F.lab((5, 0), '5', 'cb', -6, -6); F.lab((6, 0), '6', 'lt', 4, 6); F.lab((-1, 0), '-1', 'lb', 4, -4)
    F.lab((0, 2), '2', 'lb', 6, -2); F.lab((0, 1), '1', 'rc', -8, 0); F.lab((0, -1), '-1', 'rc', -8, 0)
    F.lab((6.0, 2.0), 'y=f(x)', 'rb', 0, 0)
    return F.render()


def i10():  # 61번 해설 g(t)
    F = Frame((-0.8, 4.6), (-0.8, 2.9), 70, 70, M)
    F.axes('t'); O(F, 'rt', -6, 4)
    F.seg((-0.7, 2), (4.4, 2), 3.2)
    F.dashed((0, 1), (3, 1)); F.dashed((3, 0), (3, 2))
    odot(F, (0, 2)); odot(F, (3, 2)); fdot(F, (0, 1)); fdot(F, (3, 1))
    F.lab((3, 0), '3', 'ct', 0, 8); F.lab((0, 2), '2', 'rb', -8, -4); F.lab((0, 1), '1', 'rc', -8, 0)
    F.lab((3.6, 2), 'y=g(t)', 'cb', 0, -10)
    return F.render()


JOBS = {k: v for k, v in globals().items() if k[0] == 'i' and k[1:].isdigit()}
if __name__ == '__main__':
    run(JOBS, OUT, sys.argv[2:], wide=('i8',))
