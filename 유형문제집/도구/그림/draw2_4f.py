# -*- coding: utf-8 -*-
"""공통수학2 유형서 4단원 193번(f4-17) 그림과 '도형 f(x, y)=0의 이동' 내신 문항 그림(2026-11-08 사용자 요청).
python 그림/draw2_4f.py [파일 ...]  (KATEX_DIR 필요)
- c2_4_f417: 백영고 2026 2학기 중간 17번. 시험지 파일에 그림이 없어 문제 조건대로 그림(t=4일 때의 모습, 공통부분 색칠).
- n1795(안양외고)·n1933(화성고)·n1862(우성고)·e10-7(잠실고): 학교 시험지 hwp의 그림을 보고 같은 모양으로 새로 그림.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from draw import HERE
from draw5 import LN, fit_shoot
from draw6 import geo, right_mark, PINK, GREEN, SKY
from draw2_3y import DOT, THIN
from draw2_4y import poly_line


def fig_f417():
    t = 4
    O, C, A = (0, 0), (10, 0), (0, 10)
    D, B = (0, 8), (-8, 0)
    O2, D2, B2 = (t, 0), (t, 8), (t - 8, 0)
    F = geo((-9.2, 12.0), (-1.2, 11.4), 20, (20, 20, 20, 24))
    F.axes()
    F.poly([(0, 0), (4, 0), (4, 6), (3, 7), (0, 4)], PINK)
    poly_line(F, [O, C, A, O])
    poly_line(F, [D, B], THIN, DOT)
    poly_line(F, [O2, D2, B2], LN)
    F.pt(O, "O", "rt", -4, 5)
    F.pt(A, "A", "rc", -6, 0); F.pt(C, "C", "ct", 0, 6); F.pt(D, "D", "lc", 6, 0); F.pt(B, "B", "ct", 0, 6)
    F.lab(O2, r"\mathrm{O'}", "ct", 0, 6); F.lab(D2, r"\mathrm{D'}", "lc", 6, 0); F.lab(B2, r"\mathrm{B'}", "ct", 0, 6)
    return F.render()


def fig_n1795():
    f = [(4, 0), (7, 0), (7, 3), (5.5, 3), (5.5, 1.5), (4, 1.5), (4, 0)]
    g = [(x - 10, -y - 3) for x, y in f]
    F = geo((-8.4, 9.4), (-8.0, 5.0), 26, (20, 20, 20, 20))
    F.axes()
    F.seg((0, 3), (5.5, 3), THIN, DOT)
    F.seg((-6, 0), (-6, -3), THIN, DOT); F.seg((-3, 0), (-3, -3), THIN, DOT)
    F.seg((0, -3), (-3, -3), THIN, DOT); F.seg((0, -6), (-4.5, -6), THIN, DOT)
    poly_line(F, f, 2.6); poly_line(F, g, 2.6)
    right_mark(F, (7, 0), (4, 0), (7, 3), k=0.7)
    right_mark(F, (-3, -3), (-6, -3), (-3, -6), k=0.7)
    F.pt((0, 0), "O", "lt", 5, 5)
    F.lab((0, 3), "3", "rc", -6, 0, 20); F.lab((4, 0), "4", "ct", 0, 7, 20); F.lab((7, 0), "7", "ct", 0, 7, 20)
    F.lab((-6, 0), "-6", "cb", 0, -6, 20); F.lab((-3, 0), "-3", "cb", 0, -6, 20)
    F.lab((0, -3), "-3", "lc", 6, 0, 20); F.lab((0, -6), "-6", "lc", 6, 0, 20)
    F.lab((6.4, 3.4), "f(x,~y)=0", "cb", 0, -2, 20)
    F.lab((-6.2, -6.4), "g(x,~y)=0", "ct", 0, 4, 20)
    return F.render()


def fig_n1933():
    F = geo((-0.9, 6.6), (-0.7, 2.9), 70, (20, 20, 20, 20))
    F.axes()
    F.poly([(2, 2), (3, 2), (3, 1)], SKY)
    F.poly([(2, 2), (2, 1), (3, 1)], GREEN)
    poly_line(F, [(2, 1), (3, 1), (3, 2), (2, 2), (2, 1)], 2.4)
    F.seg((2, 2), (3, 1), 2.4)
    F.seg((0, 2), (2, 2), THIN, DOT); F.seg((0, 1), (2, 1), THIN, DOT)
    F.seg((2, 0), (2, 1), THIN, DOT); F.seg((3, 0), (3, 1), THIN, DOT)
    F.pt((0, 0), "O", "rt", -4, 5)
    F.lab((0, 2), "2", "rc", -6, 0, 20); F.lab((0, 1), "1", "rc", -6, 0, 20)
    F.lab((2, 0), "2", "ct", 0, 7, 20); F.lab((3, 0), "3", "ct", 0, 7, 20)
    F.lab((3.0, 2.0), "f(x,~y)=0", "lc", 10, -4, 20)
    F.lab((3.0, 1.0), "g(x,~y)=0", "lc", 10, 4, 20)
    return F.render()


def fig_e10_7():
    F = geo((-2.4, 8.2), (-0.8, 3.4), 50, (20, 20, 20, 20))
    F.axes()
    F.seg((-2.3, 2), (3, 2), 2.6)
    F.seg((3, 2), (4, 0), 2.6)
    F.seg((3, 0), (3, 2), THIN, DOT)
    F.pt((0, 0), "O", "rt", -4, 5)
    F.lab((0, 2), "2", "rt", -5, 5, 20); F.lab((3, 0), "3", "ct", 0, 7, 20); F.lab((4, 0), "4", "ct", 0, 7, 20)
    F.lab((3.5, 1.0), "f(x,~y)=0", "lc", 10, 0, 20)
    return F.render()


def fig_n1862():
    F = geo((-0.7, 6.0), (-0.6, 2.8), 56, (20, 20, 20, 20))
    F.axes()
    F.poly([(3, 0), (5, 0), (4, 2)], SKY)
    poly_line(F, [(3, 0), (5, 0), (4, 2), (3, 0)], 2.4)
    F.seg((0, 2), (4, 2), THIN, DOT); F.seg((4, 0), (4, 2), THIN, DOT)
    F.pt((0, 0), "O", "rt", -4, 5)
    F.lab((0, 2), "2", "rc", -6, 0, 20)
    F.lab((3, 0), "3", "ct", 0, 7, 20); F.lab((4, 0), "4", "ct", 0, 7, 20); F.lab((5, 0), "5", "ct", 0, 7, 20)
    return F.render()


def fig_g259():
    # 기본서 4단원 156번(고쟁이 259): 정사각형 ABCD(한 변 6), AE:ED=CF:FD=1:2, BE·BF로 접어 A→A', C→C'
    A, B, C, D = (0, 6), (0, 0), (6, 0), (6, 6)
    E, F = (2, 6), (6, 2)
    A2, C2 = (3.6, 4.8), (4.8, 3.6)
    F_ = geo((-0.9, 6.9), (-0.9, 6.9), 40, (20, 20, 20, 20))
    F_.poly([B, E, A2], PINK); F_.poly([B, F, C2], SKY)
    poly_line(F_, [E, D, F], 2.4)                       # 접은 뒤에도 남는 종이의 변
    for p, q in ((A, B), (A, E), (B, C), (C, F)):       # 접혀서 옮겨 간 원래 자리는 점선
        F_.seg(p, q, THIN, DOT)
    F_.seg(B, E, LN); F_.seg(B, F, LN)
    poly_line(F_, [E, A2, B], LN); poly_line(F_, [F, C2, B], LN)
    F_.pt(A, "A", "rb", -6, -4); F_.pt(B, "B", "rt", -6, 4); F_.pt(C, "C", "lt", 6, 4); F_.pt(D, "D", "lb", 6, -4)
    F_.pt(E, "E", "cb", 0, -6); F_.pt(F, "F", "lc", 6, 0)
    F_.lab(A2, r"\mathrm{A'}", "cb", 0, -6); F_.lab(C2, r"\mathrm{C'}", "lc", 6, 0)
    return F_.render()


FIGS = (("c2_4_f417.png", fig_f417, 8500), ("c2_4_n1795.png", fig_n1795, 9000), ("c2_4_n1933.png", fig_n1933, 7000),
        ("c2_4_e10-7.png", fig_e10_7, 7000), ("c2_4_n1862.png", fig_n1862, 7000),
        ("c2_4_g259.png", fig_g259, 6000))

if __name__ == "__main__":
    for name, fn, wd in FIGS:
        if len(sys.argv) > 1 and name not in sys.argv[1:]:
            continue
        fit_shoot(name, fn, wd, HERE)
