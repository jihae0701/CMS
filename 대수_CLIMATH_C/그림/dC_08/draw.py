# -*- coding: utf-8 -*-
"""대수 C 8. 등차수열과 등비수열 — 스캔 그림 다시 그리기 (iN = 문서의 imageN)"""
import sys, math
sys.path.insert(0, '/tmp/claude-0/-home-user-CMS/7a122d51-a5b1-5def-9637-d43cb9a9b6ef/scratchpad/figw')
from geo import *
from mathfig import Frame, dim_arc, right_mark, PINK, SKY
OUT = sys.argv[1]


def carc(F, p, q, h, arrow=False, dash=False, wd=1.6):
    """p→q 위(h>0) 또는 아래(h<0)로 휜 곡선(픽셀 h)"""
    (x1, y1), (x2, y2) = F.P(*p), F.P(*q); cx, cy = (x1 + x2) / 2, (y1 + y2) / 2 - 2 * h
    F.svg.append('<path d="M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" fill="none" stroke="#000" stroke-width="%s" %s %s/>'
                 % (x1, y1, cx, cy, x2, y2, wd, DASH if dash else '', 'marker-end="url(#am2)"' if arrow else ''))


AM = '<marker id="am2" viewBox="0 0 13 10" refX="12" refY="5" markerWidth="7.8" markerHeight="6" orient="auto"><path d="M13,5 L0.5,0.3 L2.5,5 L0.5,9.7 z" fill="#000"/></marker>'


def i2():  # 12번 해설 [다른 풀이]
    F = Frame((0, 9), (-3.4, 2.6), 46, 46, (20, 20, 20, 20)); F.svg.append('<defs>%s</defs>' % AM)
    for k, (nm, v) in enumerate((('A', '115'), ('B', '315'), ('C', '515'))):
        poly(F, [(3 * k, 0), (3 * k + 3, 0), (3 * k + 3, 2), (3 * k, 2)], None, 2.6)
        F.lab((3 * k + 1.5, 1.3), nm, 'cc'); F.lab((3 * k + 1.5, 0.6), v, 'cc')
        carc(F, (3 * k, 2), (3 * k + 3, 2), 12, dash=True, wd=1.4)
    F.lab((1.5, 2.25), 'S_{10}', 'cb', 0, -10); F.lab((4.5, 2.25), 'S_{20}-S_{10}', 'cb', 0, -10); F.lab((7.5, 2.25), 'S_{30}-S_{20}', 'cb', 0, -10)
    for k in range(2):
        carc(F, (3 * k + 1.2, -0.25), (3 * k + 4.0, -0.25), -14, arrow=True)
        F.lab((3 * k + 2.6, -0.95), '+200', 'ct')
    F.seg((2.6, -2.55), (2.6, -1.75), 1.4, 'marker-end="url(#am2)"')
    F.lab((2.6, -2.6), '\\text{공차}', 'ct', 0, 2)
    return F.render()


def i3():  # 18번 문제
    h = lambda x: 20 - 2 * x if x <= 5 else 10 + 3 * (x - 5)
    F = Frame((0, 10), (0, 25), 62, 13, (40, 40, 40, 40))
    poly(F, [(0, 0), (10, 0), (10, 25), (5, 10), (0, 20)], None, 2.6)
    for k in range(1, 10):
        x = 10 - k; F.seg((x, 0), (x, h(x)), 3.0 if k == 5 else 2.4)
    for x in range(0, 11):
        X, Y = F.P(x, 0)
        if x < 10: F.svg.append('<polyline points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="none" stroke="#000" stroke-width="1.4"/>' % (X, Y - 13, X + 13, Y - 13, X + 13, Y))
        if x > 0: F.svg.append('<polyline points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="none" stroke="#000" stroke-width="1.4"/>' % (X, Y - 13, X - 13, Y - 13, X - 13, Y)) if x in (10,) else None
    F.pt((0, 0), 'D', 'rt', -6, 4); F.pt((10, 0), 'E', 'lt', 6, 4); F.pt((0, 20), 'C', 'rb', -6, -2); F.pt((10, 25), 'A', 'lb', 6, -2)
    F.pt((5, 10), 'B', 'cb', 0, -10)
    for k, s in ((1, 'P_{1}'), (2, 'P_{2}'), (5, 'P_{5}'), (9, 'P_{9}')):
        F.lab((10 - k, 0), '\\mathrm{P}_{%d}' % k, 'ct', 0, 8)
    for x in (7.0, 3.0): F.lab((x, 0), '\\cdots', 'ct', 0, 14)
    for k in (1, 2, 9):
        x = 10 - k; F.lab((x, h(x)), '\\mathrm{Q}_{%d}' % k, 'rb', -2, -6)
    F.lab((7.0, h(7.0)), '\\cdot^{\\cdot^{\\cdot}}', 'rb', -8, -10); F.lab((3.0, h(3.0)), '\\cdots', 'cb', 0, -10)
    dim_arc(F, (5, 0), (5, 10), '10', -1, 16)
    return F.render()


def grid(F, ox, n, cell, cols):
    for (i, j), c in cols.items():
        F.poly([(ox + i * cell, j * cell), (ox + (i + 1) * cell, j * cell), (ox + (i + 1) * cell, (j + 1) * cell), (ox + i * cell, (j + 1) * cell)], c)
    for k in range(n + 1):
        w = 2.4 if k in (0, n) else 1.2
        F.seg((ox + k * cell, 0), (ox + k * cell, n * cell), w); F.seg((ox, k * cell), (ox + n * cell, k * cell), w)


def i4():  # 59번 문제
    F = Frame((0, 22), (-2.2, 9), 34, 34, (20, 20, 20, 20))
    grid(F, 0, 3, 3, {(1, 1): PINK})
    cols = {}
    for i in range(3, 6):
        for j in range(3, 6): cols[(i, j)] = PINK
    for bi in range(3):
        for bj in range(3):
            if (bi, bj) != (1, 1): cols[(3 * bi + 1, 3 * bj + 1)] = SKY
    grid(F, 13, 9, 1, cols)
    F.lab((4.5, -0.6), '\\text{[첫 번째]}', 'ct'); F.lab((17.5, -0.6), '\\text{[두 번째]}', 'ct')
    return F.render()


JOBS = {k: v for k, v in globals().items() if k[0] == 'i' and k[1:].isdigit()}
if __name__ == '__main__':
    run_crop(JOBS, OUT, sys.argv[2:])
