# -*- coding: utf-8 -*-
"""공통수학2 기본서 단원 조립: 사용자가 손본 1단원 편집본(기본서/원본/기본서_편집본보기_1단원.hwpx)을 틀로 삼는다.

python compose01.py [<출력.hwpx>]      (기본: 공통수학2/기본서/1. 평면좌표.hwpx)
- 틀의 문단을 복제해 쓴다(제작기준 '기본서 편집 기준'):
  STEP 1 개념(소제목·개념 줄·참고 상자) → 새 쪽에 줄 노트 12단(6쪽, 틀의 표 문단 그대로)
  → STEP 2 유형별 학습하기(유형마다 새 쪽, 유형 머리·가운데 정렬 설명) → STEP 3 단원 마무리 하기 → 끝 쪽(단원 이름 상자).
- 문항: 번호 문단(대표문제는 번호 상자, 그림 없음) + 문제 문단(해설은 미주) + 조건·보기 그림자 상자(4행×3열 표)
  + 단서 '(단, …)'는 오른쪽 정렬 문단 + 그림 문단(가운데). 글 안의 '⏎'는 줄바꿈(긴 식을 따로 한 줄에).
- 한 단에 2문항: 위 문항은 단 맨 위, 아래 문항은 단의 가운데쯤(세로 약 43000/86000)에서 시작하도록 빈 줄을 채우고,
  다음 단의 첫 문항은 단 나눔으로 시작한다. 빈 줄 수는 문항 높이를 어림해 정한다(한글에서 다시 맞출 수 있음).
- 번호·미주는 001부터. 그림은 도구/그림/의 PNG를 image101부터 넣는다(1픽셀=6.4 HWPUNIT 약속은 그림 파일 쪽에서 맞춤).
"""
import sys, re, os, struct, math, importlib
HERE = os.path.dirname(os.path.abspath(__file__))
TOOL = os.path.dirname(HERE)
ROOT = os.path.dirname(TOOL)
sys.path.insert(0, os.path.join(TOOL, "기본서"))
sys.path.insert(0, HERE)
import hwpxio as io, fixes, numbering as nb, eqsize

DATA = importlib.import_module(os.environ.get("C2DATA", "data01"))
UNIT_NO, UNIT_TITLE = "1.", "평면좌표"
SRC = os.path.join(ROOT, "기본서", "원본", "기본서_편집본보기_1단원.hwpx")
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "공통수학2", "기본서", "%s %s.hwpx" % (UNIT_NO, UNIT_TITLE))
PIC_DIR = os.path.join(TOOL, "그림")
START = 1

f, order = io.read(SRC)
head, T, tail = io.split(f["Contents/section0.xml"].decode("utf-8"))
T = [io.nolines(p) for p in T]
ENDNOTE = re.compile(r"<hp:endNote .*?</hp:endNote>", re.S)


def body(p):
    return io.text(ENDNOTE.sub("", p))


def pp(p):
    return re.search(r'paraPrIDRef="(\d+)"', p).group(1)


def find(pred, start=0):
    return next(i for i in range(start, len(T)) if pred(T[i]))


def opentag(p):
    return re.match(r"<hp:p [^>]*>", p).group(0)


def first_cp(p):
    return re.search(r'<hp:run charPrIDRef="(\d+)"', p).group(1)


# ---------------------------------------------------------------- 틀 문단
FIRST = T[0]                                                      # 구역 설정 + STEP 1 머리
SUB = T[find(lambda p: pp(p) == "26" and body(p).strip())]        # 개념 소제목
CONL = T[find(lambda p: pp(p) == "27" and "<hp:equation" in p)]   # 개념 줄(수식 있음)
CGAP = T[find(lambda p: pp(p) == "28" and nb.blank(p))]           # 개념 사이 빈 줄
NOTE = T[find(lambda p: "<hp:rect" in p and body(p).startswith("참고"))]
NOTE_TBL = T[find(lambda p: 'rowCnt="28"' in p)]                  # 줄 노트 표 12개(새 쪽)
i_s2 = find(lambda p: "유형별 학습하기" in body(p))
STEP2 = T[i_s2]
HEAD1 = T[i_s2 + 1]
HEAD2 = T[find(lambda p: nb.is_heading(p) and 'pageBreak="1"' in p and pp(p) == "14", i_s2 + 2)]
DESC = T[i_s2 + 2]
GAPS = [p for p in T[i_s2 + 3:i_s2 + 6] if nb.blank(p)]
i_rep = find(lambda p: nb.num_text(p) is not None and "대표문제" in p)
REPNUM = T[i_rep]
QP = T[i_rep + 1]
BLANK = T[i_rep + 2]
NUM = T[find(lambda p: nb.num_text(p) is not None and "<hp:container" not in p)]
BOX = T[find(lambda p: 'rowCnt="4" colCnt="3"' in p and body(p).strip().startswith("(가)"))]
DAN = T[find(lambda p: body(p).strip().startswith("(단,") and "<hp:equation" in p)]
i_s3 = find(lambda p: "단원 마무리 하기" in body(p))
STEP3 = T[i_s3]
i_n3 = find(lambda p: nb.num_text(p) is not None and "<hp:container" not in p, i_s3)
NUM3, QP3 = T[i_n3], T[next(i for i in range(i_n3 + 1, len(T)) if "<hp:endNote " in T[i])]
BLANK3 = T[next(i for i in range(i_n3 + 1, len(T)) if nb.blank(T[i]) and pp(T[i]) == "10")]
END = T[-3:]
FIGP = T[find(lambda p: pp(p) == "33" and nb.blank(p))]           # 가운데 정렬 빈 문단(그림 문단 모양)


def eqdoc(p):
    d = fixes.Doc(T)
    e = re.search(r"<hp:equation [^>]*>", p).group(0)
    d.eq_open = re.sub(r'\bid="\d+"', 'id="0"', re.sub(r'zOrder="\d+"', 'zOrder="0"', e))
    d.base = int(re.search(r'baseUnit="(\d+)"', e).group(1))
    return d


qdoc, q3doc, cdoc, bdoc, ddoc = eqdoc(QP), eqdoc(QP3), eqdoc(CONL), eqdoc(BOX), eqdoc(DAN)
endoc = fixes.Doc(T)
EN0 = ENDNOTE.search(QP).group(0)

_id = [1996000000]


def nid():
    _id[0] += 1
    return _id[0]


def renew_ids(x):
    x = re.sub(r'(<hp:(?:tbl|rect|pic|container|line|ellipse|polygon|curve|equation) id=")\d+(")',
               lambda m: m.group(1) + str(nid()) + m.group(2), x)
    return re.sub(r'instid="\d+"', lambda m: 'instid="%d"' % (nid() % 1000000000), x)


def para(open_tag, cp, xml):
    return '%s<hp:run charPrIDRef="%s">%s</hp:run></hp:p>' % (open_tag, cp, xml)


def inline(doc, text):
    """'⏎'는 줄바꿈"""
    parts = [doc.inline(s.strip()) for s in text.split("⏎")]
    return "<hp:t><hp:lineBreak/></hp:t>".join(parts)


def scripts(texts):
    return [s for s in fixes.scripts_of([t.replace("⏎", " ") for t in texts])]


# ---------------------------------------------------------------- 수식 크기
def all_texts():
    out = []
    for _, ls in DATA.CONCEPT:
        for l in ls:
            out += l["note"] if isinstance(l, dict) else [l]
    for _, d, ps in DATA.TYPES:
        out += d
    for it in [it for _, _, ps in DATA.TYPES for it in ps] + DATA.STEP3:
        for part in it["q"]:
            if isinstance(part, str):
                out.append(part)
            elif "box" in part:
                out += part["box"]
        out += it["sol"] + [ans_line(it)]
    return out


def ans_line(it):
    a = it["ans"]
    return "󰂼 " + (a if re.match(r"[①-⑤ㄱ-ㅎ]", a) or "$" in a else "$%s$" % a)


eqsize.ensure(scripts(all_texts()))


# ---------------------------------------------------------------- 그림
PIC_T = ('<hp:pic id="0" zOrder="0" numberingType="PICTURE" textWrap="TOP_AND_BOTTOM" textFlow="BOTH_SIDES" lock="0" dropcapstyle="None" href="" groupLevel="0" instid="0" reverse="0">'
         '<hp:offset x="0" y="0"/><hp:orgSz width="{W}" height="{H}"/><hp:curSz width="{W}" height="{H}"/><hp:flip horizontal="0" vertical="0"/>'
         '<hp:rotationInfo angle="0" centerX="{CX}" centerY="{CY}" rotateimage="0"/><hp:renderingInfo><hc:transMatrix e1="1" e2="0" e3="0" e4="0" e5="1" e6="0"/>'
         '<hc:scaMatrix e1="1" e2="0" e3="0" e4="0" e5="1" e6="0"/><hc:rotMatrix e1="1" e2="0" e3="0" e4="0" e5="1" e6="0"/></hp:renderingInfo>'
         '<hp:imgRect><hc:pt0 x="0" y="0"/><hc:pt1 x="{W}" y="0"/><hc:pt2 x="{W}" y="{H}"/><hc:pt3 x="0" y="{H}"/></hp:imgRect>'
         '<hp:imgClip left="0" right="{W}" top="0" bottom="{H}"/><hp:inMargin left="0" right="0" top="0" bottom="0"/><hp:imgDim dimwidth="{W}" dimheight="{H}"/>'
         '<hc:img binaryItemIDRef="{IMG}" bright="0" contrast="0" effect="REAL_PIC" alpha="0"/><hp:effects/>'
         '<hp:sz width="{W}" widthRelTo="ABSOLUTE" height="{H}" heightRelTo="ABSOLUTE" protect="0"/>'
         '<hp:pos treatAsChar="1" affectLSpacing="0" flowWithText="1" allowOverlap="0" holdAnchorAndSO="0" vertRelTo="PARA" horzRelTo="PARA" vertAlign="TOP" horzAlign="LEFT" vertOffset="0" horzOffset="0"/>'
         '<hp:outMargin left="0" right="0" top="0" bottom="0"/><hp:shapeComment>그림입니다.</hp:shapeComment></hp:pic>')
new_imgs = {}


def pic_size(fn, width):
    pw, ph = struct.unpack(">II", open(os.path.join(PIC_DIR, fn), "rb").read(24)[16:24])
    return int(width), round(int(width) * ph / pw)


def pic_para(fn, width):
    if fn not in new_imgs:
        new_imgs[fn] = "image%d" % (101 + len(new_imgs))
    W, H = pic_size(fn, width)
    x = PIC_T.format(W=W, H=H, CX=W // 2, CY=H // 2, IMG=new_imgs[fn])
    return renew_ids(para(opentag(FIGP), first_cp(FIGP), x + "<hp:t/>"))


# ---------------------------------------------------------------- 상자(그림자 표)
def box_para(lines):
    """틀의 조건 상자(4행×3열 표, 3행 첫 칸의 글상자)에 lines를 한 줄씩 넣고 높이를 맞춘다"""
    x = BOX
    r0 = x.index("<hp:rect ", x.index("<hp:tbl"))
    r1 = x.index("</hp:rect>", r0) + len("</hp:rect>")
    rect = x[r0:r1]
    sl0 = rect.index(">", rect.index("<hp:subList", rect.index("<hp:drawText"))) + 1
    sl1 = rect.rindex("</hp:subList>")
    inner = rect[sl0:sl1]
    ip = re.search(r"<hp:p [^>]*>", inner).group(0)
    icp = re.search(r'<hp:run charPrIDRef="(\d+)">', inner).group(1)
    rect = rect[:sl0] + "".join(para(ip, icp, inline(bdoc, ln) + "<hp:t/>") for ln in lines) + rect[sl1:]
    n = sum(rows(ln, 30) for ln in lines)
    old_h = int(re.search(r'<hp:sz width="10000" widthRelTo="COLUMN" height="(\d+)"', rect).group(1))
    h = 567 + 1450 * n
    rect = re.sub(r'(<hp:sz width="10000" widthRelTo="COLUMN" height=")\d+"', lambda m: m.group(1) + '%d"' % h, rect)
    x = x[:r0] + rect + x[r1:]
    tb_h = int(re.search(r'<hp:tbl [^>]*>\s*<hp:sz width="\d+" widthRelTo="ABSOLUTE" height="(\d+)"', x).group(1))
    x = re.sub(r'(<hp:tbl [^>]*>\s*<hp:sz width="\d+" widthRelTo="ABSOLUTE" height=")\d+"',
               lambda m: m.group(1) + '%d"' % (tb_h - old_h + h), x, count=1)
    return renew_ids(x), tb_h - old_h + h


# ---------------------------------------------------------------- 높이 어림(HWPUNIT)
def rows(text, per=32):
    """글 한 줄(⏎로 나뉜 줄마다)의 화면 줄 수: 수식은 글자 수의 1/3쯤으로 센다"""
    n = 0
    for seg in text.split("⏎"):
        vis = re.sub(r"\$(.+?)\$", lambda m: "x" * max(1, len(re.sub(r"\s|rm|~|LEFT|RIGHT|overline", "", m.group(1))) // 2), seg)
        n += max(1, math.ceil(len(vis) / per))
    return n


LINE, NUM_H, BLANK_H = 1950, 1700, 1600
MID, COL = 43000, 86000


def split_q(part):
    """문제 글에서 끝의 '(단, …)'을 떼어 낸다"""
    m = re.search(r"\s*(\(단,[^()]*(?:\([^()]*\)[^()]*)*\))\s*$", part)
    if m and m.start() > 0:
        return part[:m.start()], m.group(1)
    return part, None


# ---------------------------------------------------------------- 문항
def problem(it, num_tmpl, q_tmpl, doc):
    """[문단들], 높이"""
    out, h = [], NUM_H
    num = renew_ids(num_tmpl)
    out.append(num)
    q_open, run_cp = opentag(q_tmpl), first_cp(q_tmpl)
    m_cp = re.search(r'<hp:run charPrIDRef="(\d+)">(?:(?!</hp:run>).)*?<hp:ctrl><hp:endNote ', q_tmpl, re.S)
    ctrl_cp = m_cp.group(1) if m_cp else run_cp
    en = endoc.endnote_body(EN0, [ans_line(it)] + it["sol"])
    en = re.sub(r'instId="\d+"', 'instId="%d"' % (nid() % 2000000000), en, count=1)
    parts = list(it["q"])
    first = True
    for part in parts:
        if isinstance(part, str):
            text, dan = split_q(part)
            if text.strip():
                xml = inline(doc, text)
                if first:
                    out.append('%s<hp:run charPrIDRef="%s">%s</hp:run><hp:run charPrIDRef="%s"><hp:ctrl>%s</hp:ctrl><hp:t/></hp:run></hp:p>'
                               % (q_open, run_cp, xml, ctrl_cp, en))
                    first = False
                else:
                    out.append(para(q_open, run_cp, xml))
                h += LINE * rows(text)
            if dan:
                out.append(para(opentag(DAN), first_cp(DAN), inline(ddoc, dan)))
                h += LINE
        elif "box" in part:
            x, bh = box_para(part["box"])
            out.append(x)
            h += bh + 600
        elif "img" in part:
            out.append(pic_para(part["img"], part["w"]))
            h += pic_size(part["img"], part["w"])[1] + 800
    return out, h


def place(probs, num_rep, num_norm, q_tmpl, doc, blank, y0):
    """한 단에 2문항(위·가운데). y0: 첫 단에서 문항이 시작하는 높이"""
    P, slot, y = [], 0, y0
    for k, it in enumerate(probs):
        ps, h = problem(it, num_rep if it.get("rep") else num_norm, q_tmpl, doc)
        if k and slot == 0:                                   # 새 단의 맨 위
            ps[0] = io.set_break(ps[0], col=1)
            y = 0
        P += ps
        y += h
        if slot == 0 and k + 1 < len(probs):
            n = int(round((MID - y) / BLANK_H))
            if MID - y < BLANK_H * 2 or y > MID:              # 너무 길면 다음 문항은 다음 단 맨 위로
                slot = 0
                continue
            P += [blank] * n
            y += n * BLANK_H
            slot = 1
        else:
            slot = 0
    return P


def heading(k, title):
    src = HEAD1 if k == 0 else HEAD2
    x = src.replace("<hp:t>01</hp:t>", "<hp:t>%02d</hp:t>" % (k + 1), 1)
    old_title = re.findall(r"<hp:t>([^<]*)</hp:t>", x)[1]
    x = x.replace("<hp:t>%s</hp:t>" % old_title, "<hp:t>%s</hp:t>" % title, 1)
    return renew_ids(x)


def desc_paras(lines):
    return [para(opentag(DESC), first_cp(DESC), inline(cdoc, ln)) for ln in lines]


def concept_paras():
    out = [FIRST]
    for k, (title, lines) in enumerate(DATA.CONCEPT):
        if k:
            out.append(CGAP)
        out.append(para(opentag(SUB), first_cp(SUB), "<hp:t> %s</hp:t>" % title))
        for ln in lines:
            if isinstance(ln, dict):
                r0 = NOTE.index("<hp:rect ")
                r1 = NOTE.index("</hp:rect>") + len("</hp:rect>")
                body_xml = "<hp:t><hp:lineBreak/></hp:t>".join(inline(cdoc, s) for s in ln["note"])
                out.append(renew_ids(para(opentag(NOTE), first_cp(NOTE), NOTE[r0:r1] + "<hp:t> </hp:t>" + body_xml)))
            else:
                out.append(para(opentag(CONL), first_cp(CONL), inline(cdoc, ln)))
    return out


# ---------------------------------------------------------------- 조립
P = concept_paras()
P.append(renew_ids(NOTE_TBL))
P.append(STEP2)
for k, (title, desc, probs) in enumerate(DATA.TYPES):
    P.append(heading(k, title))
    ds = desc_paras(desc)
    P += ds
    P += GAPS
    y0 = 3200 + sum(LINE * rows(d, 34) for d in desc) + 2 * BLANK_H
    P += place(probs, REPNUM, NUM, QP, qdoc, BLANK, y0)
P.append(STEP3)
P += place(DATA.STEP3, NUM3, NUM3, QP3, q3doc, BLANK3, 3500)
P += [END[0].replace('name="답1.다항식의 연산"', 'name="답%s%s"' % (UNIT_NO, UNIT_TITLE)),
      END[1].replace("<hp:t>1. 다항식의 연산과 항등식</hp:t>", "<hp:t>%s %s</hp:t>" % (UNIT_NO, UNIT_TITLE)),
      END[2]]

P, nprob, _ = nb.renumber(P, NUM, start=START)
P = nb.note_start(P, START)

sec = head + "".join(P) + tail
f["Contents/section0.xml"] = sec.encode("utf-8")
for mp in ("Contents/masterpage0.xml", "Contents/masterpage1.xml"):
    x = f[mp].decode("utf-8")
    x = x.replace("<hp:t>1.</hp:t>", "<hp:t>%s</hp:t>" % UNIT_NO).replace("<hp:t>다항식의 연산과 항등식</hp:t>", "<hp:t>%s</hp:t>" % UNIT_TITLE)
    x = x.replace("<hp:t>공통수학1</hp:t>", "<hp:t>공통수학2</hp:t>")
    x = re.sub(r"(<hp:t>공통수학</hp:t>(?:(?!<hp:t>).)*?<hp:t> </hp:t>(?:(?!<hp:t>).)*?<hp:t>)1(</hp:t>)", r"\g<1>2\2", x, flags=re.S)
    f[mp] = x.encode("utf-8")
hpf = f["Contents/content.hpf"].decode("utf-8")
for fn, img in new_imgs.items():
    name = "BinData/%s.png" % img
    f[name] = open(os.path.join(PIC_DIR, fn), "rb").read()
    order.append(name)
    k = hpf.index("/>", hpf.rindex('<opf:item id="image')) + 2
    hpf = hpf[:k] + '<opf:item id="%s" href="%s" media-type="image/png" isEmbeded="1"/>' % (img, name) + hpf[k:]
f["Contents/content.hpf"] = hpf.encode("utf-8")
if "Preview/PrvText.txt" in f:
    f["Preview/PrvText.txt"] = ("%s %s" % (UNIT_NO, UNIT_TITLE)).encode("utf-8")
os.makedirs(os.path.dirname(OUT), exist_ok=True)
io.write(OUT, f, order)
sys.path.insert(0, TOOL)
import eqfix
eqfix.fix_file(OUT)
print("문항", nprob, "문단", len(P), "그림", len(new_imgs), "->", OUT)
