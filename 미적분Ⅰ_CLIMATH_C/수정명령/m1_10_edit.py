# -*- coding: utf-8 -*-
"""미적분Ⅰ 10단원(정적분의 활용) 내용 고치기"""
import sys, re
sys.path.insert(0, '.')
from mjedit import Ed
ed = Ed('u_mj/m1_10.hwpx')
E, T, SA, op = ed.E, ed.T, ed.SA, ed.op
NE = {'넓이는?': '넓이를 구하시오.'}
for n, v, m, end in [(4, '22', '②', '넓이는?'), (5, '137', '④', '값은?'), (13, '{16} over {3}', '③', '값은?'), (15, '{1} over {6}', '①', '넓이는?'),
                     (17, '28', '⑤', '값은?'), (20, '1', '④', '변화량은?'), (21, '45``rmm', '③', '최고 높이는?'), (24, '16', '③', '값은?'),
                     (25, '{37} over {12}', '④', '넓이는?'), (27, '{4} over {3}', '④', '최솟값은?'), (28, '{7} over {3}', '④', '넓이는?'),
                     (29, '{8} over {3}', '②', '넓이는?'), (30, '{27} over {4}', '①', '넓이는?'), (32, '{51} over {4}', '③', '값은?'),
                     (33, '23', '②', '값은?'), (34, '{8} over {3}', '④', '넓이는?'), (35, '{1} over {6}', '③', '넓이는?'),
                     (37, '{11} over {2}', '⑤', '거리는?'), (39, '13', '③', '값은?'), (40, '{3} over {2}', '④', '넓이는?'),
                     (45, '675``rmm', '③', '높이는?')]:
    ne = {'넓이는?': '넓이를 구하시오.', '변화량은?': '변화량을 구하시오.', '최고 높이는?': '최고 높이를 구하시오.', '최솟값은?': '최솟값을 구하시오.',
          '거리는?': '거리를 구하시오.', '높이는?': '높이를 구하시오.'}.get(end)
    SA(n, v, m, ending=end, new_ending=ne)
# 33: 해설 새로 씀
for t in ['함수 ⟦y=f(x)⟧의 그래프와 그 역함수 ⟦y=g(x)⟧의 그래프는 직선 ⟦y=x⟧에 대하여 대칭이다.',
          '⟦f(1)=1⟧, ⟦f(2)=2⟧이므로 ⟦g(1)=1⟧, ⟦g(2)=2⟧',
          '따라서 구하는 넓이는',
          '⟦int _{1} ^{2} g(x)dx=2 TIMES 2-1 TIMES 1- int _{1} ^{2} f(x)dx⟧',
          '⟦=3- int _{1} ^{2} LEFT ( {1} over {3} x ^{2} + {2} over {3} RIGHT ) dx⟧',
          '⟦=3- LEFT [ {1} over {9} x ^{3} + {2} over {3} x RIGHT ] _{1} ^{2} =3- {13} over {9} = {14} over {9}⟧',
          '따라서 ⟦p=9⟧, ⟦q=14⟧이므로 ⟦p+q=23⟧']:
    op({'op': 'add_para', 'n': 33, 'part': 'sol', 'text': t, 'like_n': 31, 'like': '따라서 구하는 넓이를'})
E(11, 'sol', '{3} over {8}', sub='{8} over {3}')
T(1, 'q', '구하시오', '구하시오.')
E(1, 'sol', '{1} over {3} x^2 - {1} over {2} x^2', sub='{1} over {3} x^3 - {1} over {2} x^2')
E(3, 'sol', 'y= it- x^3 +ax', sub='y= it- x^2 +ax')
E(5, 'sol', '=int _{ 0} ^{ 1} {(x^3 - x^2 )dx  }+', sub='= it- int _{ 0} ^{ 1} {(x^3 - x^2 )dx  }+')
E(6, 'sol', '= {1} over {2} x^2 +2x', sub='+ {1} over {2} x^2 +2x')
E(12, 'q', '-ax  ^{2} ,', sub='-ax  ^{2}')
E(12, 'q', 'a<a<1', '0<a<1')
E(12, 'sol', 'a=1', 'x=1')
E(14, 'sol', '{x-(x  ^{3} -3x  ^{2} +3x)dx}', sub='{ LEFT { x-(x  ^{3} -3x  ^{2} +3x) RIGHT } dx}')
E(17, 'q', 'int _{0} ^{14}', sub='int _{2} ^{14}')
E(17, 'sol', 'B=  int _{0} ^{14}', sub='B=  int _{2} ^{14}')
T(18, 'q', '떄', '때')
T(18, 'sol', '운동방향', '운동 방향'); T(18, 'sol', '진행방향', '진행 방향')
for n in (19, 36):
    T(n, 'q', '(3) ', '⑶ ')
    T(n, 'sol', '(3) ', '⑶ ', all=True)
T(36, 'sol', '운동방향', '운동 방향')
T(20, 'q', '에 서의', '에서의')
E(23, 'sol', 'right) dt', sub='right) dy')
E(25, 'sol', 'y= it-2x  ^{2}', sub='y= it-x  ^{2}')
E(26, 'q', '`=`q  over  p', '{q} over {p}')
E(29, 'sol', '- LEFT [ pile{`#`} {1} over {3} x  ^{3} -x  ^{2} RIGHT ]', sub='+ LEFT [ pile{`#`} {1} over {3} x  ^{3} -x  ^{2} RIGHT ]')
T(31, 'q', '위의 점', ' 위의 점')
T(34, 'sol', '어두운 부분', '색칠한 부분')
E(39, 'q', 'q over p', '{q} over {p}')
E(39, 'sol', 'eqalign', 'f(x)= {cases{``-x  ^{2} +2x&~(x LEQ 1)#``-x+2&~(x GEQ 1)}}')
E(40, 'sol', 'int _ ^ (x ^{2} -1)dx', sub='int (x ^{2} -1)dx')
T(42, 'q', '이등분 될', '이등분될')
T(44, 'q', '넓이를 구하', '넓이를 구하시오.')
op({'op': 'del_para', 'n': 44, 'part': 'q', 'anchor': '^시오.'})
E(45, 'sol', 'int_35^40', sub='int_30^45')
# 수식 속 줄바꿈·탭
done = {(39, 'sol')}
for n in range(1, 47):
    for part in ('q', 'sol'):
        if (n, part) in done:
            continue
        for s in set(ed.scripts(n, part)):
            if re.search(r'[\t\n]', s) and not re.search(r'#\s*\n', s):
                op({'op': 'eq', 'n': n, 'part': part, 'old': s, 'new': re.sub(r'\s*[\r\n\t]+\s*', ' ', s).strip()})
ed.run('u_mj/m1_10_edit.json')
