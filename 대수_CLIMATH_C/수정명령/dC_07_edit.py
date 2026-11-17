# -*- coding: utf-8 -*-
"""대수 C 7단원(삼각함수의 활용) 내용 고치기"""
import sys, re
sys.path.insert(0, '.')
from mjedit import Ed
ed = Ed(sys.argv[1] if len(sys.argv) > 1 else 'u_dC/dC_07.hwpx')
E, T, SA, op, SPLIT = ed.E, ed.T, ed.SA, ed.op, ed.SPLIT
def EQ(n, part, old, new, **k):
    d = {'op': 'eq', 'n': n, 'part': part, 'old': old, 'new': new}; d.update(k); op(d)
EQ(2, 'sol', 'sin45°=2R=4', '{c} over {sin45°} =2R=4')
EQ(11, 'sol', '6rm`m', '6')
EQ(15, 'sol', '=3 ^{2} + sqrt {2 ^{2}} -2 TIMES 3 TIMES sqrt {2} TIMES cos`45°', '=3 ^{2} +( sqrt {2} ) ^{2} -2 TIMES 3 TIMES sqrt {2} TIMES cos`45°')
EQ(15, 'sol', '= 9 + 2 - 6SQRT2 TIMES SQRT2 OVER2', '=9+2-6 sqrt {2} TIMES {sqrt {2}} over {2}')
EQ(17, 'sol', '=  { a^2 + b^2 - c^2 } over 2ab', '= { a^2 + b^2 - c^2 } over {2ab}')
E(19, 'sol', '2 TIMES 8k times 2k', sub='2 TIMES 8k times 7k')
T(20, 'q', '크기의 구하시오', '크기를 구하시오')
EQ(21, 'sol', '6ROOT6', '6 sqrt {6}')
EQ(25, 'sol', 'S= sqrt {10 LEFT ( 10-7)(10-8 RIGHT ) (10-5)} =10 sqrt {3}', 'S= sqrt {10(10-7)(10-8)(10-5)} =10 sqrt {3}')
# 26: 반지름 4인 원에 외접하는 삼각형의 넓이는 48√3보다 작을 수 없음 → 반지름 1(넓이 12 그대로), 답 24
EQ(26, 'q', '4', '1')
EQ(26, 'sol', '4', '1')
EQ(26, 'sol', '12= {a+b+c} over {2} cdot 4', '12= {a+b+c} over {2} cdot 1')
EQ(26, 'sol', 'a+b+c=6', 'a+b+c=24')
EQ(26, 'sol', '6', '24', all=True)
EQ(28, 'sol', 'sin``theta+6`sin``theta=7`sin``theta', '=sin``theta+6`sin``theta=7`sin``theta')
EQ(38, 'sol', '{rm bar{AD}}  ^{2} =3  ^{2} -2  ^{2} -2 cdot 3 cdot 2 cdot {11} over {14}', '{rm bar{AD}}  ^{2} =3  ^{2} +2  ^{2} -2 cdot 3 cdot 2 cdot {11} over {14}')
EQ(39, 'sol', "ARCH{rm A'A'}=2 pi{cdot}1=2 pi", "ARCH{rm AA'}=2 pi{cdot}1=2 pi")
T(41, 'sol', '정삼각형의 전개도', '정삼각뿔의 전개도')
EQ(44, 'q', 'bar{rm AD it} \\ \U000f005a bar{rm BC it}', 'bar{rm AD} `//` bar{rm BC}')
T(44, 'sol', '선번', '선분')
for s in sorted(set(q for q in ed.scripts(46, 'sol') if re.search(r'angleit|itangle|angle[xyz]', q))):
    EQ(46, 'sol', s, re.sub(r'(it)?angle(it)?([xyz])', r'angle \3', s), all=True)
ed.run('u_dC/dC_07_edit.json')
print('miss', ed.miss)
