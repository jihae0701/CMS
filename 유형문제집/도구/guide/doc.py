# -*- coding: utf-8 -*-
"""기본서 수업 필수 문항 가이드(한글 파일) 만들기 (2026-11-19).
python doc.py <1|2> <analyze.py가 만든 json> <출력.hwpx>
- 틀(글꼴·문단·표 모양)은 조립제법_표.hwpx(짝 문항 정리표 pairtable.py와 같은 방식).
- 단원마다: ① 꼭 풀어 줄 문항 표(기본서 번호·유형·꼭 풀 이유·유형서에서 이어지는 문항) ② 유형 연계 표(유형서 유형 → 기본서 유형).
"""
import sys, os, re, json, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
TPL = os.path.join(ROOT, "조립제법_표.hwpx")
bookno, src, out = int(sys.argv[1]), sys.argv[2], sys.argv[3]
R = json.load(open(src, encoding="utf-8"))

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


GRAY = '<hc:fillBrush><hc:winBrush faceColor="#E5E5E5" hatchColor="#999999" alpha="0"/></hc:fillBrush>'
PINK = '<hc:fillBrush><hc:winBrush faceColor="#FDECEC" hatchColor="#999999" alpha="0"/></hc:fillBrush>'
head, BF_HEAD = add_item(head, "borderFill", "borderFills", "3", lambda x: x.replace("</hh:borderFill>", GRAY + "</hh:borderFill>"))
head, BF_REP = add_item(head, "borderFill", "borderFills", "3", lambda x: x.replace("</hh:borderFill>", PINK + "</hh:borderFill>"))
head, PP_C = add_item(head, "paraPr", "paraProperties", "0",
                      lambda x: x.replace('horizontal="JUSTIFY"', 'horizontal="CENTER"').replace('value="160"', 'value="130"'))
head, PP_L = add_item(head, "paraPr", "paraProperties", "0",
                      lambda x: x.replace('horizontal="JUSTIFY"', 'horizontal="LEFT"').replace('value="160"', 'value="130"'))
head, CP_B = add_item(head, "charPr", "charProperties", "0", lambda x: x.replace('<hh:underline', '<hh:bold/><hh:underline'))
head, CP_S = add_item(head, "charPr", "charProperties", "0", lambda x: x.replace('height="1000"', 'height="900"', 1))
head, CP_T = add_item(head, "charPr", "charProperties", "0",
                      lambda x: x.replace('height="1000"', 'height="1600"', 1).replace('<hh:underline', '<hh:bold/><hh:underline'))
head, CP_H = add_item(head, "charPr", "charProperties", "0",
                      lambda x: x.replace('height="1000"', 'height="1250"', 1).replace('<hh:underline', '<hh:bold/><hh:underline'))
files["Contents/header.xml"] = head.encode("utf-8")

sec = files["Contents/section0.xml"].decode("utf-8")
first = sec[:sec.index('<hp:run charPrIDRef="0"><hp:tbl')] + "</hp:p>"
NID = [3100000000]


def nid():
    NID[0] += 1
    return str(NID[0])


esc = lambda t: t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def para(text, pp=0, cp=0, page_break=False):
    return ('<hp:p id="%s" paraPrIDRef="%d" styleIDRef="0" pageBreak="%d" columnBreak="0" merged="0"><hp:run charPrIDRef="%d">%s</hp:run></hp:p>'
            % (nid(), pp, 1 if page_break else 0, cp, "<hp:t>%s</hp:t>" % esc(text) if text else "<hp:t/>"))


def cell(r, c, text, w, bf, pp, cp, h=1500):
    lines = text.split("\n")
    ps = "".join(para(t, pp, cp) for t in lines)
    return ('<hp:tc name="" header="%d" hasMargin="0" protect="0" editable="0" dirty="0" borderFillIDRef="%d">'
            '<hp:subList id="" textDirection="HORIZONTAL" lineWrap="BREAK" vertAlign="CENTER" linkListIDRef="0" linkListNextIDRef="0" textWidth="0" textHeight="0" hasTextRef="0" hasNumRef="0">'
            '%s</hp:subList><hp:cellAddr colAddr="%d" rowAddr="%d"/><hp:cellSpan colSpan="1" rowSpan="1"/>'
            '<hp:cellSz width="%d" height="%d"/><hp:cellMargin left="400" right="400" top="120" bottom="120"/></hp:tc>'
            % (1 if r == 0 else 0, bf, ps, c, r, w, h * len(lines)))


def table(rows, widths, aligns, rowfill=None):
    trs = []
    for r, row in enumerate(rows):
        tcs = []
        for c, t in enumerate(row):
            if r == 0:
                tcs.append(cell(r, c, t, widths[c], BF_HEAD, PP_C, CP_B))
            else:
                bf = BF_REP if (rowfill and rowfill[r]) else 3
                tcs.append(cell(r, c, t, widths[c], bf, PP_C if aligns[c] == "c" else PP_L, CP_S))
        trs.append("<hp:tr>%s</hp:tr>" % "".join(tcs))
    H = sum(1500 * max(len(t.split("\n")) for t in row) for row in rows)
    tbl = ('<hp:tbl id="%s" zOrder="0" numberingType="TABLE" textWrap="TOP_AND_BOTTOM" textFlow="BOTH_SIDES" lock="0" dropcapstyle="None" pageBreak="CELL" repeatHeader="1" rowCnt="%d" colCnt="%d" cellSpacing="0" borderFillIDRef="3" noAdjust="0">'
           '<hp:sz width="%d" widthRelTo="ABSOLUTE" height="%d" heightRelTo="ABSOLUTE" protect="0"/>'
           '<hp:pos treatAsChar="1" affectLSpacing="0" flowWithText="1" allowOverlap="0" holdAnchorAndSO="0" vertRelTo="PARA" horzRelTo="PARA" vertAlign="TOP" horzAlign="LEFT" vertOffset="0" horzOffset="0"/>'
           '<hp:outMargin left="0" right="0" top="0" bottom="0"/><hp:inMargin left="400" right="400" top="120" bottom="120"/>%s</hp:tbl>'
           % (nid(), len(rows), len(widths), sum(widths), H, "".join(trs)))
    return ('<hp:p id="%s" paraPrIDRef="%d" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0"><hp:run charPrIDRef="0">%s<hp:t/></hp:run></hp:p>'
            % (nid(), PP_C, tbl))


def tname(t):
    if not t:
        return "단원 마무리"
    return "%02d %s" % (t[0], t[1])


def twin_text(t):
    lab = {"같은 문제": "같은 문제(숫자까지 같음)", "쌍둥이": "쌍둥이", "같은 틀": "같은 틀"}[t["kind"]]
    s = "%03d %s" % (t["n"], lab)
    if t["stage"] == "종합":
        s += ", 단원종합" + (" · " + t["mock"] if t["mock"] else "")
        if t["lite"] is True: s += " · Lite 같음"
        elif t["lite"] is False: s += " · Lite는 다른 문항"
    return s


body = [first, para("공통수학%d 기본서(CLIMATH ⓜ) 수업 필수 문항" % bookno, PP_C, CP_T), para(""),
        para("· 기본서 수업에서 꼭 풀어 줄 문항 = 대표문제 + 유형서(CMStory Core·Lite)에 쌍둥이·같은 틀 문항이 있는 기본서 문항.", PP_L),
        para("· 쌍둥이: 숫자만 바꾸거나 거의 같은 문제 / 같은 틀: 조건·묻는 방식의 문장이 같고 식만 다른 문제 / 같은 문제: 숫자까지 같은 문제.", PP_L),
        para("· 대표문제에 쌍둥이가 없으면, 이어지는 유형서 유형에서 가장 닮은 문항을 '이어 풀기'로 적었다(유형서 과제 연결용).", PP_L),
        para("· 유형서 문항 번호는 Core와 Lite가 같다. 단원종합문제는 Lite에서 바뀐 문항이 있어 'Lite 같음/다른 문항'을 따로 적었다.", PP_L),
        para("· 짝은 기본서·유형서 완성본의 문제 글을 모두 꺼내 수식 뼈대(숫자는 지움)와 문장 낱말의 겹침으로 자동으로 찾았다. 수업 전에 짝 문항을 한 번 확인해 주세요.", PP_L),
        para("")]
# 요약 표
rows = [["단원", "기본서 번호", "대표문제", "쌍둥이·같은 틀이 있는 문항", "꼭 풀 문항 합계"]]
for r in R:
    reps = sum(1 for m in r["must"] if m["rep"])
    tw = sum(1 for m in r["must"] if m["twins"] and not m["rep"])
    rows.append(["%d. %s" % (r["unit"], r["name"]), "%03d~%03d" % tuple(r["b_range"]), str(reps), "%d (대표문제 제외)" % tw, str(len(r["must"]))])
body.append(table(rows, [13500, 7500, 6000, 12500, 8690], "lcccc"))
for r in R:
    body.append(para("%d. %s   (기본서 %03d~%03d · 유형서 %03d~%03d)" % (r["unit"], r["name"], r["b_range"][0], r["b_range"][1], r["y_range"][0], r["y_range"][1]), PP_L, CP_H, page_break=True))
    body.append(para(""))
    body.append(para("① 꼭 풀어 줄 문항 (분홍 칸 = 대표문제)", PP_L, CP_B))
    rows = [["기본서", "유형", "꼭 풀 이유", "유형서에서 이어지는 문항 (Core·Lite 번호 같음)"]]
    fill = [False]
    for m in r["must"]:
        why = []
        if m["rep"]: why.append("대표문제")
        kinds = sorted(set(t["kind"] for t in m["twins"]), key=["같은 문제", "쌍둥이", "같은 틀"].index)
        if kinds: why.append("유형서 " + "·".join(kinds))
        link = "\n".join(twin_text(t) for t in m["twins"]) if m["twins"] else (
            "이어 풀기: " + ", ".join("%03d" % f["n"] for f in m["follow"]) if m["follow"] else "-")
        rows.append(["%03d" % m["n"], tname(m["type"]), " + ".join(why), link])
        fill.append(m["rep"])
    body.append(table(rows, [5000, 15500, 9500, 18190], "cllc", fill))
    body.append(para(""))
    body.append(para("② 유형 연계 (유형서 유형 → 가까운 기본서 유형)", PP_L, CP_B))
    rows = [["유형서 유형", "유형서 번호", "가까운 기본서 유형", "기본서 대표문제"]]
    bt = {t["no"]: t for t in r["btypes"]}
    for t in r["ytypes"]:
        b = bt.get(t["btype"]) if t["fit"] >= 0.3 else None
        rows.append(["%02d %s" % (t["no"], t["title"]), "%03d~%03d" % tuple(t["range"]),
                     ("%02d %s" % (b["no"], b["title"])) if b else "직접 대응 없음(개념으로 설명)",
                     ", ".join("%03d" % n for n in b["reps"]) if b else "-"])
    if r["y_mix"]:
        rows.append(["단원종합문제", "%03d~%03d" % (r["y_mix"][0], r["y_mix"][-1]), "단원 마무리(STEP 3)·여러 유형", "-"])
    body.append(table(rows, [15500, 7000, 17190, 8500], "lcll"))
    body.append(para(""))

files["Contents/section0.xml"] = ("".join(body) + "</hs:sec>").encode("utf-8")
if "Preview/PrvText.txt" in files:
    files["Preview/PrvText.txt"] = ("공통수학%d 기본서 수업 필수 문항" % bookno).encode("utf-8")
with zipfile.ZipFile(out, "w") as w:
    for n in z.namelist():
        info = zipfile.ZipInfo(n, date_time=(1980, 1, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_STORED if n == "mimetype" else zipfile.ZIP_DEFLATED
        w.writestr(info, files[n])
print("->", out)
