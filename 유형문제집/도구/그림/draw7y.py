# -*- coding: utf-8 -*-
"""유형서 7단원(여러 가지 방정식) 그림. python 그림/draw7y.py [파일 ...]  (KATEX_DIR 필요)
그림 속 위치는 답이 드러나지 않도록 답과 다른 값으로 그린 개형이다.
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from draw import HERE
from draw5 import Frame, fit_shoot


def fig_o53():
    # 올림포스 고난도 06단원 53번: 원 O에 내접하는 사각형 ABCD, BD는 지름 (A는 60°, C는 -48° 위치로 그린 개형)
    F = Frame((-1.15, 1.15), (-1.12, 1.12), 100, 100, (36, 30, 36, 30))
    cx, cy = F.P(0, 0)
    F.svg.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="#000" stroke-width="1.8"/>' % (cx, cy, F.sx))
    pol = lambda d: (math.cos(math.radians(d)), math.sin(math.radians(d)))
    A, B, C, D = pol(62), (-1, 0), pol(-50), (1, 0)
    for p, q in ((B, A), (A, D), (D, C), (C, B), (B, D)):
        F.seg(p, q)
    F.pt(A, "A", "lb", 4, -3); F.pt(B, "B", "rc", -7, 0); F.pt(C, "C", "lt", 4, 3); F.pt(D, "D", "lc", 7, 0)
    F.lab(pol(128), "O", "rb", -4, -4, 22)
    return F.render()


# (파일, 함수, 문서에 넣는 폭 HWPUNIT = unit07.py의 "w")
FIGS = (("u7_o53.png", fig_o53, 9000),)

if __name__ == "__main__":
    for name, fn, wd in FIGS:
        if len(sys.argv) > 1 and name not in sys.argv[1:]:
            continue
        fit_shoot(name, fn, wd, HERE)
