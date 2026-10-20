# -*- coding: utf-8 -*-
"""출처를 붙여 넣은 모의고사 객관식 문항은 원문 그대로 객관식(5지선다)으로 싣는다(사용자 규칙).
단원 파일에는 정답을 수(검산용)로 두고, gen.py가 문서를 만들 때 이 표로 발문 끝을 원문대로 되돌리고
보기를 붙이며 정답을 ①~⑤로 바꾼다. 고른 번호의 보기 값이 단원 파일의 정답과 다르면 멈춘다.

표: 출처 → (보기 5개, 정답 번호, 발문 고치기[(바꿀 글, 새 글), ...] 또는 None)
None이면 마지막 '…을/를 구하시오.'를 '…은?/는?'으로 바꾼다(원문 발문과 대조함).
"""
import re
from sympy import sympify, simplify

MARK = "①②③④⑤"


def _c(*v):
    return ["$%s$" % x for x in v]


TABLE = {
    "2025년 6월 고1 14번": (_c(28, 30, 32, 34, 36), "⑤", None),
    "2025년 10월 고1 19번": (_c(-3, -2, -1, 0, 1), "⑤", None),
    "2025년 6월 고1 17번": (_c(48, 52, 56, 60, 64), "①", None),
    "2025년 9월 고1 15번": (_c(-9, -7, -5, -3, -1), "④", None),
    "2026년 3월 고2 20번": (_c(4, 6, 8, 10, 12), "④", None),
    "2025년 3월 고1 15번": (_c(22, 24, 26, 28, 30), "④", None),
    "2025년 10월 고1 18번": (_c(5, 6, 7, 8, 9), "②", None),
    "2025년 9월 고1 16번": (_c(7, 10, 13, 16, 19), "②", None),
    "2025년 6월 고1 15번": (_c(11, 12, 13, 14, 15), "②", None),
    "2024년 3월 고2 15번": (_c(-32, -16, -8, -4, -2), "①", None),
    "2025년 6월 고1 19번": (_c(60, 64, 68, 72, 76), "④", None),
    "2026년 9월 고1 19번": (_c(60, 64, 68, 72, 76), "①", None),
    "2025년 9월 고1 20번": (_c(15, 16, 17, 18, 19), "③", None),
    "2026년 9월 고1 18번": (_c(130, 132, 134, 136, 138), "②", None),
    "2026년 9월 고1 16번": (_c(3, 4, 5, 6, 7), "②", None),
    "2025년 9월 고1 18번": (_c("{27} over {8}", "{7} over {2}", "{29} over {8}", "{15} over {4}", "{31} over {8}"), "④", None),
    "2010년 11월 고1 19번": (_c(14, 15, 16, 17, 18), "⑤",
                         [("이다. 이차부등식", "이다. 이때, 이차부등식")]),
    "2015년 9월 고1 14번": (_c(32, 34, 36, 38, 40), "④", None),
    "2024년 6월 고1 21번": (_c("1+ sqrt {3}", "2+ sqrt {3}", "3+ sqrt {3}", "4+ sqrt {3}", "5+ sqrt {3}"), "②", None),
    "2024년 10월 고1 20번": (_c("{15} over {2}", 8, "{17} over {2}", 9, "{19} over {2}"), "④", None),
    "2021년 9월 고1 21번": (_c("7+ sqrt {3}", "7+2 sqrt {3}", "7+3 sqrt {3}", "9+2 sqrt {3}", "9+3 sqrt {3}"), "②", None),
    "2009년 11월 고1 21번": (_c("{sqrt {5}} over {2} -1", "sqrt {5} -2", "2- sqrt {3}", "sqrt {3} -1", "3- sqrt {5}"), "②", None),
    "2014학년도 경찰대학 11번": (_c(2, "2 sqrt {2}", "2 sqrt {3}", 4, "2 sqrt {5}"), "⑤", None),
    "2025년 6월 고1 21번": (_c(45, 48, 51, 54, 57), "①", None),
    "2024년 10월 고1 18번": (_c(2, "{7} over {3}", "{8} over {3}", 3, "{10} over {3}"), "⑤", None),
    "2026년 9월 고1 17번": (_c(972, 984, 996, 1008, 1020), "④", None),
    "2025년 10월 고1 16번": (_c(228, 234, 240, 246, 252), "⑤", None),
    "2026년 3월 고2 16번": (_c(168, 180, 192, 204, 216), "⑤", None),
    "2026년 9월 고1 20번": (_c(240, 270, 300, 330, 360), "③", None),
    "2025년 9월 고1 21번": (_c(410, 420, 430, 440, 450), "⑤", None),
    "2026년 9월 고1 15번": (_c(10, 13, 16, 19, 22), "③", None),
    "2025년 10월 고1 15번": (_c(3, 4, 5, 6, 7), "②", None),
    "2021년 4월 고3 28번": (_c(78, 82, 86, 90, 94), "⑤", None),
}


def value(s):
    """'$-3$', '{15} over {4}', '2 sqrt {5}' 같은 답을 수로"""
    s = s.strip().strip("$").replace("`", "")
    s = re.sub(r"\{([^{}]*)\}\s*over\s*\{([^{}]*)\}", r"((\1)/(\2))", s)
    s = re.sub(r"sqrt\s*\{\s*([^{}]*)\}", r"sqrt(\1)", s)
    s = re.sub(r"(\d)\s*sqrt", r"\1*sqrt", s).replace(" ", "")
    return sympify(s)


def key(src):
    return re.sub(r"\s*\[\d점\]\s*$", "", src or "").strip()


def apply(items):
    used = set()
    for it in items:
        k = key(it.get("src"))
        if "h" in it or k not in TABLE:
            continue
        ch, mark, edits = TABLE[k]
        if any(isinstance(p, dict) and "ch" in p for p in it["q"]):
            raise SystemExit("이미 객관식인 문항이 표에 있음: %s" % k)
        got = value(ch[MARK.index(mark)])
        if simplify(got - value(it["ans"])) != 0:
            raise SystemExit("객관식 정답 불일치 %s: 보기 %s, 단원 정답 %s" % (k, got, it["ans"]))
        q = list(it["q"])
        # 발문 끝('…구하시오.')이 든 문단 — 뒤에 단서 문단 '(단, …)'이나 그림이 따로 올 수 있다
        last = max([i for i, p in enumerate(q) if isinstance(p, str) and "구하시오." in p]
                   or [i for i, p in enumerate(q) if isinstance(p, str)])
        s = q[last]
        if edits:
            for a, b in edits:
                if a not in s:
                    raise SystemExit("발문 고치기 실패 %s: %s" % (k, a))
                s = s.replace(a, b)
        s, n = re.subn(r"(을|를) 구하시오\.", lambda m: "은?" if m.group(1) == "을" else "는?", s)
        if n != 1:
            raise SystemExit("발문 끝을 찾지 못함 %s" % k)
        q[last] = s
        q.append({"ch": ch})
        it["q"], it["ans"] = q, mark
        used.add(k)
    return used
