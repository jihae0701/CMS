# -*- coding: utf-8 -*-
"""정답 줄 머리 통일: 미주 첫 문단의 '정답', '[정답]', '답', 머리 없음 → 정답 기호 󰂼
    python3 anshead.py 파일.hwpx"""
import sys, re, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hwpxedit import load, save, endnotes, paras_in, TPAT
A = '\U000f00bc'
path = sys.argv[1]
x = load(path)
log = []
for k in range(len(endnotes(x)) - 1, -1, -1):
    s, e = endnotes(x)[k]
    ps = paras_in(x, [(s, e)])
    if not ps:
        continue
    a, b = ps[0]
    p = x[a:b]
    if A in p:
        continue
    m = TPAT.search(p)
    if not m:
        continue
    t = m.group(1)
    nt = re.sub(r'^\s*(\[정답\]|정답|답)\s*', ' ' + A + ' ', t, count=1)
    if nt == t:
        nt = ' ' + A + ' ' + t.lstrip()
    p = p[:m.start(1)] + nt + p[m.end(1):]
    x = x[:a] + p + x[b:]
    log.append((k + 1, t[:12], nt[:14]))
save(path, x)
for l in reversed(log):
    print('  ', l)
print('정답 줄 머리 고침', len(log))
