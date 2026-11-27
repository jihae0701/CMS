# -*- coding: utf-8 -*-
"""글자로 쓴 숫자·점 이름(대문자)을 수식 개체로 (2026-11-26).
python text2eq.py <입력 hwpx> <출력 hwpx>
- 사용자(CLIMATH(m) 대수 1단원 수정본): 문제·해설의 글자 숫자를 수식으로('8의 세제곱근' → '$8$의 세제곱근'), 점 이름도 수식으로('선분 AB' → '선분 $rm AB$')
  → '내가 숫자 영문자 수식으로 쓴 것도 확인했어?' '응'(남은 곳도 모두 바꾸기).
- 바꾸는 것: 본문·미주의 글자(hp:t) 속 숫자(정수·소수) → 수식 '8', 대문자 1~4자 낱말(점·도형 이름) → 수식 'rm ABC'.
  그리고 수식 안 집합 조건 막대 `|` → 'left |'(사용자 수정본과 같게).
- 단위 낱말(kcal·dB·m·mAh·cm·kg …, 홀로 쓰인 것) → 수식 'rm kcal'(2026-11-26 사용자 '맨 앞에 rm 붙여서').
- 그대로 두는 것: 'Step 1'·'STEP 1'·'(1)' 따름 번호, 모의고사 출처('2023년 11월 고2 14번 [4점]'), 상자(그리기 개체 글상자) 안 글자(개념·유형 상자 머리 등),
  바탕쪽·머리말(이 도구는 section 파일만 고침), 이미 수식인 것.
- 괄호 숫자 ⑴⑵…⒇ → (1)(2)…(20) 글자로(2026-11-27 사용자 '⑴ ⑵를 (1) (2) 이런 식으로 바꿔'). 글상자·미주 안도 모두.
- 수식 속 각도 'DEG' → 유니코드 00B0 '°'(2026-11-27 사용자 '수식에서 각도를 DEG를 쓰지 않고, 컨트롤 F10 들어가서 유니코드 00B0').
- 수식 크기는 사용자 파일에서 한글이 잰 값(11pt): 숫자 한 자 525, 소수점 263, 대문자 A 825·B 750·C 675·D 750·E 675·F 675·G 825·H 825·M 975·N 825·
  O 825·P 675·Q 825·R 750·S 600·T 675·U 750·X 750 …(그 밖 750), 높이 1125, baseLine 85.
"""
import re, sys, zipfile, html, random

CAP = dict(A=825, B=750, C=675, D=750, E=675, F=675, G=825, H=825, I=375, J=525, K=825, L=675, M=975, N=825, O=825, P=675,
           Q=825, R=750, S=600, T=675, U=750, V=825, W=1050, X=750, Y=750, Z=675)
rnd = random.Random(20261126)


def eq(sc, w):
    return ('<hp:equation id="%d" zOrder="0" numberingType="EQUATION" textWrap="TOP_AND_BOTTOM" textFlow="BOTH_SIDES" lock="0" '
            'dropcapstyle="None" version="Equation Version 60" baseLine="85" textColor="#000000" baseUnit="1100" lineMode="CHAR" font="HancomEQN">'
            '<hp:sz width="%d" widthRelTo="ABSOLUTE" height="1125" heightRelTo="ABSOLUTE" protect="0"/>'
            '<hp:pos treatAsChar="1" affectLSpacing="0" flowWithText="1" allowOverlap="0" holdAnchorAndSO="0" vertRelTo="PARA" horzRelTo="PARA" '
            'vertAlign="TOP" horzAlign="LEFT" vertOffset="0" horzOffset="0"/><hp:outMargin left="56" right="56" top="0" bottom="0"/>'
            '<hp:shapeComment>수식입니다.</hp:shapeComment><hp:script>%s</hp:script></hp:equation>') % (rnd.randrange(1, 2 ** 31 - 1), w, sc)


# 2026-11-26 사용자 '단위 kcal, dB, m는 수식으로 써, 맨 앞에 rm 붙여서' → 단위 낱말도 수식 'rm kcal'
UNITS = ["kcal", "mAh", "dB", "km", "cm", "mm", "kg", "mL", "m", "g", "L", "s", "h", "Hz", "W", "V", "A"]
LOW = dict(a=450, b=525, c=450, d=525, e=450, g=525, h=525, k=525, l=300, m=825, s=450, z=450, L=675, A=825, B=750, H=825, W=1050, V=825)
TOK = re.compile(r"(?<![0-9A-Za-z.])(\d+(?:\.\d+)?)(?![0-9A-Za-z])|(?<![A-Za-z])(%s)(?![A-Za-z])|(?<![A-Za-z])([A-Z]{1,4})(?![A-Za-z])"
                 % "|".join(u for u in UNITS if not re.fullmatch(r"[A-Z]+", u)))
MOCK = re.compile(r"\d{4}년|\d+월\s*고\d|\d+번\s*\[\d+점\]")


def keep_span(text):
    """바꾸지 않을 구간들(따름 번호·Step 번호)"""
    spans = []
    for m in re.finditer(r"(?:STEP|Step)\s*\d+|\(\d+\)|\[\d+점\]|\d+번|\d+월|\d{4}년|고\d", text):
        spans.append((m.start(), m.end()))
    return spans


def conv_text(t):
    """hp:t 안 글자 조각 → (새 XML, 바꾼 개수). 반환 XML은 '</hp:t>수식<hp:t>' 꼴로 글자 요소를 끊음"""
    if MOCK.search(t):
        return html.escape(t, quote=False), 0
    ks = keep_span(t)
    out, last, n = [], 0, 0
    for m in TOK.finditer(t):
        if any(a <= m.start() < b for a, b in ks):
            continue
        out.append(html.escape(t[last:m.start()], quote=False))
        if m.group(1):
            v = m.group(1)
            w = 525 * len(v.replace(".", "")) + (263 if "." in v else 0)
            out.append("</hp:t>" + eq(v, w) + "<hp:t>")
        elif m.group(2):
            v = m.group(2)                                    # 단위(kcal, dB, m, mAh …) → 'rm kcal'
            out.append("</hp:t>" + eq("rm " + v, sum(LOW.get(c, 525) for c in v)) + "<hp:t>")
        else:
            v = m.group(3)
            out.append("</hp:t>" + eq("rm " + v, sum(CAP.get(c, 750) for c in v)) + "<hp:t>")
        last = m.end(); n += 1
    out.append(html.escape(t[last:], quote=False))
    return "".join(out), n


def convert(xml):
    """section XML 전체에서(그리기 개체 글상자·수식 안은 빼고) 글자 숫자·대문자를 수식으로"""
    total = [0]
    # 손대지 않을 구간: 그리기 글상자(drawText), 수식
    protect = [(m.start(), m.end()) for m in re.finditer(r"<hp:drawText.*?</hp:drawText>|<hp:equation .*?</hp:equation>", xml, re.S)]
    protect.sort()

    def inside(pos):
        lo, hi = 0, len(protect)
        while lo < hi:
            mid = (lo + hi) // 2
            if protect[mid][1] <= pos: lo = mid + 1
            else: hi = mid
        return lo < len(protect) and protect[lo][0] <= pos < protect[lo][1]

    def rep_t(m):
        if inside(m.start()):
            return m.group(0)
        inner = m.group(1)
        parts = re.split(r"(<[^>]+>)", inner)
        res = []
        for p in parts:
            if p.startswith("<"):
                res.append(p)
            else:
                x, k = conv_text(html.unescape(p))
                total[0] += k
                res.append(x)
        s = "<hp:t>" + "".join(res) + "</hp:t>"
        return s.replace("<hp:t></hp:t>", "")

    out = re.sub(r"<hp:t>(.*?)</hp:t>", rep_t, xml, flags=re.S)
    # 집합 조건 막대: 사용자 수정본처럼 `|` → left | (수식 안)
    out, _ = bars(out)
    return out, total[0]


OPW = re.compile(r"(times|over|cdot|cdots|le|ge|leq|geq|ne|neq|of|sqrt|root|THEREFORE|therefore|because)$", re.I)


def bars_script(sc):
    """수식 하나의 맨 막대 | → 집합 조건은 'left |', 절댓값은 'left | … right |'(2026-11-27 사용자 '절댓값도 left | x-3 right |').
    이미 left|·right|인 막대는 그대로. 짝이 안 맞으면 None"""
    pos = [m.start() for m in re.finditer(r"\|", sc) if not re.search(r"(left|right)$", sc[:m.start()].rstrip(" `~"), re.I)]
    if not pos:
        return sc
    kind = {}
    rest = pos
    if re.search(r"lbrace|LEFT\s*\{", sc) and len(pos) % 2 == 1:
        kind[pos[0]] = "left |"; rest = pos[1:]                # 집합 조건 막대(첫 번째)
    stack, last = [], None
    for p in rest:
        pre = sc[:p].rstrip(" `~")
        prev = pre[-1:] if pre else ""
        if not stack or not prev or prev in "=+-*/({[,<>^_!" or OPW.search(pre) or (prev == "|" and last is not None):
            kind[p] = "left |"; stack.append(p)
        else:
            kind[p] = "right |"; stack.pop()
        last = p
    if stack:
        return None
    out, q = [], 0
    for p in pos:
        out.append(sc[q:p]); out.append(" %s " % kind[p]); q = p + 1
    out.append(sc[q:])
    return re.sub(r"  +", " ", "".join(out))


def bars(xml):
    """section XML의 수식 막대 바꾸기 → (xml, 바꾼 수식 수, 짝이 안 맞아 둔 수식 목록)"""
    n, bad = [0], []
    def f(m):
        sc = html.unescape(m.group(1))
        r = bars_script(sc)
        if r is None:
            bad.append(sc); return m.group(0)
        if r == sc:
            return m.group(0)
        n[0] += 1
        return "<hp:script>%s</hp:script>" % html.escape(r, quote=False)
    xml = re.sub(r"<hp:script>([^<]*)</hp:script>", f, xml)
    return xml, n[0], bad


DEG = re.compile(r"(<hp:script>[^<]*?)\s*(?<![A-Za-z])DEG(?![A-Za-z])")     # '500DEG'처럼 숫자에 붙은 것도


def deg(xml):
    """수식 속 각도 DEG → °(사용자 파일처럼 '90 DEG' → '90 °')"""
    n = 0
    while True:
        xml, k = DEG.subn(lambda m: m.group(1) + " °", xml)
        if not k:
            return xml, n
        n += k


CIRC = {chr(0x2474 + i): "(%d)" % (i + 1) for i in range(20)}
CIRC_RE = re.compile("[%s]" % "".join(CIRC))


def circ(xml):
    """글자(hp:t) 속 ⑴⑵… → (1)(2)…"""
    n = [0]
    def f(m):
        t, k = CIRC_RE.subn(lambda c: CIRC[c.group(0)], m.group(0))
        n[0] += k
        return t
    xml = re.sub(r"<hp:t>.*?</hp:t>", f, xml, flags=re.S)
    return xml, n[0]


def convert_file(src, dst):
    z = zipfile.ZipFile(src)
    items = [(i, z.read(i.filename)) for i in z.infolist()]
    z.close()
    n = 0
    with zipfile.ZipFile(dst, "w") as w:
        for info, data in items:
            if re.match(r"Contents/section\d+\.xml$", info.filename):
                s, k = convert(data.decode("utf-8")); n += k
                s, k = deg(s); n += k
                s, k = circ(s); n += k
                data = s.encode("utf-8")
            w.writestr(info, data)
    return n


if __name__ == "__main__":
    print(sys.argv[2], "수식으로 바꾼 곳", convert_file(sys.argv[1], sys.argv[2]))
