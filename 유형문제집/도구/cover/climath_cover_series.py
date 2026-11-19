# -*- coding: utf-8 -*-
"""CLIMATH 개념유형·워크북 표지 4종(공통수학1·2 × 개념유형·워크북) — 앞·책등·뒤 (2026-11-19).
python climath_cover_series.py <표지 폴더> <원본 폴더> <Pretendard 폴더>
- 사용자: '위(CLIMATH(m) 표지)와 똑같은 형태로 4개의 표지를 더 만들어줘. 가운데 이미지를 지금 주는 걸로(책 제목도 써 있는 이미지니까 그냥 쓰면 돼).
  책등은 공통수학1 동그라미(c) 둥근 네모 상자(개념유형) / 공통수학1 동그라미(c) 둥근 네모 상자(워크북), 공통수학2 동일'.
- 앞표지: CLIMATH(m) 앞표지(위 CLIMATH 로고·아래 cms 로고 그대로)의 색 띠(y 260~1665)를 받은 그림의 바탕색으로 채우고, 받은 그림(2000×2000, 제목 포함)을
  0.78배로 줄여 띠 가운데(그림 속 내용 가운데 기준)에 놓음. CLI MATH·ⓜ·제목 줄은 쓰지 않음(그림에 제목이 있음).
- 책등: CLIMATH(m) 책등의 '공통수학 N' 글자·CLIMATH·cms 로고는 그대로 두고, 띠 색을 그림 바탕색으로. ⓜ 자리에 ⓒ(같은 크기의 원 테두리 + c),
  그 아래에 둥근 네모 상자(검은 테두리)와 '개념유형'/'워크북'(Pretendard SemiBold).
- 뒤표지: 원본 뒤표지의 오른쪽 색 띠를 그림 바탕색으로.
"""
import os, sys
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

CDIR, ODIR, PDIR = sys.argv[1:4]
FB = lambda w: os.path.join(PDIR, "Pretendard-%s.otf" % w)
BLACK = np.array((14.0, 16.0, 16.0))
lum = lambda a: a[..., 0] * 0.299 + a[..., 1] * 0.587 + a[..., 2] * 0.114

BOOKS = [  # (과목, 종류, 그림, 책등 원본)
    (1, "개념유형", "16.webp"), (1, "워크북", "17.webp"),
    (2, "개념유형", "18.webp"), (2, "워크북", "19.webp"),
]
SCALE = 0.78


def black_layer(a):
    """띠 안의 검은 글자를 떼어 냄(바탕을 메워 추정 → 검정 비율)"""
    L = lum(a)
    core = L < 40
    dark = (cv2.dilate(core.astype(np.uint8), np.ones((5, 5), np.uint8)) > 0) & (L < 130)
    fg = cv2.dilate(dark.astype(np.uint8) * 255, np.ones((7, 7), np.uint8))
    B = cv2.inpaint(a.clip(0, 255).astype(np.uint8), fg, 6, cv2.INPAINT_TELEA).astype(float)
    d = BLACK - B
    al = ((a - B) * d).sum(axis=2) / np.maximum((d * d).sum(axis=2), 1.0)
    al = np.clip(al, 0, 1) * (fg > 0)
    al[al < 0.04] = 0
    return al


def supersample(draw_fn, w, h, S=4):
    big = Image.new("L", (w * S, h * S), 0)
    draw_fn(ImageDraw.Draw(big), S)
    return np.asarray(big.resize((w, h), Image.LANCZOS)).astype(float) / 255.0


for n, kind, pic in BOOKS:
    art = Image.open(os.path.join(ODIR, pic)).convert("RGB")
    A = np.asarray(art).astype(int)
    bg = tuple(int(v) for v in np.median(np.array([A[5, 5], A[5, -5], A[-5, 5], A[-5, -5]]), axis=0))
    d = np.abs(A - np.array(bg)).sum(axis=2) > 25
    ys, xs = np.nonzero(d)
    ccx, ccy = (xs.min() + xs.max()) / 2, (ys.min() + ys.max()) / 2       # 그림 속 내용 가운데
    tag = "CLIMATH_공통수학%d_%s" % (n, kind)

    # ---------------------------------------------------------------- 앞표지
    fr = Image.open(os.path.join(CDIR, "CLIMATH_공통수학%d_앞표지.png" % n)).convert("RGB")
    Y0, Y1 = 260, 1666
    band = Image.new("RGB", (fr.width, Y1 - Y0), bg)
    sm = art.resize((round(art.width * SCALE), round(art.height * SCALE)), Image.LANCZOS)
    px = round(fr.width / 2 - ccx * SCALE)
    py = round((Y1 - Y0) / 2 - ccy * SCALE)
    band.paste(sm, (px, py))
    fr.paste(band, (0, Y0))
    fr.save(os.path.join(CDIR, tag + "_앞표지.png"))

    # ---------------------------------------------------------------- 책등
    sp = np.asarray(Image.open(os.path.join(CDIR, "CLIMATH_공통수학%d_책등.png" % n)).convert("RGB")).astype(float)
    SY0, SY1, SX0, SX1 = 261, 1667, 1178, 1414
    al = black_layer(sp[SY0:SY1, SX0:SX1])
    al[712 - SY0:753 - SY0] = 0                                          # ⓜ 지움
    sp[SY0:SY1, SX0:SX1] = np.array(bg, float) * (1 - al[..., None]) + BLACK * al[..., None]
    # ⓒ: ⓜ와 같은 원(가운데 (1364.5, 732), 바깥 반지름 16.5, 테두리 4) + 'c'
    cx, cy, R, T = 1364.5, 732.0, 16.5, 4.0
    W_, H_ = 60, 60
    ox, oy = int(cx) - 30, int(cy) - 30
    ring = supersample(lambda dr, S: dr.ellipse(((cx - ox - R) * S, (cy - oy - R) * S, (cx - ox + R) * S, (cy - oy + R) * S),
                                                outline=255, width=int(T * S)), W_, H_)
    f = ImageFont.truetype(FB("ExtraBold"), 100)                         # ⓜ 안 m처럼 굵게
    bb = f.getbbox("c", anchor="ls")
    fsz = 100 * 14.0 / (bb[3] - bb[1])                                    # 'c' 높이 = ⓜ 안 'm' 높이(14px)
    def draw_c(dr, S):
        ff = ImageFont.truetype(FB("ExtraBold"), fsz * S)
        b = ff.getbbox("c", anchor="ls")
        dr.text((30 * S - (b[0] + b[2]) / 2, 30 * S - (b[1] + b[3]) / 2), "c", font=ff, fill=255, anchor="ls")
    cm = supersample(draw_c, W_, H_)
    cm = np.rot90(cm, -1)                                                 # 책등 글씨처럼 시계 방향 90°
    m = np.maximum(ring, cm)
    reg = sp[oy:oy + H_, ox:ox + W_]
    sp[oy:oy + H_, ox:ox + W_] = reg * (1 - m[..., None]) + BLACK * m[..., None]
    # 둥근 네모 상자 + 글자(세로, 위→아래)
    f2 = ImageFont.truetype(FB("SemiBold"), 100)
    b2 = f2.getbbox("가", anchor="ls")
    tsz = 100 * 17.0 / (b2[3] - b2[1])                                    # 글자 높이 17px(책 이름 30px보다 작게)
    ft = ImageFont.truetype(FB("SemiBold"), tsz)
    tb = ft.getbbox(kind, anchor="ls")
    tw = tb[2] - tb[0]
    BW_, PADL = 34, 9                                                     # 상자 폭(책등 가로), 글자 앞뒤 여백
    BL = int(tw + 2 * PADL)                                               # 상자 길이(책등 세로)
    by0 = 765                                                             # ⓒ 아래(749) + 16
    bx0 = int(round(cx - BW_ / 2))
    def draw_box(dr, S):
        dr.rounded_rectangle((1 * S, 1 * S, (BL - 1) * S, (BW_ - 1) * S), radius=8 * S, outline=255, width=int(2 * S))
    def draw_txt(dr, S):
        ff = ImageFont.truetype(FB("SemiBold"), tsz * S)
        b = ff.getbbox(kind, anchor="ls")
        dr.text((BL / 2 * S - (b[0] + b[2]) / 2, BW_ / 2 * S - (b[1] + b[3]) / 2), kind, font=ff, fill=255, anchor="ls")
    bm = np.maximum(supersample(draw_box, BL, BW_), supersample(draw_txt, BL, BW_))
    bm = np.rot90(bm, -1)                                                 # (BL×BW) → 세로 상자(BW 폭 × BL 길이)
    hh, ww = bm.shape
    reg = sp[by0:by0 + hh, bx0:bx0 + ww]
    sp[by0:by0 + hh, bx0:bx0 + ww] = reg * (1 - bm[..., None]) + BLACK * bm[..., None]
    Image.fromarray(sp.clip(0, 255).astype(np.uint8)).save(os.path.join(CDIR, tag + "_책등.png"))
    print(tag, "바탕", bg, "앞 그림 %.2f배 (%d, %d)" % (SCALE, px, py + Y0), "책등 상자", (bx0, by0, bx0 + ww - 1, by0 + hh - 1))

    # ---------------------------------------------------------------- 뒤표지
    bk = Image.open(os.path.join(ODIR, "CLIMATH_공통수학1_뒤표지.jpg")).convert("RGB")
    ImageDraw.Draw(bk).rectangle((1172, 256, 1473, 1661), fill=bg)
    bk.save(os.path.join(CDIR, tag + "_뒤표지.png"))
