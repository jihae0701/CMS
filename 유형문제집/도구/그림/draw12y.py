# -*- coding: utf-8 -*-
"""유형서 12단원(행렬) 그림. python 그림/draw12y.py [파일 ...]  (KATEX_DIR 필요)
- u12_fruit.png: n488 — [표1] 두 지역의 포도·딸기 개당 생산 비용, [표2] 개당 이익금
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from draw import HERE
from draw5 import fit_shoot
from draw12 import two, CW

HEAD = ["", "$\\mathrm{A}$ 지역", "$\\mathrm{B}$ 지역"]


def fig_fruit():
    return two((CW, [HEAD, ["포도", "$2000$", "$2200$"], ["딸기", "$3000$", "$3200$"]], "(단위: 원)", "[표1] 개당 생산 비용", None),
               (CW, [HEAD, ["포도", "$350$", "$290$"], ["딸기", "$850$", "$540$"]], "(단위: 원)", "[표2] 개당 이익금", None))


FIGS = (("u12_fruit.png", fig_fruit, 10000),)

if __name__ == "__main__":
    for name, fn, wd in FIGS:
        if len(sys.argv) > 1 and name not in sys.argv[1:]:
            continue
        fit_shoot(name, fn, wd, HERE)
