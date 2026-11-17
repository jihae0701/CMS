# -*- coding: utf-8 -*-
"""미적분Ⅰ M 6. 도함수의 활용(3) — C에 없던 스캔 그림 다시 그리기 (iN = 문서의 imageN).  python3 draw.py 출력폴더 [이름...]"""
import sys, math
sys.path.insert(0, '/home/user/CMS/.claude/skills/math-figure-rules'); sys.path.insert(0, '/tmp/claude-0/-home-user-CMS/7a122d51-a5b1-5def-9637-d43cb9a9b6ef/scratchpad/figw')
from mathfig import Frame, SKY, PINK
from mjcommon import odot, fdot, plot, axes2, O, run, herm
OUT = sys.argv[1]
M = (16, 16, 16, 16)

from mathfig import DASH, dot, right_mark, GREEN, YELLOW
from mjcommon import arr


def ell(F, c, rx, ry, wd=2.0, dash='', fill='none', half=None):
    X, Y = F.P(*c); a, b = rx * F.sx, ry * F.sy
    if half is None:
        F.svg.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s" stroke="#000" stroke-width="%s" %s/>' % (X, Y, a, b, fill, wd, dash))
    else:   # half='front'(아래 반) / 'back'(위 반)
        sw = 0 if half == 'front' else 1
        F.svg.append('<path d="M %.1f %.1f A %.1f %.1f 0 0 %d %.1f %.1f" fill="none" stroke="#000" stroke-width="%s" %s/>' % (X - a, Y, a, b, sw, X + a, Y, wd, dash))


def i9():   # 12번 해설 y=g(x)
    g = lambda x: -7 * x if x < 0 else x ** 3 - 9 * x * x + 15 * x
    s = 0.1
    F = Frame((-1.0, 8.8), (-2.9, 1.6), 55, 55, M)
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, lambda x: g(x) * s, -0.2, 6.9, n=400)
    F.dashed((1, 0), (1, 0.7)); F.dashed((0, 0.7), (1, 0.7)); F.dashed((5, 0), (5, -2.5)); F.dashed((0, -2.5), (5, -2.5))
    F.lab((1, 0), '1', 'ct', 0, 8); F.lab((5, 0), '5', 'cb', 0, -8); F.lab((0, 0.7), '7', 'rc', -8, 0); F.lab((0, -2.5), '-25', 'rc', -8, 0)
    F.lab((6.3, g(6.3) * s), 'y=g(x)', 'lc', 8, 4)
    return F.render()


def i10():  # 13번 해설 y=f'(x)=4x^2(x-k)
    f = lambda x: 0.9 * x * x * (x - 1.5)
    F = Frame((-1.2, 2.6), (-0.9, 1.6), 80, 80, M)
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, f, -0.45, 1.95)
    F.lab((1.5, 0), 'k', 'rb', -6, -4); F.lab((1.95, f(1.95)), "y=f'(x)", 'rc', -12, 0)
    return F.render()


def i15():  # 20번 문제 레일 (A 5 m, B 25 m, AB 36 m)
    s = 0.1
    hx = math.sqrt(36 ** 2 - 20 ** 2) * s
    A, B = (0, 0.5), (hx, 2.5)
    F = Frame((-0.5, hx + 0.9), (-0.25, 2.9), 110, 110, M)
    F.poly([(-0.5, 0), (hx + 0.9, 0), (hx + 0.9, -0.2), (-0.5, -0.2)], YELLOW)
    F.seg((-0.5, 0), (hx + 0.9, 0), 2.0)
    F.poly([(-0.3, 0), (0, 0), (0, 0.5), (-0.3, 0.5)], SKY); F.seg((-0.3, 0.5), (0, 0.5), 2.0); F.seg((0, 0), (0, 0.5), 2.0)
    F.seg(A, B, 3.2); F.seg((hx, 0), B, 2.0)
    right_mark(F, (hx, 0), (0, 0), B, 0.12); right_mark(F, (0, 0), (0, 0.5), (1, 0), 0.1)
    F.pt(A, 'A', 'rb', -6, -4); F.pt(B, 'B', 'cb', 0, -8)
    F.lab((hx / 2 - 0.25, 1.5 + 0.25), '36~\\mathrm{m}', 'rb', -4, -4); F.lab((hx, 1.25), '25~\\mathrm{m}', 'lc', 8, 0); F.lab((0, 0.25), '5~\\mathrm{m}', 'lc', 8, 0)
    return F.render()


def i14():  # 20번 해설
    s = 0.1
    hx = math.sqrt(36 ** 2 - 20 ** 2) * s
    A, B, C, D = (0, 0.5), (hx, 2.5), (0, 0), (hx, 0)
    S = (hx, 0.5); u = 0.62; P = (hx * u, 0.5 + 2.0 * u); Q = (P[0], 0); R = (P[0], 0.5)
    F = Frame((-0.6, hx + 0.9), (-0.4, 2.8), 110, 110, M)
    F.polyline([A, B, D, C, A]); F.seg(A, S, 2.0); F.seg(P, Q, 2.0)
    for v, p, q in ((R, P, S), (S, B, A), (D, C, B), (Q, C, P)):
        right_mark(F, v, p, q, 0.1)
    for p, n, a, dx, dy in ((A, 'A', 'rb', -6, -4), (B, 'B', 'cb', 0, -8), (C, 'C', 'ct', 0, 8), (D, 'D', 'ct', 0, 8), (P, 'P', 'lb', 6, -4), (Q, 'Q', 'ct', 0, 8), (R, 'R', 'lt', 6, 4), (S, 'S', 'lb', 6, -4)):
        F.pt(p, n, a, dx, dy)
    F.lab((hx * 0.38, 0.5 + 2.0 * 0.38), '36~\\mathrm{m}', 'rb', -6, -6); F.lab((hx, 1.5), '20~\\mathrm{m}', 'lc', 8, 0)
    F.lab((0, 0.25), '5~\\mathrm{m}', 'rc', -8, 0); F.lab((hx, 0.25), '5~\\mathrm{m}', 'lc', 8, 0)
    return F.render()


def i16():  # 22번 해설 원기둥 r, h
    F = Frame((-1.5, 1.7), (-0.6, 2.7), 100, 100, M)
    rx, ry, H = 1.3, 0.35, 2.0
    F.poly([(-rx, 0), (-rx, H), (rx, H), (rx, 0)], YELLOW)
    ell(F, (0, H), rx, ry, fill=YELLOW); ell(F, (0, 0), rx, ry, half='front'); ell(F, (0, 0), rx, ry, dash=DASH, half='back')
    F.seg((-rx, 0), (-rx, H), 2.0); F.seg((rx, 0), (rx, H), 2.0)
    F.seg((0, 0), (rx * 0.85, -ry * 0.53), 2.0); dot(F, (0, 0))
    F.lab((rx * 0.45, -0.18), 'r', 'cb', 0, -4); F.lab((rx, H / 2), 'h', 'lc', 8, 0)
    return F.render()


def i18():  # 25번 해설 f(x)=x^3+3x^2-9x+1 (-1≤x≤2)
    f = lambda x: x ** 3 + 3 * x * x - 9 * x + 1
    s = 0.25
    F = Frame((-1.9, 3.0), (-1.6, 3.6), 60, 60, M)
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, lambda x: f(x) * s, -1, 2)
    for x in (-1, 1, 2):
        F.dashed((x, 0), (x, f(x) * s)); F.dashed((0, f(x) * s), (x, f(x) * s))
    F.lab((-1, 0), '-1', 'ct', -4, 8); F.lab((1, 0), '1', 'cb', 0, -8); F.lab((2, 0), '2', 'ct', 0, 8)
    F.lab((0, 12 * s), '12', 'lc', 8, 0); F.lab((0, 3 * s), '3', 'lb', 6, -4); F.lab((0, -4 * s), '-4', 'rc', -8, 0)
    F.lab((2, 3 * s), 'y=f(x)', 'lc', 8, 0)
    return F.render()


def i19():  # 26번 해설 f(x)=(x-1)^3-p^2(x-1) (p=1.6 개형)
    p = 1.6; f = lambda x: 0.45 * ((x - 1) ** 3 - p * p * (x - 1))
    F = Frame((-1.4, 3.7), (-1.9, 1.9), 70, 70, M)
    F.axes(); O(F, 'rb', -6, -4)
    plot(F, f, -1.05, 3.05)
    m1, m2 = 1 - p / math.sqrt(3), 1 + p / math.sqrt(3)
    F.dashed((m1, 0), (m1, f(m1))); F.dashed((m2, 0), (m2, f(m2)))
    F.lab((1 - p, 0), '1-p', 'rt', -2, 6); F.lab((1, 0), '1', 'lb', 4, -4); F.lab((1 + p, 0), '1+p', 'lb', 4, -4)
    F.lab((m1, 0), '1-\\dfrac{p}{\\sqrt{3}}', 'ct', 0, 8); F.lab((m2, 0), '1+\\dfrac{p}{\\sqrt{3}}', 'cb', 0, -8)
    F.lab((3.05, f(3.05)), 'y=f(x)', 'rc', -12, 0)
    return F.render()


def i22():  # 35번 문제 P(2t,0), Q(0,t), y=2x, R
    P, Q = (3, 0), (0, 1.5); R = (0.6, 1.2)
    F = Frame((-0.7, 4.0), (-0.9, 3.0), 75, 75, M)
    F.axes(); O(F, 'rt', -6, 4)
    F.seg((-0.4, -0.8), (1.45, 2.9), 2.0); F.seg(Q, P, 2.0)
    dot(F, P); dot(F, Q); dot(F, R)
    arr(F, (1.4, 0.25), (2.4, 0.25), 1.6, 9); arr(F, (-0.25, 0.4), (-0.25, 1.0), 1.6, 9)
    F.pt(P, 'P', 'ct', 0, 8); F.pt(Q, 'Q', 'rc', -8, 0); F.pt(R, 'R', 'lb', 6, -4); F.lab((1.45, 2.9), 'y=2x', 'lc', 6, 0)
    return F.render()


def cone(F, water=None, labels=False):
    R, H = 1.4, 2.6
    if water:
        r = R * water; h = H * water
        F.poly([(0, 0), (-r, h), (r, h)], SKY); ell(F, (0, h), r, r * 0.22, fill=SKY)
    ell(F, (0, H), R, R * 0.22, wd=2.4)
    F.seg((-R, H), (0, 0), 2.4); F.seg((R, H), (0, 0), 2.4)
    if labels:
        h = H * water; r = R * water
        F.seg((0, h), (r, h), 2.0); F.seg((0, 0), (0, h), 2.0, DASH)
        F.lab((r / 2, h), 'r~\\mathrm{cm}', 'cb', 0, -6); F.lab((0, h / 2), 'h~\\mathrm{cm}', 'rc', -8, 0)


def i24():  # 36번 문제 원뿔 그릇
    F = Frame((-1.6, 1.6), (-0.2, 3.0), 90, 90, M)
    cone(F, 0.32)
    return F.render()


def i23():  # 36번 해설
    F = Frame((-1.6, 1.6), (-0.2, 3.0), 90, 90, M)
    cone(F, 0.68, True)
    return F.render()


f41 = lambda x: x ** 4 - 2 * x * x


def i30():  # 41번 해설 f(x)=x^4-2x^2, y=1, y=-1
    F = Frame((-2.0, 2.5), (-1.5, 1.9), 75, 75, M)
    F.axes(); O(F, 'cb', 0, -6)
    plot(F, f41, -1.6, 1.6)
    F.seg((-1.9, 1), (1.9, 1), 2.0); F.seg((-1.9, -1), (1.9, -1), 2.0)
    F.dashed((-1, 0), (-1, -1)); F.dashed((1, 0), (1, -1))
    F.lab((-1, 0), '-1', 'cb', 0, -8); F.lab((1, 0), '1', 'cb', 0, -8); F.lab((0, 1), '1', 'lb', 6, -4); F.lab((0, -1), '-1', 'lt', 6, 4)
    F.lab((1.6, f41(1.6)), 'y=f(x)', 'lc', 6, 0); F.lab((1.9, 1), 'y=1', 'lc', 6, 0); F.lab((1.9, -1), 'y=-1', 'lc', 6, 0)
    return F.render()


def i32():  # 41번 해설 y=(g∘f)(x)=f(x)^2-1
    F = Frame((-2.0, 3.6), (-1.5, 1.9), 75, 75, M)
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, lambda x: f41(x) ** 2 - 1, -1.62, 1.62, n=500)
    F.lab((-1, 0), '-1', 'cb', 0, -8); F.lab((1, 0), '1', 'cb', 4, -8); F.lab((0, -1), '-1', 'lt', 6, 4)
    F.lab((1.62, f41(1.62) ** 2 - 1), 'y=(g\\circ f)(x)', 'lc', 6, 6)
    return F.render()


def i36():  # 46번 문제 원 위의 두 점
    F = Frame((-1.5, 1.5), (-1.4, 1.5), 90, 90, M)
    F.svg.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="#000" stroke-width="2.4"/>' % (F.P(0, 0) + (1.2 * F.sx,)))
    A = (0, 1.2); P = (1.2 * math.cos(2.3), 1.2 * math.sin(2.3)); Q = (-1.2, 0)
    for p in (A, P, Q): dot(F, p)
    F.pt(A, 'A', 'cb', 0, -8); F.pt(P, 'P', 'rb', -6, -2); F.pt(Q, 'Q', 'rc', -8, 0)
    arr(F, (1.05 * math.cos(2.55), 1.05 * math.sin(2.55)), (1.05 * math.cos(2.85), 1.05 * math.sin(2.85)), 1.6, 8)
    arr(F, (1.05 * math.cos(3.05), 1.05 * math.sin(3.05)), (1.05 * math.cos(3.35), 1.05 * math.sin(3.35)), 1.6, 8)
    return F.render()


def i37():  # 46번 해설 f(t)=t^3-2t^2-4t, 100의 배수
    f = lambda t: t ** 3 - 2 * t * t - 4 * t
    s = 0.005
    F = Frame((-1.0, 11.6), (-0.6, 4.2), 32, 60, M)
    F.axes('t'); O(F, 'rt', -6, 4)
    plot(F, lambda t: f(t) * s, 0, 10)
    for k in range(1, 8):
        y = 100 * k; F.dashed((0, y * s), (10, y * s)); F.lab((0, y * s), str(y), 'rc', -8, 0)
        r = bisect(lambda t: f(t) - y, 2, 10); dot(F, (r, y * s))
    r0 = bisect(lambda t: f(t), 2, 4); dot(F, (r0, 0))
    F.dashed((0, 760 * s), (10, 760 * s)); F.dashed((10, 0), (10, 760 * s)); odot(F, (10, 760 * s)); odot(F, (0, 0))
    F.lab((10, 760 * s), '760', 'lc', 10, 0); F.lab((10, 0), '10', 'ct', 0, 8)
    return F.render()


def bisect(h, a, b):
    for _ in range(60):
        m = (a + b) / 2
        if (h(a) > 0) == (h(m) > 0): a = m
        else: b = m
    return (a + b) / 2


def i38():  # 47번 문제 y=f(x)=-x(x-3t), A, B 삼등분점, C 꼭짓점 (t=1)
    f = lambda x: -x * (x - 3)
    F = Frame((-0.8, 5.2), (-1.4, 3.0), 75, 75, M)
    F.poly([(1, 0), (1.5, 2.25), (2, 0)], SKY)
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, f, -0.4, 3.4); F.polyline([(1, 0), (1.5, 2.25), (2, 0)], 'stroke-width="2"')
    dot(F, (3, 0))
    F.pt((1, 0), 'A', 'ct', 0, 8); F.pt((2, 0), 'B', 'ct', 0, 8); F.pt((1.5, 2.25), 'C', 'cb', 0, -8); F.pt((3, 0), 'P', 'lb', 6, -4)
    F.lab((3.4, f(3.4)), 'y=f(x)', 'lc', 6, 0)
    return F.render()


def abs49(c, line, hi, dv=9):
    f = lambda x: (x ** 3 - 6 * x * x + c) / dv
    F = Frame((-1.6, 7.0), (-4.4, 2.6), 55, 55, M)
    F.axes(); O(F, 'rt', -6, 4)
    lo = -1.2
    plot(F, lambda x: abs(f(x)), lo, hi, n=500)
    xs = [lo + (hi - lo) * i / 500 for i in range(501)]
    runs, cur = [], []
    for x in xs:
        if f(x) < 0: cur.append(x)
        elif cur: runs.append(cur); cur = []
    if cur: runs.append(cur)
    for r in runs:
        plot(F, f, r[0], r[-1], wd=2.0, dash=DASH)
    F.seg((-1.5, line / dv), (6.7, line / dv), 2.0)
    F.dashed((4, 0), (4, abs(f(4)))); F.lab((4, 0), '4', 'ct', 6, 8)
    return F, f


def i39():  # 49번 해설 f(0)f(4)≥0 이면 근이 많아야 4개 (f(0)<0 개형, c=-4)
    F, f = abs49(-4, 18.0, 6.3, 18)
    F.lab((2.0, abs(f(2.0))), 'y=|f(x)|', 'rb', -10, -4); F.lab((6.7, 1.0), 'y=k', 'rb', 0, -6); F.lab((4, f(4)), 'y=f(x)', 'ct', 0, 8)
    return F.render()


def i40():  # 49번 해설 |f(0)|=|f(4)|-2 (c=15)
    F, f = abs49(15, 15.0, 6.15)
    F.lab((2.2, 15 / 9), 'y=|f(4)|-2', 'cb', 0, -6)
    F.lab((6.15, abs(f(6.15))), 'y=|f(x)|', 'rc', -12, 0); F.lab((4, f(4)), 'y=f(x)', 'ct', 0, 8)
    return F.render()


f50 = lambda x: x ** 4 - 6 * x * x + 8 * x


def g50(F, k, s, lo=-3.25, hi=1.85):
    g = lambda x: f50(x) if f50(x) >= k else 2 * k - f50(x)
    plot(F, lambda x: g(x) * s, lo, hi, n=600)
    return g


def i41():  # 50번 해설 y=f(x)
    s = 0.07
    F = Frame((-3.6, 3.6), (-1.9, 2.6), 60, 60, M)
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, lambda x: f50(x) * s, -3.2, 1.8, n=400)
    F.dashed((-2, 0), (-2, -24 * s)); F.dashed((-2, -24 * s), (0, -24 * s)); F.dashed((1, 0), (1, 3 * s)); F.dashed((0, 3 * s), (1, 3 * s))
    F.lab((-2, 0), '-2', 'cb', 0, -8); F.lab((1, 0), '1', 'ct', 0, 8); F.lab((0, 3 * s), '3', 'rb', -6, -4); F.lab((0, -24 * s), '-24', 'lc', 8, 0)
    F.lab((1.8, f50(1.8) * s), 'y=f(x)', 'lc', 6, 0)
    return F.render()


def i42():  # 50번 해설 k=-12
    s = 0.07
    F = Frame((-3.6, 3.6), (-1.9, 2.6), 60, 60, M)
    F.axes(); O(F, 'rt', -6, 4)
    g = g50(F, -12, s, -3.2, 1.8)
    F.dashed((-2, 0), (-2, -12 * s)); F.dashed((-3.5, -12 * s), (0, -12 * s)); F.dashed((1, 0), (1, 3 * s)); F.dashed((0, 3 * s), (1, 3 * s))
    F.lab((-2, 0), '-2', 'cb', 0, -8); F.lab((1, 0), '1', 'ct', 0, 8); F.lab((0, 3 * s), '3', 'rb', -6, -4); F.lab((0, -12 * s), '-12', 'lc', 8, 0)
    F.lab((1.8, g(1.8) * s), 'y=g(x)', 'lc', 6, 0)
    return F.render()


def i43():  # 50번 해설 k=3
    s = 0.07
    F = Frame((-3.9, 3.6), (-0.9, 2.6), 60, 60, M)
    F.axes(); O(F, 'rt', -6, 4)
    g = g50(F, 3, s, -3.3, 1.8)
    F.dashed((-2, 0), (-2, 30 * s)); F.dashed((-2, 30 * s), (0, 30 * s)); F.dashed((-3, 0), (-3, 3 * s)); F.dashed((-3.6, 3 * s), (1.8, 3 * s))
    F.lab((-2, 0), '-2', 'ct', 0, 8); F.lab((-3, 0), '-3', 'ct', 0, 8); F.lab((1, 0), '1', 'ct', 0, 8); F.lab((0, 3 * s), '3', 'lb', 6, -4); F.lab((0, 30 * s), '30', 'lc', 8, 0)
    F.lab((1.8, g(1.8) * s), 'y=g(x)', 'lc', 6, 0)
    return F.render()


JOBS = {k: v for k, v in globals().items() if k[0] == 'i' and k[1:].isdigit()}
if __name__ == '__main__':
    run(JOBS, OUT, sys.argv[2:])
