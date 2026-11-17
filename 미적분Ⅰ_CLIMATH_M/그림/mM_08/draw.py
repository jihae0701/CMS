# -*- coding: utf-8 -*-
"""미적분Ⅰ M 8. 정적분 — C에 없던 스캔 그림 다시 그리기 (iN = 문서의 imageN).  python3 draw.py 출력폴더 [이름...]"""
import sys, math
sys.path.insert(0, '/home/user/CMS/.claude/skills/math-figure-rules'); sys.path.insert(0, '/tmp/claude-0/-home-user-CMS/7a122d51-a5b1-5def-9637-d43cb9a9b6ef/scratchpad/figw')
from mathfig import Frame, SKY, PINK
from mjcommon import odot, fdot, plot, axes2, O, run, herm, table, UP, DN
OUT = sys.argv[1]
M = (16, 16, 16, 16)

MN = '\\text{극소}'


def i12():  # 58번 문제 f(x)=-x(x-4) (0≤x<4), x-4 (4≤x≤8)
    F = Frame((-0.7, 9.0), (-0.8, 4.7), 50, 50, M)
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, lambda x: -x * (x - 4), 0, 4); F.seg((4, 0), (8, 4), 3.2)
    F.dashed((0, 4), (8, 4)); F.dashed((8, 0), (8, 4))
    F.lab((4, 0), '4', 'ct', 0, 8); F.lab((8, 0), '8', 'ct', 0, 8); F.lab((0, 4), '4', 'rc', -8, 0)
    F.lab((6.6, 2.6), 'y=f(x)', 'rb', -6, -6)
    return F.render()


def i11():  # 58번 해설 증감표 (g'(a) 부호 바로잡음)
    return table([['a', '(0)', '\\cdots', '3', '\\cdots', '(4)'], ["g'(a)", '', '-', '0', '+', ''],
                  ['g(a)', '\\dfrac{32}{3}', DN, MN, UP, '8']], [80] + [78] * 5, rh=62)


def i14():  # 59번 해설 f(x)=2x^3-3x^2-36x+3
    f = lambda x: 2 * x ** 3 - 3 * x ** 2 - 36 * x + 3
    s = 0.03
    g = lambda x: f(x) * s
    F = Frame((-4.4, 6.3), (-2.7, 2.1), 50, 50, M)
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, g, -4.1, 5.62)
    F.dashed((-2, 0), (-2, g(-2))); F.dashed((-2, g(-2)), (0, g(-2))); F.dashed((3, 0), (3, g(3))); F.dashed((0, g(3)), (3, g(3)))
    F.lab((-2, 0), '-2', 'ct', -8, 8); F.lab((3, 0), '3', 'cb', 6, -6)
    F.lab((0, g(-2)), '47', 'lc', 8, 0); F.lab((0, g(3)), '-78', 'rc', -8, 0); F.lab((0, g(0)), '3', 'lb', 6, -4)
    F.lab((5.6, g(5.6)), 'y=f(x)', 'rc', -12, 4)
    return F.render()


JOBS = {k: v for k, v in globals().items() if k[0] == 'i' and k[1:].isdigit()}
if __name__ == '__main__':
    run(JOBS, OUT, sys.argv[2:], natural=('i11',))
