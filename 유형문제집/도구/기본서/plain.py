# -*- coding: utf-8 -*-
"""본문 설명 문단 고치기(설명 문단의 글자 수식은 그대로 두고 오타만 고친다; 표 형식은 수식도 넣을 수 있음).

표의 항목
  ("rw", 찾을 글, 새 글)            문단 전체를 새로 쓴다. 새 글이 문자열이면 첫 글자 모양으로,
                                    [(글자모양, 글), ...]이면 그 모양별로 쓴다. "\\n"은 줄 바꿈.
  ("sub", 찾을 글, 옛 글, 새 글)    문단 글자 요소 안에서 일부만 바꾼다.
"""
import re
from xml.sax.saxutils import escape
import hwpxio as io, eqsize


def _inline(text, doc):
    out = []
    for k, part in enumerate(re.split(r"\$(.+?)\$", text)):
        if k % 2:
            out.append(doc.eq(part.strip(), doc.body_base))
        elif part:
            out.append("<hp:t>%s</hp:t>" % "<hp:lineBreak/>".join(escape(s) for s in part.split("\n")))
    return "".join(out)


def rewrite(P, table, doc):
    texts = []
    for e in table:
        new = e[2] if e[0] == "rw" else e[3]
        texts += [t for _, t in new] if isinstance(new, list) else [new]
    eqsize.ensure([m.strip() for t in texts for m in re.findall(r"\$(.+?)\$", t)])
    for e in table:
        key = e[1]
        hit = [i for i, p in enumerate(P) if key in io.text(p) and "<hp:endNote " not in p]
        if len(hit) != 1:
            print("본문 수식 바꾸기 실패:", key, hit)
            continue
        i = hit[0]
        p = P[i]
        if e[0] == "rw":
            head = re.match(r"<hp:p [^>]*>", p).group(0)
            new = e[2]
            if isinstance(new, str):
                cp = (re.search(r'<hp:run charPrIDRef="(\d+)"><hp:t>[^<\s]', p) or re.search(r'<hp:run charPrIDRef="(\d+)">', p)).group(1)
                new = [(cp, new)]
            P[i] = head + "".join('<hp:run charPrIDRef="%s">%s</hp:run>' % (cp, _inline(t, doc)) for cp, t in new) + "</hp:p>"
        else:
            old, new = escape(e[2]), e[3]
            n = "".join(("</hp:t>" + doc.eq(q.strip(), doc.body_base) + "<hp:t>") if k % 2 else escape(q)
                        for k, q in enumerate(re.split(r"\$(.+?)\$", new)))
            if old not in p:
                print("본문 수식 바꾸기 실패(글 없음):", key, e[2])
                continue
            P[i] = p.replace(old, n, 1)
    return P


TABLE1 = [
    ("sub", "a+b=t-c, b+c=t-a", "바뀌어 계산한다", "바꾸어 계산한다"),
    ("sub", "5제곱은 2제곱과", "4제곱이 곱으로", "4제곱의 곱으로"),
]
TABLE2 = [
    ("sub", "g(x)으로 나누었을 때의 나머지는", "g(x)으로", "g(x)로"),
    ("sub", "g(x)으로 나누었을 때의 나머지와", "g(x)으로", "g(x)로"),
    ("sub", "교과서에서는", "[방법1]를 제사하고", "[방법1]을 제시하고"),
    ("sub", "수의 나눗셈에서는", "N를 n으로", "N을 n으로"),
    ("sub", "은 자연수, r은 음의 아닌 정수", "음의 아닌", "음이 아닌"),
    ("sub", "이 성립한다면 f(x)는 x-1", "x-3를", "x-3을"),
]
