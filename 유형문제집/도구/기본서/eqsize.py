# -*- coding: utf-8 -*-
"""수식 크기(HWPUNIT, 글자 크기 11pt 기준) — 도구/gen.py와 같은 환산"""
import json, os, sys
TOOL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOL)
CACHE = os.path.join(TOOL, "eqcache.json")
EQ = json.load(open(CACHE)) if os.path.exists(CACHE) else {}


def ensure(scripts):
    todo = sorted(set(s for s in scripts if s not in EQ))
    if not todo:
        return
    from eqmeasure import measure
    res, latex = measure(todo)
    for sc, r, lx in zip(todo, res, latex):
        if r[3]:
            print("수식 측정 근사:", sc, r[3][:80])
            r = [0.62 * len(sc) * 16 / 1.6, 18, 14, None]
        w, h, asc = r[0], r[1], r[2]
        W = int(68.8 * w + 61)
        if h > 20.5:
            H = int(max(1125, 57.14 * h + 303))
        elif "sqrt" in sc or "root" in sc:
            H = 1538
        elif "_" in sc:
            H = 1350
        elif "^" in sc:
            H = 1313
        else:
            H = 1125
        BL = int(max(50, min(90, 111.7 * (asc / h) - 2.6))) if h else 85
        EQ[sc] = (W, H, BL)
    json.dump(EQ, open(CACHE, "w"), ensure_ascii=False)


def size(sc, base=1100):
    W, H, BL = EQ[sc]
    k = base / 1100.0
    return int(W * k), int(H * k), BL
