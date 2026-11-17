# -*- coding: utf-8 -*-
"""대수 그림 공통: 창 안만 그리는 곡선, 점근선"""
import sys, math
sys.path.insert(0, '/home/user/CMS/.claude/skills/math-figure-rules'); sys.path.insert(0, '/tmp/claude-0/-home-user-CMS/7a122d51-a5b1-5def-9637-d43cb9a9b6ef/scratchpad/figw')
from mathfig import Frame, DASH, dot, SKY
from mjcommon import odot, fdot, plot, O, run, herm, arr, PINK


def pc(F, f, a, b, y0, y1, dash=False, wd=3.2, n=400, gray=False):
    """[a,b]에서 y가 [y0,y1] 안인 부분만 그린다"""
    seg = []
    def flush():
        if len(seg) > 1:
            P = ' '.join('%.1f,%.1f' % F.P(x, y) for x, y in seg)
            st = '#999' if gray else '#000'
            F.svg.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="%s" stroke-linejoin="round" %s/>' % (P, st, wd, DASH if dash else ''))
        seg.clear()
    for i in range(n + 1):
        x = a + (b - a) * i / n
        try: y = f(x)
        except Exception: y = None
        if y is not None and y0 <= y <= y1: seg.append((x, y))
        else: flush()
    flush()


def hline(F, y, x0, x1):
    F.dashed((x0, y), (x1, y))


def vline(F, x, y0, y1):
    F.dashed((x, y0), (x, y1))


def bisect(h, a, b):
    for _ in range(80):
        m = (a + b) / 2
        if (h(a) > 0) == (h(m) > 0): a = m
        else: b = m
    return (a + b) / 2


def spiral(F, deg, r0=14, dr=5, c=(0, 0), wd=1.6, arrow=True):
    """원점에서 각 deg(도, 음수면 시계 방향)만큼 도는 나선 호(한 바퀴마다 dr px씩 커짐)와 끝 화살표"""
    X0, Y0 = F.P(*c)
    n = max(30, int(abs(deg) / 4))
    pts = []
    for i in range(n + 1):
        t = deg * i / n
        r = r0 + dr * abs(t) / 360.0
        a = math.radians(t)
        pts.append((X0 + r * math.cos(a), Y0 - r * math.sin(a)))
    F.svg.append('<polyline points="%s" fill="none" stroke="#000" stroke-width="%s"/>' % (' '.join('%.1f,%.1f' % p for p in pts), wd))
    if arrow:
        (x1, y1), (x2, y2) = pts[-2], pts[-1]
        d = math.hypot(x2 - x1, y2 - y1) or 1; ux, uy = (x2 - x1) / d, (y2 - y1) / d; h = 7
        bx, by = x2 - ux * h, y2 - uy * h
        F.svg.append('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="#000"/>' % (x2, y2, bx + uy * h * 0.45, by - ux * h * 0.45, bx - uy * h * 0.45, by + ux * h * 0.45))
    return pts[-1]


def ray(F, p, q, wd=3.2):
    (x1, y1), (x2, y2) = F.P(*p), F.P(*q)
    F.svg.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#000" stroke-width="%s" marker-end="url(#ar)"/>' % (x1, y1, x2, y2, wd))


def circ(F, c, r, wd=3.2, fill='none'):
    X, Y = F.P(*c)
    F.svg.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s" stroke="#000" stroke-width="%s"/>' % (X, Y, r * F.sx, r * F.sy, fill, wd))


def angpt(F, deg, rpx, c=(0, 0)):
    """원점에서 화면 반지름 rpx, 각 deg 자리의 수학 좌표"""
    X, Y = F.P(*c); a = math.radians(deg)
    return F.inv(X + rpx * math.cos(a), Y - rpx * math.sin(a))


if not hasattr(Frame, 'inv'):
    Frame.inv = lambda self, X, Y: (self.xr[0] + (X - self.m[0]) / self.sx, self.yr[1] - (Y - self.m[1]) / self.sy)
