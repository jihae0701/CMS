# CORE 2회 문제·해설 그림 다시 그리기 (math-figure-rules 약속)
import math, json, sys, os
from mathfig import (Frame, fit_shoot, roots, dot, right_mark, dim_arc, DASH, SKY, STROKE)


def thin(F, f, a, b, n=80):
    """비교용·정의역 밖 곡선: 점선(굵기 1.5, 5,4)"""
    pts = " ".join("%.1f,%.1f" % F.P(a + (b - a) * i / n, f(a + (b - a) * i / n)) for i in range(n + 1))
    F.svg.append('<polyline points="%s" fill="none" stroke="#000" stroke-width="1.5" %s/>' % (pts, DASH))


def arrow(F, p, q, wd=1.5):
    F.svg.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#000" stroke-width="%s" marker-end="url(#ar)"/>'
                 % (F.P(*p) + F.P(*q) + (wd,)))


# 5번: f'(x)=3x(x-2), g'(x)=2x (문제의 값 그대로)
def fig05():
    fp = lambda x: 3 * x * (x - 2)
    gp = lambda x: 2 * x
    F = Frame((-0.9, 3.6), (-3.6, 7.6), 70, 32, (14, 14, 110, 14))
    F.axes()
    F.curve(fp, roots(fp, -3, 1, 7.2)[0], roots(fp, 1, 6, 7.2)[0])
    F.seg((-0.85, gp(-0.85)), (3.4, gp(3.4)))
    F.pt((0, 0), "O", "rt", -24, 4)
    F.lab((2, 0), "2", "rt", -6, 6)
    x1 = roots(fp, 1, 6, 7.2)[0]
    F.lab((x1, 7.2), r"y=f'(x)", "rc", -10, 0)
    F.lab((3.4, gp(3.4)), r"y=g'(x)", "lc", 8, 0)
    return F.render()


# 6번: 개형 f'(x)=1.2(x-2)²+1.2, g'(x)=-(x-1.5)²+4.25 (f'(0)=6, g'(0)=2)
def fig06():
    fp = lambda x: 1.2 * (x - 2) ** 2 + 1.2
    gp = lambda x: -(x - 1.5) ** 2 + 4.25
    F = Frame((-0.8, 4.6), (-1.8, 8.6), 70, 34, (40, 14, 110, 14))
    F.axes()
    F.curve(fp, roots(fp, -2, 2, 7.2)[0], roots(fp, 2, 7, 7.2)[0])
    F.curve(gp, -0.7, roots(gp, 2, 6, -1.6)[0])
    F.pt((0, 0), "O", "rt", -6, 6)
    F.lab((0, 6), "6", "rc", -8, 0); F.lab((0, 2), "2", "rc", -8, 0)
    x1 = roots(fp, 2, 7, 7.2)[0]
    F.lab((x1, 7.2), r"y=f'(x)", "lc", 8, 0)
    x2 = roots(gp, 2, 6, -1.6)[0]
    F.lab((x2, -1.6), r"y=g'(x)", "lc", 8, 0)
    return F.render()


# 7번: 개형 g'(x)=0.9x+5, f'(x)=g'(x)+0.6(x-1)²(x-4) (b=1에서 접함, e=4)
def fig07():
    gp = lambda x: 0.9 * x + 5
    fp = lambda x: gp(x) + 0.6 * (x - 1) ** 2 * (x - 4)
    c, d = 2 - math.sqrt(0.5), 2 + math.sqrt(0.5)
    a = roots(fp, -1, 0, 0)[0]
    F = Frame((-0.9, 5.2), (-1.2, 10.4), 90, 26, (14, 14, 110, 14))
    F.axes()
    F.curve(fp, roots(fp, -1.2, 0, -1.0)[0], roots(fp, 4, 6, 10.0)[0])
    F.seg((-0.8, gp(-0.8)), (5.0, gp(5.0)))
    for v in (1, c, d, 4):
        F.dashed((v, fp(v)), (v, 0))
    F.pt((0, 0), "O", "lt", 6, 6)
    for v, s in ((a, "a"), (1, "b"), (c, "c"), (d, "d"), (4, "e")):
        F.lab((v, 0), s, "ct", 0, 8)
    x1 = roots(fp, 4, 6, 10.0)[0]
    F.lab((x1, 10.0), r"y=f'(x)", "rc", -10, 0)
    F.lab((5.0, gp(5.0)), r"y=g'(x)", "lc", 8, 0)
    return F.render()


# 20번: 바닥·경사면·공(그림 약속에 맞춘 모식도, 길이는 비율대로가 아님)
def fig20():
    F = Frame((-0.6, 12.0), (-2.6, 3.2), 46, 46, (14, 14, 14, 14))
    B, top = (8, 0), (10.8, 2.8 * math.tan(math.radians(30)))
    F.poly([(-0.5, 0), (11.8, 0), (11.8, -0.3), (-0.5, -0.3)], SKY)
    F.poly([(10.8, 0), (11.8, 0), (11.8, 3.0), (10.8, 3.0)], SKY)
    F.seg((-0.5, 0), (10.8, 0)); F.seg((-0.5, -0.3), (11.8, -0.3))
    F.seg((10.8, 0), (10.8, 3.0)); F.seg((10.8, 3.0), (11.8, 3.0)); F.seg((11.8, 3.0), (11.8, -0.3))
    F.seg(B, top)
    r = 0.7
    cx = (1, r)
    X, Y = F.P(*cx)
    F.svg.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="#000" stroke-width="%s"/>' % (X, Y, r * F.sx, STROKE))
    dot(F, cx)
    F.seg(cx, (1 + r * math.cos(math.radians(30)), r + r * math.sin(math.radians(30))))
    F.lab((1 + r, r + 0.35), r"\dfrac{1}{5}\,\mathrm{m}", "lb", 10, 0)
    arrow(F, (2.0, 0.35), (3.0, 0.35))
    dot(F, (1, 0)); dot(F, B)
    F.pt((1, 0), "A", "rt", -8, 18)
    F.pt(B, "B", "lt", 8, 18)
    dim_arc(F, (1, 0), B, "0000000", 1, 30)          # 끊는 길이는 보이는 글자 폭(약 7자)으로 잡고
    F.labels[-1] = F.labels[-1][:2] + (r"\dfrac{50-\sqrt{3}}{5}\,\mathrm{m}",) + F.labels[-1][3:]   # 실제 글자로 바꾼다
    # 30° 표시
    R = 0.75
    pts = [(8 + R * math.cos(math.radians(a)), R * math.sin(math.radians(a))) for a in range(0, 31, 3)]
    F.svg.append('<polyline points="%s" fill="none" stroke="#000" stroke-width="1.5"/>' % " ".join("%.1f,%.1f" % F.P(*p) for p in pts))
    F.lab((9.3, 0), r"30^{\circ}", "lb", 0, -3)
    return F.render()


# 34번 정답 (2): y=f(x)와 직선 y=3x
def fig34():
    f = lambda x: -6 * (x - 1) ** 2 + 6 if x < 1.5 else 6 * (x - 1) ** 2 + 3
    F = Frame((-0.7, 2.6), (-2.2, 10.0), 110, 34, (40, 14, 100, 14))
    F.axes()
    F.curve(lambda x: -6 * (x - 1) ** 2 + 6, roots(lambda x: -6 * (x - 1) ** 2 + 6, -1, 1, -2.0)[0], 1.5)
    F.curve(lambda x: 6 * (x - 1) ** 2 + 3, 1.5, roots(lambda x: 6 * (x - 1) ** 2 + 3, 1.5, 4, 9.6)[0])
    F.seg((-0.6, -1.8), (2.5, 7.5))
    F.dashed((0, 6), (1, 6)); F.dashed((1, 6), (1, 0))
    F.dashed((0, 4.5), (1.5, 4.5)); F.dashed((1.5, 4.5), (1.5, 0))
    F.pt((0, 0), "O", "lt", 6, 6)
    F.lab((0, 6), "6", "rc", -8, 0); F.lab((0, 4.5), r"\dfrac{9}{2}", "rc", -8, 0)
    F.lab((1, 0), "1", "ct", 0, 8); F.lab((1.5, 0), r"\dfrac{3}{2}", "ct", 0, 8)
    x1 = roots(lambda x: 6 * (x - 1) ** 2 + 3, 1.5, 4, 9.6)[0]
    F.lab((x1, 9.6), r"y=f(x)", "lc", 8, 0)
    F.lab((2.5, 7.5), r"y=3x", "lc", 8, 0)
    return F.render()


# 36번: 개형 f(x)=x³/4+3x/2 (f(2)=5, ∫₀²f=4), 색칠은 ∫₀²f
def fig36():
    f = lambda x: 0.25 * x ** 3 + 1.5 * x
    F = Frame((-2.9, 3.2), (-6.0, 6.6), 52, 26, (40, 14, 110, 14))
    F.poly([(0, 0)] + [(2 * i / 60, f(2 * i / 60)) for i in range(61)] + [(2, 0)], SKY)
    F.axes()
    F.curve(f, -2, 2)
    F.dashed((0, 5), (2, 5)); F.dashed((2, 5), (2, 0))
    F.dashed((0, -5), (-2, -5)); F.dashed((-2, -5), (-2, 0))
    F.pt((0, 0), "O", "lt", 6, 6)
    F.lab((0, 5), "5", "rc", -8, 0); F.lab((0, -5), "-5", "lc", 8, 0)
    F.lab((2, 0), "2", "lt", 6, 6); F.lab((-2, 0), "-2", "cb", 0, -8)
    F.lab((2, 5), r"y=f(x)", "lc", 10, 0)
    return F.render()


# 46번: 개형 k=2.5 (답 k=3과 다른 값)
def fig46():
    k = 2.5
    y = lambda x: (x - 1) * (x - k)
    F = Frame((-0.8, 4.6), (-1.0, 5.2), 70, 84, (14, 14, 250, 34))
    F.poly([(1 + (k - 1) * i / 60, y(1 + (k - 1) * i / 60)) for i in range(61)], SKY)
    F.poly([(k, 0)] + [(k + i / 60, y(k + i / 60)) for i in range(61)] + [(k + 1, 0)], SKY)
    F.axes()
    F.curve(y, roots(y, -2, 1, 4.6)[0], roots(y, 2, 6, 4.6)[0])
    F.seg((k + 1, -1.1), (k + 1, 5.0))
    F.pt((0, 0), "O", "rt", -6, 6)
    F.lab((1, 0), "1", "rt", -6, 6)
    F.lab((k, 0), "k", "lt", 6, 6)
    F.pt((1.75, -0.27), "A", "cc", 0, 0)
    F.pt((3.25, 0.7), "B", "cc", 0, 0)
    x1 = roots(y, 2, 6, 4.6)[0]
    F.lab((x1, 4.6), r"y=(x-1)(x-k)", "lc", 10, 0)
    F.lab((k + 1, -1.1), r"x=k+1", "lc", 8, 0)
    return F.render()


# 10번 해설: f(x)=(x+1/2)²(x-5/2)²+1 과 직선 y=1 (색 선을 검은 선으로)
def fig10s():
    Y = lambda x: (x + 0.5) ** 2 * (x - 2.5) ** 2
    F = Frame((-1.6, 3.8), (-0.9, 7.2), 80, 34, (14, 14, 40, 14))
    F.seg((-1.5, 0), (3.5, 0), 2.0)
    F.curve(Y, roots(Y, -3, -0.5, 6.4)[0], roots(Y, 2.5, 5, 6.4)[0])
    F.dashed((1, Y(1)), (1, 0))
    F.lab((3.5, 0), "1", "lc", 8, 0)
    F.lab((-0.5, 0), "k", "ct", 0, 8); F.lab((1, 0), "1", "ct", 0, 8); F.lab((2.5, 0), "k+3", "ct", 0, 8)
    F.lab((1, Y(1)), r"y=f(x)", "cb", 0, -10)
    return F.render()


# 39번 해설: a<0일 때 y=f(x) (개형 a=-3), M=3+√2
def fig39s():
    a = -3
    M = 3 + math.sqrt(2)
    F = Frame((-2.0, 5.4), (-4.7, 4.1), 64, 40, (40, 14, 14, 14))
    F.axes()
    F.curve(lambda x: -x * x + 1, -1.75, 1)
    F.polyline([(1, 0), (2, -a), (M, a * (M - 2) - a)])
    F.seg((M, 0), (M, a * (M - 2) - a), 2.0)
    F.dashed((0, -a), (2, -a)); F.dashed((2, -a), (2, 0))
    F.pt((0, 0), "O", "rt", -6, 6)
    F.lab((0, -a), "-a", "rc", -8, 0); F.lab((0, 1), "1", "rb", -6, -4)
    F.lab((-1, 0), "-1", "rb", -4, -6)
    F.lab((1, 0), "1", "lt", 4, 6); F.lab((2, 0), "2", "ct", 8, 6); F.lab((3, 0), "3", "rt", -6, 6)
    F.lab((M, 0), "M", "cb", 0, -8)
    F.lab((2, -a), r"y=f(x)", "lb", 10, 0)
    return F.render()


FIGS = {"image2": ("fig05.png", fig05), "image4": ("fig06.png", fig06), "image6": ("fig07.png", fig07),
        "image8": ("fig20.png", fig20), "image1": ("fig34.png", fig34), "image9": ("fig36.png", fig36),
        "image10": ("fig46.png", fig46), "image13": ("fig10s.png", fig10s), "image11": ("fig39s.png", fig39s)}

if __name__ == "__main__":
    only = sys.argv[1:]
    widths = json.load(open("widths.json")) if os.path.exists("widths.json") else {}
    for k, (fn, f) in FIGS.items():
        if only and k not in only:
            continue
        widths[k] = fit_shoot(fn, f)
    json.dump(widths, open("widths.json", "w"), indent=1)
    print(widths)
