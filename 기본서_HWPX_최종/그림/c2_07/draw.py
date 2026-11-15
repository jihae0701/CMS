import sys, math
sys.path.insert(0, '/home/user/CMS/.claude/skills/math-figure-rules')
from mathfig import Frame, fit_shoot, right_mark, dim_arc
OUT = sys.argv[1]

def f37q():   # ∠A=∠C=90°, AB=8, AD=4
    B, C = (0, 0), (5.2, 0)
    D = (5.2, math.sqrt(80 - 5.2 ** 2))
    d = math.hypot(*D); a = (64 - 16 + d * d) / (2 * d); h = math.sqrt(64 - a * a)
    u = (D[0] / d, D[1] / d); n = (-u[1], u[0])
    A = (a * u[0] + h * n[0], a * u[1] + h * n[1])
    F = Frame((-1.6, 6.4), (-0.7, 8.6), 50, 50, (14, 14, 14, 14))
    for p, q in ((A, B), (B, C), (C, D), (D, A)):
        F.seg(p, q, 3.2)
    right_mark(F, A, B, D, 0.4); right_mark(F, C, B, D, 0.4)
    dim_arc(F, B, A, '8', -1); dim_arc(F, A, D, '4', -1)
    F.pt(A, 'A', 'rb', -6, -4); F.pt(B, 'B', 'rt', -6, 4); F.pt(C, 'C', 'lt', 6, 4); F.pt(D, 'D', 'lc', 8, 0)
    return F.render()

print('37q', fit_shoot(OUT + '/c2_07_37q.png', f37q))
