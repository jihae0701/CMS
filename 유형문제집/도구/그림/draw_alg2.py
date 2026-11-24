# -*- coding: utf-8 -*-
"""CLIMATH(m) 대수 2단원 '로그' 그림 — 올림포스 고난도 대수 01의 스캔 그림을 그림 규칙대로 다시 그림 (2026-11-24).
python 도구/그림/draw_alg2.py   (KATEX_DIR 필요) → 도구/그림/alg2_*.png
- alg2_pc16: STEP3 2026 평촌고 중간 16 변형 — 삼각형 ABC, 선분 DE // BC, DE = BC/4(개형).
- alg2_k33s: 고난도 33번 해설 — ㉠(x>a, x≠a+1)과 ㉡(b<x<b+3)의 수직선. 빈 점은 b, b+1, b+3(제외), 아래에 b=a, b+1=a+1, b+2=5.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from draw import HERE, STROKE
from draw5 import fit_shoot
from draw6 import geo
from draw5 import AX

ARROW = ('<marker id="ar" viewBox="0 0 13 10" refX="12" refY="5" markerWidth="9.1" markerHeight="7" orient="auto">'
         '<path d="M13,5 L0.5,0.3 L2.5,5 L0.5,9.7 z" fill="#000"/></marker>')


def xaxis(F, x0, x1):
    """x축만(원본이 수직선) — 약속된 화살표와 x 글자(draw5.Frame.axes와 같은 위치)"""
    (a, y), (b, _) = F.P(x0, 0), F.P(x1, 0)
    F.svg.append('<defs>%s</defs><line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#000" stroke-width="%s" marker-end="url(#ar)"/>' % (ARROW, a, y, b, y, AX))
    F.labels.append((b + 0.3, y + 1.1, "x", 22, "rt"))


def polyline(F, pts):
    F.svg.append('<polyline points="%s" fill="none" stroke="#000" stroke-width="%s" stroke-linejoin="round"/>'
                 % (" ".join("%.1f,%.1f" % F.P(*q) for q in pts), STROKE))


def hole(F, p, r=6):
    F.svg.append('<circle cx="%.1f" cy="%.1f" r="%s" fill="#fff" stroke="#000" stroke-width="2"/>' % (F.P(*p) + (r,)))


def fig_k33s():
    F = geo((-0.7, 4.7), (-1.3, 1.45), 70, (20, 34, 40, 10))
    xaxis(F, -0.7, 4.7)
    polyline(F, [(0, 0), (0.22, 0.5), (0.78, 0.5), (1, 0), (1.22, 0.5), (4.3, 0.5)])      # ㉠ x>a, x≠a+1
    polyline(F, [(0, 0), (0, 1.05), (3, 1.05), (3, 0)])                                    # ㉡ b<x<b+3
    for x in (0, 1, 3):
        hole(F, (x, 0))
    F.lab((4.3, 0.5), r"\text{㉠}", "lc", 8, 0)
    F.lab((1.5, 1.05), r"\text{㉡}", "cb", 0, -8)
    for x, top, bot in ((0, "b", "a"), (1, "b+1", "a+1"), (2, "b+2", "5")):
        F.lab((x, 0), top, "ct", 0, 12)
        F.lab((x, 0), r"\Vert", "ct", 0, 40)
        F.lab((x, 0), bot, "ct", 0, 66)
    F.lab((3, 0), "b+3", "ct", 0, 12)
    return F.render()


def fig_pc16():
    # 평촌고 중간 16 변형: 삼각형 ABC, DE // BC, DE = BC/4 (개형)
    A, B, C = (1.6, 3.2), (0, 0), (4, 0)
    t = 0.25
    D = (A[0] + t * (B[0] - A[0]), A[1] + t * (B[1] - A[1]))
    E = (A[0] + t * (C[0] - A[0]), A[1] + t * (C[1] - A[1]))
    F = geo((-0.4, 4.4), (-0.35, 3.55), 64, (30, 34, 30, 30))
    for p, q in ((A, B), (B, C), (C, A)):
        F.seg(p, q, STROKE)
    F.seg(D, E)
    F.pt(A, "A", "cb", 0, -8); F.pt(B, "B", "rc", -10, 0); F.pt(C, "C", "lc", 10, 0)
    F.pt(D, "D", "rc", -10, 0); F.pt(E, "E", "lc", 10, 0)
    return F.render()


FIGS = {"alg2_pc16.png": (fig_pc16, 7000), "alg2_k33s.png": (fig_k33s, 8000)}

if __name__ == "__main__":
    for name in sys.argv[1:] or FIGS:
        fn, w = FIGS[name]
        fit_shoot(name, fn, w, HERE)
