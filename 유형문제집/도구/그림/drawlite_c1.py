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
    """구멍 뚫린 정육면체(올림포스 유형편 03-69). 사용자 지시(2026-11-10): 색칠은 하늘색만, 길이 표시는 처음 방식
    (앞면 아래·왼쪽 2x+y, 구멍 윗변 x+y). 구멍 안쪽 벽은 그 벽이 향한 방향의 면 색(하늘색 명도)으로, 안쪽 끝은 흰색."""
    L, h = 3.0, 1.3                      # 정육면체 모서리, 구멍 한 변(그림은 개형)
    ox, oy = 0.5, 0.42                   # 깊이 방향 한 칸의 비스듬한 이동
    P = lambda x, y, z: (x + z * ox, y + z * oy)
    F = geo((-0.2, L + L * ox + 0.2), (-0.2, L + L * oy + 0.2), 70, (120, 30, 30, 90))
    a, b = (L - h) / 2, (L + h) / 2
    d = 0.55
    # (구멍 네 꼭짓점, 화면에서 안쪽으로 들어가는 방향, 변마다 안쪽 벽의 색)
    holes = [
        ([P(a, a, 0), P(b, a, 0), P(b, b, 0), P(a, b, 0)], (d * ox, d * oy), (TOP, SIDE, TOP, SIDE)),
        ([P(a, L, a), P(b, L, a), P(b, L, b), P(a, L, b)], (0, -0.3), (FRONT, SIDE, FRONT, SIDE)),
        ([P(L, a, a), P(L, a, b), P(L, b, b), P(L, b, a)], (-0.32, 0), (TOP, FRONT, TOP, FRONT)),
    ]
    info = []
    for q, (vx, vy), cols in holes:      # poly는 맨 아래 층에 끼워 넣으므로 위에 보일 것부터
        Q = ccw(q)
        far = clip(ccw([(x + vx, y + vy) for x, y in q]), Q)
        F.poly(far, "#ffffff")
        for k in range(4):
            p0, p1 = q[k], q[(k + 1) % 4]
            wall = clip(ccw([p0, p1, (p1[0] + vx, p1[1] + vy), (p0[0] + vx, p0[1] + vy)]), Q)
            if len(wall) >= 3:
                F.poly(wall, cols[k])
        info.append((q, (vx, vy), far))
    F.poly([P(0, 0, 0), P(L, 0, 0), P(L, L, 0), P(0, L, 0)], FRONT)
    F.poly([P(0, L, 0), P(L, L, 0), P(L, L, L), P(0, L, L)], TOP)
    F.poly([P(L, 0, 0), P(L, 0, L), P(L, L, L), P(L, L, 0)], SIDE)
    for p, q in ((P(0, 0, 0), P(L, 0, 0)), (P(L, 0, 0), P(L, L, 0)), (P(L, L, 0), P(0, L, 0)), (P(0, L, 0), P(0, 0, 0)),
                 (P(0, L, 0), P(0, L, L)), (P(0, L, L), P(L, L, L)), (P(L, L, L), P(L, L, 0)),
                 (P(L, 0, 0), P(L, 0, L)), (P(L, 0, L), P(L, L, L))):
        F.seg(p, q, STROKE)
    for q, (vx, vy), far in info:
        for k in range(4):
            F.seg(q[k], q[(k + 1) % 4])
        for k in range(len(far)):
            F.seg(far[k], far[(k + 1) % len(far)])
        for c in q:                      # 구멍 꼭짓점에서 안쪽 꼭짓점으로(안쪽 꼭짓점이 보일 때)
            cc = (c[0] + vx, c[1] + vy)
            if any(abs(cc[0] - u[0]) < 1e-9 and abs(cc[1] - u[1]) < 1e-9 for u in far):
                F.seg(c, cc)
    dim_arc(F, P(0, 0, 0), P(L, 0, 0), "2x+y", 1)
    dim_arc(F, P(0, 0, 0), P(0, L, 0), "2x+y", -1)
    dim_arc(F, P(a, b, 0), P(b, b, 0), "x+y", -1, 10)
    return F.render()


FIGS = (("lite1_03_cube.png", fig_cube, 10000),)

if __name__ == "__main__":
    for name, fn, wd in FIGS:
        if len(sys.argv) > 1 and name not in sys.argv[1:]:
            continue
        print(name, fit_shoot(name, fn, wd, HERE))
