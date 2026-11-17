# -*- coding: utf-8 -*-
"""미적분Ⅰ M 5단원(도함수의 활용(2)) — C에서 옮기지 못한 문항 고치기"""
import sys, re, html
sys.path.insert(0, '.')
import hwpxedit as H
from mjedit import Ed
P = sys.argv[1] if len(sys.argv) > 1 else 'u_mM/mM_05.hwpx'
# 55: 증감표(53번 표가 잘못 들어감)를 다시 채움 — 표 안 수식을 차례로 바꾸고, 미분계수가 없는 두 칸은 비움
x = H.load(P)
(a, b), = [sp for sp in H.region(x, 55, 'sol') if '<hp:tbl' in x[sp[0]:sp[1]]][:1]
t0 = x.index('<hp:tbl', a); t1 = x.index('</hp:tbl>', t0) + len('</hp:tbl>')
tbl = x[t0:t1]
eqs = list(H.EQ.finditer(tbl))
old = [html.unescape(H.SC.search(m.group(0)).group(2)) for m in eqs]
assert [s.strip() for s in old] == ['x', 'cdots', '-1', 'cdots', '1', 'cdots', '3', 'cdots', "f`' LEFT ( x RIGHT )", '-', '-', '-', '0', '+', '+', '+',
                                    'f LEFT ( x RIGHT )', 'NEARROW', '0', 'NEARROW', '-', 'SEARROW', '0', 'NEARROW'], old
new = ['x', 'cdots', '-1', 'cdots', '{1} over {6}', 'cdots', '1', 'cdots', "f`' LEFT ( x RIGHT )", '+', None, '+', '0', '-', None, '+',
       'f LEFT ( x RIGHT )', 'NEARROW', '-1', 'NEARROW', '{37} over {12}', 'SEARROW', '1', 'NEARROW']
out, pos = [], 0
for m, s in zip(eqs, new):
    out.append(tbl[pos:m.start()])
    if s is not None:
        e = m.group(0); sm = H.SC.search(e)
        out.append(e[:sm.start(2)] + html.escape(s, quote=False) + e[sm.end(2):])
    pos = m.end()
out.append(tbl[pos:])
x = x[:t0] + ''.join(out) + x[t1:]
H.save(P, x)
ed = Ed(P)
E, T, SA, op = ed.E, ed.T, ed.SA, ed.op
E(55, 'sol', 'f LEFT ( x RIGHT ) {cases{x&', sub='f LEFT ( x RIGHT ) = {cases{x&')
for n, v, m, end in [(13, '26', '①', '합은?'), (14, '- {19} over {4}', '⑤', '값은?'), (16, '9', '④', '값은?'), (21, '5', '③', '합은?'), (27, '7', '③', '값은?'),
                     (30, '-3', '②', '최댓값은?'), (32, '3', '②', '값은?'), (36, '10', '⑤', '극댓값은?'), (40, '11', '③', '개수는?'), (51, '3', '⑤', '값은?'),
                     (53, '2', '④', '합은?'), (55, '{49} over {12}', '③', '값은?'), (61, '7', '①', '값은?')]:
    ne = end.replace('값은?', '값을 구하시오.') if end.endswith('값은?') else end[:-2] + ('를 구하시오.' if end in ('개수는?',) else '을 구하시오.')
    SA(n, v, m, ending=end, new_ending=ne)
op({'op': 'del_para', 'n': 10, 'part': 'sol', 'anchor': '^그래프는 ⟦x=3⟧에서'})
E(18, 'sol', "f`'(t)=it-3t^{2}+3=it-3", "f`'(t)=it-3t^{2}+3")
E(18, 'sol', '{x}', '{t}'); E(18, 'sol', '{f` prime (x)}', '{f` prime (t)}'); E(18, 'sol', '{f(x)}', '{f(t)}')
E(19, 'sol', "S``'(t)=0`", "S`'(t)=0`")
E(21, 'sol', 'g LEFT ( t RIGHT ) = it-2t  ^{3} +t  ^{2} +2', sub='g LEFT ( t RIGHT ) = it-2t  ^{3} +3t  ^{2} +2')
op({'op': 'eq', 'n': 21, 'part': 'sol', 'old': '+', 'new': '-', 'first': True})
E(21, 'sol', 'g LEFT ( x RIGHT )', 'g LEFT ( t RIGHT )')
E(22, 'sol', 'P', 'rm P')
E(51, 'sol', "f`' LEFT ( x RIGHT ) 3x", sub="f`' LEFT ( x RIGHT ) =3x")
T(59, 'q', '어두운 부분', '색칠한 부분')
E(61, 'sol', '=LEFT ( 2- {2} over {3} a^{2}  RIGHT )LEFT', sub='=LEFT ( 2- {2} over {3} a RIGHT )^{2} LEFT')
T(63, 'sol', '일 대 ', '일 때 ')
ed.run('u_mM/mM_05_edit.json')
