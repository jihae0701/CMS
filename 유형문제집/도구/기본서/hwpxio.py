# -*- coding: utf-8 -*-
"""HWPX 읽기/쓰기 공용 함수"""
import re, zipfile


def read(path):
    z = zipfile.ZipFile(path)
    files = {i.filename: z.read(i.filename) for i in z.infolist()}
    order = [i.filename for i in z.infolist()]
    return files, order


def write(path, files, order):
    with zipfile.ZipFile(path, "w") as z:
        for name in order:
            data = files[name]
            if name == "mimetype":
                z.writestr(zipfile.ZipInfo(name), data, compress_type=zipfile.ZIP_STORED)
            else:
                z.writestr(name, data, compress_type=zipfile.ZIP_DEFLATED)


def top_spans(x):
    start = x.index(">", x.index("<hs:sec")) + 1
    out, depth, st = [], 0, 0
    for m in re.finditer(r"<hp:p\b[^>]*?(/?)>|</hp:p>", x[start:]):
        t, pos = m.group(0), m.start() + start
        if t.startswith("</"):
            depth -= 1
            if depth == 0:
                out.append((st, m.end() + start))
        elif not t.endswith("/>"):
            if depth == 0:
                st = pos
            depth += 1
    return out


def split(sec):
    sp = top_spans(sec)
    head = sec[:sp[0][0]]
    tail = sec[sp[-1][1]:]
    return head, [sec[a:b] for a, b in sp], tail


def text(x):
    out = []
    for m in re.finditer(r'<hp:t(?:\s[^>]*)?>(.*?)</hp:t>|<hp:script[^>]*>(.*?)</hp:script>', x, re.S):
        if m.group(1) is not None:
            out.append(re.sub(r"<[^>]+>", " ", m.group(1)))
        else:
            out.append("$" + re.sub(r"\s+", " ", m.group(2)).strip() + "$")
    return "".join(out)


def nolines(p):
    return re.sub(r"<hp:linesegarray>.*?</hp:linesegarray>", "", p, flags=re.S)


def set_break(p, page=None, col=None):
    head = re.match(r"<hp:p [^>]*>", p).group(0)
    h = head
    if page is not None:
        h = re.sub(r'pageBreak="\d"', 'pageBreak="%d"' % page, h)
    if col is not None:
        h = re.sub(r'columnBreak="\d"', 'columnBreak="%d"' % col, h)
    return h + p[len(head):]
