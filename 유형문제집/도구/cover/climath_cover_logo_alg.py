# -*- coding: utf-8 -*-
"""CLIMATH(c) 대수 표지: CREVERSE 로고 → cms 로고 (2026-11-26).
python climath_cover_logo_alg.py <원본 폴더> <표지 폴더> <cms 로고>
- 사용자: CLIMATH(c) 대수 표지 3장(뒤표지·책등·앞표지)을 주고 '표지 파일 수정'.
  공통수학 CLIMATH 표지 규칙(climath_cover_logo.py) 그대로: CREVERSE 로고만 cms(Master Charcoal) 로고로, CREVERSE 자리 가운데, 자리는 둘레 바탕색으로 지움.
  · 앞표지: 높이 23px(위 CLIMATH 'C' 높이) · 책등: 시계 방향 90°, 폭 19px(책등 위 CLIMATH 'C' 높이)
  · 뒤표지: 이 표지는 가운데에 CREVERSE가 있음(공통수학 뒤표지는 CLIMATH) → 같은 규칙으로 cms 로고(앞표지와 같은 23px).
"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw

odir, cdir, logo = sys.argv[1:4]


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


for part, search, size, rot in (("앞표지", (560, 1760, 920, 1860), 23, 0), ("책등", (1300, 1700, 1414, 1920), 19, -90),
                                ("뒤표지", (500, 1000, 850, 1120), 23, 0)):
    im = Image.open(os.path.join(odir, "CLIMATH_c_대수_%s.jpg" % part)).convert("RGB")
    print(part)
    put_logo(im, search, logo, size, rot).save(os.path.join(cdir, "CLIMATH_c_대수_%s.png" % part))
