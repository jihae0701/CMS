# -*- coding: utf-8 -*-
"""미적분Ⅰ 6단원(도함수의 활용(3)) 내용 고치기"""
import sys
sys.path.insert(0, '.')
from mjedit import Ed
ed = Ed('u_mj/m1_06.hwpx')
E, T, SA, op = ed.E, ed.T, ed.SA, ed.op
SA(5, '-1<k<1', '④', ending='범위는?', new_ending='범위를 구하시오.')
SA(19, '0<m<4', '②', ending='범위는?', new_ending='범위를 구하시오.')
SA(25, 'a GEQ 4', '③', ending='범위는?', new_ending='범위를 구하시오.')
SA(41, '{1} over {2} <t<4', '①', ending='범위는?', new_ending='범위를 구하시오.')
SA(6, '-21', '①', ending='합은?', new_ending='합을 구하시오.')
SA(20, '-13', '③', ending='합은?', new_ending='합을 구하시오.')
SA(18, '6', '①', ending='개수는?', new_ending='개수를 구하시오.')
SA(16, '-50', '①', ending='가속도는?', new_ending='가속도를 구하시오.')
SA(27, '-3', '③', ending='가속도는?', new_ending='가속도를 구하시오.')
for n, v, m in [(15, '2', '②'), (21, '1', '①'), (23, '- {2} over {3}', '②'), (26, '12', '②'), (28, '5', '⑤'), (35, '2', '②')]:
    SA(n, v, m)
# 39: 정답 줄은 이미 값(8) — 묻는 말과 선택지만
T(39, 'q', '최댓값은?', '최댓값을 구하시오.')
for c in '①②③④⑤':
    op({'op': 'del_para', 'n': 39, 'part': 'q', 'anchor': '^' + c, 'optional': c != '①'})

E(7, 'sol', '=l`', sub='=k`')
E(9, 'sol', 'f`(x) = x^3 + 2ax^2', sub='f`(x) = x^4 + 2ax^2')
E(10, 'sol', 'x^3 +2x+a ge', sub='x^4 +2x+a ge')
op({'op': 'del_eq', 'n': 12, 'part': 'sol', 'old': '-27', 'first': True})
T(12, 'sol', '대의', '때의')
E(22, 'sol', 'f LEFT =( x RIGHT ) x', sub='f LEFT ( x RIGHT ) =x')
T(22, 'sol', '삼차 방정식', '삼차방정식'); T(22, 'sol', '이 때,', '이때,')
E(22, 'sol', '.....', 'cdots cdots')
E(29, 'q', '2t  ^{3} -9t+12t', sub='2t  ^{3} -9t  ^{2} +12t')
T(32, 'q', '구하시오. 단,', '구하시오. (단, ')
E(33, 'sol', ' g(x)=6x^2 +6x-12', sub=" g'(x)=6x^2 +6x-12")
E(34, 'q', '-12+3-k', sub='-12x+3-k')
for n in (37, 39, 40):
    for s in [s for s in ed.scripts(n, 'q') if '\t' in s]:
        op({'op': 'eq', 'n': n, 'part': 'q', 'old': s, 'new': s.replace('\t', ' ')})
T(37, 'sol', '이 개수는', '의 개수는')
op({'op': 'add_para', 'n': 37, 'part': 'sol', 'after': 'f LEFT ( x RIGHT ) =4x  ^{3} -ax  ^{2} +2⟧로 놓으면', 'like_n': 37, 'like': '로 놓으면',
    'text': "⟦f prime LEFT ( x RIGHT ) =12x ^{2} -2ax=2x LEFT ( 6x-a RIGHT )⟧"})
E(38, 'sol', '+2x+2+(x+1)', sub='+2x+2=(x+1)')
# 42: 정답 줄과 해설 다시 씀
op({'op': 'del_eq', 'n': 42, 'part': 'sol', 'old': '{ㄱ,`ㄴ}'})
op({'op': 'text', 'n': 42, 'part': 'sol', 'old': ' [정답] ', 'new': ' [정답] ③', 'exact': True})
for a in ('v>2,`t>2', '= it-x+2', '그런데', '따라서 옳은 것은'):
    op({'op': 'del_para', 'n': 42, 'part': 'sol', 'anchor': a})
for t in ['ㄱ. ⟦t<2⟧일 때 ⟦v>0⟧, ⟦t>2⟧일 때 ⟦v<0⟧이고, ⟦t=2⟧일 때 ⟦v=0⟧이므로 ⟦t=2⟧일 때 움직이는 방향이 반대로 바뀐다. (참)',
          'ㄴ. ⟦1<t<3⟧에서 ⟦v(t)= it-t+2⟧이므로 가속도는 ⟦a(t)=v prime (t)= it-1⟧로 일정하다. (참)',
          'ㄷ. ⟦v=0⟧이면 물체는 움직이는 방향을 바꾸거나 정지한다.⏎그런데 ⟦t=4⟧에서 ⟦v= it-1⟧이므로 물체는 정지해 있지 않다. (거짓)',
          '따라서 옳은 것은 ㄱ, ㄴ이다.']:
    op({'op': 'add_para', 'n': 42, 'part': 'sol', 'text': t, 'like_n': 41, 'like': '이때, 두 점'})
ed.run('u_mj/m1_06_edit.json')
