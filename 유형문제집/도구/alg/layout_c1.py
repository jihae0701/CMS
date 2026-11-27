# -*- coding: utf-8 -*-
"""대수(c) 1단원 사용자 재편집본의 편집 상태를 다른 단원에 맞춤 (2026-11-27).
python layout_c1.py <hwpx> ...   (제자리에 고쳐 씀)
사용자가 고른 것:
- 번호 글자 14pt, 번호 폭 300: 번호 문단이 쓰는 문단번호(1수준)의 글자 모양을 14pt로 복제해 바꾸고 widthAdjust=300.
- STEP 머리 상자 위 여백 0: 'STEP'과 '개념 익히기(확인하기)·유형별 학습하기·단원 마무리 하기'가 든 묶음 상자의 바깥 여백 위 → 0.
- 선택지 바로 앞 번호 문단 아래 간격 600: 다음 문단이 ①로 시작하는 문단(번호 문단이 아니어도 — 사용자 파일에서 보기 끝 줄 등은 원래 600)의
  문단 모양을 복제해 문단 아래 600(hp:case 600, hp:default 1200 — 사용자 파일 값).
"""
import re, sys, zipfile, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "guide"))
from extract import top_paras


def add_item(h, kind, tag, src_id, edit):
    m = re.search(r'<hh:%s id="%s" .*?</hh:%s>' % (tag, src_id, tag), h, re.S)
    c = re.search(r'<hh:%s itemCnt="(\d+)"' % kind, h)
    nid = int(c.group(1))
    blk = edit(m.group(0).replace('id="%s"' % src_id, 'id="%d"' % nid, 1))
    h = h[:c.start()] + '<hh:%s itemCnt="%d"' % (kind, nid + 1) + h[c.end():]
    e = h.index("</hh:%s>" % kind)
    return h[:e] + blk + h[e:], str(nid)


def plain(p):
    p = re.sub(r"<hp:endNote .*?</hp:endNote>", "", p, flags=re.S)
    p = re.sub(r"<hp:equation .*?</hp:equation>", "<hp:t>E</hp:t>", p, flags=re.S)
    return "".join(re.findall(r"<hp:t>(.*?)</hp:t>", p, re.S)).strip()


def elems(s, tag):
    i = 0
    while True:
        a = s.find("<hp:%s " % tag, i)
        if a < 0:
            return
        d = 0
        for m in re.finditer(r"<hp:%s |</hp:%s>" % (tag, tag), s[a:]):
            d += 1 if m.group(0).startswith("<hp:%s " % tag) else -1
            if d == 0:
                j = a + m.end(); break
        yield a, j
        i = j


def fix(path):
    zi = zipfile.ZipFile(path); items = [(i, zi.read(i.filename)) for i in zi.infolist()]; zi.close()
    H = next(k for k, (i, _) in enumerate(items) if i.filename == "Contents/header.xml")
    h = items[H][1].decode("utf-8")
    rep = dict(num=0, step=0, ch=0)
    nums, clone = set(), {}
    for k, (info, d) in enumerate(items):
        if not re.match(r"Contents/section\d+\.xml", info.filename):
            continue
        s = d.decode("utf-8")
        # 1) STEP 머리 상자
        out, pos = [], 0
        for a, j in elems(s, "container"):
            el = s[a:j]
            t = re.sub(r"<[^>]+>", "", el)
            if "STEP" in t and re.search(r"개념 익히기|개념 확인하기|유형별 학습하기|단원 마무리 하기", t):
                oms = list(re.finditer(r'<hp:outMargin left="(\d+)" right="(\d+)" top="(\d+)" bottom="(\d+)"/>', el))
                om = oms[-1]
                if om.group(3) != "0":
                    el = el[:om.start()] + '<hp:outMargin left="%s" right="%s" top="0" bottom="%s"/>' % (om.group(1), om.group(2), om.group(4)) + el[om.end():]
                    rep["step"] += 1
            out.append(s[pos:a] + el); pos = j
        out.append(s[pos:]); s = "".join(out)
        # 2) 번호 문단: 문단번호 모음, 선택지 앞이면 문단 아래 600
        P = top_paras(s)
        new, cur = [], 0
        for n, p in enumerate(P):
            i = s.index(p, cur); cur = i + len(p)
            pid = re.search(r'paraPrIDRef="(\d+)"', p).group(1)
            pp = re.search(r'<hh:paraPr id="%s" .*?</hh:paraPr>' % pid, h, re.S).group(0)
            if "<hp:endNote " in p:
                hd = re.search(r'<hh:heading type="NUMBER" idRef="(\d+)"', pp)
                if hd:
                    nums.add(hd.group(1))
            if n + 1 < len(P) and plain(P[n + 1]).startswith("①") and plain(p) and not re.search(r'<hc:next value="600"', pp):
                if pid not in clone:
                    def ed(b):
                        if "<hp:case" in b:
                            b = re.sub(r'(<hp:case [^>]*>.*?<hc:next value=")\d+', r"\g<1>600", b, count=1, flags=re.S)
                            return re.sub(r'(<hp:default>.*?<hc:next value=")\d+', r"\g<1>1200", b, count=1, flags=re.S)
                        return re.sub(r'(<hc:next value=")\d+', r"\g<1>600", b, count=1)
                    h, clone[pid] = add_item(h, "paraProperties", "paraPr", pid, ed)
                new.append((i, p.replace('paraPrIDRef="%s"' % pid, 'paraPrIDRef="%s"' % clone[pid], 1)))
                rep["ch"] += 1
        for i, p2 in sorted(new, reverse=True):
            j = s.index(">", i) + 1
            s = s[:i] + p2[:p2.index(">") + 1] + s[j:]
        items[k] = (info, s.encode("utf-8"))
    # 3) 문단번호 글자 14pt, 폭 300
    for nid in sorted(nums):
        m = re.search(r'<hh:numbering id="%s" .*?</hh:numbering>' % nid, h, re.S)
        blk = m.group(0)
        ph = re.search(r'<hh:paraHead [^>]*level="1"[^>]*>', blk).group(0)
        cid = re.search(r'charPrIDRef="(\d+)"', ph).group(1)
        h2 = h
        if cid != "4294967295":
            h2, ncid = add_item(h, "charProperties", "charPr", cid, lambda b: re.sub(r'height="\d+"', 'height="1400"', b, count=1))
            ph2 = ph.replace('charPrIDRef="%s"' % cid, 'charPrIDRef="%s"' % ncid)
        else:
            ph2 = ph
        ph2 = re.sub(r'widthAdjust="-?\d+"', 'widthAdjust="300"', ph2)
        m = re.search(r'<hh:numbering id="%s" .*?</hh:numbering>' % nid, h2, re.S)
        h = h2[:m.start()] + m.group(0).replace(ph, ph2, 1) + h2[m.end():]
        rep["num"] += 1
    items[H] = (items[H][0], h.encode("utf-8"))
    with zipfile.ZipFile(path, "w") as zo:
        for info, d in items:
            zo.writestr(info, d, compress_type=zipfile.ZIP_STORED if info.filename == "mimetype" else zipfile.ZIP_DEFLATED)
    return rep


if __name__ == "__main__":
    for f in sys.argv[1:]:
        print(os.path.basename(f), fix(f))
