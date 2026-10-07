# -*- coding: utf-8 -*-
"""업로드된 모의고사 HML을 템플릿으로 반편성고사 시험지(HML) 생성
- 출처 표 없음, 미주(정답·해설)는 각 문제 첫 문단 맨 앞, 배점은 발문 끝
사용: python make_exam.py <템플릿.hml> <그림폴더> <출력폴더>
"""
import sys, os, re, base64, random, json
from xml.sax.saxutils import escape
from PIL import Image
from problems import M1, M2, PTS, points
from eqmeasure import measure

TPL, FIGDIR, OUTDIR = sys.argv[1:4]
os.makedirs(OUTDIR, exist_ok=True)
SRC = open(TPL, encoding="utf-8").read()
random.seed(20261207)
_z = [600000]

def inst():
    return random.randint(1000000, 99999999)

def zorder():
    _z[0] += 1
    return _z[0]

CIRC = "①②③④⑤"

# ---------- 수식 ----------
EQ = {}

def collect(text, bag):
    for m in re.finditer(r"\$(.+?)\$", text):
        bag.add(m.group(1))

def eq_sizes(scripts):
    scripts = sorted(scripts)
    res, latex = measure(scripts)
    for sc, r, lx in zip(scripts, res, latex):
        if r[3]:
            raise SystemExit("수식 변환 오류: %s -> %s (%s)" % (sc, lx, r[3]))
        w, h, asc = r[0], r[1], r[2]
        W = int(70.39 * w + 184)
        H = int(max(1125, 114.1 * h - 930))
        BL = int(max(50, min(90, 199.3 * (asc / h) - 71.6))) if h else 85
        EQ[sc] = (W, H, BL)

def eq_xml(sc):
    W, H, BL = EQ[sc]
    return ('<EQUATION BaseLine="%d" BaseUnit="1100" LineMode="false" TextColor="0" Version="Equation Version 60">'
            '<SHAPEOBJECT InstId="%d" Lock="false" NumberingType="Equation" ZOrder="%d">'
            '<SIZE Height="%d" HeightRelTo="Absolute" Protect="false" Width="%d" WidthRelTo="Absolute"/>'
            '<POSITION AffectLSpacing="false" AllowOverlap="false" FlowWithText="true" HoldAnchorAndSO="false" HorzAlign="Left" HorzOffset="0" HorzRelTo="Para" TreatAsChar="true" VertAlign="Top" VertOffset="0" VertRelTo="Para"/>'
            '<OUTSIDEMARGIN Bottom="0" Left="0" Right="0" Top="0"/><SHAPECOMMENT>수식입니다.</SHAPECOMMENT></SHAPEOBJECT>'
            '<SCRIPT>%s</SCRIPT></EQUATION>') % (BL, inst(), zorder(), H, W, escape(sc))

def runs(text):
    """'글자 $수식$ 글자' -> CHAR/EQUATION 요소열"""
    out = []
    for i, part in enumerate(re.split(r"\$(.+?)\$", text)):
        if i % 2:
            out.append(eq_xml(part))
        elif part:
            out.append("<CHAR>%s</CHAR>" % escape(part))
    return "".join(out)

def para(text, shape=1, tab=False, extra=""):
    lead = "<CHAR><TAB/></CHAR>" if tab else ""
    return '<P ParaShape="%d" Style="0"%s><TEXT CharShape="0">%s%s<CHAR></CHAR></TEXT></P>' % (shape, extra, lead, runs(text))

def is_display(text):
    t = text.strip().rstrip(",").strip()
    return t.startswith("$") and t.endswith("$") and t.count("$") == 2

# ---------- 조건 상자 ----------
def box_xml(lines):
    ps = "".join('<P ParaShape="1" Style="0"><TEXT CharShape="0">%s</TEXT></P>' % runs(l) for l in lines)
    return ('<P ParaShape="1" Style="0"><TEXT CharShape="0">'
            '<TABLE BorderFill="1" CellSpacing="0" ColCount="1" PageBreak="Cell" RepeatHeader="true" RowCount="1">'
            '<SHAPEOBJECT InstId="%d" Lock="false" NumberingType="Table" ZOrder="%d">'
            '<SIZE Height="%d" HeightRelTo="Absolute" Protect="false" Width="28776" WidthRelTo="Absolute"/>'
            '<POSITION AffectLSpacing="false" AllowOverlap="false" FlowWithText="true" HoldAnchorAndSO="false" HorzAlign="Left" HorzOffset="0" HorzRelTo="Para" TreatAsChar="true" VertAlign="Top" VertOffset="0" VertRelTo="Para"/>'
            '<OUTSIDEMARGIN Bottom="0" Left="0" Right="0" Top="0"/></SHAPEOBJECT>'
            '<INSIDEMARGIN Bottom="1133" Left="0" Right="0" Top="1133"/><ROW>'
            '<CELL BorderFill="8" ColAddr="0" ColSpan="1" Dirty="false" Editable="false" HasMargin="false" Header="false" Height="282" Protect="false" RowAddr="0" RowSpan="1" Width="28776">'
            '<CELLMARGIN Bottom="566" Left="850" Right="850" Top="566"/>'
            '<PARALIST LineWrap="Break" LinkListID="0" LinkListIDNext="0" TextDirection="0" VertAlign="Center">%s</PARALIST>'
            '</CELL></ROW></TABLE><CHAR></CHAR></TEXT></P>') % (inst(), zorder(), 2000 + 1900 * len(lines), ps)

# ---------- 그림 ----------
BIN = []  # (id, path)
PIC_TPL = open(os.path.join(os.path.dirname(TPL), "tpl_picture.xml"), encoding="utf-8").read()

def pic_xml(fname, width):
    path = os.path.join(FIGDIR, fname)
    BIN.append(path)
    bid = len(BIN)
    pw, ph = Image.open(path).size
    oriW, oriH = pw * 75, ph * 75
    curW = width
    curH = int(width * ph / pw)
    x = PIC_TPL
    x = re.sub(r'<SHAPECOMMENT>.*?</SHAPECOMMENT><CAPTION.*?</CAPTION>', '<SHAPECOMMENT>그림입니다.</SHAPECOMMENT>', x, flags=re.S)
    x = re.sub(r'InstId="\d+"', 'InstId="%d"' % inst(), x, count=1)
    x = re.sub(r'ZOrder="\d+"', 'ZOrder="%d"' % zorder(), x, count=1)
    x = x.replace('<SIZE Height="12514"', '<SIZE Height="%d"' % curH).replace('Width="16038" WidthRelTo', 'Width="%d" WidthRelTo' % curW)
    x = x.replace('CurHeight="12514" CurWidth="16038"', 'CurHeight="%d" CurWidth="%d"' % (curH, curW))
    x = x.replace('InstID="1039776602"', 'InstID="%d"' % inst())
    x = x.replace('OriHeight="23175" OriWidth="29700"', 'OriHeight="%d" OriWidth="%d"' % (oriH, oriW))
    x = x.replace('CenterX="8019" CenterY="6257"', 'CenterX="%d" CenterY="%d"' % (curW // 2, curH // 2))
    x = x.replace('<SCAMATRIX E1="0.54000" E2="0.00000" E3="0.00000" E4="0.00000" E5="0.53998" E6="0.00000"/>',
                  '<SCAMATRIX E1="%.5f" E2="0.00000" E3="0.00000" E4="0.00000" E5="%.5f" E6="0.00000"/>' % (curW / oriW, curH / oriH))
    x = x.replace('X1="29700" X2="29700"', 'X1="%d" X2="%d"' % (oriW, oriW)).replace('Y2="23175" Y3="23175"', 'Y2="%d" Y3="%d"' % (oriH, oriH))
    x = x.replace('<IMAGECLIP Bottom="23160" Left="0" Right="29700" Top="0"/>', '<IMAGECLIP Bottom="%d" Left="0" Right="%d" Top="0"/>' % (oriH, oriW))
    x = x.replace('<IMAGEDIM Height="23160" Width="29700"/>', '<IMAGEDIM Height="%d" Width="%d"/>' % (oriH, oriW))
    x = x.replace('BinItem="1"', 'BinItem="%d"' % bid)
    return '<P ParaShape="11" Style="0"><TEXT CharShape="0">%s<CHAR></CHAR></TEXT></P>' % x

FIGW = {"room.png": 19000, "chair.png": 16000, "mapping.png": 15000, "sqrt.png": 16000,
        "reflect.png": 16500, "twocurve.png": 15500, "circleline.png": 17000}

# ---------- 선지 ----------
T = 4000  # 기본 탭 간격(추정)

def choice_lines(ch):
    def line(items, start):
        out, pos = [], 0
        for k, sc in enumerate(items):
            w = 1300 + EQ[sc][0]
            if k:
                target = max(k * 9000, pos + 700)
                tabs = 0
                while pos < target:
                    pos = (pos // T + 1) * T
                    tabs += 1
                out.append("<CHAR>%s%s </CHAR>" % ("<TAB/>" * tabs, CIRC[start + k]))
            else:
                out.append("<CHAR>%s </CHAR>" % CIRC[start])
            out.append(eq_xml(sc))
            pos += w
        return '<P ParaShape="1" Style="0"><TEXT CharShape="0">%s<CHAR></CHAR></TEXT></P>' % "".join(out)
    return line(ch[:3], 0) + line(ch[3:], 3)

# ---------- 미주(정답·해설) ----------
def endnote(pr):
    ans = CIRC[pr["ans"] - 1] if pr["choices"] else str(pr["ans"])
    ps = ['<P ParaShape="1" Style="0"><TEXT CharShape="0"><AUTONUM Number="%d" NumberType="Endnote">'
          '<AUTONUMFORMAT SuffixChar="." Superscript="false" Type="Digit"/></AUTONUM><CHAR> [정답] %s</CHAR></TEXT></P>' % (pr["no"], ans),
          '<P ParaShape="1" Style="0"><TEXT CharShape="0"/></P>',
          '<P ParaShape="1" Style="0"><TEXT CharShape="0"><CHAR>[해설]</CHAR></TEXT></P>']
    for l in pr["sol"]:
        ps.append('<P ParaShape="1" Style="0"><TEXT CharShape="0">%s<CHAR></CHAR></TEXT></P>' % runs(l))
    return ('<ENDNOTE><PARALIST LineWrap="Break" LinkListID="0" LinkListIDNext="0" TextDirection="0" VertAlign="Top">%s</PARALIST></ENDNOTE>'
            % "".join(ps))

def problem(pr, colbreak):
    pts = points(pr)
    tag = " [%d점]" % pts
    body = list(pr["body"])
    body2 = list(pr.get("body2", []))
    # 배점은 발문(마지막 텍스트 문단) 끝에
    if body2:
        body2[-1] += tag
    else:
        body[-1] += tag
    cb = ' ColumnBreak="true" PageBreak="false"' if colbreak else ""
    first = body[0]
    out = ['<P ParaShape="8" Style="0"%s><TEXT CharShape="1">%s</TEXT><TEXT CharShape="0">%s<CHAR></CHAR></TEXT></P>'
           % (cb, endnote(pr), runs(first))]
    for l in body[1:]:
        out.append(para(l, tab=is_display(l)))
    # 순서: 그림이 있으면 본문-그림-발문-조건, 없으면 본문-조건-발문
    if pr.get("fig"):
        out.append(pic_xml(pr["fig"], FIGW[pr["fig"]]))
        out += [para(l, tab=is_display(l)) for l in body2]
        if pr.get("box"):
            out.append(box_xml(pr["box"]))
    else:
        if pr.get("box"):
            out.append(box_xml(pr["box"]))
        out += [para(l, tab=is_display(l)) for l in body2]
    if pr["choices"]:
        out.append(choice_lines(pr["choices"]))
    return "".join(out)

def build(M, subject, short, layout, outname):
    global BIN
    BIN = []
    bag = set()
    for p in M:
        for l in p["body"] + p.get("body2", []) + (p.get("box") or []) + p["sol"]:
            collect(l, bag)
        for c in p["choices"] or []:
            bag.add(c)
    bag.add("[3점]")
    eq_sizes(bag - set(EQ))

    s = SRC
    head, rest = s[:s.index("<BODY>")], s[s.index("<BODY>"):]
    head = re.sub(r"<DOCSUMMARY>.*?</DOCSUMMARY>",
                  "<DOCSUMMARY><TITLE>예비고1 반편성고사 %s</TITLE><SUBJECT>%s</SUBJECT><AUTHOR></AUTHOR><DATE>2026년</DATE>"
                  "<KEYWORDS>반편성고사</KEYWORDS><COMMENTS></COMMENTS></DOCSUMMARY>" % (subject, subject), head, flags=re.S)
    # 첫 문단: 제목 표까지 유지, 출처 표 제거
    cut = rest.index('<TEXT CharShape="0"><TABLE BorderFill="1" CellSpacing="0" ColCount="3" PageBreak="Cell"')
    prefix = rest[:cut] + "</P>"
    prefix = prefix.replace("<CHAR>2026년 3월 고2</CHAR>", "<CHAR>예비고1 반편성고사</CHAR>", 1)
    prefix = prefix.replace("<CHAR>제2교시</CHAR>", "<CHAR>60분</CHAR>", 1)
    k = prefix.index("<CHAR>예비고1 반편성고사</CHAR>")
    j = prefix.index("<CHAR>수학영역</CHAR>", k)
    prefix = prefix[:j] + "<CHAR>%s</CHAR>" % subject + prefix[j + len("<CHAR>수학영역</CHAR>"):]

    # 문항 본문
    first_in_col = {grp[0] for grp in layout}
    parts = []
    for p in M:
        parts.append(problem(p, colbreak=(p["no"] in first_in_col and p["no"] != 1)))

    # 빠른 정답 + 해설 머리
    m1 = re.search(r'<P ParaShape="0" Style="0" ColumnBreak="false" PageBreak="true"><TEXT CharShape="0"><TABLE.*?</TABLE></TEXT></P>', rest, re.S)
    qa_tbl = m1.group(0)
    tail_start = rest.index('<P ParaShape="1" Style="0" ColumnBreak="false" PageBreak="true">')
    m2 = re.search(r'<P [^>]*><TEXT CharShape="0"><TABLE(?:(?!</TABLE>).)*?\(해설\).*?</TABLE></TEXT></P>', rest[tail_start + 10:], re.S)
    sol_tbl = m2.group(0)
    qa = qa_tbl.replace("2026년 3월 고2(빠른 정답)", "%s (빠른 정답)" % subject).replace("<CHAR>작업공간</CHAR>", "<CHAR>예비고1 반편성고사</CHAR>").replace("<CHAR>2026.07.10</CHAR>", "<CHAR>100점 만점</CHAR>")
    so = sol_tbl.replace("2026년 3월 고2(해설)", "%s (해설)" % subject).replace("<CHAR>작업공간</CHAR>", "<CHAR>예비고1 반편성고사</CHAR>").replace("<CHAR>2026.07.10</CHAR>", "<CHAR></CHAR>")
    lines = []
    for p in M:
        ans = CIRC[p["ans"] - 1] if p["choices"] else str(p["ans"])
        lines.append('<P ParaShape="3" Style="0"><TEXT CharShape="0"><AUTONUM Number="%d" NumberType="Endnote">'
                     '<AUTONUMFORMAT SuffixChar="." Superscript="false" Type="Digit"/></AUTONUM><CHAR> [정답] %s   (%d점, %s)</CHAR></TEXT></P>'
                     % (p["no"], ans, points(p), p["unit"]))
    tail = ('<P ParaShape="1" Style="0" ColumnBreak="false" PageBreak="true"><TEXT CharShape="0"/></P>' + qa + "".join(lines) + so)
    body_end = rest[rest.index("</SECTION>"):rest.index("<TAIL>")]

    # 그림 바이너리
    items = "".join('<BINITEM BinData="%d" Format="png" Type="Embedding"/>' % (i + 1) for i in range(len(BIN)))
    head = re.sub(r'<BINDATALIST Count="\d+">.*?</BINDATALIST>', '<BINDATALIST Count="%d">%s</BINDATALIST>' % (len(BIN), items), head, flags=re.S)
    if not BIN:
        head = re.sub(r'<BINDATALIST Count="0"></BINDATALIST>', '', head)
    tailpart = s[s.index("<TAIL>"):]
    store = ""
    for i, pth in enumerate(BIN):
        raw = open(pth, "rb").read()
        b64 = base64.b64encode(raw).decode()
        b64 = "\n".join(b64[k:k + 76] for k in range(0, len(b64), 76))
        store += '<BINDATA Encoding="Base64" Id="%d" Size="%d">%s</BINDATA>' % (i + 1, len(raw), b64)
    tailpart = re.sub(r"<BINDATASTORAGE>.*?</BINDATASTORAGE>", "<BINDATASTORAGE>%s</BINDATASTORAGE>" % store, tailpart, flags=re.S)

    doc = head + prefix + "".join(parts) + tail + body_end + tailpart
    path = os.path.join(OUTDIR, outname)
    open(path, "w", encoding="utf-8").write(doc)
    return path

L1 = [[1, 2], [3, 4], [5, 6], [7, 8], [9, 10], [11], [12], [13], [14], [15, 16], [17], [18, 19], [20]]
L2 = [[1, 2], [3, 4], [5, 6], [7, 8], [9], [10], [11], [12], [13], [14], [15, 16], [17, 18], [19], [20]]
p1 = build(M1, "공통수학1", "공수1", L1, "예비고1_반편성고사_공통수학1.hml")
p2 = build(M2, "공통수학2", "공수2", L2, "예비고1_반편성고사_공통수학2.hml")
json.dump({k: v for k, v in EQ.items()}, open(os.path.join(OUTDIR, "_eqsizes.json"), "w"), ensure_ascii=False)
print(p1, p2)
