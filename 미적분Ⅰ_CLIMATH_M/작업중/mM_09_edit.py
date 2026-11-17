# -*- coding: utf-8 -*-
"""미적분Ⅰ M 9단원(정적분으로 정의된 함수) — C에서 옮기지 못한 문항 고치기 (끝에 negsub.py)"""
import sys
sys.path.insert(0, '.')
from mjedit import Ed
ed = Ed(sys.argv[1] if len(sys.argv) > 1 else 'u_mM/mM_09.hwpx')
E, T, SA, op = ed.E, ed.T, ed.SA, ed.op
op({'op': 'text_eq', 'n': 9, 'part': 'sol', 'old': ' [정답] ', 'pre': ' [정답] ', 'eq': 'f(x)=12x-2', 'post': ''}) if False else None
E(9, 'sol', '{LEFT ( x-t RIGHT ) f LEFT ( t RIGHT ) d} t', sub='{LEFT ( x-t RIGHT ) f LEFT ( t RIGHT ) dt}')
op({'op': 'eq', 'n': 9, 'part': 'sol', 'old': ' {12x-2}', 'new': 'f(x)=12x-2'})
T(11, 'q', '의 극댓값은? [4점]', '의 극댓값은?')
for n, v, mk, end, ne in [(11, '26', '⑤', '극댓값은?', '극댓값을 구하시오.'), (24, '{1} over {3}', '①', '최댓값은?', '최댓값을 구하시오.'), (26, '{1} over {2}', '③', '값은?', '값을 구하시오.'),
                          (33, '- {3} over {2}', '③', '값은?', '값을 구하시오.'), (34, '-4', '①', '값은?', '값을 구하시오.'), (44, '0', '③', '값은?', '값을 구하시오.'),
                          (45, 'sqrt {6}', '④', '최댓값은?', '최댓값을 구하시오.')]:
    SA(n, v, mk, ending=end, new_ending=ne)
E(12, 'sol', 'A`= LEFT { x   `LEFT | `it RIGHT .  f LEFT ( x RIGHT ) neq 0 RIGHT }`', 'A= LEFT { x left| f LEFT ( x RIGHT ) neq 0 RIGHT }')
E(12, 'sol', 'g   LEFT ( x  RIGHT ) = {1} over {3} x ^{3} +x ^{2} +a  ~ LEFT ( a RIGHT .`', 'g LEFT ( x RIGHT ) = {1} over {3} x ^{3} +x ^{2} +a')
T(12, 'sol', '는 실수', ' (a는 실수)')
op({'op': 'text_eq', 'n': 12, 'part': 'sol', 'old': 'a는 실수', 'pre': '', 'eq': 'a', 'post': '는 실수', 'sub': True})
op({'op': 'del_eq', 'n': 12, 'part': 'sol', 'old': 'LEFT. it RIGHT )'})
T(24, 'sol', '이라하면', '이라 하면')
E(41, 'sol', 'f` prime (x)+x(2x+k)+x ^{2} +kx-1=3x ^{2} +8x-2', sub='f` prime (x)+x(2x+k)+x ^{2} +kx-1-k=3x ^{2} +8x-2')
E(41, 'sol', 'THEREFORE ~k= it 1', 'THEREFORE ~k=1')
# 42: 정답 오류 40 → 28
E(42, 'sol', 'g(x)-8 RIGHT =3x(x+2)', sub='g(x)-8=3x(x+2)')
E(42, 'sol', 'f(2)+g(2)=8+32=40', 'f(2)+g(2)=-4+32=28')
op({'op': 'eq', 'n': 42, 'part': 'sol', 'old': '40', 'new': '28'})
# 43 ㄷ 집합
E(43, 'q', 'LEFT { `k`` LEFT | `` int _{-1} ^{x}', 'LEFT { k left| int _{-1} ^{k} {g prime LEFT ( x RIGHT ) dx} =0,~k')
E(43, 'q', 'LEFT. pile{`#`} RIGHT }', 'RIGHT }')
E(44, 'sol', "LEFT ( x^n RIGHT )' =nx^n-1", "LEFT ( x^n RIGHT )' =nx^{n-1}")
E(45, 'q', '{a}{{from^2020^11^대수능고3나^5}}', 'a')
for s in [s for s in ed.scripts(45, 'sol') if '2x ^ int' in s]:
    op({'op': 'eq', 'n': 45, 'part': 'sol', 'old': s, 'new': s.replace('2x ^ int', '2x int')})
for a_, b_ in (('ⅰ) ', '(ⅰ) '), ('ⅱ) ', '(ⅱ) '), ('ⅲ) ', '(ⅲ) ')):
    T(45, 'sol', a_, b_, exact=True)
T(45, 'sol', '인 어떤점에서 ', '인 어떤 점에서 ')
T(45, 'sol', '경우에 항상  ', '인 경우에 항상 ')
T(45, 'sol', '면 되고, 최대의 ', '이면 되고, 최대의 ')
ed.run('u_mM/mM_09_edit.json')
