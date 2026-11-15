# -*- coding: utf-8 -*-
"""문항 문단을 글(T)·수식(E) 조각으로 보여 준다 (수정 명령을 정확히 쓰기 위해).
    python3 dumpu.py 파일.hwpx 7q 7s 51 ...   (q=문제, s=해설, 숫자만이면 둘 다)"""
import sys, re, html
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from hwpxedit import load, region, paras_in, SC
TOK = re.compile(r'<hp:equation\b.*?</hp:equation>|<hp:t>(?:[^<]|<hp:lineBreak/>|<hp:tab[^>]*/>)*</hp:t>|<hp:(?:tbl|pic|container|rect)\b', re.S)
def toks(p):
    out = []
    for m in TOK.finditer(p):
        g = m.group(0)
        if g.startswith('<hp:equation'):
            sm = SC.search(g); out.append('E' + repr(html.unescape(sm.group(2)) if sm else ''))
        elif g.startswith('<hp:t>'):
            out.append('T' + repr(html.unescape(re.sub(r'<hp:lineBreak/>', '⏎', re.sub(r'<hp:tab[^>]*/>', '⇥', g[6:-7])))))
        else:
            out.append('{' + g[4:] + '}')
    return out
x = load(sys.argv[1])
for a in sys.argv[2:]:
    n = int(re.match(r'\d+', a).group(0)); suf = a[len(str(n)):]
    parts = {'q': ['q'], 's': ['sol'], '': ['q', 'sol']}[suf]
    for part in parts:
        print('【%d %s】' % (n, part))
        for s, e in paras_in(x, region(x, n, part)):
            seg = x[s:e]
            if part == 'q':
                seg = re.sub(r'<hp:endNote\b.*?</hp:endNote>', '', seg, flags=re.S)
            t = toks(seg)
            if t:
                print('  ¶', ' '.join(t)[:1500])
