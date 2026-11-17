# -*- coding: utf-8 -*-
"""미적분Ⅰ M 4단원(접선의 방정식과 평균값 정리) — C에서 옮기지 못한 문항 고치기"""
import sys
sys.path.insert(0, '.')
from mjedit import Ed
ed = Ed(sys.argv[1] if len(sys.argv) > 1 else 'u_mM/mM_04.hwpx')
E, T, SA, op = ed.E, ed.T, ed.SA, ed.op
SA(10, 'sqrt {5}', '④', ending='최단 거리는?', new_ending='최단 거리를 구하시오.')
SA(11, '{sqrt {2}} over {2}', '①', ending='최단 거리는?', new_ending='최단 거리를 구하시오.')
SA(12, '3', '③', ending='기울기는?', new_ending='기울기를 구하시오.')
SA(13, '{5} over {4}', '①')
SA(19, '23', '③', ending='최솟값은?', new_ending='최솟값을 구하시오.')
SA(20, '8', '③', ending='개수는?', new_ending='개수를 구하시오.')
SA(42, '{2 sqrt {5}} over {5}', '②', ending='최솟값은?', new_ending='최솟값을 구하시오.')
SA(51, '-7', '②')
SA(54, '-4', '①')
SA(55, '16', '③', ending='최댓값은?', new_ending='최댓값을 구하시오.')
SA(56, '36', '①')
SA(57, '2', '②', ending='최댓값은?', new_ending='최댓값을 구하시오.')
T(12, 'sol', '점선의 기울기', '접선의 기울기')
T(13, 'sol', '이 점하는 점', '이 접하는 점')
T(13, 'sol', '점점을', '접점을')
T(19, 'sol', '에서 연속이', '에서 연속이고')
T(19, 'sol', '고 열린구간', '열린구간')
T(20, 'sol', '집하에서', '집합에서')
# 56
for a, b in (('㉢', '㉡'), ('㉣', '㉢'), ('㉤', '㉣')):
    T(56, 'sol', a, b, all=True)
T(56, 'sol', '다을', '㉠을')
E(56, 'sol', 'f(x)=x^{2}+a x-3( because(', 'f(x)=x^{2}+ax-3')
T(56, 'sol', '가)', ' (∵ 조건 (가))', after_eq='f(x)=x^{2}+ax-3')
op({'op': 'del_eq', 'n': 56, 'part': 'sol', 'old': ')'})
E(56, 'sol', 'f(x)=x^{3}+a x^{2}+b x-3( because', 'f(x)=x^{3}+ax^{2}+bx-3')
T(56, 'sol', '(가))라 하면', ' (∵ 조건 (가))라 하면')
E(57, 'sol', 'y=|2 a(x-1)|=|2 a  PVER  x-1|', 'y=|2a(x-1)|=|2a||x-1|')
# 58
E(58, 'sol', 'rm B left(it5a,``0 right)', 'rm B left( 5a,``0 right)')
E(58, 'sol', 'rmbarOA =it root5 a', 'bar{rm OA} = sqrt {5} a')
E(58, 'sol', 'rmbarAB =2root5 ita`', 'bar{rm AB} =2 sqrt {5} a')
E(58, 'sol', 'rmbarOA times barAB', 'bar{rm OA} times bar{rm AB}')
# 59
T(59, 'sol', '접섬', '접선')
E(59, 'sol', '(because~', 'LEFT ( because~t GEQ it-2 RIGHT )')
op({'op': 'del_eq', 'n': 59, 'part': 'sol', 'old': 't{ge{it-2)}}'})
T(59, 'q', '도함수의 활용⑴', '도함수의 활용(1)')
ed.run('u_mM/mM_04_edit.json')
