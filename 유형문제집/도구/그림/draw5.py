# -*- coding: utf-8 -*-
"""유형서 5단원 그림 (SVG + KaTeX를 Chromium으로 PNG로 찍는다)
python 그림/draw5.py   (KATEX_DIR 필요)
- u5_n1090.png: f(x)=(x+2)(x-4), g(x)=-(x-1)(x-4)의 그래프
- u5_n1162.png: f(x)=3(x+4)(x-5), g(x)=-2(x-2)(x-5)의 그래프 (세로는 줄여 그린 개형)
- u5_n3040.png: 포물선 모양 조형물, 조명, 그림자의 끝
- u5_m3243.png, u5_m3336.png, u5_m3217.png: 모의고사 원본 그림의 모양을 따라 다시 그린 그림
  (글자가 선과 겹치지 않게 자리를 옮김, 답이 드러나지 않도록 비율은 개형으로)
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
    arrow = '<marker id="ar" viewBox="0 0 13 10" refX="12" refY="5" markerWidth="9.1" markerHeight="7" orient="auto">' \
            '<path d="M13,5 L0.5,0.3 L2.5,5 L0.5,9.7 z" fill="#000"/></marker>'   # 뒤가 오목하고 긴 화살표(사용자 예시, x축 화살표 기준)
    return ('<defs>%s</defs><line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#000" stroke-width="%s" marker-end="url(#ar)"/>'
            '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#000" stroke-width="%s" marker-end="url(#ar)"/>'
            % (arrow, x0, y0, x1, y0, AX, ox, yb, ox, yt, AX))


def two_parabolas(f, g, xr, yr, sx, sy, ticks, flab, glab):
    """f, g: 함수, xr/yr: 보이는 범위, sx/sy: 한 칸 픽셀, ticks: x절편 눈금, flab/glab: (x, y, 위치) 이름표"""
    F = Frame(xr, yr, sx, sy, (30, 30, 100, 30))          # 축·화살표·x, y 이름은 Frame.axes(공통 기준)
    fx = [x / 100 for x in range(int(xr[0] * 100), int(xr[1] * 100) + 1) if yr[0] <= f(x / 100) <= yr[1]]
    gx = [x / 100 for x in range(int(xr[0] * 100), int(xr[1] * 100) + 1) if yr[0] <= g(x / 100) <= yr[1]]
    F.axes()
    F.curve(f, fx[0], fx[-1]); F.curve(g, gx[0], gx[-1])
    F.lab((0, 0), r"\mathrm{O}", "rt", -5, 5, 20)
    for tx, anc, dx, dy in ticks:
        F.lab((tx, 0), str(tx) if tx >= 0 else "-%d" % -tx, ("r" if anc == "l" else "l") + ("t" if dy > 0 else "b"), dx, dy, 20)
    for (x, y, anc), tex in ((flab, "y=f(x)"), (glab, "y=g(x)")):
        F.lab((x, y), tex, anc, 0, 0, 20)
    return F.render()


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
    s, sx = 30 * ZOOM, 70 * ZOOM   # 가로를 늘려 그린 개형(접하는 관계는 그대로 유지됨). ZOOM: 문서 폭에 맞춘 확대
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


LN = 2.0      # 직선·선분 굵기 (곡선은 STROKE)
ZOOM = 1.0    # 그림 전체 확대(한 칸 픽셀에만 곱함). 글자·화살표 크기는 그대로 두고 그림 크기만 맞출 때 쓴다
K_HWP = 6.4   # 문서에 넣을 때 PNG 1픽셀당 HWPUNIT(모든 그림 같게: 화살표·글자 크기가 같아 보이도록)


class Frame:
    """수학 좌표 -> 화면 좌표. xr/yr: 보이는 범위, sx/sy: 한 칸 픽셀, m=(왼, 위, 오른, 아래) 여백"""

    def __init__(self, xr, yr, sx, sy, m):
        sx, sy = sx * ZOOM, sy * ZOOM
        self.xr, self.yr, self.sx, self.sy, self.m = xr, yr, sx, sy, m
        self.w = int((xr[1] - xr[0]) * sx + m[0] + m[2])
        self.h = int((yr[1] - yr[0]) * sy + m[1] + m[3])
        self.svg, self.labels = [], []

    def P(self, x, y):
        return (self.m[0] + (x - self.xr[0]) * self.sx, self.m[1] + (self.yr[1] - y) * self.sy)

    def axes(self):
        self.svg.append(axes(self.P, self.xr, self.yr))
        X, Y = self.P(self.xr[1], 0)
        self.labels.append((X + 0.3, Y + 1.1, "x", 22, "rt"))     # 사용자 예시에 맞춘 위치
        X, Y = self.P(0, self.yr[1])
        self.labels.append((X - 10, Y + 3.7, "y", 22, "rc"))     # y는 화살표 왼쪽, 글자 윗끝을 화살표 끝 높이에(사용자 예시)

    def curve(self, f, x0, x1):
        self.svg.append(curve(f, x0, x1, self.P))

    def seg(self, p, q, wd=LN, extra=""):
        self.svg.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#000" stroke-width="%s" stroke-linecap="round" %s/>'
                        % (self.P(*p) + self.P(*q) + (wd, extra)))

    def poly(self, pts, fill):
        self.svg.insert(0, '<polygon points="%s" fill="%s" stroke="none"/>' % (" ".join("%.1f,%.1f" % self.P(*p) for p in pts), fill))

    def lab(self, p, tex, anc, dx=0, dy=0, size=21):
        X, Y = self.P(*p)
        self.labels.append((X + dx, Y + dy, tex, size, anc))

    def pt(self, p, name, anc, dx, dy):
        self.lab(p, r"\mathrm{%s}" % name, anc, dx, dy)

    def render(self):
        svg = '<svg width="%d" height="%d" style="position:absolute;left:0;top:0">%s</svg>' % (self.w, self.h, "".join(self.svg))
        return page(svg, self.labels, self.w, self.h), self.w, self.h



def fit_shoot(name, fn, target_w, out_dir):
    """문서 폭 target_w(HWPUNIT)일 때 1픽셀=K_HWP가 되도록 ZOOM을 맞춰 그린다. 결과 PNG 폭 = target_w/K_HWP
    ZOOM은 이 함수가 정의된 모듈의 전역값(Frame과 같은 모듈)을 바꾼다."""
    from draw import shoot
    G = globals()
    G["ZOOM"] = 1.0
    want = target_w / K_HWP / 3                       # shoot는 3배로 찍는다
    for _ in range(10):                               # 여백은 그대로이므로 몇 번 맞춘다
        doc, w, h = fn()
        if abs(w - want) < 1:
            break
        G["ZOOM"] *= want / w
    doc, w, h = fn()
    shoot(doc, w, h, os.path.join(out_dir, name))
    G["ZOOM"] = 1.0


def roots(f, lo, hi, v, n=4000):
    """f(x)=v인 x (구간 [lo, hi]에서 부호 바뀜으로 찾음)"""
    out, xs = [], [lo + (hi - lo) * i / n for i in range(n + 1)]
    for a, b in zip(xs, xs[1:]):
        if (f(a) - v) * (f(b) - v) <= 0:
            for _ in range(60):
                c = (a + b) / 2
                if (f(a) - v) * (f(c) - v) <= 0: b = c
                else: a = c
            out.append((a + b) / 2)
    return out


def fig_m3243():
    # 2025년 6월 고1 16번: y=x^2-(a+1)x+a 와 직선 y=bx-b (A(1,0)에서 접함, b=1-a). 개형으로 a=3.5
    a = 3.5
    b = 1 - a
    f = lambda x: x * x - (a + 1) * x + a
    g = lambda x: b * x - b
    F = Frame((-1.5, 5.2), (-2.7, 5.7), 46, 34, (20, 10, 60, 10))
    F.axes()
    x0, x1 = roots(f, -2, 1, 4.4)[0], roots(f, 2, 6, 4.4)[0]
    F.curve(f, x0, x1)
    l0, l1 = roots(g, -3, 1, 4.4)[0], roots(g, 1, 4, -2.6)[0]
    F.seg((l0, g(l0)), (l1, g(l1)))
    F.seg((0, a), (a, 0))                               # 선분 CB
    F.lab((l1, g(l1)), r"y=bx-b", "lc", 8, 0, 20)          # 위쪽은 y축 이름표와 겹치므로 아래 끝에 둠
    F.lab((x1, f(x1)), r"y=x^{2}-(a+1)x+a", "rb", 58, -6, 20)
    F.pt((0, 0), "O", "rt", -5, 5)
    F.pt((1, 0), "A", "rt", -3, 5)
    F.pt((a, 0), "B", "lt", 6, 4)
    F.pt((0, a), "C", "lb", 7, -3)
    F.pt((0, -b), "D", "rt", -6, 3)
    return F.render()


def fig_m3336():
    # 2026년 9월 고1 19번: f(x)=k(x-p)(x-q) 가 y=-x 에 접함. 개형으로 A=1, B=4.5 (k는 접하도록 계산)
    p, q = 1.0, 4.5
    # k(x-p)(x-q)=-x 의 판별식 (k(p+q)-1)^2-4k*kpq=0 의 큰 근
    A2, B2 = (p + q) ** 2 - 4 * p * q, -2 * (p + q)
    k = (-B2 + (B2 * B2 - 4 * A2) ** 0.5) / (2 * A2)
    f = lambda x: k * (x - p) * (x - q)
    tx = (k * (p + q) - 1) / (2 * k)                     # 접점 P의 x좌표
    F = Frame((-2.5, 6.4), (-3.9, 6.6), 40, 40, (20, 14, 100, 14))
    F.axes()
    x0, x1 = roots(f, -2, p, 6.2)[0], roots(f, q, 8, 6.2)[0]
    F.curve(f, x0, x1)
    F.seg((-1.45, 1.45), (3.7, -3.7))
    F.lab((x1, f(x1)), r"y=f(x)", "lc", 8, 4, 20)
    F.lab((-1.45, 1.45), r"y=-x", "cb", -4, -6, 20)
    F.pt((0, 0), "O", "rt", -5, 5)
    F.pt((p, 0), "A", "lb", 5, -4)
    F.pt((q, 0), "B", "rb", -5, -4)
    F.pt((0, k * p * q), "C", "rt", -6, 3)
    F.pt((tx, -tx), "P", "rt", -6, 4)
    return F.render()


def fig_m3217():
    # 2025년 3월 고1 20번: y=-ax^2+8ax, C(4,16a), D(4,0), A(4-t,s), B(4+t,s), DE // BC
    a, t = 15 / 32, (16 / 5) ** 0.5
    f = lambda x: -a * x * x + 8 * a * x
    C, D = (4, 16 * a), (4, 0)
    A, B = (4 - t, f(4 - t)), (4 + t, f(4 + t))
    m = (B[1] - C[1]) / (B[0] - C[0])
    h = lambda x: m * (x - 4)
    ex = max(roots(lambda x: f(x) - h(x), 4, 12, 0))
    E = (ex, f(ex))
    F = Frame((-1.6, 10.6), (-5.6, 8.6), 36, 36, (16, 30, 64, 10))
    F.poly([(0, 0), A, D], "#d6ecfb")                     # 삼각형 AOD (연한 하늘)
    F.axes()
    x0, x1 = roots(f, -3, 0, -5.4)[0], roots(f, 8, 12, -5.4)[0]
    F.curve(f, x0, x1)
    F.seg((-1.2, h(-1.2)), (10.2, h(10.2)))               # 점 D를 지나고 BC에 평행한 직선
    for p_, q_ in ((( 0, 0), A), (A, D), (A, B), (C, A), (C, B), (C, D), (C, E), (B, E)):
        F.seg(p_, q_)
    X, Y = F.P(*D)
    F.svg.append('<polyline points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="none" stroke="#000" stroke-width="1.6"/>'
                 % (X + 11, Y, X + 11, Y - 11, X, Y - 11))
    F.lab((4 + ((16 * a - 3.4) / a) ** 0.5, 3.4), r"y=-ax^{2}+8ax", "lc", 12, 0, 20)
    F.pt((0, 0), "O", "lt", 5, 5)
    F.pt(A, "A", "rb", -7, -1)
    F.pt(B, "B", "lb", 7, -1)
    F.pt(C, "C", "cb", 0, -7)
    F.pt(D, "D", "rt", -4, 5)
    F.pt(E, "E", "lb", 9, -2)
    return F.render()


if __name__ == "__main__":
    # (파일, 함수, 문서에 넣는 폭 HWPUNIT = unit05.py의 "w"). 1픽셀=K_HWP로 맞춘다
    for name, fn, wd in (("u5_n1090.png", fig_n1090, 16000), ("u5_n1162.png", fig_n1162, 16000), ("u5_n3040.png", fig_n3040, 9000),
                         ("u5_m3243.png", fig_m3243, 12500), ("u5_m3336.png", fig_m3336, 13000), ("u5_m3217.png", fig_m3217, 14000)):
        if len(sys.argv) > 1 and name not in sys.argv[1:]:
            continue
        fit_shoot(name, fn, wd, HERE)
