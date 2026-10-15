# -*- coding: utf-8 -*-
"""기본서 12단원(행렬) 그림. python 그림/draw12.py [파일 ...]  (KATEX_DIR 필요)
- g12_store.png: 06 대표문제 — [표1] 두 편의점의 삼각김밥·컵라면 가격, [표2] 철수·영희가 살 개수
- g12_burger.png: 06 유제 — [표1] 7월·8월 판매 개수, [표2] 두 가게의 개당 가격
- g12_school.png: STEP 3 — <표1> 두 학교의 학년별 학생 수, <표2> 학년별 활동 비율
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from draw import HERE
from draw5 import fit_shoot
from draw6 import geo
from draw10 import poly_line, text


def cell_text(F, p, t):
    """t가 $…$이면 수식, 아니면 글"""
    if t.startswith("$") and t.endswith("$") and t.count("$") == 2:
        F.lab(p, t.strip("$"), "cc")
    else:
        text(F, p, t)


def table(F, x0, top, cw, rh, rows, unit, cap, corner=None):
    """왼쪽 위 (x0, top), 열 너비 cw, 행 높이 rh. rows[0]은 머리 행, 각 행의 첫 칸은 머리 열.
    corner=(위 오른쪽 글, 아래 왼쪽 글)이면 머리 행을 높이고 첫 칸에 대각선을 그어 두 글을 나눠 넣는다."""
    hs = [1.1 if corner else rh] + [rh] * (len(rows) - 1)
    ys = [top]
    for h in hs:
        ys.append(ys[-1] - h)
    W = sum(cw)
    poly_line(F, [(x0, top), (x0 + W, top), (x0 + W, ys[-1]), (x0, ys[-1])])
    x = x0
    for w in cw[:-1]:
        x += w
        F.seg((x, top), (x, ys[-1]))
    for y in ys[1:-1]:
        F.seg((x0, y), (x0 + W, y))
    for r, row in enumerate(rows):
        x = x0
        for c, t in enumerate(row):
            if t:
                cell_text(F, (x + cw[c] / 2, (ys[r] + ys[r + 1]) / 2), t)
            x += cw[c]
    if corner:
        h = hs[0]
        F.seg((x0, top), (x0 + cw[0], top - h))
        text(F, (x0 + cw[0] * 0.8, top - h * 0.27), corner[0])
        text(F, (x0 + cw[0] * 0.2, top - h * 0.73), corner[1])
    text(F, (x0 + W, top + 0.42), unit, "rc")
    text(F, (x0 + W / 2, ys[-1] - 0.4), cap)


def two(t1, t2):
    """표 두 개를 위아래로 놓는다. t = (열 너비, 행, 단위, 표 이름, 대각선 머리)"""
    F = geo((-0.1, 7.1), (-0.25, 7.55 if t1[4] else 6.65), 72, (8, 8, 8, 8))
    for top, (cw, rows, unit, cap, corner) in (((6.95 if t1[4] else 6.0), t1), ((3.15 if t1[4] else 2.75), t2)):
        table(F, 0, top, cw, 0.6, rows, unit, cap, corner)
    return F.render()


CW = [2.8, 2.1, 2.1]


def fig_store():
    return two((CW, [["", "삼각김밥", "컵라면"], ["편의점 $\\mathrm{P}$", "$3000$", "$1200$"], ["편의점 $\\mathrm{Q}$", "$3500$", "$1000$"]],
                "(단위: 원)", "[표1]", None),
               (CW, [["", "철수", "영희"], ["삼각김밥", "$3$", "$3$"], ["컵라면", "$4$", "$5$"]],
                "(단위: 개)", "[표2]", None))


def fig_burger():
    return two((CW, [["", "불고기버거", "새우버거"], ["$7$월", "$450$", "$350$"], ["$8$월", "$400$", "$500$"]],
                "(단위: 개)", "[표1]", None),
               (CW, [["", "가게 $\\mathrm{P}$", "가게 $\\mathrm{Q}$"], ["불고기버거", "$8000$", "$9000$"], ["새우버거", "$10000$", "$12000$"]],
                "(단위: 원)", "[표2]", None))


def fig_school():
    return two((CW, [["", "$1$학년", "$2$학년"], ["$\\mathrm{A}$", "$220$", "$210$"], ["$\\mathrm{B}$", "$250$", "$230$"]],
                "(단위: 명)", "<표1>", ("학년", "학교")),
               (CW, [["", "농구", "탁구"], ["$1$학년", "$40$", "$60$"], ["$2$학년", "$50$", "$50$"]],
                "(단위: \\%)", "<표2>", ("활동", "학년")))


FIGS = (("g12_store.png", fig_store, 10000), ("g12_burger.png", fig_burger, 10000),
        ("g12_school.png", fig_school, 10000))

if __name__ == "__main__":
    for name, fn, wd in FIGS:
        if len(sys.argv) > 1 and name not in sys.argv[1:]:
            continue
        fit_shoot(name, fn, wd, HERE)
