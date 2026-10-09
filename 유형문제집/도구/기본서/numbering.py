# -*- coding: utf-8 -*-
"""기본서 문항 번호를 처음부터 차례로 다시 매긴다(번호 문단이 없으면 새로 넣는다)."""
import re
import hwpxio as io


def blank(p):
    return not re.search(r'<hp:t>[^<]*\S[^<]*</hp:t>|<hp:equation|<hp:tbl|<hp:rect|<hp:pic|<hp:container|<hp:endNote |<hp:line ', p)


def is_heading(p):
    t = io.text(p)
    return bool(re.search(r"유형$|STEP \d$", t))


def num_text(p):
    """번호 문단이면 번호 글자, 아니면 None. (대표문제 상자 글자는 뺀다)"""
    q = re.sub(r"<hp:container.*?</hp:container>", "", p, flags=re.S)
    q = re.sub(r"<hp:rect.*?</hp:rect>", "", q, flags=re.S)
    if "<hp:endNote " in q or "<hp:equation" in q:
        return None
    t = io.text(q).strip()
    if re.fullmatch(r"\d{2,3}", t):
        return t
    if t == "" and "대표문제" in p:
        return ""
    return None


def segments(P):
    """미주 하나 = 문항 하나. (시작, 미주 문단) 목록"""
    E = [i for i, p in enumerate(P) if "<hp:endNote " in p]
    out, prev = [], -1
    for e in E:
        a = e
        while a - 1 > prev and not blank(P[a - 1]) and not is_heading(P[a - 1]):
            a -= 1
        out.append((a, e))
        b = e
        while b + 1 < len(P) and not blank(P[b + 1]) and not is_heading(P[b + 1]) and "<hp:endNote " not in P[b + 1]:
            b += 1
        prev = b
    return out


def set_number(p, n, template=None):
    """번호 문단의 첫 두 run: 앞의 0은 흐린 글자, 나머지는 진한 글자"""
    if template is not None and not re.search(r"<hp:t>\d+</hp:t>", p):
        # 대표문제 상자만 있고 번호 글자가 없는 문단: 본보기의 두 run을 앞에 붙인다
        runs = re.findall(r'<hp:run charPrIDRef="\d+"><hp:t>[^<]*</hp:t></hp:run>', template)[:2]
        head = re.match(r"<hp:p [^>]*>", p).group(0)
        p = head + "".join(runs) + p[len(head):]
    s = "%03d" % n
    z = len(s) - len(s.lstrip("0"))
    zeros, digits = s[:z], s[z:]
    runs = list(re.finditer(r'<hp:run charPrIDRef="\d+">(?:<hp:t>[^<]*</hp:t>|<hp:t/>)?', p))
    r1, r2 = runs[0], runs[1]
    new1 = re.sub(r"<hp:t>[^<]*</hp:t>|<hp:t/>", "", r1.group(0)) + ("<hp:t>%s</hp:t>" % zeros if zeros else "<hp:t/>")
    new2 = re.sub(r"<hp:t>[^<]*</hp:t>|<hp:t/>", "", r2.group(0)) + "<hp:t>%s</hp:t>" % digits
    return p[:r1.start()] + new1 + p[r1.end():r2.start()] + new2 + p[r2.end():]


def renumber(P, template):
    """P: 문단 목록. template: 대표문제 상자가 없는 번호 문단(새로 넣을 때 씀)"""
    segs = segments(P)
    inserts = {}
    numpara = {}
    for k, (a, e) in enumerate(segs, 1):
        if num_text(P[a]) is not None:
            numpara[a] = k
        else:
            inserts[a] = k
    out = []
    for i, p in enumerate(P):
        if i in inserts:
            out.append(set_number(template, inserts[i]))
        if i in numpara:
            p = set_number(p, numpara[i], template)
        out.append(p)
    return out, len(segs), len(inserts)
