# -*- coding: utf-8 -*-
"""미적분Ⅰ 5단원(도함수의 활용(2)) 내용 고치기"""
import sys
sys.path.insert(0, '.')
from mjedit import Ed
ed = Ed('u_mj/m1_05.hwpx')
E, T, SA, op = ed.E, ed.T, ed.SA, ed.op
for n, v, m in [(13, '9', '④'), (15, '9', '④'), (20, '-3', '②'), (21, '30', '③'), (23, '4', '④'), (25, '3', '②'), (27, '1', '①'),
                (29, '10', '⑤'), (39, '256', '③'), (48, '5', '②')]:
    SA(n, v, m)
for n, v, m in [(16, '-2', '①'), (18, '5', '③'), (32, '-3', '③')]:
    SA(n, v, m, ending='합은?', new_ending='합을 구하시오.')
for n, v, m in [(24, '5', '③'), (31, '10', '④'), (35, '1', '①')]:
    SA(n, v, m, ending='개수는?', new_ending='개수를 구하시오.')
SA(33, 'a> {3} over {2}', '③', ending='범위는?', new_ending='범위를 구하시오.')
SA(49, 'a LEQ it-34', '②', ending='범위는?', new_ending='범위를 구하시오.')
SA(40, '{20} over {3} `` rm cm', '③', ending='길이는?', new_ending='길이를 구하시오.')
SA(19, '5', '⑤', ending='몇 시간 동안인가?', new_ending='몇 시간 동안인지 구하시오.')
# 19 정답 뒤 '시간'
op({'op': 'append', 'n': 19, 'part': 'sol', 'after_eq': '5', 'text': '시간', 'nth': 1})
# 14: 최댓값·최솟값 서술형 정답
T(14, 'q', '최솟값은?', '최솟값을 구하시오.')
op({'op': 'del_para', 'n': 14, 'part': 'q', 'anchor': '^①'})
for c in '②③④⑤':
    op({'op': 'del_para', 'n': 14, 'part': 'q', 'anchor': '^' + c, 'optional': True})
op({'op': 'text_eq', 'n': 14, 'part': 'sol', 'old': ' [정답] ③', 'pre': ' [정답] 최댓값 ', 'eq': '3', 'post': ', 최솟값은 없다.'})

E(1, 'q', '[2,~inf]', sub='[2,~inf)')
T(2, 'sol', '풀이참조', '풀이 참조')
op({'op': 'text', 'n': 6, 'part': 'sol', 'old': ' [정답] ⑴ 극댓값 ', 'new': ' [정답] ⑴ 극솟값 ', 'exact': True})
T(6, 'sol', ' 극솟값 ', ' 극댓값 ', exact=True)
T(12, 'sol', '도는', '또는')
E(19, 'sol', '+6t+20>0', sub='+6t+20 GEQ 0')
E(22, 'sol', '(2,~5)', sub='[2,~5]')
E(26, 'sol', "f`'(x)-3x", sub="f`'(x)= it-3x")
op({'op': 'add_para', 'n': 30, 'part': 'sol', 'text': '따라서 ⟦a⟧의 값이 될 수 없는 것은 ② ⟦0⟧이다.', 'like_n': 30, 'like': '판별식을'})
for s in [s for s in ed.scripts(40, 'sol') if 'rmcm' in s]:
    op({'op': 'eq', 'n': 40, 'part': 'sol', 'old': s, 'new': s.replace('rmcm', 'rm cm')})
T(41, 'q', '같을 ⏎때', '같을 때')
T(43, 'q', '을 구하시오.', '의 값을 구하시오.', after_eq='M`+ m')
E(48, 'sol', '4a+b= it-14', sub='4a+b=14')
ed.run('u_mj/m1_05_edit.json')
