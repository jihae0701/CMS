# -*- coding: utf-8 -*-
"""대수 C 8단원(등차수열과 등비수열) 내용 고치기"""
import sys
sys.path.insert(0, '.')
from mjedit import Ed
ed = Ed(sys.argv[1] if len(sys.argv) > 1 else 'u_dC/dC_08.hwpx')
E, T, SA, op, SPLIT = ed.E, ed.T, ed.SA, ed.op, ed.SPLIT
def EQ(n, part, old, new, **k):
    d = {'op': 'eq', 'n': n, 'part': part, 'old': old, 'new': new}; d.update(k); op(d)
EQ(5, 'q', 'log  _{`} 4,', 'log`4,'); EQ(5, 'q', 'log  _{`} 16', 'log`16')
# 6: k의 값을 묻는데 정답이 '제100항'
T(6, 'sol', ' [정답] 제', ' [정답] ', exact=True); T(6, 'sol', '항', '', exact=True)
# 22 ⑵: 문제 수열(√2−1, 1, √2+1, 3−2√2는 등비수열이 아님) → 해설·정답에 맞춰 √2+1, 1, √2−1, 3−2√2
EQ(22, 'q', 'sqrt {2} -1,~1,~ sqrt {2} +1,~3-2 sqrt {2} ,~ CDOTS ', 'sqrt {2} +1,~1,~ sqrt {2} -1,~3-2 sqrt {2} ,~ CDOTS')
T(23, 'sol', '공차를 ', '공비를 ')
# 27 ⑴: 문제를 해설(log10²+log10⁴+…, 10개 항, 2046)에 맞춤
EQ(27, 'q', 'log`10+log`10  ^{3} +log`10  ^{9} + it CDOTS it +log`10  ^{3  ^{n}}', 'log`10  ^{2} +log`10  ^{4} +log`10  ^{8} + it CDOTS it +log`10  ^{2  ^{10}}')
# 48: 묻는 말 꼴, 단위 띄어쓰기
T(48, 'q', '원리합계는?', '원리합계를 구하시오.')
for n in (48, 49):
    op({'op': 'text', 'n': n, 'part': 'sol', 'old': '만원', 'new': '만 원', 'all': True})
EQ(50, 'q', 'left{a  _{n} right', 'LEFT { a  _{n} RIGHT }'); EQ(51, 'q', 'left{a  _{n} right', 'LEFT { a  _{n} RIGHT }')
T(50, 'q', '제몇 항', '제 몇 항')
EQ(53, 'q', '(a_1 +a_2 + it CDOTS it +a_10 )+(b_1 +b_2 +  itCDOTS it +b_10 )', '(a_1 +a_2 + it CDOTS it +a_10 )+(b_1 +b_2 + it CDOTS it +b_10 )')
EQ(55, 'sol', '"{"a_n"}",~"{"b_n"}"', 'LEFT { a_n RIGHT } ,~ LEFT { b_n RIGHT }')
T(55, 'sol', '이룹니다.', '이룬다.')
ed.run('u_dC/dC_08_edit.json')
print('miss', ed.miss)
