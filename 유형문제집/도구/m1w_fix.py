# -*- coding: utf-8 -*-
"""CLIMATH(m) 공통수학1 워크북 — 사용자 수정본에 맞춰 정답·풀이 고치기 (2026-11-24).
python m1w_fix.py <사용자수정본.hwpx> <정답풀이.py> <출력.hwpx>
- 사용자: '워크북 고쳤어. 수정된 상태에 맞게 정답 풀이 수정해야 해. 정답은 정답 (1) (2) (3) 이런 식으로 따름 문제 답 나열하는 형태로.
  5단원 문제 수가 줄었으니 CLIMATH(m) 공통수학1 5단원 맨 마지막 문제 변형해서 넣어 줘.'
- 정답풀이.py: F[문항 번호(1~141, 수정본 순서)] = dict(ans=[단계별 답], sol=None(지금 풀이 그대로) | [새 풀이 줄]), NEW5(5단원 끝에 넣을 문항).
- 미주 첫 문단: 사용자 수정본 꼴(글자 모양 41, ' 󰂼 ') + '(1) 답  (2) 답 …'(단계가 없으면 답만). 풀이 문단은 문단 모양 5 · 글자 모양 42.
- 수식 안 '보이는 중괄호'로 쓴 묶음({f(x)-x}{f(x)-5} 등 — 한글 수식에서는 괄호가 안 보임)은 미주(정답·풀이)에서 left { … right }로 바꿈.
  문제 글은 사용자 것이라 그대로 두고 알림.
- 문제·단계 문단은 손대지 않음. 미주 번호는 차례대로 다시 매김.
"""
import sys, os, re, zipfile, html, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "guide"))
from extract import top_paras

SRC, DATA, OUT = sys.argv[1:4]
spec = importlib.util.spec_from_file_location("fixdata", DATA)
D = importlib.util.module_from_spec(spec)
spec.loader.exec_module(D)
F, NEW5 = D.F, D.NEW5

# m1w_build.py의 수식 크기 어림(_w, eq)을 그대로 씀
src = open(os.path.join(HERE, "m1w_build.py"), encoding="utf-8").read()
a, b = src.index("EQ_TPL = ("), src.index("# ---------------------------------------------------------------- 틀")
g = {"re": re, "html": html}
exec(src[a:b], g)
g["EQID"][0] = 1850000000                                     # 수정본 수식 id(최대 1800003892)와 겹치지 않게
eq_raw = g["eq"]

KEEPPRE = r"(\^|_|sqrt|over|left|LEFT|rm|it|bold|bar|hat|vec|dot|pmatrix|bmatrix|matrix|cases|eqalign)$"


def fix_braces(sc):
    """보이는 괄호로 쓴 { … } → left { … right } (^·_·sqrt·over 인자, 분자, 짧은 이름은 그대로)"""
    out, i = [], 0
    while i < len(sc):
        c = sc[i]
        if c == "{" and not re.search(KEEPPRE, sc[:i].rstrip()) and not sc[:i].endswith(("^", "_")):
            d, j = 0, i
            while j < len(sc):
                if sc[j] == "{": d += 1
                elif sc[j] == "}":
                    d -= 1
                    if d == 0: break
                j += 1
            inner = sc[i + 1:j]
            post = sc[j + 1:].lstrip()
            if j < len(sc) and not post.startswith("over") and not re.fullmatch(r"\s*\w{0,3}\s*", inner):
                out.append(" left { " + fix_braces(inner) + " right } ")
                i = j + 1
                continue
        out.append(c)
        i += 1
    return "".join(out)


def eq(sc):
    return eq_raw(fix_braces(sc))


def runs_of(text):
    out = []
    for k, part in enumerate(re.split(r"\$", text)):
        if k % 2:
            if part.strip():
                out.append(eq(part))
        elif part:
            out.append("<hp:t>%s</hp:t>" % html.escape(part, quote=False))
    return "".join(out)


def ans_line(ans):
    if len(ans) == 1:
        return runs_of(ans[0])
    return runs_of("  ".join("(%d) %s" % (k, a) for k, a in enumerate(ans, 1)))


def sol_para(line):
    return ('<hp:p id="2147483648" paraPrIDRef="5" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0">'
            '<hp:run charPrIDRef="42">%s</hp:run></hp:p>' % runs_of(line))


def fix_old_eqs(p):
    """그대로 두는 풀이 문단의 수식 속 보이는 괄호만 고침"""
    return re.sub(r"<hp:script>([^<]*)</hp:script>",
                  lambda m: "<hp:script>%s</hp:script>" % html.escape(fix_braces(html.unescape(m.group(1))), quote=False), p)


N = [0]


def new_endnote(en, item):
    """en: 원래 <hp:endNote …>…</hp:endNote>"""
    N[0] += 1
    i = en.index("<hp:subList")
    j = en.index(">", i) + 1
    head = en[:j]
    head = re.sub(r'number="\d+"', 'number="%d"' % N[0], head, count=1)
    head = re.sub(r'instId="\d+"', 'instId="%d"' % (1950000000 + N[0]), head, count=1)
    paras = top_paras(en[j:en.rindex("</hp:subList>")])
    first = paras[0]
    autonum = re.search(r"<hp:ctrl><hp:autoNum .*?</hp:ctrl>", first, re.S).group(0)
    autonum = re.sub(r'num="\d+"', 'num="%d"' % N[0], autonum, count=1)
    ps = ['<hp:p id="2147483648" paraPrIDRef="5" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0">'
          '<hp:run charPrIDRef="41">%s<hp:t> 󰂼 </hp:t>%s</hp:run></hp:p>' % (autonum, ans_line(item["ans"]))]
    if item.get("sol") is None:
        ps += [fix_old_eqs(re.sub(r"<hp:linesegarray>.*?</hp:linesegarray>", "", p, flags=re.S)) for p in paras[1:]]
    else:
        ps += [sol_para(l) for l in item["sol"]]
    return head + "".join(ps) + "</hp:subList></hp:endNote>"


z = zipfile.ZipFile(SRC)
files = {n: z.read(n) for n in z.namelist()}
nsec = len([n for n in files if re.match(r"Contents/section\d+\.xml$", n)])
idx = 0
EN_TPL = None
for k in range(nsec):
    name = "Contents/section%d.xml" % k
    s = files[name].decode("utf-8")
    P = top_paras(s)
    head_xml, tail_xml = s[:s.index(P[0])], s[s.rindex(P[-1]) + len(P[-1]):]
    out = []
    for p in P:
        ens = re.findall(r"<hp:endNote .*?</hp:endNote>", p, re.S)
        if ens:
            idx += 1
            assert len(ens) == 1, idx
            EN_TPL = EN_TPL or (ens[0], p)
            p = p.replace(ens[0], new_endnote(ens[0], F[idx]))
        out.append(p)
    if k == 4:                                                 # 5단원 끝에 새 문항(한 단에 1문항: 단 나누기)
        en_src, p_src = EN_TPL
        prob_en = new_endnote(en_src, NEW5)
        out.append('<hp:p id="3990000001" paraPrIDRef="35" styleIDRef="0" pageBreak="0" columnBreak="1" merged="0">'
                   '<hp:run charPrIDRef="26"><hp:ctrl>%s</hp:ctrl></hp:run><hp:run charPrIDRef="25">%s</hp:run></hp:p>'
                   % (prob_en, runs_of(NEW5["q"])))
        for t, st in enumerate(NEW5["steps"], 1):
            if t > 1:
                out.append('<hp:p id="%d" paraPrIDRef="34" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0"><hp:run charPrIDRef="25"/></hp:p>' % (3990000010 + t))
            out.append('<hp:p id="%d" paraPrIDRef="34" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0"><hp:run charPrIDRef="25">%s</hp:run></hp:p>'
                       % (3990000020 + t, runs_of("(%d) %s" % (t, st))))
        # 다음 단원 미주 번호가 1 늘어난 것을 위해 N은 그대로 이어짐(위 new_endnote에서 +1)
    files[name] = (head_xml + "".join(out) + tail_xml).encode("utf-8")
assert idx == len(F), (idx, len(F))

with zipfile.ZipFile(OUT, "w") as w:
    for n in z.namelist():
        info = zipfile.ZipInfo(n, date_time=(1980, 1, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_STORED if n == "mimetype" else zipfile.ZIP_DEFLATED
        w.writestr(info, files[n])
print("문항", idx, "+ 5단원 새 문항 1 → 미주", N[0], "->", OUT)
