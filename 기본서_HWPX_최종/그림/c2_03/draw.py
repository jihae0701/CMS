import sys
sys.path.insert(0, '/home/user/CMS/.claude/skills/math-figure-rules')
from mathfig import Frame, fit_shoot, SKY
OUT = sys.argv[1]

def f40():
    F = Frame((-5.4, 5.6), (-3.2, 3.4), 50, 50, (14, 14, 14, 14))
    P = [(4, 0), (0, 2), (-4, 0), (0, -2)]
    F.poly(P, SKY)
    F.axes(); F.pt((0, 0), 'O', 'rt', -6, 4)
    for i in range(4):
        F.seg(P[i], P[(i + 1) % 4], 3.2)
    F.lab((4, 0), '4', 'lt', 4, 4); F.lab((-4, 0), '-4', 'rt', -4, 4)
    F.lab((0, 2), '2', 'lb', 6, -4); F.lab((0, -2), '-2', 'lt', 6, 4)
    return F.render()

if len(sys.argv) < 3:
    print('40', fit_shoot(OUT + '/c2_03_40.png', f40))

# ---- 화면 캡처 그림 다시 그리기 (15·16·17·24·36번)
import math
from mathfig import dot, right_mark, DASH

def tick(F, p, q, n=2, L=6, gap=4):
    (x1, y1), (x2, y2) = F.P(*p), F.P(*q)
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    d = math.hypot(x2 - x1, y2 - y1); ux, uy = (x2 - x1) / d, (y2 - y1) / d
    for i in range(n):
        o = (i - (n - 1) / 2) * gap
        cx, cy = mx + ux * o, my + uy * o
        F.svg.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#000" stroke-width="1.6"/>' % (cx + uy * L, cy - ux * L, cx - uy * L, cy + ux * L))

def arc(F, c, r, t0, t1, wd=3.2):
    n = 80
    pts = [(c[0] + r * math.cos(math.radians(t0 + (t1 - t0) * i / n)), c[1] + r * math.sin(math.radians(t0 + (t1 - t0) * i / n))) for i in range(n + 1)]
    F.svg.append('<polyline points="%s" fill="none" stroke="#000" stroke-width="%s"/>' % (" ".join("%.1f,%.1f" % F.P(*p) for p in pts), wd))

def mirror(F, P, a, b, c):
    d = (a * P[0] + b * P[1] + c) / (a * a + b * b)
    return (P[0] - 2 * d * a, P[1] - 2 * d * b)

def g15():
    A, B, A1, P = (1, 2), (3, 4), (2, 1), (2.5, 2.5)
    F = Frame((-0.6, 5.0), (-0.6, 5.0), 70, 70, (24, 24, 24, 24))
    F.axes(); F.pt((0, 0), 'O', 'lt', 4, 4)
    F.seg((-0.4, -0.4), (4.6, 4.6), 2.0); F.lab((4.6, 4.6), 'y=x', 'rc', -8, -6)
    F.seg(A, P, 3.2); F.seg(P, B, 3.2); F.seg(A1, P, 2.0)
    F.dashed(A, A1); right_mark(F, (1.5, 1.5), A, P, 0.15); tick(F, A, (1.5, 1.5), 1); tick(F, (1.5, 1.5), A1, 1)
    tick(F, A, P, 2); tick(F, A1, P, 2)
    for p in (A, B, A1, P):
        dot(F, p)
    F.pt(A, 'A(1,\\ 2)', 'rc', -8, 0); F.pt(B, 'B(3,\\ 4)', 'rc', -8, 0)
    F.pt(A1, "A'(2,\\ 1)", 'lt', 6, 4); F.pt(P, 'P', 'lc', 8, 4)
    return F.render()

def dshape(F, c):   # 중심 c, 반지름 1의 왼쪽 반원 + 오른쪽 지름(세로)
    arc(F, c, 1, 90, 270); F.seg((c[0], c[1] + 1), (c[0], c[1] - 1), 3.2)

def g16():
    F = Frame((-1.0, 2.2), (-1.6, 1.8), 80, 80, (24, 24, 24, 24))
    F.axes(); F.pt((0, 0), 'O', 'rt', -6, 4)
    dshape(F, (1, 0))
    F.dashed((1, 1), (0, 1)); F.dashed((1, -1), (0, -1))
    F.lab((0, 1), '1', 'rc', -6, 0); F.lab((0, -1), '-1', 'rc', -6, 0); F.lab((1, 0), '1', 'lt', 6, 4)
    return F.render()

def g17s():
    F = Frame((-2.6, 8.4), (-2.4, 2.8), 90, 90, (24, 24, 24, 24))
    def ax(ox):
        F.svg.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#000" stroke-width="2" marker-end="url(#ar)"/>' % (F.P(ox - 1.7, 0) + F.P(ox + 2.3, 0)))
        F.svg.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#000" stroke-width="2" marker-end="url(#ar)"/>' % (F.P(ox, -1.6) + F.P(ox, 2.4)))
        F.lab((ox + 2.3, 0), 'x', 'rt', 0, 4); F.lab((ox, 2.4), 'y', 'rt', -6, 2); F.pt((ox, 0), 'O', 'rt', -4, 4)
        F.lab((ox - 1, 0), '-1', 'rt', -4, 4); F.lab((ox, 1), '1', 'lc', 6, 0); F.lab((ox, -1), '-1', 'lc', 6, 0)
    ax(0)
    dshape(F, (1, 0)); dshape(F, (0, 0))
    F.lab((1, 0), '1', 'lt', 6, 4)
    F.lab((1.3, 1.3), 'f(x,\\ y)=0', 'lb', 0, 0)
    F.lab((-0.6, -1.4), 'f(x+1,\\ y)=0', 'ct', 0, 4)
    F.lab((3.0, 0.6), '\\Rightarrow', 'cc')
    ax(5.4)
    dshape(F, (5.4, 0))
    F.lab((5.4, -1.4), 'f(x+1,\\ -y)=0', 'ct', 0, 4)
    return F.render()

def choice(kind):
    xr, yr = {1: ((-1.8, 1.4), (-1.6, 1.8)), 2: ((-1.8, 1.4), (-1.6, 1.8)), 3: ((-1.8, 1.8), (-0.8, 1.8)),
              4: ((-0.8, 2.6), (-0.6, 1.8)), 5: ((-2.6, 0.8), (-0.6, 1.8))}[kind]
    F = Frame(xr, yr, 80, 80, (24, 24, 24, 24))
    F.axes(); F.pt((0, 0), 'O', 'rt', -4, 4)
    if kind == 1:
        dshape(F, (0, 0)); F.lab((-1, 0), '-1', 'rt', -6, 4); F.lab((0, 1), '1', 'lc', 6, -4); F.lab((0, -1), '-1', 'lc', 6, 4)
    if kind == 2:
        arc(F, (-1, 0), 1, -90, 90); F.seg((-1, 1), (-1, -1), 3.2)
        F.dashed((-1, 1), (0, 1)); F.dashed((-1, -1), (0, -1))
        F.lab((-1, 0), '-1', 'rt', -6, 4); F.lab((0, 1), '1', 'lc', 6, 0); F.lab((0, -1), '-1', 'lc', 6, 0)
    if kind == 3:
        arc(F, (0, 0), 1, 0, 180); F.seg((-1, 0), (1, 0), 3.2)
        F.lab((-1, 0), '-1', 'ct', 0, 8); F.lab((1, 0), '1', 'ct', 0, 8); F.lab((0, 1), '1', 'rb', -6, -4)
    if kind == 4:
        arc(F, (1, 1), 1, 180, 360); F.seg((0, 1), (2, 1), 3.2); F.dashed((2, 1), (2, 0))
        F.lab((1, 0), '1', 'ct', 0, 8); F.lab((2, 0), '2', 'ct', 0, 8); F.lab((0, 1), '1', 'rc', -6, 0)
    if kind == 5:
        arc(F, (-1, 1), 1, 180, 360); F.seg((-2, 1), (0, 1), 3.2); F.dashed((-2, 1), (-2, 0))
        F.lab((-1, 0), '-1', 'ct', 0, 8); F.lab((-2, 0), '-2', 'ct', 0, 8); F.lab((0, 1), '1', 'lc', 6, 0)
    return F.render()

def g24():
    P = (-1.0, 7 / 3)
    Q = mirror(None, P, 1, 4, -5); M = ((P[0] + Q[0]) / 2, (P[1] + Q[1]) / 2)
    F = Frame((-3.6, 4.6), (-0.6, 3.2), 90, 90, (24, 24, 24, 24))
    l1 = lambda x: (5 - 2 * x) / 3; l2 = lambda x: (5 - x) / 4
    v = (3.588, 0.353); l3 = lambda x: 1 + v[1] / v[0] * (x - 1)
    F.seg((-1.5, l1(-1.5)), (2.4, l1(2.4)), 2.4); F.seg((-2.0, l2(-2.0)), (4.4, l2(4.4)), 2.0); F.seg((-2.0, l3(-2.0)), (4.4, l3(4.4)), 2.4)
    F.seg(P, Q, 1.6); right_mark(F, M, P, (4.4, l2(4.4)), 0.12); tick(F, P, M, 2); tick(F, M, Q, 2)
    dot(F, P); dot(F, Q)
    F.pt(P, 'P(\\mathit{x},\\ \\mathit{y})', 'rc', -8, 0); F.pt(Q, "Q(\\mathit{x'},\\ \\mathit{y'})", 'rt', -4, 6)
    F.lab((-1.5, l1(-1.5)), '2x+3y=5', 'lb', 6, -4); F.lab((4.4, l2(4.4)), 'x+4y=5', 'rt', 0, 6)
    return F.render()

def g36():
    A, B = (1, 5), (4, 10)
    A1 = (3, 3); P = (10 / 3, 16 / 3)
    F = Frame((-0.8, 8.6), (-0.8, 11.0), 50, 50, (24, 24, 24, 24))
    F.axes(); F.pt((0, 0), 'O', 'rt', -6, 4)
    F.seg((-0.7, 1.3), (6.0, 8.0), 2.0); F.lab((6.0, 8.0), 'y=x+2', 'lc', 8, 0)
    F.seg(A, P, 3.2); F.seg(P, B, 3.2); F.seg(A1, P, 2.0); F.dashed(A, A1)
    M = (2, 4); right_mark(F, M, A, (6.0, 8.0), 0.3); tick(F, A, M, 1); tick(F, M, A1, 1)
    tick(F, A, P, 2); tick(F, A1, P, 2)
    for p in (A, B, A1, P):
        dot(F, p)
    F.pt(A, 'A(1,\\ 5)', 'cb', 0, -10); F.pt(B, 'B(4,\\ 10)', 'lc', 8, 0)
    F.pt(A1, "A'(3,\\ 3)", 'lt', 6, 4); F.pt(P, 'P', 'lc', 8, 0)
    return F.render()

JOBS2 = {'15': g15, '16q': g16, '17s': g17s, '17c1': lambda: choice(1), '17c2': lambda: choice(2), '17c3': lambda: choice(3),
         '17c4': lambda: choice(4), '17c5': lambda: choice(5), '24': g24, '36': g36}
if len(sys.argv) > 2 and sys.argv[2] == 'cap':
    for k in JOBS2:
        print(k, fit_shoot(OUT + '/c2_03_%s.png' % k, JOBS2[k]))
