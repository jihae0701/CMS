# -*- coding: utf-8 -*-
"""CLIMATH 책등 아래 cms 로고를 책등 가운데 줄에 맞춤 (2026-11-26).
python spine_logo_center.py <책등 PNG> ...
- 사용자: '책등 세 글씨가 삐뚤삐뚤하지 않은지, 가운데 정렬' → 잼: 위 CLIMATH 로고 1364.5, 가운데 글자(대·수·ⓒ / 공통수학·ⓜ) 1364~1365, 아래 cms 로고 1371.0
  (옛 CREVERSE 자리 가운데에 맞췄던 것) → '응 모두 맞춰 줘': cms 로고만 가로로 옮겨 가운데를 위 CLIMATH 로고 가운데(1364.5)에 맞춤.
- 로고 둘레는 단색 바탕(흰 종이 또는 워크북 #F0F0F0)이라 로고 둘레 상자를 바탕색으로 채운 판에 반 픽셀까지 옮긴 로고(이중선형 보간)를 얹음.
"""
import sys
import numpy as np
from PIL import Image

for f in sys.argv[1:]:
    im = Image.open(f).convert("RGB")
    a = np.asarray(im).astype(float)
    L = a.mean(axis=2)
    W = a.shape[1]
    ink = L < 120
    def span(y0, y1):
        c = np.nonzero(ink[y0:y1, W - 150:].any(0))[0] + W - 150
        return c.min(), c.max()
    t0, t1 = span(60, 240)
    axis = (t0 + t1) / 2
    r = np.nonzero(ink[1680:1940, W - 150:].any(1))[0] + 1680
    y0, y1 = r.min() - 4, r.max() + 5
    b0, b1 = span(1680, 1940)
    dx = axis - (b0 + b1) / 2
    x0, x1 = int(b0) - 12, int(b1) + 13
    reg = a[y0:y1, x0:x1].copy()
    bg = np.median(np.concatenate([reg[0], reg[-1], reg[:, 0], reg[:, -1]]), axis=0)
    # 옮기기: 열 방향 이중선형(반 픽셀 포함), 바깥은 바탕색
    xs = np.arange(x1 - x0) - dx
    i0 = np.floor(xs).astype(int); fr = (xs - i0)[None, :, None]
    def col(i):
        out = np.empty((reg.shape[0], len(i), 3)); ok = (i >= 0) & (i < reg.shape[1])
        out[:] = bg; out[:, ok] = reg[:, i[ok]]
        return out
    new = col(i0) * (1 - fr) + col(i0 + 1) * fr
    a[y0:y1, x0:x1] = new
    Image.fromarray(a.round().clip(0, 255).astype(np.uint8)).save(f)
    L2 = a.mean(axis=2); c = np.nonzero((L2[1680:1940, W - 150:] < 120).any(0))[0] + W - 150
    print("%s: 축 %.1f, cms %.1f → %.1f (옮김 %+.1f), 바탕 %s" % (f, axis, (b0 + b1) / 2, (c.min() + c.max()) / 2, dx, bg.round()))
