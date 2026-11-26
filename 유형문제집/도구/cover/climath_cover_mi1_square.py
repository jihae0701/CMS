# -*- coding: utf-8 -*-
"""CLIMATH(c) 미적분Ⅰ 표지 — 기울인 정사각형 바탕 (2026-11-26).
python climath_cover_mi1_square.py <표지 폴더>
- 사용자: (대수 네모 시안 B를 보고) '기울인 정사각형 이용, 주황 좀 더 핑크한 주황으로 하고 책등이 초록빛이 되도록 좌우 색 배합 바꾸기'
  → '정사각형 기울인 거를 CLIMATH(c) 미적분1 표지로 하기'.
- 바탕 짜임은 확률과 통계·미적분Ⅰ(옛 동그라미)과 같음: 색 띠(y 264~1665)를 x 737에서 반 나눠 좌우 세로 그러데이션 + 큰 도형(색 엇갈림).
  · 왼쪽(책등 쪽): 연두 크림 (226, 236, 192) → 하늘빛 도는 연두 (179, 226, 182)  / 오른쪽: 분홍빛 주황 (252, 186, 172) → 연한 살구 크림 (246, 214, 190)
  · 14° 기울인 정사각형(한 변 900, 가운데 735, 880): 왼쪽 연한 분홍 주황 (253, 215, 206), 오른쪽 연한 연두 (224, 238, 205).
- 앞표지: 지금 미적분Ⅰ 앞표지(이전 판 `표지/시안/이전_CLIMATH_c_미적분1_*.png`)의 검은 글자(CLI MATH·ⓒ·'미적분 Ⅰ')를 떼어 새 바탕 위에, 제목 줄·로고는 그대로 다시.
- 책등·뒤표지: 색 띠(책등 x 1178~1413, 뒤 x 1178~1473, y 264~1665)를 앞표지 띠 왼쪽 끝 세로 색(연두 그러데이션)으로. 책등 글씨(제목·ⓒ)는 떼어 다시 얹음.
"""
import os, sys
import numpy as np
import cv2
from PIL import Image, ImageDraw

cdir = sys.argv[1]
BLACK = np.array((14.0, 16.0, 16.0))
lum = lambda a: a[..., 0] * 0.299 + a[..., 1] * 0.587 + a[..., 2] * 0.114
rd = lambda n: np.asarray(Image.open(os.path.join(cdir, n)).convert("RGB")).astype(float)
sv = lambda a, n: Image.fromarray(a.round().clip(0, 255).astype(np.uint8)).save(os.path.join(cdir, n))
BY0, BY1, SPLIT = 264, 1666, 737
LT, LB = (226, 236, 192), (179, 226, 182)       # 진한 연두 (183,228,161)에 하늘색 (170,220,245)을 약 25% 섞음 — 2026-11-26 사용자 '연두색 중 진한 부분에 하늘색 한 스푼'
RT, RB = (252, 186, 172), (246, 214, 190)
SQL, SQR = (253, 215, 206), (224, 238, 205)


def vgrad(c0, c1, h):
    t = np.linspace(0, 1, h)[:, None]
    return np.array(c0, float)[None] * (1 - t) + np.array(c1, float)[None] * t


def black_alpha(a, boxes, thr=40, wide=140):
    L = lum(a)
    core = np.zeros(L.shape, bool)
    for (x0, y0, x1, y1) in boxes:
        core[y0:y1, x0:x1] = L[y0:y1, x0:x1] < thr
    dark = (cv2.dilate(core.astype(np.uint8), np.ones((5, 5), np.uint8)) > 0) & (L < wide)
    fg = cv2.dilate(dark.astype(np.uint8) * 255, np.ones((7, 7), np.uint8))
    B = cv2.inpaint(a.clip(0, 255).astype(np.uint8), fg, 6, cv2.INPAINT_TELEA).astype(float)
    d = BLACK - B
    al = np.clip(((a - B) * d).sum(axis=2) / np.maximum((d * d).sum(axis=2), 1.0), 0, 1) * (fg > 0)
    al[al < 0.04] = 0
    return al


def lines(im):
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
        r = im[Y0:Y0 + Hd, X0:X0 + Wd]
        r = r * (1 - o) + np.array(EDGE, float) * o
        im[Y0:Y0 + Hd, X0:X0 + Wd] = r * (1 - i) + 255.0 * i


# ---------------------------------------------------------------- 앞표지
cur = rd("시안/이전_CLIMATH_c_미적분1_앞표지.png")
H, W = cur.shape[:2]
alpha = black_alpha(cur, [(450, 460, 1015, 1285), (560, 1465, 920, 1555)])
h = BY1 - BY0
band = np.empty((h, W, 3))
band[:, :SPLIT] = vgrad(LT, LB, h)[:, None, :]
band[:, SPLIT:] = vgrad(RT, RB, h)[:, None, :]
t = np.radians(14); c, s = np.cos(t), np.sin(t)
cx, cy, side = 735, 880, 900
sq = [(cx + dx * c - dy * s, cy + dx * s + dy * c) for dx, dy in ((-side / 2, -side / 2), (side / 2, -side / 2), (side / 2, side / 2), (-side / 2, side / 2))]
S = 4
m = Image.new("L", (W * S, h * S), 0)
ImageDraw.Draw(m).polygon([(x * S, (y - BY0) * S) for x, y in sq], fill=255)
m = np.asarray(m.resize((W, h), Image.LANCZOS)).astype(float)[..., None] / 255.0
sqc = np.empty((h, W, 3)); sqc[:, :SPLIT] = SQL; sqc[:, SPLIT:] = SQR
band = band * (1 - m) + sqc * m
im = cur.copy()
im[250:BY0] = 254.0; im[BY1:1680] = 254.0
im[BY0:BY1] = band
im = im * (1 - alpha[..., None]) + BLACK * alpha[..., None]
lines(im)
sv(im, "CLIMATH_c_미적분1_앞표지.png")
strip = band[:, 0].copy()                                   # 앞표지 띠 왼쪽 끝 세로 색 = 책등·뒤표지 띠 색

# ---------------------------------------------------------------- 책등
sp = rd("시안/이전_CLIMATH_c_미적분1_책등.png")
sal = black_alpha(sp, [(1300, 480, 1414, 780)], thr=60, wide=150)
sp[250:BY0, 1170:] = 255.0; sp[BY1:1680, 1170:] = 255.0
sp[BY0:BY1, 1178:1414] = strip[:, None, :]
sp = sp * (1 - sal[..., None]) + BLACK * sal[..., None]
sv(sp, "CLIMATH_c_미적분1_책등.png")

# ---------------------------------------------------------------- 뒤표지
bk = rd("시안/이전_CLIMATH_c_미적분1_뒤표지.png")
bk[250:BY0, 1170:] = 255.0; bk[BY1:1680, 1170:] = 255.0
bk[BY0:BY1, 1178:1474] = strip[:, None, :]
sv(bk, "CLIMATH_c_미적분1_뒤표지.png")
print("-> CLIMATH_c_미적분1_{앞표지,책등,뒤표지}.png (기울인 정사각형)")
