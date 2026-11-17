# -*- coding: utf-8 -*-
"""공통수학2 유형서 합본 목차 (2026-11-17 사용자 '위에파일 기준으로 목차만들어줘' — 사용자가 올린 합본 PDF 12개 기준 쪽 번호).
python toc.py <출력.hwpx> [--full]   (기본은 단원명과 쪽만, --full이면 유형까지)
- 쪽 번호는 toc_c2y.json(합본 PDF에서 유형 제목이 처음 나오는 쪽을 찾은 값; 8단원 '절대부등식'은 쪽 머리말과 겹쳐 손으로 147쪽).
- 틀은 공통수학2 유형서 1단원 파일(쪽 크기·2단·바탕쪽·글꼴), 바탕쪽 단원 이름 자리에 '목차'.
- 대단원 줄, 단원 줄(굵게, 연한 색 칸), 유형 줄(들여 씀)을 선 없는 표(이름 | 쪽)로.
"""
import sys, os, re, zipfile, json
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TPL = os.path.join(ROOT, "공통수학2", "유형서", "01_평면좌표.hwpx")
DATA = json.load(open(os.path.join(HERE, "toc_c2y.json"), encoding="utf-8"))
BIG = {1: "Ⅰ. 도형의 방정식", 5: "Ⅱ. 집합과 명제", 9: "Ⅲ. 함수와 그래프"}
out = [a for a in sys.argv[1:] if not a.startswith('--')][0]

z = zipfile.ZipFile(TPL)
files = {n: z.read(n) for n in z.namelist()}
head = files["Contents/header.xml"].decode("utf-8")


def add_item(head, tag, plural, src_id, fn):
    m = re.search(r'<hh:%s id="%s".*?</hh:%s>' % (tag, src_id, tag), head, re.S)
    cnt = int(re.search(r'<hh:%s itemCnt="(\d+)"' % plural, head).group(1))
    new = fn(re.sub(r'id="%s"' % src_id, 'id="%d"' % cnt, m.group(0), count=1))
    end = head.index("</hh:%s>" % plural)
    head = head[:end] + new + head[end:]
    head = re.sub(r'<hh:%s itemCnt="\d+"' % plural, '<hh:%s itemCnt="%d"' % (plural, cnt + 1), head, count=1)
    return head, cnt


def fill(x, color=None, bottom=False):
    x = re.sub(r"<hc:fillBrush>.*?</hc:fillBrush>", "", x, flags=re.S)
    if bottom:
        x = re.sub(r'<hh:bottomBorder type="[A-Z_]+" width="[^"]+" color="[^"]+"/>', '<hh:bottomBorder type="SOLID" width="0.12 mm" color="#7F8C99"/>', x)
    if color:
        x = x.replace("</hh:borderFill>", '<hc:fillBrush><hc:winBrush faceColor="%s" hatchColor="#999999" alpha="0"/></hc:fillBrush></hh:borderFill>' % color)
    return x


head, BF_NONE = add_item(head, "borderFill", "borderFills", "1", lambda x: fill(x))
head, BF_UNIT = add_item(head, "borderFill", "borderFills", "1", lambda x: fill(x, "#E8EEF6", True))
head, BF_LINE = add_item(head, "borderFill", "borderFills", "1", lambda x: fill(x, None, True))
head, PP_C = add_item(head, "paraPr", "paraProperties", "0", lambda x: x.replace('horizontal="JUSTIFY"', 'horizontal="CENTER"').replace('value="160"', 'value="130"'))
head, PP_L = add_item(head, "paraPr", "paraProperties", "0", lambda x: x.replace('horizontal="JUSTIFY"', 'horizontal="LEFT"').replace('value="160"', 'value="130"'))
head, PP_R = add_item(head, "paraPr", "paraProperties", "0", lambda x: x.replace('horizontal="JUSTIFY"', 'horizontal="RIGHT"').replace('value="160"', 'value="130"'))
head, PP_I = add_item(head, "paraPr", "paraProperties", "0",
                      lambda x: x.replace('horizontal="JUSTIFY"', 'horizontal="LEFT"').replace('value="160"', 'value="130"')
                      .replace('<hc:left value="0" unit="HWPUNIT"/>', '<hc:left value="1400" unit="HWPUNIT"/>'))
B = lambda x: x.replace("<hh:underline", "<hh:bold/><hh:underline")
head, CP_T = add_item(head, "charPr", "charProperties", "0", lambda x: B(x.replace('height="1000"', 'height="2400"', 1)))
head, CP_BIG = add_item(head, "charPr", "charProperties", "0", lambda x: B(x.replace('height="1000"', 'height="1250"', 1)))
head, CP_U = add_item(head, "charPr", "charProperties", "0", lambda x: B(x.replace('height="1000"', 'height="1100"', 1)))
head, CP_N = add_item(head, "charPr", "charProperties", "0", lambda x: x.replace('height="1000"', 'height="980"', 1))
files["Contents/header.xml"] = head.encode("utf-8")
for n in list(files):
    if re.match(r"Contents/masterpage\d+\.xml", n):
        files[n] = files[n].decode("utf-8").replace("<hp:t>평면좌표</hp:t>", "<hp:t>목차</hp:t>").encode("utf-8")

sec = files["Contents/section0.xml"].decode("utf-8")
i0 = sec.index("<hp:p ")
p0 = sec[i0:sec.index("</hp:p>", i0) + 7]
run0 = re.match(r"<hp:p [^>]*><hp:run [^>]*>", p0).group(0)
keep = re.search(r"<hp:secPr\b.*?</hp:secPr>", p0, re.S).group(0)
keep += "".join(m.group(0) for m in re.finditer(r"<hp:ctrl>(?:(?!</hp:ctrl>).)*?<hp:(?:colPr|footer|header|pageNum)\b.*?</hp:ctrl>", p0, re.S))
first = sec[:i0] + run0 + keep + "<hp:t/></hp:run></hp:p>"
NID = [3300000000]


def nid():
    NID[0] += 1
    return str(NID[0])


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def para(text, pp, cp):
    return ('<hp:p id="%s" paraPrIDRef="%d" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0"><hp:run charPrIDRef="%d">%s</hp:run></hp:p>'
            % (nid(), pp, cp, "<hp:t>%s</hp:t>" % esc(text) if text else "<hp:t/>"))


W1, W2, H = 25000, 4000, 1500


def cell(r, c, inner, w, bf):
    return ('<hp:tc name="" header="0" hasMargin="0" protect="0" editable="0" dirty="0" borderFillIDRef="%d">'
            '<hp:subList id="" textDirection="HORIZONTAL" lineWrap="BREAK" vertAlign="CENTER" linkListIDRef="0" linkListNextIDRef="0" textWidth="0" textHeight="0" hasTextRef="0" hasNumRef="0">'
            '%s</hp:subList><hp:cellAddr colAddr="%d" rowAddr="%d"/><hp:cellSpan colSpan="1" rowSpan="1"/>'
            '<hp:cellSz width="%d" height="%d"/><hp:cellMargin left="283" right="283" top="100" bottom="100"/></hp:tc>' % (bf, inner, c, r, w, H))


def table(rows):
    trs = []
    for r, (name, page, unit) in enumerate(rows):
        if unit == "plain":                     # 간략 목차: 단원 줄을 굵게, 칸 색 없이 아래 선만
            bf, pp, cp = BF_LINE, PP_L, CP_U
        else:
            bf, pp, cp = (BF_UNIT, PP_L, CP_U) if unit else (BF_NONE, PP_I, CP_N)
        trs.append("<hp:tr>%s%s</hp:tr>" % (cell(r, 0, para(name, pp, cp), W1, bf), cell(r, 1, para(str(page), PP_R, cp), W2, bf)))
    tbl = ('<hp:tbl id="%s" zOrder="0" numberingType="TABLE" textWrap="TOP_AND_BOTTOM" textFlow="BOTH_SIDES" lock="0" dropcapstyle="None" pageBreak="CELL" repeatHeader="0" rowCnt="%d" colCnt="2" cellSpacing="0" borderFillIDRef="%d" noAdjust="0">'
           '<hp:sz width="%d" widthRelTo="ABSOLUTE" height="%d" heightRelTo="ABSOLUTE" protect="0"/>'
           '<hp:pos treatAsChar="1" affectLSpacing="0" flowWithText="1" allowOverlap="0" holdAnchorAndSO="0" vertRelTo="PARA" horzRelTo="PARA" vertAlign="TOP" horzAlign="LEFT" vertOffset="0" horzOffset="0"/>'
           '<hp:outMargin left="0" right="0" top="0" bottom="0"/><hp:inMargin left="283" right="283" top="100" bottom="100"/>%s</hp:tbl>'
           % (nid(), len(rows), BF_NONE, W1 + W2, H * len(rows), "".join(trs)))
    return '<hp:p id="%s" paraPrIDRef="%d" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0"><hp:run charPrIDRef="%d">%s<hp:t/></hp:run></hp:p>' % (nid(), PP_C, CP_N, tbl)


body = [para("목차", PP_C, CP_T), para("공통수학2 유형서 (CMS Story)", PP_C, CP_N), para("", PP_L, CP_N)]
SIMPLE = "--full" not in sys.argv          # 기본: 단원명만(2026-11-17 사용자 '목차는 단원명만 간략히'), --full: 유형까지
rows_all = []
for no, title, p0_, items in DATA:
    if no in BIG:
        if SIMPLE and rows_all:
            body.append(table(rows_all)); body.append(para("", PP_L, CP_N)); rows_all = []
        body.append(para(BIG[no], PP_L, CP_BIG))
    if SIMPLE:
        rows_all.append(("%02d  %s" % (no, title), p0_, "plain"))
        continue
    rows = [("%02d  %s" % (no, title), p0_, True)] + [(n, p, False) for n, p in items]
    body.append(table(rows))
    body.append(para("", PP_L, CP_N))
if SIMPLE and rows_all:
    body.append(table(rows_all))
files["Contents/section0.xml"] = (first + "".join(body) + "</hs:sec>").encode("utf-8")
if "Preview/PrvText.txt" in files:
    files["Preview/PrvText.txt"] = "목차".encode("utf-8")
with zipfile.ZipFile(out, "w") as w:
    for n in z.namelist():
        info = zipfile.ZipInfo(n, date_time=(1980, 1, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_STORED if n == "mimetype" else zipfile.ZIP_DEFLATED
        w.writestr(info, files[n])
print("단원", len(DATA), "유형", sum(len(d[3]) for d in DATA), "->", out)
