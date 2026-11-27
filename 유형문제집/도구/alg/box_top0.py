# -*- coding: utf-8 -*-
"""개념·유형 상자 위 여백: 쪽·단 맨 위에 오는 상자만 0 (2026-11-27 사용자 '가: 쪽이나 단 맨 위에 오는 상자만 0').
대수 (c)·(m) 틀은 개념·유형 02부터 쪽 나눔이거나 단 맨 위에서 시작(저장된 줄 위치 vertpos 0, 사용자 1단원 수정본도 02부터 모두 0)
→ 02부터의 개념 상자(rect)·유형 상자(container)의 바깥 여백 위를 0. 01은 STEP 머리 바로 아래라 그대로.
그리고 선택지 바로 앞 빈 줄: 빈 줄을 지우고 그 앞 글 문단의 문단 아래를 600(사용자 '응').
python box_top0.py <hwpx> ...   (제자리)
"""
import re, sys, zipfile, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "guide"))
from extract import top_paras
from layout_c1 import elems, plain, add_item


def fix(path):
    zi = zipfile.ZipFile(path); items = [(i, zi.read(i.filename)) for i in zi.infolist()]; zi.close()
    H = next(k for k, (i, _) in enumerate(items) if i.filename == "Contents/header.xml")
    h = items[H][1].decode("utf-8")
    rep = dict(box=0, blank=0)
    for k, (info, d) in enumerate(items):
        if not re.match(r"Contents/section\d+\.xml", info.filename):
            continue
        s = d.decode("utf-8")
        # 1) 상자
        edits = []
        for tag in ("rect", "container"):
            for a, j in elems(s, tag):
                el = s[a:j]
                t = re.sub(r"<[^>]+>", "", re.sub(r"<hp:equation .*?</hp:equation>", "E", el, flags=re.S)).strip()
                m = re.match(r"0(\d)", t)
                if not m or m.group(1) == "1" or not re.search(r"개념|유형", t[:60]):
                    continue
                oms = list(re.finditer(r'<hp:outMargin left="(\d+)" right="(\d+)" top="(\d+)" bottom="(\d+)"/>', el))
                if not oms or oms[-1].group(3) == "0":
                    continue
                om = oms[-1]
                edits.append((a + om.start(), a + om.end(), '<hp:outMargin left="%s" right="%s" top="0" bottom="%s"/>' % (om.group(1), om.group(2), om.group(4))))
        # 바깥 상자만(안쪽에 든 rect가 겹치면 같은 outMargin일 수 없음 — 위치로 중복 제거)
        for a, b, r in sorted(set(edits), reverse=True):
            s = s[:a] + r + s[b:]
            rep["box"] += 1
        # 2) 선택지 앞 빈 줄
        P = top_paras(s)
        cur, cuts = 0, []
        pos = []
        for p in P:
            i = s.index(p, cur); pos.append(i); cur = i + len(p)
        for n in range(2, len(P)):
            if plain(P[n]).startswith("①") and not plain(P[n - 1]) and not re.search(r"<hp:(pic|tbl|rect|container|ctrl)\b", P[n - 1]) and plain(P[n - 2]):
                cuts.append(n)
        for n in reversed(cuts):
            q = P[n - 2]; pid = re.search(r'paraPrIDRef="(\d+)"', q).group(1)
            pp = re.search(r'<hh:paraPr id="%s" .*?</hh:paraPr>' % pid, h, re.S).group(0)
            q2 = q
            if not re.search(r'<hc:next value="600"', pp):
                def ed(b):
                    if "<hp:case" in b:
                        b = re.sub(r'(<hp:case [^>]*>.*?<hc:next value=")\d+', r"\g<1>600", b, count=1, flags=re.S)
                        return re.sub(r'(<hp:default>.*?<hc:next value=")\d+', r"\g<1>1200", b, count=1, flags=re.S)
                    return re.sub(r'(<hc:next value=")\d+', r"\g<1>600", b, count=1)
                h, nid = add_item(h, "paraProperties", "paraPr", pid, ed)
                q2 = q.replace('paraPrIDRef="%s"' % pid, 'paraPrIDRef="%s"' % nid, 1)
            a = pos[n - 2]; b = pos[n - 1] + len(P[n - 1])
            s = s[:a] + q2 + s[b:]
            rep["blank"] += 1
        items[k] = (info, s.encode("utf-8"))
    items[H] = (items[H][0], h.encode("utf-8"))
    with zipfile.ZipFile(path, "w") as zo:
        for info, d in items:
            zo.writestr(info, d, compress_type=zipfile.ZIP_STORED if info.filename == "mimetype" else zipfile.ZIP_DEFLATED)
    return rep


if __name__ == "__main__":
    for f in sys.argv[1:]:
        print(os.path.basename(f), fix(f))
