# -*- coding: utf-8 -*-
"""CLIMATH 표지 3장의 CREVERSE 로고 → cms 로고 (책 이름만 바꿔 씀) (2026-11-26).
python climath_cover_logo_book.py <원본 폴더> <표지 폴더> <cms 로고> <책 꼬리(예: c_확률과통계)>
- 원본: <원본 폴더>/CLIMATH_<꼬리>_{앞표지,책등,뒤표지}.jpg → <표지 폴더>/CLIMATH_<꼬리>_{앞표지,책등,뒤표지}.png
- 규칙은 대수 표지(climath_cover_logo_alg.py)와 같음: cms(Master Charcoal) 로고, CREVERSE 자리는 둘레 바탕색으로 지움.
  · 앞표지: 높이 23px(위 CLIMATH 'C' 높이), CREVERSE 자리 가운데.
  · 책등: 시계 방향 90°, 폭 19px, 세로는 CREVERSE 자리 가운데·가로는 위 CLIMATH 로고 가운데(책등 가운데 줄, 반 픽셀까지).
  · 뒤표지: 가운데 CREVERSE → cms 23px(가운데). 뒤표지 폭이 앞표지와 달라도(확률과 통계 1446px) CREVERSE를 찾아 그 자리에.
- 2026-11-26 사용자 '표지 수정'(CLIMATH(c) 확률과 통계 표지 3장)에서 처음 씀.
"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw

odir, cdir, logo, tag = sys.argv[1:5]


def ink_box(a, box, thr=600):
    x0, y0, x1, y1 = box
    m = a[y0:y1, x0:x1].sum(axis=2) < thr
    ys, xs = np.nonzero(m)
    return (x0 + xs.min(), y0 + ys.min(), x0 + xs.max(), y0 + ys.max()), tuple(int(v) for v in a[y0 - 4, x0])


def logo_alpha(size, rot):
    lg = Image.open(logo).convert("RGBA")
    al = np.asarray(lg)[..., 3]
    ys, xs = np.nonzero(al > 10)
    lg = lg.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
    if rot:
        lg = lg.rotate(rot, expand=True)
        w = size; h = round(lg.height * w / lg.width)
    else:
        h = size; w = round(lg.width * h / lg.height)
    return lg.resize((w, h), Image.LANCZOS)


def put(img, search, size, rot=0, cx=None, pad=6):
    a = np.asarray(img).astype(int)
    (x0, y0, x1, y1), bg = ink_box(a, search)
    lg = logo_alpha(size, rot)
    ImageDraw.Draw(img).rectangle((x0 - pad, y0 - pad, x1 + pad, y1 + pad), fill=bg)
    cx = (x0 + x1) / 2 if cx is None else cx
    cy = (y0 + y1) / 2
    # 반 픽셀 자리까지: 4배로 키운 판에 놓고 줄임
    S = 4
    w, h = lg.size
    X, Y = cx - w / 2, cy - h / 2
    bx0, by0 = int(np.floor(X)) - 2, int(np.floor(Y)) - 2
    BWd, BHd = w + 5, h + 5
    big = Image.new("RGBA", (BWd * S, BHd * S), (0, 0, 0, 0))
    big.paste(lg.resize((w * S, h * S), Image.LANCZOS), (round((X - bx0) * S), round((Y - by0) * S)))
    sm = big.resize((BWd, BHd), Image.LANCZOS)
    img.paste(sm, (bx0, by0), sm)
    print("  CREVERSE (%d, %d, %d, %d) → cms 가운데 (%.1f, %.1f), 바탕 %s" % (x0, y0, x1, y1, cx, cy, bg))
    return img


def spine_axis(img):
    a = np.asarray(img.convert("L")).astype(int)
    W = a.shape[1]
    c = np.nonzero((a[60:240, W - 150:] < 120).any(0))[0] + W - 150
    return (c.min() + c.max()) / 2


for part in ("앞표지", "책등", "뒤표지"):
    src = os.path.join(odir, "CLIMATH_%s_%s.png" % (tag, part))         # 정리한 원본(png)이 있으면 그것(미적분Ⅰ), 없으면 받은 jpg
    if not os.path.exists(src):
        src = src[:-4] + ".jpg"
    im = Image.open(src).convert("RGB")
    W = im.width
    print(part, im.size)
    if part == "앞표지":
        put(im, (560, 1760, 920, 1860), 23)
    elif part == "책등":
        put(im, (W - 114, 1700, W, 1920), 19, rot=-90, cx=spine_axis(im))
    else:
        put(im, (W // 2 - 250, 980, W // 2 + 150, 1150), 23)
    im.save(os.path.join(cdir, "CLIMATH_%s_%s.png" % (tag, part)))
