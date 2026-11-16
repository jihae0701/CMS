# -*- coding: utf-8 -*-
"""미적분Ⅰ 8단원(정적분) 내용 고치기"""
import sys
sys.path.insert(0, '.')
from mjedit import Ed
ed = Ed('u_mj/m1_08.hwpx')
E, T, SA, op = ed.E, ed.T, ed.SA, ed.op
for n, v, m in [(6, '21', '①'), (7, '9', '②'), (8, '- {2} over {3}', '②'), (9, '132', '②'), (10, '64', '⑤'), (11, '{69} over {4}', '③'),
                (12, '{9} over {4}', '③'), (15, '18', '④'), (20, '15', '⑤'), (21, '-4', '①'), (22, '10', '③'), (24, '0', '③'),
                (25, '-2', '①'), (26, '{19} over {3}', '⑤'), (27, '{13} over {12}', '③'), (28, '8', '③'), (29, '-1', '②'),
                (34, '{8} over {3}', '④'), (39, '12', '④'), (40, '11', '①'), (43, '0', '④')]:
    SA(n, v, m)
E(2, 'sol', '(2x^3 -2)dx', sub='(2x^3 -x)dx')
E(3, 'sol', '=27-5=22 RIGHT .', sub='=27-5=22')
E(3, 'sol', 'pile{LEFT [', '= int _{1} ^{2} 4xdx= LEFT [ pile{`#`} 2x ^{2} RIGHT ] _{1} ^{2} =8-2=6')
E(8, 'sol', '{{x^2 +1}-}', 'int_0^1 left( {x^4} over {x^2 +1} - {1} over {x^2 +1} right)dx')
T(13, 'sol', '대임하면', '대입하면')
T(16, 'sol', '⟦x⟧대신' if False else '대신', ' 대신', exact=True)
E(18, 'sol', '+x ^{2} +1 RIGHT ) dx+', sub='+x ^{2} -1 RIGHT ) dx+')
op({'op': 'del_eq', 'n': 24, 'part': 'sol', 'old': ''})
E(25, 'sol', 'f` prime (x) RIGHT', sub='f(x) RIGHT')
T(30, 'sol', '따라서', '따라서 ', exact=False, after_eq=None) if False else None
E(31, 'sol', 'therefore`` LEFT { f', sub='therefore`` int _{-3} ^{3} LEFT { f')
E(40, 'sol', '{f(x)=0}', sub='{f(x)dx} =0')
E(41, 'sol', '``x+2x&', sub='``k+2x&')
# 43 해설 새로 씀
for a in ('int_1^5', 'int_1^2 (-x+3)'):
    op({'op': 'del_para', 'n': 43, 'part': 'sol', 'anchor': a, 'optional': True})
for t in ['적분 구간이 이어지므로 두 정적분을 하나로 합치면',
          '⟦int _{-1} ^{0} (2x ^{3} -6x ^{2} -3x+2)dx+ int _{0} ^{1} (2t ^{3} -6t ^{2} -3t+2)dt⟧⏎⟦= int _{-1} ^{1} (2x ^{3} -6x ^{2} -3x+2)dx⟧',
          '이때, ⟦2x ^{3} -3x⟧는 기함수, ⟦-6x ^{2} +2⟧는 우함수이므로',
          '⟦int _{-1} ^{1} (2x ^{3} -6x ^{2} -3x+2)dx=2 int _{0} ^{1} (-6x ^{2} +2)dx⟧⏎⟦=2 LEFT [ -2x ^{3} +2x RIGHT ] _{0} ^{1} =2 times 0=0⟧']:
    op({'op': 'add_para', 'n': 43, 'part': 'sol', 'text': t, 'like_n': 44, 'like': '20a=20'})
ed.run('u_mj/m1_08_edit.json')
