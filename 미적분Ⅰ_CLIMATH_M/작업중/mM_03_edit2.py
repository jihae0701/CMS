# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '.')
from mjedit import Ed
ed = Ed('u_mM/mM_03.hwpx')
for n in (46, 59):
    for a in ('>풀이전략', '>문제풀이'):
        ed.op({'op': 'del_para', 'n': n, 'part': 'sol', 'anchor': a})
ed.E(19, 'sol', "THEREFORE f'(-1)+f'(2)=7+13=20", "THEREFORE f'(-1)+f'(2)=7+13=20")
ed.run('u_mM/mM_03_edit2.json')
# (2차) 49 쉼표를 수식 밖으로
ed2 = Ed('u_mM/mM_03.hwpx')
ed2.E(49, 'q', '=0,~-1<a<6 RIGHT } ,', sub='=0,~-1<a<6 RIGHT }')
ed2.op({'op': 'append', 'n': 49, 'part': 'q', 'after_eq': 'A= LEFT { a left| lim _{x `->` a} LEFT { f(x)-f(a) RIGHT } =0,~-1<a<6 RIGHT }', 'text': ','})
ed2.run('u_mM/mM_03_edit2b.json')
