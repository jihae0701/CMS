# -*- coding: utf-8 -*-
"""CLIMATH(c) 미적분Ⅰ 표지를 다른 CLIMATH 표지(대수·확률과 통계·공통수학)와 같은 틀로 정리 (2026-11-26).
python climath_cover_mi1.py <원본 폴더>   → <원본 폴더>/CLIMATH_c_미적분1_{앞표지,책등,뒤표지}.png (정리한 원본; 로고는 climath_cover_logo_book.py로)
- 사용자: 미적분Ⅰ 표지 3장 + '이 파일은 위의 파일과 비율 등등 다른 게 많아서 위 표지들과 통일되도록 수정해야 할 것들이 많아'.
- 잰 차이(받은 것 → 맞춘 것):
  · 앞표지 폭 1414 → 1474: 양옆에 30px씩 띠 바탕을 이어 붙임(띠는 가로로는 단색, 세로 그러데이션). 그러면 큰 CLI MATH(437~968 → 467~998), CREVERSE 가운데(706 → 736)가 대수 표지와 같은 자리.
  · 위 CLIMATH 로고: 작고(136×36) 자리가 다름(161, 128) → 지우고 대수 앞표지의 로고(143~299 × 113~153)를 같은 자리에.
  · 제목 줄: 테두리 없는 흰 줄(굵기 약 8px, x 358~1031, y 1466·1603) → 지우고 공통수학·대수와 같은 줄(흰 4.2px + 테두리 1.45px, x 455.3~1020.3, 가운데 y 1441.65·1577.65).
  · 제목 '미적분 Ⅰ'(검은 글씨, 높이 60px — 대수 '대 수' 59px와 같음): 글자 모양·크기 그대로 두 줄 사이 가운데(가로 737.8, 세로 1509.65)로 옮김(위로 약 25px).
  · 뒤표지 폭 1414 → 1474: 오른쪽 색 띠를 60px 더 이어 붙여 띠가 대수 뒤표지처럼 x 1178~1473(가운데 CREVERSE 자리 666.5도 대수와 같음).
  · 책등: 크기·자리가 다른 표지와 같아 그대로(CREVERSE만 로고 단계에서 cms로).
"""
import os, sys
import numpy as np
import cv2
from PIL import Image, ImageDraw

od = sys.argv[1]
BLACK = np.array((14.0, 16.0, 16.0))
lum = lambda a: a[..., 0] * 0.299 + a[..., 1] * 0.587 + a[..., 2] * 0.114
rd = lambda n: np.asarray(Image.open(os.path.join(od, n)).convert("RGB")).astype(float)
sv = lambda a, n: Image.fromarray(a.round().clip(0, 255).astype(np.uint8)).save(os.path.join(od, n))

# ================================================================ 앞표지
f = rd("CLIMATH_c_미적분1_앞표지_받은것.jpg")
H, W = f.shape[:2]
PADX = 30
g = np.empty((H, W + 2 * PADX, 3))
g[:, PADX:PADX + W] = f
g[:, :PADX] = np.median(f[:, 2:12], axis=1)[:, None, :]          # 왼쪽 끝 색(줄마다)을 이어 붙임
g[:, PADX + W:] = np.median(f[:, W - 12:W - 2], axis=1)[:, None, :]
f = g
# 위 CLIMATH 로고 바꾸기
d = rd("CLIMATH_c_대수_앞표지.jpg")
f[95:185, 120:360] = d[95:185, 120:360]                           # 띠(265~) 위 흰 자리: 대수 앞표지 그대로(로고 143~299 × 113~153)
# 제목 글씨 떼어 내기(검정 비율) → 지우기
TX0, TY0, TX1, TY1 = 560 + PADX, 1492, 835 + PADX, 1577
reg = f[TY0:TY1, TX0:TX1]
L = lum(reg)
dk = cv2.dilate((L < 120).astype(np.uint8) * 255, np.ones((5, 5), np.uint8))
B = cv2.inpaint(reg.clip(0, 255).astype(np.uint8), dk, 5, cv2.INPAINT_TELEA).astype(float)
dd = BLACK - B
ta = np.clip(((reg - B) * dd).sum(axis=2) / np.maximum((dd * dd).sum(axis=2), 1.0), 0, 1) * (dk > 0)
ta[ta < 0.04] = 0
# 글씨 자리 바탕: 원 아래라 줄마다 왼쪽·오른쪽 두 색뿐(가운데 세로 경계) → 글씨 바로 위 깨끗한 줄(1487)의 가로 모양을
# 줄마다 왼쪽·오른쪽 색 차이만큼 옮겨 채움(메우기(inpaint)는 경계선을 일그러뜨려서 쓰지 않음)
REF = 1487
ref = f[REF].copy()
SPLIT = 697 + PADX
for y in range(TY0, TY1):
    dl = np.median(f[y, 400:440], axis=0) - np.median(f[REF, 400:440], axis=0)
    dr = np.median(f[y, 1080:1120], axis=0) - np.median(f[REF, 1080:1120], axis=0)
    row = ref.copy()
    row[:SPLIT] += dl; row[SPLIT:] += dr
    f[y, TX0:TX1] = row[TX0:TX1]
ys, xs = np.nonzero(ta > 0.5)
gcx, gcy = TX0 + (xs.min() + xs.max()) / 2, TY0 + (ys.min() + ys.max()) / 2
print("제목 잉크", (TX0 + xs.min(), TY0 + ys.min(), TX0 + xs.max(), TY0 + ys.max()), "가운데 (%.1f, %.1f)" % (gcx, gcy))
# 옛 제목 줄 지우기: 줄 위·아래 바탕 사이를 열마다 직선 보간
for (ya, yb) in ((1458, 1476), (1594, 1613)):
    xa, xb = 350 + PADX, 1040 + PADX
    top, bot = f[ya, xa:xb].copy(), f[yb, xa:xb].copy()
    for y in range(ya + 1, yb):
        t = (y - ya) / (yb - ya)
        f[y, xa:xb] = top * (1 - t) + bot * t
# 새 제목 줄(공통수학·대수와 같은 굵기·자리)
EDGE = (45, 38, 45); T, HW = 1.45, 4.2; X0W, X1W = 455.3, 1020.3
for cy in (1441.65, 1577.65):
    y0, y1 = cy - HW / 2, cy + HW / 2
    X0, Y0 = int(X0W - T) - 2, int(y0 - T) - 2
    Wd, Hd = int(X1W + T) + 3 - X0, int(y1 + T) + 3 - Y0
    def mk(a0, b0, a1, b1):
        m = Image.new("L", (Wd * 8, Hd * 8), 0)
        ImageDraw.Draw(m).rectangle(((a0 - X0) * 8, (b0 - Y0) * 8, (a1 - X0) * 8 - 1, (b1 - Y0) * 8 - 1), fill=255)
        return np.asarray(m.resize((Wd, Hd), Image.LANCZOS)).astype(float)[..., None] / 255.0
    o, i = mk(X0W - T, y0 - T, X1W + T, y1 + T), mk(X0W, y0, X1W, y1)
    r = f[Y0:Y0 + Hd, X0:X0 + Wd]
    r = r * (1 - o) + np.array(EDGE, float) * o
    f[Y0:Y0 + Hd, X0:X0 + Wd] = r * (1 - i) + 255.0 * i
# 제목 글씨를 두 줄 사이 가운데로(반 픽셀까지)
CX, CY = (X0W + X1W) / 2, (1441.65 + 1577.65) / 2
dx, dy = CX - gcx, CY - gcy
M = np.float32([[1, 0, dx], [0, 1, dy]])
full = np.zeros(f.shape[:2], np.float32)
full[TY0:TY1, TX0:TX1] = ta
full = cv2.warpAffine(full, M, (f.shape[1], f.shape[0]), flags=cv2.INTER_LINEAR, borderValue=0)
f = f * (1 - full[..., None]) + BLACK * full[..., None]
print("제목 옮김 (%+.1f, %+.1f)" % (dx, dy))
sv(f, "CLIMATH_c_미적분1_앞표지.png")

# ================================================================ 책등(그대로)
sv(rd("CLIMATH_c_미적분1_책등_받은것.jpg"), "CLIMATH_c_미적분1_책등.png")

# ================================================================ 뒤표지: 오른쪽 띠를 60px 더
b = rd("CLIMATH_c_미적분1_뒤표지_받은것.jpg")
H, W = b.shape[:2]
g = np.empty((H, W + 60, 3))
g[:, :W] = b
g[:, W:] = np.median(b[:, W - 12:W - 2], axis=1)[:, None, :]
sv(g, "CLIMATH_c_미적분1_뒤표지.png")
print("앞 %s, 뒤 %s" % (f.shape[1::-1], g.shape[1::-1]))
