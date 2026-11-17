# -*- coding: utf-8 -*-
"""대수 C 5단원(삼각함수) 내용 고치기"""
import sys, re
sys.path.insert(0, '.')
from mjedit import Ed
ed = Ed(sys.argv[1] if len(sys.argv) > 1 else 'u_dC/dC_05.hwpx')
E, T, SA, op, SPLIT = ed.E, ed.T, ed.SA, ed.op, ed.SPLIT
def EQ(n, part, old, new, **k):
    d = {'op': 'eq', 'n': n, 'part': part, 'old': old, 'new': new}; d.update(k); op(d)
# 붙여 쓴 명령(360DEGtimesn) 띄우기
for n in (4, 5):
    for s in sorted(set(q for q in ed.scripts(n, 'sol') if 'DEGtimes' in q)):
        EQ(n, 'sol', s, re.sub(r'\s*(\d+)DEG', r' \1 DEG', s).replace('DEGtimesn', 'DEG times n').replace('DEGtimes', 'DEG times').replace('  ', ' '), all=True)
EQ(2, 'sol', '510 Deg-360 Deg  times 1+150 Deg', '510 Deg =360 Deg times 1+150 Deg')
T(3, 'sol', '따라서 각 ', '따라서 각 ', optional=True)
E(3, 'sol', '{theta} over {2} `', new='{theta} over {3} `')
T(6, 'q', '말하시오', '말하시오.', optional=True)
# 8: 정답 ⑷ 부호, 다른 풀이 번호·식
E(8, 'sol', '390 Deg', new='-390 Deg', nth=1)
op({'op': 'del_para', 'n': 8, 'part': 'sol', 'anchor': '-60 Deg times 2'})
op({'op': 'del_para', 'n': 8, 'part': 'sol', 'anchor': '-30 Deg times 13'})
op({'op': 'add_para', 'n': 8, 'part': 'sol', 'after': '[다른 풀이]', 'text': '⑷ ⟦- {13} over {6} pi⟧는 ⟦- {pi} over {6} times 13⟧이므로 ⟦-30 Deg times 13= it-390 Deg⟧'})
op({'op': 'add_para', 'n': 8, 'part': 'sol', 'after': '[다른 풀이]', 'text': '⑵ ⟦-120 Deg⟧는 ⟦-60 Deg times 2⟧이므로 ⟦- {pi} over {3} times 2= it- {2} over {3} pi⟧'})
# 9, 10, 14: 정답 줄 낱말
T(9, 'sol', ', 호의 길이 ', ', 넓이 ', exact=True)
T(10, 'sol', ' 넓이 ', ' 호의 길이 ', exact=True)
T(14, 'sol', ',  ', ', 넓이 ', exact=True)
T(9, 'sol', '[정답] 반지름의 길이 ', '[정답] 반지름의 길이 ', optional=True)
EQ(12, 'sol', '60 Deg=8=480 Deg', '60 Deg times 8=480 Deg')
EQ(24, 'sol', 'sin`theta<0,~tantheta>0', 'sin`theta<0,~tan`theta>0')
EQ(38, 'sol', 'tan(360°+128°)', 'tan(360°+120°)')
EQ(39, 'sol', '= {1 over {2}}', '= {1} over {2}')
EQ(40, 'sol', '=tan`(360 ° + 340 °)', '=tan`(360 ° + 330 °)')
EQ(40, 'sol', '=tan`  340 ° ', '=tan`330 °')
# 44: 없는 ㉠
T(44, 'sol', '를 ㉠에 대입하면 ', '이므로 ', optional=True)
# 45: 객관식 정답 줄은 번호로
op({'op': 'del_eq', 'n': 45, 'part': 'sol', 'old': '{pi} over {2}'})
T(45, 'sol', ' [정답] ', ' [정답] ④', exact=True)
EQ(47, 'sol', 'ROOT7 OVER4', '{sqrt {7}} over {4}')
T(52, 'q', '간단히 하여라.', '간단히 하시오.')
E(52, 'sol', 'LEFT ( 1 + sin` theta }  RIGHT )', sub='LEFT ( 1 + sin` theta RIGHT ) }')
E(52, 'sol', '} over { LEFT ( 1-sin` theta RIGHT ) LEFT ( 1 + sin` theta RIGHT ) }', sub='} over { LEFT ( 1-sin` theta RIGHT ) LEFT ( 1 + sin` theta RIGHT )}') if False else None
EQ(55, 'sol', 'theta = piover 6 ,~ {5} over {6} pi', 'theta = {pi} over {6} ,~ {5} over {6} pi')
EQ(57, 'sol', ' sqrt3 - {3} over {6}', '{sqrt3 -3} over {6}')
EQ(57, 'sol', ' bar\\OP =  sqrt {(-1)^2 + (sqrt3 )^2} =2`', 'bar{rm OP} = sqrt {(-1)^2 + (sqrt3 )^2} =2')
# 59: 식 모양(해설 계산 sinθ/tanθ + cosθ·tanθ에 맞춤)
EQ(59, 'q', '{sin`theta} over {{tan`theta}+cos} `theta`tan`theta= IT- {1} over {5} ', '{sin`theta} over {tan`theta} +cos`theta`tan`theta= it- {1} over {5}')
EQ(59, 'sol', '{sin`theta} over {{tan`theta}+cos} `theta`tan`theta= it- {1} over {5} `', '{sin`theta} over {tan`theta} +cos`theta`tan`theta= it- {1} over {5}')
EQ(59, 'sol', '{sin`theta} over {{{sin`theta} over {cos`theta}}+cos} `theta times {sin`theta} over {cos`theta} = it- {1} over {5}', '{sin`theta} over {{sin`theta} over {cos`theta}} +cos`theta times {sin`theta} over {cos`theta} = it- {1} over {5}')
EQ(60, 'sol', '+root{sin^2`theta + 2`sin`theta`cos`theta +cos^2`theta} ', '-root{sin^2`theta + 2`sin`theta`cos`theta +cos^2`theta}')
SA(60, '-2`cos``theta', '②', ending='간단히 하면?', new_ending='간단히 하시오.')
ed.run('u_dC/dC_05_edit.json')
print('miss', ed.miss)
