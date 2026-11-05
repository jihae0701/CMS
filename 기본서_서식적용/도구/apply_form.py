"""HWP 파일의 용지 여백·바탕쪽 개체 위치를 서식(1. 다항식의 연산과 항등식.hwpx)과 같게 맞춘다. 내용은 건드리지 않는다.
python3 apply_form.py 입력.hwp 출력.hwp"""
import sys, struct, zlib
sys.path.insert(0, __import__('os').path.dirname(__file__))
from hwplib import Hwp, recs, pack
import cfb
HB = 16
# 서식 값 (HWPUNIT)
PAGE = dict(left=4535, right=4535, top=850, bottom=6236, header=7086, footer=2834, gutter=2267)
TEXT_H = 86174     # 바탕쪽 글 영역 높이
# 바탕쪽 개체: (쪽, 폭, 높이) -> (세로 위치, 가로 위치)
POS = {
    (0, 61514, 5936): (566, 4251),      # 단원명 표
    (0, 1, 88021): (6655, 35268),       # 단 구분 세로선
    (0, 61395, 1): (94677, 0),          # 아래 가로선
    (0, 10113, 2374): (94535, 37),      # 과목명 상자
    (0, 4473, 1867): (95244, 32985),    # 쪽 번호 상자
    (1, 61514, 5936): (566, 4251),
    (1, 1, 88022): (6599, 37533),
    (1, 4473, 1867): (95332, 35340),
    (1, 62106, 3223): (94005, 6803),    # 로고 묶음
}

def patch_section(data):
    rs = recs(data)
    mp = -1; done = set(); npage = 0; insecd = False
    for r in rs:
        t, l, p = r
        if t == HB + 55 and l == 1 and p[:4] == b'dces':
            insecd = True; continue
        if insecd and l <= 1:
            insecd = False
        if not insecd:
            continue
        if t == HB + 57:   # PAGE_DEF
            w, h, L, R, T, B, hd, ft, g = struct.unpack_from('<9I', p)
            p = struct.pack('<9I', w, h, PAGE['left'], PAGE['right'], PAGE['top'], PAGE['bottom'],
                            PAGE['header'], PAGE['footer'], PAGE['gutter']) + p[36:]
            r[2] = p; npage += 1
        elif t == HB + 56 and l == 2:   # 바탕쪽 글 목록
            mp += 1
            p = bytearray(p); struct.pack_into('<I', p, 12, TEXT_H); r[2] = bytes(p)
        elif t == HB + 55 and l == 3 and mp in (0, 1):
            w, hgt = struct.unpack_from('<II', p, 16)
            key = (mp, w, hgt)
            vo, ho = POS[key]
            p = bytearray(p); struct.pack_into('<ii', p, 8, vo, ho); r[2] = bytes(p)
            done.add(key)
    assert npage == 1 and mp == 1 and done == set(POS), (npage, set(POS) - done)
    return pack(rs)

def main(src, dst):
    h = Hwp(src)
    root = cfb.read_tree(src)
    node = cfb.find(root, 'BodyText/Section0')
    raw = h.stream('BodyText/Section0')
    new = patch_section(raw)
    assert len(new) == len(raw)
    if h.compressed:
        import hwpzip; data = hwpzip.compress(new)
    else:
        data = new
    import inplace
    if not inplace.replace_stream(src, dst, ['BodyText', 'Section0'], data):
        node.data = data
        cfb.write(root, dst)
        return 'rewrite'
    return 'inplace'

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
