# -*- coding: utf-8 -*-
"""정답 줄에 '또는'·±·쉼표로 여러 값이 있는 문항과 그 문제 끝 문장을 보여 준다 ("모두 구하시오" 검토용)"""
import sys, re
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from hwpxedit import load, region, paras_in, render, endnotes
x = load(sys.argv[1])
for n in range(1, len(endnotes(x)) + 1):
    sol = [render(x[s:e]).strip() for s, e in paras_in(x, region(x, n, 'sol'))]
    ans = sol[0] if sol else ''
    if re.search(r'또는|±|\+-|\bpm\b', ans):
        q = ' '.join(render(re.sub(r'<hp:endNote\b.*?</hp:endNote>', '', x[s:e], flags=re.S)).strip() for s, e in paras_in(x, region(x, n, 'q')))
        q = re.sub(r'\{(rect|container|tbl|pic)\}[^⟦]*?>', '', q)
        qs = re.findall(r'[^.?]*(?:구하시오|구하여라|푸시오|구한 것은|값은)[^.]*\.?', q)
        print(n, '| 정답:', ans[:90].replace('\n', ' '), '| 문제:', ' / '.join(t.strip()[-70:] for t in qs)[:260])
