# -*- coding: utf-8 -*-
"""미적분Ⅰ 4단원(도함수의 활용(1)) 내용 고치기"""
import sys
sys.path.insert(0, '.')
from mjedit import Ed
ed = Ed('u_mj/m1_04.hwpx')
E, T, SA, op = ed.E, ed.T, ed.SA, ed.op

SAL = [(6, '25', '③'), (7, '0', '①'), (15, 'sqrt {3}', '⑤'), (17, '2', '②'), (19, '4', '④'), (20, '5', '⑤'), (21, '-15', '②'),
       (23, '- {1} over {6}', '③'), (24, '6', '①'), (28, '-2', '②'), (29, '-2', '①'), (30, '{2 sqrt {2}} over {3}', '②'),
       (31, '6', '②'), (32, '{27} over {4}', '⑤'), (33, '16', '③'), (34, '-1', '②'), (35, '{7} over {2}', '④'), (36, '-2', '③'),
       (37, '6', '④'), (39, '{1} over {2}', '②'), (44, '6', '⑤')]
for n, v, m in SAL:
    SA(n, v, m)
SA(22, '5', '⑤', ending='절편은?', new_ending='절편을 구하시오.')
SA(25, 'y=3x', '④', ending='방정식은?', new_ending='방정식을 구하시오.')
SA(26, 'y=9x-20', '④', ending='방정식은?', new_ending='방정식을 구하시오.')
SA(27, '3 sqrt {5}', '④', ending='길이는?', new_ending='길이를 구하시오.')
SA(42, 'y=x-1', '②', ending='방정식은?', new_ending='방정식을 구하시오.', sol_old=' [정답] ② ')
SA(45, '{4} over {3}', '②', sol_old=' [정답] ② ')
SA(47, '{sqrt {10}} over {10}', '②', sol_old=' [정답] ② ')
SA(49, '-2', '②', sol_old=' [정답] ② ')

E(15, 'sol', 'f(x)=x  ^{2} +2x', sub='f(x)=x  ^{3} +2x')
T(21, 'q', '이다. 이때, ', '라 할 때, ')
E(22, 'sol', "g'(2)=g(2)", sub="g'(2)=f(2)")
for n in (27, 33):
    for s in [s for s in ed.scripts(n, 'q') if s.strip() in ('RMA', 'RMB', 'RMC', 'RMAB')]:
        op({'op': 'eq', 'n': n, 'part': 'q', 'old': s, 'new': 'rm ' + s.strip()[2:], 'first': True})
T(37, 'q', '만족하는', '만족시키는', all=True)
T(37, 'sol', '만족하는', '만족시키는', all=True)
T(38, 'sol', '닫힌 구간', '닫힌구간')
E(41, 'q', 'x³', sub='x ^{3} ')
E(46, 'sol', '=9a  ^{2}', sub='=9s  ^{2}')
ed.run('u_mj/m1_04_edit.json')
