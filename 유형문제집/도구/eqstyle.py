# -*- coding: utf-8 -*-
"""공통수학2 수식 표기 기준(사용자 5·6단원 완성본, 2026-11-10)을 hwpx의 수식에 입힌다.

사용자가 5·6단원 기본서·유형서 완성본에서 고친 방식:
  1. 여집합: A^{C} → A^{∁} (U+2201 여집합 기호)
  2. 조건제시법의 세로줄: LEFT { x`vert`… RIGHT } → LEFT { x left| … RIGHT }
  3. 조건 속 한글은 수식 밖 글자로: 'U=LEFT { x`vert`x는~10~이하의~자연수 RIGHT }'
       → 수식 'U=LEFT { x left| x' + 글자 '는 ' + 수식 '10' + 글자 '이하의 자연수' + 수식 'it right'
     (조건이 수식으로 끝나면 마지막 수식에 'RIGHT }'를 그대로 둔다: 수식 'X=LEFT { x left| x in A' + 글자 '이고 ' + 수식 'x notin B RIGHT }')
  4. 합의 줄임표: s_{1} + CDOTS +s_{n} → s_{1} + it CDOTS it +s_{n} (목록 '1,~2,~CDOTS,~10'은 그대로)
  5. 수식 바로 뒤의 '이하·이상·미만·초과·또는·그리고' 앞은 한 칸 띄운다: '10 이하의 자연수' (사용자 요청 2026-11-10)

python eqstyle.py 파일.hwpx [...]   (그 자리에서 고친다)
gen.py(DESIGN="c2")와 기본서2/compose01.py가 저장할 때 자동으로 부른다.
cases·pile·행렬처럼 여러 줄인 수식, 괄호 안({…})에 든 한글은 나누지 않고 그대로 둔다(1·2·4만 적용).
"""
import re, sys, os, json, shutil, zipfile, html

HERE = os.path.dirname(os.path.abspath(__file__))
HANGUL = r"[가-힣]"
KOR = re.compile(r"([가-힣]+(?:[~`\s]*[가-힣]+)*)")
SEP = "~` \t"


# ---------------------------------------------------------------- 스크립트 단위
def simple(sc):
    """1·2·4: 한 수식 안에서 바꾸기"""
    s = re.sub(r"\^\s*\{\s*`?\s*C\s*\}", "^{∁}", sc)
    # 조건제시법 세로줄: LEFT { 원소 `vert` 조건 — LEFT { 와 vert 사이에 다른 괄호가 없을 때
    s = re.sub(r"(LEFT\s*\{(?:[^{}|]|\{[^{}]*\})*?)\s*`?\s*\bvert\b\s*`?\s*", r"\1 left| ", s)
    s = re.sub(r"\+\s*(?:it\s+)?CDOTS\s*(?:it\s*)?\+", "+ it CDOTS it +", s)
    return s


def _depth_ok(s, spans):
    """한글 조각이 모두 중괄호(LEFT{·RIGHT} 제외) 밖에 있는지"""
    depth, d = 0, []
    i = 0
    marks = {}
    for m in re.finditer(r"(LEFT|RIGHT|left|right)\s*([{}])", s):
        marks[m.end() - 1] = True
    for i, ch in enumerate(s):
        d.append(depth)
        if ch == "{" and i not in marks:
            depth += 1
        elif ch == "}" and i not in marks:
            depth -= 1
    return all(d[a] == 0 for a, b in spans)


def split(sc):
    """3: 한글이 든 조건제시법 수식을 [('eq', 수식), ('t', 글자), ...]로. 나눌 수 없으면 None"""
    if not re.search(HANGUL, sc) or not re.search(r"\bleft\s*\|", sc):
        return None
    if re.search(r"\b(cases|pile|lpile|rpile|matrix|pmatrix|bmatrix|dmatrix)\b|#", sc):
        return None
    spans = [m.span() for m in KOR.finditer(sc)]
    if not _depth_ok(sc, spans):
        return None
    parts = KOR.split(sc)          # 수식, 한글, 수식, 한글, ..., 수식
    out = []
    n = len(parts)
    for i, p in enumerate(parts):
        if i % 2 == 1:              # 한글
            t = re.sub(r"[~`\s]+", " ", p)
            nxt = parts[i + 1]
            m = re.match(r"[~`\s]*([,.])?[~`\s]*", nxt)
            if m.group(1):
                t += m.group(1) + " "
            elif m.group(0):
                t += " "
            parts[i + 1] = nxt[m.end():]
            out.append(["t", t])
        else:                       # 수식
            e = p.rstrip(SEP)
            if i == n - 1 and re.fullmatch(r"\s*RIGHT\s*\}\s*", e):
                e = "it right"
            e = e.strip(SEP)
            if e:
                out.append(["eq", e])
    # 붙은 글자 조각 합치기, 끝 글자 뒤 빈칸 정리
    res = []
    for k, v in out:
        if res and res[-1][0] == k == "t":
            res[-1][1] += v
        else:
            res.append([k, v])
    for i, (k, v) in enumerate(res):      # 닫는 수식 'it right' 앞·문단 끝 글자는 뒤 빈칸 없이(사용자 완성본)
        if k == "t" and (i == len(res) - 1 or res[i + 1][1] == "it right"):
            res[i][1] = v.rstrip()
    return [tuple(x) for x in res]


def style_script(sc):
    """수식 하나 -> (바뀐 수식) 또는 [조각들]"""
    s = simple(sc)
    p = split(s)
    return p if p else s


# ---------------------------------------------------------------- 크기(gen.py와 같은 식)
CACHE = os.path.join(HERE, "eqcache.json")


def sizes(scripts):
    EQ = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
    todo = sorted(set(s for s in scripts if s not in EQ))
    if todo:
        from eqmeasure import measure
        res, latex = measure(todo)
        for sc, r in zip(todo, res):
            if r[3]:
                r = [0.62 * len(sc) * 16 / 1.6, 18, 14, None]
            w, h, asc = r[0], r[1], r[2]
            W = int(68.8 * w + 61)
            if h > 20.5:
                H = int(max(1125, 57.14 * h + 303))
            elif "sqrt" in sc or "root" in sc:
                H = 1538
            elif "_" in sc:
                H = 1350
            elif "^" in sc:
                H = 1313
            else:
                H = 1125
            BL = int(max(50, min(90, 111.7 * (asc / h) - 2.6))) if h else 85
            EQ[sc] = (W, H, BL)
        json.dump(EQ, open(CACHE, "w"), ensure_ascii=False)
    return EQ


# ---------------------------------------------------------------- hwpx
EQPAT = re.compile(r"<hp:equation\b[^>]*>.*?</hp:equation>", re.S)
SCPAT = re.compile(r"(<hp:script\b[^>]*>)(.*?)(</hp:script>)", re.S)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# 5. 수식 바로 뒤에 오는 낱말(조사가 아닌 것) 앞은 띄운다: '10 이하의 자연수', 'x<-6 또는 x>-2' (2026-11-10 사용자 요청 '숫자와 한글 사이에 빈칸')
SPACE_WORDS = ("이하", "이상", "미만", "초과", "또는", "그리고")
SPACE = re.compile(r"(</hp:equation>(?:</hp:run><hp:run\b[^>]*>)?<hp:t>)((?:%s))" % "|".join(SPACE_WORDS))


def style_xml(xml, stat=None):
    stat = stat if stat is not None else {}
    ids = [int(x) for x in re.findall(r'<hp:equation\b[^>]*\bid="(\d+)"', xml)]
    nid = [max(ids + [1700000000]) + 1]
    plan = []
    for m in EQPAT.finditer(xml):
        sm = SCPAT.search(m.group(0))
        if not sm:
            continue
        sc = html.unescape(sm.group(2))
        new = style_script(sc)
        if new != sc:
            plan.append((m, sm, sc, new))
    need = [p for _, _, _, new in plan if isinstance(new, list) for k, p in new if k == "eq"]
    EQ = sizes(need) if need else {}
    out, last = [], 0
    for m, sm, sc, new in plan:
        out.append(xml[last:m.start()])
        el = m.group(0)
        if isinstance(new, str):
            stat["simple"] = stat.get("simple", 0) + 1
            el = el[:sm.start(2)] + esc(new) + el[sm.end(2):]
            out.append(el)
        else:
            stat["split"] = stat.get("split", 0) + 1
            pieces = []
            for k, v in new:
                if k == "t":
                    pieces.append("<hp:t>%s</hp:t>" % esc(v))
                    continue
                W, H, BL = EQ[v]
                e = re.sub(r'(<hp:equation\b[^>]*\bid=")\d+(")', lambda q: q.group(1) + str(nid[0]) + q.group(2), el, count=1)
                nid[0] += 1
                e = re.sub(r'(<hp:equation\b[^>]*\bbaseLine=")\d+(")', lambda q: q.group(1) + str(BL) + q.group(2), e, count=1)
                e = re.sub(r'(<hp:sz\b[^>]*\bwidth=")\d+(")', lambda q: q.group(1) + str(W) + q.group(2), e, count=1)
                e = re.sub(r'(<hp:sz\b[^>]*\bheight=")\d+(")', lambda q: q.group(1) + str(H) + q.group(2), e, count=1)
                s2 = SCPAT.search(e)
                e = e[:s2.start()] + "<hp:script>" + esc(v) + "</hp:script>" + e[s2.end():]
                pieces.append(e)
            out.append("".join(pieces))
        last = m.end()
    out.append(xml[last:])
    xml2, k = SPACE.subn(lambda m: m.group(1) + " " + m.group(2), "".join(out))
    if k:
        stat["space"] = stat.get("space", 0) + k
    return xml2, stat


def style_file(path):
    zin = zipfile.ZipFile(path)
    items = [(i, zin.read(i.filename)) for i in zin.infolist()]
    zin.close()
    stat = {}
    out = []
    for info, data in items:
        if info.filename.startswith("Contents/section") and info.filename.endswith(".xml"):
            xml, stat = style_xml(data.decode("utf-8"), stat)
            data = xml.encode("utf-8")
        out.append((info, data))
    if stat:
        tmp = path + ".tmp"
        with zipfile.ZipFile(tmp, "w") as z:
            for info, data in out:
                z.writestr(info, data, compress_type=info.compress_type)
        shutil.move(tmp, path)
    return stat


if __name__ == "__main__":
    for p in sys.argv[1:]:
        print(style_file(p), p)
