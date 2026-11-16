# -*- coding: utf-8 -*-
"""공통수학2 유형서 12단원(무리식과 무리함수) 완성본(2026-11-16) 등록.  python fix12y_final.py <입력.hwpx> <출력.hwpx>  (환경변수 S: swapimg.py 위치)
- 미주 시작 649 → 644(11단원 유형서 585~643에 이어지게, 번호 값만 −5) → 644~698
- 붙여 넣은 스캔 그림 7장을 다시 그린 그림(도구/그림/draw2_12y.py)으로: image3(659 문제), 4(662 해설), 5(662 문제), 6(672 해설), 7(677 해설), 8(678 해설), 9(693 문제)
  image1(로고), image2(보기 아이콘)는 그대로.
"""
import sys, os, re, zipfile, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
G = os.path.join(HERE, "그림")
src, out = sys.argv[1:3]
D = -5
z = zipfile.ZipFile(src)
items = [(i, z.read(i.filename)) for i in z.infolist()]
s = z.read("Contents/section0.xml").decode()
sub = lambda pat, x: re.sub(pat, lambda m: m.group(1) + str(int(m.group(2)) + D) + m.group(3), x)
s = sub(r'(<hp:newNum num=")(\d+)(" numType="ENDNOTE")', s)
s = sub(r'(<hp:autoNum num=")(\d+)(" numType="ENDNOTE")', s)
s = sub(r'(<hp:endNote number=")(\d+)(")', s)
s = re.sub(r'(<hp:endNotePr>.*?newNum=")(\d+)(")', lambda m: m.group(1) + str(int(m.group(2)) + D) + m.group(3), s, count=1, flags=re.S)
tmp = out + ".tmp.hwpx"
with zipfile.ZipFile(tmp, "w") as zo:
    for info, data in items:
        if info.filename == "Contents/section0.xml":
            data = s.encode("utf-8")
        zo.writestr(info, data, compress_type=info.compress_type)
W = {"image3": ("c2y12_659.png", 10000), "image4": ("c2y12_662s.png", 9000), "image5": ("c2y12_662p.png", 10000),
     "image6": ("c2y12_672.png", 15000), "image7": ("c2y12_677.png", 9000), "image8": ("c2y12_678.png", 9000), "image9": ("c2y12_693.png", 10000)}
subprocess.check_call([sys.executable, "-I", os.path.join(os.environ["S"], "swapimg.py"), tmp, out] +
                      ["%s=%s@%d" % (k, os.path.join(G, f), w) for k, (f, w) in W.items()])
os.remove(tmp)
print("->", out)
