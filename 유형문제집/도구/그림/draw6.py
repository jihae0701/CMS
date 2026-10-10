# -*- coding: utf-8 -*-
"""기본서 6단원(이차함수의 최대, 최소) 그림. python 그림/draw6.py [파일 ...]  (KATEX_DIR 필요)
그림 속 위치는 답이 드러나지 않도록 답과 다른 값으로 그린 개형이다.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from draw import page, shoot, HERE, STROKE
from draw5 import Frame, LN, roots

GRAY = "#e3e3e3"


def geo(xr, yr, s, m=(30, 30, 30, 30)):
    return Frame(xr, yr, s, s, m)


def right_mark(F, v, p, q, k=0.06):
    """v에서 v->p, v->q 방향의 직각 표시 (수학 좌표, k는 변 길이 비율)"""
    import math
    def u(a, b):
        dx, dy = b[0] - a[0], b[1] - a[1]
        n = math.hypot(dx, dy)
        return dx / n, dy / n
    a, b = u(v, p), u(v, q)
    L = k
    p1 = (v[0] + a[0] * L, v[1] + a[1] * L)
    p2 = (p1[0] + b[0] * L, p1[1] + b[1] * L)
    p3 = (v[0] + b[0] * L, v[1] + b[1] * L)
    F.svg.append('<polyline points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="none" stroke="#000" stroke-width="1.6"/>'
                 % (F.P(*p1) + F.P(*p2) + F.P(*p3)))


def dim_arc(F, p, q, label, side, bulge=16, size=20, gap=6):
    """선분 pq의 길이 표시: side 쪽(화면 법선 방향 +1/-1)으로 휜 점선 호와 가운데 글자"""
    import math
    (x1, y1), (x2, y2) = F.P(*p), F.P(*q)
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    dx, dy = x2 - x1, y2 - y1
    n = math.hypot(dx, dy)
    nx, ny = -dy / n * side, dx / n * side
    cx, cy = mx + nx * 2 * bulge, my + ny * 2 * bulge
    F.svg.append('<path d="M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" fill="none" stroke="#000" stroke-width="1.5" stroke-dasharray="5,4"/>'
                 % (x1, y1, cx, cy, x2, y2))
    lx, ly = mx + nx * (bulge + gap), my + ny * (bulge + gap)
    anc = ("l" if nx > 0.5 else "r" if nx < -0.5 else "c") + ("t" if ny > 0.5 else "b" if ny < -0.5 else "c")
    F.labels.append((lx, ly, label, size, anc))


def fig_paper():
    # 직각삼각형 A(0,30), B(0,0), C(20,0)에서 직사각형 EBFD (그림은 ED=7). 길이는 점선 호로 표시
    F = geo((-2, 22), (-2, 31), 9, (60, 22, 34, 50))
    A, B, C = (0, 30), (0, 0), (20, 0)
    e = 7
    E, D, Fp = (0, 30 - 1.5 * e), (e, 30 - 1.5 * e), (e, 0)
    F.poly([E, B, Fp, D], GRAY)
    for p, q in ((A, B), (B, C), (C, A)):
        F.seg(p, q, STROKE)
    F.seg(E, D); F.seg(D, Fp)
    right_mark(F, B, A, C, 1.2)
    dim_arc(F, B, A, "30", -1, 18)          # AB 왼쪽
    dim_arc(F, B, C, "20", 1, 18)           # BC 아래쪽
    F.pt(A, "A", "cb", 0, -6); F.pt(B, "B", "rt", -9, 9); F.pt(C, "C", "lc", 8, 0)
    F.pt(E, "E", "lc", 6, -12); F.pt(D, "D", "lb", 6, -2); F.pt(Fp, "F", "lb", 5, -4)
    return F.render()


def fig_rect8():
    f = lambda t: -t * t + 8 * t
    a = 2.6
    F = Frame((-1.2, 9.4), (-1.6, 18.2), 40, 17, (20, 12, 20, 12))
    F.axes()
    F.curve(f, roots(f, -1, 1, -1.4)[0], roots(f, 7, 9.5, -1.4)[0])
    A, B, C, D = (4 - a, 0), (4 + a, 0), (4 + a, f(4 + a)), (4 - a, f(4 - a))
    for p, q in ((A, D), (D, C), (C, B)):
        F.seg(p, q)
    F.pt((0, 0), "O", "rt", -5, 5)
    F.pt(A, "A", "ct", 0, 5); F.pt(B, "B", "ct", 0, 5); F.pt(C, "C", "lb", 6, -2); F.pt(D, "D", "rb", -6, -2)
    F.lab((4, 16), r"y=-x^{2}+8x", "cb", 0, -8, 20)
    return F.render()


def fig_curveP():
    f = lambda t: t * t - 3 * t - 4
    F = Frame((-2.6, 5.8), (-7.2, 6.2), 40, 26, (20, 12, 150, 12))
    F.axes()
    x0, x1 = roots(f, -3, 1.5, 5.6)[0], roots(f, 1.5, 6, 5.6)[0]
    F.curve(f, x0, x1)
    F.svg.append('<circle cx="%.1f" cy="%.1f" r="4" fill="#000"/>' % F.P(2.6, f(2.6)))
    F.pt((0, 0), "O", "rt", -5, 5)
    F.pt((-1, 0), "A", "rt", -5, 5); F.pt((4, 0), "B", "lt", 6, 5)
    F.lab((2.6, f(2.6)), r"\mathrm{P}(a,\,b)", "lt", 6, 4, 20)
    F.lab((x1, f(x1)), r"y=x^{2}-3x-4", "lc", 8, 6, 20)
    return F.render()


def fig_tri():
    # 밑변 BC=20, 높이 18, A의 발은 B에서 7 (그림은 PS의 높이 7)
    F = geo((-1, 21), (-1, 19.5), 11, (28, 26, 28, 26))
    A, B, C = (7, 18), (0, 0), (20, 0)
    h = 7
    P_ = (A[0] * h / 18, h); S_ = (C[0] + (A[0] - C[0]) * h / 18, h)
    Q_, R_ = (P_[0], 0), (S_[0], 0)
    F.poly([P_, Q_, R_, S_], GRAY)
    for p, q in ((A, B), (B, C), (C, A)):
        F.seg(p, q, STROKE)
    for p, q in ((P_, Q_), (P_, S_), (S_, R_)):
        F.seg(p, q)
    F.pt(A, "A", "cb", 0, -6); F.pt(B, "B", "rt", -5, 4); F.pt(C, "C", "lt", 5, 4)
    F.pt(P_, "P", "rc", -8, 0); F.pt(S_, "S", "lc", 8, 0); F.pt(Q_, "Q", "ct", 0, 6); F.pt(R_, "R", "ct", 0, 6)
    return F.render()


def fig_two():
    # f=(x-5)^2+1, g=-(x-5)^2+51 (세로를 줄여 그린 개형), 직사각형 a=3
    sy = 5.4
    F = Frame((-1.4, 11.6), (-3, 56), 32, sy, (20, 12, 95, 30))
    F.axes()
    f = lambda t: (t - 5) ** 2 + 1
    g = lambda t: -(t - 5) ** 2 + 51
    F.curve(f, -0.8, 10.8)
    F.curve(g, -0.8, 10.8)
    a = 3.2
    A, B, C, D = (5 - a, f(5 - a)), (5 + a, f(5 + a)), (5 + a, g(5 + a)), (5 - a, g(5 - a))
    for p, q in ((A, B), (B, C), (C, D), (D, A)):
        F.seg(p, q)
    F.pt((0, 0), "O", "rt", -5, 5)
    F.pt(A, "A", "rt", -5, 4); F.pt(B, "B", "lt", 5, 4); F.pt(C, "C", "lb", 5, -3); F.pt(D, "D", "rb", -5, -3)
    F.lab((10.8, f(10.8)), r"y=f(x)", "lc", 8, 0, 20)
    F.lab((10.8, g(10.8)), r"y=g(x)", "lc", 8, 0, 20)
    return F.render()


def fig_isos():
    # 직각이등변삼각형: A(0,12)… 회전하여 빗변 BC를 아래에 둔다. B(0,0), C(12√2,0), A(6√2, 6√2)
    import math
    r2 = math.sqrt(2)
    B, C, A = (0, 0), (12 * r2, 0), (6 * r2, 6 * r2)
    xv = 2.4                                    # CP=2x (그림은 x=2.4)
    t = 2 * xv / 12
    P_ = (C[0] + (A[0] - C[0]) * t, C[1] + (A[1] - C[1]) * t)
    Q_ = (P_[0], 0)
    R_ = (P_[0] - (A[0] - B[0]) * (P_[1] / A[1]) * 0 - (P_[1] / A[1]) * 0, P_[1])
    R_ = (P_[1], P_[1])                         # AB 위: y=x
    F = geo((-1, 18), (-1.2, 9.6), 15, (26, 26, 26, 26))
    F.poly([P_, R_, B, Q_], GRAY)
    for p, q in ((A, B), (B, C), (C, A)):
        F.seg(p, q, STROKE)
    F.seg(P_, Q_); F.seg(P_, R_)
    right_mark(F, A, B, C, 0.9); right_mark(F, Q_, P_, C, 0.7)
    F.pt(A, "A", "cb", 0, -6); F.pt(B, "B", "rt", -5, 4); F.pt(C, "C", "lt", 5, 4)
    F.pt(P_, "P", "lb", 6, -2); F.pt(Q_, "Q", "ct", 0, 6); F.pt(R_, "R", "rb", -6, -2)
    return F.render()


def fig_curveAC():
    f = lambda t: t * t - 6 * t + 5
    F = Frame((-1.4, 7.4), (-5.2, 8.6), 40, 24, (20, 12, 150, 12))
    F.axes()
    F.curve(f, roots(f, -1.5, 3, 8)[0], roots(f, 3, 8, 8)[0])
    F.svg.append('<circle cx="%.1f" cy="%.1f" r="4" fill="#000"/>' % F.P(3.6, f(3.6)))
    F.pt((0, 0), "O", "rt", -5, 5)
    F.pt((0, 5), "A", "rc", -7, 0); F.pt((1, 0), "B", "rt", -4, 5); F.pt((5, 0), "C", "lt", 6, 5)
    F.lab((3.6, f(3.6)), r"\mathrm{P}(a,\,b)", "lt", 6, 4, 20)
    x1 = roots(f, 3, 8, 8)[0]
    F.lab((x1, 8), r"y=x^{2}-6x+5", "lc", 8, 4, 20)
    return F.render()


def fig_equi():
    import math
    r3 = math.sqrt(3)
    B, C, A = (-1, 0), (1, 0), (0, r3)
    Pm = (0, 0)
    Q_ = (0, 0.75)
    F = geo((-1.3, 1.3), (-0.25, 1.95), 150, (26, 30, 26, 30))
    for p, q in ((A, B), (B, C), (C, A)):
        F.seg(p, q, STROKE)
    F.seg(A, Pm); F.seg(B, Q_); F.seg(C, Q_)
    F.svg.append('<circle cx="%.1f" cy="%.1f" r="3.5" fill="#000"/>' % F.P(*Q_))
    F.pt(A, "A", "cb", 0, -6); F.pt(B, "B", "rt", -5, 4); F.pt(C, "C", "lt", 5, 4)
    F.pt(Pm, "P", "ct", 0, 6); F.pt(Q_, "Q", "rc", -8, -10)
    dim_arc(F, Pm, Q_, "x", -1, 12)         # PQ 왼쪽(BQ와 AP 사이)
    return F.render()


def fig_abc():
    aa = 1.3
    f = lambda t: t * t - (aa + 4) * t + 3 * aa + 3
    F = Frame((-1.2, 5.6), (-1.6, 8.4), 50, 30, (20, 40, 20, 12))
    F.axes()
    F.curve(f, roots(f, -1.5, 2.5, 8)[0], roots(f, 2.5, 7, 8)[0])
    A, B, C = (aa + 1, 0), (3, 0), (0, 3 * aa + 3)
    F.poly([A, B, C], GRAY)
    F.seg(C, A); F.seg(C, B)
    F.pt((0, 0), "O", "rt", -5, 5)
    F.pt(A, "A", "rt", -3, 5); F.pt(B, "B", "lt", 4, 5); F.pt(C, "C", "rc", -7, 0)
    x1 = roots(f, 2.5, 7, 8)[0]
    F.lab((x1, 8), r"y=x^{2}-(a+4)x+3a+3", "rb", 10, -6, 18)
    return F.render()


FIGS = (("g6_paper.png", fig_paper), ("g6_rect8.png", fig_rect8), ("g6_curveP.png", fig_curveP),
        ("g6_tri.png", fig_tri), ("g6_two.png", fig_two), ("g6_isos.png", fig_isos),
        ("g6_curveAC.png", fig_curveAC), ("g6_equi.png", fig_equi), ("g6_abc.png", fig_abc))

if __name__ == "__main__":
    for name, fn in FIGS:
        if len(sys.argv) > 1 and name not in sys.argv[1:]:
            continue
        doc, w, h = fn()
        shoot(doc, w, h, os.path.join(HERE, name))
