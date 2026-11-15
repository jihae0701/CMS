import sys
sys.path.insert(0, '/home/user/CMS/.claude/skills/math-figure-rules')
from mathfig import Frame, fit_shoot, dot
OUT = sys.argv[1]

def f1():  # f(x)=(x+1)(x-2), g(x)=-(x+1)(x-4), x=-1, 3에서 만남
    F = Frame((-2.3, 5.3), (-5.0, 7.4), 44, 30, (16, 16, 110, 16))
    F.axes()
    f = lambda x: (x + 1) * (x - 2); g = lambda x: -(x + 1) * (x - 4)
    F.curve(f, -1.95, 3.45); F.curve(g, -1.55, 4.75)
    F.dashed((3, 4), (3, 0)); dot(F, (3, 4))
    F.pt((0, 0), "O", "rt", -6, 4)
    F.lab((-1, 0), '-1', 'rt', -6, 6)
    for x, l in ((2, '2'), (3, '3'), (4, '4')):
        F.lab((x, 0), l, 'ct', 0, 8)
    F.lab((3.45, f(3.45)), r"y=f(x)", "lc", 8, 6)
    F.lab((4.75, g(4.75)), r"y=g(x)", "lc", 8, 0)
    return F.render()

def f2():  # y=ax^2+bx+c (근 -2, 3), y=mx+n (x=-2, 4에서 만남)
    F = Frame((-3.6, 5.6), (-3.8, 5.8), 40, 40, (16, 16, 190, 16))
    F.axes()
    p = lambda x: 0.5 * (x + 2) * (x - 3); l = lambda x: 0.5 * (x + 2)
    F.curve(p, -3.2, 4.5)
    F.seg((-3.4, l(-3.4)), (5.3, l(5.3)), 2.0)
    F.dashed((4, 3), (4, 0)); dot(F, (4, 3))
    F.pt((0, 0), "O", "rt", -6, 4)
    for x, lab in ((-2, '-2'), (3, '3'), (4, '4')):
        F.lab((x, 0), lab, 'ct', 0, 8)
    F.lab((4.5, p(4.5)), r"y=ax^2+bx+c", "lc", 8, 6)
    F.lab((5.3, l(5.3)), r"y=mx+n", "lc", 8, 0)
    return F.render()

def f24():  # y=f(x) (위로 볼록), y=x+1, 교점 (2, 3), (7, 8)
    F = Frame((-1.2, 10.4), (-3.4, 13.6), 28, 20, (16, 16, 120, 16))
    F.axes()
    f = lambda x: x + 1 - (x - 2) * (x - 7)
    F.curve(f, 1.0, 8.8)
    F.seg((-1.0, 0.0), (9.6, 10.6), 2.0)
    for (x, y) in ((2, 3), (7, 8)):
        dot(F, (x, y)); F.dashed((x, y), (x, 0)); F.dashed((x, y), (0, y))
        F.lab((x, 0), str(x), 'ct', 0, 8); F.lab((0, y), str(y), 'rc', -8, 0)
    F.pt((0, 0), "O", "rt", -6, 4)
    F.lab((9.6, 10.6), r"y=x+1", "lc", 8, 0)
    F.lab((8.8, f(8.8)), r"y=f(x)", "lc", 8, 4)
    return F.render()

def f26():  # y=f(x), x절편 -4, 1
    F = Frame((-5.6, 2.8), (-3.6, 6.4), 40, 40, (16, 16, 110, 16))
    F.axes()
    f = lambda x: 0.5 * (x + 4) * (x - 1)
    F.curve(f, -5.2, 2.1)
    F.pt((0, 0), "O", "rt", -6, 4)
    F.lab((-4, 0), '-4', 'ct', -6, 8); F.lab((1, 0), '1', 'ct', 6, 8)
    F.lab((2.1, f(2.1)), r"y=f(x)", "lc", 8, 0)
    return F.render()

for k, fn in (('1', f1), ('2', f2), ('24', f24), ('26', f26)):
    print(k, '폭', fit_shoot(OUT + '/c1_10_%s.png' % k, fn))
