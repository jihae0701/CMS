# -*- coding: utf-8 -*-
"""미적분Ⅰ M 10단원(정적분의 활용) — C에서 옮기지 못한 문항 + C에서 글을 직접 고친 것 (끝에 negsub.py)"""
import sys, html
sys.path.insert(0, '.')
import hwpxedit as H
from mjedit import Ed
P = sys.argv[1] if len(sys.argv) > 1 else 'u_mM/mM_10.hwpx'
# 29: 수식 S가 두 번 → 두 번째 지움 (C 26번과 같음)
x = H.load(P)
ms = [m for a, b in H.region(x, 29, 'q') for m in H.EQ.finditer(x, a, b) if html.unescape(H.SC.search(m.group(0)).group(2)) == '`S']
assert len(ms) == 2
x = x[:ms[1].start()] + x[ms[1].end():]
H.save(P, x)
ed = Ed(P)
E, T, SA, op = ed.E, ed.T, ed.SA, ed.op
# 15: 쉼표, (단, …) 괄호를 글로 (C 12번과 같음)
op({'op': 'append', 'n': 15, 'part': 'q', 'after_eq': 'y=x  ^{3} -ax  ^{2}', 'text': ','})
op({'op': 'del_eq', 'n': 15, 'part': 'q', 'old': '('})
op({'op': 'del_eq', 'n': 15, 'part': 'q', 'old': ')'})
T(15, 'q', '단, ', '(단, ')
op({'op': 'append', 'n': 15, 'part': 'q', 'after_eq': '0<a<1', 'text': ')'})
# 39: (3) → ⑶, 운동방향 → 운동 방향
T(39, 'q', '(3) ', '⑶ ')
T(39, 'sol', '  (3) ', '  ⑶ ')
T(39, 'sol', '(3) ', '⑶ ', exact=True)
T(39, 'sol', '는 운동방향을 바꾸게 되므로 ', '는 운동 방향을 바꾸게 되므로 ')
for n, v, mk, end, ne in [(3, '2', '②', '넓이는?', '넓이를 구하시오.'), (6, '16', '③', '값은?', '값을 구하시오.'), (10, '{27} over {4}', '①', '넓이는?', '넓이를 구하시오.'),
                          (12, '{3} over {2}', '③', '값은?', '값을 구하시오.'), (27, '137', '④', '값은?', '값을 구하시오.'), (31, '{7} over {3}', '④', '넓이는?', '넓이를 구하시오.'),
                          (32, '{8} over {3}', '②', '넓이는?', '넓이를 구하시오.'), (36, '23', '②', '값은?', '값을 구하시오.'), (50, '{129} over {4}', '③', '최댓값은?', '최댓값을 구하시오.')]:
    SA(n, v, mk, ending=end, new_ending=ne)
E(36, 'sol', 'int_1 ^2 f(x) dx + int_f(1) ^f(2) g(x) = 2f(2)-f(1)', 'int _{1} ^{2} f(x) dx + int _{f(1)} ^{f(2)} g(x)dx = 2f(2)-f(1)')
E(48, 'sol', ' = int_0^sqrtk (k- x^2 )dx + int_sqrtk ^2 ( x^2 -k )dx ', ' = int _{0} ^{sqrt k} (k- x^2 )dx + int _{sqrt k} ^{2} ( x^2 -k )dx')
for s in [s for s in ed.scripts(48, 'sol') if 'sqrtk' in s and 'int' not in s]:
    op({'op': 'eq', 'n': 48, 'part': 'sol', 'old': s, 'new': s.replace('sqrtk', 'sqrt k'), 'all': True})
E(50, 'sol', "f`' LEFT ( t RIGHT ) =0`", "f`' LEFT ( t RIGHT ) +1=0`")
E(50, 'sol', '\nS`prime(t)', "S`'(t)")
ed.run('u_mM/mM_10_edit.json')
