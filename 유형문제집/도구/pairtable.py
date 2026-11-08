# -*- coding: utf-8 -*-
"""공통수학1 기본서·유형서 짝 문항 정리표를 한글 파일(HWPX)로 만든다(2026-11-08 사용자 요청).
python pairtable.py <출력.hwpx>
- 짝은 기본서 480문항과 유형서 691문항의 문제 글을 4글자 묶음으로 비교해 닮은 정도(자카드)로 찾았다. 표의 설명은 손으로 썼다.
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
            tcs.append(cell(r, c, t, w, H * rs, rs, cs, headrow=(r == 0), bold=False))
        trs.append("<hp:tr>%s</hp:tr>" % "".join(tcs))
    W = sum(widths)
    tbl = ('<hp:tbl id="%s" zOrder="0" numberingType="TABLE" textWrap="TOP_AND_BOTTOM" textFlow="BOTH_SIDES" lock="0" dropcapstyle="None" pageBreak="CELL" repeatHeader="1" rowCnt="%d" colCnt="%d" cellSpacing="0" borderFillIDRef="3" noAdjust="0">'
           '<hp:sz width="%d" widthRelTo="ABSOLUTE" height="%d" heightRelTo="ABSOLUTE" protect="0"/>'
           '<hp:pos treatAsChar="1" affectLSpacing="0" flowWithText="1" allowOverlap="0" holdAnchorAndSO="0" vertRelTo="PARA" horzRelTo="PARA" vertAlign="TOP" horzAlign="LEFT" vertOffset="0" horzOffset="0"/>'
           '<hp:outMargin left="0" right="0" top="0" bottom="0"/><hp:inMargin left="510" right="510" top="141" bottom="141"/>%s</hp:tbl>'
           % (nid(), len(rows), len(widths), W, H * len(rows), "".join(trs)))
    return ('<hp:p id="%s" paraPrIDRef="%d" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0"><hp:run charPrIDRef="0">%s<hp:t/></hp:run></hp:p>'
            % (nid(), PP_C, tbl))



# ---------------------------------------------------------------- 자료 (기본서 번호(정답), 유형서 번호(정답), 단원, 닮은 정도, 설명)
MAIN = [
    ("같은 문항", "7", "291 (2)", "390 (2)", "96%", "연립방정식 x+y=2a, (x+1)(y+1)=5+a²의 해가 모두 실수인 정수 a의 최솟값 — 문제와 답이 숫자까지 같다."),
    ("거의 같음", "7", "279 (b=−2, c=−a)", "371 (−2)", "57%", "사차방정식 x⁴+ax³+bx²+cx+1=0의 실근이 −1, 1뿐 — 조건이 같고 묻는 것만 다르다(a, b, c의 값 ↔ a+b+c)."),
    ("거의 같음", "8", "299 (4)", "432 (5)", "41%", "모든 실수 x에 대하여 √((k+2)x²−2(k+2)x+4)가 실수 — 같은 식에서 기본서만 역수(1/√ )라 등호 조건이 다르다."),
    ("같은 틀", "6", "241 (8)", "327 (7)", "44%", "f(x)=a(x−b)², k≤x≤k+2에서 최댓값과 최솟값의 차 g(k) — 주어진 조건과 묻는 값이 다르다."),
    ("숫자 변형", "1", "40 (364)", "44 (33)", "47%", "(3x²−x−1)⁵의 홀수 차 계수를 3의 거듭제곱으로 ↔ (2x²+x−2)⁵, 2의 거듭제곱으로."),
    ("숫자 변형", "2", "70 (8)", "71 (5)", "57%", "f(x)를 x²+2(나머지 3x−1), x+1(나머지 2)로 ↔ x²+1(나머지 x−2), x+1(나머지 3)로 나눌 때 R(1)."),
    ("숫자 변형", "2", "71 (48)", "79 (8)", "50%", "나머지 R(x)의 R(3): x²⁴−1을 (x−1)²으로 ↔ x⁴−3x³+5x−1을 (x−2)³으로."),
    ("숫자 변형", "2", "71 (48)", "119 (−3)", "43%", "나머지 R(x)의 R(3): x²⁴−1을 (x−1)²으로 ↔ x⁵−3x⁴+2x³+x²−x+1을 (x−1)³으로."),
    ("숫자 변형", "3", "112 (62)", "171 (38)", "48%", "a²(b+c)+b²(c+a)+c²(a+b)+3abc=230 → (a−b)²+(b−c)²+(c−a)² ↔ =310 → a²+b²+c²."),
    ("숫자 변형", "4", "132 (5)", "210 (−8)", "54%", "근의 공식을 잘못 알고 푼 두 근으로 원래 두 근의 제곱의 합 — 잘못 안 공식과 두 근이 다르다."),
    ("숫자 변형", "8", "311 (19)", "450 (5)", "47%", "두 이차함수 f, g의 조건 (가)~(다) — 조건의 수치와 묻는 값이 다르다."),
    ("숫자 변형", "10", "366 (720)", "538 (420)", "60%", "5개 영역을 5가지 색으로 이웃한 영역은 다르게 칠하기 — 영역 배치(그림)가 다르다."),
    ("숫자 변형", "10", "370 (30)", "562 (30)", "51%", "0~4로 만든 4의 배수: 서로 다른 4개로 네 자리 ↔ 다섯 개를 한 번씩 써서 다섯 자리(답은 둘 다 30)."),
    ("숫자 변형", "10", "382 (360)", "572 (18)", "49%", "같은 것이 있는 숫자 나열: 0, 1, 1, 1, 2, 2, 3으로 일곱 자리 ↔ 1, 1, 2, 2, 3으로 다섯 자리 홀수."),
    ("숫자 변형", "10", "385 (60)", "569 (150)", "61%", "0~4 중복 허락: 세 자리 짝수 ↔ 네 자리 3000 이상 짝수."),
]
REF = [
    ("1", "27 (8√2)", "18 (10)", "38%", "x⁴−6x²+4=0일 때 x³−8/x³ ↔ x⁴−7x²+9=0일 때 x³−27/x³."),
    ("3", "99 (−3)", "164 (−8)", "39%", "f(x+1)²−9=(x−1)(x+1)(x²+5) ↔ f(x+1)²−25=(x+1)(x−3)(x²−2x+7), f(x+a)의 나머지 조건."),
    ("4 / 3", "139 (0)", "135 (3)", "36%", "x, y에 대한 두 일차식의 곱으로 인수분해 — 식이 다르다."),
    ("4", "131 (5)", "207 (1)", "37%", "근과 계수의 관계로 식의 값 — 이차방정식과 구하는 식이 다르다."),
    ("4", "135 (−9/4)", "216 (7/4)", "36%", "f(x)=0의 두 근 → f(2x+1)=0 ↔ f(2x+5)=0의 두 근의 곱."),
    ("6", "214 (2)", "324 (−5)", "41%", "k≤x≤k+2(k+1)에서 이차함수의 최댓값·최솟값 조건으로 k의 합 — 함수와 범위가 다르다."),
    ("8", "301 (4/25)", "433 (51)", "39%", "이차부등식의 해와 f(x)≥(일차식) 조건으로 f값의 최댓값·최솟값 — 조건이 다르다."),
    ("9", "335 (8)", "499 (1)", "37%", "|x−k|≤6, x²−x−6>0 ↔ x²−x−12>0의 정수해의 합 조건."),
    ("9 / 4", "346 (a>8)", "213 (4)", "38%", "두 근의 부호가 다르고 음의 근의 절댓값이 더 큼 — 식이 다르고 범위 ↔ 정수 a."),
    ("10", "372 (144)", "583 (1008)", "41%", "1·2학년 학생 의자 배치: 4명·2명 ↔ 3명·4명, 조건 (나)가 다르다."),
    ("11 / 10", "428 (120)", "561 (39)", "40%", "숫자로 만든 수: 1~6 중 4개로 네 자리 3의 배수 ↔ 0~6 중 3개로 세 자리 6의 배수."),
]

rows = [["구분", "단원", "기본서 번호 (정답)", "유형서 번호 (정답)", "닮은 정도", "같은 점·다른 점"]]
for r in MAIN:
    rows.append(list(r))
widths = [5200, 3000, 7000, 7000, 4200, 21790]
rows2 = [["단원", "기본서 번호 (정답)", "유형서 번호 (정답)", "닮은 정도", "같은 점·다른 점"]]
for r in REF:
    rows2.append(list(r))
widths2 = [4200, 7000, 7000, 4200, 25790]

TITLE = "공통수학1 기본서·유형서 짝 문항 정리"
body = (first + para(TITLE, PP_C, CP_T) + para("")
        + para("· 기본서 480문항(001~480)과 유형서 691문항(001~691)의 문제 글을 모두 꺼내 짝마다 비교했다(4글자 묶음의 겹침 비율 = 닮은 정도).")
        + para("· 숫자까지 같은 문항은 1쌍(기본서 291 = 유형서 390)이다. 조건이 같고 묻는 것만 다른 문항이 1쌍(279 ↔ 371), 식이 거의 같은 문항이 1쌍(299 ↔ 432) 있다.")
        + para("· 나머지는 같은 틀에서 숫자나 조건을 바꾼 짝이다(어려운 기본서 문항은 숫자를 바꾼 변형으로 유형서에 넣는다는 기준).")
        + para("") + para("1. 닮은 정도 42% 이상", 0, CP_B) + table(rows, widths, {}) + para("")
        + para("2. 닮은 정도 36~41% (같은 유형의 숫자·조건 변형, 참고)", 0, CP_B) + table(rows2, widths2, {}) + para(""))
sec_new = body + "</hs:sec>"
files["Contents/section0.xml"] = sec_new.encode("utf-8")
if "Preview/PrvText.txt" in files:
    files["Preview/PrvText.txt"] = TITLE.encode("utf-8")

out = sys.argv[1]
with zipfile.ZipFile(out, "w") as w:
    for n in z.namelist():
        info = zipfile.ZipInfo(n, date_time=(1980, 1, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_STORED if n == "mimetype" else zipfile.ZIP_DEFLATED
        w.writestr(info, files[n])
print("->", out, len(MAIN), len(REF))
