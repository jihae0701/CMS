# -*- coding: utf-8 -*-
"""미적분Ⅰ M 10. 정적분의 활용 — C에 없던 스캔 그림 다시 그리기 (iN = 문서의 imageN).  python3 draw.py 출력폴더 [이름...]"""
import sys, math
sys.path.insert(0, '/home/user/CMS/.claude/skills/math-figure-rules'); sys.path.insert(0, '/tmp/claude-0/-home-user-CMS/7a122d51-a5b1-5def-9637-d43cb9a9b6ef/scratchpad/figw')
from mathfig import Frame, SKY, PINK
from mjcommon import odot, fdot, plot, axes2, O, run, herm
OUT = sys.argv[1]
M = (16, 16, 16, 16)

from mathfig import DASH, dot, right_mark, GREEN
from mjcommon import arr


def area(F, f, a, b, g=lambda x: 0, col=SKY, n=80):
    F.poly([(a + (b - a) * i / n, f(a + (b - a) * i / n)) for i in range(n + 1)] + [(b - (b - a) * i / n, g(b - (b - a) * i / n)) for i in range(n + 1)], col)


def i3():   # 3번 해설 y=x^2-3|x|+2
    f = lambda x: x * x - 3 * abs(x) + 2
    F = Frame((-2.9, 3.0), (-0.9, 2.6), 60, 60, M)
    area(F, f, -2, 2)
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, f, -2.75, 2.75, n=300)
    for x in (-2, -1, 1, 2):
        F.lab((x, 0), str(x) if x > 0 else '-%d' % -x, 'cb' if abs(x) == 1 else 'ct', 0, -8 if abs(x) == 1 else 8)
    F.lab((0, 2), '2', 'lb', 6, -2); F.lab((2.75, f(2.75)), 'y=x^2-3|x|+2', 'rc', -12, -6)
    return F.render()


f11 = lambda x: 2 * x ** 3 + 1


def eleven(F, o, shade):
    g = lambda x: f11(x - 2) + 2
    if shade == 'para':
        F.poly([(o - 1, -1), (o + 1, 3), (o + 3, 5), (o + 1, 1)], SKY)
    elif shade == 'bulge':
        F.poly([(o - 1, -1), (o + 1, 3), (o + 3, 5), (o + 1, 1)], SKY)
        area(F, lambda x: f11(x - o), o - 1, o + 1, lambda x: 2 * (x - o) + 1, PINK)
        area(F, lambda x: g(x - o), o + 1, o + 3, lambda x: 2 * (x - o) - 1, PINK)
    axes2(F, o, o - 2.4, o + 3.9, -2.4, 5.9); F.pt((o, 0), 'O', 'rt', -4, 4)
    plot(F, lambda x: f11(x - o), o - 1.15, o + 1.15); plot(F, lambda x: g(x - o), o + 0.85, o + 3.12)
    F.seg((o - 2.3, -2.3), (o + 3.8, 3.8), 2.0); F.seg((o - 2.3, -0.3), (o + 3.5, 5.5), 2.0)
    for p in [(-1, -1), (1, 3), (3, 5), (1, 1)]:
        F.dashed((o + p[0], 0), (o + p[0], p[1])); F.dashed((o, p[1]), (o + p[0], p[1]))
    F.lab((o - 1, 0), '-1', 'cb', -6, -8); F.lab((o + 1, 0), '1', 'lt', 4, 6); F.lab((o + 3, 0), '3', 'ct', 0, 8); F.lab((o - 2, 0), '-2', 'cb', 0, -8)
    for y in (1, 3, 5):
        F.lab((o, y), str(y), 'rc', -8, 0)
    F.lab((o, -1), '-1', 'lc', 6, 4)
    F.lab((o - 1.15, f11(-1.15)), 'y=f(x)', 'rc', -6, 0); F.lab((o + 3.12, g(3.12)), 'y=f(x-2)+2', 'lb', 6, -6)
    F.lab((o + 3.8, 3.8), 'y=x', 'lc', 6, 0); F.lab((o + 3.5, 5.5), 'y=x+2', 'lt', 6, 6)


def i6():   # 11번 문제
    F = Frame((-4.2, 7.6), (-2.5, 6.9), 42, 42, M)
    eleven(F, 0, None)
    return F.render()


def i5():   # 11번 해설 (두 부분의 넓이가 같음 → 평행사변형)
    F = Frame((-4.2, 20.6), (-2.5, 6.9), 36, 36, M)
    eleven(F, 0, 'bulge'); eleven(F, 12.0, 'para')
    arr(F, (6.9, 2.0), (7.9, 2.0), 2.4, 12)
    return F.render()


def i7():   # 12번 문제 y=-x^2+4x, O, A(3,3), P(t,-t^2+4t) (t=1.5 개형)
    f = lambda x: -x * x + 4 * x
    t = 1.5; P = (t, f(t)); A = (3, 3)
    F = Frame((-0.6, 5.2), (-1.6, 4.6), 60, 60, M)
    area(F, f, 0, t, lambda x: x * f(t) / t, SKY); area(F, f, t, 3, lambda x: P[1] + (x - t) * (3 - P[1]) / (3 - t), PINK)
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, f, -0.15, 4.25)
    F.seg((0, 0), P); F.seg(P, A)
    dot(F, P); dot(F, A)
    F.pt(P, 'P', 'rb', -4, -6); F.lab(A, '\\mathrm{A}(3,~3)', 'lb', 6, -4)
    F.lab((0.42, 1.75), 'S_1', 'rc', -4, 0); F.lab((2.3, 3.75), 'S_2', 'cc')
    F.lab((4, 0), '4', 'rt', -4, 6); F.lab((4.2, f(4.2)), 'y=-x^2+4x', 'rc', -10, 4)
    return F.render()


def i34():  # 43번 해설 f(x)=x(4-x)/3, g(x)=|x-1|-1
    f = lambda x: x * (4 - x) / 3; g = lambda x: abs(x - 1) - 1
    F = Frame((-1.6, 6.8), (-1.6, 2.6), 60, 60, M)
    area(F, f, 0, 3, g)
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, f, -0.4, 4.6); F.polyline([(-1.4, 0.4), (1, -1), (4.6, 2.6)])
    F.dashed((1, 0), (1, -1)); F.dashed((0, -1), (1, -1)); F.dashed((3, 0), (3, 1))
    F.lab((1, 0), '1', 'cb', 0, -8); F.lab((3, 0), '3', 'cb', 6, -8); F.lab((4, 0), '4', 'ct', 4, 8); F.lab((2, 0), '2', 'ct', 0, 8); F.lab((0, -1), '-1', 'rc', -8, 0)
    F.lab((4.6, f(4.6)), 'y=f(x)', 'lc', 6, 0); F.lab((4.6, 2.6), 'y=g(x)', 'lc', 6, 0)
    return F.render()


R45 = math.sqrt(2)


def lens(F):
    n = 60
    top = [(x, 1.5 - math.sqrt(2 - x * x)) for x in [-1 + 2 * i / n for i in range(n + 1)]]
    bot = [(x, x * x / 2) for x in [1 - 2 * i / n for i in range(n + 1)]]
    F.poly(top + bot, SKY)


def circ(F, c, r, wd=2.0):
    F.svg.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="#000" stroke-width="%s"/>' % (F.P(*c) + (r * F.sx, wd)))


def i37():  # 45번 문제 속 [모양] 아이콘
    F = Frame((-1.05, 1.05), (-0.04, 0.54), 70, 70, (6, 6, 6, 6))
    lens(F)
    plot(F, lambda x: 1.5 - math.sqrt(2 - x * x), -1, 1, wd=2.4); plot(F, lambda x: x * x / 2, -1, 1, wd=2.4)
    return F.render()


def i38():  # 45번 문제
    F = Frame((-3.0, 3.3), (-0.7, 3.6), 60, 60, M)
    lens(F)
    F.axes(); O(F, 'ct', 0, 8)
    plot(F, lambda x: x * x / 2, -2.6, 2.6); circ(F, (0, 1.5), R45)
    dot(F, (0, 1.5)); F.lab((0, 1.5), '\\dfrac{3}{2}', 'rc', -8, 0); F.lab((-1.2, 2.5), 'C', 'rb', 0, 0)
    F.lab((2.6, 3.38), 'y=\\dfrac{1}{2}x^2', 'rc', -12, -4)
    return F.render()


def i36():  # 45번 해설
    F = Frame((-3.0, 4.6), (-1.4, 3.6), 60, 60, M)
    lens(F)
    F.axes(); O(F, 'ct', 0, 8)
    plot(F, lambda x: x * x / 2, -2.6, 2.6); circ(F, (0, 1.5), R45)
    F.seg((-1.4, 2.9), (2.3, -0.8), 2.0); F.seg((-0.2, -0.7), (2.6, 2.1), 2.0)
    F.seg((-1, 0.5), (0, 1.5), 2.0)
    for p in [(0, 1.5), (1, 0.5), (-1, 0.5)]:
        dot(F, p)
    right_mark(F, (0, 1.5), (-1, 0.5), (1, 0.5), 0.18); right_mark(F, (1, 0.5), (0, 1.5), (2, 1.5), 0.18)
    F.pt((0, 1.5), 'A', 'lc', 8, -6); F.pt((1, 0.5), 'P', 'lt', 6, 4); F.pt((-1, 0.5), 'Q', 'rt', -6, 4)
    F.lab((2.3, -0.8), 'y=-x+\\dfrac{3}{2}', 'lc', 6, 0); F.lab((2.6, 3.38), 'y=\\dfrac{1}{2}x^2', 'rc', -12, -4)
    return F.render()


def i41():  # 48번 문제 y=x^2, y=k, x=2 (k=1.2 개형)
    k = 1.2; r = math.sqrt(k)
    F = Frame((-0.7, 3.8), (-0.6, 4.6), 70, 55, M)
    area(F, lambda x: k, 0, r, lambda x: x * x, GREEN); area(F, lambda x: x * x, r, 2, lambda x: k, GREEN)
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, lambda x: x * x, -0.4, 2.1); F.seg((-0.5, k), (2.9, k), 2.0)
    F.dashed((2, 0), (2, 4)); F.dashed((0, 4), (2, 4))
    F.lab((0, k), 'k', 'rc', -8, 0); F.lab((0, 4), '4', 'rc', -8, 0); F.lab((2, 0), '2', 'ct', 0, 8)
    F.lab((0.42, 0.75), 'S_1', 'cc'); F.lab((1.72, 1.75), 'S_2', 'cc')
    F.lab((2.9, k), 'y=k', 'lc', 6, 0); F.lab((2.1, 4.41), 'y=x^2', 'lc', 6, 0)
    return F.render()


f50 = lambda x: x * (x - 6) * (x - 9) / 9
K = 5 - math.sqrt(7)


def fifty(t, labs, lines=(), extra=None, xl=-0.9, xr=10.6):
    F = Frame((xl, xr), (-3.6, 7.6), 46, 40, M)
    e = t + f50(t)
    area(F, f50, 0, t); F.poly([(t, 0), (t, f50(t)), (e, 0)], SKY)
    F.axes(); F.lab((0, 0), '0', 'rt', -4, 4)
    plot(F, f50, -0.35, t); plot(F, f50, t, 10.05, wd=2.4, dash=DASH)
    F.seg((t, f50(t)), (e + 1.2, -1.2), 3.2)
    for a, b in lines:
        F.seg(a, b, 2.0)
    F.lab((10.05, f50(10.05)), 'y=f(x)', 'rc', -12, 0)
    for x, s, anc, dx, dy in labs:
        F.lab((x, 0), s, anc, dx, dy)
    if extra: extra(F)
    return F


def i44():  # 50번 해설 0<t<k
    t = 1.0
    F = fifty(t, [(t, 't', 'ct', 0, 8), (K, 'k', 'ct', 0, 8), (6, '6', 'cb', 0, -8), (9, '9', 'cb', 0, -8)],
              [((t - 0.6, f50(t) + 0.6), (t, f50(t)))], xl=-0.9)
    F.dashed((t, 0), (t, f50(t))); F.dashed((K, 0), (K, f50(K)))
    F.leader((5.0, 6.7), (t + 2.0, f50(t) - 2.0)); F.lab((5.0, 6.7), 'y=-(x-t)+f(t)', 'lb', -4, -2); F.lab((-0.3, f50(-0.3)), 'y=g(x)', 'lc', 10, 0)
    return F.render()


def i45():  # 50번 해설 t=k
    t = K
    F = fifty(t, [(t, 'k', 'ct', 0, 8), (6, '6', 'ct', 0, 8), (9, '9', 'cb', 0, -8)], [((t - 0.6, f50(t) + 0.6), (t, f50(t)))], xl=-0.9)
    F.dashed((t, 0), (t, f50(t)))
    F.leader((5.0, 6.7), (t + 2.0, f50(t) - 2.0)); F.lab((5.0, 6.7), 'y=-(x-t)+f(t)', 'lb', -4, -2); F.lab((-0.3, f50(-0.3)), 'y=g(x)', 'lc', 10, 0)
    return F.render()


def i46():  # 50번 해설 t=3
    t = 3
    F = fifty(t, [(3, '3', 'ct', 0, 8), (6, '6', 'cb', 0, -8), (9, '9', 'cb', 6, -8)], [((1.5, 7.5), (3, 6))])
    F.dashed((3, 0), (3, 6)); F.dashed((K, 0), (K, f50(K)))
    dot(F, (3, 6)); F.lab((3, 6), '(3,~6)', 'lb', 6, -4); F.lab((1.5, 7.5), 'y=-x+9', 'lc', 6, 0)
    F.leader((K, -0.1), (K - 0.3, -1.3)); F.lab((K - 0.3, -1.3), '5-\\sqrt{7}', 'ct', 0, 4)
    return F.render()


def i47():  # 50번 해설 k<t<3
    t = 2.7
    F = fifty(t, [(K, 'k', 'ct', -4, 8), (t, 't', 'ct', 0, 8), (3, '3', 'ct', 6, 8), (6, '6', 'cb', 0, -8), (9, '9', 'cb', 6, -8)],
              [((1.2, 7.8), (10.2, -1.2))])
    for x in (K, t, 3):
        F.dashed((x, 0), (x, f50(x)))
    dot(F, (3, 6)); F.lab((3, 6), '(3,~6)', 'lb', 6, -4); F.lab((1.2, 7.8), 'y=-x+9', 'lc', 6, 0)
    return F.render()


def i48():  # 50번 해설 3<t<6
    t = 4.6
    F = fifty(t, [(K, 'k', 'ct', 0, 8), (3, '3', 'ct', 0, 8), (t, 't', 'ct', 0, 8), (6, '6', 'ct', 4, 8), (9, '9', 'cb', 6, -8)],
              [((1.2, 7.8), (10.2, -1.2))])
    for x in (K, 3, t):
        F.dashed((x, 0), (x, f50(x)))
    dot(F, (3, 6)); F.lab((3, 6), '(3,~6)', 'lb', 6, -4); F.lab((1.2, 7.8), 'y=-x+9', 'lc', 6, 0); F.lab((1.0, -2.6), 'y=g(x)', 'lc', 6, 0)
    return F.render()


def i49():  # 50번 [다른 풀이] 일반의 t
    t = 1.2
    F = fifty(t, [(t, 't', 'ct', 0, 8), (t + f50(t), 't+f(t)', 'ct', 0, 8), (6, '6', 'cb', 0, -8), (9, '9', 'cb', 0, -8)],
              [((t - 0.6, f50(t) + 0.6), (t, f50(t)))], xl=-2.6)
    F.dashed((t, 0), (t, f50(t))); dot(F, (t, f50(t)))
    F.lab((t, f50(t)), '(t,~f(t))', 'rc', -8, 6); F.leader((5.0, 6.7), (t + 2.0, f50(t) - 2.0)); F.lab((5.0, 6.7), 'y=-(x-t)+f(t)', 'lb', -4, -2)
    F.lab((-0.3, f50(-0.3)), 'y=g(x)', 'lc', 10, 0)
    return F.render()


JOBS = {k: v for k, v in globals().items() if k[0] == 'i' and k[1:].isdigit()}
if __name__ == '__main__':
    run(JOBS, OUT, sys.argv[2:], wide=('i5',))
