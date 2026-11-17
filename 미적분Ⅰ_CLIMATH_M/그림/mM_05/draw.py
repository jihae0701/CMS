# -*- coding: utf-8 -*-
"""미적분Ⅰ M 5. 도함수의 활용(2) — C에 없던 스캔 그림 다시 그리기 (iN = 문서의 imageN).  python3 draw.py 출력폴더 [이름...]"""
import sys, math
sys.path.insert(0, '/home/user/CMS/.claude/skills/math-figure-rules'); sys.path.insert(0, '/tmp/claude-0/-home-user-CMS/7a122d51-a5b1-5def-9637-d43cb9a9b6ef/scratchpad/figw')
from mathfig import Frame, SKY, PINK
from mjcommon import odot, fdot, plot, axes2, O, run, herm
OUT = sys.argv[1]
M = (16, 16, 16, 16)

from mathfig import DASH, dot


def bisect(h, a, b):
    for _ in range(60):
        m = (a + b) / 2
        if (h(a) > 0) == (h(m) > 0): a = m
        else: b = m
    return (a + b) / 2


def i12():  # 8번 해설 (ⅰ) a>0 (a=3 개형)
    f = lambda x: x ** 3 - 3 * x if x >= 0 else 3 * x - x ** 3
    F = Frame((-2.3, 2.6), (-2.6, 2.4), 60, 60, M)
    F.axes(); O(F, 'rt', -2, 4)
    plot(F, f, -2.05, 2.05, n=300)
    F.dashed((-1, 0), (-1, -2)); F.dashed((1, 0), (1, -2))
    F.lab((-1, 0), '-\\sqrt{\\dfrac{a}{3}}', 'cb', 0, -6); F.lab((1, 0), '1', 'cb', 6, -8)
    F.lab((2.05, f(2.05)), 'y=f(x)', 'rc', -12, 0)
    return F.render()


def i13():  # 8번 해설 (ⅱ) a<0 (a=-5/2)
    a = -2.5
    f = lambda x: a * (x ** 3 - 3 * x) if x >= 0 else a * x - x ** 3
    F = Frame((-1.2, 2.6), (-1.6, 6.2), 60, 40, M)
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, f, -1.05, 1.98, n=300)
    F.dashed((1, 0), (1, 5)); F.dashed((0, 5), (1, 5))
    F.lab((1, 0), '1', 'lt', 4, 6); F.lab((0, 5), '5', 'rc', -8, 0)
    F.lab((1, 5), 'y=f(x)', 'lb', 8, -6)
    return F.render()


def i14():  # 10번 해설 f(x)=(x+1)(x-3)^3 개형
    f = lambda x: 0.06 * (x + 1) * (x - 3) ** 3
    F = Frame((-1.6, 4.4), (-1.9, 1.6), 60, 60, M)
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, f, -1.25, 4.15)
    return F.render()


def gt(o, F, a):
    g = lambda t: 0.35 * t * t * abs(2 * t + a)
    plot(F, lambda x: g(x - o), o + min(0, -a / 2) - 0.62, o + max(0, -a / 2) + 0.62, n=300)
    return g


def i22():  # 22번 해설 a>0
    F = Frame((-2.6, 1.6), (-0.9, 2.2), 70, 70, M)
    F.axes(); O(F, 'rt', -6, 4)
    a = 3; g = gt(0, F, a)
    F.lab((-a / 2, 0), '-\\dfrac{a}{2}', 'ct', 0, 8); F.lab((0.62, g(0.62)), 'y=g(t)', 'lc', 8, 0)
    return F.render()


def i23():  # 22번 해설 a<0
    F = Frame((-1.6, 2.6), (-0.9, 2.2), 70, 70, M)
    F.axes(); O(F, 'rt', -6, 4)
    a = -3; g = gt(0, F, a)
    F.lab((-a / 2, 0), '-\\dfrac{a}{2}', 'ct', 0, 8); F.lab((2.12, g(2.12)), 'y=g(t)', 'rc', -12, 0)
    return F.render()


def i24():  # 24번 문제 y=f'(x)(직선), y=g'(x)(이차)
    p = lambda x: 0.45 * (x - 0.7) * (x - 4.6); l = lambda x: 0.75 * (x - 2.2)
    b = bisect(lambda x: p(x) - l(x), 0.7, 2.2); e = bisect(lambda x: p(x) - l(x), 4.6, 7)
    F = Frame((-0.8, 8.9), (-2.6, 3.4), 55, 55, M)
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, p, -0.35, 5.9); F.seg((-0.5, l(-0.5)), (7.0, l(7.0)), 2.0)
    F.dashed((b, 0), (b, p(b))); F.dashed((e, 0), (e, p(e)))
    F.lab((0.7, 0), 'a', 'cb', -4, -8); F.lab((b, 0), 'b', 'cb', 4, -8); F.lab((2.2, 0), 'c', 'ct', 0, 8); F.lab((4.6, 0), 'd', 'cb', 0, -8); F.lab((e, 0), 'e', 'ct', 0, 8)
    F.lab((5.9, p(5.9)), "y=g'(x)", 'rc', -12, 0); F.lab((7.0, l(7.0)), "y=f'(x)", 'lt', -6, 8)
    return F.render()


def i27():  # 40번 해설 y=f'(x)=-3(x-1)^2+10 개형
    f = lambda x: 0.32 * (-3 * (x - 1) ** 2 + 10)
    F = Frame((-2.7, 4.4), (-3.2, 3.9), 55, 55, M)
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, f, -2.05, 4.05)
    F.dashed((-2, 0), (-2, f(-2))); F.dashed((1, 0), (1, f(1))); F.dashed((3, 0), (3, f(3)))
    F.lab((-2, 0), '-2', 'cb', 0, -8); F.lab((1, 0), '1', 'ct', 6, 8); F.lab((3, 0), '3', 'cb', 6, -8)
    F.lab((1.5, f(1.5)), "y=f'(x)", 'lb', 10, -6)
    return F.render()


f43 = lambda x: (x - 1) ** 3 + 1


def i28():  # 43번 해설 f(x)=(x-1)^3+1
    F = Frame((-0.9, 2.6), (-1.4, 3.0), 75, 75, M)
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, f43, -0.35, 2.2)
    F.dashed((1, 0), (1, 1)); F.dashed((0, 1), (1, 1))
    F.lab((1, 0), '1', 'ct', 0, 8); F.lab((0, 1), '1', 'rc', -8, 0); F.lab((2.2, f43(2.2)), 'y=f(x)', 'rc', -12, 0)
    return F.render()


def absk(F, o, k, x0=-0.55, x1=2.3):
    h = lambda x: f43(x) - k
    z = 1 + (k - 1) ** (1 / 3) if k >= 1 else 1 - (1 - k) ** (1 / 3)
    plot(F, lambda x: abs(h(x - o)), o + x0, o + x1, n=300)
    xa = bisect(lambda x: h(x) + 2.7, -3, z)
    plot(F, lambda x: h(x - o), o + max(x0, xa), o + z, wd=2.0, dash=DASH)
    return h


def i29():  # 43번 해설 k<1, k>1
    F = Frame((-1.2, 7.4), (-2.9, 2.9), 60, 60, M)
    o2 = 4.4
    for o, k, cap in ((0, 0.5, '(k<1\\text{일 때})'), (o2, 1.6, '(k>1\\text{일 때})')):
        axes2(F, o, o - 1.2, o + 2.8, -2.0, 2.9); F.pt((o, 0), 'O', 'rt', -6, 4)
        h = absk(F, o, k)
        F.lab((o, abs(h(0))), 'k', 'rb', -6, -2); F.lab((o, h(0)), '-k', 'rc', -8, 0)
        F.lab((o + 2.3, abs(h(2.3))), 'y=g(x)', 'rc', -12, 0); F.lab((o + 1.0, -2.2), cap, 'ct', 0, 6)
    return F.render()


def i30():  # 43번 해설 k=1
    F = Frame((-0.9, 2.6), (-2.0, 2.6), 75, 75, M)
    F.axes(); O(F, 'rt', -6, 4)
    absk(F, 0, 1.0)
    F.lab((0, 1), '1', 'rc', -8, 0); F.lab((0, -1), '-1', 'lc', 8, 4); F.lab((2.3, abs(f43(2.3) - 1)), 'y=g(x)', 'rc', -12, 0)
    return F.render()


def cub(F, o, line):
    f = lambda x: 0.55 * (x - o) ** 3 - 1.5 * (x - o)
    plot(F, f, o - 2.05, o + 2.05)
    a, b = line
    F.seg((o - 2.4, a * -2.4 + b), (o + 2.4, a * 2.4 + b), 2.0)
    F.lab((o + 2.05, f(o + 2.05)), 'y=f(x)', 'rc', -12, 0); F.lab((o + 2.4, a * 2.4 + b), 'y=g(x)', 'lt', 6, 6)


def i31():  # 44번 해설 두 그래프(교점이 생기는 경우)
    F = Frame((-2.7, 11.0), (-2.2, 2.6), 45, 45, M)
    cub(F, 0, (0.35, 0.0)); cub(F, 6.2, (0.35, 0.9))
    return F.render()


def i32():  # 44번 해설 변곡점에서 접할 때
    f = lambda x: 0.55 * x ** 3 - 1.5 * x
    F = Frame((-2.3, 3.4), (-2.6, 2.6), 60, 60, M)
    plot(F, f, -2.05, 2.05); F.seg((-1.7, 2.55), (1.7, -2.55), 2.0); dot(F, (0, 0))
    F.lab((2.05, f(2.05)), 'y=f(x)', 'rc', -12, 0); F.lab((1.7, -2.55), 'y=g(x)', 'lc', 6, 0)
    return F.render()


def i38():  # 53번 문제 이차함수 f(-1)=f(3)=0
    f = lambda x: 0.6 * (x + 1) * (x - 3)
    F = Frame((-2.0, 4.6), (-2.8, 2.6), 55, 55, M)
    F.axes(); O(F, 'lt', 4, 4)
    plot(F, f, -1.75, 3.75)
    F.lab((-1, 0), '-1', 'rb', -4, -4); F.lab((3, 0), '3', 'lb', 4, -4); F.lab((3.75, f(3.75)), 'y=f(x)', 'rc', -12, 0)
    return F.render()


def i39():  # 55번 해설
    f = lambda x: x if abs(x) >= 1 else -3 * x * x + x + 3
    F = Frame((-2.6, 3.4), (-2.4, 3.6), 55, 55, M)
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, f, -2.4, 3.0, n=400)
    F.dashed((1, 0), (1, 1)); F.dashed((0, 1), (1, 1)); F.dashed((-1, 0), (-1, -1)); F.dashed((-1, -1), (0, -1))
    F.lab((1, 0), '1', 'ct', 0, 8); F.lab((-1, 0), '-1', 'cb', -6, -8); F.lab((0, 1), '1', 'rc', -8, 0); F.lab((0, -1), '-1', 'lc', 8, 0)
    F.lab((0, 3), '3', 'rb', -6, -4); F.lab((3.0, 3.0), 'y=f(x)', 'rc', -12, 0)
    return F.render()


def sixtyone(a, k):
    h = lambda x: 0.3 * (x - a) ** 2 * (x - k) if a != k else 0.45 * (x - a) ** 3
    lo = min(a, k) - (1.0 if a != k else 1.5)
    hi = bisect(lambda x: abs(h(x)) - 2.3, max(a, k) + 0.01, max(a, k) + 4)
    F = Frame((lo - 0.2, hi + 0.6), (-2.6, 2.6), 60, 60, M)
    F.xaxis(lo - 0.2, hi + 0.6)
    plot(F, lambda x: abs(h(x)), lo, hi, n=400)
    xs = [lo + (hi - lo) * i / 400 for i in range(401)]
    seg = [x for x in xs if h(x) < 0]
    if seg:
        x0 = max(seg[0], bisect(lambda x: h(x) + 2.5, lo - 3, seg[-1]))
        plot(F, h, x0, seg[-1], wd=2.0, dash=DASH)
    F.lab((hi, abs(h(hi))), 'y=g(x)', 'rc', -12, 0)
    return F


def i43():  # 61번 해설 a<k
    F = sixtyone(0, 3.0); F.lab((0, 0), 'a', 'ct', 0, 8); F.lab((3.0, 0), 'k', 'ct', 0, 8)
    return F.render()


def i44():  # 61번 해설 a=k
    F = sixtyone(0, 0); F.lab((0, 0), 'a=k', 'ct', 0, 8)
    return F.render()


def i45():  # 61번 해설 a>k
    F = sixtyone(3.0, 0); F.lab((0, 0), 'k', 'ct', 0, 8); F.lab((3.0, 0), 'a', 'ct', 0, 8)
    return F.render()


f63 = lambda x: (x - 3) ** 3 * (x + 1) + 27


def i46():  # 63번 해설 [그림 1] y=g(x)-27, [그림 2] y=f(x), y=27
    s = 0.07
    F = Frame((-4.9, 13.4), (-3.3, 3.9), 45, 45, (70, 16, 16, 16))
    g = lambda x: (f63(abs(x)) - 27) * s
    axes2(F, 0, -4.8, 4.9, -2.4, 3.0); O(F, 'rt', -4, 4)
    plot(F, g, -4.25, 4.25, n=400)
    F.lab((-3, 0), '-\\alpha', 'cb', 0, -8); F.lab((3, 0), '\\alpha', 'cb', 0, -8); F.lab((0, g(0)), '-27', 'lc', 8, 0)
    F.lab((-4.25, g(4.25)), 'y=g(x)-27', 'lb', -4, -16); F.lab((0, -2.7), '[\\text{그림 1}]', 'ct', 0, 4)
    o = 8.0
    axes2(F, o, o - 2.4, o + 4.9, -0.8, 3.9); F.pt((o, 0), 'O', 'rt', -4, 4)
    h = lambda x: f63(x - o) * s
    plot(F, h, o - 1.3, o + 4.0, n=400); F.seg((o - 2.3, 27 * s), (o + 4.6, 27 * s), 2.0)
    F.dashed((o - 1, 0), (o - 1, 27 * s)); F.dashed((o + 3, 0), (o + 3, 27 * s))
    F.lab((o - 1, 0), '\\beta', 'ct', 0, 8); F.lab((o + 3, 0), '\\alpha', 'ct', 0, 8)
    F.lab((o - 2.3, 27 * s), 'y=27', 'rc', -6, 0); F.lab((o + 4.0, h(o + 4.0)), 'y=f(x)', 'rc', -12, -6); F.lab((o + 1.2, -2.7), '[\\text{그림 2}]', 'ct', 0, 4)
    return F.render()


JOBS = {k: v for k, v in globals().items() if k[0] == 'i' and k[1:].isdigit()}
if __name__ == '__main__':
    run(JOBS, OUT, sys.argv[2:], wide=('i29', 'i31', 'i46'))
