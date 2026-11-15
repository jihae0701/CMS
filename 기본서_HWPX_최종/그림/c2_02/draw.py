import sys, math
sys.path.insert(0, '/home/user/CMS/.claude/skills/math-figure-rules')
sys.path.insert(0, '/tmp/claude-0/-home-user-CMS/7a122d51-a5b1-5def-9637-d43cb9a9b6ef/scratchpad/figw/common')
from mathfig import Frame, fit_shoot, dot, right_mark, dim_arc, SKY, DASH
from nl2 import numline2
OUT = sys.argv[1]
FILL = SKY
r5 = math.sqrt(5)

def O(F, dx=-6, dy=4):
    F.pt((0, 0), "O", "rt", dx, dy)

def circ(F, c, r, extra=''):
    X, Y = F.P(*c)
    F.svg.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="#000" stroke-width="3.2" %s/>' % (X, Y, r * F.sx, extra))

def tick(F, p, q, n=2, L=7, gap=4):
    (x1, y1), (x2, y2) = F.P(*p), F.P(*q)
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    d = math.hypot(x2 - x1, y2 - y1); ux, uy = (x2 - x1) / d, (y2 - y1) / d
    nx, ny = -uy, ux
    for i in range(n):
        o = (i - (n - 1) / 2) * gap
        cx, cy = mx + ux * o, my + uy * o
        F.svg.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#000" stroke-width="1.6"/>'
                     % (cx - nx * L, cy - ny * L, cx + nx * L, cy + ny * L))

def f17():
    O1, O2 = (0, 0), (-2, -1)
    P, Q, M = (-0.4, -2.2), (-2, 1), (-1.2, -0.6)
    F = Frame((-4.4, 2.6), (-3.4, 2.6), 60, 60, (14, 14, 14, 14))
    circ(F, O1, r5); circ(F, O2, 2)
    d = (1.6, -3.2)
    F.seg((Q[0] - 0.25 * d[0], Q[1] - 0.25 * d[1]), (P[0] + 0.25 * d[0], P[1] + 0.25 * d[1]), 2.4)
    F.seg(O1, O2, 2.0); F.seg(O1, P, 2.0)
    right_mark(F, M, O1, P, 0.16)
    tick(F, P, M); tick(F, M, Q)
    for p in (O1, O2):
        dot(F, p)
    F.pt(O1, 'O', 'lc', 8, 0)
    F.pt(O2, "O'", 'rc', -8, 0)
    F.pt(P, 'P', 'lt', 6, 4)
    F.pt(Q, 'Q', 'rb', -6, -4)
    F.pt(M, 'M', 'lc', 12, 10)
    return F.render()

def f33():
    a, b = -4.4, -1.6     # -3-√5, -3+√5 (간격은 보기 좋게)
    F = numline2(-7.4, 1.4, [(None, a, 2, ''), (b, None, 2, ''), (-6, 0, 1, '')],
                 [(-6, '-6', True), (a, '-3-\\sqrt{5}', False), (b, '-3+\\sqrt{5}', False), (0, '0', True)],
                 shade=[(-6, a, 1), (b, 0, 1)], name='k', unit=60, hstep=0.7, bottom=-1.1)
    return F.render()

def f38():
    C, A, B = (2, 2), (0, 3), (4, 1)
    P = (2 + r5 * math.cos(math.radians(62)), 2 + r5 * math.sin(math.radians(62)))
    F = Frame((-0.9, 5.4), (-0.7, 4.9), 70, 70, (90, 14, 70, 14))
    F.axes(); O(F)
    circ(F, C, r5)
    F.seg(A, B, 2.0); F.seg(A, P, 2.0); F.seg(B, P, 2.0)
    right_mark(F, P, A, B, 0.22)
    for p in (A, B, C, P):
        dot(F, p)
    F.pt(A, 'A(0,\\ 3)', 'rc', -10, -6)
    F.pt(B, 'B(4,\\ 1)', 'lt', 8, 2)
    F.lab(P, 'P(x,\\ y)', 'lb', 6, -4)
    return F.render()

def f45():
    A, B, C, P = (-2, 0), (3, 0), (7, 0), (7, 6)
    F = Frame((-3, 14), (-6.6, 7.2), 30, 30, (14, 14, 14, 14))
    F.poly([A, B, P], FILL)
    F.axes(); F.pt((0, 0), 'O', 'rt', -4, 4)
    circ(F, C, 6)
    F.seg(A, P, 2.4); F.seg(B, P, 2.4)
    F.dashed(P, C)
    right_mark(F, C, P, (0, 0), 0.6)
    dim_arc(F, C, P, '6', -1)
    for p in (A, B, C, P):
        dot(F, p)
    F.pt(A, 'A', 'cb', 0, -10); F.lab(A, '-2', 'rt', -2, 6)
    F.pt(B, 'B', 'cb', 6, -10); F.lab(B, '3', 'ct', 0, 8)
    F.lab(C, '7', 'ct', 8, 8)
    F.pt(P, 'P', 'cb', 0, -10)
    return F.render()

def f56():
    F = Frame((-1.8, 5.6), (-1.6, 9.2), 40, 40, (14, 14, 14, 14))
    F.poly([(0, 0), (4, 0), (0, 8)], FILL)
    F.axes(); O(F)
    circ(F, (1, 1), r5)
    F.seg((-0.3, 8.6), (4.4, -0.8), 2.4)
    F.dashed((1, 1), (1, 0)); F.dashed((1, 1), (0, 1))
    F.seg((1, 1), (3, 2), 1.6)
    right_mark(F, (3, 2), (1, 1), (4, 0), 0.3)
    for p in ((1, 1), (3, 2)):
        dot(F, p)
    F.lab((3, 2), '(3,\\ 2)', 'lb', 8, -2)
    F.lab((0, 8), '8', 'rc', -8, 0); F.lab((4, 0), '4', 'ct', -8, 8)
    F.lab((0, 1), '1', 'rc', -8, 0); F.lab((1, 0), '1', 'ct', 0, 8)
    return F.render()

def f59():
    F = Frame((-3.3, 4.2), (-4.8, 3.2), 56, 56, (14, 14, 200, 14))
    F.axes(); O(F, -6, 4)
    circ(F, (0, 0), r5)
    F.seg((-3.2, -0.9), (2.6, -3.8), 2.4)     # x+2y+5=0
    F.seg((0.75, -3.5), (3.6, 2.2), 2.4)      # 2x-y-5=0
    F.seg((0, 0), (2, -1), 1.6)
    right_mark(F, (2, -1), (0, 0), (3.6, 2.2), 0.22)
    F.lab((1, -0.5), '\\sqrt{5}', 'rt', -2, 6)
    dot(F, (1, -3))
    F.lab((1, -3), '(1,\\ -3)', 'lc', 12, 4)
    F.lab((2.6, -3.8), 'x+2y+5=0', 'lc', 8, 0)
    F.lab((3.6, 2.2), '2x-y-5=0', 'lc', 8, 0)
    return F.render()

def f60():
    m = 1 / math.sqrt(3)
    F = Frame((-2.8, 3.2), (-2.6, 2.6), 90, 90, (14, 14, 14, 14))
    arc = [(2 * math.cos(t), 2 * math.sin(t)) for t in [i * math.radians(24.4) / 20 for i in range(21)]]
    F.poly([(-1, 0), (2, 0)] + arc[1:] + [(1.427, 0.824)], FILL)
    arc2 = [(2 * math.cos(t), 2 * math.sin(t)) for t in [math.pi + i * math.radians(15.5) / 20 for i in range(21)]]
    F.poly([(-1, 0), (-2, 0)] + arc2[1:] + [(-1.927, -0.535)], FILL)
    F.axes(); F.pt((0, 0), 'O', 'lt', 4, 4)
    circ(F, (0, 0), 2)
    F.curve(lambda x: math.sqrt(max(0, 1 - (x - 1) ** 2)), 0, 2, 'stroke-width="3.2"')
    F.curve(lambda x: -math.sqrt(max(0, 1 - (x + 1) ** 2)), -2, 0, 'stroke-width="3.2"')
    F.curve(lambda x: -math.sqrt(max(0, 1 - (x - 1) ** 2)), 0, 2, 'stroke-width="1.5" ' + DASH)
    F.seg((-2.6, -1.6 * m), (2.9, 3.9 * m), 2.0)
    for p in ((-1, 0), (1, 0)):
        dot(F, p)
    F.lab((-1, 0), '-1', 'ct', -6, 8); F.lab((1, 0), '1', 'ct', 0, 8)
    F.lab((2.9, 3.9 * m), 'y=m(x+1)', 'rb', 0, -6)
    return F.render()

def f66():
    C, P = (1, -1), (-2, 4)
    u = (-3 / math.sqrt(34), 5 / math.sqrt(34))
    Q1 = (C[0] + 2 * u[0], C[1] + 2 * u[1]); Q = (C[0] - 2 * u[0], C[1] - 2 * u[1])
    F = Frame((-3.2, 3.8), (-3.6, 4.8), 60, 60, (14, 14, 14, 14))
    circ(F, C, 2)
    F.seg(P, Q, 2.4)
    for p in (P, C, Q1, Q):
        dot(F, p)
    dim_arc(F, Q1, C, '2', -1, bulge=12)
    dim_arc(F, C, Q, '2', -1, bulge=12)
    F.pt(P, 'P(-2,\\ 4)', 'lb', 6, -4)
    F.pt(C, 'O', 'rc', -10, 0)
    F.pt(Q1, "Q'", 'rc', -10, 0)
    F.pt(Q, 'Q', 'lt', 6, 4)
    return F.render()

JOBS = {'17': f17, '33': f33, '38': f38, '45': f45, '56': f56, '59': f59, '60': f60, '66': f66}
for k in (sys.argv[2:] or JOBS):
    print(k, fit_shoot(OUT + '/c2_02_%s.png' % k, JOBS[k]))
