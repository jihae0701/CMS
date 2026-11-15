# -*- coding: utf-8 -*-
"""1단원(함수의 극한) 오타·오류 고치기 + 단답형 바꾸기"""
import sys, json
from common_fix import *

SRC, OUT = sys.argv[1], sys.argv[2]
d = Doc(load(SRC))
ALL = [d.root]
E = d.endnote
P = d.problem_paras

# ---------------------------------------------------------------- 개념
eq_fix(ALL, '개념01', '개념', '수학 오류', 'f(x)``->``a', 'f(x)``->``alpha', 'f(x)→a', 'f(x)→α', problem_only=True)
text_sub(ALL, '개념02', '개념', '문법', '같지 않는 경우', '같지 않은 경우', problem_only=True)
text_sub(ALL, '개념02', '개념', '표현', '극한 문제는 항상 ', '극한 문제는 ', problem_only=True)
text_sub(ALL, '개념04', '개념', '오타', '식의 정리한다', '식을 정리한다', problem_only=True)
text_sub(ALL, '개념05', '개념', '오타', '계산하다.', '계산한다.', problem_only=True)
text_sub(ALL, '개념05', '개념', '오타', '바뀌어', '바꾸어', problem_only=True)

# ---------------------------------------------------------------- 문항
text_sub([E(3)], 3, '해설⑶', '오타', '가까워진다..', '가까워진다.')

for p in [p for p in E(4).iter(HP + 'p') if own_text(p).lstrip().startswith('⑸')]:
    p.getparent().remove(p)
log(4, '해설', '오류', '문제에 없는 ⑸ 항목 두 개', '삭제(문제는 ⑴~⑷)')

eq_fix([E(9)], 9, '해설⑵', '오타', 'lim _{ x->1- } {left[2x-1right] }=2', 'lim _{ x->1- } {left[2x+1right] }=2',
       'lim[2x-1]', 'lim[2x+1]')
text_sub([E(9)], 9, '해설⑵', '오타', '(우극한값이므로', '(우극한값)이므로')

text_sub(P(10), 10, '문제', '문장 오류', '다음 중 극한값 중', '다음 극한값 중', problem_only=True)

eq_fix([E(11)], 11, '해설⑵', '수학 오류', 'lim_x->0{f(x)}=4', 'lim_x->0{h(x)}=4', 'lim f(x)=4', 'lim h(x)=4')
eq_fix([E(11)], 11, '해설⑵', '수학 오류', '=4lim_x->0{f(x)}-lim_x->0{g(x)}=4times2-4=4',
       '=4lim_x->0{f(x)}-lim_x->0{h(x)}=4times2-4=4', '4 lim f(x) − lim g(x)', '4 lim f(x) − lim h(x)')

eq_fix([E(16)], 16, '해설', '수식 오류',
       '= lim _{x -> 0} {} {LEFT { (1-x)-(1+x) RIGHT } ( sqrt {4+x} + sqrt {4-x} )} over {LEFT . LEFT {   (4+x)-(4-x) RIGHT } ( sqrt {1-x} + sqrt {1+x} )}',
       '= lim _{x -> 0} {} {LEFT { (1-x)-(1+x) RIGHT } ( sqrt {4+x} + sqrt {4-x} )} over {LEFT {   (4+x)-(4-x) RIGHT } ( sqrt {1-x} + sqrt {1+x} )}',
       '짝 없는 LEFT .', '삭제')
eq_fix([E(16)], 16, '해설', '수식 오류',
       '= lim _{x -> 0} {} left(- { sqrt {4+x} + sqrt {4-x} )} over  {( sqrt {1-x} + sqrt {1+x} )}right)=-2',
       '= lim _{x -> 0} {} {-( sqrt {4+x} + sqrt {4-x} )} over {sqrt {1-x} + sqrt {1+x}} =-2',
       '괄호가 엉킨 식', '-(√(4+x)+√(4-x))/(√(1-x)+√(1+x)) = -2')

eq_fix([E(17)], 17, '해설', '오타', 'lim _{x -> `1} {} {1} over {x-1} LEFT ( {x  ^{5`} `+5} over {x+1} -3 RIGHT )',
       'lim _{x -> `1} {} {1} over {x-1} LEFT ( {x  ^{2`} `+5} over {x+1} -3 RIGHT )', 'x⁵+5', 'x²+5')


def nth_text(scope, old, new, n):
    hits = [(el, w) for el, w in t_nodes(scope, solution_only=True) if old in ((el.text if w == 'text' else el.tail) or '')]
    el, w = hits[n]
    if w == 'text':
        el.text = el.text.replace(old, new)
    else:
        el.tail = el.tail.replace(old, new)


hits = [(el, w) for el, w in t_nodes([E(18)]) if '으로 나누면' in ((el.text if w == 'text' else el.tail) or '')]
assert len(hits) == 3
nth_text([E(18)], '으로 나누면', '로 나누면', 2)
log(18, '해설⑶', '조사', 'x으로 나누면', 'x로 나누면')

for old, new in [
        (' lim_{x rarrow inf} -2t over { sqrt { t^2 +1} -3t', 'lim _{t rarrow inf} {-2t} over {sqrt {t^2 +1} -3t}'),
        ('= lim_{x rarrow inf} {-2t(sqrt{t^2 +1} +3t ) } over { (sqrt {t^2 +1 }-3t ) ( sqrt {t^2 +1} +3t )',
         '= lim _{t rarrow inf} {-2t(sqrt{t^2 +1} +3t)} over {(sqrt {t^2 +1}-3t)(sqrt {t^2 +1} +3t)}'),
        ('{= lim _{x rarrow  INF } { -2t( sqrt {t ^{2} +1} +3t)} over {-8t ^{2} +1}',
         '= lim _{t rarrow INF } {-2t( sqrt {t ^{2} +1} +3t)} over {-8t ^{2} +1}'),
        (' lim_{x rarrow inf} {-2 left (sqrt{1+{1overt^2}}+3right) } over { -8 + {1overt^2 } ',
         '= lim _{t rarrow inf} {-2 left ( sqrt{1+{1 over t^2}}+3 right )} over {-8 + {1 over t^2}}'),
        ('= {-2(sqrt1+0 +3) }over {-8+0', '= {-2( sqrt {1+0} +3)} over {-8+0}')]:
    eq_fix([E(23)], 23, '해설', '', old, new)
log(23, '해설', '오류', 't로 치환했는데 lim 아래가 x→∞, 중간 "=" 빠짐, 괄호 누락', 'lim 아래를 t→∞로, "=" 넣고 괄호 정리')

eq_fix([E(24)], 24, '해설', '수학 오류', '= {2+3} over {2+2}  times {sqrt {1} + sqrt {2}} over {sqrt {1} + sqrt {2}}',
       '= {2+3} over {2+2}  times {sqrt {1} + sqrt {1}} over {sqrt {1} + sqrt {1}}', '(√1+√2)/(√1+√2)', '(√1+√1)/(√1+√1)')

eq_fix([E(27)], 27, '해설', '오타',
       '{5x  ^{3} -x  ^{2} -3x-2} over {x  ^{3} +5} < {f(x)+2x+1} over {x  ^{3} +5} < {5x  ^{3} +x  ^{2} +x+4} over {x  ^{3} +5}',
       '{5x  ^{3} -x  ^{2} +3x-2} over {x  ^{3} +5} < {f(x)+2x+1} over {x  ^{3} +5} < {5x  ^{3} +x  ^{2} +x+4} over {x  ^{3} +5}',
       '5x³-x²-3x-2', '5x³-x²+3x-2')

p30 = find_para(E(30), starts='⑶')
replace_para(d, 30, p30, ['⑶ $0<x<3$일 때 $f(x)=3$이므로|$lim _{ x->0+ } {g(f(x)) }=g(3)=3$'])
log(30, '해설⑶', '수학 오류', 'g(x)=t로 치환, x→0+일 때 t→3', 'x→0+일 때 f(x)=3(일정)이므로 g(f(x))=g(3)=3')

# 33번 해설: 둘째 항목은 ㄴ, ㄴ·ㄷ 결론 보충
p33b = find_para(E(33), contains='3t+1')
text_sub([p33b], 33, '해설', '번호 오류', 'ㄷ. ', 'ㄴ. ')
add_paras(d, 33, p33b, ['따라서 거짓'], tmpl_p=p33b)
p33c = find_para(E(33), contains='2t+1')
replace_para(d, 33, p33c, [
    'ㄷ. $x -> - INF$일 때 ${2x+1} over {2x} =1+ {1} over {2x} -> 1-$이므로',
    '$lim _{x -> - INF } {f LEFT ( {2x+1} over {2x} RIGHT )} = lim _{t -> 1-} f(t)=1$',
    '따라서 참',
    '그러므로 옳은 것은 ㄱ, ㄷ이다.'])
log(33, '해설', '풀이 보충', 'ㄴ·ㄷ의 참/거짓 결론과 ㄷ 풀이 없음', 'ㄴ 거짓, ㄷ 풀이(x→-∞일 때 (2x+1)/(2x)→1-)·참, 결론 추가')
text_sub(P(33), 33, '문제', '그림 위치', '오른쪽 그림', '그림', problem_only=True)

eq_fix([E(37)], 37, '해설', '계산 오류', '=18cdot {1} over {6} =2', '=18cdot {1} over {6} =3', '18·1/6 = 2', '18·1/6 = 3')

text_sub(P(39), 39, '문제', '표현', '만족할 때', '만족시킬 때', problem_only=True)
eq_edit([E(39)], 39, '해설', '수학 오류', '{h LEFT ( x RIGHT )} over {g LEFT ( x RIGHT )} =0',
        'over {g LEFT ( x RIGHT )} =0', 'over {f LEFT ( x RIGHT )} =0', show=('lim h(x)/g(x)=0', 'lim h(x)/f(x)=0'))

text_sub([E(41)], 41, '해설', '논리 오류', '일 때, (분자)', '일 때, (분모)', quiet=True)
text_sub([E(41)], 41, '해설', '논리 오류', '존재하므로 (분모)', '존재하므로 (분자)', quiet=True)
log(41, '해설', '논리 오류', '(분자)→0이고 … (분모)→0이어야 한다', '(분모)→0이고 … (분자)→0이어야 한다')

p43 = E(43).findall('.//' + HP + 'p')[-1]
assert own_text(p43).strip() == ''
replace_para(d, 43, p43, [
    '$lim _{x->inf} ( sqrt {x^2 +ax} - sqrt {x^2 -ax} )$',
    '$= lim _{x->inf} {2ax} over {sqrt {x^2 +ax} + sqrt {x^2 -ax}}$',
    '$= lim _{x->inf} {2a} over {sqrt {1+ {a} over {x}} + sqrt {1- {a} over {x}}} = {2a} over {2} =a$',
    '따라서 $a=5$'])
log(43, '해설', '풀이 없음', '(빈칸)', '분자 유리화 → 극한값 a → a=5 풀이 추가')

text_sub([E(44)], 44, '해설', '논리 보완', '이므로 (분모)', '이고, 0이 아닌 극한값이 존재하므로 (분모)')

text_sub(P(48), 48, '문제', '띄어쓰기', '다항함수', '다항함수 ', problem_only=True)

eq_fix([E(51)], 51, '해설 ㄱ', '', 'lim _{x -> a} {} f(x)', 'lim _{x -> 0} {} f(x)', n=0)
eq_fix([E(51)], 51, '해설 ㄱ', '', 'lim _{x -> a} {}', 'lim _{x -> 0} {}')
eq_fix([E(51)], 51, '해설 ㄱ', '', 'lim _{x->`a} {`left{f(x)+g(x)right}=0}', 'lim _{x->`0} {`left{f(x)+g(x)right}=0}', solution_only=True)
eq_fix([E(51)], 51, '해설 ㄱ', '', 'lim _{x->`a} {`left{f(x)+g(x)right}}', 'lim _{x->`0} {`left{f(x)+g(x)right}}', solution_only=True)
log(51, '해설 ㄱ', '수학 오류', '반례가 x→0인데 lim 아래를 x→a로 씀', 'x→0')
eq_fix([E(51)], 51, '해설 ㄷ', '수식 오류', '`f(x)=`h(x)+k(x) over  2', '`f(x)=` {h(x)+k(x)} over  2',
       'f(x)=h(x)+k(x) over 2 (등식 전체가 분자로 보임)', 'f(x) = {h(x)+k(x)}/2')

# ---------------------------------------------------------------- 단답형
SHORT = {
    6: ('$4$', [('값은?', '값을 구하시오.')]),
    7: ('$-2$', [('값은?', '값을 구하시오.')]),
    15: ('$32$', [('값은?', '값을 구하시오.')]),
    16: ('$-2$', [('값은?', '값을 구하시오.')]),
    17: ('$- {1} over {2}$', [('값은?', '값을 구하시오.')]),
    20: ('$1$', [('값은?', '값을 구하시오.')]),
    21: ('$2$', [('값은?', '값을 구하시오.')]),
    22: ('$-1$', [('값은?', '값을 구하시오.')]),
    23: ('$1$', [('값은?', '값을 구하시오.')]),
    24: ('${5} over {4}$', [('값은?', '값을 구하시오.')]),
    28: ('$4$', [('값은?', '값을 구하시오.')]),
    29: ('$-2$', [('값은?', '값을 구하시오.')]),
    31: ('$5$', [('값은?', '값을 구하시오.')]),
    32: ('ㄱ, ㄴ', [('옳은 것을 모두 고른 것은?', '옳은 것만을 있는 대로 고르시오.')]),
    33: ('ㄱ, ㄷ', [('있는 대로 고른 것은?', '있는 대로 고르시오.')]),
    36: ('$- {5} over {2}$', [('값은?', '값을 구하시오.')]),
    37: ('$3$', [('값은?', '값을 구하시오.')]),
    38: ('$-1$', [('값은?', '값을 구하시오.')]),
    39: ('$7$', [('값은?', '값을 구하시오.')]),
    42: ('$12$', [('값은?', '값을 구하시오.')]),
    44: ('$-4$', [('값은?', '값을 구하시오.')]),
    45: ('${1} over {4}$', [('값은?', '값을 구하시오.')]),
    46: ('$64$', [('값은?', '값을 구하시오.')]),
    47: ('$9$', [('값은?', '값을 구하시오.')]),
    51: ('ㄷ', [('옳은 것을 모두 고른 것은?', '옳은 것만을 있는 대로 고르시오.')]),
    53: ('$2$', [(' 값', ' 값'), ('은?', '을 구하시오.')]),
    55: ('$10$', [('값은?', '값을 구하시오.')]),
}
for k, (ans, subs) in SHORT.items():
    print("Q",k); to_short(d, k, ans, subs)

# ---------------------------------------------------------------- 전체
ul = {}
strip_bold_and_braces(d, ul)
nq = drop_quick_answers(d)
log('전체', '본문 끝', '삭제', f'빠른 정답 목록 {nq}줄', '삭제(정답은 각 해설 첫 줄에 있음)')

save(d.tree, OUT)
json.dump({'log': LOG, 'bold': sorted(map(str, ul['bold'])), 'brace': sorted(map(str, ul['brace']))},
          open(OUT + '.log.json', 'w'), ensure_ascii=False, indent=1)
print('ok', len(LOG))
