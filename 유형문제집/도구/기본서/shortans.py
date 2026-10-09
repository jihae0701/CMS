# -*- coding: utf-8 -*-
"""기본서 5지선다를 단답형으로 바꾼다.

- 선지 문단(①…, ④…)을 지우고, 그 안에 미주가 있으면 발문 문단 끝으로 옮긴다.
- 발문 끝 「~은?/~는?」을 「~을/를 구하시오.」로 바꾼다.
- 해설의 정답 표시 「󰂼 ③」을 그 선지의 값 「󰂼 (수식)」으로 바꾼다.
keep: 5지선다를 유지할 문항 번호(문서 안 미주 순서, 1부터)
"""
import re
from xml.sax.saxutils import escape
import hwpxio as io, numbering as nb, eqsize

CIRC = "①②③④⑤"
EN = re.compile(r"<hp:endNote .*?</hp:endNote>", re.S)


def _choices(P, rng):
    """선지 문단 번호와 {번호: 수식} 사전"""
    idx, vals = [], {}
    for i in rng:
        body = EN.sub("", P[i])
        t = io.text(body).strip()
        if t[:1] in ("①", "④"):
            idx.append(i)
            # 선지 기호 뒤의 첫 수식(또는 글)을 값으로
            for m in re.finditer(r"([①②③④⑤])\s*((?:\$[^$]*\$)+|[^①②③④⑤]+)", t):
                vals[CIRC.index(m.group(1)) + 1] = m.group(2).strip()
    return idx, vals


def convert(P, doc, keep=()):
    segs = nb.segments(P)
    drop, log = set(), []
    for k, (a, e) in enumerate(segs, 1):
        if k in keep:
            continue
        nxt = segs[k][0] if k < len(segs) else len(P)
        stop = next((i for i in range(a + 1, nxt) if nb.is_heading(P[i])), nxt)   # 다음 유형 제목에서 멈춤
        rng = list(range(a, stop))
        cidx, vals = _choices(P, rng)
        if not cidx:
            continue
        en = EN.search(P[e]).group(0)
        m = re.search(r"󰂼\s*([①②③④⑤])", io.text(en))
        if not m:
            log.append((k, "정답 표시 없음"))
            continue
        val = vals.get(CIRC.index(m.group(1)) + 1, "")
        sc = "".join(re.findall(r"\$([^$]*)\$", val)).strip()
        if not sc and re.fullmatch(r"-?\d+", val.strip()):      # 보기가 수식이 아닌 글자 숫자
            sc, val = val.strip(), "$%s$" % val.strip()
        if not sc or len(re.findall(r"\$", val)) != 2:
            log.append((k, "값 읽기 실패", val))
            continue
        # 1) 정답 표시: 󰂼 ③ -> 󰂼 (수식)
        eqsize.ensure([sc])
        def ans(mm):
            return mm.group(1) + "</hp:t>" + doc.eq(sc) + "<hp:t>"
        new_en = re.sub(r"(<hp:t>[^<]*?󰂼\s*)[①②③④⑤]", ans, en, count=1)
        if new_en == en:
            # 󰂼와 ③이 서로 다른 글자 요소에 있을 때
            i0 = en.index("󰂼")
            mm = re.compile(r"[①②③④⑤]").search(en, i0)
            if mm and mm.start() - i0 < 300:
                new_en = en[:mm.start()] + "</hp:t>" + doc.eq(sc) + "<hp:t>" + en[mm.end():]
        if new_en == en:
            log.append((k, "정답 표시 바꾸기 실패"))
            continue
        P[e] = P[e].replace(en, new_en, 1)
        en = new_en
        # 2) 발문: 마지막 '?' 문단
        qs = [i for i in rng if i not in cidx and "?" in io.text(EN.sub("", P[i]))]
        if not qs:
            log.append((k, "발문 못 찾음"))
            continue
        qi = qs[-1]
        def ask(mm):
            j = {"은": "을", "는": "를"}[mm.group(1)]
            return j + " 구하시오."
        body = EN.sub("\x00", P[qi])
        nb_ = re.sub(r"([은는])\?", ask, body, count=1)
        if nb_ == body:
            log.append((k, "발문 바꾸기 실패", io.text(body)[-30:]))
        P[qi] = nb_.replace("\x00", EN.search(P[qi]).group(0)) if EN.search(P[qi]) else nb_
        # 3) 선지 문단 지우기(미주가 있으면 발문 문단 끝으로)
        for i in cidx:
            enm = EN.search(P[i])
            if enm:
                P[qi] = re.sub(r"(</hp:run>)(</hp:p>)$", lambda z: enm.group(0) + z.group(1) + z.group(2), P[qi], count=1) \
                    if P[qi].endswith("</hp:run></hp:p>") else P[qi]
                if enm.group(0) not in P[qi]:
                    P[qi] = P[qi][:-len("</hp:run></hp:p>")] + enm.group(0) + "</hp:run></hp:p>"
            drop.add(i)
        log.append((k, "단답형", sc))
    P = [p for i, p in enumerate(P) if i not in drop]
    return P, log
