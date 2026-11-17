# -*- coding: utf-8 -*-
"""정답 머리가 없는 해설 첫 문단 맨 앞 글에 '[정답] ' 넣기: python3 anshead_add.py 파일 n [n...]"""
import sys, re, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hwpxedit as H
p = sys.argv[1]; x = H.load(p)
for n in map(int, sys.argv[2:]):
    s, e = H.paras_in(x, H.region(x, n, 'sol'))[0]
    para = x[s:e]
    assert '[정답]' not in H.render(para), n
    m = re.search(r'<hp:t>([^<]*[^\s<][^<]*)</hp:t>', para)
    para = para[:m.start()] + '<hp:t>[정답] ' + m.group(1).lstrip() + '</hp:t>' + para[m.end():]
    x = x[:s] + para + x[e:]; H._PCACHE.clear()
    print(n, '정답 머리 넣음')
H.save(p, x)
