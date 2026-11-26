# -*- coding: utf-8 -*-
"""CLIMATH(m) 대수 앞표지 시안 2개 (2026-11-26).
python climath_cover_m_alg.py <표지 폴더> <원본 폴더> <출력 폴더>
- 사용자: '밑 바탕 이미지를 바꿔서 CLIMATH(m) 표지를 만든다면? 앞표지 시안 2개 줘 봐'.
- 틀: CLIMATH(m) 공통수학1 앞표지(로고 고친 것) — 위 CLIMATH·아래 cms 로고, 검은 CLI MATH와 ⓜ는 그대로 떼어 얹고, 색 띠(y 260~1665) 바탕만 새로 그림.
  제목 '대 수'는 CLIMATH(c) 대수 앞표지의 글자 모양을 가져와 (m) 표지처럼 흰 글씨 + 검은 테두리(2px)로, (m) 제목과 같은 높이·두 줄 사이 가운데.
  제목 줄 두 개는 (m) 공통수학 표지와 같은 굵기(흰 4.2px + 테두리 1.45px).
- 시안 A '유리 리본': (m) 공통수학2 바탕의 유리 리본(바탕을 추정해 '차이'로 떼어 냄)을 대수 색(코랄·살구·민트)으로 색만 돌려, 살구→민트 그러데이션 위에 큰 것 하나(오른쪽)·작은 것 하나(왼쪽 아래).
- 시안 B '지수·로그 곡선': y = 2^x 꼴 곡선과 그 역함수(로그) 곡선을 굵은 유리 관으로 그려 직선 y = x에 대칭으로 교차(대수 내용), 연보라→살구 그러데이션.
"""
import os, sys, math
import numpy as np
import cv2
from PIL import Image, ImageDraw

cdir, odir, outdir = sys.argv[1:4]
os.makedirs(outdir, exist_ok=True)
BLACK = np.array((14.0, 16.0, 16.0))
WHITE = np.array((252.0, 252.0, 252.0))
lum = lambda a: a[..., 0] * 0.299 + a[..., 1] * 0.587 + a[..., 2] * 0.114
Y0, Y1 = 260, 1666
BW, BH = 1474, Y1 - Y0
rng = np.random.default_rng(7)


def grad4(tl, tr, bl, br, w=BW, h=BH):
    y = np.linspace(0, 1, h)[:, None, None]; x = np.linspace(0, 1, w)[None, :, None]
    tl, tr, bl, br = (np.array(c, float) for c in (tl, tr, bl, br))
    g = (tl * (1 - x) + tr * x) * (1 - y) + (bl * (1 - x) + br * x) * y
    return g + rng.normal(0, 1.2, g.shape)                   # 아주 옅은 결(띠가 지지 않게)


# ---------------------------------------------------------------- 앞에 놓일 것: 검은 CLI MATH·ⓜ (m 공통수학1 앞표지에서)
front = np.asarray(Image.open(os.path.join(cdir, "CLIMATH_공통수학1_앞표지.png")).convert("RGB")).astype(float)
band = front[Y0:Y1].copy()
L = lum(band)
LET = (450, 460 - Y0, 1015, 1285 - Y0)
core = np.zeros(L.shape, bool)
core[LET[1]:LET[3], LET[0]:LET[2]] = L[LET[1]:LET[3], LET[0]:LET[2]] < 40
dark = (cv2.dilate(core.astype(np.uint8), np.ones((5, 5), np.uint8)) > 0) & (L < 130)
fg = cv2.dilate(dark.astype(np.uint8) * 255, np.ones((7, 7), np.uint8))
B = cv2.inpaint(band.clip(0, 255).astype(np.uint8), fg, 6, cv2.INPAINT_TELEA).astype(float)
d = BLACK - B
alpha = ((band - B) * d).sum(axis=2) / np.maximum((d * d).sum(axis=2), 1.0)
alpha = np.clip(alpha, 0, 1) * (fg > 0)
alpha[alpha < 0.04] = 0
ys, xs = np.nonzero(alpha > 0.5)
print("CLI MATH·ⓜ 잉크", (xs.min(), ys.min() + Y0, xs.max(), ys.max() + Y0))

# ---------------------------------------------------------------- 제목 '대 수': (c) 대수 앞표지 글자 → 흰 속 + 검은 테두리
cf = np.asarray(Image.open(os.path.join(odir, "CLIMATH_c_대수_앞표지.jpg")).convert("RGB")).astype(float)
reg = cf[1470:1552, 650:825]
Lr = lum(reg)
bgc = np.median(np.concatenate([reg[0], reg[-1], reg[:, 0], reg[:, -1]]), axis=0)
ta = np.clip((lum(bgc[None, None]) - Lr) / (lum(bgc[None, None]) - 20.0), 0, 1)      # 검은 글자 비율
ta[ta < 0.05] = 0
SC = 62.0 / 59.0                                           # (m) 제목 글자(테두리 뺀) 높이 약 62px ← (c) '대수' 59px
ta = cv2.resize(ta.astype(np.float32), (round(ta.shape[1] * SC), round(ta.shape[0] * SC)), interpolation=cv2.INTER_CUBIC).clip(0, 1)
pad = 6
ta = np.pad(ta, pad)
S = 4
big = cv2.resize(ta, (ta.shape[1] * S, ta.shape[0] * S), interpolation=cv2.INTER_CUBIC)
outl = cv2.dilate((big > 0.5).astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * 2 * S + 1, 2 * 2 * S + 1)))
outl = cv2.resize(outl.astype(np.float32), (ta.shape[1], ta.shape[0]), interpolation=cv2.INTER_AREA)
fill = ta
iy, ix = np.nonzero(outl > 0.5)
tcx, tcy = (ix.min() + ix.max()) / 2, (iy.min() + iy.max()) / 2
LINE_CX, TITLE_CY = (455.3 + 1020.3) / 2, (1441.65 + 1577.65) / 2
tx, ty = round(LINE_CX - tcx), round(TITLE_CY - tcy) - Y0


def put_front(bandbg):
    out = bandbg * (1 - alpha[..., None]) + BLACK * alpha[..., None]
    h, w = outl.shape
    r = out[ty:ty + h, tx:tx + w]
    r = r * (1 - outl[..., None]) + BLACK * outl[..., None]
    r = r * (1 - fill[..., None]) + WHITE * fill[..., None]
    out[ty:ty + h, tx:tx + w] = r
    # 제목 줄(공통수학과 같은 굵기)
    T, HW = 1.45, 4.2
    for cy in (1441.65 - Y0, 1577.65 - Y0):
        y0, y1 = cy - HW / 2, cy + HW / 2
        X0, YY = int(455.3 - T) - 2, int(y0 - T) - 2
        W_, H_ = int(1020.3 + T) + 3 - X0, int(y1 + T) + 3 - YY
        def mk(x0, y0_, x1, y1_):
            m = Image.new("L", (W_ * 8, H_ * 8), 0)
            ImageDraw.Draw(m).rectangle(((x0 - X0) * 8, (y0_ - YY) * 8, (x1 - X0) * 8 - 1, (y1_ - YY) * 8 - 1), fill=255)
            return np.asarray(m.resize((W_, H_), Image.LANCZOS)).astype(float)[..., None] / 255.0
        o, i = mk(455.3 - T, y0 - T, 1020.3 + T, y1 + T), mk(455.3, y0, 1020.3, y1)
        rr = out[YY:YY + H_, X0:X0 + W_]
        rr = rr * (1 - o) + np.array((45, 38, 45), float) * o
        out[YY:YY + H_, X0:X0 + W_] = rr * (1 - i) + 255.0 * i
    return out


def save(bandbg, name):
    im = front.copy()
    im[Y0:Y1] = put_front(bandbg)
    Image.fromarray(im.round().clip(0, 255).astype(np.uint8)).save(os.path.join(outdir, name))
    print("->", name)


# ================================================================ 시안 A: 유리 리본(색 돌림)
src = np.asarray(Image.open(os.path.join(odir, "CLIMATH_공통수학2_바탕.webp")).convert("RGB")).astype(np.float32)
H0, W0 = src.shape[:2]
row = src[:, 5:300].mean(axis=1)
diff = np.abs(src - np.repeat(row[:, None, :], W0, axis=1)).sum(axis=2)
mask = cv2.dilate((diff > 28).astype(np.uint8) * 255, np.ones((25, 25), np.uint8))
k = 8
small = cv2.resize(src, (W0 // k, H0 // k), interpolation=cv2.INTER_AREA).clip(0, 255).astype(np.uint8)
fillb = cv2.inpaint(small, cv2.resize(mask, (W0 // k, H0 // k), interpolation=cv2.INTER_NEAREST), 12, cv2.INPAINT_TELEA)
Bs = cv2.GaussianBlur(cv2.resize(fillb, (W0, H0), interpolation=cv2.INTER_CUBIC).astype(np.float32), (0, 0), 25)
soft = cv2.GaussianBlur(mask.astype(np.float32) / 255.0, (0, 0), 6)
rib = src                                                   # 리본이 있는 원래 그림(바탕 포함)
# 색 돌림: 리본 색(파랑·보라·하늘)을 코랄·살구·자홍으로 — HSV 색상 +165°, 채도 약간 올림
hsv = cv2.cvtColor(rib.clip(0, 255).astype(np.uint8), cv2.COLOR_RGB2HSV).astype(np.float32)
hsv[..., 0] = (hsv[..., 0] + 165 / 2) % 180
hsv[..., 1] = np.clip(hsv[..., 1] * 1.08, 0, 255)
ribc = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2RGB).astype(np.float32)
hsvb = cv2.cvtColor(Bs.clip(0, 255).astype(np.uint8), cv2.COLOR_RGB2HSV).astype(np.float32)
hsvb[..., 0] = (hsvb[..., 0] + 165 / 2) % 180
Bc = cv2.cvtColor(hsvb.astype(np.uint8), cv2.COLOR_HSV2RGB).astype(np.float32)
deltac = (ribc - Bc) * soft[..., None]                      # 색 돌린 유리의 '차이'

sc = BH / H0
SW, SH = round(W0 * sc), BH
Dc = cv2.resize(deltac, (SW, SH), interpolation=cv2.INTER_AREA)
bgA = grad4((255, 214, 196), (255, 232, 205), (226, 240, 214), (205, 236, 222))   # 살구 → 민트
canvasA = bgA.copy()
off = SW - BW - 150                                         # 오른쪽 끝 맞춤 + 오른쪽으로 150px (공통수학2와 같은 배치)
x0 = -off
xa, xb = max(0, x0), min(BW, x0 + SW)
canvasA[:, xa:xb] += Dc[:, xa - x0:xb - x0]


def place(canvas, dd, s, ang, cx, cy, flip=False):
    if flip:
        dd = dd[:, ::-1]
    h, w = dd.shape[:2]
    M = cv2.getRotationMatrix2D((w / 2, h / 2), ang, s)
    cos, sin = abs(M[0, 0]), abs(M[0, 1])
    nw, nh = int(h * sin + w * cos) + 2, int(h * cos + w * sin) + 2
    M[0, 2] += nw / 2 - w / 2; M[1, 2] += nh / 2 - h / 2
    r = cv2.warpAffine(dd, M, (nw, nh), flags=cv2.INTER_AREA, borderValue=(0, 0, 0))
    x0, y0 = int(cx - nw / 2), int(cy - nh / 2)
    X0, YY = max(0, x0), max(0, y0)
    X1, YB = min(canvas.shape[1], x0 + nw), min(canvas.shape[0], y0 + nh)
    canvas[YY:YB, X0:X1] += r[YY - y0:YB - y0, X0 - x0:X1 - x0]


place(canvasA, deltac, 0.58 * sc, 50, 170, BH - 110)        # 작은 리본: 왼쪽 아래 구석(공통수학2 시안 B 자리)
save(canvasA.clip(0, 255), "CLIMATH_대수_m_앞표지_시안A.png")


# ================================================================ 시안 B: 지수·로그 곡선 유리 관
def tube_layer(pts, r, cols, w=BW, h=BH):
    """곡선 pts(N×2, 띠 좌표)를 반지름 r의 유리 관으로: (색, 비율). cols = 곡선을 따라 바뀌는 색 [(t, (R,G,B)), …]"""
    S = 1
    idx = np.full((h, w), -1, np.int32)
    canvas = np.ones((h, w), np.uint8)
    dense = []
    for i in range(len(pts) - 1):
        a_, b_ = pts[i], pts[i + 1]
        n = int(max(abs(b_[0] - a_[0]), abs(b_[1] - a_[1]))) + 1
        for t in np.linspace(0, 1, n, endpoint=False):
            dense.append((a_[0] + (b_[0] - a_[0]) * t, a_[1] + (b_[1] - a_[1]) * t, (i + t) / (len(pts) - 1)))
    dense = np.array(dense)
    px = np.round(dense[:, 0]).astype(int); py = np.round(dense[:, 1]).astype(int)
    ok = (px >= 0) & (px < w) & (py >= 0) & (py < h)
    canvas[py[ok], px[ok]] = 0
    idx[py[ok], px[ok]] = np.nonzero(ok)[0]
    dist, lab = cv2.distanceTransformWithLabels(canvas, cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
    zy, zx = np.nonzero(canvas == 0)
    lab2idx = np.zeros(lab.max() + 1, np.int64)
    lab2idx[lab[zy, zx]] = idx[zy, zx]
    near = lab2idx[lab]
    t = dense[near, 2]
    # 단면 위치(부호): 곡선 진행 방향의 왼쪽(+)/오른쪽(−)
    tang = np.gradient(dense[:, :2], axis=0)
    tang /= np.maximum(np.linalg.norm(tang, axis=1, keepdims=True), 1e-6)
    gx, gy = np.meshgrid(np.arange(w), np.arange(h))
    vx, vy = gx - dense[near, 0], gy - dense[near, 1]
    side = np.sign(tang[near, 0] * vy - tang[near, 1] * vx)
    u = np.clip(dist / r, 0, 1) * side                       # −1 ~ 1
    inside = dist <= r
    nz = np.sqrt(np.clip(1 - u * u, 0, 1))
    base = np.zeros((h, w, 3))
    ts = [c[0] for c in cols]; cs = np.array([c[1] for c in cols], float)
    for ch in range(3):
        base[..., ch] = np.interp(t, ts, cs[:, ch])
    shade = 0.55 + 0.45 * nz                                 # 가운데 밝고 가장자리 진함
    col = base * shade[..., None]
    hl = np.exp(-((u + 0.45) / 0.13) ** 2) * nz              # 위쪽 반사광 띠
    rim = np.exp(-((np.abs(u) - 0.93) / 0.05) ** 2)          # 가장자리 밝은 테
    col = col + (255 - col) * (0.85 * hl + 0.35 * rim)[..., None]
    a = (0.62 + 0.30 * (1 - nz)) * inside                    # 유리: 가운데 더 비침
    a = cv2.GaussianBlur(a.astype(np.float32), (0, 0), 0.8)
    return col, a


def over(canvas, col, a):
    return canvas * (1 - a[..., None]) + col * a[..., None]


bgB = grad4((233, 222, 252), (246, 226, 240), (255, 226, 210), (255, 238, 214))   # 연보라 → 살구
# 축: 띠 좌표에서 원점 (cx, cy), 한 칸 U px — 두 곡선이 y=x(오른쪽 위로 가는 대각선)에 대칭, 교차점이 오른쪽 위
U, cx, cy = 210.0, 980.0, 900.0
xs_ = np.linspace(-6.0, 2.35, 500)
exp_pts = np.stack([cx + U * xs_, cy - U * (2 ** xs_ - 0.0)], 1)                 # y = 2^x
log_pts = np.stack([cx + U * (2 ** xs_), cy - U * xs_], 1)                       # x = 2^y (역함수)
c_exp = [(0, (255, 156, 120)), (0.6, (255, 120, 150)), (1, (200, 110, 220))]     # 코랄 → 자홍 → 보라
c_log = [(0, (90, 200, 190)), (0.6, (110, 170, 240)), (1, (150, 130, 240))]      # 민트 → 하늘 → 보라
canvasB = bgB.copy()
col, a = tube_layer(log_pts, 62, c_log); canvasB = over(canvasB, col, a)
col, a = tube_layer(exp_pts, 62, c_exp); canvasB = over(canvasB, col, a)
# 둥근 알갱이 구 두 개(작은 강조)
for (ox, oy, rr, c1, c2) in ((250, 1180, 120, (255, 170, 140), (255, 236, 196)),):   # 오른쪽 위 작은 구는 얼룩처럼 보여 뺌
    gx, gy = np.meshgrid(np.arange(BW), np.arange(BH))
    dd = np.sqrt((gx - ox) ** 2 + (gy - oy) ** 2) / rr
    m = np.clip((1 - dd) * 60, 0, 1)                        # 가장자리 또렷하게(알갱이 결은 아래 잡음)
    tt = np.clip((gx - ox + gy - oy) / (2 * rr) + 0.5, 0, 1)[..., None]
    cc = np.array(c1, float) * (1 - tt) + np.array(c2, float) * tt
    cc = cc + rng.normal(0, 9, cc.shape)
    canvasB = canvasB * (1 - 0.85 * m[..., None]) + cc * (0.85 * m[..., None])
save(canvasB.clip(0, 255), "CLIMATH_대수_m_앞표지_시안B.png")
