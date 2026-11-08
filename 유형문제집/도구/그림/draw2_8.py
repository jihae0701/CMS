# -*- coding: utf-8 -*-
"""공통수학2 유형서 8단원(절대부등식) 그림. python 그림/draw2_8.py [파일 ...]  (KATEX_DIR 필요)
- c2_8_s1393: 수매씽 1393 — 지름 AB=4인 반원 위의 점 P, PA·PB의 중점 M·N, 선분 AN·BM.
  사진의 그림을 보고 같은 모양으로 새로 그림. 점 P는 답(최댓값)이 나오는 꼭대기와 다른 자리에 그린 개형이다.
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from draw import HERE
from draw5 import LN, fit_shoot
from draw6 import geo, dim_arc
from draw2_1 import tick, small_arc


def fig_s1393():
    A, B = (-2, 0), (2, 0)
    th = math.radians(68)
    P = (2 * math.cos(th), 2 * math.sin(th))
    M = ((A[0] + P[0]) / 2, (A[1] + P[1]) / 2)
    N = ((B[0] + P[0]) / 2, (B[1] + P[1]) / 2)
    F = geo((-2.4, 2.4), (-0.7, 2.25), 64, (24, 24, 24, 24))
    arc = [(2 * math.cos(math.pi * k / 180), 2 * math.sin(math.pi * k / 180)) for k in range(0, 181)]
    F.svg.append('<polyline points="%s" fill="none" stroke="#000" stroke-width="%s" stroke-linejoin="round"/>'
                 % (" ".join("%.1f,%.1f" % F.P(*q) for q in arc), LN))
    F.seg(A, B, LN)
    F.seg(A, P, LN); F.seg(P, B, LN)
    F.seg(A, N, LN); F.seg(B, M, LN)
    tick(F, P, M, 2); tick(F, M, A, 2)
    tick(F, P, N, 1); tick(F, N, B, 1)
    small_arc(F, A, B, "4", 1, 32)       # 점선 호 휨: 처음(51)보다 낮추고 20은 너무 낮다고 해서 32(사용자 요청)
    F.pt(A, "A", "rc", -6, 2); F.pt(B, "B", "lc", 6, 2); F.pt(P, "P", "cb", 0, -6)
    F.pt(M, "M", "rb", -3, 2); F.pt(N, "N", "lc", 9, -3)          # N은 활꼴(현 PB와 호 사이) 안에(사용자 요청)
    return F.render()


FIGS = (("c2_8_s1393.png", fig_s1393, 11000),)

if __name__ == "__main__":
    for name, fn, wd in FIGS:
        if len(sys.argv) > 1 and name not in sys.argv[1:]:
            continue
        fit_shoot(name, fn, wd, HERE)
