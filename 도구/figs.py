# -*- coding: utf-8 -*-
"""1·2단원 문제 속 그림 (mathfig 약속 그대로). python3 figs.py 출력폴더 [이름...]"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mathfig as M
from mathfig import Frame, fit_shoot, dot, right_mark, SKY, GREEN

OPEN_R = 4.0


def odot(F, p):
    """빈 점(○): 흰 바탕 검은 테두리"""
    F.svg.append('<circle cx="%.1f" cy="%.1f" r="%s" fill="#fff" stroke="#000" stroke-width="1.6"/>' % (F.P(*p) + (OPEN_R,)))


def fdot(F, p):
    dot(F, p, 4.0)


def g(F, f, a, b):
    """함수 그래프 조각(굵기 3.2)"""
    F.curve(f, a, b)


def gl(F, p, q):
    """직선 모양 그래프 조각(그래프이므로 3.2)"""
    F.seg(p, q, M.STROKE)


def dash(F, *pts):
    for p, q in zip(pts, pts[1:]):
        F.dashed(p, q)


def xt(F, x, s, up=False, dx=0):
    F.lab((x, 0), s, 'cb' if up else 'ct', dx, -6 if up else 6)


def yt(F, y, s, right=False, dy=0):
    F.lab((0, y), s, 'lc' if right else 'rc', 7 if right else -7, dy)


def O(F, anc='rt', dx=-4, dy=4):
    F.pt((0, 0), 'O', anc, dx, dy)


def name(F, p, s, anc='lc', dx=6, dy=0):
    F.lab(p, s, anc, dx, dy)


def smooth(t):
    return t * t * (3 - 2 * t)


# ===================================================================== 1단원
def u1_q4():
    F = Frame((-3.0, 3.4), (-1.7, 2.8), 40, 40, (20, 14, 30, 14))
    F.axes()
    dash(F, (-2, 0), (-2, 1), (2, 1))
    dash(F, (-1, 0), (-1, -1)); dash(F, (0, 2), (1, 2), (1, 0)); dash(F, (2, 1), (2, 0))
    gl(F, (-2.8, 1.8), (-2, 1))
    gl(F, (-2, 0), (-1, -1)); gl(F, (-1, -1), (0, -1))
    gl(F, (0, 0), (1, 2)); gl(F, (1, 2), (2, 1)); gl(F, (2, 1), (3.2, 1))
    fdot(F, (-2, 1)); odot(F, (-2, 0)); odot(F, (0, -1)); fdot(F, (0, 0)); odot(F, (1, 2))
    fdot(F, (1, 1)); odot(F, (2, 1)); fdot(F, (2, 0))
    xt(F, -2, '-2', dx=-14); xt(F, -1, '-1', up=True); xt(F, 1, '1'); xt(F, 2, '2')
    yt(F, 1, '1', dy=12); yt(F, 2, '2'); F.lab((0, -1), '-1', 'lc', 8, 0)
    O(F, 'rt', -5, 4)
    name(F, (2.2, 1.9), 'y=f(x)', 'lc', 0, 0)
    return F.render()


def u1_q5_f():
    F = Frame((-2.7, 2.7), (-1.7, 1.9), 40, 40, (16, 14, 30, 14))
    F.axes()
    dash(F, (-2, 0), (-2, 1), (2, 1), (2, 0)); dash(F, (-1, 0), (-1, -1), (1, -1), (1, 0))
    gl(F, (-2.55, 1.55), (-1, 0)); gl(F, (-1, -1), (0, 0)); gl(F, (0, 0), (1, -1)); gl(F, (1, 0), (2.55, 1.55))
    odot(F, (-1, 0)); fdot(F, (-1, -1)); odot(F, (0, 0)); fdot(F, (0, 1)); fdot(F, (1, -1)); odot(F, (1, 0))
    xt(F, -2, '-2', dx=-4); xt(F, -1, '-1', dx=-16); xt(F, 1, '1', dx=14); xt(F, 2, '2')
    yt(F, 1, '1', dy=-12); F.lab((0, -1), '-1', 'lt', 6, 4)
    F.pt((0, 0), 'O', 'rb', -6, -6)
    name(F, (0.9, 1.65), 'y=f(x)', 'lc', 0, 0)
    return F.render()


def u1_q5_g():
    F = Frame((-1.7, 2.7), (-2.2, 1.9), 40, 40, (16, 14, 30, 14))
    F.axes()
    dash(F, (1, 1), (1, -1), (0, -1))
    gl(F, (-1.6, 1), (1, 1)); gl(F, (1, -1), (2.1, -2.1))
    fdot(F, (1, 1)); odot(F, (1, -1))
    xt(F, 1, '1', dx=14); yt(F, 1, '1', dy=-12); yt(F, -1, '-1')
    O(F)
    name(F, (1.25, 1.55), 'y=g(x)', 'lc', 0, 0)
    return F.render()


def u1_q6():
    F = Frame((-2.6, 1.7), (-1.6, 3.6), 44, 44, (20, 14, 90, 14))
    F.axes()
    dash(F, (-2, 0), (-2, 2), (1, 2)); dash(F, (1, 0), (1, 3), (0, 3)); dash(F, (-1, 0), (-1, 1), (0, 1))
    dash(F, (-1, -1), (0, -1))
    g(F, lambda x: 2 - 2 * (x + 2) ** 2, -2, -1)
    g(F, lambda x: -x * x, -1, 0)
    gl(F, (0, 1), (1, 3))
    fdot(F, (-2, 2)); odot(F, (-1, 0)); fdot(F, (-1, 1)); odot(F, (-1, -1)); odot(F, (0, 0))
    fdot(F, (0, 1)); odot(F, (1, 3)); fdot(F, (1, 2))
    xt(F, -2, '-2'); xt(F, -1, '-1', dx=-6); xt(F, 1, '1')
    yt(F, 1, '1', dy=-14); F.lab((0, 2), '2', 'rb', -6, -4); yt(F, 3, '3'); F.lab((0, -1), '-1', 'lc', 8, 0)
    O(F, 'lt', 5, 4)
    name(F, (1.0, 3.0), 'y=f(x)', 'lc', 10, 0)
    return F.render()


def u1_q8():
    F = Frame((-0.6, 6.8), (-0.5, 4.1), 34, 34, (16, 14, 30, 14))
    F.axes()
    a, b, c, d_, e = 1, 2, 3, 4, 6
    top = 3.0
    dash(F, (0, top), (d_, top))
    for x, y in ((a, 0.6), (b, 1.4), (c, top), (d_, top), (e, 3.6)):
        dash(F, (x, 0), (x, y))
    gl(F, (a, 0.6), (b, 1.4))
    g(F, lambda x: 0.9 + (x - b) ** 3 - 0.5 * math.sin(math.pi * (x - b)) * (1 - (x - b)), b, c)
    gl(F, (c, 1.9), (d_, 1.7))
    g(F, lambda x: 0.9 + 2.7 * (1 - (1 - (x - d_) / 2) ** 2), d_, e)
    fdot(F, (a, 0.6)); fdot(F, (b, 1.4)); odot(F, (b, 0.9)); odot(F, (c, 1.9)); fdot(F, (c, top))
    odot(F, (d_, 1.7)); fdot(F, (d_, top)); odot(F, (d_, 0.9)); odot(F, (e, 3.6))
    for x, s in ((a, 'a'), (b, 'b'), (c, 'c'), (d_, 'd'), (e, 'e')):
        xt(F, x, s)
    O(F)
    name(F, (6.0, 3.6), 'y=f(x)', 'rb', -8, -8)
    return F.render()


def u1_q30_f():
    F = Frame((-1.3, 4.7), (-0.8, 6.0), 30, 30, (20, 14, 30, 14))
    F.axes()
    dash(F, (0, 5), (3, 5)); dash(F, (3, 0), (3, 5))
    gl(F, (-1.2, 0), (0, 0)); gl(F, (0, 3), (3, 3)); gl(F, (3, 5), (4.7, 5))
    odot(F, (0, 0)); fdot(F, (0, 3)); odot(F, (3, 3)); fdot(F, (3, 5))
    xt(F, 3, '3'); yt(F, 3, '3'); yt(F, 5, '5')
    O(F)
    name(F, (2.3, 5.55), 'y=f(x)', 'lc', 0, 0)
    return F.render()


def u1_q30_g():
    F = Frame((-2.2, 4.7), (-1.2, 4.0), 30, 30, (20, 14, 30, 14))
    F.axes()
    dash(F, (0, 3), (3, 3)); dash(F, (3, 0), (3, 3))
    g(F, lambda x: 3 - x * x / 3, -2.1, 3)
    g(F, lambda x: 2.4 * math.sqrt(max(0, x - 3)), 3, 4.6)
    odot(F, (0, 3)); fdot(F, (0, 1)); odot(F, (3, 0)); fdot(F, (3, 3))
    xt(F, 3, '3', dx=8); yt(F, 1, '1'); F.lab((0, 3), '3', 'rb', -8, -4)
    O(F)
    name(F, (3.3, 3.6), 'y=g(x)', 'lc', 0, 0)
    return F.render()


def u1_q31():
    F = Frame((-0.5, 4.8), (-0.6, 3.7), 44, 44, (20, 16, 30, 14))
    F.axes()
    dash(F, (0, 3), (3, 3)); dash(F, (0, 2), (4, 2)); dash(F, (0, 1), (3, 1))
    for x, y in ((1, 1), (2, 3), (3, 3), (4, 2)):
        dash(F, (x, 0), (x, y))
    g(F, lambda x: 1 + 2 * (1 - x) ** 2, 0, 1)

    def mid(x):
        t = x - 1
        return 1 - 1.2 * t * (1 - t) ** 2 * 2.2 + 1.0 * smooth(t) + 3.2 * t * t * (1 - t)
    g(F, mid, 1, 2)
    gl(F, (2, 3), (3, 3))
    g(F, lambda x: 1 + (x - 3) ** 2, 3, 4)
    fdot(F, (0, 3)); odot(F, (1, 1)); fdot(F, (1, 0)); odot(F, (2, mid(2))); fdot(F, (2, 1))
    odot(F, (2, 3)); odot(F, (3, 3)); fdot(F, (3, 2)); odot(F, (3, 1)); fdot(F, (4, 2))
    for x in (1, 2, 3, 4):
        xt(F, x, str(x))
    for y in (1, 2, 3):
        yt(F, y, str(y))
    O(F)
    name(F, (1.0, 3.35), 'y=f(x)', 'lc', 0, 0)
    return F.render()


def u1_q32_f():
    F = Frame((-2.3, 2.5), (-1.9, 1.9), 40, 40, (16, 14, 30, 14))
    F.axes()
    gl(F, (-2.2, -1.2), (0, 1)); gl(F, (0, -1), (2.2, 1.2))
    odot(F, (0, 1)); fdot(F, (0, 0)); odot(F, (0, -1))
    xt(F, -1, '-1', up=True, dx=-16); xt(F, 1, '1', dx=8)
    yt(F, 1, '1', right=True); F.lab((0, -1), '-1', 'rc', -8, 0)
    O(F, 'rt', -6, 6)
    name(F, (1.0, 1.55), 'y=f(x)', 'lc', 0, 0)
    return F.render()


def u1_q32_g():
    F = Frame((-1.9, 1.9), (-0.5, 2.8), 40, 40, (16, 14, 30, 14))
    F.axes()
    dash(F, (-1, 0), (-1, 1), (1, 1), (1, 0))
    g(F, lambda x: x * x, -1.6, 1.6)
    xt(F, -1, '-1'); xt(F, 1, '1'); yt(F, 1, '1', dy=-12)
    O(F)
    name(F, (0.55, 2.45), 'y=g(x)', 'lc', 0, 0)
    return F.render()


def u1_q33():
    F = Frame((-0.8, 4.8), (-0.8, 3.9), 40, 40, (20, 14, 30, 14))
    F.axes()
    dash(F, (0, 3), (1, 3)); dash(F, (0, 2), (3, 2)); dash(F, (0, 1), (3, 1))
    dash(F, (1, 0), (1, 3)); dash(F, (2, 0), (2, 2)); dash(F, (3, 0), (3, 2))
    gl(F, (-0.6, -0.6), (1, 1)); gl(F, (1, 3), (3, 1)); gl(F, (3, 2), (4.7, 3.7))
    odot(F, (1, 1)); fdot(F, (1, 3)); odot(F, (2, 2)); fdot(F, (2, 1)); fdot(F, (3, 1)); odot(F, (3, 2))
    for x in (1, 2, 3):
        xt(F, x, str(x))
    for y in (1, 2, 3):
        yt(F, y, str(y))
    O(F, 'lt', 6, 4)
    name(F, (3.3, 3.5), 'y=f(x)', 'rc', 0, 0)
    return F.render()


def u1_q52_f():
    F = Frame((-2.3, 2.3), (-1.7, 1.9), 40, 40, (16, 14, 30, 14))
    F.axes()
    dash(F, (-1, 0), (-1, -1), (1, -1), (1, 0))
    gl(F, (-2.2, 1.2), (-1, 0)); gl(F, (1, 0), (2.2, 1.2))
    g(F, lambda x: -x * x, -1, 1)
    fdot(F, (-1, 0)); fdot(F, (1, 0)); odot(F, (-1, -1)); odot(F, (1, -1))
    xt(F, -1, '-1', dx=-16); xt(F, 1, '1', dx=14)
    F.lab((0, -1), '-1', 'rt', -5, 4)
    O(F, 'rb', -5, -6)
    name(F, (0.6, 1.55), 'y=f(x)', 'lc', 0, 0)
    return F.render()


def u1_q52_g():
    F = Frame((-2.3, 2.3), (-1.7, 1.9), 40, 40, (16, 14, 30, 14))
    F.axes()
    dash(F, (-1, 1), (-1, -1), (0, -1)); dash(F, (0, 1), (1, 1), (1, 0))
    gl(F, (-2.2, 1), (-1, 1)); gl(F, (-1, -1), (1, 1)); gl(F, (1, 1), (2.2, 1))
    fdot(F, (-1, 1)); odot(F, (-1, -1))
    xt(F, -1, '-1', dx=-10); xt(F, 1, '1', dx=8)
    yt(F, 1, '1', dy=-12); F.lab((0, -1), '-1', 'lc', 8, 0)
    O(F, 'lt', 6, 4)
    name(F, (0.9, 1.55), 'y=g(x)', 'lc', 0, 0)
    return F.render()


def u1_q59():
    F = Frame((-1.5, 2.0), (-0.5, 3.6), 54, 54, (16, 14, 30, 14))
    Pp = (1.25, 1.5625)
    F.poly([(0, 0), (0, 3), Pp], SKY)
    F.poly([(0, 0), (1, 0), Pp], GREEN)
    F.axes()
    g(F, lambda x: x * x, -1.75, 1.83)
    F.seg((0, 3), Pp); F.seg((0, 0), Pp); F.seg((1, 0), Pp)
    fdot(F, Pp)
    F.pt((0, 3), 'R', 'rc', -8, 0)
    F.pt(Pp, 'P', 'lc', 8, 2)
    F.pt((1, 0), 'Q', 'ct', 0, 6)
    O(F)
    F.lab((0.3, 1.75), 'B(x)', 'cc', 0, 0)
    F.seg((0.95, 0.45), (1.55, 0.55), 1.5)
    F.lab((1.55, 0.55), 'A(x)', 'lc', 4, 0)
    name(F, (1.83, 3.35), 'y=x^2', 'rc', -8, 0)
    return F.render()


# ===================================================================== 2단원
def u2_q2():
    F = Frame((-2.7, 2.7), (-1.6, 1.9), 40, 40, (16, 14, 30, 14))
    F.axes()
    dash(F, (-2, 0), (-2, 1), (1, 1), (1, 0)); dash(F, (-1, 0), (-1, 1))
    gl(F, (-2, 1), (-1, 0)); g(F, lambda x: x * x - 1, -1, 1); gl(F, (1, 1), (2, 0))
    odot(F, (-2, 1)); odot(F, (-1, 0)); fdot(F, (-1, 1)); odot(F, (0, -1)); fdot(F, (0, 0))
    odot(F, (1, 0)); fdot(F, (1, 1)); odot(F, (2, 0))
    xt(F, -2, '-2'); xt(F, -1, '-1', dx=-16); xt(F, 1, '1', dx=14); xt(F, 2, '2')
    F.lab((0, 1), '1', 'lb', 5, -2); F.lab((0, -1), '-1', 'rt', -8, 6)
    F.pt((0, 0), 'O', 'lt', 6, 4)
    name(F, (-2.1, 1.35), 'y=f(x)', 'lc', 0, 0)
    return F.render()


def u2_q4():
    F = Frame((-1.6, 3.7), (-2.6, 2.6), 40, 40, (20, 14, 30, 14))
    F.axes()
    dash(F, (-1, 0), (-1, -1), (0, -1)); dash(F, (1, 0), (1, -2), (0, -2))
    dash(F, (0, 1), (2, 1), (2, 0)); dash(F, (0, 2), (3, 2), (3, 0))
    gl(F, (-1, -1), (0, 0)); g(F, lambda x: -2 * x * x, 0, 1); g(F, lambda x: (x - 1) ** 2, 1, 2)
    g(F, lambda x: 1 + (x - 2) ** 2, 2, 3)
    fdot(F, (-1, -1)); odot(F, (1, -2)); fdot(F, (1, 0)); odot(F, (2, 1)); fdot(F, (2, 0)); fdot(F, (3, 2))
    xt(F, -1, '-1', up=True); xt(F, 1, '1', up=True, dx=8); xt(F, 2, '2'); xt(F, 3, '3')
    yt(F, 1, '1'); yt(F, 2, '2'); F.lab((0, -1), '-1', 'lc', 8, 0); F.lab((0, -2), '-2', 'rc', -7, 0)
    O(F, 'rb', -5, -6)
    name(F, (2.35, 2.35), 'y=f(x)', 'rc', 0, 0)
    return F.render()


def u2_q5():
    F = Frame((-1.6, 3.6), (-1.6, 2.4), 44, 44, (16, 14, 30, 14))
    F.axes()
    dash(F, (0, 1), (2, 1), (2, -1), (0, -1))
    gl(F, (-1.4, -1.4), (0, 0))
    g(F, lambda x: 1 + 0.9 * math.sqrt(max(0.0, 1 - (x - 1) ** 2)), 0, 2)
    gl(F, (2, -1), (3.5, -1))
    odot(F, (0, 0)); fdot(F, (0, 1)); odot(F, (2, 1)); fdot(F, (2, -1))
    xt(F, 2, '2', dx=12); yt(F, 1, '1'); yt(F, -1, '-1')
    O(F, 'lt', 6, 4)
    name(F, (2.3, 2.0), 'y=f(x)', 'lc', 0, 0)
    return F.render()


def u2_q18_f():
    F = Frame((-1.9, 1.9), (-1.6, 1.8), 44, 44, (16, 14, 30, 14))
    F.axes()
    dash(F, (-1, 0), (-1, 1), (1, 1), (1, -1), (-1, -1), (-1, 0))
    gl(F, (-1.8, 1), (-1, 1)); gl(F, (-1, -1), (1, 1)); gl(F, (1, -1), (1.8, -1))
    odot(F, (-1, 1)); fdot(F, (-1, -1)); fdot(F, (1, 1)); odot(F, (1, -1))
    xt(F, -1, '-1', up=True, dx=-18); xt(F, 1, '1', dx=14)
    F.lab((0, 1), '1', 'rb', -5, -3); F.lab((0, -1), '-1', 'rt', -5, 4)
    O(F, 'lt', 6, 4)
    name(F, (0.85, 1.5), 'y=f(x)', 'lc', 0, 0)
    return F.render()


def u2_q18_g():
    F = Frame((-1.9, 1.9), (-1.6, 1.8), 44, 44, (16, 14, 30, 14))
    F.axes()
    dash(F, (-1, -1), (1, -1)); dash(F, (1, 0), (1, 1), (0, 1)); dash(F, (1, 0), (1, -1))
    gl(F, (-1.8, -1), (-1, -1)); g(F, lambda x: -x * x, -1, 1); gl(F, (1, 1), (1.8, 1))
    odot(F, (-1, -1)); fdot(F, (-1, 0)); fdot(F, (1, -1)); odot(F, (1, 1))
    xt(F, -1, '-1', up=True, dx=-12); xt(F, 1, '1', up=True, dx=14)
    yt(F, 1, '1'); F.lab((0, -1), '-1', 'rt', -5, 4)
    F.pt((0, 0), 'O', 'rb', -5, -6)
    name(F, (0.55, 1.5), 'y=g(x)', 'lc', 0, 0)
    return F.render()


def u2_q19_f():
    F = Frame((-1.5, 2.9), (-1.0, 2.2), 44, 44, (16, 14, 30, 14))
    F.axes()
    dash(F, (0, 1), (1, 1), (1, 0))
    g(F, lambda x: x * x, -1.45, 1); gl(F, (1, 1), (2.8, -0.8))
    odot(F, (1, 1)); fdot(F, (1, 0))
    xt(F, 1, '1', dx=8); xt(F, 2, '2', dx=-12); yt(F, 1, '1')
    O(F)
    name(F, (1.2, 1.55), 'y=f(x)', 'lc', 0, 0)
    return F.render()


def u2_q19_g():
    F = Frame((-1.0, 3.1), (-1.6, 2.6), 44, 44, (16, 14, 30, 14))
    F.axes()
    dash(F, (0, 1), (2, 1), (2, -1), (0, -1)); dash(F, (1, 0), (1, 1))
    gl(F, (-0.9, -0.9), (1, 1))
    g(F, lambda x: 1 - 2 * math.sqrt(max(0.0, x - 1)), 1, 2)
    g(F, lambda x: 1 + 1.6 * (x - 2) ** 2, 2, 2.95)
    fdot(F, (2, -1)); odot(F, (2, 1))
    xt(F, 1, '1', dx=-8); xt(F, 2, '2', dx=10); yt(F, 1, '1'); yt(F, -1, '-1')
    O(F, 'lt', 6, 4)
    name(F, (2.3, 2.4), 'y=g(x)', 'rc', 0, 0)
    return F.render()


def u2_q23():
    F = Frame((-2.6, 3.7), (-3.6, 1.7), 40, 40, (20, 14, 30, 14))
    F.axes()
    dash(F, (-1, 0), (-1, -1), (0, -1)); dash(F, (0, 1), (1, 1), (1, 0))
    dash(F, (2, 0), (2, -3), (0, -3)); dash(F, (0, -2), (3, -2), (3, 0))
    g(F, lambda x: (x + 1) ** 2 - 1, -2, -1)
    g(F, lambda x: -1 + 2 * smooth((x + 1) / 2) if x <= 1 else 1 - 3 * (x - 1) ** 2, -1, 2)
    g(F, lambda x: -3 + (x - 2) ** 2, 2, 3)
    fdot(F, (-2, 0)); odot(F, (-1, -1)); fdot(F, (-1, 0)); fdot(F, (2, -2)); odot(F, (2, -3)); fdot(F, (3, -2))
    xt(F, -2, '-2', up=True); xt(F, -1, '-1', up=True); xt(F, 1, '1'); xt(F, 2, '2', up=True); xt(F, 3, '3', up=True)
    yt(F, 1, '1'); F.lab((0, -1), '-1', 'lc', 8, 0); yt(F, -2, '-2'); yt(F, -3, '-3')
    O(F, 'rb', -5, -5)
    name(F, (1.3, 1.35), 'y=f(x)', 'lc', 0, 0)
    return F.render()


def u2_q29():
    F = Frame((-1.6, 2.6), (-1.6, 2.6), 44, 44, (16, 14, 30, 14))
    F.axes()
    gl(F, (-1.4, 2.4), (0, 1)); gl(F, (0, -1), (2.4, 1.4))
    odot(F, (0, 1)); fdot(F, (0, 0)); odot(F, (0, -1))
    F.lab((0, 1), '1', 'lc', 9, 0); F.lab((0, -1), '-1', 'rc', -8, 0)
    O(F, 'rt', -6, 6)
    name(F, (1.4, 1.9), 'y=f(x)', 'lc', 0, 0)
    return F.render()


def u2_q32_f():
    F = Frame((-2.2, 1.6), (-1.2, 2.3), 40, 40, (16, 14, 30, 14))
    F.axes()
    gl(F, (-2.1, -1.1), (1.2, 2.2))
    xt(F, -1, '-1', dx=8); yt(F, 1, '1', dy=-10)
    O(F)
    name(F, (-1.3, 0.9), 'y=f(x)', 'rc', 0, 0)
    return F.render()


def u2_q32_g():
    F = Frame((-2.0, 2.1), (-1.9, 1.9), 40, 40, (16, 14, 30, 14))
    F.axes()
    dash(F, (-1, 1), (1, 1), (1, -1), (-1, -1), (-1, 1))
    gl(F, (-1.8, 1.8), (-1, 1)); gl(F, (-1, -1), (1, 1)); gl(F, (1, -1), (1.8, -1.8))
    odot(F, (-1, 1)); fdot(F, (-1, 0)); odot(F, (-1, -1)); odot(F, (1, 1)); fdot(F, (1, 0)); odot(F, (1, -1))
    xt(F, -1, '-1', dx=-26); xt(F, 1, '1', dx=20)
    F.lab((0, 1), '1', 'rb', -5, -3); F.lab((0, -1), '-1', 'lt', 5, 4)
    O(F, 'lt', 5, 5)
    name(F, (1.05, 1.5), 'y=g(x)', 'lc', 0, 0)
    return F.render()


def u2_q33_f():
    F = Frame((-1.8, 2.6), (-0.6, 1.8), 44, 44, (16, 14, 30, 14))
    F.axes()
    dash(F, (-1, 0), (-1, 1), (2, 1), (2, 0))
    gl(F, (-1.6, 1.6), (0, 0)); gl(F, (0, 0), (1, 0)); gl(F, (1, 0), (2.5, 1.5))
    xt(F, -1, '-1'); xt(F, 1, '1'); xt(F, 2, '2'); F.lab((0, 1), '1', 'rb', -6, -4)
    O(F)
    name(F, (1.7, 1.55), 'y=f(x)', 'rc', 0, 0)
    return F.render()


def u2_q33_g():
    F = Frame((-1.6, 2.7), (-0.6, 1.8), 44, 44, (16, 14, 30, 14))
    F.axes()
    dash(F, (0, 1), (1, 1))
    gl(F, (-1.5, 0), (0, 0)); gl(F, (0, 1), (1, 0)); gl(F, (1, 1), (2.6, 1))
    odot(F, (0, 0)); fdot(F, (0, 1)); odot(F, (1, 0)); fdot(F, (1, 1))
    xt(F, 1, '1'); yt(F, 1, '1')
    O(F)
    name(F, (1.1, 1.45), 'y=g(x)', 'lc', 0, 0)
    return F.render()


def u2_q35():
    F = Frame((-1.4, 3.2), (-0.8, 2.9), 44, 44, (20, 14, 30, 14))
    F.axes()
    dash(F, (0, 2), (1, 2), (1, 0)); dash(F, (0, 1), (1, 1))
    g(F, lambda x: 1.6 * x * x, -1.3, 0)
    gl(F, (0, 1), (1, 2)); gl(F, (1, 2), (3.0, -0.6))
    odot(F, (0, 0)); fdot(F, (0, 1)); odot(F, (1, 2)); fdot(F, (1, 1))
    xt(F, 1, '1', dx=-8); yt(F, 1, '1'); yt(F, 2, '2')
    O(F)
    name(F, (1.5, 2.5), 'y=f(x)', 'lc', 0, 0)
    return F.render()


def u2_q38():
    F = Frame((-0.4, 6.7), (-1.6, 2.6), 38, 38, (20, 14, 30, 14))
    F.axes()
    dash(F, (0, 2), (4, 2)); dash(F, (0, 1), (5, 1)); dash(F, (0, -1), (3, -1))
    dash(F, (2, 0), (2, 2)); dash(F, (4, 0), (4, 2)); dash(F, (3, 0), (3, -1)); dash(F, (5, 0), (5, 1))
    gl(F, (0, 1), (1, 0)); gl(F, (1, 0), (2, 1)); gl(F, (2, 1), (3, -1)); gl(F, (3, -1), (4, 0))
    gl(F, (4, 0), (5, 1)); gl(F, (5, 1), (6, 0))
    fdot(F, (0, 1)); odot(F, (2, 1)); fdot(F, (2, 2)); odot(F, (4, 0)); fdot(F, (4, 2)); fdot(F, (6, 0))
    for x in (1, 2, 4, 5, 6):
        xt(F, x, str(x), dx=(8 if x == 4 else 0))
    xt(F, 3, '3', up=True)
    yt(F, 1, '1'); yt(F, 2, '2'); yt(F, -1, '-1')
    O(F)
    name(F, (5.2, 1.4), 'y=f(x)', 'lc', 0, 0)
    return F.render()


def u2_q42():
    F = Frame((-0.6, 4.7), (-0.6, 5.8), 34, 34, (20, 14, 30, 14))
    F.axes()
    dash(F, (0, 4), (2, 4)); dash(F, (0, 1), (2, 1)); dash(F, (2, 0), (2, 4))
    gl(F, (-0.5, -0.25), (2, 1)); gl(F, (2, 4), (4.5, 5.25))
    odot(F, (2, 1)); fdot(F, (2, 4))
    xt(F, 2, '2'); yt(F, 1, '1'); yt(F, 4, '4')
    O(F, 'lt', 6, 4)
    name(F, (2.6, 3.7), 'y=f(x)', 'lc', 0, 0)
    return F.render()


# 이름: (함수, 문서 폭 HWPUNIT)
FIGS = {
    'u1_q4': (u1_q4, 12000), 'u1_q5_f': (u1_q5_f, 11000), 'u1_q5_g': (u1_q5_g, 9500),
    'u1_q6': (u1_q6, 9500), 'u1_q8': (u1_q8, 11000), 'u1_q30_f': (u1_q30_f, 9500), 'u1_q30_g': (u1_q30_g, 11000),
    'u1_q31': (u1_q31, 11000), 'u1_q32_f': (u1_q32_f, 9500), 'u1_q32_g': (u1_q32_g, 8500), 'u1_q33': (u1_q33, 11000),
    'u1_q52_f': (u1_q52_f, 10000), 'u1_q52_g': (u1_q52_g, 10000), 'u1_q59': (u1_q59, 9500),
    'u2_q2': (u2_q2, 11500), 'u2_q4': (u2_q4, 11000), 'u2_q5': (u2_q5, 10000),
    'u2_q18_f': (u2_q18_f, 9500), 'u2_q18_g': (u2_q18_g, 9500), 'u2_q19_f': (u2_q19_f, 10000), 'u2_q19_g': (u2_q19_g, 9500),
    'u2_q23': (u2_q23, 11500), 'u2_q29': (u2_q29, 9500), 'u2_q32_f': (u2_q32_f, 9000), 'u2_q32_g': (u2_q32_g, 10000),
    'u2_q33_f': (u2_q33_f, 10000), 'u2_q33_g': (u2_q33_g, 10000), 'u2_q35': (u2_q35, 10000),
    'u2_q38': (u2_q38, 12500), 'u2_q42': (u2_q42, 10000),
}

if __name__ == '__main__':
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    names = sys.argv[2:] or list(FIGS)
    for n in names:
        fn, w = FIGS[n]
        fit_shoot(n + '.png', fn, w, out)
