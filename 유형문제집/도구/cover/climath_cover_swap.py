# -*- coding: utf-8 -*-
"""CLIMATH(c) 대수 ↔ 미적분Ⅰ 표지 바탕 맞바꾼 시안 (2026-11-26).
python climath_cover_swap.py <표지 폴더> <출력 폴더>
- 사용자: '대수랑 미적분1 서로 표지 바꿀까 봐'.
- 두 앞표지는 이제 틀이 같음(1474×2000, 큰 CLI MATH·ⓒ·제목 줄·로고 자리 같음) → 다른 책 앞표지에서 제목 글씨만 지우고 이 책 제목 글씨를 그 자리(두 줄 사이 가운데)에 얹음.
  · 대수 바탕(+미적분Ⅰ 제목): 대수 앞표지의 '대 수'를 지움(부드러운 그러데이션이라 메우기(inpaint)).
  · 미적분Ⅰ 바탕(+대수 제목): '미적분 Ⅰ'을 지움(원 아래 두 색 — 줄마다 왼쪽·오른쪽 색으로 채워 세로 경계 그대로).
- 책등: 이 책 책등의 검은 글씨(제목·ⓒ)를 떼어 다른 책 책등(그 책 글씨를 지운 것) 색 띠 위에. 위 CLIMATH·아래 cms는 같음.
- 뒤표지: 두 책 뒤표지는 색 띠 색만 다르므로 맞바꿔 복사.
"""
import os, sys
import numpy as np
import cv2
from PIL import Image

cdir, outdir = sys.argv[1:3]
os.makedirs(outdir, exist_ok=True)
BLACK = np.array((14.0, 16.0, 16.0))
lum = lambda a: a[..., 0] * 0.299 + a[..., 1] * 0.587 + a[..., 2] * 0.114
rd = lambda n: np.asarray(Image.open(os.path.join(cdir, n)).convert("RGB")).astype(float)
sv = lambda a, n: Image.fromarray(a.round().clip(0, 255).astype(np.uint8)).save(os.path.join(outdir, n))


def take(a, box, thr=120):
    """box 안 검은 글씨의 비율과 글씨를 메워 지운 바탕"""
    x0, y0, x1, y1 = box
    reg = a[y0:y1, x0:x1]
    dk = cv2.dilate((lum(reg) < thr).astype(np.uint8) * 255, np.ones((5, 5), np.uint8))
    B = cv2.inpaint(reg.clip(0, 255).astype(np.uint8), dk, 5, cv2.INPAINT_TELEA).astype(float)
    d = BLACK - B
    al = np.clip(((reg - B) * d).sum(axis=2) / np.maximum((d * d).sum(axis=2), 1.0), 0, 1) * (dk > 0)
    al[al < 0.04] = 0
    return al, B


TB = (470, 1452, 1005, 1568)                 # 두 제목 줄 사이(글씨만, 줄은 안 건드림)
alg, mi = rd("CLIMATH_c_대수_앞표지.png"), rd("CLIMATH_c_미적분1_앞표지.png")
a_alg, B_alg = take(alg, TB)
a_mi, _ = take(mi, TB)
# 미적분Ⅰ 바탕에서 제목 지우기: 줄마다 왼쪽·오른쪽 색(세로 경계 x 727)
x0, y0, x1, y1 = TB
B_mi = mi[y0:y1, x0:x1].copy()
REF = y0
for y in range(y0, y1):
    dl = np.median(mi[y, 400:440], axis=0) - np.median(mi[REF, 400:440], axis=0)
    dr = np.median(mi[y, 1080:1120], axis=0) - np.median(mi[REF, 1080:1120], axis=0)
    row = mi[REF, x0:x1].copy()
    row[:727 - x0] += dl; row[727 - x0:] += dr
    B_mi[y - y0] = row
# 대수 제목 + 미적분Ⅰ 바탕 / 미적분Ⅰ 제목 + 대수 바탕
f1 = mi.copy(); f1[y0:y1, x0:x1] = B_mi * (1 - a_alg[..., None]) + BLACK * a_alg[..., None]
f2 = alg.copy(); f2[y0:y1, x0:x1] = B_alg * (1 - a_mi[..., None]) + BLACK * a_mi[..., None]
# 2026-11-26 사용자 '색 바뀌는 경계에 흰 줄이 보이는 데가 있는지 확인': 받은 미적분Ⅰ 원본 그림(동그라미)은 가운데 색 경계 x 725에
# 1px 흰 줄(예: (255, 229, 213))과 그 옆 섞인 화소가 있음 → 줄마다 경계 왼쪽 723~724는 722의 색, 오른쪽 725~727은 728의 색으로 채움
# (검은 글자·흰 제목 줄이 지나가는 줄은 건드리지 않음)
for y in range(264, 1666):
    lc, rc = f1[y, 722].copy(), f1[y, 728].copy()
    if min(lum(lc[None])[0], lum(rc[None])[0]) < 120 or max(lc.min(), rc.min()) > 240:
        continue
    for x in (723, 724):
        if lum(f1[y, x][None])[0] > 120: f1[y, x] = lc
    for x in (725, 726, 727):
        if lum(f1[y, x][None])[0] > 120: f1[y, x] = rc
sv(f1, "바꿈_CLIMATH_c_대수_앞표지.png"); sv(f2, "바꿈_CLIMATH_c_미적분1_앞표지.png")

# 책등: 색 띠 안 글씨(제목·ⓒ) 바꿔 끼우기
SB = (1300, 480, 1414, 780)
s_alg, s_mi = rd("CLIMATH_c_대수_책등.png"), rd("CLIMATH_c_미적분1_책등.png")
sa_alg, sB_alg = take(s_alg, SB, 110)
sa_mi, sB_mi = take(s_mi, SB, 110)
# 미적분Ⅰ 책등 띠는 세로 그러데이션뿐(가로로 단색) → 메우기 자국(희미한 원)이 남지 않게 줄마다 글씨 없는 왼쪽(x 1200~1320) 색으로
sB_mi = np.repeat(np.median(s_mi[SB[1]:SB[3], 1200:1320], axis=1)[:, None, :], SB[2] - SB[0], axis=1)
x0, y0, x1, y1 = SB
g1 = s_mi.copy(); g1[y0:y1, x0:x1] = sB_mi * (1 - sa_alg[..., None]) + BLACK * sa_alg[..., None]
g2 = s_alg.copy(); g2[y0:y1, x0:x1] = sB_alg * (1 - sa_mi[..., None]) + BLACK * sa_mi[..., None]
sv(g1, "바꿈_CLIMATH_c_대수_책등.png"); sv(g2, "바꿈_CLIMATH_c_미적분1_책등.png")

# 뒤표지: 맞바꿈
sv(rd("CLIMATH_c_미적분1_뒤표지.png"), "바꿈_CLIMATH_c_대수_뒤표지.png")
sv(rd("CLIMATH_c_대수_뒤표지.png"), "바꿈_CLIMATH_c_미적분1_뒤표지.png")
print("-> 바꿈_CLIMATH_c_{대수,미적분1}_{앞표지,책등,뒤표지}.png")
