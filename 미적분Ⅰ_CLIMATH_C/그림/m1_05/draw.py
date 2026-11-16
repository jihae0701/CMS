# -*- coding: utf-8 -*-
"""미적분Ⅰ 5. 도함수의 활용(2) — 스캔 그림 다시 그리기.  python3 draw.py 출력폴더 [이름...]"""
import sys, math
sys.path.insert(0, '/home/user/CMS/.claude/skills/math-figure-rules'); sys.path.insert(0, '..')
from mathfig import Frame, DASH, SKY, GREEN, dot, right_mark, dim_arc, roots, AX
from mjcommon import odot, fdot, plot, O, run, arr, axes2, herm
OUT = sys.argv[1]
M = (16, 16, 16, 16)
MS = (120, 30, 140, 40)
PINK, YEL = '#ffd9e6', '#fff3bf'
r3 = math.sqrt(3)


def xaxis_at(F, y0, x0, x1, name='x'):
    (a, y), (b, _) = F.P(x0, y0), F.P(x1, y0)
    F.svg.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#000" stroke-width="%s" marker-end="url(#ar)"/>' % (a, y, b, y, AX))
    F.labels.append((b + 0.3, y + 1.1, name, 22, 'rt'))


def callout(F, p, text, q, anc):
    """q 자리에 글자, q에서 p(곡선 위 점)로 가는 가는 화살표"""
    F.lab(q, text, anc)
    arr(F, q, p, 1.2, 7)


def sketch(F, f, x0, x1, yb, marks):
    """좌표축 없는 개형: marks=[(x, '아래 글자')]"""
    plot(F, f, x0, x1)
    for m in marks:
        x, t = m[0], m[1]
        F.dashed((x, f(x)), (x, yb)); F.lab((x, yb), t, m[2] if len(m) > 2 else 'ct', 0, 6)


# ── 1번: f'(x) 개형 (극소 x=±1, 극대 x=0)
fp1 = lambda x: 1.5 * ((x * x - 1) ** 2 - 0.6)


def i3():   # 1번 해설
    F = Frame((-2.3, 2.4), (-1.4, 2.5), 80, 80, M)
    F.axes(); O(F, 'lb', 4, -4)
    plot(F, fp1, -1.62, 1.62)
    for x in (-1, 1):
        F.dashed((x, 0), (x, fp1(x)))
    for x, t in ((-2, '-2'), (2, '2')):
        F.seg((x, 0), (x, 0.08), 1.5); F.lab((x, 0), t, 'ct', 0, 8)
    F.lab((-1, 0), '-1', 'cb', 0, -6); F.lab((1, 0), '1', 'cb', 0, -6)
    z = math.sqrt(1 + math.sqrt(0.6)); w = math.sqrt(1 - math.sqrt(0.6))
    for x, t in ((-z, 'a'), (-w, 'b'), (w, 'c'), (z, 'd')):
        F.lab((x, 0), t, 'ct', 6 if x > 0 else -6, 6)
    F.lab((1.62, fp1(1.62)), "y=f'(x)", 'rc', -12, 0)
    return F.render()


def i4():   # 1번 문제
    F = Frame((-2.3, 2.4), (-1.4, 2.5), 80, 80, M)
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, fp1, -1.62, 1.62)
    for x in (-1, 1):
        F.dashed((x, 0), (x, fp1(x)))
    for x, t in ((-2, '-2'), (2, '2')):
        F.seg((x, 0), (x, 0.08), 1.5); F.lab((x, 0), t, 'ct', 0, 8)
    F.lab((-1, 0), '-1', 'cb', 0, -6); F.lab((1, 0), '1', 'cb', 0, -6)
    F.lab((1.62, fp1(1.62)), "y=f'(x)", 'rc', -12, 0)
    return F.render()


def i5():   # 4번 해설: ⑴ f'=-x²+8x+a, ⑵ f'=3x²-2ax+3
    F = Frame((-2.3, 23.2), (-2.2, 5.6), 45, 45, (16, 16, 110, 16))
    g1 = lambda x: (-(x - 4) ** 2 + 27) / 5.5
    F.xaxis(-2.2, 6.6)
    plot(F, g1, -1, 3); plot(F, g1, -1.4, -1, 3.2, DASH); plot(F, g1, 3, 6.3, 3.2, DASH)
    odot(F, (-1, g1(-1))); odot(F, (3, g1(3)))
    F.dashed((-1, 0), (-1, g1(-1))); F.dashed((3, 0), (3, g1(3))); F.dashed((4, 0), (4, g1(4)))
    F.lab((-1, 0), '-1', 'ct', 4, 6); F.lab((3, 0), '3', 'ct', -6, 6); F.lab((4, 0), '4', 'ct', 6, 6)
    F.lab((6.3, g1(6.3)), "y=f'(x)", 'lt', 6, 4); F.lab((-2.2, 5.3), '(1)', 'lc')
    ox = 14.0
    g2 = lambda x: 2.0 * (((x - ox) / 2 - 1.5) ** 2 - 0.6)
    xaxis_at(F, 0, ox - 0.9, ox + 7.2)
    plot(F, g2, ox + 2, ox + 4); plot(F, g2, ox + 0.2, ox + 2, 3.2, DASH); plot(F, g2, ox + 4, ox + 5.8, 3.2, DASH)
    odot(F, (ox + 2, g2(ox + 2))); odot(F, (ox + 4, g2(ox + 4)))
    F.dashed((ox + 2, 0), (ox + 2, g2(ox + 2))); F.dashed((ox + 4, 0), (ox + 4, g2(ox + 4)))
    F.lab((ox + 2, 0), '1', 'cb', 0, -6); F.lab((ox + 4, 0), '2', 'cb', 0, -6)
    F.lab((ox + 5.8, g2(ox + 5.8)), "y=f'(x)", 'lc', 8, 0); F.lab((ox - 0.9, 5.3), '(2)', 'lc')
    return F.render()


def i6():   # 5번 해설 ⑴ x³+3x²-9x+4
    f = lambda x: (x ** 3 + 3 * x * x - 9 * x + 4) / 9
    F = Frame((-5.6, 3.2), (-2.0, 4.6), 45, 45, MS)
    sketch(F, f, -5.2, 2.75, -1.8, [(-3, 'x=-3'), (1, 'x=1')])
    callout(F, (-3, f(-3)), '\\text{극댓값 }31', (-1.8, 4.4), 'lc')
    callout(F, (1, f(1)), '\\text{극솟값 }-1', (1.9, -1.0), 'lc')
    return F.render()


def i7():   # 5번 해설 ⑵ -x³+3x²+5
    f = lambda x: (-x ** 3 + 3 * x * x + 5) / 2.2
    F = Frame((-2.3, 4.2), (0.0, 5.6), 60, 60, MS)
    sketch(F, f, -1.45, 3.75, 0.5, [(0, 'x=0'), (2, 'x=2')])
    callout(F, (0, f(0)), '\\text{극솟값 }5', (-1.3, 1.5), 'rc')
    callout(F, (2, f(2)), '\\text{극댓값 }9', (2.7, 5.3), 'lc')
    return F.render()


def i8():   # 6번 해설 ⑴ 3x⁴+4x³-12x²+5
    f = lambda x: (3 * x ** 4 + 4 * x ** 3 - 12 * x * x + 5) / 9
    F = Frame((-5.6, 3.6), (-4.5, 2.7), 70, 60, M)
    sketch(F, f, -2.95, 1.62, -4.1, [(-2, 'x=-2'), (0, 'x=0'), (1, 'x=1', 'lt')])
    callout(F, (-2, f(-2)), '\\text{극솟값 }-27', (-3.2, -2.0), 'rc')
    callout(F, (0, f(0)), '\\text{극댓값 }5', (-0.7, 2.2), 'rc')
    callout(F, (1, f(1)), '\\text{극솟값 }0', (1.8, -0.9), 'lc')
    return F.render()


def i9():   # 6번 해설 ⑵ x⁴-4x³+3
    f = lambda x: (x ** 4 - 4 * x ** 3 + 3) / 6
    F = Frame((-1.6, 5.0), (-5.6, 3.8), 60, 60, (40, 16, 160, 40))
    sketch(F, f, -1.25, 4.35, -5.2, [(0, 'x=0'), (3, 'x=3')])
    callout(F, (0, f(0)), '\\text{극값을 갖지 않음}', (0.4, 3.4), 'lc')
    callout(F, (3, f(3)), '\\text{극솟값 }-24', (3.8, -4.6), 'lc')
    return F.render()


def i10():  # 7번 문제 f'(x): a~g
    g = herm([(-3.6, -2.4, 5.0), (-3.0, 0, 3.5), (-2.3, 1.2, 0), (-1.4, 0, 0), (-0.5, 0.8, 1.6), (0.5, 1.5, 0),
              (1.3, 0, -2.6), (1.95, -1.0, 0), (2.6, 0, 2.6), (3.2, 1.9, 3.8)])
    F = Frame((-3.9, 3.9), (-2.2, 2.3), 60, 60, M)
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, g, -3.6, 3.2)
    for x in (-2.3, 0.5, 1.95):
        F.dashed((x, 0), (x, g(x)))
    for x, t, d in ((-3.0, 'a', 'rt'), (-2.3, 'b', 'ct'), (-1.4, 'c', 'ct'), (0.5, 'd', 'ct'), (1.3, 'e', 'rt'), (1.95, 'f', 'cb'), (2.6, 'g', 'lt')):
        F.lab((x, 0), t, d, -6 if d == 'rt' else (6 if d == 'lt' else 0), -6 if d == 'cb' else 6)
    F.lab((3.2, 1.9), "y=f'(x)", 'rc', -12, 0)
    return F.render()


def i12():  # 8번 해설 ⑴ x=1에서 극소
    f = lambda x: (x ** 3 + 3 * x * x - 9 * x + 3) / 9
    F = Frame((-5.2, 2.9), (-1.9, 3.8), 45, 45, (30, 16, 30, 40))
    sketch(F, f, -5.0, 2.6, -1.7, [(1, 'x=1')])
    return F.render()


def i13():  # 8번 해설 ⑵ x=1 극대, x=2 극소
    f = lambda x: (2 * x ** 3 - 9 * x * x + 12 * x) * 1.6
    F = Frame((0.0, 3.0), (6.0, 10.0), 110, 110, (30, 16, 30, 40))
    sketch(F, f, 0.25, 2.78, 6.3, [(1, 'x=1'), (2, 'x=2')])
    return F.render()


def i14():  # 9번 해설 ⑴ x=-1 극대, x=1 극소
    f = lambda x: (x ** 3 - 3 * x) / 1.2
    F = Frame((-2.1, 2.2), (-2.6, 2.3), 80, 80, (30, 16, 30, 40))
    sketch(F, f, -1.95, 2.0, -2.3, [(-1, 'x=-1'), (1, 'x=1')])
    return F.render()


def i15():  # 9번 해설 ⑵ x=0, 2 극대, x=1 극소
    f = lambda x: (-x ** 4 + 4 * x ** 3 - 4 * x * x) * 2.2
    F = Frame((-0.9, 2.9), (-3.4, 0.4), 110, 110, (30, 16, 30, 40))
    sketch(F, f, -0.45, 2.45, -3.1, [(0, 'x=0'), (1, 'x=1'), (2, 'x=2')])
    return F.render()


def i16():  # 10번 해설 x³-3x+5, [-3, 3]
    f = lambda x: x ** 3 - 3 * x + 5
    F = Frame((-3.9, 4.2), (-15.5, 26.0), 50, 6.5, (16, 16, 70, 16))
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, f, -3, 3); fdot(F, (-3, -13)); fdot(F, (3, 23))
    F.dashed((-3, 0), (-3, -13)); F.dashed((-3, -13), (0, -13)); F.dashed((3, 0), (3, 23)); F.dashed((0, 23), (3, 23))
    F.dashed((-1, 0), (-1, 7)); F.dashed((-1, 7), (0, 7)); F.dashed((1, 0), (1, 3)); F.dashed((0, 3), (1, 3))
    F.lab((-3, 0), '-3', 'cb', -6, -6); F.lab((-1, 0), '-1', 'ct', 0, 8); F.lab((1, 0), '1', 'ct', 0, 8); F.lab((3, 0), '3', 'ct', 0, 8)
    F.lab((0, 23), '23', 'rc', -8, 8); F.lab((0, 7), '7', 'lb', 6, -2); F.lab((0, 3), '3', 'lt', 6, 2); F.lab((0, -13), '-13', 'lc', 8, 0)
    F.lab((3, 23), 'y=f(x)', 'lc', 10, 0)
    return F.render()


def i17():  # 11번 해설 -x²(x-4)²+10
    f = lambda x: -(x * (x - 4)) ** 2 + 10
    F = Frame((-1.4, 5.6), (-8.0, 12.5), 70, 14, (16, 16, 90, 16))
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, f, -0.95, 4.95)
    F.dashed((0, 10), (4, 10)); F.dashed((4, 0), (4, 10)); F.dashed((2, 0), (2, -6)); F.dashed((0, -6), (2, -6))
    F.lab((2, 0), '2', 'cb', 0, -6); F.lab((4, 0), '4', 'ct', 8, 6); F.lab((0, 10), '10', 'rc', -8, 8); F.lab((0, -6), '-6', 'rc', -8, 0)
    F.lab((4.5, f(4.5) + 6), 'y=f(x)', 'lc', 6, 0)
    return F.render()


def i18():  # 16번 해설 t=x²-4x+2, [0, 4]
    f = lambda x: x * x - 4 * x + 2
    F = Frame((-0.9, 5.0), (-2.8, 4.3), 70, 70, M)
    F.axes('x', 't'); O(F, 'rt', -6, 4)
    plot(F, f, 0, 4); plot(F, f, -0.45, 0, 3.2, DASH); plot(F, f, 4, 4.45, 3.2, DASH)
    fdot(F, (0, 2)); fdot(F, (4, 2))
    F.dashed((0, 2), (4, 2)); F.dashed((4, 0), (4, 2)); F.dashed((2, 0), (2, -2)); F.dashed((0, -2), (2, -2))
    F.lab((2, 0), '2', 'cb', 0, -6); F.lab((4, 0), '4', 'ct', 8, 6); F.lab((0, 2), '2', 'rc', -8, 0); F.lab((0, -2), '-2', 'rc', -8, 0)
    F.lab((2.3, -2), 't=x^{2}-4x+2', 'lt', 6, 8)
    return F.render()


def i19():  # 17번 문제 y=x(x-6)², P, H
    f = lambda x: x * (x - 6) ** 2
    F = Frame((-0.8, 9.0), (-12.0, 46.0), 50, 6, (16, 16, 70, 16))
    P = (4, 16); H = (4, 0)
    F.poly([(0, 0), P, H], YEL)
    F.axes(); O(F, 'lt', 4, 6)
    plot(F, f, -0.4, 8.6)
    F.seg((0, 0), P, 2.0); F.seg(P, H, 2.0); right_mark(F, H, P, (0, 0), 0.5)
    fdot(F, P)
    F.pt(P, 'P', 'lb', 6, -4); F.pt(H, 'H', 'ct', 0, 8); F.pt((6, 0), 'A', 'ct', 0, 8)
    F.lab((8.6, f(8.6)), 'y=x(x-6)^{2}', 'rc', -12, 0)
    return F.render()


def i20():  # 23번 해설 f'=-3x²+4x+a, [1, 2]에서 ≥ 0
    f = lambda x: -1.6 * (x - 1.5) ** 2 + 2.0
    F = Frame((-0.6, 3.4), (-1.0, 2.4), 90, 90, (16, 16, 100, 16))
    F.xaxis(-0.5, 3.3)
    plot(F, f, 0.3, 2.7)
    F.dashed((1, 0), (1, f(1))); F.dashed((2, 0), (2, f(2)))
    F.lab((1, 0), '1', 'ct', 0, 6); F.lab((2, 0), '2', 'ct', 0, 6)
    F.lab((2.45, f(2.45)), "y=f'(x)", 'lc', 10, 0)
    return F.render()


def i21():  # 24번 해설 [그림 1] y=f(x), [그림 2] y=|f(x)|
    f = lambda x: 2 * x ** 3 - 3 * x * x - 12 * x
    S = 0.09
    F = Frame((-2.6, 10.6), (-24 * S - 0.9, 25 * S + 0.4), 55, 55, M)
    g = lambda x: f(x) * S
    axes2(F, 0, -2.5, 4.1, -24 * S, 24.5 * S); O(F, 'rt', -6, 4)
    plot(F, g, -2.15, 3.62)
    F.dashed((-1, 0), (-1, 7 * S)); F.dashed((-1, 7 * S), (0, 7 * S)); F.dashed((2, 0), (2, -20 * S)); F.dashed((0, -20 * S), (2, -20 * S))
    F.lab((-1, 0), '-1', 'ct', 0, 6); F.lab((2, 0), '2', 'cb', 0, -6); F.lab((0, 7 * S), '7', 'lb', 6, -2); F.lab((0, -20 * S), '-20', 'rc', -8, 0)
    F.lab((3.62, g(3.62)), 'y=f(x)', 'rc', -12, 0)
    F.lab((0.8, -24 * S), '[\\text{그림 1}]', 'ct', 0, 12)
    ox = 6.4
    axes2(F, ox, ox - 2.5, ox + 4.1, -24 * S, 24.5 * S); F.pt((ox, 0), 'O', 'rt', -6, 4)
    h = lambda x: abs(g(x - ox))
    plot(F, h, ox - 2.0, ox + 3.6)
    z1, z2 = (3 - math.sqrt(105)) / 4, (3 + math.sqrt(105)) / 4
    plot(F, lambda x: g(x - ox), ox - 2.15, ox + z1, 3.2, DASH); plot(F, lambda x: g(x - ox), ox, ox + z2, 3.2, DASH)
    F.dashed((ox - 1, 0), (ox - 1, 7 * S)); F.dashed((ox - 1, 7 * S), (ox, 7 * S)); F.dashed((ox + 2, -20 * S), (ox + 2, 20 * S))
    F.dashed((ox, 20 * S), (ox + 2, 20 * S)); F.dashed((ox, -20 * S), (ox + 2, -20 * S))
    for p in [(ox + z1, 0), (ox - 1, 7 * S), (ox, 0), (ox + 2, 20 * S), (ox + z2, 0)]:
        fdot(F, p)
    F.lab((ox - 1, 0), '-1', 'ct', 0, 6); F.lab((ox + 2, 0), '2', 'ct', 8, 6); F.lab((ox, 7 * S), '7', 'lb', 6, -2)
    F.lab((ox, 20 * S), '20', 'rc', -8, 0); F.lab((ox, -20 * S), '-20', 'rc', -8, 0)
    F.lab((ox + 2.3, 1.85), 'y=|f(x)|', 'lb', 6, -4)
    F.lab((ox + 0.8, -24 * S), '[\\text{그림 2}]', 'ct', 0, 12)
    return F.render()


def i22():  # 33번 해설 f'(0)>0, f'(1)<0
    f = lambda x: 1.3 * (x - 1.2) ** 2 - 0.65
    F = Frame((-0.6, 2.9), (-1.0, 2.3), 100, 100, M)
    F.xaxis(-0.5, 2.8)
    plot(F, f, -0.1, 2.45)
    F.dashed((0, 0), (0, f(0))); F.dashed((1, 0), (1, f(1)))
    a, b = 1.2 - math.sqrt(0.5), 1.2 + math.sqrt(0.5)
    F.lab((0, 0), '0', 'ct', 0, 6); F.lab((1, 0), '1', 'cb', 0, -6); F.lab((a, 0), '\\alpha', 'rt', -4, 6); F.lab((b, 0), '\\beta', 'lt', 4, 6)
    F.lab((2.45, f(2.45)), "y=f'(x)", 'rc', -12, 0)
    return F.render()


def i23(lab=True, col=SKY):  # 38번 해설 y=9-x², 사다리꼴 PQRS
    f = lambda x: 9 - x * x
    t = 1.6
    F = Frame((-4.2, 4.6), (-1.6, 11.6), 50, 30, (90, 16, 130, 16))
    F.poly([(-3, 0), (3, 0), (t, f(t)), (-t, f(t))], col)
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, f, -3.3, 3.3)
    F.polyline([(-3, 0), (-t, f(t)), (t, f(t)), (3, 0)], 'stroke-width="2.0"')
    F.lab((0, 9), '9', 'rb', -6, -4)
    F.pt((-3, 0), 'P', 'rb', -6, -4); F.pt((3, 0), 'Q', 'lb', 6, -4)
    if lab:
        F.lab((-3, 0), '-3', 'rt', -4, 6); F.lab((3, 0), '3', 'lt', 4, 6)
        F.pt((-t, f(t)), 'S', 'rb', -6, -2); F.lab((t, f(t)), '\\mathrm{R}(t,\\ 9-t^{2})', 'lb', 6, -2)
    F.lab((-2.4, f(-2.4)), 'y=9-x^{2}', 'rc', -10, 0)
    return F.render()


def i24():  # 38번 문제
    return i23(False, GREEN)


def tri39(F, a, body=None, corner=PINK, labels=True):
    """한 변 24인 정삼각형에서 꼭짓점 주위 사각형을 잘라 냄(꼭짓점에서 a만큼)"""
    A, B, C = (0, 0), (24, 0), (12, 12 * r3)
    V = [A, B, C]
    def mv(p, q, d):
        L = math.hypot(q[0] - p[0], q[1] - p[1]); return (p[0] + (q[0] - p[0]) * d / L, p[1] + (q[1] - p[1]) * d / L)
    G = (12, 4 * r3)
    inner = [mv(v, G, a / math.cos(math.pi / 6)) for v in V]
    if body:
        F.poly(V, body)
    for i, v in enumerate(V):
        p1, p2 = mv(v, V[(i + 1) % 3], a), mv(v, V[(i + 2) % 3], a)
        F.poly([v, p1, inner[i], p2], corner)
        F.seg(p1, inner[i], 2.0); F.seg(p2, inner[i], 2.0)
        right_mark(F, p1, v, inner[i], 0.9); right_mark(F, p2, v, inner[i], 0.9)
    F.polyline(V + [A], 'stroke-width="2.0"'.replace('3.2', '2'))
    F.polyline(inner + [inner[0]], DASH + ' stroke-width="1.5"')
    if labels:
        dim_arc(F, A, C, '24', -1)
    return mv(A, B, a)


def i25():  # 39번 해설
    F = Frame((-3.0, 25.0), (-3.0, 22.0), 16, 16, M)
    p = tri39(F, 3.0)
    dim_arc(F, (0, 0), p, 'x', 1, 10)
    return F.render()


def i27():  # 39번 문제
    F = Frame((-3.0, 25.0), (-1.0, 22.0), 16, 16, M)
    tri39(F, 3.0, YEL, '#e6e6e6')
    return F.render()


def i26():  # 39번 해설: 꼭짓점 부분
    x = 4.0; h = x / r3
    V, P1, Q, P2 = (0, 0), (x, 0), (x, h), (x / 2, x * r3 / 2)
    F = Frame((-0.6, 5.6), (-1.4, 3.9), 70, 70, M)
    F.poly([V, P1, Q, P2], '#e6e6e6')
    F.seg(V, P2, 2.0); F.seg(P2, Q, 2.0); F.seg(V, Q, 1.5)
    F.seg(V, P1, 3.2); F.seg(P1, Q, 3.2)
    right_mark(F, P1, V, Q, 0.3)
    def ang(c, a1, a2, rad):
        X, Y = F.P(*c); s, e = a1, a2
        x1, y1 = X + rad * math.cos(s), Y - rad * math.sin(s); x2, y2 = X + rad * math.cos(e), Y - rad * math.sin(e)
        F.svg.append('<path d="M%.1f,%.1f A%.1f,%.1f 0 0 0 %.1f,%.1f" fill="none" stroke="#000" stroke-width="1.2"/>' % (x1, y1, rad, rad, x2, y2))
    ang(V, 0, math.pi / 6, 40); ang(Q, math.pi + math.pi / 6, 3 * math.pi / 2, 26)
    F.lab((1.5, 0.35), '30^{\\circ}', 'lc', 10, 0); F.lab((x, h), '60^{\\circ}', 'rt', -12, 12)
    dim_arc(F, V, P1, 'x', 1); dim_arc(F, P1, Q, 'h', 1)
    return F.render()


def i28():  # 40번 해설 [그림 1], [그림 2]
    F = Frame((-1.0, 47.0), (-7.0, 21.5), 9, 9, M)
    for ox, k in ((0, 1), (25, 2)):
        A, B, C = (ox, 0), (ox + 20, 0), (ox + 10, 20)
        x, y = 5.0, 10.0
        F.polyline([A, B, C, A], 'stroke-width="2.0"')
        F.seg((ox + 10, 0), C, 2.0)
        F.polyline([(ox + 10 - x, 0), (ox + 10 - x, y), (ox + 10 + x, y), (ox + 10 + x, 0)])
        if k == 1:
            dim_arc(F, (ox + 10, 0), (ox + 10, y), 'y', -1, 14); dim_arc(F, (ox + 10, 0), (ox + 10 + x, 0), 'x', 1, 10)
        else:
            dim_arc(F, (ox + 10, y), C, '20-y', 1, 14); dim_arc(F, (ox + 10, y), (ox + 10 + x, y), 'x', 1, 10)
            dim_arc(F, (ox + 10, 0), C, '20', -1, 44); dim_arc(F, (ox + 10, 0), B, '10', 1, 12)
        F.lab((ox + 10, -3.5), '[\\text{그림 %d}]' % k, 'ct')
    return F.render()


def i29():  # 40번 문제: 원뿔에 내접한 원기둥
    F = Frame((-11.5, 15.0), (-6.0, 21.0), 14, 14, M)
    R, H, r, h = 10, 20, 5, 10
    ry = 2.4
    def ell(cx, cy, a, b, half, dash=False, fill=None):
        X, Y = F.P(cx, cy); A, Bv = a * F.sx, b * F.sy
        if half == 'full':
            F.svg.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s" stroke="#000" stroke-width="1.5" %s/>' % (X, Y, A, Bv, fill or 'none', DASH if dash else ''))
        else:
            sweep = 0 if half == 'front' else 1
            F.svg.append('<path d="M%.1f,%.1f A%.1f,%.1f 0 0 %d %.1f,%.1f" fill="none" stroke="#000" stroke-width="%s" %s/>' % (X - A, Y, A, Bv, sweep, X + A, Y, 2.0 if not dash else 1.5, DASH if dash else ''))
    # 원뿔 몸통
    X0, Y0 = F.P(-R, 0); X1, Y1 = F.P(R, 0); XA, YA = F.P(0, H); Bv = ry * F.sy; A = R * F.sx
    F.svg.append('<path d="M%.1f,%.1f L%.1f,%.1f L%.1f,%.1f A%.1f,%.1f 0 0 1 %.1f,%.1f z" fill="%s" stroke="none"/>' % (XA, YA, X1, Y1, X0 + 2 * A, Y0, A, Bv, X0, Y0, YEL))
    F.svg.append('<path d="M%.1f,%.1f L%.1f,%.1f L%.1f,%.1f z" fill="%s" stroke="none"/>' % (XA, YA, X0, Y0, X1, Y1, YEL))
    # 원기둥
    x0, yb = F.P(-r, 0); x1, _ = F.P(r, 0); _, yt = F.P(0, h); b2 = ry * r / R * F.sy; a2 = r * F.sx
    F.svg.append('<path d="M%.1f,%.1f L%.1f,%.1f A%.1f,%.1f 0 0 0 %.1f,%.1f L%.1f,%.1f A%.1f,%.1f 0 0 1 %.1f,%.1f z" fill="#ffe08a" stroke="none"/>'
                 % (x0, yt, x0, yb, a2, b2, x1, yb, x1, yt, a2, b2, x0, yt))
    ell(0, 0, R, ry, 'back', True); ell(0, 0, R, ry, 'front')
    F.seg((0, H), (-R, 0), 2.0); F.seg((0, H), (R, 0), 2.0)
    ell(0, 0, r, ry * r / R, 'back', True); ell(0, 0, r, ry * r / R, 'front', True)
    ell(0, h, r, ry * r / R, 'full', True)
    F.dashed((-r, 0), (-r, h)); F.dashed((r, 0), (r, h))
    F.seg((0, 0), (0, H), 1.5); F.seg((0, 0), (-R, 0), 1.5)
    right_mark(F, (0, 0), (0, 1), (-1, 0), 0.9)
    dim_arc(F, (0, 0), (0, H), '20\\,\\mathrm{cm}', 1, 30)
    dim_arc(F, (-R, 0), (0, 0), '10\\,\\mathrm{cm}', 1, 34)
    return F.render()


def i30():  # 41번 문제 f'(x)
    g = herm([(-2.9, -1.0, 0.3), (-2, -0.75, 0.45), (-1, 0, 1.0), (0, 1.2, 1.1), (1, 1.75, 0), (2, 0, -2.2), (3, -1.0, 0),
              (4, 0, 2.2), (5, 1.95, 0.9), (6.0, 2.6, 0.4)])
    F = Frame((-3.1, 6.6), (-1.6, 3.0), 60, 60, M)
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, g, -2.9, 6.0)
    for x in (-2, 1, 3, 5):
        F.dashed((x, 0), (x, g(x)))
    F.lab((-2, 0), '-2', 'cb', 0, -6); F.lab((-1, 0), '-1', 'rt', -2, 6); F.lab((1, 0), '1', 'ct', 0, 6); F.lab((2, 0), '2', 'rt', -4, 6)
    F.lab((3, 0), '3', 'cb', 0, -6); F.lab((4, 0), '4', 'lt', 4, 6); F.lab((5, 0), '5', 'ct', 0, 6)
    F.lab((6.0, 2.6), "y=f'(x)", 'rb', -6, -10)
    return F.render()


def i31():  # 44번 해설 x=-1 극대, x=1 극소
    return i14()


def i32():  # 47번 해설 f'(x), 0<α<1<β<2
    f = lambda x: 1.3 * (x - 1) ** 2 - 0.8
    F = Frame((-0.6, 2.9), (-1.2, 2.2), 100, 100, M)
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, f, -0.1, 2.12)
    F.dashed((1, 0), (1, f(1))); F.dashed((2, 0), (2, f(2)))
    a, b = 1 - math.sqrt(0.8 / 1.3), 1 + math.sqrt(0.8 / 1.3)
    F.lab((1, 0), '1', 'cb', 0, -6); F.lab((2, 0), '2', 'lt', 4, 6); F.lab((a, 0), '\\alpha', 'lt', 4, 6); F.lab((b, 0), '\\beta', 'rt', -4, 6)
    F.lab((2.12, f(2.12)), "y=f'(x)", 'rc', -12, 0)
    return F.render()


def box50(F, x=6.0, y=4.0, shade=True):
    s2 = math.sqrt(2); S = 10 * s2; c = S / 2; r = x / s2
    T, R_, B, L = (c, c + r), (c + r, c), (c, c - r), (c - r, c)
    flaps = []
    for p, q, n in ((T, R_, (1, 1)), (R_, B, (1, -1)), (B, L, (-1, -1)), (L, T, (-1, 1))):
        nx, ny = n[0] * y / s2, n[1] * y / s2
        flaps.append([p, q, (q[0] + nx, q[1] + ny), (p[0] + nx, p[1] + ny)])
    if shade:
        F.poly([(0, 0), (S, 0), (S, S), (0, S)], GREEN)
        F.poly([T, R_, B, L], '#fff')
        for fl in flaps:
            F.poly(fl, '#fff')
    for fl in flaps:
        F.polyline([fl[0], fl[3], fl[2], fl[1]], 'stroke-width="2.0"'.replace('2.0', '2'))
    F.polyline([T, R_, B, L, T], DASH + ' stroke-width="1.5"')
    F.polyline([(0, 0), (S, 0), (S, S), (0, S), (0, 0)], 'stroke-width="4"')
    dim_arc(F, (0, 0), (S, 0), '10\\sqrt{2}', 1)
    return S, c, r, L


def i33():  # 50번 문제
    F = Frame((-0.6, 14.8), (-3.4, 14.8), 30, 30, M)
    box50(F)
    return F.render()


def i34():  # 50번 해설
    F = Frame((-4.0, 14.8), (-3.4, 14.8), 30, 30, M)
    S, c, r, L = box50(F, shade=False)
    y = 4.0; s2 = math.sqrt(2)
    p1, p2 = (0, c + y / s2), (0, c - y / s2)
    dim_arc(F, (0, S), p1, '\\dfrac{x}{\\sqrt{2}}', 1)
    dim_arc(F, p1, p2, '\\sqrt{2}y', 1)
    dim_arc(F, p1, (c - y / s2, S), 'x', 1)
    dim_arc(F, p2, L, 'y', 1, 10)
    return F.render()


JOBS = {k: v for k, v in globals().items() if k[0] == 'i' and k[1:].isdigit()}
if __name__ == '__main__':
    run(JOBS, OUT, sys.argv[2:], wide=('i21', 'i28'))
