# -*- coding: utf-8 -*-
"""줄 배치 정보(linesegarray)가 없는 문단에 한 줄짜리 줄 배치 정보를 넣는다(한글이 열 때 다시 배치함).
    python3 fix_lsa.py 파일.hwpx
본보기: 같은 paraPrIDRef를 쓰는 문단 중 자기 줄 배치 정보가 있는 문단의 첫 줄(textpos=0)."""
import sys, re, zipfile, shutil


def own_lsa(seg):
    k = seg.rfind('<hp:linesegarray>')
    if k < 0 or seg.find('</hp:run>', k) >= 0:
        return None
    return seg[k:seg.index('</hp:linesegarray>', k) + len('</hp:linesegarray>')]


def fix(x):
    spans, stack = [], []
    for m in re.finditer(r'<(/?)hp:p\b[^>]*?(/?)>', x):
        if m.group(2) == '/':
            continue
        if m.group(1) == '':
            stack.append(m.start())
        else:
            spans.append((stack.pop(), m.end()))
    proto, bad = {}, []
    for s, e in spans:
        seg = x[s:e]
        pp = re.match(r'<hp:p\b[^>]*paraPrIDRef="(\d+)"', seg).group(1)
        l = own_lsa(seg)
        if l:
            first = re.search(r'<hp:lineseg\b[^>]*/>', l).group(0)
            proto.setdefault(pp, first)
        else:
            bad.append((e, pp))
    default = next(iter(proto.values()))
    n = 0
    for e, pp in sorted(bad, reverse=True):
        ls = re.sub(r'textpos="\d+"', 'textpos="0"', proto.get(pp, default))
        ins = '<hp:linesegarray>%s</hp:linesegarray>' % ls
        x = x[:e - len('</hp:p>')] + ins + x[e - len('</hp:p>'):]
        n += 1
    return x, n


def trim_overflow(x):
    """줄 기록의 글자 위치가 문단 글자 수를 넘는 문단: 넘는 줄 기록을 지운다"""
    import refcheck, hwpxedit
    bad = refcheck.lineseg_overflow(x)
    for s in sorted(bad, reverse=True):
        depth, e = 0, None
        for t in re.finditer(r'<(/?)hp:p\b[^>]*?(/?)>', x[s:]):
            if t.group(2) == '/':
                continue
            depth += 1 if t.group(1) == '' else -1
            if depth == 0:
                e = s + t.end(); break
        x = x[:s] + hwpxedit.trim_lineseg(x[s:e]) + x[e:]
    return x, len(bad)


def dedupe_ids(x):
    """개체 id가 겹치면 뒤의 것을 새 번호로"""
    import random
    seen, n = set(re.findall(r'<hp:(?:tbl|pic|equation|rect|container|line|ellipse|polygon|arc|curve)\b[^>]*?\bid="(\d+)"', x)), 0
    cnt = {}
    def rep(m):
        nonlocal n
        v = m.group(2)
        cnt[v] = cnt.get(v, 0) + 1
        if v == '0' or cnt[v] == 1:
            return m.group(0)
        while True:
            w = str(random.randint(1000000000, 2100000000))
            if w not in seen:
                break
        seen.add(w); n += 1
        return m.group(1) + w + '"'
    x = re.sub(r'(<hp:(?:tbl|pic|equation|rect|container|line|ellipse|polygon|arc|curve)\b[^>]*?\bid=")(\d+)"', rep, x)
    return x, n


if __name__ == '__main__':
    path = sys.argv[1]
    z = zipfile.ZipFile(path)
    items = [(i, z.read(i.filename)) for i in z.infolist()]
    z.close()
    tot = 0
    with zipfile.ZipFile(path + '.tmp', 'w') as zo:
        for info, data in items:
            if re.match(r'Contents/(section\d+|masterpage\d+)\.xml', info.filename):
                t, n = fix(data.decode('utf-8'))
                t, n2 = trim_overflow(t)
                t, n3 = dedupe_ids(t)
                tot += n
                if n2 or n3:
                    print(info.filename, '넘는 줄 기록 정리 문단', n2, '겹친 개체 id 바꿈', n3)
                data = t.encode('utf-8')
            zo.writestr(info, data, compress_type=info.compress_type)
    shutil.move(path + '.tmp', path)
    print('줄 배치 정보 넣음', tot)
