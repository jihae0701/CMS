# -*- coding: utf-8 -*-
"""본문에 글자로 적힌 수식(a+b+c=t, f(1)=0 따위)을 수식 개체로 바꾼다.

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
    ("rw", "(단, t는 상수)", "$a+b+c=t$ (단, $t$는 상수)로 주어졌을 때,"),
    ("rw", "a+b=t-c, b+c=t-a", "$a+b=t-c$, $b+c=t-a$, $c+a=t-b$로 바꾸어 계산한다."),
    ("rw", "(x-1)(xn-1+", "$(x-1)(x^{n-1} +x^{n-2} +x^{n-3} + cdots +x+1)=x^n -1$"),
    ("rw", "(x-y)(xn-1+", "$(x-y)(x^{n-1} +x^{n-2} y+x^{n-3} y^2 + cdots +xy^{n-2} +y^{n-1} )=x^n -y^n$"),
    ("rw", "5제곱은 2제곱과", "$5$제곱은 $2$제곱과 $3$제곱의 곱, $7$제곱은 $3$제곱과 $4$제곱의 곱으로 표현한다."),
    ("sub", "다항식의 모든 계수의 합은 f(1)임을", "f(1)임을", "$f(1)$임을"),
]
TABLE2 = [
    ("sub", "f(m), f(n)의 값을 구한다", "f(m), f(n)의 값", "$f(m)$, $f(n)$의 값"),
    ("sub", "나머지가 0인 것이 아니다", "나머지가 0인", "나머지가 $0$인"),
    ("rw", "g(x)으로 나누었을 때의 나머지는", "$f(x)$를 $g(x)$로 나누었을 때의 나머지는 $R(x)$를 $g(x)$로 나누었을 때의 나머지와 같다."),
    ("rw", "항등식의 성질을 이용하여 푸는 방법", [("16", "[방법1] 나머지를 $ax+b$라 놓고, 항등식의 성질을 이용하여 푸는 방법"), ("53", "\n"),
                                       ("16", "$x^n -1=(x-1)(x^{n-1} +x^{n-2} +x^{n-3} + cdots +x+1)$임을 기억하자.")]),
    ("rw", "(x-1)(xn-1+", "$(x-1)(x^{n-1} +x^{n-2} +x^{n-3} + cdots +x+1)=x^n -1$"),
    ("rw", "(x-y)(xn-1+", "$(x-y)(x^{n-1} +x^{n-2} y+x^{n-3} y^2 + cdots +xy^{n-2} +y^{n-1} )=x^n -y^n$"),
    ("sub", "교과서에서는", "[방법1]를 제사하고", "[방법1]을 제시하고"),
    ("rw", "수의 나눗셈에서는", [("53", " "), ("59", "수의 나눗셈에서는 $N$을 $n$으로 나누면 나머지 $r$는 $0 le r < n$이다.")]),
    ("rw", "은 자연수, r은 음의 아닌 정수", "($N$, $n$은 자연수, $r$는 음이 아닌 정수)"),
    ("rw", "이 성립한다면 f(x)는 x-1", "$f(1)=0$, $f(2)=0$, $f(3)=0$이 성립한다면 $f(x)$는 $x-1$, $x-2$, $x-3$을 인수로 갖는다."),
]
