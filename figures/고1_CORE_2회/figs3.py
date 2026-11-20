# 고1 2학기 CORE 2회 문제 그림 다시 그리기 (math-figure-rules 약속)
import math, json, sys, os
import mathfig
from mathfig import (Frame, fit_shoot, roots, dot, right_mark, dim_arc, DASH, SKY, STROKE, page)

GAP_PANEL = 36   # 여러 그래프를 나란히 둘 때 칸 사이 간격(px)


def panels(frames):
    """같은 크기로 그린 칸들을 가로로 나란히 놓는다"""
    svg, labels, x = [], [], 0
    h = max(F.h for F in frames)
    for F in frames:
        svg.append('<g transform="translate(%.1f,0)">%s</g>' % (x, "".join(F.svg)))
        labels += [(l[0] + x,) + tuple(l[1:]) for l in F.labels]
        x += F.w + GAP_PANEL
    w = int(x - GAP_PANEL)
    s = '<svg width="%d" height="%d" style="position:absolute;left:0;top:0">%s</svg>' % (w, h, "".join(svg))
    return page(s, labels, w, h), w, h


# 26번: 직각삼각형 ABC(AB=6, AC=3, A=90°) 안의 직사각형 PQRS (개형: 높이 1.6)
def fig26():
    B = (0, 0)
    tb = math.atan2(3, 6)
    A = (6 * math.cos(tb), 6 * math.sin(tb))
    C = (3 * math.sqrt(5), 0)
    h = 1.6
    P, S = (2 * h, h), (C[0] - h / 2, h)
    Q, R = (P[0], 0), (S[0], 0)
    F = Frame((-0.3, 7.1), (-0.3, 3.1), 70, 70, (30, 30, 30, 30))
    F.poly([P, Q, R, S], SKY)
    for p, q in ((A, B), (B, C), (C, A), (P, Q), (Q, R), (R, S), (S, P)):
        F.seg(p, q)
    right_mark(F, A, B, C, 0.35)
    F.pt(A, "A", "cb", 0, -8); F.pt(B, "B", "rc", -8, 0); F.pt(C, "C", "lc", 8, 0)
    F.pt(P, "P", "rb", -6, -6); F.pt(S, "S", "lb", 6, -6)
    F.pt(Q, "Q", "ct", 0, 8); F.pt(R, "R", "ct", 0, 8)
    return F.render()


# 33번: y=f(x), y=(f∘g)(x)의 그래프(문제의 값 그대로)
def fig33():
    def one(pts, name):
        F = Frame((-0.7, 5.9), (-0.7, 6.1), 46, 46, (14, 14, 14, 14))
        F.grid(range(1, 6), range(1, 6))
        F.axes()
        for p in pts:
            dot(F, p)
        F.pt((0, 0), "O", "rt", -6, 6)
        for v in range(1, 6):
            F.lab((v, 0), str(v), "ct", 0, 8); F.lab((0, v), str(v), "rc", -8, 0)
        F.lab((3, 5.6), name, "cc")
        return F
    a = one([(1, 3), (2, 1), (3, 2), (4, 5), (5, 4)], r"y=f(x)")
    b = one([(1, 4), (2, 3), (3, 5), (4, 2), (5, 1)], r"y=(f \circ g)(x)")
    return panels([a, b])


# 42번: 세 함수 f, g, h의 그래프(문제의 값 그대로)
def fig42():
    def one(pts, guides, name):
        F = Frame((-0.6, 2.8), (-0.6, 2.9), 62, 62, (14, 14, 14, 14))
        F.axes()
        for p, q in guides:
            F.dashed(p, q)
        F.polyline(pts)
        F.pt((0, 0), "O", "rt", -6, 6)
        F.lab((1, 0), "1", "ct", 0, 8); F.lab((2, 0), "2", "ct", 0, 8)
        F.lab((0, 2), "2", "rc", -8, 0)
        F.lab(name[0], name[1], "lb", 6, -4)
        return F, pts
    f, _ = one([(0, 0), (1, 2), (2, 0)], [((0, 2), (1, 2)), ((1, 2), (1, 0))], ((1, 2), r"y=f(x)"))
    g, _ = one([(0, 1), (1, 0), (2, 2)], [((0, 2), (2, 2)), ((2, 2), (2, 0))], ((2, 2), r"y=g(x)"))
    g.lab((0, 1), "1", "rc", -8, 0)
    h, _ = one([(0, 2), (1, 2), (2, 0)], [((1, 2), (1, 0))], ((1.4, 1.2), r"y=h(x)"))
    return panels([f, g, h])


# 46번: y=1/x, y=k/x (개형 k=18, 답과 다른 값), 직선 AB·CD의 기울기 -1
def fig46():
    k = 18.0
    A, B = (0.25, 4), (4, 0.25)
    C, D = (3, k / 3), (k / 3, 3)
    F = Frame((-0.9, 9.6), (-0.9, 9.0), 46, 40, (14, 14, 110, 14))
    F.axes()
    F.curve(lambda x: 1 / x, 1 / 8.4, 9.3)
    F.curve(lambda x: k / x, k / 8.4, 9.3)
    F.seg(A, B); F.seg(C, D)
    F.dashed(C, (3, 0))
    for p in (A, B, C, D):
        dot(F, p)
    F.pt((0, 0), "O", "rt", -6, 6)
    F.pt(A, "A", "lc", 8, 0); F.pt(B, "B", "lb", 4, -8); F.pt(C, "C", "lb", 6, -6); F.pt(D, "D", "lb", 6, -6)
    F.lab((3, 0), "3", "rt", -4, 6); F.lab((4, 0), "4", "lt", 4, 6)
    F.lab((7.6, 1 / 7.6), r"y=\dfrac{1}{x}", "cb", 0, -14)
    F.lab((9.3, k / 9.3), r"y=\dfrac{k}{x}", "lc", 8, 0)
    return F.render()


# 51번: y=√(5x), y=√(2x), 직선 y=k (개형 k=3, 답 k²=30과 다른 값), PQ=9 표시
def fig51():
    k = 3.0
    Q, P = (k * k / 5, k), (k * k / 2, k)
    F = Frame((-1.3, 9.8), (-1.6, 7.6), 46, 46, (14, 14, 140, 14))
    F.axes()
    F.curve(lambda x: math.sqrt(5 * x), 0, 9.6, )
    F.curve(lambda x: math.sqrt(2 * x), 0, 9.6)
    F.seg((-1.2, k), (9.6, k))
    F.pt((0, 0), "O", "rt", -6, 6)
    F.pt(Q, "Q", "rb", -6, -6); F.pt(P, "P", "lt", 4, 6)
    dim_arc(F, Q, P, "9", -1, 22)
    F.lab((9.6, math.sqrt(5 * 9.6)), r"y=\sqrt{5x}", "lc", 8, 0)
    F.lab((9.6, math.sqrt(2 * 9.6)), r"y=\sqrt{2x}", "lc", 8, 0)
    F.lab((9.6, k), r"y=k", "lc", 8, 6)
    return F.render()


# 53번: y=√(4x+8), y=√(-4x+16), 직선 y=k (개형 k=2), 직사각형 ACDB
def fig53():
    k = 2.0
    l = lambda x: math.sqrt(4 * x + 8)
    r = lambda x: math.sqrt(-4 * x + 16)
    A, B = ((k * k - 8) / 4, k), ((16 - k * k) / 4, k)
    Cc, D = (A[0], 0), (B[0], 0)
    F = Frame((-3.0, 6.4), (-1.0, 6.2), 60, 50, (14, 14, 170, 14))
    F.axes()
    F.curve(l, -2, 6.0); F.curve(r, -2.6, 4)
    F.seg((-2.9, k), (6.0, k))
    F.dashed(A, Cc); F.dashed(B, D)
    right_mark(F, Cc, A, (Cc[0] + 1, 0), 0.22)
    right_mark(F, D, B, (D[0] + 1, 0), 0.22)
    F.pt((0, 0), "O", "lt", 6, 6)
    F.pt(A, "A", "rb", -6, -6); F.pt(B, "B", "lb", 6, -6)
    F.pt(Cc, "C", "ct", 0, 8); F.pt(D, "D", "ct", 0, 8)
    F.lab((6.0, l(6.0)), r"y=\sqrt{4x+8}", "lc", 8, 0)
    F.lab((3.85, r(3.85)), r"y=\sqrt{-4x+16}", "lc", 12, 0)
    F.lab((6.0, k), r"y=k", "lc", 8, 0)
    return F.render()


FIGS = {"image4": ("fig26.png", fig26, None), "image6": ("fig33.png", fig33, 18000), "image8": ("fig42.png", fig42, 21000),
        "image9": ("fig46.png", fig46, None), "image10": ("fig51.png", fig51, None), "image11": ("fig53.png", fig53, None)}

if __name__ == "__main__":
    only = sys.argv[1:]
    widths = json.load(open("widths.json")) if os.path.exists("widths.json") else {}
    for k, (fn, f, w) in FIGS.items():
        if only and k not in only:
            continue
        widths[k] = fit_shoot(fn, f, w) if w else fit_shoot(fn, f)
    json.dump(widths, open("widths.json", "w"), indent=1)
    print(widths)
