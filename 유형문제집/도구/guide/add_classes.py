# -*- coding: utf-8 -*-
"""예비고1 수업가이드 — 사용자 작업본(TF 공통수학까지) 뒤에 반별 수업 안내를 이어 붙임 (2026-11-23).
python add_classes.py <사용자작업본.hwpx> <출력.hwpx>
- 순서(사용자): TF 공통수학1, 2(사용자 것 그대로) / HF 공통수학 / 추가 연계 수업 미적분2, 미적분1 / HF5 공통수학1 심화.
- 진도: 진도계획표38_2026 겨울방학(TF,고등전체) 'TF반' 시트(HF1·HF2, TF3·TF4 미적분2, TF5·TF6 미적분1, HF5 공통심화).
- HF: 기본서 CLIMATH ⓒ 공통수학1, 2 + 워크북. 1교시 개념 설명·STEP1, 2교시 STEP2·워크북 질의응답, 워크북(STEP1·2)은 진도에 맞춘 과제.
  공통수학1 단원별 쪽·번호는 hf_c1.json(책 쪽 = 인디자인 CLIMATH(c)_공통수학1 345쪽, 워크북 = CLIMATH(c)_공통수학1_워크북 PDF 쪽).
- HF5: 교재 CLIMATH ⓜ 공통수학1, 개념 수업 안내는 TF 개념 수업(4)과 같음.
- 문단·표 모양은 사용자 작업본에서 복제(제목 = 'TF 공통수학 수업' 문단, 항목 = '1) 교재' 문단, 진도계획표 = '2) 진도계획표' 문단(경로 그림 포함), 표 = 1단원 표).
"""
import sys, os, re, json, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from extract import top_paras

SRC, OUT = sys.argv[1:3]
C1 = json.load(open(os.path.join(HERE, "hf_c1.json"), encoding="utf-8"))

z = zipfile.ZipFile(SRC)
files = {n: z.read(n) for n in z.namelist()}
sec = files["Contents/section0.xml"].decode("utf-8")
P = top_paras(sec)
head_xml = sec[:sec.index(P[0])]
tail_xml = sec[sec.rindex(P[-1]) + len(P[-1]):]


def txt(p):
    return re.sub(r"<[^>]+>", "", "".join(re.findall(r"<hp:t>(.*?)</hp:t>", p, re.S)))


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def find(pred):
    return next(i for i, p in enumerate(P) if pred(p))


i_tf = find(lambda p: txt(p).strip() == "TF 공통수학 수업")
H_PARA, HB_PARA = P[i_tf], P[i_tf + 1]                      # 제목(자동 번호), 빈 줄
i_bk = find(lambda p: txt(p).startswith("1) 교재"))
ITEM, IB_PARA = P[i_bk], P[i_bk + 1]                        # 항목 문단(라벨 charPr 12 + 본문 charPr 9), 빈 줄
PLAN = P[find(lambda p: txt(p).startswith("2) 진도계획표"))]   # 진도계획표 경로 그림 문단
i_t1 = find(lambda p: "<hp:tbl" in p)
T_PARA, CAP_PARA = P[i_t1], P[i_t1 - 2]                      # 표 문단, 단원 제목 문단(paraPr 22 · charPr 13)
TBL = re.search(r"<hp:tbl .*?</hp:tbl>", T_PARA, re.S).group(0)
TRS = re.findall(r"<hp:tr>.*?</hp:tr>", TBL, re.S)
TC_H = re.findall(r"<hp:tc .*?</hp:tc>", TRS[0], re.S)[0]
TC_B = re.findall(r"<hp:tc .*?</hp:tc>", TRS[1], re.S)[0]
LAB_CP = re.search(r'<hp:run charPrIDRef="(\d+)"><hp:t>1\) 교재', ITEM).group(1)
BODY_CP = re.findall(r'<hp:run charPrIDRef="(\d+)">', ITEM)[1]
NID = [3995000000]


def nid():
    NID[0] += 1
    return str(NID[0])


def set_ids(x):
    x = re.sub(r'(<hp:p id=")\d+"', lambda m: m.group(1) + nid() + '"', x)
    x = re.sub(r'(<hp:(?:pic|tbl) id=")\d+"', lambda m: m.group(1) + nid() + '"', x)
    x = re.sub(r'(instid=")\d+"', lambda m: m.group(1) + nid() + '"', x)
    return re.sub(r"<hp:linesegarray>.*?</hp:linesegarray>", "", x, flags=re.S)


def tx(t):
    return esc(t).replace("\n", "<hp:lineBreak/>")


def heading(text):
    h = re.sub(r"<hp:t>[^<]*</hp:t>", "<hp:t>%s</hp:t>" % esc(text), H_PARA, count=1)
    return set_ids(re.sub(r'pageBreak="\d"', 'pageBreak="1"', h, count=1))


def item(label, lines, inline=False):
    """'1) 교재' 꼴: 라벨(굵게) + 줄바꿈 + 본문 줄들. inline: TF '4) ' 꼴(라벨 뒤에 바로 본문)"""
    pp = re.search(r'paraPrIDRef="(\d+)"', ITEM).group(1)
    runs = '<hp:run charPrIDRef="%s"><hp:t>%s%s</hp:t></hp:run>' % (LAB_CP, tx(label), "<hp:lineBreak/>" if lines and not inline else "")
    if lines:
        runs += '<hp:run charPrIDRef="%s"><hp:t>%s</hp:t></hp:run>' % (BODY_CP, tx("\n".join(lines)))
    return '<hp:p id="%s" paraPrIDRef="%s" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0">%s</hp:p>' % (nid(), pp, runs)


def caption(text):
    return set_ids(re.sub(r"<hp:t>[^<]*</hp:t>", "<hp:t>%s</hp:t>" % esc(text), CAP_PARA, count=1))


# 표 칸 테두리(사용자 표): 머리 4 | 6 | 7…, 몸 11 | 10 | 3…, 마지막 줄 첫 칸 12, 색칠 줄 9 | 5 | 8…
def tc(text, col, row, width, height, head, shade, last, left):
    t = TC_H if head else TC_B
    if head:
        bf = "4" if col == 0 else "6" if col == 1 else "7"
    elif shade:
        bf = "9" if col == 0 else "5" if col == 1 else "8"
    else:
        bf = ("12" if last else "11") if col == 0 else "10" if col == 1 else "3"
    t = re.sub(r'(<hp:tc [^>]*borderFillIDRef=")\d+', r"\g<1>" + bf, t, count=1)
    t = re.sub(r'(<hp:p [^>]*paraPrIDRef=")\d+', r"\g<1>" + ("22" if left and not head else "21"), t, count=1)
    t = re.sub(r"<hp:t>[^<]*</hp:t>", lambda _: "<hp:t>%s</hp:t>" % tx(text), t, count=1)
    t = re.sub(r'<hp:cellAddr colAddr="\d+" rowAddr="\d+"/>', '<hp:cellAddr colAddr="%d" rowAddr="%d"/>' % (col, row), t)
    t = re.sub(r'<hp:cellSz width="\d+" height="\d+"/>', '<hp:cellSz width="%d" height="%d"/>' % (width, height), t)
    return t


def table(header, rows, widths, left=(), shade=()):
    """rows: 칸 글자 목록(줄바꿈 '\n'). shade: 색칠할 줄 번호(1부터)"""
    assert sum(widths) == 48190 and all(len(r) == len(widths) for r in [header] + rows)
    trs, total = [], 0
    for r, cells in enumerate([header] + rows):
        h = 1500 + 1170 * (max(c.count("\n") for c in cells))
        total += h
        trs.append("<hp:tr>" + "".join(
            tc(c, k, r, widths[k], h, r == 0, r in shade, r == len(rows), k in left) for k, c in enumerate(cells)) + "</hp:tr>")
    t = re.sub(r"<hp:tr>.*</hp:tr>", lambda _: "".join(trs), TBL, count=1, flags=re.S)
    t = re.sub(r'rowCnt="\d+" colCnt="\d+"', 'rowCnt="%d" colCnt="%d"' % (len(trs), len(widths)), t, count=1)
    t = re.sub(r'(<hp:sz width="\d+" widthRelTo="ABSOLUTE" height=")\d+', lambda q: q.group(1) + str(total), t, count=1)
    return set_ids(T_PARA.replace(re.search(r"<hp:tbl .*?</hp:tbl>", T_PARA, re.S).group(0), t))


def blank():
    return set_ids(IB_PARA)


# ================================================================ HF 공통수학
C1_NAMES = ["다항식의 연산", "항등식", "나머지정리", "인수분해", "복소수", "이차함수와 이차방정식의 관계", "이차함수의 최대·최소",
            "고차방정식", "연립방정식", "연립부등식과 이차부등식", "연립이차부등식", "순열", "조합", "행렬"]
C2_NAMES = ["점과 직선", "원의 방정식", "도형의 이동", "집합", "집합의 연산", "명제", "명제의 증명", "여러 가지 함수",
            "합성함수와 역함수", "유리함수", "무리함수"]
# 진도계획표 TF반 시트 HF1(월·금), HF2(화·목) — (공통수학1/2, 단원, HF1 날짜, HF2 날짜, 비고)
HF_PLAN = [
    (1, 1, "11/27(금)", "11/26(목)", "OT/테스트 리뷰"), (1, 2, "11/27(금)", "11/26(목)", "1단원과 같은 날"),
    (1, 3, "11/30(월)", "12/1(화)", ""), (1, 4, "12/4(금)", "12/3(목)", ""), (1, 5, "12/7(월)", "12/8(화)", ""),
    (1, 6, "12/11(금)", "12/10(목)", ""), (1, 7, "12/14(월)", "12/15(화)", ""), (1, 8, "12/18(금)", "12/17(목)", ""),
    (1, 9, "12/21(월)", "12/22(화)", ""), (1, 10, "12/25(금)", "12/24(목)", ""), (1, 11, "12/28(월)", "12/29(화)", ""),
    (0, "수업 없음", "1/1(금)", "-", ""),
    (1, 12, "1/4(월)", "12/31(목)", "HF1은 13단원과 같은 날"), (1, 13, "1/4(월)", "1/5(화)", ""), (1, 14, "1/8(금)", "1/7(목)", ""),
    (2, 1, "1/11(월)", "1/12(화)", ""), (2, 2, "1/15(금)", "1/14(목)", ""), (2, 3, "1/18(월)", "1/19(화)", ""),
    (2, 4, "1/22(금)", "1/21(목)", ""), (2, 5, "1/25(월)", "1/26(화)", ""), (2, 6, "1/29(금)", "1/28(목)", ""),
    (2, 7, "2/1(월)", "2/2(화)", ""), (2, 8, "2/5(금)", "2/4(목)", ""), (0, "설날 연휴", "2/8(월)", "2/9(화)", ""),
    (2, 9, "2/12(금)", "2/11(목)", ""), (2, 10, "2/15(월)", "2/16(화)", ""), (2, 11, "2/19(금)", "2/18(목)", ""),
    (0, "고등부 개강", "2/22(월)", "2/23(화)", ""),
]


def hf_block():
    out = [heading("HF 공통수학 수업"), set_ids(HB_PARA),
           item("1) 교재", ["기본서 CLIMATH ⓒ 공통수학1, 2", "워크북 CLIMATH ⓒ 공통수학1, 2 워크북"]), blank(),
           set_ids(PLAN)]
    rows, shade = [], []
    for subj, u, d1, d2, note in HF_PLAN:
        if subj == 0:
            rows.append(["-", u, d1, d2, note]); shade.append(len(rows))
        else:
            rows.append(["공통수학%d" % subj, "%d. %s" % (u, (C1_NAMES if subj == 1 else C2_NAMES)[u - 1]), d1, d2, note])
    out += [table(["과목", "단원", "HF1 (월·금)", "HF2 (화·목)", "비고"], rows, [7000, 15190, 8000, 8000, 10000], left=(1, 4), shade=shade),
            blank(),
            item("3) 수업구조", ["",
                                "- HF1 월·금, HF2 화·목 5:30~10:00",
                                "- 공통수학1부터 단원 순서대로 진도 (첫 시간 OT/테스트 리뷰)",
                                "  1교시 단원 개념 설명 + STEP1 개념 확인하기",
                                "  2교시 STEP2 유형별 학습하기 + 워크북 질의응답",
                                "- 워크북도 단원마다 STEP1, STEP2로 되어 있습니다.",
                                "  진도계획표대로 그날 나간 단원의 워크북을 과제로 내주고,",
                                "  다음 시간 2교시에 질의응답 받아주세요."]),
            blank(),
            item("4) 단원별 수업 범위 (공통수학1)", ["쪽은 책 쪽이고, 개념 필기는 단원 앞의 줄 노트 쪽입니다.",
                                              "기본서 번호는 단원마다 1번부터, 워크북 번호는 책 전체에 이어집니다.",
                                              "유형별 문항 번호는 CLIMATH ⓒ 공통수학1 단원분류표를 보시면 됩니다."]),
            blank()]
    rows = []
    for d in C1:
        rows.append(["%d. %s" % (d["u"], d["name"]),
                     "개념 필기 %d~%d쪽\nSTEP1 %d~%d쪽 (1~%d번)" % (d["opener"] + 1, d["s1_page"] - 1, d["s1_page"], d["s2_page"] - 1, d["s1_last"]),
                     "STEP2 %d~%d쪽\n유형 01~%02d (%d~%d번)" % (d["s2_page"], d["end"], d["s2_types"], d["s2_first"], d["total"]),
                     "%d~%d쪽\nSTEP1 %d~%d번 · STEP2 %d~%d번" % (d["wb_page"], d["wb_end"], d["wb_first"], d["wb_s2_first"] - 1, d["wb_s2_first"], d["wb_last"])])
    out += [table(["단원", "1교시 개념 설명 · STEP1", "2교시 STEP2", "과제 워크북 (다음 시간 질의응답)"], rows,
                  [12000, 11000, 11000, 14190], left=(0,)), blank()]
    return out


# ================================================================ 추가 연계 수업 미적분2, 미적분1
CAL2 = ["수열의 극한", "급수", "지수·로그함수의 미분", "삼각함수의 덧셈정리", "삼각함수의 미분", "여러 가지 미분법", "접선의 방정식",
        "극대, 극소와 그래프", "도함수의 활용", "부정적분", "정적분", "정적분과 함수", "정적분의 활용"]
CAL1 = ["함수의 극한", "함수의 연속", "미분계수와 도함수", "접선의 방정식", "극대, 극소와 그래프", "도함수의 활용", "부정적분",
        "정적분", "정적분과 함수", "정적분의 활용"]
# (단원 번호 또는 행사 이름, TF3/TF5 수, TF4/TF6 일)
CAL2_PLAN = [(1, "11/25(수)", "11/29(일)"), (2, "12/2(수)", "12/6(일)"), (3, "12/9(수)", "12/13(일)"), (4, "12/16(수)", "12/20(일)"),
             (5, "12/23(수)", "12/27(일)"), (6, "12/30(수)", "1/3(일)"), (7, "1/6(수)", "1/10(일)"), (8, "1/13(수)", "1/17(일)"),
             (9, "1/20(수)", "1/24(일)"), (10, "1/27(수)", "1/31(일)"), ("설날 연휴", "-", "2/7(일)"), (11, "2/3(수)", "2/14(일)"),
             (12, "2/10(수)", "2/14(일)"), (13, "2/17(수)", "2/21(일)"), ("고등부 개강", "2/24(수)", "2/28(일)")]
CAL1_PLAN = [(1, "11/25(수)", "11/29(일)"), (2, "12/2(수)", "12/6(일)"), (3, "12/9(수)", "12/13(일)"), (4, "12/16(수)", "12/20(일)"),
             (5, "12/23(수)", "12/27(일)"), ("중간평가", "12/30(수)", "1/3(일)"), (6, "1/6(수)", "1/10(일)"), (7, "1/13(수)", "1/17(일)"),
             (8, "1/20(수)", "1/24(일)"), (9, "1/27(수)", "1/31(일)"), ("설날 연휴", "-", "2/7(일)"), (10, "2/3(수)", "2/14(일)"),
             ("기말평가 및 풀이", "2/10(수)", "-"), ("수능 문제 풀이", "2/17(수)", "2/21(일)"), ("고등부 개강", "2/24(수)", "2/28(일)")]


def plan_table(plan, names, h1, h2):
    rows, shade = [], []
    for u, d1, d2 in plan:
        if isinstance(u, int):
            rows.append(["%d. %s" % (u, names[u - 1]), d1, d2])
        else:
            rows.append([u, d1, d2]); shade.append(len(rows))
    return table(["단원", h1, h2], rows, [20190, 14000, 14000], left=(0,), shade=shade)


def cal_block():
    return [heading("추가 연계 수업 (미적분2, 미적분1)"), set_ids(HB_PARA),
            item("1) 교재", ["미적분2 수매씽 미적분2", "미적분1 수매씽 미적분1"]), blank(),
            set_ids(PLAN), caption("미적분2"), plan_table(CAL2_PLAN, CAL2, "TF3 (수)", "TF4 (일)"), blank(),
            caption("미적분1"), plan_table(CAL1_PLAN, CAL1, "TF5 (수)", "TF6 (일)"), blank(),
            item("3) 수업구조", ["",
                                "- 미적분2 TF3 수 5:30~9:50, TF4 일 12:40~5:00",
                                "- 미적분1 TF5 수 5:30~9:50, TF6 일 12:40~5:00",
                                "- 진도계획표대로 한 회차에 한 단원씩 나갑니다.",
                                "  첫 시간 대수 TEST, 그다음부터는 매 시간 주간테스트(지난 단원)를 봅니다."]),
            blank()]


# ================================================================ HF5 공통수학1 심화
CM1 = ["다항식의 연산과 항등식", "나머지정리", "인수분해", "복소수와 이차방정식", "이차함수와 이차방정식의 관계", "이차함수의 최대, 최소",
       "여러 가지 방정식", "이차부등식", "연립부등식", "경우의 수와 순열", "조합", "행렬"]
HF5_DATES = ["12/2(수)", "12/9(수)", "12/16(수)", "12/23(수)", "12/30(수)", "1/6(수)", "1/13(수)", "1/20(수)", "1/27(수)",
             "2/3(수)", "2/10(수)", "2/17(수)"]


def hf5_block():
    rows = [["%d. %s" % (u, CM1[u - 1]), HF5_DATES[u - 1], "서술형 클리닉 %d회" % u if u <= 11 else "-"] for u in range(1, 13)]
    return [heading("HF5 공통수학1 심화 수업"), set_ids(HB_PARA),
            item("1) 교재", ["기본서 CLIMATH ⓜ 공통수학1"]), blank(),
            set_ids(PLAN), table(["단원", "HF5 (수)", "같은 날"], rows, [20190, 12000, 16000], left=(0,)), blank(),
            item("3) 수업구조", ["",
                                "- 수 5:30~9:50",
                                "- 진도계획표대로 한 회차에 CLIMATH ⓜ 공통수학1 한 단원 개념 수업 + 서술형 클리닉"]),
            blank(),
            item("4) ", ["개념 수업 시 CLIMATH ⓜ 단원별 필수 문항은 TF 공통수학 수업 4)와 같습니다.",
                         "공통수학1 단원별 표의 문제를 반드시 풀어 주시고, 시간이 되시면 단원마무리 문제를 모두 풀어 주세요.",
                         "남은 문제는 과제로 내주고, 다음 시간에 질의응답 받아주세요."], inline=True),
            blank()]


new = P + hf_block() + cal_block() + hf5_block()
sec_new = head_xml + "".join(new) + tail_xml
files["Contents/section0.xml"] = sec_new.encode("utf-8")
with zipfile.ZipFile(OUT, "w") as w:
    for n in z.namelist():
        info = zipfile.ZipInfo(n, date_time=(1980, 1, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_STORED if n == "mimetype" else zipfile.ZIP_DEFLATED
        w.writestr(info, files[n])
print("문단", len(P), "->", len(new), "표", sec_new.count("<hp:tbl "), "->", OUT)
