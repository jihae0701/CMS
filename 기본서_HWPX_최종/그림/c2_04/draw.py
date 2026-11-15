import sys
sys.path.insert(0, '/home/user/CMS/.claude/skills/math-figure-rules')
from mathfig import Frame, fit_shoot, dot, venn_set
OUT = sys.argv[1]

def f3():
    F = Frame((-1.4, 1.4), (-1.3, 1.4), 120, 120, (14, 14, 14, 14))
    venn_set(F, 0, 0, 1.1, 1.1, 'D')
    for (x, y), t in (((-0.4, 0.35), '2'), ((0.4, 0.35), '4'), ((-0.4, -0.4), '6'), ((0.4, -0.4), '8')):
        F.lab((x, y), t, 'cc')
    return F.render()

def f30q():
    F = Frame((-2.5, 2.5), (-1.4, 1.5), 110, 110, (14, 14, 14, 14))
    venn_set(F, -0.75, 0, 1.2, 1.2, 'A', ang=110)
    venn_set(F, 0.75, 0, 1.2, 1.2, 'B', ang=70)
    for (x, y), t in (((-1.25, 0.4), '-1'), ((-1.25, -0.4), '1'), ((0, 0), '0'), ((1.25, 0.4), '-2'), ((1.25, -0.4), '2')):
        F.lab((x, y), t, 'cc')
    return F.render()

def f30s():
    F = Frame((-2, 2.2), (-2.9, 3), 60, 60, (14, 14, 14, 14))
    F.axes(); F.pt((0, 0), 'O', 'rt', -6, 4)
    for y in (2, -2):
        F.dashed((-1, y), (1, y))
    for x in (1, -1):
        F.dashed((x, -2), (x, 2))
    for x in (-1, 0, 1):
        for y in (-2, 0, 2):
            dot(F, (x, y), 5)
    F.lab((-1, 0), '-1', 'rt', -4, 6); F.lab((1, 0), '1', 'lt', 4, 6)
    F.lab((0, 2), '2', 'rb', -6, -4); F.lab((0, -2), '-2', 'rt', -6, 6)
    return F.render()

JOBS = {'3': f3, '30q': f30q, '30s': f30s}
for k in (sys.argv[2:] or JOBS):
    print(k, fit_shoot(OUT + '/c2_04_%s.png' % k, JOBS[k]))
