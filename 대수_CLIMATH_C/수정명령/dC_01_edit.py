# -*- coding: utf-8 -*-
"""대수 C 1단원(지수) 내용 고치기"""
import sys
sys.path.insert(0, '.')
from mjedit import Ed
ed = Ed(sys.argv[1] if len(sys.argv) > 1 else 'u_dC/dC_01.hwpx')
E, T, SA, op, SPLIT = ed.E, ed.T, ed.SA, ed.op, ed.SPLIT
# 1: 정답 줄 ⑵ 세 값을 쉼표로
op({'op': 'eq', 'n': 1, 'part': 'sol', 'old': 'x= {-3+-3sqrt3 i} over {2}', 'new': '3,~ {-3 +- 3 sqrt {3} i} over {2}', 'first': True})
op({'op': 'del_eq', 'n': 1, 'part': 'sol', 'old': '3'})
op({'op': 'text', 'n': 1, 'part': 'sol', 'old': ' 또는 ', 'new': '', 'before_eq': '3,~ {-3 +- 3 sqrt {3} i} over {2}'})
# 2: 깨진 거듭제곱근, ± 글자
E(2, 'sol', ' sqrt{3}of2', new='root {3} of {2}')
E(2, 'sol', ' -sqrt{4}of2 ,~sqrt{4}of2', new='-root {4} of {2} ,~root {4} of {2}')
E(2, 'sol', '±root {4} of {2}', sub='+- root {4} of {2}')
# 4: 수식 속 ∴
E(4, 'sol', '∴   f(-2', sub='THEREFORE ~f(-2')
# 5: ② 해설 '의 세제곱근을' → '에서'
T(5, 'sol', '의 세제곱근을 ', '에서 ', after_eq='x ^{3} = it-27')
# 7: 보기 ㄱ 띄어쓰기, 해설 ㄴ·ㄹ 오타
T(7, 'q', '개 이다.', '개이다.', optional=True)
T(7, 'sol', '일 짝수일 때', '이 짝수일 때')
E(7, 'sol', '-4,', new='-4')
# 8: 조건제시법(조건 속 한글 분리), 집합 기호 소문자
E(8, 'q', 'S= LEFT {', new='S= LEFT { (a,~b) left| root {a} of {b}')
E(8, 'q', 'LEFT. a IN A', new='a in A,~b in B RIGHT }')
# 11: 근호 안 음수·곱 묶기
E(11, 'q', 'root{5}of-32', new='root{5}of{-32} +root{4}of81 -root{3}of{-64}')
E(11, 'sol', 'root{5}of-32', new='root{5}of{-32} +root{4}of81 -root{3}of{-64}')
E(11, 'sol', 'root{5}of(-2)^5', new='=root{5}of{(-2)^5} +root{4}of{3^4} -root{3}of{(-4)^3}')
E(11, 'sol', 'div2-2', sub='div 2-2')
E(11, 'sol', '=root{3}of2 times 4 -root{3}of2 times 6', new='=root{3}of{2 times 4} -root{3}of{2 times 6} +root{3}of{2 times 9} +root{3}of{3 times 4} -root{3}of{3 times 6} +root{3}of{3 times 9}')
# 12: 근호 안 묶기
E(12, 'q', 'root{4}of4ab^2', sub='root{4}of{4ab^2}')
E(12, 'sol', 'root{4}of4ab^2', sub='root{4}of{4ab^2}', nth=1)
# 13: 해설 둘째 줄 곱셈 기호 자리
E(13, 'sol', 'over {root{6}of{root{4}ofx}times} {root{4}', sub='over {root{6}of{root{4}ofx}} times {root{4}')
# 14: '하여라' → '하시오', 깨진 근호, 지수 자리 eqalign/pile → 수
T(14, 'q', '간단히 하여라.', '간단히 하시오.')
E(14, 'q', 'OF27^4', new='root {3} of {27 ^{4}}')
E(14, 'q', '{root 5} over {sqrt {3}of{5}}', sub='{sqrt {5}} over {root {3} of {5}}')
# 15: 근호 안 묶기, 오타
E(15, 'q', 'root{3} of8b^2', sub='root{3} of{8b^2}')
E(15, 'sol', 'root{3} of8b^2', sub='root{3} of{8b^2}')
E(15, 'sol', 'root{6} of64b^4', sub='root{6} of{64b^4}')
T(15, 'sol', '근호 앞의 수 ', '근호의 지수 ')
T(15, 'sol', '통일한 다.', '통일한다.')
# 16: ÷ → div
for part in ('q', 'sol'):
    E(16, part, '÷', sub=' div ', nth=1)
# 17: 선지 ⑤ 2 → 단답형
SA(15, 'a^{2}', '③', ending='간단히 하면?', new_ending='간단히 하시오.')
SA(17, '2', '⑤', ending='간단히 하면?', new_ending='간단히 하시오.')
# 20: DIVIDEa 띄어 쓰기, 단답형
E(20, 'sol', 'b DIVIDEa', sub='b DIVIDE a')
SA(20, 'a ^{{7} over {12}} b ^{{1} over {6}}', '②', ending='간단히 하면 (단, ', new_ending='간단히 하시오. (단, ')
# 21: 수식 속 한글, 단답형
SPLIT(21, 'sol', 'a= sqrt {3} 에서``a  ^{2} =3', ['a= sqrt {3}', '에서 ', 'a  ^{2} =3'])
SA(21, '3 TIMES 5  ^{{1} over {3}}', '②')
# 22: ÷ → div
E(22, 'q', '÷27', sub=' div 27')
E(22, 'sol', '÷27  ^{{8} over {9}} =3', sub=' div 27  ^{{8} over {9}} =3')
# 24: 문제를 해설에 맞춤(∛ 안에 a√a), 물음표 오타
E(24, 'q', 'root{4} of{a root{3} ofa roota}', sub='root {4} of {a root {3} of {a sqrt {a}}}')
T(24, 'q', '구하시오.? ', '구하시오. ', optional=True)
T(24, 'q', '구하시오.?', '구하시오.', optional=True)
SA(25, 'a^{ 1 over 3} b^{ 1 over 2 }', '①', ending='나타내면?', new_ending='나타내시오.')
SA(27, 'a- {1} over {b}', '④', ending='간단히 하면?', new_ending='간단히 하시오.')
SA(29, 'x ^{{1} over {3}} +x ^{- {1} over {3}}', '①', ending='간단히 하면?', new_ending='간단히 하시오.')
# 30: 문제 오타 x^{1/4}x^{1/4} → x^{1/4}y^{1/4}
E(30, 'q', '+x ^{{1} over {4}} x ^{{1} over {4}}', sub='+x ^{{1} over {4}} y ^{{1} over {4}}')
# 34
E(34, 'sol', 'DIVIDE3', sub='DIVIDE 3')
# 37: 떠도는 ⑴
T(37, 'sol', '⑴ ', '', optional=True)
# 39: 조건제시법 다시 쓰기
E(39, 'q', 'A= left{ x left|', new='A= LEFT { x left| x= LEFT ( {1} over {81} RIGHT ) ^{{1} over {n}}')
op({'op': 'del_eq', 'n': 39, 'part': 'q', 'old': [s for s in ed.scripts(39, 'q') if s.lstrip(' `').startswith('x= LEFT')][0].strip()})
E(39, 'q', 'pile{ `#` } right}', new='pile{it#it} RIGHT }')
# 40: 쉼표 오타
T(40, 'q', '. ', ', ', after_eq='a')
SA(44, '5+2 sqrt {6}', '①')
SA(49, '2^{ {5} over {4} }', '③')
ed.run('u_dC/dC_01_edit.json')
print('miss', ed.miss)
