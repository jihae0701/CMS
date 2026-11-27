# -*- coding: utf-8 -*-
"""CLIMATH(m) 대수 단원 — CLIMATH(c) 대수 서식·개념·유형 분류로 만들기 (2026-11-24).
python build_c.py <단원 번호> <출력.hwpx>
- 틀: CLIMATH_c/대수/<단원>.hwpx (CLIMATH(c) 대수 완성본). 표지·STEP 상자·개념 상자(개념 정리 글 포함)·유형 상자·바탕쪽·끝 쪽을 그대로 쓰고,
  문항만 바꿔 넣음. 문항 번호는 틀의 문단 번호(머리 번호)가 매김.
- 문항 자료: CLIMATH_m/대수/문항/cNN.py — STEP1[개념별 목록], STEP2[유형별 목록(+NEW_TYPES 추가 유형)], STEP3[목록].
  · no=N  : 올림포스 고난도 대수(자료/고난도/0K_*.hwpx, 단원 kd_unit) N번 — 문제·수식·그림·해설을 옮김(객관식은 mc=True만 남기고 단답형으로).
  · on/src + q·choices·ans·sol : 글로 쓴 문항(유형ON·내신 변형·모의고사) — 수식은 $…$.
- 미주: 틀과 같이 ' [정답] 답' + 풀이 문단(문단 1·글자 25).
"""
import sys, os, re, zipfile, html, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
from kd import load as kd_load, en_paras, plain
sys.path.insert(0, os.path.join(HERE, "..", "guide"))
from extract import top_paras

UNIT, OUT = int(sys.argv[1]), sys.argv[2]
spec = importlib.util.spec_from_file_location("c", os.path.join(ROOT, "CLIMATH_m", "대수", "문항", "c%02d.py" % UNIT))
U = importlib.util.module_from_spec(spec)
spec.loader.exec_module(U)
TPL = os.path.join(ROOT, "CLIMATH_c", "대수", U.TEMPLATE)
KD_UNIT = getattr(U, "KD_UNIT", 1)

tz = zipfile.ZipFile(TPL)
files = {n: tz.read(n) for n in tz.namelist()}
names = list(tz.namelist())
ts = files["Contents/section0.xml"].decode("utf-8")
TP = top_paras(ts)
HEAD, TAIL_XML = ts[:ts.index(TP[0])], ts[ts.rindex(TP[-1]) + len(TP[-1]):]


def is_box(p):
    return "<hp:rect" in p or "<hp:container" in p


def box_text(p):
    return plain(p).strip()


EN_IDX = [i for i, p in enumerate(TP) if "<hp:endNote " in p]
I_STEP1 = next(i for i, p in enumerate(TP) if is_box(p) and box_text(p).startswith("개념 익히기"))
I_STEP2 = next(i for i, p in enumerate(TP) if is_box(p) and box_text(p).startswith("유형별 학습하기"))
I_STEP3 = next(i for i, p in enumerate(TP) if is_box(p) and box_text(p).startswith("단원 마무리"))
CONCEPTS = [i for i, p in enumerate(TP[:I_STEP2]) if i > I_STEP1 and is_box(p) and re.match(r"^\d\d", box_text(p)) and "개념" in box_text(p)[:60]]
TYPES = [i for i, p in enumerate(TP) if I_STEP2 < i < I_STEP3 and is_box(p) and re.match(r"^\d\d", box_text(p))]
LAST_EN = EN_IDX[-1]
I_TAIL = next(i for i in range(LAST_EN + 1, len(TP)) if 'pageBreak="1"' in TP[i][:250] or 'columnBreak="1"' in TP[i][:250] or is_box(TP[i]))
EN_HEAD = re.search(r"<hp:endNote [^>]*>", ts).group(0)
SUBLIST = re.search(r"<hp:endNote [^>]*>(<hp:subList [^>]*>)", ts).group(1)
AUTONUM = re.search(r"<hp:ctrl><hp:autoNum [^>]*numType=\"ENDNOTE\">.*?</hp:ctrl>", ts, re.S).group(0)
assert len(CONCEPTS) == len(U.STEP1), (len(CONCEPTS), len(U.STEP1))


# ---------------------------------------------------------------- 틀마다 다른 문단·글자 모양 번호 읽기 (2026-11-25)
# CLIMATH(c) 대수 단원 파일은 단원마다 머리(header)의 모양 번호가 다름(1단원: 문항 번호 문단 69·글자 60·문제 26/63, 2단원: 80·57·17/89 …).
# 예전에는 1단원 번호를 그대로 써서 2단원 문서의 번호 문단(자동 번호)·문제 글꼴이 틀렸음 → 틀의 문항에서 역할별 번호를 읽어 씀.
from collections import Counter as _C


def _pp(p):
    return re.match(r'<hp:p [^>]*paraPrIDRef="(\d+)"', p).group(1)


def _roles():
    R = {}
    for name, (lo, hi) in (("1", (I_STEP1, I_STEP2)), ("2", (I_STEP2, len(TP)))):
        e = [i for i in EN_IDX if lo < i < hi]
        R["en" + name] = _C(_pp(TP[i]) for i in e).most_common(1)[0][0]
        q, ch, dan, qcp = _C(), _C(), _C(), _C()
        for i in e:
            j = i + 1
            while j < len(TP) and not plain(TP[j]).strip() and "<hp:pic" not in TP[j]:
                j += 1
            if j < len(TP):
                q[_pp(TP[j])] += 1
                qcp.update(re.findall(r'<hp:run charPrIDRef="(\d+)"><hp:t>', TP[j]))
            for k in range(i + 1, min(i + 40, len(TP))):
                if "<hp:endNote " in TP[k] or is_box(TP[k]):
                    break
                t = plain(TP[k]).strip()
                if t.startswith("①"):
                    ch[_pp(TP[k])] += 1
                elif t.startswith("(단"):
                    dan[_pp(TP[k])] += 1
        R["q" + name] = q.most_common(1)[0][0]
        R["ch" + name] = (ch.most_common(1) or [(R["q" + name],)])[0][0]
        R["dan" + name] = (dan.most_common(1) or [(None,)])[0][0]
        R["qcp" + name] = qcp.most_common(1)[0][0]
    R["encp"] = _C(m for i in EN_IDX for m in re.findall(r'<hp:run charPrIDRef="(\d+)"><hp:ctrl><hp:endNote', TP[i])).most_common(1)[0][0]
    R["qcp"] = R["qcp1"]
    hd = files["Contents/header.xml"].decode("utf-8")
    R["center"] = next(m.group(1) for m in re.finditer(r'<hh:paraPr id="(\d+)" .*?</hh:paraPr>', hd, re.S)
                       if 'horizontal="CENTER"' in m.group(0) and 'heading type="NONE"' in m.group(0)
                       and re.search(r'<hc:left value="0"', m.group(0)) and re.search(r'<hc:intent value="0"', m.group(0)))
    R["dan"] = R["dan2"] or R["dan1"]
    return R


R = _roles()
R.update(getattr(U, "ROLE_OVERRIDE", {}))                    # 단원 자료에서 고정할 때(1단원: 사용자가 본 판과 같게)
STEP_NOW = [1]
print("틀 모양 번호:", R)

CNT = {"eq": 2100000000, "pic": 2200000000, "inst": 2300000000, "p": 2400000000, "en": 0, "bin": 0}
def nxt(k):
    CNT[k] += 1
    return CNT[k]
BIN = []


def renum(x, srcz=None, binmap=None):
    x = re.sub(r'(<hp:equation id=")\d+"', lambda m: m.group(1) + str(nxt("eq")) + '"', x)
    x = re.sub(r'(<hp:(?:pic|container|rect|polygon|line|ellipse|tbl) id=")(\d+)"', lambda m: m.group(1) + (str(nxt("pic")) if m.group(2) != "0" else "0") + '"', x)
    x = re.sub(r'(instid=")\d+"', lambda m: m.group(1) + str(nxt("inst")) + '"', x)
    if srcz is not None:
        def b(m):
            old = m.group(1)
            if old not in binmap:
                hpf = srcz.read("Contents/content.hpf").decode("utf-8")
                it = re.search(r'<opf:item id="%s" href="([^"]+)" media-type="([^"]+)"' % re.escape(old), hpf)
                ext = os.path.splitext(it.group(1))[1]
                new = "algc%d_%d" % (UNIT, nxt("bin"))
                BIN.append((new, "BinData/%s%s" % (new, ext), srcz.read(it.group(1)), it.group(2)))
                binmap[old] = new
            return 'binaryItemIDRef="%s"' % binmap[old]
        x = re.sub(r'binaryItemIDRef="([^"]+)"', b, x)
    return x


def clean(p):
    p = re.sub(r"<hp:linesegarray>.*?</hp:linesegarray>", "", p, flags=re.S)
    return renum(p)


# ---------------------------------------------------------------- 수식(글로 쓴 문항)
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
            out.append("<hp:t>%s</hp:t>" % html.escape(part, quote=False))
    return "".join(out)


# ---------------------------------------------------------------- 문단
def para(pp, cp, inner, style="2"):
    return ('<hp:p id="%d" paraPrIDRef="%s" styleIDRef="%s" pageBreak="0" columnBreak="0" merged="0"><hp:run charPrIDRef="%s">%s</hp:run></hp:p>'
            % (nxt("p"), pp, style, cp, inner or "<hp:t/>"))


def endnote(ans_xml, sol_xml):
    CNT["en"] += 1
    head = re.sub(r'number="\d+"', 'number="%d"' % CNT["en"], EN_HEAD, count=1)
    head = re.sub(r'instId="\d+"', 'instId="%d"' % (2500000000 + CNT["en"]), head, count=1)
    an = re.sub(r'num="\d+"', 'num="%d"' % CNT["en"], AUTONUM, count=1)
    first = ('<hp:p id="2147483648" paraPrIDRef="1" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0"><hp:run charPrIDRef="25">%s<hp:t> [정답] </hp:t>%s</hp:run></hp:p>' % (an, ans_xml))
    sols = "".join('<hp:p id="2147483648" paraPrIDRef="1" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0"><hp:run charPrIDRef="25">%s</hp:run></hp:p>' % (s or "<hp:t/>") for s in sol_xml)
    return head + SUBLIST + first + sols + "</hp:subList></hp:endNote>"


# ---------------------------------------------------------------- 모의고사 출처(CMStory처럼 번호 문단 오른쪽 끝, 예: 2025년 6월 고2 19번)
HDR = files["Contents/header.xml"].decode("utf-8")


def _add(kind, tag, xml_of_id):
    """header의 hh:<tag> 목록 끝에 하나 더(새 id), itemCnt 늘림"""
    global HDR
    m = re.search(r'<hh:%s itemCnt="(\d+)"' % kind, HDR)
    nid = int(m.group(1))
    HDR = HDR[:m.start()] + '<hh:%s itemCnt="%d"' % (kind, nid + 1) + HDR[m.end():]
    end = HDR.index("</hh:%s>" % kind)
    HDR = HDR[:end] + xml_of_id(nid) + HDR[end:]
    return str(nid)


SRC_TAB = _add("tabProperties", "tabPr", lambda i: '<hh:tabPr id="%d" autoTabLeft="0" autoTabRight="0"><hp:switch><hp:case hp:required-namespace="http://www.hancom.co.kr/hwpml/2016/HwpUnitChar"><hh:tabItem pos="29620" type="RIGHT" leader="NONE" unit="HWPUNIT"/></hp:case><hp:default><hh:tabItem pos="59240" type="RIGHT" leader="NONE"/></hp:default></hp:switch></hh:tabPr>' % i)
_p69 = re.search(r'<hh:paraPr id="%s" .*?</hh:paraPr>' % R["en2"], HDR, re.S).group(0)
SRC_PARA = _add("paraProperties", "paraPr", lambda i: re.sub(r'tabPrIDRef="\d+"', 'tabPrIDRef="%s"' % SRC_TAB, _p69.replace('id="%s"' % R["en2"], 'id="%d"' % i, 1), count=1))
_c1 = re.search(r'<hh:charPr id="%s" .*?</hh:charPr>' % R["qcp"], HDR, re.S).group(0)
SRC_CHAR = _add("charProperties", "charPr", lambda i: re.sub(r'textColor="#[0-9A-Fa-f]+"', 'textColor="#315F97"', _c1.replace('id="%s"' % R["qcp"], 'id="%d"' % i, 1).replace('height="1000"', 'height="900"', 1), count=1))


def en_para(en, src=None):
    if not src:
        return '<hp:p id="2147483648" paraPrIDRef="%s" styleIDRef="2" pageBreak="0" columnBreak="0" merged="0"><hp:run charPrIDRef="%s"><hp:ctrl>%s</hp:ctrl><hp:t/></hp:run></hp:p>' % (R["en%d" % min(STEP_NOW[0], 2)], R["encp"], en)
    tab = max(1000, 29620 - 3000 - 900 * len(src))
    return ('<hp:p id="2147483648" paraPrIDRef="%s" styleIDRef="2" pageBreak="0" columnBreak="0" merged="0"><hp:run charPrIDRef="%s"><hp:ctrl>%s</hp:ctrl></hp:run>'
            '<hp:run charPrIDRef="%s"><hp:t><hp:tab width="%d" leader="0" type="2"/></hp:t></hp:run><hp:run charPrIDRef="%s"><hp:t>%s</hp:t></hp:run></hp:p>'
            % (SRC_PARA, R["encp"], en, R["encp"], tab, SRC_CHAR, html.escape(src, quote=False)))


def q_para(qp, inner):
    t = re.sub(r"<[^>]+>", "", inner).strip()
    return para(R["dan"] if t.startswith("(단") and R["dan"] else qp, R["qcp"], inner)


# ---------------------------------------------------------------- 고난도 문항
TOK = re.compile(r"<hp:tbl .*?</hp:tbl>|<hp:pic .*?</hp:pic>|<hp:endNote .*?</hp:endNote>|<hp:equation .*?</hp:equation>|<hp:t>(.*?)</hp:t>|<hp:t/>", re.S)


def tokens(p):
    out = []
    for m in TOK.finditer(p):
        g = m.group(0)
        if g.startswith("<hp:tbl"): out.append(("tbl", g))
        elif g.startswith("<hp:pic"): out.append(("pic", g))
        elif g.startswith("<hp:endNote"): continue
        elif g.startswith("<hp:equation"): out.append(("eq", g))
        elif m.group(1) is not None:
            t = re.sub(r"<hp:(?!lineBreak|tab)[^>]*/?>", "", m.group(1))
            if t: out.append(("t", t))
    return out


def tbl_lines(tbl):
    rows = []
    for tc in re.findall(r"<hp:tc .*?</hp:tc>", tbl, re.S):
        sub = tc[tc.index("<hp:subList"):]
        for p in top_paras(sub[sub.index(">") + 1:]):
            tk = tokens(p)
            if any(k != "t" or v.strip() for k, v in tk):
                rows.append(tk)
    return rows


def xml_of(tk, z, binmap):
    return "".join("<hp:t>%s</hp:t>" % v if k == "t" else renum(v, z, binmap) for k, v in tk)


def batchim(ch):
    o = ord(ch) - 0xAC00
    return 0 <= o < 11172 and o % 28 != 0


FIXED = [("있는 대로 고른 것은?", "있는 대로 고르시오."), ("나타낸 것은?", "나타내시오."), ("간단히 한 것은?", "간단히 하시오."), ("구한 것은?", "구하시오.")]


def to_short(t):
    for a_, b_ in FIXED:
        if a_ in t:
            return t.replace(a_, b_, 1)
    m = re.search(r"(\S*?)(은|는)\?", t)
    if not m:
        return t
    w = m.group(1)
    return t[:m.start()] + w + ("을" if batchim(w[-1] if w else "것") else "를") + " 구하시오." + t[m.end():]


def choice_map(choice_paras):
    seq = []
    for p in choice_paras:
        seq += tokens(p)
    cur, res = None, {}
    for k, v in seq:
        if k == "t":
            for x in re.split(r"([①②③④⑤])", re.sub(r"<hp:tab[^>]*/>", " ", v)):
                if x and x in "①②③④⑤":
                    cur = "①②③④⑤".index(x) + 1; res[cur] = []
                elif cur and x.strip():
                    res[cur].append(("t", x.strip()))
        elif cur:
            res[cur].append((k, v))
    return res


SRC = {}


def kd_unit(u):
    if u not in SRC:
        d = os.path.join(ROOT, "CLIMATH_m", "대수", "자료", "고난도")
        path = os.path.join(d, next(f for f in os.listdir(d) if f.startswith("%02d_" % u) and f.endswith(".hwpx")))
        items, z = kd_load(path)
        SRC[u] = ({it["no"]: it for it in items}, z, {})
    return SRC[u]


def num_eq(tk):
    return [("eq", G["eq"](v.strip())) if k == "t" and re.fullmatch(r"\s*-?[\d.]+\s*", v) else (k, v) for k, v in tk]


def kd_problem(pr, qp, blanks):
    items, z, binmap = kd_unit(pr.get("unit", KD_UNIT))
    it = items[pr["no"]]
    stem = [[(k, v) for k, v in tokens(p) if not (k == "t" and v.strip() == "서술형 문제")] for p in it["paras"]]
    stem = [s for s in stem if s]
    enp = en_paras(it["en"])
    first = tokens(enp[0])
    ftxt = "".join(v for k, v in first if k == "t")
    m = re.search(r"\[정답\]\s*([①②③④⑤])", ftxt)
    mc = bool(it["choices"]) and pr.get("mc", False)
    if it["choices"] and not mc:
        done = False
        for s in reversed(stem):
            for j in range(len(s) - 1, -1, -1):
                if s[j][0] == "t" and "?" in s[j][1]:
                    s[j] = ("t", to_short(s[j][1])); done = True; break
            if done: break
        ans = choice_map(it["choices"])["①②③④⑤".index(m.group(1)) + 1]
    elif it["choices"]:
        ans = [("t", m.group(1))]
    else:
        ans, seen = [], False
        for k, v in first:
            if k == "t" and "[정답]" in v:
                seen = True; v = v.split("[정답]", 1)[1].strip()
                if v: ans.append(("t", v))
            elif seen:
                ans.append((k, v))
    ans = num_eq(ans)
    sols = []
    for p in enp[1:]:
        tk = tokens(p)
        if any(k == "tbl" for k, _ in tk):
            tb = next(v for k, v in tk if k == "tbl")
            if "채점" in plain(tb):
                continue
            sols += [xml_of(r, z, binmap) for r in tbl_lines(tb)]
            tk = [(k, v) for k, v in tk if k != "tbl"]
            if not any(k != "t" or v.strip() for k, v in tk):
                continue
        if all(k == "t" for k, _ in tk) and re.fullmatch(r"[…\.·\s]*[❶❷❸❹❺]\s*", "".join(v for _, v in tk)):
            continue
        sols.append(xml_of(tk, z, binmap))
    while sols and not re.search(r"<hp:t>[^<]*\S|<hp:equation|<hp:pic", sols[-1]):
        sols.pop()
    out = [en_para(endnote(xml_of(ans, z, binmap), sols))]
    for s in stem:
        cur = []
        def flush():
            if cur:
                out.append(q_para(qp, xml_of(cur, z, binmap))); cur.clear()
        for k, v in s:
            if k == "pic":
                flush(); out.append(para(R["center"], R["qcp"], renum(v, z, binmap)))
            elif k == "tbl":
                flush()
                for row in tbl_lines(v):
                    txt = html.unescape("".join(x for k2, x in row if k2 == "t")).replace(" ", "")
                    if txt in ("<보기>", "〈보기〉"):
                        out.append(para(R["center"], R["qcp"], "<hp:t>〈보기〉</hp:t>"))
                    else:
                        out.append(q_para(qp, xml_of(row, z, binmap)))
            else:
                cur.append((k, v))
        flush()
    if mc:
        for p in it["choices"]:
            out.append(para(R["ch%d" % min(STEP_NOW[0], 2)], R["qcp"], xml_of(tokens(p), z, binmap)))
    out += [para(qp, R["qcp"], "") for _ in range(blanks)]
    return out


def new_pic(png, W):
    """새로 그린 PNG를 그림 개체로(고난도 자료의 첫 그림 개체를 본뜸). 폭 W(HWPUNIT), 높이는 PNG 비율 — 그림 규칙 1픽셀=6.4"""
    from PIL import Image
    items, z, binmap = kd_unit(KD_UNIT)
    src = "".join(z.read(n).decode("utf-8") for n in z.namelist() if re.match(r"Contents/section\d+\.xml", n))
    p = re.search(r"<hp:pic\b.*?</hp:pic>", src, re.S).group(0)
    new = "algc%d_%d" % (UNIT, nxt("bin"))
    data = open(os.path.join(ROOT, png), "rb").read()
    BIN.append((new, "BinData/%s.png" % new, data, "image/png"))
    pw, ph = Image.open(os.path.join(ROOT, png)).size
    H = round(W * ph / pw)
    p = re.sub(r'binaryItemIDRef="[^"]+"', 'binaryItemIDRef="%s"' % new, p)
    p = re.sub(r'<hp:orgSz [^>]*/>', '<hp:orgSz width="%d" height="%d"/>' % (W, H), p)
    p = re.sub(r'<hp:curSz [^>]*/>', '<hp:curSz width="%d" height="%d"/>' % (W, H), p)
    p = re.sub(r'centerX="\d+" centerY="\d+"', 'centerX="%d" centerY="%d"' % (W // 2, H // 2), p)
    p = re.sub(r'<hc:scaMatrix [^>]*/>', '<hc:scaMatrix e1="1" e2="0" e3="0" e4="0" e5="1" e6="0"/>', p)
    p = re.sub(r'<hp:imgRect>.*?</hp:imgRect>', '<hp:imgRect><hc:pt0 x="0" y="0"/><hc:pt1 x="%d" y="0"/><hc:pt2 x="%d" y="%d"/><hc:pt3 x="0" y="%d"/></hp:imgRect>' % (W, W, H, H), p, flags=re.S)
    p = re.sub(r'<hp:imgClip [^>]*/>', '<hp:imgClip left="0" right="%d" top="0" bottom="%d"/>' % (W, H), p)
    p = re.sub(r'<hp:imgDim [^>]*/>', '<hp:imgDim dimwidth="%d" dimheight="%d"/>' % (W, H), p)
    p = re.sub(r'(<hp:sz width=")\d+(" widthRelTo="ABSOLUTE" height=")\d+(")', lambda q: q.group(1) + str(W) + q.group(2) + str(H) + q.group(3), p)
    return para(R["center"], R["qcp"], renum(p))


def text_problem(pr, qp, blanks):
    out = [en_para(endnote(runs_of(pr["ans"]), [runs_of(l) for l in pr["sol"]]), pr.get("mock") if isinstance(pr.get("mock"), str) else None)]
    for l in pr["q"]:
        out.append(q_para(qp, runs_of(l)))
    if pr.get("pic"):
        out.append(new_pic(*pr["pic"]))
    for l in pr.get("choices") or []:
        out.append(para(R["ch%d" % min(STEP_NOW[0], 2)], R["qcp"], runs_of(l)))
    out += [para(qp, R["qcp"], "") for _ in range(blanks)]
    return out


def problem(pr, qp, blanks):
    return kd_problem(pr, qp, blanks) if "no" in pr else text_problem(pr, qp, blanks)


# ---------------------------------------------------------------- 유형 상자(새 유형은 마지막 유형 상자 복제)
def type_box_new(no, name):
    b = TP[TYPES[-1]]
    ts_ = re.findall(r"<hp:t>[^<]*</hp:t>", b)
    b = b.replace(ts_[0], "<hp:t>%02d</hp:t>" % no, 1)
    # 이름은 둘째 글 조각부터 '유형' 앞까지 → 하나로
    names_ = [x for x in ts_[1:] if x != "<hp:t>유형</hp:t>"]
    b = b.replace(names_[0], "<hp:t>%s</hp:t>" % html.escape(name, quote=False), 1)
    for x in names_[1:]:
        b = b.replace(x, "<hp:t/>", 1)
    b = re.sub(r"<hp:equation .*?</hp:equation>", "", b, flags=re.S)
    return clean(b)


# ---------------------------------------------------------------- 조립
body = [clean(p) if i else p for i, p in enumerate(TP[:I_STEP1 + 1])]
n = 0
for k, probs in enumerate(U.STEP1):
    ci = CONCEPTS[k]
    first_en = next(i for i in EN_IDX if i > ci)
    body += [clean(p) for p in TP[ci:first_en] if not ("<hp:endNote " in p)]
    for pr in probs:
        STEP_NOW[0] = 1; body += problem(pr, R["q1"], 8); n += 1
body.append(clean(TP[I_STEP2]))
for k, probs in enumerate(U.STEP2):
    if k < len(TYPES):
        bx = clean(TP[TYPES[k]])
        t0 = re.search(r"<hp:t>(\d\d)</hp:t>", bx)               # 유형 번호를 차례대로(CLIMATH(c) 3단원 틀은 '실생활에의 활용'도 06이라 07로)
        if t0 and t0.group(1) != "%02d" % (k + 1):
            bx = bx.replace(t0.group(0), "<hp:t>%02d</hp:t>" % (k + 1), 1)
        body.append(bx)
    else:
        body.append(type_box_new(k + 1, U.NEW_TYPES[k + 1]))
    for pr in probs:
        STEP_NOW[0] = 2; body += problem(pr, R["q2"], 10); n += 1
body.append(clean(TP[I_STEP3]))
for pr in U.STEP3:
    STEP_NOW[0] = 3; body += problem(pr, R["q2"], 13); n += 1
body += [clean(p) for p in TP[I_TAIL:]]

files["Contents/header.xml"] = HDR.encode("utf-8")
# 바탕쪽의 'CLIMATH ⓒ' → 'ⓜ' (2026-11-25 사용자 '바탕쪽에 동그라미 c를 동그라미 m으로')
for _n in list(files):
    if re.match(r"Contents/masterpage\d+\.xml$", _n):
        files[_n] = files[_n].decode("utf-8").replace("<hp:t>ⓒ</hp:t>", "<hp:t>ⓜ</hp:t>").encode("utf-8")
        # 2026-11-26 사용자(1단원 수정본) '바탕쪽 각 페이지 아래 흰 사각형 모두 지웠어' → 흰 네모(4473×1866) 지움
        from drop_mp_whitebox import drop as _drop_wb
        files[_n] = _drop_wb(files[_n].decode("utf-8"))[0].encode("utf-8")
files["Contents/section0.xml"] = (HEAD + "".join(body) + TAIL_XML).encode("utf-8")
if BIN:
    hpf = files["Contents/content.hpf"].decode("utf-8")
    hpf = hpf.replace("</opf:manifest>", "".join('<opf:item id="%s" href="%s" media-type="%s" isEmbeded="1"/>' % (i, p, mt) for i, p, d, mt in BIN) + "</opf:manifest>", 1)
    files["Contents/content.hpf"] = hpf.encode("utf-8")
    for i, p, d, mt in BIN:
        files[p] = d; names.append(p)
with zipfile.ZipFile(OUT, "w") as w:
    for nm in names:
        info = zipfile.ZipInfo(nm, date_time=(1980, 1, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_STORED if nm == "mimetype" else zipfile.ZIP_DEFLATED
        w.writestr(info, files[nm])
# 다시 그린 그림으로 바꾸기(그림 규칙: PNG 1픽셀 = 6.4 HWPUNIT, 폭은 cNN.py의 PICS)
PICS = getattr(U, "PICS", {})
if PICS:
    import subprocess
    bm = kd_unit(KD_UNIT)[2]
    reps = ["%s=%s@%d" % (bm[k], os.path.join(ROOT, f), w) for k, (f, w) in PICS.items() if k in bm]
    if reps:
        subprocess.run([sys.executable, os.path.join(ROOT, "그림규칙", "math-figure-rules", "hwpx_swapimg.py"), OUT, OUT] + reps, check=True)
# 2026-11-26 사용자(1단원 수정본) '숫자·영문자 수식으로' → 글자 숫자·점 이름(대문자)을 수식으로, 집합 조건 막대 `|` → left |
from text2eq import convert_file as _t2e
_t2e_n = _t2e(OUT, OUT)
print("  글자 숫자·대문자 → 수식", _t2e_n)
# 2026-11-26 사용자 '미주 다음 줄에 문제 시작 → 모의고사 기출 빼고 미주 바로 옆에 문제 시작'
from num_inline import convert_file as _ni
print("  번호 줄에 첫 문제 문단 붙임", _ni(OUT, OUT))
# 2026-11-27 대수(c) 1단원 사용자 재편집본: 번호 글자 14pt·번호 폭 300, STEP 머리 상자 위 여백 0, 선택지 바로 앞 문단 아래 600
from layout_c1 import fix as _lay
print("  편집(번호 14pt 등)", _lay(OUT))
print("단원", UNIT, U.NAME, "문항", n, "(STEP1 %d, STEP2 %d, STEP3 %d)" % (sum(map(len, U.STEP1)), sum(map(len, U.STEP2)), len(U.STEP3)), "그림", len(BIN), "->", OUT)
