import sys, math
sys.path.insert(0, '/home/user/CMS/.claude/skills/math-figure-rules')
from mathfig import Frame, fit_shoot, dot, right_mark, YELLOW, DASH
OUT = sys.argv[1]
R = 1.0

def P(k):
    a = math.radians(90 - 36 * (k - 1))
    return (R * math.cos(a), R * math.sin(a))

def circle(F):
    (cx, cy) = F.P(0, 0)
    F.svg.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="#000" stroke-width="3.2"/>' % (cx, cy, R * F.sx))

def names(F):
    for k in range(1, 11):
        x, y = P(k)
        dot(F, (x, y))
        a = math.atan2(y, x)
        F.lab((x * 1.2, y * 1.2), r'\mathrm{P}_{%d}' % k, 'cc', 0, 0)
    dot(F, (0, 0))

def right_tri():
    # 37번 (2): 지름 P1P6을 빗변으로 하는 직각삼각형
    F = Frame((-1.4, 1.4), (-1.35, 1.35), 120, 120, (10, 10, 10, 10))
    circle(F)
    F.seg(P(1), P(6))
    for k in range(2, 6):
        F.seg(P(1), P(k)); F.seg(P(6), P(k))
        right_mark(F, P(k), P(1), P(6))
    names(F)
    return F.render()

def obtuse_tri():
    # 37번 (3): 둔각삼각형 예 (P1P2P5, P6P8P10)
    F = Frame((-1.4, 1.4), (-1.35, 1.35), 120, 120, (10, 10, 10, 10))
    F.poly([P(1), P(2), P(5)], YELLOW)
    F.poly([P(6), P(8), P(10)], YELLOW)
    circle(F)
    F.dashed(P(1), P(6))
    for tri in ((1, 2, 5), (6, 8, 10)):
        for i in range(3):
            F.seg(P(tri[i]), P(tri[(i + 1) % 3]))
    names(F)
    return F.render()

def tri41():
    # 41번 해설: 두 직선 AD, AF와 직선 l3로 만든 삼각형 색칠
    y = lambda py: (503 - py) / 100
    A = (7.40, y(45))
    base = {'B': 3.30, 'D': 4.50, 'E': 5.67, 'F': 6.81, 'G': 7.95, 'C': 9.12}
    F = Frame((2.6, 10.0), (-0.05, 4.75), 100, 100, (14, 40, 40, 34))
    def at(name, yy):   # 직선 A-name 위에서 높이 yy인 점
        bx = base[name]
        t = (A[1] - yy) / A[1]
        return (A[0] + (bx - A[0]) * t, yy)
    l3 = y(389)
    F.poly([A, at('D', l3), at('F', l3)], YELLOW)
    for nm, bx in base.items():
        F.seg(A, (bx, 0))
    F.seg((base['B'], 0), (base['C'], 0))
    for i, py in enumerate((158, 273, 389)):
        yy = y(py)
        L, Rr = at('B', yy), at('C', yy)
        F.seg(L, Rr)
        F.dashed((2.85, yy), L); F.dashed(Rr, (9.35, yy))
        F.lab((9.35, yy), 'l_{%d}' % (i + 1), 'lc', 10, 0)
    F.pt(A, 'A', 'cb', 0, -6)
    F.pt((base['B'], 0), 'B', 'rc', -8, 0)
    F.pt((base['C'], 0), 'C', 'lc', 8, 0)
    for nm in 'DEFG':
        F.pt((base[nm], 0), nm, 'ct', 0, 8)
    return F.render()

print('37a', fit_shoot(OUT + '/c1_13_37a.png', right_tri))
print('37b', fit_shoot(OUT + '/c1_13_37b.png', obtuse_tri))
print('41', fit_shoot(OUT + '/c1_13_41.png', tri41))
