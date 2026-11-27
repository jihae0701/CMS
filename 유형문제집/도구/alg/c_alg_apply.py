# -*- coding: utf-8 -*-
"""CLIMATH(c) 대수 10단원에 CLIMATH(m) 대수 편집 상태를 맞춤(2026-11-27 사용자 '위 편집 상태에 맞게 대수(C) 파일 모두 수정').
바탕쪽 흰 네모 지움 → text2eq(글자 숫자·대문자·단위 → 수식, 각도 DEG → °) → num_inline(번호 옆 문제 시작, 내어 쓰기 16pt, 미주 표시 1pt).
python c_alg_apply.py [출력 폴더]
"""
import sys, os, re, zipfile, shutil, collections
sys.path.insert(0, "/home/user/CMS/유형문제집/도구/alg")
from drop_mp_whitebox import drop
from text2eq import convert_file as t2e
from num_inline import convert_file as ni
C = "/home/user/CMS/유형문제집/CLIMATH_c/대수/"
OUT = sys.argv[1] if len(sys.argv) > 1 else C          # 출력 폴더(기본: 제자리)
os.makedirs(OUT, exist_ok=True)
UP1 = C + "1. 지수_사용자수정본.hwpx"   # 2026-11-27 사용자가 올린 1단원 최신본
files = sorted([f for f in os.listdir(C) if f.endswith(".hwpx") and "사용자수정본" not in f], key=lambda f: int(f.split(".")[0]))
for f in files:
    src = UP1 if f.startswith("1. ") else C + f
    dst = OUT + f
    zi = zipfile.ZipFile(src); items = [(i, zi.read(i.filename)) for i in zi.infolist()]; zi.close()
    nb = 0
    for k, (i, d) in enumerate(items):
        if re.match(r"Contents/masterpage\d+\.xml", i.filename):
            x, n = drop(d.decode("utf-8")); nb += n; items[k] = (i, x.encode("utf-8"))
    with zipfile.ZipFile(dst, "w") as zo:
        for i, d in items: zo.writestr(i, d, compress_type=zipfile.ZIP_STORED if i.filename == "mimetype" else zipfile.ZIP_DEFLATED)
    a = t2e(dst, dst)
    b = ni(dst, dst)
    s = zipfile.ZipFile(dst).read("Contents/section0.xml").decode()
    en = s.count("<hp:endNote ")
    print("%-22s 흰네모 %d | 수식으로 %d | 번호옆 붙임 %d / 미주 %d" % (f, nb, a, b, en))
