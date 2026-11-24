# -*- coding: utf-8 -*-
"""CLIMATH(m) 대수 단원 파일 만들기 (2026-11-24).
python build_unit.py <단원 번호> <출력.hwpx>
- 틀: CLIMATH ⓜ 공통수학1 기본서 1단원(기본서/1. 다항식의 연산과 항등식.hwpx) — 글꼴·문단 모양·STEP 상자·유형 상자·번호 꼴·미주 꼴을 그대로 씀.
- STEP1·2: 올림포스 고난도 대수 단원 HWPX(CLIMATH_m/대수/자료/고난도/)에서 고른 문항(CLIMATH_m/대수/문항/uNN.py의 STEP1·STEP2).
  문제 글·수식·그림과 풀이(미주)를 옮김. 객관식은 mc=True인 것만 남기고 단답형으로 바꿈(물음 끝 '…은?' → '…을 구하시오.', 정답 = 고른 번호의 선택지 값).
  풀이는 자료 그대로(첫 줄 '[정답] …'과 서술형 채점 기준 표만 뺌, 표는 글 줄로 바꿈).
- STEP3: uNN.py의 STEP3(내신 기출 숫자 변형, 모의고사 기출) — 글로 쓴 문제·풀이를 수식으로 만듦.
- 한 단에 1문항(번호 문단 단 나누기), 개념 묶음마다 유형 상자(번호·이름·'개념'/'유형').
"""
import sys, os, re, zipfile, html, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, ".."))
from kd import load as kd_load, en_paras, plain
sys.path.insert(0, os.path.join(HERE, "..", "guide"))
from extract import top_paras

UNIT, OUT = int(sys.argv[1]), sys.argv[2]
TPL = os.path.join(ROOT, "기본서", "1. 다항식의 연산과 항등식.hwpx")
spec = importlib.util.spec_from_file_location("u", os.path.join(ROOT, "CLIMATH_m", "대수", "문항", "u%02d.py" % UNIT))
U = importlib.util.module_from_spec(spec)
spec.loader.exec_module(U)

# ---------------------------------------------------------------- 틀
tz = zipfile.ZipFile(TPL)
files = {n: tz.read(n) for n in tz.namelist()}
names = list(tz.namelist())
ts = files["Contents/section0.xml"].decode("utf-8")
TP = top_paras(ts)
HEAD, TAIL = ts[:ts.index(TP[0])], ts[ts.rindex(TP[-1]) + len(TP[-1]):]
def tpl_find(pred):
    return next(p for p in TP if pred(p))
def ptxt(p):
    return "".join(re.findall(r"<hp:t>([^<]*)</hp:t>", p))
STEP1_BOX = TP[0]                                                         # secPr + 'STEP 1' 상자
STEP2_BOX = tpl_find(lambda p: "유형별 학습하기" in ptxt(p) and "<hp:rect" in p)
STEP3_BOX = tpl_find(lambda p: "단원 마무리" in ptxt(p))
TYPE_BOX = tpl_find(lambda p: re.findall(r"<hp:t>([^<]*)</hp:t>", p)[-1:] == ["유형"] and "<hp:rect" in p)
EN_HEAD = re.search(r"<hp:endNote [^>]*>", ts).group(0)
SUBLIST = re.search(r"<hp:endNote [^>]*>(<hp:subList [^>]*>)", ts).group(1)
AUTONUM = re.search(r"<hp:ctrl><hp:autoNum [^>]*numType=\"ENDNOTE\">.*?</hp:ctrl>", ts, re.S).group(0)

# ---------------------------------------------------------------- id
CNT = {"eq": 2100000000, "pic": 2200000000, "inst": 2300000000, "p": 2400000000, "en": 0, "bin": 0}
def nxt(k):
    CNT[k] += 1
    return CNT[k]
BIN = []                                                                 # (새 이름, 데이터, media-type)


def renum(x, srcz=None, binmap=None):
    """복사한 수식·그림·도형의 id 새로 매김, 그림은 BinData 옮김"""
    x = re.sub(r'(<hp:equation id=")\d+"', lambda m: m.group(1) + str(nxt("eq")) + '"', x)
    x = re.sub(r'(<hp:(?:pic|container|rect|polygon|line|ellipse) id=")(\d+)"', lambda m: m.group(1) + (str(nxt("pic")) if m.group(2) != "0" else "0") + '"', x)
    x = re.sub(r'(instid=")\d+"', lambda m: m.group(1) + str(nxt("inst")) + '"', x)
    if srcz is not None:
        def b(m):
            old = m.group(1)
            if old not in binmap:
                hpf = srcz.read("Contents/content.hpf").decode("utf-8")
                it = re.search(r'<opf:item id="%s" href="([^"]+)" media-type="([^"]+)"' % re.escape(old), hpf)
                ext = os.path.splitext(it.group(1))[1]
                new = "alg%d_%d" % (UNIT, nxt("bin"))
                BIN.append((new, "BinData/%s%s" % (new, ext), srcz.read(it.group(1)), it.group(2)))
                binmap[old] = new
            return 'binaryItemIDRef="%s"' % binmap[old]
        x = re.sub(r'binaryItemIDRef="([^"]+)"', b, x)
    return x


# ---------------------------------------------------------------- 원본 문단 → 조각
TOK = re.compile(r"<hp:tbl .*?</hp:tbl>|<hp:pic .*?</hp:pic>|<hp:endNote .*?</hp:endNote>|<hp:equation .*?</hp:equation>"
                 r"|<hp:t>(.*?)</hp:t>|<hp:t/>", re.S)


def tokens(p):
    out = []
    for m in TOK.finditer(p):
        g = m.group(0)
        if g.startswith("<hp:tbl"):
            out.append(("tbl", g))
        elif g.startswith("<hp:pic"):
            out.append(("pic", g))
        elif g.startswith("<hp:endNote"):
            continue
        elif g.startswith("<hp:equation"):
            out.append(("eq", g))
        elif m.group(1) is not None:
            t = re.sub(r"<hp:(?!lineBreak|tab)[^>]*/?>", "", m.group(1))     # 글 속 제어 꼬리표 정리(줄바꿈·탭은 둠)
            if t:
                out.append(("t", t))
    return out


def tbl_lines(tbl):
    """표 → 줄 목록(칸 안 문단마다 한 줄)"""
    rows = []
    for tc in re.findall(r"<hp:tc .*?</hp:tc>", tbl, re.S):
        sub = tc[tc.index("<hp:subList"):]
        for p in top_paras(sub[sub.index(">") + 1:]):
            tk = tokens(p)
            if any(k != "t" or v.strip() for k, v in tk):
                rows.append(tk)
    return rows


def xml_of(tk, srcz, binmap):
    out = []
    for k, v in tk:
        if k == "t":
            out.append("<hp:t>%s</hp:t>" % v)
        else:
            out.append(renum(v, srcz, binmap))
    return "".join(out)


def para(pp, cp, inner, style="0", col=False, page=False):
    return ('<hp:p id="%d" paraPrIDRef="%s" styleIDRef="%s" pageBreak="%d" columnBreak="%d" merged="0"><hp:run charPrIDRef="%s">%s</hp:run></hp:p>'
            % (nxt("p"), pp, style, 1 if page else 0, 1 if col else 0, cp, inner or "<hp:t/>"))


# ---------------------------------------------------------------- 물음 바꾸기(객관식 → 단답형)
def batchim(ch):
    o = ord(ch) - 0xAC00
    return 0 <= o < 11172 and o % 28 != 0


FIXED = [("있는 대로 고른 것은?", "있는 대로 고르시오."), ("나타낸 것은?", "나타내시오."), ("간단히 한 것은?", "간단히 하시오."),
         ("구한 것은?", "구하시오.")]


def to_short(t):
    for a, b in FIXED:
        if a in t:
            return t.replace(a, b, 1)
    m = re.search(r"(\S*?)(은|는)\?", t)
    if not m:
        return t
    w = m.group(1)
    last = w[-1] if w else "것"
    obj = "을" if batchim(last) else "를"
    return t[:m.start()] + w + obj + " 구하시오." + t[m.end():]


def convert_stem(stem_tks):
    """마지막 '?' 든 글 조각을 바꿈"""
    for i in range(len(stem_tks) - 1, -1, -1):
        for j in range(len(stem_tks[i]) - 1, -1, -1):
            k, v = stem_tks[i][j]
            if k == "t" and "?" in v:
                stem_tks[i][j] = ("t", to_short(v))
                return stem_tks
    raise ValueError("물음 끝 '?'가 없음")


def choice_map(choice_paras):
    """선택지 문단 → {번호: 조각}"""
    seq = []
    for p in choice_paras:
        seq += tokens(p)
    cur, res = None, {}
    for k, v in seq:
        if k == "t":
            parts = re.split(r"([①②③④⑤])", re.sub(r"<hp:tab[^>]*/>", " ", v))
            for x in parts:
                if x in "①②③④⑤" and x:
                    cur = "①②③④⑤".index(x) + 1
                    res[cur] = []
                elif cur and x.strip():
                    res[cur].append(("t", x.strip()))
        elif cur:
            res[cur].append((k, v))
    return res


# ---------------------------------------------------------------- 미주
def endnote(ans_xml, sol_paras_xml):
    CNT["en"] += 1
    head = re.sub(r'number="\d+"', 'number="%d"' % CNT["en"], EN_HEAD, count=1)
    head = re.sub(r'instId="\d+"', 'instId="%d"' % (2500000000 + CNT["en"]), head, count=1)
    an = re.sub(r'num="\d+"', 'num="%d"' % CNT["en"], AUTONUM, count=1)
    first = ('<hp:p id="2147483648" paraPrIDRef="34" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0"><hp:run charPrIDRef="18">%s<hp:t> 󰂼 </hp:t>%s</hp:run></hp:p>'
             % (an, ans_xml))
    return head + SUBLIST + first + "".join(sol_paras_xml) + "</hp:subList></hp:endNote>"


def sol_para(inner):
    return ('<hp:p id="2147483648" paraPrIDRef="34" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0"><hp:run charPrIDRef="18">%s</hp:run></hp:p>'
            % (inner or "<hp:t/>"))


# ---------------------------------------------------------------- 상자·번호
def type_box(no, name, word, col=True):
    b = TYPE_BOX
    ts_ = re.findall(r"<hp:t>[^<]*</hp:t>", b)
    b = b.replace(ts_[0], "<hp:t>%02d</hp:t>" % no, 1)
    b = b.replace(ts_[1], "<hp:t>%s</hp:t>" % html.escape(name, quote=False), 1)
    b = b.replace(ts_[2], "<hp:t>%s</hp:t>" % word, 1)
    b = re.sub(r'pageBreak="\d" columnBreak="\d"', 'pageBreak="0" columnBreak="%d"' % (1 if col else 0), b, count=1)
    b = re.sub(r"<hp:linesegarray>.*?</hp:linesegarray>", "", b, flags=re.S)
    return renum(b)


def num_para(n, col):
    s = "%03d" % n
    d = str(n)
    lead = s[:len(s) - len(d)]
    inner = ('<hp:run charPrIDRef="39"><hp:t>%s</hp:t></hp:run>' % lead if lead else "") + '<hp:run charPrIDRef="46"><hp:t>%s</hp:t></hp:run>' % d
    return '<hp:p id="%d" paraPrIDRef="29" styleIDRef="0" pageBreak="0" columnBreak="%d" merged="0">%s</hp:p>' % (nxt("p"), 1 if col else 0, inner)


def box(b, page):
    b = re.sub(r"<hp:linesegarray>.*?</hp:linesegarray>", "", b, flags=re.S)
    b = re.sub(r'pageBreak="\d"', 'pageBreak="%d"' % (1 if page else 0), b, count=1)
    return renum(b)


# ---------------------------------------------------------------- 고난도 문항 → 문단
SRC = {}


def kd_unit(u):
    if u not in SRC:
        path = [os.path.join(ROOT, "CLIMATH_m", "대수", "자료", "고난도", f) for f in os.listdir(os.path.join(ROOT, "CLIMATH_m", "대수", "자료", "고난도"))
                if f.startswith("%02d_" % u) and f.endswith(".hwpx")][0]
        items, z = kd_load(path)
        SRC[u] = ({it["no"]: it for it in items}, z, {})
    return SRC[u]


def kd_problem(spec, num, pp, col):
    items, z, binmap = kd_unit(spec.get("unit", UNIT))
    it = items[spec["no"]]
    stem = [tokens(p) for p in it["paras"]]
    stem = [[(k, v) for k, v in s if not (k == "t" and v.strip() in ("서술형 문제",))] for s in stem]
    stem = [s for s in stem if s]
    # 정답
    enp = en_paras(it["en"])
    first = tokens(enp[0])
    ftxt = "".join(v for k, v in first if k == "t")
    m = re.search(r"\[정답\]\s*([①②③④⑤])", ftxt)
    mc = bool(it["choices"]) and spec.get("mc", False)
    if it["choices"] and not mc:
        stem = convert_stem(stem)
        ans_tk = choice_map(it["choices"])["①②③④⑤".index(m.group(1)) + 1]
    elif it["choices"]:
        ans_tk = [("t", m.group(1))]
    else:
        ans_tk = []
        seen = False
        for k, v in first:
            if k == "t" and "[정답]" in v:
                seen = True
                v = v.split("[정답]", 1)[1].strip()
                if v:
                    ans_tk.append(("t", v))
            elif seen:
                ans_tk.append((k, v))
    if spec.get("ans"):
        ans_tk = [("t", spec["ans"])]
    ans_tk = [("eq", G["eq"](v.strip())) if k == "t" and re.fullmatch(r"\s*-?[\d.]+\s*", v) else (k, v) for k, v in ans_tk]   # 숫자 정답은 수식으로
    # 풀이
    sols = []
    for p in enp[1:]:
        tk = tokens(p)
        if any(k == "tbl" for k, _ in tk):
            tb = next(v for k, v in tk if k == "tbl")
            if "채점" in plain(tb):
                continue
            for row in tbl_lines(tb):
                sols.append(sol_para(xml_of(row, z, binmap)))
            tk = [(k, v) for k, v in tk if k != "tbl"]
            if not any(k != "t" or v.strip() for k, v in tk):
                continue
        if all(k == "t" for k, _ in tk) and re.fullmatch(r"[…\.·\s]*[❶❷❸❹❺]\s*", "".join(v for _, v in tk)):
            continue                                                   # 서술형 단계 표시 줄(채점 표를 뺐으므로)
        sols.append(sol_para(xml_of(tk, z, binmap)))
    while sols and sols[-1].endswith("<hp:t/></hp:run></hp:p>") and "<hp:equation" not in sols[-1] and re.search(r"<hp:t>[^<]*\S", sols[-1]) is None:
        sols.pop()
    en = endnote(xml_of(ans_tk, z, binmap), sols)
    # 문제 문단(표는 줄로, 그림은 가운데 문단)
    out = [num_para(num, col)]
    first_done = False
    for s in stem:
        chunks, cur = [], []
        for k, v in s:
            if k in ("tbl", "pic"):
                if cur:
                    chunks.append(("p", cur)); cur = []
                chunks.append((k, v))
            else:
                cur.append((k, v))
        if cur:
            chunks.append(("p", cur))
        for kind, v in chunks:
            if kind == "p":
                inner = xml_of(v, z, binmap)
                if not first_done:
                    inner += "<hp:ctrl>%s</hp:ctrl><hp:t/>" % en
                    first_done = True
                out.append(para(pp, "59", inner, style="16"))
            elif kind == "pic":
                out.append(para("3", "59", renum(v, z, binmap)))
            else:
                rows = tbl_lines(v)
                for row in rows:
                    txt = html.unescape("".join(x for k2, x in row if k2 == "t")).strip()
                    if txt.replace(" ", "") in ("<보기>", "〈보기〉", "<보 기>"):
                        out.append(para("3", "59", "<hp:t>〈보기〉</hp:t>"))
                    else:
                        out.append(para(pp, "59", xml_of(row, z, binmap), style="16"))
    if not first_done:
        raise ValueError("문제 글이 없음 %s" % spec)
    if mc:
        for p in it["choices"]:
            out.append(para("48", "59", xml_of(tokens(p), z, binmap), style="17"))
    return out


# ---------------------------------------------------------------- 글로 쓴 문항(STEP3) → 문단
EQ_SRC = open(os.path.join(ROOT, "도구", "m1w_build.py"), encoding="utf-8").read()
a, b = EQ_SRC.index("EQ_TPL = ("), EQ_SRC.index("# ---------------------------------------------------------------- 틀")
G = {"re": re, "html": html}
exec(EQ_SRC[a:b], G)
G["EQID"][0] = 2600000000


def runs_of(text):
    out = []
    for k, part in enumerate(re.split(r"\$", text)):
        if k % 2:
            if part.strip():
                out.append(G["eq"](part))
        elif part:
            out.append("<hp:t>%s</hp:t>" % html.escape(part, quote=False).replace("\n", "<hp:lineBreak/>"))
    return "".join(out)


def text_problem(pr, num, pp, col):
    en = endnote(runs_of(pr["ans"]), [sol_para(runs_of(l)) for l in pr["sol"]])
    out = [num_para(num, col)]
    lines = pr["q"] if isinstance(pr["q"], list) else [pr["q"]]
    for i, l in enumerate(lines):
        inner = runs_of(l)
        if i == 0:
            inner += "<hp:ctrl>%s</hp:ctrl><hp:t/>" % en
        out.append(para(pp, "59", inner, style="16"))
    if pr.get("choices"):
        out.append(para("48", "59", runs_of(pr["choices"]), style="17"))
    return out


# ---------------------------------------------------------------- 조립
body = []
n = U.START
def add_groups(groups, word, pp):
    global n
    for gi, (gname, probs) in enumerate(groups, 1):
        body.append(type_box(gi, gname, word, col=gi > 1))           # STEP 상자 바로 뒤 첫 묶음은 같은 단
        for k, pr in enumerate(probs):
            col = k > 0
            if "no" in pr:
                body.extend(kd_problem(pr, n, pp, col))
            else:
                body.extend(text_problem(pr, n, pp, col))
            n += 1

body.append(STEP1_BOX if True else "")
add_groups(U.STEP1, "개념", "35")
body.append(box(STEP2_BOX, True))
add_groups(U.STEP2, "유형", "35")
if getattr(U, "STEP3", None):
    body.append(box(STEP3_BOX, True))
    for k, pr in enumerate(U.STEP3):
        body.extend(text_problem(pr, n, "53", k > 0) if "no" not in pr else kd_problem(pr, n, "53", k > 0))
        n += 1

sec = HEAD + "".join(body) + TAIL
files["Contents/section0.xml"] = sec.encode("utf-8")
# 바탕쪽: 단원 이름·과목
for mp in ("Contents/masterpage0.xml", "Contents/masterpage1.xml"):
    s = files[mp].decode("utf-8")
    s = s.replace("<hp:t>1.</hp:t>", "<hp:t>%d.</hp:t>" % UNIT, 1).replace("<hp:t>다항식의 연산과 항등식</hp:t>", "<hp:t>%s</hp:t>" % U.NAME, 1)
    s = s.replace("<hp:t>공통수학1</hp:t>", "<hp:t>대수</hp:t>")
    s = re.sub(r"<hp:t>공통수학</hp:t>(.*?)<hp:t>1</hp:t>", r"<hp:t>대수</hp:t>\1<hp:t/>", s, count=1, flags=re.S)
    files[mp] = s.encode("utf-8")
if BIN:
    hpf = files["Contents/content.hpf"].decode("utf-8")
    hpf = hpf.replace("</opf:manifest>", "".join('<opf:item id="%s" href="%s" media-type="%s" isEmbeded="1"/>' % (i, p, mt) for i, p, d, mt in BIN) + "</opf:manifest>", 1)
    files["Contents/content.hpf"] = hpf.encode("utf-8")
    for i, p, d, mt in BIN:
        files[p] = d
        names.append(p)
files["Preview/PrvText.txt"] = ("CLIMATH(m) 대수 %d. %s" % (UNIT, U.NAME)).encode("utf-8")
with zipfile.ZipFile(OUT, "w") as w:
    for nm in names:
        info = zipfile.ZipInfo(nm, date_time=(1980, 1, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_STORED if nm == "mimetype" else zipfile.ZIP_DEFLATED
        w.writestr(info, files[nm])
print("단원", UNIT, U.NAME, "문항", n - U.START, "(%03d~%03d)" % (U.START, n - 1), "그림", len(BIN), "->", OUT)
