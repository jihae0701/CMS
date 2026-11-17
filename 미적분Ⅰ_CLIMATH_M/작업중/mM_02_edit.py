# -*- coding: utf-8 -*-
"""미적분Ⅰ M 2단원(함수의 연속) — C에서 옮기지 못한 문항 고치기"""
import sys
sys.path.insert(0, '.')
from mjedit import Ed
ed = Ed(sys.argv[1] if len(sys.argv) > 1 else 'u_mM/mM_02.hwpx')
E, T, SA, op = ed.E, ed.T, ed.SA, ed.op
# C 23번과 같은 문제 오류: 구간 [3, 5] → [-2, 3]
op({'op': 'eq', 'n': 29, 'part': 'q', 'old': '[3,~5]', 'new': '[-2,~3]'})
# 3: 떠도는 수식·글자 지움(C 3번과 같음)
op({'op': 'del_eq', 'n': 3, 'part': 'sol', 'old': 'lim _{x `->` 0+}'})
T(3, 'sol', 'g', '', exact=True)
for n, v, m in [(8, '2', '②'), (17, '1', '④'), (48, '1', '④'), (49, '6', '①')]:
    SA(n, v, m)
SA(35, '12', '①', ending='합은?', new_ending='값의 합을 구하시오.')
# 26: 따옴표 괄호
E(26, 'sol', '"{"a(x-1)^2 +b"}"', sub='LEFT { a(x-1)^2 +b RIGHT }')
# 36: 문제 (나) 4 → -4 (해설에 맞춤)
E(36, 'q', 'over {x-1} =4', sub='over {x-1} = it-4')
T(40, 'q', '는 ', '가 ', after_eq='(f CIRCf)(x)')
T(40, 'q', '함수이 연속성', '함수의 연속성')
# 42
E(42, 'sol', 'THEREFORE ~f(x)=3``(0<x<2)', sub='THEREFORE ~f(x)=2``(0<x<2)')
E(42, 'sol', 'BARHP', sub='bar{HP}')
for s in sorted(set(s for s in ed.scripts(42, 'sol') if s.startswith('RM'))):
    op({'op': 'eq', 'n': 42, 'part': 'sol', 'old': s, 'new': 'rm ' + s[2:], 'all': True})
T(45, 'sol', '적어도 두 개 이상', '적어도 두 개', optional=True)
# 47: 모든 k의 값의 합
SA(47, '24', '③', ending='값은?', new_ending='값의 합을 구하시오.')
T(47, 'sol', '계소', '계수', optional=True)
for n in (47, 48, 49, 53):
    op({'op': 'text', 'n': n, 'part': 'sol', 'old': '[해설] ', 'new': '', 'optional': True})
    op({'op': 'del_para', 'n': n, 'part': 'sol', 'anchor': '[해설]', 'exact': True, 'optional': True})
# 51: 정답 오류 -5 → -6, 해설 새로
SA(51, '-6', '④', ending='값은?')
op({'op': 'del_para', 'n': 51, 'part': 'sol', 'anchor': 'b=it-4'})
for t in ['⟦a != b⟧이므로 ⟦f(x)⟧는 ⟦x=0⟧에서만 불연속이고, ⟦f(x-2)⟧는 ⟦x=2⟧에서만 불연속이다. 따라서 ⟦f(x)f(x-2)⟧가 ⟦x=0⟧, ⟦x=2⟧에서 연속이면 된다.',
          '(ⅰ) ⟦x``->``0⟧일 때 ⟦f(x-2)``->``f(-2)=4+b⟧이므로⏎⟦lim _{x `->` 0+} f(x)f(x-2)=a(4+b)⟧, ⟦lim _{x `->` 0-} f(x)f(x-2)=b(4+b)⟧, ⟦f(0)f(-2)=a(4+b)⟧⏎⟦(a-b)(4+b)=0⟧이고 ⟦a != b⟧이므로 ⟦b= it-4⟧',
          '(ⅱ) ⟦x``->``2⟧일 때 ⟦f(x)``->``f(2)=2+a⟧이므로⏎⟦lim _{x `->` 2+} f(x)f(x-2)=(2+a)a⟧, ⟦lim _{x `->` 2-} f(x)f(x-2)=(2+a)b⟧, ⟦f(2)f(0)=(2+a)a⟧⏎⟦(2+a)(a-b)=0⟧이고 ⟦a != b⟧이므로 ⟦a= it-2⟧',
          '따라서 ⟦a+b=(-2)+(-4)= it-6⟧']:
    op({'op': 'add_para', 'n': 51, 'part': 'sol', 'text': t, 'like_n': 3, 'like': '따라서 모든 실수'})
# 52: 정답 오류 ③ → ⑤, 머리말 지움
op({'op': 'text', 'n': 52, 'part': 'sol', 'old': '답 ③', 'new': ' [정답] ⑤'})
for a in ('[해설]', '[풀이전략]', '다.', '[문제풀이]'):
    op({'op': 'del_para', 'n': 52, 'part': 'sol', 'anchor': a, 'exact': True})
for a in ('^[step1]', '^[step2]'):
    op({'op': 'del_para', 'n': 52, 'part': 'sol', 'anchor': a})
E(52, 'sol', '=2 lim _{t `->` 2} { f(t)-3}', sub='=2 lim _{t `->` 2} f(t)-3')
# 53
E(53, 'sol', 'g(0)= lim _{x `->` 0-} {g(x)=1`,``` lim _{a `->` 0+} {g(x)= it-1}}', 'g(0)= lim _{x `->` 0-} g(x)=1`,``` lim _{x `->` 0+} g(x)= it-1')
E(53, 'sol', 'lim _{t `->` 0+} {g(x)}}', sub='lim _{x `->` 0+} {g(x)}}')
SA(53, '2', '②', ending='합은?', new_ending='합을 구하시오.', sol_old='답 ②')
# 55
E(55, 'sol', '(x  ^{2} -8a+a)', sub='(a  ^{2} -8a+a)')
# 56
for a in ('[해설]', '[풀이전략]', '[문제풀이]'):
    op({'op': 'del_para', 'n': 56, 'part': 'sol', 'anchor': a, 'exact': True})
for a in ('^이차부등식의 해와', '^이용하여 합을', '^[step1]', '^[step2]'):
    op({'op': 'del_para', 'n': 56, 'part': 'sol', 'anchor': a})
T(56, 'sol', '함수 ', '함수 ', optional=True)
E(56, 'sol', 'g(x)`', sub='g(a)`', nth=None) if any('g(x)`' == s.strip() or s.strip() == 'g(x)`' for s in ed.scripts(56, 'sol')) else None
ed.run('u_mM/mM_02_edit.json')
