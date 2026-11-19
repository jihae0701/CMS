# -*- coding: utf-8 -*-
"""CLIMATH(m) 공통수학2 앞표지 바탕 다시 짜기 (2026-11-19).
python make_bg_c2.py <새 바탕 그림(리본)> <출력 폴더>  → bg_A.png, bg_B.png (앞표지 색 띠 크기 1474×1406)
- 사용자: '메인 이미지가 살짝 마음에 안 들어. 색깔 유지, 이미지 형태 유지, 공통수학1처럼 메인 그래픽이 오른쪽에 큰 거, 왼쪽 아래 작은 거 하나. 그래픽이 자연스럽게 제시해줘'.
- 시안 A(작은 리본 좌우 뒤집음, 0.62배, 45°)·B(그대로, 0.58배, 50°) — 여러 각도·크기를 그려 보고 잘린 끝이 안 보이는 것만 고름.
- 방법: 리본 그림에서 바탕(보라→하늘→연두 그러데이션)을 추정(리본 자리를 줄여서 메운 뒤 부드럽게)하고, 리본 = 그림 − 바탕(차이)으로 떼어 냄.
  새 바탕 = 추정한 바탕을 띠 크기로. 큰 리본 = 원래 리본(오른쪽, 지금 표지와 같은 크기·자리). 작은 리본 = 떼어 낸 리본을 줄이고 돌려 왼쪽 아래에(띠 가장자리에 걸쳐 잘리게).
  리본은 투명한 유리라 '차이'를 더하는 식으로 얹어, 아래 바탕색(연두·노랑)이 비쳐 보이게 함.
"""
import os, sys
import numpy as np
import cv2
from PIL import Image

src, outdir = sys.argv[1:3]
os.makedirs(outdir, exist_ok=True)
a = np.asarray(Image.open(src).convert("RGB")).astype(np.float32)
H0, W0 = a.shape[:2]

# ---- 바탕 추정: 줄마다 왼쪽 끝 색을 기준으로 리본 자리 찾기 → 줄여서 메우기 → 키워서 흐리게
row = a[:, 5:300].mean(axis=1)                                    # 줄마다 바탕색(왼쪽, 리본 없음)
rough = np.repeat(row[:, None, :], W0, axis=1)
diff = np.abs(a - rough).sum(axis=2)
mask = (diff > 28).astype(np.uint8) * 255
mask = cv2.dilate(mask, np.ones((25, 25), np.uint8))
k = 8
small = cv2.resize(a, (W0 // k, H0 // k), interpolation=cv2.INTER_AREA).clip(0, 255).astype(np.uint8)
msmall = cv2.resize(mask, (W0 // k, H0 // k), interpolation=cv2.INTER_NEAREST)
fill = cv2.inpaint(small, msmall, 12, cv2.INPAINT_TELEA)
B = cv2.resize(fill, (W0, H0), interpolation=cv2.INTER_CUBIC).astype(np.float32)
B = cv2.GaussianBlur(B, (0, 0), 25)
delta = a - B                                                     # 리본(유리)의 차이
soft = cv2.GaussianBlur(mask.astype(np.float32) / 255.0, (0, 0), 6)
delta *= soft[..., None]                                          # 리본 밖은 0

# ---- 띠 크기로(지금 표지와 같은 배치: 높이 맞춤 ×0.773, 오른쪽 끝 맞춤)
BW, BH = 1474, 1406
sc = max(BW / W0, BH / H0)
SW, SH = round(W0 * sc), round(H0 * sc)
off = SW - BW
Bb = cv2.resize(B, (SW, SH), interpolation=cv2.INTER_AREA)[:, off:off + BW]
Db = cv2.resize(delta, (SW, SH), interpolation=cv2.INTER_AREA)[:, off:off + BW]


def place(canvas, d, s, ang, cx, cy, flip=False, crop=None):
    """리본 차이 d를 s배·ang도 돌려 (cx, cy)에 가운데가 오게 더함. crop=(y0, y1): 리본의 그 높이 구간만"""
    if crop:
        d = d[crop[0]:crop[1]]
    if flip:
        d = d[:, ::-1]
    h, w = d.shape[:2]
    M = cv2.getRotationMatrix2D((w / 2, h / 2), ang, s)
    cos, sin = abs(M[0, 0]), abs(M[0, 1])
    nw, nh = int(h * sin + w * cos) + 2, int(h * cos + w * sin) + 2
    M[0, 2] += nw / 2 - w / 2
    M[1, 2] += nh / 2 - h / 2
    r = cv2.warpAffine(d, M, (nw, nh), flags=cv2.INTER_AREA, borderValue=(0, 0, 0))
    x0, y0 = int(cx - nw / 2), int(cy - nh / 2)
    X0, Y0 = max(0, x0), max(0, y0)
    X1, Y1 = min(canvas.shape[1], x0 + nw), min(canvas.shape[0], y0 + nh)
    canvas[Y0:Y1, X0:X1] += r[Y0 - y0:Y1 - y0, X0 - x0:X1 - x0]


# 작은 리본: 리본 부분(원본 x 800~2000)만 잘라 좌우로 뒤집거나 그대로, 비스듬히 돌려 왼쪽 아래 구석에 —
# 두 잘린 끝(원본 위·아래 끝)이 왼쪽 가장자리와 아래 가장자리 밖으로 나가게(공통수학1의 작은 고리처럼 가장자리에 걸침)
RIB = delta[:, 800:2000]
variants = {
    "A": dict(s=0.62 * sc, ang=45, cx=110, cy=1240, flip=True),
    "B": dict(s=0.58 * sc, ang=50, cx=120, cy=1250, flip=False),
}
for name, v in variants.items():
    D = Db.copy()
    place(D, RIB, **v)
    out = (Bb + D).clip(0, 255).astype(np.uint8)
    Image.fromarray(out).save(os.path.join(outdir, "bg_%s.png" % name))
    print(name, v)
Image.fromarray((Bb + Db).clip(0, 255).astype(np.uint8)).save(os.path.join(outdir, "bg_0.png"))   # 비교용: 큰 리본만

# ================================================================ 시안 B 확정판(2026-11-19): 펼친 표지(뒤표지 띠 | 책등 | 앞표지)
# 사용자: 'B가 더 마음에 들어, 그래픽이 전반적으로 오른쪽으로 좀 더(큰 그래픽 윗부분이 조금 잘리겠지), 왼쪽 아래 작은 그래픽은 잘 연장해서 책등과 뒤표지까지'.
# - 한 장으로 이어 붙인 띠(뒤표지 띠 302 + 책등 236 + 앞표지 1474 = 2012 × 1406)에 그려서 세 조각으로 자름 → 이음매에서 그림이 이어짐.
# - 큰 리본: 오른쪽으로 150px(앞표지 폭의 약 10%) 옮김 → 오른쪽 위가 조금 더 잘림.
# - 작은 리본: 시안 B와 같은 모양(뒤집지 않음)을 0.75배·75°로 길게 눕혀, 뒤표지 띠 왼쪽 끝에서 들어와 책등 위로 휘고 앞표지 왼쪽 아래로 내려가
#   아래 가장자리 밖으로 나가게(잘린 두 끝이 모두 띠 밖). 바탕은 앞표지 띠 왼쪽 끝 세로 색을 뒤표지·책등 쪽으로 이어 씀.
BK, SP = 302, 236
X0 = BK + SP
WT = X0 + BW
SHIFT = 150
Bs = cv2.resize(B, (SW, SH), interpolation=cv2.INTER_AREA)
Ds = cv2.resize(delta, (SW, SH), interpolation=cv2.INTER_AREA)
# 띠 윗선이 원래 그림에서 뒤표지 256·책등 261·앞표지 260으로 조금씩 달라, 펼친 띠는 실제 높이(y 256~1666)로 그려 각자 자리에서 자름
TOP = {"back": 256, "spine": 261, "front": 260}
Y0w = min(TOP.values())
HC = BH + max(TOP.values()) - Y0w
fo = TOP["front"] - Y0w
bgw = np.zeros((HC, WT, 3), np.float32)
Dw = np.zeros_like(bgw)
fb = Bs[:, off:off + BW]
bgw[fo:fo + BH, X0:] = fb
bgw[:fo, X0:] = fb[:1]
bgw[fo + BH:, X0:] = fb[-1:]
bgw[:, :X0] = bgw[:, X0:X0 + 1]
st = off - SHIFT
srcD = Ds[:, max(0, st):st + BW]
Dw[fo:fo + BH, X0 + max(0, -st):X0 + max(0, -st) + srcD.shape[1]] = srcD[:, :BW - max(0, -st)]
place(Dw, RIB, s=0.75 * sc, ang=75, cx=X0 - 150, cy=1260 + fo, flip=False)
wrap = (bgw + Dw).clip(0, 255).astype(np.uint8)
cut = lambda k, x0, x1: wrap[TOP[k] - Y0w:TOP[k] - Y0w + BH, x0:x1]
Image.fromarray(cut("back", 0, BK)).save(os.path.join(outdir, "wrap_back.png"))
Image.fromarray(cut("spine", BK, X0)).save(os.path.join(outdir, "wrap_spine.png"))
Image.fromarray(cut("front", X0, WT)).save(os.path.join(outdir, "wrap_front.png"))
Image.fromarray(wrap).save(os.path.join(outdir, "wrap_all.png"))
print("펼친 띠", wrap.shape, "큰 리본 오른쪽으로", SHIFT, "px")

# ================================================================ 앞표지 확정(2026-11-19)
# 사용자: '책등에 이어지게 하지 말자'(책등·뒤표지는 리본 없는 색 띠) → '작은 그래픽이 앞표지 아래 나오도록 다시 수정', '큰 그래픽이 오른쪽으로 이동한 것은 좋아'.
# 큰 리본: 오른쪽으로 150px(그대로). 작은 리본: 시안 B(0.58배·50°, 뒤집지 않음)를 앞표지 왼쪽 아래 구석에 — 앞표지 안에서 보이게.
Df = np.zeros((BH, BW, 3), np.float32)
Df[:, max(0, -st):max(0, -st) + srcD.shape[1]] = srcD[:, :BW - max(0, -st)]
place(Df, RIB, **variants["B"])
Image.fromarray((fb + Df).clip(0, 255).astype(np.uint8)).save(os.path.join(outdir, "front_final.png"))
print("앞표지 확정 바탕: 큰 리본 +150px, 작은 리본 시안 B")
