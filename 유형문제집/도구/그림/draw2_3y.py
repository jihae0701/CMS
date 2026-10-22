# -*- coding: utf-8 -*-
"""공통수학2 유형서 3단원(원의 방정식) 그림. python 그림/draw2_3y.py [파일 ...]  (KATEX_DIR 필요)
학력평가 원문 그림(HIT기출, 2024년 3월 고2·2026년 3월 고2는 시험지 hml의 그림)을 같은 모양으로 새로 그렸다.
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from draw import HERE, STROKE
from draw5 import Frame, LN, fit_shoot
from draw6 import geo, right_mark

DOT = 'stroke-dasharray="5,5" stroke-width="1.3"'
THIN = 1.3


def circ(F, c, R):
    X, Y = F.P(*c)
    F.svg.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="#000" stroke-width="%s"/>' % (X, Y, R * F.sx, LN))


def dot(F, p, r=2.8):
    X, Y = F.P(*p)
    F.svg.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#000"/>' % (X, Y, r))


def line(F, f, x0, x1, wd=None):
    F.seg((x0, f(x0)), (x1, f(x1)), wd or LN)


def fig_m2603():
    # 2026년 3월 고2 17번: 원 (x-3)²+(y-3)²=9, 직선 y=mx (0<m<1), 중심 A, 수선의 발 H, 원점에 가까운 교점 B
    m = 2 - math.sqrt(3)
    A = (3.0, 3.0)
    t = (A[0] + m * A[1]) / (1 + m * m)
    H = (t, m * t)
    hb = math.sqrt(9 - ((m * 3 - 3) ** 2) / (1 + m * m))
    u = (1 / math.sqrt(1 + m * m), m / math.sqrt(1 + m * m))
    B = (H[0] - hb * u[0], H[1] - hb * u[1])
    F = Frame((-0.6, 7.6), (-0.6, 6.6), 34, 34, (20, 20, 110, 16))
    F.axes()
    circ(F, A, 3)
    line(F, lambda x: m * x, -0.4, 7.2)
    F.seg(A, H, LN)
    right_mark(F, H, A, (0, 0), 0.32)
    dot(F, A)
    F.pt((0, 0), "O", "rt", -5, 5)
    F.pt(A, "A", "cb", 0, -8); F.pt(B, "B", "cb", -2, -7); F.pt(H, "H", "ct", 2, 8)
    F.lab((5.2, 5.4), "C", "lb", 4, -2, 22)
    F.lab((7.2, m * 7.2), "y=mx", "lc", 5, 0, 20)
    return F.render()


def fig_m2309c():
    # 2023년 9월 고1 20번: 정사각형 OABC(한 변 4), 세 선분 OA, AB, BC의 내분점 P, Q, R와 세 점을 지나는 원 C
    s = 1.25
    P, Q, R = (0, s), (s, 4), (4, 4 - s)
    cx, cy = (P[0] + R[0]) / 2, (P[1] + R[1]) / 2
    rr = math.hypot(R[0] - cx, R[1] - cy)
    F = Frame((-1.1, 5.3), (-1.0, 5.0), 40, 40, (22, 20, 30, 14))
    F.axes()
    for p, q in (((0, 4), (4, 4)), ((4, 4), (4, 0))):
        F.seg(p, q, LN)
    circ(F, (cx, cy), rr)
    for p in (P, Q, R):
        dot(F, p, 2.4)
    F.pt((0, 0), "O", "rt", -5, 5)
    F.pt((0, 4), "A", "rb", -6, -3); F.pt((4, 4), "B", "lb", 5, -3); F.pt((4, 0), "C", "ct", 4, 6)
    F.pt(P, "P", "rc", -7, 0); F.pt(Q, "Q", "cb", 0, -7); F.pt(R, "R", "lc", 7, 0)
    F.lab((cx + rr, cy - 1.0), "C", "lc", 6, 0, 22)
    return F.render()


def fig_m2209b():
    # 2022년 9월 고1 28번: x축과 y=mx에 접하는 반지름 2인 원, 접점 P, Q, 직선 PQ와 y축의 교점 R
    C = (4.0, 2.0)
    P = (4.0, 0.0)
    Q = (12 / 5, 16 / 5)
    R = (0.0, 8.0)
    F = Frame((-1.0, 7.6), (-1.2, 9.2), 26, 26, (20, 20, 44, 14))
    F.axes()
    circ(F, C, 2)
    line(F, lambda x: 4 * x / 3, -0.6, 6.4)
    d = (P[0] - R[0], P[1] - R[1])
    F.seg((R[0] - 0.12 * d[0], R[1] - 0.12 * d[1]), (P[0] + 0.12 * d[0], P[1] + 0.12 * d[1]), LN)
    F.pt((0, 0), "O", "lt", 4, 5)
    F.pt(P, "P", "ct", -3, 7); F.pt(Q, "Q", "cb", 0, -10); F.pt(R, "R", "rc", -7, 0)
    F.lab((6.4, 6.4 * 4 / 3), "y=mx", "lc", 5, 0, 20)
    return F.render()


def fig_m2203():
    # 2022년 3월 고2 19번: l1: 2x+y+2=0, l2: x-2y-4=0, A(0, -2), B(-1, 0), C(4, 0), 외접원, P(제1사분면), Q
    A, B, C = (0, -2), (-1, 0), (4, 0)
    P, Q = (6, 6), (3, 2)
    F = Frame((-2.6, 7.6), (-3.4, 7.0), 30, 30, (22, 20, 30, 14))
    F.axes()
    circ(F, (1.5, 0), 2.5)
    line(F, lambda x: -2 * x - 2, -2.2, 0.55)            # l1
    line(F, lambda x: x / 2 - 2, -0.8, 7.0)              # l2
    F.seg(P, B, LN); F.seg(P, C, LN)
    dot(F, P); dot(F, Q)
    F.pt((0, 0), "O", "lb", 4, -3)
    F.pt(A, "A", "rt", -5, 5); F.pt(B, "B", "rb", -5, -3); F.pt(C, "C", "lb", 5, -3)
    F.pt(P, "P", "lc", 6, 0); F.pt(Q, "Q", "lc", 6, 2)
    F.lab((-2.2, 2.4), "l_{1}", "rc", -3, 0, 22); F.lab((7.0, 1.5), "l_{2}", "lc", 4, 0, 22)
    return F.render()


def fig_m2009():
    # 2020년 9월 고1 27번: C1: (x+6)²+y²=4, C2: (x-5)²+(y+3)²=1, l: y=x-2
    F = Frame((-8.8, 7.6), (-5.4, 5.6), 22, 22, (20, 20, 30, 14))
    F.axes()
    circ(F, (-6, 0), 2); circ(F, (5, -3), 1)
    line(F, lambda x: x - 2, -3.2, 7.2)
    F.pt((0, 0), "O", "rt", -5, 5)
    F.lab((-7.4, 1.5), "C_{1}", "rb", -2, -2, 22)
    F.lab((5.75, -3.7), "C_{2}", "lt", 4, 2, 22)
    F.lab((7.2, 5.2), "l", "lc", 5, 0, 22)
    return F.render()


def fig_m2421():
    # 2024년 3월 고2 21번: l1: y=mx, l2: y=x/m, y=x 위의 중심 A, 접점 P, Q, 직선 PQ와 x축의 교점 R, 직선 AQ와 l1의 교점 B
    A = (20 / 3, 20 / 3)
    rr = (20 / 3) / math.sqrt(5)
    P, Q, R, B = (4, 8), (8, 4), (12, 0), (5, 10)
    F = Frame((-0.8, 14.0), (-0.8, 13.0), 22, 22, (20, 34, 150, 26))
    F.axes()
    circ(F, A, rr)
    line(F, lambda x: 2 * x, -0.3, 6.1)                  # l1
    line(F, lambda x: x, -0.3, 10.6, THIN)               # y=x
    line(F, lambda x: x / 2, -0.4, 13.4)                 # l2
    F.seg((3.0, 9.0), (12.8, -0.8), LN)                  # 직선 PQ
    F.seg((4.4, 11.2), (8.9, 2.2), LN)                   # 직선 AQ (B를 지남)
    dot(F, A)
    F.pt((0, 0), "O", "rt", -5, 5)
    F.pt(P, "P", "rc", -7, 0); F.pt(Q, "Q", "ct", -5, 9); F.pt(R, "R", "lb", 5, -4)
    F.pt(A, "A", "lc", 7, -2); F.pt(B, "B", "rc", -7, 2)
    F.lab((6.1, 12.2), "l_{1}:~y=mx", "cb", 0, -4, 20)
    F.lab((10.6, 10.6), "y=x", "lc", 4, 0, 20)
    F.lab((13.4, 6.7), "l_{2}:~y=\\frac{1}{m}x", "lc", 4, 0, 20)
    return F.render()


def fig_m2503b():
    # 2025년 3월 고2 28번: 중심 A(y=x 위, 반지름 3, OA=5), P1, P2, 접선 l: y=x/7, 교점 Q1, Q2
    k = 5 / math.sqrt(2)
    A = (k, k)
    P1 = (A[0] - 3 / math.sqrt(2), A[1] - 3 / math.sqrt(2))
    P2 = (A[0] + 3 / math.sqrt(2), A[1] + 3 / math.sqrt(2))
    m = 1 / 7

    def meet(Pp):
        c = Pp[0] + Pp[1]
        x = c / (1 + m)
        return (x, m * x)
    Q1, Q2 = meet(P1), meet(P2)
    T = (A[0] + 3 * m / math.sqrt(1 + m * m) * 1, 0)    # 자리만
    F = Frame((-0.8, 11.0), (-0.9, 8.6), 32, 32, (20, 20, 40, 14))
    F.axes()
    circ(F, A, 3)
    line(F, lambda x: x, -0.4, 7.6)
    line(F, lambda x: m * x, -0.6, 10.6)
    for Pp, Qq, ext in ((P1, Q1, 0.6), (P2, Q2, 0.5)):
        d = (Qq[0] - Pp[0], Qq[1] - Pp[1])
        F.seg((Pp[0] - ext * d[0] / 3, Pp[1] - ext * d[1] / 3), (Qq[0] + 0.12 * d[0], Qq[1] + 0.12 * d[1]), LN)
    F.seg(A, Q1, LN); F.seg(A, Q2, LN)
    dot(F, A)
    F.pt((0, 0), "O", "rt", -5, 5)
    F.pt(A, "A", "cb", -3, -8)
    F.lab(P1, r"\mathrm{P}_{1}", "rc", -6, 0); F.lab(P2, r"\mathrm{P}_{2}", "lb", 5, -3)
    F.lab(Q1, r"\mathrm{Q}_{1}", "ct", 0, 8); F.lab(Q2, r"\mathrm{Q}_{2}", "cb", 0, -8)
    F.lab((A[0] - 2.4, A[1] + 2.2), "C", "rb", -2, -2, 22)
    F.lab((7.6, 7.6), "y=x", "lc", 4, 0, 20)
    F.lab((10.6, 10.6 * m), "l", "lc", 5, 0, 22)
    return F.render()


def fig_m2209c():
    # 2022년 9월 고1 29번: 원 x²+y²=100, A1(3, √91), A2(7, √51), B(-10, 0), C1, C2
    A1, A2 = (3, math.sqrt(91)), (7, math.sqrt(51))
    C1, C2 = (-3, -math.sqrt(91)), (-7, -math.sqrt(51))
    B = (-10, 0)
    F = geo((-11.4, 13.0), (-11.0, 11.6), 13, (20, 20, 20, 14))
    F.axes()
    circ(F, (0, 0), 10)
    for p in (A1, A2, C1, C2):
        F.seg(B, p, LN)
    F.seg((3, 0), A1, THIN, DOT); F.seg((7, 0), A2, THIN, DOT)
    F.seg((-7, 0), C2, THIN, DOT); F.seg((0, C1[1]), C1, THIN, DOT)
    F.pt((0, 0), "O", "rt", -4, 5)
    F.pt(B, "B", "rt", -4, 5)
    F.lab(A1, r"\mathrm{A}_{1}", "cb", 0, -6); F.lab(A2, r"\mathrm{A}_{2}", "lb", 4, -3)
    F.lab(C1, r"\mathrm{C}_{1}", "ct", -2, 6); F.lab(C2, r"\mathrm{C}_{2}", "rt", -4, 4)
    F.lab((3, 0), "3", "ct", 0, 6, 20); F.lab((7, 0), "7", "ct", 0, 6, 20)
    F.lab((-7, 0), "b", "lt", 3, 3, 20); F.lab((0, C1[1]), "a", "lc", 9, 0, 20)
    return F.render()


FIGS = (("c2_3_m2603.png", fig_m2603, 9000), ("c2_3_m2309c.png", fig_m2309c, 8500), ("c2_3_m2209b.png", fig_m2209b, 8000),
        ("c2_3_m2203.png", fig_m2203, 8000), ("c2_3_m2009.png", fig_m2009, 8500), ("c2_3_m2421.png", fig_m2421, 10000),
        ("c2_3_m2503b.png", fig_m2503b, 8500), ("c2_3_m2209c.png", fig_m2209c, 8000))

if __name__ == "__main__":
    for name, fn, wd in FIGS:
        if len(sys.argv) > 1 and name not in sys.argv[1:]:
            continue
        fit_shoot(name, fn, wd, HERE)
