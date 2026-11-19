# -*- coding: utf-8 -*-
"""CMStory 표지(미적분 Ⅰ 표지 이미지)를 공통수학1·2로 바꾸기 (2026-11-19).
python cmstory_cover.py <앞표지.jpg> <책등.jpg> <뒤(가운데 로고).jpg> <Pretendard 폴더> <출력 폴더>
- 사용자: 'CMStory 기출+변형 미적분 Ⅰ' 표지 이미지 3장(2000×2000)을 주고 '이걸 공통수학1, 2 만들어줘'.
- 파란 글자 '미적분 Ⅰ'(앞표지·뒤·책등)을 지우고 같은 자리·같은 글씨 기준선에 '공통수학1'/'공통수학2'를 Pretendard Bold로 씀
  (원래 글씨와 Pretendard Bold의 '미적분 Ⅰ'를 겹쳐 크기·기준선을 맞춘 뒤 같은 크기로). 앞표지는 오른쪽 끝, 뒤·책등은 시작점을 원래와 같게.
- 책등의 '고2' → '고1'(Pretendard Medium, 검정). 나머지(CMStory 글자·C 고리·CLIMATH 띠·CREVERSE 로고·'기출+변형')는 그대로.
"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

front, spine, back, fdir, outdir = sys.argv[1:6]
FONT = lambda w: os.path.join(fdir, "Pretendard-%s.otf" % w)
os.makedirs(outdir, exist_ok=True)


def ink_box(mask):
    ys, xs = np.nonzero(mask)
    return xs.min(), ys.min(), xs.max(), ys.max()


def find(img, box, kind):
    a = np.asarray(img.convert("RGB")).astype(int)
    x0, y0, x1, y1 = box
    s = a[y0:y1, x0:x1]
    if kind == "blue":
        m = (s[..., 2] > 200) & (s[..., 0] < 120) & (s[..., 1] < 160)
    else:
        m = s.sum(axis=2) < 300
    bx = ink_box(m)
    col = tuple(int(v) for v in np.median(s[m], axis=0))
    return (bx[0] + x0, bx[1] + y0, bx[2] + x0, bx[3] + y0), col


def render(text, font, rot):
    """글자를 흰 바탕 마스크로 (기준점 (0,0)에서 그린 위치 그대로), rot=-90이면 시계 방향으로 돌림"""
    W = int(font.size * len(text) * 1.4) + 40
    m = Image.new("L", (W, W), 0)
    ImageDraw.Draw(m).text((20, W // 2), text, font=font, fill=255, anchor="ls")    # 기준선 왼쪽 = (20, W/2)
    origin = (20, W // 2)
    if rot:
        m = m.rotate(rot, expand=True)                 # 정사각형이라 크기 같음: (x, y) → (W-1-y, x) (시계 방향 90°)
        origin = (W - 1 - origin[1], origin[0])
    return m, origin


def place(img, old_text, new_text, box, kind, weight, rot=0, align="left", pad=5):
    (bx, col) = find(img, box, kind)
    h = (bx[3] - bx[1] + 1) if not rot else (bx[2] - bx[0] + 1)          # 글자 높이(책등은 가로 폭)
    # 크기: Pretendard로 그린 옛 글자의 잉크 높이가 원래와 같도록
    size = 100
    for _ in range(3):
        f = ImageFont.truetype(FONT(weight), size)
        m, o = render(old_text, f, rot)
        ob = ink_box(np.asarray(m) > 128)
        hh = (ob[3] - ob[1] + 1) if not rot else (ob[2] - ob[0] + 1)
        size = size * h / hh
    f = ImageFont.truetype(FONT(weight), round(size, 1))
    m_old, o_old = render(old_text, f, rot)
    ob = ink_box(np.asarray(m_old) > 128)
    # 기준점 위치(원래 잉크 상자에 옛 글자 잉크 상자를 맞춤)
    if not rot:
        if align == "right":
            dx = bx[2] - ob[2]
        else:
            dx = bx[0] - ob[0]
        dy = bx[1] - ob[1]
    else:
        dx = bx[2] - ob[2]                              # 글자 위쪽이 오른쪽(시계 방향): 오른쪽 끝 맞춤
        dy = bx[1] - ob[1]                              # 시작(위) 맞춤
    m_new, o_new = render(new_text, f, rot)
    nb = ink_box(np.asarray(m_new) > 128)
    if not rot and align == "right":                    # 오른쪽 맞춤: 새 글자 오른쪽 끝을 원래 오른쪽 끝에
        dx = bx[2] - nb[2]
    # 지우기
    d = ImageDraw.Draw(img)
    d.rectangle((bx[0] - pad, bx[1] - pad, bx[2] + pad, bx[3] + pad), fill=(255, 255, 255))
    # 쓰기
    a = np.asarray(img).astype(float)
    mk = np.asarray(m_new).astype(float) / 255.0
    H, W = mk.shape
    X0, Y0 = int(round(dx)), int(round(dy))
    ys, xs = slice(max(0, Y0), min(a.shape[0], Y0 + H)), slice(max(0, X0), min(a.shape[1], X0 + W))
    mm = mk[ys.start - Y0:ys.stop - Y0, xs.start - X0:xs.stop - X0][..., None]
    a[ys, xs] = a[ys, xs] * (1 - mm) + np.array(col, float) * mm
    out = Image.fromarray(a.clip(0, 255).astype(np.uint8))
    nbox = (nb[0] + X0, nb[1] + Y0, nb[2] + X0, nb[3] + Y0)
    print("  %s → %s: 원래 %s 색 %s, 크기 %.1f, 새 글자 %s" % (old_text, new_text, bx, col, size, nbox))
    return out


for n in (1, 2):
    name = "공통수학%d" % n
    print(name)
    im = Image.open(front).convert("RGB")
    im = place(im, "미적분 Ⅰ", name, (1400, 250, 1880, 450), "blue", "Bold", align="right")
    im.save(os.path.join(outdir, "CMStory_%s_앞표지.png" % name))
    im = Image.open(back).convert("RGB")
    im = place(im, "미적분 Ⅰ", name, (1100, 800, 1450, 960), "blue", "Bold")
    im.save(os.path.join(outdir, "CMStory_%s_로고면.png" % name))
    im = Image.open(spine).convert("RGB")
    im = place(im, "미적분 Ⅰ", name, (500, 930, 600, 1100), "blue", "Bold", rot=-90)
    im = place(im, "고2", "고1", (500, 860, 620, 930), "dark", "Medium", rot=-90, pad=3)
    im.save(os.path.join(outdir, "CMStory_%s_책등.png" % name))
