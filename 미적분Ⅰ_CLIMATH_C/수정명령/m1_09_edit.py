# -*- coding: utf-8 -*-
"""미적분Ⅰ 9단원(정적분으로 정의된 함수) 내용 고치기"""
import sys
sys.path.insert(0, '.')
from mjedit import Ed
ed = Ed('u_mj/m1_09.hwpx')
E, T, SA, op = ed.E, ed.T, ed.SA, ed.op
for n, v, m in [(8, '-11', '①'), (13, '0', '①'), (14, '10', '①'), (17, '6', '③'), (18, '5', '①'), (19, '6', '②'), (20, '1', '①'),
                (22, '-1', '③'), (24, '1', '⑤'), (26, '24', '④'), (27, '100', '⑤'), (28, '1', '⑤'), (29, '{15} over {8}', '⑤'), (30, '4', '①')]:
    SA(n, v, m)
SA(15, '2', '③', ending='개수는?', new_ending='개수를 구하시오.')
SA(16, '-2', '①', ending='곱은?', new_ending='곱을 구하시오.')
# 23: 해설이 다른 문제 풀이 → 새로 씀, 정답 13/2
T(23, 'q', '값은?', '값을 구하시오.')
for c in '①②③④⑤':
    op({'op': 'del_para', 'n': 23, 'part': 'q', 'anchor': '^' + c, 'optional': c != '①'})
op({'op': 'clear_sol', 'n': 23, 'part': 'sol'})
op({'op': 'eq', 'n': 23, 'part': 'sol', 'old': '{2}', 'new': '{13} over {2}'})
for t in ['주어진 식의 좌변을 정리하면',
          '⟦int _{0} ^{x} (x-t)f(t)dt=x int _{0} ^{x} f(t)dt- int _{0} ^{x} tf(t)dt⟧',
          '이므로 주어진 식은',
          '⟦x int _{0} ^{x} f(t)dt- int _{0} ^{x} tf(t)dt= {1} over {3} x ^{3} + {1} over {4} x ^{2}⟧',
          '위의 식의 양변을 ⟦x⟧에 대하여 미분하면',
          '⟦int _{0} ^{x} f(t)dt+xf(x)-xf(x)=x ^{2} + {1} over {2} x⟧',
          '⟦therefore~ int _{0} ^{x} f(t)dt=x ^{2} + {1} over {2} x⟧',
          '위의 식의 양변을 다시 ⟦x⟧에 대하여 미분하면',
          '⟦f(x)=2x+ {1} over {2}⟧',
          '⟦therefore~f(3)=6+ {1} over {2} = {13} over {2}⟧']:
    op({'op': 'add_para', 'n': 23, 'part': 'sol', 'text': t, 'like_n': 31, 'like': '이므로 주어진 식은'})
T(3, 'sol', '대입하면◀', '대입하면 ')
E(7, 'sol', '=6x ^{3} +f LEFT', sub='=6x ^{2} +f LEFT')
T(9, 'sol', '[다른풀이]', '[다른 풀이]')
E(10, 'sol', 'd} t', sub='dt}')
E(12, 'sol', 'int _{2} ^{2+x}', sub='int _{2} ^{2+2x}')
E(13, 'sol', 'k="-4"', 'k= it-4')
E(15, 'sol', '(2x+1)f(t)', sub='(2x+1)f(t)dt')
E(18, 'sol', '=3x  ^{2} -4a+1', sub='=3x  ^{2} -4x+1')
T(20, 'sol', '㉠에 양변을 ', '㉠의 양변에 ')
E(20, 'sol', '=12x  ^{2} -4x', sub='=12x  ^{3} -4x')
E(33, 'sol', 'int_3 ^3', sub='int_-3 ^3')
E(37, 'q', 'lim _{x `->` 2} int_2 ^x', sub='lim _{x `->` 2} {1} over {x-2} int_2 ^x')
ed.run('u_mj/m1_09_edit.json')
