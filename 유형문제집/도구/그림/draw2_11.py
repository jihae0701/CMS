# -*- coding: utf-8 -*-
"""공통수학2 11단원(유리식과 유리함수) 기본서·유형서 완성본(2026-11-16)에 붙여 넣은 스캔 그림을 그림 규칙대로 다시 그림.
python draw2_11.py [파일 ...]  (KATEX_DIR 필요)
기본서
- c2b11_400 : 400번 해설 점근선 x=1, x=k, y=6, y=−k로 둘러싸인 직사각형(개형 k=3, 연분홍)
- c2b11_409 : 409번 해설 y=(2x+2)/(x+2), 치역 y≤3/2 또는 y≥4인 부분(실선)과 그 띠(하늘)
유형서(번호는 미주 585부터로 맞춘 뒤 번호)
- c2y11_596 : 596번 문제 y=(bx−c)/(x+a) (점근선 x=1, y=2, 점 (2, 0))
- c2y11_615 : 615번 해설 y=1/(x−1) (2≤x≤3 실선), y=ax, y=bx
- c2y11_623 : 623번 해설 y=(x−1)/(x+1), 점근선의 교점 A(−1, 1), y=−x, y=x+2, 원, P₁, P₂
- c2y11_628 : 628번 해설 y=4/(x−1)−2, A(−1, 1), B(3, −5), P(3, 0), M(1, −2), 직선 x+y+1=0
- c2y11_633a / c2y11_633b : 633번 해설 y=(k+15)/(x−3)+5, (ⅰ) k+15<0 (ⅱ) k+15>0 (개형: k+15=−4, 11)
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from draw import HERE, STROKE
from draw5 import Frame, fit_shoot
from draw10y import dot

PINK, SKY = "#ffd9e6", "#d6ecfb"
DASH = 'stroke-dasharray="5,4"'


def fn(F, f, x0, x1, extra="", n=300):
    pts = [(x0 + (x1 - x0) * i / n, f(x0 + (x1 - x0) * i / n)) for i in range(n + 1)]
    F.svg.append('<polyline points="%s" fill="none" stroke="#000" stroke-width="%s" stroke-linejoin="round" %s/>'
                 % (" ".join("%.1f,%.1f" % F.P(*p) for p in pts), STROKE, extra))


def dash(F, p, q):
    F.seg(p, q, 1.5, DASH)


def odot(F, p, r=4.5):
    X, Y = F.P(*p)
    F.svg.append('<circle cx="%.1f" cy="%.1f" r="%s" fill="#fff" stroke="#000" stroke-width="1.6"/>' % (X, Y, r))


def tick(F, p, q, n=2):
    """선분 pq 가운데에 같은 길이 표시(짧은 빗금 n개)"""
    (x1, y1), (x2, y2) = F.P(*p), F.P(*q)
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    L = math.hypot(x2 - x1, y2 - y1); ux, uy = (x2 - x1) / L, (y2 - y1) / L
    for k in range(n):
        o = (k - (n - 1) / 2) * 5
        cx, cy = mx + ux * o, my + uy * o
        F.svg.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#000" stroke-width="1.5"/>'
                     % (cx - uy * 6, cy + ux * 6, cx + uy * 6, cy - ux * 6))


# ---------------------------------------------------------------- 기본서 400 (k=3)
def b400():
    K = 3
    F = Frame((-1.0, 5.4), (-4.4, 7.4), 40, 32, (16, 12, 80, 40))
    F.poly([(1, 6), (K, 6), (K, -K), (1, -K)], PINK)
    F.axes()
    for x in (1, K):
        dash(F, (x, 7.0), (x, -4.2))
    for y in (6, -K):
        dash(F, (-0.6, y), (5.0, y))
    F.pt((0, 0), "O", "rt", -4, 4)
    F.lab((1, 0), "1", "lt", 4, 4); F.lab((K, 0), "k", "lt", 4, 4)
    F.lab((0, 6), "6", "rb", -5, -3); F.lab((0, -K), "-k", "rt", -5, 3)
    F.lab((5.0, 6), "y=6", "lc", 6, 0); F.lab((5.0, -K), "y=-k", "lc", 6, 0)
    F.lab((1, -4.2), "x=1", "ct", -14, 6); F.lab((K, -4.2), "x=k", "ct", 14, 6)
    return F.render()


# ---------------------------------------------------------------- 기본서 409
def b409():
    f = lambda x: 2 - 2 / (x + 2)
    F = Frame((-5.0, 4.0), (-3.6, 6.6), 40, 48, (16, 12, 30, 12))
    F.poly([(-5.0, 4), (4.0, 4), (4.0, 6.6), (-5.0, 6.6)], SKY)
    F.poly([(-5.0, 1.5), (4.0, 1.5), (4.0, -3.6), (-5.0, -3.6)], SKY)
    F.axes()
    dash(F, (-2, 6.4), (-2, -3.4)); dash(F, (-4.9, 2), (3.9, 2))
    fn(F, f, -4.9, -3, DASH); fn(F, f, -3, -2 - 2 / 4.4)
    fn(F, f, -2 + 2 / 5.4, 2); fn(F, f, 2, 3.9, DASH)
    dot(F, (-3, 4), 4.5); dot(F, (2, 1.5), 4.5)
    dash(F, (-3, 4), (-3, 0)); dash(F, (-3, 4), (0, 4)); dash(F, (2, 1.5), (2, 0)); dash(F, (2, 1.5), (0, 1.5))
    F.pt((0, 0), "O", "lt", 4, 4)
    F.lab((-3, 0), "-3", "rb", -4, -4); F.lab((-2, 0), "-2", "lt", 4, 6); F.lab((2, 0), "2", "ct", 0, 6)
    F.lab((0, 4), "4", "lb", 5, -3); F.lab((0, 2), "2", "lb", 5, -2); F.lab((0, 1.5), r"\dfrac{3}{2}", "rc", -6, 4)
    return F.render()


# ---------------------------------------------------------------- 유형서 596 (문제)
def y596():
    f = lambda x: 2 - 2 / (x - 1)
    F = Frame((-2.2, 4.6), (-2.6, 6.2), 40, 32, (16, 12, 16, 12)); F.axes()
    dash(F, (1, 6.0), (1, -2.4)); dash(F, (-2.0, 2), (4.4, 2))
    fn(F, f, -2.0, 1 - 2 / 4.0); fn(F, f, 1 + 2 / 4.4, 4.4)
    F.pt((0, 0), "O", "rt", -4, 4)
    F.lab((1, 0), "1", "rt", -4, 4); F.lab((2, 0), "2", "lt", 6, 4); F.lab((0, 2), "2", "rb", -5, -3)
    return F.render()


# ---------------------------------------------------------------- 유형서 615
def y615():
    f = lambda x: 1 / (x - 1)
    F = Frame((-1.4, 4.2), (-1.6, 2.4), 70, 80, (40, 12, 120, 12)); F.axes()
    dash(F, (1, 2.3), (1, -1.5))
    fn(F, f, -1.3, 1 - 1 / 1.5, DASH); fn(F, f, 1 + 1 / 2.3, 2, DASH); fn(F, f, 2, 3); fn(F, f, 3, 4.0, DASH)
    F.seg((-1.3, -0.65), (3.9, 1.95), 2.0); F.seg((-1.3, -1.3 / 6), (4.0, 4.0 / 6), 2.0)
    dot(F, (2, 1), 4.5); dot(F, (3, 0.5), 4.5)
    dash(F, (2, 1), (2, 0)); dash(F, (2, 1), (0, 1)); dash(F, (3, 0.5), (3, 0)); dash(F, (3, 0.5), (0, 0.5))
    F.pt((0, 0), "O", "lt", 4, 4)
    F.lab((1, 0), "1", "lt", 4, 4); F.lab((2, 0), "2", "lt", 4, 4); F.lab((3, 0), "3", "lt", 4, 4)
    F.lab((0, 1), "1", "rc", -6, 0); F.lab((-0.75, 0.62), r"\dfrac{1}{2}", "rc", -2, 0); F.seg((-0.72, 0.58), (-0.08, 0.5), 1.2)
    F.lab((3.9, 1.95), "y=bx", "lc", 6, 0); F.lab((4.0, 4.0 / 6), "y=ax", "lc", 6, -4)
    F.lab((1.9, -1.2), r"y=\dfrac{1}{x-1}", "lc", 0, 0); F.seg((1.88, -1.2), (1.18, -1.3), 1.2)
    return F.render()


# ---------------------------------------------------------------- 유형서 623
def y623():
    f = lambda x: 1 - 2 / (x + 1)
    r2 = math.sqrt(2)
    A = (-1, 1); P1 = (-1 + r2, 1 - r2); P2 = (-1 - r2, 1 + r2)
    F = Frame((-4.4, 2.6), (-2.4, 4.4), 54, 54, (16, 12, 130, 12)); F.axes()
    dash(F, (-1, 4.3), (-1, -2.3)); dash(F, (-4.3, 1), (2.5, 1))
    fn(F, f, -4.3, -1 - 2 / 3.3); fn(F, f, -1 + 2 / 3.3, 2.5)
    F.svg.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="#000" stroke-width="2.0"/>' % (F.P(*A) + (2 * F.sx,)))
    F.seg((-4.3, 4.3), (2.3, -2.3), 2.0); F.seg((-4.3, -2.3), (2.3, 4.3), 2.0)
    F.seg(A, P1, 1.5); F.seg(A, P2, 1.5)
    tick(F, A, P1); tick(F, A, P2)
    for p in (A, P1, P2):
        dot(F, p, 4.5)
    F.pt((0, 0), "O", "rt", -4, 4)
    F.pt((1.1, 1.55), r"A(-1,~1)", "lc", 0, 0); F.seg((1.05, 1.5), (-0.85, 1.07), 1.2)
    F.pt((1.9, -0.75), "P_{1}", "lc", 0, 0); F.seg((1.82, -0.72), (0.55, -0.45), 1.2); F.pt((-3.9, 3.3), "P_{2}", "cc", 0, 0); F.seg((-3.7, 3.1), (-2.5, 2.5), 1.2)
    F.lab((2.3, -2.3), "y=-x", "lc", 6, 0); F.lab((2.3, 4.3), "y=x+2", "lc", 6, 6)
    return F.render()


# ---------------------------------------------------------------- 유형서 628
def y628():
    f = lambda x: 4 / (x - 1) - 2
    A, B, P, M = (-1, 1), (3, -5), (3, 0), (1, -2)
    F = Frame((-3.0, 5.6), (-6.4, 4.2), 40, 34, (16, 12, 110, 30))
    F.poly([A, P, B], PINK)
    F.axes()
    dash(F, (1, 4.0), (1, -6.2)); dash(F, (-2.9, -2), (5.4, -2))
    fn(F, f, -2.9, 1 - 4 / 4.1); fn(F, f, 1 + 4 / 6.2, 5.4)
    F.seg(A, P); F.seg(P, B); F.seg(A, B); F.seg(P, M, 1.5)
    F.seg((-2.0, 1.0), (4.4, -5.4), 2.0)                         # x+y+1=0
    tick(F, A, M); tick(F, M, B)
    s = 0.32                                                     # 직각 표시(PM ⟂ x+y+1=0)
    q1, q2 = (M[0] + s / math.sqrt(2), M[1] + s / math.sqrt(2)), (M[0] - s / math.sqrt(2), M[1] + s / math.sqrt(2))
    F.svg.append('<polyline points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="none" stroke="#000" stroke-width="1.6"/>'
                 % (F.P(*q1) + F.P(q1[0] - s / math.sqrt(2), q1[1] + s / math.sqrt(2)) + F.P(*q2)))
    for p in (A, B, P, M):
        dot(F, p, 4.5)
    F.pt((0, 0), "O", "lb", 4, -4); F.lab((0, -2), "-2", "rt", -5, 3)
    F.pt(A, r"A(-1,~1)", "rb", -6, -6); F.pt(B, r"B(3,~-5)", "ct", 0, 8); F.pt(M, "M", "rt", -8, 4)
    F.lab(P, r"\mathrm{P}\left(t,~\dfrac{4}{t-1}-2\right)", "lb", 6, -6)
    F.lab((4.4, -5.4), "x+y+1=0", "lc", 6, 0)
    return F.render()


# ---------------------------------------------------------------- 유형서 633 (ⅰ) k+15<0 (ⅱ) k+15>0
def y633(c):
    f = lambda x: 5 + c / (x - 3)
    F = Frame((-1.4, 6.4), (-3.4, 12.6), 36, 18, (16, 12, 16, 12)); F.axes()
    dash(F, (1, 12.4), (1, -3.2)); dash(F, (3, 12.4), (3, -3.2)); dash(F, (-1.2, 5), (6.2, 5))
    if c < 0:
        fn(F, f, -1.3, 1); fn(F, f, 1, 3 + c / 7.4, DASH); fn(F, f, 3 - c / 8.4, 6.3, DASH)
    else:
        fn(F, f, -1.3, 1); fn(F, f, 1, 3 - c / 8.2, DASH); fn(F, f, 3 + c / 7.4, 6.3, DASH)
    odot(F, (1, f(1)))
    F.pt((0, 0), "O", "rt", -4, 4)
    F.lab((1, 0), "1", "lt", 4, 4) if c < 0 else F.lab((1, 0), "1", "lb", 4, -4)
    F.lab((3, 0), "3", "lt", 4, 4) if c < 0 else F.lab((3, 0), "3", "lb", 4, -4)
    F.lab((0, 5), "5", "rb", -5, -3)
    return F.render()


FIGS = [("c2b11_400.png", b400, 9500), ("c2b11_409.png", b409, 9500), ("c2y11_596.png", y596, 11000),
        ("c2y11_615.png", y615, 11000), ("c2y11_623.png", y623, 11000), ("c2y11_628.png", y628, 11000),
        ("c2y11_633a.png", lambda: y633(-4), 9000), ("c2y11_633b.png", lambda: y633(11), 9000)]

if __name__ == "__main__":
    for name, fnc, wd in FIGS:
        if len(sys.argv) > 1 and name not in sys.argv[1:]:
            continue
        print(name, fit_shoot(name, fnc, wd, HERE))
