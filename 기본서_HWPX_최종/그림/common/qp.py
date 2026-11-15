# -*- coding: utf-8 -*-
"""제한된 범위의 함수 그래프 공통: 범위 안 실선(3.2), 밖 점선(1.5), 끝점·꼭짓점 점(빈 점 가능), 축까지 점선, 눈금 글자"""
import sys
sys.path.insert(0, '/home/user/CMS/.claude/skills/math-figure-rules')
from mathfig import Frame, dot, DASH

def qplot(f, dom, xr, yr, sx, sy, xname='x', yname='y', pts=(), opens=(), guides=None, xt=(), yt=(),
          label=None, yaxis=True, crange=None, m=(16, 16, 16, 16), origin=True, solid_only=False):
    F = Frame(xr, yr, sx, sy, m)
    if yaxis:
        F.axes(xname, yname)
    else:
        F.xaxis(xr[0], xr[1], xname)
    lo, hi = crange or (xr[0] + 0.05 * (xr[1] - xr[0]), xr[1] - 0.05 * (xr[1] - xr[0]))
    def poly(a, b, wd, dash):
        n = 160
        P = ["%.1f,%.1f" % F.P(a + (b - a) * i / n, f(a + (b - a) * i / n)) for i in range(n + 1)]
        F.svg.append('<polyline points="%s" fill="none" stroke="#000" stroke-width="%s" stroke-linejoin="round" %s/>' % (" ".join(P), wd, dash))
    if not solid_only:
        if lo < dom[0]:
            poly(lo, dom[0], 1.5, DASH)
        if dom[1] < hi:
            poly(dom[1], hi, 1.5, DASH)
    poly(dom[0], dom[1], 3.2, '')
    for p in list(pts) + list(opens):
        gx, gy = (True, yaxis) if guides is None else guides.get(p, (True, yaxis))
        if gx and abs(p[1]) > 1e-9:
            F.dashed(p, (p[0], 0))
        if gy and abs(p[0]) > 1e-9:
            F.dashed(p, (0, p[1]))
    for p in pts:
        dot(F, p, 4.5)
    for p in opens:
        X, Y = F.P(*p)
        F.svg.append('<circle cx="%.1f" cy="%.1f" r="5" fill="#fff" stroke="#000" stroke-width="2"/>' % (X, Y))
    for x, lab in xt:
        F.lab((x, 0), lab, 'ct', 0, 8)
    for y, lab in yt:
        F.lab((0, y), lab, 'rc', -8, 0)
    if origin and yaxis:
        F.pt((0, 0), "O", "rt", -6, 4)
    if label:
        t, x, anc, dx, dy = label
        F.lab((x, f(x)), t, anc, dx, dy)
    return F
