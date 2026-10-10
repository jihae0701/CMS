# -*- coding: utf-8 -*-
"""유형서 5단원 그림 (SVG + KaTeX를 Chromium으로 PNG로 찍는다)
python 그림/draw5.py   (KATEX_DIR 필요)
- u5_n1090.png: f(x)=(x+2)(x-4), g(x)=-(x-1)(x-4)의 그래프
- u5_n1162.png: f(x)=3(x+4)(x-5), g(x)=-2(x-2)(x-5)의 그래프 (세로는 줄여 그린 개형)
- u5_n3040.png: 포물선 모양 조형물, 조명, 그림자의 끝
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from draw import page, shoot, HERE, STROKE

AX = 2.0      # 좌표축 굵기


def curve(f, x0, x1, P, n=200, extra=""):
    pts = []
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        pts.append("%.1f,%.1f" % P(x, f(x)))
    return '<polyline points="%s" fill="none" stroke="#000" stroke-width="%s" stroke-linejoin="round" %s/>' % (
        " ".join(pts), STROKE, extra)


def axes(P, xr, yr):
    (x0, y0), (x1, _) = P(xr[0], 0), P(xr[1], 0)
    (ox, yb), (_, yt) = P(0, yr[0]), P(0, yr[1])
    arrow = '<marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">' \
            '<path d="M0,0 L10,5 L0,10 z" fill="#000"/></marker>'
    return ('<defs>%s</defs><line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#000" stroke-width="%s" marker-end="url(#ar)"/>'
            '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#000" stroke-width="%s" marker-end="url(#ar)"/>'
            % (arrow, x0, y0, x1, y0, AX, ox, yb, ox, yt, AX))


def two_parabolas(f, g, xr, yr, sx, sy, ticks, flab, glab):
    """f, g: 함수, xr/yr: 보이는 범위, sx/sy: 한 칸 픽셀, ticks: x절편 눈금, flab/glab: (x, y, 위치) 이름표"""
    ml = 30
    w = int((xr[1] - xr[0]) * sx + 2 * ml + 70)
    h = int((yr[1] - yr[0]) * sy + 2 * ml)

    def P(x, y):
        return (ml + (x - xr[0]) * sx, ml + (yr[1] - y) * sy)
    fx = [x / 100 for x in range(int(xr[0] * 100), int(xr[1] * 100) + 1) if yr[0] <= f(x / 100) <= yr[1]]
    gx = [x / 100 for x in range(int(xr[0] * 100), int(xr[1] * 100) + 1) if yr[0] <= g(x / 100) <= yr[1]]
    svg = axes(P, xr, yr) + curve(f, fx[0], fx[-1], P) + curve(g, gx[0], gx[-1], P)
    labels = [(P(xr[1], 0)[0] - 2, P(0, 0)[1] + 6, "x", 22, "rt"), (P(0, yr[1])[0] + 8, P(0, yr[1])[1] + 2, "y", 22, "lt"),
              (P(0, 0)[0] - 5, P(0, 0)[1] + 5, r"\mathrm{O}", 20, "rt")]
    for tx, anc, dx, dy in ticks:
        X, Y = P(tx, 0)
        labels.append((X + dx, Y + dy, str(tx) if tx >= 0 else "-%d" % -tx, 20,
                       ("r" if anc == "l" else "l") + ("t" if dy > 0 else "b")))
    for (x, y, anc), tex in ((flab, "y=f(x)"), (glab, "y=g(x)")):
        X, Y = P(x, y)
        labels.append((X, Y, tex, 20, anc))
    svg = '<svg width="%d" height="%d" style="position:absolute;left:0;top:0">%s</svg>' % (w, h, svg)
    return page(svg, labels, w, h), w, h


def fig_n1090():
    f = lambda x: (x + 2) * (x - 4)
    g = lambda x: -(x - 1) * (x - 4)
    return two_parabolas(f, g, (-3.2, 6.2), (-9.8, 7.5), 40, 18,
                         [(-2, "l", -4, 5), (1, "r", 6, 5), (4, "r", 20, 4)], (4.6, 6.9, "rb"), (5.7, -6.0, "lc"))


def fig_n1162():
    # 세로를 줄여 그린 개형 (f의 최솟값이 매우 작아 비율대로 그리면 g가 보이지 않음)
    k = 0.11
    f = lambda x: k * 3 * (x + 4) * (x - 5)
    g = lambda x: 2.2 * (-2) * (x - 2) * (x - 5) / 4.5
    return two_parabolas(f, g, (-5.2, 7.2), (-7.2, 6.5), 30, 22,
                         [(-4, "l", -4, 5), (2, "l", -6, -4), (5, "r", 20, 4)], (6.0, 5.6, "rb"), (6.5, -4.6, "lc"))


def fig_n3040():
    # 지면 y=0, A(0,0), B(2,0), 조형물 y=-4x^2+8x, 조명 (0,9), 그림자 끝 C(9/4, 0)
    s, sx = 30, 70          # 가로를 늘려 그린 개형(접하는 관계는 그대로 유지됨)
    ml, mt = 40, 26
    xr = (-0.6, 3.0)
    w, h = int((xr[1] - xr[0]) * sx + 2 * ml), int(9.6 * s + mt + 40)

    def P(x, y):
        return (ml + (x - xr[0]) * sx, mt + (9.6 - y) * s)
    ground = '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#000" stroke-width="%s"/>' % (P(xr[0], 0) + P(xr[1], 0) + (AX,))
    arch = curve(lambda x: -4 * x * x + 8 * x, 0, 2, P)
    pole = '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#000" stroke-width="%s"/>' % (P(0, 0) + P(0, 9) + (STROKE,))
    lamp = '<circle cx="%.1f" cy="%.1f" r="6" fill="#fff" stroke="#000" stroke-width="2"/>' % P(0, 9)
    ray = '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#000" stroke-width="1.6" stroke-dasharray="6,5"/>' % (P(0, 9) + P(2.25, 0))
    shadow = '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#000" stroke-width="6" stroke-opacity="0.35"/>' % (P(2, 0) + P(2.25, 0))
    # 높이 4m 표시(점선)
    hgt = '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#000" stroke-width="1.4" stroke-dasharray="4,4"/>' % (P(1, 0) + P(1, 4))
    svg = '<svg width="%d" height="%d" style="position:absolute;left:0;top:0">%s</svg>' % (
        w, h, ground + shadow + arch + hgt + ray + pole + lamp)
    labels = [(P(0, 0)[0] - 4, P(0, 0)[1] + 6, r"\mathrm{A}", 21, "rt"), (P(2, 0)[0] - 2, P(2, 0)[1] + 6, r"\mathrm{B}", 21, "ct"),
              (P(2.25, 0)[0] + 4, P(2.25, 0)[1] + 6, r"\mathrm{C}", 21, "lt"),
              (P(1, 1.6)[0] - 6, P(1, 1.6)[1], r"4\,\mathrm{m}", 18, "rc"), (P(1, 0)[0], P(1, 0)[1] + 8, r"2\,\mathrm{m}", 18, "ct"),
              (P(0, 6)[0] - 8, P(0, 6)[1], r"9\,\mathrm{m}", 18, "rc")]
    return page(svg, labels, w, h), w, h


if __name__ == "__main__":
    for name, fn in (("u5_n1090.png", fig_n1090), ("u5_n1162.png", fig_n1162), ("u5_n3040.png", fig_n3040)):
        doc, w, h = fn()
        shoot(doc, w, h, os.path.join(HERE, name))
