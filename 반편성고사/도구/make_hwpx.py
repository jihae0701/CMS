# -*- coding: utf-8 -*-
"""학원에서 편집한 공통수학1 시험지(hwpx)를 틀로 진단평가 시험지(hwpx) 생성
- 표지·머리말·쪽 번호·흐린 CLIMATH 로고·'5지선다형/단답형' 표시·조건 상자 모양은 틀을 그대로 사용
- 미주(정답·해설)는 각 문제 첫 문단 맨 앞, 배점은 발문 끝, 해설에 '[해설]' 표기 없음
사용: python make_hwpx.py <틀.hwpx> <그림폴더> <출력폴더>
"""
import sys, os, re, zipfile, random
from xml.sax.saxutils import escape
from PIL import Image
from problems import M1, M2, points
from eqmeasure import measure

TPL, FIGDIR, OUTDIR = sys.argv[1:4]
os.makedirs(OUTDIR, exist_ok=True)
random.seed(20261008)
CIRC = "①②③④⑤"
COLW = 29620                       # 단 너비(HWPUNIT)
FIGW = {"room.png": 19000, "chair.png": 16000, "mapping.png": 15000, "sqrt.png": 16000,
        "reflect.png": 16500, "twocurve.png": 15500, "circleline.png": 17000, "tangent2.png": 15500}
# 단 구성: 한 단에 한 문항 또는 두 문항 (14단 = 7쪽)
LAYOUT = [[1, 2], [3, 4], [5, 6], [7, 8], [9, 10], [11], [12], [13], [14], [15, 16], [17], [18], [19], [20]]

_id = [1300000000]
def nid():
    _id[0] += 1
    return _id[0]
_z = [2000]
def nz():
    _z[0] += 1
    return _z[0]

# ---------- 틀 읽기 ----------
ZIN = zipfile.ZipFile(TPL)
FILES = {i.filename: ZIN.read(i.filename) for i in ZIN.infolist()}
ORDER = [i.filename for i in ZIN.infolist()]
SEC = FILES["Contents/section0.xml"].decode("utf-8")

def top_paras(x):
    """최상위 문단 (시작, 끝) 목록"""
    root = x.index(">", x.index("<hs:sec")) + 1
    out, depth, cur = [], 0, None
    for m in re.finditer(r"<(/?)hp:p\b[^>]*?(/?)>", x[root:]):
        close, selfc = m.group(1), m.group(2)
        if not close and not selfc:
            if depth == 0:
                cur = root + m.start()
            depth += 1
        elif close:
            depth -= 1
            if depth == 0:
                out.append((cur, root + m.end()))
    return out

SPANS = top_paras(SEC)
PARA = [SEC[a:b] for a, b in SPANS]
FIRST = next(i for i, p in enumerate(PARA) if "<hp:endNote " in p)          # 1번 문항 문단
QA = next(i for i, p in enumerate(PARA) if "(빠른 정답)" in p)               # 빠른 정답 표
PREFIX = SEC[:SPANS[FIRST][0]]
QA_HEAD = PARA[QA]
QA_LINE = PARA[QA + 1]
TAIL_PARAS = PARA[QA + 21:]
TAIL_END = SEC[SPANS[-1][1]:]
HDR_ODD = re.search(r'<hp:ctrl><hp:header id="1" applyPageType="ODD">.*?</hp:header></hp:ctrl>', SEC, re.S).group(0)
WM = re.search(r'<hp:pic [^>]*textWrap="BEHIND_TEXT"(?:(?!</hp:pic>).)*?vertOffset="45354".*?</hp:pic>', SEC, re.S).group(0)
SHORT = re.sub(r"<hp:linesegarray>.*?</hp:linesegarray>", "", next(p for p in PARA if "<hp:t>단답형</hp:t>" in p and "<hp:tbl " in p), flags=re.S)
BOX = next(p for p in PARA if "<hp:rect " in p and "<hp:tbl " in p and "<hp:endNote " not in p and 'rowCnt="4"' in p)
PIC = next(p for p in PARA if 'binaryItemIDRef="image2"' in p)
PIC = re.search(r"<hp:pic .*?</hp:pic>", PIC, re.S).group(0)

# ---------- 수식 ----------
EQ = {}
def collect(text, bag):
    for m in re.finditer(r"\$(.+?)\$", text):
        bag.add(m.group(1))

def eq_sizes(scripts):
    scripts = sorted(scripts - set(EQ))
    if not scripts:
        return
    res, latex = measure(scripts)
    for sc, r, lx in zip(scripts, res, latex):
        if r[3]:
            raise SystemExit("수식 변환 오류: %s -> %s (%s)" % (sc, lx, r[3]))
        w, h, asc = r[0], r[1], r[2]
        # 학원 편집본(한글이 다시 계산한 크기 330개)으로 맞춘 근사식
        W = int(68.8 * w + 61)
        if h > 20.5:
            H = int(max(1125, 57.14 * h + 303))
        elif "sqrt" in sc:
            H = 1538
        elif "_" in sc:
            H = 1350
        elif "^" in sc:
            H = 1313
        else:
            H = 1125
        BL = int(max(50, min(90, 111.7 * (asc / h) - 2.6))) if h else 85
        EQ[sc] = (W, H, BL)

def eq_xml(sc):
    W, H, BL = EQ[sc]
    return ('<hp:equation id="%d" zOrder="%d" numberingType="EQUATION" textWrap="TOP_AND_BOTTOM" textFlow="BOTH_SIDES" lock="0" '
            'dropcapstyle="None" version="Equation Version 60" baseLine="%d" textColor="#000000" baseUnit="1100" lineMode="CHAR" font="HancomEQN">'
            '<hp:sz width="%d" widthRelTo="ABSOLUTE" height="%d" heightRelTo="ABSOLUTE" protect="0"/>'
            '<hp:pos treatAsChar="1" affectLSpacing="0" flowWithText="1" allowOverlap="0" holdAnchorAndSO="0" vertRelTo="PARA" horzRelTo="PARA" '
            'vertAlign="TOP" horzAlign="LEFT" vertOffset="0" horzOffset="0"/><hp:outMargin left="0" right="0" top="0" bottom="0"/>'
            '<hp:shapeComment>수식입니다.</hp:shapeComment><hp:script>%s</hp:script></hp:equation>') % (nid(), nz(), BL, W, H, escape(sc))

TAB = '<hp:tab width="%d" leader="0" type="1"/>'

def content(text, lead_tab=False):
    """'글자 $수식$' -> hp:t / hp:equation 열"""
    out = ["<hp:t>%s</hp:t>" % (TAB % 4000)] if lead_tab else []
    for i, part in enumerate(re.split(r"\$(.+?)\$", text)):
        if i % 2:
            out.append(eq_xml(part))
        elif part:
            out.append("<hp:t>%s</hp:t>" % escape(part))
    out.append("<hp:t/>")
    return "".join(out)

def para(inner, pp=17, st=0, cb=False):
    return ('<hp:p id="2147483648" paraPrIDRef="%d" styleIDRef="%d" pageBreak="0" columnBreak="%d" merged="0">%s</hp:p>'
            % (pp, st, 1 if cb else 0, inner))

def run(inner, cp=36):
    return '<hp:run charPrIDRef="%d">%s</hp:run>' % (cp, inner)

def blank():
    return '<hp:p id="0" paraPrIDRef="17" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0"><hp:run charPrIDRef="36"/></hp:p>'

def is_display(text):
    t = text.strip().rstrip(",").strip()
    return t.startswith("$") and t.endswith("$") and t.count("$") == 2

# ---------- 폭·높이 어림 ----------
def text_w(text, han=1060, sp=500, oth=800):
    w = 0
    for i, part in enumerate(re.split(r"\$(.+?)\$", text)):
        if i % 2:
            w += EQ[part][0]
        else:
            for c in part:
                w += han if "가" <= c <= "힣" else sp if c == " " else oth
    return w

def tall(text):
    return max([EQ[m][1] for m in re.findall(r"\$(.+?)\$", text)] + [1125])

def lines_h(text, width=COLW, pitch=1650, scale=1.0):
    n = max(1, -(-int(text_w(text) * scale * 1.03) // width))
    return n * pitch + (tall(text) - 1125)

# ---------- 미주 ----------
def endnote(pr):
    ans = CIRC[pr["ans"] - 1] if pr["choices"] else str(pr["ans"])
    ps = [para(run('<hp:ctrl><hp:autoNum num="%d" numType="ENDNOTE"><hp:autoNumFormat type="DIGIT" userChar="" prefixChar="" '
                   'suffixChar=")" supscript="0"/></hp:autoNum></hp:ctrl><hp:t> [정답] %s</hp:t>' % (pr["no"], ans), 3))]
    for l in pr["sol"]:
        ps.append(para(run(content(l), 3)))
    return ('<hp:ctrl><hp:endNote number="%d" suffixChar="41" instId="%d"><hp:subList id="" textDirection="HORIZONTAL" lineWrap="BREAK" '
            'vertAlign="TOP" linkListIDRef="0" linkListNextIDRef="0" textWidth="0" textHeight="0" hasTextRef="0" hasNumRef="0">%s'
            '</hp:subList></hp:endNote></hp:ctrl>') % (pr["no"], random.randint(10 ** 9, 2 * 10 ** 9), "".join(ps))

# ---------- 조건 상자(모의고사 모양) ----------
def box_xml(lines):
    inner, nline = [], 0
    for l in lines:
        n = max(1, -(-int(text_w(l, 1106, 520, 830) * 1.04) // 28361))
        nline += n
        inner.append(para(run(content(l), 3), pp=53))
    extra = sum(max(0, tall(l) - 1350) for l in lines)
    hr = nline * 1724 - 10 + extra
    x = BOX
    x = re.sub(r"(<hp:drawText [^>]*><hp:subList [^>]*>).*?(</hp:subList>)", lambda m: m.group(1) + "".join(inner) + m.group(2), x, count=1, flags=re.S)
    x = re.sub(r'(<hp:tbl [^>]*>)<hp:sz width="(\d+)" widthRelTo="ABSOLUTE" height="\d+"',
               lambda m: m.group(1) + '<hp:sz width="%s" widthRelTo="ABSOLUTE" height="%d"' % (m.group(2), hr + 1001), x, count=1)
    x = re.sub(r'<hp:curSz width="(\d+)" height="\d+"/>', lambda m: '<hp:curSz width="%s" height="%d"/>' % (m.group(1), hr), x, count=1)
    x = re.sub(r'(<hp:rotationInfo angle="0" centerX="\d+") centerY="\d+"', lambda m: m.group(1) + ' centerY="%d"' % (hr // 2), x, count=1)
    x = re.sub(r'(<hc:scaMatrix e1="[\d.]+" e2="0" e3="0" e4="0") e5="[\d.]+"', lambda m: m.group(1) + ' e5="%.6f"' % (hr / 8504), x, count=1)
    x = re.sub(r'<hp:tbl id="\d+" zOrder="\d+"', lambda m: '<hp:tbl id="%d" zOrder="%d"' % (nid(), nz()), x, count=1)
    x = re.sub(r'<hp:rect id="\d+" zOrder="\d+"', lambda m: '<hp:rect id="%d" zOrder="%d"' % (nid(), nz()), x, count=1)
    x = re.sub(r' instid="\d+"', lambda m: ' instid="%d"' % nid(), x)
    x = re.sub(r"<hp:linesegarray>.*?</hp:linesegarray>", "", x, flags=re.S)
    return x, hr + 1001 + 900

# ---------- 그림 ----------
BIN = []
def pic_xml(fname):
    path = os.path.join(FIGDIR, fname)
    BIN.append(path)
    bid = "image%d" % (len(BIN) + 1)          # image1 은 CLIMATH 로고
    pw, ph = Image.open(path).size
    ow, oh = pw * 75, ph * 75
    cw = FIGW[fname]
    ch = int(cw * ph / pw)
    x = PIC
    x = re.sub(r'<hp:pic id="\d+" zOrder="\d+"', '<hp:pic id="%d" zOrder="%d"' % (nid(), nz()), x, count=1)
    x = re.sub(r' instid="\d+"', ' instid="%d"' % nid(), x, count=1)
    x = re.sub(r'<hp:orgSz width="\d+" height="\d+"/>', '<hp:orgSz width="%d" height="%d"/>' % (ow, oh), x)
    x = re.sub(r'<hp:curSz width="\d+" height="\d+"/>', '<hp:curSz width="%d" height="%d"/>' % (cw, ch), x)
    x = re.sub(r'centerX="\d+" centerY="\d+"', 'centerX="%d" centerY="%d"' % (cw // 2, ch // 2), x)
    x = re.sub(r"<hp:renderingInfo>.*?</hp:renderingInfo>",
               '<hp:renderingInfo><hc:transMatrix e1="1" e2="0" e3="0" e4="0" e5="1" e6="0"/>'
               '<hc:scaMatrix e1="%.5f" e2="0" e3="0" e4="0" e5="%.5f" e6="0"/><hc:rotMatrix e1="1" e2="0" e3="0" e4="0" e5="1" e6="0"/></hp:renderingInfo>'
               % (cw / ow, ch / oh), x, flags=re.S)
    x = x.replace('binaryItemIDRef="image2"', 'binaryItemIDRef="%s"' % bid)
    x = re.sub(r"<hp:imgRect>.*?</hp:imgRect>", '<hp:imgRect><hc:pt0 x="0" y="0"/><hc:pt1 x="%d" y="0"/><hc:pt2 x="%d" y="%d"/><hc:pt3 x="0" y="%d"/></hp:imgRect>'
               % (ow, ow, oh, oh), x, flags=re.S)
    x = re.sub(r'<hp:imgClip [^>]*/>', '<hp:imgClip left="0" right="%d" top="0" bottom="%d"/>' % (ow, oh), x)
    x = re.sub(r'<hp:imgDim [^>]*/>', '<hp:imgDim dimwidth="%d" dimheight="%d"/>' % (ow, oh), x)
    x = re.sub(r'<hp:sz width="\d+" widthRelTo="ABSOLUTE" height="\d+"', '<hp:sz width="%d" widthRelTo="ABSOLUTE" height="%d"' % (cw, ch), x)
    return para(run(x + "<hp:t/>"), pp=50), ch + 1200

def watermark(first_page):
    x = WM
    x = re.sub(r'<hp:pic id="\d+" zOrder="\d+"', '<hp:pic id="%d" zOrder="%d"' % (nid(), _z[0] % 7), x, count=1)
    x = re.sub(r' instid="\d+"', ' instid="%d"' % nid(), x, count=1)
    x = re.sub(r'vertOffset="\d+"', 'vertOffset="%d"' % (48189 if first_page else 45354), x, count=1)
    return run(x + "<hp:t/>")

# ---------- 선지 ----------
def choice_lines(ch):
    def line(items, start):
        out, pos = [], 0
        for k, sc in enumerate(items):
            if k:
                stop = 9870 * k
                out.append("<hp:t>%s%s </hp:t>" % (TAB % max(300, stop - pos), CIRC[start + k]))
                pos = stop
            else:
                out.append("<hp:t>%s </hp:t>" % CIRC[start])
            out.append(eq_xml(sc))
            pos += 1300 + EQ[sc][0]
        out.append("<hp:t/>")
        return para(run("".join(out)), pp=54)
    h = 2 * (max(EQ[c][1] for c in ch) + 550)
    return line(ch[:3], 0) + line(ch[3:], 3), h

# ---------- 문항 ----------
def problem(pr, colbreak, extra_run=""):
    tag = " [%d점]" % points(pr)
    body, body2 = list(pr["body"]), list(pr.get("body2", []))
    if body2:
        body2[-1] += tag
    else:
        body[-1] += tag
    out, h = [], 600
    first = run(endnote(pr), 43) + extra_run + run(content(body[0]))
    out.append(para(first, pp=45, cb=colbreak))
    h += lines_h(body[0]) + 500
    for l in body[1:]:
        out.append(para(run(content(l, is_display(l)))))
        h += lines_h(l)
    def add_fig():
        nonlocal h
        x, fh = pic_xml(pr["fig"])
        out.append(x); h += fh
    def add_box():
        nonlocal h
        x, bh = box_xml(pr["box"])
        out.append(x); h += bh
    if pr.get("fig") and not pr.get("figlast"):
        add_fig()
        for l in body2:
            out.append(para(run(content(l, is_display(l))))); h += lines_h(l)
        if pr.get("box"):
            add_box()
    else:
        if pr.get("box"):
            add_box()
        for l in body2:
            out.append(para(run(content(l, is_display(l))))); h += lines_h(l)
        if pr.get("fig"):
            add_fig()
    if pr["choices"]:
        out.append(blank()); h += 1650
        x, chh = choice_lines(pr["choices"])
        out.append(x); h += chh
    return "".join(out), h

def build(M, subject, outname):
    global BIN
    BIN = []
    bag = set()
    for p in M:
        for l in p["body"] + p.get("body2", []) + (p.get("box") or []) + p["sol"]:
            collect(l, bag)
        for c in p["choices"] or []:
            bag.add(c)
    eq_sizes(bag)
    byno = {p["no"]: p for p in M}
    prefix = PREFIX.replace("공통수학1", subject).replace("반편성고사", "진단평가")
    hdr = HDR_ODD.replace("공통수학1", subject)
    cap_first, cap = 70000, 82000
    parts = []
    for ci, grp in enumerate(LAYOUT):
        page_first = ci % 2 == 0
        for gi, no in enumerate(grp):
            pr = byno[no]
            extra = ""
            if gi == 0 and page_first:
                extra += watermark(ci == 0)
            if no == 5:
                extra = hdr.replace("<hp:ctrl>", "<hp:run charPrIDRef=\"43\"><hp:ctrl>", 1).replace("</hp:header></hp:ctrl>", "</hp:header></hp:ctrl></hp:run>", 1) + extra
            colbreak = gi == 0 and ci > 0
            if no == 15:      # '단답형' 표시가 단의 첫 줄
                parts.append(SHORT.replace('columnBreak="0"', 'columnBreak="1"', 1))
                colbreak = False
            x, h = problem(pr, colbreak, extra)
            parts.append(x)
            if gi == 0 and len(grp) == 2:
                c = cap_first if ci == 0 else cap
                nxt = problem_height(byno[grp[1]])
                pad = int(min(c * 0.5 - h, c - 6000 - h - nxt) // 1650)
                parts.append(blank() * max(3, pad))
                if h + 3 * 1650 + nxt > c - 3000:
                    print("  주의: %s %d·%d번 한 단에 넣기 빠듯함 (어림 %d/%d)" % (subject, grp[0], grp[1], h + nxt, c))
            elif h > (cap_first if ci == 0 else cap) - 3000:
                print("  주의: %s %d번 단 높이 초과 가능 (어림 %d)" % (subject, no, h))
    # 빠른 정답
    qa = [QA_HEAD.replace("공통수학1", subject).replace("예비고1 반편성고사", "예비고1 진단평가")]
    for p in M:
        ans = CIRC[p["ans"] - 1] if p["choices"] else str(p["ans"])
        line = re.sub(r'<hp:autoNum num="\d+"', '<hp:autoNum num="%d"' % p["no"], QA_LINE, count=1)
        line = re.sub(r"<hp:t> \[정답\][^<]*</hp:t>", "<hp:t> [정답] %s   (%d점, %s)</hp:t>" % (ans, points(p), p["unit"]), line, count=1)
        qa.append(re.sub(r"<hp:linesegarray>.*?</hp:linesegarray>", "", line, flags=re.S))
    sec = prefix + "".join(parts) + "".join(qa) + "".join(TAIL_PARAS) + TAIL_END
    write(sec, subject, outname)

_heights = {}
def problem_height(pr):
    if pr["no"] not in _heights:
        state = (_id[0], _z[0], list(BIN))
        _heights[pr["no"]] = problem(pr, False)[1]
        _id[0], _z[0] = state[0], state[1]
        BIN[:] = state[2]
    return _heights[pr["no"]]

def preview_digit(png, digit):
    """파일 미리보기 그림(표지)의 '공통수학1' 끝 숫자만 바꿈 (한글에서 저장하면 다시 만들어짐)"""
    import io
    from PIL import ImageDraw, ImageFont
    font = os.path.expanduser("~/.fonts/NotoSansKR-800.ttf")
    if not os.path.exists(font):
        return png
    im = Image.open(io.BytesIO(png)).convert("RGB")
    px = im.load()
    ys = [y for y in range(140, 280) if any(px[x, y][0] < 128 for x in range(200, 520))]
    if not ys:
        return png
    y0, y1 = min(ys), max(ys)
    dark = [x for x in range(200, 520) if any(px[x, y][0] < 128 for y in range(y0, y1 + 1))]
    x1 = max(dark)
    x0 = x1
    while x0 - 1 in dark:
        x0 -= 1
    d = ImageDraw.Draw(im)
    d.rectangle([x0 - 2, y0 - 2, x1 + 6, y1 + 2], fill="white")
    f = ImageFont.truetype(font, int((y1 - y0) * 1.32))
    bb = d.textbbox((0, 0), digit, font=f)
    d.text((x0 - bb[0], y0 - bb[1]), digit, fill="black", font=f)
    out = io.BytesIO()
    im.save(out, "PNG")
    return out.getvalue()

def write(sec, subject, outname):
    files = dict(FILES)
    files["Contents/section0.xml"] = sec.encode("utf-8")
    for k in [k for k in files if re.match(r"BinData/image\d+\.png$", k) and k != "BinData/image1.png"]:
        del files[k]
    items = ['<opf:item id="image1" href="BinData/image1.png" media-type="image/png" isEmbeded="1"/>']
    for i, pth in enumerate(BIN):
        name = "BinData/image%d.png" % (i + 2)
        files[name] = open(pth, "rb").read()
        items.append('<opf:item id="image%d" href="%s" media-type="image/png" isEmbeded="1"/>' % (i + 2, name))
    hpf = files["Contents/content.hpf"].decode("utf-8")
    hpf = re.sub(r'(<opf:item id="image\d+"[^>]*/>)+', "".join(items), hpf, count=1)
    hpf = re.sub(r"<opf:title>.*?</opf:title>", "<opf:title>예비고1 진단평가 %s</opf:title>" % subject, hpf, flags=re.S)
    files["Contents/content.hpf"] = hpf.encode("utf-8")
    prv = files["Preview/PrvText.txt"].decode("utf-8", "ignore").replace("공통수학1", subject)
    files["Preview/PrvText.txt"] = prv.encode("utf-8")
    if subject[-1] != "1":
        files["Preview/PrvImage.png"] = preview_digit(files["Preview/PrvImage.png"], subject[-1])
    order = [k for k in ORDER if k in files and not k.startswith("BinData/")]
    bins = sorted([k for k in files if k.startswith("BinData/")], key=lambda s: int(re.search(r"(\d+)", s).group(1)))
    k = order.index("Contents/header.xml") + 1
    order = order[:k] + bins + order[k:]
    path = os.path.join(OUTDIR, outname)
    with zipfile.ZipFile(path, "w") as z:
        for name in order:
            ct = zipfile.ZIP_STORED if name in ("mimetype", "version.xml") or name.endswith(".png") else zipfile.ZIP_DEFLATED
            z.writestr(zipfile.ZipInfo(name, date_time=(2026, 10, 8, 0, 0, 0)), files[name], compress_type=ct)
    print(path)

build(M1, "공통수학1", "예비고1_진단평가_공통수학1.hwpx")
_heights.clear()
build(M2, "공통수학2", "예비고1_진단평가_공통수학2.hwpx")
