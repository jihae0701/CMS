# -*- coding: utf-8 -*-
"""HWP5(.hwp) 본문 글과 수식 스크립트 꺼내기 (pyhwp 없이 olefile만 사용).
python hwp5text.py 입력.hwp > 출력.txt
- 문단마다 한 줄, 수식은 $...$ 로 그 자리에 넣는다. 표 칸의 문단도 차례대로 나온다.
- 그림은 [그림], 표 시작은 [표] 로 표시.
"""
import sys, zlib, struct
import olefile

TAG_PARA_HEADER, TAG_PARA_TEXT, TAG_CTRL_HEADER, TAG_EQEDIT = 66, 67, 71, 88
EXT = {1, 2, 3, 11, 12, 14, 15, 16, 17, 18, 21, 22, 23}       # 확장·인라인 컨트롤(8 wchar)
INL = {4, 5, 6, 7, 8, 9, 19, 20}


def records(data):
    i, n = 0, len(data)
    while i + 4 <= n:
        h = struct.unpack_from("<I", data, i)[0]; i += 4
        tag, lvl, size = h & 0x3FF, (h >> 10) & 0x3FF, h >> 20
        if size == 0xFFF:
            size = struct.unpack_from("<I", data, i)[0]; i += 4
        yield tag, lvl, data[i:i + size]
        i += size


def para_text(b):
    out, ctrls, i = [], [], 0
    while i + 2 <= len(b):
        c = struct.unpack_from("<H", b, i)[0]
        if c in EXT or c in INL:
            if c in EXT:
                cid = b[i + 2:i + 6][::-1].decode("latin1")
                out.append(("C", cid)); ctrls.append(cid)
            i += 16; continue
        if c == 13:
            break
        if c == 10:
            out.append(("T", "\n"))
        elif c == 9:
            out.append(("T", " "))
        elif c >= 32:
            out.append(("T", chr(c)))
        i += 2
    return out


def extract(path):
    ole = olefile.OleFileIO(path)
    hdr = ole.openstream("FileHeader").read()
    comp = struct.unpack_from("<I", hdr, 36)[0] & 1
    secs = sorted((s for s in ole.listdir() if s[0] == "BodyText"), key=lambda s: int(s[1][7:]))
    paras = []          # [level, parts, eq_slots]
    cur_lvl = 0
    for s in secs:
        data = ole.openstream(s).read()
        if comp:
            data = zlib.decompress(data, -15)
        for tag, lvl, b in records(data):
            if tag == TAG_PARA_HEADER:
                cur_lvl = lvl
            elif tag == TAG_PARA_TEXT:
                parts = para_text(b)
                paras.append([cur_lvl, parts])
            elif tag == TAG_EQEDIT:
                ln = struct.unpack_from("<H", b, 4)[0]
                scr = b[6:6 + 2 * ln].decode("utf-16-le", "replace")
                for p in reversed(paras):
                    if p[0] == lvl - 2 and any(x == ("C", "eqed") for x in p[1]):
                        k = p[1].index(("C", "eqed"))
                        p[1][k] = ("T", " $" + scr.replace("\r\n", " ").replace("\n", " ") + "$ ")
                        break
    lines = []
    for lvl, parts in paras:
        t = "".join(v if k == "T" else {"gso ": "[그림]", "tbl ": "[표]", "eqed": "[수식?]"}.get(v, "") for k, v in parts)
        t = t.strip()
        if t:
            lines.append(t)
    return "\n".join(lines)


if __name__ == "__main__":
    sys.stdout.write(extract(sys.argv[1]) + "\n")
