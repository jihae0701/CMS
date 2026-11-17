# -*- coding: utf-8 -*-
"""대수 C 10단원(수학적 귀납법) 내용 고치기"""
import sys, re
sys.path.insert(0, '.')
from mjedit import Ed
ed = Ed(sys.argv[1] if len(sys.argv) > 1 else 'u_dC/dC_10.hwpx')
E, T, SA, op, SPLIT = ed.E, ed.T, ed.SA, ed.op, ed.SPLIT
def EQ(n, part, old, new, **k):
    d = {'op': 'eq', 'n': n, 'part': part, 'old': old, 'new': new}; d.update(k); op(d)
def ANS(n, old, val, pre=' [정답] ', post=''):
    op({'op': 'text_eq', 'n': n, 'part': 'sol', 'old': old, 'pre': pre, 'eq': val, 'post': post})
for n in (1, 2, 3, 4):
    EQ(n, 'sol', 'left{a_n right', 'LEFT { a_n RIGHT }', all=True)
for n, o in [(20, '"{"a_n"}"'), (31, '"{"a_n"}"'), (34, '"{"a_n -3"}"')]:
    EQ(n, 'sol', o, o.replace('"{"', 'LEFT { ').replace('"}"', ' RIGHT }'))
EQ(2, 'sol', '3^10 ', '3^8')          # 정답 3^10 → 3^8 (해설)
T(4, 'sol', '첫째항이 ⟦3⟧', '첫째항이 ⟦1⟧', optional=True)
ed.T(4, 'sol', '공비가 ', '공비가 ', optional=True)
EQ(5, 'sol', 'a _{8} -a _{7} =3 ^{1} +5', 'a _{8} -a _{7} =3 ^{5}')
EQ(6, 'sol', '=1+2 {times{1 times (3^{n-1} -1)}} over {3-1} =3^{n-1}', '=1+2 times {3^{n-1} -1} over {3-1} =3^{n-1}')
# 8: 문제 a8=55 → 85 (해설·정답 5에 맞춤)
EQ(8, 'q', 'a_8 =55', 'a_8 =85')
EQ(8, 'sol', '=a_1 +(a_2 -a_1 {){2^{n-1} -1}} over {2-1}', '=a_1 +(a_2 -a_1 ) {2^{n-1} -1} over {2-1}')
EQ(9, 'q', 'a _{1} = 1 OVER4', 'a _{1} = {1} over {4}')
EQ(9, 'sol', '+', 'times', all=True)
EQ(10, 'sol', 'a_8 -1 = 1 times 3^r', 'a_8 -1 = 1 times 3^7')
EQ(11, 'sol', 'a _{7} = 3^5 cdota _{6}', 'a _{7} = 3^5 cdot a _{6}')
# 12 ⑵: a1=−2이면 모든 항이 −2 → 해설(첫째항 a1+2=1)에 맞춰 a1=−1, 답 3^6−2=727
EQ(12, 'q', 'a _{1} = it -2', 'a _{1} = it -1')
EQ(12, 'sol', 'a_7 = 3^6 +2 ', 'a_7 = 3^6 -2')
EQ(12, 'sol', '731', '727', all=True)
EQ(13, 'sol', '18 0 = 2^2 times 3^2 times 5', '180 = 2^2 times 3^2 times 5')
EQ(13, 'sol', '=4^2 times 3', '=4^2 times 3^2')
# 16: 해설이 다른 조건(3n) 것 → p(2^a·5^b), 정답 ④ → ⑤
op({'op': 'text', 'n': 16, 'part': 'sol', 'old': ' [정답] ④', 'new': ' [정답] ⑤'})
op({'op': 'clear_sol', 'n': 16, 'part': 'sol'})
for t in ['주어진 조건에 의하여 음이 아닌 정수 ⟦a⟧, ⟦b⟧에 대하여 ⟦p(2^a times 5^b )⟧는 참이다.',
          '① ⟦42=2 cdot 3 cdot 7⟧ ⏎② ⟦45=3^2 cdot 5⟧ ⏎③ ⟦66=2 cdot 3 cdot 11⟧ ⏎④ ⟦148=2^2 cdot 37⟧ ⏎⑤ ⟦200=2^3 cdot 5^2⟧',
          '따라서 반드시 참인 명제는 ⟦p(200)⟧이다.']:
    op({'op': 'add_para', 'n': 16, 'part': 'sol', 'text': t, 'like_n': 13, 'like': '이므로 ①'})
# 19: 문제는 합만 묻는데 정답이 ⑴ 5 ⑵ 180 → 180
op({'op': 'del_eq', 'n': 19, 'part': 'sol', 'old': '5'})
T(19, 'sol', ' [정답] ⑴ ', ' [정답] ', exact=True)
T(19, 'sol', '⑵ ', '', exact=True)
EQ(19, 'sol', 'sum_{k=1}^100 a_k =(a_1 +a_2 +a_3 +a_4 +a_5 )+`cdots`(a_96 +a_97 +a_98 +a_99 +a_100 )', 'sum_{k=1}^100 a_k =(a_1 +a_2 +a_3 +a_4 +a_5 )+`cdots`+(a_96 +a_97 +a_98 +a_99 +a_100 )')
EQ(22, 'sol', '3S  _{n+1} -S  _{`n+1} -2S  _{`n} =a  _{n}', '3S  _{n+1} -S  _{n+2} -2S  _{n} =a  _{n}')
EQ(24, 'sol', 'sum _{k=1`} ^{200}a_k  =0', 'sum _{k=1} ^{6} a_k =0')
T(25, 'sol', '번재', '번째')
for part in ('q', 'sol'):
    for s in sorted(set(q for q in ed.scripts(26, part) if 'rmg' in q)):
        EQ(26, part, s, s.replace('rmg', '`rm g'), all=True)
T(26, 'sol', '남깁니다.', '남긴다.')
ANS(30, ' [정답] ②', '{1} over {4}')
EQ(31, 'sol', 'a_3 = 2r^{n-1} =50', 'a_3 = 2r^{2} =50')
T(31, 'sol', '이 때, ', '이때, ', optional=True)
ANS(32, ' [정답] ⑤', '13', pre=' [정답] 제', post='항')
EQ(34, 'sol', 'therefore ~ matrix { a_{n+1} -3 = 2 (a_n -3 )}', 'therefore ~ a_{n+1} -3 = 2 (a_n -3 )')
# 36: 단답형
SA(36, '16', '③')
# 35: 문제 글 없이 미주만 있는 문단(해설은 6단원 43번 것) → 지움 (마지막에)
ed.run('u_dC/dC_10_edit.json')
print('miss', ed.miss)
