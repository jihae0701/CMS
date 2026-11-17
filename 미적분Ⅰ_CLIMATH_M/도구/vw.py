# -*- coding: utf-8 -*-
"""문제·해설 보기: python3 vw.py 파일 번호... (수식 ⟦…⟧, 그림 [그림], 표 [표] 줄임)"""
import sys, re, html, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hwpxedit as H
x = H.load(sys.argv[1])
def show(a, b, part='sol'):
    s = x[a:b]
    if part == 'q':
        s = re.sub(r'<hp:endNote\b.*?</hp:endNote>', '', s, flags=re.S)
    s = re.sub(r'<hp:equation (?:(?!</hp:equation>).)*?<hp:script\b[^>]*>(.*?)</hp:script></hp:equation>', lambda m: '⟦' + m.group(1).replace('<', '&lt;') + '⟧', s, flags=re.S)
    s = re.sub(r'<hp:pic (?:(?!</hp:pic>).)*</hp:pic>', '[그림]', s, flags=re.S)
    s = re.sub(r'<hp:lineBreak/>', '⏎', s)
    s = re.sub(r'<hp:tab[^>]*/>', ' ', s)
    s = re.sub(r'<hp:(rect|container|tbl|line|ellipse|polygon|curve)\b', r'[\1]<x', s)
    s = re.sub(r'<[^>]+>', '', s)
    s = re.sub(r'그림입니다\.|사각형입니다\.|묶음 개체입니다\.|수식입니다\.|원본 그림의 (이름|크기):\S*( \S*)?', '', s)
    return html.unescape(s)
for a in sys.argv[2:]:
    n = int(a)
    for part in ('q', 'sol'):
        print('【%d %s】' % (n, part))
        for s0, e0 in H.paras_in(x, H.region(x, n, part)):
            t = show(s0, e0, part).strip()
            if t:
                print('  ¶', t[:900])
