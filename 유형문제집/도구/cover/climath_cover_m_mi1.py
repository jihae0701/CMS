# -*- coding: utf-8 -*-
"""CLIMATH(m) 미적분Ⅰ 표지를 다른 CLIMATH 표지와 같은 틀로 정리 (2026-11-26).
python climath_cover_m_mi1.py <원본 폴더>   → <원본 폴더>/CLIMATH_m_미적분1_{앞표지,책등,뒤표지}.png (정리한 원본; 로고는 climath_cover_logo_book.py로)
- 사용자: CLIMATH(m) 미적분Ⅰ 표지 3장(파란 바탕, 흰 테두리 검은 글자, 흰 ⓜ, 흰 제목) + '이것도 수정'. (c) 미적분Ⅰ과 같은 차이를 같은 방법으로 맞춤:
  · 앞표지 폭 1414 → 1474(양옆 30px씩 띠 바탕 이어 붙임) → 큰 CLI MATH 467~985·CREVERSE 자리가 다른 표지와 같아짐.
  · 위 CLIMATH 로고(136×36 at 161,124) → 대수 앞표지 로고(143~299 × 113~153).
  · 띠 높이: 앞 253~1666, 책등·뒤 264~1676로 서로 달랐음 → 모두 264~1665(확률과 통계·미적분Ⅰ(c)와 같음; 넘친 줄은 흰 종이로).
  · 제목 줄(테두리 없는 흰 줄 약 8px, x 357~1031, y 1426·1562) → 공통수학·대수와 같은 줄(흰 4.2px + 테두리, x 455~1020, 가운데 y 1441.65·1577.65).
  · 제목 '미적분 Ⅰ'(흰 글씨, 높이 60px) 모양·크기 그대로 두 줄 사이 가운데(737.8, 1509.65)로 옮김. 지운 자리는 줄마다 평평한 파랑으로 채움.
  · 뒤표지 폭 1414 → 1474(오른쪽 띠 60px 이어 붙여 띠 x 1178~1473).
  · 옛 아래 제목 줄 밑을 지나가던 왼쪽 아래 가는 원호는 원에 맞춰(가운데 540.4, 1292.5, 반지름 303.1) 전체를 지우고 한 번에 다시 그림(이음매 없게).
"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw

od = sys.argv[1]
WHITE = np.array((252.0, 252.0, 252.0))
rd = lambda n: np.asarray(Image.open(os.path.join(od, n)).convert("RGB")).astype(float)
sv = lambda a, n: Image.fromarray(a.round().clip(0, 255).astype(np.uint8)).save(os.path.join(od, n))
BY0, BY1 = 264, 1666

# ================================================================ 앞표지
f = rd("CLIMATH_m_미적분1_앞표지_받은것.jpg")
H, W = f.shape[:2]
PADX = 30
g = np.empty((H, W + 2 * PADX, 3))
g[:, PADX:PADX + W] = f
g[:, :PADX] = np.median(f[:, 2:12], axis=1)[:, None, :]
g[:, PADX + W:] = np.median(f[:, W - 12:W - 2], axis=1)[:, None, :]
f = g
f[240:BY0] = 254.0                                           # 띠 위쪽 넘친 줄(253~263) → 흰 종이
f[BY1:1690] = np.where((f[BY1:1690].min(axis=2, keepdims=True) > 200), f[BY1:1690], 254.0)
d = rd("CLIMATH_c_대수_앞표지.jpg")
f[95:185, 120:360] = d[95:185, 120:360]                      # 위 CLIMATH 로고
# 제목(흰 글씨) 떼어 내기: 바탕은 평평한 파랑(줄마다 x 1100~1200 색)
TX0, TY0, TX1, TY1 = 560 + PADX, 1452, 835 + PADX, 1535
bgrow = np.median(f[TY0:TY1, 1100:1200], axis=1)            # 줄마다 바탕
reg = f[TY0:TY1, TX0:TX1]
B = np.repeat(bgrow[:, None, :], TX1 - TX0, axis=1)
dd = WHITE - B
ta = np.clip(((reg - B) * dd).sum(axis=2) / np.maximum((dd * dd).sum(axis=2), 1.0), 0, 1)
ta[ta < 0.06] = 0
f[TY0:TY1, TX0:TX1] = B
ys, xs = np.nonzero(ta > 0.5)
gcx, gcy = TX0 + (xs.min() + xs.max()) / 2, TY0 + (ys.min() + ys.max()) / 2
print("제목 잉크", (TX0 + xs.min(), TY0 + ys.min(), TX0 + xs.max(), TY0 + ys.max()), "가운데 (%.1f, %.1f)" % (gcx, gcy))
# 옛 제목 줄 지우기: 그 자리 바탕은 평평한 파랑이라 줄마다 오른쪽(x 1100~1200) 바탕색으로 채움
# (위·아래 줄 사이 보간은 지나가는 원호를 세로로 번지게 해서 쓰지 않음; 원호는 아래에서 다시 그림)
for (ya, yb) in ((1416, 1436), (1552, 1572)):
    xa, xb = 350 + PADX, 1040 + PADX
    f[ya + 1:yb, xa:xb] = np.median(f[ya + 1:yb, 1100:1200], axis=1)[:, None, :]
# 왼쪽 아래 가는 원호: 옛 아래 줄 밑을 지나가서 줄을 지우면 끊김 → 원호 전체를 지우고(가는 선만 메우기) 같은 원으로 처음부터 끝까지 한 번에 다시 그림
# (2026-11-26 사용자 '원호 지워졌다가 다시 그린 부분이 끊어진 것처럼 보여' — 구간만 다시 그리면 이음매가 남음).
# 원 = 받은 그림의 가는 흰 선 화소 1219개에 맞춘 원: 가운데 (540.39, 1292.52)(받은 그림 좌표), 반지름 303.08. 원호 = 원의 왼쪽, y 1008~1594, 끝 x ≤ 527.
import cv2
ACX, ACY, AR, AW = 540.39 + PADX, 1292.52, 303.08, 1.2
AY0, AY1, AXMAX = 1004, 1598, 526 + PADX            # 아래 꼬리 끝 x 525(받은 그림)
TOPX = 440 + PADX                                           # 위 끝은 M 글자 흰 테두리(x 441~)에서 멈춤 — 테두리는 건드리지 않음
gy, gx = np.mgrid[AY0:AY1, int(ACX - AR) - 4:AXMAX]
on_arc = (gx < ACX) | (gy > ACY)                             # 원의 왼쪽 반(아래 꼬리는 x ≤ 527까지)
dist = np.abs(np.hypot(gx - ACX, gy - ACY) - AR)
X0A = int(ACX - AR) - 4
mask = np.zeros(f.shape[:2], np.uint8)
keep = ~((gx >= TOPX) & (gy < 1100))
mask[AY0:AY1, X0A:AXMAX] = ((dist <= 3.5) & on_arc & keep).astype(np.uint8) * 255      # 꼬리가 맞춘 원에서 2px쯤 벗어나 넉넉히
f = cv2.inpaint(f.clip(0, 255).astype(np.uint8), mask, 3, cv2.INPAINT_TELEA).astype(float)
S8 = 8
yy, xx = np.mgrid[AY0 * S8:AY1 * S8, X0A * S8:AXMAX * S8] / S8 + 0.5 / S8
ring = ((np.abs(np.hypot(xx - ACX, yy - ACY) - AR) <= AW / 2) & ((xx < ACX) | (yy > ACY)) & ~((xx >= TOPX) & (yy < 1100))).astype(np.float32)
ring = ring.reshape(AY1 - AY0, S8, AXMAX - X0A, S8).mean(axis=(1, 3))[..., None]
f[AY0:AY1, X0A:AXMAX] = f[AY0:AY1, X0A:AXMAX] * (1 - ring) + np.array((250.0, 253.0, 255.0)) * ring
# 새 제목 줄
EDGE = (45, 38, 45); T, HW = 1.45, 4.2; X0W, X1W = 455.3, 1020.3
for cy in (1441.65, 1577.65):
    y0, y1 = cy - HW / 2, cy + HW / 2
    X0, Y0 = int(X0W - T) - 2, int(y0 - T) - 2
    Wd, Hd = int(X1W + T) + 3 - X0, int(y1 + T) + 3 - Y0
    def mk(a0, b0, a1, b1):
        m = Image.new("L", (Wd * 8, Hd * 8), 0)
        # 2026-11-26 사용자 '미적분 글씨 위아래 선 검정 테두리 끝부분이 둥근 느낌이 나게': 양 끝을 반원(모서리 반지름 = 높이의 반)으로
        ImageDraw.Draw(m).rounded_rectangle(((a0 - X0) * 8, (b0 - Y0) * 8, (a1 - X0) * 8 - 1, (b1 - Y0) * 8 - 1), radius=(b1 - b0) * 8 / 2, fill=255)
        return np.asarray(m.resize((Wd, Hd), Image.LANCZOS)).astype(float)[..., None] / 255.0
    o, i = mk(X0W - T, y0 - T, X1W + T, y1 + T), mk(X0W, y0, X1W, y1)
    r = f[Y0:Y0 + Hd, X0:X0 + Wd]
    r = r * (1 - o) + np.array(EDGE, float) * o
    f[Y0:Y0 + Hd, X0:X0 + Wd] = r * (1 - i) + 255.0 * i
# 제목을 두 줄 사이 가운데로(반 픽셀까지)
import cv2
CX, CY = (X0W + X1W) / 2, (1441.65 + 1577.65) / 2
dx, dy = CX - gcx, CY - gcy
full = np.zeros(f.shape[:2], np.float32)
full[TY0:TY1, TX0:TX1] = ta
full = cv2.warpAffine(full, np.float32([[1, 0, dx], [0, 1, dy]]), (f.shape[1], f.shape[0]), flags=cv2.INTER_LINEAR, borderValue=0)
# 2026-11-26 사용자 '앞표지 미적분1 검은 테두리 만들기': 흰 글씨 둘레에 검은 테두리 2px((m) 공통수학 제목과 같은 두께) — 4배 세분 표본으로 넓힌 모양
S4 = 4
big = cv2.resize(full, (full.shape[1] * S4, full.shape[0] * S4), interpolation=cv2.INTER_LINEAR)
ol = cv2.dilate((big > 0.5).astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * 2 * S4 + 1, 2 * 2 * S4 + 1)))
ol = cv2.resize(ol.astype(np.float32), (full.shape[1], full.shape[0]), interpolation=cv2.INTER_AREA)
f = f * (1 - ol[..., None]) + np.array((14.0, 16.0, 16.0)) * ol[..., None]
f = f * (1 - full[..., None]) + WHITE * full[..., None]
print("제목 옮김 (%+.1f, %+.1f)" % (dx, dy))
sv(f, "CLIMATH_m_미적분1_앞표지.png")

# ================================================================ 책등: 띠 아래 넘친 줄(1666~1676) → 흰 종이
s = rd("CLIMATH_m_미적분1_책등_받은것.jpg")
s[BY1:1690, 1170:] = 255.0
# 2026-11-26 사용자 '책등 미적분1 (m) 흰 글씨로 수정': 띠 안 검은 글씨('미적분 Ⅰ'·ⓜ)를 흰 글씨로(앞표지 흰 제목·흰 ⓜ와 맞춤).
# 바탕은 평평한 파랑(줄마다 x 1190~1300 색) → 검정 비율을 구해 같은 비율로 흰색을 얹음
SX0, SY0, SX1, SY1 = 1300, 480, 1414, 780
sb = np.repeat(np.median(s[SY0:SY1, 1190:1300], axis=1)[:, None, :], SX1 - SX0, axis=1)
BLK = np.array((14.0, 16.0, 16.0))
dd = BLK - sb
al = np.clip(((s[SY0:SY1, SX0:SX1] - sb) * dd).sum(axis=2) / np.maximum((dd * dd).sum(axis=2), 1.0), 0, 1)
al[al < 0.04] = 0
s[SY0:SY1, SX0:SX1] = sb * (1 - al[..., None]) + WHITE * al[..., None]
sv(s, "CLIMATH_m_미적분1_책등.png")

# ================================================================ 뒤표지: 띠 아래 정리 + 오른쪽 띠 60px
b = rd("CLIMATH_m_미적분1_뒤표지_받은것.jpg")
b[BY1:1690, 1170:] = 255.0
H, W = b.shape[:2]
g = np.empty((H, W + 60, 3))
g[:, :W] = b
g[:, W:] = np.median(b[:, W - 12:W - 2], axis=1)[:, None, :]
sv(g, "CLIMATH_m_미적분1_뒤표지.png")
