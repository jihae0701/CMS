import sys, math
sys.path.insert(0, '/home/user/CMS/.claude/skills/math-figure-rules')
from mathfig import Frame, fit_shoot, dot, right_mark, dim_arc, SKY, YELLOW, DASH
OUT = sys.argv[1]
FILL = SKY

def O(F, dx=-6, dy=4):
    F.pt((0, 0), "O", "rt", dx, dy)

def tick(F, p, q, n=2, L=7, gap=4):
    (x1, y1), (x2, y2) = F.P(*p), F.P(*q)
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    d = math.hypot(x2 - x1, y2 - y1); ux, uy = (x2 - x1) / d, (y2 - y1) / d
    nx, ny = -uy, ux
    for i in range(n):
        o = (i - (n - 1) / 2) * gap
        cx, cy = mx + ux * o, my + uy * o
        F.svg.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#000" stroke-width="1.6"/>'
                     % (cx - nx * L + ux * 2, cy - ny * L + uy * 2, cx + nx * L - ux * 2, cy + ny * L - uy * 2))

def foot(A, B, C):
    bx, by = C[0] - B[0], C[1] - B[1]
    t = ((A[0] - B[0]) * bx + (A[1] - B[1]) * by) / (bx * bx + by * by)
    return (B[0] + t * bx, B[1] + t * by)

def tri_h(F, A, B, C, k=0.18):
    H = foot(A, B, C)
    F.poly([A, B, C], FILL)
    F.seg(A, H, 1.6)
    right_mark(F, H, A, C, k)
    return H

def f25():
    A, B, C = (0, 3), (1, -1), (-3, 1)
    F = Frame((-4, 2.3), (-2, 4), 60, 60, (90, 14, 90, 14))
    F.axes(); F.pt((0, 0), 'O', 'lb', 4, -4)
    H = tri_h(F, A, B, C)
    for p, q in ((A, B), (B, C), (C, A)):
        F.seg(p, q, 3.2)
    for p in (A, B, C):
        dot(F, p)
    F.lab(((A[0] + H[0]) / 2, (A[1] + H[1]) / 2), 'h', 'rc', -6, 0)
    F.pt(A, 'A(0,\\ 3)', 'lc', 10, -8)
    F.pt(B, 'B(1,\\ -1)', 'lt', 6, 6)
    F.pt(C, 'C(-3,\\ 1)', 'rb', -4, -6)
    return F.render()

def f26():
    A, B, C = (1, 5), (-4, 0), (5, 3)
    F = Frame((-5.3, 8.5), (-1.2, 7.4), 50, 64, (100, 14, 200, 14))
    F.axes(); O(F)
    H = tri_h(F, A, B, C, 0.4)
    F.seg((-5, -1), (3, 7), 2.0)          # x-y+4=0
    F.seg((-5.2, -0.4), (8.5, 4.1667), 2.0)          # x-3y+4=0
    F.seg((-1.5, 6.25), (8.5, 1.25), 2.0)           # x+2y-11=0
    for p in (A, B, C):
        dot(F, p)
    F.lab(((A[0] + H[0]) / 2, (A[1] + H[1]) / 2), 'h', 'rc', -6, 0)
    F.pt(A, 'A(1,\\ 5)', 'lc', 18, -3)
    F.pt(B, 'B(-4,\\ 0)', 'rb', -6, -6)
    F.pt(C, 'C(5,\\ 3)', 'ct', 0, 10)
    F.lab((3, 7), 'x-y+4=0', 'lc', 6, 0)
    F.lab((8.5, 4.1667), 'x-3y+4=0', 'lc', 6, 0)
    F.lab((8.5, 1.25), 'x+2y-11=0', 'lc', 6, 0)
    return F.render()

def f33(sol):
    c, A = 2.5, (2.1, 3.2)
    B, C = (-c, 0), (c, 0)
    F = Frame((-3.6, 4.2), (-0.9, 4.3), 60, 60, (14, 14, 14, 14))
    F.axes()
    for p, q in ((B, A), (A, C), ((0, 0), A)):
        F.seg(p, q, 3.2)
    F.seg(B, C, 3.2)
    F.pt(A, 'A(\\mathit{a},\\ \\mathit{b})', 'lb', 4, -6)
    if sol:
        F.pt(B, 'B(-\\mathit{c},\\ 0)', 'ct', 0, 10)
        F.pt(C, 'C(\\mathit{c},\\ 0)', 'lb', 4, -6)
        F.pt((0, 0), 'O', 'rt', -6, 6)
        F.pt((0, 0), 'M(0,\\ 0)', 'lt', 6, 6)
    else:
        tick(F, B, (0, 0)); tick(F, (0, 0), C)
        F.pt(B, 'B(-\\mathit{c},\\ 0)', 'ct', 0, 10)
        F.pt(C, 'C', 'ct', 0, 10)
        F.pt((0, 0), 'O', 'rt', -6, 6); F.pt((0, 0), '(M)', 'lt', 4, 6)
    return F.render()

def f34(sol):
    B, D = (1, 3), (7, 11)
    u = (0.6, 0.8); n = (-0.8, 0.6)
    A = (B[0] + 3.8 * u[0] + 3.25 * n[0], B[1] + 3.8 * u[1] + 3.25 * n[1])
    C = (B[0] + D[0] - A[0], B[1] + D[1] - A[1])
    M = ((B[0] + D[0]) / 2, (B[1] + D[1]) / 2)
    F = Frame((-2.6, 9.6), (-0.8, 12.2), 34, 34, (14, 14, 70, 14))
    F.axes(); O(F)
    for p, q in ((A, B), (B, C), (C, D), (D, A), (A, C)):
        F.seg(p, q, 3.2)
    if sol:
        F.seg(B, D, 2.0)
        dot(F, M)
        tick(F, A, M); tick(F, M, C)
        F.pt(M, 'M', 'cb', 0, -10)
    dim_arc(F, B, A, '5', -1)
    dim_arc(F, B, C, '7', 1)
    for p in (B, D):
        dot(F, p)
    F.pt(A, 'A', 'rb', -4, -4)
    F.pt(C, 'C', 'lc', 8, 0)
    F.pt(B, 'B(1,\\ 3)', 'ct', 0, 10)
    F.pt(D, 'D(7,\\ 11)', 'lc', 8, 0)
    return F.render()

def f44():
    A, B, C = (2, 2), (5, 8), (7, 12)
    F = Frame((0.5, 13), (1, 13.5), 34, 34, (14, 14, 14, 14))
    F.seg(A, C, 2.0)
    for p in (A, B, C):
        dot(F, p)
    dim_arc(F, A, C, '5', 1, bulge=125)
    dim_arc(F, A, B, '3', -1)
    dim_arc(F, B, C, '2', -1)
    F.pt(A, 'A(2,\\ 2)', 'lc', 10, 4)
    F.pt(B, 'B(5,\\ 8)', 'lc', 12, 4)
    F.pt(C, 'C(\\mathit{a},\\ \\mathit{b})', 'lc', 10, 0)
    return F.render()

def f46():
    F = Frame((-3.6, 7.6), (-6, 42), 40, 6.2, (160, 14, 40, 14))
    F.axes(); O(F)
    F.curve(lambda x: x * x, -3.4, 6.55, 'stroke-width="3.2"')
    F.seg((-3.2, -0.8), (7.2, 40.8), 2.0)
    for p in ((-2, 4), (6, 36), (0, 12)):
        dot(F, p)
    F.pt((-2, 4), 'A', 'rb', -8, -2)
    F.pt((6, 36), 'B', 'rc', -10, 0)
    F.pt((0, 12), 'P', 'rc', -8, 0)
    F.lab((4.6, 21.16), 'y=x^2', 'lc', 10, 0)
    F.lab((-3.2, -0.8), 'y=ax+12', 'rc', -8, 0)
    return F.render()

def f50():
    P, Q, R = (3, 7), (1, 1), (9, 3)
    A, B, C = (2, 4), (6, 5), (5, 2)
    l = lambda x: x / 4 + 3.5
    F = Frame((-0.8, 11.5), (-0.9, 8.3), 48, 48, (14, 14, 30, 14))
    F.axes(); O(F)
    F.seg((-0.5, l(-0.5)), (11, l(11)), 3.2)
    F.lab((11, l(11)), 'l', 'lc', 8, 0)
    for p, q in ((P, Q), (P, R), (Q, R), (A, C), (B, C)):
        F.seg(p, q, 2.0)
    for X in (P, Q, R):
        H = foot(X, (0, 3.5), (4, 4.5))
        F.seg(X, H, 1.6, DASH)
        right_mark(F, H, X, (11, l(11)) if X != R else (0, 3.5), 0.22)
        tick(F, X, H, 1)
        nm = {P: "P'", Q: "Q'", R: "R'"}[X]
        F.pt(H, nm, 'lt' if X == P else 'rb' if X == Q else 'lb', 4 if X != Q else -4, 4 if X == P else -4)
    for p in (P, Q, R, A, B, C):
        dot(F, p)
    tick(F, Q, C, 2); tick(F, C, R, 2)
    F.pt(P, 'P(3,\\ 7)', 'cb', 0, -8)
    F.pt(Q, 'Q(1,\\ 1)', 'lt', 8, 2)
    F.pt(R, 'R(9,\\ 3)', 'lt', 6, 4)
    F.pt(A, 'A', 'rb', -8, -6)
    F.pt(B, 'B', 'cb', 0, -10)
    F.pt(C, 'C', 'ct', 0, 8)
    return F.render()

def f52():
    A, B, C, D = (0, 3), (-1, 1), (3, 2), (4, 4)
    F = Frame((-2, 5.2), (-0.8, 5), 60, 60, (14, 14, 14, 14))
    F.poly([A, B, C, D], FILL)
    F.axes(); O(F)
    for p, q in ((A, B), (B, C), (C, D), (D, A)):
        F.seg(p, q, 3.2)
    for (x, y) in (B, C, D):
        F.dashed((x, y), (x, 0)); F.dashed((x, y), (0, y))
    for p in (A, B, C, D):
        dot(F, p)
    F.lab((-1, 0), '-1', 'ct', 0, 8); F.lab((3, 0), '3', 'ct', 0, 8); F.lab((4, 0), '4', 'ct', 0, 8)
    F.lab((0, 1), '1', 'lc', 6, 6); F.lab((0, 2), '2', 'rc', -6, 0); F.lab((0, 4), '4', 'rc', -6, 0)
    F.pt(A, 'A', 'rc', -8, 0)
    F.pt(B, 'B', 'rc', -8, 0)
    F.pt(C, 'C', 'lt', 6, 4)
    F.pt(D, 'D', 'lb', 6, -4)
    return F.render()

JOBS = {'25': f25, '26': f26, '33q': lambda: f33(False), '33s': lambda: f33(True), '34q': lambda: f34(False),
        '34s': lambda: f34(True), '44': f44, '46': f46, '50s': f50, '52': f52}
for k in (sys.argv[2:] or JOBS):
    print(k, fit_shoot(OUT + '/c2_01_%s.png' % k, JOBS[k]))
