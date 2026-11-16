# -*- coding: utf-8 -*-
"""미적분Ⅰ 2단원(함수의 연속) 내용 고치기"""
import sys
sys.path.insert(0, '.')
from mjedit import Ed
ed = Ed('u_mj/m1_02.hwpx')
E, T, SA, op = ed.E, ed.T, ed.SA, ed.op
LIKE = {'like_n': 15, 'like': '따라서 실수 전체의 집합에서'}

# 단답형
SA(2, '3', '③'); SA(8, '48', '④'); SA(9, '2', '②'); SA(10, '-4', '①'); SA(12, '{2} over {3}', '③'); SA(17, '-6', '①')
SA(27, '3', '③', ending='적어도 몇 개의 실근을 갖는가?', new_ending='적어도 몇 개의 실근을 갖는지 구하시오.')
SA(34, '3', '③', ending='개수는?', new_ending='개수를 구하시오.', sol_old='[정답] ③')
SA(35, '8', '③'); SA(36, '0', '②'); SA(41, '5', '③')
SA(43, '-6', '④')   # 정답 오류: 해설 a=-2, b=-4 → -6

# 고치기
E(1, 'sol', '= lim _{x `->` 0+} {`x} =0', sub='= lim _{x `->` 0-} {`x} =0')
op({'op': 'del_eq', 'n': 3, 'part': 'sol', 'old': 'lim _{x `->` 0+}'})
T(3, 'sol', 'g', '', exact=True)
E(6, 'sol', 'lim _{x `->` 1} {` {x ^{2} +ax-6} over {x-2} =b}', sub='lim _{x `->` 2} {` {x ^{2} +ax-6} over {x-2} =b}')
E(6, 'sol', 'lim _{x `->` 1} {` LEFT ( x+3 RIGHT )}', sub='lim _{x `->` 2} {` LEFT ( x+3 RIGHT )}')
E(7, 'sol', '{` {x ^{2} -x+2} over {LEFT ( x-2', sub='{` {x ^{2} -x-2} over {LEFT ( x-2')
T(15, 'sol', '에서 불연속이다', '에서 불연속이다.', exact=True)
E(17, 'sol', 'root5', '{-3 PLUSMINUS sqrt {5}} over {2}')
E(21, 'sol', '=x ^{2} +2x-5', sub='=x ^{3} +2x-5')
T(26, 'q', '만족할 때', '만족시킬 때'); T(26, 'q', '닫힌 구간', '닫힌구간')
E(33, 'sol', 'g LEFT ( a RIGHT )', sub='g LEFT ( 0 RIGHT )')
E(40, 'sol', 'lim _{x `->` inf} x^n+1', sub='lim _{n `->` inf} x^n+1')
E(40, 'sol', 'over {1+ {1} over {x}} =x', sub='over {1+ {1} over {x ^{n}}} =x')
T(42, 'q', '연속이⏎다.', '연속이다.')
y = [s for s in ed.scripts(44, 'sol') if s.strip() == 'y=(x-1)']
if len(y) == 1:
    op({'op': 'eq', 'n': 44, 'part': 'sol', 'old': y[0], 'new': 'y=(x-1)f(x)'})
else:
    print('!! 44', y)
T(44, 'sol', '연속이어야한다.', '연속인지만 조사하면 된다.')
E(48, 'sol', 'lim _{x `->` -inf} = it-inf', 'lim _{x `->` -inf} f(x)= it-inf')

# 빠진 해설
def add(n, text):
    d = {'op': 'add_para', 'n': n, 'part': 'sol', 'text': text}; d.update(LIKE); op(d)

for t in ['⟦g(x)=x ^{2} -3x+2=(x-1)(x-2)⟧이므로',
          '① ⟦2f(x)+g(x)=x ^{2} -x+4⟧는 다항함수이므로 구간 ⟦(-inf,~inf)⟧에서 연속이다.',
          '② ⟦f(x)g(x)⟧는 다항함수이므로 구간 ⟦(-inf,~inf)⟧에서 연속이다.',
          '③ ⟦{f(x)} over {g(x)}⟧는 ⟦g(x)=0⟧, 즉 ⟦x=1⟧, ⟦x=2⟧에서 정의되지 않으므로 구간 ⟦(-inf,~1)⟧, ⟦(1,~2)⟧, ⟦(2,~inf)⟧에서 연속이다.',
          '④ ⟦(f CIRC g)(x)=g(x)+1=x ^{2} -3x+3= LEFT ( x- {3} over {2} RIGHT ) ^{2} + {3} over {4} >0⟧이므로 ⟦{1} over {(f CIRC g)(x)}⟧는 구간 ⟦(-inf,~inf)⟧에서 연속이다.',
          '⑤ ⟦(g CIRC f)(x)=(x+1) ^{2} -3(x+1)+2=x(x-1)⟧이므로 ⟦{1} over {(g CIRC f)(x)}⟧는 ⟦x=0⟧, ⟦x=1⟧에서 정의되지 않는다. 즉, 연속인 구간은 ⟦(-inf,~0)⟧, ⟦(0,~1)⟧, ⟦(1,~inf)⟧이다.',
          '따라서 잘못 나타낸 것은 ⑤이다.']:
    add(16, t)
for t in ['⟦x<1⟧일 때 ⟦f(x)=(x-1) ^{2} -2> it-2⟧, ⟦x GEQ 1⟧일 때 ⟦f(x)= it-(x-1) ^{2} +2 LEQ 2⟧이고, ⟦f(x)⟧는 ⟦x=1⟧에서만 불연속이다.',
          '따라서 ⟦(f CIRC f)(x)⟧는 ⟦x=1⟧ 또는 ⟦f(x)=1⟧인 ⟦x⟧에서 불연속일 수 있다.',
          '(ⅰ) ⟦x``->``1-⟧일 때 ⟦f(x)``->``-2+⟧이므로 ⟦lim _{x `->` 1-} f(f(x))=f(-2)=7⟧⏎⟦x``->``1+⟧일 때 ⟦f(x)``->``2-⟧이므로 ⟦lim _{x `->` 1+} f(f(x))=f(2)=1⟧⏎즉, ⟦x=1⟧에서 불연속이다.',
          '(ⅱ) ⟦f(x)=1⟧인 ⟦x⟧는 ⟦x ^{2} -2x-1=1~(x<1)⟧에서 ⟦x=1- sqrt {3}⟧, ⟦-x ^{2} +2x+1=1~(x GEQ 1)⟧에서 ⟦x=2⟧이다.⏎이 두 점의 좌우에서 ⟦f(x)⟧의 값은 ⟦1⟧보다 큰 값에서 작은 값으로 바뀌므로 ⟦f(f(x))⟧의 좌극한과 우극한은 각각 ⟦lim _{t `->` 1+} f(t)=2⟧, ⟦lim _{t `->` 1-} f(t)= it-2⟧가 되어 서로 다르다. 즉, ⟦x=1- sqrt {3}⟧, ⟦x=2⟧에서 불연속이다.',
          '따라서 ⟦(f CIRC f)(x)⟧가 불연속인 ⟦x⟧는 ⟦1- sqrt {3}⟧, ⟦1⟧, ⟦2⟧의 ⟦3⟧개이다.']:
    add(34, t)
op({'op': 'del_para', 'n': 43, 'part': 'sol', 'anchor': 'b=it-4'})
for t in ['⟦a != b⟧이므로 ⟦f(x)⟧는 ⟦x=0⟧에서만 불연속이고, ⟦f(x-2)⟧는 ⟦x=2⟧에서만 불연속이다. 따라서 ⟦f(x)f(x-2)⟧가 ⟦x=0⟧, ⟦x=2⟧에서 연속이면 된다.',
          '(ⅰ) ⟦x``->``0⟧일 때 ⟦f(x-2)``->``f(-2)=4+b⟧이므로⏎⟦lim _{x `->` 0+} f(x)f(x-2)=a(4+b)⟧, ⟦lim _{x `->` 0-} f(x)f(x-2)=b(4+b)⟧, ⟦f(0)f(-2)=a(4+b)⟧⏎⟦(a-b)(4+b)=0⟧이고 ⟦a != b⟧이므로 ⟦b= it-4⟧',
          '(ⅱ) ⟦x``->``2⟧일 때 ⟦f(x)``->``f(2)=2+a⟧이므로⏎⟦lim _{x `->` 2+} f(x)f(x-2)=(2+a)a⟧, ⟦lim _{x `->` 2-} f(x)f(x-2)=(2+a)b⟧, ⟦f(2)f(0)=(2+a)a⟧⏎⟦(2+a)(a-b)=0⟧이고 ⟦a != b⟧이므로 ⟦a= it-2⟧',
          '따라서 ⟦a+b=(-2)+(-4)= it-6⟧']:
    add(43, t)
ed.run('u_mj/m1_02_edit.json')
