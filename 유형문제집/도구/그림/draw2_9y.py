# -*- coding: utf-8 -*-
"""공통수학2 유형서 9단원(함수) 완성본(2026-11-14)에 붙여 넣은 스캔 그림을 그림 규칙대로 다시 그림.  python draw2_9y.py [파일 ...]
- c2y9_490a.png / c2y9_490b.png : 490번 해설 f(x)=2x (|x|≥2), ax²+2x−4a (|x|≤2) — (ⅰ) a>0, (ⅱ) a<0 (개형: a=±0.35)
- c2y9_491.png : 491번 해설 f₁(x)=x²−ax+3, f₂(x)=−x²+2bx−3, x=1에서 이어짐, a/2<1<b (개형: a=1.2, b=3.4)
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from draw import HERE, STROKE
from draw5 import Frame, fit_shoot

DASH = 'stroke-dasharray="5,4"'


def pl(F, f, x0, x1, extra="", n=200):
    pts = " ".join("%.1f,%.1f" % F.P(x0 + (x1 - x0) * i / n, f(x0 + (x1 - x0) * i / n)) for i in range(n + 1))
    F.svg.append('<polyline points="%s" fill="none" stroke="#000" stroke-width="%s" stroke-linejoin="round" %s/>' % (pts, STROKE, extra))


def dash(F, p, q):
    F.seg(p, q, 1.5, DASH)


def fig490(a):
    h = lambda x: a * x * x + 2 * x - 4 * a
    F = Frame((-4.6, 4.6), (-5.6, 6.0), 30, 24, (16, 12, 18, 12))
    F.axes()
    if a > 0:
        pl(F, h, -4.4, -2, DASH); pl(F, lambda x: 2 * x, -2.7, -2); pl(F, lambda x: 2 * x, 2, 2.9)
    else:
        pl(F, h, 2, 4.4, DASH); pl(F, lambda x: 2 * x, 2, 2.9); pl(F, lambda x: 2 * x, -2.7, -2)
    pl(F, h, -2, 2)
    dash(F, (2, 4), (2, 0)); dash(F, (2, 4), (0, 4)); dash(F, (-2, -4), (-2, 0)); dash(F, (-2, -4), (0, -4))
    F.pt((0, 0), "O", "rb", -4, -4) if a > 0 else F.pt((0, 0), "O", "lt", 4, 4)
    F.lab((2, 0), "2", "ct", 0, 6)
    F.lab((-2, 0), "-2", "cb", 0, -6) if a > 0 else F.lab((-2, 0), "-2", "cb", 0, -6)
    F.lab((0, 4), "4", "rc", -6, 0); F.lab((0, -4), "-4", "lc", 6, 0)
    return F.render()


def fig491():
    A, B = 1.6, 3.2                      # f₁(1)=f₂(1) (2b=8−a), a/2<1<b
    f1 = lambda x: x * x - A * x + 3
    f2 = lambda x: -x * x + 2 * B * x - 3
    F = Frame((-0.8, 6.8), (-4.0, 10.6), 34, 13, (40, 12, 30, 24))
    F.axes()
    pl(F, f1, -0.5, 1, DASH); pl(F, f1, 1, 3.5)
    pl(F, f2, -0.1, 1); pl(F, f2, 1, 6.5, DASH)
    dash(F, (A / 2, f1(A / 2)), (A / 2, 0)); dash(F, (1, f1(1)), (1, 0)); dash(F, (B, f2(B)), (B, 0))
    F.pt((0, 0), "O", "rt", -4, 4)
    F.lab((A / 2, 0), r"\dfrac{a}{2}", "rt", -2, 6); F.lab((1, 0), "1", "lt", 4, 6); F.lab((B, 0), "b", "ct", 0, 6)
    F.lab((3.5, f1(3.5)), "y=f_{1}(x)", "lc", 10, 0); F.lab((-0.1, f2(-0.1)), "y=f_{2}(x)", "lc", 14, 4)
    return F.render()


FIGS = [("c2y9_490a.png", lambda: fig490(0.35), 10000), ("c2y9_490b.png", lambda: fig490(-0.35), 10000), ("c2y9_491.png", fig491, 10000)]

if __name__ == "__main__":
    for name, fn, wd in FIGS:
        if len(sys.argv) > 1 and name not in sys.argv[1:]:
            continue
        print(name, fit_shoot(name, fn, wd, HERE))
