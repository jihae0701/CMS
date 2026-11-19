# -*- coding: utf-8 -*-
"""빠른 정답 — 목록 형태(CLIMATH(c) 공통수학1) (2026-11-19).
python quickans_list.py [c1c|c1w] <출력.hwpx> [시작 쪽 번호]   (책을 빼면 c1c)
- c1w(2026-11-19 워크북): 사용자 'CLIMATH(c) 워크북도 만들어 줘. 연보라 페이지 필요 없음. 목차와 빠른 정답만 있으면 됨' + 워크북 한 파일
  (CLIMATH_c/공통수학1_워크북/CLIMATH(c)_공통수학1_워크북.hwpx: 구역 14개 = 단원, 미주 번호 1~364가 단원을 넘어 이어짐, 정답 표시 '정답'/'[정답]').
  틀은 워크북 파일(쪽 번호가 인쇄되는 바탕쪽)의 첫 구역만 남김. 단원 띠는 본책 1단원 파일의 초록 띠를 복사(띠 안 글자 모양은 글꼴째 옮김).
  문항 번호는 미주 번호 그대로, 정답 표시는 본책과 같이 '󰂼'로. 시작 쪽 번호를 주면 첫 문단에 쪽 번호 새로 시작.
- 사용자: '빠른 정답 파일을 봤는데, CLIMATH(c)는 따름 문제가 많아서 이 형태(표)로는 안 예뻐. 내가 올려 준 형태로 했으면 좋겠고.
  미주의 첫 줄만 가져오다 보니 빠른 정답에 따름 문제 정답이 누락된 게 있는 것처럼 보여' + 보기 PDF(다른 책 빠른 정답 20쪽).
- 보기 형태: 2단, 단원마다 새 쪽에서 초록 둥근 띠 'N. 단원명'(흰 글자), 문항마다 한 문단 'N. 󰂼 정답'(굴림 10pt, 내어쓰기로 둘째 줄부터 정답 자리에 맞춤),
  따름 문제 (1)(2)…는 미주의 정답 줄을 그대로(줄바꿈·탭 그대로).
- 틀: 1단원 파일(쪽 크기·여백·2단·바탕쪽·꼬리말). 바탕쪽 단원 이름 자리에는 '빠른 정답'. 단원 띠는 단원 파일 끝에 있는 초록 둥근 띠(29484×2549, #008000)를 복사해
  글자만 'N. 단원명'으로(원래 문단 번호 매기기로 '1.'이 붙던 것을 글자로 씀).
- 정답 범위(미주): 정답 표시('󰂼', 6단원 19번은 그림 정답.png) 뒤부터
  · 첫 문단: 첫 줄 + 줄바꿈 뒤 줄이 따름 번호((k)·⑴·①, 번호는 앞보다 큼)·빈칸/탭·'='·'또는'으로 시작하면 정답이 이어짐(4단원 33번 '= …', 9단원 연립방정식 둘째 줄 등).
    그 밖의 글로 시작하는 줄(풀이: 2단원 22번, 13단원 35번)에서 멈춤.
  · 다음 문단: 바로 다음 따름 번호로 시작하면 정답이 이어짐(4단원 2번 (4)). 번호가 다시 (1)부터면 풀이.
  · 앞 줄이 '또는'으로 끝나면 다음 줄·문단은 무엇으로 시작하든 정답(9단원 4번: 연립방정식 해가 다음 문단으로 넘어감).
"""
import sys, os, re, zipfile, html

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DIR = os.path.join(ROOT, "CLIMATH_c", "공통수학1")
ARGS = sys.argv[1:]
BOOK = ARGS.pop(0) if ARGS and ARGS[0] in ("c1c", "c1w") else "c1c"
OUT = ARGS[0]
START = int(ARGS[1]) if len(ARGS) > 1 else None
WB = os.path.join(ROOT, "CLIMATH_c", "공통수학1_워크북", "CLIMATH(c)_공통수학1_워크북.hwpx")
UNITS = ["다항식의 연산", "항등식", "나머지정리", "인수분해", "복소수", "이차함수와 이차방정식의 관계", "이차함수의 최대·최소",
         "고차방정식", "연립방정식", "연립부등식과 이차부등식", "연립이차부등식", "순열", "조합", "행렬"]
MARK = "󰂼"
MARKS = re.compile(r"󰂼|\[정답\]|정답|답\.")           # 본책 '󰂼', 워크북 '정답'·'[정답]'·'답.'(184번)
MARK_PICS = ["image27"]                                    # 워크북의 '정답' 상자 그림

# ---------------------------------------------------------------- 미주 → 정답 토큰
TOK = re.compile(r"<hp:ctrl(?:\s[^>]*)?>.*?</hp:ctrl>|<hp:t(?:\s[^>]*)?/>|<hp:t(?:\s[^>]*)?>(.*?)</hp:t>|(<hp:equation\b.*?</hp:equation>)|(<hp:pic\b.*?</hp:pic>)"
                 r"|<hp:(rect|tbl|container|ellipse|line|polygon|arc|curve|ole)\b.*?</hp:\4>", re.S)
INNER = re.compile(r"<hp:lineBreak/>|(<hp:tab\b[^>]*/>|<hp:tab\b[^>]*>.*?</hp:tab>)|(<hp:[A-Za-z]+\b[^>]*/>)|([^<]+)", re.S)
LABEL = re.compile(r"^[ \t　]*(?:\((\d+)\)|([⑴-⒇])|([①-⑳]))")


def tokens(p):
    """문단 → [(종류, xml)]: t(이미 이스케이프된 글), br, tab, x(그 밖의 글 속 요소), eq, other"""
    p = re.sub(r"<hp:linesegarray>.*?</hp:linesegarray>", "", p, flags=re.S)
    p = re.sub(r"<hp:pic\b(?:(?!</hp:pic>).)*?정답\.png(?:(?!</hp:pic>).)*</hp:pic>", "<hp:t>%s</hp:t>" % MARK, p, flags=re.S)
    # 워크북 7단원 186번: 정답 표시가 '정답' 상자 그림(BinData image27.png) → 표시 글자로
    p = re.sub(r'<hp:pic\b(?:(?!</hp:pic>).)*?binaryItemIDRef="(?:%s)"(?:(?!</hp:pic>).)*</hp:pic>' % "|".join(MARK_PICS), "<hp:t>%s</hp:t>" % MARK, p, flags=re.S)
    # 글자처럼 취급하지 않는(떠 있는) 그림은 풀이 그림 → 뺌(워크북 171번 그래프, 309번 그림)
    p = re.sub(r'<hp:pic\b(?:(?!</hp:pic>).)*?<hp:pos treatAsChar="0"(?:(?!</hp:pic>).)*</hp:pic>', "", p, flags=re.S)
    out = []
    for m in TOK.finditer(p):
        if m.group(2):
            out.append(("eq", m.group(2)))
        elif m.group(3) or m.group(4):
            out.append(("other", m.group(0)))
        elif m.group(1) is not None:
            for q in INNER.finditer(m.group(1)):
                if q.group(0) == "<hp:lineBreak/>":
                    out.append(("br", ""))
                elif q.group(1):
                    out.append(("tab", q.group(1)))
                elif q.group(2):
                    out.append(("x", q.group(2)))
                else:
                    out.append(("t", q.group(3)))
    return out


def lines(toks):
    ls, cur = [], []
    for t in toks:
        if t[0] == "br":
            ls.append(cur)
            cur = []
        else:
            cur.append(t)
    ls.append(cur)
    return ls


def plain(line):
    return "".join(html.unescape(v) if k == "t" else ("\t" if k == "tab" else ("E" if k == "eq" else "")) for k, v in line)


def label(txt):
    m = LABEL.match(txt)
    if not m:
        return None
    if m.group(1):
        return int(m.group(1))
    if m.group(2):
        return ord(m.group(2)) - 0x2473
    return ord(m.group(3)) - 0x245F


def strip_line(line):
    """줄 앞뒤의 빈칸·탭 정리(앞은 빈칸만 남기지 않음 — 둘째 줄부터는 내어쓰기 자리에서 시작)"""
    line = list(line)
    while line and (line[-1][0] == "tab" or (line[-1][0] == "t" and not line[-1][1].strip()) or line[-1][0] == "x"):
        line.pop()
    if line and line[-1][0] == "t":
        line[-1] = ("t", line[-1][1].rstrip())
    return line


def answer(en, where):
    ps = re.findall(r"<hp:p\b[^>]*>.*?</hp:p>", en, re.S)
    # 미주 안 문단은 겹치지 않음(글상자 등 안 문단은 없다고 봄) — 첫 문단에서 표시 찾기
    t0 = tokens(ps[0])
    k = next((i for i, (kk, v) in enumerate(t0) if kk == "t" and MARKS.search(html.unescape(v))), None)
    if k is None:                                           # 표시 없이 첫 문단이 '해설참조' 같은 글(워크북 5단원 131번) → 그 글을 정답 자리에
        k = next((i for i, (kk, v) in enumerate(t0) if kk == "t" and html.unescape(v).strip()), None)
        if k is None:
            raise SystemExit("정답 표시 없음: %s" % where)
        print("정답 표시 없음 → 첫 문단 글 그대로:", where, html.unescape(t0[k][1]).strip()[:20])
        t0 = t0[:k] + [("t", " " + t0[k][1].lstrip())] + t0[k + 1:]
        if html.unescape(t0[k][1]).strip() == "해설참조" and len(ps) > 1:
            # 2026-11-19 사용자 '해설참조도 정답 만들어 줄 수 있어?' — 워크북 131번: 풀이 첫 문단이 정답 줄('x=2, y=1 또는 x=−2, y=−1') → 그것을 정답으로
            ps = ps[1:]
            t0 = [("t", " ")] + tokens(ps[0])
            k = 0
            print("   → 풀이 첫 문단을 정답으로")
        v, mm = t0[k][1], re.match(r"", "")
    else:
        v = t0[k][1]
        mm = MARKS.search(v)
    rest = v[mm.end():]
    t0 = [("t", MARK + " " + rest.lstrip())] + t0[k + 1:]
    out_lines, last, stop, cont = [], 0, False, False
    for pi, p in enumerate(ps):
        ls = lines(t0 if pi == 0 else tokens(p))
        if pi > 0:
            lb = label(plain(ls[0]))
            if not ((last and lb == last + 1) or cont):
                break
        for li, ln in enumerate(ls):
            txt = plain(ln)
            if (pi, li) != (0, 0) and not cont:
                lb = label(txt)
                if lb is not None:
                    if lb <= last:
                        stop = True
                        break
                elif not re.match(r"^([ \t　]|=|또는)", txt) and txt.strip():
                    stop = True
                    break
            for m in re.finditer(r"\((\d+)\)|([⑴-⒇])|([①-⑳])", txt):
                n = int(m.group(1)) if m.group(1) else (ord(m.group(2)) - 0x2473 if m.group(2) else ord(m.group(3)) - 0x245F)
                if n == last + 1:
                    last = n
            cont = txt.rstrip().endswith("또는")         # '… 또는'으로 끝나면 다음 줄·문단에 정답이 이어짐(9단원 4번)
            s = strip_line(ln)
            if (pi, li) != (0, 0):
                while s and s[0][0] in ("tab", "x") or (s and s[0][0] == "t" and not html.unescape(s[0][1]).strip()):
                    s.pop(0)
                if s and s[0][0] == "t":
                    s[0] = ("t", s[0][1].lstrip(" 　"))
            if s:
                out_lines.append(s)
        if stop:
            break
    others = [x for ln in out_lines for x in ln if x[0] == "other"]
    if others:
        print("정답 안에 그림·표 등:", where, len(others))
    return out_lines


data = []
for u, name in enumerate(UNITS, 1):
    if BOOK == "c1c":
        x = zipfile.ZipFile(os.path.join(DIR, "%d. %s.hwpx" % (u, name))).read("Contents/section0.xml").decode("utf-8")
    else:
        x = zipfile.ZipFile(WB).read("Contents/section%d.xml" % (u - 1)).decode("utf-8")
    ens = re.findall(r"<hp:endNote .*?</hp:endNote>", x, re.S)
    if BOOK == "c1c":
        nums = list(range(1, len(ens) + 1))
    else:                                                   # 워크북: 미주 번호(단원을 넘어 이어짐)
        nums = [int(re.search(r'<hp:autoNum num="(\d+)" numType="ENDNOTE"', en).group(1)) for en in ens]
    data.append((u, name, [(n, answer(en, "%d단원 %d번" % (u, n))) for n, en in zip(nums, ens)]))
allnums = [n for _, _, a in data for n, _ in a]
assert allnums == (list(range(1, len(allnums) + 1)) if BOOK == "c1w" else allnums), "미주 번호가 이어지지 않음"

# ---------------------------------------------------------------- 틀
MAIN1 = os.path.join(DIR, "1. %s.hwpx" % UNITS[0])
TPL = MAIN1 if BOOK == "c1c" else WB
z = zipfile.ZipFile(TPL)
files = {n: z.read(n) for n in z.namelist()}
NAMES = list(z.namelist())
if BOOK == "c1w":                                           # 첫 구역(1단원)과 그 바탕쪽(0·1)만 남김
    drop = [n for n in NAMES if (re.match(r"Contents/section(\d+)\.xml$", n) and n != "Contents/section0.xml")
            or (re.match(r"Contents/masterpage(\d+)\.xml$", n) and int(re.search(r"\d+", n).group(0)) > 1)]
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
if BOOK == "c1w":
    head = re.sub(r'secCnt="\d+"', 'secCnt="1"', head, count=1)
sec = files["Contents/section0.xml"].decode("utf-8")
msec = zipfile.ZipFile(MAIN1).read("Contents/section0.xml").decode("utf-8")       # 단원 띠는 본책 1단원 파일에서
mhead = zipfile.ZipFile(MAIN1).read("Contents/header.xml").decode("utf-8")


def add_item(head, tag, plural, src_id, fn):
    m = re.search(r'<hh:%s id="%s".*?</hh:%s>' % (tag, src_id, tag), head, re.S)
    cnt = int(re.search(r'<hh:%s itemCnt="(\d+)"' % plural, head).group(1))
    nid_ = max(int(x) for x in re.findall(r'<hh:%s id="(\d+)"' % tag, head)) + 1
    new = fn(re.sub(r'id="%s"' % src_id, 'id="%d"' % nid_, m.group(0), count=1))
    end = head.index("</hh:%s>" % plural)
    head = head[:end] + new + head[end:]
    head = re.sub(r'<hh:%s itemCnt="\d+"' % plural, '<hh:%s itemCnt="%d"' % (plural, cnt + 1), head, count=1)
    return head, nid_


def margins(x, intent, nxt, spacing):
    """HwpUnitChar 쪽(case)과 옛 쪽(default, 값 2배) 모두"""
    def f(seg, k):
        seg = re.sub(r'(<hc:intent value=")-?\d+', lambda m: m.group(1) + str(intent * k), seg)
        seg = re.sub(r'(<hc:left value=")-?\d+', lambda m: m.group(1) + "0", seg)
        seg = re.sub(r'(<hc:prev value=")-?\d+', lambda m: m.group(1) + "0", seg)
        seg = re.sub(r'(<hc:next value=")-?\d+', lambda m: m.group(1) + str(nxt * k), seg)
        seg = re.sub(r'(<hh:lineSpacing type=")[A-Z_]+(" value=")\d+', lambda m: m.group(1) + "PERCENT" + m.group(2) + str(spacing), seg)
        return seg
    x = re.sub(r"<hp:case\b.*?</hp:case>", lambda m: f(m.group(0), 1), x, flags=re.S)
    x = re.sub(r"<hp:default>.*?</hp:default>", lambda m: f(m.group(0), 2), x, flags=re.S)
    return x


# 원래 미주 정답 문단의 글자 모양(굴림 11pt 굵게, charPr 24) → 10pt 보통
src_cp = re.search(r'<hp:endNote .*?<hp:run charPrIDRef="(\d+)"><hp:ctrl><hp:autoNum', sec, re.S).group(1)
head, CP_A = add_item(head, "charPr", "charProperties", src_cp,
                      lambda x: re.sub(r'height="\d+"', 'height="1000"', x, count=1).replace("<hh:bold/>", "").replace("<hh:italic/>", ""))
# 'N.' 뒤 탭(19pt 자리) → '󰂼 '(15pt) 뒤 34pt에서 정답 시작, 내어쓰기 34pt로 둘째 줄(따름 문제 (2)…)도 (1)과 같은 자리
TABPOS, HANG = 1900, 3400
TAB_ITEM = ('<hp:switch><hp:case hp:required-namespace="http://www.hancom.co.kr/hwpml/2016/HwpUnitChar"><hh:tabItem pos="%d" type="LEFT" leader="NONE" unit="HWPUNIT"/></hp:case>'
            '<hp:default><hh:tabItem pos="%d" type="LEFT" leader="NONE"/></hp:default></hp:switch>' % (TABPOS, TABPOS * 2))
TP_A = max(int(x) for x in re.findall(r'<hh:tabPr id="(\d+)"', head)) + 1          # 탭 모양(빈 꼴 <hh:tabPr …/>가 있어 add_item 대신 직접)
_e = head.index("</hh:tabProperties>")
head = head[:_e] + '<hh:tabPr id="%d" autoTabLeft="0" autoTabRight="0">%s</hh:tabPr>' % (TP_A, TAB_ITEM) + head[_e:]
head = re.sub(r'<hh:tabProperties itemCnt="(\d+)"', lambda m: '<hh:tabProperties itemCnt="%d"' % (int(m.group(1)) + 1), head, count=1)
src_pp = re.search(r'<hp:endNote .*?<hp:p [^>]*paraPrIDRef="(\d+)"', sec, re.S).group(1)      # 원래 미주 정답 문단 모양
head, PP_A = add_item(head, "paraPr", "paraProperties", src_pp,
                      lambda x: re.sub(r'tabPrIDRef="\d+"', 'tabPrIDRef="%d"' % TP_A,
                                       margins(re.sub(r'horizontal="[A-Z_]+"', 'horizontal="LEFT"', x), -HANG, 0, 250), count=1))
# 단원 띠
band_rect = re.search(r"<hp:rect\b(?:(?!<hp:rect\b).)*?faceColor=\"#008000\".*?</hp:rect>", msec, re.S).group(0)
if BOOK == "c1c":
    band_run_cp = re.search(r'<hp:run charPrIDRef="(\d+)">(?:(?!<hp:run ).)*?faceColor="#008000"', sec, re.S).group(1)
    inner_pp = re.search(r'<hp:drawText\b.*?<hp:p [^>]*paraPrIDRef="(\d+)"', band_rect, re.S).group(1)
    head, PP_BT = add_item(head, "paraPr", "paraProperties", inner_pp,
                           lambda x: re.sub(r'<hh:heading type="NUMBER" idRef="\d+" level="\d+"/>', '<hh:heading type="NONE" idRef="0" level="0"/>', x))
else:
    # 띠 안 글자 모양(흰 14pt HY울릉도M 등)을 본책 머리에서 글꼴째 옮김, 띠 문단은 가운데 정렬
    band_run_cp = None
    inner_cp = re.search(r'<hp:drawText\b.*?<hp:run charPrIDRef="(\d+)"', band_rect, re.S).group(1)
    cx = re.search(r'<hh:charPr id="%s".*?</hh:charPr>' % inner_cp, mhead, re.S).group(0)
    LANGS = ("HANGUL", "LATIN", "HANJA", "JAPANESE", "OTHER", "SYMBOL", "USER")
    fr = dict(re.findall(r'(\w+)="(\d+)"', re.search(r"<hh:fontRef ([^/]*)/>", cx).group(1)))
    newref = {}
    for lang in LANGS:
        mf = re.search(r'<hh:fontface lang="%s".*?</hh:fontface>' % lang, mhead, re.S).group(0)
        face_xml = re.search(r'<hh:font id="%s" .*?</hh:font>' % fr[lang.lower()], mf, re.S).group(0)
        face = re.search(r'face="([^"]+)"', face_xml).group(1)
        m = re.search(r'(<hh:fontface lang="%s" fontCnt=")(\d+)(">)(.*?)(</hh:fontface>)' % lang, head, re.S)
        have = dict((b, a) for a, b in re.findall(r'<hh:font id="(\d+)" face="([^"]+)"', m.group(4)))
        if face not in have:
            n_ = int(m.group(2))
            head = head[:m.start()] + m.group(1) + str(n_ + 1) + m.group(3) + m.group(4) + re.sub(r'id="\d+"', 'id="%d"' % n_, face_xml, count=1) + m.group(5) + head[m.end():]
            have[face] = str(n_)
        newref[lang.lower()] = have[face]
    cx = re.sub(r"<hh:fontRef [^/]*/>", "<hh:fontRef %s/>" % " ".join('%s="%s"' % (l, newref[l]) for l in [x.lower() for x in LANGS]), cx)
    cx = re.sub(r'borderFillIDRef="\d+"', 'borderFillIDRef="1"', cx, count=1)
    CP_BT = max(int(x) for x in re.findall(r'<hh:charPr id="(\d+)"', head)) + 1
    _e = head.index("</hh:charProperties>")
    head = head[:_e] + re.sub(r'id="\d+"', 'id="%d"' % CP_BT, cx, count=1) + head[_e:]
    head = re.sub(r'<hh:charProperties itemCnt="(\d+)"', lambda m: '<hh:charProperties itemCnt="%d"' % (int(m.group(1)) + 1), head, count=1)
    band_rect = re.sub(r'(<hp:drawText\b.*?<hp:run charPrIDRef=")\d+', lambda m: m.group(1) + str(CP_BT), band_rect, count=1, flags=re.S)
    head, PP_BT = add_item(head, "paraPr", "paraProperties", src_pp,
                           lambda x: margins(re.sub(r'horizontal="[A-Z_]+"', 'horizontal="CENTER"', x), 0, 0, 100))
head, PP_B = add_item(head, "paraPr", "paraProperties", src_pp,
                      lambda x: margins(re.sub(r'horizontal="[A-Z_]+"', 'horizontal="LEFT"', x), 0, 1200, 100))
files["Contents/header.xml"] = head.encode("utf-8")

# 바탕쪽: 단원 이름 자리에 '빠른 정답'
for n in list(files):
    if re.match(r"Contents/masterpage\d+\.xml", n):
        mx = files[n].decode("utf-8")
        mx = mx.replace("<hp:t>%s</hp:t>" % UNITS[0], "<hp:t>빠른 정답</hp:t>").replace("<hp:t>1.</hp:t>", "<hp:t></hp:t>")
        mx = mx.replace("<hp:t>1. %s</hp:t>" % UNITS[0], "<hp:t>빠른 정답</hp:t>")          # 워크북 바탕쪽은 '1. 다항식의 연산' 한 덩어리
        files[n] = mx.encode("utf-8")

# 첫 문단(구역 정의·단 정의·꼬리말)
i0 = sec.index("<hp:p ")
d, j = 0, i0
for m in re.finditer(r"<hp:p [^>]*>|</hp:p>", sec[i0:]):
    d += 1 if m.group(0).startswith("<hp:p ") else -1
    if d == 0:
        j = i0 + m.end()
        break
p0 = sec[i0:j]
run0 = re.match(r"<hp:p [^>]*><hp:run [^>]*>", p0).group(0)
keep = re.search(r"<hp:secPr\b.*?</hp:secPr>", p0, re.S).group(0)
keep += "".join(m.group(0) for m in re.finditer(r"<hp:ctrl><hp:(?:colPr|pageNum)\b(?:(?!</hp:ctrl>).)*</hp:ctrl>|<hp:ctrl><hp:(footer|header)\b.*?</hp:\1></hp:ctrl>", p0, re.S))
if START:
    keep += '<hp:ctrl><hp:newNum num="%d" numType="PAGE"/></hp:ctrl>' % START
first_open = re.sub(r'paraPrIDRef="\d+"', 'paraPrIDRef="%d"' % PP_B, run0, count=1)
first_open = re.sub(r'styleIDRef="\d+"', 'styleIDRef="0"', first_open, count=1)
NID = [3400000000]
EQID = [3500000000]


def nid():
    NID[0] += 1
    return str(NID[0])


def band(u, name):
    r = band_rect
    r = re.sub(r'(<hp:rect\b[^>]*?\bid=")\d+', lambda m: m.group(1) + nid(), r, count=1)
    r = re.sub(r'(<hp:rect\b[^>]*?\binstid=")\d+', lambda m: m.group(1) + nid(), r, count=1)
    r = re.sub(r"(<hp:drawText\b.*?<hp:p [^>]*?)paraPrIDRef=\"\d+\"", lambda m: m.group(1) + 'paraPrIDRef="%d"' % PP_BT, r, count=1, flags=re.S)
    r = re.sub(r"<hp:linesegarray>.*?</hp:linesegarray>", "", r, flags=re.S)
    r = re.sub(r"(<hp:drawText\b.*?<hp:t>).*?(</hp:t>)", lambda m: m.group(1) + html.escape("%d. %s" % (u, name)) + m.group(2), r, count=1, flags=re.S)
    return '<hp:run charPrIDRef="%s">%s</hp:run><hp:run charPrIDRef="%d"><hp:t/></hp:run>' % (band_run_cp or CP_A, r, CP_A)


W_COL = (72852 - 4535 - 4535 - 2267 - 2268) // 2       # 단 너비(쪽 너비 − 왼쪽·오른쪽 여백 − 제본 여백 − 단 사이) ÷ 2


def eqfix(e):
    EQID[0] += 1
    e = re.sub(r'(<hp:equation\b[^>]*?\bid=")\d+', lambda m: m.group(1) + str(EQID[0]), e, count=1)
    bu = int(re.search(r'baseUnit="(\d+)"', e).group(1))
    if bu != 1000:                                  # 정답 글자(10pt)와 같은 크기로
        k0 = 1000 / bu
        e = re.sub(r'baseUnit="\d+"', 'baseUnit="1000"', e, count=1)
        e = re.sub(r'<hp:sz width="(\d+)" widthRelTo="ABSOLUTE" height="(\d+)"',
                   lambda q: '<hp:sz width="%d" widthRelTo="ABSOLUTE" height="%d"' % (int(int(q.group(1)) * k0), int(int(q.group(2)) * k0)), e, count=1)
    m = re.search(r'<hp:sz width="(\d+)" widthRelTo="ABSOLUTE" height="(\d+)"', e)
    avail = W_COL - HANG - 600
    if m and int(m.group(1)) > avail:              # 단보다 넓은 수식은 줄여서 맞춤
        k = avail / int(m.group(1))
        e = re.sub(r'<hp:sz width="\d+" widthRelTo="ABSOLUTE" height="\d+"',
                   '<hp:sz width="%d" widthRelTo="ABSOLUTE" height="%d"' % (avail, int(int(m.group(2)) * k)), e, count=1)
        e = re.sub(r'baseUnit="(\d+)"', lambda q: 'baseUnit="%d"' % int(int(q.group(1)) * k), e, count=1)
    return e


def ans_para(no, ls):
    parts = ['<hp:t>%d.<hp:tab width="%d" leader="0" type="1"/></hp:t>' % (no, TABPOS - (1000 if no > 9 else 500))]
    for li, ln in enumerate(ls):
        if li:
            parts.append("<hp:t><hp:lineBreak/></hp:t>")
        for k, v in ln:
            if k == "t":
                parts.append("<hp:t>%s</hp:t>" % v)
            elif k in ("tab", "x"):
                parts.append("<hp:t>%s</hp:t>" % v)
            elif k == "eq":
                parts.append(eqfix(v))
            elif k == "other":
                parts.append(v)
    return ('<hp:p id="%s" paraPrIDRef="%d" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0"><hp:run charPrIDRef="%d">%s<hp:t/></hp:run></hp:p>'
            % (nid(), PP_A, CP_A, "".join(parts)))


body = []
total = 0
for k, (u, name, ans) in enumerate(data):
    if k == 0:
        body.append(sec[:i0] + first_open + keep + "<hp:t/></hp:run>" + band(u, name) + "</hp:p>")
    else:
        body.append('<hp:p id="%s" paraPrIDRef="%d" styleIDRef="0" pageBreak="1" columnBreak="0" merged="0">%s</hp:p>' % (nid(), PP_B, band(u, name)))
    for n, ls in ans:
        body.append(ans_para(n, ls))
    total += len(ans)
files["Contents/section0.xml"] = ("".join(body) + "</hs:sec>").encode("utf-8")
if "Preview/PrvText.txt" in files:
    files["Preview/PrvText.txt"] = ("CLIMATH(c) 공통수학1 %s빠른 정답" % ("워크북 " if BOOK == "c1w" else "")).encode("utf-8")
with zipfile.ZipFile(OUT, "w") as w:
    for n in NAMES:
        info = zipfile.ZipInfo(n, date_time=(1980, 1, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_STORED if n == "mimetype" else zipfile.ZIP_DEFLATED
        w.writestr(info, files[n])
multi = sum(1 for _, _, a in data for _, ls in a if len(ls) > 1)
print("단원", len(data), "문항", total, "여러 줄 정답", multi, "->", OUT)
