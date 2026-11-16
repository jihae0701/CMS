# -*- coding: utf-8 -*-
"""공통수학2 11단원(유리식과 유리함수) 기본서·유형서 완성본(2026-11-16) 등록.
python fix11_final.py 기본서.hwpx 기본서_출력.hwpx 유형서.hwpx 유형서_출력.hwpx   (환경변수 S: swapimg.py 위치)
기본서(미주 395~435, 10단원 394에 이어짐 — 번호는 그대로)
- 붙여 넣은 스캔 그림 2장을 다시 그린 그림(도구/그림/draw2_11.py)으로: image2(400번 해설), image4(409번 해설)
- 해설 첫 줄 '[정답]'(굵은 11pt) 7곳 → '󰂼'(다른 문항과 같은 10pt)
유형서
- 미주 시작 590 → 585(10단원 유형서 522~584에 이어지게, 번호 값만 −5) → 585~643
- 붙여 넣은 스캔 그림 6장을 다시 그린 그림으로: image3(596번 문제), 4(615번 해설), 5(623번 해설), 6(628번 해설), 7·8(633번 해설)
- 628번 문제 수식 '{rmA{ LEFT ( -1 ,~1 RIGHT )'(닫히지 않은 중괄호 둘) → 'rm A LEFT ( -1 ,~1 RIGHT )',
  해설 수식 '=2overline {rm PB'}'(붙여 써서 한 낱말로 읽힘) → '=2 overline {rm PB'}'
"""
import sys, os, re, zipfile, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
G = os.path.join(HERE, "그림")
bsrc, bout, ysrc, yout = sys.argv[1:5]
SW = os.path.join(os.environ["S"], "swapimg.py")


def rewrite(src, dst, fn):
    z = zipfile.ZipFile(src)
    items = [(i, z.read(i.filename)) for i in z.infolist()]
    with zipfile.ZipFile(dst, "w") as zo:
        for info, data in items:
            if info.filename == "Contents/section0.xml":
                data = fn(data.decode("utf-8")).encode("utf-8")
            zo.writestr(info, data, compress_type=info.compress_type)


def b_fix(s):
    n = [0]

    def ans(m):
        n[0] += 1
        return m.group(0).replace('<hp:run charPrIDRef="%s">' % m.group(1), '<hp:run charPrIDRef="18">', 1).replace("<hp:t> [정답] </hp:t>", "<hp:t> 󰂼 </hp:t>", 1)
    s = re.sub(r'<hp:run charPrIDRef="(7[34])"><hp:ctrl><hp:autoNum num="\d+" numType="ENDNOTE">.*?<hp:t> \[정답\] </hp:t>', ans, s, flags=re.S)
    print("기본서 [정답] → 󰂼:", n[0], "남은 [정답]:", s.count("[정답]"))
    return s


def y_fix(s):
    D = -5
    sub = lambda pat, x: re.sub(pat, lambda m: m.group(1) + str(int(m.group(2)) + D) + m.group(3), x)
    s = sub(r'(<hp:newNum num=")(\d+)(" numType="ENDNOTE")', s)
    s = sub(r'(<hp:autoNum num=")(\d+)(" numType="ENDNOTE")', s)
    s = sub(r'(<hp:endNote number=")(\d+)(")', s)
    s = re.sub(r'(<hp:endNotePr>.*?newNum=")(\d+)(")', lambda m: m.group(1) + str(int(m.group(2)) + D) + m.group(3), s, count=1, flags=re.S)
    for a, b in ((">{rmA{ LEFT ( -1 ,~1 RIGHT )<", ">rm A LEFT ( -1 ,~1 RIGHT )<"),
                 (">overline {rm PC} =2overline {rm PB'}<", ">overline {rm PC} =2 overline {rm PB'}<")):
        assert s.count(a) == 1, a
        s = s.replace(a, b)
    return s


for src, dst, fn, W in ((bsrc, bout, b_fix, {"image2": ("c2b11_400.png", 9500), "image4": ("c2b11_409.png", 9500)}),
                        (ysrc, yout, y_fix, {"image3": ("c2y11_596.png", 11000), "image4": ("c2y11_615.png", 11000),
                                             "image5": ("c2y11_623.png", 11000), "image6": ("c2y11_628.png", 11000),
                                             "image7": ("c2y11_633a.png", 9000), "image8": ("c2y11_633b.png", 9000)})):
    tmp = dst + ".tmp.hwpx"
    rewrite(src, tmp, fn)
    subprocess.check_call([sys.executable, "-I", SW, tmp, dst] + ["%s=%s@%d" % (k, os.path.join(G, f), w) for k, (f, w) in W.items()])
    os.remove(tmp)
    print("->", dst)
