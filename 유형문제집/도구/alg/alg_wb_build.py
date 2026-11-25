# -*- coding: utf-8 -*-
"""CLIMATH(m) 대수 워크북(한글 HWPX) 만들기 (2026-11-25).
python alg_wb_build.py <출력.hwpx> [단원 번호 …]   (빼면 문항 파일이 있는 단원 모두)
- 사용자: '지수 로그 워크북 만들자. 유형 골고루, 본책 STEP1 난도 느낌(좀 더 어려워도 됨), 본책의 모의고사 기출문제는 숫자 변형으로 반드시 넣기,
  단원별 문제 수 20~25', 서식 = CLIMATH(c) 워크북 서식, 내신 기출은 원문 그대로(모의고사만 숫자 변형).
- 문항: CLIMATH_m/대수/워크북/문항/wNN.py — STEP1, STEP2 (각각 dict(src, q=[줄…], choices=[줄…], ans, sol=[줄…], pic=(PNG, 폭))). 글 속 $…$는 한글 수식.
- 틀: CLIMATH(c) 공통수학1 워크북 HWPX(쪽·2단·바탕쪽·글자/문단 모양, STEP 1·STEP 2 상자). 구역 = 단원, 바탕쪽은 1단원 것을 복사해 ⓒ→ⓜ, 과목 '대수', 단원 이름.
  STEP 상자 없음(2026-11-25 사용자), 문제 문단(35, 번호 = 미주 번호, 단원을 넘어 이어짐), 둘째 줄부터(조건·보기) 34, 선택지 68, 그림 34, 풀이 공간 빈 줄(34) 14줄.
  미주: ' 정답 답'(글자 44) + 풀이(문단 5·글자 45, '$='로 시작하는 줄은 54).
"""
import sys, os, re, zipfile, html, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "도구", "guide"))
from extract import top_paras

TPL = os.path.join(ROOT, "CLIMATH_c", "공통수학1_워크북", "CLIMATH(c)_공통수학1_워크북.hwpx")
QDIR = os.path.join(ROOT, "CLIMATH_m", "대수", "워크북", "문항")
UNITS = ["지수", "로그", "지수함수", "로그함수", "삼각함수", "삼각함수의 그래프", "삼각함수의 활용", "등차수열과 등비수열", "수열의 합", "수학적 귀납법"]
OUT = sys.argv[1]
SEL = [int(a) for a in sys.argv[2:]] or [u for u in range(1, 11) if os.path.exists(os.path.join(QDIR, "w%02d.py" % u))]
BLANK = 14

EQ_SRC = open(os.path.join(ROOT, "도구", "m1w_build.py"), encoding="utf-8").read()
a, b = EQ_SRC.index("EQ_TPL = ("), EQ_SRC.index("# ---------------------------------------------------------------- 틀")
G = {"re": re, "html": html}
exec(EQ_SRC[a:b], G)
G["EQID"][0] = 2700000000
runs_of = G["runs_of"]


def load(u):
    spec = importlib.util.spec_from_file_location("w%02d" % u, os.path.join(QDIR, "w%02d.py" % u))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


z = zipfile.ZipFile(TPL)
files = {n: z.read(n) for n in z.namelist()}
NAMES = list(z.namelist())
NU = len(SEL)
drop = [n for n in NAMES if (re.match(r"Contents/section(\d+)\.xml$", n) and int(re.search(r"\d+", n).group(0)) >= NU)
        or (re.match(r"Contents/masterpage(\d+)\.xml$", n) and int(re.search(r"\d+", n).group(0)) >= 2 * NU)]
for n in drop:
    del files[n]
NAMES = [n for n in NAMES if n not in drop]
hpf = files["Contents/content.hpf"].decode("utf-8")
for n in drop:
    iid = os.path.basename(n)[:-4]
    hpf = re.sub(r'<opf:item id="%s" [^>]*/>' % iid, "", hpf)
    hpf = re.sub(r'<opf:itemref idref="%s" [^>]*/>' % iid, "", hpf)
files["Contents/content.hpf"] = hpf.encode("utf-8")
head = files["Contents/header.xml"].decode("utf-8")
files["Contents/header.xml"] = re.sub(r'secCnt="\d+"', 'secCnt="%d"' % NU, head, count=1).encode("utf-8")
files["Preview/PrvText.txt"] = "CLIMATH(m) 대수 워크북".encode("utf-8")

mp0, mp1 = files["Contents/masterpage0.xml"].decode("utf-8"), files["Contents/masterpage1.xml"].decode("utf-8")
mp0 = re.sub(r'(<hp:p [^>]*paraPrIDRef=")135("[^>]*>(?:(?!<hp:p ).)*?<hp:t>다항식의 연산</hp:t>)', r"\g<1>134\2", mp0, count=1, flags=re.S)
for j, u in enumerate(SEL):
    title = "%d. %s" % (u, UNITS[u - 1])
    for k, src in ((0, mp0), (1, mp1)):
        m = src.replace("<hp:t>ⓒ</hp:t>", "<hp:t>ⓜ</hp:t>")
        m = m.replace("<hp:t>다항식의 연산</hp:t>", "<hp:t>%s</hp:t>" % html.escape(title)).replace("<hp:t>1. 다항식의 연산</hp:t>", "<hp:t>%s</hp:t>" % html.escape(title))
        m = m.replace("<hp:t>공통수학1</hp:t>", "<hp:t>대수</hp:t>")
        m = re.sub(r"<hp:t>공통수학</hp:t>(.*?)<hp:t>1</hp:t>", r"<hp:t>대수</hp:t>\1<hp:t/>", m, count=1, flags=re.S)
        m = re.sub(r'(<masterPage [^>]*\bid=")masterpage\d+"', r'\g<1>masterpage%d"' % (2 * j + k), m, count=1)
        if j:
            m = re.sub(r'(\s(?:id|instid)=")(\d{6,})"', lambda q: '%s%d"' % (q.group(1), int(q.group(2)) + 7919 * j), m)
        files["Contents/masterpage%d.xml" % (2 * j + k)] = m.encode("utf-8")

sec0 = files["Contents/section0.xml"].decode("utf-8")
P0 = top_paras(sec0)
head_xml = sec0[:sec0.index("<hp:p ")]
first = re.sub(r"<hp:linesegarray>.*?</hp:linesegarray>", "", P0[0])                          # 구역 정의(+ STEP 1 상자)
# 2026-11-25 사용자 'STEP 1, 2 박스는 없애 줘' → 구역 첫 문단의 상자와 글자를 빼고, STEP 2 상자는 넣지 않음(문항 순서는 STEP1 → STEP2 그대로)
first = re.sub(r"<hp:rect\b.*?</hp:rect>", "", first, flags=re.S)
first = re.sub(r"<hp:t>[^<]*</hp:t>", "<hp:t/>", first)
step2 = re.sub(r"<hp:linesegarray>.*?</hp:linesegarray>", "", next(p for p in P0 if "<hp:rect" in p and "STEP 2" in re.sub(r"<[^>]+>", "", p)))
en_open = re.search(r"<hp:endNote [^>]*><hp:subList [^>]*>", sec0).group(0)
autonum = re.search(r'<hp:ctrl><hp:autoNum num="\d+" numType="ENDNOTE">.*?</hp:ctrl>', sec0, re.S).group(0)
NID = [3800000000]
NEWBIN = []


def nid():
    NID[0] += 1
    return str(NID[0])


def para(pp, inner, cp="26"):
    return '<hp:p id="%s" paraPrIDRef="%s" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0"><hp:run charPrIDRef="%s">%s</hp:run></hp:p>' % (
        nid(), pp, cp, inner or "<hp:t/>")


PIC_TPL = ('<hp:pic id="%d" zOrder="0" numberingType="PICTURE" textWrap="TOP_AND_BOTTOM" textFlow="BOTH_SIDES" lock="0" dropcapstyle="None" href="" groupLevel="0" instid="%d" reverse="0">'
           '<hp:offset x="0" y="0"/><hp:orgSz width="%d" height="%d"/><hp:curSz width="%d" height="%d"/><hp:flip horizontal="0" vertical="0"/>'
           '<hp:rotationInfo angle="0" centerX="%d" centerY="%d" rotateimage="0"/><hp:renderingInfo><hc:transMatrix e1="1" e2="0" e3="0" e4="0" e5="1" e6="0"/>'
           '<hc:scaMatrix e1="1" e2="0" e3="0" e4="0" e5="1" e6="0"/><hc:rotMatrix e1="1" e2="0" e3="0" e4="0" e5="1" e6="0"/></hp:renderingInfo>'
           '<hc:img binaryItemIDRef="%s" bright="0" contrast="0" effect="REAL_PIC" alpha="0"/><hp:imgRect><hc:pt0 x="0" y="0"/><hc:pt1 x="%d" y="0"/>'
           '<hc:pt2 x="%d" y="%d"/><hc:pt3 x="0" y="%d"/></hp:imgRect><hp:imgClip left="0" right="%d" top="0" bottom="%d"/><hp:inMargin left="0" right="0" top="0" bottom="0"/>'
           '<hp:imgDim dimwidth="%d" dimheight="%d"/><hp:effects/><hp:sz width="%d" widthRelTo="ABSOLUTE" height="%d" heightRelTo="ABSOLUTE" protect="0"/>'
           '<hp:pos treatAsChar="1" affectLSpacing="0" flowWithText="1" allowOverlap="0" holdAnchorAndSO="0" vertRelTo="PARA" horzRelTo="PARA" vertAlign="TOP" horzAlign="LEFT" vertOffset="0" horzOffset="0"/>'
           '<hp:outMargin left="0" right="0" top="0" bottom="0"/><hp:shapeComment>그림입니다.</hp:shapeComment></hp:pic>')


def pic_para(png, W):
    """새로 그린 그림(PNG) — 그림 규칙: 문서 폭 W(HWPUNIT), 높이는 PNG 비율(1픽셀 = 6.4 HWPUNIT 약속은 W를 정할 때 지킴)"""
    from PIL import Image
    path = os.path.join(ROOT, png)
    pw, ph = Image.open(path).size
    H = int(W * ph / pw)
    k = len(NEWBIN) + 1
    iid = "algwb%d" % k
    NEWBIN.append(("BinData/%s.png" % iid, open(path, "rb").read(), iid, "image/png"))
    pic = PIC_TPL % (3900000000 + k, 3910000000 + k, W, H, W, H, W // 2, H // 2, iid, W, W, H, H, pw * 75, ph * 75, pw * 75, ph * 75, W, H)
    return para("34", pic + "<hp:t/>")


ENO = [0]


def endnote(ans, sol):
    ENO[0] += 1
    ps = ['<hp:p id="2147483648" paraPrIDRef="5" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0"><hp:run charPrIDRef="44">%s<hp:t> 정답 </hp:t>%s</hp:run></hp:p>'
          % (re.sub(r'num="\d+"', 'num="%d"' % ENO[0], autonum, count=1), runs_of(ans))]
    for line in sol:
        pp = "54" if line.lstrip().startswith("$=") else "5"
        ps.append('<hp:p id="2147483648" paraPrIDRef="%s" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0"><hp:run charPrIDRef="45">%s</hp:run></hp:p>' % (pp, runs_of(line)))
    o = re.sub(r'number="\d+"', 'number="%d"' % ENO[0], en_open, count=1)
    o = re.sub(r'instId="\d+"', 'instId="%d"' % (1950000000 + ENO[0]), o, count=1)
    return o + "".join(ps) + "</hp:subList></hp:endNote>"


def problem(pr):
    out = ['<hp:p id="%s" paraPrIDRef="35" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0"><hp:run charPrIDRef="27"><hp:ctrl>%s</hp:ctrl></hp:run>'
           '<hp:run charPrIDRef="26">%s</hp:run></hp:p>' % (nid(), endnote(pr["ans"], pr["sol"]), runs_of(pr["q"][0]))]
    out += [para("34", runs_of(l)) for l in pr["q"][1:]]
    if pr.get("pic"):
        out.append(pic_para(*pr["pic"]))
    out += [para("68", runs_of(l)) for l in pr.get("choices") or []]
    out += [para("34", "") for _ in range(BLANK)]
    return out


total, MAP = 0, []
for j, u in enumerate(SEL):
    M = load(u)
    f = re.sub(r'<hp:masterPage idRef="masterpage\d+"/>\s*<hp:masterPage idRef="masterpage\d+"/>',
               '<hp:masterPage idRef="masterpage%d"/><hp:masterPage idRef="masterpage%d"/>' % (2 * j, 2 * j + 1), first, count=1)
    body = [head_xml + f]
    for st, probs in ((1, M.STEP1), (2, M.STEP2)):
        for pr in probs:
            body += problem(pr)
            MAP.append((u, st, ENO[0], pr["src"]))
            total += 1
    files["Contents/section%d.xml" % j] = ("".join(body) + "</hs:sec>").encode("utf-8")

if NEWBIN:
    hpf = files["Contents/content.hpf"].decode("utf-8")
    hpf = hpf.replace("</opf:manifest>", "".join('<opf:item id="%s" href="%s" media-type="%s" isEmbeded="1"/>' % (iid, p, mt) for p, d, iid, mt in NEWBIN) + "</opf:manifest>", 1)
    files["Contents/content.hpf"] = hpf.encode("utf-8")
    for p, d, iid, mt in NEWBIN:
        files[p] = d
        NAMES.append(p)
with zipfile.ZipFile(OUT, "w") as w:
    for n in NAMES:
        info = zipfile.ZipInfo(n, date_time=(1980, 1, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_STORED if n == "mimetype" else zipfile.ZIP_DEFLATED
        w.writestr(info, files[n])
print("단원", SEL, "문항", total, "->", OUT)
with open(os.path.splitext(OUT)[0] + "_출처.tsv", "w", encoding="utf-8") as f:
    f.write("단원\tSTEP\t워크북 번호\t출처\n" + "".join("%d\t%d\t%d\t%s\n" % m for m in MAP))
