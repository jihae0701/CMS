# -*- coding: utf-8 -*-
"""공통수학2 기본서 1단원(평면좌표) 그림. python 그림/draw2_1.py [파일 ...]  (KATEX_DIR 필요)
원본(Basecamp 2-1) 그림의 모양을 따라 새로 그렸다. 움직이는 점(P, Q, R)과 답에 해당하는 점(C)은 답과 다른 자리에 그린 개형이다.
길이는 휜 점선 호의 가운데를 끊고 쓴다(draw6.dim_arc).
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from draw import HERE, STROKE
from draw5 import Frame, LN, fit_shoot
from draw6 import geo, right_mark, dim_arc

DASH = 'stroke-dasharray="6,5"'


def dot(F, p, r=4.2):
    F.svg.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#000"/>' % (F.P(*p) + (r,)))


def angle_arc(F, v, p, q, r=22, n=1):
    """꼭짓점 v에서 v->p, v->q 사이의 각 표시(화면 반지름 r, n겹)"""
    X, Y = F.P(*v)
    a1 = math.atan2(-(p[1] - v[1]) * F.sy, (p[0] - v[0]) * F.sx)
    a2 = math.atan2(-(q[1] - v[1]) * F.sy, (q[0] - v[0]) * F.sx)
    d = (a2 - a1) % (2 * math.pi)
    if d > math.pi:
        a1, a2, d = a2, a1, 2 * math.pi - d
    for k in range(n):
        rr = r + 5 * k
        F.svg.append('<path d="M%.1f,%.1f A%.1f,%.1f 0 0,1 %.1f,%.1f" fill="none" stroke="#000" stroke-width="1.6"/>'
                     % (X + rr * math.cos(a1), Y + rr * math.sin(a1), rr, rr, X + rr * math.cos(a1 + d), Y + rr * math.sin(a1 + d)))


def tick(F, p, q, n=2, L=8):
    """선분 pq의 가운데에 같은 길이 표시(짧은 금 n개)"""
    (x1, y1), (x2, y2) = F.P(*p), F.P(*q)
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    dx, dy = x2 - x1, y2 - y1
    s = math.hypot(dx, dy)
    ux, uy = dx / s, dy / s
    for k in range(n):
        o = (k - (n - 1) / 2) * 5
        cx, cy = mx + ux * o, my + uy * o
        F.svg.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#000" stroke-width="1.8"/>'
                     % (cx - uy * L, cy + ux * L, cx + uy * L, cy - ux * L))


def fig_056():
    # AB=3, AC=5, BD=4, DC=2
    B, C, D = (0, 0), (6, 0), (4, 0)
    A = (5 / 3, math.sqrt(56) / 3)
    F = geo((-0.5, 6.5), (-1.3, 3.3), 52, (40, 34, 40, 20))
    for p, q in ((A, B), (B, C), (C, A)):
        F.seg(p, q, STROKE)
    F.seg(A, D)
    F.pt(A, "A", "cb", 0, -6); F.pt(B, "B", "rc", -8, 0); F.pt(C, "C", "lc", 8, 0); F.pt(D, "D", "lb", 6, -4)
    dim_arc(F, B, A, "3", -1); dim_arc(F, A, C, "5", -1)
    dim_arc(F, B, D, "4", 1, 12); dim_arc(F, D, C, "2", 1, 12)
    return F.render()


def fig_058():
    # AB=5, BC=9, AC=7, AD=AB
    B, C = (0, 0), (9, 0)
    A = (19 / 6, math.sqrt(25 - (19 / 6) ** 2))
    D = (19 / 3, 0)
    F = geo((-0.5, 9.5), (-2.6, 4.4), 38, (40, 34, 40, 20))
    for p, q in ((A, B), (B, C), (C, A)):
        F.seg(p, q, STROKE)
    F.seg(A, D)
    tick(F, A, B, 2); tick(F, A, D, 2)
    F.pt(A, "A", "cb", 0, -6); F.pt(B, "B", "rc", -8, 0); F.pt(C, "C", "lc", 8, 0); F.pt(D, "D", "lb", 6, -4)
    dim_arc(F, B, A, "5", -1); dim_arc(F, A, C, "7", -1); dim_arc(F, B, C, "9", 1, 14)
    return F.render()


def fig_053():
    # AB=BC=6, AC=4, BD=DE=EC=2, AD=a, AE=b
    B, C, D, E = (0, 0), (6, 0), (2, 0), (4, 0)
    A = (14 / 3, math.sqrt(128) / 3)
    F = geo((-0.5, 6.6), (-1.3, 4.5), 50, (40, 34, 40, 20))
    for p, q in ((A, B), (B, C), (C, A)):
        F.seg(p, q, STROKE)
    F.seg(A, D); F.seg(A, E)
    F.pt(A, "A", "cb", 0, -6); F.pt(B, "B", "rc", -8, 0); F.pt(C, "C", "lc", 8, 0)
    F.pt(D, "D", "ct", 0, 6); F.pt(E, "E", "ct", 0, 6)
    dim_arc(F, B, A, "6", -1); dim_arc(F, A, C, "4", -1)
    dim_arc(F, B, D, "2", -1, 12); dim_arc(F, D, E, "2", -1, 12); dim_arc(F, E, C, "2", -1, 12)
    F.lab(((A[0] + D[0]) / 2, (A[1] + D[1]) / 2), "a", "rc", -6, 0)
    F.lab(((A[0] + E[0]) / 2, (A[1] + E[1]) / 2), "b", "lc", 5, 4)
    return F.render()


def fig_070():
    # 가로 40, 세로 30. A는 왼쪽 변(위에서 10), B는 오른쪽 변(아래에서 10). P는 위 변, Q는 아래 변(최소 자리와 다르게)
    F = geo((-9, 49), (-8, 34), 6.2, (12, 12, 12, 12))
    O, R1, R2, R3 = (0, 0), (40, 0), (40, 30), (0, 30)
    for p, q in ((O, R1), (R1, R2), (R2, R3), (R3, O)):
        F.seg(p, q, STROKE)
    A, B, P_, Q_ = (0, 20), (40, 10), (6, 30), (31, 0)
    for p, q in ((A, P_), (P_, Q_), (Q_, B)):
        F.seg(p, q)
    for p in (A, B, P_, Q_):
        dot(F, p)
    F.pt(A, "A", "lt", 7, 4); F.pt(B, "B", "rb", -6, -6); F.pt(P_, "P", "cb", 0, -7); F.pt(Q_, "Q", "ct", 0, 7)
    dim_arc(F, R3, A, "10", 1, 10); dim_arc(F, O, R3, "30", -1, 18)
    dim_arc(F, O, R1, "40", -1, 18); dim_arc(F, R1, B, "10", 1, 10)
    return F.render()


def fig_072():
    # 가로 40, 세로 30. A는 위 변(왼쪽에서 10), B는 아래 변(오른쪽에서 10). P는 왼쪽 변, Q는 오른쪽 변
    F = geo((-8, 48), (-8, 38), 6.2, (12, 12, 12, 12))
    O, R1, R2, R3 = (0, 0), (40, 0), (40, 30), (0, 30)
    for p, q in ((O, R1), (R1, R2), (R2, R3), (R3, O)):
        F.seg(p, q, STROKE)
    A, B, P_, Q_ = (10, 30), (30, 0), (0, 19), (40, 9)
    for p, q in ((A, P_), (P_, Q_), (Q_, B)):
        F.seg(p, q)
    for p in (A, B, P_, Q_):
        dot(F, p)
    F.pt(A, "A", "lt", 5, 5); F.pt(B, "B", "rb", -5, -5); F.pt(P_, "P", "rc", -8, 0); F.pt(Q_, "Q", "rb", -6, -8)
    dim_arc(F, R3, A, "10", -1, 10); dim_arc(F, B, R1, "10", 1, 10)
    dim_arc(F, R1, R2, "30", 1, 18); dim_arc(F, O, R1, "40", -1, 18)
    return F.render()


def fig_078():
    # 정사각형 OABC, OP=3, AP=5, CP=7 (한 변 √58)
    s = math.sqrt(58)
    P_ = ((58 - 16) / (2 * s), (58 - 40) / (2 * s))
    F = Frame((-1.0, 9.2), (-1.5, 8.9), 30, 30, (20, 12, 20, 12))
    F.axes()
    O, A, B, C = (0, 0), (s, 0), (s, s), (0, s)
    F.seg(A, B, STROKE); F.seg(B, C, STROKE)
    F.seg(O, A, STROKE); F.seg(O, C, STROKE)
    for q in (O, A, C):
        F.seg(P_, q)
    dot(F, P_, 3.6)
    F.pt((0, 0), "O", "rt", -5, 5)
    F.pt(A, "A", "ct", 0, 6); F.pt(B, "B", "lb", 5, -3); F.pt(C, "C", "rc", -8, 0); F.pt(P_, "P", "rc", -9, 7)
    dim_arc(F, O, P_, "3", 1, 40); dim_arc(F, P_, A, "5", 1, 8); dim_arc(F, C, P_, "7", -1, 10)
    return F.render()


def fig_080():
    # AB=AC인 직각이등변삼각형, D는 BC 위
    B, C, A = (-1, 0), (1, 0), (0, 1)
    D = (-0.38, 0)
    F = geo((-1.15, 1.15), (-0.18, 1.12), 160, (34, 30, 34, 20))
    for p, q in ((A, B), (B, C), (C, A)):
        F.seg(p, q, STROKE)
    F.seg(A, D)
    right_mark(F, A, B, C, 0.1)
    F.pt(A, "A", "cb", 0, -6); F.pt(B, "B", "rc", -8, 0); F.pt(C, "C", "lc", 8, 0); F.pt(D, "D", "ct", 0, 6)
    return F.render()


def fig_073():
    # A(6, 10), B(8, -8), 직선 x=2. P, Q는 y축 위, R은 x=2 위(최소 자리와 다르게)
    F = Frame((-1.6, 10.2), (-9.4, 12.2), 24, 19, (20, 12, 20, 12))
    F.axes()
    A, B = (6, 10), (8, -8)
    P_, R_, Q_ = (0, 7), (2, 2.5), (0, -4)
    F.seg((2, -9.2), (2, 11.4), LN)
    for p, q in ((A, P_), (P_, R_), (R_, Q_), (Q_, B)):
        F.seg(p, q)
    for p in (A, B, P_, Q_, R_):
        dot(F, p, 3.6)
    F.pt((0, 0), "O", "rt", -5, 5)
    F.pt(A, "A", "lc", 7, 0); F.pt(B, "B", "lc", 7, 0)
    F.pt(P_, "P", "rc", -9, 7); F.pt(Q_, "Q", "rc", -7, 0); F.pt(R_, "R", "lc", 7, 2)
    F.lab((2, 11.4), r"x=2", "lc", 6, 4)
    return F.render()


def fig_057():
    # AB=9, AC=7, BD:DC=3:1, AD=6 (BC=4√7)
    import math
    k = math.sqrt(7)
    B, C = (0, 0), (4 * k, 0)
    D = (3 * k, 0)
    ax = (81 - 49 + 16 * 7) / (8 * k)          # AB²−AC² = BC(2x−BC)
    A = (ax, math.sqrt(81 - ax * ax))
    F = geo((-0.6, 11.2), (-1.5, 6.3), 26, (40, 34, 40, 20))
    for p, q in ((A, B), (B, C), (C, A)):
        F.seg(p, q, STROKE)
    F.seg(A, D)
    F.pt(A, "A", "cb", 0, -6); F.pt(B, "B", "rc", -8, 0); F.pt(C, "C", "lc", 8, 0); F.pt(D, "D", "ct", 0, 6)
    dim_arc(F, B, A, "9", -1); dim_arc(F, A, C, "7", -1)
    F.lab(((A[0] + D[0]) / 2, (A[1] + D[1]) / 2), "6", "lc", 6, 0)
    return F.render()


# (파일, 함수, 문서에 넣는 폭 HWPUNIT = data01.py의 "w")
FIGS = (("c2_1_056.png", fig_056, 9500),
        ("c2_1_058.png", fig_058, 9500), ("c2_1_053.png", fig_053, 9500), ("c2_1_070.png", fig_070, 10000),
        ("c2_1_072.png", fig_072, 10000), ("c2_1_078.png", fig_078, 9000), ("c2_1_080.png", fig_080, 9000),
        ("c2_1_073.png", fig_073, 7800), ("c2_1_057.png", fig_057, 9500))

if __name__ == "__main__":
    for name, fn, wd in FIGS:
        if len(sys.argv) > 1 and name not in sys.argv[1:]:
            continue
        fit_shoot(name, fn, wd, HERE)
