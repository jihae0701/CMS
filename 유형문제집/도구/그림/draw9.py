# -*- coding: utf-8 -*-
"""기본서 9단원(연립부등식) 그림. python 그림/draw9.py [파일 ...]  (KATEX_DIR 필요)
- g9_roots.png: 개념 — 이차방정식의 근의 위치(a>0): ⑴ 두 근이 모두 p보다 큼 ⑵ 모두 p보다 작음 ⑶ 두 근 사이에 p ⑷ 두 근이 모두 p, q 사이
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from draw import HERE
from draw5 import Frame, roots, fit_shoot
from draw8 import ARROW, xaxis

DASH = 'stroke-dasharray="5,4"'


def fig_roots():
    F = Frame((0, 22.6), (-1.75, 2.75), 46, 46, (10, 10, 10, 10))
    F.svg.append(ARROW)
    for c, ps, cap, ax in ((2.6, (-1.8,), "⑴", True), (8.3, (1.8,), "⑵", True),
                           (14.0, (0.35,), "⑶", False), (19.7, (-1.8, 1.8), "⑷", True)):
        f = lambda t, c=c: 0.75 * (t - c) ** 2 - 0.75
        xaxis(F, c - 2.4, c + 2.8)
        F.curve(f, roots(f, c - 3, c, 2.5)[0], roots(f, c, c + 3, 2.5)[0])
        F.lab((c - 1, 0), r"\alpha", "rt", -3, 4); F.lab((c + 1, 0), r"\beta", "lt", 3, 4)
        if ax:
            F.seg((c, -0.75), (c, 2.3), 1.3, DASH)
        for d, nm in zip(ps, "pq"):
            p = c + d
            F.seg((p, 0), (p, f(p)), 1.3, DASH)
            F.lab((p, 0), nm, "ct", 0, 6) if f(p) > 0 else F.lab((p, 0), nm, "cb", 0, -5)
        F.lab((c, -1.25), cap, "ct", 0, 0)
    return F.render()


FIGS = (("g9_roots.png", fig_roots, 21000),)

if __name__ == "__main__":
    for name, fn, wd in FIGS:
        if len(sys.argv) > 1 and name not in sys.argv[1:]:
            continue
        fit_shoot(name, fn, wd, HERE)
