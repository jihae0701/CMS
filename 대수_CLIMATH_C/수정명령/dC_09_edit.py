# -*- coding: utf-8 -*-
"""대수 C 9단원(수열의 합) 내용 고치기"""
import sys, re
sys.path.insert(0, '.')
from mjedit import Ed
ed = Ed(sys.argv[1] if len(sys.argv) > 1 else 'u_dC/dC_09.hwpx')
E, T, SA, op, SPLIT = ed.E, ed.T, ed.SA, ed.op, ed.SPLIT
def EQ(n, part, old, new, **k):
    d = {'op': 'eq', 'n': n, 'part': part, 'old': old, 'new': new}; d.update(k); op(d)
# 2 ⑴: 정답 6 → −6 (해설 계산)
EQ(2, 'sol', ' 6', '-6')
EQ(7, 'sol', '={ 2(2^5 -1) } over 2-1 +{ 3(3^5 -1) } over 3-1', '= { 2(2^5 -1) } over {2-1} + { 3(3^5 -1) } over {3-1}')
# 9: ⑵ 정답이 10번 ⑵의 것 → 330, ⑴ 해설 중괄호
EQ(9, 'sol', '  n(2n+1) (7n+1)', '330')
EQ(9, 'sol', '= 4 times {left( 6 times 7  over 2 right) ^2 - 6 times 7 over 2}', '=4 times left( {6 times 7} over {2} right) ^2 - {6 times 7} over {2}')
# 10 ⑴: 정답·해설 오류 n(n+1)(n+2)/3 → n(n+1)(2n+7)/6
EQ(10, 'sol', '{n(n+1)(n+2)} over {3}', '{n(n+1)(2n+7)} over {6}')
EQ(10, 'sol', '=sum _{ k=1} ^{n } {i^2 } + 2 sum _{ k=1} ^{n } {i }  ', '=sum _{ i=1} ^{n } {i^2 } + 2 sum _{ i=1} ^{n } {i }')
EQ(10, 'sol', '= {n (n+1)} over {6}  left{(2n+1)+ 3 right', '= {n (n+1)} over {6} LEFT { (2n+1)+6 RIGHT }')
EQ(10, 'sol', '= {n(n+1)(n+2)} over {3}', '= {n(n+1)(2n+7)} over {6}')
EQ(11, 'sol', '= 2 sum _{ k=1} ^{10 }{k^2 } - 2 sum _{ k=1} ^{10 }{{k} + sum _{ k=1} ^{10 }{3}}', '= 2 sum _{ k=1} ^{10 }{k^2 } - 2 sum _{ k=1} ^{10 } k + sum _{ k=1} ^{10 } 3')
EQ(14, 'sol', '= sum _{k=1} ^{10} {(k  -1} ) -(1-1)', '= sum _{k=1} ^{10} (k-1) -(1-1)')
T(15, 'q', ' 값을 구하시오', '의 값을 구하시오', optional=True)
# 24: 빠진 수식 S_n
op({'op': 'text_eq', 'n': 24, 'part': 'q', 'old': '합을 이라 할 때', 'pre': '합을 ', 'eq': 'S_n', 'post': '이라 할 때', 'sub': True})
EQ(25, 'sol', '= {1} over {3} left{(10 +10^2 +10^3 + itcdots it +10^n ) - 1 times n  right', '= {1} over {3} LEFT { (10 +10^2 +10^3 + it cdots it +10^n ) - 1 times n RIGHT }')
# 26 ⑵: 정답 175/132 → 175/264 (해설 마지막 줄 ½ 빠짐)
EQ(26, 'sol', ' {175} over {132}', '{175} over {264}')
EQ(26, 'sol', '= {{175} over {132}}', '= {1} over {2} times {175} over {132} = {175} over {264}')
# 27 ⑴: 정답·해설 오류(1/2 → 1/1) → n/(2(3n+2))
EQ(27, 'sol', '{3n+1} over {3(3n+2)}', '{n} over {2(3n+2)}')
EQ(27, 'sol', '= {1} over {3} LEFT ( {1} over {1} - {1} over {3n+2} RIGHT )', '= {1} over {3} LEFT ( {1} over {2} - {1} over {3n+2} RIGHT )')
EQ(27, 'sol', '= {3n+1} over {3(3n+2)}', '= {n} over {2(3n+2)}')
# 27 ⑵: 문제 수열 1/(2²−1), 1/(3²−1), …과 해설 1/((2n)²−1)이 다름 → 문제를 해설·정답에 맞춤
EQ(27, 'q', '{1} over {3^2 -1}', '{1} over {4^2 -1}', first=True) if False else None
for o, nw in [('{1} over {5 ^{2} -1}', '{1} over {8^2 -1}'), ('{1} over {4^2 -1}', '{1} over {6^2 -1}'), ('{1} over {3^2 -1}', '{1} over {4^2 -1}')]:
    EQ(27, 'q', o, nw)
# 27 ⑶: 해설 ½ → 2
EQ(27, 'sol', 'sum_{k=1}^n {1} over {2} left( {1} over {k} - {1} over {k+1} right) ', 'sum_{k=1}^n 2 left( {1} over {k} - {1} over {k+1} right)')
EQ(27, 'sol', '= {1} over {2} left{ left( 1 - {1} over {2} right) +  left( 1 over {2}  - {1} over {3} right)+ it cdots it +  left( 1 over {n} - {1} over {n+1} right) right', '=2 LEFT { left( 1 - {1} over {2} right) + left( {1} over {2} - {1} over {3} right) + it cdots it + left( {1} over {n} - {1} over {n+1} right) RIGHT }')
EQ(27, 'sol', '= {1} over {2}  left(1- {1} over {n+1} right)', '=2 left(1- {1} over {n+1} right)')
EQ(27, 'sol', '= 2n over n+1', '= {2n} over {n+1}')
EQ(29, 'sol', 'S`=1`cdot 2+2`cdot 4+`cdot 8+4`cdot 16+cdots+10`cdot 2`  ^{10} `', 'S`=1`cdot 2+2`cdot 4+3`cdot 8+4`cdot 16+cdots+10`cdot 2`  ^{10}')
E(30, 'sol', '6` CDOT  LEFT ( {1} over {3} RIGHT )  ^{2}', sub='6` CDOT  LEFT ( {1} over {3} RIGHT )  ^{3}')
EQ(31, 'sol', '=2n ^{2} -n+1- LEFT { 2(n-1) ^{2} RIGHT . -(n-1) +1 right', '=2n ^{2} -n+1- LEFT { 2(n-1) ^{2} -(n-1) +1 RIGHT }')
T(34, 'q', '다음을 계산하여라.', '다음 값을 구하시오.')
# 35, 49: root 뒤 식 묶기
def rt(s):
    s = re.sub(r'root\s*([a-z0-9]+)\s*\+\s*1', r'sqrt {\1+1}', s)
    return re.sub(r'root\s*([a-z0-9]+)', r'sqrt {\1}', s)
for n, part in [(35, 'sol'), (49, 'q'), (49, 'sol')]:
    for s in sorted(set(q for q in ed.scripts(n, part) if 'root' in q)):
        EQ(n, part, s, rt(s), all=True)
# 37, 38: 로그 분수 모양(log(k+1)/k가 아니라 log((k+1)/k))
EQ(37, 'sol', '=sum _{ k=1} ^{99 } {log{k+1}} over {k} =log{{2} over {1}}+log{{3} over {2}}+log{{4} over {3}}+cdots+log{{100} over {99}}``', '=sum _{k=1} ^{99} log {k+1} over {k} =log {2} over {1} +log {3} over {2} +log {4} over {3} + cdots +log {100} over {99}')
EQ(38, 'sol', '=sum _{ k=2} ^{100 } {log{k^2 -1}} over {k^2} ``', '=sum _{k=2} ^{100} log {k^2 -1} over {k^2}')
EQ(38, 'sol', '=sum _{ k=2} ^{100 } {log{(k-1)(k+1)}} over {k^2} ``', '=sum _{k=2} ^{100} log {(k-1)(k+1)} over {k^2}')
EQ(38, 'sol', '= {log{1 cdot 3}} over {2^2} {+log{2 cdot 4}} over {3^2} {+log{3 cdot 5}} over {4^2} +``cdots`` {+log{99 cdot 101}} over {100^2} ``', '=log {1 cdot 3} over {2^2} +log {2 cdot 4} over {3^2} +log {3 cdot 5} over {4^2} + cdots +log {99 cdot 101} over {100^2}')
EQ(38, 'sol', '=log LEFT ( {1 cdot 3} over {2^2} {times{2 cdot 4}} over {3^2} {times{3 cdot 5}} over {4^2} times``cdots`` {times{99 cdot 101}} over {100^2} RIGHT )``', '=log LEFT ( {1 cdot 3} over {2^2} times {2 cdot 4} over {3^2} times {3 cdot 5} over {4^2} times cdots times {99 cdot 101} over {100^2} RIGHT )')
EQ(38, 'sol', '= {log{1 cdot 101}} over {2 cdot 100} =log101-log2 -2``', '=log {1 cdot 101} over {2 cdot 100} =log`101-log`2-2')
EQ(38, 'sol', 'log101-log2-2``', 'log`101-log`2-2')
T(44, 'q', '첫재항', '첫째항')
EQ(46, 'sol', '40 OVER21', '{40} over {21}')
ed.run('u_dC/dC_09_edit.json')
print('miss', ed.miss)
