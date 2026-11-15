# -*- coding: utf-8 -*-
"""3단원(미분계수와 도함수) 오타·오류 고치기 + 단답형 바꾸기"""
import sys, json
from common_fix import *

SRC, OUT = sys.argv[1], sys.argv[2]
d = Doc(load(SRC))
ALL = [d.root]
E = d.endnote
P = d.problem_paras


def eq_set_contains(scope, q, where, kind_, contains, new, show, **kw):
    hits = [e for e in iter_scope(scope, 'equation', kw.get('problem_only', False))
            if contains in (e.find(HP + 'script').text or '')]
    assert len(hits) == 1, (contains, len(hits))
    set_script(hits[0], new)
    if kind_:
        log(q, where, kind_, show[0], show[1])


# ---------------------------------------------------------------- 개념
text_sub(ALL, '개념01', '개념(제목)', '오타', '평균변화울과 미분계수', '평균변화율과 미분계수', problem_only=True)
eq_set_contains(ALL, '개념03', '개념(소제목)', '수식 정리', 'cases{g(x) _{it}', 'f(x)= {cases{g(x)&(x LEQ a)#h(x)&(x`>a)}}',
                ('수식 안 "_{it}" 찌꺼기·"&&"', '정리'), problem_only=True)
text_sub(ALL, '개념03', '개념(소제목)', '문법', '에서 미분가능일 조건', '에서 미분가능할 조건', problem_only=True)
eq_fix(ALL, '개념03', '개념(ⅱ)', '수학 오류', 'lim _{x` -> `a} {{g(x)-f(a)} over {x-a}} = lim _{x` -> `a} {{h(x)-f(a)} over {x-a}}',
       'lim _{x` -> `a-} {{g(x)-f(a)} over {x-a}} = lim _{x` -> `a+} {{h(x)-f(a)} over {x-a}}',
       'lim_{x→a} (g(x)-f(a))/(x-a) = lim_{x→a} (h(x)-f(a))/(x-a)', '좌극한 x→a-, 우극한 x→a+로', problem_only=True)
text_sub(ALL, '개념04', '개념', '띄어쓰기', '미분한다하고', '미분한다고 하고', problem_only=True)

# ---------------------------------------------------------------- 문항
text_sub([E(5)], 5, '해설', '오타', '[다른  이]', '[다른 풀이]')

t6 = [t for t in iter_scope(P(6), 't', True) if t.text == '오' and t.getnext() is not None and t.getnext().tag == HP + 'pic']
assert len(t6) == 1
t6[0].text = ''
text_sub(P(6), 6, '문제', '그림 위치', '른쪽 그림은', '그림은', problem_only=True, quiet=True)
log(6, '문제', '그림 위치', '오른쪽 그림은', '그림은')

text_sub(P(7), 7, '문제', '그림 위치', '오른쪽 그림은', '그림은', problem_only=True)
text_sub([E(7)], 7, '해설', '띄어쓰기', '는 두 점', '는 두 점 ')
text_sub([E(7)], 7, '해설', '표현', '위의 그래프에서 ', '그래프에서 ', quiet=True)
text_sub([E(7)], 7, '해설', '표현', ' 이다', '이다.', quiet=True)
log(7, '해설', '문장부호', '위의 그래프에서 B<A<C 이다', '그래프에서 B<A<C이다.')

eq_fix([E(10)], 10, '해설⑴', '오타', '=f`prime LEFT ( 3 RIGHT ) times3=6', '=f`prime LEFT ( a RIGHT ) times3=6', "f'(3)×3", "f'(a)×3")

for old, new in [("= 1 over 12 f`'(2)= 1 over 2", "= 1 over 12 f`'(-2)= 1 over 2"), ("f`'(2)=6", "f`'(-2)=6"),
                 ("f(2)f`'(2)=18", "f(-2)f`'(-2)=18")]:
    eq_fix([E(12)], 12, '해설', '', old, new)
log(12, '해설', '오타', "f'(2), f(2) (세 곳)", "f'(-2), f(-2)")

eq_edit([E(14)], 14, '해설⑴', '오타', 'f LEFT ( 1+2h RIGHT ) -f LEFT ( a RIGHT )', 'f LEFT ( 1+2h RIGHT ) -f LEFT ( a RIGHT )',
        'f LEFT ( a+2h RIGHT ) -f LEFT ( a RIGHT )', show=('f(1+2h)-f(a)', 'f(a+2h)-f(a)'))

text_sub([E(17)], 17, '해설 ㄷ', '오타', '중ㅇ서 ', '중에서 ')
text_sub([E(17)], 17, '해설', '띄어쓰기', '옳은 것은ㄱ', '옳은 것은 ㄱ')

eq_fix([E(18)], 18, '해설⑵', '오타', 'lim _{ x->0} {`f(x) }=f(1)', 'lim _{ x->1} {`f(x) }=f(1)', 'lim_{x→0} f(x)=f(1)', 'lim_{x→1} f(x)=f(1)')

eq_edit([E(23)], 23, '해설⑵', '오타', 'f(x)=3x ^{ 3}+x+1', 'f(x)=3x ^{ 3}+x+1', 'f(x)=3x ^{ 2}+x+1', show=('f(x)=3x³+x+1', 'f(x)=3x²+x+1'))

text_sub([E(30)], 30, '정답', '표기', ' 답 ③', ' [정답] ③', quiet=True)
eq_fix([E(30)], 30, '해설 ㄷ', '수학 오류', 'h(0)=0', 'h(0)=3', 'h(0)=0', 'h(0)=3')
n30 = 0
for e in E(30).iter(HP + 'equation'):
    sc = e.find(HP + 'script').text or ''
    if '{x-4`|`x`|}' in sc:
        set_script(e, sc.replace('{x-4`|`x`|}', '{x  ^{2} -4`|`x`|}'))
        n30 += 1
assert n30 == 2
log(30, '해설 ㄷ', '오타', '{x-4|x|}/x (두 곳)', '{x²-4|x|}/x')

eq_fix([E(31)], 31, '해설 ㄷ', '오타', 'f(x)=t', "f prime (x)=t", 'f(x)=t로 놓으면', "f'(x)=t로 놓으면")
eq_fix([E(31)], 31, '해설 ㄷ', '수식 오류', 'lim _{x -> -1+} {f(f prime (x)} )= lim _{t->0-} {} f(t)=-1',
       'lim _{x -> -1+} f(f prime (x))= lim _{t->0-} {} f(t)=-1', "lim {f(f'(x)} ) (괄호 엉킴)", "lim f(f'(x))")
eq_fix(P(31), 31, '보기 ㄷ', '수식 오류', 'lim _{x -> -1+} {f(f prime (x)}) =0', 'lim _{x -> -1+} f(f prime (x)) =0',
       "lim {f(f'(x)}) (괄호 엉킴)", "lim f(f'(x))", problem_only=True)

eq_edit([E(32)], 32, '해설', '오타', 'lim _{x->+1}', 'lim _{x->+1}', 'lim _{x->1+}', show=('lim_{x→+1}', 'lim_{x→1+}'))

eq_fix([E(33)], 33, '해설(ⅱ)', '수학 오류', 'lim _{x->`-1+} {`f(x)} = lim _{x->`-1-} {`f(x)}',
       'lim _{x->`-1+} {`f prime (x)} = lim _{x->`-1-} {`f prime (x)}', "미분계수 비교인데 lim f(x)로 씀", "lim f'(x)")

eq_fix([E(43)], 43, '해설 [다른 풀이]', '계산 오류', 'THEREFORE a+b=20', 'THEREFORE a+b=-20', 'a+b=20', 'a+b=-20')

eq_fix([E(44)], 44, '해설', '수학 오류', '2x  ^{4} +px  ^{2} +qx+6=(x-1)Q(x)+5x-4',
       '2x  ^{4} +px  ^{2} +qx+6=(x-1)  ^{2} Q(x)+5x-4', '…=(x-1)Q(x)+5x-4', '…=(x-1)²Q(x)+5x-4')
text_sub([E(44)], 44, '해설', '오타', '에 대하며 미분하면', '에 대하여 미분하면')

text_sub(P(47), 47, '문제', '수학 오류', '실수 전체의 집합에서 연속인 함수 ', '실수 전체의 집합에서 미분가능한 함수 ', problem_only=True)
eq_edit([E(47)], 47, '해설', '오타', '(because~f(2)=3`,``f(4)-9)', 'f(4)-9', 'f(4)=9', show=('f(4)-9', 'f(4)=9'))

text_sub([E(48)], 48, '정답', '정답 오류', '[정답] ㄱ, ㄴ', '[정답] ㄱ, ㄷ', solution_only=True)
p48 = find_para(E(48), starts='ㄴ.')
add_paras(d, 48, p48, ["즉, $f'(1)=0$이므로 거짓"], tmpl_p=p48)
log(48, '해설 ㄴ', '풀이 보충', "계산만 있고 결론 없음", "즉, f'(1)=0이므로 거짓")

eq_edit([E(49)], 49, '해설', '오타', 'g(x)&= lim _{ x`->`1}', 'g(x)&=', 'g(1)&=', show=('g(x)= lim g(x)', 'g(1)= lim g(x)'))

text_sub(P(53), 53, '문제', '띄어쓰기', '이다. 함수', '이다. 함수 ', problem_only=True)

# ---------------------------------------------------------------- 단답형
V = [('값은?', '값을 구하시오.')]
SEL = [('옳은 것을 모두 고른 것은?', '옳은 것만을 있는 대로 고르시오.')]
SHORT = {
    6: ('ㄷ', SEL), 7: ('$B<A<C$', [('의 대소 관계로 알맞은 것은?', '의 대소 관계를 부등호로 나타내시오.')]),
    11: ('${1} over {2}$', V), 12: ('$18$', V), 15: ('$6$', V),
    16: ('㈎ $2$, ㈏ $4$', [('알맞은 것을 차례대로 나열한 것은?', '알맞은 수를 구하시오.')]),
    24: ('$24$', V), 25: ('$10$', V), 26: ('$6$', V), 27: ('${2} over {3}$', V), 28: ('$-2$', V), 29: ('$12$', V),
    30: ('ㄷ', [('미분가능하지 않은 것을 ', '미분가능하지 않은 것만을 '), ('에서 모두 고른 것은?', '에서 있는 대로 고르시오.')]),
    31: ('ㄴ', SEL), 33: ('$8$', V), 34: ('${1} over {3}$', V), 35: ('$1$', V), 36: ('$27$', V), 37: ('$20$', V),
    38: ('$5$', [('미분계수는?', '미분계수를 구하시오.')]), 39: ('$4$', V),
    42: ("$xf(x)+a$", [('다음 중 ', ''), ('와 같은 것은?', '를 구하시오.')]), 52: ('$-2$', V),
}
for k, (ans, subs) in SHORT.items():
    print('Q', k)
    to_short(d, k, ans, subs)

# 보기가 문제 문단 안에 줄바꿈으로 들어 있는 문항
p19 = [p for p in P(19) if '위의 증명에서' in own_text(p)][0]
truncate_after(p19, '위의 증명에서 ㈎, ㈏에 알맞은 것은?', '위의 증명에서 ㈎, ㈏에 알맞은 식을 구하시오.')
set_answer(d, 19, '㈎ $x^{n-1} +x^{n-2} a+x^{n-3} a^2 + CDOTS +a^{n-1}$, ㈏ $na^{n-1}$')
p45 = [p for p in P(45) if '의 값은?' in own_text(p)][0]
truncate_after(p45, '의 값은?', '의 값을 구하시오.')
set_answer(d, 45, '$-2$')

ul = {}
strip_bold_and_braces(d, ul)
nq = drop_quick_answers(d)
log('전체', '본문 끝', '삭제', f'빠른 정답 목록 {nq}줄', '삭제(정답은 각 해설 첫 줄에 있음)')

save(d.tree, OUT)
json.dump({'log': LOG, 'bold': sorted(map(str, ul['bold'])), 'brace': sorted(map(str, ul['brace']))},
          open(OUT + '.log.json', 'w'), ensure_ascii=False, indent=1)
print('ok', len(LOG))
