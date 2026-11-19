# -*- coding: utf-8 -*-
"""CLIMATH(c) 공통수학1 단원분류표(수정할 수 있는 한글 HWPX) (2026-11-19).
python c1c_unittable.py <단원 PDF 폴더(u01.pdf~u14.pdf)> <출력.hwpx>
- 사용자: 'CLIMATH(c) 공통수학1 … 다 작업한 후 이 책의 단원분류표 만들기'.
- 대단원(교육과정 공통수학1: Ⅰ 다항식 / Ⅱ 방정식과 부등식 / Ⅲ 경우의 수 / Ⅳ 행렬) → 단원 → STEP 1 개념 확인하기(개념) · STEP 2 유형별 학습하기(유형).
- 개념·유형 이름과 문항 번호는 단원 HWPX(CLIMATH_c/공통수학1)에서 읽음: 'STEP N' 줄, 두 자리 번호 줄 + 다음 줄 이름, 그 사이 미주 수.
  이름 속 수식은 아래 NAME_EQ로 글자로 바꿈. 문항 번호는 미주 번호(단원마다 1부터).
- 쪽은 책(인디자인 CLIMATH(c)_공통수학1_차례_쪽번호.idml) 쪽: 단원 표지 쪽 + 단원 PDF 쪽(제목 줄이 처음 나오는 쪽).
- 틀(글꼴·문단 모양)은 조립제법_표.hwpx(unittable.py와 같음).
"""
import sys, os, re, zipfile, html
import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TPL = os.path.join(ROOT, "조립제법_표.hwpx")
HDIR = os.path.join(ROOT, "CLIMATH_c", "공통수학1")
PDIR, OUT = sys.argv[1:3]

UNITS = ["다항식의 연산", "항등식", "나머지정리", "인수분해", "복소수", "이차함수와 이차방정식의 관계", "이차함수의 최대·최소",
         "고차방정식", "연립방정식", "연립부등식과 이차부등식", "연립이차부등식", "순열", "조합", "행렬"]
BIG = {1: "Ⅰ. 다항식", 5: "Ⅱ. 방정식과 부등식", 12: "Ⅲ. 경우의 수", 14: "Ⅳ. 행렬"}
OPENER = [2, 30, 54, 78, 104, 132, 162, 188, 212, 234, 256, 280, 306, 328]     # 책 단원 표지 쪽(climath2_build.py c1c, 351쪽 — 2026-11-19 8·12단원 PDF 교체 뒤)
STEPNAME = {"STEP 1": "STEP 1 개념 확인하기", "STEP 2": "STEP 2 유형별 학습하기"}
NAME_EQ = [  # 이름 속 수식(HWP 수식 → 글자)
    ("〔bold{f LEFT ( x RIGHT ) =0}〕과 〔{bold{f LEFT ( ax+b RIGHT ) =0}}〕", "f(x)=0과 f(ax+b)=0"),
    ("〔bold ax>b`〕", "ax>b"),
    ("〔bold { rm {{} _{n} P  _{r} }}〕", "ₙPᵣ"),
    ("〔bold { {it} _{n} {rm C}  _{itr} }〕", "ₙCᵣ"),
    ("〔bold { {} _{n} {rm C}  _{r} }〕", "ₙCᵣ"),
    ("〔bold { AB=BA }〕", "AB=BA"), ("〔bold{ AB= BA}〕", "AB=BA"),
    ("〔E〕", "E"), ("〔bold{ E}〕", "E"),
    ("𝒙𝒏-𝒚𝒏", "xⁿ−yⁿ"), ("x1, x2", "x₁, x₂"),
]


def sections(path):
    """[(STEP, 번호, 이름, 첫 문항 번호)], 문항 수"""
    s = zipfile.ZipFile(path).read("Contents/section0.xml").decode("utf-8")
    s = re.sub(r"<hp:endNote .*?</hp:endNote>", "\x01", s, flags=re.S)
    s = re.sub(r"<hp:script>(.*?)</hp:script>", r"〔\1〕", s, flags=re.S)
    s = re.sub(r"<hp:shapeComment>.*?</hp:shapeComment>", "", s, flags=re.S)
    lines = [html.unescape(x) for x in re.sub(r"<[^>]+>", "", re.sub(r"</hp:p>", "\n", s)).split("\n")]
    n, step, out = 0, None, []
    for i, line in enumerate(lines):
        c = line.count("\x01")
        L = line.replace("\x01", "").strip()
        if not c and re.match(r"^STEP\s*\d$", L):
            step = L
        if not c and re.match(r"^\d\d$", L):
            nm = next(x.strip() for x in lines[i + 1:] if x.strip())
            nm = re.sub(r"\s+", " ", re.sub(r"수식입니다\.", " ", nm))
            for a, b in NAME_EQ:
                nm = nm.replace(re.sub(r"\s+", " ", a), b)
            nm = re.sub(r"\s+", " ", nm).strip()
            if len(nm) < 50 and not re.search(r"구하시오|\x01", nm):   # 문제 글(8단원 '20 가로의 길이…' 같은 것)은 제목이 아님
                assert "〔" not in nm, nm
                out.append([step, L, nm, n + 1])
        n += c
    return out, n


def pages(pdf, secs):
    """제목 줄('NN 이름')이 처음 나오는 단원 PDF 쪽(1부터) — 차례대로 찾음"""
    d = pymupdf.open(pdf)
    lines = [(i + 1, l.strip()) for i, p in enumerate(d) for l in p.get_text().split("\n")]
    res, k = [], 0
    for st, no, nm, first in secs:
        # 'NN 이름' 한 줄, 또는 'NN'만 있는 줄(이름이 다음 줄이거나 수식으로 시작: 6단원 11, 12단원 ₙPᵣ 등)
        while not ((re.match(r"^%s\s+\S" % no, lines[k][1]) and not lines[k][1].endswith("."))
                   or lines[k][1] == no):
            k += 1
        res.append(lines[k][0])
        k += 1
    return res, d.page_count


data = []
for u, name in enumerate(UNITS, 1):
    path = os.path.join(HDIR, "%d. %s.hwpx" % (u, name))
    secs, total = sections(path)
    pg, npg = pages(os.path.join(PDIR, "u%02d.pdf" % u), secs)
    assert pg == sorted(pg), (u, pg)
    rows = []
    for k, (st, no, nm, first) in enumerate(secs):
        last = (secs[k + 1][3] - 1) if k + 1 < len(secs) else total
        rows.append((st, no, nm, OPENER[u - 1] + pg[k], first, last))
    data.append((u, name, OPENER[u - 1], OPENER[u - 1] + npg, total, rows))


# ---------------------------------------------------------------- 한글 파일
def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


z = zipfile.ZipFile(TPL)
files = {n: z.read(n) for n in z.namelist()}
head = files["Contents/header.xml"].decode("utf-8")


def add_item(head, tag, plural, src_id, fn):
    m = re.search(r'<hh:%s id="%s".*?</hh:%s>' % (tag, src_id, tag), head, re.S)
    cnt = int(re.search(r'<hh:%s itemCnt="(\d+)"' % plural, head).group(1))
    nid_ = max(int(x) for x in re.findall(r'<hh:%s id="(\d+)"' % tag, head)) + 1
    new = fn(re.sub(r'id="%s"' % src_id, 'id="%d"' % nid_, m.group(0), count=1))
    end = head.index("</hh:%s>" % plural)
    head = head[:end] + new + head[end:]
    head = re.sub(r'<hh:%s itemCnt="\d+"' % plural, '<hh:%s itemCnt="%d"' % (plural, cnt + 1), head, count=1)
    return head, nid_


def fill(color):
    return lambda x: x.replace("</hh:borderFill>", '<hc:fillBrush><hc:winBrush faceColor="%s" hatchColor="#999999" alpha="0"/></hc:fillBrush></hh:borderFill>' % color)


head, BF_HEAD = add_item(head, "borderFill", "borderFills", "3", fill("#E5E5E5"))
head, BF_S1 = add_item(head, "borderFill", "borderFills", "3", fill("#EFE8F4"))      # STEP 1 칸: 연보라(책 보라 표지 색 계열)
head, BF_S2 = add_item(head, "borderFill", "borderFills", "3", fill("#E6F0F8"))      # STEP 2 칸: 연파랑
head, PP_C = add_item(head, "paraPr", "paraProperties", "0",
                      lambda x: x.replace('horizontal="JUSTIFY"', 'horizontal="CENTER"').replace('value="160"', 'value="130"'))
head, PP_L = add_item(head, "paraPr", "paraProperties", "0",
                      lambda x: x.replace('horizontal="JUSTIFY"', 'horizontal="LEFT"').replace('value="160"', 'value="130"'))
head, CP_B = add_item(head, "charPr", "charProperties", "0", lambda x: x.replace('<hh:underline', '<hh:bold/><hh:underline'))
head, CP_S = add_item(head, "charPr", "charProperties", "0", lambda x: x.replace('height="1000"', 'height="900"', 1))
head, CP_U = add_item(head, "charPr", "charProperties", "0",
                      lambda x: x.replace('height="1000"', 'height="1200"', 1).replace('<hh:underline', '<hh:bold/><hh:underline'))
head, CP_T = add_item(head, "charPr", "charProperties", "0",
                      lambda x: x.replace('height="1000"', 'height="1600"', 1).replace('<hh:underline', '<hh:bold/><hh:underline'))
files["Contents/header.xml"] = head.encode("utf-8")

sec = files["Contents/section0.xml"].decode("utf-8")
first = sec[:sec.index("<hp:run charPrIDRef=\"0\"><hp:tbl")] + "</hp:p>"
NID = [3300000000]


def nid():
    NID[0] += 1
    return str(NID[0])


def para(text, pp=0, cp=0):
    return ('<hp:p id="%s" paraPrIDRef="%d" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0"><hp:run charPrIDRef="%d">%s</hp:run></hp:p>'
            % (nid(), pp, cp, "<hp:t>%s</hp:t>" % esc(text) if text else "<hp:t/>"))


H = 1450


def table(rows, widths, spans=None, head_rows=1, bf=None, left_cols=(), bold_last=False):
    """rows: [[칸 글자 또는 None(합쳐진 자리)]], spans: {(r, c): (rowSpan, colSpan)}, bf: {(r, c): borderFill}"""
    spans, bf = spans or {}, bf or {}
    trs = []
    for r, row in enumerate(rows):
        tcs = []
        for c, t in enumerate(row):
            if t is None:
                continue
            rs, cs = spans.get((r, c), (1, 1))
            hd = r < head_rows
            b = BF_HEAD if hd else bf.get((r, c), 3)
            cp = CP_B if hd or (bold_last and r == len(rows) - 1) else CP_S
            pp = PP_L if (c in left_cols and not hd) else PP_C
            tcs.append('<hp:tc name="" header="%d" hasMargin="0" protect="0" editable="0" dirty="0" borderFillIDRef="%d">'
                       '<hp:subList id="" textDirection="HORIZONTAL" lineWrap="BREAK" vertAlign="CENTER" linkListIDRef="0" linkListNextIDRef="0" textWidth="0" textHeight="0" hasTextRef="0" hasNumRef="0">'
                       '%s</hp:subList><hp:cellAddr colAddr="%d" rowAddr="%d"/><hp:cellSpan colSpan="%d" rowSpan="%d"/>'
                       '<hp:cellSz width="%d" height="%d"/><hp:cellMargin left="400" right="400" top="100" bottom="100"/></hp:tc>'
                       % (1 if hd else 0, b, para(t, pp, cp), c, r, cs, rs, sum(widths[c:c + cs]), H * rs))
        trs.append("<hp:tr>%s</hp:tr>" % "".join(tcs))
    tbl = ('<hp:tbl id="%s" zOrder="0" numberingType="TABLE" textWrap="TOP_AND_BOTTOM" textFlow="BOTH_SIDES" lock="0" dropcapstyle="None" pageBreak="CELL" repeatHeader="1" rowCnt="%d" colCnt="%d" cellSpacing="0" borderFillIDRef="3" noAdjust="0">'
           '<hp:sz width="%d" widthRelTo="ABSOLUTE" height="%d" heightRelTo="ABSOLUTE" protect="0"/>'
           '<hp:pos treatAsChar="1" affectLSpacing="0" flowWithText="1" allowOverlap="0" holdAnchorAndSO="0" vertRelTo="PARA" horzRelTo="PARA" vertAlign="TOP" horzAlign="LEFT" vertOffset="0" horzOffset="0"/>'
           '<hp:outMargin left="0" right="0" top="0" bottom="0"/><hp:inMargin left="400" right="400" top="100" bottom="100"/>%s</hp:tbl>'
           % (nid(), len(rows), len(widths), sum(widths), H * len(rows), "".join(trs)))
    return ('<hp:p id="%s" paraPrIDRef="%d" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0"><hp:run charPrIDRef="0">%s<hp:t/></hp:run></hp:p>'
            % (nid(), PP_C, tbl))


rng = lambda a, b: "%d~%d" % (a, b) if b > a else "%d" % a
big_of = lambda u: BIG[max(k for k in BIG if k <= u)]

# 1) 단원별 한눈에 보기
W1 = [7400, 12990, 4600, 3600, 5000, 3600, 5000, 6000]           # 합 48190 = 쪽 너비 − 왼쪽·오른쪽 여백
r1 = [["대단원", "단원", "쪽", "개념 수", "STEP 1 문항", "유형 수", "STEP 2 문항", "문항 수"]]
sp1 = {}
for u, name, op, end, total, rows in data:
    s1 = [r for r in rows if r[0] == "STEP 1"]
    s2 = [r for r in rows if r[0] == "STEP 2"]
    if u in BIG:
        sp1[(len(r1), 0)] = (sum(1 for d in data if big_of(d[0]) == BIG[u]), 1)
    r1.append([BIG[u] if u in BIG else None, "%d. %s" % (u, name), rng(op, end), str(len(s1)), rng(s1[0][4], s1[-1][5]),
               str(len(s2)), rng(s2[0][4], s2[-1][5]), str(total)])
TOT = sum(d[4] for d in data)
r1.append(["합계", None, "", str(sum(len([r for r in d[5] if r[0] == "STEP 1"]) for d in data)), "",
           str(sum(len([r for r in d[5] if r[0] == "STEP 2"]) for d in data)), "", str(TOT)])
sp1[(len(r1) - 1, 0)] = (1, 2)

TITLE = "CLIMATH ⓒ 공통수학1 단원분류표"
body = [first, para(TITLE, PP_C, CP_T), para(""), para("단원별 한눈에 보기", 0, CP_U), table(r1, W1, sp1, bold_last=True), para(""),
        para("· 쪽은 책 쪽 번호(단원 표지 쪽 ~ 단원 마지막 쪽). 문항 번호는 단원마다 1번부터 시작한다.", 0, CP_S),
        para("· 단원마다 STEP 1 개념 확인하기(개념 + 대표문항·유제)와 STEP 2 유형별 학습하기(유형별 문항)로 나뉜다.", 0, CP_S)]

# 2) 단원마다 개념·유형 분류
W2 = [7600, 3000, 22790, 4000, 6000, 4800]
for u, name, op, end, total, rows in data:
    if u in BIG:
        body.append('<hp:p id="%s" paraPrIDRef="0" styleIDRef="0" pageBreak="1" columnBreak="0" merged="0"><hp:run charPrIDRef="%d"><hp:t>%s</hp:t></hp:run></hp:p>'
                    % (nid(), CP_T, esc(BIG[u])))
    else:
        body.append(para(""))
    body.append(para("%d. %s   (%s쪽, %d문항)" % (u, name, rng(op, end), total), 0, CP_U))
    rr = [["구분", "번호", "개념·유형", "쪽", "문항 번호", "문항 수"]]
    sp, bf = {}, {}
    for k, (st, no, nm, pg, a, b) in enumerate(rows):
        r = len(rr)
        lab = None
        if k == 0 or rows[k - 1][0] != st:
            sp[(r, 0)] = (sum(1 for x in rows if x[0] == st), 1)
            lab = STEPNAME.get(st, st)
        rr.append([lab, no, nm, str(pg), rng(a, b), str(b - a + 1)])
        for c in range(6):
            bf[(r, c)] = BF_S1 if st == "STEP 1" else BF_S2
    body.append(table(rr, W2, sp, bf=bf, left_cols=(2,)))

files["Contents/section0.xml"] = ("".join(body) + "</hs:sec>").encode("utf-8")
if "Preview/PrvText.txt" in files:
    files["Preview/PrvText.txt"] = TITLE.encode("utf-8")
with zipfile.ZipFile(OUT, "w") as w:
    for n in z.namelist():
        info = zipfile.ZipInfo(n, date_time=(1980, 1, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_STORED if n == "mimetype" else zipfile.ZIP_DEFLATED
        w.writestr(info, files[n])
for u, name, op, end, total, rows in data:
    print(u, name, rng(op, end), total, "개념", sum(r[0] == "STEP 1" for r in rows), "유형", sum(r[0] == "STEP 2" for r in rows))
    for r in rows:
        print("    ", r)
print("합계", TOT, "->", OUT)

# ---------------------------------------------------------------- 보기용 PDF(선택: 세 번째 인자) — 한글 파일과 같은 내용, Pretendard
if len(sys.argv) > 3:
    from playwright.sync_api import sync_playwright
    PDF_OUT = sys.argv[3]
    FONT = os.environ.get("PRETENDARD", "")
    h = lambda t: html.escape(str(t))
    css = ("@page{size:A4;margin:14mm 13mm 14mm 13mm}"
           + ("@font-face{font-family:P;src:url('file://%s/Pretendard-Regular.otf')}@font-face{font-family:P;font-weight:700;src:url('file://%s/Pretendard-Bold.otf')}" % (FONT, FONT) if FONT else "")
           + "body{font-family:P,sans-serif;font-size:9pt;color:#111}h1{font-size:17pt;text-align:center;margin:0 0 10px}"
           "h2{font-size:13pt;margin:16px 0 6px;color:#5b3f73;border-bottom:2px solid #9166a5;padding-bottom:3px}h3{font-size:10.5pt;margin:12px 0 4px}"
           "table{border-collapse:collapse;width:100%}th,td{border:0.6px solid #888;padding:3px 5px;text-align:center}th{background:#e5e5e5;white-space:nowrap}"
           "td.l{text-align:left}tr.s1 td{background:#efe8f4}tr.s2 td{background:#e6f0f8}tr.tot td{font-weight:700}.pb{break-before:page}"
           "p.n{margin:3px 0;font-size:8.5pt;color:#333}div.u{break-inside:avoid;page-break-inside:avoid}")
    o = ["<html><head><meta charset='utf-8'><style>%s</style></head><body><h1>%s</h1><h3>단원별 한눈에 보기</h3><table>" % (css, h(TITLE))]
    o.append("<tr>%s</tr>" % "".join("<th>%s</th>" % h(c) for c in r1[0]))
    for r, row in enumerate(r1[1:], 1):
        tds = []
        for c, t in enumerate(row):
            if t is None: continue
            rs, cs = sp1.get((r, c), (1, 1))
            tds.append("<td rowspan=%d colspan=%d%s>%s</td>" % (rs, cs, " class=l" if c == 1 else "", h(t)))
        o.append("<tr%s>%s</tr>" % (" class=tot" if r == len(r1) - 1 else "", "".join(tds)))
    o.append("</table><p class=n>· 쪽은 책 쪽 번호(단원 표지 쪽 ~ 단원 마지막 쪽). 문항 번호는 단원마다 1번부터 시작한다.</p>"
             "<p class=n>· 단원마다 STEP 1 개념 확인하기(개념 + 대표문항·유제)와 STEP 2 유형별 학습하기(유형별 문항)로 나뉜다.</p>")
    for u, name, op, end, total, rows in data:
        if u in BIG:
            o.append("<h2 class=pb>%s</h2>" % h(BIG[u]))
        o.append("<div class=u><h3>%d. %s &nbsp;<span style='font-weight:400;color:#555'>(%s쪽, %d문항)</span></h3><table>"
                 "<tr><th style='width:17%%'>구분</th><th style='width:6%%'>번호</th><th>개념·유형</th><th style='width:7%%'>쪽</th><th style='width:11%%'>문항 번호</th><th style='width:8%%'>문항 수</th></tr>" % (u, h(name), rng(op, end), total))
        for k, (st, no, nm, pg, a, b) in enumerate(rows):
            lab = ""
            if k == 0 or rows[k - 1][0] != st:
                lab = "<td rowspan=%d>%s</td>" % (sum(1 for x in rows if x[0] == st), h(STEPNAME.get(st, st)).replace(" 개념", "<br>개념").replace(" 유형", "<br>유형"))
            o.append("<tr class=%s>%s<td>%s</td><td class=l>%s</td><td>%d</td><td>%s</td><td>%d</td></tr>"
                     % ("s1" if st == "STEP 1" else "s2", lab, no, h(nm), pg, rng(a, b), b - a + 1))
        o.append("</table></div>")
    o.append("</body></html>")
    tmp = PDF_OUT + ".html"
    open(tmp, "w", encoding="utf-8").write("".join(o))
    with sync_playwright() as p:
        import glob as _g
        b = p.chromium.launch(executable_path=next(iter(sorted(_g.glob("/opt/pw-browsers/chromium-*/chrome-linux*/chrome"), reverse=True))))
        pg_ = b.new_page()
        pg_.goto("file://" + os.path.abspath(tmp))
        pg_.pdf(path=PDF_OUT, format="A4", prefer_css_page_size=True, print_background=True)
        b.close()
    os.remove(tmp)
    print("PDF ->", PDF_OUT)
