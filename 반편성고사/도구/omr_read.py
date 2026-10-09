# -*- coding: utf-8 -*-
"""답안지 스캔 판독: 객관식 1~14번에 학생이 표시한 번호를 읽는다.
- 스캔(PDF 여러 쪽 또는 JPG/PNG)마다 표 테두리를 찾아 기울기를 바로잡고, ①~⑤ 칸의 잉크 양을 비교
- 표시가 없거나 두 개 이상이면 '확인 필요'로 표시하고, 확인용 그림(이름 칸 + 해당 줄)을 만든다
사용: python omr_read.py <출력폴더> <스캔파일...>
결과: <출력폴더>/판독결과.json, 확인_XX.png (쪽마다 이름 칸과 판독 결과)
"""
import sys, os, json, subprocess, tempfile, glob
import numpy as np
import cv2

W = 1654                       # 처리 기준 폭(A4 200dpi)
N_MC = 14

def load_pages(path):
    if path.lower().endswith(".pdf"):
        tmp = tempfile.mkdtemp()
        subprocess.run(["pdftoppm", "-r", "200", "-gray", "-png", path, os.path.join(tmp, "p")], check=True)
        for f in sorted(glob.glob(os.path.join(tmp, "p*.png"))):
            yield "%s#%d" % (os.path.basename(path), int(f.rsplit("-", 1)[1].split(".")[0])), cv2.imread(f, cv2.IMREAD_GRAYSCALE)
    else:
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            raise SystemExit("그림을 열 수 없음: " + path)
        yield os.path.basename(path), img

def ink(gray):
    """어두운 부분 = 1 (조명 차이를 줄이려고 배경을 나눠 정규화)"""
    bg = cv2.medianBlur(gray, 51)
    norm = cv2.divide(gray, bg, scale=255)
    _, b = cv2.threshold(norm, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    return b

def lines(b, horiz, length):
    k = cv2.getStructuringElement(cv2.MORPH_RECT, (length, 1) if horiz else (1, length))
    return cv2.morphologyEx(b, cv2.MORPH_OPEN, k)

def deskew(gray):
    """가로 투영의 날카로움이 가장 큰 각도로 회전(표 가로선이 수평이 되도록)"""
    b = ink(gray)
    small = cv2.resize(b, (b.shape[1] // 2, b.shape[0] // 2), interpolation=cv2.INTER_AREA)
    hgt, wid = small.shape
    def score(ang):
        M = cv2.getRotationMatrix2D((wid / 2, hgt / 2), ang, 1.0)
        r = cv2.warpAffine(small, M, (wid, hgt), flags=cv2.INTER_NEAREST, borderValue=0)
        prof = r.sum(1).astype(float)
        return float((prof ** 2).sum())
    best = max(np.arange(-6, 6.01, 0.25), key=score)
    best = max(np.arange(best - 0.25, best + 0.251, 0.05), key=score)
    M = cv2.getRotationMatrix2D((gray.shape[1] / 2, gray.shape[0] / 2), float(best), 1.0)
    return cv2.warpAffine(gray, M, (gray.shape[1], gray.shape[0]), flags=cv2.INTER_CUBIC, borderValue=255)

def tables(b):
    """표 테두리 → [(x, y, w, h, 가로선 y목록, 세로선 x목록)]"""
    hl = lines(b, True, 60)
    vl = lines(b, False, 40)
    grid = cv2.dilate(hl | vl, np.ones((5, 5), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(grid)
    out = []
    for i in range(1, n):
        x, y, w, h, a = st[i]
        if w < 200 or h < 40:
            continue
        def runs(prof, minlen):
            idx = np.nonzero(prof > minlen)[0]
            if not len(idx):
                return []
            groups, cur = [], [idx[0]]
            for v in idx[1:]:
                if v - cur[-1] <= 3:
                    cur.append(v)
                else:
                    groups.append(cur); cur = [v]
            groups.append(cur)
            return [int(np.mean(g)) for g in groups]
        hy = runs(hl[y:y + h, x:x + w].sum(1) / 255, w * 0.6)
        vx = runs(vl[y:y + h, x:x + w].sum(0) / 255, h * 0.6)
        out.append((x, y, w, h, [y + v for v in hy], [x + v for v in vx]))
    return out

def read_page(gray):
    scale = W / gray.shape[1]
    gray = cv2.resize(gray, (W, int(gray.shape[0] * scale)), interpolation=cv2.INTER_AREA)
    gray = deskew(gray)
    b = ink(gray)
    T = tables(b)
    mc = sorted([t for t in T if len(t[4]) == 8 and len(t[5]) >= 3], key=lambda t: t[0])
    if len(mc) != 2:
        return {"error": "객관식 표를 찾지 못함(찾은 표 %d개)" % len(mc)}, gray
    cells = []
    for t in mc:
        xs = t[5]
        x0, x1 = xs[1], xs[-1]
        for r in range(7):
            y0, y1 = t[4][r], t[4][r + 1]
            cells.append((x0, y0, x1, y1))
    # 칸 크기를 맞춰 겹친 뒤, 행마다 다른 위치에 있는 표시는 중앙값으로 지워져 인쇄된 ①~⑤만 남음
    CW, CH = 420, 48
    crops = []
    for (x0, y0, x1, y1) in cells:
        m = 6
        c = b[y0 + m:y1 - m, x0 + m:x1 - m]
        crops.append(cv2.resize(c, (CW, CH), interpolation=cv2.INTER_AREA).astype(float) / 255)
    stack = np.array(crops)
    tmpl = np.median(stack, axis=0)
    prof = tmpl.sum(0)
    on = prof > max(0.6, prof.max() * 0.08)
    segs, i = [], 0
    while i < CW:
        if on[i]:
            j = i
            while j < CW and on[j]:
                j += 1
            segs.append([i, j]); i = j
        else:
            i += 1
    # 가까운 조각을 합쳐 5개 글자로
    while len(segs) > 5:
        gaps = [segs[k + 1][0] - segs[k][1] for k in range(len(segs) - 1)]
        k = int(np.argmin(gaps)); segs[k] = [segs[k][0], segs[k + 1][1]]; del segs[k + 1]
    if len(segs) != 5:
        lo, hi = (np.nonzero(on)[0][[0, -1]] if on.any() else (40, CW - 40))
        step = (hi - lo) / 5
        segs = [[int(lo + k * step), int(lo + (k + 1) * step)] for k in range(5)]
    centers = [(s[0] + s[1]) / 2 for s in segs]
    half = min(np.diff(centers)) / 2 if len(centers) > 1 else 20
    answers, conf, flags = [], [], []
    for q, c in enumerate(stack):
        extra = []
        for cx in centers:
            a, z = int(max(0, cx - half)), int(min(CW, cx + half))
            extra.append(float(np.clip(c[:, a:z] - tmpl[:, a:z], 0, None).sum()))
        glyph = float(tmpl[:, int(centers[0] - half):int(centers[0] + half)].sum()) or 1.0
        e = np.array(extra) / glyph                 # 인쇄된 글자 하나의 잉크 양 기준
        order = np.argsort(e)[::-1]
        med = float(np.median(e))
        d1, d2 = float(e[order[0]] - med), float(e[order[1]] - med)   # 가장 진한 칸·둘째 칸이 나머지보다 얼마나 진한가
        conf.append(round(d1 - d2, 2))
        if d1 < 0.25:
            answers.append(None); flags.append("표시 없음")
        elif d2 > 0.3:
            answers.append(None); flags.append("두 개 이상 표시(%d·%d번)" % (order[0] + 1, order[1] + 1))
        else:
            answers.append(int(order[0]) + 1)
            flags.append("흐림·확인" if d1 < 0.35 or d2 > 0.2 else "")
    # 이름 칸(머리 표 중 가장 오른쪽 표의 둘째 칸)
    head = sorted([t for t in T if len(t[4]) == 2 and t[1] < mc[0][1]], key=lambda t: t[0])
    name_box = None
    if head and len(head[-1][5]) >= 3:
        t = head[-1]
        name_box = (t[5][1], t[4][0], t[5][-1], t[4][1])
    return {"answers": answers, "conf": conf, "flags": flags, "cells": cells, "name_box": name_box,
            "head": [(t[5][1], t[4][0], t[5][-1], t[4][1]) for t in head if len(t[5]) >= 3]}, gray

def review_image(gray, res, label, path):
    """확인용: 머리 칸(현재반·학교·이름) + 판독 결과를 표시한 객관식 표"""
    vis = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    for q, (x0, y0, x1, y1) in enumerate(res["cells"]):
        a, fl = res["answers"][q], res["flags"][q]
        col = (0, 140, 0) if not fl else (0, 0, 230)
        cv2.rectangle(vis, (x0, y0), (x1, y1), col, 3 if fl else 1)
        txt = "%s" % (a if a else "-")
        cv2.putText(vis, txt, (x1 + 8, (y0 + y1) // 2 + 12), cv2.FONT_HERSHEY_SIMPLEX, 1.1, col, 3)
    ys = [c[1] for c in res["cells"]] + [c[3] for c in res["cells"]]
    top = max(0, min([h[1] for h in res["head"]] + [min(ys)]) - 20)
    crop = vis[top:max(ys) + 20, :]
    cv2.putText(crop, label, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (200, 0, 0), 3)
    cv2.imwrite(path, cv2.resize(crop, (crop.shape[1] // 2, crop.shape[0] // 2), interpolation=cv2.INTER_AREA))

def main(outdir, files):
    os.makedirs(outdir, exist_ok=True)
    results = []
    k = 0
    for f in files:
        for label, img in load_pages(f):
            k += 1
            res, gray = read_page(img)
            item = {"no": k, "source": label}
            if "error" in res:
                item["error"] = res["error"]
                print("%2d %s  오류: %s" % (k, label, res["error"]))
            else:
                item.update(answers=res["answers"], flags=res["flags"], conf=res["conf"])
                review_image(gray, res, "%d  %s" % (k, label), os.path.join(outdir, "확인_%02d.png" % k))
                bad = [q + 1 for q, fl in enumerate(res["flags"]) if fl]
                print("%2d %s  %s%s" % (k, label, "".join(str(a) if a else "-" for a in res["answers"]),
                                        "  확인 필요: %s" % bad if bad else ""))
            results.append(item)
    json.dump(results, open(os.path.join(outdir, "판독결과.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
