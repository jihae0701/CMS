import sys, math
sys.path.insert(0, '/home/user/CMS/.claude/skills/math-figure-rules')
from mathfig import Frame, fit_shoot, dot, SKY, DASH
OUT = sys.argv[1]

def O(F, anc='rt', dx=-6, dy=4):
    F.pt((0, 0), 'O', anc, dx, dy)

def branch(F, f, a, b, ylo, yhi, wd=3.2, extra=''):
    pts, seg = [], []
    n = 300
    for i in range(n + 1):
        x = a + (b - a) * i / n
        y = f(x)
        if ylo <= y <= yhi:
            seg.append((x, y))
        elif seg:
            pts.append(seg); seg = []
    if seg:
        pts.append(seg)
    for s in pts:
        if len(s) > 1:
            F.svg.append('<polyline points="%s" fill="none" stroke="#000" stroke-width="%s" stroke-linejoin="round" %s/>'
                         % (" ".join("%.1f,%.1f" % F.P(*p) for p in s), wd, extra))

def hyper(F, h, k, c, x0, x1, y0, y1, dom=None):
    f = lambda x: k + c / (x - h)
    eps = 1e-3
    for a, b in ((x0, h - eps), (h + eps, x1)):
        if dom is None:
            branch(F, f, a, b, y0, y1)
        else:
            lo, hi = max(a, dom[0]), min(b, dom[1])
            if lo < hi:
                branch(F, f, lo, hi, y0, y1)
                if a < lo: branch(F, f, a, lo, y0, y1, 1.5, DASH)
                if hi < b: branch(F, f, hi, b, y0, y1, 1.5, DASH)
            else:
                branch(F, f, a, b, y0, y1, 1.5, DASH)

def f29():
    k = 3.2
    F = Frame((-2.2, 4.4), (-1.0, 4.2), 60, 60, (14, 14, 14, 14))
    F.poly([(-1, 1), (k, 1), (k, k), (-1, k)], SKY)
    F.axes(); O(F)
    for x in (-1, k):
        F.seg((x, -0.9), (x, 4.0), 2.4)
    for y in (1, k):
        F.seg((-2.1, y), (4.2, y), 2.4)
    F.lab((-1, 0), '-1', 'rt', -6, 6); F.lab((k, 0), 'k', 'lt', 6, 6)
    F.lab((0, 1), '1', 'lt', 6, 6); F.lab((0, k), 'k', 'lb', 6, -6)
    return F.render()

def f33():
    F = Frame((-1.6, 6.2), (-4.2, 4.2), 50, 50, (14, 40, 180, 14))
    F.axes(); O(F, 'rb', -6, -4)
    F.dashed((2, -4.1), (2, 4.1)); F.dashed((-1.5, -1), (6.1, -1))
    hyper(F, 2, -1, 3, -1.5, 6.1, -4.1, 4.1)
    F.seg((-1.0, -4.0), (5.8, 2.8), 2.0)
    dot(F, (2, -1))
    F.lab((2, 0), '2', 'lb', 4, -4); F.lab((0, -1), '-1', 'rt', -6, 4)
    F.lab((2.4, 3.8), 'y=\\frac{-x+5}{x-2}', 'lc', 8, 0)
    F.lab((5.8, 2.8), 'y=mx+n', 'lc', 6, 0)
    return F.render()

def f35():
    F = Frame((-5.2, 3.2), (-4.2, 4.2), 50, 50, (14, 14, 14, 14))
    F.axes(); O(F, 'lb', 4, -4)
    F.dashed((-2, -4.1), (-2, 4.1)); F.dashed((-5.1, 1), (3.1, 1))
    hyper(F, -2, 1, -3, -5.1, 3.1, -4.1, 4.1, dom=(-1, 1))
    for p in ((-1, -2), (1, 0)):
        dot(F, p)
    F.dashed((-1, -2), (-1, 0)); F.dashed((-1, -2), (0, -2))
    F.lab((-2, 0), '-2', 'rt', -4, 4); F.lab((-1, 0), '-1', 'cb', 0, -6); F.lab((1, 0), '1', 'ct', 0, 8)
    F.lab((0, 1), '1', 'lb', 6, -4); F.lab((0, -2), '-2', 'lc', 6, 0)
    F.lab((1.2, -3.0), 'y=\\frac{x-1}{x+2}', 'lc', 0, 0)
    return F.render()

def f36a():   # 0<a<2 (a=1): y=2/(x+1)+2
    F = Frame((-3.6, 3.4), (-1.2, 5.6), 55, 55, (14, 14, 14, 14))
    F.axes(); O(F)
    F.dashed((-1, -1.1), (-1, 5.5)); F.dashed((-3.5, 2), (3.3, 2))
    hyper(F, -1, 2, 2, -3.5, 3.3, -1.1, 5.5, dom=(0, 2))
    for p in ((0, 4), (2, 2 + 2 / 3)):
        dot(F, p)
    F.dashed((2, 2 + 2 / 3), (2, 0))
    F.lab((0, 4), '\\frac{4}{a}', 'lb', 6, -2); F.lab((0, 2), '2', 'rb', -6, -4)
    F.lab((-1, 0), '-a', 'rt', -4, 4); F.lab((2, 0), '2', 'ct', 0, 8)
    F.lab((0.5, 5.0), 'y=\\frac{2x+4}{x+a}', 'lc', 8, 0)
    return F.render()

def f36b():   # a>2 (a=6): y=2-8/(x+6)
    F = Frame((-8.6, 3.4), (-1.6, 4.2), 40, 60, (14, 14, 14, 14))
    F.axes(); O(F, 'lt', 4, 4)
    F.dashed((-6, -1.5), (-6, 4.1)); F.dashed((-8.5, 2), (3.3, 2))
    hyper(F, -6, 2, -8, -8.5, 3.3, -1.5, 4.1, dom=(0, 2))
    for p in ((0, 2 / 3), (2, 1)):
        dot(F, p)
    F.dashed((2, 1), (2, 0)); F.dashed((2, 1), (0, 1))
    F.lab((0, 2), '2', 'lb', 6, -4); F.lab((0, 1), '1', 'rc', -6, 0)
    F.lab((-6, 0), '-a', 'rt', -4, 4); F.lab((2, 0), '2', 'ct', 0, 8)
    F.lab((-1.0, 3.3), 'y=\\frac{2x+4}{x+a}', 'rc', -6, 0)
    return F.render()

def f41():
    F = Frame((-3.6, 7.4), (-5.6, 7.4), 40, 40, (14, 14, 14, 14))
    F.axes(); O(F, 'rt', -6, 4)
    F.dashed((3, -5.5), (3, 7.3)); F.dashed((-3.5, -1), (7.3, -1))
    hyper(F, 3, -1, -9, -3.5, 7.3, -5.5, 7.3)
    F.seg((-1.1, -5.4), (2.05, 7.2), 2.0)
    dot(F, (1.5, 5))
    F.lab((3, 0), '3', 'lb', 4, -4)
    F.lab((7.3, -1), 'y=-1', 'rt', 0, 6)
    F.lab((3.2, 6.4), 'y=kx-1', 'lc', 6, 0)
    F.lab((-3.4, 5.8), 'y=-\\frac{x+6}{x-3}', 'lc', 0, 0)
    return F.render()

def f42():
    F = Frame((-4.2, 4.6), (-4.2, 4.6), 45, 45, (14, 14, 14, 14))
    F.axes(); O(F)
    F.dashed((-4.1, 1), (4.5, 1))
    hyper(F, 0, 1, -2, -4.1, 4.5, -4.1, 4.5)
    F.seg((-3.6, -2.6), (3.4, 4.4), 2.0)
    F.lab((0, 1), '1', 'rb', -6, -4); F.lab((2, 0), '2', 'ct', 4, 8)
    F.lab((3.4, 4.4), 'y=ax+1', 'rc', -8, 0)
    F.lab((4.4, -1.6), 'y=\\frac{x-2}{x}', 'rc', 0, 0)
    return F.render()

JOBS = {'29': f29, '33': f33, '35': f35, '36a': f36a, '36b': f36b, '41': f41, '42': f42}
for k in (sys.argv[2:] or JOBS):
    print(k, fit_shoot(OUT + '/c2_10_%s.png' % k, JOBS[k]))
