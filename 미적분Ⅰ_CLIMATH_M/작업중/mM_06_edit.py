# -*- coding: utf-8 -*-
"""미적분Ⅰ M 6단원(도함수의 활용(3)) — C에서 옮기지 못한 문항 고치기"""
import sys, html
sys.path.insert(0, '.')
import hwpxedit as H
from mjedit import Ed
P = sys.argv[1] if len(sys.argv) > 1 else 'u_mM/mM_06.hwpx'
# 12: 같은 구간식 수식이 한 문단에 두 번 → 두 번째 지움
x = H.load(P)
dup = 'g(x)= cases{     -7 x &&&(f(x) < it -x) #     2 f(x) - 5x &&&(f(x) ge it -x) }'
ms = [m for a, b in H.region(x, 12, 'sol') for m in H.EQ.finditer(x, a, b) if html.unescape(H.SC.search(m.group(0)).group(2)) == dup]
assert len(ms) == 2
x = x[:ms[1].start()] + x[ms[1].end():]
H.save(P, x)
ed = Ed(P)
E, T, SA, op = ed.E, ed.T, ed.SA, ed.op
E(8, 'sol', 'f LEFT =( x RIGHT ) x  ^{3} +2ax-2`', 'f LEFT ( x RIGHT ) =x  ^{3} +2ax-2`')
E(12, 'q', '{from^2021^09^평가원^중}', 'f(x)= {1} over {2} x^3 - {9} over {2} x^2 + 10x')
E(12, 'sol', '(0 ,````', '(0,~0)')
op({'op': 'eq', 'n': 13, 'part': 'q', 'old': "f`' LEFT ( x RIGHT ) ＜0", 'new': "f`' LEFT ( x RIGHT ) <0"})
op({'op': 'eq', 'n': 13, 'part': 'sol', 'old': "f`' LEFT ( x RIGHT ) ＜0", 'new': "f`' LEFT ( x RIGHT ) <0"})
E(13, 'sol', 'THEREFORE ~k＞0', sub='because ~k>0')
SA(13, '{2} over {3}', '⑤')
E(20, 'sol', 'rmbar AP``:``bar PR = bar AB``:``bar BS', 'bar{rm AP} ``:`` bar{rm PR} = bar{rm AB} ``:`` bar{rm BS}')
E(20, 'sol', 'LEFT ( 12t-t^2 RIGHT )``:``rmbar PR = 36``:``20', 'LEFT ( 12t-t^2 RIGHT ) ``:`` bar{rm PR} =36``:``20')
E(20, 'sol', 'THEREFORE````{rmbar PR}', sub='THEREFORE```` bar{rm PR}')
E(20, 'sol', '=rmbar PQ = bar PR + bar RQ', '= bar{rm PQ} = bar{rm PR} + bar{rm RQ}')
E(21, 'q', 'rmbarAB =barBC =2`cm,~angleB=90°', 'bar{rm AB} = bar{rm BC} =2`rm cm,~ angle rm B=90 DEG')
E(21, 'sol', "S``'(t)=6t+5", "S`'(t)=6t+5")
E(21, 'sol', "S``'(t)=29", "S`'(4)=29")
SA(21, '29', '②', ending='변화율은?', new_ending='변화율을 구하시오.')
E(22, 'sol', 'piover50', sub='{pi} over {50}')
E(25, 'sol', 'f(x)=x^3 +3x^3 -9x+1', 'f(x)=x^3 +3x^2 -9x+1')
SA(25, '0', '②', ending='합은?', new_ending='합을 구하시오.')
SA(26, '10', '④')
T(35, 'q', '양이 방향', '양의 방향')
E(43, 'q', 'x^n+1 -(n+1)x+2 ge k', 'x^{n+1} -(n+1)x+2 ge k')
E(43, 'sol', 'f(x)=x^n+1 -(n+1)x+2', 'f(x)=x^{n+1} -(n+1)x+2')
E(43, 'sol', 'x^n+1 -(n+1)x+2 ge k', 'x^{n+1} -(n+1)x+2 ge k')
SA(43, '12', '④')
ed.ops[-1] = {'op': 'text_eq', 'n': 43, 'part': 'sol', 'old': ' ④', 'pre': ' ', 'eq': '12', 'post': ''}  # 정답 줄 조각이 ' '·'[정답]'·' ④'로 나뉨
E(47, 'sol', "S``'(t)= {27} over {8} t^2", "S`'(t)= {27} over {8} t^2")
E(47, 'sol', "S``' {left({2root3}}", "S`' LEFT ( {2 sqrt {3}} over {9} RIGHT ) = {27} over {8} times LEFT ( {2 sqrt {3}} over {9} RIGHT )^2 = {1} over {2}")
E(50, 'sol', "f`'(x)=4x^2 -12x+8", "f`'(x)=4x^3 -12x+8")
ed.run('u_mM/mM_06_edit.json')
