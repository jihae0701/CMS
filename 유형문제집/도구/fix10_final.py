# -*- coding: utf-8 -*-
"""공통수학2 기본서 10단원(합성함수와 역함수) 사용자 최종본(2026-11-14) 마무리.  python fix10_final.py <입력.hwpx> <출력.hwpx>  (환경변수 S: swapimg.py 위치)
- 붙여 넣은 스캔 그림 11장을 다시 그린 그림(도구/그림/draw2_10b.py)으로 바꿈: image2(369 f·g 나란히), 3(370 문제), 4(370 해설), 6(373 문제), 7·8(373 해설),
  9(383), 10(384), 11(386), 12·13(394)
- 해설에 그래프를 새로 넣음(그림 문단은 370번 해설의 그림 문단을 본뜸): 369 y=(g∘f)(x), 371 y=f(f(x))와 y=|x|/5, 372 y=g(t)·y=f(x), 382 둘러싸인 부분
- 369번: 문제가 '합성함수를 구하고 그래프를 그리시오'로 바뀌었는데 정답·첫 줄이 옛 문제(g(f(x))=−g(x)의 해)대로 남아 있어 정답을 '해설참조'로, 첫 두 줄을 고침
- 해설 첫 줄 '[정답]'(굵은 11pt) → '󰂼'(다른 문항과 같은 10pt)
"""
import sys, os, re, zipfile, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from lite import Builder
from PIL import Image

src, out = sys.argv[1:3]
G = os.path.join(HERE, "그림")
g = lambda n: os.path.join(G, n)


def side(a, b, name, gap=40):
    A, B_ = Image.open(g(a)).convert("RGB"), Image.open(g(b)).convert("RGB")
    o = Image.new("RGB", (A.width + gap + B_.width, max(A.height, B_.height)), "white")
    o.paste(A, (0, (o.height - A.height) // 2)); o.paste(B_, (A.width + gap, (o.height - B_.height) // 2))
    o.save(g(name))
    return o.width


w369 = side("c2b10_369f.png", "c2b10_369g.png", "c2b10_369.png")
w372 = side("c2b10_372g.png", "c2b10_372.png", "c2b10_372w.png")

z = zipfile.ZipFile(src)
items = [(i, z.read(i.filename)) for i in z.infolist()]
s = z.read("Contents/section0.xml").decode()
hpf = z.read("Contents/content.hpf").decode()


def ens():
    return {re.search(r'autoNum num="(\d+)"', m.group(0)).group(1): m for m in re.finditer(r"<hp:endNote .*?</hp:endNote>", s, re.S)}


E = ens()
# 그림 문단 틀: 370번 해설의 그림 문단
e370 = E["370"].group(0)
pic_tpl = next(m.group(0) for m in re.finditer(r"<hp:p [^>]*>.*?</hp:p>", e370, re.S) if "<hp:pic" in m.group(0))
NEW = {"369": "image14", "371": "image15", "372": "image16", "382": "image17"}
FILE = {"image14": "c2b10_369s.png", "image15": "c2b10_371.png", "image16": "c2b10_372w.png", "image17": "c2b10_382.png"}


def pic_para(img, k):
    p = pic_tpl.replace('binaryItemIDRef="image4"', 'binaryItemIDRef="%s"' % img)
    p = re.sub(r'(<hp:pic id=")\d+', lambda m: m.group(1) + str(1996100100 + k), p, count=1)
    p = re.sub(r'(instid=")\d+', lambda m: m.group(1) + str(996100100 + k), p, count=1)
    return p


SENT = {"369": "$y= LEFT ( g CIRC f RIGHT ) LEFT ( x RIGHT )$의 그래프는 다음과 같다.",
        "371": "$y=f(f(x))$와 $y= {1} over {5} LEFT | x RIGHT |$의 그래프는 다음과 같다.",
        "372": "$y=g(t)$와 직선 $y=1$, $y=f(x)$와 두 직선 $y=0$, $y= {3} over {2}$의 그래프는 다음과 같다.",
        "382": "두 그래프로 둘러싸인 부분은 다음과 같다."}
L369 = ["$g LEFT ( f LEFT ( x RIGHT ) RIGHT )$는 $f LEFT ( x RIGHT )$의 값의 범위에 따라 $g$의 식이 달라진다.",
        "$f LEFT ( x RIGHT )$의 값이 $4$보다 큰 경우, $-4$ 이상 $4$ 이하인 경우, $-4$보다 작은 경우로 나누어 구한다."]
B = Builder(s)
for t in list(SENT.values()) + L369:
    B.collect(t)
B.sizes()


def para(pp, cp, t):
    return ('<hp:p id="2147483648" paraPrIDRef="%s" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0"><hp:run charPrIDRef="%s">%s</hp:run></hp:p>'
            % (pp, cp, B.inline(t)))


def body_paras(e):
    return list(re.finditer(r'<hp:p [^>]*paraPrIDRef="(\d+)"[^>]*><hp:run charPrIDRef="(\d+)">.*?</hp:p>', e, re.S))


for k, (no, img) in enumerate(NEW.items()):
    m = ens()[no]
    e = m.group(0)
    ps = body_paras(e)
    cp = ps[1].group(2)
    add = para("2", cp, SENT[no]) + pic_para(img, k)
    if no == "369":
        e2 = e[:ps[-1].end()] + add + e[ps[-1].end():]                     # 마지막 줄(∴ g(f(x))=…) 다음
        # 옛 문제의 정답·첫 두 줄
        a0 = ps[0].group(0)
        head = re.match(r".*?</hp:ctrl>", a0, re.S).group(0).replace('charPrIDRef="82"', 'charPrIDRef="18"', 1)
        a1 = head + "<hp:t> 󰂼 해설참조</hp:t></hp:run>" + a0[a0.index("<hp:linesegarray>"):]
        assert "[정답]" in a0 and "또는" in a0
        assert "치환하여 푸는 꼴이 아니다" in ps[1].group(0) and "직접 구한 다음 범위를 나누어 푼다" in ps[2].group(0)
        new12 = para("2", cp, L369[0]) + para("2", cp, L369[1])
        e2 = e2.replace(ps[1].group(0) + ps[2].group(0), new12, 1).replace(a0, a1, 1)
    elif no == "382":
        e2 = e[:ps[-1].end()] + add + e[ps[-1].end():]
    else:
        last = ps[-1]
        assert "따라서" in last.group(0)
        e2 = e[:last.start()] + add + e[last.start():]
    s = s[:m.start()] + e2 + s[m.end():]

# '[정답]' → '󰂼'
def ans(m):
    p = m.group(0)
    return p.replace('<hp:run charPrIDRef="82">', '<hp:run charPrIDRef="18">', 1).replace("<hp:t> [정답] </hp:t>", "<hp:t> 󰂼 </hp:t>", 1)


s = s.replace("<hp:t> [정답] ①</hp:t>", "<hp:t> 󰂼 ①</hp:t>", 1)       # 380번(이미 10pt)
n0 = s.count("[정답]")
s = re.sub(r'<hp:run charPrIDRef="82"><hp:ctrl><hp:autoNum num="\d+" numType="ENDNOTE">.*?<hp:t> \[정답\] </hp:t>', ans, s, flags=re.S)
print("[정답] → 󰂼:", n0 - s.count("[정답]"), "곳, 남은 [정답]:", s.count("[정답]"))

# 새 그림 항목
last_item = re.search(r'<opf:item id="image13"[^>]*/>', hpf).group(0)
hpf = hpf.replace(last_item, last_item + "".join('<opf:item id="%s" href="BinData/%s.png" media-type="image/png" isEmbeded="1"/>' % (i, i) for i in FILE))
tmp = out + ".tmp.hwpx"
with zipfile.ZipFile(tmp, "w") as zo:
    for info, data in items:
        if info.filename == "Contents/section0.xml":
            data = s.encode("utf-8")
        elif info.filename == "Contents/content.hpf":
            data = hpf.encode("utf-8")
        zo.writestr(info, data, compress_type=info.compress_type)
    for i, f in FILE.items():
        zo.writestr("BinData/%s.png" % i, open(g(f), "rb").read(), compress_type=zipfile.ZIP_DEFLATED)
sw = os.path.join(os.environ["S"], "swapimg.py")
W = {"image2": ("c2b10_369.png", 20000), "image3": ("c2b10_370.png", 11000), "image4": ("c2b10_370s.png", 11000),
     "image6": ("c2b10_373.png", 8000), "image7": ("c2b10_373a.png", 8000), "image8": ("c2b10_373b.png", 9000),
     "image9": ("c2b10_383.png", 10000), "image10": ("c2b10_384.png", 9000), "image11": ("c2b10_386.png", 9000),
     "image12": ("c2b10_394a.png", 10000), "image13": ("c2b10_394b.png", 11000),
     "image14": ("c2b10_369s.png", 11000), "image15": ("c2b10_371.png", 10000), "image16": ("c2b10_372w.png", 17000),
     "image17": ("c2b10_382.png", 9000)}
subprocess.check_call([sys.executable, "-I", sw, tmp, out] + ["%s=%s@%d" % (k, g(f), w) for k, (f, w) in W.items()])
os.remove(tmp)
print("->", out)
