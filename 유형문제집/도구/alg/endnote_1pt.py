# -*- coding: utf-8 -*-
"""본문의 미주 표시(미주 조종 글자가 든 run)를 모두 글자 크기 1pt로 (2026-11-27 사용자 '미주 크기 모두 1인지 확인해').
num_inline.tiny()는 run 맨 앞이 미주일 때만 잡아서, 그림이 앞에 묶인 번호 문단·워크북(3pt)이 남았음 → run 안 어디에 있든 바꿈.
python endnote_1pt.py <hwpx> ...   (제자리)
"""
import re, sys, zipfile, os
RUN = re.compile(r'<hp:run charPrIDRef="(\d+)">((?:(?!</hp:run>).)*?<hp:ctrl><hp:endNote )', re.S)


def fix(path):
    zi = zipfile.ZipFile(path); items = [(i, zi.read(i.filename)) for i in zi.infolist()]; zi.close()
    H = next(k for k, (i, _) in enumerate(items) if i.filename == "Contents/header.xml")
    h = items[H][1].decode("utf-8")
    new, n = {}, 0
    for k, (info, d) in enumerate(items):
        if not re.match(r"Contents/section\d+\.xml", info.filename):
            continue
        s = d.decode("utf-8")
        def f(m):
            global_h = None
            nonlocal h, n
            cid = m.group(1)
            hh = re.search(r'<hh:charPr id="%s" height="(\d+)"' % cid, h).group(1)
            if hh == "100":
                return m.group(0)
            if cid not in new:
                blk = re.search(r'<hh:charPr id="%s" .*?</hh:charPr>' % cid, h, re.S).group(0)
                c = re.search(r'<hh:charProperties itemCnt="(\d+)"', h)
                nid = int(c.group(1))
                blk = re.sub(r'height="\d+"', 'height="100"', blk.replace('id="%s"' % cid, 'id="%d"' % nid, 1), count=1)
                h = h[:c.start()] + '<hh:charProperties itemCnt="%d"' % (nid + 1) + h[c.end():]
                e = h.index("</hh:charProperties>")
                h = h[:e] + blk + h[e:]
                new[cid] = str(nid)
            n += 1
            return '<hp:run charPrIDRef="%s">' % new[cid] + m.group(2)
        s = RUN.sub(f, s)
        items[k] = (info, s.encode("utf-8"))
    items[H] = (items[H][0], h.encode("utf-8"))
    with zipfile.ZipFile(path, "w") as zo:
        for info, d in items:
            zo.writestr(info, d, compress_type=zipfile.ZIP_STORED if info.filename == "mimetype" else zipfile.ZIP_DEFLATED)
    return n


if __name__ == "__main__":
    for f in sys.argv[1:]:
        print(os.path.basename(f), "1pt로 바꾼 미주 표시", fix(f))
