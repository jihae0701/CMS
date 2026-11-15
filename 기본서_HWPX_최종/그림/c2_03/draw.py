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

print('40', fit_shoot(OUT + '/c2_03_40.png', f40))
