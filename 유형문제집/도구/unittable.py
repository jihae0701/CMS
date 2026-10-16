# -*- coding: utf-8 -*-
"""공통수학1 단원표·단원별 문항 수를 수정 가능한 한글 파일(HWPX)로 만든다.
python unittable.py <출력.hwpx>
- 문항 수와 번호는 기본서(기본서/*.hwpx)·유형서(공통수학1/*.hwpx)의 미주 번호를 직접 읽어 센다.
  유형서 시작 번호는 미주 번호 매기기(endNotePr newNum)에서 읽는다(8·9단원 사용자 수정본은 이 값으로 번호가 이어진다).
- 틀(글꼴·문단 모양)은 조립제법_표.hwpx를 쓰고, 가운데 정렬 문단·굵은 글자·회색 머리 칸 모양을 덧붙인다.
"""
import sys, os, re, zipfile, glob

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TPL = os.path.join(ROOT, "조립제법_표.hwpx")

UNITS = [  # (대단원, 단원 번호, 단원명, 기본서 파일, 유형서 파일)
    ("Ⅰ. 다항식", 1, "다항식의 연산과 항등식", "1. 다항식의 연산과 항등식", "01_다항식의_연산과_항등식"),
    ("Ⅰ. 다항식", 2, "나머지정리", "2. 나머지정리", "02_나머지정리"),
    ("Ⅰ. 다항식", 3, "인수분해", "3. 인수분해", "03_인수분해"),
    ("Ⅱ. 방정식과 부등식", 4, "복소수와 이차방정식", "4. 복소수와 이차방정식", "04_복소수와_이차방정식"),
    ("Ⅱ. 방정식과 부등식", 5, "이차함수와 이차방정식의 관계", "5. 이차함수와 이차방정식의 관계", "05_이차함수와_이차방정식의_관계"),
    ("Ⅱ. 방정식과 부등식", 6, "이차함수의 최대, 최소", "6. 이차함수의 최대, 최소", "06_이차함수의_최대_최소"),
    ("Ⅱ. 방정식과 부등식", 7, "여러 가지 방정식", "7. 여러 가지 방정식", "07_여러_가지_방정식"),
    ("Ⅱ. 방정식과 부등식", 8, "이차부등식", "8. 이차부등식", "08_이차부등식"),
    ("Ⅱ. 방정식과 부등식", 9, "연립부등식", "9. 연립부등식", "09_연립부등식"),
    ("Ⅲ. 경우의 수", 10, "경우의 수와 순열", "10. 경우의 수와 순열", "10_경우의_수와_순열"),
    ("Ⅲ. 경우의 수", 11, "조합", "11. 조합", "11_조합"),
    ("Ⅳ. 행렬", 12, "행렬", "12. 행렬", "12_행렬"),
]


def count(path):
    x = zipfile.ZipFile(path).read("Contents/section0.xml").decode("utf-8")
    n = len(re.findall(r'<hp:autoNum num="\d+" numType="ENDNOTE"', x))
    start = int(re.search(r"<hp:endNotePr>.*?<hp:numbering [^>]*newNum=\"(\d+)\"", x, re.S).group(1))
    return n, start


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ---------------------------------------------------------------- 머리(header.xml): 모양 덧붙이기
z = zipfile.ZipFile(TPL)
files = {n: z.read(n) for n in z.namelist()}
head = files["Contents/header.xml"].decode("utf-8")


def add_item(head, tag, plural, src_id, new_xml_fn):
    m = re.search(r'<hh:%s id="%s".*?</hh:%s>' % (tag, src_id, tag), head, re.S)
    cnt = int(re.search(r'<hh:%s itemCnt="(\d+)"' % plural, head).group(1))
    new = new_xml_fn(re.sub(r'id="%s"' % src_id, 'id="%d"' % cnt, m.group(0), count=1))
    end = head.index("</hh:%s>" % plural)
    head = head[:end] + new + head[end:]
    head = re.sub(r'<hh:%s itemCnt="\d+"' % plural, '<hh:%s itemCnt="%d"' % (plural, cnt + 1), head, count=1)
    return head, cnt


GRAY = '<hc:fillBrush><hc:winBrush faceColor="#E5E5E5" hatchColor="#999999" alpha="0"/></hc:fillBrush>'
head, BF_HEAD = add_item(head, "borderFill", "borderFills", "3", lambda x: x.replace("</hh:borderFill>", GRAY + "</hh:borderFill>"))
head, PP_C = add_item(head, "paraPr", "paraProperties", "0",
                      lambda x: x.replace('horizontal="JUSTIFY"', 'horizontal="CENTER"').replace('value="160"', 'value="130"'))
head, CP_B = add_item(head, "charPr", "charProperties", "0", lambda x: x.replace('<hh:underline', '<hh:bold/><hh:underline'))
head, CP_T = add_item(head, "charPr", "charProperties", "0",
                      lambda x: x.replace('height="1000"', 'height="1600"', 1).replace('<hh:underline', '<hh:bold/><hh:underline'))
files["Contents/header.xml"] = head.encode("utf-8")

# ---------------------------------------------------------------- 본문
sec = files["Contents/section0.xml"].decode("utf-8")
first = sec[:sec.index("<hp:run charPrIDRef=\"0\"><hp:tbl")]          # 구역 정의(secPr)가 든 첫 문단의 앞부분
first = first + "</hp:p>"
NID = [3000000000]


def nid():
    NID[0] += 1
    return str(NID[0])


def para(text, pp=0, cp=0):
    return ('<hp:p id="%s" paraPrIDRef="%d" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0"><hp:run charPrIDRef="%d">%s</hp:run></hp:p>'
            % (nid(), pp, cp, "<hp:t>%s</hp:t>" % esc(text) if text else "<hp:t/>"))


def cell(r, c, text, w, h=1700, rs=1, cs=1, headrow=False, bold=False):
    return ('<hp:tc name="" header="%d" hasMargin="0" protect="0" editable="0" dirty="0" borderFillIDRef="%d">'
            '<hp:subList id="" textDirection="HORIZONTAL" lineWrap="BREAK" vertAlign="CENTER" linkListIDRef="0" linkListNextIDRef="0" textWidth="0" textHeight="0" hasTextRef="0" hasNumRef="0">'
            '%s</hp:subList><hp:cellAddr colAddr="%d" rowAddr="%d"/><hp:cellSpan colSpan="%d" rowSpan="%d"/>'
            '<hp:cellSz width="%d" height="%d"/><hp:cellMargin left="510" right="510" top="141" bottom="141"/></hp:tc>'
            % (1 if headrow else 0, BF_HEAD if headrow else 3, para(text, PP_C, CP_B if (headrow or bold) else 0), c, r, cs, rs, w, h))


def table(rows, widths, spans):
    """rows: [[칸 글자 또는 None(합쳐진 자리)]], spans: {(r, c): (rowSpan, colSpan)}"""
    H = 1700
    trs = []
    for r, row in enumerate(rows):
        tcs = []
        for c, t in enumerate(row):
            if t is None:
                continue
            rs, cs = spans.get((r, c), (1, 1))
            w = sum(widths[c:c + cs])
            tcs.append(cell(r, c, t, w, H * rs, rs, cs, headrow=(r == 0), bold=(r == len(rows) - 1)))
        trs.append("<hp:tr>%s</hp:tr>" % "".join(tcs))
    W = sum(widths)
    tbl = ('<hp:tbl id="%s" zOrder="0" numberingType="TABLE" textWrap="TOP_AND_BOTTOM" textFlow="BOTH_SIDES" lock="0" dropcapstyle="None" pageBreak="CELL" repeatHeader="1" rowCnt="%d" colCnt="%d" cellSpacing="0" borderFillIDRef="3" noAdjust="0">'
           '<hp:sz width="%d" widthRelTo="ABSOLUTE" height="%d" heightRelTo="ABSOLUTE" protect="0"/>'
           '<hp:pos treatAsChar="1" affectLSpacing="0" flowWithText="1" allowOverlap="0" holdAnchorAndSO="0" vertRelTo="PARA" horzRelTo="PARA" vertAlign="TOP" horzAlign="LEFT" vertOffset="0" horzOffset="0"/>'
           '<hp:outMargin left="0" right="0" top="0" bottom="0"/><hp:inMargin left="510" right="510" top="141" bottom="141"/>%s</hp:tbl>'
           % (nid(), len(rows), len(widths), W, H * len(rows), "".join(trs)))
    return ('<hp:p id="%s" paraPrIDRef="%d" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0"><hp:run charPrIDRef="0">%s<hp:t/></hp:run></hp:p>'
            % (nid(), PP_C, tbl))


# ---------------------------------------------------------------- 자료
data = []
for big, no, name, bfile, yfile in UNITS:
    bn, bs = count(os.path.join(ROOT, "기본서", bfile + ".hwpx"))
    yn, ys = count(os.path.join(ROOT, "공통수학1", yfile + ".hwpx"))
    data.append((big, no, name, bn, bs, yn, ys))
for a, b in zip(data, data[1:]):          # 번호가 끊김 없이 이어지는지 확인
    assert a[4] + a[3] == b[4] and a[6] + a[5] == b[6], (a, b)

rows = [["대단원", "단원", "기본서 문항 수", "기본서 번호", "유형서 문항 수", "유형서 번호"]]
spans = {}
for k, (big, no, name, bn, bs, yn, ys) in enumerate(data):
    first_of_big = k == 0 or data[k - 1][0] != big
    if first_of_big:
        span = sum(1 for d in data if d[0] == big)
        spans[(len(rows), 0)] = (span, 1)
    rows.append([big if first_of_big else None, "%d. %s" % (no, name), str(bn), "%03d~%03d" % (bs, bs + bn - 1),
                 str(yn), "%03d~%03d" % (ys, ys + yn - 1)])
TB = sum(d[3] for d in data)
TY = sum(d[5] for d in data)
rows.append(["합계", None, str(TB), "%03d~%03d" % (1, TB), str(TY), "%03d~%03d" % (1, TY)])
spans[(len(rows) - 1, 0)] = (1, 2)
widths = [8300, 13890, 6500, 6500, 6500, 6500]           # 합 48190 = 쪽 너비 59528 − 왼쪽·오른쪽 여백

body = (first + para("공통수학1 단원표와 단원별 문항 수", PP_C, CP_T) + para("")
        + table(rows, widths, spans) + para("")
        + para("· 기본서와 유형서의 문항 번호는 각각 1단원부터 끊김 없이 이어진다(기본서 %d문항, 유형서 %d문항)." % (TB, TY)))
sec_new = body + "</hs:sec>"          # body의 첫 부분(first)에 이미 xml 머리와 <hs:sec>가 들어 있다
files["Contents/section0.xml"] = sec_new.encode("utf-8")
if "Preview/PrvText.txt" in files:
    files["Preview/PrvText.txt"] = "공통수학1 단원표와 단원별 문항 수".encode("utf-8")

out = sys.argv[1]
with zipfile.ZipFile(out, "w") as w:
    for n in z.namelist():                                   # mimetype은 맨 앞, 압축하지 않음
        info = zipfile.ZipInfo(n, date_time=(1980, 1, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_STORED if n == "mimetype" else zipfile.ZIP_DEFLATED
        w.writestr(info, files[n])
for d in data:
    print(d)
print("기본서", TB, "유형서", TY, "->", out)
