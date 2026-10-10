# -*- coding: utf-8 -*-
"""기본서 문항 고치기: 문제 글/수식 바꾸기, 해설(미주) 새로 쓰기, 시험지 흔적 지우기"""
import re, collections
from xml.sax.saxutils import escape
import hwpxio as io, numbering as nb, eqsize

ENDNOTE = re.compile(r"<hp:endNote .*?</hp:endNote>", re.S)


class Doc:
    """한 문서 안의 해설 모양 본보기"""

    def __init__(self, P):
        self.P = P
        firsts, lines, eqs = collections.Counter(), collections.Counter(), []
        for p in P:
            for en in ENDNOTE.findall(p):
                ps = re.findall(r"<hp:p [^>]*>.*?</hp:p>", en, re.S)
                if not ps:
                    continue
                if "󰂼" in ps[0]:
                    m = re.match(r'(<hp:p [^>]*>)<hp:run charPrIDRef="(\d+)">', ps[0])
                    firsts[(m.group(1), m.group(2))] += 1
                for q in ps[1:]:
                    m = re.match(r'(<hp:p [^>]*>)<hp:run charPrIDRef="(\d+)">', q)
                    if m and "<hp:equation" in q:
                        lines[(m.group(1), m.group(2))] += 1
                        eqs += re.findall(r"<hp:equation [^>]*>", q)
        self.first = firsts.most_common(1)[0][0]
        self.line = lines.most_common(1)[0][0]
        body_eqs = [e for p in P for e in re.findall(r"<hp:equation [^>]*>", ENDNOTE.sub("", p))]
        self.body_base = int(collections.Counter(re.search(r'baseUnit="(\d+)"', e).group(1) for e in body_eqs).most_common(1)[0][0])
        bases = collections.Counter(re.search(r'baseUnit="(\d+)"', e).group(1) for e in eqs)
        self.base = int(bases.most_common(1)[0][0])
        self.eq_open = collections.Counter(re.sub(r'\bid="\d+"', 'id="0"', re.sub(r'zOrder="\d+"', 'zOrder="0"', e))
                                           for e in eqs).most_common(1)[0][0]

    def eq(self, sc, base=None):
        base = base or self.base
        W, H, BL = eqsize.size(sc, base)
        op = re.sub(r'baseLine="\d+"', 'baseLine="%d"' % BL, self.eq_open)
        op = re.sub(r'baseUnit="\d+"', 'baseUnit="%d"' % base, op)
        return (op + '<hp:sz width="%d" widthRelTo="ABSOLUTE" height="%d" heightRelTo="ABSOLUTE" protect="0"/>'
                '<hp:pos treatAsChar="1" affectLSpacing="0" flowWithText="1" allowOverlap="0" holdAnchorAndSO="0" '
                'vertRelTo="PARA" horzRelTo="PARA" vertAlign="TOP" horzAlign="LEFT" vertOffset="0" horzOffset="0"/>'
                '<hp:outMargin left="56" right="56" top="0" bottom="0"/><hp:shapeComment>수식입니다.</hp:shapeComment>'
                '<hp:script>%s</hp:script></hp:equation>') % (W, H, escape(sc))

    def inline(self, text, base=None):
        out = []
        for i, part in enumerate(re.split(r"\$(.+?)\$", text)):
            if i % 2:
                out.append(self.eq(part, base))
            elif part:
                out.append("<hp:t>%s</hp:t>" % escape(part))
        return "".join(out) or "<hp:t/>"

    def endnote_body(self, old_en, lines):
        """lines[0]: '󰂼 ②' 같은 정답 표시, 나머지: 풀이 줄"""
        auto = re.search(r"<hp:ctrl><hp:autoNum .*?</hp:ctrl>", old_en, re.S).group(0)
        ph, pc = self.first
        first = '%s<hp:run charPrIDRef="%s">%s%s</hp:run></hp:p>' % (ph, pc, auto, self.inline(" " + lines[0]))
        lh, lc = self.line
        rest = "".join('%s<hp:run charPrIDRef="%s">%s</hp:run></hp:p>' % (lh, lc, self.inline(l)) for l in lines[1:])
        a = old_en.index(">", old_en.index("<hp:subList")) + 1
        b = old_en.rindex("</hp:subList>")
        return old_en[:a] + first + rest + old_en[b:]


def scripts_of(lines):
    out = []
    for l in lines:
        out += [m.strip() for m in re.findall(r"\$(.+?)\$", l)]
    return out


def resize_eq(eqxml, base_default):
    sc = re.search(r"<hp:script[^>]*>(.*?)</hp:script>", eqxml, re.S).group(1)
    from xml.sax.saxutils import unescape
    sc_u = unescape(sc)
    eqsize.ensure([sc_u])
    base = int(re.search(r'baseUnit="(\d+)"', eqxml).group(1)) if 'baseUnit="' in eqxml else base_default
    W, H, BL = eqsize.size(sc_u, base)
    eqxml = re.sub(r'(<hp:sz width=")\d+(" widthRelTo="ABSOLUTE" height=")\d+', lambda m: m.group(1) + str(W) + m.group(2) + str(H), eqxml, count=1)
    return eqxml


def _replace_in(x, old, new, doc, mode="any"):
    """x 안에서 old를 new로(수식이면 크기를 다시 잼). 바뀐 개수를 돌려준다."""
    if old.startswith("$") and old.endswith("$"):
        o, n = escape(old[1:-1]), escape(new[1:-1])
        eqs = list(re.finditer(r"<hp:equation .*?</hp:equation>", x, re.S))

        def script(m):
            return re.search(r"<hp:script[^>]*>(.*?)</hp:script>", m.group(0), re.S).group(1)
        exact = [m for m in eqs if script(m).strip() == o.strip()]
        sub = [m for m in eqs if o in script(m)]
        hit = exact if mode == "exact" else sub if mode == "sub" else (exact or sub)
        if not hit:
            return x, 0
        m = hit[0]
        sc = script(m)
        new_sc = n if sc.strip() == o.strip() else sc.replace(o, n, 1)
        neq = m.group(0).replace(">" + sc + "</hp:script>", ">" + new_sc + "</hp:script>", 1)
        return x[:m.start()] + resize_eq(neq, doc.base) + x[m.end():], 1
    o = escape(old)
    if "$" in new:
        # 글 속에 수식을 넣을 때: 글자 요소를 닫고 수식을 끼운 뒤 다시 연다
        parts = re.split(r"\$(.+?)\$", new)
        n = "".join(("</hp:t>" + doc.eq(q, doc.body_base) + "<hp:t>") if i % 2 else escape(q) for i, q in enumerate(parts))
    else:
        n = escape(new)
    if o in x:
        return x.replace(o, n, 1), 1
    return x, 0


def apply(P, fixes, label=""):
    """fixes: {k(미주 순서): [작업, ...]}"""
    doc = Doc(P)
    all_sc = []
    for ops in fixes.values():
        for op in ops:
            if op[0] == "sol":
                all_sc += scripts_of(op[1])
            elif op[0] == "ans":
                all_sc += scripts_of([op[1]])
            elif op[0] == "qtext":
                all_sc += scripts_of([op[2]])
            elif op[0] in ("q", "solrep") and not op[2].startswith("$"):
                all_sc += scripts_of([op[2]])
    eqsize.ensure(all_sc)
    segs = nb.segments(P)
    E = [e for _, e in segs]
    drop = set()
    log = []
    for k, ops in fixes.items():
        a, e = segs[k - 1]
        b = e
        while b + 1 < len(P) and not nb.blank(P[b + 1]) and not nb.is_heading(P[b + 1]) and "<hp:endNote " not in P[b + 1]:
            b += 1
        rng = list(range(a, b + 1))
        for op in ops:
            kind = op[0]
            if kind == "sol":
                en = ENDNOTE.search(P[e]).group(0)
                P[e] = P[e].replace(en, doc.endnote_body(en, op[1]), 1)
                ok = 1
            elif kind == "ans":
                # 해설 첫 문단(정답 표시)만 바꾼다
                en = ENDNOTE.search(P[e]).group(0)
                a1 = en.index(">", en.index("<hp:subList")) + 1
                fp = re.match(r"<hp:p [^>]*>.*?</hp:p>", en[a1:], re.S).group(0)
                auto = re.search(r"<hp:ctrl><hp:autoNum .*?</hp:ctrl>", fp, re.S).group(0)
                ph, pc = doc.first
                newfp = '%s<hp:run charPrIDRef="%s">%s%s</hp:run></hp:p>' % (ph, pc, auto, doc.inline(" " + op[1]))
                P[e] = P[e].replace(en, en[:a1] + newfp + en[a1 + len(fp):], 1)
                ok = 1
            elif kind in ("q", "solrep"):
                ok = 0
                modes = ["exact", "sub"] if op[1].startswith("$") else ["any"]
                for mode in modes:
                    if ok:
                        break
                    for i in rng:
                        p = P[i]
                        en = ENDNOTE.search(p)
                        if kind == "q":
                            body = ENDNOTE.sub("\x00", p)
                            body, c = _replace_in(body, op[1], op[2], doc, mode)
                            if c:
                                P[i] = body.replace("\x00", en.group(0)) if en else body
                                ok = 1
                                break
                        elif en:
                            new, c = _replace_in(en.group(0), op[1], op[2], doc, mode)
                            if c:
                                P[i] = p.replace(en.group(0), new, 1)
                                ok = 1
                                break
            elif kind == "deleq":
                # ("deleq", "q"|"sol", 수식) : 그 수식 개체를 지운다(정확히 같은 것)
                ok = 0
                for i in rng:
                    p = P[i]
                    en = ENDNOTE.search(p)
                    part = (en.group(0) if en else "") if op[1] == "sol" else ENDNOTE.sub("\x00", p)
                    for m in re.finditer(r"<hp:equation .*?</hp:equation>", part, re.S):
                        sc = re.search(r"<hp:script[^>]*>(.*?)</hp:script>", m.group(0), re.S).group(1)
                        if sc.strip() == escape(op[2]).strip():
                            newpart = part[:m.start()] + part[m.end():]
                            if op[1] == "sol":
                                P[i] = p.replace(en.group(0), newpart, 1)
                            else:
                                P[i] = newpart.replace("\x00", en.group(0)) if en else newpart
                            ok = 1
                            break
                    if ok:
                        break
            elif kind == "drop":
                # 문항 전체(번호 문단부터 다음 문항 직전까지, 제목 문단은 남김)를 지운다
                nxt = segs[k][0] if k < len(segs) else len(P)
                j = a
                while j < nxt and not nb.is_heading(P[j]) and not ("<hp:rect" in P[j] and re.search(r"[0-9]\. ", io.text(P[j]))):
                    drop.add(j)
                    j += 1
                ok = 1
            elif kind == "soldel":
                # ("soldel", 글귀): 해설(미주)에서 글귀가 든 문단을 지운다 ([출제의도] 같은 시험지 흔적)
                en = ENDNOTE.search(P[e]).group(0)
                ps = re.findall(r"<hp:p [^>]*>.*?</hp:p>", en, re.S)
                hit = [q for q in ps[1:] if op[1] in io.text(q)]
                ok = int(bool(hit))
                if hit:
                    P[e] = P[e].replace(en, en.replace(hit[0], "", 1), 1)
            elif kind == "qtext":
                # ("qtext", 글귀, 새 문장): 글귀가 든 문제 문단의 내용을 새 문장으로 바꾼다(미주는 그대로 둠)
                ok = 0
                for i in rng:
                    p = P[i]
                    if op[1] in io.text(ENDNOTE.sub("", p)):
                        head = re.match(r"<hp:p [^>]*>", p).group(0)
                        c = re.search(r'<hp:run charPrIDRef="(\d+)">', p).group(1)
                        enrun = re.search(r'<hp:run charPrIDRef="\d+"><hp:ctrl><hp:endNote .*?</hp:endNote></hp:ctrl>.*?</hp:run>', p, re.S)
                        P[i] = (head + '<hp:run charPrIDRef="%s">%s</hp:run>' % (c, doc.inline(op[2], doc.body_base))
                                + (enrun.group(0) if enrun else "") + "</hp:p>")
                        ok = 1
                        break
            elif kind == "delpara":
                ok = 0
                for i in rng:
                    if op[1] in io.text(P[i]) and "<hp:endNote " not in P[i]:
                        drop.add(i)
                        ok = 1
                        break
            else:
                raise ValueError(op)
            log.append((label, k, kind, op[1] if kind not in ("sol", "drop") else (op[1][0] if kind == "sol" else ""), ok))
            if not ok:
                print("적용 실패:", label, k, op[:3])
    P = [p for i, p in enumerate(P) if i not in drop]
    bad = [l for l in log if not l[-1]]
    for l in bad:
        print("적용 실패:", l)
    return P, log
