# CORE 1회 문제·해설 그림 다시 그리기 (math-figure-rules 약속)
import math, json, sys
from mathfig import (Frame, fit_shoot, roots, dot, right_mark, dim_arc, DASH, SKY, STROKE)


def circle(F, c, r, wd=STROKE):
    (X, Y) = F.P(*c)
    F.svg.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="none" stroke="#000" stroke-width="%s"/>'
                 % (X, Y, r * F.sx, r * F.sy, wd))


def thin(F, f, a, b, n=80):
    """비교용·정의역 밖 곡선: 점선(굵기 1.5, 5,4)"""
    pts = " ".join("%.1f,%.1f" % F.P(a + (b - a) * i / n, f(a + (b - a) * i / n)) for i in range(n + 1))
    F.svg.append('<polyline points="%s" fill="none" stroke="#000" stroke-width="1.5" %s/>' % (pts, DASH))


# 3번: y=f'(x)(위로 볼록한 포물선)와 y=g'(x)(직선). 개형: f'=-(x+1)(x-3), g'=x+1 (α=-1, β=2, γ=3)
def fig03():
    fp = lambda x: -(x + 1) * (x - 3)
    gp = lambda x: x + 1
    F = Frame((-2.3, 4.6), (-2.3, 5.6), 46, 46, (110, 14, 100, 14))
    F.axes()
    F.curve(fp, roots(fp, -4, 1, -2.1)[0], roots(fp, 1, 6, -2.1)[0])
    F.seg((-2.2, gp(-2.2)), (4.3, gp(4.3)))
    F.dashed((2, 3), (2, 0))
    F.pt((0, 0), "O", "rt", -4, 4)
    F.lab((-1, 0), r"\alpha", "rb", -8, -8)
    F.lab((2, 0), r"\beta", "ct", 0, 6)
    F.lab((3, 0), r"\gamma", "lt", 6, 6)
    F.lab((4.3, gp(4.3)), r"y=g'(x)", "lc", 8, 0)
    F.lab((-0.55, fp(-0.55)), r"y=f'(x)", "rc", -16, 0)
    return F.render()


# 15번: 정사각형 ABCD(중심 (0,2)), EFGH(중심이 y=x²/2 위, 개형 t=1.5)
def fig15():
    p = lambda x: 0.5 * x * x
    t = 1.6
    cy = p(t)
    F = Frame((-2.7, 3.4), (-0.7, 4.4), 52, 52, (14, 14, 110, 14))
    F.axes()
    F.curve(p, -2.9, 2.9)
    A, B, C, D = (-1, 3), (-1, 1), (1, 1), (1, 3)
    E, Fp, G, H = (t - 1, cy + 1), (t - 1, cy - 1), (t + 1, cy - 1), (t + 1, cy + 1)
    for sq in ((A, B, C, D), (E, Fp, G, H)):
        for i in range(4):
            F.seg(sq[i], sq[(i + 1) % 4])
    F.pt((0, 0), "O", "rt", -4, 4)
    F.pt(A, "A", "rb", -6, -6); F.pt(B, "B", "rt", -6, 6); F.pt(C, "C", "lt", 4, 4); F.pt(D, "D", "lb", 4, -4)
    F.pt(E, "E", "rb", -4, -4); F.pt(Fp, "F", "rc", -8, -10); F.pt(G, "G", "lc", 14, 0); F.pt(H, "H", "lb", 4, -4)
    dim_arc(F, B, A, "2", -1, 22)
    dim_arc(F, G, H, "2", 1, 22)
    F.lab((2.9, p(2.9)), r"y=\dfrac{1}{2}x^2", "lc", 8, 6)
    return F.render()


# 40번: y=g(x)=|F(x)|, F=ax(x-1)(x-3)(x-6). 개형(세로는 |F|/(1+|F|/8)로 줄여 그림)
def fig40():
    Fx = lambda x: x * (x - 1) * (x - 3) * (x - 6)
    g = lambda x: abs(Fx(x)) / (1 + abs(Fx(x)) / 8)
    F = Frame((-0.9, 7.0), (-0.6, 7.6), 46, 28, (14, 14, 90, 14))
    F.axes()
    for a_, b_ in ((-0.62, 0), (0, 1), (1, 3), (3, 6), (6, 6.18)):
        F.curve(g, a_, b_)
    F.pt((0, 0), "O", "rt", -4, 4)
    for v in (1, 3):
        F.lab((v, 0), str(v), "ct", 0, 6)
    F.lab((6, 0), "6", "rt", -5, 6)
    F.lab((6.18, g(6.18)), r"y=g(x)", "lc", 8, 0)
    return F.render()


# 41번: 두 곡선 y=f(x), y=g(x). 개형: a=1, b=3, c=5
def fig41():
    f = lambda x: 0.2 * (x - 3) * (x - 0.5)
    g = lambda x: f(x) - 0.2 * (x - 1) * (x - 3) * (x - 5)
    F = Frame((-0.6, 7.0), (-1.8, 4.2), 52, 52, (14, 14, 100, 14))
    F.axes()
    F.curve(f, -0.4, roots(f, 4, 9, 3.4)[0])
    F.curve(g, roots(g, -1, 1, 3.4)[0], roots(g, 5, 7, -1.6)[0])
    F.dashed((5, f(5)), (5, 0))
    F.pt((0, 0), "O", "rt", -4, 4)
    F.lab((1, 0), "a", "cb", 0, -8)
    F.lab((3, 0), "b", "ct", 6, 8)
    F.lab((5, 0), "c", "ct", 0, 8)
    x1 = roots(f, 4, 9, 3.4)[0]
    F.lab((x1, 3.4), r"y=f(x)", "lc", 8, 0)
    x2 = roots(g, 5, 7, -1.6)[0]
    F.lab((x2, -1.6), r"y=g(x)", "lc", 8, 0)
    return F.render()


# 45번: 곡선 y=√x, 원 C(O, A(t²,t), B(0,t)을 지남), 넓이 S(t). 개형 t=1.5
def fig45():
    t = 1.5
    c = (t * t / 2, t / 2)
    r = math.sqrt(t ** 4 + t * t) / 2
    F = Frame((-0.7, 3.6), (-0.9, 2.6), 90, 90, (14, 14, 130, 14))
    a0 = math.atan2(t - c[1], t * t - c[0])
    a1 = math.atan2(-c[1], -c[0])
    region = [((t * i / 120) ** 2, t * i / 120) for i in range(121)]
    region += [(c[0] + r * math.cos(a0 + (a1 - a0) * k / 120), c[1] + r * math.sin(a0 + (a1 - a0) * k / 120)) for k in range(121)]
    F.poly(region, SKY)
    F.axes()
    circle(F, c, r)
    F.polyline([((math.sqrt(3.4) * i / 200) ** 2, math.sqrt(3.4) * i / 200) for i in range(201)])
    F.pt((0, 0), "O", "rt", -4, 4)
    F.pt((t * t, t), "A", "lt", 8, 2)
    F.pt((0, t), "B", "rc", -8, 0)
    F.lab((1.55, 0.45), r"S(t)", "cc")
    F.lab((3.4, math.sqrt(3.4)), r"y=\sqrt{x}", "lc", 16, 0)
    return F.render()


# 46번: y=-x²+5x+p, 직선 y=x, y축. 개형 p=-2 (답과 다른 값)
def fig46():
    p = -2
    q = lambda x: -x * x + 5 * x + p
    al, be = 2 - math.sqrt(2), 2 + math.sqrt(2)
    F = Frame((-1.2, 5.9), (-2.6, 5.4), 48, 48, (14, 14, 30, 14))
    F.poly([(0, 0), (al, al)] + [(x, q(x)) for x in [al * (60 - i) / 60 for i in range(61)]], SKY)
    F.axes()
    F.curve(q, -0.1, roots(q, 3, 7, -2.5)[0])
    F.seg((-1.1, -1.1), (5.0, 5.0))
    F.pt((0, 0), "O", "rb", -4, -4)
    F.pt((0.22, -0.55), "A", "cc", 0, 0)
    F.pt((2.0, 2.95), "B", "cc", 0, 0)
    F.lab((5.0, 5.0), r"y=x", "lc", 8, 0)
    x2 = roots(q, 3, 7, -2.5)[0]
    F.lab((x2, -2.5), r"y=-x^2+5x+p", "rc", -14, 0)
    return F.render()


# 49번: v(t) 그래프(문제의 값 그대로)
def fig49():
    pts = [(0, 0), (1, 2), (3, -2), (5, 2), (6, 2), (8, 0)]
    F = Frame((-0.7, 8.9), (-2.9, 3.1), 62, 48, (60, 14, 30, 14))
    F.axes("t", "v(t)")
    F.dashed((0, 2), (6, 2)); F.dashed((1, 2), (1, 0)); F.dashed((5, 2), (5, 0)); F.dashed((6, 2), (6, 0))
    F.dashed((0, -2), (3, -2)); F.dashed((3, -2), (3, 0))
    F.polyline(pts)
    F.pt((0, 0), "O", "rt", -4, 4)
    F.lab((0, 2), "2", "rc", -8, 0); F.lab((0, -2), "-2", "rc", -8, 0)
    for v, anc, dx in ((1, "ct", 0), (2, "lt", 6), (4, "rt", -6), (5, "ct", 0), (6, "ct", 0), (8, "ct", 0)):
        F.lab((v, 0), str(v), anc, dx, 6)
    F.lab((3, 0), "3", "cb", 0, -6)
    return F.render()


# 7번 해설 그림: y=h(x), 기준선 y=p, k=-1일 때의 모양(검은 선; 정의되지 않는 쪽은 점선)
def fig07s():
    fY = lambda x: (x + 2) * (x - 1) ** 2          # f(x)-p
    gY = lambda x: -5 * (x + 2)                    # g(x)-p
    F = Frame((-3.3, 2.5), (-3.4, 5.3), 70, 44, (110, 14, 40, 60))
    F.seg((-3.3, 0), (2.3, 0), 2.0)
    F.curve(gY, -3.0, -2)
    F.curve(fY, -2, 2.08)
    thin(F, gY, -2, -1.35)
    thin(F, fY, -2.25, -2)
    F.dashed((-1, fY(-1)), (-1, 0))
    F.lab((2.3, 0), "p", "lc", 8, 0)
    F.lab((-2, 0), "-k-3", "rt", -16, 6)
    F.lab((-1, 0), "k", "ct", 0, 6)
    F.lab((1, 0), "1", "ct", 0, 6)
    F.lab((-1, fY(-1)), r"y=h(x)", "cb", 0, -10)
    F.lab((-2.25, fY(-2.25)), r"y=f(x)", "rt", -6, 4)
    F.lab((-1.35, gY(-1.35)), r"g(x)=-5x+6", "lt", 8, 2)
    return F.render()


FIGS = {"image3": ("fig03.png", fig03), "image4": ("fig15.png", fig15), "image1": ("fig40.png", fig40),
        "image6": ("fig41.png", fig41), "image7": ("fig45.png", fig45), "image8": ("fig46.png", fig46),
        "image9": ("fig49.png", fig49), "image11": ("fig07s.png", fig07s)}

if __name__ == "__main__":
    only = sys.argv[1:]
    widths = {}
    for k, (fn, f) in FIGS.items():
        if only and k not in only:
            continue
        widths[k] = fit_shoot(fn, f)
    old = json.load(open("widths.json")) if __import__("os").path.exists("widths.json") else {}
    old.update(widths)
    json.dump(old, open("widths.json", "w"), indent=1)
    print(old)
