# -*- coding: utf-8 -*-
"""유형서 그림 다시 그리기 (SVG + KaTeX를 Chromium으로 PNG로 찍는다)
python 그림/draw.py   (KATEX_DIR 필요)
- image86.png: 1단원 4번 정육면체 (폼의 그림은 위가 잘려 있음)
- image83.png: 1단원 17번 직각삼각형 (선분 CD의 길이 표시 점선, ∠C 직각 표시)
"""
import os, math
from html import escape
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
KATEX = os.environ["KATEX_DIR"]
STROKE = 3.2
ZOOM = 1.0     # 그림 크기만 키우거나 줄임(글자 크기는 그대로). 문서 폭에 1픽셀=6.4 HWPUNIT로 맞출 때 쓴다
CHROME = os.environ.get("CHROME", "/opt/pw-browsers/chromium-1194/chrome-linux/chrome")


def page(svg, labels, w, h):
    """labels: [(x, y, tex, size, anchor)] anchor는 글자 상자의 기준(가운데 'c', 왼쪽 'l' 등)"""
    divs = []
    for x, y, tex, size, anc in labels:
        tx = {"c": "-50%", "l": "0", "r": "-100%"}[anc[0]]
        ty = {"c": "-50%", "t": "0", "b": "-100%"}[anc[1] if len(anc) > 1 else "c"]
        divs.append('<div class="lb" style="left:%.1fpx;top:%.1fpx;font-size:%dpx;transform:translate(%s,%s)" data-tex="%s"></div>'
                    % (x, y, size, tx, ty, escape(tex, quote=True)))
    return """<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="file://%s/katex.min.css"><script src="file://%s/katex.min.js"></script>
<style>body{margin:0;background:#fff}#fig{position:relative;width:%dpx;height:%dpx;background:#fff}
.lb{position:absolute;white-space:nowrap;line-height:1}</style></head><body>
<div id="fig">%s%s</div>
<script>document.querySelectorAll('.lb').forEach(e=>katex.render(e.dataset.tex,e,{throwOnError:true}))</script>
</body></html>""" % (KATEX, KATEX, w, h, svg, "".join(divs))


def shoot(html, w, h, out, scale=3):
    path = os.path.join(HERE, "_draw.html")
    open(path, "w", encoding="utf-8").write(html)
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME)
        pg = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=scale)
        pg.goto("file://" + path)
        pg.wait_for_timeout(300)
        pg.locator("#fig").screenshot(path=out)
        b.close()
    os.remove(path)
    print("->", out)


def cube():
    # 꼭짓점 쪽에서 본 정육면체: 앞 모서리 x=0, 왼쪽·오른쪽 면, 위 면
    W, d, H, m = 150 * ZOOM, 48 * ZOOM, 150 * ZOOM, 12
    ox, oy = m + W, m + 2 * d          # 앞 모서리 위 꼭짓점
    F, L, R, K = (ox, oy), (ox - W, oy - d), (ox + W, oy - d), (ox, oy - 2 * d)
    F2, L2, R2 = (ox, oy + H), (ox - W, oy - d + H), (ox + W, oy - d + H)
    w, h = int(2 * W + 2 * m), int(2 * d + H + 2 * m)

    def poly(pts, fill):
        return '<polygon points="%s" fill="%s" stroke="#000" stroke-width="%s" stroke-linejoin="round"/>' % (
            " ".join("%.1f,%.1f" % p for p in pts), fill, STROKE)
    svg = '<svg width="%d" height="%d" style="position:absolute;left:0;top:0">%s%s%s</svg>' % (
        w, h, poly([F, L, K, R], "#ebf6fd"), poly([F, L, L2, F2], "#d6ecfb"), poly([F, R, R2, F2], "#c1e1f7"))   # 세 면: 연한 하늘색, 명도만 다르게(위 밝게, 오른쪽 어둡게)
    labels = [(ox, oy - d, r"3x^{3}-x^{2}", 25, "cc"),
              (ox - W / 2, oy - d / 2 + H / 2, r"-x^{3}+x", 25, "cc"),
              (ox + W / 2, oy - d / 2 + H / 2, r"x^{3}+1", 25, "cc")]
    return page(svg, labels, w, h), w, h


def triangle():
    # 원래 그림과 같은 비율: B(0,0), C(850,0), A(850,1220) (수학 좌표), 화면에 맞게 줄임
    s = 0.28 * ZOOM
    Bm, Cm, Am = (0, 0), (850, 0), (850, 1220)
    ux, uy = Am[0] - Bm[0], Am[1] - Bm[1]
    t = ((Cm[0] - Bm[0]) * ux + (Cm[1] - Bm[1]) * uy) / (ux * ux + uy * uy)
    Dm = (Bm[0] + t * ux, Bm[1] + t * uy)
    ml, mt = 50, 45
    H = 1220 * s
    w, h = int(850 * s + 2 * ml + 10), int(H + 2 * mt)

    def P(q):
        return (ml + q[0] * s, mt + H - q[1] * s)
    B, C, A, D = P(Bm), P(Cm), P(Am), P(Dm)

    def line(p, q, extra=""):
        return '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#000" stroke-width="%s" stroke-linecap="round" %s/>' % (
            p[0], p[1], q[0], q[1], STROKE, extra)

    def unit(p, q):
        dx, dy = q[0] - p[0], q[1] - p[1]
        n = math.hypot(dx, dy)
        return dx / n, dy / n

    def right_mark(v, p, q, k=13):
        a, b = unit(v, p), unit(v, q)
        p1 = (v[0] + a[0] * k, v[1] + a[1] * k)
        p2 = (p1[0] + b[0] * k, p1[1] + b[1] * k)
        p3 = (v[0] + b[0] * k, v[1] + b[1] * k)
        return '<polyline points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="none" stroke="#000" stroke-width="2"/>' % (
            p1 + p2 + p3)
    # 선분 CD 길이 표시: CD 바깥(삼각형 ACD 쪽)으로 휜 점선
    mx, my = (C[0] + D[0]) / 2, (C[1] + D[1]) / 2
    ex, ey = unit(D, C)
    nx, ny = ey, -ex                    # CD에 수직, A 쪽
    if (A[0] - mx) * nx + (A[1] - my) * ny < 0:
        nx, ny = -nx, -ny
    bulge = 19
    cx, cy = mx + nx * bulge * 2, my + ny * bulge * 2
    arc = '<path d="M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" fill="none" stroke="#000" stroke-width="1.6" stroke-dasharray="5,4"/>' % (
        D[0], D[1], cx, cy, C[0], C[1])
    svg = '<svg width="%d" height="%d" style="position:absolute;left:0;top:0">%s%s%s%s%s%s%s</svg>' % (
        w, h, line(A, B), line(B, C), line(C, A), line(C, D), right_mark(D, C, A), right_mark(C, B, A), arc)
    lx, ly = mx + nx * (bulge + 17), my + ny * (bulge + 17)
    labels = [(A[0], A[1] - 8, r"\mathrm{A}", 24, "cb"), (B[0] - 6, B[1] + 4, r"\mathrm{B}", 24, "rc"),
              (C[0] + 6, C[1] + 4, r"\mathrm{C}", 24, "lc"), (D[0] - 10, D[1] - 6, r"\mathrm{D}", 24, "rb"),
              (lx, ly, "1", 22, "cc")]
    return page(svg, labels, w, h), w, h


if __name__ == "__main__":
    # (파일, 함수, 폼 그림의 가로 HWPUNIT). 1픽셀=6.4 HWPUNIT가 되도록 ZOOM을 맞춘다(그림 축척 통일)
    for name, fn, wd in (("image86.png", cube, 13033), ("image83.png", triangle, 11357)):
        want = wd / 6.4 / 3
        ZOOM = 1.0
        for _ in range(10):
            doc, w, h = fn()
            if abs(w - want) < 1:
                break
            ZOOM *= want / w
        doc, w, h = fn()
        shoot(doc, w, h, os.path.join(HERE, name))
