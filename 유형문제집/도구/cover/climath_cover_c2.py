# -*- coding: utf-8 -*-
"""CLIMATH(m) 공통수학2 표지(앞·책등·뒤)를 공통수학1 표지에서 만들기 (2026-11-19).
python climath_cover_c2.py <공통수학1 앞(로고 바꾼 것)> <공통수학1 책등(로고 바꾼 것)> <공통수학1 뒤> <새 바탕 그림> <Pretendard 폴더> <둥근 글꼴(숫자)> <출력 폴더>
- 사용자: '공통수학2 앞, 뒤, 책등 만들어줘. 위의 공통수학1과 같은 형태인데 아래 깔린 이미지를 이걸로 해'(파랑 리본 그림, 보라→하늘→연두 바탕).
- 앞표지: 색 띠(y 260~1665)의 바탕만 새 그림으로. 앞에 놓인 것(검은 CLI MATH 글자, ⓜ 원, 제목 줄 두 개, '공통수학1' 흰 글씨+검은 테두리)은
  원래 그림에서 떼어 내어(바탕을 메워 추정한 뒤 화소마다 '검정/흰색 × 비율 + 바탕'으로 풀어 비율을 구함) 새 바탕 위에 그대로 얹음.
  새 그림은 띠 높이에 맞춰 줄이고(×0.773) 오른쪽 끝을 맞춰 자름(리본이 오른쪽에 오게).
  제목 '1' → '2': 원래 글꼴(둥근 글씨)이 없어 숫자만 M PLUS Rounded 1c Bold(같은 둥근 모양, '1'과 높이·테두리 두께를 맞춤)로 쓰고, 제목 전체를 두 줄 사이 가운데로 다시 맞춤.
- 책등·뒤표지: 색 띠(단색 그러데이션)를 새 그림 왼쪽 끝 세로 색(앞표지 띠 왼쪽 끝과 같은 색)으로 바꿈. 책등 '공통수학 1' → '공통수학 2'(숫자만 Pretendard Bold로 다시 씀).
  로고(CLIMATH, cms)와 ⓜ는 그대로.
"""
import os, sys
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

front, spine, back, newbg, pdir, rfont, outdir = sys.argv[1:8]
FRONT_BG = sys.argv[8] if len(sys.argv) > 8 else None      # 2026-11-19: 앞표지 띠 바탕을 따로 짠 그림(make_bg_c2.py, 띠 크기)
SUFFIX = sys.argv[9] if len(sys.argv) > 9 else ""
os.makedirs(outdir, exist_ok=True)
BLACK = np.array((14.0, 16.0, 16.0))
WHITE = np.array((252.0, 252.0, 252.0))
lum = lambda a: a[..., 0] * 0.299 + a[..., 1] * 0.587 + a[..., 2] * 0.114

bg_src = np.asarray(Image.open(newbg).convert("RGB")).astype(float)


def bg_fill(w, h, align="right"):
    sc = max(w / bg_src.shape[1], h / bg_src.shape[0])
    im = Image.fromarray(bg_src.astype(np.uint8)).resize((round(bg_src.shape[1] * sc), round(bg_src.shape[0] * sc)), Image.LANCZOS)
    x = im.width - w if align == "right" else (im.width - w) // 2
    return np.asarray(im.crop((x, 0, x + w, h))).astype(float)


def bg_strip(w, h):
    """새 그림 왼쪽 끝(리본 없는 곳)의 세로 색 → 높이 h, 폭 w의 띠"""
    col = bg_src[:, 5:120].mean(axis=1)                     # 줄마다 평균색
    col = cv2.resize(col[:, None, :].astype(np.float32), (1, h), interpolation=cv2.INTER_AREA)[:, 0, :]
    return np.repeat(col[:, None, :], w, axis=1).astype(float)


def separate(a, white_boxes=(), dark_boxes=None):
    """원래 띠 a(H×W×3)에서 앞에 놓인 검정·흰색을 떼어 냄 → (비율, 앞색).
    dark_boxes: 검정을 찾을 곳(옛 고리 그림의 어두운 테두리선이 섞이지 않게). 검정은 아주 진한 곳(밝기<40)에서 시작해 둘레(밝기<130)로 넓힘."""
    L = lum(a)
    core = L < 40
    if dark_boxes is not None:
        keep = np.zeros_like(core)
        for (x0, y0, x1, y1) in dark_boxes:
            keep[y0:y1, x0:x1] = True
        core &= keep
    dark = (cv2.dilate(core.astype(np.uint8), np.ones((5, 5), np.uint8)) > 0) & (L < 130)
    white = np.zeros_like(dark)
    near = cv2.dilate(dark.astype(np.uint8), np.ones((15, 15), np.uint8)) > 0     # 흰 속은 검은 테두리 바로 안쪽만(유리 반사광 빼기)
    for (x0, y0, x1, y1) in white_boxes:
        white[y0:y1, x0:x1] = (L[y0:y1, x0:x1] > 225) & near[y0:y1, x0:x1]
    fg = (dark | white).astype(np.uint8) * 255
    fg = cv2.dilate(fg, np.ones((7, 7), np.uint8))
    B = cv2.inpaint(a.clip(0, 255).astype(np.uint8), fg, 6, cv2.INPAINT_TELEA).astype(float)
    F = np.where((L < lum(B))[..., None], BLACK, WHITE)
    if white_boxes:
        allow = np.zeros_like(dark)
        for (x0, y0, x1, y1) in white_boxes:
            allow[y0:y1, x0:x1] = True
        F = np.where((~allow)[..., None], BLACK, F)
    else:
        F = np.broadcast_to(BLACK, a.shape).copy()
    d = F - B
    alpha = ((a - B) * d).sum(axis=2) / np.maximum((d * d).sum(axis=2), 1.0)
    alpha = np.clip(alpha, 0, 1) * (fg > 0)
    alpha[alpha < 0.04] = 0
    return alpha, F


def compose(bg, alpha, F):
    return bg * (1 - alpha[..., None]) + F * alpha[..., None]


def ink(mask):
    ys, xs = np.nonzero(mask)
    return xs.min(), ys.min(), xs.max(), ys.max()


# ================================================================ 앞표지
im = np.asarray(Image.open(front).convert("RGB")).astype(float)
Y0, Y1 = 260, 1666
band = im[Y0:Y1].copy()
H, W = band.shape[:2]
TXT = (560, 1460 - Y0, 920, 1560 - Y0)                     # 제목 글씨 둘레(띠 안 좌표)
LETTERS = (450, 460 - Y0, 1015, 1285 - Y0)                 # CLI MATH 글자와 ⓜ
alpha, F = separate(band, [TXT], [LETTERS, TXT])         # 제목 줄 두 개는 떼어 내지 않고 아래에서 새로 그림
# 제목: '공통수학1'의 잉크 범위와 '1'
tx0, ty0, tx1, ty1 = TXT
tmask = alpha[ty0:ty1, tx0:tx1] > 0.5
gx0, gy0, gx1, gy1 = ink(tmask)
cols = tmask.any(axis=0)
runs, st = [], None
for i, c in enumerate(cols):
    if c and st is None: st = i
    if not c and st is not None: runs.append((st, i - 1)); st = None
if st is not None: runs.append((st, len(cols) - 1))
one = runs[-1]                                              # 마지막 덩어리 = '1'
oy = np.nonzero(tmask[:, one[0]:one[1] + 1].any(axis=1))[0]
one_box = (tx0 + one[0], ty0 + oy.min(), tx0 + one[1], ty0 + oy.max())
print("앞표지 제목 잉크", (tx0 + gx0, ty0 + gy0 + Y0, tx0 + gx1, ty0 + gy1 + Y0), "'1'", (one_box[0], one_box[1] + Y0, one_box[2], one_box[3] + Y0))
# '1' 지우기
alpha[one_box[1] - 2:one_box[3] + 3, one_box[0] - 2:one_box[2] + 3] = 0
# '2' 그리기(흰 글씨 + 검은 테두리): '1'을 같은 글꼴로 그려 높이를 맞춘 크기
stroke = 2
h1 = one_box[3] - one_box[1] + 1
size = 60.0
for _ in range(4):
    f = ImageFont.truetype(rfont, size)
    m = Image.new("L", (400, 300), 0); ImageDraw.Draw(m).text((50, 250), "1", font=f, fill=255, anchor="ls", stroke_width=stroke)
    b = ink(np.asarray(m) > 128)
    size *= h1 / (b[3] - b[1] + 1)
f = ImageFont.truetype(rfont, size)
fill_m = Image.new("L", (400, 300), 0); ImageDraw.Draw(fill_m).text((50, 250), "2", font=f, fill=255, anchor="ls")
out_m = Image.new("L", (400, 300), 0); ImageDraw.Draw(out_m).text((50, 250), "2", font=f, fill=255, anchor="ls", stroke_width=stroke)
one_m = Image.new("L", (400, 300), 0); ImageDraw.Draw(one_m).text((50, 250), "1", font=f, fill=255, anchor="ls", stroke_width=stroke)
ob = ink(np.asarray(one_m) > 128); nb = ink(np.asarray(out_m) > 128)
dy = one_box[3] - ob[3]                                     # 아랫선 맞춤
dx = one_box[0] - nb[0]                                     # 왼쪽 시작 맞춤
A_out = np.asarray(out_m).astype(float) / 255.0
A_fill = np.asarray(fill_m).astype(float) / 255.0
hh, ww = A_out.shape
sub = (slice(dy, dy + hh), slice(dx, dx + ww))
a_o = alpha[sub]; F_o = F[sub]
# 흰 속 + 검은 테두리: 앞색 = 흰(속) 또는 검정(테두리), 비율 = 테두리 포함 모양
newF = np.where((A_fill > 0.5)[..., None], WHITE, BLACK)
newF = A_fill[..., None] * WHITE + (1 - A_fill[..., None]) * BLACK
mix = np.maximum(a_o, A_out)
F[sub] = np.where((A_out > a_o)[..., None], newF, F_o)
alpha[sub] = mix
# 제목 전체를 두 줄 사이 가운데로
tmask2 = alpha[ty0:ty1, tx0:tx1] > 0.5
g2 = ink(tmask2)
# 제목 줄: 원래 그림에서 잰 자리(흰 속 + 검은 테두리 약 1.5px), x 455~1020, y 1441~1447 / 1573~1578
RULES = [(455, 1441, 1020, 1447), (455, 1573, 1020, 1578)]
line_c = (455 + 1020) / 2
cur_c = tx0 + (g2[0] + g2[2]) / 2
shift = int(round(line_c - cur_c))
if shift:
    ta, tF = alpha[ty0:ty1, tx0:tx1].copy(), F[ty0:ty1, tx0:tx1].copy()
    alpha[ty0:ty1, tx0:tx1] = 0
    alpha[ty0:ty1, tx0 + shift:tx1 + shift] = np.maximum(alpha[ty0:ty1, tx0 + shift:tx1 + shift], ta)
    F[ty0:ty1, tx0 + shift:tx1 + shift] = np.where((ta > 0)[..., None], tF, F[ty0:ty1, tx0 + shift:tx1 + shift])
print("  '2' 크기 %.1f, 제목 가운데 맞춤 %+dpx (줄 가운데 %.1f)" % (size, shift, line_c))
newband = compose(np.asarray(Image.open(FRONT_BG).convert("RGB")).astype(float)[:H, :W] if FRONT_BG else bg_fill(W, H, "right"), alpha, F)
SS = 4
for (x0, y0, x1, y1) in RULES:
    pw, ph = (x1 - x0 + 7) * SS, (y1 - y0 + 7) * SS
    big = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
    ImageDraw.Draw(big).rectangle((3 * SS, 3 * SS, (x1 - x0 + 4) * SS - 1, (y1 - y0 + 4) * SS - 1), fill=(252, 252, 252, 255), outline=(14, 16, 16, 255), width=6)
    sm = np.asarray(big.resize((x1 - x0 + 7, y1 - y0 + 7), Image.LANCZOS)).astype(float)
    a_ = sm[..., 3:4] / 255.0
    yy0, xx0 = y0 - 3 - Y0, x0 - 3
    reg = newband[yy0:yy0 + sm.shape[0], xx0:xx0 + sm.shape[1]]
    newband[yy0:yy0 + sm.shape[0], xx0:xx0 + sm.shape[1]] = reg * (1 - a_) + sm[..., :3] * a_
im[Y0:Y1] = newband
Image.fromarray(im.clip(0, 255).astype(np.uint8)).save(os.path.join(outdir, "CLIMATH_공통수학2_앞표지%s.png" % SUFFIX))
FRONT_LEFT_TOP = newband[5, 2]

# ================================================================ 책등
im = np.asarray(Image.open(spine).convert("RGB")).astype(float)
SY0, SY1, SX0, SX1 = 261, 1667, 1178, 1414
band = im[SY0:SY1, SX0:SX1].copy()
alpha, F = separate(band)
# '1' (세로 글씨: 위→아래) 찾기 — 글씨 덩어리 중 짧은 것(y 680~688)
m = alpha > 0.5
rows = m.any(axis=1)
runs, st = [], None
for i, r in enumerate(rows):
    if r and st is None: st = i
    if not r and st is not None: runs.append((st, i - 1)); st = None
txt_runs = [r for r in runs if 540 - SY0 - 20 <= r[0] <= 760 - SY0]
one = min(txt_runs, key=lambda r: r[1] - r[0])
ox = np.nonzero(m[one[0]:one[1] + 1].any(axis=0))[0]
one_box = (ox.min(), one[0], ox.max(), one[1])
print("책등 '1'", (SX0 + one_box[0], SY0 + one_box[1], SX0 + one_box[2], SY0 + one_box[3]))
alpha[one_box[1] - 2:one_box[3] + 3, one_box[0] - 2:one_box[2] + 3] = 0
fp = os.path.join(pdir, "Pretendard-Bold.otf")
gh = one_box[2] - one_box[0] + 1                            # '1'의 글자 높이(책등에선 가로 폭)
size = 30.0
for _ in range(4):
    f = ImageFont.truetype(fp, size)
    mm = Image.new("L", (200, 200), 0); ImageDraw.Draw(mm).text((50, 150), "1", font=f, fill=255, anchor="ls")
    b = ink(np.asarray(mm.rotate(-90, expand=True)) > 128)
    size *= gh / (b[2] - b[0] + 1)
f = ImageFont.truetype(fp, size)
def rot_mask(t):
    mm = Image.new("L", (200, 200), 0); ImageDraw.Draw(mm).text((50, 150), t, font=f, fill=255, anchor="ls")
    return np.asarray(mm.rotate(-90, expand=True)).astype(float) / 255.0
m1, m2 = rot_mask("1"), rot_mask("2")
b1, b2 = ink(m1 > 0.5), ink(m2 > 0.5)
X = one_box[0] - b1[0]                                      # 아랫선(책등에선 왼쪽) 맞춤 — '1'과 같은 기준
Y = one_box[1] - b2[1]                                      # 시작(위) 맞춤
c0 = min(b1[0], b2[0]) - 3                                  # 잉크 둘레만 잘라 씀
m2 = m2[:, c0:b2[2] + 4]; X += c0; b2 = (b2[0] - c0, b2[1], b2[2] - c0, b2[3])
hh, ww = m2.shape
sub = (slice(Y, Y + hh), slice(X, X + ww))
alpha[sub] = np.maximum(alpha[sub], m2)
F[sub] = BLACK
print("  책등 '2' 크기 %.1f → (%d, %d, %d, %d)" % (size, SX0 + X + b2[0], SY0 + Y + b2[1], SX0 + X + b2[2], SY0 + Y + b2[3]))
im[SY0:SY1, SX0:SX1] = compose(bg_strip(SX1 - SX0, SY1 - SY0), alpha, F)
Image.fromarray(im.clip(0, 255).astype(np.uint8)).save(os.path.join(outdir, "CLIMATH_공통수학2_책등.png"))

# ================================================================ 뒤표지
im = np.asarray(Image.open(back).convert("RGB")).astype(float)
BY0, BY1, BX0, BX1 = 256, 1662, 1172, 1474
band = im[BY0:BY1, BX0:BX1].copy()
alpha, F = separate(band)
im[BY0:BY1, BX0:BX1] = compose(bg_strip(BX1 - BX0, BY1 - BY0), alpha, F)
Image.fromarray(im.clip(0, 255).astype(np.uint8)).save(os.path.join(outdir, "CLIMATH_공통수학2_뒤표지.png"))
print("뒤표지 띠", (BX0, BY0, BX1, BY1), "앞에 놓인 것", int((alpha > 0.5).sum()), "화소")
