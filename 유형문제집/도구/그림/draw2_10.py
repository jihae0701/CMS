# -*- coding: utf-8 -*-
"""공통수학2 기본서·유형서 10단원(합성함수와 역함수) 그림. python 그림/draw2_10.py [파일 ...]  (KATEX_DIR 필요)
- c2_10_b61: Basecamp 2-2 9장 61번(290) — [0, 2]에서 X로의 두 함수 y=f(x)(꼭짓점 (0,0),(1,2),(2,0)), y=g(x)((0,1),(1,0),(2,2))의 그래프를 나란히.
  책 그림을 보고 같은 모양으로 새로 그림.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from draw import HERE
from draw5 import Frame, LN, axes, fit_shoot


def dashed(F, p, q):
    F.seg(p, q, 1.5, 'stroke-dasharray="5,4"')


def panel(F, ox, xr, yr, pts, name, xt, yt, nlab):
    """ox만큼 오른쪽으로 옮긴 좌표축에 꺾은선 pts를 그린다. xt/yt: 눈금, nlab: (점, 위치, dx, dy) 이름표 자리"""
    Q = lambda x, y: F.P(x + ox, y)
    F.svg.append(axes(Q, xr, yr))
    X, Y = Q(xr[1], 0); F.labels.append((X + 0.3, Y + 1.1, "x", 22, "rt"))
    X, Y = Q(0, yr[1]); F.labels.append((X - 10, Y + 3.7, "y", 22, "rc"))
    F.svg.append('<polyline points="%s" fill="none" stroke="#000" stroke-width="%s" stroke-linejoin="round"/>'
                 % (" ".join("%.1f,%.1f" % Q(*p) for p in pts), LN + 0.4))
    X, Y = Q(0, 0); F.labels.append((X - 5, Y + 5, r"\mathrm{O}", 20, "rt"))
    for t in xt:
        X, Y = Q(t, 0); F.labels.append((X, Y + 5, str(t), 20, "ct"))
    for t in yt:
        X, Y = Q(0, t); F.labels.append((X - 5, Y, str(t), 20, "rc"))
    p, anc, dx, dy = nlab
    X, Y = Q(*p); F.labels.append((X + dx, Y + dy, name, 21, anc))


def fig_b61():
    F = Frame((-0.45, 6.3), (-0.45, 2.75), 52, 52, (20, 16, 20, 16))
    f = [(0, 0), (1, 2), (2, 0)]
    g = [(0, 1), (1, 0), (2, 2)]
    panel(F, 0, (-0.4, 2.5), (-0.4, 2.7), f, r"y=f(x)", (1, 2), (2,), ((1.35, 2.25), "lc", 0, 0))
    dashed(F, (0, 2), (1, 2)); dashed(F, (1, 2), (1, 0))
    panel(F, 3.75, (-0.4, 2.5), (-0.4, 2.7), g, r"y=g(x)", (1, 2), (1, 2), ((0.45, 2.25), "lc", 0, 0))
    dashed(F, (3.75, 2), (5.75, 2)); dashed(F, (5.75, 2), (5.75, 0))
    return F.render()


FIGS = (("c2_10_b61.png", fig_b61, 13000),)

if __name__ == "__main__":
    for name, fn, wd in FIGS:
        if len(sys.argv) > 1 and name not in sys.argv[1:]:
            continue
        fit_shoot(name, fn, wd, HERE)
