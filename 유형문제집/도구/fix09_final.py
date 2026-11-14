# -*- coding: utf-8 -*-
"""공통수학2 기본서 9단원 사용자 최종본(2026-11-14) 마무리: 323번 해설 (4)~(8) 추가, 스캔 그림 4장을 다시 그린 그림으로,
327번 문장·정답 표기 정리.  python fix09_final.py <입력.hwpx> <출력.hwpx>"""
import sys, os, re, zipfile, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from lite import Builder
from PIL import Image

src, out = sys.argv[1:3]
G = os.path.join(HERE, "그림")
# 323번 그래프 8개를 두 개씩 나란히 한 장으로
ims = [Image.open(os.path.join(G, "c2b9_323_%d.png" % k)).convert("RGB") for k in range(1, 9)]
gap = 30
W = max(ims[2 * r].width + ims[2 * r + 1].width for r in range(4)) + gap
H = sum(max(ims[2 * r].height, ims[2 * r + 1].height) for r in range(4)) + gap * 3
o = Image.new("RGB", (W, H), "white")
y = 0
for r in range(4):
    a, b = ims[2 * r], ims[2 * r + 1]
    o.paste(a, (0, y)); o.paste(b, (a.width + gap, y))
    y += max(a.height, b.height) + gap
comp = os.path.join(G, "c2b9_323.png")
o.save(comp)

z = zipfile.ZipFile(src)
items = [(i, z.read(i.filename)) for i in z.infolist()]
s = z.read("Contents/section0.xml").decode()
ens = list(re.finditer(r"<hp:endNote .*?</hp:endNote>", s, re.S))
e323 = ens[11].group(0)
assert "해설참조" in e323 and "(3) " in e323
B = Builder(s)
LINES = [
    "(4) $y= LEFT | ` LEFT | `x-1`RIGHT |- LEFT | `x-3`RIGHT | RIGHT |$에서",
    "   $x<1$일 때 $y= LEFT | -(x-1)+(x-3) RIGHT | =2$",
    "   $1 leq x<3$일 때 $y= LEFT | (x-1)+(x-3) RIGHT | = LEFT | 2x-4 RIGHT |$",
    "   $x geq 3$일 때 $y= LEFT | (x-1)-(x-3) RIGHT | =2$",
    "   따라서 $1 leq x<2$일 때 $y= it-2x+4$, $2 leq x<3$일 때 $y=2x-4$",
    "(5) $y= LEFT | x^{2} -1 RIGHT |$의 그래프는 $y=x^{2} -1$의 그래프에서",
    "   $x$축 아랫부분 $(-1<x<1)$을 $x$축 위로 접어 올린 것이다.",
    "(6) $LEFT | x RIGHT | ^{2} =x^{2}$이므로 $y= LEFT | x RIGHT | ^{2} -1=x^{2} -1$",
    "(7) $x geq 0$, $y geq 0$일 때 $x+y=4$이고, 그래프는 $x$축, $y$축,",
    "   원점에 대하여 대칭이므로 네 점 $(4,~0)$, $(0,~4)$, $(-4,~0)$, $(0,~-4)$를",
    "   꼭짓점으로 하는 정사각형이다.",
    "(8) $x geq 0$, $y geq 0$일 때 $x-2y=2$, 즉 $y= {1} over {2} x-1$ $(x geq 2)$이고,",
    "   그래프는 $x$축, $y$축, 원점에 대하여 대칭이다.",
]
for l in LINES:
    B.collect(l)
B.sizes()
po = '<hp:p id="2147483648" paraPrIDRef="23" styleIDRef="12" pageBreak="0" columnBreak="0" merged="0"><hp:run charPrIDRef="34">'
add = "".join(po + B.inline(l) + "</hp:run></hp:p>" for l in LINES)
paras = list(re.finditer(r"<hp:p .*?</hp:p>", e323, re.S))
picp = [m for m in paras if "<hp:pic" in m.group(0)][0]
e_new = e323[:picp.start()] + add + e323[picp.start():]
s = s[:ens[11].start()] + e_new + s[ens[11].end():]
# 327번 문장·정답
s = s.replace("<hp:t>의 그래프가 만나지 않도록 실수 하는 </hp:t>", "<hp:t>의 그래프가 만나지 않도록 하는 실수 </hp:t>", 1)
s = s.replace('<hp:script xml:space="preserve"> {-1&lt;m&lt;0</hp:script>', "<hp:script>-1&lt;m&lt;0</hp:script>", 1)
tmp = out + ".tmp.hwpx"
with zipfile.ZipFile(tmp, "w") as zo:
    for info, data in items:
        if info.filename == "Contents/section0.xml":
            data = s.encode("utf-8")
        zo.writestr(info, data, compress_type=info.compress_type)
sw = os.path.join(os.environ["S"], "swapimg.py")
subprocess.check_call([sys.executable, "-I", sw, tmp, out,
                       "image2=%s@10000" % os.path.join(G, "c2b9_314.png"),
                       "image3=%s@%d" % (comp, round(W * 6.4)),
                       "image4=%s@10000" % os.path.join(G, "c2b9_327.png"),
                       "image5=%s@8800" % os.path.join(G, "c2b9_329.png")])
os.remove(tmp)
print("->", out)
