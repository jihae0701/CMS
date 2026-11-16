# -*- coding: utf-8 -*-
"""미적분Ⅰ 1. 함수의 극한 — 스캔 그림 다시 그리기 (image2~11, 13~20)
    python3 draw.py 출력폴더 [이름...]"""
import sys, math
sys.path.insert(0, '/home/user/CMS/.claude/skills/math-figure-rules')
from mathfig import Frame, fit_shoot, dot, DASH, SKY
OUT = sys.argv[1]
PINK = '#fbe0d8'
YEL = '#fbefc2'


def odot(F, p):
    X, Y = F.P(*p)
    F.svg.append('<circle cx="%.1f" cy="%.1f" r="5" fill="#fff" stroke="#000" stroke-width="2"/>' % (X, Y))


def fdot(F, p):
    dot(F, p, 4.5)


def plot(F, f, a, b, wd=3.2, dash='', n=160):
    P = ["%.1f,%.1f" % F.P(a + (b - a) * i / n, f(a + (b - a) * i / n)) for i in range(n + 1)]
    F.svg.append('<polyline points="%s" fill="none" stroke="#000" stroke-width="%s" stroke-linejoin="round" %s/>' % (" ".join(P), wd, dash))


def arr(F, p, q, wd=1.6, head=7):
    """작은 화살표(다가가는 방향 표시)"""
    (x1, y1), (x2, y2) = F.P(*p), F.P(*q)
    d = math.hypot(x2 - x1, y2 - y1); ux, uy = (x2 - x1) / d, (y2 - y1) / d
    bx, by = x2 - ux * head, y2 - uy * head
    F.svg.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#000" stroke-width="%s"/>' % (x1, y1, bx, by, wd))
    F.svg.append('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="#000"/>' % (x2, y2, bx + uy * head * 0.45, by - ux * head * 0.45, bx - uy * head * 0.45, by + ux * head * 0.45))


def along(F, f, x0, x1, off):
    """곡선 y=f(x) 옆(화면에서 off px 떨어진 곳)에 x0→x1 방향 화살표"""
    (a, b), (c, d) = F.P(x0, f(x0)), F.P(x1, f(x1))
    L = math.hypot(c - a, d - b); nx, ny = -(d - b) / L, (c - a) / L
    p = F.inv(a + nx * off, b + ny * off); q = F.inv(c + nx * off, d + ny * off)
    arr(F, p, q)


def _inv(self, X, Y):
    x0, y0 = self.P(0, 0); x1, _ = self.P(1, 0); _, y1 = self.P(0, 1)
    return ((X - x0) / (x1 - x0), (Y - y0) / (y1 - y0))


Frame.inv = _inv


def axes2(F, ox, x0, x1, y0, y1):
    """F.axes()와 같은 모양의 축을 원점 (ox, 0)에 그린다(그래프 두 개를 나란히 그릴 때). x, y 글자 자리도 axes()와 같게"""
    from mathfig import AX
    (a, y), (b, _) = F.P(x0, 0), F.P(x1, 0)
    F.svg.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#000" stroke-width="%s" marker-end="url(#ar)"/>' % (a, y, b, y, AX))
    F.labels.append((b + 0.3, y + 1.1, 'x', 22, 'rt'))
    (X, yb), (_, yt) = F.P(ox, y0), F.P(ox, y1)
    F.svg.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#000" stroke-width="%s" marker-end="url(#ar)"/>' % (X, yb, X, yt, AX))
    F.labels.append((X - 10, yt + 3.7, 'y', 22, 'rc'))


def O(F, anc='rt', dx=-6, dy=4):
    F.pt((0, 0), 'O', anc, dx, dy)


# ── 2번 해설 ─────────────────────────────
def g2a():   # y=(x^2-9)/(x-3)=x+3, x≠3
    F = Frame((-4.6, 5.2), (-1.4, 8.2), 40, 40, (16, 16, 16, 16))
    F.axes(); O(F, 'lt', 4, 4)
    f = lambda x: x + 3
    plot(F, f, -4.2, 4.6); odot(F, (3, 6))
    F.dashed((3, 6), (3, 0)); F.dashed((3, 6), (0, 6))
    F.lab((-3, 0), '-3', 'rt', -2, 4); F.lab((3, 0), '3', 'ct', 0, 8)
    F.lab((0, 6), '6', 'rc', -8, 0); F.lab((0, 3), '3', 'rc', -8, 0)
    along(F, f, 1.6, 2.6, 14); along(F, f, 4.4, 3.4, -14)
    arr(F, (1.9, -0.55), (2.7, -0.55)); arr(F, (4.1, -0.55), (3.3, -0.55))
    F.lab((3.6, f(3.6)), 'y=f(x)', 'rc', -12, -6)
    return F.render()


def g2b():   # y=√(2x+1)
    F = Frame((-1.4, 4.0), (-0.9, 3.2), 70, 70, (16, 16, 16, 16))
    F.axes(); O(F, 'lt', 4, 4)
    f = lambda x: math.sqrt(max(2 * x + 1, 0))
    plot(F, f, -0.5, 3.6)
    F.dashed((2, f(2)), (2, 0)); F.dashed((2, f(2)), (0, f(2)))
    F.lab((-0.5, 0), '-\\frac{1}{2}', 'ct', 0, 8); F.lab((2, 0), '2', 'ct', 0, 8)
    F.lab((0, 1), '1', 'rc', -8, 0); F.lab((0, f(2)), '\\sqrt{5}', 'rc', -8, 0)
    along(F, f, 1.2, 1.8, -14); along(F, f, 3.0, 2.3, 14)
    arr(F, (1.2, -0.3), (1.8, -0.3)); arr(F, (2.8, -0.3), (2.2, -0.3))
    F.lab((3.6, f(3.6)), 'y=f(x)', 'rb', 0, -8)
    return F.render()


def g2c():   # y=1/(x-1)^2+3
    F = Frame((-1.4, 3.6), (-0.8, 6.6), 60, 60, (16, 16, 16, 16))
    F.axes(); O(F, 'rt', -6, 4)
    f = lambda x: 1 / (x - 1) ** 2 + 3
    plot(F, f, -1.2, 1 - 1 / math.sqrt(3.3)); plot(F, f, 1 + 1 / math.sqrt(3.3), 3.4)
    F.dashed((1, -0.6), (1, 6.4)); F.dashed((-1.3, 3), (3.5, 3))
    F.lab((1, 0), '1', 'lt', 4, 4); F.lab((0, 3), '3', 'rb', -6, -2); F.lab((0, 4), '4', 'rc', -8, 0)
    fdot(F, (0, 4)) if False else None
    arr(F, (0.25, -0.35), (0.8, -0.35)); arr(F, (1.75, -0.35), (1.2, -0.35))
    arr(F, (0.42, 5.3), (0.5, 6.2)); arr(F, (1.58, 5.3), (1.5, 6.2))
    F.lab((2.2, f(2.2)), 'y=f(x)', 'lb', 4, -6)
    return F.render()


# ── 3번 해설 ─────────────────────────────
def g3a():   # y=x^2+3x-2
    F = Frame((-4.8, 3.0), (-5.2, 4.6), 50, 50, (16, 16, 16, 16))
    F.axes(); O(F, 'rt', -6, 4)
    f = lambda x: x * x + 3 * x - 2
    plot(F, f, -4.55, 1.45)
    F.dashed((-1.5, f(-1.5)), (-1.5, 0)); F.dashed((-1.5, f(-1.5)), (0, f(-1.5)))
    F.lab((-1.5, 0), '-\\frac{3}{2}', 'cb', 0, -6); F.lab((0, -2), '-2', 'lc', 6, 0); F.lab((0, f(-1.5)), '-\\frac{17}{4}', 'lc', 6, 0)
    along(F, f, 1.05, 1.35, -14)
    F.lab((-1.6, 3.4), 'y=f(x)', 'cc')
    return F.render()


def g3b():   # y=√(2x-1)
    F = Frame((-0.6, 5.0), (-0.8, 3.4), 60, 60, (16, 16, 16, 16))
    F.axes(); O(F, 'rt', -6, 4)
    f = lambda x: math.sqrt(max(2 * x - 1, 0))
    plot(F, f, 0.5, 4.7)
    F.lab((0.5, 0), '\\frac{1}{2}', 'ct', 0, 8)
    arr(F, (3.4, -0.35), (4.3, -0.35)); along(F, f, 3.6, 4.4, 14)
    F.lab((3.2, f(3.2)), 'y=f(x)', 'rb', 0, -12)
    return F.render()


def g3c():   # y=1/x^2-1
    F = Frame((-3.8, 3.8), (-1.9, 3.6), 55, 55, (16, 16, 16, 16))
    F.axes(); O(F, 'rt', -6, 4)
    f = lambda x: 1 / (x * x) - 1
    plot(F, f, -3.6, -1 / math.sqrt(4.3)); plot(F, f, 1 / math.sqrt(4.3), 3.6)
    F.dashed((-3.7, -1), (3.7, -1))
    F.lab((-1, 0), '-1', 'cb', 0, -6); F.lab((1, 0), '1', 'cb', 0, -6); F.lab((0, -1), '-1', 'lt', 6, 4)
    arr(F, (-2.4, 0.3), (-3.4, 0.3)); along(F, f, -2.6, -3.4, -14)
    F.lab((0.7, f(0.7)), 'y=f(x)', 'lc', 12, 0)
    return F.render()


# ── 4번 문제 ─────────────────────────────
def g4():
    F = Frame((-3.6, 4.6), (-1.8, 2.8), 60, 60, (16, 16, 16, 16))
    F.axes(); O(F, 'rt', -6, 4)
    F.seg((-3.2, 2.2), (-2, 1), 3.2)
    F.polyline([(-2, 0), (-1, -1), (0, -1)], 'stroke-width="3.2"')
    F.seg((0, 0), (1, 2), 3.2); F.seg((1, 2), (2, 1), 3.2); F.seg((2, 1), (3.3, 1), 3.2)
    F.dashed((-2, 1), (2, 1)); F.dashed((-1, -1), (-1, 0)); F.dashed((1, 2), (1, 0)); F.dashed((1, 2), (0, 2)); F.dashed((2, 1), (2, 0))
    for p in [(-2, 1), (0, 0), (1, 1), (2, 0)]:
        fdot(F, p)
    for p in [(-2, 0), (0, -1), (1, 2), (2, 1)]:
        odot(F, p)
    F.lab((-2, 0), '-2', 'ct', 0, 10); F.lab((-1, 0), '-1', 'cb', 0, -6); F.lab((1, 0), '1', 'ct', 0, 8); F.lab((2, 0), '2', 'ct', 0, 10)
    F.lab((0, 1), '1', 'rc', -8, 0); F.lab((0, 2), '2', 'rc', -8, 0); F.lab((0, -1), '-1', 'lc', 10, 0)
    F.lab((2.4, 1.6), 'y=f(x)', 'lc', 0, 0)
    return F.render()


# ── 5번 문제(두 그래프) ───────────────────
def g5():
    F = Frame((-2.8, 9.4), (-2.0, 2.9), 60, 60, (16, 16, 16, 16))
    # y=f(x)
    axes2(F, 0, -2.7, 2.7, -1.9, 2.8); O(F, 'rb', -6, -4)
    F.seg((-2.5, 1.5), (-1, 0), 3.2); F.seg((-1, -1), (0, 0), 3.2); F.seg((0, 0), (1, -1), 3.2); F.seg((1, 0), (2.5, 1.5), 3.2)
    F.dashed((-2, 0), (-2, 1)); F.dashed((-2, 1), (2, 1)); F.dashed((2, 1), (2, 0))
    F.dashed((-1, 0), (-1, -1)); F.dashed((-1, -1), (1, -1)); F.dashed((1, -1), (1, 0))
    fdot(F, (0, 1)); fdot(F, (-1, -1)); fdot(F, (1, -1))
    odot(F, (-1, 0)); odot(F, (0, 0)); odot(F, (1, 0))
    F.lab((-2, 0), '-2', 'ct', 0, 8); F.lab((-1, 0), '-1', 'ct', -6, 8); F.lab((1, 0), '1', 'ct', 6, 8); F.lab((2, 0), '2', 'ct', 0, 8)
    F.lab((0, 1), '1', 'rb', -6, -4); F.lab((0, -1), '-1', 'rt', -6, 10)
    F.lab((1.3, 1.9), 'y=f(x)', 'lc', 0, 0)
    # y=g(x)  (원점을 (5.6, 0)으로 옮겨 그림)
    ox = 5.6
    axes2(F, ox, ox - 2.2, ox + 2.5, -1.9, 2.8); F.pt((ox, 0), 'O', 'rt', -6, 4)
    F.seg((ox - 2.1, 1), (ox + 1, 1), 3.2); F.seg((ox + 1, -1), (ox + 2.0, -2.0), 3.2)
    F.dashed((ox + 1, 1), (ox + 1, -1)); F.dashed((ox + 1, -1), (ox, -1))
    fdot(F, (ox + 1, 1)); odot(F, (ox + 1, -1))
    F.lab((ox + 1, 0), '1', 'lt', 6, 4); F.lab((ox, 1), '1', 'rb', -6, -4); F.lab((ox, -1), '-1', 'rc', -8, 0)
    F.lab((ox + 1.2, 1.7), 'y=g(x)', 'lc', 0, 0)
    return F.render()


# ── 6번 문제 ─────────────────────────────
def g6():
    F = Frame((-2.8, 2.0), (-1.6, 3.8), 70, 70, (16, 16, 16, 16))
    F.axes(); O(F, 'lt', 4, 4)
    plot(F, lambda x: 2 - 2 * (x + 2) ** 2, -2, -1)
    plot(F, lambda x: -(x) ** 2, -1, 0)
    F.seg((0, 1), (1, 3), 3.2)
    F.dashed((-2, 2), (-2, 0)); F.dashed((-2, 2), (1, 2)); F.dashed((1, 3), (1, 0)); F.dashed((1, 3), (0, 3))
    F.dashed((-1, 1), (0, 1)); F.dashed((-1, 1), (-1, -1)); F.dashed((-1, -1), (0, -1))
    for p in [(-2, 2), (-1, 1), (0, 1), (1, 2)]:
        fdot(F, p)
    for p in [(-1, 0), (-1, -1), (0, 0), (1, 3)]:
        odot(F, p)
    F.lab((-2, 0), '-2', 'ct', 0, 8); F.lab((-1, 0), '-1', 'rt', -4, 8); F.lab((1, 0), '1', 'ct', 0, 8)
    F.lab((0, 1), '1', 'rb', -6, -2); F.lab((0, 2), '2', 'rb', -6, -2); F.lab((0, 3), '3', 'rc', -8, 0); F.lab((0, -1), '-1', 'lc', 8, 0)
    F.lab((0.4, 3.5), 'y=f(x)', 'lc', 0, 0)
    return F.render()


# ── 8번 문제 ─────────────────────────────
def g8():
    A, B, C, D, E = 1.0, 2.0, 3.0, 4.0, 6.0
    F = Frame((-0.6, 7.0), (-0.6, 3.9), 55, 55, (16, 16, 16, 16))
    F.axes(); O(F, 'rt', -6, 4)
    F.seg((A, 0.9), (B, 1.6), 3.2)
    p3 = lambda t: (1 - t) ** 3 * 1.0 + 3 * (1 - t) ** 2 * t * 0.0 + 3 * (1 - t) * t * t * 0.9 + t ** 3 * 2.2
    pts = []
    for i in range(61):
        t = i / 60
        x = (1 - t) ** 3 * B + 3 * (1 - t) ** 2 * t * (B + 0.55) + 3 * (1 - t) * t * t * (C - 0.25) + t ** 3 * C
        pts.append((x, p3(t)))
    F.polyline(pts, 'stroke-width="3.2"')
    F.seg((C, 2.2), (D, 1.9), 3.2)
    q = [((1 - t) ** 2 * D + 2 * (1 - t) * t * (D + 0.4) + t * t * E, (1 - t) ** 2 * 1.0 + 2 * (1 - t) * t * 3.6 + t * t * 3.4) for t in [i / 60 for i in range(61)]]
    F.polyline(q, 'stroke-width="3.2"')
    F.dashed((0, 2.9), (D, 2.9))
    for x, y in [(A, 0.9), (B, 1.0), (C, 2.2), (D, 1.0), (E, 3.4)]:
        F.dashed((x, y), (x, 0))
    F.dashed((C, 2.9), (C, 2.2)); F.dashed((D, 2.9), (D, 1.9))
    for p in [(A, 0.9), (B, 1.6), (C, 2.9), (D, 2.9)]:
        fdot(F, p)
    for p in [(B, 1.0), (C, 2.2), (D, 1.9), (D, 1.0), (E, 3.4)]:
        odot(F, p)
    for x, n in [(A, 'a'), (B, 'b'), (C, 'c'), (D, 'd'), (E, 'e')]:
        F.lab((x, 0), n, 'ct', 0, 8)
    F.lab((E, 3.4), 'y=f(x)', 'rb', -6, -10)
    return F.render()


# ── 9번 해설 ─────────────────────────────
def g9a():   # y=(x-1)/|x-1|
    F = Frame((-1.4, 3.4), (-1.8, 2.0), 60, 60, (16, 16, 16, 16))
    F.axes(); O(F, 'rt', -6, 4)
    F.seg((-1.2, -1), (1, -1), 3.2); F.seg((1, 1), (3.0, 1), 3.2)
    F.dashed((1, 1), (1, -1)); F.dashed((1, 1), (0, 1))
    odot(F, (1, -1)); odot(F, (1, 1))
    F.lab((1, 0), '1', 'lt', 6, 4); F.lab((0, 1), '1', 'rc', -8, 0); F.lab((0, -1), '-1', 'rt', -6, 6)
    arr(F, (0.35, -0.75), (0.8, -0.75)); arr(F, (1.75, 1.3), (1.25, 1.3))
    arr(F, (0.35, -0.3), (0.8, -0.3)); arr(F, (1.75, 0.3), (1.25, 0.3))
    F.lab((1.6, 1.65), 'y=\\frac{x-1}{|x-1|}', 'lc', 0, 0)
    return F.render()


def g9b():   # y=[2x+1]
    F = Frame((-0.7, 2.6), (-0.7, 3.9), 80, 80, (16, 16, 16, 16))
    F.axes(); O(F, 'rt', -6, 4)
    for k, (a, b) in enumerate([(0, 0.5), (0.5, 1), (1, 1.5)]):
        y = k + 1
        F.seg((a, y), (b, y), 3.2); fdot(F, (a, y)); odot(F, (b, y))
        F.dashed((b, y), (b, 0)); F.dashed((a, y), (0, y)) if a > 0 else None
    F.dashed((1.5, 3), (0, 3))
    F.svg.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#000" stroke-width="2" stroke-dasharray="1,5" stroke-linecap="round"/>' % (F.P(1.6, 3.2) + F.P(1.85, 3.6)))
    F.svg.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#000" stroke-width="2" stroke-dasharray="1,5" stroke-linecap="round"/>' % (F.P(-0.1, 0.8) + F.P(-0.35, 0.4)))
    F.lab((0.5, 0), '\\frac{1}{2}', 'ct', 0, 8); F.lab((1, 0), '1', 'ct', 0, 8); F.lab((1.5, 0), '\\frac{3}{2}', 'ct', 0, 8)
    F.lab((0, 1), '1', 'rb', -6, -4); F.lab((0, 2), '2', 'rc', -8, 0); F.lab((0, 3), '3', 'rc', -8, 0)
    arr(F, (0.6, 0.18), (0.92, 0.18)); arr(F, (1.4, 0.18), (1.08, 0.18))
    arr(F, (0.6, 1.7), (0.92, 1.7)); arr(F, (1.4, 2.7), (1.08, 2.7))
    F.lab((0.25, 3.6), 'y=[2x+1]', 'lc', 0, 0)
    return F.render()


# ── 30번 문제(두 그래프) ──────────────────
def g30():
    F = Frame((-1.0, 15.2), (-1.4, 6.4), 42, 42, (16, 16, 16, 16))
    axes2(F, 0, -0.9, 5.0, -1.3, 6.3); O(F, 'rt', -6, 4)
    F.seg((-0.85, 0), (0, 0), 3.2); F.seg((0, 3), (3, 3), 3.2); F.seg((3, 5), (4.9, 5), 3.2)
    F.dashed((3, 5), (3, 0)); F.dashed((3, 5), (0, 5))
    fdot(F, (0, 3)); fdot(F, (3, 5)); odot(F, (0, 0)); odot(F, (3, 3))
    F.lab((3, 0), '3', 'ct', 0, 8); F.lab((0, 3), '3', 'rc', -8, 0); F.lab((0, 5), '5', 'rc', -8, 0)
    F.lab((3.2, 5.6), 'y=f(x)', 'lc', 0, 0)
    ox = 9.0
    axes2(F, ox, ox - 3.6, ox + 5.6, -1.3, 6.3); F.pt((ox, 0), 'O', 'rt', -6, 4)
    g = lambda t: 3 - t * t / 3
    plot(F, lambda x: g(x - ox), ox - 3.4, ox + 3)
    plot(F, lambda x: 1.7 * math.sqrt(max(x - ox - 3, 0)), ox + 3, ox + 5.2)
    F.dashed((ox, 3), (ox + 3, 3)); F.dashed((ox + 3, 3), (ox + 3, 0))
    odot(F, (ox, 3)); fdot(F, (ox, 1)); fdot(F, (ox + 3, 3)); odot(F, (ox + 3, 0))
    F.lab((ox + 3, 0), '3', 'ct', 0, 10); F.lab((ox, 3), '3', 'rb', -6, -4); F.lab((ox, 1), '1', 'rc', -8, 0)
    F.lab((ox + 2.6, 4.4), 'y=g(x)', 'lc', 0, 0)
    return F.render()


# ── 31번 문제 ────────────────────────────
def g31():
    F = Frame((-0.5, 4.8), (-0.6, 3.8), 70, 70, (16, 16, 16, 16))
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, lambda x: 1 + 2 * (1 - x) ** 2, 0, 1)
    X = [1, 1.25, 1.8, 2]; Y = [1, 0.82, 2.15, 2]
    def lag(x):
        s = 0
        for i in range(4):
            t = Y[i]
            for j in range(4):
                if j != i:
                    t *= (x - X[j]) / (X[i] - X[j])
            s += t
        return s
    plot(F, lag, 1, 2)
    F.seg((2, 3), (3, 3), 3.2)
    plot(F, lambda x: 1 + (x - 3) ** 2, 3, 4)
    F.dashed((0, 3), (2, 3)); F.dashed((0, 2), (4, 2)); F.dashed((0, 1), (3, 1))
    for x in (1, 2, 3, 4):
        F.dashed((x, 0), (x, 3 if x in (2, 3) else (1 if x == 1 else 2)))
    for p in [(0, 3), (1, 0), (2, 1), (3, 2), (4, 2)]:
        fdot(F, p)
    for p in [(1, 1), (2, 2), (2, 3), (3, 3), (3, 1)]:
        odot(F, p)
    for x in (1, 2, 3, 4):
        F.lab((x, 0), str(x), 'ct', 0, 10)
    for y in (1, 2, 3):
        F.lab((0, y), str(y), 'rc', -8, 0)
    F.lab((1.2, 3.45), 'y=f(x)', 'lc', 0, 0)
    return F.render()


# ── 32번 문제 ────────────────────────────
def g32f():
    F = Frame((-2.4, 2.4), (-1.9, 2.1), 70, 70, (16, 16, 16, 16))
    F.axes(); O(F, 'rt', -6, 4)
    F.seg((-2.2, -1.2), (0, 1), 3.2); F.seg((0, -1), (2.2, 1.2), 3.2)
    fdot(F, (0, 0)); odot(F, (0, 1)); odot(F, (0, -1))
    F.lab((-1, 0), '-1', 'rt', -6, 4); F.lab((1, 0), '1', 'lb', 6, -4); F.lab((0, 1), '1', 'lc', 8, 0); F.lab((0, -1), '-1', 'rc', -8, 0)
    F.lab((0.5, 1.75), 'y=f(x)', 'lc', 0, 0)
    return F.render()


def g32g():
    F = Frame((-2.0, 2.0), (-0.7, 2.6), 80, 80, (16, 16, 16, 16))
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, lambda x: x * x, -1.55, 1.55)
    F.dashed((-1, 1), (1, 1)); F.dashed((-1, 1), (-1, 0)); F.dashed((1, 1), (1, 0))
    F.lab((-1, 0), '-1', 'ct', 0, 8); F.lab((1, 0), '1', 'ct', 0, 8); F.lab((0, 1), '1', 'rb', -6, -4)
    F.lab((1.55, 2.4), 'y=g(x)', 'rc', -10, 0)
    return F.render()


# ── 52번 문제(두 그래프) ──────────────────
def g52():
    F = Frame((-2.3, 8.4), (-1.7, 2.4), 60, 60, (16, 16, 16, 16))
    axes2(F, 0, -2.2, 2.4, -1.6, 2.3); O(F, 'rt', -6, 4)
    F.seg((-2.0, 1.0), (-1, 0), 3.2); F.seg((1, 0), (2.0, 1.0), 3.2)
    plot(F, lambda x: 0.3 - 1.3 * x * x, -1, 1)
    F.dashed((-1, 0), (-1, -1)); F.dashed((-1, -1), (1, -1)); F.dashed((1, -1), (1, 0))
    fdot(F, (-1, 0)); fdot(F, (1, 0)); odot(F, (-1, -1)); odot(F, (1, -1))
    F.lab((-1, 0), '-1', 'rb', -4, -4); F.lab((1, 0), '1', 'lb', 4, -4); F.lab((0, -1), '-1', 'rt', -4, 6)
    F.lab((0.9, 1.45), 'y=f(x)', 'lc', 0, 0)
    ox = 5.0
    axes2(F, ox, ox - 2.2, ox + 2.1, -1.6, 2.3); F.pt((ox, 0), 'O', 'lt', 4, 4)
    F.seg((ox - 2.0, 1), (ox - 1, 1), 3.2); F.seg((ox - 1, -1), (ox + 1, 1), 3.2); F.seg((ox + 1, 1), (ox + 2.0, 1), 3.2)
    F.dashed((ox - 1, 1), (ox - 1, -1)); F.dashed((ox - 1, 1), (ox, 1)); F.dashed((ox + 1, 1), (ox + 1, 0)); F.dashed((ox, 1), (ox + 1, 1)); F.dashed((ox - 1, -1), (ox, -1))
    fdot(F, (ox - 1, 1)); odot(F, (ox - 1, -1))
    F.lab((ox - 1, 0), '-1', 'rt', -4, 4); F.lab((ox + 1, 0), '1', 'ct', 0, 8); F.lab((ox, 1), '1', 'lb', 6, -4); F.lab((ox, -1), '-1', 'lc', 8, 0)
    F.lab((ox + 0.8, 1.5), 'y=g(x)', 'lc', 0, 0)
    return F.render()


# ── 59번 문제 ────────────────────────────
def g59():
    F = Frame((-1.8, 2.2), (-0.6, 4.6), 80, 80, (16, 16, 16, 16))
    x0 = 1.35
    P, Q, R = (x0, x0 * x0), (1, 0), (0, 3)
    F.poly([(0, 0), R, P], YEL); F.poly([(0, 0), P, Q], PINK)
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, lambda x: x * x, -1.75, 2.08)
    F.seg((0, 0), P, 2.0); F.seg(R, P, 2.0); F.seg(P, Q, 2.0)
    fdot(F, P)
    F.pt(P, 'P', 'lc', 8, 0); F.pt(Q, 'Q', 'ct', 0, 8); F.pt(R, 'R', 'rc', -8, 0)
    F.lab((0.45, 1.62), 'B(x)', 'cc')
    F.leader((1.6, 0.45), (0.85, 0.55)); F.lab((1.6, 0.45), 'A(x)', 'lc', 4, 0)
    F.lab((1.98, 3.9), 'y=x^{2}', 'rc', -10, 0)
    return F.render()


JOBS = {'2a': g2a, '2b': g2b, '2c': g2c, '3a': g3a, '3b': g3b, '3c': g3c, '4': g4, '5': g5, '6': g6, '8': g8,
        '9a': g9a, '9b': g9b, '30': g30, '31': g31, '32f': g32f, '32g': g32g, '52': g52, '59': g59}
if __name__ == '__main__':
    names = sys.argv[2:] or list(JOBS)
    for k in names:
        print(k, fit_shoot(OUT + '/m1_%s.png' % k, JOBS[k]))
