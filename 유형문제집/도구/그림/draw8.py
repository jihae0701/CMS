# -*- coding: utf-8 -*-
"""기본서 8단원(이차부등식) 그림. python 그림/draw8.py [파일 ...]  (KATEX_DIR 필요)
- g8_cases.png: 개념 — a>0일 때 판별식 D의 부호에 따른 y=ax²+bx+c의 그래프와 x축
- g8_s4.png: STEP 3 — 두 점 (−2, 0), (3, 0)을 지나는 이차함수 y=f(x)의 그래프
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from draw import HERE
from draw5 import Frame, roots, fit_shoot, AX

ARROW = ('<defs><marker id="ar" viewBox="0 0 13 10" refX="12" refY="5" markerWidth="9.1" markerHeight="7" orient="auto">'
         '<path d="M13,5 L0.5,0.3 L2.5,5 L0.5,9.7 z" fill="#000"/></marker></defs>')


def xaxis(F, x0, x1):
    (a, y), (b, _) = F.P(x0, 0), F.P(x1, 0)
    F.svg.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#000" stroke-width="%s" marker-end="url(#ar)"/>'
                 % (a, y, b, y, AX))
    F.labels.append((b + 0.3, y + 1.1, "x", 22, "rt"))


def fig_cases():
    F = Frame((0, 15.6), (-1.75, 2.6), 46, 46, (10, 10, 10, 10))
    F.svg.append(ARROW)
    for c, kind, cap in ((2.5, 2, "D>0"), (7.8, 1, "D=0"), (13.1, 0, "D<0")):
        lift = {2: -0.75, 1: 0.0, 0: 0.55}[kind]
        f = lambda t, c=c, lift=lift: 0.75 * (t - c) ** 2 + lift
        xaxis(F, c - 2.3, c + 2.3)
        F.curve(f, roots(f, c - 3, c, 2.4)[0], roots(f, c, c + 3, 2.4)[0])
        if kind == 2:
            r = (0.75 / 0.75) ** 0.5
            F.lab((c - r, 0), r"\alpha", "rt", -2, 4); F.lab((c + r, 0), r"\beta", "lt", 2, 4)
        elif kind == 1:
            F.lab((c, 0), r"\alpha", "ct", 0, 6)
        F.lab((c, -1.2), cap, "ct", 0, 0)
    return F.render()


def fig_s4():
    f = lambda t: 0.5 * (t + 2) * (t - 3)
    F = Frame((-3.6, 4.6), (-3.6, 2.6), 34, 34, (20, 12, 70, 12))
    F.axes()
    F.curve(f, roots(f, -6, 0.5, 2.3)[0], roots(f, 0.5, 7, 2.3)[0])
    F.pt((0, 0), "O", "rt", -4, 4)
    F.lab((-2, 0), "-2", "rt", -3, 4); F.lab((3, 0), "3", "lt", 3, 4)
    x1 = roots(f, 0.5, 7, 2.3)[0]
    F.lab((x1, 2.3), r"y=f(x)", "lc", 6, 4, 20)
    return F.render()


# (파일, 함수, 문서에 넣는 폭 HWPUNIT)
FIGS = (("g8_cases.png", fig_cases, 21000), ("g8_s4.png", fig_s4, 9000))

if __name__ == "__main__":
    for name, fn, wd in FIGS:
        if len(sys.argv) > 1 and name not in sys.argv[1:]:
            continue
        fit_shoot(name, fn, wd, HERE)
