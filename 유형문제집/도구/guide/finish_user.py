# -*- coding: utf-8 -*-
"""사용자가 만들던 '예비고1 수업가이드'를 다듬고 공통수학1·2 필수 문항 표를 끝까지 채움 (2026-11-21).
python finish_user.py <사용자 수업가이드.hwpx> <출력.hwpx>
- 사용자: '내가 수업가이드 만들고 있어. 손봐주고 이어서 공통수학1, 2 마무리해 줘' + 사용자 파일(공통사항 + 공통수학1 1·2단원 필수 문항 표).
- 사용자 표는 우리 수업필수문항 문서(doc.py)의 '① 꼭 풀어 줄 문항' 표를 옮겨 다듬은 것 → 사용자가 다듬은 규칙을 그대로 따라 나머지 단원을 만든다.
  · 머리줄 '번호 | 유형 | 꼭 풀 이유 | 유형서에서 이어지는 문항'
  · 꼭 풀 이유: 대표문제면 '대표문제'(뒤의 '+ 유형서 쌍둥이' 등은 뺌), 아니면 '유형서 ' + 가장 가까운 짝 하나(같은 문제 > 쌍둥이 > 같은 틀)
  · 이어지는 문항: 종류별로 묶어 번호순 '036, 037, 043 쌍둥이', 종류가 둘이면 첫 번호 순서로 '064 같은 틀, 067, 068 쌍둥이'.
    단원종합·Lite 메모는 뺌. 짝이 없으면 '이어 풀기: …'(번호순), 그것도 없으면 '-'.
- 표·단원 제목 모양은 사용자 파일의 1단원 표(머리줄·대표문제 줄·일반 줄)와 2단원 제목 문단을 복제.
- 다듬기: 오타(CMStroy→CMStory), 쉼표('공통수학1. 2'→'공통수학1, 2', '1. 2교시'→'1, 2교시'), 3)과 4) 사이 빈 줄 5줄→1줄,
  사용자 2단원 표의 번호 띄어쓰기를 1단원처럼 쉼표로('063 064 071'→'063, 064, 071'), 이어 풀기 번호순.
  1단원에서 사용자가 뺀 032번은 그대로 뺀 채 둠.
"""
import sys, os, re, json, zipfile, html

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from extract import top_paras

SRC, OUT = sys.argv[1:3]
G = {1: json.load(open(os.path.join(HERE, "guide1.json"), encoding="utf-8")),
     2: json.load(open(os.path.join(HERE, "guide2.json"), encoding="utf-8"))}
z = zipfile.ZipFile(SRC)
files = {n: z.read(n) for n in z.namelist()}
sec = files["Contents/section0.xml"].decode("utf-8")
P = top_paras(sec)
head_xml, tail_xml = sec[:sec.index(P[0])], sec[sec.rindex(P[-1]) + len(P[-1]):]
esc = lambda t: html.escape(t, quote=False)
txt = lambda p: html.unescape(re.sub(r"<[^>]+>", "", p))


# ---------------------------------------------------------------- 다듬기(공통사항)
def fix_text(p):
    def f(m):
        t = m.group(1)
        t = t.replace("CMStroy", "CMStory").replace("공통수학1. 2", "공통수학1, 2").replace("1. 2교시", "1, 2교시")
        return "<hp:t>%s</hp:t>" % t
    return re.sub(r"<hp:t>([^<]*)</hp:t>", f, p)


P = [fix_text(p) for p in P]
# 줄바꿈 개체와 같은 <hp:t> 안에 있는 글자도 고침(글자 노드만)
def fix_nodes(p):
    def f(m):
        t = m.group(1)
        t = t.replace("CMStroy", "CMStory").replace("공통수학1. 2", "공통수학1, 2").replace("1. 2교시", "1, 2교시")
        t = t.replace("대표문제와 단원마무리의 일부 문제를 선별하였습니다.",
                      "대표문제와, 유형서(CMStory)에 쌍둥이·같은 틀 문제가 있는 문제(단원 마무리 포함)를 선별하였습니다.")
        return ">" + t + "<"
    return re.sub(r">([^<>]+)<", f, p)


P = [fix_nodes(p) for p in P]
# 3) 수업구조와 4) 사이 빈 문단 5개 → 1개
i3 = next(i for i, p in enumerate(P) if "월/화" in txt(p))
i4 = next(i for i, p in enumerate(P) if txt(p).strip().startswith("4)"))
blanks = [i for i in range(i3 + 1, i4) if not txt(P[i]).strip() and "<hp:pic" not in P[i] and "<hp:tbl" not in P[i]]
P = [p for i, p in enumerate(P) if i not in blanks[1:]]


# ---------------------------------------------------------------- 사용자 표 다듬기(쉼표, 이어 풀기 번호순)
def norm_link(t):
    t = t.strip()
    m = re.match(r"이어 풀기:\s*(.*)$", t)
    if m:
        ns = sorted(re.findall(r"\d{3}", m.group(1)))
        return "이어 풀기: " + ", ".join(ns)
    parts = []
    for seg in re.split(r",\s*(?=\d{3}[^,]*?(?:쌍둥이|같은 틀|같은 문제))", t):
        mm = re.match(r"^([\d,\s]+?)\s*(쌍둥이|같은 틀|같은 문제.*)$", seg.strip())
        if mm:
            parts.append(", ".join(re.findall(r"\d{3}", mm.group(1))) + " " + mm.group(2))
        else:
            parts.append(seg.strip())
    return ", ".join(parts)


def fix_table(p):
    def tc(m):
        c = m.group(0)
        if 'colAddr="3"' in c and 'rowAddr="0"' not in c:
            c = re.sub(r"<hp:t>([^<]*)</hp:t>", lambda q: "<hp:t>%s</hp:t>" % esc(norm_link(html.unescape(q.group(1)))), c, count=1)
        return c
    return re.sub(r"<hp:tc .*?</hp:tc>", tc, p, flags=re.S)


i4 = next(i for i, p in enumerate(P) if txt(p).strip().startswith("4)"))
_legend = re.sub(r"<hp:t>.*?</hp:t>", "", P[i4], flags=re.S)
_legend = re.sub(r"(<hp:run [^>]*>)", r"\1<hp:t>§</hp:t>", _legend, count=1)
_legend = _legend.replace("<hp:t>§</hp:t>", "<hp:t>※ 표 보는 법: 쌍둥이 = 숫자만 바꾸거나 거의 같은 문제, 같은 틀 = 조건·묻는 방식은 같고 식만 다른 문제, "
                          "이어 풀기 = 쌍둥이가 없는 대표문제와 가장 닮은 유형서 문항(과제용). 유형서 번호는 Core와 Lite가 같습니다.</hp:t>", 1)
_legend = re.sub(r'(<hp:p id=")\d+"', r'\g<1>3989999999"', _legend, count=1)
_legend = re.sub(r"<hp:linesegarray>.*?</hp:linesegarray>", "", _legend, flags=re.S)
P = P[:i4 + 1] + [_legend] + P[i4 + 1:]
tbl_idx = [i for i, p in enumerate(P) if "<hp:tbl" in p]
for i in tbl_idx:
    P[i] = fix_table(P[i])

# ---------------------------------------------------------------- 견본
T1 = P[tbl_idx[0]]                                           # 1단원 표 문단
tbl = re.search(r"<hp:tbl .*?</hp:tbl>", T1, re.S).group(0)
trs = re.findall(r"<hp:tr>.*?</hp:tr>", tbl, re.S)
HEADER_TR = trs[0]
U1 = G[1][0]["must"]
rows_n = [int(txt(re.findall(r"<hp:tc .*?</hp:tc>", tr, re.S)[0]).strip()) for tr in trs[1:]]
rep_of = {m["n"]: m["rep"] for m in U1}
REP_TR = trs[1 + next(k for k, n in enumerate(rows_n) if rep_of.get(n))]
NON_TR = trs[1 + next(k for k, n in enumerate(rows_n) if not rep_of.get(n))]
i_h2 = next(i for i, p in enumerate(P) if re.match(r"2\. ", txt(p).strip()))   # 2단원 제목(쪽 나눔)
H_PARA, B_PARA, T_PARA, A_PARA = P[i_h2], P[i_h2 + 1], P[i_h2 + 2], P[i_h2 + 3]
NID = [3990000000]


def nid():
    NID[0] += 1
    return str(NID[0])


def set_ids(x):
    x = re.sub(r'(<hp:p id=")\d+"', lambda m: m.group(1) + nid() + '"', x)
    x = re.sub(r"<hp:linesegarray>.*?</hp:linesegarray>", "", x, flags=re.S)
    return x


def heading(text, page_break=True):
    h = re.sub(r"<hp:t>[^<]*</hp:t>", "<hp:t></hp:t>", H_PARA)
    h = h.replace("<hp:t></hp:t>", "<hp:t>%s</hp:t>" % esc(text), 1)
    h = re.sub(r"<hp:t></hp:t>", "", h)
    h = re.sub(r'pageBreak="\d"', 'pageBreak="%d"' % (1 if page_break else 0), h, count=1)
    return set_ids(h)


def row_xml(tpl, r, cells):
    tr = tpl
    tcs = re.findall(r"<hp:tc .*?</hp:tc>", tr, re.S)
    out = []
    for c, (tc, val) in enumerate(zip(tcs, cells)):
        tc = re.sub(r"<hp:t>[^<]*</hp:t>|<hp:t/>", "§", tc)
        tc = tc.replace("§", "<hp:t>%s</hp:t>" % esc(val), 1).replace("§", "")
        tc = re.sub(r'rowAddr="\d+"', 'rowAddr="%d"' % r, tc)
        out.append(tc)
    return "<hp:tr>" + "".join(out) + "</hp:tr>"


def link_text(m):
    if m["twins"]:
        groups = {}
        for t in m["twins"]:
            groups.setdefault(t["kind"], []).append(t["n"])
        gl = sorted(groups.items(), key=lambda kv: min(kv[1]))
        return ", ".join(", ".join("%03d" % n for n in sorted(ns)) + " " + k for k, ns in gl)
    if m.get("follow"):
        return "이어 풀기: " + ", ".join("%03d" % f["n"] for f in sorted(m["follow"], key=lambda f: f["n"]))
    return "-"


def reason(m):
    if m["rep"]:
        return "대표문제"
    kinds = sorted(set(t["kind"] for t in m["twins"]), key=["같은 문제", "쌍둥이", "같은 틀"].index)
    return "유형서 " + kinds[0] if kinds else "-"


def tname(t):
    return "단원 마무리" if not t else "%02d %s" % (t[0], t[1])


def table_para(must):
    rows = [HEADER_TR]
    for k, m in enumerate(must, 1):
        rows.append(row_xml(REP_TR if m["rep"] else NON_TR, k, ["%03d" % m["n"], tname(m["type"]), reason(m), link_text(m)]))
    t = re.sub(r"<hp:tr>.*</hp:tr>", lambda _: "".join(rows), tbl, count=1, flags=re.S)
    t = re.sub(r'rowCnt="\d+"', 'rowCnt="%d"' % len(rows), t, count=1)
    t = re.sub(r'(<hp:sz width="\d+" widthRelTo="ABSOLUTE" height=")\d+', lambda q: q.group(1) + str(1500 * len(rows) + 670), t, count=1)
    t = re.sub(r'(<hp:tbl [^>]*?\bid=")\d+', lambda q: q.group(1) + nid(), t, count=1)
    para = T_PARA.replace(re.search(r"<hp:tbl .*?</hp:tbl>", T_PARA, re.S).group(0), t)
    return set_ids(para)


def unit_block(u, first_page_break=True):
    return [heading("%d. %s   (기본서 %03d~%03d · 유형서 %03d~%03d)" % (u["unit"], u["name"], u["b_range"][0], u["b_range"][1], u["y_range"][0], u["y_range"][1]), first_page_break),
            set_ids(B_PARA), table_para(u["must"]), set_ids(A_PARA)]


# ---------------------------------------------------------------- 이어 붙이기
last_tbl = tbl_idx[-1]
end = last_tbl + 2 if last_tbl + 1 < len(P) else last_tbl + 1    # 2단원 표 뒤 빈 문단까지 사용자 것
new = P[:end]
for u in G[1][2:]:
    new += unit_block(u)
new.append(heading("공통수학2  (기본서 CLIMATH ⓜ 공통수학2 · 유형서 CMStory 공통수학2)"))
new.append(set_ids(B_PARA))
for k, u in enumerate(G[2]):
    new += unit_block(u, first_page_break=(k > 0))
sec_new = head_xml + "".join(new) + tail_xml
files["Contents/section0.xml"] = sec_new.encode("utf-8")
with zipfile.ZipFile(OUT, "w") as w:
    for n in z.namelist():
        info = zipfile.ZipInfo(n, date_time=(1980, 1, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_STORED if n == "mimetype" else zipfile.ZIP_DEFLATED
        w.writestr(info, files[n])
print("공통수학1 단원", len(G[1]), "공통수학2 단원", len(G[2]), "표", sec_new.count("<hp:tbl "), "->", OUT)
