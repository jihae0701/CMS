# -*- coding: utf-8 -*-
"""기본서 6단원 = 이차함수의 최대, 최소 (학원 초안이 없어 data6.py의 자료로 새로 만든다)

python compose6.py <본보기: 기본서 5단원.hwpx> <출력.hwpx>
- 모양(제목 상자, 개념 문단, 유형 머리, 대표문제 번호, 문제 문단, 조건 상자, 보기 상자, 선택지, 미주)은
  기본서 5단원 파일의 문단을 복제해 쓴다.
- 구성: STEP 1 개념 확인하기 / STEP 2 유형별 학습하기(유형 01~07, 유형마다 새 쪽) / STEP 3 단원 마무리 하기
- 문항 번호는 5단원(161~200)에 이어 201부터. 그림은 도구/그림/의 PNG를 image101부터 넣는다.
"""
import sys, re, os, struct, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hwpxio as io, fixes, numbering as nb, eqsize, addprob, data6

SRC, OUT = sys.argv[1:3]
START = 201
UNIT_NO, UNIT_TITLE = "6.", "이차함수의 최대, 최소"
PIC_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "그림")

f, o = io.read(SRC)
head, T, tail = io.split(f["Contents/section0.xml"].decode("utf-8"))
T = [io.nolines(p) for p in T]
ENDNOTE = re.compile(r"<hp:endNote .*?</hp:endNote>", re.S)


def body(p):
    return io.text(ENDNOTE.sub("", p))


def find(pred, start=0):
    return next(i for i in range(start, len(T)) if pred(T[i]))


def num_index(n):
    return next(i for i, p in enumerate(T) if nb.num_text(p) == n)


# ---------------------------------------------------------------- 본보기 문단
STEP1 = T[0]
SUB = T[find(lambda p: re.match(r'<hp:p [^>]*paraPrIDRef="64"', p) and body(p).strip())]
CON = T[find(lambda p: re.match(r'<hp:p [^>]*paraPrIDRef="65"', p) and "<hp:tbl" not in p and body(p).strip())]
GAP1 = T[find(lambda p: re.match(r'<hp:p [^>]*paraPrIDRef="66"', p) and nb.blank(p))]
i_s2 = find(lambda p: "유형별 학습하기" in body(p))
STEP2 = T[i_s2]
HEAD1 = T[i_s2 + 1]                                       # 첫 유형 머리(쪽 나눔 없음)
i_h2 = find(lambda p: nb.is_heading(p) and 'pageBreak="1"' in p and "유형" in body(p), i_s2 + 2)
HEAD2 = T[i_h2]                                           # 둘째부터(새 쪽)
DESC = T[i_h2 + 1]
GAP2 = next(p for p in T[i_h2 + 1:i_h2 + 6] if nb.blank(p))
STEP3 = T[find(lambda p: "단원 마무리 하기" in body(p))]
LAST = T[-1]                                              # 끝 쪽(단원 이름 상자)
REP_T = num_index("164")                                  # 대표문제(문제 한 문단)
NOR_T = num_index("166")                                  # 보통 문항(문제 한 문단)
BOX_P = next(p for p in T if "<hp:tbl" in p and body(p).strip().startswith("(가)") and "<hp:endNote " not in p)
BOGI_P = next(p for p in T if "<hp:endNote " in p and "ㄱ." in body(p) and "<hp:tbl" in p)
CH1 = next(p for p in T if body(p).startswith("① ㄱ"))
CH2 = next(p for p in T if body(p).startswith("④ ㄴ, ㄷ"))
SPACER = next(p for p in T[REP_T + 2:] if nb.blank(p) and 'Break="1"' not in p)

# 문제 글 수식 모양(본보기 문제 문단의 수식)
q_p = T[NOR_T + 1]
qdoc = fixes.Doc(T)
qeq = re.search(r"<hp:equation [^>]*>", q_p).group(0)
qdoc.eq_open = re.sub(r'\bid="\d+"', 'id="0"', re.sub(r'zOrder="\d+"', 'zOrder="0"', qeq))
qdoc.base = int(re.search(r'baseUnit="(\d+)"', qeq).group(1))
Q_OPEN = re.match(r"<hp:p [^>]*>", q_p).group(0)
Q_CP = re.search(r'<hp:run charPrIDRef="(\d+)">', q_p).group(1)

# 개념·유형 설명 수식 모양(본문 수식)
cdoc = fixes.Doc(T)
ceq = re.search(r"<hp:equation [^>]*>", CON).group(0)
cdoc.eq_open = re.sub(r'\bid="\d+"', 'id="0"', re.sub(r'zOrder="\d+"', 'zOrder="0"', ceq))
cdoc.base = int(re.search(r'baseUnit="(\d+)"', ceq).group(1))

# 상자 안 수식 모양
bdoc = fixes.Doc(T)
beq = re.search(r"<hp:equation [^>]*>", BOX_P).group(0)
bdoc.eq_open = re.sub(r'\bid="\d+"', 'id="0"', re.sub(r'zOrder="\d+"', 'zOrder="0"', beq))
bdoc.base = int(re.search(r'baseUnit="(\d+)"', beq).group(1))

# ---------------------------------------------------------------- 수식 크기
texts = [s for _, ls in data6.CONCEPT for s in ls] + [s for _, d, _ in data6.TYPES for s in d]
items = [it for _, _, ps in data6.TYPES for it in ps] + data6.STEP3
for it in items:
    for part in it["q"]:
        if isinstance(part, str):
            texts.append(part)
        elif "box" in part:
            texts += part["box"]
        elif "bogi" in part:
            texts += part["bogi"]
eqsize.ensure(fixes.scripts_of(texts) + [s for it in items for s in fixes.scripts_of([it["ans"]] + it["sol"])]
              + fixes.scripts_of(["$" + it["ans"] + "$" for it in items if not it["ans"].startswith(("①", "②", "③", "④", "⑤"))]))

_id = [1995000000]


def nid():
    _id[0] += 1
    return _id[0]


def renew_ids(x):
    x = re.sub(r'(<hp:(?:tbl|rect|pic|container|line|ellipse|polygon|curve|equation) id=")\d+(")',
               lambda m: m.group(1) + str(nid()) + m.group(2), x)
    return re.sub(r'instid="\d+"', lambda m: 'instid="%d"' % (nid() % 1000000000), x)


def para(open_tag, cp, xml):
    return '%s<hp:run charPrIDRef="%s">%s</hp:run></hp:p>' % (open_tag, cp, xml)


def first_run_cp(p):
    return re.search(r'<hp:run charPrIDRef="(\d+)">', p).group(1)


# ---------------------------------------------------------------- 조각 만들기
def concept_paras():
    out = [STEP1]
    sub_open, sub_cp = re.match(r"<hp:p [^>]*>", SUB).group(0), first_run_cp(SUB)
    con_open = re.match(r"<hp:p [^>]*>", CON).group(0)
    con_cp = re.findall(r'<hp:run charPrIDRef="(\d+)">', CON)[-1]
    for k, (title, lines) in enumerate(data6.CONCEPT):
        if k:
            out.append(GAP1)
        out.append(para(sub_open, sub_cp, "<hp:t> %s</hp:t>" % title))
        for ln in lines:
            out.append(para(con_open, con_cp, cdoc.inline(ln)))
    return out


def heading(k, title):
    src = HEAD1 if k == 0 else HEAD2
    old_no = "01" if k == 0 else "02"
    old_title = re.search(r'styleIDRef="14"[^>]*><hp:run charPrIDRef="\d+"><hp:t>([^<]*)</hp:t>', src).group(1)
    x = src.replace("<hp:t>%s</hp:t>" % old_no, "<hp:t>%02d</hp:t>" % (k + 1), 1)
    x = x.replace("<hp:t>%s</hp:t>" % old_title, "<hp:t>%s</hp:t>" % title, 1)
    return renew_ids(x)


def desc_paras(lines):
    op, cp = re.match(r"<hp:p [^>]*>", DESC).group(0), first_run_cp(DESC)
    return [para(op, cp, cdoc.inline(ln)) for ln in lines]


def rect_fill(x, lines, doc, old_n):
    """x 안의 첫 글상자(drawText)에 lines를 한 줄씩 넣고 높이를 줄 수에 맞춘다"""
    r0 = x.index("<hp:rect ", x.index("<hp:tbl"))
    r1 = x.index("</hp:rect>", r0) + len("</hp:rect>")
    rect = x[r0:r1]
    sl0 = rect.index(">", rect.index("<hp:subList", rect.index("<hp:drawText"))) + 1
    sl1 = rect.index("</hp:subList>", sl0)
    inner_p = re.search(r"<hp:p [^>]*>", rect[sl0:sl1]).group(0)
    inner_cp = re.search(r'<hp:run charPrIDRef="(\d+)">', rect[sl0:sl1]).group(1)
    new_inner = "".join(para(inner_p, inner_cp, doc.inline(ln) + "<hp:t/>") for ln in lines)
    old_h = int(re.search(r'<hp:curSz width="\d+" height="(\d+)"/>', rect).group(1))
    # 줄 수(한 줄에 대략 34자)
    def nrow(ln):
        vis = re.sub(r"\$(.+?)\$", lambda m: "x" * max(1, len(m.group(1)) // 3), ln)
        return max(1, math.ceil(len(vis) / 34))
    n = sum(nrow(ln) for ln in lines)
    per = (old_h - 567) / old_n
    h = int(567 + per * n)
    rect = rect[:sl0] + new_inner + rect[sl1:]
    rect = re.sub(r'<hp:curSz width="(\d+)" height="\d+"/>', lambda m: '<hp:curSz width="%s" height="%d"/>' % (m.group(1), h), rect, count=1)
    rect = re.sub(r'(centerY=")\d+"', lambda m: m.group(1) + '%d"' % (h // 2), rect, count=1)
    rect = re.sub(r'(<hc:scaMatrix e1="[^"]+" e2="0" e3="0" e4="0" e5=")[^"]+"', lambda m: m.group(1) + '%.6f"' % (h / 8504), rect, count=1)
    rect = re.sub(r'(<hp:sz width="10000" widthRelTo="COLUMN" height=")\d+"', lambda m: m.group(1) + '%d"' % h, rect)
    x = x[:r0] + rect + x[r1:]
    tb_h = int(re.search(r'<hp:tbl [^>]*>\s*<hp:sz width="\d+" widthRelTo="ABSOLUTE" height="(\d+)"', x).group(1))
    x = re.sub(r'(<hp:tbl [^>]*>\s*<hp:sz width="\d+" widthRelTo="ABSOLUTE" height=")\d+"',
               lambda m: m.group(1) + '%d"' % (tb_h - old_h + h), x, count=1)
    return renew_ids(x)


def box_para(lines):
    return rect_fill(BOX_P, lines, bdoc, 2)


def bogi_para(lines):
    tb = BOGI_P[BOGI_P.index("<hp:tbl"):BOGI_P.index("</hp:tbl>") + len("</hp:tbl>")]
    op = re.match(r"<hp:p [^>]*>", BOGI_P).group(0)
    x = para(op, first_run_cp(BOGI_P), tb + "<hp:t/>")
    old_n = len(re.findall(r"<hp:p ", tb[tb.index("<hp:drawText", tb.index("<hp:rect ")):tb.index("</hp:drawText>", tb.index("<hp:rect "))])) - 1
    return rect_fill(x, lines, bdoc, max(old_n, 1))


def choice_paras(ch):
    tab = re.search(r'<hp:tab [^>]*/>', CH1).group(0)
    marks = "①②③④⑤"
    out = []
    for src, idx in ((CH1, (0, 1, 2)), (CH2, (3, 4))):
        op, cp = re.match(r"<hp:p [^>]*>", src).group(0), first_run_cp(src)
        t = tab.join("%s %s" % (marks[i], ch[i]) for i in idx)
        out.append(para(op, cp, "<hp:t>%s</hp:t>" % t))
    return out


pic_src = next(p for p in T if "<hp:pic " in p and "<hp:container" not in p and 'treatAsChar="1"' in p)
PIC_T = re.search(r"<hp:pic .*?</hp:pic>", pic_src, re.S).group(0)
FIG_P = next(p for p in T if p.startswith("<hp:p ") and "<hp:container" in p and not nb.num_text(p)
             and not io.text(re.sub(r"<hp:container .*?</hp:container>", "", p, flags=re.S)).strip())
FIG_OPEN = re.match(r"<hp:p [^>]*>", FIG_P).group(0)
FIG_CP = first_run_cp(FIG_P)
new_imgs = {}


def pic_para(fn, width):
    if fn not in new_imgs:
        new_imgs[fn] = "image%d" % (101 + len(new_imgs))
    img = new_imgs[fn]
    pw, ph = struct.unpack(">II", open(os.path.join(PIC_DIR, fn), "rb").read(24)[16:24])
    W, H = int(width), round(int(width) * ph / pw)
    x = re.sub(r'binaryItemIDRef="[^"]+"', 'binaryItemIDRef="%s"' % img, PIC_T)
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
    return renew_ids(para(FIG_OPEN, FIG_CP, x + "<hp:t/>"))


def problem(it, blanks):
    ans = it["ans"]
    a_line = "󰂼 " + (ans if ans.startswith(("①", "②", "③", "④", "⑤")) else "$%s$" % ans)
    first = it["q"][0]
    built = addprob.build(T, nb.num_text(T[REP_T if it["rep"] else NOR_T]),
                          [{"q": first, "ans": a_line, "sol": it["sol"]}], blanks=blanks)
    num_p, q_par, spacers = built[0], built[1], built[2:]
    extra = []
    for part in it["q"][1:]:
        if isinstance(part, str):
            extra.append(para(Q_OPEN, Q_CP, qdoc.inline(part)))
        elif "box" in part:
            extra.append(box_para(part["box"]))
        elif "bogi" in part:
            extra.append(bogi_para(part["bogi"]))
        elif "ch" in part:
            extra += choice_paras(part["ch"])
        elif "img" in part:
            extra.append(pic_para(part["img"], part["w"]))
    return [renew_ids(num_p), renew_ids(q_par)] + extra + spacers


# ---------------------------------------------------------------- 조립
P = concept_paras()
P.append(STEP2)
for k, (title, desc, probs) in enumerate(data6.TYPES):
    P.append(heading(k, title))
    P += desc_paras(desc)
    P.append(GAP2)
    for it in probs:
        has_fig = any(isinstance(x, dict) and "img" in x for x in it["q"])
        P += problem(it, 8 if has_fig else 16)
P.append(STEP3)
for it in data6.STEP3:
    has_fig = any(isinstance(x, dict) and "img" in x for x in it["q"])
    P += problem(it, 6 if has_fig else 14)
P.append(LAST.replace("<hp:t>5. 이차함수와 이차방정식의 관계</hp:t>", "<hp:t>%s %s</hp:t>" % (UNIT_NO, UNIT_TITLE)))

tmpl = T[NOR_T]
P, nprob, _ = nb.renumber(P, tmpl, start=START)
P = nb.note_start(P, START)

f["Contents/section0.xml"] = (head + "".join(P) + tail).encode("utf-8")
for mp in ("Contents/masterpage0.xml", "Contents/masterpage1.xml"):
    x = f[mp].decode("utf-8")
    x = x.replace("<hp:t>5.</hp:t>", "<hp:t>%s</hp:t>" % UNIT_NO).replace("<hp:t>이차함수와 이차방정식의 관계</hp:t>", "<hp:t>%s</hp:t>" % UNIT_TITLE)
    f[mp] = x.encode("utf-8")
# 5단원 본보기에서 옮겨 온 그림(image101)은 지우고 6단원 그림을 넣는다
hpf = f["Contents/content.hpf"].decode("utf-8")
for name in [n for n in list(f) if re.match(r"BinData/image1\d\d\.png$", n)]:
    del f[name]
    o.remove(name)
    hpf = re.sub(r'<opf:item id="%s"[^>]*/>' % re.escape(name[8:-4]), "", hpf)
for fn, img in new_imgs.items():
    name = "BinData/%s.png" % img
    f[name] = open(os.path.join(PIC_DIR, fn), "rb").read()
    o.append(name)
    k = hpf.index("/>", hpf.rindex('<opf:item id="image')) + 2
    hpf = hpf[:k] + '<opf:item id="%s" href="%s" media-type="image/png" isEmbeded="1"/>' % (img, name) + hpf[k:]
f["Contents/content.hpf"] = hpf.encode("utf-8")
io.write(OUT, f, o)
print("문항", nprob, "문단", len(P), "그림", len(new_imgs), "->", OUT)
