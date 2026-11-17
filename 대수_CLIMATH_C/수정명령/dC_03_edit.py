# -*- coding: utf-8 -*-
"""대수 C 3단원(지수함수) 내용 고치기"""
import sys
sys.path.insert(0, '.')
from mjedit import Ed
ed = Ed(sys.argv[1] if len(sys.argv) > 1 else 'u_dC/dC_03.hwpx')
E, T, SA, op, SPLIT = ed.E, ed.T, ed.SA, ed.op, ed.SPLIT
# 3: 문장 오류
T(3, 'q', '의 값이 증가할 때, ', '의 값이 증가할 때 ', after_eq='x')
T(3, 'q', '의 값이 증가할 때, 실수 ', '의 값도 증가하도록 하는 실수 ', after_eq='y')
# 4 ⑵: 지수 묶음
E(4, 'sol', '3^{-x}+1 =2^x', sub='3^{-x+1} =2^x')
# 5: 해설에 a 구하는 과정 넣기
op({'op': 'add_para', 'n': 5, 'part': 'sol', 'after': '[정답]', 'text': '⟦f(6)=a^{6} = {1} over {8} =2^{-3}⟧이고 ⟦a>0⟧이므로 ⟦a=2^{- {1} over {2}} = {sqrt {2}} over {2}⟧'})
# 조건제시법 세로줄 left|, 조건 속 한글
for n, part, o in [(10, 'q', 'LEFT { x``|``-3 LEQ x LEQ it-1 RIGHT } `'), (11, 'q', 'LEFT { x``|``-3 LEQ x LEQ 1 RIGHT } `'),
                   (58, 'q', 'LEFT { x``|``x > 1 over 2  RIGHT } `'), (58, 'q', 'LEFT { y``|``y> it-2 RIGHT }`'), (58, 'sol', 'LEFT { y``|``y> it-2 RIGHT }`')]:
    op({'op': 'eq', 'n': n, 'part': part, 'old': o, 'new': o.replace('``|``', ' left| ').rstrip(' `')})
for o in ['LEFT { y LEFT | y>1 RIGHT. RIGHT }', 'LEFT { y LEFT | y> it-1 RIGHT. RIGHT }', 'LEFT { y LEFT | y<2 RIGHT. RIGHT }']:
    op({'op': 'eq', 'n': 12, 'part': 'sol', 'old': o, 'new': o.replace('LEFT |', 'left|').replace(' RIGHT. RIGHT }', ' RIGHT }')})
op({'op': 'eq', 'n': 12, 'part': 'sol', 'old': 'LEFT { y LEFT | y< it-2` RIGHT. RIGHT },', 'new': 'LEFT { y left| y< it-2 RIGHT }'})
T(13, 'sol', 'ㄴ ', 'ㄴ. ', optional=True)
# 15: 치역 집합 표기 + 점근선 방정식 빠짐
for o, r, a in [('left{ y` |`y>1인 `실수right', 'y>1', 'y=1'), ('left{ y` |`y> it-2인 `실수right', 'y> it-2', 'y= it-2'),
                ('left{ y` |`y< it-1인 `실수right', 'y< it-1', 'y= it-1'), ('left{ y` |`y< 2인 `실수right', 'y<2', 'y=2')]:
    SPLIT(15, 'sol', o, ['LEFT { y left| %s RIGHT }' % r, '이고, 점근선의 방정식은 ', a])
E(15, 'sol', '4^{-x}-2 -2', sub='4^{-x-2} -2')
T(16, 'sol', 'ㄱ, ㄹ이다', 'ㄱ, ㄹ이다.', optional=True)
# 18: 지수 묶음
E(18, 'sol', '2^{-1}-m +n=1', new='2^{-1-m} +n=1')
E(18, 'sol', '2^{-m} - 2^{-1}-m =4', new='2^{-m} -2^{-1-m} =4')
T(21, 'sol', '성립한다..', '성립한다.')
# 25 ⑶: (1/2)^2 → (1/2)^0
E(25, 'sol', 'right)^2 = 5^0', sub='right)^0 = 5^0')
E(31, 'sol', '{3} over {2} left( log`2 - log`3 ) x', sub='{3} over {2} (log`2 - log`3 ) x')
# 37: 전각 +
for part in ('q', 'sol'):
    for s in sorted(set(q for q in ed.scripts(37, part) if '＋' in q)):
        op({'op': 'eq', 'n': 37, 'part': part, 'old': s, 'new': s.replace('＋', '+'), 'all': True})
# 40: g(x)
op({'op': 'eq', 'n': 40, 'part': 'q', 'old': 'rmg(itx)=2  ^{f(x)}', 'new': 'g(x)=2  ^{f(x)}'})
op({'op': 'eq', 'n': 40, 'part': 'q', 'old': 'rmg(itx)', 'new': 'g(x)'})
E(42, 'sol', '2root{3^{-x}+y}', sub='2root{3^{-x+y}}')
E(45, 'sol', '{ {-{7} over {2}}}', new='- {7} over {2}')
E(46, 'sol', '- 2^{-x}+2 +2', sub='- 2^{-x+2} +2')
T(46, 'sol', '⑴ ', '', optional=True)
T(52, 'sol', '이차방정식 ㉠이 항상', '이차부등식 ㉠이 항상')
E(55, 'sol', '43 . times times times', sub='43. CDOTS')
T(68, 'q', '의을 구하시오', '의 값을 구하시오')
ed.run('u_dC/dC_03_edit.json')
print('miss', ed.miss)
