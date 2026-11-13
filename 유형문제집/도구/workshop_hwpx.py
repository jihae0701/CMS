# -*- coding: utf-8 -*-
"""수업 가이드 워크숍 제안서(2026-11-13 Claude Docs 문서와 같은 내용)를 수정 가능한 한글 파일(HWPX)로 만든다.
python workshop_hwpx.py <출력.hwpx>
틀(글꼴·문단 모양)은 조립제법_표.hwpx(unittable.py와 같은 방식)."""
import sys, os, re, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TPL = os.path.join(ROOT, "조립제법_표.hwpx")
z = zipfile.ZipFile(TPL)
files = {n: z.read(n) for n in z.namelist()}
head = files["Contents/header.xml"].decode("utf-8")


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def add_item(head, tag, plural, src_id, fn):
    m = re.search(r'<hh:%s id="%s".*?</hh:%s>' % (tag, src_id, tag), head, re.S)
    cnt = int(re.search(r'<hh:%s itemCnt="(\d+)"' % plural, head).group(1))
    new = fn(re.sub(r'id="%s"' % src_id, 'id="%d"' % cnt, m.group(0), count=1))
    end = head.index("</hh:%s>" % plural)
    head = head[:end] + new + head[end:]
    head = re.sub(r'<hh:%s itemCnt="\d+"' % plural, '<hh:%s itemCnt="%d"' % (plural, cnt + 1), head, count=1)
    return head, cnt


GRAY = '<hc:fillBrush><hc:winBrush faceColor="#E5E5E5" hatchColor="#999999" alpha="0"/></hc:fillBrush>'
head, BF_HEAD = add_item(head, "borderFill", "borderFills", "3", lambda x: x.replace("</hh:borderFill>", GRAY + "</hh:borderFill>"))
head, PP_C = add_item(head, "paraPr", "paraProperties", "0",
                      lambda x: x.replace('horizontal="JUSTIFY"', 'horizontal="CENTER"').replace('value="160"', 'value="130"'))
head, PP_L = add_item(head, "paraPr", "paraProperties", "0",
                      lambda x: x.replace('horizontal="JUSTIFY"', 'horizontal="LEFT"').replace('value="160"', 'value="130"'))
head, PP_H = add_item(head, "paraPr", "paraProperties", "0",          # 소제목: 위 여백
                      lambda x: re.sub(r'(<hc:prev value=")\d+(")', r'\g<1>1400\2', x))
head, CP_B = add_item(head, "charPr", "charProperties", "0", lambda x: x.replace('<hh:underline', '<hh:bold/><hh:underline'))
head, CP_T = add_item(head, "charPr", "charProperties", "0",
                      lambda x: x.replace('height="1000"', 'height="1600"', 1).replace('<hh:underline', '<hh:bold/><hh:underline'))
head, CP_H = add_item(head, "charPr", "charProperties", "0",
                      lambda x: x.replace('height="1000"', 'height="1250"', 1).replace('<hh:underline', '<hh:bold/><hh:underline'))
head, CP_S = add_item(head, "charPr", "charProperties", "0", lambda x: x.replace('height="1000"', 'height="900"', 1))
files["Contents/header.xml"] = head.encode("utf-8")

sec = files["Contents/section0.xml"].decode("utf-8")
first = sec[:sec.index("<hp:run charPrIDRef=\"0\"><hp:tbl")] + "</hp:p>"
NID = [3100000000]


def nid():
    NID[0] += 1
    return str(NID[0])


def runs(text, cp=0):
    """'**굵게**' 표시를 굵은 글자로"""
    out = []
    for k, part in enumerate(re.split(r"\*\*", text)):
        if part:
            out.append('<hp:run charPrIDRef="%d"><hp:t>%s</hp:t></hp:run>' % (CP_B if k % 2 else cp, esc(part)))
    return "".join(out) or '<hp:run charPrIDRef="%d"><hp:t/></hp:run>' % cp


def para(text, pp=0, cp=0):
    return ('<hp:p id="%s" paraPrIDRef="%d" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0">%s</hp:p>'
            % (nid(), pp, runs(text, cp)))


def cell(r, c, text, w, headrow=False):
    return ('<hp:tc name="" header="%d" hasMargin="0" protect="0" editable="0" dirty="0" borderFillIDRef="%d">'
            '<hp:subList id="" textDirection="HORIZONTAL" lineWrap="BREAK" vertAlign="CENTER" linkListIDRef="0" linkListNextIDRef="0" textWidth="0" textHeight="0" hasTextRef="0" hasNumRef="0">'
            '%s</hp:subList><hp:cellAddr colAddr="%d" rowAddr="%d"/><hp:cellSpan colSpan="1" rowSpan="1"/>'
            '<hp:cellSz width="%d" height="1500"/><hp:cellMargin left="510" right="510" top="141" bottom="141"/></hp:tc>'
            % (1 if headrow else 0, BF_HEAD if headrow else 3,
               para(text, PP_C if headrow else PP_L, CP_B if headrow else 0), c, r, w))


def table(rows, widths):
    trs = ["<hp:tr>%s</hp:tr>" % "".join(cell(r, c, t, widths[c], r == 0) for c, t in enumerate(row)) for r, row in enumerate(rows)]
    tbl = ('<hp:tbl id="%s" zOrder="0" numberingType="TABLE" textWrap="TOP_AND_BOTTOM" textFlow="BOTH_SIDES" lock="0" dropcapstyle="None" pageBreak="CELL" repeatHeader="1" rowCnt="%d" colCnt="%d" cellSpacing="0" borderFillIDRef="3" noAdjust="0">'
           '<hp:sz width="%d" widthRelTo="ABSOLUTE" height="%d" heightRelTo="ABSOLUTE" protect="0"/>'
           '<hp:pos treatAsChar="1" affectLSpacing="0" flowWithText="1" allowOverlap="0" holdAnchorAndSO="0" vertRelTo="PARA" horzRelTo="PARA" vertAlign="TOP" horzAlign="LEFT" vertOffset="0" horzOffset="0"/>'
           '<hp:outMargin left="0" right="0" top="0" bottom="0"/><hp:inMargin left="510" right="510" top="141" bottom="141"/>%s</hp:tbl>'
           % (nid(), len(rows), len(widths), sum(widths), 1500 * len(rows), "".join(trs)))
    return ('<hp:p id="%s" paraPrIDRef="%d" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0"><hp:run charPrIDRef="0">%s<hp:t/></hp:run></hp:p>'
            % (nid(), PP_C, tbl))


W = 48190   # 쪽 너비 59528 − 왼쪽·오른쪽 여백
B = []
add = B.append
add(para("CLIMATH·CMStory 수업 가이드 워크숍 제안", PP_C, CP_T))
add(para("2026년 11월 13일 초안", PP_C, CP_S))
add(para(""))
add(para("2026년 11월 19일부터 2027년 1월 7일까지 매주 화·목, 공통수학1·2의 같은 번호 단원을 한 회차에 함께 다루며 기본서를 풀고 유형서와 연계한 질의응답 수업 가이드를 단원별로 만듭니다. 교재가 아직 완성 전이라 이 문서는 틀만 잡은 초안입니다."))

add(para("1. 목적과 역할", PP_H, CP_H))
add(para("워크숍의 결과물은 단원별 '질의응답 수업 가이드'입니다. 기본서 수업과 질의응답을 맡는 선생님이 다르기 때문에, 질의응답 선생님이 기본서 수업의 흐름을 알고 유형서 질문에 답할 수 있게 하려는 것입니다."))
add(table([["누가", "무엇을", "가이드가 주는 것"],
           ["고등부 선생님", "기본서 CLIMATH(m) 수업", "기본서에서 다룬 개념·대표 문항·풀이 방식의 기준"],
           ["중등부 선생님", "개념서·유형서(CMStory Core·Lite) 질의응답", "단원별 연계표, 자주 나오는 질문과 답하는 순서, 막히는 지점"]],
          [9000, 16000, 23190]))
add(para("· 워크숍에서는 기본서를 직접 풀어 보고, 같은 단원의 유형서 문항과 짝지어 가이드 초안을 씁니다."))
add(para("· 가이드는 질의응답 선생님이 수업 전에 10분 안에 읽을 수 있는 분량을 목표로 합니다."))

add(para("2. 교재 구성", PP_H, CP_H))
add(para("세 교재를 공통수학1·2 각 12단원으로 쓰며, 단원 번호는 세 교재가 같습니다."))
add(table([["교재", "성격", "수업", "현재 상태(11/13)"],
           ["CLIMATH(m)", "기본서: 개념 → 기본 문제 → 단원 마무리", "고등부 선생님", "공통수학1·2 1~12단원 초안, 완성본 등록 중"],
           ["CMStory Core", "유형서: 유형별 문제 + 단원종합문제(고난도·모의고사)", "중등부 선생님 질의응답", "공통수학1·2 1~12단원"],
           ["CMStory Lite", "유형서: Core와 같은 번호·구성, 단원종합문제만 중·중상 난도", "중등부 선생님 질의응답", "공통수학1 1~12, 공통수학2 1~6단원"]],
          [8500, 18000, 9000, 12690]))
add(para("Core와 Lite는 단원종합문제만 다르므로, 가이드의 유형 연계는 한 번에 쓰고 단원종합문제만 따로 적습니다."))

add(para("3. 일정", PP_H, CP_H))
add(para("기간 안 화·목은 11회라 12단원과 하나가 모자랍니다. 아래 안은 분량이 가장 적은 11·12단원을 마지막 회차에 묶었습니다."))
sched = [["회차", "날짜", "공통수학1", "공통수학2"],
         ["1", "11/19(목)", "1. 다항식의 연산과 항등식", "1. 평면좌표"],
         ["2", "11/24(화)", "2. 나머지정리", "2. 직선의 방정식"],
         ["3", "11/26(목)", "3. 인수분해", "3. 원의 방정식"],
         ["4", "12/1(화)", "4. 복소수와 이차방정식", "4. 도형의 이동"],
         ["5", "12/3(목)", "5. 이차함수와 이차방정식의 관계", "5. 집합의 뜻과 표현"],
         ["—", "12/4~12/21", "쉬는 기간", "쉬는 기간"],
         ["6", "12/22(화)", "6. 이차함수의 최대, 최소", "6. 집합의 연산"],
         ["7", "12/24(목)", "7. 여러 가지 방정식", "7. 명제"],
         ["8", "12/29(화)", "8. 이차부등식", "8. 절대부등식"],
         ["9", "12/31(목)", "9. 연립부등식", "9. 함수"],
         ["10", "1/5(화)", "10. 경우의 수와 순열", "10. 합성함수와 역함수"],
         ["11", "1/7(목)", "11. 조합 · 12. 행렬", "11. 유리식과 유리함수 · 12. 무리식과 무리함수"]]
add(table(sched, [5000, 9000, 16000, 18190]))
add(para("12/24(크리스마스 이브)와 12/31(연말)은 참석이 어려울 수 있어 확인이 필요합니다."))

add(para("4. 회차 진행 방식", PP_H, CP_H))
add(para("한 회차는 '미리 풀기 → 워크숍에서 연결하기 → 가이드로 정리하기'로, 공통수학1·2 두 단원을 같은 순서로 다룹니다."))
for k, t in enumerate(["**사전 준비(회차 전)**: 참여 선생님이 해당 단원 기본서를 풀고, 막힌 문항과 학생이 물을 만한 문항에 표시합니다.",
                       "**기본서 점검**: 고등부 선생님이 수업에서 강조할 개념·대표 문항·풀이 방식을 설명합니다.",
                       "**유형서 연결**: 기본서 문항마다 이어지는 Core·Lite 유형과 문항 번호를 짝짓습니다.",
                       "**질문 예상**: 중등부 선생님 입장에서 나올 질문과 답하는 순서(힌트 → 핵심 개념 → 풀이)를 정합니다.",
                       "**가이드 초안**: 아래 '수업 가이드 틀'에 맞춰 단원마다 한 장으로 적습니다.",
                       "**정리(회차 후)**: 담당자가 초안을 다듬어 다음 회차 전에 공유합니다."], 1):
    add(para("%d. %s" % (k, t)))

add(para("5. 수업 가이드 틀", PP_H, CP_H))
add(para("단원마다 아래 다섯 항목을 채운 한 장을 만듭니다(공통수학1·2 합치면 회차당 2장)."))
for k, t in enumerate(["**단원 한눈에**: 기본서에서 다루는 핵심 개념 3~5개와 앞·뒤 단원과의 연결.",
                       "**기본서 수업 흐름**: 고등부 선생님이 쓰는 개념 설명 순서와 풀이 방식(기호·용어를 맞추기 위함).",
                       "**유형 연계표**: 아래 표처럼 기본서 문항과 Core·Lite 유형을 잇습니다.",
                       "**자주 나오는 질문**: 질문마다 답하는 순서(처음 줄 힌트 → 다시 볼 개념 → 풀이 핵심)와 흔한 오개념.",
                       "**단원종합문제 안내**: Core(고난도·모의고사)와 Lite(중·중상)로 나뉘는 문항, 학생 수준별 추천."], 1):
    add(para("%d. %s" % (k, t)))
add(para("유형 연계표 예시(칸만 잡음):"))
add(table([["기본서 문항", "핵심 개념", "Core 유형·번호", "Lite 번호", "질문 포인트"], ["", "", "", "", ""], ["", "", "", "", ""]],
          [8000, 10000, 10000, 8000, 12190]))

add(para("6. 정할 것", PP_H, CP_H))
for t in ["11회에 12단원: 마지막 회차에 11·12단원을 묶을지, 회차를 하나 더할지(예: 1/8 금 또는 1/12 화)",
          "12/24·12/31 회차를 그대로 할지, 다른 날로 옮길지",
          "회차당 시간과 장소(예: 2시간, 공통수학1·2 각 1시간)",
          "참여 선생님과 단원별 가이드 담당자",
          "아직 없는 교재: Lite 공통수학2 7~12단원을 해당 회차(12/24~) 전까지 만들지, 그 회차는 Core만으로 할지",
          "가이드 형식(한글 문서·공유 문서)과 중등부 선생님께 전달하는 시점"]:
    add(para("□ " + t))

files["Contents/section0.xml"] = (first + "".join(B) + "</hs:sec>").encode("utf-8")
if "Preview/PrvText.txt" in files:
    files["Preview/PrvText.txt"] = "CLIMATH·CMStory 수업 가이드 워크숍 제안".encode("utf-8")
out = sys.argv[1]
with zipfile.ZipFile(out, "w") as w:
    for n in z.namelist():
        info = zipfile.ZipInfo(n, date_time=(1980, 1, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_STORED if n == "mimetype" else zipfile.ZIP_DEFLATED
        w.writestr(info, files[n])
print("->", out)
