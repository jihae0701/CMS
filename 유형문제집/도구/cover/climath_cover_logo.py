# -*- coding: utf-8 -*-
"""CLIMATH(m) 기본서 표지: CREVERSE 로고만 cms 로고로 (2026-11-19).
python climath_cover_logo.py <앞표지> <책등> <앞 로고(cms 고등부)> <책등 로고(cms)> <출력 앞표지> <출력 책등>
- 사용자: CLIMATH(m) 공통수학1 표지 이미지(앞표지 1474×2000, 책등 1414×2000, 뒤표지)를 주고
  '크레버스 로고만 cms 로고로 변경, 앞표지는 cms 고등부, 책등은 cms (유형서와 동일한 크기로 넣기)'.
- 크기는 CMStory 유형서 표지(높이 2000px)와 같은 픽셀 크기: 앞표지 cms 고등부 로고 높이 40px(→ 사용자 요청으로 cms 로고, 위 CLIMATH 'C'와 같은 23px), 책등 cms 로고 폭(글자 높이) 29px → 사용자 요청으로 책등 위 CLIMATH 'C'와 같은 19px.
  위치는 CREVERSE 로고의 가운데. CREVERSE 자리는 둘레 바탕색으로 지움. 뒤표지에는 CREVERSE가 없어 바꾸지 않음.
"""
import sys
import numpy as np
from PIL import Image, ImageDraw

front, spine, logo_f, logo_s, out_f, out_s = sys.argv[1:7]


def ink_box(img, box, thr=600):
    a = np.asarray(img.convert("RGB")).astype(int)
    x0, y0, x1, y1 = box
    m = a[y0:y1, x0:x1].sum(axis=2) < thr
    ys, xs = np.nonzero(m)
    return (x0 + xs.min(), y0 + ys.min(), x0 + xs.max(), y0 + ys.max()), tuple(int(v) for v in a[y0 - 4, x0])


def put_logo(img, search, path, size, rot=0, pad=6):
    (x0, y0, x1, y1), bg = ink_box(img, search)
    lg = Image.open(path).convert("RGBA")
    al = np.asarray(lg)[..., 3]
    ys, xs = np.nonzero(al > 10)
    lg = lg.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
    if rot:
        lg = lg.rotate(rot, expand=True)
        w = size; h = round(lg.height * w / lg.width)
    else:
        h = size; w = round(lg.width * h / lg.height)
    lg = lg.resize((w, h), Image.LANCZOS)
    ImageDraw.Draw(img).rectangle((x0 - pad, y0 - pad, x1 + pad, y1 + pad), fill=bg)
    X, Y = round((x0 + x1) / 2 - w / 2), round((y0 + y1) / 2 - h / 2)
    img.paste(lg, (X, Y), lg)
    print("  CREVERSE (%d, %d, %d, %d) → cms 로고 (%d, %d, %d, %d), 바탕 %s" % (x0, y0, x1, y1, X, Y, X + w - 1, Y + h - 1, bg))
    return img


im = Image.open(front).convert("RGB")
# 2026-11-19 사용자 '개념서는 앞표지 아래 로고도 cms만 써 있는 로고로, 글씨 크기는 위 CLIMATH와 같게': 앞표지 위 CLIMATH 'C' 높이 23px(y 122~144) = cms 'c' 높이
put_logo(im, (600, 1760, 900, 1860), logo_s, 23).save(out_f)
im = Image.open(spine).convert("RGB")
# 2026-11-19 사용자 '책등 cms 크기를 위의 CLIMATH 글씨 크기와 같게(c끼리 비교)': 책등 위 CLIMATH의 'C' 글자 높이 19px(1355~1373) = cms 'c' 높이(로고 글자 높이)
put_logo(im, (1300, 1700, 1414, 1920), logo_s, 19, rot=-90).save(out_s)
