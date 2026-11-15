import sys, math
sys.path.insert(0, '/home/user/CMS/.claude/skills/math-figure-rules')
from mathfig import Frame, fit_shoot, dot, right_mark, SKY, YELLOW, DASH
OUT = sys.argv[1]
sq = lambda v: math.sqrt(max(v, 0))

def plot(F, f, a, b, solid=True, n=240):
    pts = [(a + (b - a) * i / n, f(a + (b - a) * i / n)) for i in range(n + 1)]
    F.svg.append('<polyline points="%s" fill="none" stroke="#000" stroke-width="%s" stroke-linejoin="round" %s/>'
                 % (" ".join("%.1f,%.1f" % F.P(*p) for p in pts), 3.2 if solid else 1.6, '' if solid else DASH))

def guide(F, p, gx=True, gy=True):
    if gx: F.dashed(p, (p[0], 0))
    if gy: F.dashed(p, (0, p[1]))

def base(xr, yr, s=55, sy=None, m=None, o=('rt', -6, 4)):
    F = Frame(xr, yr, s, sy or s, (24, 24, 24, 24))
    F.axes(); F.pt((0, 0), 'O', *o)
    return F

def f3a():
    F = base((-14.0, 3.2), (-1.6, 3.2), 55, 95, o=('lt', 4, 4))
    plot(F, lambda x: sq(-x), -6.4, 0, False)
    plot(F, lambda x: sq(2 - x) - 1, -6.4, 2)
    guide(F, (2, -1))
    F.lab((2, 0), '2', 'lb', 2, -4); F.lab((0, -1), '-1', 'rc', -6, 0)
    F.lab((-6.4, sq(6.4)), 'y=\\sqrt{-x}', 'rc', -8, -4)
    F.lab((-6.4, sq(8.4) - 1), 'y=\\sqrt{-x+2}-1', 'rc', -8, 6)
    return F.render()

def f3b():
    F = base((-2.8, 9.6), (-0.8, 5.4))
    plot(F, lambda x: sq(2 * x), 0, 4.6, False)
    plot(F, lambda x: sq(2 * x + 4) + 1, -2, 4.6)
    guide(F, (-2, 1))
    F.lab((-2, 0), '-2', 'ct', 0, 8); F.lab((0, 1), '1', 'lb', 6, -4)
    F.lab((4.6, sq(13.2) + 1), 'y=\\sqrt{2x+4}+1', 'lc', 8, 0)
    F.lab((4.6, sq(9.2)), 'y=\\sqrt{2x}', 'lc', 8, 0)
    return F.render()

def f3c():
    F = base((-1.8, 9.8), (-4.2, 2.8), o=('lt', 4, 4))
    plot(F, lambda x: -sq(3 * x), 0, 4.6, False)
    plot(F, lambda x: -sq(3 * x + 3) + 2, -1, 4.6)
    guide(F, (-1, 2))
    F.lab((-1, 0), '-1', 'ct', 0, 8); F.lab((0, 2), '2', 'lc', 6, 0)
    F.lab((4.6, -sq(16.8) + 2), 'y=-\\sqrt{3x+3}+2', 'lc', 8, 0)
    F.lab((4.6, -sq(13.8)), 'y=-\\sqrt{3x}', 'lc', 8, 0)
    return F.render()

def f3d():
    F = base((-12.6, 2.8), (-3.4, 3.6))
    plot(F, lambda x: -sq(-2 * x), -4.6, 0, False)
    plot(F, lambda x: -sq(-2 * x + 4) + 3, -4.6, 2)
    guide(F, (2, 3))
    F.lab((2, 0), '2', 'ct', 0, 8); F.lab((0, 3), '3', 'rc', -6, 0); F.lab((0, 1), '1', 'lt', 4, 2)
    F.lab((-4.6, -sq(13.2) + 3), 'y=-\\sqrt{-2x+4}+3', 'rc', -8, 0)
    F.lab((-4.6, -sq(9.2)), 'y=-\\sqrt{-2x}', 'rc', -8, 0)
    return F.render()

def f4a():
    F = base((-1.8, 10.8), (-2.6, 3.0), o=('lb', 4, -4))
    plot(F, lambda x: sq(x), 0, 6.2, False)
    plot(F, lambda x: sq(x + 1) - 2, -1, 6.2)
    guide(F, (-1, -2))
    F.lab((-1, 0), '-1', 'cb', 0, -6); F.lab((3, 0), '3', 'ct', 0, 8)
    F.lab((0, -1), '-1', 'lb', 6, -2); F.lab((0, -2), '-2', 'lc', 6, 0)
    F.lab((6.2, sq(6.2)), 'y=\\sqrt{x}', 'lc', 8, 0)
    F.lab((6.2, sq(7.2) - 2), 'y=\\sqrt{x+1}-2', 'lc', 8, 0)
    return F.render()

def f4b():
    F = base((-12.6, 2.8), (-2.8, 1.8), o=('lb', 4, -4))
    plot(F, lambda x: -sq(-x), -5.2, 0, False)
    plot(F, lambda x: -sq(-x + 2) + 1, -5.2, 2)
    guide(F, (2, 1))
    F.lab((2, 0), '2', 'ct', 0, 8); F.lab((0, 1), '1', 'rc', -6, 0)
    F.lab((-5.2, -sq(7.2) + 1), 'y=-\\sqrt{-x+2}+1', 'rc', -8, -4)
    F.lab((-5.2, -sq(5.2)), 'y=-\\sqrt{-x}', 'rc', -8, 4)
    return F.render()

def f8s():
    c = 1.5
    F = base((-8.6, 3.0), (-3.0, 1.4), 60, o=('rb', -6, -4))
    plot(F, lambda x: -sq(-x), -4.2, 0, False)
    plot(F, lambda x: -sq(c - x), -4.2, c)
    F.lab((c, 0), '-\\frac{c}{b}', 'cb', 0, -6)
    F.lab((0, -sq(c)), 'a\\sqrt{c}', 'lt', 6, 4)
    F.lab((-4.2, -sq(4.2)), 'y=a\\sqrt{bx}', 'rc', -8, -8)
    F.lab((-4.2, -sq(4.2 + c)), 'y=a\\sqrt{bx+c}', 'rc', -8, 8)
    return F.render()

def f9a():
    F = base((-2.2, 10.6), (-1.6, 2.8), 60, o=('rb', -6, -4))
    plot(F, lambda x: sq(2 * x) - 1, 0, 4)
    plot(F, lambda x: sq(2 * x) - 1, 4, 6.2, False)
    A, B = (0, -1), (4, sq(8) - 1)
    dot(F, A); dot(F, B); guide(F, B)
    F.lab((0, B[1]), '2\\sqrt{2}-1', 'rc', -6, 0); F.lab((0, -1), '-1', 'rc', -6, 0)
    F.lab((4, 0), '4', 'ct', 0, 8); F.lab((0.5, 0), '\\frac{1}{2}', 'lt', 2, 6)
    F.lab((6.2, sq(12.4) - 1), 'y=\\sqrt{2x}-1', 'lc', 8, 0)
    return F.render()

def f9b():
    F = base((-3.4, 6.2), (-0.8, 3.8), 60, o=('rt', -6, 4))
    f = lambda x: -sq(-x + 5) + 3
    plot(F, f, -3.2, 0, False); plot(F, f, 0, 4); plot(F, f, 4, 5, False)
    for p in ((0, f(0)), (4, 2)):
        dot(F, p)
    guide(F, (4, 2)); guide(F, (5, 3))
    F.lab((0, 3), '3', 'rc', -6, 0); F.lab((0, 2), '2', 'rc', -6, 0); F.lab((0, f(0)), '3-\\sqrt{5}', 'rc', -6, 0)
    F.lab((4, 0), '4', 'ct', 0, 8); F.lab((5, 0), '5', 'ct', 0, 8)
    F.lab((1.0, 3.3), 'y=-\\sqrt{-x+5}+3', 'lb', 0, 0)
    return F.render()

def f10a():
    F = base((-0.8, 8.6), (-1.4, 8.6), 50, o=('rt', -6, 4))
    f = lambda x: sq(2 * x - 3) + 4
    plot(F, f, 1.5, 2, False); plot(F, f, 2, 6); plot(F, f, 6, 8.4, False)
    for p in ((2, 5), (6, 7)):
        dot(F, p); guide(F, p)
    guide(F, (1.5, 4))
    F.lab((0, 7), '7', 'rc', -6, 0); F.lab((0, 5), 'b', 'rc', -6, 0); F.lab((0, 4), '4', 'rc', -6, 0)
    F.lab((1.5, 0), '\\frac{3}{2}', 'ct', -6, 6); F.lab((2, 0), '2', 'ct', 8, 6); F.lab((6, 0), 'a', 'ct', 0, 8)
    F.lab((3.2, 8.0), 'y=\\sqrt{2x-3}+4', 'lc', 0, 0)
    return F.render()

def f10b():
    F = base((-8.4, 3.2), (-1.4, 6.6), 45, o=('rt', -6, 4))
    f = lambda x: sq(4 - 2 * x) + 1
    plot(F, f, -8.0, -6, False); plot(F, f, -6, 0); plot(F, f, 0, 2, False)
    for p in ((-6, 5), (0, 3)):
        dot(F, p)
    guide(F, (-6, 5)); guide(F, (2, 1))
    F.lab((0, 5), '5', 'lc', 6, 0); F.lab((0, 3), '3', 'lb', 6, -4); F.lab((0, 1), 'b', 'rc', -6, 0)
    F.lab((-6, 0), '-6', 'ct', 0, 8); F.lab((2, 0), '\\frac{4}{a}', 'ct', 0, 8)
    F.lab((-7.8, 6.3), 'y=\\sqrt{4-ax}+b', 'lc', 0, 0)
    return F.render()

def inv_pair(f, g, xr, yr, s, pts, labs, gd=()):
    F = base(xr, yr, s, o=('rt', -6, 4))
    lo = max(xr[0], yr[0]) + 0.2; hi = min(xr[1], yr[1]) - 0.3; F.seg((lo, lo), (hi, hi), 2.0)
    for fn, a, b in (f, g):
        plot(F, fn, a, b)
    for p in pts:
        dot(F, p)
    for p in gd:
        guide(F, p)
    for p, t, anc, dx, dy in labs:
        F.lab(p, t, anc, dx, dy)
    return F.render()

def f14a():
    phi = (1 + math.sqrt(5)) / 2
    return inv_pair((lambda x: x * x - 1, 0, 1.85), (lambda x: sq(x + 1), -1, 2.6), (-1.6, 7.6), (-1.5, 2.6), 90,
                    [], [((1.3, 0.69), 'y=x^2-1~(x\\ge 0)', 'lc', 10, 0), ((2.6, sq(3.6)), 'y=\\sqrt{x+1}', 'lc', 8, 0),
                         ((2.3, 2.3), 'y=x', 'lc', 8, 0), ((-1, 0), '-1', 'cb', 0, -6), ((0, -1), '-1', 'rc', -6, 0)])

def f14b():
    return inv_pair((lambda x: sq(-2 * x + 4) - 1, -2.6, 2), (lambda x: -(x + 1) ** 2 / 2 + 2, -1, 2.0), (-2.8, 7.8), (-2.8, 3.8), 75,
                    [], [((-2.6, sq(9.2) - 1), 'y=\\sqrt{-2x+4}-1', 'lb', 0, -8), ((2.0, -2.5), 'y=-\\frac{1}{2}(x+1)^2+2', 'lc', 8, 0),
                         ((2.5, 2.5), 'y=x', 'lc', 8, 0), ((2, 0), '2', 'cb', 0, -6), ((0, 2), '2', 'lc', 6, 0),
                         ((-1, 0), '-1', 'ct', 0, 8), ((0, -1), '-1', 'rc', -6, 0)], gd=[(2, -1), (-1, 2)])

def f15():
    return inv_pair((lambda x: sq(2 * x - 2) + 1, 1, 5.2), (lambda x: (x - 1) ** 2 / 2 + 1, 1, 4.0), (-0.8, 9.0), (-0.8, 5.8), 60,
                    [(1, 1), (3, 3)], [((5.2, sq(8.4) + 1), 'y=f(x)', 'lc', 8, 0), ((4.0, 5.5), 'y=f^{-1}(x)', 'rc', -8, 0),
                                       ((5.5, 5.5), 'y=x', 'lc', 8, 0), ((1, 0), '1', 'ct', 0, 8), ((0, 1), '1', 'rc', -6, 0),
                                       ((3, 3), '\\mathrm{Q}(3,\\ 3)', 'lt', 8, 4), ((1, 1), '\\mathrm{P}', 'lt', 6, 6)], gd=[(1, 1)])

def f16():
    return inv_pair((lambda x: sq(x + 1) - 1, -1, 2.6), (lambda x: (x + 1) ** 2 - 1, -1, 0.9), (-1.8, 5.6), (-1.8, 3.2), 85,
                    [(0, 0), (-1, -1)], [((2.6, sq(3.6) - 1), 'y=f(x)', 'lc', 8, 0), ((0.9, 2.61), 'y=f^{-1}(x)', 'lc', 6, 0),
                                         ((2.5, 2.5), 'y=x', 'lc', 8, 0), ((-1, 0), '-1', 'cb', 0, -6), ((0, -1), '-1', 'lc', 6, 0)], gd=[(-1, -1)])

def f35():
    a = 1.1; b = sq(2 - a)
    F = base((-4.8, 3.0), (-0.6, 2.6), 110, o=('rt', -6, 4))
    plot(F, lambda x: sq(2 - x), -1.5, 2)
    F.dashed((a, b), (a, 0)); F.dashed((a, b), (0, b))
    right_mark(F, (a, 0), (0, 0), (a, b), 0.12); right_mark(F, (0, b), (a, b), (0, 0), 0.12)
    dot(F, (a, b))
    F.pt((a, b), 'A(\\mathit{a},\\ \\mathit{b})', 'lb', 6, -4)
    F.pt((a, 0), 'B', 'ct', 0, 8); F.pt((0, b), 'C', 'rc', -6, 0)
    F.lab((2, 0), '2', 'ct', 4, 8); F.lab((0, sq(2)), '\\sqrt{2}', 'rb', -6, -2)
    F.lab((-1.5, sq(3.5)), 'y=\\sqrt{2-x}', 'rc', -8, 0)
    return F.render()

def f36(sol):
    A, B, Op = (-2, 4), (4, 2), (0, 0)
    F = base((-6.4, 5.6), (-0.8, 5.4), 70, o=('rt', -6, 4))
    xs = [(-2 + 2 * i / 60) for i in range(61)]
    if sol:
        F.poly([(x, x * x) for x in xs] + [(0, 0)], SKY)
        F.poly([(4 * i / 60, sq(4 * i / 60)) for i in range(61)], SKY)
        F.seg(Op, A, 2.4); F.seg(Op, B, 2.4)
    else:
        F.poly([(x, x * x) for x in xs] + [(4 * i / 60, sq(4 * i / 60)) for i in range(1, 61)], SKY)
    plot(F, lambda x: x * x, -2.25, 0); plot(F, lambda x: sq(x), 0, 5.4)
    F.seg((-2.8, (10 + 2.8) / 3), (5.5, (10 - 5.5) / 3), 2.4)
    guide(F, A); guide(F, B)
    dot(F, A); dot(F, B)
    F.pt(A, 'A', 'lb', 6, -6); F.pt(B, 'B', 'cb', 0, -10)
    F.lab((-2, 0), '-2', 'ct', 0, 8); F.lab((4, 0), '4', 'ct', 0, 8); F.lab((0, 4), '4', 'lb', 6, -4); F.lab((0, 2), '2', 'rb', -6, -4)
    F.lab((-2.25, 2.25 ** 2), 'y=f(x)', 'rc', -8, 0)
    F.lab((1.2, (10 - 1.2) / 3), 'x+3y-10=0', 'lb', 6, -6)
    return F.render()

def f37(sol):
    A, B, C = (3, 3), (0.5, 2), (2, 0.5)
    F = base((-1.8, 8.0), (-1.8, 4.8), 75, o=('rt', -6, 4))
    F.poly([A, B, C], SKY)
    plot(F, lambda x: sq(2 * x + 3), -1.5, 4.2)
    plot(F, lambda x: (x * x - 3) / 2, 0, 3.75)
    F.seg((-1.6, 4.1), (4.2, -1.7), 2.0)
    for p, q in ((A, B), (B, C), (C, A)):
        F.seg(p, q, 2.4)
    for p in (A, B, C):
        dot(F, p)
    if sol:
        H = (1.25, 1.25)
        F.seg(A, H, 1.6); right_mark(F, H, A, C, 0.18)
        F.pt(H, 'H', 'rt', -6, 4)
    F.pt(A, 'A', 'rb', -6, -4); F.pt(B, 'B', 'rb', -6, -4); F.pt(C, 'C', 'lt', 6, 2)
    F.lab((-1.6, 4.1), 'l', 'rc', -6, 0)
    F.lab((4.2, sq(11.4)), 'y=f(x)', 'lc', 6, 0)
    F.lab((3.75, 4.53), 'y=g(x)', 'lc', 8, 0)
    return F.render()

JOBS = {'3a': f3a, '3b': f3b, '3c': f3c, '3d': f3d, '4a': f4a, '4b': f4b, '8s': f8s, '9a': f9a, '9b': f9b, '10a': f10a, '10b': f10b,
        '14a': f14a, '14b': f14b, '15': f15, '16': f16, '35': f35, '36q': lambda: f36(False), '36s': lambda: f36(True),
        '37q': lambda: f37(False), '37s': lambda: f37(True)}
for k in (sys.argv[2:] or JOBS):
    print(k, fit_shoot(OUT + '/c2_11_%s.png' % k, JOBS[k]))
