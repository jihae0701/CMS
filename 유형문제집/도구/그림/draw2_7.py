# -*- coding: utf-8 -*-
"""공통수학2 7단원(명제) 유형서 해설의 벤 다이어그램, 8단원(절대부등식) 기본서 마지막 문항의 반원 그림
(2026-11-13 사용자 완성본에 붙여 넣은 스캔 그림을 그림 규칙대로 다시 그림)

- c2_7_venn_r.png  : 유형서 7단원 해설(미주 32번째) — R 안에 서로 만나지 않는 P, Q
- c2_7_venn_rq.png : 유형서 7단원 해설(미주 33번째) — R 안에 Q, P는 R과 일부만 겹침
- c2_7_venn_x.png  : 유형서 7단원 해설(미주 37번째, 두 곳) — 겹친 A, B를 가로지르는 X
- c2_7_venn_x2.png : 유형서 7단원 해설(미주 37번째) — 왼쪽 X⊂A, 오른쪽 X⊂B (두 그림 나란히)
- c2_8_semi.png    : 기본서 8단원 마지막 문항 — 지름 AB=4인 반원 위의 점 P
그림 속 이름은 원본처럼 곡선을 끊은 자리에 쓴다. 집합 이름(U, A, B, P, Q, R, X)은 원본처럼 이탤릭.
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from draw import HERE
from draw5 import Frame, fit_shoot
from draw10y import dot
from draw6 import dim_arc

CW = 3.2     # 곡선·도형 테두리 굵기(그림 규칙)
GAPPX = 15   # 이름을 넣으려고 끊는 곡선의 반쪽 길이(px)


def path(F, pts, closed=False, wd=CW):
    d = "M" + " L".join("%.1f,%.1f" % F.P(*p) for p in pts) + (" Z" if closed else "")
    F.svg.append('<path d="%s" fill="none" stroke="#000" stroke-width="%s" stroke-linejoin="round" stroke-linecap="round"/>' % (d, wd))


def ell(F, cx, cy, rx, ry, name=None, ang=90, gap=None, size=21):
    """타원(원) — ang(도) 자리를 끊고 그 자리에 이름을 쓴다"""
    n = 720
    pts = [(cx + rx * math.cos(2 * math.pi * k / n), cy + ry * math.sin(2 * math.pi * k / n)) for k in range(n + 1)]
    if name is None:
        path(F, pts)
        return
    lx, ly = cx + rx * math.cos(math.radians(ang)), cy + ry * math.sin(math.radians(ang))
    LX, LY = F.P(lx, ly)
    g = gap or GAPPX
    keep, segs = [], []
    for p in pts:
        X, Y = F.P(*p)
        if math.hypot(X - LX, Y - LY) < g:
            if keep:
                segs.append(keep); keep = []
        else:
            keep.append(p)
    if keep:
        segs.append(keep)
    if len(segs) > 1 and segs[0][0] == pts[0] and segs[-1][-1] == pts[-1]:   # 시작점을 지나는 조각은 이어 붙인다
        segs[0] = segs[-1] + segs[0]; segs.pop()
    for sg in segs:
        path(F, sg)
    F.lab((lx, ly), name, "cc", 0, 0, size)


def urect(F, x0, y0, x1, y1, r=0.35, name="U", lx=None, size=21, gap=None):
    """전체집합: 모서리가 둥근 직사각형, 위 변 왼쪽을 끊고 U"""
    lx = x0 + 0.9 if lx is None else lx
    g = (gap or GAPPX) / F.sx
    pts = [(lx + g, y1), (x1 - r, y1)]
    for k in range(1, 10):
        a = math.pi / 2 - math.pi / 2 * k / 9; pts.append((x1 - r + r * math.cos(a), y1 - r + r * math.sin(a)))
    pts.append((x1, y0 + r))
    for k in range(1, 10):
        a = 0 - math.pi / 2 * k / 9; pts.append((x1 - r + r * math.cos(a), y0 + r + r * math.sin(a)))
    pts.append((x0 + r, y0))
    for k in range(1, 10):
        a = -math.pi / 2 - math.pi / 2 * k / 9; pts.append((x0 + r + r * math.cos(a), y0 + r + r * math.sin(a)))
    pts.append((x0, y1 - r))
    for k in range(1, 10):
        a = math.pi - math.pi / 2 * k / 9; pts.append((x0 + r + r * math.cos(a), y1 - r + r * math.sin(a)))
    pts.append((lx - g, y1))
    path(F, pts, wd=CW)
    F.lab((lx, y1), name, "cc", 0, 0, size)


def frame(w=10.0, h=7.0):
    return Frame((-0.3, w + 0.3), (-0.3, h + 0.5), 40, 40, (12, 12, 12, 12))


BIG = round(21 * 1.6)   # 372·373번: 사용자 요청(2026-11-13)으로 U, P, Q, R 글씨를 1.6배
BGAP = round(GAPPX * 1.6)


def fig_venn_r():
    F = Frame((-0.3, 10.3), (-0.3, 7.6), 40, 40, (12, 22, 12, 12))
    urect(F, 0, 0, 10, 7, lx=1.0, size=BIG, gap=BGAP)
    ell(F, 5, 3.3, 4.1, 2.9, "R", 90, gap=BGAP, size=BIG)
    ell(F, 3.2, 3.3, 1.5, 1.5, "P", 100, gap=BGAP, size=BIG)
    ell(F, 6.8, 3.3, 1.5, 1.5, "Q", 95, gap=BGAP, size=BIG)
    return F.render()


def fig_venn_rq():
    F = Frame((-0.3, 10.3), (-0.3, 7.6), 40, 40, (12, 22, 12, 12))
    urect(F, 0, 0, 10, 7, lx=1.0, size=BIG, gap=BGAP)
    ell(F, 6.1, 3.4, 2.6, 2.6, "R", 90, gap=BGAP, size=BIG)
    ell(F, 6.1, 3.4, 1.35, 1.35, "Q", 90, gap=BGAP, size=BIG)
    ell(F, 2.8, 2.6, 1.55, 1.55, "P", 100, gap=BGAP, size=BIG)
    return F.render()


def fig_venn_x():
    F = frame()
    urect(F, 0, 0, 10, 7)
    ell(F, 3.8, 3.4, 2.2, 2.2, "A", 100)
    ell(F, 6.2, 3.4, 2.2, 2.2, "B", 80)
    ell(F, 5.0, 3.0, 2.25, 0.85, "X", 145, gap=19)
    return F.render()


def fig_venn_x2():
    F = Frame((-0.3, 21.3), (-0.3, 7.5), 40, 40, (12, 12, 12, 12))
    urect(F, 0, 0, 10, 7)
    ell(F, 3.8, 3.4, 2.3, 2.3, "A", 100)
    ell(F, 6.2, 3.4, 2.3, 2.3, "B", 80)
    ell(F, 3.5, 3.0, 1.45, 1.45, "X", 105)
    urect(F, 11, 0, 21, 7)
    ell(F, 14.8, 3.4, 2.3, 2.3, "A", 100)
    ell(F, 17.2, 3.4, 2.3, 2.3, "B", 80)
    ell(F, 17.5, 3.0, 1.45, 1.45, "X", 75)
    return F.render()


def fig_semi():
    F = Frame((-2.6, 2.6), (-0.9, 2.25), 70, 70, (30, 16, 30, 12))
    n = 240
    path(F, [(2 * math.cos(math.pi * k / n), 2 * math.sin(math.pi * k / n)) for k in range(n + 1)])
    A, B, O = (-2, 0), (2, 0), (0, 0)
    t = math.radians(118); P = (2 * math.cos(t), 2 * math.sin(t))
    F.seg(A, B); F.seg(A, P); F.seg(P, B)
    dot(F, O, 4)
    F.pt(A, "A", "rc", -8, 4); F.pt(B, "B", "lc", 8, 4); F.pt(O, "O", "cb", 0, -8); F.pt(P, "P", "rb", -8, -6)
    dim_arc(F, A, B, "4", 1)
    return F.render()


FIGS = (("c2_7_venn_r.png", fig_venn_r, 10000), ("c2_7_venn_rq.png", fig_venn_rq, 10000),
        ("c2_7_venn_x.png", fig_venn_x, 10000), ("c2_7_venn_x2.png", fig_venn_x2, 21000),
        ("c2_8_semi.png", fig_semi, 10000))

if __name__ == "__main__":
    for name, fn, wd in FIGS:
        if len(sys.argv) > 1 and name not in sys.argv[1:]:
            continue
        print(name, fit_shoot(name, fn, wd, HERE))
