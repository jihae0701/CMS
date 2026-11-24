# -*- coding: utf-8 -*-
"""내신 기출 HWPX → 문항(문제 글·배점·정답/풀이) 대략 나누기 (2026-11-24)"""
import re, zipfile, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kd import plain, en_paras
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "guide"))
from extract import top_paras


def load(path):
    z = zipfile.ZipFile(path)
    secs = sorted(n for n in z.namelist() if re.match(r"Contents/section\d+\.xml", n))
    P = []
    for n in secs:
        P += top_paras(z.read(n).decode("utf-8"))
    probs, cur = [], None
    for p in P:
        ens = re.findall(r"<hp:endNote .*?</hp:endNote>", p, re.S)
        t = plain(p).strip()
        if ens:
            cur = dict(q=[t] if t else [], en=" / ".join(plain(x).strip() for x in en_paras(ens[0]) if plain(x).strip()))
            probs.append(cur)
        elif cur is not None and t:
            cur["q"].append(t)
    return probs


if __name__ == "__main__":
    for f in sys.argv[1:]:
        print("######", os.path.basename(f))
        for i, pr in enumerate(load(f), 1):
            q = " ".join(pr["q"])
            pt = re.findall(r"\[\s*([\d.]+)\s*점\]", q)
            print("%2d [%s] %s || %s" % (i, pt[0] if pt else "?", q[:330], pr["en"][:160]))
