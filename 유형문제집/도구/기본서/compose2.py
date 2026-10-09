# -*- coding: utf-8 -*-
"""기본서 2단원 = 나머지정리(C): 오류 수정, 문항 번호 다시 매기기, 단원 번호 3→2

사용: python compose2.py 3.나머지정리.hwpx 출력.hwpx
"""
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hwpxio as io, fixes, numbering as nb, fixC

C, OUT = sys.argv[1:3]   # 나머지정리.hwpx, 출력
f, o = io.read(C)
sec = f["Contents/section0.xml"].decode("utf-8")
head, P, tail = io.split(sec)
P = [io.nolines(p) for p in P]
P, logC = fixes.apply(P, fixC.FIX, "C")
assert "3. 나머지정리" in io.text(P[-2])
P[-2] = P[-2].replace("3. 나머지정리", "2. 나머지정리")
# 유형 04 제목의 조사
for i, p in enumerate(P):
    if "이용하여 나머지 구하기" in io.text(p):
        P[i] = p.replace("를 이용하여 나머지 구하기", "을 이용하여 나머지 구하기")
tmpl = next(p for p in P if nb.num_text(p) and "<hp:container" not in p)
P, nprob, nins = nb.renumber(P, tmpl)
print("문항", nprob, "번호 새로 넣음", nins)
f["Contents/section0.xml"] = (head + "".join(P) + tail).encode("utf-8")
for mp in ("Contents/masterpage0.xml", "Contents/masterpage1.xml"):
    x = f[mp].decode("utf-8").replace("<hp:t>3. 나머지정리</hp:t>", "<hp:t>2. 나머지정리</hp:t>")
    f[mp] = x.encode("utf-8")
io.write(OUT, f, o)
print("문단", len(P), "->", OUT)
