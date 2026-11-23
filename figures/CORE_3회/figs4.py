# 고2 2학기 CORE 3회 문제·해설 그림 다시 그리기 (math-figure-rules 약속)
import math, json, sys, os
import mathfig
from mathfig import (Frame, fit_shoot, roots, dot, right_mark, dim_arc, DASH, SKY, STROKE, page)

GAP_PANEL = 36


def panels(frames):
    svg, labels, x = [], [], 0
    h = max(F.h for F in frames)
    for F in frames:
        svg.append('<g transform="translate(%.1f,0)">%s</g>' % (x, "".join(F.svg)))
        labels += [(l[0] + x,) + tuple(l[1:]) for l in F.labels]
        x += F.w + GAP_PANEL
    w = int(x - GAP_PANEL)
    s = '<svg width="%d" height="%d" style="position:absolute;left:0;top:0">%s</svg>' % (w, h, "".join(svg))
    return page(s, labels, w, h), w, h


def arrow(F, p, q, wd=1.5):
    F.svg.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#000" stroke-width="%s" marker-end="url(#ar)"/>'
                 % (F.P(*p) + F.P(*q) + (wd,)))


# 5번: f(x)=x^3-6x^2+9x+6 (극대 (1, 10), 극소 (3, 6): 문제의 값), 세로 1/4 축소
def fig05():
    f = lambda x: (x ** 3 - 6 * x ** 2 + 9 * x + 6) / 5
    F = Frame((-0.8, 4.7), (-0.6, 3.0), 64, 64, (14, 14, 14, 14))
    F.axes()
    F.curve(f, roots(f, -1, 0, -0.55)[0], roots(f, 3.2, 5, 2.85)[0])
    F.dashed((1, f(1)), (1, 0)); F.dashed((3, f(3)), (3, 0))
    F.pt((0, 0), "O", "rt", -6, 6)
    F.lab((1, 0), "1", "ct", 0, 8); F.lab((3, 0), "3", "ct", 0, 8)
    F.lab((4.25, f(4.25)), r"y=f(x)", "rc", -10, 0)
    return F.render()


# 9번: y=|x(x-2)(x-4)| (문제의 식 그대로)
def fig09():
    f = lambda x: abs(x * (x - 2) * (x - 4))
    F = Frame((-1.3, 5.4), (-1.0, 5.0), 52, 40, (14, 14, 14, 14))
    F.axes()
    a = roots(lambda x: f(x) - 5.0, -1.2, -0.01, 0)[0]
    b = roots(lambda x: f(x) - 5.0, 4.01, 5.3, 0)[0]
    F.curve(f, a, b)
    F.pt((0, 0), "O", "rt", -6, 6)
    F.lab((2, 0), "2", "ct", 0, 8); F.lab((4, 0), "4", "ct", -4, 8)
    F.lab((2, 4.6), r"y=|x(x-2)(x-4)|", "cc")
    return F.render()


# 20번: y=(x+1)f'(x)=0.25(x+1)^3(x-2) (개형: 계수 0.25)
def fig20():
    g = lambda x: 0.25 * (x + 1) ** 3 * (x - 2)
    F = Frame((-2.6, 3.0), (-2.6, 2.8), 60, 60, (14, 14, 200, 14))
    F.axes()
    F.curve(g, roots(g, -3, -1.1, 2.5)[0], roots(g, 2.01, 3, 2.5)[0])
    F.pt((0, 0), "O", "lt", 6, 6)
    F.lab((-1, 0), "-1", "ct", 0, 10); F.lab((2, 0), "2", "rt", -6, 8)
    F.lab((2.36, 1.3), r"y=(x+1)f'(x)", "lc", 12, 0)
    return F.render()


# 21번 해설: f(x)=(x+4)(x-k)^2의 두 가지 개형 (x축만)
def fig21s():
    def one(f, xr, labs):
        F = Frame(xr, (-2.2, 1.9), 48, 48, (14, 14, 14, 14))
        F.xaxis(xr[0], xr[1])
        F.curve(f, roots(f, xr[0], xr[0] + 1.2, -1.9)[0], roots(f, xr[1] - 1.5, xr[1], 1.8)[0])
        for p, s, anc, dx, dy in labs:
            F.lab(p, s, anc, dx, dy)
        return F
    a = one(lambda x: 0.32 * x * x * (x - 3), (-1.2, 4.0),
            [((0, 0), "k", "cb", 0, -10), ((3, 0), "-4", "lb", 8, -6), ((1.2, 1.5), r"y=f(x)", "cc", 0, 0)])
    b = one(lambda x: 0.32 * x * (x - 3) ** 2, (-0.8, 4.4),
            [((0, 0), "-4", "lt", 8, 6), ((3, 0), "k", "ct", 0, 10), ((1.7, 1.5), r"y=f(x)", "cc", 0, 0)])
    return panels([a, b])


# 22번 해설: f(x)=x(x-a)^2 (개형 a=2.4)와 g(t). g는 실선, f의 나머지 부분은 점선
def fig22s():
    A = 2.4
    f = lambda x: 0.45 * x * (x - A) ** 2
    F = Frame((-0.9, 4.2), (-0.9, 3.2), 56, 56, (14, 14, 14, 14))
    F.xaxis(-0.9, 4.2, r"x\,(t)")
    F.curve(f, roots(f, -1, 0, -0.85)[0], 0)
    F.polyline([(0, 0), (A, 0)])
    F.curve(f, A, roots(f, A, 4, 3.0)[0])
    pts = " ".join("%.1f,%.1f" % F.P(A * i / 80, f(A * i / 80)) for i in range(81))
    F.svg.append('<polyline points="%s" fill="none" stroke="#000" stroke-width="1.5" %s/>' % (pts, DASH))
    F.pt((0, 0), "O", "lt", 8, 6)
    F.lab((A, 0), "a", "ct", 0, 10)
    F.lab((0.8, f(0.8)), r"y=f(x)", "cb", 0, -10)
    F.lab((roots(f, A, 4, 3.0)[0], 3.0), r"y=g(t)", "rc", -10, 0)
    return F.render()


# 26번: 밑면 한 변 10 cm, 높이 20 cm인 거꾸로 선 정사각뿔 그릇과 물 (빗각 투영, 수면 높이는 개형)
def fig26():
    k, ang = 0.45, math.radians(35)
    def P3(x, y, z):          # x: 오른쪽, y: 안쪽, z: 위
        return (x + k * y * math.cos(ang), z + k * y * math.sin(ang))
    H, s = 20.0, 10.0
    top = [P3(-s / 2, -s / 2, H), P3(s / 2, -s / 2, H), P3(s / 2, s / 2, H), P3(-s / 2, s / 2, H)]
    apex = P3(0, 0, 0)
    h = 11.0; r = s / 2 * h / H
    wat = [P3(-r, -r, h), P3(r, -r, h), P3(r, r, h), P3(-r, r, h)]
    F = Frame((-11.0, 8.0), (-1.0, 26.5), 15, 15, (14, 14, 14, 14))
    F.poly([apex, wat[1], wat[2], wat[3], wat[0]], SKY)
    for i in range(4):
        F.seg(top[i], top[(i + 1) % 4])
    for i in (0, 1, 2):
        F.seg(top[i], apex)
    F.dashed(top[3], apex)
    F.seg(wat[0], wat[1]); F.seg(wat[1], wat[2])
    F.dashed(wat[2], wat[3]); F.dashed(wat[3], wat[0])
    c = P3(0, 0, H)
    F.dashed(c, apex)
    dim_arc(F, top[3], top[2], "00000", -1, 26)          # 끊는 길이는 보이는 글자 폭으로 잡고
    F.labels[-1] = F.labels[-1][:2] + (r"10\,\mathrm{cm}",) + F.labels[-1][3:]   # 실제 글자로 바꾼다
    F.lab((-6.6, 6.0), r"20\,\mathrm{cm}", "rc", 0, 0)
    F.leader((-6.3, 6.0), (0, 8.0))
    return F.render()



# 42번: y=2-|x|/2와 x축으로 둘러싸인 삼각형, x=t-1, x=t+1 사이 (개형 t=0.6)
def fig42():
    t = 0.6
    h = lambda x: 2 - abs(x) / 2
    F = Frame((-5.0, 5.2), (-0.9, 3.4), 50, 50, (14, 14, 14, 14))
    F.poly([(t - 1, 0), (t - 1, h(t - 1)), (0, 2), (t + 1, h(t + 1)), (t + 1, 0)], SKY)
    F.axes()
    F.polyline([(-4, 0), (0, 2), (4, 0)])
    F.seg((t - 1, 0), (t - 1, h(t - 1))); F.seg((t + 1, 0), (t + 1, h(t + 1)))
    F.pt((0, 0), "O", "rt", -6, 6)
    F.lab((-4, 0), "-4", "ct", 0, 8); F.lab((4, 0), "4", "ct", 0, 8)
    F.lab((t - 1, 0), "t-1", "rt", -4, 8); F.lab((t + 1, 0), "t+1", "lt", 4, 8)
    F.lab((0, 2), "2", "rb", -8, -6)
    F.lab((t + 0.3, 0.6), "f(t)", "cc")
    return F.render()


# 50번: 길이 25 m인 선분 AB, 점 P(등속 u), 점 Q(왕복)
def fig50():
    F = Frame((-1.5, 26.5), (-6.0, 5.2), 15, 15, (14, 14, 14, 14))
    A, B = (0, 0), (25, 0)
    F.seg(A, B)
    F.seg((0, -0.6), (0, 0.6)); F.seg((25, -0.6), (25, 0.6))
    F.pt(A, "A", "ct", 0, 14); F.pt(B, "B", "ct", 0, 14)
    F.pt((3.2, 2.6), "P", "rc", 0, 0)
    arrow(F, (4.0, 2.6), (8.0, 2.6), 2.0)
    F.lab((8.6, 2.6), r"u\,\mathrm{(m/sec)}", "lc")
    # Q: B 쪽에서 A 쪽으로 가다가 되돌아오는 화살표
    X0, Y0 = F.P(20.0, 2.2); X1, Y1 = F.P(15.5, 2.2); X2, Y2 = F.P(15.5, -2.2); X3, Y3 = F.P(20.0, -2.2)
    F.svg.append('<path d="M%.1f,%.1f L%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f L%.1f,%.1f" fill="none" stroke="#000" stroke-width="2.0" marker-end="url(#ar)"/>'
                 % (X0, Y0, X1, Y1, X1 - 45, Y1, X2 - 45, Y2, X2, Y2, X3, Y3))
    F.pt((20.6, 2.2), "Q", "lc", 0, 0)
    dim_arc(F, A, B, "0000", 1, 26)
    F.labels[-1] = F.labels[-1][:2] + (r"25\,\mathrm{m}",) + F.labels[-1][3:]
    return F.render()


FIGS = {"image3": ("fig05.png", fig05), "image4": ("fig09.png", fig09), "image5": ("fig20.png", fig20),
        "image7": ("fig21s.png", fig21s, 18000), "image8": ("fig22s.png", fig22s), "image9": ("fig26.png", fig26),
        "image10": ("fig42.png", fig42), "image11": ("fig50.png", fig50)}

if __name__ == "__main__":
    only = sys.argv[1:]
    widths = json.load(open("widths.json")) if os.path.exists("widths.json") else {}
    for key, v in FIGS.items():
        if only and key not in only:
            continue
        widths[key] = fit_shoot(v[0], v[1], v[2]) if len(v) > 2 else fit_shoot(v[0], v[1])
    json.dump(widths, open("widths.json", "w"), indent=1)
    print(widths)
