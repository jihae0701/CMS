# -*- coding: utf-8 -*-
"""대수 C 6단원(삼각함수의 그래프) 내용 고치기"""
import sys
sys.path.insert(0, '.')
from mjedit import Ed
ed = Ed(sys.argv[1] if len(sys.argv) > 1 else 'u_dC/dC_06.hwpx')
E, T, SA, op, SPLIT = ed.E, ed.T, ed.SA, ed.op, ed.SPLIT
def EQ(n, part, old, new, **k):
    d = {'op': 'eq', 'n': n, 'part': part, 'old': old, 'new': new}; d.update(k); op(d)
T(1, 'sol', '방향으로 ', '방향으로 ', optional=True)
T(5, 'q', '의 합 ', '의 곱 ')
# 7, 13: 해설 속 ← 기호 → 문장으로
for n in (7, 13):
    T(n, 'sol', '이므로 ', '이다. ', after_eq='pi')
    op({'op': 'del_eq', 'n': n, 'part': 'sol', 'old': 'larrow'})
T(9, 'sol', '㉠, ㉡을 연립하여', '두 식을 연립하여')
# 10: 정답 줄 번호 ⑷, 집합 표기
T(10, 'sol', '⑶ 최댓값 ', '⑷ 최댓값 ', after_eq=' 2 pi  ')
EQ(10, 'sol', 'LEFT { y LEFT ∣ - {1} over {2}  LEQ y LEQ  {1} over {2} RIGHT } RIGHT .`', 'LEFT { y left| - {1} over {2} LEQ y LEQ {1} over {2} RIGHT }')
EQ(10, 'sol', 'y = c os `x `', 'y = cos `x `')
# 12: 조건 a>0, b>0 빠짐(해설이 a>0을 씀)
op({'op': 'text_eq', 'n': 12, 'part': 'q', 'old': '구하시오.', 'pre': '구하시오. (단, ', 'eq': 'a>0,~b>0', 'post': ')', 'sub': True})
T(16, 'sol', '그래프에서함수', '그래프에서 함수')
# 17 ⑵: 점근선 x=2nπ+π → x=2nπ, 해설에 점근선 보충
EQ(17, 'sol', 'x=2n pi +    pi', 'x=2n pi')
SPLIT(17, 'sol', '{pi} over { {1} over {3} } = 3 pi', ['{pi} over { {1} over {3} } = 3 pi', ', 점근선의 방정식 : ', 'x=3n pi + {3} over {2} pi', ' (', 'n', '은 정수)'])
SPLIT(17, 'sol', '{pi} over { {1} over {2} } = 2 pi', ['{pi} over { {1} over {2} } = 2 pi', ', 점근선의 방정식 : ', 'x=2n pi', ' (', 'n', '은 정수)'])
# 21 ⑵: cos x = 1/2 → −1/2
EQ(21, 'sol', 'THEREFORE ````cos`x= {1} over {2}', 'THEREFORE ````cos`x= it- {1} over {2}')
EQ(24, 'sol', 'THEREFORE~ sin`x=1 (-1 le sin x le 1)', 'THEREFORE~ sin`x=1~( because ~-1 le sin`x le 1)')
# 25: ⑴ 해설 x 자리, ⑵ 정답 0≤x (x=0도 해)
EQ(25, 'sol', '{pi} over {6}<pi< { 5} over { 6}pi', '{pi} over {6}<x< { 5} over { 6}pi')
EQ(25, 'sol', ' 0<x< {pi } over {3} `', '0 le x< {pi } over {3}')
# 26: 정답 오류(⑴ x≤2π, ⑵ 3π/2<x<7π/4)
EQ(26, 'sol', ' {  {7} over {4}  pi   le x < 2 pi}', '{7} over {4} pi le x le 2 pi')
EQ(26, 'sol', ' {2} over {3}  pi <x< {7} over {4}  pi ', '{3} over {2} pi <x< {7} over {4} pi')
EQ(27, 'q', '-2\t`cos^2 `x+ LEFT ( 4- sqrt { 3} RIGHT )sin`x-2 sqrt { 3}+2 ge 0`', '-2`cos^2 `x+ LEFT ( 4- sqrt { 3} RIGHT )sin`x-2 sqrt { 3}+2 ge 0')
# 30: 해설 식 오류(+1 없음), 정답 줄 ';'
EQ(30, 'sol', 'y= it-t  ^{2} +2t+1', 'y= it-t  ^{2} +2t')
T(30, 'sol', ' [정답] 최댓값 ; ', ' [정답] 최댓값 : ', exact=True); T(30, 'sol', ', 최솟값 ; ', ', 최솟값 : ', exact=True)
op({'op': 'text_eq', 'n': 39, 'part': 'sol', 'old': ' [정답] ①', 'pre': ' [정답] ', 'eq': '-3', 'post': ''})
EQ(41, 'sol', '0 LEQ t<1', '0 LEQ t LEQ 1')
EQ(45, 'sol', '= it-sin  ^{2} `x-sin`x-1', '= it-sin  ^{2} `x-sin`x+1')
ed.run('u_dC/dC_06_edit.json')
print('miss', ed.miss)
