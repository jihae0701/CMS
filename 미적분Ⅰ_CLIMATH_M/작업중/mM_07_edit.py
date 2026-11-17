# -*- coding: utf-8 -*-
"""미적분Ⅰ M 7단원(부정적분) — C에서 옮기지 못한 문항 고치기 (35번은 mM_07_q35.py)"""
import sys, re
sys.path.insert(0, '.')
import hwpxedit as H
from mjedit import Ed
P = sys.argv[1] if len(sys.argv) > 1 else 'u_mM/mM_07.hwpx'
# 33: 정답 머리가 '정답.png' 그림 → 글 [정답]
x = H.load(P)
(a, b), = H.region(x, 33, 'sol')[:1]
m = re.search(r'<hp:t> </hp:t><hp:pic\b(?:(?!</hp:pic>).)*?정답\.png(?:(?!</hp:pic>).)*?</hp:pic><hp:t> </hp:t>', x[a:b], re.S)
assert m
x = x[:a + m.start()] + '<hp:t> [정답] </hp:t>' + x[a + m.end():]
H.save(P, x)
ed = Ed(P)
E, T, SA, op = ed.E, ed.T, ed.SA, ed.op
E(11, 'sol', '2+1+2= it-k+2k+1\r\n', '2+1+2= it-k+2k+1')
for n, v, mk, end in [(13, '45', '②', '값은?'), (18, '64', '⑤', '값은?'), (21, '-6', '①', '값은?'), (27, '{1} over {6}', '④', '값은?'), (28, '-2', '①', '값은?'),
                      (32, '-2', '①', '값은?'), (34, '10', '⑤', '값은?'), (37, '47', '④', '값은?'), (38, '125', '⑤', '합은?')]:
    SA(n, v, mk, ending=end, new_ending=end.replace('값은?', '값을 구하시오.') if end == '값은?' else '합을 구하시오.')
# 정답 줄이 ' [정답] '·'②'처럼 두 조각인 문항
for o in ed.ops:
    if o['op'] == 'text_eq' and o['n'] in (13, 27, 28, 37, 38):
        o['old'], o['pre'] = o['old'].replace(' [정답] ', ''), ''
for n in (13, 37, 38):
    T(n, 'sol', '[해설] ', '')
for n in (17, 18, 32):
    op({'op': 'del_para', 'n': n, 'part': 'sol', 'anchor': '[해설]', 'exact': True})
# 24: '다음 중 f(1)을 나타낸 것은?' → 'n에 대한 식으로 나타내시오.'
T(24, 'q', '일 때, 다음 중 ', '일 때, ')
T(24, 'q', '을 나타낸 것은?', '을 n에 대한 식으로 나타내시오.')
op({'op': 'text_eq', 'n': 24, 'part': 'q', 'old': 'n에', 'pre': '', 'eq': 'n', 'post': '에', 'sub': True})
op({'op': 'del_para', 'n': 24, 'part': 'q', 'anchor': '^①'})
op({'op': 'del_para', 'n': 24, 'part': 'q', 'anchor': '^④', 'optional': True})
op({'op': 'text_eq', 'n': 24, 'part': 'sol', 'old': ' [정답] ②', 'pre': ' [정답] ', 'eq': 'n', 'post': ''})
E(27, 'sol', 'f(x)= int {x ^{3} -2x} over {x+2} dx+ int {2x-1} over {x+2} dx', 'f(x)= int {x ^{3} -2x} over {x-1} dx+ int {2x-1} over {x-1} dx')
E(27, 'sol', '= int {(x-1)(x^2 +x+1)} over {x-1}', '= int {(x-1)(x^2 +x+1)} over {x-1} dx')
E(34, 'sol', 'f(0-h)', sub='f(0+h)')
E(37, 'sol', 'f LEFT ( -1=4 RIGHT )', 'f LEFT ( -1 RIGHT ) =4')
T(37, 'sol', '애서', '에서')
E(37, 'sol', '=48+32+24-24+15=47', sub='=48+32-24-24+15=47')
E(38, 'sol', 'a int {LEFT ( {1} over {4} x ^{4} -x ^{3} -2x ^{2} +12x RIGHT )} +C', '=a LEFT ( {1} over {4} x ^{4} -x ^{3} -2x ^{2} +12x RIGHT ) +C')
op({'op': 'append', 'n': 38, 'part': 'sol', 'after_eq': '= {45} over {4} a+C=61', 'text': '   …… ㉡'})
E(38, 'sol', 'x  ^{4} -x  ^{3} -8x  ^{2}', sub='x  ^{4} -4x  ^{3} -8x  ^{2}')
# 39: 정답 줄은 이미 값(4) → 문제만 단답형으로
T(39, 'q', '값은?', '값을 구하시오.')
op({'op': 'del_para', 'n': 39, 'part': 'q', 'anchor': '^①'})
op({'op': 'del_para', 'n': 39, 'part': 'q', 'anchor': '^④'})
E(40, 'q', 'lim _{n `->` inf}', sub='lim _{x `->` inf}')
op({'op': 'eq', 'n': 40, 'part': 'sol', 'old': [s for s in ed.scripts(40, 'sol') if 'n `->`' in s][0], 'new': [s for s in ed.scripts(40, 'sol') if 'n `->`' in s][0].replace('lim _{n `->` inf}', 'lim _{x `->` inf}')})
E(47, 'q', 'int { LEFT { f(x) +4 } RIGHT } dx', 'int { LEFT { f(x) +4x RIGHT } } dx = xf(x) + 2 x^3 - 4 x^2')
E(49, 'q', "int {xf``'(x)dx= {2} over {3} x ^{3}} +x ^{2}", "int {xf`'(x)} dx= {2} over {3} x ^{3} +x ^{2}")
for a in ('Step 1 미분을', 'Step 2 곱의'):
    op({'op': 'del_para', 'n': 49, 'part': 'sol', 'anchor': a})
ed.run('u_mM/mM_07_edit.json')
