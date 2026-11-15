import sys
sys.path.insert(0, '/home/user/CMS/.claude/skills/math-figure-rules')
from mathfig import Frame, fit_shoot
OUT = sys.argv[1]

def tree():
    # 26번: a1, a2, a3, a4 가 각각 1, 2, 3, 4 가 아닌 경우(9가지)
    F = Frame((-0.4, 3.4), (0.3, 10.2), 120, 40, (16, 10, 16, 10))
    nodes = {}
    def N(key, x, y, lab):
        nodes[key] = (x, y); F.lab((x, y), lab, 'cc')
    def E(a, b):
        (x1, y1), (x2, y2) = nodes[a], nodes[b]
        F.seg((x1 + 0.13, y1), (x2 - 0.13, y2), 1.6)
    for i, t in enumerate(['a_1', 'a_2', 'a_3', 'a_4']):
        F.lab((i, 9.75), t, 'cc')
    rows = [  # (a1, y1, [(a2, y2, [(a3, y3, a4)])])
        ('2', 8, [('1', 9, [('4', 9, '3')]), ('3', 8, [('4', 8, '1')]), ('4', 7, [('1', 7, '3')])]),
        ('3', 5, [('1', 6, [('4', 6, '2')]), ('4', 4.5, [('1', 5, '2'), ('2', 4, '1')])]),
        ('4', 2, [('1', 3, [('2', 3, '3')]), ('3', 1.5, [('1', 2, '2'), ('2', 1, '1')])]),
    ]
    for a1, y1, kids in rows:
        k1 = 'n' + a1; N(k1, 0, y1, a1)
        for a2, y2, gk in kids:
            k2 = k1 + a2 + str(y2); N(k2, 1, y2, a2); E(k1, k2)
            for a3, y3, a4 in gk:
                k3 = k2 + a3 + str(y3); N(k3, 2, y3, a3); E(k2, k3)
                k4 = k3 + a4; N(k4, 3, y3, a4); E(k3, k4)
    return F.render()

print('폭', fit_shoot(OUT + '/c1_12_26.png', tree))
