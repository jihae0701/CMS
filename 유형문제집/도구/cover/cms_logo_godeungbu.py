# -*- coding: utf-8 -*-
"""cms 교과 로고 → cms 고등부 로고 (2026-11-19).
python cms_logo_godeungbu.py <cms_교과_로고.png> <Pretendard 폴더> <출력.png>
- 사용자: 'cms 로고에서 교과 대신 고등부라 쓰고 음영 크기 적당히 조절, 음영 부분 아주 짙은 회색, m 부분 파랑 부분 테두리 검정 안에 흰색으로'.
- m의 파란 획(#00AAE7): 안은 흰색, 둘레는 검정 테두리(원본 1200px 기준 7px).
- 오른쪽 둥근 음영(알약 모양): 아주 짙은 회색 #232323, 글자 '고등부'(흰색, Pretendard Bold, 원래 '교과'와 같은 글자 높이),
  음영 높이·둥근 정도·좌우 여백은 원래와 같게 두고 너비만 세 글자에 맞게 늘림. 'cms'의 회색(#414042)은 그대로.
"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

src, fdir, out = sys.argv[1:4]
im = Image.open(src).convert("RGBA")
a = np.asarray(im).astype(float)
rgb, al = a[..., :3], a[..., 3]
X = np.arange(a.shape[1])[None, :]

# ---- m의 파란 획: 흰색 + 검정 테두리
wc = np.clip((rgb[..., 2] - rgb[..., 0]) / 231.0, 0, 1) * (X < 760)          # 파랑 몫(색 기준)
hard = ((wc > 0.5) & (al > 128)).astype(np.uint8) * 255
R = 7
inner = Image.fromarray(hard, "L").filter(ImageFilter.MinFilter(2 * R + 1)).filter(ImageFilter.GaussianBlur(1.0))
E = np.asarray(inner).astype(float) / 255.0                                     # 1 = 안쪽(흰색), 0 = 테두리(검정)
target = E[..., None] * 255.0                                                   # 흰색~검정
gray = np.array((65.0, 64.0, 66.0))
mix = wc[..., None] * target + (1 - wc[..., None]) * gray
sel = wc > 0.02
rgb2 = rgb.copy()
rgb2[sel] = mix[sel]

# ---- 오른쪽 음영 지우고 새로
PILL_X0, PILL_Y0, PILL_Y1 = 806, 114, 225
pill_h = PILL_Y1 - PILL_Y0 + 1
old_text_h = 207 - 134 + 1
pad_x = 862 - PILL_X0                                                           # 원래 좌우 여백 56
f = ImageFont.truetype(os.path.join(fdir, "Pretendard-Bold.otf"), 100)
bb = f.getbbox("교과", anchor="ls")
size = 100 * old_text_h / (bb[3] - bb[1])
f = ImageFont.truetype(os.path.join(fdir, "Pretendard-Bold.otf"), size)
tb = f.getbbox("고등부", anchor="ls")
tw = tb[2] - tb[0]
pill_w = tw + 2 * pad_x
W = max(a.shape[1], PILL_X0 + pill_w + 120)
base = np.zeros((a.shape[0], W, 4))
base[:, :a.shape[1], :3] = rgb2
base[:, :a.shape[1], 3] = al
base[:, 760:, 3] = 0                                                            # 옛 음영·글자 지움
logo = Image.fromarray(base.clip(0, 255).astype(np.uint8), "RGBA")

S = 4                                                                           # 4배로 그려 줄여 매끈하게
big = Image.new("RGBA", (W * S, a.shape[0] * S), (0, 0, 0, 0))
d = ImageDraw.Draw(big)
d.rounded_rectangle((PILL_X0 * S, PILL_Y0 * S, (PILL_X0 + pill_w) * S - 1, (PILL_Y1 + 1) * S - 1), radius=pill_h * S // 2, fill=(35, 35, 35, 255))
fb = ImageFont.truetype(os.path.join(fdir, "Pretendard-Bold.otf"), size * S)
tbb = fb.getbbox("고등부", anchor="ls")
cx, cy = (PILL_X0 + pill_w / 2) * S, (PILL_Y0 + PILL_Y1 + 1) / 2 * S
d.text((cx - (tbb[0] + tbb[2]) / 2, cy - (tbb[1] + tbb[3]) / 2), "고등부", font=fb, fill=(255, 255, 255, 255), anchor="ls")
pill = big.resize((W, a.shape[0]), Image.LANCZOS)
logo = Image.alpha_composite(logo, pill)
logo.save(out)
print("음영 %d~%d × %d~%d (너비 %d, 원래 275), 글자 크기 %.1f -> %s" % (PILL_X0, PILL_X0 + pill_w - 1, PILL_Y0, PILL_Y1, pill_w, size, out))
