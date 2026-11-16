# -*- coding: utf-8 -*-
"""미적분 그림 공통 도우미 (빈 점, 찬 점, 곡선, 화살표, 두 칸 축)"""
import sys, math
sys.path.insert(0, '/home/user/CMS/.claude/skills/math-figure-rules')
from mathfig import Frame, fit_shoot, dot, DASH, SKY
PINK = '#fbe0d8'
YEL = '#fbefc2'


def odot(F, p):
    X, Y = F.P(*p)
    F.svg.append('<circle cx="%.1f" cy="%.1f" r="5" fill="#fff" stroke="#000" stroke-width="2"/>' % (X, Y))


def fdot(F, p):
    dot(F, p, 4.5)


def plot(F, f, a, b, wd=3.2, dash='', n=160):
    P = ["%.1f,%.1f" % F.P(a + (b - a) * i / n, f(a + (b - a) * i / n)) for i in range(n + 1)]
    F.svg.append('<polyline points="%s" fill="none" stroke="#000" stroke-width="%s" stroke-linejoin="round" %s/>' % (" ".join(P), wd, dash))


def arr(F, p, q, wd=1.6, head=7):
    """작은 화살표(다가가는 방향 표시)"""
    (x1, y1), (x2, y2) = F.P(*p), F.P(*q)
    d = math.hypot(x2 - x1, y2 - y1); ux, uy = (x2 - x1) / d, (y2 - y1) / d
    bx, by = x2 - ux * head, y2 - uy * head
    F.svg.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#000" stroke-width="%s"/>' % (x1, y1, bx, by, wd))
    F.svg.append('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="#000"/>' % (x2, y2, bx + uy * head * 0.45, by - ux * head * 0.45, bx - uy * head * 0.45, by + ux * head * 0.45))


def along(F, f, x0, x1, off):
    """곡선 y=f(x) 옆(화면에서 off px 떨어진 곳)에 x0→x1 방향 화살표"""
    (a, b), (c, d) = F.P(x0, f(x0)), F.P(x1, f(x1))
    L = math.hypot(c - a, d - b); nx, ny = -(d - b) / L, (c - a) / L
    p = F.inv(a + nx * off, b + ny * off); q = F.inv(c + nx * off, d + ny * off)
    arr(F, p, q)


def _inv(self, X, Y):
    x0, y0 = self.P(0, 0); x1, _ = self.P(1, 0); _, y1 = self.P(0, 1)
    return ((X - x0) / (x1 - x0), (Y - y0) / (y1 - y0))


Frame.inv = _inv


def axes2(F, ox, x0, x1, y0, y1):
    """F.axes()와 같은 모양의 축을 원점 (ox, 0)에 그린다(그래프 두 개를 나란히 그릴 때). x, y 글자 자리도 axes()와 같게"""
    from mathfig import AX
    (a, y), (b, _) = F.P(x0, 0), F.P(x1, 0)
    F.svg.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#000" stroke-width="%s" marker-end="url(#ar)"/>' % (a, y, b, y, AX))
    F.labels.append((b + 0.3, y + 1.1, 'x', 22, 'rt'))
    (X, yb), (_, yt) = F.P(ox, y0), F.P(ox, y1)
    F.svg.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#000" stroke-width="%s" marker-end="url(#ar)"/>' % (X, yb, X, yt, AX))
    F.labels.append((X - 10, yt + 3.7, 'y', 22, 'rc'))


def O(F, anc='rt', dx=-6, dy=4):
    F.pt((0, 0), 'O', anc, dx, dy)



def run(JOBS, OUT, names, wide=()):
    """wide: 두 칸 그림 이름들(문서 폭 18000)"""
    import json, os
    wf = os.path.join(OUT, 'widths.json')
    W = json.load(open(wf)) if os.path.exists(wf) else {}
    import mathfig
    nf = os.path.join(OUT, 'label_nudge.json')
    N = json.load(open(nf)) if os.path.exists(nf) else {}
    for k in names or list(JOBS):
        N.pop(k + '.png', None); mathfig.NUDGE.pop(k + '.png', None)
        json.dump(N, open(nf, 'w'), ensure_ascii=False, indent=1)
        W[k] = fit_shoot('%s.png' % k, JOBS[k], 18000 if k in wide else None, out_dir=OUT)
        print(k, W[k])
    json.dump(W, open(wf, 'w'), indent=0)


def herm(pts):
    """[(x, y, 기울기), …]를 지나는 매끄러운 곡선 함수(3차 에르미트)"""
    def f(x):
        for (x0, y0, m0), (x1, y1, m1) in zip(pts, pts[1:]):
            if x0 <= x <= x1 or (x1, y1, m1) == pts[-1]:
                h = x1 - x0; t = (x - x0) / h
                return ((2 * t ** 3 - 3 * t ** 2 + 1) * y0 + (t ** 3 - 2 * t ** 2 + t) * h * m0
                        + (-2 * t ** 3 + 3 * t ** 2) * y1 + (t ** 3 - t ** 2) * h * m1)
        return pts[0][1]
    return f
