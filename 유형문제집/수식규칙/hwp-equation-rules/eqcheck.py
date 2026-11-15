# -*- coding: utf-8 -*-
"""한글(hwpx) 문서의 수식을 수식 약속(SKILL.md)에 비추어 검사한다. 고치지 않고 알리기만 한다.
    python eqcheck.py 파일.hwpx [...] [--all]      (--all: 같은 종류를 모두 보여 줌, 기본은 종류마다 5개)
고칠 때: 1·2·4·5·6번 규칙은 eqstyle.py(명제는 --prop), '<-'는 eqfix.py가 그 자리에서 고친다.
나머지(괄호 짝, 붙여 쓴 명령, 음수 it-, 계승 등호 …)는 사람이 보고 고친다.
"""
import re, sys, html, zipfile, collections

EQ = re.compile(r"<hp:equation\b[^>]*>.*?</hp:equation>", re.S)
SC = re.compile(r"<hp:script\b[^>]*>(.*?)</hp:script>", re.S)
GLUE_CMDS = r"(overline|bar|alpha|beta|gamma|delta|theta|omega|pi|pmatrix|sqrt|times|TIMES|over|leq|geq|circ|rarrow)"
SPACE_WORDS = ("이하", "이상", "미만", "초과", "또는", "그리고")


def braces_ok(sc):
    """LEFT { · RIGHT } · left| 같은 괄호 기호를 빼고 { } 짝이 맞는지"""
    s = re.sub(r"\b(LEFT|RIGHT|left|right)\s*[{}|(\)\[\].]", " ", sc)
    d = 0
    for ch in s:
        d += (ch == "{") - (ch == "}")
        if d < 0:
            return False
    return d == 0


def piece_of_split(sc):
    """조건 속 한글을 수식 밖으로 뺀 조건제시법 조각('LEFT { x left| x' … 'it right')은 짝이 안 맞아도 정상"""
    return bool(re.search(r"\bLEFT\s*\{", sc) and not re.search(r"\bRIGHT\s*\}", sc)) or bool(re.search(r"\bright\s*$", sc.strip())) \
        or bool(re.search(r"\bRIGHT\s*\}", sc) and not re.search(r"\bLEFT\s*\{", sc))


def check_script(sc):
    out = []
    if not sc.strip():
        out.append(("빈 수식", "내용이 없는 수식 개체"))
        return out
    multi = re.search(r"\b(cases|pile|lpile|rpile|matrix|pmatrix|eqalign)\b|#", sc)
    if not braces_ok(sc) and not piece_of_split(sc):
        out.append(("괄호 짝", "{ } 짝이 맞지 않음(남거나 모자란 중괄호)"))
    if re.search(r"<\s*-(?!>)", sc):
        out.append(("'<-' 화살표", "'x<-1'은 x←1로 보임 → '< it-1'"))
    if re.search(r"[0-9]!=", sc):
        out.append(("계승 등호", "'5!=120'은 5≠120으로 보임 → '5! =120'(≠이면 그대로)"))
    m = re.search(r"(?<![A-Za-z\\])([0-9]+|[A-Za-z])" + GLUE_CMDS + r"\b", sc)
    if m and not re.search(r"\b(rm|it|bold|LEFT|RIGHT|left|right|n?subset|cap|cup|in|notin|sim|cdots|CDOTS|times|TIMES)$", sc[:m.end(1)]):
        out.append(("붙여 쓴 명령", "'%s' — 수·문자 바로 뒤 명령은 띄움('3 overline', '2 alpha beta', 'A pmatrix')" % m.group(0)))
    if re.search(r"\brm[A-Z]{1,3}\b", sc):
        out.append(("붙여 쓴 rm", "'rmAB'처럼 붙임 → 'rm AB' 또는 'rm {AB}'"))
    if re.search(r"\^\s*\{\s*`?\s*C\s*\}", sc):
        out.append(("여집합", "'^{C}' → '^{∁}'"))
    if re.search(r"\bvert\b", sc) and re.search(r"\bLEFT\s*\{", sc):
        out.append(("조건제시법 세로줄", "'`vert`' → 'left|'"))
    if re.search(r"\b(SUBSET|NSUBSET|SIM|SMALLINTER|CUP)\b", sc):
        out.append(("대문자 집합 기호", "SUBSET·NSUBSET·SIM·SMALLINTER·CUP → subset·nsubset·sim·cap·cup"))
    if re.search(r"\+\s*CDOTS\s*\+", sc):
        out.append(("합의 줄임표", "'+ CDOTS +' → '+ it CDOTS it +'"))
    if re.search(r"[^`\s]\s?\b(rarrow|RARROW)\b|\b(rarrow|RARROW)\s?[^`\s]", sc) and not re.search(r"`\s*:\s*`", sc):
        out.append(("명제 화살표 빈칸", "명제라면 'p`` rarrow ``q'(함수 f:X→Y는 'f`:`X`` rarrow ``Y')"))
    if re.search(r"(=|<|>|\bleq\b|\bgeq\b|\bLEQ\b|\bGEQ\b)\s*-\s*[0-9A-Za-z]", sc):
        out.append(("음수 it-(권장)", "관계 기호 바로 뒤 음수는 '= it-2'처럼(빼기 기호 앞뒤가 벌어지지 않게)"))
    if re.search(r",(?=[0-9A-Za-z(])", sc) and not multi:
        out.append(("쉼표 뒤 ~", "좌표·목록의 쉼표 뒤는 '~': '(1,~2)', '1,~2,~CDOTS,~10'"))
    if re.search(r"[가-힣]", sc) and not multi:
        bare = re.sub(r"\{[^{}]*\}", "", sc)
        if re.search(r"[가-힣]", bare):
            out.append(("수식 속 한글", "한글은 수식 밖 글자로(조건제시법은 '…left| x' + 글자 + 'it right')"))
    if re.search(r"\b(over)\{|\}over\b", sc):
        out.append(("분수 띄어쓰기", "'{a}over{b}' → '{a} over {b}'"))
    return out


def check_xml(xml):
    res = []
    for m in EQ.finditer(xml):
        sm = SC.search(m.group(0))
        sc = html.unescape(sm.group(1)) if sm else ""
        for k, why in check_script(sc):
            res.append((k, why, sc))
    # 수식 바로 뒤 '이하·이상·미만·초과·또는·그리고' 앞 빈칸
    for m in re.finditer(r"<hp:script\b[^>]*>([^<]*)</hp:script>.*?</hp:equation>(?:</hp:run><hp:run\b[^>]*>)?<hp:t>(%s)" % "|".join(SPACE_WORDS), xml, re.S):
        res.append(("수식 뒤 빈칸", "수식과 '%s' 사이를 한 칸 띄움(조사·단위는 붙임)" % m.group(2), html.unescape(m.group(1))))
    return res


def check_file(path, show=5):
    z = zipfile.ZipFile(path)
    res = []
    for n in sorted(z.namelist()):
        if re.match(r"Contents/section\d+\.xml$", n):
            res += check_xml(z.read(n).decode("utf-8"))
    C = collections.OrderedDict()
    for k, why, sc in res:
        C.setdefault(k, []).append((why, sc))
    print("== %s : 수식 %d개 중 확인할 곳 %d" % (path, sum(len(EQ.findall(z.read(n).decode('utf-8'))) for n in z.namelist() if re.match(r"Contents/section\d+\.xml$", n)), len(res)))
    for k, items in C.items():
        print("  [%s] %d곳 — %s" % (k, len(items), items[0][0]))
        for why, sc in items[:show]:
            print("      %s" % sc.strip()[:110])
    return len(res)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    show = 10 ** 6 if "--all" in sys.argv else 5
    for p in args:
        check_file(p, show)
