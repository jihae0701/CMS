# -*- coding: utf-8 -*-
"""빠른 정답 파일 만들기 (2026-11-16 사용자 '기본서와 유형서 올린거 빠른 정답 파일을 만드는데, 각각 맞는 문서form에다가 만들어,
공통수학1, 2 기본서 유형서 총 4개의 파일로').
python quickans.py <책: c1b|c1y|c2b|c2y|c1l|c2l> <출력.hwpx>   (c1l·c2l: CMS 스토리 라이트, 틀은 라이트 1단원 파일)
- 정답은 단원 파일(완성본)의 미주 첫 줄('󰂼' 또는 '[정답]' 뒤)을 그대로 옮긴다. 수식은 수식 개체를 그대로 복사한다.
- 문항 번호는 미주 번호(미주 번호 매기기 시작값 + 차례)다.
- 틀(문서 form)은 그 책의 1단원 파일: 쪽 크기·여백·2단·바탕쪽(머리말 띠·쪽 번호)·글꼴·글자/문단 모양을 그대로 쓰고,
  바탕쪽의 단원 이름 자리에는 '빠른 정답'을 쓴다. 본문은 단원마다 '단원 이름' 줄과 표(번호 줄·정답 줄이 번갈아, 한 줄에 3문항 — 2026-11-18 사용자 요청으로 4 → 3). 칸보다 넓은 수식은 글자 크기를 줄여 칸에 맞춘다.
"""
import sys, os, re, zipfile, glob, html

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BOOKS = {
    "c1b": ("공통수학1 기본서", os.path.join(ROOT, "기본서"), r"^(\d+)\. (.+)\.hwpx$"),
    "c1y": ("공통수학1 유형서", os.path.join(ROOT, "공통수학1"), r"^(\d\d)_(.+)\.hwpx$"),
    "c2b": ("공통수학2 기본서", os.path.join(ROOT, "공통수학2", "기본서"), r"^(\d+)\. (.+)\.hwpx$"),
    "c2y": ("공통수학2 유형서", os.path.join(ROOT, "공통수학2", "유형서"), r"^(\d\d)_(.+)\.hwpx$"),
    "c1l": ("공통수학1 유형서 라이트", os.path.join(ROOT, "스토리라이트", "공통수학1"), r"^(\d\d)_(.+)\.hwpx$"),
    "c2l": ("공통수학2 유형서 라이트", os.path.join(ROOT, "스토리라이트", "공통수학2"), r"^(\d\d)_(.+)\.hwpx$"),
}
FALLBACK = {"c1l": "c1y", "c2l": "c2y"}   # 라이트를 아직 만들지 않은 단원(공통수학2 7·8단원)은 유형서와 같으므로 유형서 파일에서 읽는다
book, out = sys.argv[1:3]
TITLE, DIR, PAT = BOOKS[book]
units = []
for f in sorted(os.listdir(DIR)):
    m = re.match(PAT, f)
    if m and "교체후보" not in f and "추가" not in f and not re.search(r"_\d+(_\d+)?번", f):
        units.append((int(m.group(1)), m.group(2).replace("_", " "), os.path.join(DIR, f)))
if book in FALLBACK:
    have = {u[0] for u in units}
    _, D2, P2 = BOOKS[FALLBACK[book]]
    for f in sorted(os.listdir(D2)):
        m = re.match(P2, f)
        if m and int(m.group(1)) not in have and "추가" not in f and "교체후보" not in f and not re.search(r"_\d+(_\d+)?번", f):
            units.append((int(m.group(1)), m.group(2).replace("_", " "), os.path.join(D2, f)))
            print("라이트 없음 → 유형서에서:", f)
units.sort()
assert [u[0] for u in units] == list(range(1, 13)), [u[0] for u in units]
NAME_FIX = {"이차함수의 최대 최소": "이차함수의 최대, 최소"}

# ---------------------------------------------------------------- 정답 읽기
EQ = re.compile(r"<hp:equation\b.*?</hp:equation>", re.S)


def answers(path):
    x = zipfile.ZipFile(path).read("Contents/section0.xml").decode("utf-8")
    ctl = re.findall(r'<hp:newNum num="(\d+)" numType="ENDNOTE"', x)
    ep = re.search(r"<hp:endNotePr>.*?newNum=\"(\d+)\".*?</hp:endNotePr>", x, re.S)
    st = int(ctl[0]) if ctl else int(ep.group(1))
    res = []
    for k, en in enumerate(re.findall(r"<hp:endNote .*?</hp:endNote>", x, re.S)):
        p = re.search(r"<hp:p\b.*?</hp:p>", en, re.S).group(0)
        p = p[p.index("</hp:ctrl>") + len("</hp:ctrl>"):] if "</hp:ctrl>" in p else p
        p = re.sub(r"<hp:linesegarray>.*?</hp:linesegarray>", "", p, flags=re.S)
        toks = []
        for m in re.finditer(r"<hp:t>(.*?)</hp:t>|<hp:t/>|(<hp:equation\b.*?</hp:equation>)|<hp:lineBreak/>", p, re.S):
            if m.group(0) == "<hp:lineBreak/>":
                if any(k_ == "t" and ("󰂼" in v or "[정답]" in v) for k_, v in toks):
                    break                   # 정답 줄 뒤에 줄바꿈으로 풀이가 이어진 경우
                continue
            if m.group(2):
                toks.append(("eq", m.group(2)))
            elif m.group(1):
                tv = m.group(1)
                before = tv.split("<hp:lineBreak/>")[0]
                if "<hp:lineBreak/>" in tv and (any(k_ == "t" and ("󰂼" in v or "[정답]" in v) for k_, v in toks) or "󰂼" in before or "[정답]" in before):
                    toks.append(("t", re.sub(r"<[^>]+>", "", tv.split("<hp:lineBreak/>")[0])))
                    break                   # 정답 뒤 줄바꿈부터는 풀이
                toks.append(("t", re.sub(r"<[^>]+>", "", tv)))
        # 표시('󰂼', '[정답]') 앞까지 버린다
        s = "".join(v if k_ == "t" else "\x00" for k_, v in toks)
        txt = [v for k_, v in toks]
        out_t, started = [], False
        for k_, v in toks:
            if not started:
                if k_ == "t" and ("󰂼" in v or "[정답]" in v):
                    v = re.split(r"󰂼|\[정답\]", v, maxsplit=1)[1]
                    started = True
                    if v.strip():
                        out_t.append(("t", v.strip()))
                continue
            out_t.append((k_, v))
        out_t = [t for t in out_t if not (t[0] == "t" and not t[1].strip())]
        if out_t and out_t[0][0] == "t":            # 앞뒤 빈칸만 지우고, 글자와 수식 사이 빈칸은 그대로(사용자 편집본)
            out_t[0] = ("t", out_t[0][1].lstrip())
        if out_t and out_t[-1][0] == "t":
            out_t[-1] = ("t", out_t[-1][1].rstrip())
        res.append((st + k, out_t))
    return res


data = []
for no, name, path in units:
    a = answers(path)
    data.append((no, NAME_FIX.get(name, name), a))
for (n1, _, a1), (n2, _, a2) in zip(data, data[1:]):
    assert a1[-1][0] + 1 == a2[0][0], ("번호가 이어지지 않음", n1, a1[-1][0], n2, a2[0][0])
for no, name, a in data:
    for n, t in a:
        if not t:
            print("정답 없음:", no, n)

# ---------------------------------------------------------------- 틀
TPL = units[0][2]
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


# 2026-11-18 사용자 편집본(공통수학1 기본서 빠른 정답) 모양으로 통일:
#  번호 칸 연분홍(#F4DEEE)·회색 0.12 mm 선, 번호 글자 13pt 굵게 #800000(HY울릉도M), 정답 칸 왼쪽·오른쪽 검은 0.2 mm·위아래 회색 0.12 mm(마지막 줄 아래는 검은 0.2 mm),
#  정답 글자 10pt 나눔명조 검정, 정답 수식 10pt, 표 바깥 검은 0.2 mm·표 위 여백 566, 단원 줄 13pt 굵게 검정(HY울릉도M),
#  제목 줄 없이 단원마다 새 단에서 시작(단 나누기), 정답 안 글자와 수식 사이 띄어쓰기 그대로.
GRAY, BLACK = ("0.12 mm", "#7F8C99"), ("0.2 mm", "#000000")


def bfill(x, l, r, t, b, fill=None):
    for side, (w_, c_) in (("left", l), ("right", r), ("top", t), ("bottom", b)):
        x = re.sub(r'<hh:%sBorder type="[A-Z_]+" width="[^"]+" color="[^"]+"/>' % side,
                   '<hh:%sBorder type="SOLID" width="%s" color="%s"/>' % (side, w_, c_), x)
    x = re.sub(r"<hc:fillBrush>.*?</hc:fillBrush>", "", x, flags=re.S)
    if fill:
        x = x.replace("</hh:borderFill>", '<hc:fillBrush><hc:winBrush faceColor="%s" hatchColor="#000000" alpha="0"/></hc:fillBrush></hh:borderFill>' % fill)
    return x


FONTS = {}
for lang in ("HANGUL", "LATIN", "HANJA", "JAPANESE", "OTHER", "SYMBOL", "USER"):
    ff = re.search(r'<hh:fontface lang="%s".*?</hh:fontface>' % lang, head, re.S).group(0)
    FONTS[lang.lower()] = {n: i for i, n in re.findall(r'<hh:font id="(\d+)" face="([^"]+)"', ff)}


def fontref(names):
    for nm in names:
        if all(nm in FONTS[l] for l in FONTS):
            return '<hh:fontRef %s/>' % " ".join('%s="%s"' % (l, FONTS[l][nm]) for l in ("hangul", "latin", "hanja", "japanese", "other", "symbol", "user"))
    return None


def cpr(x, height, color, bold, fonts):
    x = re.sub(r'height="\d+"', 'height="%d"' % height, x, count=1)
    x = re.sub(r'textColor="[^"]+"', 'textColor="%s"' % color, x, count=1)
    x = x.replace("<hh:bold/>", "").replace("<hh:italic/>", "")
    if bold:
        x = x.replace("<hh:underline", "<hh:bold/><hh:underline", 1)
    fr = fontref(fonts)
    if fr:
        x = re.sub(r"<hh:fontRef [^>]*/>", fr, x, count=1)
    return x


TITLE_FONTS = ["HY울릉도M", "나눔스퀘어 ExtraBold", "나눔스퀘어 Bold"]      # HY울릉도M이 없는 틀(공통수학2 유형서)은 나눔스퀘어
head, BF_NUM = add_item(head, "borderFill", "borderFills", "1", lambda x: bfill(x, GRAY, GRAY, GRAY, GRAY, "#F4DEEE"))
head, BF_NUM0 = add_item(head, "borderFill", "borderFills", "1", lambda x: bfill(x, GRAY, GRAY, GRAY, GRAY))
head, BF_ANS = add_item(head, "borderFill", "borderFills", "1", lambda x: bfill(x, BLACK, BLACK, GRAY, GRAY))
head, BF_ANSL = add_item(head, "borderFill", "borderFills", "1", lambda x: bfill(x, BLACK, BLACK, GRAY, BLACK))
head, BF_TBL = add_item(head, "borderFill", "borderFills", "1", lambda x: bfill(x, BLACK, BLACK, BLACK, BLACK))
head, PP_C = add_item(head, "paraPr", "paraProperties", "0",
                      lambda x: re.sub(r'(<hh:lineSpacing type="PERCENT" value=")\d+', r'\g<1>130', x.replace('horizontal="JUSTIFY"', 'horizontal="CENTER"')))
head, PP_L = add_item(head, "paraPr", "paraProperties", "0", lambda x: re.sub(r'(<hh:lineSpacing type="PERCENT" value=")\d+', r'\g<1>150', x))
head, CP_N = add_item(head, "charPr", "charProperties", "0", lambda x: cpr(x, 1300, "#800000", True, TITLE_FONTS))
head, CP_A = add_item(head, "charPr", "charProperties", "0", lambda x: cpr(x, 1000, "#000000", False, ["나눔명조"]))
head, CP_U = add_item(head, "charPr", "charProperties", "0", lambda x: cpr(x, 1300, "#000000", True, TITLE_FONTS))
files["Contents/header.xml"] = head.encode("utf-8")

# 바탕쪽: 단원 번호·이름 자리에 '빠른 정답'
unit_name = units[0][1]
for n in list(files):
    if re.match(r"Contents/masterpage\d+\.xml", n):
        mx = files[n].decode("utf-8")
        mx = mx.replace("<hp:t>%s</hp:t>" % unit_name, "<hp:t>빠른 정답</hp:t>").replace("<hp:t>1.</hp:t>", "<hp:t></hp:t>")
        files[n] = mx.encode("utf-8")

sec = files["Contents/section0.xml"].decode("utf-8")
i0 = sec.index("<hp:p ")
p0 = sec[i0:sec.index("</hp:p>", i0) + 7]
run0 = re.match(r"<hp:p [^>]*><hp:run [^>]*>", p0).group(0)
keep = re.search(r"<hp:secPr\b.*?</hp:secPr>", p0, re.S).group(0)
keep += "".join(m.group(0) for m in re.finditer(r"<hp:ctrl>(?:(?!</hp:ctrl>).)*?<hp:(?:colPr|footer|header|pageNum)\b.*?</hp:ctrl>", p0, re.S))
first = sec[:i0] + run0 + keep + "<hp:t/></hp:run></hp:p>"
NID = [3100000000]


def nid():
    NID[0] += 1
    return str(NID[0])


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


EQID = [3200000000]


def eqfix(e):
    EQID[0] += 1
    e = re.sub(r'(<hp:equation\b[^>]*?\bid=")\d+', lambda m: m.group(1) + str(EQID[0]), e, count=1)
    bu = int(re.search(r'baseUnit="(\d+)"', e).group(1))
    if bu != 1000:                                  # 정답 수식은 10pt로(사용자 편집본)
        k0 = 1000 / bu
        e = re.sub(r'baseUnit="\d+"', 'baseUnit="1000"', e, count=1)
        e = re.sub(r'<hp:sz width="(\d+)" widthRelTo="ABSOLUTE" height="(\d+)"',
                   lambda q: '<hp:sz width="%d" widthRelTo="ABSOLUTE" height="%d"' % (int(int(q.group(1)) * k0), int(int(q.group(2)) * k0)), e, count=1)
    m = re.search(r'<hp:sz width="(\d+)" widthRelTo="ABSOLUTE" height="(\d+)"', e)
    avail = W // NCOL - 450
    if m and int(m.group(1)) > avail:              # 칸보다 넓은 수식은 글자 크기를 줄여 칸에 맞춘다
        k = avail / int(m.group(1))
        e = re.sub(r'<hp:sz width="\d+" widthRelTo="ABSOLUTE" height="\d+"',
                   '<hp:sz width="%d" widthRelTo="ABSOLUTE" height="%d"' % (avail, int(int(m.group(2)) * k)), e, count=1)
        e = re.sub(r'baseUnit="(\d+)"', lambda q: 'baseUnit="%d"' % int(int(q.group(1)) * k), e, count=1)
    return e


def runs(tokens, cp):
    out = []
    for k, v in tokens:
        out.append(eqfix(v) if k == "eq" else "<hp:t>%s</hp:t>" % esc(v))
    return '<hp:run charPrIDRef="%d">%s<hp:t/></hp:run>' % (cp, "".join(out))


def para(inner, pp, cp=None):
    if cp is not None:
        inner = '<hp:run charPrIDRef="%d">%s</hp:run>' % (cp, "<hp:t>%s</hp:t>" % esc(inner) if inner else "<hp:t/>")
    return '<hp:p id="%s" paraPrIDRef="%d" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0">%s</hp:p>' % (nid(), pp, inner)


def cell(r, c, inner, w, h, bf):
    return ('<hp:tc name="" header="0" hasMargin="0" protect="0" editable="0" dirty="0" borderFillIDRef="%d">'
            '<hp:subList id="" textDirection="HORIZONTAL" lineWrap="BREAK" vertAlign="CENTER" linkListIDRef="0" linkListNextIDRef="0" textWidth="0" textHeight="0" hasTextRef="0" hasNumRef="0">'
            '%s</hp:subList><hp:cellAddr colAddr="%d" rowAddr="%d"/><hp:cellSpan colSpan="1" rowSpan="1"/>'
            '<hp:cellSz width="%d" height="%d"/><hp:cellMargin left="141" right="141" top="141" bottom="141"/></hp:tc>'
            % (bf, inner, c, r, w, h))


NCOL = 3
W = 29000
CW = W // NCOL


def table(items):
    trs, r = [], 0
    nrow = (len(items) + NCOL - 1) // NCOL
    for k in range(0, len(items), NCOL):
        chunk = items[k:k + NCOL]
        while len(chunk) < NCOL:
            chunk.append(None)
        last = (k // NCOL == nrow - 1)
        tr1 = "".join(cell(r, c, para("%03d" % it[0] if it else "", PP_C, CP_N), CW, 1300, BF_NUM if it else BF_NUM0) for c, it in enumerate(chunk))
        tr2 = "".join(cell(r + 1, c, para(runs(it[1], CP_A) if it else '<hp:run charPrIDRef="%d"><hp:t/></hp:run>' % CP_A, PP_C), CW, 1800,
                           (BF_TBL if not it else (BF_ANSL if last else BF_ANS))) for c, it in enumerate(chunk))
        trs += ["<hp:tr>%s</hp:tr>" % tr1, "<hp:tr>%s</hp:tr>" % tr2]
        r += 2
    tbl = ('<hp:tbl id="%s" zOrder="0" numberingType="TABLE" textWrap="TOP_AND_BOTTOM" textFlow="BOTH_SIDES" lock="0" dropcapstyle="None" pageBreak="CELL" repeatHeader="0" rowCnt="%d" colCnt="%d" cellSpacing="0" borderFillIDRef="%d" noAdjust="0">'
           '<hp:sz width="%d" widthRelTo="ABSOLUTE" height="%d" heightRelTo="ABSOLUTE" protect="0"/>'
           '<hp:pos treatAsChar="1" affectLSpacing="0" flowWithText="1" allowOverlap="0" holdAnchorAndSO="0" vertRelTo="PARA" horzRelTo="PARA" vertAlign="TOP" horzAlign="LEFT" vertOffset="0" horzOffset="0"/>'
           '<hp:outMargin left="0" right="0" top="566" bottom="0"/><hp:inMargin left="141" right="141" top="141" bottom="141"/>%s</hp:tbl>'
           % (nid(), r, NCOL, BF_TBL, CW * NCOL, (1300 + 1800) * (r // 2), "".join(trs)))
    return para('<hp:run charPrIDRef="%d">%s<hp:t/></hp:run>' % (CP_A, tbl), PP_C)


body = []
total = 0
for k, (no, name, a) in enumerate(data):
    u = "%d. %s  (%03d~%03d)" % (no, name, a[0][0], a[-1][0])
    if k == 0:                                   # 첫 단원 줄은 구역 정의가 든 첫 문단에(사용자 편집본처럼 제목 줄 없음)
        first = first.replace("<hp:t/></hp:run></hp:p>", '</hp:run><hp:run charPrIDRef="%d"><hp:t>%s</hp:t></hp:run></hp:p>' % (CP_U, esc(u)), 1)
        first = re.sub(r'(<hp:p [^>]*paraPrIDRef=")\d+', lambda m: m.group(1) + str(PP_L), first, count=1)
    else:                                        # 단원마다 새 단에서 시작
        body.append(para(u, PP_L, CP_U).replace('columnBreak="0"', 'columnBreak="1"', 1))
    body.append(table(a))
    total += len(a)
files["Contents/section0.xml"] = (first + "".join(body) + "</hs:sec>").encode("utf-8")
if "Preview/PrvText.txt" in files:
    files["Preview/PrvText.txt"] = ("%s 빠른 정답" % TITLE).encode("utf-8")
# 쓰지 않는 그림은 빼지 않는다(바탕쪽이 쓰는 그림이 있을 수 있음)
with zipfile.ZipFile(out, "w") as w:
    for n in z.namelist():
        info = zipfile.ZipInfo(n, date_time=(1980, 1, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_STORED if n == "mimetype" else zipfile.ZIP_DEFLATED
        w.writestr(info, files[n])
print(TITLE, "단원", len(data), "문항", total, "(%03d~%03d)" % (data[0][2][0][0], data[-1][2][-1][0]), "->", out)
