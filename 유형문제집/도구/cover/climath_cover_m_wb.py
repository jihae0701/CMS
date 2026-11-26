# -*- coding: utf-8 -*-
"""CLIMATH(m) 공통수학1 워크북 표지 — 앞·책등·뒤 (2026-11-26).
python climath_cover_m_wb.py <표지 폴더> <원본 폴더> <Pretendard 폴더>
- 사용자: 'CLIMATh(m) 공통수학1 워크북 표지 만들어줘'.
- CLIMATH(m) 공통수학1 표지(앞표지·책등·원본 뒤표지)를 그대로 쓰고, CLIMATH(c) 워크북 표지(climath_cover_series.py)와 같은 표시를 더함:
  · 앞표지: (처음엔 'CLI' 위에 '워크북' 상자를 넣었으나 2026-11-26 사용자 '앞표지에 워크북 표시 없애, 책등은 남겨'로 뺌) — (m) 앞표지 그대로 + 종이색.
  · 책등: ⓜ 그대로, 그 아래 둥근 네모 상자 안 '워크북'((c) 워크북 책등과 같은 크기·자리).
  · 뒤표지: 원본 뒤표지(오른쪽 색 띠 = (m) 그라데이션) 그대로.
  · 세 장 모두 색 띠 밖 흰 종이를 #F0F0F0(×240/255)로 — (c) 워크북과 같음.
"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

CDIR, ODIR, PDIR = sys.argv[1:4]
FB = lambda w: os.path.join(PDIR, "Pretendard-%s.otf" % w)
BLACK = np.array((14.0, 16.0, 16.0))
PAPER = 240
TAG = "CLIMATH_공통수학1_m_워크북"


def supersample(draw_fn, w, h, S=4):
    big = Image.new("L", (w * S, h * S), 0)
    draw_fn(ImageDraw.Draw(big), S)
    return np.asarray(big.resize((w, h), Image.LANCZOS)).astype(float) / 255.0


def paper(img, band):
    a = np.asarray(img.convert("RGB")).astype(float)
    keep = a.copy()
    a = a * (PAPER / 255.0)
    x0, y0, x1, y1 = band
    a[y0:y1, x0:x1] = keep[y0:y1, x0:x1]
    return Image.fromarray(a.round().clip(0, 255).astype(np.uint8))


# ---------------------------------------------------------------- 앞표지
fr = Image.open(os.path.join(CDIR, "CLIMATH_공통수학1_앞표지.png")).convert("RGB")
a = np.asarray(fr).astype(float)
X0 = 467                       # 'CLI' 왼쪽 끝
TOP = 479                      # 'CLI' 윗끝
BW, BH = 300, 80               # 상자 크기((c) 워크북 앞표지 상자 359×95를 제목 위 빈자리에 맞게 줄임)
by0 = TOP - 46 - BH            # 제목 위 46px 띄움
f0 = ImageFont.truetype(FB("Regular"), 100)
b0 = f0.getbbox("워", anchor="ls")
tsz = 100 * 40.0 / (b0[3] - b0[1])            # 글자 높이 40px
text = "워 크 북"
def draw_fill(dr, S):
    dr.rectangle((0, 0, BW * S - 1, BH * S - 1), fill=255)
def draw_line(dr, S):
    dr.rectangle((0, 0, BW * S - 1, BH * S - 1), outline=255, width=int(3 * S))
def draw_txt(dr, S):
    ff = ImageFont.truetype(FB("Regular"), tsz * S)
    b = ff.getbbox(text, anchor="ls")
    dr.text((BW / 2 * S - (b[0] + b[2]) / 2, BH / 2 * S - (b[1] + b[3]) / 2), text, font=ff, fill=255, anchor="ls")
fill = supersample(draw_fill, BW, BH)
ink = np.maximum(supersample(draw_line, BW, BH), supersample(draw_txt, BW, BH))
reg = a[by0:by0 + BH, X0:X0 + BW]
reg = reg * (1 - fill[..., None]) + 255.0 * fill[..., None]
reg = reg * (1 - ink[..., None]) + BLACK * ink[..., None]
# a[by0:by0 + BH, X0:X0 + BW] = reg   # 2026-11-26 사용자 '앞표지에 워크북 표시 없애, 책등은 남겨' → 앞표지 상자 넣지 않음
fr = paper(Image.fromarray(a.clip(0, 255).astype(np.uint8)), (0, 260, fr.width, 1666))
fr.save(os.path.join(CDIR, TAG + "_앞표지.png"))
print("앞표지: 워크북 상자 없음(색 띠 밖 종이색만)")

# ---------------------------------------------------------------- 책등: ⓜ 아래 둥근 네모 상자 + '워크북'
sp = np.asarray(Image.open(os.path.join(CDIR, "CLIMATH_공통수학1_책등.png")).convert("RGB")).astype(float)
SY0, SY1, SX0, SX1 = 261, 1667, 1178, 1414
cx = 1364.5
kind = "워크북"
f2 = ImageFont.truetype(FB("SemiBold"), 100)
b2 = f2.getbbox("가", anchor="ls")
ksz = 100 * 17.0 / (b2[3] - b2[1])
ft = ImageFont.truetype(FB("SemiBold"), ksz)
tb = ft.getbbox(kind, anchor="ls")
BW_, PADL = 34, 9
BL = int(tb[2] - tb[0] + 2 * PADL)
sby0, sbx0 = 765, int(round(cx - BW_ / 2))
def draw_box(dr, S):
    dr.rounded_rectangle((1 * S, 1 * S, (BL - 1) * S, (BW_ - 1) * S), radius=8 * S, outline=255, width=int(2 * S))
def draw_kind(dr, S):
    ff = ImageFont.truetype(FB("SemiBold"), ksz * S)
    b = ff.getbbox(kind, anchor="ls")
    dr.text((BL / 2 * S - (b[0] + b[2]) / 2, BW_ / 2 * S - (b[1] + b[3]) / 2), kind, font=ff, fill=255, anchor="ls")
bm = np.rot90(np.maximum(supersample(draw_box, BL, BW_), supersample(draw_kind, BL, BW_)), -1)
hh, ww = bm.shape
reg = sp[sby0:sby0 + hh, sbx0:sbx0 + ww]
sp[sby0:sby0 + hh, sbx0:sbx0 + ww] = reg * (1 - bm[..., None]) + BLACK * bm[..., None]
paper(Image.fromarray(sp.clip(0, 255).astype(np.uint8)), (SX0, SY0, SX1, SY1)).save(os.path.join(CDIR, TAG + "_책등.png"))
print("책등 상자", (sbx0, sby0, sbx0 + ww - 1, sby0 + hh - 1))

# ---------------------------------------------------------------- 뒤표지
bk = Image.open(os.path.join(ODIR, "CLIMATH_공통수학1_뒤표지.jpg")).convert("RGB")
paper(bk, (1172, 256, 1474, 1662)).save(os.path.join(CDIR, TAG + "_뒤표지.png"))
