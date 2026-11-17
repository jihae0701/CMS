# -*- coding: utf-8 -*-
"""글자 자리 자동 고르기: 곡선·선 점들과 이미 놓인 글자에 닿지 않는 첫 후보를 고른다"""
import re

def est(tex):
    """글자 상자 크기(px) 어림"""
    h = 22
    t = tex
    if '\\left' in t: h = 62
    elif '\\dfrac' in t or '\\frac' in t:
        h = max(h, 58 if 'sqrt' in t else 50)
        def rep(m):
            a, b = m.group(1), m.group(2)
            return 'X' * max(len(re.sub(r'\\[a-z]+', 'p', a)), len(re.sub(r'\\[a-z]+', 'p', b)))
        t = re.sub(r'\\d?frac\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}', rep, t)
    t = re.sub(r'\\(sin|cos|tan)', 'sin', t)
    t = re.sub(r'\\left|\\right|\\mathrm', '', t)
    t = re.sub(r'\\[A-Za-z]+', 'p', t)
    t = re.sub(r'[{}^_ ]', '', t)
    ops = len(re.findall(r'[=<>]', t)) * 2.0 + len(re.findall(r'(?<=.)[+\-]', t)) * 1.3
    w = 13 * (len(t) + ops) + 8
    return w, h

def box(X, Y, w, h, anc):
    hx, vy = anc[0], anc[1]
    x0 = X if hx == 'l' else (X - w if hx == 'r' else X - w / 2)
    y0 = Y if vy == 't' else (Y - h if vy == 'b' else Y - h / 2)
    return (x0, y0, x0 + w, y0 + h)

class Grid:
    def __init__(self, cell=6):
        self.c = cell; self.g = {}
    def add(self, X, Y):
        self.g.setdefault((int(X // self.c), int(Y // self.c)), []).append((X, Y))
    def hit(self, b, pad=3):
        x0, y0, x1, y1 = b[0] - pad, b[1] - pad, b[2] + pad, b[3] + pad
        n = 0
        for i in range(int(x0 // self.c), int(x1 // self.c) + 1):
            for j in range(int(y0 // self.c), int(y1 // self.c) + 1):
                for X, Y in self.g.get((i, j), ()):
                    if x0 <= X <= x1 and y0 <= Y <= y1:
                        n += 1
        return n
    def seg(self, p, q, step=2.5):
        (a, b), (c, d) = p, q
        n = max(1, int(max(abs(c - a), abs(d - b)) / step))
        for k in range(n + 1):
            self.add(a + (c - a) * k / n, b + (d - b) * k / n)

def overl(b, others, pad=3):
    return any(not (b[2] + pad < o[0] or o[2] + pad < b[0] or b[3] + pad < o[1] or o[3] + pad < b[1]) for o in others)

def hitg(grid, b):
    if isinstance(grid, tuple):
        r = grid[0].hit(b, 4) + 3 * grid[1].hit(b, 7)
        if len(grid) > 2: r += 2 * grid[2].hit(b, 5)
        return r
    return grid.hit(b)


def place(F, grid, placed, cands, tex, W=None, H=None):
    """cands: [(X, Y, anc)] 화면 좌표. 처음 맞는 후보로 F.lab을 쓴다"""
    w, h = est(tex)
    W = W or F.w; H = H or F.h
    best = None
    for k, cd in enumerate(cands):
        X, Y, anc = cd[:3]; pen = cd[3] if len(cd) > 3 else 0
        b = box(X, Y, w, h, anc)
        out = b[0] < 2 or b[1] < 2 or b[2] > W - 2 or b[3] > H - 2
        bad = hitg(grid, b) + overl(b, placed) * 1000 + out * 1000 + pen
        if best is None or bad < best[0]:
            best = (bad, X, Y, anc, b)
        if bad == 0:
            break
    _, X, Y, anc, b = best
    placed.append(b)
    F.labels.append((X, Y, tex, 22, anc))
