# -*- coding: utf-8 -*-
"""대수 C 6. 삼각함수의 그래프 — 스캔 그림 다시 그리기 (iN = 문서의 imageN)"""
import sys, math
sys.path.insert(0, '/tmp/claude-0/-home-user-CMS/7a122d51-a5b1-5def-9637-d43cb9a9b6ef/scratchpad/figw')
from dcommon import *
from autolab import Grid, place, box, est
import mathfig
mathfig.check_and_nudge = lambda name, html, w, h: ([], [])  # 자리는 autolab이 고름
OUT = sys.argv[1]
pi = math.pi; s, c, t = math.sin, math.cos, math.tan
r2, r3 = math.sqrt(2), math.sqrt(3)


def T(f):
    """tan류: 점근선 근처 값은 None"""
    def g(x):
        try:
            v = f(x)
        except Exception:
            return None
        return v if abs(v) < 1e6 else None
    return g


def G(*a, **k):
    """여백은 글자가 놓인 자리에 맞춰 정한다(두 번 그림)"""
    k['m'] = (300, 200, 300, 200)
    F, placed = _G(*a, **k)
    x0 = min([b[0] for b in placed] + [F.m[0] - 4]); y0 = min([b[1] for b in placed] + [F.m[1] - 30])
    x1 = max([b[2] for b in placed] + [F.w - F.m[2] + 8]); y1 = max([b[3] for b in placed] + [F.h - F.m[3] + 4])
    k['m'] = (int(F.m[0] - x0 + 8), int(F.m[1] - y0 + 6), int(x1 - (F.w - F.m[2]) + 14), int(y1 - (F.h - F.m[3]) + 6))
    F, placed = _G(*a, **k)
    return F.render()


def _G(xr, yr, sx, sy, curves=(), H=(), V=(), K=(), asym=(), xt=(), yt=(), dots=(), odots=(), labs=(), xname='x', m=(40, 16, 150, 16), Oanc=('rt', -6, 4), fill=None):
    if yr[1] - yr[0] <= 3.3: sy = max(sy, 95)
    F = Frame(xr, yr, sx, sy, m)
    gr = Grid(); ax = Grid(); da = Grid(); placed = []
    if fill:
        f, a, b, y0 = fill
        n = 200; pts = [(a + (b - a) * i / n, max(min(f(a + (b - a) * i / n), yr[1]), y0)) for i in range(n + 1)]
        F.poly([(a, y0)] + pts + [(b, y0)], SKY)
    F.axes(xname, 'y')
    for L in F.labels:           # x, y, O 글자 자리
        X, Y, tex, sz, anc = L
        placed.append(box(X, Y, *est(tex.replace('\\mathrm', '')), anc))
    ax.seg(F.P(xr[0], 0), F.P(xr[1], 0)); ax.seg(F.P(0, yr[0]), F.P(0, yr[1]))
    for (y, x0, x1) in H: hline(F, y, x0, x1); da.seg(F.P(x0, y), F.P(x1, y))
    for (x, y0, y1) in V: vline(F, x, y0, y1); da.seg(F.P(x, y0), F.P(x, y1))
    for x in asym:
        y1 = yr[1] - 0.02 * (yr[1] - yr[0]); vline(F, x, yr[0], y1); da.seg(F.P(x, yr[0]), F.P(x, y1))
    klabs = []
    for item in K:
        y, lab = item[0], item[1]
        x0 = item[2] if len(item) > 2 else (0 if any(abs(t[0] - y) < 1e-9 for t in yt) else xr[0]); x1 = item[3] if len(item) > 3 else xr[1] - 0.03 * (xr[1] - xr[0])
        F.seg((x0, y), (x1, y), 2.0); da.seg(F.P(x0, y), F.P(x1, y))
        if lab: klabs.append((F.P(x1, y), lab))
    for cv in curves:
        f, a, b, k = cv[:4]
        ytop = yr[1] - 0.08 * (yr[1] - yr[0])
        pc(F, T(f), a, b, yr[0], ytop, dash=(k == 'D'), gray=(k == 'G'), wd=(2.6 if k == 'G' else 3.2), n=900)
        g = T(f); prev = None
        for i in range(1201):
            x = a + (b - a) * i / 1200
            try: y = g(x)
            except Exception: y = None
            if y is not None and yr[0] <= y <= ytop:
                p = F.P(x, y)
                if prev: gr.seg(prev, p)
                prev = p
            else: prev = None
    for p in list(dots) + list(odots):
        X, Y = F.P(*p)
        for dx in (-5, 0, 5):
            for dy in (-5, 0, 5): gr.add(X + dx, Y + dy)
    for p in dots: fdot(F, p)
    for p in odots: odot(F, p)
    for (X, Y), lab in klabs:
        place(F, (ax, gr, da), placed, [(X + 8, Y, 'lc'), (X + 8, Y - 4, 'lb', 3), (X + 8, Y + 4, 'lt', 3), (X + 8, Y - 14, 'lc', 3), (X + 8, Y + 14, 'lc', 3), (X, Y - 6, 'rb'), (X, Y + 6, 'rt'), (X - 40, Y - 6, 'rb'), (X - 40, Y + 6, 'rt')], lab)
    X0, Y0 = F.P(0, 0)
    oc = [(X0 + Oanc[1], Y0 + Oanc[2], Oanc[0])] + [(X0 + dx, Y0 + dy, an, 6) for an, dx, dy in (('rt', -6, 4), ('lt', 6, 4), ('rb', -6, -4), ('lb', 6, -4), ('rt', -12, 8), ('lt', 12, 8))]
    place(F, (ax, gr, da), placed, oc, '\\mathrm{O}')
    POS = {'b': (0, 8, 'ct'), 't': (0, -6, 'cb'), 'bl': (-2, 6, 'rt'), 'br': (4, 6, 'lt'), 'tl': (-3, -6, 'rb'), 'tr': (5, -6, 'lb')}
    ORD = ['b', 't', 'br', 'bl', 'tr', 'tl']
    for x, tex, pos in xt:
        X, Y = F.P(x, 0)
        keys = [pos] + [k for k in ORD if k != pos]
        cands = [(X + POS[k][0], Y + POS[k][1], POS[k][2]) for k in keys]
        cands += [(X + POS[k][0] + s * d, Y + POS[k][1], POS[k][2]) for d in (10, 20) for k in keys for s in (-1, 1)]
        cands += [(X + d, Y + 26, 'ct') for d in (0, -14, 14)] + [(X + d, Y - 24, 'cb') for d in (0, -14, 14)]
        place(F, (ax, gr, da), placed, cands, tex)
    for item in yt:
        y, tex = item[0], item[1]; side = item[2] if len(item) > 2 else 'l'
        X, Y = F.P(0, y)
        L = [(X - 8, Y, 'rc', 0), (X - 7, Y - 6, 'rb', 12), (X - 7, Y + 6, 'rt', 12)]
        R = [(X + 8, Y, 'lc', 4), (X + 7, Y - 6, 'lb', 16), (X + 7, Y + 6, 'lt', 16)]
        place(F, (ax, gr, da), placed, (L + R) if side == 'l' else (R + L), tex)
    for p, tex, anc, dx, dy in labs:
        X, Y = F.P(*p); X += dx; Y += dy
        cands = [(X + ddx, Y + ddy, anc) for r in range(0, 6) for ddx, ddy in ([(0, 0)] if r == 0 else [(0, -12 * r), (0, 12 * r), (-18 * r, 0), (18 * r, 0), (-18 * r, -12 * r), (18 * r, -12 * r), (-18 * r, 12 * r), (18 * r, 12 * r)])]
        place(F, (ax, gr, da), placed, cands, tex)
    return F, placed


P = lambda k: k * pi
def fr(a, b, neg=False):
    return ('-' if neg else '') + '\\dfrac{%s}{%s}\\pi' % (a, b) if a != 1 else ('-' if neg else '') + '\\dfrac{\\pi}{%s}' % b


def i2():  # 1⑴ y=2sin(x/3)
    f = lambda x: 2 * s(x / 3)
    return G((-0.6, 9.6 * pi), (-2.6, 2.8), 14, 40, [(f, -0.6, 9.3 * pi, 'S')],
             H=[(2, 0, 7.5 * pi), (-2, 0, 4.5 * pi)], V=[(1.5 * pi, 0, 2), (4.5 * pi, 0, -2), (7.5 * pi, 0, 2)],
             xt=[(1.5 * pi, fr(3, 2), 'b'), (3 * pi, '3\\pi', 'tl'), (4.5 * pi, fr(9, 2), 't'), (6 * pi, '6\\pi', 'bl'), (7.5 * pi, fr(15, 2), 'b'), (9 * pi, '9\\pi', 'tl')],
             yt=[(2, '2'), (-2, '-2')], labs=[((8.3 * pi, 2.2), 'y=2\\sin\\dfrac{x}{3}', 'lb', 0, -4)])


def i3():  # 1⑵ y=2sin(x-π/2)-1, y=2sin x
    f = lambda x: 2 * s(x - pi / 2) - 1; g = lambda x: 2 * s(x)
    return G((-0.6, 2.7 * pi), (-3.6, 2.8), 44, 62, [(g, -0.6, 2.6 * pi, 'G'), (f, -0.6, 2.6 * pi, 'S')],
             H=[(2, 0, 2.5 * pi), (1, 0, pi), (-1, 0, 2 * pi), (-3, 0, 2 * pi)], V=[(pi, 0, 1), (2 * pi, 0, -3), (0.5 * pi, 0, 2), (1.5 * pi, 0, -2)],
             xt=[(0.5 * pi, '\\dfrac{\\pi}{2}', 't'), (pi, '\\pi', 'br'), (1.5 * pi, fr(3, 2), 't'), (2 * pi, '2\\pi', 'tr')],
             yt=[(2, '2'), (1, '1'), (-1, '-1'), (-2, '-2'), (-3, '-3')],
             labs=[((0.5 * pi, 2), 'y=2\\sin x', 'lb', 8, -4), ((2.2 * pi, f(2.2 * pi)), 'y=2\\sin\\left(x-\\dfrac{\\pi}{2}\\right)-1', 'lt', 4, 8)], m=(40, 16, 100, 60))


def i4():  # 2번 문제 y=a sin bx (5 sin x/3)
    f = lambda x: 5 * s(x / 3)
    return G((-0.6, 8.6 * pi), (-6.2, 6.6), 16, 18, [(f, -0.6, 8.5 * pi, 'S')],
             H=[(5, 0, 7.5 * pi), (-5, 0, 4.5 * pi)], V=[(1.5 * pi, 0, 5), (4.5 * pi, 0, -5), (7.5 * pi, 0, 5)],
             xt=[(1.5 * pi, fr(3, 2), 'b'), (3 * pi, '3\\pi', 'tl'), (4.5 * pi, fr(9, 2), 't'), (6 * pi, '6\\pi', 'bl'), (7.5 * pi, fr(15, 2), 'b')],
             yt=[(5, '5'), (-5, '-5')], m=(40, 16, 30, 16))


def i5():  # 4⑴ y=sin2x, y=sin x
    return G((-0.75 * pi, 2.3 * pi), (-1.5, 1.6), 50, 70, [(lambda x: s(x), -0.75 * pi, 2.25 * pi, 'D'), (lambda x: s(2 * x), -0.75 * pi, 2.25 * pi, 'S')],
             H=[(1, -0.75 * pi, 2.2 * pi), (-1, -0.75 * pi, 2.2 * pi)],
             xt=[(-0.5 * pi, '-\\dfrac{\\pi}{2}', 'b'), (0.5 * pi, '\\dfrac{\\pi}{2}', 'b'), (pi, '\\pi', 'tr'), (1.5 * pi, fr(3, 2), 'b'), (2 * pi, '2\\pi', 'tr')],
             yt=[(1, '1'), (-1, '-1')], labs=[((1.25 * pi, 1), 'y=\\sin 2x', 'cb', 0, -6), ((2.1 * pi, s(2.1 * pi) - 0.6), 'y=\\sin x', 'lc', 4, 0)], m=(40, 16, 110, 16))


def i6():  # 4⑵ y=-3sin2x
    f = lambda x: -3 * s(2 * x)
    ks = [(k, ) for k in range(1, 12)]
    return G((-0.25 * pi, 3.2 * pi), (-3.7, 3.9), 46, 30, [(f, -0.25 * pi, 3.15 * pi, 'S')],
             H=[(3, -0.25 * pi, 3.1 * pi), (-3, -0.25 * pi, 3.1 * pi)],
             xt=[(0.5 * pi, '\\dfrac{\\pi}{2}', 'tr'), (pi, '\\pi', 'bl'), (1.5 * pi, fr(3, 2), 'tr'), (2 * pi, '2\\pi', 'bl'), (2.5 * pi, fr(5, 2), 'tr'), (3 * pi, '3\\pi', 'tr')],
             yt=[(3, '3'), (-3, '-3')], labs=[((2.7 * pi, -3), 'y=-3\\sin 2x', 'ct', 0, 8)], m=(40, 16, 30, 40))


def i7():  # 4⑶ y=sin(x-π/2), y=sin x
    return G((-0.75 * pi, 2.4 * pi), (-1.5, 1.6), 50, 70, [(lambda x: s(x), -0.75 * pi, 2.35 * pi, 'D'), (lambda x: s(x - pi / 2), -0.75 * pi, 2.35 * pi, 'S')],
             H=[(1, -0.75 * pi, 2.3 * pi), (-1, -0.75 * pi, 2.3 * pi)],
             xt=[(-0.5 * pi, '-\\dfrac{\\pi}{2}', 'b'), (0.5 * pi, '\\dfrac{\\pi}{2}', 'b'), (pi, '\\pi', 'tr'), (1.5 * pi, fr(3, 2), 'b'), (2 * pi, '2\\pi', 'tr')],
             yt=[(1, '1'), (-1, '-1')], labs=[((pi, 1), 'y=\\sin\\left(x-\\dfrac{\\pi}{2}\\right)', 'cb', 0, -6), ((2.35 * pi, -1), 'y=\\sin x', 'lc', 6, 0)], m=(40, 16, 100, 16))


def i8():  # 4⑷ y=2sinπx+1, y=sinπx
    return G((-2.6, 4.7), (-1.6, 3.8), 60, 50, [(lambda x: s(pi * x), -2.6, 4.6, 'G'), (lambda x: 2 * s(pi * x) + 1, -2.6, 4.6, 'S')],
             H=[(3, -2.6, 4.5), (1, -2.6, 4.5), (-1, -2.6, 4.5)],
             xt=[(-2, '-2', 'bl'), (-1, '-1', 'bl'), (1, '1', 'br'), (2, '2', 'br'), (3, '3', 'br'), (4, '4', 'br')],
             yt=[(3, '3'), (1, '1'), (-1, '-1')], labs=[((2.5, 3), 'y=2\\sin\\pi x+1', 'cb', 0, -6), ((4.0, -1), 'y=\\sin\\pi x', 'ct', 0, 8)], m=(40, 16, 30, 40))


def i9():  # 7번 y=2sin(2x-3π/4)
    f = lambda x: 2 * s(2 * x - 0.75 * pi)
    return G((-0.4 * pi, 1.75 * pi), (-2.6, 2.8), 70, 40, [(f, -0.4 * pi, 1.7 * pi, 'S')],
             H=[(2, -0.4 * pi, 1.6 * pi), (-2, -0.4 * pi, 1.6 * pi)],
             xt=[(0.375 * pi, fr(3, 8), 'bl'), (0.875 * pi, fr(7, 8), 'br')], yt=[(2, '2'), (-2, '-2')],
             labs=[((1.25 * pi, 2), 'y=a\\sin(bx-c)', 'cb', 0, -6)], m=(40, 30, 30, 16))


def i10():  # 8⑴ y=3cos(x/2)
    f = lambda x: 3 * c(x / 2)
    return G((-0.6 * pi, 9.6 * pi), (-3.8, 4.2), 14, 30, [(f, -0.6 * pi, 9.5 * pi, 'S')],
             H=[(3, 0, 8 * pi), (-3, 0, 6 * pi)], V=[(2 * pi, 0, -3), (4 * pi, 0, 3), (6 * pi, 0, -3), (8 * pi, 0, 3)],
             xt=[(pi, '\\pi', 'bl'), (2 * pi, '2\\pi', 't'), (3 * pi, '3\\pi', 'br'), (4 * pi, '4\\pi', 'b'), (5 * pi, '5\\pi', 'tl'), (6 * pi, '6\\pi', 't'), (7 * pi, '7\\pi', 'bl'), (8 * pi, '8\\pi', 'b'), (9 * pi, '9\\pi', 'tr')],
             yt=[(3, '3'), (-3, '-3')], labs=[((8 * pi, 3), 'y=3\\cos\\dfrac{x}{2}', 'cb', 0, -6)], m=(40, 40, 30, 16))


def i11():  # 10⑴ y=½cos x, y=cos x
    return G((-1.3 * pi, 2.35 * pi), (-1.5, 1.6), 46, 110, [(lambda x: c(x), -1.3 * pi, 2.3 * pi, 'D'), (lambda x: 0.5 * c(x), -1.3 * pi, 2.3 * pi, 'S')],
             H=[(1, -1.3 * pi, 2.2 * pi), (0.5, -1.3 * pi, 2.2 * pi), (-0.5, -1.3 * pi, 2.2 * pi), (-1, -1.3 * pi, 2.2 * pi)],
             xt=[(-pi, '-\\pi', 'tl'), (pi, '\\pi', 'tr'), (2 * pi, '2\\pi', 'br')],
             yt=[(1, '1', 'r'), (0.5, '\\dfrac{1}{2}', 'r'), (-0.5, '-\\dfrac{1}{2}', 'r'), (-1, '-1', 'r')],
             labs=[((2.0 * pi, 0.5), 'y=\\dfrac{1}{2}\\cos x', 'lb', 8, -8), ((1.4 * pi, -1), 'y=\\cos x', 'ct', 0, 6)], m=(40, 16, 100, 16), Oanc=('rt', -6, 4))


def i12():  # 10⑵ y=2cos3x
    f = lambda x: 2 * c(3 * x)
    return G((-0.4 * pi, 1.45 * pi), (-2.7, 2.8), 100, 40, [(f, -0.4 * pi, 1.42 * pi, 'S')],
             H=[(2, -0.4 * pi, 1.4 * pi), (-2, -0.4 * pi, 1.4 * pi)], V=[(pi / 3, 0, -2), (2 * pi / 3, 0, 2), (pi, 0, -2), (4 * pi / 3, 0, 2)],
             xt=[(pi / 6, '\\dfrac{\\pi}{6}', 'br'), (pi / 3, '\\dfrac{\\pi}{3}', 't'), (pi / 2, '\\dfrac{\\pi}{2}', 'tr'), (2 * pi / 3, fr(2, 3), 'b'), (5 * pi / 6, fr(5, 6), 't'), (pi, '\\pi', 'b'), (7 * pi / 6, fr(7, 6), 't'), (4 * pi / 3, fr(4, 3), 'b')],
             yt=[(2, '2'), (-2, '-2')], labs=[((pi / 2, 2), 'y=2\\cos 3x', 'cb', 0, -6)], m=(40, 16, 30, 16))


def i13():  # 10⑶ y=3cos(x-π/4), y=cos x
    f = lambda x: 3 * c(x - pi / 4)
    return G((-0.6 * pi, 2.6 * pi), (-3.8, 4.1), 52, 34, [(lambda x: c(x), -0.6 * pi, 2.55 * pi, 'D'), (f, -0.6 * pi, 2.55 * pi, 'S')],
             H=[(3, 0, 2.25 * pi), (1, -0.6 * pi, 2.5 * pi), (-1, -0.6 * pi, 2.5 * pi), (-3, 0, 1.25 * pi)], V=[(pi / 4, 0, 3), (1.25 * pi, 0, -3), (2.25 * pi, 0, 3)],
             xt=[(pi / 4, '\\dfrac{\\pi}{4}', 'b'), (1.25 * pi, fr(5, 4), 't'), (2.25 * pi, fr(9, 4), 'b')],
             yt=[(3, '3'), (1, '1'), (-1, '-1'), (-3, '-3')],
             labs=[((2.25 * pi, 3), 'y=3\\cos\\left(x-\\dfrac{\\pi}{4}\\right)', 'cb', 0, -6), ((1.0 * pi, -1), 'y=\\cos x', 'ct', 0, 8)], m=(40, 40, 30, 30))


def i14():  # 10⑷ y=cos½(x-2π/3)-1, y=cos½x
    f = lambda x: c((x - 2 * pi / 3) / 2) - 1; g = lambda x: c(x / 2)
    return G((-0.3 * pi, 5.1 * pi), (-2.6, 1.6), 24, 56, [(g, -0.3 * pi, 5.05 * pi, 'G'), (f, -0.3 * pi, 5.05 * pi, 'S')],
             H=[(1, 0, 4 * pi), (-1, 0, 4.67 * pi), (-2, 0, 2.67 * pi)], V=[(8 * pi / 3, 0, -2), (4 * pi, 0, 1)],
             xt=[(2 * pi / 3, fr(2, 3), 'b'), (pi, '\\pi', 'tr'), (2 * pi, '2\\pi', 't'), (8 * pi / 3, fr(8, 3), 't'), (3 * pi, '3\\pi', 'br'), (4 * pi, '4\\pi', 't'), (14 * pi / 3, fr(14, 3), 'b'), (5 * pi, '5\\pi', 'tl')],
             yt=[(1, '1'), (-1, '-1'), (-2, '-2')],
             labs=[((4.2 * pi, 1.05), 'y=\\cos\\dfrac{1}{2}x', 'lb', 0, -4), ((2.67 * pi, -2), 'y=\\cos\\dfrac{1}{2}\\left(x-\\dfrac{2}{3}\\pi\\right)-1', 'ct', 0, 8)], m=(40, 30, 100, 60))


def i15():  # 13번 y=2cos(2x-π)-1
    f = lambda x: 2 * c(2 * x - pi) - 1
    return G((-0.4 * pi, 2.2 * pi), (-3.6, 2.0), 60, 40, [(f, -0.4 * pi, 2.15 * pi, 'S')],
             H=[(1, 0, 2.1 * pi), (-3, -0.4 * pi, 2.1 * pi)], V=[(pi / 2, 0, 1)],
             xt=[(pi / 2, '\\dfrac{\\pi}{2}', 'b')], yt=[(1, '1'), (-3, '-3')],
             labs=[((1.1 * pi, 1), 'y=a\\cos(bx-c)+d', 'cb', 0, -6)], m=(40, 30, 30, 16))


def i16():  # 14⑴ y=tan(x/2)
    f = lambda x: t(x / 2)
    return G((-1.6 * pi, 3.6 * pi), (-3.2, 3.2), 30, 40, [(f, -1.6 * pi, 3.55 * pi, 'S')], asym=[-pi, pi, 3 * pi],
             xt=[(-pi, '-\\pi', 'bl'), (pi, '\\pi', 'br'), (2 * pi, '2\\pi', 'br'), (3 * pi, '3\\pi', 'br')],
             labs=[((2.6 * pi, 2.6), 'y=\\tan\\dfrac{x}{2}', 'rc', -10, 0)], m=(40, 16, 30, 16))


def i17():  # 14⑵ y=½tan4x
    f = lambda x: 0.5 * t(4 * x)
    return G((-0.12 * pi, 0.62 * pi), (-2.2, 2.2), 260, 50, [(f, -0.12 * pi, 0.6 * pi, 'S')], asym=[pi / 8, 3 * pi / 8, 5 * pi / 8 - 0.0001],
             xt=[(pi / 8, '\\dfrac{\\pi}{8}', 'br'), (pi / 4, '\\dfrac{\\pi}{4}', 'b'), (3 * pi / 8, fr(3, 8), 'br'), (pi / 2, '\\dfrac{\\pi}{2}', 'b')],
             labs=[((0.4 * pi, 2.0), 'y=\\dfrac{1}{2}\\tan 4x', 'lc', 6, 0)], m=(40, 16, 30, 16))


def i18():  # 16번 y=tan(2x-π/2)
    f = lambda x: t(2 * x - pi / 2)
    return G((-0.6 * pi, 1.15 * pi), (-2.6, 2.6), 90, 46, [(f, -0.6 * pi, 1.12 * pi, 'S')], asym=[-pi / 2, pi / 2, pi],
             xt=[(-pi / 2, '-\\dfrac{\\pi}{2}', 'bl'), (pi / 2, '\\dfrac{\\pi}{2}', 'br'), (pi, '\\pi', 'br')], m=(40, 16, 30, 16), Oanc=('rt', -6, 4))


def i19():  # 17⑴ y=2tan(x/3)
    f = lambda x: 2 * t(x / 3)
    return G((-3.4 * pi, 8.3 * pi), (-3.2, 4.4), 14, 40, [(f, -3.4 * pi, 8.25 * pi, 'S')], asym=[-1.5 * pi, 1.5 * pi, 4.5 * pi, 7.5 * pi],
             xt=[(-3 * pi, '-3\\pi', 't'), (-1.5 * pi, '-\\dfrac{3}{2}\\pi', 'bl'), (1.5 * pi, fr(3, 2), 'tr'), (3 * pi, '3\\pi', 'b'), (4.5 * pi, fr(9, 2), 'tr'), (6 * pi, '6\\pi', 'b'), (7.5 * pi, fr(15, 2), 'tr')],
             labs=[((7.6 * pi, 3.0), 'y=2\\tan\\dfrac{x}{3}', 'lc', 6, 0)], m=(40, 16, 60, 16))


def i20():  # 17⑵ y=tan(x/2-π/2), y=tan(x/2)
    f = lambda x: t(x / 2 - pi / 2); g = lambda x: t(x / 2)
    return G((-2.4 * pi, 4.4 * pi), (-3.2, 3.2), 30, 62, [(g, -2.6 * pi, 4.55 * pi, 'G'), (f, -2.6 * pi, 4.55 * pi, 'S')], asym=[-2 * pi, 0.0001, 2 * pi, 4 * pi],
             xt=[(-pi, '-\\pi', 'br'), (pi, '\\pi', 'br'), (2 * pi, '2\\pi', 'tl'), (3 * pi, '3\\pi', 'br')], Oanc=('lt', 6, 4),
             labs=[((-2.3 * pi, 2.8), 'y=\\tan\\dfrac{x}{2}', 'lc', 0, 0), ((2.4 * pi, -2.9), 'y=\\tan\\left(\\dfrac{x}{2}-\\dfrac{\\pi}{2}\\right)', 'lc', 8, 0)], m=(40, 16, 30, 16))


def i21():  # 17⑶ y=tan(x-π/2)+2
    f = lambda x: t(x - pi / 2) + 2
    return G((-0.4 * pi, 2.3 * pi), (-1.6, 5.4), 50, 36, [(f, -0.4 * pi, 2.25 * pi, 'S')], H=[(2, -0.4 * pi, 2.2 * pi)], asym=[pi, 2 * pi],
             xt=[(pi / 2, '\\dfrac{\\pi}{2}', 'b'), (pi, '\\pi', 'br'), (1.5 * pi, fr(3, 2), 'b'), (2 * pi, '2\\pi', 'br')], yt=[(2, '2')],
             labs=[((1.05 * pi, 4.6), 'y=\\tan\\left(x-\\dfrac{\\pi}{2}\\right)+2', 'lc', 6, 0)], m=(40, 16, 30, 16))


# 방정식·부등식 그림 (0~2π)
def eq(f, k, klab, xs, ytick, fname, xr=(-0.25 * pi, 2.25 * pi), yr=(-1.5, 1.6), solid=None, gray=None, extra=(), opend=(2 * pi,), xname='x', start=0, m=(80, 16, 130, 16)):
    curves = []
    if solid is None:
        curves.append((f, start, 2 * pi if xname == 'x' else xr[1], 'S'))
    else:
        if gray: curves += [(f, a, b, 'G') for a, b in gray]
        curves += [(f, a, b, 'S') for a, b in solid]
    dots = [(x, k) for x, _ in xs]
    V = [(x, 0, k) for x, _ in xs]
    xt = [(x, lab, 'b' if k >= 0 else 't') for x, lab in xs]
    return G(xr, yr, 50, 70, curves, H=[(1, 0, 2 * pi), (-1, 0, 2 * pi)], V=V, K=[(k, klab)], xt=xt + list(extra), yt=ytick,
             dots=dots, odots=[(x, f(x)) for x in opend], labs=[], xname=xname, m=m)


def i22():  # 19⑴ sin x = -√3/2
    return G((-0.25 * pi, 2.3 * pi), (-1.5, 1.6), 50, 70, [(s, 0, 2 * pi, 'S')], H=[(1, 0, pi / 2), (-1, 0, 1.5 * pi)], V=[(pi / 2, 0, 1), (4 * pi / 3, 0, -r3 / 2), (5 * pi / 3, 0, -r3 / 2), (1.5 * pi, 0, -1)],
             K=[(-r3 / 2, 'y=-\\dfrac{\\sqrt{3}}{2}')], xt=[(pi / 2, '\\dfrac{\\pi}{2}', 'b'), (pi, '\\pi', 'bl'), (4 * pi / 3, fr(4, 3), 't'), (5 * pi / 3, fr(5, 3), 'tr'), (1.5 * pi, fr(3, 2), 't'), (2 * pi, '2\\pi', 'br')],
             yt=[(1, '1'), (-1, '-1')], dots=[(0, 0), (4 * pi / 3, -r3 / 2), (5 * pi / 3, -r3 / 2)], odots=[(2 * pi, 0)],
             labs=[((pi / 2, 1), 'y=\\sin x', 'cb', 0, -6)], m=(60, 16, 130, 16))


def i23():  # 19⑵ cos x = 1/√2
    return G((-0.25 * pi, 2.3 * pi), (-1.5, 1.6), 50, 70, [(c, 0, 2 * pi, 'S')], H=[(1, 0, 2 * pi), (-1, 0, pi)], V=[(pi / 4, 0, 1 / r2), (7 * pi / 4, 0, 1 / r2), (2 * pi, 0, 1), (pi, 0, -1)],
             K=[(1 / r2, 'y=\\dfrac{1}{\\sqrt{2}}')], xt=[(pi / 4, '\\dfrac{\\pi}{4}', 'b'), (pi / 2, '\\dfrac{\\pi}{2}', 'b'), (pi, '\\pi', 't'), (1.5 * pi, fr(3, 2), 'b'), (7 * pi / 4, fr(7, 4), 'b'), (2 * pi, '2\\pi', 'br')],
             yt=[(1, '1'), (-1, '-1'), (1 / r2, '\\dfrac{1}{\\sqrt{2}}')], dots=[(0, 1), (pi / 4, 1 / r2), (7 * pi / 4, 1 / r2)], odots=[(2 * pi, 1)],
             labs=[((pi, -1), 'y=\\cos x', 'ct', 0, 8)], m=(60, 16, 120, 30))


def i24():  # 19⑶ tan x = -√3
    return G((-0.25 * pi, 2.3 * pi), (-2.6, 2.6), 50, 50, [(t, 0, 2 * pi, 'S')], asym=[pi / 2, 1.5 * pi], V=[(2 * pi / 3, 0, -r3), (5 * pi / 3, 0, -r3)],
             K=[(-r3, 'y=-\\sqrt{3}')], xt=[(2 * pi / 3, fr(2, 3), 't'), (pi, '\\pi', 'br'), (5 * pi / 3, fr(5, 3), 't'), (2 * pi, '2\\pi', 'br')],
             yt=[(-r3, '-\\sqrt{3}')], dots=[(0, 0), (2 * pi / 3, -r3), (5 * pi / 3, -r3)], odots=[(2 * pi, 0)],
             labs=[((1.4 * pi, 2.4), 'y=\\tan x', 'lc', 30, 0)], m=(60, 16, 100, 16))


def i25():  # 19⑷ sin t = 1/2 (0≤t<4π)
    xs = [pi / 6, 5 * pi / 6, 13 * pi / 6, 17 * pi / 6]
    return G((-0.25 * pi, 4.3 * pi), (-1.5, 1.6), 30, 70, [(s, 0, 4 * pi, 'S')], H=[(1, 0, 2.5 * pi), (-1, 0, 3.5 * pi)], V=[(x, 0, 0.5) for x in xs],
             K=[(0.5, 'y=\\dfrac{1}{2}')], xt=[(pi / 6, '\\dfrac{\\pi}{6}', 'b'), (5 * pi / 6, fr(5, 6), 'b'), (pi, '\\pi', 'tr'), (2 * pi, '2\\pi', 'tl'), (13 * pi / 6, fr(13, 6), 'b'), (17 * pi / 6, fr(17, 6), 'b'), (3 * pi, '3\\pi', 'tr'), (4 * pi, '4\\pi', 'b')],
             yt=[(1, '1'), (-1, '-1'), (0.5, '\\dfrac{1}{2}')], dots=[(x, 0.5) for x in xs], odots=[(4 * pi, 0)], xname='t',
             labs=[((3.5 * pi, -1), 'y=\\sin t', 'ct', 0, 8)], m=(60, 16, 100, 30))


def i26():  # 19⑸ cos x = 1/2
    xs = [pi / 3, 5 * pi / 3]
    return G((-0.25 * pi, 2.3 * pi), (-1.5, 1.6), 50, 70, [(c, 0, 2 * pi, 'S')], H=[(1, 0, 2 * pi), (-1, 0, pi)], V=[(x, 0, 0.5) for x in xs] + [(pi, 0, -1)],
             K=[(0.5, 'y=\\dfrac{1}{2}')], xt=[(pi / 3, '\\dfrac{\\pi}{3}', 'b'), (pi / 2, '\\dfrac{\\pi}{2}', 'b'), (pi, '\\pi', 't'), (1.5 * pi, fr(3, 2), 'b'), (5 * pi / 3, fr(5, 3), 'b'), (2 * pi, '2\\pi', 'br')],
             yt=[(1, '1'), (-1, '-1'), (0.5, '\\dfrac{1}{2}')], dots=[(0, 1)] + [(x, 0.5) for x in xs], odots=[(2 * pi, 1)],
             labs=[((pi, -1), 'y=\\cos x', 'ct', 0, 8)], m=(60, 16, 100, 30))


def i27():  # 20⑴ sin x = -1/2
    xs = [7 * pi / 6, 11 * pi / 6]
    return G((-0.25 * pi, 2.3 * pi), (-1.5, 1.6), 50, 70, [(s, 0, 2 * pi, 'S')], H=[(1, 0, pi / 2), (-1, 0, 1.5 * pi)], V=[(x, 0, -0.5) for x in xs] + [(pi / 2, 0, 1), (1.5 * pi, 0, -1)],
             K=[(-0.5, 'y=-\\dfrac{1}{2}')], xt=[(pi / 2, '\\dfrac{\\pi}{2}', 'b'), (pi, '\\pi', 'bl'), (7 * pi / 6, fr(7, 6), 't'), (1.5 * pi, fr(3, 2), 't'), (11 * pi / 6, fr(11, 6), 't'), (2 * pi, '2\\pi', 'br')],
             yt=[(1, '1'), (-1, '-1'), (-0.5, '-\\dfrac{1}{2}')], dots=[(0, 0)] + [(x, -0.5) for x in xs], odots=[(2 * pi, 0)],
             labs=[((pi / 2, 1), 'y=\\sin x', 'cb', 0, -6)], m=(60, 30, 120, 16))


def i28():  # 20⑵ cos x = 1/2
    return i26()


def i29():  # 20⑶ tan x = 1/√3
    return G((-0.25 * pi, 2.3 * pi), (-2.6, 2.6), 50, 50, [(t, 0, 2 * pi, 'S')], asym=[pi / 2, 1.5 * pi], V=[(pi / 6, 0, 1 / r3), (7 * pi / 6, 0, 1 / r3)],
             K=[(1 / r3, 'y=\\dfrac{1}{\\sqrt{3}}')], xt=[(pi / 6, '\\dfrac{\\pi}{6}', 'b'), (pi / 2, '\\dfrac{\\pi}{2}', 'br'), (pi, '\\pi', 'tl'), (7 * pi / 6, fr(7, 6), 'b'), (1.5 * pi, fr(3, 2), 'br'), (2 * pi, '2\\pi', 'br')],
             yt=[(1 / r3, '\\dfrac{1}{\\sqrt{3}}')], dots=[(0, 0), (pi / 6, 1 / r3), (7 * pi / 6, 1 / r3)], odots=[(2 * pi, 0)],
             labs=[((1.8 * pi, -2.2), 'y=\\tan x', 'lc', 10, 0)], m=(60, 16, 120, 16))


def i30():  # 21⑴ sin x = 0
    return G((-0.25 * pi, 2.3 * pi), (-1.5, 1.6), 50, 70, [(s, 0, 2 * pi, 'S')], H=[(1, 0, pi / 2), (-1, 0, 1.5 * pi)], V=[(pi / 2, 0, 1), (1.5 * pi, 0, -1)],
             xt=[(pi / 2, '\\dfrac{\\pi}{2}', 'b'), (pi, '\\pi', 'b'), (1.5 * pi, fr(3, 2), 't'), (2 * pi, '2\\pi', 'br')], yt=[(1, '1'), (-1, '-1')],
             dots=[(0, 0), (pi, 0)], odots=[(2 * pi, 0)], labs=[((pi / 2, 1), 'y=\\sin x', 'cb', 0, -6)], m=(40, 30, 30, 16))


def i31():  # 21⑵ cos x = -1/2, -1
    return G((-0.25 * pi, 2.3 * pi), (-1.5, 1.6), 50, 70, [(c, 0, 2 * pi, 'S')], H=[(1, 0, 2 * pi)], V=[(2 * pi / 3, 0, -0.5), (4 * pi / 3, 0, -0.5), (pi, 0, -1)],
             K=[(-0.5, 'y=-\\dfrac{1}{2}'), (-1, 'y=-1')], xt=[(pi / 2, '\\dfrac{\\pi}{2}', 'b'), (2 * pi / 3, fr(2, 3), 't'), (pi, '\\pi', 't'), (4 * pi / 3, fr(4, 3), 't'), (1.5 * pi, fr(3, 2), 'b'), (2 * pi, '2\\pi', 'br')],
             yt=[(1, '1'), (-1, '-1'), (-0.5, '-\\dfrac{1}{2}')], dots=[(0, 1), (2 * pi / 3, -0.5), (4 * pi / 3, -0.5), (pi, -1)], odots=[(2 * pi, 1)],
             labs=[((2 * pi, 1), 'y=\\cos x', 'lb', 6, -4)], m=(60, 30, 120, 16))


def i32():  # 22 tan t = √3, 0≤t<π
    return G((-0.2 * pi, 1.25 * pi), (-2.6, 2.6), 90, 50, [(t, 0, pi, 'S')], asym=[pi / 2], V=[(pi / 3, 0, r3)], K=[(r3, 'y=\\sqrt{3}')],
             xt=[(pi / 3, '\\dfrac{\\pi}{3}', 'b'), (pi / 2, '\\dfrac{\\pi}{2}', 'tr'), (pi, '\\pi', 'b')], yt=[(r3, '\\sqrt{3}')],
             dots=[(0, 0), (pi / 3, r3)], odots=[(pi, 0)], xname='t', labs=[((0.62 * pi, -2.2), 'y=\\tan t', 'lc', 6, 0)], m=(60, 16, 100, 16))


def i33():  # 23 cos t = -√3/2, -π/4≤t<7π/4
    return G((-0.5 * pi, 2.0 * pi), (-1.5, 1.9), 56, 95, [(c, -pi / 4, 7 * pi / 4, 'S')], H=[(1, 0, 0)], V=[(-pi / 4, 0, c(-pi / 4)), (5 * pi / 6, 0, -r3 / 2), (7 * pi / 6, 0, -r3 / 2), (7 * pi / 4, 0, c(7 * pi / 4))],
             K=[(-r3 / 2, 'y=-\\dfrac{\\sqrt{3}}{2}')], xt=[(-pi / 4, '-\\dfrac{\\pi}{4}', 'b'), (5 * pi / 6, fr(5, 6), 't'), (7 * pi / 6, fr(7, 6), 't'), (7 * pi / 4, fr(7, 4), 'b')],
             yt=[(1, '1')], dots=[(-pi / 4, c(-pi / 4)), (5 * pi / 6, -r3 / 2), (7 * pi / 6, -r3 / 2)], odots=[(7 * pi / 4, c(7 * pi / 4))],
             xname='t', labs=[((pi, -1), 'y=\\cos t', 'ct', 0, 8)], m=(60, 16, 130, 30))


def i34():  # 24 sin x = 1
    return G((-0.25 * pi, 2.3 * pi), (-1.5, 1.6), 50, 70, [(s, 0, 2 * pi, 'S')], H=[(-1, 0, 1.5 * pi)], V=[(pi / 2, 0, 1), (1.5 * pi, 0, -1)], K=[(1, 'y=1')],
             xt=[(pi / 2, '\\dfrac{\\pi}{2}', 'b'), (pi, '\\pi', 'b'), (1.5 * pi, fr(3, 2), 't'), (2 * pi, '2\\pi', 'br')], yt=[(1, '1'), (-1, '-1')],
             dots=[(0, 0), (pi / 2, 1)], odots=[(2 * pi, 0)], labs=[((1.5 * pi, -1), 'y=\\sin x', 'ct', 0, 8)], m=(40, 16, 80, 30))


def ineq(f, k, klab, xs, solid, gray, ytk, curve_lab, m=(60, 16, 130, 30), extra=(), xname='x', xr=(-0.25 * pi, 2.3 * pi), yr=(-1.5, 1.6), odots=(), dots=None, sy=70):
    curves = [(f, a, b, 'G') for a, b in gray] + [(f, a, b, 'S') for a, b in solid]
    return G(xr, yr, 50, sy, curves, H=[(1, 0, 2 * pi), (-1, 0, 2 * pi)], V=[(x, 0, k) for x, _ in xs], K=[(k, klab)],
             xt=[(x, lab, 'b' if k >= 0 else 't') for x, lab in xs] + list(extra), yt=ytk, dots=(dots if dots is not None else []),
             odots=[(x, k) for x, _ in xs] + list(odots), labs=[curve_lab], xname=xname, m=m)


def i35():  # 25⑴ sin x > 1/2
    return ineq(s, 0.5, 'y=\\dfrac{1}{2}', [(pi / 6, '\\dfrac{\\pi}{6}'), (5 * pi / 6, fr(5, 6))], [(pi / 6, 5 * pi / 6)], [(0, pi / 6), (5 * pi / 6, 2 * pi)],
                [(1, '1'), (-1, '-1'), (0.5, '\\dfrac{1}{2}')], ((1.5 * pi, -1), 'y=\\sin x', 'ct', 0, 8), extra=[(pi, '\\pi', 'tr'), (2 * pi, '2\\pi', 'br')], odots=[(2 * pi, 0)])


def i36():  # 25⑵ cos x > 1/2
    return ineq(c, 0.5, 'y=\\dfrac{1}{2}', [(pi / 3, '\\dfrac{\\pi}{3}'), (5 * pi / 3, fr(5, 3))], [(0, pi / 3), (5 * pi / 3, 2 * pi)], [(pi / 3, 5 * pi / 3)],
                [(1, '1'), (-1, '-1'), (0.5, '\\dfrac{1}{2}')], ((pi, -1), 'y=\\cos x', 'ct', 0, 8), extra=[(pi, '\\pi', 'tr'), (2 * pi, '2\\pi', 'br')], dots=[(0, 1)], odots=[(2 * pi, 1)])


def i37():  # 26⑴ cos x ≥ 1/√2 (0≤x≤2π)
    return G((-0.25 * pi, 2.3 * pi), (-1.5, 1.6), 50, 70, [(c, pi / 4, 7 * pi / 4, 'G'), (c, 0, pi / 4, 'S'), (c, 7 * pi / 4, 2 * pi, 'S')], H=[(1, 0, 2 * pi), (-1, 0, pi)],
             V=[(pi / 4, 0, 1 / r2), (7 * pi / 4, 0, 1 / r2), (2 * pi, 0, 1), (pi, 0, -1)], K=[(1 / r2, 'y=\\dfrac{1}{\\sqrt{2}}')],
             xt=[(pi / 4, '\\dfrac{\\pi}{4}', 'b'), (pi, '\\pi', 't'), (7 * pi / 4, fr(7, 4), 'b'), (2 * pi, '2\\pi', 'br')], yt=[(1, '1'), (-1, '-1'), (1 / r2, '\\dfrac{1}{\\sqrt{2}}')],
             dots=[(0, 1), (pi / 4, 1 / r2), (7 * pi / 4, 1 / r2), (2 * pi, 1)], labs=[((pi, -1), 'y=\\cos x', 'ct', 0, 8)], m=(60, 16, 120, 30))


def i38():  # 26⑵ tan x < -1
    return G((-0.25 * pi, 2.3 * pi), (-2.6, 2.6), 50, 50, [(t, 0, 2 * pi, 'G'), (t, pi / 2 + 0.001, 3 * pi / 4, 'S'), (t, 1.5 * pi + 0.001, 7 * pi / 4, 'S')], asym=[pi / 2, 1.5 * pi],
             V=[(3 * pi / 4, 0, -1), (7 * pi / 4, 0, -1)], K=[(-1, 'y=-1')], xt=[(pi / 2, '\\dfrac{\\pi}{2}', 'br'), (3 * pi / 4, fr(3, 4), 't'), (pi, '\\pi', 'br'), (1.5 * pi, fr(3, 2), 'br'), (7 * pi / 4, fr(7, 4), 't'), (2 * pi, '2\\pi', 'br')],
             yt=[(-1, '-1')], odots=[(3 * pi / 4, -1), (7 * pi / 4, -1), (2 * pi, 0)], labs=[((0.35 * pi, 2.4), 'y=\\tan x', 'lc', 6, 0)], m=(60, 16, 100, 16))


def i39():  # 27 sin x ≥ √3/2
    return G((-0.25 * pi, 2.3 * pi), (-1.5, 1.6), 50, 70, [(s, 0, pi / 3, 'G'), (s, 2 * pi / 3, 2 * pi, 'G'), (s, pi / 3, 2 * pi / 3, 'S')], H=[(1, 0, pi / 2), (-1, 0, 1.5 * pi)],
             V=[(pi / 3, 0, r3 / 2), (pi / 2, 0, 1), (2 * pi / 3, 0, r3 / 2), (1.5 * pi, 0, -1)], K=[(r3 / 2, 'y=\\dfrac{\\sqrt{3}}{2}')],
             xt=[(pi / 3, '\\dfrac{\\pi}{3}', 'b'), (pi / 2, '\\dfrac{\\pi}{2}', 'b'), (2 * pi / 3, fr(2, 3), 'b'), (pi, '\\pi', 'tr'), (1.5 * pi, fr(3, 2), 't'), (2 * pi, '2\\pi', 'br')],
             yt=[(1, '1'), (-1, '-1'), (r3 / 2, '\\dfrac{\\sqrt{3}}{2}')], dots=[(pi / 3, r3 / 2), (2 * pi / 3, r3 / 2)], odots=[(2 * pi, 0)],
             labs=[((1.5 * pi, -1), 'y=\\sin x', 'ct', 0, 8)], m=(60, 16, 120, 30))


def i40():  # 28 cos t ≤ -1/2, -π/6≤t≤11π/6
    return G((-0.4 * pi, 2.1 * pi), (-1.5, 1.9), 50, 95, [(c, -pi / 6, 2 * pi / 3, 'G'), (c, 4 * pi / 3, 11 * pi / 6, 'G'), (c, 2 * pi / 3, 4 * pi / 3, 'S')], H=[(1, 0, 0)],
             V=[(-pi / 6, 0, r3 / 2), (2 * pi / 3, 0, -0.5), (pi, 0, -1), (4 * pi / 3, 0, -0.5), (11 * pi / 6, 0, r3 / 2)], K=[(-0.5, 'y=-\\dfrac{1}{2}')],
             xt=[(-pi / 6, '-\\dfrac{\\pi}{6}', 'b'), (pi / 2, '\\dfrac{\\pi}{2}', 'b'), (2 * pi / 3, fr(2, 3), 't'), (pi, '\\pi', 't'), (4 * pi / 3, fr(4, 3), 't'), (11 * pi / 6, fr(11, 6), 'b')],
             yt=[(1, '1'), (-1, '-1', 'r')], dots=[(2 * pi / 3, -0.5), (4 * pi / 3, -0.5), (-pi / 6, r3 / 2), (11 * pi / 6, r3 / 2)],
             xname='t', labs=[((pi, -1), 'y=\\cos t', 'ct', 0, 8)], m=(60, 30, 130, 30))


def i41():  # 29 tan t < 1, π/3≤t≤7π/3
    return G((-0.1 * pi, 2.75 * pi), (-2.6, 2.6), 50, 50, [(t, pi / 3, 7 * pi / 3, 'G'), (t, pi / 2 + 0.001, 5 * pi / 4, 'S'), (t, 1.5 * pi + 0.001, 9 * pi / 4, 'S')], asym=[pi / 2, 1.5 * pi],
             V=[(pi / 3, 0, r3), (5 * pi / 4, 0, 1), (9 * pi / 4, 0, 1), (7 * pi / 3, 0, r3)], K=[(1, 'y=1')],
             xt=[(pi / 3, '\\dfrac{\\pi}{3}', 'b'), (pi / 2, '\\dfrac{\\pi}{2}', 'br'), (5 * pi / 4, fr(5, 4), 'b'), (1.5 * pi, fr(3, 2), 'br'), (9 * pi / 4, fr(9, 4), 'bl'), (7 * pi / 3, fr(7, 3), 'br')],
             yt=[(1, '1'), (r3, '\\sqrt{3}')], H=[(r3, 0, 7 * pi / 3)], odots=[(5 * pi / 4, 1), (9 * pi / 4, 1)], dots=[(pi / 3, r3), (7 * pi / 3, r3)],
             xname='t', labs=[((1.6 * pi, -2.3), 'y=\\tan t', 'lc', 8, 0)], m=(60, 16, 80, 30))


def par(f, a, b, xr, yr, sx, sy, dots=(), odots=(), H=(), V=(), K=(), xt=(), yt=(), labs=(), asym=(), m=(60, 16, 140, 16), Oanc=('rt', -6, 4)):
    return G(xr, yr, sx, sy, [(f, xr[0], a, 'D'), (f, a, b, 'S'), (f, b, xr[1], 'D')], H=H, V=V, K=K, xt=xt, yt=yt, dots=dots, odots=odots, labs=labs, xname='t', asym=asym, m=m, Oanc=Oanc)


def i42():  # 30 y=-(t-1)^2+1, -1≤t≤1
    f = lambda u: -(u - 1) ** 2 + 1
    return par(f, -1, 1, (-1.6, 2.8), (-3.8, 1.8), 70, 50, dots=[(-1, -3), (1, 1)], H=[(1, 0, 1), (-3, -1, 0)], V=[(-1, 0, -3), (1, 0, 1)],
               xt=[(-1, '-1', 't'), (1, '1', 'b')], yt=[(1, '1'), (-3, '-3', 'r')], labs=[((1.6, f(1.6)), 'y=-(t-1)^{2}+1', 'lc', 10, 0)])


def i43():  # 31 y=2t^2+2t-1, -1≤t≤1
    f = lambda u: 2 * u * u + 2 * u - 1
    return par(f, -1, 1, (-1.8, 1.6), (-2.0, 4.6), 80, 40, dots=[(-1, -1), (-0.5, -1.5), (1, 3)], H=[(3, 0, 1), (-1.5, -0.5, 0)], V=[(1, 0, 3), (-0.5, 0, -1.5)],
               xt=[(-0.5, '-\\dfrac{1}{2}', 't'), (1, '1', 'b')], yt=[(3, '3'), (-1.5, '-\\dfrac{3}{2}', 'r')], labs=[((-1, -1), '-1', 'rc', -8, 0), ((1.1, 4.0), 'y=2t^{2}+2t-1', 'lc', 8, 0)])


def i44():  # 32 y=-t^2-4t+k+1 (k=-1 개형)
    f = lambda u: -u * u - 4 * u
    return par(f, -1, 1, (-4.6, 1.8), (-6.2, 5.0), 50, 30, dots=[(-1, 3), (1, -5)], H=[(3, -1, 0), (4, -2, 0)], V=[(-1, 0, 3), (-2, 0, 4), (1, 0, -5)],
               xt=[(-2, '-2', 'b'), (-1, '-1', 'b'), (1, '1', 't')], yt=[(3, 'k+4', 'r')], labs=[((-4.4, f(-4.4)), 'y=-t^{2}-4t+k+1', 'lc', 10, 0)], m=(60, 16, 60, 16))


def i45():  # 33 y=(-t+1)/(t+2)
    f = lambda u: (-u + 1) / (u + 2) if abs(u + 2) > 1e-6 else None
    return G((-4.2, 2.6), (-3.4, 3.4), 56, 50, [(f, -4.2, -1, 'D'), (f, -1, 1, 'S'), (f, 1, 2.6, 'D')], asym=[-2], K=[], H=[(-1, -4.2, 2.6), (2, -1, 0)], V=[(-1, 0, 2)],
             xt=[(-2, '-2', 'bl'), (-1, '-1', 'b'), (1, '1', 'b')], yt=[(2, '2', 'r'), (-1, '-1', 'r')], dots=[(-1, 2), (1, 0)], xname='t',
             labs=[((-4.1, 2.6), 'y=\\dfrac{-t+1}{t+2}', 'lc', 0, 0)], m=(40, 16, 30, 16))


def i46():  # 34 y=-t/(t-1), 1/2≤t≤√2/2
    f = lambda u: -u / (u - 1) if abs(u - 1) > 1e-6 else None
    return G((-1.2, 2.6), (-3.2, 3.8), 70, 44, [(f, -1.2, 0.5, 'D'), (f, 0.5, r2 / 2, 'S'), (f, r2 / 2, 2.6, 'D')], asym=[1], H=[(-1, -1.2, 2.6), (1, 0, 0.5), (1 + r2, 0, r2 / 2)],
             V=[(0.5, 0, 1), (r2 / 2, 0, 1 + r2)], xt=[(0.5, '\\dfrac{1}{2}', 'b'), (r2 / 2, '\\dfrac{\\sqrt{2}}{2}', 'br'), (1, '1', 'tr')], yt=[(1, '1'), (1 + r2, '1+\\sqrt{2}'), (-1, '-1')],
             dots=[(0.5, 1), (r2 / 2, 1 + r2)], xname='t', labs=[((1.3, 3.0), 'y=\\dfrac{-t}{t-1}', 'lc', 6, 0)], m=(90, 16, 30, 16))


def i47():  # 35 y=(2t+1)/(t+2), 0≤t≤1
    f = lambda u: (2 * u + 1) / (u + 2) if abs(u + 2) > 1e-6 else None
    return G((-4.2, 2.8), (-2.2, 4.2), 50, 44, [(f, -4.2, 0, 'D'), (f, 0, 1, 'S'), (f, 1, 2.8, 'D')], asym=[-2], H=[(2, -4.2, 2.8), (1, 0, 1)], V=[(1, 0, 1)],
             xt=[(-2, '-2', 'bl'), (1, '1', 'b')], yt=[(2, '2', 'r'), (1, '1', 'r'), (0.5, '\\dfrac{1}{2}', 'l')], dots=[(0, 0.5), (1, 1)], xname='t',
             labs=[((1.4, 3.3), 'y=\\dfrac{2t+1}{t+2}', 'lc', 6, 0)], m=(40, 16, 30, 16))


def cosk(sol):
    f = lambda x: c(x / 2); k = 0.6; ak = math.acos(k) * 2; bk = 2 * pi - math.acos(k) * 2 + 0  # a, b, c, d
    a = ak; b = 2 * pi - math.acos(-k) * 2 + 0
    b = 2 * math.acos(-k); cc = 4 * pi - 2 * math.acos(-k); d = 4 * pi - ak
    xs = [(a, 'a'), (b, 'b'), (cc, 'c'), (d, 'd')]
    xt = [(a, 'a', 'b'), (b, 'b', 'tl'), (cc, 'c', 'tr'), (d, 'd', 'b')]
    if sol:
        xt += [(pi, '\\pi', 'br'), (2 * pi, '2\\pi', 'b'), (3 * pi, '3\\pi', 'bl'), (4 * pi, '4\\pi', 'b')]
    return G((-0.3 * pi, 4.6 * pi), (-1.5, 1.6), 30, 70, [(f, -0.3 * pi, 4.4 * pi, 'S')], H=[(1, 0, 4 * pi), (-1, 0, 2 * pi)], V=[(a, 0, k), (b, 0, -k), (cc, 0, -k), (d, 0, k)],
             K=[(k, 'y=k'), (-k, 'y=-k')], xt=xt, yt=[(1, '1'), (-1, '-1')], labs=[((4.2 * pi, f(4.2 * pi)), 'y=\\cos\\dfrac{1}{2}x', 'cb', 0, -6)], m=(40, 30, 80, 16))


def i48(): return cosk(True)
def i49(): return cosk(False)


def i50():  # 37 y=sin x, y=k, 0≤x≤3π
    k = 0.7; a = math.asin(k); b = pi - a; cc = 2 * pi + a; d = 3 * pi - a
    return G((-0.25 * pi, 3.3 * pi), (-1.5, 1.6), 40, 70, [(s, 0, 3 * pi, 'S')], H=[(1, 0, 2.5 * pi), (-1, 0, 1.5 * pi)], V=[(a, 0, k), (b, 0, k), (cc, 0, k), (d, 0, k)],
             K=[(k, 'y=k')], xt=[(a, 'a', 'b'), (b, 'b', 'b'), (cc, 'c', 'b'), (d, 'd', 'b'), (3 * pi, '3\\pi', 'br')], yt=[(1, '1'), (-1, '-1'), (k, 'k')],
             labs=[((pi / 2, 1), 'y=\\sin x', 'cb', 0, -6)], m=(40, 30, 80, 16))


def i51():  # 38 sin πx, x/3
    return G((-3.6, 3.7), (-1.6, 1.7), 60, 70, [(lambda x: s(pi * x), -3.5, 3.5, 'S'), (lambda x: x / 3, -3.6, 3.6, 'S')], H=[(1, -3.5, 3.5), (-1, -3.5, 3.5)],
             xt=[(-3, '-3', 'b'), (-2, '-2', 'b'), (-1, '-1', 'b'), (1, '1', 'b'), (2, '2', 'b'), (3, '3', 'b')], yt=[(1, '1', 'r'), (-1, '-1', 'r')],
             labs=[((3.0, 1.0), 'y=\\dfrac{1}{3}x', 'cb', 10, -6), ((1.5, -1), 'y=\\sin\\pi x', 'ct', 0, 8)], m=(40, 30, 30, 16))


def i52():  # 39 y=-t^2+2t, y=k, -1≤t≤1
    f = lambda u: -u * u + 2 * u
    return par(f, -1, 1, (-1.8, 2.8), (-3.8, 1.8), 70, 50, dots=[(-1, -3), (1, 1)], H=[(1, 0, 1), (-3, -1, 0)], V=[(-1, 0, -3), (1, 0, 1)], K=[(-1.6, 'y=k')],
               xt=[(-1, '-1', 't'), (1, '1', 'b')], yt=[(1, '1'), (-3, '-3', 'r')], labs=[((1.0, 1.0), 'y=-t^{2}+2t', 'lb', 8, -6)])


def i53():  # 40 y=t^2-t-1, y=a
    f = lambda u: u * u - u - 1
    return par(f, -1, 1, (-1.8, 2.4), (-1.9, 2.6), 80, 60, dots=[(-1, 1), (1, -1)], H=[(1, -1, 0), (-1.25, 0, 0.5), (-1, 0, 1)], V=[(-1, 0, 1), (0.5, 0, -1.25), (1, 0, -1)], K=[(0.45, 'y=a')],
               xt=[(-1, '-1', 'b'), (0.5, '\\dfrac{1}{2}', 't'), (1, '1', 't')], yt=[(1, '1', 'r'), (-1.25, '-\\dfrac{5}{4}'), (-1, '-1', 'r')], labs=[((-1.75, 2.2), 'y=t^{2}-t-1', 'lc', 0, 0)])


def i54():  # 41 y=-t^2-4t, 0≤t<1
    f = lambda u: -u * u - 4 * u
    return G((-4.6, 1.8), (-6.2, 5.0), 50, 30, [(f, -4.6, 0, 'D'), (f, 0, 1, 'S'), (f, 1, 1.4, 'D')], H=[(4, -2, 0), (-5, 0, 1)], V=[(-2, 0, 4), (1, 0, -5)], K=[(-2.6, 'y=k')],
             xt=[(-2, '-2', 'b'), (1, '1', 'tr')], yt=[(4, '4', 'r'), (-5, '-5')], dots=[(0, 0)], odots=[(1, -5)], xname='t',
             labs=[((-4.3, f(-4.3)), 'y=-t^{2}-4t', 'lc', 10, 0)], m=(40, 16, 80, 16))


def i55():  # 43 y=2sin(x/2)+1
    f = lambda x: 2 * s(x / 2) + 1
    return G((-1.6 * pi, 4.9 * pi), (-1.6, 3.6), 30, 50, [(f, -1.6 * pi, 4.85 * pi, 'S')], H=[(3, 0, 4.8 * pi), (1, -1.6 * pi, 4.8 * pi), (-1, -pi, 3 * pi)], V=[(-pi, 0, -1), (pi, 0, 3), (3 * pi, 0, -1)],
             xt=[(-pi, '-\\pi', 't'), (pi, '\\pi', 'b'), (2 * pi, '2\\pi', 'b'), (3 * pi, '3\\pi', 't'), (4 * pi, '4\\pi', 'b')], yt=[(3, '3'), (1, '1'), (-1, '-1')],
             labs=[((pi, 3), 'y=a\\sin bx+c', 'lb', 4, -6)], m=(40, 30, 30, 16))


def rectsin(sol):
    f = lambda x: 8 * s(pi * x / 12)
    F = Frame((-2.5, 14.5), (-3.5, 10.5), 26, 24, (40, 46, 100, 16))
    F.axes(); O(F, 'rb', -6, -4)
    F.poly([(2, 0), (10, 0), (10, 4), (2, 4)], SKY)
    pc(F, f, -2.5, 14.5, -3.5, 10)
    F.polyline([(2, 0), (2, 4), (10, 4), (10, 0)])
    F.pt((2, 4), 'A', 'rb', -4, -4); F.pt((2, 0), 'B', 'lt', 4, 6); F.pt((10, 0), 'C', 'ct', 0, 8); F.pt((10, 4), 'D', 'lb', 4, -4)
    F.lab((12, 0), '12', 'lb', 5, -6)
    if sol:
        hline(F, 8, 0, 6); vline(F, 6, 0, 10.2); F.lab((6, 10.2), 'x=6', 'cb', 0, -2); F.lab((0, 8), '8', 'rc', -8, 0)
        F.lab((2, 0), '2', 'rt', -5, 6)
    F.lab((9.5, f(9.5) + 1.3), 'y=8\\sin\\dfrac{\\pi}{12}x', 'lb', 6, -6)
    dim_ = __import__('mathfig').dim_arc; dim_(F, (2, 0), (10, 0), '8', 1)
    return F.render()


def i56(): return rectsin(True)
def i57(): return rectsin(False)


def i58():  # 45 y=-t^2-t+1, -1≤t≤1
    f = lambda u: -u * u - u + 1
    return par(f, -1, 1, (-2.6, 1.8), (-2.2, 1.9), 110, 100, dots=[(-1, 1), (1, -1)], H=[(1.25, -0.5, 0), (1, -1, 0), (-1, 0, 1)], V=[(-1, 0, 1), (-0.5, 0, 1.25), (1, 0, -1)],
               xt=[(-1, '-1', 'b'), (-0.5, '-\\dfrac{1}{2}', 'b'), (1, '1', 'tr')], yt=[(1.25, '\\dfrac{5}{4}', 'r'), (1, '1', 'r'), (-1, '-1')], labs=[((0.3, 1.5), 'y=-t^{2}-t+1', 'lc', 10, 0)], m=(60, 16, 30, 16), Oanc=('lt', 4, 4))


def i59():  # 48 |cos2x|, 2x/π
    f = lambda x: abs(c(2 * x))
    return G((-1.15 * pi, 2.35 * pi), (-0.8, 1.6), 50, 90, [(f, -pi, 2.25 * pi, 'S'), (lambda x: 2 * x / pi, -0.5, 1.95, 'S')], H=[(1, -pi, 2 * pi)],
             V=[(x * pi / 2, 0, 1) for x in range(-2, 5)], xt=[(-pi, '-\\pi', 'b'), (pi / 2, '\\dfrac{\\pi}{2}', 'b'), (pi, '\\pi', 'b'), (2 * pi, '2\\pi', 'b')], yt=[(1, '1', 'r')],
             dots=[(pi / 2, 1)], labs=[((1.95, 2 * 1.95 / pi), 'y=\\dfrac{2}{\\pi}x', 'rb', -8, -6), ((2.25 * pi, 1), 'y=|\\cos 2x|', 'lc', 6, 0)], m=(40, 16, 80, 16))


def i60():  # 49 -1/2≤sin t≤1, -π/3≤t<5π/3
    lo = -0.5
    F = Frame((-0.55 * pi, 2.0 * pi), (-1.6, 1.6), 54, 70, (90, 16, 130, 30))
    xs = [(-pi / 6, '-\\dfrac{\\pi}{6}'), (7 * pi / 6, fr(7, 6))]
    return G((-0.6 * pi, 2.0 * pi), (-1.6, 1.6), 110, 120, [(s, -pi / 3, -pi / 6, 'S'), (s, -pi / 6, 7 * pi / 6, 'S'), (s, 7 * pi / 6, 5 * pi / 3, 'S')],
             H=[(-1, 0, 0)], V=[(-pi / 3, 0, s(-pi / 3)), (-pi / 6, 0, lo), (7 * pi / 6, 0, lo), (5 * pi / 3, 0, s(5 * pi / 3))], K=[(1, 'y=1'), (lo, 'y=-\\dfrac{1}{2}')],
             xt=[(-pi / 3, '-\\dfrac{\\pi}{3}', 'b'), (-pi / 6, '-\\dfrac{\\pi}{6}', 't'), (pi, '\\pi', 'b'), (7 * pi / 6, fr(7, 6), 't'), (5 * pi / 3, fr(5, 3), 't')],
             yt=[(-1, '-1', 'r')], dots=[(-pi / 3, s(-pi / 3)), (-pi / 6, lo), (7 * pi / 6, lo)], odots=[(5 * pi / 3, s(5 * pi / 3))], xname='t',
             labs=[((pi / 2, 1), 'y=\\sin t', 'cb', 0, -8)], m=(90, 30, 130, 30), fill=(s, -pi / 6, 7 * pi / 6, lo))


JOBS = {k: v for k, v in globals().items() if k[0] == 'i' and k[1:].isdigit()}
if __name__ == '__main__':
    run(JOBS, OUT, sys.argv[2:])
