# -*- coding: utf-8 -*-
"""공통수학2 유형서 10단원(합성함수와 역함수) 완성본(2026-11-14) 등록.  python fix10y_final.py <입력.hwpx> <출력.hwpx>  (환경변수 S: swapimg.py 위치)
- 미주 시작 527 → 522(9단원 유형서 463~521에 이어지게, 번호 값만 −5)
- 붙여 넣은 스캔 그림 9장을 다시 그린 그림(도구/그림/draw2_10y.py)으로: image2(528), 3(542 해설), 5(558 해설), 6(558), 7(568 해설),
  8(577 해설), 9(577), 10(587), 11(589 해설). image1(로고), image4(보기 아이콘)는 그대로.
- 573번 정답 줄 '[정답] \' 오타, 589번 해설 'triangle{rmPQR'(닫히지 않은 중괄호) → 'triangle rm PQR'
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
n = s.count("<hp:t> [정답] \\</hp:t>")
s = s.replace("<hp:t> [정답] \\</hp:t>", "<hp:t> [정답] </hp:t>")      # 573번 정답 앞 '\' 오타
print("정답 앞 \\ 지움:", n)
for t in ("PQR", "PRQ"):                                             # 589번 해설 수식의 닫히지 않은 중괄호
    s = s.replace(">triangle{rm%s</hp:script>" % t, ">triangle rm %s</hp:script>" % t)
tmp = out + ".tmp.hwpx"
with zipfile.ZipFile(tmp, "w") as zo:
    for info, data in items:
        if info.filename == "Contents/section0.xml":
            data = s.encode("utf-8")
        zo.writestr(info, data, compress_type=info.compress_type)
W = {"image2": ("c2y10_528.png", 7000), "image3": ("c2y10_542.png", 7000), "image5": ("c2y10_558s.png", 10000),
     "image6": ("c2y10_558p.png", 10000), "image7": ("c2y10_568.png", 8500), "image8": ("c2y10_577s.png", 10000),
     "image9": ("c2y10_577p.png", 10000), "image10": ("c2y10_587.png", 15000), "image11": ("c2y10_589.png", 10000)}
subprocess.check_call([sys.executable, "-I", os.path.join(os.environ["S"], "swapimg.py"), tmp, out] +
                      ["%s=%s@%d" % (k, os.path.join(G, f), w) for k, (f, w) in W.items()])
os.remove(tmp)
print("->", out)
