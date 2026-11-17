# -*- coding: utf-8 -*-
"""대수 C 2단원(로그) 내용 고치기"""
import sys
sys.path.insert(0, '.')
from mjedit import Ed
ed = Ed(sys.argv[1] if len(sys.argv) > 1 else 'u_dC/dC_02.hwpx')
E, T, SA, op, SPLIT = ed.E, ed.T, ed.SA, ed.op, ed.SPLIT
# 밑이 식인 로그: 아래 첨자 묶기
for part in ('q', 'sol'):
    op({'op': 'eq', 'n': 2, 'part': part, 'old': 'log_ sqrt { 3} `9=4', 'new': 'log _{sqrt {3}} `9=4'})
E(4, 'q', 'log_(x-1)', sub='log _{x-1} ')
E(7, 'q', 'log_8-x ``', sub='log _{8-x} ``')
E(44, 'q', 'log_a-4 (', sub='log _{a-4} (')
# 3: 해설 ⑵ 식 오타 4=32 → 4=2/3
E(3, 'sol', 'log_x `4=32', sub='log_x `4= {2} over {3}')
E(5, 'sol', '{1`}', sub='{1}')
T(11, 'q', '간단히 하여라.', '간단히 하시오.')
E(18, 'sol', '{-1} over {2}', new='- {1} over {2}')
E(20, 'sol', 'cdots CDOTS', sub='times CDOTS times')
op({'op': 'eq', 'n': 27, 'part': 'sol', 'old': '0.9542', 'new': '=0.9542', 'last': True})
# 28, 31: 정답 머리 없음
T(28, 'sol', '⑴ ', '[정답] ⑴ ', before_eq='3.4487')
T(31, 'sol', '⑴ ', '[정답] ⑴ ', before_eq='0.6990')
E(31, 'sol', ' 0. 8266', new='0.8266', nth=1)
E(31, 'sol', '= 0. 8266', new='= 0.8266')
SA(29, '2050.205', '②')
SA(30, '1.2870', '①', ending='값을 구하면?', new_ending='값을 구하시오.')
# 32: 문제의 상용로그 값을 해설(0.7868)에 맞춤
E(32, 'q', '0.7861', sub='0.7868')
# 34: 문제를 해설에 맞춤 (log_3 5 = b)
E(34, 'q', 'log` _{2} `5=b', sub='log` _{3} `5=b')
SA(35, '{1} over {2(1-a)}', '①', ending='나타내면?', new_ending='나타내시오.')
SA(36, '{2a+b} over {3+b}', '⑤', ending='나타내면?', new_ending='나타내시오.')
# 39: 두 근이 허근이면 로그가 정의되지 않음 → 두 양의 실근을 갖는 방정식, 밑 αβ+1 (답 2 유지)
op({'op': 'eq', 'n': 39, 'part': 'q', 'old': 'x^2 -3x +5 =0 ', 'new': 'x^2 -6x +2 =0'})
op({'op': 'eq', 'n': 39, 'part': 'q', 'old': 'log _{alpha+beta} `(alpha +1) + log_{alpha+beta} `(beta +1)', 'new': 'log _{alpha beta +1} `(alpha +1) +log _{alpha beta +1} `(beta +1)'})
op({'op': 'eq', 'n': 39, 'part': 'sol', 'old': 'x^2 -3x +5 =0 ', 'new': 'x^2 -6x +2 =0'})
op({'op': 'eq', 'n': 39, 'part': 'sol', 'old': 'alpha+b = 3,`````alpha beta= 5', 'new': 'alpha + beta =6,~alpha beta =2'})
for o in ['log _{alpha + beta } `( alpha +1)+log _{alpha + beta } `( beta +1)', '=log _{alpha + beta } LEFT { ( alpha +1)( beta +1) RIGHT }', '=log _{alpha + beta } `( alpha  beta + alpha + beta +1)']:
    op({'op': 'eq', 'n': 39, 'part': 'sol', 'old': o, 'new': o.replace('alpha + beta } ', 'alpha beta +1} ')})
op({'op': 'eq', 'n': 39, 'part': 'sol', 'old': '=log _{3} `(5+3+1)', 'new': '=log _{3} `(2+6+1)'})
op({'op': 'add_para', 'n': 39, 'part': 'sol', 'after': '근과 계수의 관계에 의하여', 'text': '이때 판별식 ⟦D over 4 =9-2>0⟧이고 ⟦alpha + beta >0⟧, ⟦alpha beta >0⟧이므로 ⟦alpha⟧, ⟦beta⟧는 서로 다른 두 양의 실근이다.'})
SA(43, '2x-3', '③', ending='간단히 하면?', new_ending='간단히 하시오.')
# 47: 해설 넷째 줄 2log_18 3
E(47, 'sol', '=(log _{18} `2+log _{18} `3) ^{2}', sub='=(log _{18} `2+2log _{18} `3) ^{2}')
E(47, 'sol', '(2log _{18`} `3)', sub='(2log _{18} `3)')
SA(50, '0', '③')
SA(51, '3a-b', '③', ending='나타내면?', new_ending='나타내시오.')
SA(52, '{3+ab} over {1+a+ab}', '④', ending='나타내면?', new_ending='나타내시오.')
E(53, 'sol', '=3. TIMES  TIMES  TIMES ', sub='=3. CDOTS ')
# 55: 단위 m, 지수 깨짐
E(55, 'q', 'd``rmm', new='d``rm m')
T(55, 'q', '인 곳의    수심을', '인 곳의 수심을', optional=True)
E(55, 'sol', '{8 rm``(m)}', new='8``rm m')
E(55, 'sol', 'I_0 ``2^{-0}.25d', sub='I_0 ``2^{-0.25d}')
E(55, 'sol', 'therefore``2^{-0}.25d', sub='therefore``2^{-0.25d}')
E(55, 'sol', '8``rm(m)', sub='8``rm m', nth=2) if False else E(55, 'sol', 'therefore``d = 8``rm(m)', new='therefore``d=8``rm m')
ed.run('u_dC/dC_02_edit.json')
print('miss', ed.miss)
