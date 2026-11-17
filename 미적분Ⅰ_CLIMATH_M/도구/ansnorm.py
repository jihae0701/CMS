# -*- coding: utf-8 -*-
"""해설 첫 문단의 정답 머리를 ' [정답] '으로 통일한다(정답 / 답. / 답 / [[정답]] / 사용자 정의 글자 등).
    python3 ansnorm.py 파일.hwpx"""
import sys, re, zipfile, shutil, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hwpxedit as H
p = sys.argv[1]
x = H.load(p)
HEAD = re.compile(r'^(\s*)(?:\[\[정답\]\]|\[정답\]|정답\s*:?|답\s*\.|답(?=\s)|\U000f00bc)\s*')
n, cnt, odd = 1, 0, []
edits = []
while True:
    try:
        s = H.region(x, n, 'sol')
    except Exception:
        break
    if not s:
        break
    ps = H.paras_in(x, s)
    if ps:
        a, b = ps[0]
        m = re.search(r'<hp:t>([^<]*)</hp:t>', x[a:b])
        if m and HEAD.match(m.group(1)) and not m.group(1).startswith(' [정답] '):
            new = HEAD.sub(' [정답] ', m.group(1), count=1)
            edits.append((a + m.start(1), a + m.end(1), new)); cnt += 1
        elif not (m and m.group(1).lstrip().startswith('[정답]')):
            odd.append(n)
    n += 1
for s0, e0, new in sorted(edits, reverse=True):
    x = x[:s0] + new + x[e0:]
zi = zipfile.ZipFile(p); t = p + '.tmp'; zo = zipfile.ZipFile(t, 'w')
for i in zi.infolist():
    d = zi.read(i.filename)
    if i.filename == 'Contents/section0.xml':
        d = x.encode('utf-8')
    zo.writestr(i, d, compress_type=i.compress_type)
zo.close(); shutil.move(t, p)
print(p, '정답 머리 고침', cnt, '확인할 해설', odd)
