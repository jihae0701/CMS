# -*- coding: utf-8 -*-
"""대수 C 4단원(로그함수) 내용 고치기"""
import sys
sys.path.insert(0, '.')
from mjedit import Ed
ed = Ed(sys.argv[1] if len(sys.argv) > 1 else 'u_dC/dC_04.hwpx')
E, T, SA, op, SPLIT = ed.E, ed.T, ed.SA, ed.op, ed.SPLIT
def EQ(n, part, old, new, **k):
    d = {'op': 'eq', 'n': n, 'part': part, 'old': old, 'new': new}; d.update(k); op(d)
def ANS(n, old, val):   # 정답 줄 ' [정답] ⑤' → ' [정답] ⟦val⟧'
    op({'op': 'text_eq', 'n': n, 'part': 'sol', 'old': old, 'pre': ' [정답] ', 'eq': val, 'post': ''})
# 3: 조건제시법(조건 속 한글 분리 꼴 맞춤)
EQ(3, 'sol', 'left{x`|`x>0', 'LEFT { x left| x>0', all=True)
EQ(3, 'sol', 'left{x`|`x ne 0', 'LEFT { x left| x neq 0')
EQ(3, 'sol', '`right}', 'it RIGHT }', all=True)
# 5: 정답 오류 2log5 2 → log5 2 (해설 계산과 맞춤)
EQ(5, 'sol', '2`log _{5} `2', 'log _{5} `2')
T(5, 'sol', '이 때 밑', '이때 밑', optional=True)
# 6, 52, 60: 정답 줄
ANS(6, ' [정답] ⑤', '2'); ANS(52, ' [정답] ①', '1'); ANS(60, ' [정답] 1', '1')
# 11
EQ(11, 'q', 'RMCE', 'bar{rm CE}'); EQ(11, 'sol', '{rmbarCE}=1', 'bar{rm CE} =1')
T(11, 'q', '점  ', '점 ', optional=True)
# 12, 15, 42, 47, 62: 집합 표기
EQ(12, 'sol', 'left{x  left| x>it-1 right', 'LEFT { x left| x> it-1 RIGHT }'); EQ(12, 'sol', 'left{x  left| x >0 right', 'LEFT { x left| x>0 RIGHT }')
EQ(15, 'q', 'LEFT { x`|`x> it-3 RIGHT }', 'LEFT { x left| x> it-3 RIGHT }'); EQ(15, 'sol', 'LEFT { x``|``x> it-3 RIGHT }', 'LEFT { x left| x> it-3 RIGHT }')
EQ(42, 'q', 'left{x` left|`1 le x le 81 right}', 'LEFT { x left| 1 LEQ x LEQ 81 RIGHT }')
EQ(47, 'q', 'left{x  left |2 le x le 6 right}', 'LEFT { x left| 2 LEQ x LEQ 6 RIGHT }')
EQ(62, 'q', 'left{ x  left  |   x<2 right}', 'LEFT { x left| x<2 RIGHT }')
# 13, 17: 깨진 중괄호
EQ(13, 'sol', '= it-log  _{2} `left-(x-3) right}+4', '= it-log  _{2} ` LEFT { -(x-3) RIGHT } +4')
T(13, 'sol', '대칭이동 한', '대칭이동한', optional=True); T(13, 'sol', '이 때, ', '이때, ', optional=True)
# 15 ㄱ: 해설 주어 바로잡기
EQ(15, 'sol', 'y=log _{3} ` {x+3} over {9}', 'y=log _{3} `x', last=True)
T(15, 'sol', 'ㄱ. ', 'ㄱ. 주어진 함수의 그래프는 ', optional=False)
EQ(16, 'q', 'y=2\t`log _{2} `x', 'y=2`log _{2} `x')
EQ(19, 'q', 'y=   g( it x)', 'y=g(x)'); EQ(19, 'q', 'g(it5)', 'g(5)')
# 20 ⑴: 정의역 1/2≤x≤4에서 log(2-x)가 정의되지 않고 해설이 9번 것 → 정의역 0≤x≤1(정답 최댓값 2, 최솟값 1 그대로), 해설 새로
op({'op': 'del_eq', 'n': 20, 'part': 'q', 'old': 'LEFT ( pile{ it # it}'})
op({'op': 'del_eq', 'n': 20, 'part': 'q', 'old': 'pile{ `# `} RIGHT )'})
EQ(20, 'q', '{1} over {2} le x le 4', '(0 le x le 1)')
op({'op': 'del_para', 'n': 20, 'part': 'sol', 'anchor': '1 over 100'})
op({'op': 'del_para', 'n': 20, 'part': 'sol', 'anchor': '1000=3'})
op({'op': 'add_para', 'n': 20, 'part': 'sol', 'after': '[정답]', 'text': '⑴ 밑 ⟦{1} over {2}⟧가 ⟦0< {1} over {2} <1⟧이고 ⟦x⟧의 값이 증가하면 진수 ⟦2-x⟧는 감소하므로 ⟦y⟧의 값은 증가한다.⏎⟦x=1⟧일 때 ⟦y=log _{{1} over {2}} `1+2=2⟧, ⟦x=0⟧일 때 ⟦y=log _{{1} over {2}} `2+2=1⟧이므로 최댓값은 ⟦2⟧, 최솟값은 ⟦1⟧이다.'})
for n in (21, 23):
    T(n, 'sol', '서로 바꾸면 구하면', '서로 바꾸면 구하는', all=True)
T(22, 'sol', '만나는 점을 ', '만나는 점 ', optional=True); T(25, 'sol', '만나는 점을 ', '만나는 점 ', optional=True)
T(25, 'sol', '사각형 ', '사각형 ', optional=True)
EQ(23, 'sol', 'x-1   = log_3  `(y -2)', 'x-1 =log `(y-2)')
EQ(23, 'sol', 'therefore```` x= it- log(y +1) +3  =log_{ {1} over {2} } ``(y+1) +3', 'therefore```` x= it-log _{2} `(y+1)+3 =log_{ {1} over {2} } ``(y+1) +3')
# 26: 사용할 수 없는 글자(평행 기호), 선분 표기, 사각형 이름
EQ(26, 'sol', 'rmbarAC `\U000f005a`barBD  ,```` barAB = bar CD', 'bar{rm AC} `//` bar{rm BD} ,~ bar{rm AB} = bar{rm CD}')
EQ(26, 'sol', 'rm bar OB ``:`` barOA  = 2``:``1', 'bar{rm OB} `:` bar{rm OA} =2`:`1')
EQ(26, 'sol', '2 log_ 2 \t\talpha  =  log_2 ``2 alpha  ,```` alpha^2  = 2 alpha,```` alpha ( alpha -2)=0', '2`log_2 `alpha = log_2 ``2 alpha ,~ alpha^2 = 2 alpha ,~ alpha ( alpha -2)=0')
EQ(26, 'sol', 'rmbarAB  = barCD', 'bar{rm AB} = bar{rm CD}')
T(26, 'sol', '사각형 ', '사각형 ', optional=True)
# 28: 짝 안 맞는 괄호
for part in ('q', 'sol'):
    EQ(28, part, 'LEFT ( log`  _{2} `x right)  ^{2} -4`log`  _{2} `x=12 RIGHT .', 'LEFT ( log`  _{2} `x RIGHT )  ^{2} -4`log`  _{2} `x=12')
EQ(34, 'sol', 'LEFT ( log`x right)  ^{2}  -3log`x+2=0', 'LEFT ( log`x RIGHT )  ^{2} -3log`x+2=0')
EQ(35, 'sol', 'x  ^{2} -x+2>0', 'x  ^{2} -x-2>0')
# 37: 문제 ⑵의 해설이 없고 정답·해설 ⑵가 문제 ⑶의 것 → ⑵ 해설 쓰고 번호 맞춤
SPLIT(37, 'sol', '  {1<x<3}', ['2<x LEQ 10', ' ⑶ ', '1<x<3'])
T(37, 'sol', '⑵ 진수의', '⑶ 진수의')
op({'op': 'add_para', 'n': 37, 'part': 'sol', 'after': '⑴ 진수의 조건에서', 'text': '⑵ 진수의 조건에서 ⟦x-2>0⟧, ⟦x+6>0⟧ ⟦therefore~⟧⟦x>2⟧ ⟦cdots cdots⟧㉠⏎⟦log _{2} `(x-2) LEQ log _{4} `(x+6)+1⟧에서 ⟦log _{2} `(x-2) LEQ {1} over {2} `log _{2} `(x+6)+1⟧⏎⟦2`log _{2} `(x-2) LEQ log _{2} `(x+6)+2⟧, ⟦log _{2} `(x-2) ^{2} LEQ log _{2} `4(x+6)⟧⏎이때, 밑 ⟦2⟧는 ⟦1⟧보다 크므로 ⟦(x-2) ^{2} LEQ 4(x+6)⟧⏎⟦x ^{2} -8x-20 LEQ 0⟧, ⟦(x+2)(x-10) LEQ 0⟧ ⟦therefore~⟧⟦-2 LEQ x LEQ 10⟧ ⟦cdots cdots⟧㉡⏎㉠, ㉡에서 ⟦2<x LEQ 10⟧'})
# 38: 해설 ⑵(2(log₃x)²−log₃x³+1≤0)에 해당하는 문제가 빠짐 → 문제 ⑵ 넣고 원래 ⑵를 ⑶으로
T(38, 'q', '⑵ ', '⑶ ')
op({'op': 'add_para', 'n': 38, 'part': 'q', 'after': '⟦LEFT ( log`x RIGHT )  ^{2} -2>log`x⟧', 'text': '⑵ ⟦2 LEFT ( log` _{3} `x RIGHT ) ^{2} -log` _{3} `x ^{3} +1 LEQ 0⟧'})
T(39, 'q', '다음 로그부등식을 풀어라.', '다음 부등식을 푸시오.')
EQ(39, 'q', '3`log` _{x} `10+log` _ `x>4', '3`log` _{x} `10+log`x>4')
EQ(45, 'sol', 'a+b  over 100 = 100+100 over 100 = 2', '{a+b} over {100} = {100+100} over {100} =2')
for o in ['y=4x^{2  —log_2``x}', '=log_2`` 4x^{2  —log_2``x}=log_2`` 4+log_2``x^{2 —log_2``x}']:
    EQ(46, 'sol', o, o.replace('  —', '-').replace(' —', '-'))
# 48: 정답 줄 오류(⑵ 최솟값 −5, ⑶ 최댓값 2, ⑷ 없음), 떠도는 ⑷
T(48, 'sol', ' ⑵ 최댓값: ', ' ⑵ 최솟값: ', exact=True)
EQ(48, 'sol', ' {2}', '-5'); EQ(48, 'sol', ' {-1}', '2')
op({'op': 'del_eq', 'n': 48, 'part': 'sol', 'old': '{-5}'})
T(48, 'sol', ' ⑷ 최솟값: ', '', exact=True)
op({'op': 'del_para', 'n': 48, 'part': 'sol', 'anchor': '⑷', 'exact': True})
E(49, 'sol', ' beta ` TIMES `log`` _{beta } ` alpha `=', sub=' beta `+`log`` _{beta } ` alpha `=')
# 56: 해설이 다른 문제 것 → 새로
op({'op': 'clear_sol', 'n': 56, 'part': 'sol'})
for t in ['⟦x>0⟧이므로 주어진 부등식의 양변에 밑이 ⟦3⟧인 로그를 취하면',
          '⟦log _{3} `x ^{log _{3} `x} GEQ log _{3} `ax ^{4}⟧, ⟦(log _{3} `x) ^{2} GEQ log _{3} `a+4`log _{3} `x⟧',
          '⟦log _{3} `x=t⟧로 놓으면 ⟦t⟧는 모든 실수이고 ⟦t ^{2} -4t-log _{3} `a GEQ 0⟧이 모든 실수 ⟦t⟧에 대하여 성립해야 한다.',
          '이차방정식 ⟦t ^{2} -4t-log _{3} `a=0⟧의 판별식을 ⟦D⟧라 하면',
          '⟦{D} over {4} =4+log _{3} `a LEQ 0⟧, ⟦log _{3} `a LEQ it-4⟧ ⟦therefore~⟧⟦0<a LEQ {1} over {81}⟧']:
    op({'op': 'add_para', 'n': 56, 'part': 'sol', 'text': t, 'like_n': 55, 'like': '주어진 식의 양변에'})
T(57, 'q', '모든 실수 ', '모든 양의 실수 ')
EQ(58, 'sol', '7=10`log` {B} over {A} ', '-7=10`log` {B} over {A}')
EQ(58, 'q', 'rm -7`(dB)\r\n', '-7`rm (dB)')
EQ(60, 'sol', '{1} over {3} + {2} over {3} =1', '= {1} over {3} + {2} over {3} =1')
# 62: 해설 번호·결론 오류
T(62, 'sol', '③ ', '⑤ ', optional=True)
T(62, 'sol', '옳지 않은 것은 ②, ⑤이다.', '옳지 않은 것은 ⑤이다.', optional=True)
EQ(65, 'sol', 'log`a`4= it-4', 'log _{a} `4= it-4')
EQ(66, 'sol', 'a=10,~b=8``', 'a=10,~b= it-8')
EQ(67, 'sol', '2  ^{log`2x} =3  ^{log3x}', '2  ^{log`2x} =3  ^{log`3x}')
EQ(67, 'sol', 'log2  ^{log2x} =log`3  ^{log3x}', 'log`2  ^{log`2x} =log`3  ^{log`3x}')
EQ(67, 'sol', '(log`2)  ^{2} +log`x  times log`2=(log`3)  ^{2} +log`x  times log3', '(log`2)  ^{2} +log`x  times log`2=(log`3)  ^{2} +log`x  times log`3')
T(69, 'sol', '크모로', '크므로')
op({'op': 'eq', 'n': 69, 'part': 'sol', 'old': 'x> it-1', 'new': 'x>1'})
T(69, 'sol', 'ㄱ, ㄴ 이다', 'ㄱ, ㄴ이다.', optional=True)
ed.run('u_dC/dC_04_edit.json')
print('miss', ed.miss)
