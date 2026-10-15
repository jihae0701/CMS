# -*- coding: utf-8 -*-
"""그림 검사·고침: 글자(점 이름·숫자·식)가 선·곡선·축에 붙거나 겹치는 곳을 찾고, --fix면 글자를 옮긴다.  (KATEX_DIR 필요)
python 그림/figcheck.py [--fix] [파일.png ...]      (파일을 주지 않으면 모든 그림)

- 각 그림을 문서 폭 그대로(1픽셀=6.4 HWPUNIT) 다시 그려, 선만 있는 그림과 글자만 있는 그림을 따로 찍는다.
- 글자 모양(검은 픽셀)의 범위와 선 사이 간격이 GAP(화면 px)보다 좁으면 '붙음'(사용자: 선과 숫자가 겹치려 함).
- 축 글자 x, y와 원점 O는 약속된 자리(사용자 기준 그림)라 검사하지 않는다.
  길이 점선을 끊은 자리의 글자는 옮기지 않고 알리기만 한다(점선을 끊는 길이·휘는 정도로 고친다).
- --fix: 붙은 글자를 간격이 GAP 이상이고 다른 글자와 겹치지 않으며 그림 밖으로 나가지 않는 가장 가까운 자리로 옮기고,
  옮긴 양을 label_nudge.json에 적는다(draw.page가 그릴 때 더한다). 그 뒤 PNG를 다시 찍는 것은 각 draw*.py로 한다.
- 그림 크기도 함께 적는다: 문서에서 긴 변(HWPUNIT). 약속은 약 10000(8900~11000), 넓은 개념 그림·정육면체는 예외.
"""
import os, sys, io, json, importlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image
import draw
from playwright.sync_api import sync_playwright

GAP = 8             # 글자와 선 사이 최소 간격(화면 px; 글자 크기 22px)
REACH = 22          # 글자를 옮길 수 있는 최대 거리(화면 px)
MODULES = ["draw", "draw5", "draw6", "draw6y", "draw7y", "draw8", "draw8y", "draw9", "draw10", "draw10y", "draw11", "draw11y", "draw12", "draw12y"]
SKIP = {"image86.png"}          # 정육면체: 면을 채우는 식이라 검사하지 않음
AXIS = {"x", "y", r"\mathrm{O}"}
WIDE = {"g8_cases.png", "g9_roots.png", "image86.png"}     # 크기 약속의 예외(가로로 긴 개념 그림, 정육면체)


def collect():
    figs = []
    for m in MODULES:
        mod = importlib.import_module(m)
        for name, fn, wd in getattr(mod, "FIGS", ()):
            figs.append((m, mod, name, fn, wd))
    return figs


def integral(mask):
    return np.pad(mask.astype(np.int32).cumsum(0).cumsum(1), ((1, 0), (1, 0)))


def count(I, x0, y0, x1, y1):
    """[x0, x1] x [y0, y1] 안의 1의 개수(포함 범위, 그림 밖은 잘라냄)"""
    H, W = I.shape[0] - 1, I.shape[1] - 1
    x0, y0, x1, y1 = max(0, x0), max(0, y0), min(W - 1, x1), min(H - 1, y1)
    if x0 > x1 or y0 > y1:
        return 0
    return int(I[y1 + 1, x1 + 1] - I[y0, x1 + 1] - I[y1 + 1, x0] + I[y0, x0])


def gap_of(I, b, limit=GAP + 4):
    x0, y0, x1, y1 = b
    for d in range(0, limit + 1):
        if count(I, x0 - d, y0 - d, x1 + d, y1 + d):
            return d
    return limit + 1


def render(b, html, w, h):
    path = os.path.join(draw.HERE, "_check.html")
    open(path, "w", encoding="utf-8").write(html)
    pg = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)
    pg.goto("file://" + path)
    pg.wait_for_timeout(250)
    labs = pg.evaluate("""() => [...document.querySelectorAll('.lb')].map(e => {
        const r = e.getBoundingClientRect(); return [r.left, r.top, r.right, r.bottom, e.dataset.tex,
        +e.dataset.i, e.dataset.fixed === '1']})""")
    pg.evaluate("() => document.querySelectorAll('svg').forEach(e => e.style.visibility='hidden')")
    lab_png = pg.locator("#fig").screenshot()
    pg.evaluate("() => { document.querySelectorAll('svg').forEach(e => e.style.visibility='visible');"
                " document.querySelectorAll('.lb').forEach(e => e.style.visibility='hidden') }")
    st_png = pg.locator("#fig").screenshot()
    pg.close()
    st = np.array(Image.open(io.BytesIO(st_png)).convert("L")) < 150
    lb = np.array(Image.open(io.BytesIO(lab_png)).convert("L")) < 150
    out = []
    for x0, y0, x1, y1, tex, i, fixed in labs:
        sub = lb[max(0, int(y0)):int(y1) + 1, max(0, int(x0)):int(x1) + 1]
        ys, xs = np.nonzero(sub)
        if not len(xs):
            continue
        box = (int(x0) + xs.min(), int(y0) + ys.min(), int(x0) + xs.max(), int(y0) + ys.max())
        out.append((tex, i, fixed, box))
    return st, out


def run(only=None, fix=False):
    cap = {}
    real = draw.shoot

    def fake(html, w, h, out, scale=3):
        cap["v"] = (html, w, h)
    draw.shoot = fake
    rows = []
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=draw.CHROME)
        for m, mod, name, fn, wd in collect():
            if (only and name not in only) or name in SKIP:
                continue
            for rnd in range(3 if fix else 1):
                mod.fit_shoot(name, fn, wd) if m == "draw" else mod.fit_shoot(name, fn, wd, "/tmp")
                html, w, h = cap["v"]
                st, labs = render(b, html, w, h)
                I = integral(st)
                bad = [(tex, i, fixed, box, gap_of(I, box)) for tex, i, fixed, box in labs
                       if tex not in AXIS and gap_of(I, box) < GAP]
                out = [tex for tex, i, fixed, box in labs if box[0] < 2 or box[1] < 2 or box[2] > w - 3 or box[3] > h - 3]
                if not fix or not [x for x in bad if not x[2]]:
                    break
                # 붙은 글자 옮기기: 가까운 자리부터
                boxes = {i: box for tex, i, fixed, box in labs}
                nud = draw.NUDGE.setdefault(name, {})
                cands = sorted(((dx, dy) for dx in range(-REACH, REACH + 1) for dy in range(-REACH, REACH + 1)),
                               key=lambda t: t[0] * t[0] + t[1] * t[1])
                for tex, i, fixed, box, g in bad:
                    if fixed:
                        continue
                    others = [bx for j, bx in boxes.items() if j != i]
                    for dx, dy in cands:
                        nb = (box[0] + dx, box[1] + dy, box[2] + dx, box[3] + dy)
                        if nb[0] < 2 or nb[1] < 2 or nb[2] > w - 3 or nb[3] > h - 3:
                            continue
                        if gap_of(I, nb) < GAP:
                            continue
                        if any(not (nb[2] + 4 < o[0] or o[2] + 4 < nb[0] or nb[3] + 4 < o[1] or o[3] + 4 < nb[1]) for o in others):
                            continue
                        ox, oy = nud.get(str(i), (0, 0))
                        nud[str(i)] = [ox + dx, oy + dy]
                        boxes[i] = nb
                        break
                json.dump(draw.NUDGE, open(draw.NUDGE_FILE, "w", encoding="utf-8"), ensure_ascii=False, indent=1, sort_keys=True)
            size = int(max(w, h) * 3 * 6.4)
            rows.append((name, wd, size, [(t, g, f) for t, i, f, bx, g in bad] + [(t, -1, False) for t in out]))
        b.close()
    draw.shoot = real
    return rows


if __name__ == "__main__":
    args = sys.argv[1:]
    fix = "--fix" in args
    rows = run(set(a for a in args if a != "--fix") or None, fix)
    for name, wd, size, bad in rows:
        sz = "" if name in WIDE or 8900 <= size <= 11000 else "  크기 약속 밖"
        msg = ", ".join("%s(그림 밖으로 나감)" % t if g < 0 else "%s(간격 %dpx%s)" % (t, g, ", 점선 글자" if f else "")
                        for t, g, f in bad)
        print("%-16s 폭 %5d  긴 변 %5d%s  %s" % (name, wd, size, sz, "붙음: " + msg if bad else "ok"))
