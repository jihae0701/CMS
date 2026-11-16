# -*- coding: utf-8 -*-
"""미적분Ⅰ 7단원(부정적분) 내용 고치기"""
import sys
sys.path.insert(0, '.')
from mjedit import Ed
ed = Ed('u_mj/m1_07.hwpx')
E, T, SA, op = ed.E, ed.T, ed.SA, ed.op
for n, v, m in [(5, '6', '③'), (6, '-6', '①'), (18, '10', '⑤'), (21, '16', '⑤'), (22, '-17', '⑤'), (23, '{8} over {3}', '④'),
                (26, '9', '⑤'), (33, '{8} over {3}', '④'), (34, '-1', '②'), (41, '-1', '②')]:
    SA(n, v, m)
SA(25, '-1', '②', ending='곱은?', new_ending='곱을 구하시오.')
def split(n, v, m, ending='값은?', new_ending='값을 구하시오.'):   # 정답 줄이 ' [정답] ' + '④' 두 조각
    T(n, 'q', ending, new_ending)
    for c in '①②③④⑤':
        op({'op': 'del_para', 'n': n, 'part': 'q', 'anchor': '^' + c, 'optional': c != '①'})
    op({'op': 'text_eq', 'n': n, 'part': 'sol', 'old': m, 'pre': '', 'eq': v, 'post': ''})
split(16, '-5', '⑤'); split(27, '0', '③'); split(28, '{1} over {6}', '④'); split(29, '-2', '①'); split(40, '- {2} over {3}', '②', '곱은?', '곱을 구하시오.')
def qonly(n, ending='값은?', new_ending='값을 구하시오.'):     # 정답 줄은 이미 값
    T(n, 'q', ending, new_ending)
    for c in '①②③④⑤':
        op({'op': 'del_para', 'n': n, 'part': 'q', 'anchor': '^' + c, 'optional': c != '①'})
qonly(35); qonly(42); qonly(44)

op({'op': 'del_eq', 'n': 14, 'part': 'q', 'old': ''})
E(14, 'sol', 'int(4x  ^{2} -6x', sub='int(4x  ^{3} -6x')
E(18, 'sol', 'f(0-h)', sub='f(0+h)')
for s in [s for s in ed.scripts(23, 'q') if '\t' in s]:
    op({'op': 'eq', 'n': 23, 'part': 'q', 'old': s, 'new': s.replace('\t', ' ')})
for s in [s for s in ed.scripts(23, 'sol') if '\t' in s]:
    op({'op': 'eq', 'n': 23, 'part': 'sol', 'old': s, 'new': s.replace('\t', ' ')})
E(28, 'sol', 'over {x+2} dx+ int', "f(x)= int _ ^ {x ^{3} -2x} over {x-1} dx+ int _ ^ {2x-1} over {x-1} dx")
E(28, 'sol', 'over {x-1}\'' if False else '(x^2 +x+1)} over {x-1}', sub='(x^2 +x+1)} over {x-1} dx')
E(34, 'q', 'f(2', 'f(2)')
T(34, 'q', ')의 값을', '의 값을')
for part in ('q', 'sol'):
    for s in [s for s in ed.scripts(36, part) if 'lim _{n `->` inf}' in s]:
        op({'op': 'eq', 'n': 36, 'part': part, 'old': s, 'new': s.replace('lim _{n `->` inf}', 'lim _{x `->` inf}')})
E(41, 'q', 'f(x', 'f(x)')
T(41, 'q', ')가 ', '가 ')
E(41, 'sol', '-4x ^', sub='-4x')
E(41, 'sol', 'C="3"', 'C=3')
E(42, 'sol', '0.~3', sub='0,~3')
E(43, 'q', 'f(x) +4 } RIGHT', sub='f(x) +4x RIGHT }')
E(44, 'sol', '-2 + C = 2', sub='-2 + C_1 = 2')
ed.run('u_mj/m1_07_edit.json')
