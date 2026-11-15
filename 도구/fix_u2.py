# -*- coding: utf-8 -*-
"""2단원(함수의 연속) 오타·오류 고치기 + 단답형 바꾸기"""
import sys, json
from common_fix import *

SRC, OUT = sys.argv[1], sys.argv[2]
d = Doc(load(SRC))
ALL = [d.root]
E = d.endnote
P = d.problem_paras

# ---------------------------------------------------------------- 개념
text_sub(ALL, '개념01', '개념', '띄어쓰기', '    되어있고 즉 ', '    되어 있고, 즉 ', problem_only=True)
text_sub(ALL, '개념04', '개념(제목)', '맞춤법', '최대⦁최소의 정리 및 사이값 정리', '최대·최소의 정리 및 사잇값 정리', problem_only=True)
text_sub(ALL, '개념04', '개념', '맞춤법', '사이값의 정리', '사잇값의 정리', count=3, problem_only=True)

# ---------------------------------------------------------------- 문항
eq_fix([E(1)], 1, '해설⑵', '오타', 'lim _{x -> 0-} {`f LEFT ( x RIGHT )} = lim _{x -> 0+} {`x} =0',
       'lim _{x -> 0-} {`f LEFT ( x RIGHT )} = lim _{x -> 0-} {`x} =0', 'lim_{x→0-} f(x) = lim_{x→0+} x', 'lim_{x→0-} x')

text_sub(P(2), 2, '문제', '오타', '이다. 이때, ', '개이다. 이때, ', problem_only=True)

e3 = eq_find([E(3)], 'lim_x→0+')
t3 = e3.getnext()
assert t3.tag == HP + 't' and t3.text == 'g'
e3.getparent().remove(e3)
t3.getparent().remove(t3)
log(3, '해설 ㄴ', '오타', '수식 앞에 겹쳐 들어간 "lim_{x→0+} g"', '삭제')

text_sub([E(5)], 5, '해설', '표현', 'ㄷ도 옳다.', 'ㄷ은 옳다.')

eq_fix([E(6)], 6, '해설⑴', '', 'lim _{x -> 1} {` {x ^{2} +ax-6} over {x-2} =b}', 'lim _{x -> 2} {` {x ^{2} +ax-6} over {x-2} =b}')
eq_fix([E(6)], 6, '해설⑴', '', '= lim _{x -> 1} {` LEFT ( x+3 RIGHT )} =5', '= lim _{x -> 2} {` LEFT ( x+3 RIGHT )} =5')
log(6, '해설⑴', '오타', 'lim_{x→1} (두 곳)', 'lim_{x→2}')

eq_fix([E(7)], 7, '해설', '계산 오류',
       '= lim _{x -> 2} {` {x ^{2} -x+2} over {LEFT ( x-2 RIGHT ) LEFT ( sqrt {x ^{2} -x+2} +2 RIGHT )}}',
       '= lim _{x -> 2} {` {x ^{2} -x-2} over {LEFT ( x-2 RIGHT ) LEFT ( sqrt {x ^{2} -x+2} +2 RIGHT )}}',
       '유리화한 분자 x²-x+2', 'x²-x-2')

eq_fix([E(8)], 8, '해설', '', 'a left { (x+6) - 9 right} } over { (x-3) ( root { x+6 } + 3 ) ',
       '{a left { (x+6) - 9 right }} over {(x-3) ( root { x+6 } + 3 )}')
eq_fix([E(8)], 8, '해설', '', 'a(x-3) over { (x-3) ( root { x+6 } + 3 ) ', '{a(x-3)} over {(x-3) ( root { x+6 } + 3 )}')
log(8, '해설', '수식 오류', '분자 여는 괄호·분모 닫는 괄호 누락', '괄호 짝 맞춤')

hits = [t for t in E(15).iter(HP + 't') if (t.text or '').endswith('에서 불연속이다')]
assert len(hits) == 1
hits[0].text += '.'
log(15, '해설 ㄴ', '문장부호', '불연속이다', '불연속이다.')

# 16번 해설 없음 -> 풀이
tmpl16, _, _ = note_templates(E(15))
add_paras(d, 16, E(16).findall('.//' + HP + 'p')[0], [
    '① $2f(x)+g(x)=x^2 -x+4$는 다항함수이므로 구간 $(-inf,~inf)$에서 연속이다.',
    '② $f(x)g(x)$는 다항함수이므로 구간 $(-inf,~inf)$에서 연속이다.',
    '③ $g(x)=(x-1)(x-2)$이므로 ${f(x)} over {g(x)}$는 $x=1$, $x=2$에서 정의되지 않는다.|따라서 구간 $(-inf,~1)$, $(1,~2)$, $(2,~inf)$에서 연속이다.',
    '④ $(f circ g)(x)=g(x)+1=x^2 -3x+3= LEFT ( x- {3} over {2} RIGHT ) ^{2} + {3} over {4} >0$이므로|$1 over {(f circ g)(x)}$는 구간 $(-inf,~inf)$에서 연속이다.',
    '⑤ $(g circ f)(x)=(x+1)^2 -3(x+1)+2=x(x-1)$이므로 $1 over {(g circ f)(x)}$는 $x=0$, $x=1$에서 정의되지 않는다.|따라서 구간 $(-inf,~0)$, $(0,~1)$, $(1,~inf)$에서 연속이다.',
    '따라서 잘못 나타낸 것은 ⑤이다.'], tmpl_p=tmpl16, cp=note_templates(E(15))[1])
log(16, '해설', '풀이 없음', '(정답만 있음)', '①~⑤ 각각의 연속 구간 풀이 추가')

eq_fix([E(17)], 17, '해설', '수식 오류', '-3+-{root5}}over2', '{-3 +- root 5} over 2', '-3±{√5}}/2 (괄호 엉킴)', '(-3±√5)/2')

tbl = E(18).find('.//' + HP + 'tbl')
rows = tbl.findall(HP + 'tr')
cells = rows[3].findall(HP + 'tc')
assert own_text(cells[0].find('.//' + HP + 'p')).strip() == '⟦x=1⟧', own_text(cells[0].find('.//' + HP + 'p'))
g1 = cells[2].find('.//' + HP + 'equation')
assert g1.find(HP + 'script').text.strip() == '1'
set_script(g1, '-1')
log(18, '해설 [다른 풀이] 표', '오타', 'x=1일 때 g(1)=1', 'g(1)=-1 (본풀이·합·몫과 맞춤)')

eq_fix([E(21)], 21, '해설⑴', '오타', 'f LEFT ( x RIGHT ) =x ^{2} +2x-5', 'f LEFT ( x RIGHT ) =x ^{3} +2x-5', 'f(x)=x²+2x-5', 'f(x)=x³+2x-5')

eq_fix(P(23), 23, '문제', '수학 오류', '[3,~5]', '[-2,~3]', '구간 [3, 5]', '구간 [-2, 3] (그림·보기와 맞춤)', problem_only=True)
text_sub(P(23), 23, '문제', '그림 위치', '오른쪽 그림', '그림', problem_only=True)
text_sub(P(4), 4, '문제', '그림 위치', '오른쪽 그림', '그림', problem_only=True)
text_sub(P(5), 5, '문제', '그림 위치', '오른쪽 그림', '그림', problem_only=True)
text_sub(P(35), 35, '문제', '그림 위치', '오른쪽 그림', '그림', problem_only=True)

text_sub(P(26), 26, '문제', '띄어쓰기', '닫힌 구간', '닫힌구간', problem_only=True)
text_sub(P(26), 26, '문제', '표현', '만족할 때', '만족시킬 때', problem_only=True)

eq_fix([E(33)], 33, '해설 ㄴ', '오타',
       'lim _{x -> 0} {`f LEFT ( g LEFT ( x RIGHT ) RIGHT ) =f LEFT ( g LEFT ( a RIGHT ) RIGHT ) =0}',
       'lim _{x -> 0} {`f LEFT ( g LEFT ( x RIGHT ) RIGHT ) =f LEFT ( g LEFT ( 0 RIGHT ) RIGHT ) =0}', 'f(g(a))', 'f(g(0))')

eq_fix(P(34), 34, '문제', '수식 정리', 'f(x) = cases {```~ x^2  -2x -1_{it} &(x `<1)_{it} # -x^2 +2x +1 ~&(x ge1 )',
       'f(x) = cases {```~ x^2  -2x -1 &(x `<1) # -x^2 +2x +1 ~&(x ge1 )}', '수식 안 "_{it}" 찌꺼기, cases 닫는 괄호 누락', '정리',
       problem_only=True)
text_sub(P(34), 34, '문제', '조사', '의 불연속인', '가 불연속인', problem_only=True)
add_paras(d, 34, E(34).findall('.//' + HP + 'p')[0], [
    '$x<1$일 때 $f(x)=(x-1)^2 -2$, $x GEQ 1$일 때 $f(x)=-(x-1)^2 +2$이고',
    '$lim _{x -> 1-} f(x)=-2$, $f(1)=2$이므로 $f(x)$는 $x=1$에서만 불연속이다.',
    '따라서 $(f circ f)(x)$는 $x=1$ 또는 $f(x)=1$인 $x$에서 불연속일 수 있다.',
    '(ⅰ) $x=1$일 때|$lim _{x -> 1-} f(f(x))=f(-2)=7$, $lim _{x -> 1+} f(f(x))=f(2)=1$이므로 불연속이다.',
    '(ⅱ) $f(x)=1$인 $x$는 $x=1- sqrt {3}$, $x=2$이고, 두 점에서 $f(x)$는 감소하면서 $1$을 지난다.|$f(x)$가 $1$보다 큰 쪽에서 $1$에 가까워지면 $f(f(x)) -> 2$, 작은 쪽에서 가까워지면 $f(f(x)) -> -2$이므로 두 점에서 모두 불연속이다.',
    '따라서 불연속인 $x$의 개수는 $3$이다.'], tmpl_p=tmpl16, cp=note_templates(E(15))[1])
log(34, '해설', '풀이 없음', '(정답만 있음)', 'x=1, x=1-√3, x=2에서 불연속 → 3개 풀이 추가')

eq_fix([E(40)], 40, '해설(ⅰ)', '오타', 'lim_n->inf x^n =lim_x->inf x^n+1 =0', 'lim_n->inf x^n =lim_n->inf x^n+1 =0',
       'lim_{x→∞} x^{n+1}', 'lim_{n→∞} x^{n+1}')
eq_edit([E(40)], 40, '해설(ⅲ)', '수식 오류', 'over {1+ {1} over {x}} =x', 'over {1+ {1} over {x}} =x', 'over {1+ {1} over {x ^{n}}} =x',
        show=('분모 1+1/x', '1+1/xⁿ'))

lb = [t for t in d.root.iter(HP + 't') if (t.text or '').endswith('에서 연속이') and len(t) and t[0].tag == HP + 'lineBreak'
      and (t[0].tail or '').startswith('다')]
assert len(lb) == 1
lb[0].text += lb[0][0].tail
lb[0].remove(lb[0][0])
log(42, '보기 ㄷ', '줄바꿈 오류', '연속이⏎다.', '연속이다.')

eq_fix(P(43), 43, '문제', '수식 정리', 'f(x)= {cases{``x+a~&(x GEQ 0)#x ^{2} +b~ _{it}&(x<`0)}}',
       'f(x)= {cases{``x+a~&(x GEQ 0)#x ^{2} +b~&(x<`0)}}', '수식 안 "_{it}" 찌꺼기', '삭제', problem_only=True)
p43 = find_para(E(43), contains='a=it-2')
replace_para(d, 43, p43, [
    '함수 $f(x)$는 $x=0$에서만 불연속일 수 있으므로 함수 $f(x)f(x-2)$는 $x=0$, $x=2$에서 연속이면 된다.',
    '(ⅰ) $x=0$에서|$lim _{x -> 0+} f(x)f(x-2)=a(4+b)$, $lim _{x -> 0-} f(x)f(x-2)=b(4+b)$, $f(0)f(-2)=a(4+b)$|이므로 $(a-b)(4+b)=0$에서 $a != b$이므로 $b=-4$',
    '(ⅱ) $x=2$에서|$lim _{x -> 2+} f(x)f(x-2)=(2+a)a$, $lim _{x -> 2-} f(x)f(x-2)=(2+a)b$, $f(2)f(0)=(2+a)a$|이므로 $(2+a)(a-b)=0$에서 $a != b$이므로 $a=-2$',
    '따라서 $a+b=-2+(-4)=-6$'], tmpl_p=tmpl16)
log(43, '정답', '정답 오류', '④ (-5)', '③ (-6) → 단답형 -6')
log(43, '해설', '풀이 없음', 'a=-2, b=-4만 있음', 'x=0, x=2에서의 연속 조건 풀이 추가')

text_sub([E(44)], 44, '해설 ㄷ', '표현', 'ㄷ도 옳다.', 'ㄷ은 옳다.')
text_sub([E(44)], 44, '해설 ㄷ', '논리·띄어쓰기', '에서 연속이어야한다.', '에서 연속인지만 조사하면 된다.')
eq_fix([E(44)], 44, '해설 ㄷ', '오타', 'y=(x-1) ', 'y=(x-1)f(x)', 'y=(x-1)는', 'y=(x-1)f(x)는')

eq_fix(P(46), 46, '문제', '수학 오류', 'g(x)= f(x-1)over{x^ 2 -1} ', 'g(x)= {f(x-1)} over {x^2 -1}~(x != 1)',
       'g(x)=f(x-1)/(x²-1) (x=1에서 정의 안 됨)', 'g(x)=f(x-1)/(x²-1) (x≠1) 조건 추가', problem_only=True)

eq_fix([E(48)], 48, '해설', '오타', ' lim_x→-inf =-inf', 'lim_x→-inf f(x)=-inf', 'lim_{x→-∞} = -∞', 'lim_{x→-∞} f(x) = -∞')

# ---------------------------------------------------------------- 단답형
V = [('값은?', '값을 구하시오.')]
SEL = [('옳은 것을 모두 고른 것은?', '옳은 것만을 있는 대로 고르시오.')]
SHORT = {
    2: ('$3$', V), 3: ('ㄱ, ㄴ', [('함수인 것을 ', '함수인 것만을 '), ('에서 모두 고른 것은?', '에서 있는 대로 고르시오.')]),
    4: ('ㄱ, ㄴ', SEL), 5: ('ㄱ, ㄷ', SEL), 8: ('$48$', V), 9: ('$2$', V), 10: ('$-4$', V), 12: ('${2} over {3}$', V),
    14: ('ㄱ', SEL), 17: ('$-6$', [('합은?', '합을 구하시오.')]), 23: ('ㄱ, ㄷ', SEL),
    24: ('㈎ 연속, ㈏ <, ㈐ 사잇값', [('알맞은 것은?', '알맞은 것을 쓰시오.')]),
    27: ('$3$', []), 32: ('ㄴ, ㄷ', SEL), 34: ('$3$', [('개수는?', '개수를 구하시오.')]), 35: ('$8$', V),
    36: ('$0$', V), 41: ('$5$', V), 43: ('$-6$', V), 44: ('ㄱ, ㄷ', SEL), 45: ('ㄱ', SEL),
}
for k, (ans, subs) in SHORT.items():
    print('Q', k)
    to_short(d, k, ans, subs)

ul = {}
strip_bold_and_braces(d, ul)
nq = drop_quick_answers(d)
assert nq == 0, nq

save(d.tree, OUT)
json.dump({'log': LOG, 'bold': sorted(map(str, ul['bold'])), 'brace': sorted(map(str, ul['brace']))},
          open(OUT + '.log.json', 'w'), ensure_ascii=False, indent=1)
print('ok', len(LOG))
