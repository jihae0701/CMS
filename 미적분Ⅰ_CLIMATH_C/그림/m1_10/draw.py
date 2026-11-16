# -*- coding: utf-8 -*-
"""미적분Ⅰ 10. 정적분의 활용 — 스캔 그림 다시 그리기.  python3 draw.py 출력폴더 [이름...]"""
import sys, math
sys.path.insert(0, '/home/user/CMS/.claude/skills/math-figure-rules'); sys.path.insert(0, '..')
from mathfig import Frame, DASH, SKY, GREEN, roots
from mjcommon import plot, O, run, arr, fdot, odot
OUT = sys.argv[1]
M = (16, 30, 180, 40)
ML = (130, 30, 180, 40)
YEL, PINK = '#fff3bf', '#ffd9e6'
cbrt = lambda v: math.copysign(abs(v) ** (1 / 3), v)


def band(F, f, g, a, b, col=SKY, n=80):
    """y=f, y=g 사이(a≤x≤b) 색칠"""
    P = [(a + (b - a) * i / n, f(a + (b - a) * i / n)) for i in range(n + 1)]
    Q = [(a + (b - a) * i / n, g(a + (b - a) * i / n)) for i in range(n + 1)][::-1]
    F.poly(P + Q, col)


Z = lambda x: 0


def inv(f, y, lo, hi):
    for _ in range(60):
        m = (lo + hi) / 2
        if f(m) < y:
            lo = m
        else:
            hi = m
    return (lo + hi) / 2


def callout(F, p, text, q, anc):
    F.lab(q, text, anc); arr(F, q, p, 1.2, 7)


def end_lab(F, f, x, tex, anc='rc', dx=-12, dy=0):
    F.lab((x, f(x)), tex, anc, dx, dy)


def i3():   # 4번 해설 y=6(x+1)(x-3), 1≤x≤2
    f = lambda x: 6 * (x + 1) * (x - 3) / 8
    F = Frame((-1.8, 4.2), (-3.4, 1.6), 70, 70, (270, 30, 40, 40))
    band(F, f, Z, 1, 2)
    F.axes(); O(F, 'rb', -6, -4)
    plot(F, f, -1.35, 3.35)
    F.seg((1, 0), (1, f(1)), 1.5); F.seg((2, 0), (2, f(2)), 1.5)
    F.lab((-1, 0), '-1', 'rt', -4, 6); F.lab((1, 0), '1', 'cb', 0, -6); F.lab((2, 0), '2', 'cb', 0, -6); F.lab((3, 0), '3', 'lt', 4, 6)
    end_lab(F, f, -1.35, 'y=6(x+1)(x-3)', 'rc', -8, 0)
    return F.render()


def i4():   # 5번 해설 y=x²(x-1), 0≤x≤3
    f = lambda x: x * x * (x - 1) / 4
    F = Frame((-0.9, 3.8), (-0.9, 4.9), 90, 70, M)
    band(F, f, Z, 0, 3)
    F.axes(); O(F, 'rb', -6, -4)
    plot(F, f, -0.6, 3.0)
    F.seg((3, 0), (3, f(3)), 1.5)
    F.lab((1, 0), '1', 'ct', 0, 6); F.lab((3, 0), '3', 'ct', 0, 6)
    end_lab(F, f, 3.0, 'y=x^{2}(x-1)', 'lc', 10, 0)
    return F.render()


def i5():   # 9번 해설 y=x², y=x³-2x
    f = lambda x: x * x; g = lambda x: x ** 3 - 2 * x
    F = Frame((-2.2, 2.9), (-1.8, 5.4), 80, 60, ML)
    band(F, g, f, -1, 0); band(F, f, g, 0, 2)
    F.axes(); O(F, 'lt', 6, 4)
    plot(F, f, -2.05, 2.22); plot(F, g, -1.65, 2.15)
    F.dashed((-1, 0), (-1, 1)); F.dashed((-1, 1), (0, 1)); F.dashed((2, 0), (2, 4)); F.dashed((0, 4), (2, 4))
    F.lab((2, 0), '2', 'lt', 4, 6); F.lab((0, 4), '4', 'rc', -8, 0); F.lab((0, 1), '1', 'lb', 6, -2)
    callout(F, (-1, 0), '-1', (-1.8, -0.6), 'rc')
    end_lab(F, f, -2.05, 'y=x^{2}', 'rc', -8, 0); end_lab(F, g, -1.65, 'y=x^{3}-2x', 'rc', -8, 0)
    return F.render()


def i6():   # 10번 문제 y=x²-4x, A, B
    f = lambda x: (x * x - 4 * x) / 2
    a = 5.5
    F = Frame((-1.1, 7.2), (-2.6, 4.6), 55, 55, M)
    band(F, f, Z, 0, 4, YEL); band(F, f, Z, 4, a, PINK)
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, f, -0.75, 6.0)
    F.seg((a, 0), (a, f(a)), 1.5)
    F.lab((2, -0.9), 'A', 'cc'); callout(F, (5.1, 0.7), 'B', (6.3, 2.0), 'lc')
    F.lab((4, 0), '4', 'rb', -6, -4); F.lab((a, 0), 'a', 'ct', 0, 6)
    end_lab(F, f, 6.0, 'y=x^{2}-4x', 'lc', 8, 0)
    return F.render()


fp11 = lambda x: (-x * x + 4 * x - 2) / 1.5
p11 = 2 - math.sqrt(2)


def i7():   # 11번 해설
    F = Frame((-0.8, 5.0), (-2.4, 2.0), 70, 70, M)
    band(F, fp11, Z, 0, p11); band(F, fp11, Z, p11, 4 - p11)
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, fp11, -0.15, 4.6)
    F.dashed((2, -2.3), (2, 1.9))
    callout(F, (0.18, -0.45), 'A', (0.9, -1.3), 'lc'); F.lab((2.45, 0.45), 'B', 'cc')
    F.lab((p11, 0), 'p', 'lt', 4, 6); F.lab((2, 0), '2', 'lt', 4, 6)
    end_lab(F, fp11, 4.6, 'y=-x^{2}+4x+a', 'rt', -4, 6)
    return F.render()


def i8():   # 11번 문제
    F = Frame((-0.8, 5.0), (-2.4, 2.0), 70, 70, M)
    band(F, fp11, Z, 0, p11, PINK); band(F, fp11, Z, p11, 4 - p11, GREEN)
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, fp11, -0.15, 4.6)
    callout(F, (0.2, -0.4), 'A', (0.9, -1.2), 'lc'); F.lab((2, 0.45), 'B', 'cc')
    end_lab(F, fp11, 4.6, 'y=-x^{2}+4x+a', 'rt', -4, 6)
    return F.render()


def i9():   # 12번 해설 y=x³-ax², y=x²-ax
    a = 0.45
    f = lambda x: x ** 3 - a * x * x; g = lambda x: x * x - a * x
    F = Frame((-0.3, 1.45), (-0.25, 1.25), 300, 300, M)
    band(F, f, g, 0, a); band(F, g, f, a, 1)
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, f, -0.2, 1.2); plot(F, g, -0.28, 1.15)
    F.dashed((1, 0), (1, f(1)))
    F.lab((a, 0), 'a', 'ct', 0, 6); F.lab((1, 0), '1', 'ct', 0, 6)
    end_lab(F, f, 1.2, 'y=x^{3}-ax^{2}', 'lc', 8, 0)
    callout(F, (0.2, g(0.2)), 'y=x^{2}-ax', (0.55, -0.17), 'lc')
    return F.render()


def i10():  # 13번 해설 y=x²(x-1)(x-a)
    a = 1.6
    f = lambda x: x * x * (x - 1) * (x - a) * 2.2
    F = Frame((-0.6, 2.2), (-0.8, 0.8), 160, 160, M)
    band(F, f, Z, 0, 1); band(F, f, Z, 1, a)
    F.xaxis(-0.55, 2.1)
    plot(F, f, -0.42, 1.93)
    F.lab((0, 0), '0', 'ct', 0, 6); F.lab((1, 0), '1', 'ct', 0, 6); F.lab((a, 0), 'a', 'cb', 6, -6)
    return F.render()


def inv_pair(f, x0, x1):
    """f와 그 역함수 g (단조증가)"""
    return lambda y: inv(f, y, x0 - 5, x1 + 5)


def i11():  # 14번 해설 f=x³-3x²+3x, g=f^-1
    f = lambda x: x ** 3 - 3 * x * x + 3 * x
    g = inv_pair(f, -1, 3)
    F = Frame((-0.6, 2.8), (-0.6, 2.8), 110, 110, M)
    band(F, f, g, 0, 1); band(F, g, f, 1, 2)
    F.axes(); O(F, 'lt', 4, 4)
    plot(F, f, -0.25, 2.18); plot(F, g, -0.6, 2.6); F.seg((-0.5, -0.5), (2.5, 2.5), 2.0)
    F.dashed((0, 1), (1, 1)); F.dashed((1, 0), (1, 1)); F.dashed((0, 2), (2, 2)); F.dashed((2, 0), (2, 2))
    F.lab((1, 0), '1', 'ct', 0, 6); F.lab((2, 0), '2', 'ct', 0, 6); F.lab((0, 1), '1', 'rc', -8, 0); F.lab((0, 2), '2', 'rc', -8, 0)
    end_lab(F, f, 2.18, 'y=f(x)', 'rc', -10, 0); F.lab((2.5, 2.5), 'y=x', 'lc', 6, 0); end_lab(F, g, 2.6, 'y=g(x)', 'lc', 6, 0)
    return F.render()


def i12():  # 15번 해설 f=x³-2x²+2x, g=f^-1
    f = lambda x: x ** 3 - 2 * x * x + 2 * x
    g = inv_pair(f, -1, 3)
    F = Frame((-0.6, 2.2), (-0.6, 2.2), 140, 140, M)
    band(F, f, g, 0, 1)
    F.axes(); O(F, 'rb', -6, -4)
    plot(F, f, -0.3, 1.62); plot(F, g, -0.6, 2.1); F.seg((-0.5, -0.5), (1.9, 1.9), 2.0)
    F.dashed((0, 1), (1, 1)); F.dashed((1, 0), (1, 1))
    F.lab((1, 0), '1', 'ct', 0, 6); F.lab((0, 1), '1', 'rc', -8, 0)
    end_lab(F, f, 1.62, 'y=f(x)', 'rc', -10, 0); F.lab((1.9, 1.9), 'y=x', 'lc', 6, 0); end_lab(F, g, 2.1, 'y=g(x)', 'lt', 0, 6)
    return F.render()


def inverse_regions(f, a, b, top, R, sc, lbl):
    """f(a)=fa, f(b)=fb: A=∫_a^b f (아래), C=x축 위쪽 f 왼쪽 (fa≤y≤fb), B=g 아래 (fa≤x≤fb)"""
    fa, fb = f(a), f(b)
    g = lambda y: inv(f, y, a - 3, b + 3)
    F = Frame((-0.6 * sc, R), (-0.6 * sc, top), 40 / sc, 40 / sc, M)
    n = 60
    F.poly([(0, fa)] + [(g(fa + (fb - fa) * i / n), fa + (fb - fa) * i / n) for i in range(n + 1)] + [(0, fb)], SKY)
    band(F, f, Z, a, b, GREEN); band(F, g, Z, fa, fb, PINK)
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, f, inv(f, -0.5 * sc, -5, 5) if a == 0 else 0, inv(f, top * 0.97, -5, 5)); plot(F, g, -0.5 * sc if a == 0 else 0, R * 0.95); F.seg((-0.5 * sc, -0.5 * sc), (R * 0.75, R * 0.75), 2.0)
    F.dashed((0, fb), (b, fb)); F.dashed((b, 0), (b, fb)); F.dashed((0, fa), (fb, fa)) if fa > 0 else None
    F.seg((fb, 0), (fb, b), 1.5)
    return F, g, fa, fb


def i13():  # 16번 해설 f=x³+x² (x≥0)
    f = lambda x: x ** 3 + x * x
    F, g, fa, fb = inverse_regions(f, 1, 2, 13.5, 14.5, 4, None)
    F.lab((0.15 + 1.2, 6.5), 'C', 'cc'); F.lab((1.5, 1.3), 'A', 'cc'); F.lab((7, 0.8), 'B', 'cc')
    for v in (1, 2, 12):
        F.lab((v, 0), str(v), 'ct', 0, 6)
    F.lab((0, 2), '2', 'rc', -8, 0); F.lab((0, 12), '12', 'rc', -8, 0)
    F.lab((2.3, 13.2), 'y=f(x)', 'lc', 6, 0); F.lab((10.9, 10.9), 'y=x', 'lc', 6, 0); end_lab(F, g, 13.8, 'y=g(x)', 'rb', 0, -8)
    return F.render()


def i14():  # 17번 해설 f=x³+2x+2
    f = lambda x: x ** 3 + 2 * x + 2
    F, g, fa, fb = inverse_regions(f, 0, 2, 15.5, 16.5, 4, None)
    F.lab((0.6, 9.0), 'C', 'cc'); F.lab((1.2, 1.8), 'A', 'cc'); F.lab((9, 0.7), 'B', 'cc')
    F.lab((2, 0), '2', 'ct', 0, 6); F.lab((14, 0), '14', 'ct', 0, 6); F.lab((0, 2), '2', 'rc', -8, 0); F.lab((0, 14), '14', 'rc', -8, 0)
    F.lab((2.3, 15.2), 'y=f(x)', 'lc', 6, 0); F.lab((12.4, 12.4), 'y=x', 'lc', 6, 0); end_lab(F, g, 15.7, 'y=g(x)', 'rb', 0, -8)
    return F.render()


def i15():  # 24번 해설 y=√(4-ax)
    k = 8 / 3
    f = lambda x: math.sqrt(max(0, 4 - k * x))
    F = Frame((-2.0, 2.4), (-0.9, 3.6), 90, 90, (40, 16, 40, 16))
    band(F, f, Z, 0, 1.5)
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, f, -1.8, 1.5)
    F.lab((0, 2), '2', 'lb', 6, -4)
    end_lab(F, f, -1.8, 'y=\\sqrt{4-ax}', 'lb', -10, -10)
    return F.render()


def i16():  # 25번 해설 y=x³-2x, y=-x²
    f = lambda x: x ** 3 - 2 * x; g = lambda x: -x * x
    F = Frame((-2.6, 1.9), (-4.6, 2.1), 80, 60, M)
    band(F, f, g, -2, 0); band(F, g, f, 0, 1)
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, f, -2.12, 1.62); plot(F, g, -2.12, 1.75)
    F.dashed((-2, 0), (-2, -4)); F.dashed((1, 0), (1, -1))
    F.lab((-2, 0), '-2', 'cb', 0, -6); F.lab((1, 0), '1', 'cb', 4, -6)
    end_lab(F, f, 1.62, 'y=x^{3}-2x', 'lc', 6, 0); end_lab(F, g, 1.75, 'y=-x^{2}', 'lc', 6, 0)
    return F.render()


def i17():  # 26번 해설 y=x³+4, y=3x²
    f = lambda x: x ** 3 + 4; g = lambda x: 3 * x * x
    F = Frame((-2.0, 3.0), (-2.5, 14.5), 90, 22, ML)
    band(F, f, g, -1, 2)
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, f, -1.85, 2.15); plot(F, g, -2.15, 2.15)
    F.dashed((-1, 0), (-1, 3)); F.dashed((2, 0), (2, 12))
    F.lab((-1, 0), '-1', 'ct', -6, 6); F.lab((2, 0), '2', 'ct', 6, 6); F.lab((0, 4), '4', 'lb', 6, -2)
    end_lab(F, f, 2.15, 'y=x^{3}+4', 'lc', 8, 0); end_lab(F, g, -2.15, 'y=3x^{2}', 'rc', -8, 0)
    return F.render()


def i18():  # 28번 해설 y=|x|, y=-x²+2
    f = lambda x: -x * x + 2; g = lambda x: abs(x)
    F = Frame((-2.4, 2.6), (-1.3, 2.7), 90, 90, M)
    band(F, f, g, -1, 1)
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, f, -1.75, 1.75); F.polyline([(-2.3, 2.3), (0, 0), (2.3, 2.3)], 'stroke-width="2.0"')
    F.dashed((-1, 0), (-1, 1)); F.dashed((1, 0), (1, 1))
    F.lab((-1, 0), '-1', 'ct', 0, 6); F.lab((1, 0), '1', 'ct', 0, 6); F.lab((0, 2), '2', 'rb', -6, -4)
    F.lab((2.3, 2.3), 'y=|x|', 'rc', -12, 0); end_lab(F, f, 1.75, 'y=-x^{2}+2', 'lc', 8, 0)
    return F.render()


def i19():  # 29번 해설 y=|x²-2x|, 0≤x≤3
    f = lambda x: abs(x * x - 2 * x)
    F = Frame((-0.9, 3.9), (-0.6, 4.2), 90, 90, M)
    band(F, f, Z, 0, 3)
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, f, -0.65, 3.18); F.seg((3, 0), (3, 3), 1.5)
    F.lab((2, 0), '2', 'ct', 0, 6); F.lab((3, 0), '3', 'ct', 0, 6)
    end_lab(F, f, 3.18, 'y=|x^{2}-2x|', 'lc', 6, 0)
    return F.render()


def i20(col=SKY, sol=True):  # 30번 해설 y=x³, 접선 y=3x+2
    f = lambda x: x ** 3; g = lambda x: 3 * x + 2
    F = Frame((-2.0, 2.9), (-3.0, 9.0), 90, 40, M)
    band(F, g, f, -1, 2, col)
    F.axes(); O(F, 'lt', 4, 4)
    plot(F, f, -1.4, 2.08); F.seg((-1.6, g(-1.6)), (2.3, g(2.3)), 2.0)
    F.dashed((-1, 0), (-1, -1)); F.dashed((-1, -1), (0, -1))
    F.lab((-1, 0), '-1', 'cb', 0, -6); F.lab((0, -1), '-1', 'lc', 8, 0)
    if sol:
        F.dashed((2, 0), (2, 8)); F.lab((2, 0), '2', 'ct', 6, 6)
        callout(F, (0.2, 2.6), 'y=3x+2', (-0.4, 7.0), 'rc')
    end_lab(F, f, 2.08, 'y=x^{3}', 'rc', -10, 0)
    return F.render()


def i21():  # 30번 문제
    return i20(GREEN, False)


def i22():  # 32번 해설 f=x³+x-1, g=f^-1
    f = lambda x: x ** 3 + x - 1
    g = lambda y: inv(f, y, -3, 4)
    F = Frame((-0.6, 10.5), (-0.6, 10.5), 36, 36, M)
    n = 60
    F.poly([(0, 1)] + [(g(1 + 8 * i / n), 1 + 8 * i / n) for i in range(n + 1)] + [(0, 9)], SKY)
    band(F, g, Z, 1, 9, PINK)
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, f, inv(f, 0, -2, 3), 2.0); plot(F, g, 0.0, 9.0); F.seg((-0.3, -0.3), (8.2, 8.2), 2.0)
    F.dashed((0, 2), (9, 2)); F.dashed((2, 0), (2, 9)); F.dashed((1, 0), (1, 1)); F.dashed((0, 1), (1, 1))
    F.seg((9, 0), (9, 2), 1.5); F.seg((0, 9), (2, 9), 1.5)
    F.lab((0.55, 6), 'B', 'cc'); F.lab((5.5, 0.9), 'A', 'cc')
    for v in (1, 2, 9):
        F.lab((v, 0), str(v), 'ct', 0, 6)
    F.lab((0, 1), '1', 'rc', -8, 0); F.lab((0, 2), '2', 'rc', -8, 0); F.lab((0, 9), '9', 'rc', -8, 0)
    F.lab((2.0, 9.0), 'y=f(x)', 'lc', 6, 0); F.lab((8.2, 8.2), 'y=x', 'lc', 6, 0); F.lab((9.0, g(9)), 'y=g(x)', 'cb', 0, -8)
    return F.render()


def i23():  # 32번 문제 y=x³+x-1
    f = lambda x: x ** 3 + x - 1
    F = Frame((-0.9, 1.9), (-2.0, 4.6), 110, 60, M)
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, f, -0.65, 1.6)
    F.lab((0, -1), '-1', 'lc', 8, 0); end_lab(F, f, 1.6, 'y=f(x)', 'lc', 8, 0)
    return F.render()


def i24():  # 34번 해설 y=2√x, y=√x+2
    f = lambda x: 2 * math.sqrt(x); g = lambda x: math.sqrt(x) + 2
    F = Frame((-0.9, 7.0), (-0.9, 5.6), 60, 60, (16, 16, 110, 16))
    band(F, g, f, 0, 4)
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, f, 0, 6.0); plot(F, g, 0, 6.0)
    F.dashed((0, 4), (4, 4)); F.dashed((4, 0), (4, 4))
    F.lab((4, 0), '4', 'ct', 0, 6); F.lab((0, 4), '4', 'rc', -8, 0); F.lab((0, 2), '2', 'rc', -8, 0)
    end_lab(F, f, 6.0, 'y=2\\sqrt{x}', 'lb', 6, -2); end_lab(F, g, 6.0, 'y=\\sqrt{x}+2', 'lt', 6, 2)
    return F.render()


def i25():  # 35번 해설 f=x³+x²+x, g=f^-1
    f = lambda x: x ** 3 + x * x + x
    g = lambda y: inv(f, y, -4, 4)
    F = Frame((-1.6, 1.6), (-1.6, 1.8), 120, 120, M)
    band(F, f, g, -1, 0)
    F.axes(); O(F, 'rb', -6, -4)
    plot(F, f, -1.12, 0.74); plot(F, g, -1.3, 1.45, 3.2, DASH); F.seg((-1.4, -1.4), (1.2, 1.2), 2.0)
    F.dashed((-1, 0), (-1, -1))
    F.lab((-1, 0), '-1', 'cb', 0, -6)
    end_lab(F, f, 0.74, 'y=f(x)', 'lc', 6, 0); F.lab((1.2, 1.2), 'y=x', 'lc', 6, 0); F.lab((1.45, g(1.45)), 'y=g(x)', 'lt', -10, 8)
    return F.render()


def vt(pts, xs, ys, yl='v(t)', lab=None, ticks=()):
    F = Frame((-0.9, max(p[0] for p in pts) + 1.1), (min(p[1] for p in pts) - 0.9, max(p[1] for p in pts) + 1.0), 55, 55, (50, 30, 40, 30))
    F.axes('t', yl); O(F, 'rt', -6, 4)
    F.polyline(pts)
    for x, y in pts[1:]:
        if y != 0:
            F.dashed((x, 0), (x, y))
    for y in sorted(set(p[1] for p in pts if p[1] != 0)):
        xs_y = [p[0] for p in pts if p[1] == y]
        F.dashed((0, y), (max(xs_y), y))
        F.lab((0, y), str(y), 'rc', -8, 0)
    for x in ticks:
        y = next((p[1] for p in pts if p[0] == x), 0)
        F.lab((x, 0), str(x), 'cb' if y < 0 else 'ct', 0, -6 if y < 0 else 6)
    if lab:
        F.lab(*lab)
    return F.render()


def i26():  # 36번 문제 y=v(t), 9초
    return vt([(0, 0), (1, 2), (3, 2), (5, -2), (7, 2), (9, 0)], 0, 0, 'y', ((3.2, 2.0), 'y=v(t)', 'lb', 4, -6), (1, 2, 3, 4, 5, 6, 7, 8, 9))


def i27():  # 37번 문제
    return vt([(0, 0), (1, 1), (3, 2), (4, 0), (6, -1)], 0, 0, 'v(t)', None, (1, 3, 4, 6))


def i28():  # 38번 문제 8초
    return vt([(0, 0), (1, 2), (3, 2), (5, -2), (7, 2), (8, 0)], 0, 0, 'v(t)', None, (1, 2, 3, 4, 5, 6, 7, 8))


def i30():  # 39번 해설 f=-x²+2x (x≤1), -x+2 (x≥1)
    p = lambda x: -x * x + 2 * x; l = lambda x: -x + 2
    f = lambda x: p(x) if x <= 1 else l(x)
    F = Frame((-0.6, 3.0), (-1.2, 2.5), 110, 110, M)
    band(F, f, Z, 0, 2)
    F.axes(); O(F, 'rb', -6, -4)
    plot(F, p, -0.35, 1); F.seg((1, 1), (2.8, -0.8), 3.2)
    plot(F, p, 1, 2.35, 3.2, DASH); F.seg((-0.4, 2.4), (1, 1), 1.5, DASH)
    F.dashed((1, 0), (1, 1))
    F.lab((1, 0), '1', 'ct', 0, 6); F.lab((2, 0), '2', 'ct', -6, 6)
    F.lab((1.2, 1.0), 'y=f(x)', 'lb', 4, -6)
    return F.render()


def i31():  # 40번 해설 f=x³/3-x
    f = lambda x: x ** 3 / 3 - x
    F = Frame((-2.6, 2.7), (-1.6, 1.7), 80, 80, M)
    band(F, f, Z, -math.sqrt(3), math.sqrt(3))
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, f, -2.35, 2.3)
    F.lab((-math.sqrt(3), 0), '-\\sqrt{3}', 'rb', -4, -4); F.lab((math.sqrt(3), 0), '\\sqrt{3}', 'lb', 4, -4)
    end_lab(F, f, 2.3, 'y=f(x)', 'rc', -12, 0)
    return F.render()


def i32():  # 40번 문제 f'=x²-1
    f = lambda x: x * x - 1
    F = Frame((-1.9, 2.0), (-1.6, 2.6), 90, 70, M)
    F.axes(); O(F, 'lt', 4, 4)
    plot(F, f, -1.75, 1.75)
    F.lab((-1, 0), '-1', 'rt', -4, 6); F.lab((1, 0), '1', 'lt', 4, 6); F.lab((0, -1), '-1', 'rt', -6, 6)
    end_lab(F, f, 1.75, "y=f'(x)", 'lc', 6, 0)
    return F.render()


def i33():  # 41번 문제 y=x³, y=k, x=1
    f = lambda x: x ** 3; k = 0.3; c = cbrt(k)
    K = lambda x: k
    F = Frame((-0.9, 1.7), (-0.6, 1.35), 220, 220, M)
    band(F, K, f, 0, c, YEL); band(F, f, K, c, 1, PINK)
    F.axes(); O(F, 'lt', 4, 4)
    plot(F, f, -0.85, 1.1); F.seg((-0.85, k), (1.6, k), 2.0); F.seg((1, 0), (1, 1), 1.5)
    F.dashed((0, 1), (1, 1))
    F.lab((0.22, 0.2), 'A', 'cc'); F.lab((0.88, 0.45), 'B', 'cc')
    F.lab((1, 0), '1', 'ct', 0, 6); F.lab((0, 1), '1', 'rc', -8, 0)
    F.lab((1.6, k), 'y=k', 'rb', 0, -6); end_lab(F, f, 1.1, 'y=x^{3}', 'lc', 6, 0)
    return F.render()


def i34():  # 42번 해설 y=-x²+2x, y=ax
    a = 0.6
    f = lambda x: -x * x + 2 * x; g = lambda x: a * x
    F = Frame((-0.5, 2.7), (-0.7, 1.45), 160, 160, M)
    band(F, f, Z, 0, 2)
    F.axes(); O(F, 'lt', 4, 4)
    plot(F, f, -0.12, 2.15); F.seg((-0.4, -0.24), (2.2, 1.32), 2.0)
    F.dashed((2 - a, 0), (2 - a, f(2 - a)))
    F.lab((2 - a, 0), '2-a', 'ct', -4, 6); F.lab((2, 0), '2', 'lt', 6, 6)
    F.lab((2.2, 1.32), 'y=ax', 'lc', 6, 0); F.lab((1, 1), 'y=-x^{2}+2x', 'cb', 0, -10)
    return F.render()


def i35():  # 43번 해설 f=x² (x<1), (x-2)² (x≥1), y=x
    f = lambda x: x * x if x < 1 else (x - 2) ** 2
    l = lambda x: x
    F = Frame((-1.4, 5.0), (-0.9, 4.9), 70, 70, M)
    band(F, l, f, 0, 4)
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, f, -1.2, 4.12); F.seg((-0.8, -0.8), (4.6, 4.6), 2.0)
    F.dashed((1, 0), (1, 1)); F.dashed((4, 0), (4, 4))
    fdot(F, (1, 1)); F.pt((1, 1), 'A', 'rb', -6, -4)
    F.lab((1, 0), '1', 'ct', 0, 6); F.lab((2, 0), '2', 'ct', 0, 6); F.lab((4, 0), '4', 'ct', 6, 6)
    F.lab((4.6, 4.6), 'y=x', 'lc', 6, 0); F.lab((4.12, f(4.12)), 'y=f(x)', 'rc', -10, 0)
    return F.render()


def i36():  # 44번 문제 f'(x): x=1에서 0인 일차함수
    f = lambda x: 2.2 * (x - 1)
    F = Frame((-0.9, 2.9), (-1.8, 2.8), 90, 70, M)
    F.axes(); O(F, 'rt', -6, 4)
    F.seg((0.2, f(0.2)), (2.1, f(2.1)), 3.2)
    F.lab((1, 0), '1', 'lt', 6, 6); F.lab((2.1, f(2.1)), "y=f'(x)", 'lc', 8, 0)
    return F.render()


def i37():  # 44번 해설 f=3x²-6x-9
    f = lambda x: (3 * x * x - 6 * x - 9) / 4
    F = Frame((-1.9, 4.0), (-3.4, 3.4), 70, 70, M)
    band(F, f, Z, -1, 3)
    F.axes(); O(F, 'lt', 4, 4)
    plot(F, f, -1.65, 3.65)
    F.lab((-1, 0), '-1', 'rt', -4, 6); F.lab((3, 0), '3', 'lt', 4, 6)
    end_lab(F, f, 3.65, 'y=f(x)', 'rc', -12, 0)
    return F.render()


def i38():  # 46번 문제 v(t): 극대 t=a, 0이 되는 t=b, t=c
    f = lambda t: t * (2.4 - t)
    F = Frame((-0.6, 3.4), (-1.8, 1.9), 120, 120, M)
    F.axes('t', 'v(t)'); O(F, 'rt', -6, 4)
    plot(F, f, 0, 3.1)
    F.dashed((1.2, 0), (1.2, f(1.2))); F.dashed((2.85, 0), (2.85, f(2.85)))
    F.lab((1.2, 0), 'a', 'ct', 0, 6); F.lab((2.4, 0), 'b', 'rt', -4, 6); F.lab((2.85, 0), 'c', 'cb', 0, -6)
    return F.render()


JOBS = {k: v for k, v in globals().items() if k[0] == 'i' and k[1:].isdigit()}
if __name__ == '__main__':
    run(JOBS, OUT, sys.argv[2:])
