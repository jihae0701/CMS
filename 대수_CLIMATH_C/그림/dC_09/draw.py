# -*- coding: utf-8 -*-
"""대수 C 9. 수열의 합 — 스캔 그림 다시 그리기 (iN = 문서의 imageN). image2(참고 표시)는 그대로 둔다."""
import sys, math
sys.path.insert(0, '/tmp/claude-0/-home-user-CMS/7a122d51-a5b1-5def-9637-d43cb9a9b6ef/scratchpad/figw')
from geo import *
from inline import run_inline
from mathfig import Frame
from dcommon import pc, hline, vline
from mjcommon import O
OUT = sys.argv[1]
T3 = '\\left(\\frac{1}{3}\\right)'

INL = {
    'i3': '\\underline{-)\\;2S=\\qquad\\qquad 1\\cdot 4+2\\cdot 8+3\\cdot 16+\\cdots+9\\cdot 2^{10}+10\\cdot 2^{11}}',
    'i4': '\\underline{-)\\;\\frac{1}{3}S=\\qquad\\qquad 2\\cdot ' + T3 + '^{2}+4\\cdot ' + T3 + '^{3}+\\cdots+18\\cdot ' + T3 + '^{10}+20\\cdot ' + T3 + '^{11}}',
}
WID = {'i3': 23896, 'i4': 25874}


def i5():  # 49번 문제 y=√x
    F = Frame((-0.8, 5.2), (-0.6, 2.6), 64, 92, (60, 30, 40, 30))
    F.axes(); O(F, 'rt', -6, 4)
    pc(F, math.sqrt, 0, 5.0, -1, 3, n=600)
    n, m = 1.5, 3.4
    for x in (n, m):
        hline(F, math.sqrt(x), 0, x); vline(F, x, 0, math.sqrt(x))
    F.lab((n, 0), 'n', 'ct', 0, 8); F.lab((m, 0), 'n+1', 'ct', 0, 8)
    for yy, tx in ((math.sqrt(n), '\\sqrt{n}'), (math.sqrt(m), '\\sqrt{n+1}')):
        X, Y = F.P(0, yy); F.labels.append((X - 10, Y, tx, 22, 'rc', 'cut'))
    F.lab((4.3, math.sqrt(4.3)), 'y=\\sqrt{x}', 'rb', -6, -14)
    return F.render()


def i6():  # 50번 해설: 계차수열
    F = Frame((0, 10.5), (0, 3.2), 60, 60, (16, 16, 16, 16))
    X0, Y0 = F.P(0.1, 3.1); X1, Y1 = F.P(10.4, 0.1)
    F.svg.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="16" fill="none" stroke="#000" stroke-width="1.6"/>' % (X0, Y0, X1 - X0, Y1 - Y0))
    F.lab((0.6, 2.3), '\\{a_{n}\\}:', 'lc'); F.lab((0.6, 0.9), '\\{b_{n}\\}:', 'lc')
    xs = [2.8, 4.8, 6.8, 8.8]
    for x, v in zip(xs, ('4,', '12,', '24,', '40,')): F.lab((x, 2.3), v, 'cc')
    F.lab((9.8, 2.3), '\\cdots', 'cc')
    for i, v in enumerate(('8,', '12,', '16,')):
        a, b = xs[i], xs[i + 1]; m = (a + b) / 2
        F.seg((a + 0.25, 1.95), (m, 1.3), 1.5); F.seg((m, 1.3), (b - 0.25, 1.95), 1.5)
        F.lab((m, 0.9), v, 'cc')
    F.lab((9.8, 0.9), '\\cdots', 'cc')
    return F.render()


def i7():  # 50번 문제: 성냥개비
    F = Frame((0, 17.5), (-1.2, 4), 40, 40, (16, 16, 16, 16))
    ox = 0
    for n in range(1, 5):
        for k in range(n + 1):
            F.seg((ox + k, 0), (ox + k, n), 2.2); F.seg((ox, k), (ox + n, k), 2.2)
        F.lab((ox + n / 2, 0), 'a_{%d}' % n, 'ct', 0, 8)
        ox += n + 1.0
    F.lab((ox + 0.2, 0.5), '\\cdots', 'cc')
    return F.render()


def i8():  # 51번 해설: 수 배열과 묶음
    F = Frame((0, 5), (0, 6), 56, 56, (16, 16, 16, 16))
    rows = [['1', '4', '9', '16', '\\cdots'], ['2', '3', '8', '15', '\\cdots'], ['5', '6', '7', '14', '\\cdots'],
            ['10', '11', '12', '13', '\\cdots'], ['17', '18', '\\cdots', '\\cdots', '\\cdots'], ['\\vdots', '\\vdots', '', '', '']]
    for k in range(6): F.seg((k, 0), (k, 6), 2.0) if k < 6 else None
    for k in range(7): F.seg((0, k), (5, k), 2.0)
    F.seg((5, 0), (5, 6), 2.0)
    for r, row in enumerate(rows):
        for c, v in enumerate(row):
            if v: F.lab((c + 0.5, 5.5 - r), v, 'cc')
    F.svg.append('<defs><marker id="ag" viewBox="0 0 13 10" refX="12" refY="5" markerWidth="9" markerHeight="7" orient="auto"><path d="M13,5 L0.5,0.3 L2.5,5 L0.5,9.7 z" fill="#888"/></marker></defs>')
    for g in (2, 3, 4):
        y = 6 - g + 0.5; x = g - 1 + 0.5
        pts = [(0.15, y), (x, y), (x, 5.85)]
        F.svg.append('<polyline points="%s" fill="none" stroke="#888" stroke-width="3" stroke-opacity="0.8" marker-end="url(#ag)"/>' % ' '.join('%.1f,%.1f' % F.P(*p) for p in pts))
    return F.render()


def i9():  # 51번 해설: 방향 표시(작은 화살표)
    F = Frame((0, 1), (0, 1), 40, 40, (6, 6, 6, 6))
    F.svg.append('<defs><marker id="ag2" viewBox="0 0 13 10" refX="12" refY="5" markerWidth="7" markerHeight="5.5" orient="auto"><path d="M13,5 L0.5,0.3 L2.5,5 L0.5,9.7 z" fill="#000"/></marker></defs>')
    F.svg.append('<polyline points="%s" fill="none" stroke="#000" stroke-width="2.4" marker-end="url(#ag2)"/>' % ' '.join('%.1f,%.1f' % F.P(*p) for p in [(0, 0.1), (0.8, 0.1), (0.8, 1.0)]))
    return F.render()


JOBS = {k: v for k, v in globals().items() if k[0] == 'i' and k[1:].isdigit()}
if __name__ == '__main__':
    names = sys.argv[2:]
    run_crop({k: v for k, v in JOBS.items() if k != 'i9' and (not names or k in names)}, OUT, [k for k in names if k in JOBS and k != 'i9'] or None)
    if not names or 'i9' in names:
        import mathfig, json, os
        mathfig.ZOOM = 1.0
        doc, w, h = i9(); mathfig.shoot(doc, w, h, os.path.join(OUT, 'i9.png'))
        wf = os.path.join(OUT, 'widths.json'); W = json.load(open(wf)); W['i9'] = 1188; json.dump(W, open(wf, 'w'))
    if not names or 'i3' in names or 'i4' in names:
        run_inline({k: v for k, v in INL.items() if not names or k in names}, OUT, WID)
