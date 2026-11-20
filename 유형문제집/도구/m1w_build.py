# -*- coding: utf-8 -*-
"""CLIMATH(m) 공통수학1 워크북(한글 HWPX) 만들기 (2026-11-20).
python m1w_build.py <출력.hwpx> [단원 번호 …]   (단원 번호를 빼면 문항 파일이 있는 단원 모두)
- 사용자: 'CLIMATH(m) 공통수학1 워크북을 만들고 싶어. 수업 시 반드시 풀어야 할 문제(대표문제와 유형서와 쌍둥이)로 선정한 문제의 숫자 변형 문제로 구성해.
  숫자 변형한 문제는 올려 준 파일처럼 단계별 서술형 문제였으면 좋겠는데, 풀이가 짧거나 해서 단계를 나누기 어려운 문제는 꼭 단계로 구성하지 않아도 돼.
  편집 form은 CLIMATH(c) 워크북을 참고하되 STEP 1, STEP 2 박스는 필요 없어' + 단계별 서술형 보기 파일(문제 끝 '…구하는 과정을 다음 단계로 서술하시오.' + (1)(2)(3) 줄).
- 문항: CLIMATH_m/공통수학1_워크북/문항/uNN.py (PROBS: src 원문항 번호, q 문제 글, steps 서술 단계, ans 정답, sol 풀이 줄). 글 속 $…$는 한글 수식(스크립트).
- 틀: CLIMATH(c) 공통수학1 워크북 HWPX(쪽 크기·2단·바탕쪽·글자/문단 모양). 구역 = 단원(12개), 바탕쪽은 1단원 것을 복사해 'ⓒ'→'ⓜ', 단원 이름을 기본서 12단원으로.
  문제 문단(문단 35·글자 26, 번호 = 미주 번호 27), 단계 줄(문단 34), 빈 줄(문단 34)로 풀이 공간, 한 단에 2문항(두 번째 문항 뒤 다음 문항은 단 나누기).
  미주: '정답 …'(글자 44) 다음 풀이 줄(문단 5, '$='로 시작하는 줄은 이어 쓰기 문단 54, 글자 45).
- 수식 크기는 스크립트로 어림(한글이 다시 그릴 때 맞춰짐).
"""
import sys, os, re, zipfile, html, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(HERE, "guide"))
from extract import top_paras

TPL = os.path.join(ROOT, "CLIMATH_c", "공통수학1_워크북", "CLIMATH(c)_공통수학1_워크북.hwpx")
QDIR = os.path.join(ROOT, "CLIMATH_m", "공통수학1_워크북", "문항")
UNITS = ["다항식의 연산과 항등식", "나머지정리", "인수분해", "복소수와 이차방정식", "이차함수와 이차방정식의 관계", "이차함수의 최대, 최소",
         "여러 가지 방정식", "이차부등식", "연립부등식", "경우의 수와 순열", "조합", "행렬"]
OUT = sys.argv[1]
SEL = [int(a) for a in sys.argv[2:]] or [u for u in range(1, 13) if os.path.exists(os.path.join(QDIR, "u%02d.py" % u))]
BLANK_A, BLANK_B = 16, 3          # 한 단의 첫 문항 뒤 빈 줄, 둘째 문항 뒤 빈 줄(그다음 문항은 단 나누기)


def load(u):
    spec = importlib.util.spec_from_file_location("u%02d" % u, os.path.join(QDIR, "u%02d.py" % u))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.PROBS


# ---------------------------------------------------------------- 수식
EQ_TPL = ('<hp:equation id="%d" zOrder="0" numberingType="EQUATION" textWrap="TOP_AND_BOTTOM" textFlow="BOTH_SIDES" lock="0" dropcapstyle="None" '
          'version="Equation Version 60" baseLine="%d" textColor="#000000" baseUnit="1100" lineMode="CHAR" font="HancomEQN">'
          '<hp:sz width="%d" widthRelTo="ABSOLUTE" height="%d" heightRelTo="ABSOLUTE" protect="0"/>'
          '<hp:pos treatAsChar="1" affectLSpacing="0" flowWithText="1" allowOverlap="0" holdAnchorAndSO="0" vertRelTo="PARA" horzRelTo="PARA" '
          'vertAlign="TOP" horzAlign="LEFT" vertOffset="0" horzOffset="0"/><hp:outMargin left="56" right="56" top="0" bottom="0"/>'
          '<hp:shapeComment>수식입니다.</hp:shapeComment><hp:script>%s</hp:script></hp:equation>')
EQID = [1800000000]
KW = {"times": .8, "cdot": .45, "cdots": 1.2, "therefore": 1.0, "CIRC": .7, "le": .8, "ge": .8, "leq": .8, "geq": .8, "pm": .8, "mp": .8,
      "alpha": .55, "beta": .55, "gamma": .5, "omega": .65, "pi": .55, "theta": .5, "inf": 1, "neq": .8, "bigcirc": .9, "triangle": .8, "angle": .7}
SKIP = {"rm", "it", "bold", "LEFT", "RIGHT", "left", "right", "bar", "hat", "vec", "dot", "under"}


def _w(t):
    """스크립트 → (너비 em, 높이 줄 수)"""
    t = t.strip()
    w, h, i = 0.0, 1.0, 0
    toks = re.findall(r"\{|\}|\^|_|[A-Za-z]+|\d|\s+|`|~|.", t)
    stack = []
    out = []                                  # (w, h) 조각
    def grp(j):
        """toks[j]가 '{'면 짝까지 묶어 (너비, 높이, 다음 j)"""
        if j < len(toks) and toks[j] == "{":
            d, k = 0, j
            while k < len(toks):
                if toks[k] == "{": d += 1
                elif toks[k] == "}":
                    d -= 1
                    if d == 0: break
                k += 1
            ww, hh = _w("".join(toks[j + 1:k]))
            return ww, hh, k + 1
        if j < len(toks):
            ww, hh = _w(toks[j])
            return ww, hh, j + 1
        return 0, 1, j
    j = 0
    while j < len(toks):
        tk = toks[j]
        if tk == "{":
            ww, hh, j = grp(j); out.append((ww, hh)); continue
        if tk in ("^", "_"):
            ww, hh, j = grp(j + 1); out.append((ww * .62, max(1, hh * .7))); continue
        if tk == "over":
            num = out.pop() if out else (0, 1)
            ww, hh, j = grp(j + 1)
            out.append((max(num[0], ww) + .2, num[1] + hh)); continue
        if tk == "sqrt":
            ww, hh, j = grp(j + 1); out.append((ww + .7, hh + .1)); continue
        if tk in SKIP:
            j += 1; continue
        if tk in KW:
            out.append((KW[tk], 1)); j += 1; continue
        if tk.isspace():
            j += 1; continue
        if tk == "~": out.append((.3, 1))
        elif tk == "`": out.append((.1, 1))
        elif re.fullmatch(r"[A-Za-z]+", tk): out.append((.5 * len(tk), 1))
        elif tk.isdigit(): out.append((.5, 1))
        elif tk in "+-=<>": out.append((.85, 1))
        elif tk in "()[]|": out.append((.35, 1))
        elif tk in ",.:;": out.append((.3, 1))
        elif tk in "#&": pass
        else: out.append((.9 if ord(tk) > 0x2000 else .5, 1))
        j += 1
    return sum(a for a, _ in out), max([b for _, b in out] or [1])


def eq(script):
    EQID[0] += 1
    s = script.strip()
    if "cases" in s or "matrix" in s:
        rows = s.count("#") + 1
        w, hl = _w(re.sub(r"cases|pmatrix|matrix|bmatrix", "", s).replace("#", " ").replace("&", " ")), rows
        w = w / max(1, rows) * 1.2 + 1.0
    else:
        w, hl = _w(s)
    W = int(w * 1100) + 120
    H = int(1150 * hl) if hl > 1 else 1125
    base = 85 if hl <= 1 else int(100 * (0.5 + 0.35 / hl))
    return EQ_TPL % (EQID[0], base, W, H, html.escape(s, quote=False))


def runs_of(text):
    """'글 $수식$ 글' → <hp:t>…</hp:t><hp:equation…>… (같은 run 안)"""
    out = []
    for k, part in enumerate(re.split(r"\$", text)):
        if k % 2:
            if part.strip():
                out.append(eq(part))
        elif part:
            out.append("<hp:t>%s</hp:t>" % html.escape(part, quote=False))
    return "".join(out)


# ---------------------------------------------------------------- 틀
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
head = re.sub(r'secCnt="\d+"', 'secCnt="%d"' % NU, head, count=1)
files["Contents/header.xml"] = head.encode("utf-8")
files["Preview/PrvText.txt"] = "CLIMATH(m) 공통수학1 워크북".encode("utf-8")

# 바탕쪽: 1단원 짝수·홀수 쪽을 복사(안의 개체 id는 겹치지 않게 바꿈), 'ⓒ'→'ⓜ', 단원 이름
mp0, mp1 = files["Contents/masterpage0.xml"].decode("utf-8"), files["Contents/masterpage1.xml"].decode("utf-8")
# 짝수 쪽 제목 문단(문단 번호 매기기 135)은 같은 모양의 번호 없는 134로
mp0 = re.sub(r'(<hp:p [^>]*paraPrIDRef=")135("[^>]*>(?:(?!<hp:p ).)*?<hp:t>다항식의 연산</hp:t>)', r"\g<1>134\2", mp0, count=1, flags=re.S)
for j, u in enumerate(SEL):
    title = "%d. %s" % (u, UNITS[u - 1])
    for k, src in ((0, mp0), (1, mp1)):
        m = src.replace("<hp:t>ⓒ</hp:t>", "<hp:t>ⓜ</hp:t>")
        m = m.replace("<hp:t>다항식의 연산</hp:t>", "<hp:t>%s</hp:t>" % html.escape(title)).replace("<hp:t>1. 다항식의 연산</hp:t>", "<hp:t>%s</hp:t>" % html.escape(title))
        m = re.sub(r'(<masterPage [^>]*\bid=")masterpage\d+"', r'\g<1>masterpage%d"' % (2 * j + k), m, count=1)
        if j:
            m = re.sub(r'(\s(?:id|instid)=")(\d{6,})"', lambda q: '%s%d"' % (q.group(1), int(q.group(2)) + 7919 * j), m)
        files["Contents/masterpage%d.xml" % (2 * j + k)] = m.encode("utf-8")

# 구역 첫 문단(구역 정의·단 정의) — 1단원 구역에서, STEP 상자는 뺌
sec0 = files["Contents/section0.xml"].decode("utf-8")
P0 = top_paras(sec0)
head_xml = sec0[:sec0.index("<hp:p ")]
first = re.sub(r"<hp:linesegarray>.*?</hp:linesegarray>", "", P0[0])
first = re.sub(r"<hp:rect\b.*?</hp:rect>", "", first, flags=re.S)
first = re.sub(r"<hp:t>[^<]*</hp:t>", "<hp:t/>", first)
en_open = re.search(r"<hp:endNote [^>]*><hp:subList [^>]*>", sec0).group(0)
autonum = re.search(r'<hp:ctrl><hp:autoNum num="\d+" numType="ENDNOTE">.*?</hp:ctrl>', sec0, re.S).group(0)
NID = [3600000000]


def nid():
    NID[0] += 1
    return str(NID[0])


def para(pp, cp, inner, extra=""):
    return '<hp:p id="%s" paraPrIDRef="%s" styleIDRef="0" pageBreak="0" columnBreak="%s" merged="0"><hp:run charPrIDRef="%s">%s</hp:run></hp:p>' % (
        nid(), pp, "1" if extra == "col" else "0", cp, inner or "<hp:t/>")


ENO = [0]


def endnote(ans, sol):
    ENO[0] += 1
    ps = ['<hp:p id="2147483648" paraPrIDRef="5" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0"><hp:run charPrIDRef="44">%s<hp:t> 정답 </hp:t>%s</hp:run></hp:p>'
          % (re.sub(r'num="\d+"', 'num="%d"' % ENO[0], autonum, count=1), runs_of(ans))]
    for line in sol:
        pp = "54" if line.lstrip().startswith("$=") else "5"
        ps.append('<hp:p id="2147483648" paraPrIDRef="%s" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0"><hp:run charPrIDRef="45">%s</hp:run></hp:p>' % (pp, runs_of(line)))
    o = re.sub(r'number="\d+"', 'number="%d"' % ENO[0], en_open, count=1)
    o = re.sub(r'instId="\d+"', 'instId="%d"' % (1900000000 + ENO[0]), o, count=1)
    return o + "".join(ps) + "</hp:subList></hp:endNote>"


total = 0
for j, u in enumerate(SEL):
    probs = load(u)
    f = first
    f = re.sub(r'<hp:masterPage idRef="masterpage\d+"/>\s*<hp:masterPage idRef="masterpage\d+"/>',
               '<hp:masterPage idRef="masterpage%d"/><hp:masterPage idRef="masterpage%d"/>' % (2 * j, 2 * j + 1), f, count=1)
    body = [head_xml.replace('<hs:sec ', '<hs:sec ', 1) + f]
    for i, pr in enumerate(probs):
        q = pr["q"]
        if pr.get("steps"):
            q = q.rstrip()
        col = "col" if (i and i % 2 == 0) else ""
        body.append('<hp:p id="%s" paraPrIDRef="35" styleIDRef="0" pageBreak="0" columnBreak="%s" merged="0"><hp:run charPrIDRef="27"><hp:ctrl>%s</hp:ctrl></hp:run>'
                    '<hp:run charPrIDRef="26">%s</hp:run></hp:p>' % (nid(), "1" if col else "0", endnote(pr["ans"], pr["sol"]), runs_of(q)))
        for k, st in enumerate(pr.get("steps") or [], 1):
            body.append(para("34", "26", runs_of("(%d) %s" % (k, st))))
        for _ in range(BLANK_A if i % 2 == 0 else BLANK_B):
            body.append(para("34", "26", ""))
        total += 1
    files["Contents/section%d.xml" % j] = ("".join(body) + "</hs:sec>").encode("utf-8")

with zipfile.ZipFile(OUT, "w") as w:
    for n in NAMES:
        info = zipfile.ZipInfo(n, date_time=(1980, 1, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_STORED if n == "mimetype" else zipfile.ZIP_DEFLATED
        w.writestr(info, files[n])
print("단원", SEL, "문항", total, "->", OUT)
