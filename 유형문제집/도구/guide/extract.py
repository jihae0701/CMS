# -*- coding: utf-8 -*-
"""기본서·유형서 완성본에서 문항(번호, 단계, 유형, 대표문제 여부, 문제 글) 꺼내기 — 수업 가이드용 (2026-11-19).
- 기본서: 미주가 문제 글 문단(번호 포함)에 있고 그 뒤에 선택지·조건 상자. 대표문제는 그 앞 문단의 번호 상자(도형)에 '대표문제' 글자.
- 유형서: 미주가 번호 자리(문항 처음)에 있음.
- 번호 = 미주 번호 매기기 시작값(endNotePr newNum) + 순서.
- 단계: '개념 확인하기'(STEP 1) / '유형별 학습하기'(STEP 2) / '단원 마무리 하기'(STEP 3), 유형서는 '단원종합문제'.
- 문제 글: <hp:t> 글자와 수식(<hp:script>, $…$로 감쌈). 미주(해설)는 뺌.
"""
import re, zipfile

TOK = re.compile(r"<hp:p[ >]|</hp:p>")


def top_paras(sec):
    i = sec.index("<hp:p ")
    out, depth, start = [], 0, None
    for m in TOK.finditer(sec, i):
        if m.group(0).startswith("<hp:p"):
            if depth == 0:
                start = m.start()
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                out.append(sec[start:m.end()])
    return out


def ptext(x, eq=True):
    x = re.sub(r"<hp:endNote .*?</hp:endNote>", "", x, flags=re.S)
    parts = re.findall(r"<hp:t>([^<]*)</hp:t>|<hp:script>([^<]*)</hp:script>", x)
    return "".join(a if a else ("$%s$" % b if eq else "") for a, b in parts)


def head_text(p, kind, first=False):
    """유형 머리. 기본서: 'NN 제목유형' 한 문단. 유형서: 네모(rect) 안 제목만 있는 짧은 문단(번호 없음)"""
    if "<hp:endNote " in p:
        return None
    t = re.sub(r"\s+", " ", ptext(p, eq=False)).strip()
    if kind == "b":
        m = re.match(r"^(\d{2})\s*(.+?)\s*유형$", t)
        return (int(m.group(1)), m.group(2).strip()) if m else None
    if ("<hp:rect" in p or first) and 0 < len(t) <= 30 and not re.match(r"^[(（ㄱ①②③④⑤\[]|^보\s*기", t) and "단원" not in t and "STEP" not in t:
        return (None, t)
    return None


def read(path, kind):
    sec = zipfile.ZipFile(path).read("Contents/section0.xml").decode("utf-8")
    m = re.search(r"<hp:endNotePr>.*?newNum=\"(\d+)\"", sec, re.S)
    start = int(m.group(1)) if m else 1
    P = top_paras(sec)
    items, stage, ytype, ny = [], ("" if kind == "b" else "유형"), None, 0
    k = start - 1
    pend = False
    for i, p in enumerate(P):
        t = ptext(p, eq=False)
        if kind == "b":
            if "개념 확인하기" in t: stage = "STEP1"
            if "유형별 학습하기" in t: stage = "STEP2"
            if "단원 마무리" in t: stage, ytype = "STEP3", None
        elif ("단원종합문제" in t or "단원 종합 문제" in t) and "<hp:endNote " not in p:
            stage, ytype = "종합", None
        h = head_text(p, kind, first=(i == 0)) if stage != "종합" else None
        if h:
            if kind == "y":
                ny += 1
                h = (ny, h[1])
            ytype = h
            continue
        if kind == "b" and "대표문제" in t and "<hp:endNote " not in p:
            pend = True                                   # 대표문제 번호 상자 문단 → 다음 미주 문단이 그 문항
            continue
        if "<hp:endNote " in p:
            for _ in re.findall(r"<hp:endNote ", p):
                k += 1
                items.append(dict(n=k, stage=stage, type=ytype, rep=(kind == "b" and (pend or "대표문제" in t)), q=ptext(p)))
            pend = False
        elif items:
            items[-1]["q"] += " " + ptext(p)
    return items


def fix_split(items):
    """한 문단에 다음 문항 번호(글자 'NNN')와 문제 글이 이어 붙은 경우: 그 번호부터 뒤를 다음 문항으로 옮김(번호를 글자로 쓴 단원)"""
    for a, b in zip(items, items[1:]):
        m = re.search(r"(?:^|\s)%03d\s" % b["n"], a["q"])
        if m and m.start() > 5:
            b["q"] = a["q"][m.start():] + " " + b["q"]
            a["q"] = a["q"][:m.start()]
    return items


def book(bookno):
    """공통수학 bookno의 12단원: [(단원, 이름, 기본서 문항, 유형서 문항)] — 번호는 앞 단원 문항 수를 이어 셈(완성본 번호와 같음)"""
    from files import units
    out, sb, sy = [], 1, 1
    for u, name, bf, yf in units(bookno):
        b, y = read(bf, "b"), read(yf, "y")
        for i, it in enumerate(b): it["n"] = sb + i
        for i, it in enumerate(y): it["n"] = sy + i
        sb += len(b); sy += len(y)
        out.append((u, name, fix_split(b), y, bf, yf))
    return out
