# -*- coding: utf-8 -*-
"""미적분Ⅰ 1단원(함수의 극한) 내용 고치기 명령을 만든다: 수식은 '들어 있는 글'로 찾아 정확한 원래 스크립트로 바꿔 hwpxedit 명령으로 낸다."""
import sys, json, re, html
sys.path.insert(0, '.')
import hwpxedit as H
F = 'u_mj/m1_01.hwpx'
x = H.load(F)
def scripts(n, part):
    out = []
    for a, b in H.region(x, n, part):
        for m in H.EQ.finditer(x, a, b):
            sm = H.SC.search(m.group(0))
            out.append(html.unescape(sm.group(2)) if sm else '')
    return out
ops = []
def E(n, part, find, new, sub=None):
    """find가 든 수식 하나를 new로(sub가 있으면 그 수식 속 find→sub만 바꿈)"""
    c = [s for s in scripts(n, part) if find in s]
    if len(c) != 1:
        print('!! 수식 찾기', n, part, find, len(c)); return
    old = c[0]
    ops.append({'op': 'eq', 'n': n, 'part': part, 'old': old, 'new': old.replace(find, sub) if sub is not None else new})
def T(n, part, old, new, **k):
    d = {'op': 'text', 'n': n, 'part': part, 'old': old, 'new': new}; d.update(k); ops.append(d)

# ── 단답형으로 바꾸기: (문항, 정답 값, 원래 번호)
SA = [(6, '4', '④'), (7, '-2', '②'), (15, '32', '⑤'), (16, '-2', '②'), (17, '- {1} over {2}', '①'), (20, '1', '①'), (21, '2', '②'),
      (22, '-1', '②'), (23, '1', '④'), (24, '{5} over {4}', '④'), (28, '4', '③'), (29, '-2', '①'), (31, '5', '⑤'), (36, '- {5} over {2}', '①'),
      (37, '3', '③'), (38, '-1', '①'), (39, '7', '④'), (42, '12', '②'), (44, '-4', '②'), (45, '{1} over {4}', '④'), (46, '64', '⑤'),
      (47, '9', '②'), (53, '2', '②'), (55, '10', '⑤')]
for n, v, c in SA:
    if n == 53:
        T(n, 'q', '은?', '을 구하시오.')
    else:
        T(n, 'q', '값은?', '값을 구하시오.')
    ops.append({'op': 'del_para', 'n': n, 'part': 'q', 'anchor': '①'})
    ops.append({'op': 'del_para', 'n': n, 'part': 'q', 'anchor': '④', 'optional': True})
    ops.append({'op': 'text_eq', 'n': n, 'part': 'sol', 'old': ' [정답] ' + c, 'pre': ' [정답] ', 'eq': v, 'post': ''})

# ── 문제·해설 고치기
T(3, 'sol', '가까워진다..', '가까워진다.')
ops.append({'op': 'del_para', 'n': 4, 'part': 'sol', 'anchor': 'x-1``->``-2+'})
ops.append({'op': 'del_para', 'n': 4, 'part': 'sol', 'anchor': 'x+1``->``-1-'})
E(9, 'sol', 'left[2x-1right]', 'lim _{x `->` 1-} {left[2x+1right]} =2')
E(9, 'sol', 'left[2x+1right]=3 }', 'lim _{x `->` 1+} {left[2x+1right]} =3')
T(9, 'sol', '(우극한값이므로', '(우극한값)이므로')
T(10, 'q', '다음 중 극한값 중', '다음 극한값 중')
E(11, 'sol', '=3 lim _{x `->` 1} {f(x)+lim', 'lim _{x `->` 1} LEFT { 3f(x)+f(x)g(x) RIGHT } =3 lim _{x `->` 1} f(x)+ lim _{x `->` 1} f(x) times lim _{x `->` 1} g(x)')
E(11, 'sol', 'lim _{x `->` 0} {f(x)}=4', 'lim _{x `->` 0} h(x)=4')
E(11, 'sol', '=4 lim _{x `->` 0} {f(x)}-lim', '=4 lim _{x `->` 0} f(x)- lim _{x `->` 0} h(x)=4 times 2-4=4')
E(11, 'sol', '{2 lim _{x `->` 0} {f(x)+3', 'THEREFORE~ lim _{x `->` 0} {2f(x)+3g(x)} over {3f(x)-g(x)} = {2 lim _{x `->` 0} f(x)+3 lim _{x `->` 0} g(x)} over {3 lim _{x `->` 0} f(x)- lim _{x `->` 0} g(x)}')
E(12, 'q', '{f(x)=5}', 'lim _{x `->` a} f(x)=5')
E(12, 'q', 'left{2f(x)-3g(x)right}=4}', 'lim _{x `->` a} LEFT { 2f(x)-3g(x) RIGHT } =4')
E(12, 'q', '{`g(x)}', 'lim _{x `->` a} g(x)')
E(12, 'sol', '2 cdot 5-4', '= {2 times 5-4} over {3} =2')
E(16, 'sol', 'LEFT . LEFT {', None, sub='LEFT {')
E(16, 'sol', 'left(- {', '= lim _{x `->` 0} LEFT ( - {sqrt {4+x} + sqrt {4-x}} over {sqrt {1-x} + sqrt {1+x}} RIGHT ) = it-2')
E(17, 'sol', 'x ^{5}', 'lim _{x `->` 1} {1} over {x-1} LEFT ( {x ^{2} +5} over {x+1} -3 RIGHT )')
E(17, 'sol', '-3x+2} over {x+1} RIGHT )', '= lim _{x `->` 1} LEFT ( {1} over {x-1} times {x ^{2} -3x+2} over {x+1} RIGHT )')
E(17, 'sol', '(x-1)(x-2)} over {x+1} RIGHT }', '= lim _{x `->` 1} LEFT { {1} over {x-1} times {(x-1)(x-2)} over {x+1} RIGHT }')
E(18, 'sol', '{3+ {1} over {x^2}}', None, sub='{3+ {2} over {x^2}}')
T(18, 'sol', '으로 나누면', '로 나누면', after_eq='x')
E(24, 'sol', '{sqrt {1} + sqrt {2}} over {sqrt {1} + sqrt {2}}', None, sub='{sqrt {1} + sqrt {1}} over {sqrt {1} + sqrt {1}}')
E(26, 'sol', '{x^2 -3x-2} over {x^2} =lim', 'lim _{x `->` inf} {x^2 -3x-2} over {x^2} = lim _{x `->` inf} {x^2 -3x+1} over {x^2} =1')
E(27, 'sol', '-x  ^{2} -3x-2}', None, sub='-x  ^{2} +3x-2}')
E(29, 'sol', '=`-2', None, sub='= it-2')
ops.append({'op': 'eq', 'n': 30, 'part': 'sol', 'old': 'g(x)=t', 'new': 'f(x)=t', 'nth': 3})
E(34, 'sol', 'OVER', '= {0+2} over {7-3} = {1} over {2}')
E(37, 'sol', '{1} over {6} =2', None, sub='{1} over {6} =3')
T(39, 'q', '을 만족할 때', '을 만족시킬 때')
E(39, 'sol', 'over {g LEFT ( x RIGHT )} =0', 'lim _{x `->` inf} {h LEFT ( x RIGHT )} over {f LEFT ( x RIGHT )} =0')
T(41, 'sol', '일 때, (분자)', '일 때, (분모)')
T(41, 'sol', '존재하므로 (분모)', '존재하므로 (분자)')
E(44, 'sol', 'x+a over x-1', '=lim _{x `->` -1} {x+a} over {x-1} = {-1+a} over {-2} =3')
E(45, 'sol', 'root 3+a', 'sqrt {3+a} - sqrt {4} =0')
E(45, 'sol', '1 cdot', 'ab=1 times {1} over {4} = {1} over {4}')
E(46, 'sol', '-a over 2+x', '= lim _{x `->` 2} {-a} over {2+x} = {-a} over {4} =1')
E(46, 'sol', '(-16)=64', 'ab=(-4) times (-16)=64')
T(48, 'q', '다항함수', '다항함수 ', exact=True)
E(50, 'q', 'f {left(1} over {2} right)', 'f LEFT ( {1} over {2} RIGHT )')
E(50, 'sol', 'f {left(1} over {2} right)', None, sub='f LEFT ( {1} over {2} RIGHT )')
T(51, 'q', '이면', '이면 ', exact=True)
E(51, 'sol', '`f(x)=`h(x)+k(x)', 'f(x)= {h(x)+k(x)} over {2}')
E(51, 'sol', 'over  2}  = {alpha', 'lim _{x `->` a} f(x)= lim _{x `->` a} {h(x)+k(x)} over {2} = {alpha + beta} over {2}')
E(58, 'sol', '{= 5}', None, sub='= 5')
for s in [s for s in scripts(58, 'sol') if 'f {left(1} over {x} right)' in s]:
    ops.append({'op': 'eq', 'n': 58, 'part': 'sol', 'old': s, 'new': s.replace('f {left(1} over {x} right)', 'f LEFT ( {1} over {x} RIGHT )')})

# ── 문단 새로 쓰기
ops.append({'op': 'del_para', 'n': 23, 'part': 'sol', 'anchor': '-8t ^{2} +1'})
ops.append({'op': 'append', 'n': 23, 'part': 'sol', 'after_eq': 't``->``inf', 'text': '이므로'})
ops.append({'op': 'add_para', 'n': 23, 'part': 'sol', 'after': '로 치환하면',
            'text': '⟦lim _{x `->` -inf} {2x} over {sqrt {x ^{2} +1} +3x} = lim _{t `->` inf} {-2t} over {sqrt {t ^{2} +1} -3t}⟧⏎⟦= lim _{t `->` inf} {-2t( sqrt {t ^{2} +1} +3t)} over {( sqrt {t ^{2} +1} -3t)( sqrt {t ^{2} +1} +3t)}⟧⏎⟦= lim _{t `->` inf} {-2t( sqrt {t ^{2} +1} +3t)} over {-8t ^{2} +1}⟧⏎⟦= lim _{t `->` inf} {-2 LEFT ( sqrt {1+ {1} over {t ^{2}}} +3 RIGHT )} over {-8+ {1} over {t ^{2}}}⟧⏎⟦= {-2(1+3)} over {-8} =1⟧'})
ops.append({'op': 'del_para', 'n': 33, 'part': 'sol', 'anchor': '3t+1'})
ops.append({'op': 'del_para', 'n': 33, 'part': 'sol', 'anchor': '2t+1'})
ops.append({'op': 'add_para', 'n': 33, 'part': 'sol', 'after': '따라서 참',
            'text': '따라서 옳은 것은 ㄱ, ㄷ이다.'})
ops.append({'op': 'add_para', 'n': 33, 'part': 'sol', 'after': '따라서 참',
            'text': 'ㄷ. ⟦lim _{x `->` -inf} f LEFT ( {2x+1} over {2x} RIGHT ) = lim _{x `->` -inf} f LEFT ( 1+ {1} over {2x} RIGHT )⟧⏎(⟦x``->``-inf⟧일 때 ⟦{1} over {2x} ``->``0-⟧이므로 ⟦1+ {1} over {2x} ``->``1-⟧)⏎⟦=1⟧⏎따라서 참'})
ops.append({'op': 'add_para', 'n': 33, 'part': 'sol', 'after': '3 times 0',
            'text': 'ㄴ. ⟦lim _{x `->` inf} f LEFT ( {3x+1} over {x-1} RIGHT ) = lim _{x `->` inf} f LEFT ( 3+ {4} over {x-1} RIGHT )⟧⏎(⟦x``->``inf⟧일 때 ⟦{4} over {x-1} ``->``0+⟧이므로 ⟦3+ {4} over {x-1} ``->``3+⟧)⏎⟦=2⟧⏎따라서 거짓'})
ops.append({'op': 'add_para', 'n': 43, 'part': 'sol', 'after': '[정답]', 'like_n': 44, 'like': 'a= it-5',
            'text': '⟦lim _{x `->` inf} ( sqrt {x^2 +ax} - sqrt {x^2 -ax} )⟧⏎⟦= lim _{x `->` inf} {( sqrt {x^2 +ax} - sqrt {x^2 -ax} )( sqrt {x^2 +ax} + sqrt {x^2 -ax} )} over {sqrt {x^2 +ax} + sqrt {x^2 -ax}}⟧⏎⟦= lim _{x `->` inf} {2ax} over {sqrt {x^2 +ax} + sqrt {x^2 -ax}}⟧⏎⟦= lim _{x `->` inf} {2a} over {sqrt {1+ {a} over {x}} + sqrt {1- {a} over {x}}}⟧⏎⟦= {2a} over {2} =a⟧⏎따라서 ⟦a=5⟧'})
ops.append({'op': 'del_para', 'n': 51, 'part': 'sol', 'anchor': 'f(x)+ RIGHT .'})
ops.append({'op': 'add_para', 'n': 51, 'part': 'sol', 'after': 'ㄷ은 옳다.',
            'text': '⟦lim _{x `->` a} LEFT { f(x)+g(x) RIGHT } = alpha⟧, ⟦lim _{x `->` a} LEFT { f(x)-g(x) RIGHT } = beta⟧'})
json.dump(ops, open('u_mj/m1_01_edit.json', 'w'), ensure_ascii=False, indent=0)
print('명령', len(ops))
