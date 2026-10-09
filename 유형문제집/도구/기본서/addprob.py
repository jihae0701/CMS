# -*- coding: utf-8 -*-
"""기본서에 새 문항 넣기: 기존 문항 하나(번호 문단 + 문제 문단 + 빈 문단)를 본보기로 복제한다."""
import re
import numbering as nb, eqsize, fixes

ENDNOTE = re.compile(r"<hp:endNote .*?</hp:endNote>", re.S)

# 차수를 따져 나머지를 구하는 대표 문제, f(x)=t로 놓아 항등식을 만드는 대표 문제 (유형 07에 넣음)
NEW1 = [
    {"q": "두 다항식 $f(x)$, $g(x)$에 대하여 $f(x)$를 $g(x)+x^{2}$으로 나누었을 때의 몫은 $x+1$이고 "
          "나머지는 $g(x)+3x$이다. $g(1)=3$, $f(0)=-2$일 때, $f(2)$의 값을 구하시오.",
     "ans": "󰂼 $46$",
     "sol": ["$g(x)$의 차수를 $n$이라 하자.",
             "$n geq 3$이면 나누는 식 $g(x)+x^{2}$과 나머지 $g(x)+3x$의 차수가 모두 $n$이 되어 "
             "나머지의 차수가 나누는 식의 차수보다 작아야 한다는 데 어긋난다.",
             "$n=2$이면 나머지 $g(x)+3x$는 이차식이고 나누는 식 $g(x)+x^{2}$은 이차 이하의 식이므로 역시 어긋난다.",
             "따라서 $g(x)$는 일차 이하의 식이므로 $g(x)=ax+b$ ($a$, $b$는 상수)라 하면",
             "$f(x)=(x+1)(x^{2}+ax+b)+(a+3)x+b$",
             "$f(0)=2b=-2$에서 $b=-1$, $g(1)=a+b=3$에서 $a=4$",
             "$therefore$ $f(2)=3 times 11+7 times 2-1=46$"]},
    {"q": "상수가 아닌 다항식 $f(x)$가 모든 실수 $x$에 대하여 "
          "$left {f(x) right }^{2}-3f(x)+4=f(f(x))$를 만족시킬 때, $f(5)$의 값을 구하시오.",
     "ans": "󰂼 $14$",
     "sol": ["주어진 등식의 $f(x)$를 $t$로 놓으면 $f(t)=t^{2}-3t+4$",
             "$f(x)$는 상수가 아닌 다항식이므로 $t$는 무수히 많은 값을 가진다.",
             "무수히 많은 $t$에 대하여 $f(t)=t^{2}-3t+4$가 성립하므로 이 등식은 $t$에 대한 항등식이다.",
             "즉 $f(x)=x^{2}-3x+4$이고 이때 주어진 등식이 성립한다.",
             "$therefore$ $f(5)=25-15+4=14$"]},
]


def _block(P, num):
    i = next(k for k, p in enumerate(P) if nb.num_text(p) == num)
    j = i + 1
    while j < len(P) and not nb.num_text(P[j]) and not nb.is_heading(P[j]):
        j += 1
    return i, j


def _scripts(items):
    out = []
    for it in items:
        out += fixes.scripts_of([it["q"], it["ans"]] + it["sol"])
    return out


def insert(P, after, template, items, blanks=18):
    """번호 after인 문항 뒤에 items를 넣는다. 모양은 번호 template인 문항을 따른다."""
    eqsize.ensure(_scripts(items))
    doc = fixes.Doc(P)
    ti, tj = _block(P, template)
    num_p, q_p = P[ti], P[ti + 1]
    spacer = [p for p in P[ti + 2:tj] if nb.blank(p) and 'pageBreak="1"' not in p and 'columnBreak="1"' not in p][:1]
    q_open = re.match(r"<hp:p [^>]*>", q_p).group(0)
    run_cp = re.search(r'<hp:run charPrIDRef="(\d+)">', q_p).group(1)
    ctrl_cp = re.search(r'<hp:run charPrIDRef="(\d+)"><hp:ctrl><hp:endNote ', q_p).group(1)
    en0 = ENDNOTE.search(q_p).group(0)
    # 문제 글의 수식은 해설보다 크므로 본보기 문제 문단의 수식 모양을 쓴다
    qdoc = fixes.Doc(P)
    qeq = re.search(r"<hp:equation [^>]*>", q_p).group(0)
    qdoc.eq_open = re.sub(r'\bid="\d+"', 'id="0"', re.sub(r'zOrder="\d+"', 'zOrder="0"', qeq))
    qdoc.base = int(re.search(r'baseUnit="(\d+)"', qeq).group(1))
    new = []
    for k, it in enumerate(items):
        en = doc.endnote_body(en0, [it["ans"]] + it["sol"])
        en = re.sub(r'instId="\d+"', 'instId="%d"' % (1990000000 + 1000 * len(P) % 7919 + k), en, count=1)
        q = ('%s<hp:run charPrIDRef="%s">%s</hp:run><hp:run charPrIDRef="%s"><hp:ctrl>%s</hp:ctrl><hp:t/></hp:run></hp:p>'
             % (q_open, run_cp, qdoc.inline(it["q"]), ctrl_cp, en))
        new += [num_p, q] + spacer * blanks
    ai, aj = _block(P, after)
    return P[:aj] + new + P[aj:]
