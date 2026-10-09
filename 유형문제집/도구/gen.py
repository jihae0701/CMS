# -*- coding: utf-8 -*-
"""학원 기본 폼(공통수학1_01 hwpx)을 틀로 유형 문제집 단원 파일(hwpx)을 만든다.

사용: python gen.py <폼.hwpx> <서식샘플.hwpx> <단원모듈> <출력.hwpx>
단원모듈은 UNIT(제목·번호)과 ITEMS(머리말/문항 목록)를 가진 파이썬 파일이다.
"""
import sys, os, re, json, zipfile, importlib.util
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from eqmeasure import measure  # noqa: E402

FORM, SAMPLE, UNITFILE, OUT = sys.argv[1:5]

# ---------------------------------------------------------------- 틀 읽기
zf = zipfile.ZipFile(FORM)
FILES = {i.filename: zf.read(i.filename) for i in zf.infolist()}
ORDER = [i.filename for i in zf.infolist()]
SEC = FILES["Contents/section0.xml"].decode("utf-8")
SEC_HEAD = SEC[:SEC.index(">", SEC.index("<hs:sec")) + 1]


def top_spans(x):
    start = x.index(">", x.index("<hs:sec")) + 1
    out, depth, st = [], 0, 0
    for m in re.finditer(r"<hp:p\b[^>]*?(/?)>|</hp:p>", x[start:]):
        s, pos = m.group(0), m.start() + start
        if s.startswith("</"):
            depth -= 1
            if depth == 0:
                out.append((st, m.end() + start))
        elif not s.endswith("/>"):
            if depth == 0:
                st = pos
            depth += 1
    return out


SP = top_spans(SEC)
PARA = [SEC[a:b] for a, b in SP]


def nolines(x):
    return re.sub(r"<hp:linesegarray>.*?</hp:linesegarray>", "", x, flags=re.S)


P0 = nolines(PARA[0])
HEAD = nolines(PARA[38])            # 유형 제목(단 나눔)
HEAD2 = nolines(PARA[161])          # 고난도(쪽 나눔)
BANNER = re.search(r"<hp:tbl .*?</hp:tbl>", PARA[2], re.S).group(0)
BANNER = nolines(BANNER)
TAIL = [nolines(p) for p in PARA[236:242]]
PICPARA = {}
for p in PARA:
    if "<hp:endNote" in p or "<hp:tbl" in p:
        continue
    m = re.findall(r'binaryItemIDRef="(image\d+)"', p)
    if len(m) == 1 and "<hp:pic " in p:
        PICPARA[m[0]] = nolines(p)
smp = zipfile.ZipFile(SAMPLE).read("Contents/section0.xml").decode("utf-8")
SMP_TBL = [nolines(m.group(0)) for m in re.finditer(r"<hp:tbl .*?</hp:tbl>", smp, re.S)]
# 서식샘플의 테두리/문단/글자 모양 번호를 폼의 번호로 바꾼다(같은 모양이 폼에 있음)
BF = {"5": "9", "6": "10", "7": "15", "8": "22", "9": "11", "10": "23", "11": "24", "12": "13",
      "13": "14", "14": "16", "15": "17", "16": "18", "17": "19", "18": "12", "22": "40"}
PP = {"25": 'paraPrIDRef="52" styleIDRef="0"', "23": 'paraPrIDRef="5" styleIDRef="3"',
      "30": 'paraPrIDRef="0" styleIDRef="0"', "0": 'paraPrIDRef="0" styleIDRef="0"'}
CP = {"11": "2", "12": "2", "9": "7", "10": "8", "13": "2", "7": "0", "14": "16"}


def from_sample(t):
    t = re.sub(r'borderFillIDRef="(\d+)"', lambda m: 'borderFillIDRef="%s"' % BF[m.group(1)], t)
    t = t.replace('binaryItemIDRef="image1"', 'binaryItemIDRef="image9"')
    t = re.sub(r'paraPrIDRef="(\d+)" styleIDRef="(\d+)"', lambda m: PP.get(m.group(1), m.group(0)), t)
    return re.sub(r'charPrIDRef="(\d+)"', lambda m: 'charPrIDRef="%s"' % CP.get(m.group(1), m.group(1)), t)


# 보기 상자(「보기」 꼬리표)와 조건 상자는 모두 표 칸 안에 선 없는 글상자를 두고 그 안에 글을 쓴다.
# 글상자 안쪽 여백: 왼쪽·오른쪽 425, 아래 567
BOGI = from_sample(SMP_TBL[0])
BOX = from_sample(SMP_TBL[1])

# ---------------------------------------------------------------- 단원 모듈
spec = importlib.util.spec_from_file_location("unit", UNITFILE)
U = importlib.util.module_from_spec(spec)
spec.loader.exec_module(U)


# ---------------------------------------------------------------- 글 속 숫자·영문자는 수식으로
def _math_plain(text):
    """'$수식$' 밖의 숫자·영문자를 수식으로: 대문자(점·도형 이름)는 rm, 소문자 한 글자는 기울임, 숫자는 그대로"""
    out = []
    for i, part in enumerate(re.split(r"(\$.+?\$)", text, flags=re.S)):
        if i % 2:
            out.append(part)
            continue
        part = re.sub(r"[A-Z]+(?:-[A-Z]+)*", lambda m: "$rm %s$" % m.group(0), part)
        part = re.sub(r"(?<![A-Za-z$])\d+(?:\.\d+)?", lambda m: "$%s$" % m.group(0), part)
        part = re.sub(r"(?<![A-Za-z$])[a-z](?![A-Za-z])", lambda m: "$%s$" % m.group(0), part)
        out.append(part)
    return "".join(out)


def _norm(o):
    if isinstance(o, str):
        return _math_plain(o)
    if isinstance(o, list):
        return [_norm(v) for v in o]
    if isinstance(o, dict):
        return {k: (v if k in ("pic", "syn") else _norm(v)) for k, v in o.items()}
    return o


for _it in U.ITEMS:
    if "h" not in _it:
        _it["q"] = _norm(_it["q"])
        _it["sol"] = _norm(_it["sol"])

# ---------------------------------------------------------------- 번호
_id = [1700000000]


def nid():
    _id[0] += 1
    return _id[0]


def renum(x):
    """복제한 개체의 id/instid를 새로 매긴다"""
    x = re.sub(r'(<hp:(?:tbl|rect|pic|equation|line|container|ellipse|polygon) id=")\d+(")',
               lambda m: m.group(1) + str(nid()) + m.group(2), x)
    x = re.sub(r'instid="\d+"', lambda m: 'instid="%d"' % nid(), x)
    return x


# ---------------------------------------------------------------- 수식
CACHE = os.path.join(HERE, "eqcache.json")
EQ = json.load(open(CACHE)) if os.path.exists(CACHE) else {}


def collect(obj, bag):
    if isinstance(obj, str):
        for m in re.finditer(r"\$(.+?)\$", obj, re.S):
            bag.add(m.group(1).strip())
    elif isinstance(obj, dict):
        if "syn" in obj:
            for row in obj["syn"]:
                for v in row:
                    if v:
                        bag.add(v.strip())
            return
        for v in obj.values():
            collect(v, bag)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            collect(v, bag)


def eq_sizes(scripts):
    todo = sorted(s for s in scripts if s not in EQ)
    if not todo:
        return
    res, latex = measure(todo)
    bad = []
    for sc, r, lx in zip(todo, res, latex):
        if r[3]:
            bad.append((sc, lx, r[3][:120]))
            w = 0.62 * len(sc) * 16 / 1.6
            r = [w, 18, 14, None]
        w, h, asc = r[0], r[1], r[2]
        W = int(68.8 * w + 61)
        if h > 20.5:
            H = int(max(1125, 57.14 * h + 303))
        elif "sqrt" in sc or "root" in sc:
            H = 1538
        elif "_" in sc:
            H = 1350
        elif "^" in sc:
            H = 1313
        else:
            H = 1125
        BL = int(max(50, min(90, 111.7 * (asc / h) - 2.6))) if h else 85
        EQ[sc] = (W, H, BL)
    json.dump(EQ, open(CACHE, "w"), ensure_ascii=False)
    for b in bad:
        print("수식 측정 근사:", b)


def eq_xml(sc):
    W, H, BL = EQ[sc]
    return ('<hp:equation id="%d" zOrder="0" numberingType="EQUATION" textWrap="TOP_AND_BOTTOM" textFlow="BOTH_SIDES" '
            'lock="0" dropcapstyle="None" version="Equation Version 60" baseLine="%d" textColor="#000000" baseUnit="1100" '
            'lineMode="CHAR" font="HancomEQN"><hp:sz width="%d" widthRelTo="ABSOLUTE" height="%d" heightRelTo="ABSOLUTE" protect="0"/>'
            '<hp:pos treatAsChar="1" affectLSpacing="0" flowWithText="1" allowOverlap="0" holdAnchorAndSO="0" vertRelTo="PARA" '
            'horzRelTo="PARA" vertAlign="TOP" horzAlign="LEFT" vertOffset="0" horzOffset="0"/>'
            '<hp:outMargin left="56" right="56" top="0" bottom="0"/><hp:shapeComment>수식입니다.</hp:shapeComment>'
            '<hp:script>%s</hp:script></hp:equation>') % (nid(), BL, W, H, escape(sc))


def inline(text):
    """'글자 $수식$' -> hp:t / hp:equation 열"""
    out = []
    for i, part in enumerate(re.split(r"\$(.+?)\$", text, flags=re.S)):
        if i % 2:
            out.append(eq_xml(part.strip()))
        elif part:
            segs = part.split("\n")
            t = "<hp:lineBreak/>".join(escape(s) for s in segs)
            out.append("<hp:t>%s</hp:t>" % t)
    return "".join(out) or "<hp:t/>"


def run(text, cp="0", extra=""):
    return '<hp:run charPrIDRef="%s">%s%s</hp:run>' % (cp, inline(text), extra)


def para(text, pp="3", cp="0", st="0", cb="0", pb="0", extra=""):
    return ('<hp:p id="0" paraPrIDRef="%s" styleIDRef="%s" pageBreak="%s" columnBreak="%s" merged="0">%s</hp:p>'
            % (pp, st, pb, cb, run(text, cp, extra)))


SUBLIST = ('<hp:subList id="" textDirection="HORIZONTAL" lineWrap="BREAK" vertAlign="%s" linkListIDRef="0" '
           'linkListNextIDRef="0" textWidth="0" textHeight="0" hasTextRef="0" hasNumRef="0">')


def cond_paras(lines):
    out = []
    for ln in lines:
        hang = bool(re.match(r"\s*(\([가-하]\)|[ㄱ-ㅎ]\.)", ln))
        out.append(para(ln, pp="85" if hang else "29", cp="16", st="2"))
    return "".join(out)


def replace_cell(tbl, row, col, inner):
    """(row,col) 칸의 subList 안 문단을 inner로 바꾼다"""
    for m in re.finditer(r"<hp:tc .*?</hp:tc>", tbl, re.S):
        tc = m.group(0)
        if '<hp:cellAddr colAddr="%d" rowAddr="%d"/>' % (col, row) in tc:
            a = tc.index(">", tc.index("<hp:subList")) + 1
            b = tc.rindex("</hp:subList>")
            new = tc[:a] + inner + tc[b:]
            return tbl[:m.start()] + new + tbl[m.end():]
    raise ValueError("cell not found")


# ---------------------------------------------------------------- 글상자 높이
# 글상자는 내용에 맞춰 늘어나지 않으므로 줄 수를 어림해 높이를 정한다.
# 기준(사용자 예시 44번): 글자 10pt·자간 -5%, 줄 간격 165% → 줄 사이 652,
# 줄 높이 = max(글자 1000, 그 줄 수식 높이), 글 너비 = 단 너비 - 글상자 여백 850 - 문단 오른쪽 여백 500
BOX_TEXT_W = 29211 - 850 - 500
HANG = 2241


def _char_w(ch):
    if ch == " ":
        return 475
    if "\uac00" <= ch <= "\ud7a3" or "\u3131" <= ch <= "\u318e":
        return 950
    if ch in ".,()[]:;'\"":
        return 330
    return 520


def _words(line):
    """줄을 (너비, 높이) 낱말 목록으로 쪼갠다. 수식은 낱말 안에 붙어 있을 수 있다."""
    words, cur_w, cur_h = [], 0, 1000
    for i, part in enumerate(re.split(r"\$(.+?)\$", line, flags=re.S)):
        if i % 2:
            W, H, _ = EQ[part.strip()]
            cur_w += W * 1.1 + 112
            cur_h = max(cur_h, H)
            continue
        for ch in part:
            if ch == " ":
                if cur_w:
                    words.append((cur_w, cur_h))
                cur_w, cur_h = 0, 1000
            else:
                cur_w += _char_w(ch)
    if cur_w:
        words.append((cur_w, cur_h))
    return words


def text_height(lines):
    heights = []
    for ln in lines:
        hang = bool(re.match(r"\s*(\([가-하]\)|[ㄱ-ㅎ]\.)", ln))
        for seg in ln.split("\n"):
            limit, x, h = BOX_TEXT_W, 0, 1000
            for w, wh in _words(seg):
                add = w if x == 0 else 475 + w
                if x and x + add > limit:
                    heights.append(h)
                    limit = BOX_TEXT_W - (HANG if hang else 0)
                    x, h = w, wh
                else:
                    x += add
                    h = max(h, wh)
            heights.append(h)
    return sum(heights) + 652 * (len(heights) - 1) + 567


def fill_rect(tbl, lines):
    """표 안 글상자(rect)에 조건/보기 문단을 넣고 높이를 맞춘다"""
    h = text_height(lines)
    r0 = tbl.index("<hp:rect ")
    r1 = tbl.index("</hp:rect>", r0)
    rect = tbl[r0:r1]
    a = rect.index(">", rect.index("<hp:subList", rect.index("<hp:drawText"))) + 1
    b = rect.index("</hp:subList>", a)
    rect = rect[:a] + cond_paras(lines) + rect[b:]
    rect = re.sub(r'<hp:curSz width="(\d+)" height="\d+"/>', lambda m: '<hp:curSz width="%s" height="%d"/>' % (m.group(1), h), rect, count=1)
    rect = re.sub(r'(<hp:rotationInfo angle="0" centerX="\d+" centerY=")\d+"', lambda m: m.group(1) + '%d"' % (h // 2), rect, count=1)
    rect = re.sub(r'(<hc:scaMatrix e1="[^"]+" e2="0" e3="0" e4="0" e5=")[^"]+"', lambda m: m.group(1) + '%.6f"' % (h / 8504), rect, count=1)
    rect = re.sub(r'(<hp:sz width="10000" widthRelTo="COLUMN" height=")\d+"', lambda m: m.group(1) + '%d"' % h, rect)
    return tbl[:r0] + rect + tbl[r1:]


def box_xml(lines):
    return renum(fill_rect(BOX, lines))


def bogi_xml(lines):
    return renum(fill_rect(BOGI, lines))


def syn_xml(rows):
    """조립제법 표. rows: [[나누는수, 계수...], [빈칸, ...], [빈칸, 몫..., 나머지]] (문자열은 수식)"""
    ncol = len(rows[0])
    cw, ch = 2700, 1750
    trs = []
    for r, cells in enumerate(rows):
        tcs = []
        for c in range(ncol):
            v = cells[c] if c < len(cells) else ""
            if c == 0:
                bf = "42"
            elif r == len(rows) - 1:
                bf = "43" if c == ncol - 1 else "44"
            else:
                bf = "40"
            body = run("$%s$" % v if v else "", "0")
            tcs.append(
                '<hp:tc name="" header="0" hasMargin="0" protect="0" editable="0" dirty="0" borderFillIDRef="%s">' % bf
                + SUBLIST % "CENTER"
                + '<hp:p id="0" paraPrIDRef="52" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0">%s</hp:p>' % body
                + "</hp:subList>"
                + '<hp:cellAddr colAddr="%d" rowAddr="%d"/><hp:cellSpan colSpan="1" rowSpan="1"/>' % (c, r)
                + '<hp:cellSz width="%d" height="%d"/><hp:cellMargin left="141" right="141" top="141" bottom="141"/></hp:tc>' % (cw, ch))
        trs.append("<hp:tr>%s</hp:tr>" % "".join(tcs))
    return ('<hp:tbl id="%d" zOrder="0" numberingType="TABLE" textWrap="TOP_AND_BOTTOM" textFlow="BOTH_SIDES" lock="0" '
            'dropcapstyle="None" pageBreak="CELL" repeatHeader="1" rowCnt="%d" colCnt="%d" cellSpacing="0" borderFillIDRef="40" noAdjust="0">'
            '<hp:sz width="%d" widthRelTo="ABSOLUTE" height="%d" heightRelTo="ABSOLUTE" protect="0"/>'
            '<hp:pos treatAsChar="1" affectLSpacing="0" flowWithText="1" allowOverlap="0" holdAnchorAndSO="0" vertRelTo="PARA" '
            'horzRelTo="PARA" vertAlign="TOP" horzAlign="LEFT" vertOffset="0" horzOffset="0"/>'
            '<hp:outMargin left="283" right="283" top="283" bottom="283"/><hp:inMargin left="141" right="141" top="141" bottom="141"/>%s</hp:tbl>'
            % (nid(), len(rows), ncol, cw * ncol, ch * len(rows), "".join(trs)))


def obj_para(obj_xml, pp="52"):
    return ('<hp:p id="0" paraPrIDRef="%s" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0">'
            '<hp:run charPrIDRef="0">%s<hp:t/></hp:run></hp:p>' % (pp, obj_xml))


CIRC = "①②③④⑤"


def choices_paras(ch):
    def cell(i):
        c = ch[i]
        return "%s %s" % (CIRC[i], c if ("$" in c or re.match(r"[ㄱ-ㅎ]", c)) else "$%s$" % c)
    long_ = max(len(re.sub(r"\$", "", c)) for c in ch) > 14
    if long_:
        groups = [[0, 1], [2, 3], [4]]
    else:
        groups = [[0, 1, 2], [3, 4]]
    return "".join(para("      ".join(cell(i) for i in g)) for g in groups)


def q_items(items, banner=None):
    """문항 본문 문단들. 첫 문단에 단원 머리표(banner)를 붙인다."""
    out = []
    for it in items:
        if isinstance(it, str):
            extra = ""
            if banner and not out:
                extra = banner
                banner = None
            out.append(para(it, extra=extra))
        elif "box" in it:
            out.append(obj_para(box_xml(it["box"]), pp="2").replace('styleIDRef="0"', 'styleIDRef="4"', 1)
                       .replace('<hp:run charPrIDRef="0">', '<hp:run charPrIDRef="5">', 1))
        elif "bogi" in it:
            out.append(obj_para(bogi_xml(it["bogi"]), pp="3"))
        elif "syn" in it:
            out.append(obj_para(syn_xml(it["syn"])))
        elif "pic" in it:
            out.append(renum(PICPARA[it["pic"]]))
        elif "ch" in it:
            out.append(choices_paras(it["ch"]))
        else:
            raise ValueError(it)
    if banner:
        out[0] = out[0].replace("</hp:run></hp:p>", banner + "</hp:run></hp:p>", 1)
    return "".join(out)


def endnote_para(n, ans, sol, src, cb):
    a = ans.strip()
    if "$" in a:
        ans_x = "<hp:t> [정답] </hp:t>" + inline(a)
    elif re.match(r"^[①-⑤ㄱ-ㅎ]", a) or not a:
        ans_x = "<hp:t> [정답] %s</hp:t>" % escape(a)
    else:
        ans_x = "<hp:t> [정답] </hp:t>" + eq_xml(a)
    first = ('<hp:p id="0" paraPrIDRef="30" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0"><hp:run charPrIDRef="37">'
             '<hp:ctrl><hp:autoNum num="%d" numType="ENDNOTE"><hp:autoNumFormat type="DIGIT" userChar="" prefixChar="" '
             'suffixChar=")" supscript="0"/></hp:autoNum></hp:ctrl>%s</hp:run></hp:p>') % (n, ans_x)
    body = []
    for s in sol:
        if isinstance(s, str):
            body.append(para(s, pp="30", cp="37"))
        elif "syn" in s:
            body.append(obj_para(syn_xml(s["syn"]), pp="30"))
        else:
            raise ValueError(s)
    srcx = '<hp:run charPrIDRef="34"><hp:t>%s</hp:t></hp:run>' % escape(src) if src else ""
    return ('<hp:p id="0" paraPrIDRef="31" styleIDRef="0" pageBreak="0" columnBreak="%d" merged="0"><hp:run charPrIDRef="39">'
            '<hp:ctrl><hp:endNote number="%d" suffixChar=")" instId="%d">' % (cb, n, nid())
            + SUBLIST % "TOP" + first + "".join(body) + "</hp:subList></hp:endNote></hp:ctrl></hp:run>"
            '<hp:run charPrIDRef="40"><hp:t><hp:tab width="4000" leader="0" type="1"/></hp:t></hp:run>' + srcx + "</hp:p>")


def heading(text, kind):
    tpl = HEAD2 if kind == 2 else HEAD
    old = "고난도" if kind == 2 else "다항식의 곱셈"
    return renum(tpl.replace("<hp:t>%s</hp:t>" % old, "<hp:t>%s</hp:t>" % escape(text)))


# ---------------------------------------------------------------- 조립
def build():
    items = U.ITEMS
    bag = set()
    collect(items, bag)
    for it in items:
        a = it.get("ans", "").strip()
        if a and "$" not in a and not re.match(r"^[①-⑤ㄱ-ㅎ]", a):
            bag.add(a)
    eq_sizes(bag)
    title, num = U.UNIT
    banner = renum(BANNER.replace("<hp:t>다항식의 연산</hp:t>", "<hp:t>%s</hp:t>" % escape(title))
                   .replace("<hp:t>01</hp:t>", "<hp:t>%s</hp:t>" % num))
    body = []
    first = items[0]
    assert first.get("h")
    body.append(renum(P0.replace("<hp:t>다항식의 덧셈과 뺄셈</hp:t>", "<hp:t>%s</hp:t>" % escape(first["h"]))))
    n = 0
    after_head = True
    for it in items[1:]:
        if it.get("h"):
            body.append(heading(it["h"], it.get("kind", 1)))
            after_head = True
            continue
        n += 1
        body.append(endnote_para(n, it["ans"], it["sol"], it.get("src", ""), 0 if after_head else 1))
        body.append(q_items(it["q"], banner if n == 1 else None))
        after_head = False
    tail = [t.replace("<hp:t>다항식의 연산</hp:t>", "<hp:t>%s</hp:t>" % escape(title)) for t in TAIL]
    sec = SEC_HEAD + "".join(body) + "".join(tail) + "</hs:sec>"
    return sec, n


def main():
    sec, n = build()
    title, num = U.UNIT
    used = set(re.findall(r'binaryItemIDRef="(image\d+)"', sec))
    files = dict(FILES)
    files["Contents/section0.xml"] = sec.encode("utf-8")
    for mp in ("Contents/masterpage0.xml", "Contents/masterpage1.xml"):
        files[mp] = files[mp].decode("utf-8").replace("<hp:t>다항식의 연산</hp:t>", "<hp:t>%s</hp:t>" % escape(title)).encode("utf-8")
    hpf = files["Contents/content.hpf"].decode("utf-8")
    drop = set()
    for m in re.finditer(r'<opf:item id="(image\d+)" href="([^"]+)"[^>]*/>', hpf):
        if m.group(1) not in used:
            drop.add(m.group(2))
            hpf = hpf.replace(m.group(0), "")
    files["Contents/content.hpf"] = hpf.encode("utf-8")
    files["settings.xml"] = re.sub(rb'paraIDRef="\d+" pos="\d+"', b'paraIDRef="0" pos="0"', files["settings.xml"])
    with zipfile.ZipFile(OUT, "w") as z:
        for name in ORDER:
            if name in drop:
                continue
            ct = zipfile.ZIP_STORED if name == "mimetype" else zipfile.ZIP_DEFLATED
            z.writestr(zipfile.ZipInfo(name, date_time=(2026, 10, 9, 0, 0, 0)), files[name], compress_type=ct)
    print("문항 %d개 -> %s (그림 %s)" % (n, OUT, ", ".join(sorted(used))))


if __name__ == "__main__":
    main()
