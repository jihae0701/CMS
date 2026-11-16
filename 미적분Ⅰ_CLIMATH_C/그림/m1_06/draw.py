# -*- coding: utf-8 -*-
"""미적분Ⅰ 6. 도함수의 활용(3) — 스캔 그림 다시 그리기.  python3 draw.py 출력폴더 [이름...]"""
import sys, math
sys.path.insert(0, '/home/user/CMS/.claude/skills/math-figure-rules'); sys.path.insert(0, '..')
from mathfig import Frame, DASH, SKY, AX, roots
from mjcommon import odot, fdot, plot, O, run, arr, axes2, herm
OUT = sys.argv[1]
M = (16, 16, 16, 16)


def hline(F, y, x0, x1, lab=None, anc='lc', dx=8, dy=0):
    F.seg((x0, y), (x1, y), 2.0)
    if lab:
        F.lab((x1, y), lab, anc, dx, dy)


def callout(F, p, text, q, anc):
    F.lab(q, text, anc); arr(F, q, p, 1.2, 7)


def i3():   # 1번 해설 ⑴ x³-3x²+2
    f = lambda x: x ** 3 - 3 * x * x + 2
    F = Frame((-1.4, 3.4), (-2.9, 3.0), 80, 60, M)
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, f, -0.88, 2.95)
    F.dashed((2, 0), (2, -2)); F.dashed((0, -2), (2, -2))
    F.lab((2, 0), '2', 'cb', 0, -6); F.lab((0, 2), '2', 'rb', -6, -4); F.lab((0, -2), '-2', 'rc', -8, 0)
    F.lab((2.95, f(2.95)), 'y=f(x)', 'rc', -12, 0)
    return F.render()


def i4():   # 1번 해설 ⑵ x⁴-6x²-8x+13
    f = lambda x: x ** 4 - 6 * x * x - 8 * x + 13
    F = Frame((-2.3, 3.4), (-14, 27), 80, 9, M)
    F.axes(); O(F, 'lt', 4, 4)
    plot(F, f, -2.05, 2.95)
    F.dashed((-1, 0), (-1, 16)); F.dashed((-1, 16), (0, 16)); F.dashed((2, 0), (2, -11)); F.dashed((0, -11), (2, -11))
    F.lab((-1, 0), '-1', 'ct', 0, 6); F.lab((2, 0), '2', 'cb', 0, -6); F.lab((0, 16), '16', 'lb', 6, -4); F.lab((0, -11), '-11', 'rc', -8, 0)
    callout(F, (0, 13), '13', (0.9, 11.0), 'lc')
    F.lab((2.95, f(2.95)), 'y=f(x)', 'rc', -12, 0)
    return F.render()


def i5():   # 3번 해설 ⑴ x³-6x²+9x+4
    f = lambda x: x ** 3 - 6 * x * x + 9 * x + 4
    F = Frame((-0.9, 4.6), (-1.5, 10.5), 70, 30, M)
    F.axes(); O(F, 'lt', 4, 4)
    plot(F, f, -0.4, 4.25)
    F.dashed((1, 0), (1, 8)); F.dashed((0, 8), (1, 8)); F.dashed((3, 0), (3, 4)); F.dashed((0, 4), (3, 4))
    F.lab((1, 0), '1', 'ct', 0, 6); F.lab((3, 0), '3', 'ct', 0, 6); F.lab((0, 8), '8', 'rc', -8, 0); F.lab((0, 4), '4', 'rc', -8, 6)
    F.lab((4.25, f(4.25)), 'y=f(x)', 'rc', -12, 0)
    return F.render()


def i6():   # 3번 해설 ⑵ 2x⁴-4x²+1
    f = lambda x: 2 * x ** 4 - 4 * x * x + 1
    F = Frame((-2.0, 2.1), (-1.8, 2.8), 90, 70, M)
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, f, -1.6, 1.6)
    F.dashed((-1, 0), (-1, -1)); F.dashed((1, 0), (1, -1)); F.dashed((-1, -1), (1, -1))
    F.lab((-1, 0), '-1', 'cb', 0, -6); F.lab((1, 0), '1', 'cb', 0, -6); F.lab((0, 1), '1', 'lb', 6, -4); F.lab((0, -1), '-1', 'rt', -6, 6)
    F.lab((1.6, f(1.6)), 'y=f(x)', 'rc', -12, 0)
    return F.render()


def i7():   # 4번 해설 2x³-9x²+12x, y=k
    f = lambda x: 2 * x ** 3 - 9 * x * x + 12 * x
    F = Frame((-0.7, 3.5), (-1.3, 7.5), 90, 40, (16, 16, 70, 16))
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, f, -0.12, 2.75)
    hline(F, 4.5, -0.6, 3.3, 'y=k', 'lc', 8, 0)
    F.dashed((1, 0), (1, 5)); F.dashed((0, 5), (1, 5)); F.dashed((2, 0), (2, 4)); F.dashed((0, 4), (2, 4))
    F.lab((1, 0), '1', 'ct', 0, 6); F.lab((2, 0), '2', 'ct', 0, 6); F.lab((0, 5), '5', 'rb', -6, -2); F.lab((0, 4), '4', 'rt', -6, 2)
    F.lab((2.75, f(2.75)), 'y=f(x)', 'rc', -12, 0)
    return F.render()


def i8():   # 6번 해설 (두 그림)
    g = lambda x: (3 * x ** 4 + 8 * x ** 3 - 6 * x * x - 24 * x) / 7
    F = Frame((-3.0, 6.6), (-3.0, 2.4), 70, 70, (16, 16, 110, 16))
    f1 = lambda x: (g(x) * 7 - 8) / 7 / 1.6
    F.xaxis(-3.0, 1.75)
    plot(F, f1, -2.75, 1.5)
    for x in (-1, 1):
        F.dashed((x, 0), (x, f1(x)))
    F.lab((-2, 0), '-2', 'ct', 0, 6); F.lab((-1, 0), '-1', 'ct', 8, 6); F.lab((1, 0), '1', 'cb', 0, -6)
    F.lab((-2.75, f1(-2.75)), 'y=f(x)', 'lc', 10, 0)
    o = 4.7
    f2 = lambda x: (g(x - o) * 7 - 13) / 7 / 1.6
    F.xaxis(o - 3.0, o + 1.75)
    plot(F, f2, o - 2.62, o + 1.55)
    for x in (-2, 1):
        F.dashed((o + x, 0), (o + x, f2(o + x)))
    F.lab((o - 2, 0), '-2', 'cb', 0, -6); F.lab((o - 1, 0), '-1', 'cb', 0, -8); F.lab((o + 1, 0), '1', 'cb', 0, -6)
    F.lab((o + 1.55, f2(o + 1.55)), 'y=f(x)', 'lc', 8, 0)
    return F.render()


def i9():   # 7번 해설 3x⁴-4x³-12x²+5, y=k
    f = lambda x: 3 * x ** 4 - 4 * x ** 3 - 12 * x * x + 5
    F = Frame((-1.9, 3.3), (-29, 13), 80, 7, (16, 16, 70, 16))
    F.axes(); O(F, 'lt', 6, 6)
    e0 = roots(lambda x: f(x) - 12, -2, -1, 0)[0]; e1 = roots(lambda x: f(x) - 12, 2, 3.5, 0)[0]
    plot(F, f, e0, e1)
    hline(F, 2.5, -1.8, 3.0, 'y=k', 'lc', 8, 0)
    F.dashed((2, 0), (2, -27)); F.dashed((0, -27), (2, -27))
    F.lab((2, 0), '2', 'cb', -6, -6); F.lab((0, 5), '5', 'lb', 6, -2); F.lab((0, -27), '-27', 'rc', -8, 0)
    callout(F, (-1, 0), '-1', (-1.7, -4.5), 'rc')
    F.lab((e1, 12), 'y=f(x)', 'rc', -12, 0)
    return F.render()


def i10():  # 8번 해설 x³-3x²-9x, y=p
    f = lambda x: x ** 3 - 3 * x * x - 9 * x
    F = Frame((-2.4, 5.4), (-30, 12), 60, 7, (16, 16, 70, 16))
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, f, -2.1, 5.05)
    hline(F, -6, -2.3, 4.8, 'y=p', 'lc', 8, 0)
    F.dashed((-1, 0), (-1, 5)); F.dashed((-1, 5), (0, 5)); F.dashed((3, 0), (3, -27)); F.dashed((0, -27), (3, -27))
    F.lab((-1, 0), '-1', 'ct', 0, 6); F.lab((3, 0), '3', 'lt', 4, 6); F.lab((0, 5), '5', 'lc', 8, 0); F.lab((0, -27), '-27', 'rc', -8, 0)
    F.lab((5.05, f(5.05)), 'y=f(x)', 'rc', -12, 0)
    return F.render()


def i11():  # 14번 문제 x=f(t)
    f = lambda t: t * (t - 2.2) * (t - 4.4) / 2.2
    F = Frame((-0.7, 5.3), (-2.4, 2.9), 70, 70, M)
    F.axes('t', 'x'); O(F, 'rt', -6, 4)
    e1 = roots(lambda t: f(t) - 2.6, 4.4, 6, 0)[0]
    plot(F, f, 0, e1)
    a = 2.2 - 2.2 / math.sqrt(3); c = 2.2 + 2.2 / math.sqrt(3)
    F.dashed((a, 0), (a, f(a))); F.dashed((c, 0), (c, f(c)))
    F.lab((a, 0), 'a', 'ct', 0, 6); F.lab((2.2, 0), 'b', 'lb', 6, -4); F.lab((c, 0), 'c', 'cb', 0, -6); F.lab((4.4, 0), 'd', 'rt', -6, 6)
    F.lab((e1, 2.6), 'x=f(t)', 'rc', -12, 0)
    return F.render()


def i13():  # 17번 문제 v(t)
    F = Frame((-3, 33), (-7.5, 7.8), 14, 18, M)
    F.axes('t', 'v(t)'); O(F, 'rt', -6, 4)
    F.polyline([(0, 0), (5, 5), (10, 5), (20, -5), (30, 5)])
    F.dashed((0, 5), (30, 5)); F.dashed((5, 0), (5, 5)); F.dashed((10, 0), (10, 5)); F.dashed((30, 0), (30, 5))
    F.dashed((20, 0), (20, -5)); F.dashed((0, -5), (20, -5))
    for x in (5, 10, 15, 25, 30):
        F.lab((x, 0), str(x), 'ct', 0, 6)
    F.lab((20, 0), '20', 'cb', 0, -6); F.lab((0, 5), '5', 'rc', -8, 0); F.lab((0, -5), '-5', 'rc', -8, 0)
    return F.render()


def i14():  # 18번 해설 y=h(x) 개형: 극대 x=-2, 극소 x=1
    f = lambda x: (2 * x ** 3 + 3 * x * x - 12 * x) / 6
    F = Frame((-3.6, 2.6), (-2.0, 4.0), 70, 60, M)
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, f, -3.25, 2.2)
    F.dashed((-2, 0), (-2, f(-2))); F.dashed((1, 0), (1, f(1)))
    F.lab((-2, 0), '-2', 'ct', 0, 6); F.lab((1, 0), '1', 'cb', 0, -6)
    F.lab((2.2, f(2.2)), 'y=h(x)', 'rc', -12, 0)
    return F.render()


def i15():  # 26번 해설 v=3t²-6t-4, [0, 3]
    f = lambda t: 3 * t * t - 6 * t - 4
    F = Frame((-1.4, 4.0), (-8.5, 7.5), 80, 22, M)
    F.axes('t', 'v'); O(F, 'rt', -6, 4)
    plot(F, f, 0, 3); plot(F, f, -0.75, 0, 3.2, DASH); plot(F, f, 3, 3.23, 3.2, DASH)
    fdot(F, (0, -4)); fdot(F, (3, 5))
    F.dashed((1, 0), (1, -7)); F.dashed((0, -7), (1, -7)); F.dashed((3, 0), (3, 5)); F.dashed((0, 5), (3, 5))
    F.lab((1, 0), '1', 'cb', 0, -6); F.lab((3, 0), '3', 'ct', 8, 6); F.lab((0, 5), '5', 'rc', -8, 0); F.lab((0, -4), '-4', 'rc', -8, 0); F.lab((0, -7), '-7', 'rc', -8, 0)
    F.lab((1.6, -7), 'v=3t^{2}-6t-4', 'lt', 4, 8)
    return F.render()


def i17():  # 31번 해설 f(x) 개형: 극소 x=-1, 5 / 극대 x=3, 네 실근
    f = herm([(-2.15, 2.3, -6), (-1, -1.7, 0), (1.0, 0.0, 1.5), (3, 1.4, 0), (5, -0.8, 0), (6.0, 2.2, 6)])
    F = Frame((-2.6, 6.8), (-2.2, 2.9), 60, 60, M)
    F.xaxis(-2.6, 6.7)
    plot(F, f, -2.15, 6.0)
    for x in (-1, 3, 5):
        F.dashed((x, 0), (x, f(x)))
    F.lab((-1, 0), '-1', 'cb', 0, -6); F.lab((3, 0), '3', 'ct', 0, 6); F.lab((5, 0), '5', 'cb', 0, -6)
    F.lab((6.0, 2.2), 'y=f(x)', 'rc', -12, 0)
    return F.render()


def i18():  # 31번 문제 f'(x)
    fp = lambda x: (x + 1) * (x - 3) * (x - 5) / 12
    F = Frame((-2.0, 6.4), (-2.0, 2.4), 60, 60, M)
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, fp, -1.75, 5.7)
    p = (7 - math.sqrt(13)) / 3; q = (7 + math.sqrt(13)) / 3
    F.dashed((p, 0), (p, fp(p))); F.dashed((q, 0), (q, fp(q)))
    F.lab((-1, 0), '-1', 'cb', -6, -6); F.lab((p, 0), 'p', 'ct', 0, 6); F.lab((3, 0), '3', 'ct', 0, 6)
    F.lab((q, 0), 'q', 'cb', 0, -6); F.lab((5, 0), '5', 'ct', 8, 6)
    F.lab((5.7, fp(5.7)), "y=f'(x)", 'rc', -12, 0)
    return F.render()


def table(cols, rows, widths, rh=42):
    """증감표: cols[0]은 머리 칸. rows=[[칸 글자…], …]"""
    W = sum(widths); H = rh * len(rows)
    F = Frame((0, W), (0, H), 1, 1, (6, 6, 6, 6))
    F.poly([(0, 0), (widths[0], 0), (widths[0], H), (0, H)], SKY)
    xs = [0]
    for w in widths:
        xs.append(xs[-1] + w)
    for i in range(1, len(rows)):
        F.seg((0, H - i * rh), (W, H - i * rh), 1.0)
    for x in xs[1:-1]:
        F.seg((x, 0), (x, H), 1.0)
    F.seg((0, H), (W, H), 2.4); F.seg((0, 0), (W, 0), 2.4)
    for r, row in enumerate(rows):
        for c, t in enumerate(row):
            if t:
                F.lab(((xs[c] + xs[c + 1]) / 2, H - (r + 0.5) * rh), t, 'cc')
    return F.render()


UP, DN = '\\nearrow', '\\searrow'


def i19():  # 32번 해설
    return table(0, [['x', '\\cdots', '-\\sqrt{a}', '\\cdots', '\\sqrt{a}', '\\cdots'],
                     ["f'(x)", '+', '0', '-', '0', '+'],
                     ['f(x)', UP, '4a\\sqrt{a}+4', DN, '-4a\\sqrt{a}+4', UP]], [80, 64, 130, 64, 140, 64])


def i20():  # 34번 해설
    return table(0, [['x', '\\cdots', '-3', '\\cdots', '-1', '\\cdots', '1', '\\cdots'],
                     ["f'(x)", '-', '0', '+', '0', '-', '0', '+'],
                     ['f(x)', DN, '-9', UP, '7', DN, '-9', UP]], [80] + [62] * 7)


def i23():  # 36번 해설
    return table(0, [['x', '-1', '\\cdots', '-\\dfrac{1}{2}', '\\cdots', '1', '\\cdots', '2'],
                     ["h'(x)", '', '+', '0', '-', '0', '+', ''],
                     ['h(x)', 'a-1', UP, 'a+\\dfrac{7}{4}', DN, 'a-5', UP, 'a+8']], [80, 76, 56, 86, 56, 76, 56, 76], 64)


def i24():  # 37번 해설
    return table(0, [['x', '0', '\\cdots', '\\dfrac{a}{6}', '\\cdots'],
                     ["f'(x)", '', '-', '0', '+'],
                     ['f(x)', '', DN, '\\text{극소}', UP]], [80, 90, 90, 90, 90], 64)


def i21():  # 34번 해설 x⁴+4x³-2x²-12x, y=k-3
    f = lambda x: (x ** 4 + 4 * x ** 3 - 2 * x * x - 12 * x)
    F = Frame((-4.0, 2.6), (-11, 10.5), 60, 11, (16, 16, 110, 16))
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, f, -3.85, 1.88)
    hline(F, 4.0, -3.95, 2.3, 'y=k-3', 'lc', 8, 0)
    F.dashed((-3, 0), (-3, -9)); F.dashed((1, 0), (1, -9)); F.dashed((-3, -9), (1, -9)); F.dashed((-1, 0), (-1, 7)); F.dashed((-1, 7), (0, 7))
    F.lab((-3, 0), '-3', 'cb', 0, -6); F.lab((-1, 0), '-1', 'rt', -4, 6); F.lab((1, 0), '1', 'cb', 0, -6)
    F.lab((0, 7), '7', 'lc', 8, 0); F.lab((0, -9), '-9', 'rt', -6, 6)
    F.lab((1.88, f(1.88)), 'y=f(x)', 'lc', 8, 0)
    return F.render()


def i22():  # 35번 해설: x=1에서 x축에 접함
    f = lambda x: (x - 1) ** 2 * ((x - 1) ** 2 + 2) / 2
    F = Frame((-0.9, 2.9), (-0.6, 3.2), 90, 90, M)
    F.xaxis(-0.8, 2.8)
    plot(F, f, -0.45, 2.45)
    F.lab((1, 0), '1', 'ct', 0, 6)
    F.lab((2.45, f(2.45)), 'y=f(x)', 'rc', -12, 0)
    return F.render()


def i25():  # 39번 해설 v=3t²-6t-5, [0, 3] 개형
    f = lambda t: (3 * t * t - 6 * t - 5) / 3
    F = Frame((-2.6, 4.4), (-4.4, 2.0), 80, 80, M)
    plot(F, f, 0, 3); fdot(F, (0, f(0))); fdot(F, (3, f(3)))
    yb = -4.0
    for t, s in ((0, 't=0'), (1, 't=1'), (3, 't=3')):
        F.dashed((t, f(t)), (t, yb)); F.lab((t, yb), s, 'ct', 0, 6)
    callout(F, (0, f(0)), 'v=-5', (-0.9, -0.6), 'rc')
    callout(F, (1, f(1)), 'v=-8', (2.0, -3.5), 'lc')
    callout(F, (3, f(3)), 'v=4', (1.8, 1.6), 'rc')
    return F.render()


def i26():  # 41·42번 v=f(t)
    F = Frame((-0.9, 7.2), (-1.8, 2.0), 70, 70, M)
    F.axes('t', 'v'); O(F, 'rt', -6, 4)
    F.polyline([(0, 0), (1, 1), (3, -1), (5, -1), (6, 0)])
    F.dashed((0, 1), (1, 1)); F.dashed((1, 0), (1, 1)); F.dashed((0, -1), (3, -1)); F.dashed((3, 0), (3, -1)); F.dashed((4, 0), (4, -1)); F.dashed((5, 0), (5, -1))
    F.lab((1, 0), '1', 'ct', 0, 6); F.lab((2, 0), '2', 'ct', 6, 6)
    for x in (3, 4, 5, 6):
        F.lab((x, 0), str(x), 'cb', 0, -6)
    F.lab((0, 1), '1', 'rc', -8, 0); F.lab((0, -1), '-1', 'rc', -8, 0)
    F.lab((1, 1), 'v=f(t)', 'lb', 6, -6)
    return F.render()


JOBS = {k: v for k, v in globals().items() if k[0] == 'i' and k[1:].isdigit()}
if __name__ == '__main__':
    run(JOBS, OUT, sys.argv[2:], wide=('i8',), natural=('i19', 'i20', 'i23', 'i24'))
