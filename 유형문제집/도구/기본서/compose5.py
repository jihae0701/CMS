# -*- coding: utf-8 -*-
"""기본서 5단원 = 이차함수와 이차방정식의 관계 (학원 초안 '6. 이차함수와 이차방정식의 관계(초안).hwpx'를 1~4단원 기본서 모양으로 정리)

python compose5.py <초안.hwpx> <번호 본보기(2단원 원본).hwpx> <출력.hwpx>
- 수식 안의 변환 흔적을 지우고, 검수 수정(fixF.FIX)을 초안 문항 순서(k)대로 적용한다.
- 유형: 01 이차함수의 성질 / 02 x절편과 이차방정식의 근 / 03 이차함수와 일차함수의 그래프의 교점 / 04 곡선과 직선의 위치 관계
  / 05 방정식의 해와 두 함수의 그래프의 교점 / 06 접선의 방정식 / 07 근의 위치 / 08 이차함수의 활용
- 겹치는 문항 2개(07의 '적어도 한 근', 08의 α³+β³=40)를 빼고 판별식으로 위치 관계를 판단하는 기본 문항을 02, 03에 1개씩 넣는다.
- 08 유형은 대표문제가 없어 첫 문항(S₁−S₂=20)을 대표문제로 삼고, 그 뒤에 유형서에서 옮긴 m3243을 유제로 둔다. 전체 41문항.
- 유형마다 새 쪽에서 시작, 문항 번호는 4단원(122~160)에 이어 161부터.
"""
import sys, re, os, struct
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from xml.sax.saxutils import escape, unescape
import hwpxio as io, hwpxmerge as hm, fixes, numbering as nb, shortans, addprob, fixF

SRC, NUMSRC, OUT = sys.argv[1:4]
START = 161           # 1단원 001~041, 2단원 042~081, 3단원 082~121, 4단원 122~160에 이어서

f, o = io.read(SRC)
sec = f["Contents/section0.xml"].decode("utf-8")
head, P, tail = io.split(sec)
P = [io.nolines(p) for p in P]

# 0. 수식 안의 변환 흔적 (바뀐 수식은 크기를 다시 잰다)
doc0 = fixes.Doc(P)


def clean_eq(m):
    eq = m.group(0)
    sm = re.search(r"(<hp:script[^>]*>)(.*?)(</hp:script>)", eq, re.S)
    if not sm:
        return eq
    sc = unescape(sm.group(2))
    new = sc
    for pat, rep in fixF.SCRIPT_FIX:
        new = re.sub(pat, rep, new)
    if new == sc:
        return eq
    new = new.strip()
    eq = eq[:sm.start()] + sm.group(1) + escape(new) + sm.group(3) + eq[sm.end():]
    return fixes.resize_eq(eq, doc0.base)


P = [re.sub(r"<hp:equation .*?</hp:equation>", clean_eq, p, flags=re.S) for p in P]


def body_text(i):
    return io.text(re.sub(r"<hp:endNote .*?</hp:endNote>", "", P[i], flags=re.S))


def seg_text(a, e):
    return "".join(body_text(i) for i in range(a, e + 1))


# 문항 알아보기 글귀(초안 순서 k -> 문제 글 앞부분)
segs = nb.segments(P)
SIG = {k: seg_text(*segs[k - 1])[:60] for k in range(1, len(segs) + 1)}

# 1. 개념 설명 문단 오타 (문항 밖 문단만)
inseg = set()
for a, e in segs:
    inseg |= set(range(a, e + 1))
for key, old, new in fixF.CONCEPT_FIX:
    i = next(i for i, p in enumerate(P) if i not in inseg and "<hp:endNote " not in p and key in io.text(p))
    assert "<hp:t>" in P[i] and old in P[i], (key, old)
    P[i] = P[i].replace(old, new, 1)

# 2. 171번(초안 k=11) 해설 (ⅱ)의 '교점이 1개' -> 3개
a, e = segs[10]
en = re.search(r"<hp:endNote .*?</hp:endNote>", P[e], re.S).group(0)
j = en.index("(ⅱ)")
m = re.compile(r"(<hp:equation .*?<hp:script>)\s*1\s*(</hp:script></hp:equation>)", re.S)
hit = [x for x in m.finditer(en, j)][0]
neq = fixes.resize_eq(hit.group(1) + "3" + hit.group(2), doc0.base)
P[e] = P[e].replace(en, en[:hit.start()] + neq + en[hit.end():], 1)

# 3. 검수 수정 (초안 순서 k)
P, log = fixes.apply(P, fixF.FIX, "F")


def find_seg(sig):
    for a, e in nb.segments(P):
        if sig in seg_text(a, e):
            return a, e
    raise ValueError(sig)


# 4. 08 유형 대표문제: 대표문제 머리 문단(07 유형 것)을 문항 앞에 붙인다
rep_head = next(p for p in P if nb.num_text(p) == "")
a, _ = find_seg(SIG[fixF.REP08])
P = P[:a] + [rep_head] + P[a:]

# 5. 유형마다 새 쪽 (01은 'STEP 2' 제목 바로 뒤라 그대로)
s2 = next(i for i, p in enumerate(P) if "유형별 학습하기" in io.text(p))
s3 = next(i for i, p in enumerate(P) if "단원 마무리 하기" in io.text(p))
for i in range(s2 + 1, s3):
    if nb.is_heading(P[i]) and not re.match(r"01", io.text(P[i]).strip()):
        P[i] = io.set_break(P[i], page=1)

# 6. 문항 번호 문단 본보기(2단원 원본의 번호 문단)를 이 문서 번호 체계로
fn, on = io.read(NUMSRC)
hN = fn["Contents/header.xml"].decode("utf-8")
_, PN, _ = io.split(fn["Contents/section0.xml"].decode("utf-8"))
M = hm.Merger(f["Contents/header.xml"].decode("utf-8"), hN)
tmpl = M.body(next(io.nolines(p) for p in PN if nb.num_text(p) and "<hp:container" not in p))
P, nprob, nins = nb.renumber(P, tmpl, start=START)


def num_of(sig):
    a, _ = find_seg(sig)
    i = a
    while nb.num_text(P[i]) is None:
        i -= 1
    return nb.num_text(P[i])


# 7. 새 문항 (판별식으로 위치 관계 판단)
for k, item in fixF.NEW_AFTER:
    P = addprob.insert(P, num_of(SIG[k]), num_of(SIG[fixF.NEW_TEMPLATE]), [item], blanks=16)
    P, nprob, _ = nb.renumber(P, tmpl, start=START)


# 7-2. 유형서에서 옮겨 온 그림 문항: 문제 문단 뒤에 그림 문단(182번 그림 문단처럼 가운데 정렬)을 둔다
PIC_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "그림")
pic_tpl = re.search(r"<hp:pic .*?</hp:pic>", next(p for p in P if "<hp:pic " in p and 'treatAsChar="1"' in p
                                                     and "<hp:container" not in p), re.S).group(0)
fig_p = next(p for p in P if p.startswith("<hp:p ") and "<hp:container" in p and not nb.num_text(p)
             and not io.text(re.sub(r"<hp:container .*?</hp:container>", "", p, flags=re.S)).strip())
fig_open = re.match(r"<hp:p [^>]*>", fig_p).group(0)
fig_cp = re.search(r'<hp:run charPrIDRef="(\d+)">', fig_p).group(1)
new_imgs = []


def pic_para(fn, width):
    img = "image%d" % (101 + len(new_imgs))
    new_imgs.append((fn, img))
    pw, ph = struct.unpack(">II", open(os.path.join(PIC_DIR, fn), "rb").read(24)[16:24])
    W, H = int(width), round(int(width) * ph / pw)
    x = re.sub(r'binaryItemIDRef="[^"]+"', 'binaryItemIDRef="%s"' % img, pic_tpl)
    x = re.sub(r'\bid="\d+"', 'id="%d"' % (1990500000 + len(new_imgs)), x, count=1)
    x = re.sub(r'instid="\d+"', 'instid="%d"' % (990500000 + len(new_imgs)), x, count=1)
    x = re.sub(r'<hp:orgSz [^>]*/>', '<hp:orgSz width="%d" height="%d"/>' % (W, H), x)
    x = re.sub(r'<hp:curSz [^>]*/>', '<hp:curSz width="%d" height="%d"/>' % (W, H), x)
    x = re.sub(r'centerX="\d+" centerY="\d+"', 'centerX="%d" centerY="%d"' % (W // 2, H // 2), x)
    x = re.sub(r'<hc:scaMatrix [^>]*/>', '<hc:scaMatrix e1="1" e2="0" e3="0" e4="0" e5="1" e6="0"/>', x)
    x = re.sub(r'<hp:imgRect>.*?</hp:imgRect>', '<hp:imgRect><hc:pt0 x="0" y="0"/><hc:pt1 x="%d" y="0"/>'
               '<hc:pt2 x="%d" y="%d"/><hc:pt3 x="0" y="%d"/></hp:imgRect>' % (W, W, H, H), x, flags=re.S)
    x = re.sub(r'<hp:imgClip [^>]*/>', '<hp:imgClip left="0" right="%d" top="0" bottom="%d"/>' % (W, H), x)
    x = re.sub(r'<hp:imgDim [^>]*/>', '<hp:imgDim dimwidth="%d" dimheight="%d"/>' % (W, H), x)
    x = re.sub(r'<hp:sz width="\d+" widthRelTo="ABSOLUTE" height="\d+"',
               '<hp:sz width="%d" widthRelTo="ABSOLUTE" height="%d"' % (W, H), x)
    x = re.sub(r'<hp:outMargin [^>]*/>', '<hp:outMargin left="0" right="0" top="0" bottom="0"/>', x)
    x = re.sub(r"<hp:shapeComment>.*?</hp:shapeComment>", "<hp:shapeComment>그림입니다.</hp:shapeComment>", x, flags=re.S)
    return '%s<hp:run charPrIDRef="%s">%s<hp:t/></hp:run></hp:p>' % (fig_open, fig_cp, x)


for k, item, fn, width in fixF.NEW_PIC_AFTER:
    after = num_of(SIG[k])
    new = addprob.build(P, num_of(SIG[fixF.NEW_TEMPLATE]), [item], blanks=14)
    new = new[:2] + [pic_para(fn, width)] + new[2:]
    _, aj = addprob._block(P, after)
    P = P[:aj] + new + P[aj:]
    P, nprob, _ = nb.renumber(P, tmpl, start=START)
hpf = f["Contents/content.hpf"].decode("utf-8")
for fn, img in new_imgs:
    name = "BinData/%s.png" % img
    f[name] = open(os.path.join(PIC_DIR, fn), "rb").read()
    o.append(name)
    k = hpf.index("/>", hpf.rindex('<opf:item id="image')) + 2
    hpf = hpf[:k] + '<opf:item id="%s" href="%s" media-type="image/png" isEmbeded="1"/>' % (img, name) + hpf[k:]
f["Contents/content.hpf"] = hpf.encode("utf-8")


# 8. 단답형 바꾸기 (보기 ㄱㄴㄷ·범위 답 문항은 5지선다로 남김)
def seg_pos(sub):
    for kk, (a, e) in enumerate(nb.segments(P), 1):
        if sub in seg_text(a, e):
            return kk
    raise ValueError(sub)


keep = tuple(seg_pos(s) for s in fixF.KEEP_MC)
P, slog = shortans.convert(P, fixes.Doc(P), keep=keep)
print("단답형", sum(1 for l in slog if l[1] == "단답형"), [l for l in slog if l[1] != "단답형"])
P, nprob, _ = nb.renumber(P, tmpl, start=START)
P = nb.note_start(P, START)
print("문항", nprob, "5지선다", sorted(keep))

f["Contents/section0.xml"] = (head + "".join(P) + tail).encode("utf-8")
f["Contents/header.xml"] = M.hA.encode("utf-8")
io.write(OUT, f, o)
print("문단", len(P), "->", OUT)
