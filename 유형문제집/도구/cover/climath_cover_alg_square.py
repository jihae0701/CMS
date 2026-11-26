# -*- coding: utf-8 -*-
"""CLIMATH(c) 대수 앞표지 — 바탕을 확률과 통계(세모)·미적분Ⅰ(동그라미)처럼 '두 쪽 색 + 큰 도형'으로, 도형은 네모 (2026-11-26).
python climath_cover_alg_square.py <표지 폴더> <출력 폴더>
- 사용자: '확률과 통계(c), 미적분1(c) 밑에 도형 동그라미 세모 형태잖아. 대수(c) 밑에 이미지를 이것들과 유사한 느낌이 들도록 네모로 만들어 봐'.
- 두 책 바탕의 짜임(잰 것): 색 띠를 세로로 반 나눠(확통 x 745, 미적분 727) 왼쪽·오른쪽이 서로 다른 세로 그러데이션, 그 위에 큰 도형 하나 —
  도형 안은 단색이고 반 나눔 선에서 색이 바뀌며, 도형 왼쪽은 오른쪽 바탕 계열의 연한 색, 오른쪽은 왼쪽 바탕 계열의 연한 색(색을 엇갈림).
- 대수 색(받은 대수 바탕에서 잼): 살구 (254, 197, 170) · 크림 (241, 222, 189) · 카키 (225, 211, 166) · 연두 (183, 228, 161).
  왼쪽: 살구 → 카키 크림 / 오른쪽: 크림 → 연두 / 네모 안: 왼쪽 연한 연두, 오른쪽 연한 살구. 나눔 선 x 737(앞표지 가운데).
- 네모: 시안 A 반듯한 정사각형(한 변 940, 큰 글자 가운데 뒤), 시안 B 14° 기울인 정사각형(한 변 900).
- 나머지(위 CLIMATH·아래 cms 로고, CLI MATH·ⓒ, '대 수', 제목 줄)는 지금 대수 앞표지(CLIMATH_c_대수_앞표지.png) 그대로: 검은 글자는 떼어 새 바탕 위에 얹고 제목 줄은 같은 모양으로 다시 그림.
"""
import os, sys
import numpy as np
import cv2
from PIL import Image, ImageDraw

cdir, outdir = sys.argv[1:3]
os.makedirs(outdir, exist_ok=True)
BLACK = np.array((14.0, 16.0, 16.0))
lum = lambda a: a[..., 0] * 0.299 + a[..., 1] * 0.587 + a[..., 2] * 0.114
cur = np.asarray(Image.open(os.path.join(cdir, "CLIMATH_c_대수_앞표지.png")).convert("RGB")).astype(float)
H, W = cur.shape[:2]
BY0, BY1 = 264, 1666                 # 새 색 띠(확통·미적분과 같은 높이)
SPLIT = 737

# ---- 지금 앞표지에서 검은 글자(CLI MATH·ⓒ·'대 수') 비율 떼어 내기
L = lum(cur)
core = np.zeros(L.shape, bool)
for (x0, y0, x1, y1) in ((450, 460, 1015, 1285), (640, 1465, 840, 1555)):
    core[y0:y1, x0:x1] = L[y0:y1, x0:x1] < 40
dark = (cv2.dilate(core.astype(np.uint8), np.ones((5, 5), np.uint8)) > 0) & (L < 140)
fg = cv2.dilate(dark.astype(np.uint8) * 255, np.ones((7, 7), np.uint8))
B = cv2.inpaint(cur.clip(0, 255).astype(np.uint8), fg, 6, cv2.INPAINT_TELEA).astype(float)
d = BLACK - B
alpha = np.clip(((cur - B) * d).sum(axis=2) / np.maximum((d * d).sum(axis=2), 1.0), 0, 1) * (fg > 0)
alpha[alpha < 0.04] = 0


def vgrad(c0, c1, h):
    t = np.linspace(0, 1, h)[:, None]
    return np.array(c0, float)[None] * (1 - t) + np.array(c1, float)[None] * t


def band_bg(square):
    h = BY1 - BY0
    bg = np.empty((h, W, 3))
    bg[:, :SPLIT] = vgrad((254, 197, 170), (232, 214, 168), h)[:, None, :]
    bg[:, SPLIT:] = vgrad((242, 224, 190), (183, 228, 161), h)[:, None, :]
    # 네모(4배 세분 표본 가장자리)
    S = 4
    m = Image.new("L", (W * S, h * S), 0)
    ImageDraw.Draw(m).polygon([(x * S, (y - BY0) * S) for x, y in square], fill=255)
    m = np.asarray(m.resize((W, h), Image.LANCZOS)).astype(float)[..., None] / 255.0
    sq = np.empty((h, W, 3))
    sq[:, :SPLIT] = (222, 237, 203)        # 네모 왼쪽: 연한 연두(오른쪽 바탕 계열)
    sq[:, SPLIT:] = (253, 216, 192)        # 네모 오른쪽: 연한 살구(왼쪽 바탕 계열)
    return bg * (1 - m) + sq * m


def square(cx, cy, side, deg):
    t = np.radians(deg)
    c, s = np.cos(t), np.sin(t)
    return [(cx + (dx * c - dy * s), cy + (dx * s + dy * c)) for dx, dy in ((-side / 2, -side / 2), (side / 2, -side / 2), (side / 2, side / 2), (-side / 2, side / 2))]


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


for name, sq in (("A", square(732, 875, 940, 0)), ("B", square(735, 880, 900, 14))):
    im = cur.copy()
    im[250:BY0] = 254.0; im[BY1:1680] = 254.0             # 옛 띠의 흐린 위·아래 끝 → 흰 종이
    im[BY0:BY1] = band_bg(sq)
    im = im * (1 - alpha[..., None]) + BLACK * alpha[..., None]
    lines(im)
    Image.fromarray(im.round().clip(0, 255).astype(np.uint8)).save(os.path.join(outdir, "CLIMATH_c_대수_앞표지_네모%s.png" % name))
    print("-> 네모", name)
