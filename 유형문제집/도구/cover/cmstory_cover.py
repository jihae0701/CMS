# -*- coding: utf-8 -*-
"""CMStory 표지(미적분 Ⅰ 표지 이미지)를 공통수학1·2로 바꾸기 (2026-11-19).
python cmstory_cover.py <앞표지.jpg> <책등.jpg> <뒤(가운데 로고).jpg> <Pretendard 폴더> <출력 폴더>
- 사용자: 'CMStory 기출+변형 미적분 Ⅰ' 표지 이미지 3장(2000×2000)을 주고 '이걸 공통수학1, 2 만들어줘'.
- 파란 글자 '미적분 Ⅰ'(앞표지·뒤·책등)을 지우고 같은 자리·같은 글씨 기준선에 '공통수학1'/'공통수학2'를 Pretendard Bold로 씀
  (원래 글씨와 Pretendard Bold의 '미적분 Ⅰ'를 겹쳐 크기·기준선을 맞춘 뒤 같은 크기로). 앞표지는 오른쪽 끝, 뒤·책등은 시작점을 원래와 같게.
- 사용자 '크레버스 로고 빼고 이걸로해줘': CREVERSE 로고(앞표지 오른쪽 아래·로고면 아래 가운데·책등 아래)를 지우고 cms 교과 로고를 같은 높이로
  (앞표지는 오른쪽 끝 맞춤, 로고면은 가운데, 책등은 시계 방향으로 돌려 가운데).
- 사용자 '파랑 대신에 색깔은 각 유형서 메인색을 써': 파란 부분(책 이름 글자·C 고리·책등 띠)을 유형서 머리말의 '고1' 상자 색으로 —
  공통수학1 #F38623(주황, 사용자 IDML 단원 표지 색과 같음), 공통수학2 #207B4D(초록). 화소마다 흰색·파랑(52,114,253)·검정의 섞임으로 풀어
  파랑 몫만 메인색으로 바꿈(흰 글자·검은 글자·회색 그림자는 그대로, 고리의 옅은 선은 옅은 메인색).
- 사용자 '기출 +변형 대신 유형+기출'(앞표지·로고면): 원래 '기출'과 '+'는 그 화소를 그대로 옮기고 '유형'만 Pretendard SemiBold로 씀
  (원래 '변형'과 같은 크기·기준선으로 맞춤). 순서 '유형 + 기출', 낱말 사이 간격은 원래대로. 앞표지는 오른쪽 끝 맞춤, 로고면은 왼쪽 끝 맞춤.
- 책등의 '고2' → '고1'(Pretendard Medium, 검정) — 2026-11-19 사용자 요청으로 학년 표시는 없애고 책 이름을 그 자리(시작 883px)로 올림.
- 유형서 라이트(8번째 인수 = 필기체 글꼴): 책등의 책 이름 뒤에 얇은 필기체 'Lite'(Sacramento, 메인색)를 더한 책등을 따로 저장.
- 책등 띠의 '기출모음집' → '유형문제집'(흰 글씨 Pretendard SemiBold, 같은 크기·시작점), 책등의 cms 로고만 80%(가운데 그대로). 나머지(CMStory 글자·C 고리·CLIMATH 띠·CREVERSE 로고·'기출+변형')는 그대로.
"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

front, spine, back, fdir, outdir = sys.argv[1:6]
SCRIPT = sys.argv[8] if len(sys.argv) > 8 else None       # 2026-11-19 사용자 '유형서 라이트 표지는 책등에만, 공통수학1 뒤에 얇고 필기체 같은 Lite' — 필기체 글꼴(Sacramento)
LOGO_SPINE = sys.argv[7] if len(sys.argv) > 7 else None   # 2026-11-19 사용자 '책등은 cms 로고 다른 걸로' — 책등 전용 로고(없으면 LOGO)
LOGO = sys.argv[6] if len(sys.argv) > 6 else None          # 2026-11-19 사용자 'CREVERSE 로고 빼고 이걸로' — cms 교과 로고(PNG, 투명 바탕)
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
    elif kind == "white":
        m = s.min(axis=2) > 200
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


def place(img, old_text, new_text, box, kind, weight, rot=0, align="left", pad=5, start=None):
    """start: 책등(rot)에서 새 글자 시작(위) 높이를 따로 줄 때"""
    (bx, col) = find(img, box, kind)
    _a = np.asarray(img.convert("RGB")).astype(int)[box[1]:box[3], box[0]:box[2]]
    bg = (255, 255, 255) if kind != "white" else tuple(int(v) for v in np.median(_a[_a.min(axis=2) < 180], axis=0))   # 흰 글자는 띠 색으로 지움
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
        if start is not None:
            dy = start - ob[1]
    m_new, o_new = render(new_text, f, rot)
    nb = ink_box(np.asarray(m_new) > 128)
    if not rot and align == "right":                    # 오른쪽 맞춤: 새 글자 오른쪽 끝을 원래 오른쪽 끝에
        dx = bx[2] - nb[2]
    # 지우기
    d = ImageDraw.Draw(img)
    d.rectangle((bx[0] - pad, bx[1] - pad, bx[2] + pad, bx[3] + pad), fill=bg)
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


def tagline(img, w1, plus, w2, align, pad=4):
    """'기출 + 변형' → '유형 + 기출'. w1·plus·w2 = 원래 '기출'·'+'·'변형'의 잉크 상자 (x0, y0, x1, y1)"""
    a = np.asarray(img).astype(float)
    blk = lambda b: a[b[1]:b[3] + 1, b[0]:b[2] + 1].copy()
    gi, pl = blk(w1), blk(plus)
    g1, g2 = plus[0] - w1[2] - 1, w2[0] - plus[2] - 1                   # 원래 간격(기출↔+, +↔변형)
    # '유형' 크기: Pretendard SemiBold '변형' 잉크 높이를 원래 '변형'과 같게
    h = w2[3] - w2[1] + 1
    size = 50.0
    for _ in range(3):
        f = ImageFont.truetype(FONT("SemiBold"), size)
        ob = ink_box(np.asarray(render("변형", f, 0)[0]) > 128)
        size = size * h / (ob[3] - ob[1] + 1)
    f = ImageFont.truetype(FONT("SemiBold"), round(size, 1))
    mo, _ = render("변형", f, 0); ob = ink_box(np.asarray(mo) > 128)
    mn, _ = render("유형", f, 0); nb = ink_box(np.asarray(mn) > 128)
    # 2026-11-19 사용자 '미묘하게 줄 안 맞는 것도 수정'(아는체는 '안 바꿀게'): '기출'도 원래 화소 대신 같은 글꼴·같은 기준선으로 씀
    mg, _ = render("기출", f, 0); gb = ink_box(np.asarray(mg) > 128)
    dy = w2[1] - ob[1]                                                     # 기준선: 원래 '변형'과 같게(두 낱말 모두)
    wn = nb[2] - nb[0] + 1
    W1, WP = gb[2] - gb[0] + 1, plus[2] - plus[0] + 1
    total = wn + g1 + WP + g2 + W1
    if align == "right":
        left = w2[2] - total + 1
    else:
        left = w1[0]
    xs_new, xs_plus, xs_gi = left, left + wn + g1, left + wn + g1 + WP + g2
    col = np.median(gi[gi.sum(axis=2) < 300], axis=0)
    # 지우기
    X0 = min(w1[0], xs_new) - pad; X1 = max(w2[2], xs_gi + W1 - 1) + pad
    Y0 = min(w1[1], plus[1], w2[1]) - pad; Y1 = max(w1[3], plus[3], w2[3]) + pad
    a[Y0:Y1 + 1, X0:X1 + 1] = 255
    # 기출·+ 옮기기(어두운 쪽 남기기)
    def put(block, x, y):
        H_, W_ = block.shape[:2]
        a[y:y + H_, x:x + W_] = np.minimum(a[y:y + H_, x:x + W_], block)
    put(pl, xs_plus, plus[1])
    # 유형·기출 쓰기(같은 기준선)
    for mask, bb_, x_ in ((mn, nb, xs_new), (mg, gb, xs_gi)):
        mk = np.asarray(mask).astype(float) / 255.0
        ox = x_ - bb_[0]
        H_, W_ = mk.shape
        sub = a[dy:dy + H_, ox:ox + W_]
        m3 = mk[:sub.shape[0], :sub.shape[1]][..., None]
        a[dy:dy + H_, ox:ox + W_] = sub * (1 - m3) + col * m3
    print("  유형+기출: 유형 %d~%d, + %d~%d, 기출 %d~%d (크기 %.1f)" % (xs_new, xs_new + wn - 1, xs_plus, xs_plus + WP - 1, xs_gi, xs_gi + W1 - 1, size))
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))


def lite_mark(img, color, gap=10, k=1.15):
    """책등의 '공통수학N' 바로 뒤(아래)에 얇은 필기체 'Lite'. 크기: 'Lite' 잉크 높이 = 책 이름 글자 높이 × 1.15, 아랫선(책등에서 왼쪽 끝)을 책 이름과 맞춤"""
    a = np.asarray(img).astype(float)
    x0, y0, x1, y1 = 500, 860, 600, 1300
    m = np.abs(a[y0:y1, x0:x1] - np.array(color, float)).sum(axis=2) < 60
    ys, xs = np.nonzero(m)
    bx = (x0 + xs.min(), y0 + ys.min(), x0 + xs.max(), y0 + ys.max())
    h = bx[2] - bx[0] + 1
    size = 60.0
    for _ in range(3):
        f = ImageFont.truetype(SCRIPT, size); bb = f.getbbox("Lite"); size *= h * k / (bb[3] - bb[1])
    f = ImageFont.truetype(SCRIPT, size); bb = f.getbbox("Lite")
    mk = Image.new("L", (bb[2] + 20, bb[3] + 20), 0)
    ImageDraw.Draw(mk).text((10, 10), "Lite", font=f, fill=255)
    mk = mk.rotate(-90, expand=True)
    lb = ink_box(np.asarray(mk) > 128)
    X, Y = bx[0] - lb[0], bx[3] + gap - lb[1]
    m3 = np.asarray(mk).astype(float)[..., None] / 255.0
    H_, W_ = m3.shape[:2]
    a[Y:Y + H_, X:X + W_] = a[Y:Y + H_, X:X + W_] * (1 - m3) + np.array(color, float) * m3
    print("  Lite: 책 이름 %s 뒤 (%d, %d, %d, %d), 크기 %.1f" % (bx, X + lb[0], Y + lb[1], X + lb[2], Y + lb[3], size))
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))


MAIN = {1: (243, 123, 15), 2: (32, 123, 77)}   # 공통수학1: #F38623에서 채도만 0.86 → 0.94(같은 색상·밝기) — 2026-11-19 사용자 '공수1 메인주황 채도 조금 높여'
BLUE = np.array((52, 114, 253), float)


def recolor(img, target):
    a = np.asarray(img).astype(float) - 255.0
    u, v = BLUE - 255.0, np.array((-255.0, -255.0, -255.0))
    M = np.stack([u, v], axis=1)                                   # 3×2
    coef = np.linalg.lstsq(M, a.reshape(-1, 3).T, rcond=None)[0]    # 2×N: 파랑 몫 b, 검정 몫 k
    b, k = np.clip(coef[0], 0, None), np.clip(coef[1], 0, None)
    blue = b > 0.02
    fit = (M @ np.stack([b, k])).T
    resid = a.reshape(-1, 3) - fit
    new = np.outer(b, np.array(target, float) - 255.0) + np.outer(k, v) + resid * (~blue)[:, None]
    out = a.reshape(-1, 3).copy()
    out[blue] = new[blue]
    return Image.fromarray((out.reshape(a.shape) + 255.0).clip(0, 255).astype(np.uint8))


def logo(img, box, align, rot=0, pad=6, scale=1.0, path=None):
    path = path or LOGO
    if not path:
        return img
    lg = Image.open(path).convert("RGBA")
    al = np.asarray(lg)[..., 3]
    ys, xs = np.nonzero(al > 10)
    lg = lg.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
    if rot:
        lg = lg.rotate(rot, expand=True)
    x0, y0, x1, y1 = box
    if not rot:
        h = y1 - y0 + 1; w = round(lg.width * h / lg.height)
    else:
        w = x1 - x0 + 1; h = round(lg.height * w / lg.width)
    w, h = round(w * scale), round(h * scale)
    lg = lg.resize((w, h), Image.LANCZOS)
    ImageDraw.Draw(img).rectangle((x0 - pad, y0 - pad, x1 + pad, y1 + pad), fill=(255, 255, 255))
    cy = (y0 + y1) / 2; cx = (x0 + x1) / 2
    X = x1 + 1 - w if align == "right" else round(cx - w / 2)
    Y = round(cy - h / 2)
    img.paste(lg, (int(X), int(Y)), lg)
    print("  로고: CREVERSE %s → cms 로고 (%d, %d, %d, %d)" % (box, X, Y, X + w - 1, Y + h - 1))
    return img


for n in (1, 2):
    name = "공통수학%d" % n
    print(name)
    im = Image.open(front).convert("RGB")
    im = place(im, "미적분 Ⅰ", name, (1400, 250, 1880, 450), "blue", "Bold", align="right")
    im = tagline(im, (1550, 190, 1644, 242), (1681, 197, 1714, 229), (1733, 192, 1815, 238), "right")
    im = recolor(im, MAIN[n])
    im = logo(im, (1634, 1823, 1833, 1862), "right")
    im.save(os.path.join(outdir, "CMStory_%s_앞표지.png" % name))
    im = Image.open(back).convert("RGB")
    im = place(im, "미적분 Ⅰ", name, (1100, 800, 1450, 960), "blue", "Bold")
    im = tagline(im, (818, 765, 874, 795), (887, 768, 905, 787), (917, 765, 966, 792), "left")
    im = recolor(im, MAIN[n])
    im = logo(im, (895, 1762, 1095, 1800), "center")
    im.save(os.path.join(outdir, "CMStory_%s_로고면.png" % name))
    im = Image.open(spine).convert("RGB")
    # 2026-11-19 사용자 '책등 고1 표시 없애고 공통수학 글씨 위로 올리고 / 기출모음집 대신 유형문제집 / 책등의 cms 로고만 80%로 축소'
    ImageDraw.Draw(im).rectangle((535, 880, 556, 916), fill=(255, 255, 255))          # '고2' 지움(고1 표시 없음)
    im = place(im, "미적분 Ⅰ", name, (500, 930, 600, 1100), "blue", "Bold", rot=-90, start=883)   # 옛 '고2' 자리에서 시작
    im = place(im, "기출모음집", "유형문제집", (520, 220, 580, 360), "white", "SemiBold", rot=-90, pad=3)
    im = recolor(im, MAIN[n])
    im = logo(im, (530, 1665, 566, 1852), "center", rot=-90, scale=0.8, path=LOGO_SPINE)
    im.save(os.path.join(outdir, "CMStory_%s_책등.png" % name))
    if SCRIPT:                                                     # 유형서 라이트: 책등만 다름(앞표지·로고면은 유형서와 같음)
        lite_mark(im, MAIN[n]).save(os.path.join(outdir, "CMStory_%s_라이트_책등.png" % name))
