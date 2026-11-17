# -*- coding: utf-8 -*-
"""미적분Ⅰ M 8단원(정적분) — C에서 옮기지 못한 문항 고치기 (끝에 negsub.py로 첨자 묶음)"""
import sys, re
sys.path.insert(0, '.')
import hwpxedit as H
from mjedit import Ed
P = sys.argv[1] if len(sys.argv) > 1 else 'u_mM/mM_08.hwpx'
x = H.load(P)   # 59: 정답 머리 그림 → [정답]
(a, b), = H.region(x, 59, 'sol')[:1]
m = re.search(r'<hp:t> </hp:t><hp:pic\b(?:(?!</hp:pic>).)*?정답\.png(?:(?!</hp:pic>).)*?</hp:pic><hp:t> </hp:t>', x[a:b], re.S)
assert m
x = x[:a + m.start()] + '<hp:t> [정답] </hp:t>' + x[a + m.end():]
H.save(P, x)
ed = Ed(P)
E, T, SA, op = ed.E, ed.T, ed.SA, ed.op
for n, v, mk in [(15, '18', '④'), (17, '{11} over {3}', '③'), (20, '10', '②'), (21, '-2', '①'), (23, '4', '④'), (26, '12', '①'), (27, '10', '⑤'),
                      (34, '{19} over {3}', '⑤'), (35, '{3} over {2}', '③'), (40, '13', '②'), (48, '12', '④'), (55, '385', '⑤'), (56, '-16', '④'), (57, '31', '①')]:
    SA(n, v, mk)
for n in (26, 27, 40, 57):
    T(n, 'sol', '[해설] ', '')
op({'op': 'del_para', 'n': 53, 'part': 'sol', 'anchor': '[해설]', 'exact': True})
for s in [s for s in ed.scripts(18, 'q') if 'x^2n' in s]:
    op({'op': 'eq', 'n': 18, 'part': 'q', 'old': s, 'new': s.replace('x^2n-1', 'x^{2n-1}').replace('x^2n-2', 'x^{2n-2}').replace('x^2n', 'x^{2n}')})
E(26, 'sol', ' int _{0} ^{2} {LEFT { f(x)-f(-x) RIGHT } dx=16}', sub=' int _{0} ^{2} {LEFT { f(x)+f(-x) RIGHT } dx=16}')
E(27, 'sol', '= {bmatrix{x  ^{3}&-6x  ^{2}&+8x}}  _{-1} ^{5}', '= LEFT [ x  ^{3} -6x  ^{2} +8x RIGHT ]  _{-1} ^{5}')
E(34, 'sol', 'left [ pile{ `#` } x right]_-2^0', sub='LEFT [ x RIGHT ] _{-2} ^{0}')
E(55, 'q', 'sum_k=1^10{int_0^k{2f(x)dx}}', 'sum _{k=1} ^{10} {int _{0} ^{k} {2f(x)dx}}')
E(55, 'sol', 'therefore sum_k=1 ^10 int_0 ^k', 'therefore sum _{k=1} ^{10} int _{0} ^{k} {2f(x)dx}= sum _{k=1} ^{10} k^2 = {10 times 11 times 21} over {6} = 385')
E(57, 'q', ' int _{2} ^{k-1} ', sub=' int _{2} ^{k+1} ')
E(57, 'sol', 'f(x)=a(x-2)  ^{2} +4(a는`0이`아닌`상수)', 'f(x)=a(x-2)  ^{2} +4')
op({'op': 'append', 'n': 57, 'part': 'sol', 'after_eq': 'f(x)=a(x-2)  ^{2} +4', 'text': ' (a는 0이 아닌 상수)'})
op({'op': 'text_eq', 'n': 57, 'part': 'sol', 'old': 'a는 0이', 'pre': '', 'eq': 'a', 'post': '는 0이', 'sub': True})
E(59, 'sol', 'x  ^{2} -x-6-0`', 'x  ^{2} -x-6=0')
_s = [s for s in ed.scripts(59, 'sol') if s.startswith('LEFT. = LEFT [')][0]
op({'op': 'eq', 'n': 59, 'part': 'sol', 'old': _s, 'new': _s[len('LEFT. '):].rstrip()[:-len('RIGHT')].rstrip()})
for a_, b_ in (('ⅰ) ', '(ⅰ) '), ('ⅱ) ', '(ⅱ) '), ('ⅲ) ', '(ⅲ) ')):
    T(59, 'sol', a_, b_)
ed.run('u_mM/mM_08_edit.json')
