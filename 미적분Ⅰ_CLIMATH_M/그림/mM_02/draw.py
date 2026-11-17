# -*- coding: utf-8 -*-
"""미적분Ⅰ M 2. 함수의 연속 — C에 없던 스캔 그림 다시 그리기 (iN = 문서의 imageN).  python3 draw.py 출력폴더 [이름...]"""
import sys, math
sys.path.insert(0, '/home/user/CMS/.claude/skills/math-figure-rules'); sys.path.insert(0, '/tmp/claude-0/-home-user-CMS/7a122d51-a5b1-5def-9637-d43cb9a9b6ef/scratchpad/figw')
from mathfig import Frame, SKY, PINK
from mjcommon import odot, fdot, plot, axes2, O, run, herm
OUT = sys.argv[1]
M = (16, 16, 16, 16)

from mathfig import DASH, dot, right_mark


def i8():   # 4번 문제
    F = Frame((-1.6, 3.0), (-0.8, 2.7), 70, 70, M)
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, lambda x: x * x, -1.45, 0); F.seg((0, 1), (1, 2), 3.2); F.seg((1, 0), (2.8, 1.8), 3.2)
    F.dashed((0, 2), (1, 2)); F.dashed((1, 0), (1, 2)); F.dashed((0, 1), (1, 1))
    odot(F, (0, 0)); fdot(F, (0, 1)); odot(F, (1, 2)); fdot(F, (1, 1)); odot(F, (1, 0))
    F.lab((1, 0), '1', 'ct', 0, 10); F.lab((0, 1), '1', 'rc', -8, 0); F.lab((0, 2), '2', 'rc', -8, 0)
    F.lab((1.0, 2.0), 'y=f(x)', 'lb', 4, -10)
    return F.render()


def i9():   # 5번 문제 f, g
    F = Frame((-1.6, 8.9), (-0.8, 2.6), 60, 60, M)
    axes2(F, 0, -1.6, 2.7, -0.8, 2.6); O(F, 'rt', -6, 4)
    F.seg((-1.4, 1.4), (0, 0), 3.2); F.seg((0, 1), (1, 2), 3.2); F.seg((1, 1), (2.3, -0.3), 3.2)
    F.dashed((0, 2), (1, 2)); F.dashed((1, 0), (1, 2)); F.dashed((0, 1), (1, 1))
    odot(F, (0, 0)); fdot(F, (0, 1)); odot(F, (1, 2)); fdot(F, (1, 1))
    F.lab((1, 0), '1', 'ct', 0, 8); F.lab((0, 1), '1', 'rc', -8, 0); F.lab((0, 2), '2', 'rc', -8, 0)
    F.lab((1.0, 2.0), 'y=f(x)', 'lb', 4, -8)
    ox = 6.1
    axes2(F, ox, ox - 3.0, ox + 2.6, -0.8, 2.6); F.pt((ox, 0), 'O', 'rt', -6, 4)
    plot(F, lambda x: 2 - 0.7 * (x - ox + 1.2) ** 2, ox - 2.9, ox); F.seg((ox, 0), (ox + 1, 0), 3.2); F.seg((ox + 1, 1), (ox + 2.3, 2.3), 3.2)
    F.dashed((ox, 1), (ox + 1, 1)); F.dashed((ox + 1, 0), (ox + 1, 1))
    odot(F, (ox, 1)); fdot(F, (ox, 0)); odot(F, (ox + 1, 0)); fdot(F, (ox + 1, 1))
    F.lab((ox + 1, 0), '1', 'ct', 0, 8); F.lab((ox, 1), '1', 'lb', 6, -4)
    F.lab((ox + 2.3, 2.3), 'y=g(x)', 'rc', -12, 0)
    return F.render()


def i12():  # 17번 문제
    F = Frame((-1.8, 3.0), (-2.6, 2.6), 60, 60, M)
    F.axes(); O(F, 'rt', -6, 4)
    F.seg((-1.6, 2.6), (0, 1), 3.2); F.seg((0, -2), (2.8, 0.8), 3.2)
    odot(F, (0, 1)); fdot(F, (0, -2))
    F.lab((0, 1), '1', 'lc', 8, 0); F.lab((0, -2), '-2', 'rc', -8, 0)
    F.lab((2.8, 0.8), 'y=f(x)', 'rb', -14, -6)
    return F.render()


def i19():  # 37번 문제
    F = Frame((-2.6, 4.0), (-1.9, 2.6), 60, 60, M)
    F.axes(); O(F, 'rb', -6, -4)
    F.seg((-2.5, -1.5), (0, 1), 3.2)
    plot(F, herm([(0, -1, 2.2), (1, 0, 0.0), (2, -1, 0.0), (3, 0, 2.6), (3.7, 2.3, 4.0)]), 0, 3.7)
    F.dashed((-2, 0), (-2, -1)); F.dashed((-2, -1), (2, -1)); F.dashed((2, 0), (2, -1))
    fdot(F, (0, 1)); odot(F, (0, -1))
    F.lab((-2, 0), '-2', 'cb', 0, -8); F.lab((-1, 0), '-1', 'cb', -2, -8); F.lab((1, 0), '1', 'ct', 0, 8); F.lab((2, 0), '2', 'cb', 0, -8); F.lab((3, 0), '3', 'lt', 4, 6)
    F.lab((0, 1), '1', 'lc', 8, 0); F.lab((0, -1), '-1', 'rt', -6, 4)
    F.lab((3.7, 2.3), 'y=f(x)', 'rc', -12, 0)
    return F.render()


def i20():  # 38번 보기 ㄱ, ㄴ, ㄷ
    F = Frame((-1.6, 13.6), (-1.6, 2.1), 55, 55, M)
    for i, o in enumerate((0, 5.2, 10.4)):
        axes2(F, o, o - 1.5, o + 3.0, -1.4, 2.0); F.pt((o, 0), 'O', 'rt', -6, 4)
        F.lab((o - 1.5, 2.0), 'ㄱㄴㄷ'[i] + '.', 'lt', 0, 0)
    F.seg((0, 1), (2.8, 1), 3.2); F.seg((-1.4, -1), (0, -1), 3.2); odot(F, (0, 1)); fdot(F, (0, -1))
    F.lab((0, 1), '1', 'rc', -8, 0); F.lab((0, -1), '-1', 'lc', 8, 0); F.lab((1.6, 1), 'y=f(x)', 'cb', 0, -10)
    o = 5.2
    F.seg((o - 1.3, 2.0), (o, 1), 3.2); F.seg((o, 1), (o + 2.8, -0.4), 3.2); odot(F, (o, 1)); fdot(F, (o, -1))
    F.lab((o, 1), '1', 'lb', 6, -4); F.lab((o, -1), '-1', 'lc', 8, 0); F.lab((o + 2, 0), '2', 'cb', 0, -8); F.lab((o + 0.9, 1.6), 'y=f(x)', 'lc', 0, 0)
    o = 10.4
    plot(F, lambda x: 1 / (1 - (x - o)), o - 1.5, o + 0.42); plot(F, lambda x: 1 / ((x - o) - 1), o + 1.58, o + 2.9)
    F.dashed((o + 1, -1.4), (o + 1, 2.0))
    F.lab((o, 1), '1', 'rb', -6, -4); F.lab((o + 1, 0), '1', 'lt', 4, 6); F.lab((o + 1.6, 1.8), 'y=f(x)', 'lc', 0, 0)
    return F.render()


def i21():  # 40번 문제
    F = Frame((-1.9, 3.4), (-1.3, 2.4), 70, 70, M)
    F.axes(); O(F, 'rt', -6, 4)
    F.seg((-1.8, -0.8), (0, 1), 3.2); F.seg((0, 1), (1, 0), 3.2); F.seg((1, 0), (3.2, 2.2), 3.2)
    F.dashed((0, 1), (2, 1)); F.dashed((1, 0), (1, 1)); F.dashed((2, 0), (2, 1))
    odot(F, (1, 0)); fdot(F, (1, 1))
    F.lab((-1, 0), '-1', 'ct', 4, 8); F.lab((1, 0), '1', 'ct', 0, 10); F.lab((2, 0), '2', 'ct', 0, 8); F.lab((0, 1), '1', 'rb', -6, -4)
    F.lab((3.2, 2.2), 'y=f(x)', 'rc', -12, 0)
    return F.render()


def i22():  # 41번 해설 y=g(x), y=h(x)
    F = Frame((-1.9, 3.3), (-0.9, 3.4), 70, 70, M)
    F.axes(); O(F, 'rt', -6, 4)
    F.seg((-1.8, 1.8), (0, 0), 3.2); F.seg((0, 1), (1.95, 2.95), 3.2); odot(F, (0, 1)); fdot(F, (0, 0))
    plot(F, lambda x: x * x, -1.75, 1.75)
    for a in (0.4, -0.5):
        plot(F, lambda x, a=a: x * x + a, -1.65, 1.65, wd=2.0, dash=DASH)
    F.lab((0, 1), '1', 'rc', -8, 0)
    F.lab((1.75, 3.06), 'y=h(x)', 'lc', 6, 0); F.lab((1.95, 2.95), 'y=g(x)', 'lt', 6, 8)
    return F.render()


def i23():  # 41번 해설 y=f(a)
    F = Frame((-0.9, 2.0), (-0.9, 3.6), 150, 55, M)
    F.axes('a'); O(F, 'rt', -6, 4)
    F.seg((-0.85, 2), (0, 2), 3.2); F.seg((0, 3), (0.25, 3), 3.2); F.seg((0.25, 1), (1, 1), 3.2); F.seg((1, 2), (1.25, 2), 3.2); F.seg((1.25, 0), (1.9, 0), 3.2)
    F.dashed((0.25, 0), (0.25, 3)); F.dashed((0, 2), (1, 2)); F.dashed((1, 0), (1, 2)); F.dashed((1.25, 0), (1.25, 2)); F.dashed((0, 1), (0.25, 1))
    odot(F, (0, 2)); fdot(F, (0, 3)); odot(F, (0.25, 3)); fdot(F, (0.25, 2)); odot(F, (0.25, 1)); fdot(F, (1, 1)); odot(F, (1, 2)); odot(F, (1.25, 2))
    fdot(F, (1.25, 1)); odot(F, (1.25, 0))
    F.dashed((1.0, 1), (1.25, 1))
    F.lab((0.25, 0), '\\dfrac{1}{4}', 'ct', 0, 8); F.lab((1, 0), '1', 'ct', 0, 8); F.lab((1.25, 0), '\\dfrac{5}{4}', 'ct', 0, 8)
    F.lab((0, 1), '1', 'rc', -8, 0); F.lab((0, 2), '2', 'rb', -8, -4); F.lab((0, 3), '3', 'rc', -8, 0)
    F.lab((0.75, 2), 'y=f(a)', 'cb', 0, -12)
    return F.render()


def tri(F, ox, oy, s):
    A, B, C = (ox, oy), (ox + 4 * s, oy), (ox + 4 * s, oy + 3 * s)
    F.seg(A, B, 3.2); F.seg(B, C, 3.2); F.seg(A, C, 3.2)
    right_mark(F, B, A, C, 0.28 * s)
    F.pt(A, 'A', 'rc', -8, 0); F.pt(B, 'B', 'lc', 8, 4); F.pt(C, 'C', 'cb', 0, -8)
    return A, B, C


def circ(F, c, r, wd=2.0):
    F.svg.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="#000" stroke-width="%s"/>' % (F.P(*c) + (r * F.sx, wd)))


def i26():  # 42번 문제 (AP=x 작을 때)
    F = Frame((-2.6, 4.7), (-2.6, 3.4), 60, 60, M)
    A, B, C = tri(F, 0, 0, 1.0)
    P = (0.35, 0); circ(F, P, 2); dot(F, P); F.pt(P, 'P', 'ct', 0, 8); F.lab((-1.6, -1.6), 'O', 'rt', 0, 0)
    return F.render()


def i24():  # 42번 해설 [그림 1] AP=2, [그림 2] AP=x, PH=2
    F = Frame((-0.6, 11.7), (-2.9, 3.3), 45, 45, M)
    A, B, C = tri(F, 0, 0, 1.0)
    P = (2, 0); circ(F, P, 2); dot(F, P); F.pt(P, 'P', 'ct', 0, 8); F.lab((0.6, -1.5), 'O', 'rt', 0, 0)
    F.lab((1, 0), '2', 'cb', 0, -6)
    F.lab((2.0, -2.5), '[\\text{그림 1}]', 'ct', 0, 4)
    ox = 5.8
    A, B, C = tri(F, ox, 0, 1.0)
    x = 10 / 3; P = (ox + x, 0); H = (ox + x * 16 / 25, x * 12 / 25)
    circ(F, P, 2); dot(F, P); F.seg(P, H, 2.0); right_mark(F, H, C, P, 0.25)
    F.pt(P, 'P', 'ct', -6, 8); F.pt(H, 'H', 'rb', -6, -4); F.lab(((P[0] + H[0]) / 2, (P[1] + H[1]) / 2), '2', 'lc', 6, 0)
    F.lab((ox + x / 2, 0), 'x', 'ct', 0, 6); F.lab((ox + x + 1.5, -1.5), 'O', 'lt', 0, 0)
    F.lab((ox + 2.0, -2.5), '[\\text{그림 2}]', 'ct', 0, 4)
    return F.render()


def i25():  # 42번 해설 y=f(x)
    F = Frame((-0.6, 4.7), (-1.1, 4.7), 70, 55, M)
    F.axes(); O(F, 'rt', -6, 4)
    t = 10 / 3
    F.seg((0, 2), (2, 2), 3.2); F.seg((2, 4), (t, 4), 3.2); F.seg((t, 2), (4, 2), 3.2)
    for x0 in (2, t):
        F.dashed((x0, 0), (x0, 4))
    F.dashed((4, 0), (4, 2)); F.dashed((0, 4), (2, 4)); F.dashed((0, 3), (t, 3)); F.dashed((2, 2), (t, 2))
    odot(F, (0, 2)); odot(F, (2, 2)); fdot(F, (2, 3)); odot(F, (2, 4)); odot(F, (t, 4)); fdot(F, (t, 3)); odot(F, (t, 2)); odot(F, (4, 2))
    F.lab((2, 0), '2', 'ct', 0, 8); F.lab((t, 0), '\\dfrac{10}{3}', 'ct', 0, 8); F.lab((4, 0), '4', 'ct', 4, 8)
    for y in (2, 3, 4):
        F.lab((0, y), str(y), 'rc', -8, 0)
    F.lab((2.6, 4), 'y=f(x)', 'cb', 0, -10)
    return F.render()


def i29():  # 53번 해설 y=f(x)
    F = Frame((-2.9, 4.4), (-2.6, 3.6), 55, 55, M)
    F.axes(); O(F, 'rt', -6, 4)
    F.seg((-2.8, -0.8), (0, 2), 3.2); F.seg((0, 3), (1, 2), 3.2); F.seg((1, -2), (4.2, 1.2), 3.2)
    F.dashed((0, 2), (1, 2)); F.dashed((1, 2), (1, -2)); F.dashed((0, -2), (1, -2))
    odot(F, (0, 2)); fdot(F, (0, 3)); fdot(F, (1, 2)); odot(F, (1, -2))
    F.lab((-2, 0), '-2', 'ct', 4, 8); F.lab((1, 0), '1', 'lt', 4, 6); F.lab((3, 0), '3', 'rt', -4, 6)
    F.lab((0, 3), '3', 'rc', -8, 0); F.lab((0, 2), '2', 'rc', -8, -4); F.lab((0, -2), '-2', 'rc', -8, 0)
    F.lab((0.6, 2.7), 'y=f(x)', 'lb', 8, -4)
    return F.render()


JOBS = {k: v for k, v in globals().items() if k[0] == 'i' and k[1:].isdigit()}
if __name__ == '__main__':
    run(JOBS, OUT, sys.argv[2:], wide=('i9', 'i20', 'i24'))
