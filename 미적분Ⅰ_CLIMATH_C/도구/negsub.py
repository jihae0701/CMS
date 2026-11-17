# -*- coding: utf-8 -*-
"""수식에서 묶지 않은 음수·식 첨자를 묶는다: int_-1^1 → int_{-1}^1, x^-2 → x^{-2}, sum_k=1^10 → sum_{k=1}^10
   (한글 수식의 첨자는 다음 낱말 하나만 받으므로 '-1'·'k=1'은 묶어야 한다)
   python3 negsub.py 파일.hwpx [--dry]"""
import sys, re, html, zipfile, shutil
sys.path.insert(0, '.')
import hwpxedit as H
P = sys.argv[1]; dry = '--dry' in sys.argv
x = H.load(P)
pat1 = re.compile(r'([_^])(\s?)(-\s?[0-9]+|-[a-z])(?![0-9a-z{])')
pat2 = re.compile(r'_([a-z])=([0-9]+)(?![0-9])')
n = 0
def fix(m):
    global n
    s = html.unescape(m.group(2))
    t = pat2.sub(lambda q: '_{%s=%s}' % (q.group(1), q.group(2)), pat1.sub(lambda q: '%s{%s}' % (q.group(1), q.group(3).replace(' ', '')), s))
    if t != s:
        n += 1
        if dry: print(repr(s), '→', repr(t))
    return m.group(1) + html.escape(t, quote=False) + m.group(3)
y = H.SC.sub(fix, x)
print(P, '첨자 묶음', n)
if not dry and y != x:
    H.save(P, y)
