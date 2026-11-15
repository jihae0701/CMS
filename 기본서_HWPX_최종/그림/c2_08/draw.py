import sys, math
sys.path.insert(0, '/home/user/CMS/.claude/skills/math-figure-rules')
from mathfig import Frame, fit_shoot, DASH
OUT = sys.argv[1]

def arrow(F, p, q, wd=2.0):
    F.svg.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#000" stroke-width="%s" marker-end="url(#ar)"/>' % (F.P(*p) + F.P(*q) + (wd,)))

def poly(F, pts, wd=3.2, extra=''):
    F.svg.append('<polyline points="%s" fill="none" stroke="#000" stroke-width="%s" stroke-linejoin="round" %s/>'
                 % (" ".join("%.1f,%.1f" % F.P(*p) for p in pts), wd, extra))

def f8():
    W, H = 7.4, 5.8
    F = Frame((0, 2 * W), (-3 * H, 0), 64, 64, (14, 14, 14, 14))
    def panel(k, name, draw, oanc=('rt', -4, 4)):
        i, j = divmod(k, 2)
        ox, oy = j * W + 3.7, -(i * H + 2.9)
        tr = lambda x, y: (ox + x, oy + y)
        arrow(F, tr(-3.0, 0), tr(3.0, 0)); arrow(F, tr(0, -2.5), tr(0, 2.5))
        F.lab(tr(3.0, 0), 'x', 'rt', 0, 4); F.lab(tr(0, 2.5), 'y', 'rt', -6, 2)
        F.pt(tr(0, 0), 'O', *oanc)
        F.lab(tr(-3.5, 2.5), '\\text{%s.}' % name, 'lt')
        for seg in draw():
            poly(F, [tr(x, y) for x, y in seg])
    panel(0, 'ㄱ', lambda: [[(-2.6, 0.9), (-0.9, 0.9), (0.9, -0.9), (2.2, -0.9)]])
    panel(1, 'ㄴ', lambda: [[(x / 20, 0.6 - 0.35 * math.exp(0.9 * x / 20)) for x in range(-56, 44)]])
    panel(2, 'ㄷ', lambda: [[(0.5 * (y / 20 + 0.5) ** 2 - 2.0, y / 20) for y in range(-48, 29)]])
    panel(3, 'ㄹ', lambda: [[(-1.2, 1.2), (1.9, -1.9)]])
    panel(4, 'ㅁ', lambda: [[(2.4, 0), (0, 1.5), (-2.4, 0), (0, -1.5), (2.4, 0)]], ('rt', -8, 0))
    panel(5, 'ㅂ', lambda: [[(-2.6, 1.0), (2.2, 1.0)]])
    return F.render()

def f16():
    F = Frame((-1.0, 2.2), (-0.7, 2.4), 110, 110, (40, 14, 14, 14))
    F.axes(); F.pt((0, 0), 'O', 'rt', -6, 4)
    F.curve(lambda x: x * x - x, -0.95, 1.95, 'stroke-width="3.2"')
    F.dashed((0.5, -0.25), (0.5, 0)); F.dashed((0.5, -0.25), (0, -0.25))
    F.lab((0.5, 0), '\\frac{1}{2}', 'cb', 0, -6)
    F.lab((0, -0.25), '-\\frac{1}{4}', 'rc', -36, 4)
    F.lab((1.85, 1.85 ** 2 - 1.85), 'y=x^2-x', 'rc', -12, 0)
    return F.render()

JOBS = {'8': f8, '16': f16}
for k in (sys.argv[2:] or JOBS):
    print(k, fit_shoot(OUT + '/c2_08_%s.png' % k, JOBS[k]))
