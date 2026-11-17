# -*- coding: utf-8 -*-
"""미적분Ⅰ M 3단원(미분계수와 도함수) — C에서 옮기지 못한 문항 고치기"""
import sys
sys.path.insert(0, '.')
import hwpxedit as H
from mjedit import Ed
P = sys.argv[1] if len(sys.argv) > 1 else 'u_mM/mM_03.hwpx'
# 60: 해설을 [정답] 줄만 남기고 지운 뒤 다시 씀
x = H.load(P)
ps = H.paras_in(x, H.region(x, 60, 'sol'))
assert '[정답]' in H.render(x[ps[0][0]:ps[0][1]]) and len(ps) > 5
for s, e in reversed(ps[1:]):
    x = x[:s] + x[e:]
H.save(P, x)
ed = Ed(P)
E, T, SA, op = ed.E, ed.T, ed.SA, ed.op
op({'op': 'text', 'n': 60, 'part': 'sol', 'old': ' [정답] ①', 'new': ' [정답] ④'})
for t in ['ㄱ. ⟦lim _{x `->` 2} (x-2)=0⟧이므로 ⟦lim _{x `->` 2} f(x)=0⟧이고, ⟦f(x)⟧가 연속함수이므로 ⟦f(2)=0⟧⏎따라서 ⟦lim _{x `->` 2} {f(x)} over {x-2} = lim _{x `->` 2} {f(x)-f(2)} over {x-2}⟧의 값이 존재하므로 ⟦f(x)⟧는 ⟦x=2⟧에서 미분가능하다. (참)',
          'ㄴ. [반례] ⟦f(x)= LEFT | x-2 RIGHT | + LEFT | x+2 RIGHT |⟧이면 ⟦f(-x)= LEFT | -x-2 RIGHT | + LEFT | -x+2 RIGHT | =f(x)⟧이므로⏎⟦lim _{x `->` 2} {f(x)-f(-x)} over {x ^{2} -4} = lim _{x `->` 2} {0} over {x ^{2} -4} =0⟧⏎으로 극한값이 존재한다. 그러나⏎⟦lim _{x `->` 2+} {f(x)-f(2)} over {x-2} = lim _{x `->` 2+} {(x-2)+(x+2)-4} over {x-2} =2⟧⏎⟦lim _{x `->` 2-} {f(x)-f(2)} over {x-2} = lim _{x `->` 2-} {-(x-2)+(x+2)-4} over {x-2} =0⟧⏎이므로 ⟦f(x)⟧는 ⟦x=2⟧에서 미분가능하지 않다. (거짓)',
          'ㄷ. ⟦h ^{3} =t⟧로 놓으면 ⟦h `->` 0+⟧일 때 ⟦t `->` 0+⟧, ⟦h `->` 0-⟧일 때 ⟦t `->` 0-⟧이므로⏎⟦lim _{h `->` 0} {f(2+h ^{3} )-f(2)} over {h ^{3}} = lim _{t `->` 0} {f(2+t)-f(2)} over {t}⟧⏎따라서 이 극한값이 존재하면 ⟦f prime (2)⟧가 존재하므로 ⟦f(x)⟧는 ⟦x=2⟧에서 미분가능하다. (참)',
          '따라서 옳은 것은 ㄱ, ㄷ이다.']:
    op({'op': 'add_para', 'n': 60, 'part': 'sol', 'text': t})
# 14
E(14, 'sol', '{1} over {h} LEFT { f LEFT ( 1+2h RIGHT ) -f LEFT ( a RIGHT )', sub='{1} over {h} LEFT { f LEFT ( a+2h RIGHT ) -f LEFT ( a RIGHT )')
# 19
T(19, 'q', '의', '의 값을 구하시오.', after_eq="f'(-1)+f'(2)`")
op({'op': 'del_para', 'n': 19, 'part': 'q', 'anchor': '값을 구하시오.', 'exact': True})
E(19, 'sol', 'f(x)=3x ^{ 3}+x+1', 'f(x)=3x ^{2} +x+1')
E(27, 'sol', 'lim _{x `->` 0} {`f(x) }=f(1)', 'lim _{x `->` 1} f(x)=f(1)')
# 28
E(28, 'sol', 'h(0)=0', 'h(0)=3')
E(28, 'sol', 'lim _{x `->` 0+} {x-4`|`x`|} over {x}', sub='lim _{x `->` 0+} {x ^{2} -4`|`x`|} over {x}')
E(28, 'sol', 'lim _{x `->` 0-} {x-4`|`x`|} over {x}', sub='lim _{x `->` 0-} {x ^{2} -4`|`x`|} over {x}')
E(28, 'sol', '= lim _{x `->` 0+} {`(x-4} )= it-4', '= lim _{x `->` 0+} (x-4)= it-4')
# 30
SA(30, '-1', '②')
E(30, 'sol', 'x LEQ 1', 'x<1')
E(30, 'sol', '2x+b+7=0', '2a+b+7=0')
for a, b in (('(i) ', '(ⅰ) '), ('(ii) ', '(ⅱ) ')):
    T(30, 'sol', a, b)
# 31
E(31, 'sol', 'lim _{x `->` 0-} {g prime (x)} = lim _{x `->` 0+} {g prime (x)}', 'lim _{x `->` 0-} {g(x)-g(0)} over {x} = lim _{x `->` 0+} {g(x)-g(0)} over {x}')
SA(44, '16', '②')
SA(47, '4', '②')
SA(49, '10', '③', ending='합은?', new_ending='합을 구하시오.')
for n in (30, 44, 47, 48, 49, 57, 61):
    op({'op': 'del_para', 'n': n, 'part': 'sol', 'anchor': '[해설]', 'exact': True})
# 46: 머리말 지움, 좌미분계수 줄 넣음
for a in ('[해설]', '[rect]풀이전략', '[rect]문제풀이', '풀이전략', '문제풀이'):
    op({'op': 'del_para', 'n': 46, 'part': 'sol', 'anchor': a, 'exact': True, 'optional': True})
for a in ('^⟦x=2⟧에서 미분계수가 존재하는지', '^[step1]', '^[step2]', '^[step 3]', '^⟦x=2⟧에서의 미분계수를 구한다.'):
    op({'op': 'del_para', 'n': 46, 'part': 'sol', 'anchor': a})
T(46, 'sol', '미분가능하지 않다. (참)', '에서 미분가능하지 않다. (참)')
T(46, 'sol', '이르모', '이므로')
op({'op': 'add_para', 'n': 46, 'part': 'sol', 'after': '⟦=2 TIMES (-2)= it-4⟧',
    'text': '⟦lim _{x `->` 2-} {f(x)g(x)} over {x-2} = lim _{x `->` 2-} {f(x) TIMES (-2x+4)} over {x-2}⟧⏎⟦= lim _{x `->` 2-} LEFT { -2f(x) RIGHT } =(-2) TIMES 2= it-4⟧'})
# 48
T(48, 'q', '에서옳은', '에서 옳은')
E(48, 'sol', 'lim _{x `->` 0} {{f(x)} over {(x-1)  ^{k}}}', sub='lim _{x `->` 1} {{f(x)} over {(x-1)  ^{k}}}')
# 49 집합 A, B
op({'op': 'eq', 'n': 49, 'part': 'q', 'old': 'LEFT. A= LEFT { a left| lim _{x `->` a} {LEFT { f(x)-f(a) RIGHT } =0,`-1<a<6}  RIGHT ',
    'new': 'A= LEFT { a left| lim _{x `->` a} LEFT { f(x)-f(a) RIGHT } =0,~-1<a<6 RIGHT } ,'})
op({'op': 'eq', 'n': 49, 'part': 'q', 'old': 'LEFT . B= LEFT { b LEFT | lim _{x `->` b} {{f(x)-f(b)} over {x-b}} 의`값이`존재하고,`-1<b<6 RIGHT } RIGHT . RIGHT .',
    'new': 'B= LEFT { b left| lim _{x `->` b} {f(x)-f(b)} over {x-b} 의`값이`존재하고,`-1<b<6 RIGHT }'})
# 57 채점 표
E(57, 'sol', "f prime (1)f'(1)+g(1)g prime (1)", "f(1)f'(1)+g(1)g'(1)")
# 59
SA(59, '-13', '②')
for a in ('[해설]', '[rect]풀이전략', '[rect]문제풀이', '풀이전략', '문제풀이'):
    op({'op': 'del_para', 'n': 59, 'part': 'sol', 'anchor': a, 'exact': True, 'optional': True})
for a in ('^다항식의 나눗셈을 이용하여', '^[step 1]', '^[step 2]', '^[step 3]'):
    op({'op': 'del_para', 'n': 59, 'part': 'sol', 'anchor': a})
op({'op': 'append', 'n': 59, 'part': 'sol', 'after_eq': 'g(1)=a+b= it-3', 'text': ' …… ㉤'})
# 61
E(61, 'sol', '= lim _{x `->` 0+} {LEFT { (x-t)(x-3) RIGHT } = it-3t}', sub='= lim _{x `->` 0+} {LEFT { -(x-t)(x-3) RIGHT } = it-3t}')
for a, b in (('(i) ', '(ⅰ) '), ('(ii) ', '(ⅱ) '), ('(iii) ', '(ⅲ) ')):
    T(61, 'sol', a, b)
# 62: 정답 오류 -2 → -4
E(62, 'q', '\tf(x)', 'f(x)=x')
op({'op': 'del_eq', 'n': 62, 'part': 'q', 'old': '=x'})
SA(62, '-4', '②', ending='의 값은?')
E(62, 'sol', 'h(t)= {cases', sub=None, new=[s for s in ed.scripts(62, 'sol') if s.startswith('h(t)= {cases')][0].replace('(t< it 3)', '(t< it-3)').replace('(-4 LEQ t< it -1)', '(-3 LEQ t< it-1)'))
E(62, 'sol', 'h prime (t)= {cases', sub=None, new=[s for s in ed.scripts(62, 'sol') if s.startswith('h prime (t)= {cases')][0].replace('#~`-t _{it}&', '#~`-1 _{it}&'))
op({'op': 'add_para', 'n': 62, 'part': 'sol', 'text': '따라서 ⟦a+b+c=(-3)+(-1)+0= it-4⟧'})
ed.run('u_mM/mM_03_edit.json')
