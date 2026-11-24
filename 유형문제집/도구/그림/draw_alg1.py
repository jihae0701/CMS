# -*- coding: utf-8 -*-
"""CLIMATH(m) 대수 1단원 '지수' 그림 — 올림포스 고난도 대수 01의 스캔 그림을 그림 규칙대로 다시 그림 (2026-11-24).
python 도구/그림/draw_alg1.py   (KATEX_DIR 필요) → 도구/그림/alg1_*.png
- alg1_k09: 고난도 9번 사각형 ABCD (∠CBA=60°, ∠ADC=30°, ∠ACB=∠CAD=90°). 값은 문제 조건대로 BC=1, AC=√3, AD=3 비율.
- alg1_k32: 고난도 32번 직각삼각형 ABC (AB=∛54, AC=∛2, ∠C=90°), D·E는 수선의 발. 길이는 휜 점선 호 가운데.
  개형: 원본처럼 AD = AB/6(실제는 AB/9)으로, ∠C = 90°는 지킴.
- alg1_k32s: 같은 문항 해설 그림(∠BAC=θ, ∠DCB=θ 표시).
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from draw import HERE, STROKE
from draw5 import fit_shoot
from draw6 import geo, right_mark, dim_arc
from draw2_1 import angle_arc


def tri(F, *pts):
    for p, q in zip(pts, pts[1:] + pts[:1]):
        F.seg(p, q, STROKE)


def fig_k09():
    B, C = (0, 0), (1, 0)
    A = (1, math.sqrt(3))
    D = (1 + 3, math.sqrt(3))
    F = geo((-0.3, 4.3), (-0.25, 2.0), 80, (34, 30, 34, 26))
    tri(F, A, B, C); F.seg(A, D, STROKE); F.seg(C, D, STROKE)
    right_mark(F, C, A, B, 0.13); right_mark(F, A, C, D, 0.13)
    angle_arc(F, B, C, A, 26); angle_arc(F, D, A, C, 44)
    F.lab(B, r"60^\circ", "lb", 30, -8); F.lab(D, r"30^\circ", "rt", -54, 4)
    F.pt(A, "A", "rb", -8, -4); F.pt(B, "B", "rc", -10, 0); F.pt(C, "C", "ct", 0, 8); F.pt(D, "D", "lc", 10, 0)
    return F.render()


def _k32():
    # 개형: 실제 비율(AD = AB/9)이면 C가 A에 너무 붙어 원본 그림처럼 AD = AB/6으로 그림(∠C = 90°는 지킴, AB를 지름으로 하는 원 위의 C)
    A, B = (0, 0), (6, 0)
    C = (1, math.sqrt(5))
    D = (1, 0)
    t = ((D[0] - C[0]) * (B[0] - C[0]) + (D[1] - C[1]) * (B[1] - C[1])) / ((B[0] - C[0]) ** 2 + (B[1] - C[1]) ** 2)
    E = (C[0] + t * (B[0] - C[0]), C[1] + t * (B[1] - C[1]))
    return A, B, C, D, E


def bis_lab(F, v, p, q, tex, r):
    """꼭짓점 v의 각 vp, vq의 이등분선 방향으로 r픽셀 떨어진 곳에 글자"""
    X, Y = F.P(*v)
    u = []
    for w in (p, q):
        x, y = F.P(*w); n = math.hypot(x - X, y - Y); u.append(((x - X) / n, (y - Y) / n))
    bx, by = u[0][0] + u[1][0], u[0][1] + u[1][1]; n = math.hypot(bx, by)
    F.labels.append((X + bx / n * r, Y + by / n * r, tex, 22, "cc"))


def base32(F, A, B, C, D, E, dlab=(0, 8)):
    tri(F, A, B, C); F.seg(C, D); F.seg(D, E)
    right_mark(F, C, A, B, 0.28); right_mark(F, D, C, B, 0.22); right_mark(F, E, D, B, 0.22)
    F.pt(A, "A", "rc", -10, 0); F.pt(B, "B", "lc", 10, 0); F.pt(C, "C", "cb", 0, -8)
    F.pt(D, "D", "ct", dlab[0], dlab[1]); F.pt(E, "E", "lb", 4, -8)


def fig_k32():
    A, B, C, D, E = _k32()
    F = geo((-0.9, 6.5), (-1.3, 2.65), 52, (34, 30, 34, 20))
    base32(F, A, B, C, D, E, (12, 1))                     # D는 AB에 붙이고 살짝 오른쪽(사용자)
    dim_arc(F, A, C, r"\sqrt[3]{2}", -1, 22); dim_arc(F, A, B, r"\sqrt[3]{54}", 1, 0, minr=0.16)   # 아래 호는 곡률을 낮춤(사용자, 선분 길이의 0.16배 — D 글자와 8px 이상)
    return F.render()


def fig_k32s():
    A, B, C, D, E = _k32()
    F = geo((-0.6, 6.5), (-0.5, 2.65), 52, (34, 30, 34, 20))
    base32(F, A, B, C, D, E)
    angle_arc(F, A, B, C, 26); angle_arc(F, C, D, B, 26)
    bis_lab(F, A, B, C, r"\theta", 40); bis_lab(F, C, D, B, r"\theta", 46)
    return F.render()


FIGS = {"alg1_k09.png": (fig_k09, 10000), "alg1_k32.png": (fig_k32, 10000), "alg1_k32s.png": (fig_k32s, 8000)}

if __name__ == "__main__":
    for name in sys.argv[1:] or FIGS:
        fn, w = FIGS[name]
        fit_shoot(name, fn, w, HERE)
