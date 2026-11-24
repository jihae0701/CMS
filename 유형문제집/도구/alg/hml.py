# -*- coding: utf-8 -*-
"""모의고사 기출 HML → 문항(출처·번호·배점·문제·정답·해설) (2026-11-24)"""
import re, html, sys


def ptext(x):
    out = []
    for m in re.finditer(r"<CHAR>([^<]*)</CHAR>|<SCRIPT>([^<]*)</SCRIPT>|(<LINEBREAK/>)|(<PICTURE)|(<TABLE)", x):
        if m.group(1) is not None: out.append(html.unescape(m.group(1)))
        elif m.group(2) is not None: out.append("$" + html.unescape(m.group(2)) + "$")
        elif m.group(3): out.append(" ")
        elif m.group(4): out.append("[그림]")
        else: out.append("[표]")
    return "".join(out)


def load(path):
    """문항 = [출처] 표 → 미주([정답][해설]) 붙은 문단 → 문제 글. 본문을 미주 자리로 나누고 각 조각을 [출처]에서 다시 나눔"""
    s = open(path, encoding="utf-8", errors="ignore").read()
    body = s[s.index("<BODY"):]
    ens = list(re.finditer(r"<ENDNOTE[^>]*>(.*?)</ENDNOTE>", body, re.S))
    noen = re.sub(r"<ENDNOTE[^>]*>.*?</ENDNOTE>", "\x01", body, flags=re.S)
    chunks = noen.split("\x01")
    def paras_text(x):
        return [ptext(p).strip() for p in re.findall(r"<P [^>]*>(.*?)</P>", x, re.S)]
    items = []
    for i, m in enumerate(ens):
        lines = [l for l in (ptext(p).strip() for p in re.findall(r"<P [^>]*>(.*?)</P>", m.group(1), re.S)) if l]
        before = " ".join(paras_text(chunks[i] + "</P>"))
        src = before[before.rfind("[출처]"):] if "[출처]" in before else ""
        after = " ".join(t for t in paras_text("<P x>" + chunks[i + 1]) if t)
        q = after[:after.find("[출처]")] if "[출처]" in after else after
        q = re.sub(r"\[표\]\s*$", "", q.strip())
        mm = re.search(r"\[출처\]\s*(.*?)\s(\d+)\s*\[([\d.]+)점\]", src)
        items.append(dict(lines=lines, q=q, src=mm.group(1) if mm else src[:50], no=int(mm.group(2)) if mm else 0,
                          pt=float(mm.group(3)) if mm else 0, xml_en=m.group(0)))
    return items


if __name__ == "__main__":
    for i, it in enumerate(load(sys.argv[1]), 1):
        ok = it["pt"] >= 4 and it["no"] not in (15, 21, 22, 30)
        if ok or "-a" in sys.argv:
            print("%2d %s %s번 %s점 %s" % (i, it["src"], it["no"], it["pt"], "★" if ok else ""))
            print("   Q:", it["q"][:500])
            print("   A:", " / ".join(it["lines"][1:4])[:200])
