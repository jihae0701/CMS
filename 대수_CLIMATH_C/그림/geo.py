# -*- coding: utf-8 -*-
"""도형 그림 도우미: 같은 비율 틀, 다각형, 점 이름(바깥쪽), 각 표시, 같은 길이 표시, 길이 점선 호"""
import math, sys
sys.path.insert(0, '/home/user/CMS/.claude/skills/math-figure-rules')
from mathfig import Frame, dim_arc, right_mark, dot, SKY, PINK, GREEN, LAVENDER, YELLOW, DASH

DEG = '^{\\circ}'


def frame(pts, s, pad=(130, 110, 130, 110)):
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    return Frame((min(xs), max(xs)), (min(ys), max(ys)), s, s, pad)


def rot(pts, deg, c=(0, 0)):
    a = math.radians(deg); ca, sa = math.cos(a), math.sin(a)
    return [(c[0] + (x - c[0]) * ca - (y - c[1]) * sa, c[1] + (x - c[0]) * sa + (y - c[1]) * ca) for x, y in pts]


def P(r, deg, c=(0, 0)):
    a = math.radians(deg); return (c[0] + r * math.cos(a), c[1] + r * math.sin(a))


def lerp(p, q, t):
    return (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)


def inter(p1, p2, p3, p4):
    """직선 p1p2와 p3p4의 교점"""
    d = (p1[0] - p2[0]) * (p3[1] - p4[1]) - (p1[1] - p2[1]) * (p3[0] - p4[0])
    a = p1[0] * p2[1] - p1[1] * p2[0]; b = p3[0] * p4[1] - p3[1] * p4[0]
    return ((a * (p3[0] - p4[0]) - (p1[0] - p2[0]) * b) / d, (a * (p3[1] - p4[1]) - (p1[1] - p2[1]) * b) / d)


def cen(pts):
    return (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts))


def poly(F, pts, fill=None, wd=2.6, close=True):
    if fill: F.poly(pts, fill)
    q = list(pts) + ([pts[0]] if close else [])
    F.svg.append('<polyline points="%s" fill="none" stroke="#000" stroke-width="%s" stroke-linejoin="round"/>'
                 % (' '.join('%.1f,%.1f' % F.P(*p) for p in q), wd))


def seg(F, p, q, wd=1.8, dash=False):
    F.seg(p, q, wd, DASH if dash else '')


def circle(F, c, r, wd=1.8, fill='none', dash=False):
    X, Y = F.P(*c)
    F.svg.insert(1 if fill != 'none' else len(F.svg), '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="#000" stroke-width="%s" %s/>'
                 % (X, Y, r * F.sx, fill, wd, DASH if dash else ''))


def arc(F, c, r, a0, a1, wd=2.6, dash=False):
    pts = [P(r, a0 + (a1 - a0) * i / 120, c) for i in range(121)]
    F.svg.append('<polyline points="%s" fill="none" stroke="#000" stroke-width="%s" %s/>'
                 % (' '.join('%.1f,%.1f' % F.P(*p) for p in pts), wd, DASH if dash else ''))


def name(F, p, nm, c, d=10, ext=None):
    """점 이름: 중심 c에서 p 쪽 바깥으로 d픽셀"""
    X, Y = F.P(*p); CX, CY = F.P(*c)
    dx, dy = X - CX, Y - CY; n = math.hypot(dx, dy) or 1; dx, dy = dx / n, dy / n
    if ext: dx, dy = ext
    h = 'l' if dx > 0.38 else ('r' if dx < -0.38 else 'c')
    v = 't' if dy > 0.38 else ('b' if dy < -0.38 else 'c')
    F.labels.append((X + dx * d, Y + dy * d, '\\mathrm{%s}' % nm, 22, h + v))


def _dir(F, a, b):
    (x1, y1), (x2, y2) = F.P(*a), F.P(*b)
    return math.atan2(-(y2 - y1), x2 - x1)


def ang(F, V, A, B, r=24, lab=None, lr=None, n=1, wd=1.5):
    """꼭짓점 V에서 VA→VB 사이(작은 쪽) 각 호. lab: 각 글자(호 바깥, 이등분선 위)"""
    X, Y = F.P(*V)
    a1, a2 = _dir(F, V, A), _dir(F, V, B)
    d = (a2 - a1 + 3 * math.pi) % (2 * math.pi) - math.pi
    for k in range(n):
        rr = r + 5 * k
        pts = [(X + rr * math.cos(a1 + d * i / 40), Y - rr * math.sin(a1 + d * i / 40)) for i in range(41)]
        F.svg.append('<polyline points="%s" fill="none" stroke="#000" stroke-width="%s"/>' % (' '.join('%.1f,%.1f' % p for p in pts), wd))
    if lab:
        m = a1 + d / 2; L = lr or (r + 18)
        F.labels.append((X + L * math.cos(m), Y - L * math.sin(m), lab, 22, 'cc'))


def tick(F, p, q, n=1, t=0.5, L=7):
    (x1, y1), (x2, y2) = F.P(*p), F.P(*q)
    mx, my = x1 + (x2 - x1) * t, y1 + (y2 - y1) * t
    dx, dy = x2 - x1, y2 - y1; k = math.hypot(dx, dy); ux, uy = dx / k, dy / k; nx, ny = -uy, ux
    for i in range(n):
        o = (i - (n - 1) / 2) * 5
        cx, cy = mx + ux * o, my + uy * o
        F.svg.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#000" stroke-width="1.6"/>' % (cx - nx * L, cy - ny * L, cx + nx * L, cy + ny * L))


def omark(F, p, q, t=0.5):
    X, Y = F.P(*lerp(p, q, t))
    F.svg.append('<circle cx="%.1f" cy="%.1f" r="4.5" fill="#fff" stroke="#000" stroke-width="1.5"/>' % (X, Y))


def dim(F, p, q, lab, c, bulge=16):
    """길이 점선 호: 중심 c 반대쪽으로 휜다"""
    (x1, y1), (x2, y2) = F.P(*p), F.P(*q); CX, CY = F.P(*c)
    dx, dy = x2 - x1, y2 - y1
    nx, ny = -dy, dx
    side = 1 if (nx * (CX - (x1 + x2) / 2) + ny * (CY - (y1 + y2) / 2)) < 0 else -1
    dim_arc(F, p, q, lab, side, bulge)


def clab(F, p, q, lab, c, d=16, t=0.5):
    """선분 pq 옆(c 쪽으로 d픽셀)에 길이 글자 — 원의 현처럼 점선 호를 둘 수 없을 때"""
    X, Y = F.P(*lerp(p, q, t)); CX, CY = F.P(*c)
    (x1, y1), (x2, y2) = F.P(*p), F.P(*q); nx, ny = -(y2 - y1), x2 - x1; n = math.hypot(nx, ny); nx, ny = nx / n, ny / n
    if nx * (CX - X) + ny * (CY - Y) < 0: nx, ny = -nx, -ny
    F.labels.append((X + nx * d, Y + ny * d, lab, 22, 'cc'))


def run_crop(JOBS, OUT, names, long_side=10000, wide=()):
    """여백을 넉넉히 두고 찍은 뒤 흰 테두리를 잘라 낸다(1픽셀=6.4 HWPUNIT 유지, 긴 변 약 10000)"""
    import json, os
    import mathfig
    from mathfig import fit_shoot, K_HWP
    from PIL import Image
    wf = os.path.join(OUT, 'widths.json'); W = json.load(open(wf)) if os.path.exists(wf) else {}
    nf = os.path.join(OUT, 'label_nudge.json')
    def crop(fn):
        im = Image.open(fn).convert('RGB'); g = im.convert('L').point(lambda v: 255 if v < 245 else 0)
        b = g.getbbox(); pad = 18
        b = (max(0, b[0] - pad), max(0, b[1] - pad), min(im.width, b[2] + pad), min(im.height, b[3] + pad))
        im.crop(b).save(fn); return b[2] - b[0], b[3] - b[1]
    for k in names or list(JOBS):
        N = json.load(open(nf)) if os.path.exists(nf) else {}
        N.pop(k + '.png', None); mathfig.NUDGE.pop(k + '.png', None); json.dump(N, open(nf, 'w'))
        fn = os.path.join(OUT, k + '.png'); LS = 18000 if k in wide else long_side
        tw = fit_shoot(k + '.png', JOBS[k], LS if k in wide else None, out_dir=OUT)
        for _ in range(2):
            cw, ch = crop(fn); L = max(cw, ch) * K_HWP
            if abs(L - LS) < 400: break
            tw = int(tw * LS / L)
            N = json.load(open(nf)) if os.path.exists(nf) else {}
            N.pop(k + '.png', None); mathfig.NUDGE.pop(k + '.png', None); json.dump(N, open(nf, 'w'))
            fit_shoot(k + '.png', JOBS[k], tw, out_dir=OUT)
        cw, ch = crop(fn)
        W[k] = int(round(cw * K_HWP)); print(k, W[k], int(ch * K_HWP))
    json.dump(W, open(wf, 'w'), indent=0)
