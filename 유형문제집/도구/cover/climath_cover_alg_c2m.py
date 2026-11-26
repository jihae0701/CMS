# -*- coding: utf-8 -*-
"""CLIMATH(m) 대수 표지 = CLIMATH(c) 대수 표지에서 ⓒ만 ⓜ로 (2026-11-26).
python climath_cover_alg_c2m.py <표지 폴더>
- 사용자: (시안 대신) '그냥 c 표지에 동그라미 m만 수정해서 올려 줘'.
- 앞표지: 큰 원(가운데 (916.5, 1190.5), 바깥 반지름 81, 안 반지름 약 59 — (m) 공통수학1 앞표지의 ⓜ와 자리·크기가 똑같음)은 그대로 두고,
  원 안(반지름 57)의 'c'를 지우고(어두운 화소를 둘레 바탕으로 메움) (m) 공통수학1 앞표지 원 안의 'm'(바탕을 메워 추정한 뒤 검정 비율로 떼어 냄)을 그대로 얹음.
- 책등: ⓒ(가운데 (1364.0, 636.5), 지름 33)를 통째로 지우고 (m) 공통수학1 책등의 ⓜ(가운데 (1364.5, 732))를 떼어 내 같은 높이, 가로는 책등 가운데 줄(1364.5)에 얹음.
- 뒤표지: ⓒ가 없어 그대로 복사. 나머지(그림·CLI MATH·'대수'·로고·제목 줄)는 CLIMATH(c) 대수 표지 그대로.
"""
import os, sys
import numpy as np
import cv2
from PIL import Image

cdir = sys.argv[1]
BLACK = np.array((14.0, 16.0, 16.0))
lum = lambda a: a[..., 0] * 0.299 + a[..., 1] * 0.587 + a[..., 2] * 0.114
load = lambda n: np.asarray(Image.open(os.path.join(cdir, n)).convert("RGB")).astype(float)


def dark_alpha(a, region_mask, thr=110):
    """region_mask 안의 검은 글자 비율과 글자를 지운 바탕"""
    L = lum(a)
    dk = ((L < thr) & region_mask).astype(np.uint8) * 255
    dk = cv2.dilate(dk, np.ones((5, 5), np.uint8))
    B = cv2.inpaint(a.clip(0, 255).astype(np.uint8), dk, 5, cv2.INPAINT_TELEA).astype(float)
    d = BLACK - B
    al = ((a - B) * d).sum(axis=2) / np.maximum((d * d).sum(axis=2), 1.0)
    al = np.clip(al, 0, 1) * (dk > 0)
    al[al < 0.04] = 0
    return al, B


# ---------------------------------------------------------------- 앞표지
c = load("CLIMATH_c_대수_앞표지.png")
m = load("CLIMATH_공통수학1_앞표지.png")
cx, cy, R = 916.5, 1190.5, 57.0
x0, y0, x1, y1 = int(cx - 70), int(cy - 70), int(cx + 71), int(cy + 71)
gy, gx = np.mgrid[y0:y1, x0:x1]
disc = np.hypot(gx - cx, gy - cy) <= R
_, Bc = dark_alpha(c[y0:y1, x0:x1], disc)                  # 'c' 지운 바탕
am, _ = dark_alpha(m[y0:y1, x0:x1], disc)                  # 'm' 비율
reg = c[y0:y1, x0:x1].copy()
reg[disc] = Bc[disc]
reg = reg * (1 - am[..., None]) + BLACK * am[..., None]
c[y0:y1, x0:x1] = reg
Image.fromarray(c.round().clip(0, 255).astype(np.uint8)).save(os.path.join(cdir, "CLIMATH_m_대수_앞표지.png"))

# ---------------------------------------------------------------- 책등
c = load("CLIMATH_c_대수_책등.png")
m = load("CLIMATH_공통수학1_책등.png")
def win(cx_, cy_, r=26):
    return int(cx_ - r), int(cy_ - r), int(cx_ + r + 1), int(cy_ + r + 1)
X0, Y0, X1, Y1 = win(1364.0, 636.5)
gy, gx = np.mgrid[Y0:Y1, X0:X1]
_, Bc = dark_alpha(c[Y0:Y1, X0:X1], np.hypot(gx - 1364.0, gy - 636.5) <= 19.5)   # ⓒ 통째로 지움
mx, my = 1364.5, 732.0
MX0, MY0, MX1, MY1 = win(mx, my)
gy2, gx2 = np.mgrid[MY0:MY1, MX0:MX1]
am, _ = dark_alpha(m[MY0:MY1, MX0:MX1], np.hypot(gx2 - mx, gy2 - my) <= 19.5)
tx, ty = 1364.5 - mx, 636.5 - my                            # 옮김(가로 0, 세로 −95.5)
M = np.float32([[1, 0, (MX0 - X0) + tx], [0, 1, (MY0 - Y0) + ty]])
am2 = cv2.warpAffine(am.astype(np.float32), M, (X1 - X0, Y1 - Y0), flags=cv2.INTER_LINEAR, borderValue=0)
c[Y0:Y1, X0:X1] = Bc * (1 - am2[..., None]) + BLACK * am2[..., None]
Image.fromarray(c.round().clip(0, 255).astype(np.uint8)).save(os.path.join(cdir, "CLIMATH_m_대수_책등.png"))

# ---------------------------------------------------------------- 뒤표지(그대로)
Image.open(os.path.join(cdir, "CLIMATH_c_대수_뒤표지.png")).save(os.path.join(cdir, "CLIMATH_m_대수_뒤표지.png"))
print("-> CLIMATH_m_대수_{앞표지,책등,뒤표지}.png")
