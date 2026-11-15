# -*- coding: utf-8 -*-
"""수학 문제 그림 도구 (SVG + KaTeX를 Chromium으로 찍어 PNG로 만든다)

그림 약속(SKILL.md)을 코드로 고정해 둔 것이다. 축·화살표·x, y 글자 위치, 선 굵기, 글자 크기, 연한 색,
1픽셀=6.4 HWPUNIT 맞춤이 모든 그림에서 같게 나온다.

필요: pip install playwright (Chromium). KaTeX는 KATEX_DIR(katex/dist 폴더)가 있으면 그것을, 없으면 CDN을 쓴다.
Chromium 경로는 CHROME 환경 변수로 바꿀 수 있다(없으면 playwright 기본).

예)
    from mathfig import Frame, fit_shoot, roots, dot, right_mark, dim_arc, SKY
    def fig():
        f = lambda t: 0.5 * (t + 2) * (t - 3)
        F = Frame((-3.6, 4.6), (-3.6, 2.6), 34, 34, (20, 12, 70, 12))
        F.axes()
        F.curve(f, roots(f, -6, 0.5, 2.3)[0], roots(f, 0.5, 7, 2.3)[0])
        F.pt((0, 0), "O", "rt", -4, 4)
        F.lab((-2, 0), "-2", "rt", -3, 4); F.lab((3, 0), "3", "lt", 3, 4)
        return F.render()
    fit_shoot("graph.png", fig, 9000, ".")      # 문서에 넣는 폭 9000 HWPUNIT
"""
import os, math
from html import escape

# ---------------------------------------------------------------- 약속된 값 (바꾸지 않는다)
FONT = 22          # 그림 안 글씨 크기(px). 모두 같게. 면을 채우는 큰 글씨(정육면체 면의 식)만 예외
STROKE = 3.2       # 곡선·도형 테두리 굵기
LN = 2.0           # 직선·선분 굵기
AX = 2.0           # 좌표축 굵기
K_HWP = 6.4        # 문서에 넣을 때 PNG 1픽셀당 HWPUNIT (모든 그림 같게)
ZOOM = 1.0         # fit_shoot가 조정한다(그림 크기만 바뀌고 글자·화살표 크기는 그대로)

# 색칠은 회색 대신 연한 색
PINK, GREEN, SKY, LAVENDER, YELLOW = "#ffd9e6", "#dcf3d2", "#d6ecfb", "#e8defa", "#fff3bf"
# 정육면체 세 면: 연한 하늘색 한 색에 명도만 다르게
CUBE_TOP, CUBE_LEFT, CUBE_RIGHT = "#ebf6fd", "#d6ecfb", "#c1e1f7"

# 뒤가 오목하고 긴 화살표 머리(기준 그림 axes_example.png를 픽셀 단위로 재어 맞춤: 길이 24, 반폭 9, 오목 3픽셀)
ARROW = ('<marker id="ar" viewBox="0 0 13 10" refX="12" refY="5" markerWidth="9.1" markerHeight="7" orient="auto">'
         '<path d="M13,5 L0.5,0.3 L2.5,5 L0.5,9.7 z" fill="#000"/></marker>')

KATEX = os.environ.get("KATEX_DIR")
CHROME = os.environ.get("CHROME")


def _katex_links():
    if KATEX:
        base = "file://" + KATEX
    else:
        base = "https://cdn.jsdelivr.net/npm/katex@0.16.9/dist"
    return '<link rel="stylesheet" href="%s/katex.min.css"><script src="%s/katex.min.js"></script>' % (base, base)


def page(svg, labels, w, h):
    """labels: [(x, y, tex, size, anchor)]. anchor는 글자 상자의 기준점: 가로 l/c/r + 세로 t/c/b (예: 'rt')
    글씨 크기는 FONT로 통일한다(size가 FONT보다 훨씬 큰 경우만 그대로). 분수는 \\dfrac로 바꿔 숫자가 작아지지 않게 한다."""
    divs = []
    for x, y, tex, size, anc in labels:
        size = size if size > FONT + 4 else FONT
        tex = tex.replace(r"\dfrac", r"\frac").replace(r"\frac", r"\dfrac")
        tx = {"c": "-50%", "l": "0", "r": "-100%"}[anc[0]]
        ty = {"c": "-50%", "t": "0", "b": "-100%"}[anc[1] if len(anc) > 1 else "c"]
        divs.append('<div class="lb" style="left:%.1fpx;top:%.1fpx;font-size:%dpx;transform:translate(%s,%s)" data-tex="%s"></div>'
                    % (x, y, size, tx, ty, escape(tex, quote=True)))
    return """<!doctype html><html><head><meta charset="utf-8">%s
<style>body{margin:0;background:#fff}#fig{position:relative;width:%dpx;height:%dpx;background:#fff}
.lb{position:absolute;white-space:nowrap;line-height:1}</style></head><body>
<div id="fig">%s%s</div>
<script>document.querySelectorAll('.lb').forEach(e=>katex.render(e.dataset.tex,e,{throwOnError:true}))</script>
</body></html>""" % (_katex_links(), w, h, svg, "".join(divs))


def shoot(html, w, h, out, scale=3):
    """HTML을 3배 해상도 PNG로 찍는다"""
    from playwright.sync_api import sync_playwright
    path = os.path.abspath(out) + ".html"
    open(path, "w", encoding="utf-8").write(html)
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME) if CHROME else p.chromium.launch()
        pg = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=scale)
        pg.goto("file://" + path)
        pg.wait_for_function("document.querySelectorAll('.lb .katex').length === document.querySelectorAll('.lb').length")
        pg.wait_for_timeout(200)
        pg.locator("#fig").screenshot(path=out)
        b.close()
    os.remove(path)
    print("->", out)


def curve(f, x0, x1, P, n=200, extra=""):
    pts = ["%.1f,%.1f" % P(x0 + (x1 - x0) * i / n, f(x0 + (x1 - x0) * i / n)) for i in range(n + 1)]
    return '<polyline points="%s" fill="none" stroke="#000" stroke-width="%s" stroke-linejoin="round" %s/>' % (
        " ".join(pts), STROKE, extra)


class Frame:
    """수학 좌표 -> 화면 좌표. xr/yr: 보이는 범위, sx/sy: 한 칸 픽셀, m=(왼, 위, 오른, 아래) 여백(px)"""

    def __init__(self, xr, yr, sx, sy, m):
        sx, sy = sx * ZOOM, sy * ZOOM
        self.xr, self.yr, self.sx, self.sy, self.m = xr, yr, sx, sy, m
        self.w = int((xr[1] - xr[0]) * sx + m[0] + m[2])
        self.h = int((yr[1] - yr[0]) * sy + m[1] + m[3])
        self.svg, self.labels = ["<defs>%s</defs>" % ARROW], []

    def P(self, x, y):
        return (self.m[0] + (x - self.xr[0]) * self.sx, self.m[1] + (self.yr[1] - y) * self.sy)

    def axes(self):
        """x축·y축(보이는 범위 끝까지)과 x, y 글자. y는 y축 화살표 왼쪽(글자 윗끝 = 화살표 끝 높이),
        x는 x축 아래(글자 오른쪽 끝 = 화살표 끝 바로 왼쪽)"""
        self.xaxis(self.xr[0], self.xr[1])
        (ox, yb), (_, yt) = self.P(0, self.yr[0]), self.P(0, self.yr[1])
        self.svg.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#000" stroke-width="%s" marker-end="url(#ar)"/>'
                        % (ox, yb, ox, yt, AX))
        self.labels.append((ox - 10, yt + 3.7, "y", 22, "rc"))

    def xaxis(self, x0, x1):
        """x축만(그래프와 x축의 위치 관계 그림 등)"""
        (a, y), (b, _) = self.P(x0, 0), self.P(x1, 0)
        self.svg.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#000" stroke-width="%s" marker-end="url(#ar)"/>'
                        % (a, y, b, y, AX))
        self.labels.append((b + 0.3, y + 1.1, "x", 22, "rt"))

    def curve(self, f, x0, x1, extra=""):
        self.svg.append(curve(f, x0, x1, self.P, extra=extra))

    def seg(self, p, q, wd=LN, extra=""):
        self.svg.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#000" stroke-width="%s" stroke-linecap="round" %s/>'
                        % (self.P(*p) + self.P(*q) + (wd, extra)))

    def dashed(self, p, q):
        self.seg(p, q, 1.5, 'stroke-dasharray="5,4"')

    def poly(self, pts, fill):
        """색칠(테두리 없음, 맨 아래 층)"""
        self.svg.insert(1, '<polygon points="%s" fill="%s" stroke="none"/>' % (" ".join("%.1f,%.1f" % self.P(*p) for p in pts), fill))

    def lab(self, p, tex, anc, dx=0, dy=0, size=FONT):
        X, Y = self.P(*p)
        self.labels.append((X + dx, Y + dy, tex, size, anc))

    def pt(self, p, name, anc, dx, dy):
        """점 이름은 로만체(\\mathrm)"""
        self.lab(p, r"\mathrm{%s}" % name, anc, dx, dy)

    def render(self):
        svg = '<svg width="%d" height="%d" style="position:absolute;left:0;top:0">%s</svg>' % (self.w, self.h, "".join(self.svg))
        return page(svg, self.labels, self.w, self.h), self.w, self.h


def fit_shoot(name, fn, target_w, out_dir="."):
    """문서 폭 target_w(HWPUNIT)일 때 PNG 1픽셀 = K_HWP가 되도록 ZOOM만 맞춰 찍는다.
    결과 PNG의 CSS 폭 = target_w / K_HWP / 3 (3배 해상도). 글자·화살표는 픽셀 크기 그대로라 모든 그림에서 같아 보인다."""
    G = globals()
    G["ZOOM"] = 1.0
    want = target_w / K_HWP / 3
    for _ in range(10):
        doc, w, h = fn()
        if abs(w - want) < 1:
            break
        G["ZOOM"] *= want / w
    doc, w, h = fn()
    shoot(doc, w, h, os.path.join(out_dir, name))
    G["ZOOM"] = 1.0


def roots(f, lo, hi, v, n=4000):
    """f(x)=v인 x (구간 [lo, hi]에서 부호 바뀜으로 찾음). 곡선을 보이는 높이 v에서 끊을 때 쓴다"""
    out, xs = [], [lo + (hi - lo) * i / n for i in range(n + 1)]
    for a, b in zip(xs, xs[1:]):
        if (f(a) - v) * (f(b) - v) <= 0:
            for _ in range(60):
                c = (a + b) / 2
                if (f(a) - v) * (f(c) - v) <= 0:
                    b = c
                else:
                    a = c
            out.append((a + b) / 2)
    return out


def dot(F, p, r=3.5):
    F.svg.append('<circle cx="%.1f" cy="%.1f" r="%s" fill="#000"/>' % (F.P(*p) + (r,)))


def right_mark(F, v, p, q, k=0.06):
    """꼭짓점 v에서 v->p, v->q 방향의 직각 표시 (k: 수학 좌표 길이)"""
    def u(a, b):
        dx, dy = b[0] - a[0], b[1] - a[1]
        n = math.hypot(dx, dy)
        return dx / n, dy / n
    a, b = u(v, p), u(v, q)
    p1 = (v[0] + a[0] * k, v[1] + a[1] * k)
    p2 = (p1[0] + b[0] * k, p1[1] + b[1] * k)
    p3 = (v[0] + b[0] * k, v[1] + b[1] * k)
    F.svg.append('<polyline points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="none" stroke="#000" stroke-width="1.6"/>'
                 % (F.P(*p1) + F.P(*p2) + F.P(*p3)))


def dim_arc(F, p, q, label, side, bulge=16, size=FONT, gap=6, cut=True):
    """선분 pq의 길이 표시: side 쪽(+1/-1)으로 휜 점선 호를 긋는다.
    약속: 점선의 가운데를 끊고 그 끊은 자리에 길이를 쓴다(cut=True, 기본).
    bulge는 호가 선분에서 떨어지는 정도(픽셀). 글자가 다른 점 이름·선과 붙으면 bulge를 키운다(보통 16~46).
    cut=False는 예전 모양(끊지 않은 호 바깥에 글자)으로, 새 그림에는 쓰지 않는다."""
    (x1, y1), (x2, y2) = F.P(*p), F.P(*q)
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    dx, dy = x2 - x1, y2 - y1
    n = math.hypot(dx, dy)
    nx, ny = -dy / n * side, dx / n * side
    cx, cy = mx + nx * 2 * bulge, my + ny * 2 * bulge
    dash = 'fill="none" stroke="#000" stroke-width="1.5" stroke-dasharray="5,4"'
    if not cut:
        F.svg.append('<path d="M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" %s/>' % (x1, y1, cx, cy, x2, y2, dash))
        lx, ly = mx + nx * (bulge + gap), my + ny * (bulge + gap)
        anc = ("l" if nx > 0.5 else "r" if nx < -0.5 else "c") + ("t" if ny > 0.5 else "b" if ny < -0.5 else "c")
        F.labels.append((lx, ly, label, size, anc))
        return

    def B(t):
        return ((1 - t) ** 2 * x1 + 2 * t * (1 - t) * cx + t * t * x2, (1 - t) ** 2 * y1 + 2 * t * (1 - t) * cy + t * t * y2)

    def sub(t0, t1):                    # 2차 베지에의 [t0, t1] 부분
        a, b = B(t0), B(t1)
        d0 = (2 * (1 - t0) * (cx - x1) + 2 * t0 * (x2 - cx), 2 * (1 - t0) * (cy - y1) + 2 * t0 * (y2 - cy))
        h = (t1 - t0) / 2
        c = (a[0] + d0[0] * h, a[1] + d0[1] * h)
        return '<path d="M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" %s/>' % (a + c + b + (dash,))

    M = B(0.5)
    # 끊는 길이: 호가 가로로 지나면 글자 폭, 세로로 지나면 글자 높이에 여유를 더한 만큼
    half = (len(label) * 0.62 * size) / 2 + 6 if abs(dx) >= abs(dy) else size * 0.75 / 2 + 10
    t = 0.5
    while t > 0 and math.hypot(B(t)[0] - M[0], B(t)[1] - M[1]) < half:
        t -= 0.002
    F.svg.append(sub(0, t))
    F.svg.append(sub(1 - t, 1))
    F.labels.append((M[0], M[1], label, size, "cc"))

if __name__ == "__main__":
    # 시험: 두 점 (-2, 0), (3, 0)을 지나는 포물선과 직사각형 길이 표시
    def fig_graph():
        f = lambda t: 0.5 * (t + 2) * (t - 3)
        F = Frame((-3.6, 4.6), (-3.6, 2.6), 34, 34, (20, 12, 70, 12))
        F.axes()
        F.curve(f, roots(f, -6, 0.5, 2.3)[0], roots(f, 0.5, 7, 2.3)[0])
        F.pt((0, 0), "O", "rt", -4, 4)
        F.lab((-2, 0), "-2", "rt", -3, 4); F.lab((3, 0), "3", "lt", 3, 4)
        x1 = roots(f, 0.5, 7, 2.3)[0]
        F.lab((x1, 2.3), r"y=f(x)", "lc", 6, 4)
        return F.render()

    def fig_rect():
        F = Frame((-0.5, 8.5), (-0.5, 5.5), 30, 30, (60, 30, 40, 50))
        A, B, C, D = (0, 4), (0, 0), (7, 0), (7, 4)
        F.poly([A, B, C, D], SKY)
        for p, q in ((A, B), (B, C), (C, D), (D, A)):
            F.seg(p, q)
        right_mark(F, B, A, C, 0.45)
        F.pt(A, "A", "rb", -4, -4); F.pt(B, "B", "rt", -4, 4); F.pt(C, "C", "lt", 4, 4); F.pt(D, "D", "lb", 4, -4)
        dim_arc(F, B, C, "7", 1, 22)
        dim_arc(F, B, A, "4", -1, 22)
        return F.render()

    fit_shoot("example_graph.png", fig_graph, 9000)
    fit_shoot("example_rect.png", fig_rect, 9000)
