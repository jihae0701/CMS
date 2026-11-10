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
    """구멍 뚫린 정육면체(올림포스 유형편 03-69). 원본 그림처럼 그린다(사용자 지시 2026-11-10):
    - 앞면 구멍: 터널 벽의 깊이는 (모서리−구멍)/2이고 그 뒤는 가운데 빈 공간이므로, 구멍 왼쪽 아래 꼭짓점에서
      비스듬한 선 하나와 그 끝에서 위·오른쪽으로 뻗는 선 둘만 긋고, 왼쪽 벽·아래 벽만 칠한다.
    - 윗면 구멍은 테두리만, 옆면 구멍은 아래 벽의 끝선 하나.
    - 색칠은 하늘색만(세 면, 벽은 같은 방향 면의 색), 길이 표시는 처음 방식(앞면 아래·왼쪽 2x+y, 구멍 윗변 x+y)."""
    L, h = 3.0, 1.3                      # 정육면체 모서리, 구멍 한 변(그림은 개형)
    ox, oy = 0.5, 0.42                   # 깊이 방향 한 칸의 비스듬한 이동
    P = lambda x, y, z: (x + z * ox, y + z * oy)
    F = geo((-0.2, L + L * ox + 0.2), (-0.2, L + L * oy + 0.2), 70, (120, 30, 30, 90))
    a, b = (L - h) / 2, (L + h) / 2
    front = [P(a, a, 0), P(b, a, 0), P(b, b, 0), P(a, b, 0)]
    top = [P(a, L, a), P(b, L, a), P(b, L, b), P(a, L, b)]
    side = [P(L, a, a), P(L, a, b), P(L, b, b), P(L, b, a)]
    # 앞면 구멍 안
    v = (a * ox * 0.8, a * oy * 0.8)     # 벽이 끝나는 깊이(화면)
    A0, B0, C0, D0 = front
    K = (A0[0] + v[0], A0[1] + v[1])
    Kr, Ku = (B0[0], K[1]), (K[0], D0[1])
    side_wall = clip(ccw([P(L, a, a), P(L, a, b), (P(L, a, b)[0] - 0.35, P(L, a, b)[1]), (P(L, a, a)[0] - 0.35, P(L, a, a)[1])]), ccw(side))
    # poly는 맨 아래 층에 끼워 넣으므로 위에 보일 것부터
    F.poly([A0, K, Ku, D0], SIDE)        # 왼쪽 벽(오른쪽을 향함)
    F.poly([A0, B0, Kr, K], TOP)         # 아래 벽(위를 향함)
    F.poly(side_wall, TOP)
    for q in (front, top, side):
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
    F.seg(A0, K); F.seg(K, Kr); F.seg(K, Ku)
    e0, e1 = P(L, a, a), P(L, a, b)
    sw = [u for u in side_wall if min(abs(u[0] - e[0]) + abs(u[1] - e[1]) for e in (e0, e1)) > 1e-6]   # 옆면 아래 벽의 끝선
    if len(sw) >= 2:
        sw.sort(key=lambda u: u[0]); F.seg(sw[0], sw[-1])
        F.seg(e1, (e1[0] - 0.35 * F.sx, e1[1]) if False else sw[-1])      # 뒤쪽 아래 꼭짓점에서 벽 끝까지
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
