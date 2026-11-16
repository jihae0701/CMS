# -*- coding: utf-8 -*-
"""미적분Ⅰ 3단원(미분계수와 도함수) 내용 고치기"""
import sys
sys.path.insert(0, '.')
from mjedit import Ed
ed = Ed('u_mj/m1_03.hwpx')
E, T, SA, op = ed.E, ed.T, ed.SA, ed.op

for n, v, m in [(11, '{1} over {2}', '①'), (12, '18', '④'), (15, '6', '④'), (24, '24', '④'), (25, '10', '⑤'), (26, '6', '③'),
                (27, '{2} over {3}', '②'), (28, '-2', '②'), (29, '12', '③'), (33, '8', '⑤'), (34, '{1} over {3}', '②'),
                (35, '1', '①'), (36, '27', '②'), (37, '20', '②'), (38, '5', '①'), (39, '4', '⑤'), (52, '-2', '②')]:
    if n == 38:
        SA(n, v, m, ending='미분계수는?', new_ending='미분계수를 구하시오.')
    elif n == 29:
        SA(n, v, m, ending='값은?')
    else:
        SA(n, v, m)

T(5, 'sol', '[다른  이]', '[다른 풀이]')
op({'op': 'text_eq', 'n': 45, 'part': 'sol', 'old': ' [정답] ①', 'pre': ' [정답] ', 'eq': '-2', 'post': ''})
T(7, 'sol', ' 이다', '이다.', exact=True)
E(10, 'sol', 'f`prime LEFT ( 3 RIGHT ) times', sub='f`prime LEFT ( a RIGHT ) times')
E(12, 'sol', '1 over 12', '= {1} over {12} f` prime (-2)= {1} over {2}')
E(12, 'sol', "'(2)=6", 'f` prime (-2)=6')
E(12, 'sol', '=18', 'f(-2)f` prime (-2)=3 times 6=18')
E(14, 'sol', 'f LEFT ( 1+2h RIGHT ) -f LEFT ( a RIGHT )', sub='f LEFT ( a+2h RIGHT ) -f LEFT ( a RIGHT )')
T(17, 'sol', '중ㅇ서', '중에서'); T(17, 'sol', '것은ㄱ, ㄷ', '것은 ㄱ, ㄷ')
E(18, 'sol', 'lim _{x `->` 0} {`f(x) }=f(1)', 'lim _{x `->` 1} {`f(x) }=f(1)')
E(23, 'sol', 'f(x)=3x ^{ 3}+x+1', sub='f(x)=3x ^{ 2}+x+1')
E(26, 'sol', '{3} over {rm 2 it}', sub='{3} over {2}')
op({'op': 'text', 'n': 30, 'part': 'sol', 'old': ' 답 ③', 'new': ' [정답] ③', 'exact': True})
E(30, 'sol', 'h(0)=0', sub='h(0)=3')
for s in [s for s in ed.scripts(30, 'sol') if '{x-4`|`x`|} over {x}' in s]:
    op({'op': 'eq', 'n': 30, 'part': 'sol', 'old': s, 'new': s.replace('{x-4`|`x`|} over {x}', '{x ^{2} -4`|`x`|} over {x}')})
E(30, 'sol', '{`(x-4} )', sub='{`(x-4)}')
for part in ('q', 'sol'):
    for s in [s for s in ed.scripts(31, part) if 'f(f prime (x)}' in s]:
        op({'op': 'eq', 'n': 31, 'part': part, 'old': s, 'new': s.replace('{f(f prime (x)} )', 'f(f prime (x))').replace('{f(f prime (x)})', 'f(f prime (x))')})
E(31, 'sol', 'f(x)=t', 'f prime (x)=t')
E(32, 'sol', 'lim _{x `->` +1}', sub='lim _{x `->` 1+}')
for s in [s for s in ed.scripts(33, 'sol') if s.startswith('lim _{x `->` -1+} {`f(x)} = lim _{x `->` -1-} {`f(x)}')]:
    op({'op': 'eq', 'n': 33, 'part': 'sol', 'old': s, 'new': "lim _{x `->` -1+} f` prime (x) = lim _{x `->` -1-} f` prime (x)"})
E(43, 'sol', 'a+b=20', sub='a+b= it-20')
E(44, 'sol', '=(x-1)Q(x)+5x-4', sub='=(x-1) ^{2} Q(x)+5x-4')
T(44, 'sol', '대하며', '대하여')
E(47, 'sol', 'f(4)-9', "lim _{x `->` 2} {f(x^2 )-9} over {f(x)-3} #=lim _{x `->` 2} {f(x^2 )-f(4)} over {f(x)-f(2)} ~(because~f(2)=3,~f(4)=9) #= lim _{x `->` 2} LEFT { {f(x^2 )-f(4)} over {x^2 -4} times {x-2} over {f(x)-f(2)} times (x+2) RIGHT } #=f` prime (4) times {1} over {f` prime (2)} times 4 #=9 times {1} over {3} times 4=12")
op({'op': 'text', 'n': 48, 'part': 'sol', 'old': ' [정답] ㄱ, ㄴ', 'new': ' [정답] ㄱ, ㄷ', 'exact': True})
E(48, 'sol', 'TIMES {1} over {3} =0', sub='TIMES {1} over {3} =0 #\r\n& THEREFORE ~f` prime (1)=0 ~(거짓)')
E(49, 'sol', 'g(x)&=', sub='g(1)&=')
T(53, 'q', '함수', '함수 ', exact=True)
ed.run('u_mj/m1_03_edit.json')
