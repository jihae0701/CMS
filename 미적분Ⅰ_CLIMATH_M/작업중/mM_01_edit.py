# -*- coding: utf-8 -*-
"""미적분Ⅰ M 1단원(함수의 극한) — C에서 옮기지 못한 문항(새·바뀐 문항) 고치기"""
import sys
sys.path.insert(0, '.')
from mjedit import Ed
ed = Ed(sys.argv[1] if len(sys.argv) > 1 else 'u_mM/mM_01.hwpx')
E, T, SA, op = ed.E, ed.T, ed.SA, ed.op
for n, v, m in [(6, '-2', '②'), (11, '-1', '①'), (14, '1', '④'), (17, '-5', '⑤'), (18, '3', '③'), (32, '{5} over {4}', '④'),
                (33, '20', '⑤'), (34, '3', '②'), (41, '- {1} over {2}', '①'), (43, '-1', '②'), (49, '64', '⑤'), (52, '-2', '①'), (60, '-1', '②'),
                (61, '2', '⑤'), (62, '1', '①'), (63, '16', '④'), (64, '4', '⑤'), (68, '7', '③'), (69, '-1', '④'), (74, '32', '①'),
                (75, '{3} over {5}', '③'), (76, '4', '④'), (78, '{1} over {4}', '②')]:
    SA(n, v, m)
SA(19, 'a=2,~b= it-1', '④')
SA(21, '-1', '①', ending='은?', new_ending='을 구하시오.')
SA(79, '{49} over {8}', '④', sol_old=' [정답] ④ ')
T(19, 'sol', '띠라서', '따라서')
E(14, 'sol', 'lim _{x `->` +0} f(x)', sub='lim _{x `->` 0+} f(x)')
T(12, 'sol', '수렴하는 것은 ㄱ, ㄷ, ㄹ', '수렴하는 것은 ㄱ, ㄷ, ㄹ이다.')
# 15: 문제 ⑶ x→0+ ↔ 해설 x→0- → 문제를 해설에 맞춤
op({'op': 'eq', 'n': 15, 'part': 'q', 'old': 'lim _{x `->` 0+} {{LEFT [ x-1 RIGHT ]} over {x-1}}  ', 'new': 'lim _{x `->` 0-} {{LEFT [ x-1 RIGHT ]} over {x-1}}'})
E(15, 'sol', 'lim _{x `->` 0+} {{0} =0}', sub='lim _{x `->` 0+} {0} over {x} =0')
T(15, 'q', '극한의 조사하고', '극한을 조사하고')
E(21, 'sol', 'lim _{x `->` 2} {f(1-x)} =it-1', sub='lim _{x `->` 2} {f(x)} =it-1')
# 23: 해설 항목 이름·참거짓·결론
op({'op': 'text', 'n': 23, 'part': 'sol', 'old': 'ㄷ. ', 'new': 'ㄴ. ', 'before_eq': 'lim _{t `->` inf} {f LEFT ( {3t+1} over {t-1} RIGHT )}'})
op({'op': 'append', 'n': 23, 'part': 'sol', 'after_eq': '=2', 'text': ' (거짓)'})
op({'op': 'append', 'n': 23, 'part': 'sol', 'after_eq': 'lim _{t `->` -inf} {f LEFT ( {2t+1} over {2t} RIGHT )} =1', 'text': ' (참)'})
op({'op': 'add_para', 'n': 23, 'part': 'sol', 'text': '따라서 옳은 것은 ㄱ, ㄷ이다.'})
op({'op': 'eq', 'n': 27, 'part': 'q', 'old': 'alpha', 'new': 'k', 'last': True})
op({'op': 'text', 'n': 34, 'part': 'sol', 'old': '[해설] ', 'new': ''})
E(34, 'sol', 'sqrt {x  ^{4} +1} +x}}', sub='sqrt {x  ^{4} +1} +x  ^{2}}}')
E(34, 'sol', 'x  ^{n-1} LEFT ( sqrt {1+ {1} over {x}} +1 RIGHT )', sub='x  ^{n-2} LEFT ( sqrt {1+ {1} over {x}} +1 RIGHT )')
# 41: 문제 x^5 → x^2 (해설·선택지 기준)
for p in ('q', 'sol'):
    op({'op': 'eq', 'n': 41, 'part': p, 'old': 'lim _{x `->` 1} {1} over {x-1} LEFT ( {x ^{5} `+5} over {x+1} -3 RIGHT )', 'new': 'lim _{x `->` 1} {1} over {x-1} LEFT ( {x ^{2} +5} over {x+1} -3 RIGHT )'})
# 51: 정답 오류 6 → 7
op({'op': 'eq', 'n': 51, 'part': 'sol', 'old': ' {6}', 'new': '7'})
E(51, 'sol', 'f(x)=3x  ^{3} +x  ^{2} +2x', sub='f(x)=3x  ^{3} +2x  ^{2} +2x')
E(51, 'sol', 'f(1)=6', sub='f(1)=7')
op({'op': 'text', 'n': 53, 'part': 'q', 'old': ']에서', 'new': '에서'})
E(53, 'q', '{x^2 –1}', sub='{x^2 -1}')
T(55, 'q', '존재하면 |', '존재하면 ')
E(55, 'sol', 'lim _{x `->` 0} f(x) over g(x) =beta', sub='lim _{x `->` a} f(x) over g(x) =beta')
# 60: 절편 계산 줄 다시 씀
E(60, 'sol', '- {roott} over {2} = {t} over {roott} (x -t)`', '- {sqrt t} over {2} = it- sqrt t LEFT ( x - {t} over {2} RIGHT )')
E(60, 'sol', 'y - root {t} over {2} = it- {t^2} over {roott} `', 'y - {sqrt t} over {2} = it- sqrt t LEFT ( 0 - {t} over {2} RIGHT )')
_s = [s for s in ed.scripts(60, 'sol') if '-1 sqrt {t}} over' in s][0]
op({'op': 'eq', 'n': 60, 'part': 'sol', 'old': _s, 'new': _s.replace('-1 sqrt {t}} over', '- {1} over {2} sqrt {t}} over').replace('+1 sqrt {t}} = it-1', '+ {1} over {2} sqrt {t}} = it-1')})
# 62: 해설 변수 x → t, 삼각형 이름
op({'op': 'del_para', 'n': 62, 'part': 'sol', 'anchor': '해설'})
for s in [s for s in ed.scripts(62, 'sol') if 'x' in s]:
    op({'op': 'eq', 'n': 62, 'part': 'sol', 'old': s, 'new': s.replace('x', 't').replace('TRIANGLE {{rm ABC}}', 'TRIANGLE {{rm AOB}}')})
E(63, 'sol', 'bar{rm AH}=6-y', sub='bar{rm AH}= LEFT | y-6 RIGHT |')
for s in [s for s in ed.scripts(64, 'sol') if '＝' in s]:
    op({'op': 'eq', 'n': 64, 'part': 'sol', 'old': s, 'new': s.replace('＝', '=')})
for n in (65, 68, 74, 77):
    op({'op': 'text', 'n': n, 'part': 'sol', 'old': '[해설] ', 'new': ''})
op({'op': 'del_eq', 'n': 68, 'part': 'sol', 'old': 'lim _{x `->` inf} {{2f(x)-g(x)} over {f(x)+2g(x)}} = lim _{x `->` inf} {{h(x)-1} over {h(x)+1} = {2} over {4} = {1} over {2}}'})
T(69, 'sol', '최솟값', '최댓값', after_eq='x=2'); T(69, 'sol', '최댓값', '최솟값', before_eq=' - {1} over {4} ')
E(77, 'sol', '{x  ^{2} +ax  ^{2} +bx+1}', sub='{x  ^{3} +ax  ^{2} +bx+1}')
E(78, 'q', '{\\P} it (t,~ t^2 )', sub='rm P it (t,~ t^2 )')
E(78, 'sol', '{\\M} left(', sub='rm M left(')
E(78, 'sol', '– 1 over t', sub='- 1 over t')
for s in [s for s in ed.scripts(79, 'sol') if s.strip() == 'y= g(x)' or s.strip() == 'y=g(x)']:
    op({'op': 'eq', 'n': 79, 'part': 'sol', 'old': s, 'new': 'y=h(x)', 'all': True})
E(79, 'sol', 'g(x)= {cases{pile{########}}}', sub='f(a)= {cases{pile{########}}}')
E(79, 'sol', 'lim _{a `->` k+1} f(a) neq lim _{a `->` k-1} f(a) ', sub='lim _{a `->` k+} f(a) neq lim _{a `->` k-} f(a)')
T(79, 'sol', '따라서', '따라서 ')
ed.run('u_mM/mM_01_edit.json')
