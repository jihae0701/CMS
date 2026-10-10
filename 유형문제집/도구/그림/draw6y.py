# -*- coding: utf-8 -*-
"""유형서 6단원(이차함수의 최대, 최소) 그림. python 그림/draw6y.py [파일 ...]  (KATEX_DIR 필요)
그림 속 위치는 답이 드러나지 않도록 답과 다른 값으로 그린 개형이다. 모의고사 문항은 원본 그림의 모양을 따른다.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from draw import shoot, HERE
from draw5 import Frame, roots
from draw6 import right_mark, PINK, GREEN, SKY


def dot(F, p, r=3.5):
    F.svg.append('<circle cx="%.1f" cy="%.1f" r="%s" fill="#000"/>' % (F.P(*p) + (r,)))


def fig_o44():
    # 올림포스 44번: P는 y=-x^2+5x-4 위의 제1사분면 점 (그림은 x=2.2)
    f = lambda t: -t * t + 5 * t - 4
    F = Frame((-0.9, 5.4), (-1.6, 3.2), 48, 48, (20, 12, 190, 12))
    F.axes()
    F.curve(f, roots(f, 0, 2.5, -1.5)[0], roots(f, 2.5, 6, -1.5)[0])
    px = 2.2
    P_, Q_, R_ = (px, f(px)), (px, 0), (0, f(px))
    F.seg(R_, P_); F.seg(P_, Q_)
    right_mark(F, R_, (0, 0), P_, 0.2); right_mark(F, Q_, P_, (0, 0), 0.2)
    dot(F, P_)
    F.pt((0, 0), "O", "rt", -5, 5)
    F.pt(P_, "P", "cb", 0, -7); F.pt(Q_, "Q", "ct", 0, 6); F.pt(R_, "R", "rc", -7, 0)
    F.lab((3.9, f(3.9)), r"y=-x^{2}+5x-4", "lc", 12, -4, 20)
    return F.render()


def fig_n1151():
    # 내신(영복여고): y=-x^2+4, y=x^2+2x, 점 A의 x좌표 a=-0.7 (그림)
    f = lambda t: -t * t + 4
    g = lambda t: t * t + 2 * t
    a = -0.7
    A, B = (a, f(a)), (-a, f(a))
    C, D = (a, g(a)), (-2 - a, g(a))
    F = Frame((-3.4, 2.9), (-1.8, 5.0), 52, 46, (20, 12, 150, 12))
    F.poly([A, B, C, D], SKY)
    F.axes()
    F.curve(f, roots(f, -4, 0, -1.6)[0], roots(f, 0, 4, -1.6)[0])
    F.curve(g, roots(g, -4, -1, 4.7)[0], roots(g, -1, 3, 4.7)[0])
    for p, q in ((A, B), (B, C), (C, D), (D, A)):
        F.seg(p, q)
    for p in (A, B, C, D):
        dot(F, p, 3)
    F.pt((0, 0), "O", "lt", 4, 4)
    F.pt(A, "A", "rb", -4, -4); F.pt(B, "B", "lb", 4, -4); F.pt(C, "C", "lt", 5, 3); F.pt(D, "D", "rt", -5, 3)
    F.lab((2.35, f(2.35)), r"y=-x^{2}+4", "lc", 10, 0, 20)
    x1 = roots(g, -1, 3, 4.7)[0]
    F.lab((x1, 4.7), r"y=x^{2}+2x", "lc", 8, 4, 20)
    return F.render()


def fig_n1169():
    # 내신(양명고): y=-x^2/2+4x, 직선 y=3x/4, 사다리꼴 ABCD (그림은 t=1.5)
    f = lambda u: -u * u / 2 + 4 * u
    l = lambda u: 0.75 * u
    tt = 1.5
    A, B = (4 + tt, f(4 + tt)), (4 - tt, f(4 - tt))
    C, D = (4 - tt, l(4 - tt)), (4 + tt, l(4 + tt))
    F = Frame((-0.9, 9.0), (-1.2, 9.0), 40, 34, (20, 12, 150, 12))
    F.poly([A, B, C, D], GREEN)
    F.axes()
    F.curve(f, roots(f, -1, 4, -1.0)[0], roots(f, 4, 10, -1.0)[0])
    F.seg((-0.8, l(-0.8)), (8.8, l(8.8)))
    for p, q in ((A, B), (B, C), (C, D), (D, A)):
        F.seg(p, q)
    F.pt((0, 0), "O", "lt", 5, 5)
    F.pt(A, "A", "lb", 5, -3); F.pt(B, "B", "rb", -5, -3); F.pt(C, "C", "rt", -4, 5); F.pt(D, "D", "lt", 4, 5)
    F.lab((7.6, f(7.6)), r"y=-\frac{1}{2}x^{2}+4x", "lc", 12, 0, 19)
    F.lab((8.8, l(8.8)), r"y=\frac{3}{4}x", "lc", 6, 0, 19)
    return F.render()


def fig_m3285():
    # 2025년 9월 고1 28번: f=x^2/2-2x, l1: y=mx, l2: y=m(x-4) (그림은 m=0.55)
    f = lambda u: u * u / 2 - 2 * u
    mv = 0.55
    xB, xC = 2 * mv + 4, 2 * mv
    O, A = (0, 0), (4, 0)
    B, C = (xB, f(xB)), (xC, f(xC))
    D, E = (xB, 0), (xC, 0)
    F = Frame((-1.4, 6.3), (-2.9, 4.6), 52, 52, (20, 12, 60, 12))
    F.poly([A, E, C], PINK); F.poly([A, D, B], SKY)
    F.axes()
    F.curve(f, roots(f, -2, 2, 4.3)[0], roots(f, 2, 8, 4.3)[0])
    F.seg((-1.0, -mv), (6.0, 6.0 * mv))                          # l1
    F.seg((-0.4, mv * (-4.4)), (6.0, mv * 2.0))                  # l2
    F.seg(E, C); F.seg(A, C); F.seg(B, D); F.seg(A, B)
    right_mark(F, E, A, C, 0.18); right_mark(F, D, A, B, 0.18)
    F.pt(O, "O", "rt", -5, 5); F.pt(A, "A", "ct", 0, 6)
    F.pt(B, "B", "rb", -5, -3); F.pt(C, "C", "ct", 0, 6); F.pt(D, "D", "lt", 4, 5); F.pt(E, "E", "rb", -5, -3)
    F.lab((6.0, 6.0 * mv), r"l_{1}", "lc", 6, 0, 20)
    F.lab((6.0, 2.0 * mv), r"l_{2}", "lc", 6, 0, 20)
    x1 = roots(f, 2, 8, 4.3)[0]
    F.lab((x1, 4.3), r"y=f(x)", "rc", -10, 6, 20)
    return F.render()


def fig_m3335():
    # 2026년 9월 고1 18번: f=x^2+x-4, 직선 y=mx+4 (그림은 m=3)
    f = lambda u: u * u + u - 4
    mv = 3.0
    g = lambda u: mv * u + 4
    xs = roots(lambda u: f(u) - g(u), -5, 8, 0)
    xA, xB = xs[0], xs[1]
    O, A, B, C, D = (0, 0), (xA, f(xA)), (xB, f(xB)), (0, -4), (0, 4)
    F = Frame((-5.2, 5.4), (-5.6, 18.0), 32, 11, (60, 12, 20, 12))
    F.poly([O, A, C], SKY); F.poly([O, B, D], PINK)
    F.axes()
    F.curve(f, roots(f, -6, -0.5, 17.5)[0], roots(f, -0.5, 6, 17.5)[0])
    l0, l1 = roots(g, -6, 0, -5.4)[0], roots(g, 0, 6, 17.6)[0]
    F.seg((l0, g(l0)), (l1, g(l1)))
    F.seg(O, A); F.seg(A, C); F.seg(O, B); F.seg(B, D)
    F.pt(O, "O", "lt", 5, 4); F.pt(A, "A", "rc", -7, 0); F.pt(B, "B", "lc", 7, 2)
    F.pt(C, "C", "lt", 6, 2); F.pt(D, "D", "rc", -7, 0)
    F.lab((-4.4, f(-4.4)), r"y=f(x)", "lc", 10, 0, 20)
    F.lab((l0, g(l0)), r"y=mx+4", "rc", -6, 0, 20)
    return F.render()


FIGS = (("u6_o44.png", fig_o44), ("u6_n1151.png", fig_n1151), ("u6_n1169.png", fig_n1169),
        ("u6_m3285.png", fig_m3285), ("u6_m3335.png", fig_m3335))

if __name__ == "__main__":
    for name, fn in FIGS:
        if len(sys.argv) > 1 and name not in sys.argv[1:]:
            continue
        doc, w, h = fn()
        shoot(doc, w, h, os.path.join(HERE, name))
