import sys, math
sys.path.insert(0, '/home/user/CMS/.claude/skills/math-figure-rules')
from mathfig import Frame, fit_shoot, dot
OUT = sys.argv[1]
r2 = math.sqrt(2)

def f25():  # y=ax^2+bx+c 와 y=mx (P, Q의 x좌표 3∓√2) — y=x^2-5x+7, y=x
    F = Frame((-1.2, 7.0), (-1.6, 8.2), 34, 34, (16, 16, 90, 16))
    F.axes()
    F.curve(lambda x: x * x - 5 * x + 7, 0.25, 5.15)
    F.seg((-1.2, -1.2), (6.3, 6.3), 2.0)
    P, Q = (3 - r2, 3 - r2), (3 + r2, 3 + r2)
    dot(F, P); dot(F, Q)
    F.dashed(P, (P[0], 0))
    F.pt((0, 0), "O", "rt", -6, 4)
    F.pt(P, "P", "rb", -6, -6); F.pt(Q, "Q", "lc", 10, 2)
    F.lab((P[0], 0), r"3-\sqrt{2}", "ct", 0, 8)
    F.lab((5.15, 5.15 ** 2 - 5 * 5.15 + 7), r"y=ax^2+bx+c", "lb", -150, -2)
    F.lab((6.3, 6.3), r"y=mx", "lc", 6, 0)
    return F.render()

def f49():  # y=x^2+ax+b, x축과 A, B (A<0<B) — y=x^2-x-2
    F = Frame((-2.2, 3.4), (-2.9, 4.6), 44, 44, (16, 16, 150, 16))
    F.axes()
    F.curve(lambda x: x * x - x - 2, -1.75, 2.75)
    F.pt((0, 0), "O", "lt", 5, 4)
    F.pt((-1, 0), "A", "rt", -4, 4); F.pt((2, 0), "B", "lt", 4, 4)
    F.lab((2.75, 2.75 ** 2 - 2.75 - 2), r"y=x^2+ax+b", "lc", 6, 4)
    return F.render()

def f53():  # y=x^2+ax+48 과 y=mx, A(x=3), B(x=16) — y=x^2-18x+48, y=x
    F = Frame((-1.5, 23.0), (-36, 52), 15, 3.4, (16, 16, 160, 16))
    F.axes()
    g = lambda x: x * x - 18 * x + 48
    F.curve(g, 0.0, 17.6)
    F.seg((-1.2, -1.2), (21.0, 21.0), 2.0)
    A, B = (3, 3), (16, 16)
    dot(F, A); dot(F, B)
    F.dashed(A, (3, 0))
    F.pt((0, 0), "O", "rt", -6, 4)
    F.pt(A, "A", "rb", -6, -6); F.pt(B, "B", "rb", -8, -4)
    F.lab((3, 0), "3", "ct", 0, 8)
    F.lab((17.6, g(17.6)), r"y=x^2+ax+48", "lc", 8, 6)
    F.lab((21.0, 21.0), r"y=mx", "lc", 6, 0)
    return F.render()

def f59():  # y=|x^2-2| 와 y=-x+9/4 (접선), y=-x+√2
    F = Frame((-2.6, 3.2), (-1.8, 4.4), 52, 52, (16, 16, 150, 16))
    F.axes()
    F.curve(lambda x: abs(x * x - 2), -2.45, 2.45)
    F.seg((-2.1, 2.25 + 2.1), (2.8, 2.25 - 2.8), 2.0)
    F.seg((-2.4, r2 + 2.4), (3.0, r2 - 3.0), 2.0)
    F.pt((0, 0), "O", "rt", -6, 4)
    F.lab((-r2, 0), r"-\sqrt{2}", "ct", 0, 8); F.lab((r2, 0), r"\sqrt{2}", "rt", -6, 8)
    F.lab((0, 2), "2", "lb", 6, -4)
    dot(F, (0, 2)); dot(F, (-r2, 0)); dot(F, (r2, 0))
    F.lab((2.45, 2.45 ** 2 - 2), r"y=|x^2-2|", "lc", 8, 6)
    F.lab((2.8, 2.25 - 2.8), r"y=-x+\dfrac{9}{4}", "lc", 6, 0)
    F.lab((3.0, r2 - 3.0), r"y=-x+\sqrt{2}", "lc", 6, 0)
    return F.render()

for name, fn in (('25', f25), ('49', f49), ('53', f53), ('59', f59)):
    print(name, '폭', fit_shoot(OUT + '/c1_06_%s.png' % name, fn))
