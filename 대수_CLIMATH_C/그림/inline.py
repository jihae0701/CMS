# -*- coding: utf-8 -*-
"""본문 속 수식 그림(스캔한 식 줄, 답 상자 등): KaTeX로 찍고 테두리를 잘라 낸다. 폭은 원래 그림 폭을 그대로 쓴다."""
import sys, os, json
sys.path.insert(0, '/home/user/CMS/.claude/skills/math-figure-rules')
import mathfig
from PIL import Image


def shoot_tex(tex, out, size=40, w=2400, h=200):
    labels = [(10, h / 2, tex, size, 'lc')]
    html = mathfig.page('<svg width="%d" height="%d"></svg>' % (w, h), labels, w, h)
    mathfig.shoot(html, w, h, out)
    im = Image.open(out).convert('RGB'); g = im.convert('L').point(lambda v: 255 if v < 245 else 0)
    b = g.getbbox(); pad = 6
    im.crop((max(0, b[0] - pad), max(0, b[1] - pad), min(im.width, b[2] + pad), min(im.height, b[3] + pad))).save(out)


def run_inline(items, OUT, widths):
    wf = os.path.join(OUT, 'widths.json'); W = json.load(open(wf)) if os.path.exists(wf) else {}
    for k, tex in items.items():
        shoot_tex(tex, os.path.join(OUT, k + '.png'))
        W[k] = widths[k]; print(k, W[k])
    json.dump(W, open(wf, 'w'), indent=0)
