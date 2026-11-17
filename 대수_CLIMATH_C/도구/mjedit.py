# -*- coding: utf-8 -*-
"""미적분 단원 내용 고치기 명령 만들기 도우미.
    from mjedit import Ed
    ed = Ed('u_mj/m1_02.hwpx')
    ed.E(n, part, find, new, sub=None)   # find가 든 수식 하나를 new로 (sub면 그 수식 속 find→sub)
    ed.T(n, part, old, new, **k)         # 글 바꾸기(hwpxedit text)
    ed.SA(n, value, mark, ending='값은?') # 단답형: 묻는 말, 선택지 문단 지움, 정답 줄 값으로
    ed.op({...})                         # 그 밖의 hwpxedit 명령
    ed.run()                             # 적용하고 실패를 보여 줌
수식 찾기가 안 되면 '!!'로 알린다."""
import sys, json, html, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hwpxedit as H


class Ed:
    def __init__(self, path):
        self.path = path
        self.x = H.load(path)
        self.ops = []
        self.miss = []

    def scripts(self, n, part):
        out = []
        for a, b in H.region(self.x, n, part):
            for m in H.EQ.finditer(self.x, a, b):
                sm = H.SC.search(m.group(0))
                out.append(html.unescape(sm.group(2)) if sm else '')
        return out

    def E(self, n, part, find, new=None, sub=None, nth=None):
        c = [s for s in self.scripts(n, part) if find in s]
        if nth is not None:
            c = c[nth - 1:nth]
        if len(c) != 1:
            self.miss.append((n, part, find, len(c))); print('!! 수식', n, part, repr(find), len(c)); return
        old = c[0]
        d = {'op': 'eq', 'n': n, 'part': part, 'old': old, 'new': old.replace(find, sub) if sub is not None else new}
        if self.scripts(n, part).count(old) > 1:
            d['first'] = True
        self.ops.append(d)

    def T(self, n, part, old, new, **k):
        d = {'op': 'text', 'n': n, 'part': part, 'old': old, 'new': new}; d.update(k); self.ops.append(d)

    def op(self, d):
        self.ops.append(d)

    def SA(self, n, value, mark, ending='값은?', new_ending=None, sol_old=None):
        """단답형으로: 묻는 말 ending → new_ending, 선택지(①/④ 문단) 지움, 정답 줄 ' [정답] ④' → ' [정답] ⟦값⟧'"""
        if new_ending is None:
            new_ending = ending.replace('값은?', '값을 구하시오.') if '값은?' in ending else ending.replace('은?', '을 구하시오.')
        self.T(n, 'q', ending, new_ending)
        self.ops.append({'op': 'del_para', 'n': n, 'part': 'q', 'anchor': '^①'})
        for c in '②③④⑤':
            self.ops.append({'op': 'del_para', 'n': n, 'part': 'q', 'anchor': '^' + c, 'optional': True})
        old, pre = sol_old or (' [정답] ' + mark), ' [정답] '
        if not sol_old:   # 정답 줄 글 조각이 ' [정답] '·'④'처럼 나뉜 경우
            try:
                s, e = H.paras_in(self.x, H.region(self.x, n, 'sol'))[0]
                frags = [html.unescape(m.group(1)) for m in H.TPAT.finditer(self.x, s, e)]
                if old not in frags:
                    for cand, pr in ((mark, ''), (' ' + mark, ' '), (mark + ' ', ''), (' ' + mark + ' ', ' ')):
                        if cand in frags:
                            old, pre = cand, pr
                            break
            except Exception:
                pass
        self.ops.append({'op': 'text_eq', 'n': n, 'part': 'sol', 'old': old, 'pre': pre, 'eq': value, 'post': ''})

    def SPLIT(self, n, part, old, parts, nth=None):
        """수식 속 한글 나누기: 수식 old → [수식 parts[0]][글 parts[1]][수식 parts[2]]…"""
        c = [q for q in self.scripts(n, part) if q == old]
        if not c:
            self.miss.append((n, part, old, 0)); print('!! 수식', n, part, repr(old), 0); return
        d = {'op': 'eq', 'n': n, 'part': part, 'old': old, 'new': parts[0]}
        if len(c) > 1: d['first'] = True
        self.ops.append(d)
        mk = '@@%d' % (len(self.ops))
        self.ops.append({'op': 'append', 'n': n, 'part': part, 'after_eq': parts[0], 'text': parts[1] + (mk + '1' if len(parts) > 2 else '')})
        k = 1
        for i in range(2, len(parts), 2):
            post = (parts[i + 1] if i + 1 < len(parts) else '') + (mk + str(k + 1) if i + 2 < len(parts) else '')
            self.ops.append({'op': 'text_eq', 'n': n, 'part': part, 'old': mk + str(k), 'pre': '', 'eq': parts[i], 'post': post, 'sub': True})
            k += 1

    def run(self, save_json=None):
        if save_json:
            json.dump(self.ops, open(save_json, 'w'), ensure_ascii=False, indent=0)
        fails = H.apply(self.path, self.ops)
        real = [f for f in fails if not f[2].get('optional')]
        for i, msg, op in real:
            print('실패', i, msg, json.dumps(op, ensure_ascii=False)[:200])
        print('명령', len(self.ops), '실패', len(real), '(선택 명령 실패', len(fails) - len(real), ')')
        self.x = H.load(self.path)
        return real
