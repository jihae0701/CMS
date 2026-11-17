# -*- coding: utf-8 -*-
"""미적분Ⅰ M 7. 부정적분 — C에 없던 스캔 그림 다시 그리기 (iN = 문서의 imageN).  python3 draw.py 출력폴더 [이름...]"""
import sys, math
sys.path.insert(0, '/home/user/CMS/.claude/skills/math-figure-rules'); sys.path.insert(0, '/tmp/claude-0/-home-user-CMS/7a122d51-a5b1-5def-9637-d43cb9a9b6ef/scratchpad/figw')
from mathfig import Frame, SKY, PINK
from mjcommon import odot, fdot, plot, axes2, O, run, herm, table, UP, DN
OUT = sys.argv[1]
M = (16, 16, 16, 16)



def i6():   # 18번 문제 y=x(x-α)^2 (α=3 개형)
    f = lambda x: 0.32 * x * (x - 3) ** 2
    F = Frame((-0.7, 4.6), (-0.9, 2.6), 70, 70, M)
    F.axes(); O(F, 'lt', 4, 4)
    plot(F, f, -0.45, 4.38)
    F.lab((3, 0), '\\alpha', 'ct', 0, 8)
    F.lab((4.0, f(4.0)), 'y=f(x)', 'rc', -12, -4)
    return F.render()


def i12():  # 38번 문제 y=f'(x)=a(x+2)(x-2)(x-3)
    f = lambda x: 0.16 * (x + 2) * (x - 2) * (x - 3)
    F = Frame((-2.9, 4.4), (-1.9, 2.4), 60, 60, M)
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, f, -2.55, 3.95)
    F.lab((-2, 0), '-2', 'rb', -6, -4); F.lab((2, 0), '2', 'rt', -4, 6); F.lab((3, 0), '3', 'lt', 4, 6)
    F.lab((3.9, f(3.9)), "y=f'(x)", 'rc', -12, 0)
    return F.render()


def i10():  # 38번 해설 증감표
    return table([['x', '\\cdots', '-2', '\\cdots', '2', '\\cdots', '3', '\\cdots'], ["f'(x)", '-', '0', '+', '0', '-', '0', '+'],
                  ['f(x)', DN, '-64', UP, '64', DN, '61', UP]], [80] + [70] * 7)


def i11():  # 38번 해설 y=f(x), y=|f(x)|  f=x^4-4x^3-8x^2+48x+16
    f = lambda x: x ** 4 - 4 * x ** 3 - 8 * x ** 2 + 48 * x + 16
    sy = 0.035
    g = lambda x: f(x) * sy
    ox = 8.6
    F = Frame((-3.7, ox + 4.6), (-2.5, 3.2), 55, 55, M)
    axes2(F, 0, -3.7, 4.5, -2.5, 3.2); O(F, 'lt', 4, 4)
    plot(F, g, -3.42, 4.0)
    F.dashed((-2, 0), (-2, g(-2))); F.dashed((-2, g(-2)), (0, g(-2)))
    F.dashed((2, 0), (2, g(2))); F.dashed((0, g(2)), (2, g(2))); F.dashed((3, 0), (3, g(3))); F.dashed((0, g(3)), (3, g(3)))
    F.lab((-2, 0), '-2', 'cb', 0, -8); F.lab((2, 0), '2', 'ct', -4, 8); F.lab((3, 0), '3', 'ct', 4, 8)
    F.lab((0, g(-2)), '-64', 'lc', 8, 0); F.lab((0, g(0)), '16', 'rb', -6, -2)
    F.lab((0, g(2)), '64', 'rb', -6, 0); F.lab((0, g(3)), '61', 'rt', -6, 0)
    F.lab((4.0, g(4.0)), 'y=f(x)', 'rc', -12, 6)
    axes2(F, ox, ox - 3.7, ox + 4.5, -0.7, 3.2); F.pt((ox, 0), 'O', 'rt', -6, 4)
    h = lambda x: abs(g(x - ox))
    plot(F, h, ox - 3.42, ox + 4.0, n=500)
    F.dashed((ox - 2, 0), (ox - 2, h(ox - 2))); F.dashed((ox + 2, 0), (ox + 2, h(ox + 2))); F.dashed((ox + 3, 0), (ox + 3, h(ox + 3)))
    F.dashed((ox - 2, h(ox - 2)), (ox + 2, h(ox + 2))); F.dashed((ox, h(ox + 3)), (ox + 3, h(ox + 3)))
    F.lab((ox - 2, 0), '-2', 'ct', 0, 8); F.lab((ox + 2, 0), '2', 'ct', -4, 8); F.lab((ox + 3, 0), '3', 'ct', 4, 8)
    F.lab((ox, h(ox + 2)), '64', 'rb', -6, 0); F.lab((ox, h(ox + 3)), '61', 'rt', -6, 0)
    F.lab((ox + 4.0, h(ox + 4.0)), 'y=|f(x)|', 'rc', -12, 6)
    return F.render()


JOBS = {k: v for k, v in globals().items() if k[0] == 'i' and k[1:].isdigit()}
if __name__ == '__main__':
    run(JOBS, OUT, sys.argv[2:], wide=('i11',), natural=('i10',))
