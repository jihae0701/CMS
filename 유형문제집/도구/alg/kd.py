# -*- coding: utf-8 -*-
"""올림포스 고난도 대수 단원 HWPX → 문항 목록(그룹·개념·번호·코드·문제 문단·선택지·미주) (2026-11-24)"""
import re, zipfile, html, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "guide"))
from extract import top_paras

GROUPS = ["내신 빈출 필수 문제", "내신 고득점 도전 문제", "변별력을 만드는 1등급 문제", "1등급을 넘어서는 상위 1%"]


def plain(x):
    """문단 → 글(수식은 $…$, 그림 [그림], 표 [표])"""
    x = re.sub(r"<hp:endNote .*?</hp:endNote>", "", x, flags=re.S)
    out = []
    for m in re.finditer(r"<hp:t>(.*?)</hp:t>|<hp:script[^>]*>([^<]*)</hp:script>|(<hp:pic )|(<hp:tbl )", x, re.S):
        if m.group(1) is not None:
            out.append(re.sub(r"<[^>]+>", " ", m.group(1)))
        elif m.group(2) is not None:
            out.append("$" + html.unescape(m.group(2)) + "$")
        elif m.group(3):
            out.append("[그림]")
        else:
            out.append("[표]")
    return html.unescape("".join(out))


def load(path):
    z = zipfile.ZipFile(path)
    s = z.read("Contents/section0.xml").decode("utf-8")
    P = top_paras(s)
    items, grp, con, cur = [], None, None, None
    for p in P:
        t = plain(p).strip()
        if t in GROUPS:
            grp = GROUPS.index(t); cur = None; continue
        m = re.match(r"^■\s*(\d+)\s*(.+)$", t)
        if m and "<hp:endNote" not in p:
            con = (int(m.group(1)), m.group(2).strip()); cur = None; continue
        m = re.match(r"^(\d\d)\s*▶\s*(\d{5}-\d{4})", t)
        if m and "<hp:endNote" not in p:
            m2 = re.search(r"\|\s*(.+?)\s*\|", t)
            c2 = (None, m2.group(1)) if m2 else (con if grp == 0 else None)
            cur = dict(no=int(m.group(1)), code=m.group(2), grp=grp, con=c2, paras=[], choices=[], en=None, head=p)
            items.append(cur); continue
        if cur is None:
            continue
        en = re.findall(r"<hp:endNote .*?</hp:endNote>", p, re.S)
        if en:
            cur["en"] = en[0]
        if re.match(r"^\s*①", t) or (cur["choices"] and re.match(r"^\s*④", t)):
            cur["choices"].append(p)
        elif t or "<hp:pic" in p or "<hp:tbl" in p or en:
            cur["paras"].append(p)
    return items, z


def en_paras(en):
    i = en.index("<hp:subList"); j = en.index(">", i) + 1
    return top_paras(en[j:en.rindex("</hp:subList>")])


if __name__ == "__main__":
    items, z = load(sys.argv[1])
    for it in items:
        print("=== %02d %s [%s] %s" % (it["no"], it["code"], GROUPS[it["grp"]][:6], it["con"]))
        for p in it["paras"]:
            print("  Q:", plain(p)[:400])
        for p in it["choices"]:
            print("  C:", plain(p)[:200])
        if it["en"]:
            ns = [plain(p).strip() for p in en_paras(it["en"])]
            ns = [n for n in ns if n]
            print("  N(%d):" % len(ns), " / ".join(ns[:2])[:200], " ... ", " / ".join(ns[-2:])[:200])
