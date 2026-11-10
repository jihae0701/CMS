# -*- coding: utf-8 -*-
"""CMS 스토리 라이트 공통수학1 그림. python 그림/drawlite_c1.py [파일 ...]  (KATEX_DIR 필요)
- lite1_03_cube.png: 3단원 o3-69 — 모서리 2x+y인 정육면체의 각 면 가운데에 한 변이 x+y인 정사각형 구멍을 뚫은 입체
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from draw import HERE
from draw5 import fit_shoot
from draw6 import geo, dim_arc

TOP, FRONT, SIDE = "#ebf6fd", "#d6ecfb", "#c1e1f7"   # 정육면체 세 면(하늘색 명도만 다르게)
STROKE = 3.2


def clip(subj, clipper):
    """볼록 다각형끼리의 겹친 부분(Sutherland–Hodgman, 반시계 방향 clipper)"""
    def inside(p, a, b):
        return (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0]) >= -1e-12
    def inter(p, q, a, b):
        x1, y1 = p; x2, y2 = q; x3, y3 = a; x4, y4 = b
        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
        return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))
    out = subj
    for k in range(len(clipper)):
        a, b = clipper[k], clipper[(k + 1) % len(clipper)]
        inp, out = out, []
        for m in range(len(inp)):
            p, q = inp[m], inp[(m + 1) % len(inp)]
            if inside(q, a, b):
                if not inside(p, a, b):
                    out.append(inter(p, q, a, b))
                out.append(q)
            elif inside(p, a, b):
                out.append(inter(p, q, a, b))
    return out


def ccw(pts):
    s = sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1] for i in range(len(pts)))
    return pts if s > 0 else pts[::-1]


def fig_cube():
    """원본(올림포스 유형편 03-69) 모양대로: 세 면의 가운데 구멍, 앞면 구멍 안에 터널 모서리, 길이 다섯 군데.
    색칠은 정육면체 세 면의 하늘색만(사용자 지시 2026-11-10), 구멍은 칠하지 않음."""
    L, h = 3.0, 1.1                      # 정육면체 모서리, 구멍 한 변(그림은 개형)
    ox, oy = 0.5, 0.42                   # 깊이 방향 한 칸의 비스듬한 이동
    d = 0.45                             # 앞면 구멍 안쪽으로 보이는 깊이
    P = lambda x, y, z: (x + z * ox, y + z * oy)
    F = geo((-0.2, L + L * ox + 0.2), (-0.2, L + L * oy + 0.2), 80, (150, 50, 20, 60))
    a, b = (L - h) / 2, (L + h) / 2
    front = [P(a, a, 0), P(b, a, 0), P(b, b, 0), P(a, b, 0)]
    top = [P(a, L, a), P(b, L, a), P(b, L, b), P(a, L, b)]
    side = [P(L, a, a), P(L, a, b), P(L, b, b), P(L, b, a)]
    for q in (front, top, side):         # poly는 맨 아래 층에 끼워 넣으므로 구멍(흰색)부터
        F.poly(q, "#ffffff")
    F.poly([P(0, 0, 0), P(L, 0, 0), P(L, L, 0), P(0, L, 0)], FRONT)
    F.poly([P(0, L, 0), P(L, L, 0), P(L, L, L), P(0, L, L)], TOP)
    F.poly([P(L, 0, 0), P(L, 0, L), P(L, L, L), P(L, L, 0)], SIDE)
    for p, q in ((P(0, 0, 0), P(L, 0, 0)), (P(L, 0, 0), P(L, L, 0)), (P(L, L, 0), P(0, L, 0)), (P(0, L, 0), P(0, 0, 0)),
                 (P(0, L, 0), P(0, L, L)), (P(0, L, L), P(L, L, L)), (P(L, L, L), P(L, L, 0)),
                 (P(L, 0, 0), P(L, 0, L)), (P(L, 0, L), P(L, L, L))):
        F.seg(p, q, STROKE)
    for q in (front, top, side):
        for k in range(4):
            F.seg(q[k], q[(k + 1) % 4])
    # 앞면 구멍 안: 터널의 안쪽 모서리(왼쪽 아래 모서리에서 비스듬히, 거기서 가로·세로)
    A0 = P(a, a, 0)
    K = (A0[0] + d * ox, A0[1] + d * oy)
    F.seg(A0, K)
    F.seg(K, (front[1][0], K[1]))
    F.seg(K, (K[0], front[3][1]))
    # 길이: 정육면체 모서리 셋(가로, 세로, 깊이)과 구멍 한 변 둘
    dim_arc(F, P(0, 0, 0), P(L, 0, 0), "2x+y", 1)
    dim_arc(F, P(0, 0, 0), P(0, L, 0), "2x+y", -1, 48)
    dim_arc(F, P(0, L, 0), P(0, L, L), "2x+y", -1, 40)
    dim_arc(F, P(a, a, 0), P(b, a, 0), "x+y", 1, 10)
    # 구멍 왼쪽 변: 원본처럼 점선 호만 긋고, 바깥 위의 글자에서 휜 화살표로 가리킨다(구멍이 작아 호 가운데에 글자가 안 들어감)
    (x1, y1), (x2, y2) = F.P(*P(a, a, 0)), F.P(*P(a, b, 0))
    bx = min(x1, x2) - 0.4 * abs(y2 - y1)
    my = (y1 + y2) / 2
    F.svg.append('<path d="M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" fill="none" stroke="#000" stroke-width="1.5" stroke-dasharray="5,4"/>'
                 % (x1, y1, bx, my, x2, y2))
    tipx, tipy = (x1 + 2 * (bx) + x2) / 4 + (x1 - bx) * 0 - 2, my          # 호의 가운데
    tipx = 0.25 * x1 + 0.5 * bx + 0.25 * x2
    sx, sy = F.P(*P(0, L, 0))
    lx, ly = sx - 110, sy + 0.2 * (y1 - sy)                                  # 글자 자리(정육면체 왼쪽 바깥, 앞면 위쪽 높이)
    F.svg.append('<defs><marker id="ar2" viewBox="0 0 13 10" refX="12" refY="5" markerWidth="9.1" markerHeight="7" orient="auto">'
                 '<path d="M13,5 L0.5,0.3 L2.5,5 L0.5,9.7 z" fill="#000"/></marker></defs>')
    F.svg.append('<path d="M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" fill="none" stroke="#000" stroke-width="1.6" marker-end="url(#ar2)"/>'
                 % (lx + 40, ly, tipx - 10, ly - 4, tipx - 2, tipy - 12))
    F.labels.append((lx, ly, "x+y", 22, "cc"))
    return F.render()


FIGS = (("lite1_03_cube.png", fig_cube, 10000),)

if __name__ == "__main__":
    for name, fn, wd in FIGS:
        if len(sys.argv) > 1 and name not in sys.argv[1:]:
            continue
        print(name, fit_shoot(name, fn, wd, HERE))
