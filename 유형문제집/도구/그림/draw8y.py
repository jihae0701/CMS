# -*- coding: utf-8 -*-
"""유형서 8단원(이차부등식) 그림. python 그림/draw8y.py [파일 ...]  (KATEX_DIR 필요)
x절편·교점은 문제에서 주는 값이라 그대로 그리고, 나머지 모양은 개형이다.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from draw import HERE
from draw5 import Frame, roots, fit_shoot


def dashed(F, p, q):
    F.seg(p, q, 1.5, 'stroke-dasharray="5,4"')


def fig_y72():
    # 올림포스 유형편 72번: y=f(x)는 x축과 -3, 5에서 만나고 아래로 볼록
    f = lambda t: 0.22 * (t + 3) * (t - 5)
    F = Frame((-5.2, 7.2), (-4.4, 3.0), 26, 26, (20, 12, 110, 12))
    F.axes()
    F.curve(f, roots(f, -8, 1, 2.7)[0], roots(f, 1, 9, 2.7)[0])
    F.pt((0, 0), "O", "rt", -4, 4)
    F.lab((-3, 0), "-3", "rt", -3, 4); F.lab((5, 0), "5", "lt", 3, 4)
    F.lab((roots(f, 1, 9, 2.7)[0], 2.7), r"y=f(x)", "lc", 6, 4)
    return F.render()


def fig_y73():
    # 올림포스 유형편 73번: 두 그래프의 교점의 x좌표가 -1, 3 (그림은 f=x(x-4)/2, g=-x^2/2+3)
    f = lambda t: 0.5 * t * (t - 4)
    g = lambda t: -0.5 * t * t + 3
    F = Frame((-3.6, 6.0), (-3.3, 4.6), 30, 30, (20, 12, 110, 12))
    F.axes()
    F.curve(f, roots(f, -5, 2, 4.2)[0], roots(f, 2, 8, 4.2)[0])
    F.curve(g, -2.9, 3.3)
    dashed(F, (-1, f(-1)), (-1, 0)); dashed(F, (3, f(3)), (3, 0))
    F.pt((0, 0), "O", "rt", -4, 4)
    F.lab((-1, 0), "-1", "rt", -3, 4); F.lab((3, 0), "3", "lb", 3, -4)
    F.lab((roots(f, 2, 8, 4.2)[0], 4.2), r"y=f(x)", "lc", 6, 4)
    F.lab((3.3, g(3.3)), r"y=g(x)", "lc", 6, 2)
    return F.render()


def fig_w1():
    # 새 문항: y=f(x)는 x축과 -2, 5에서 만나고 아래로 볼록, 직선 y=g(x)는 x축과 2에서 만나고 기울기 양수
    f = lambda t: 0.25 * (t + 2) * (t - 5)
    g = lambda t: 0.45 * (t - 2)
    F = Frame((-4.0, 7.6), (-3.6, 4.6), 28, 28, (20, 12, 110, 12))
    F.axes()
    F.curve(f, roots(f, -8, 1.5, 4.3)[0], roots(f, 1.5, 10, 4.3)[0])
    F.seg((-3.6, g(-3.6)), (7.2, g(7.2)))
    F.pt((0, 0), "O", "rt", -4, 4)
    F.lab((-2, 0), "-2", "rt", -3, 4); F.lab((2, 0), "2", "lt", 4, 4); F.lab((5, 0), "5", "lt", 4, 4)
    F.lab((roots(f, 1.5, 10, 4.3)[0], 4.3), r"y=f(x)", "lc", 6, 4)
    F.lab((7.2, g(7.2)), r"y=g(x)", "lc", 6, 0)
    return F.render()

def fig_m1509():
    # 2015년 9월 고1 14번: f(x)=x^2+px+p, 꼭짓점 A, y절편 B, 직선 l=AB (그림은 p=2.6)
    from draw6y import dot
    pv = 2.6
    f = lambda t: t * t + pv * t + pv
    l = lambda t: pv / 2 * t + pv
    A, B = (-pv / 2, f(-pv / 2)), (0, pv)
    F = Frame((-3.6, 1.9), (-1.2, 4.6), 38, 38, (20, 12, 110, 12))
    F.axes()
    F.curve(f, roots(f, -6, -1.3, 4.3)[0], roots(f, -1.3, 4, 4.3)[0])
    F.seg((-2.5, l(-2.5)), (0.7, l(0.7)))
    dot(F, A); dot(F, B)
    F.pt((0, 0), "O", "rt", -4, 4)
    F.pt(A, "A", "ct", 0, 7); F.pt(B, "B", "rc", -8, 2)
    F.lab((roots(f, -1.3, 4, 4.3)[0], 4.3), r"y=f(x)", "lc", 6, 4)
    F.lab((0.7, l(0.7)), "l", "lc", 6, 2)
    return F.render()


# (파일, 함수, 문서에 넣는 폭 HWPUNIT = unit08.py의 "w")
FIGS = (("u8_y72.png", fig_y72, 9000), ("u8_y73.png", fig_y73, 10000), ("u8_w1.png", fig_w1, 10000), ("u8_m1509.png", fig_m1509, 9000))

if __name__ == "__main__":
    for name, fn, wd in FIGS:
        if len(sys.argv) > 1 and name not in sys.argv[1:]:
            continue
        fit_shoot(name, fn, wd, HERE)
