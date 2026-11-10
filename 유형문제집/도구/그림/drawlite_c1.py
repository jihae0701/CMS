# -*- coding: utf-8 -*-
"""CMS 스토리 라이트 공통수학1 그림. python 그림/drawlite_c1.py [파일 ...]  (KATEX_DIR 필요)
- lite1_03_cube.png: 3단원 o3-69 — 모서리 2x+y인 정육면체의 각 면 가운데에 한 변이 x+y인 정사각형 구멍을 뚫은 입체
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from draw import HERE
from draw5 import fit_shoot
from draw6 import geo, dim_arc
from draw import cut_arc
import math

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


def dim2(F, p, q, label, side, k=1.0, chars=None, size=22):
    """dim_arc와 같은 점선 호(가운데를 끊고 길이)인데, 휘는 정도를 k배로 바꾸고 끊는 길이를 보이는 글자 수(chars)로 맞춘다."""
    (x1, y1), (x2, y2) = F.P(*p), F.P(*q)
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    dx, dy = x2 - x1, y2 - y1
    n = math.hypot(dx, dy)
    bulge = 0.2 * n * k
    nx, ny = -dy / n * side, dx / n * side
    cx, cy = mx + nx * 2 * bulge, my + ny * 2 * bulge
    arcs, (lx, ly) = cut_arc(x1, y1, cx, cy, x2, y2, label, size, chars=chars)
    F.svg += arcs
    F.labels.append((lx, ly, label, size, "cc", "dim"))


def fig_cube():
    """구멍 뚫린 정육면체(올림포스 유형편 03-69). 원본 그림을 따라 그린다(사용자 지시 2026-11-10):
    - 앞면 구멍: 왼쪽 아래 꼭짓점에서 구멍 가운데쯤까지 비스듬한 선, 그 끝에서 위쪽 변·오른쪽 변까지 선(안쪽은 칠하지 않음)
    - 윗면 구멍: 뒤쪽 왼쪽 꼭짓점에서 앞쪽 변까지 세로선 / 옆면 구멍: 뒤쪽 아래 꼭짓점에서 왼쪽 변까지 가로선
    - 색칠은 정육면체 세 면의 하늘색만, 길이 표시는 처음 방식(앞면 아래·왼쪽 2x+y, 구멍 윗변 x+y)."""
    L, h = 3.0, 1.1                      # 정육면체 모서리, 구멍 한 변(원본 비율)
    ox, oy = 0.5, 0.42                   # 깊이 방향 한 칸의 비스듬한 이동
    P = lambda x, y, z: (x + z * ox, y + z * oy)
    F = geo((-0.2, L + L * ox + 0.2), (-0.2, L + L * oy + 0.2), 70, (120, 30, 30, 90))
    a, b = (L - h) / 2, (L + h) / 2
    front = [P(a, a, 0), P(b, a, 0), P(b, b, 0), P(a, b, 0)]
    top = [P(a, L, a), P(b, L, a), P(b, L, b), P(a, L, b)]
    side = [P(L, a, a), P(L, a, b), P(L, b, b), P(L, b, a)]
    A0 = front[0]
    t = 0.47 * h / ox                    # 비스듬한 선의 끝이 구멍 가로의 0.47쯤에 오게(원본)
    K = (A0[0] + t * ox, A0[1] + t * oy)
    Kr, Ku = (front[1][0], K[1]), (K[0], front[3][1])
    s0, s1 = side[0], side[1]            # 옆면 구멍: 뒤쪽 아래 꼭짓점에서 왼쪽 변까지 가로선(원본)
    side_line = (s1, (s0[0], s1[1]))
    top_line = (top[3], (top[3][0], top[0][1]))   # 윗면 구멍: 뒤쪽 왼쪽 꼭짓점에서 앞쪽 변까지 세로선(원본)
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
    F.seg(A0, K); F.seg(K, Kr); F.seg(K, Ku)
    F.seg(*side_line); F.seg(*top_line)
    dim2(F, P(0, 0, 0), P(L, 0, 0), "2x+y", 1, k=0.9, chars=5.6)   # 아래 호: 곡률 10% 줄임(사용자 요청), 글자와 점선 띄움
    dim_arc(F, P(0, 0, 0), P(0, L, 0), "2x+y", -1)
    dim_arc(F, front[3], front[2], "x+y", -1, 10)
    return F.render()


FIGS = (("lite1_03_cube.png", fig_cube, 10000),)

if __name__ == "__main__":
    for name, fn, wd in FIGS:
        if len(sys.argv) > 1 and name not in sys.argv[1:]:
            continue
        print(name, fit_shoot(name, fn, wd, HERE))
