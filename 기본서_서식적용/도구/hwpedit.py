# -*- coding: utf-8 -*-
"""HWP 5.0 본문(BodyText/Section0) 레코드 단위 편집 도구.

글자 표현(render):
  - 일반 글자는 그대로, 줄 바꿈은 ⏎, 탭은 ⇥, 문단 끝은 표시하지 않음
  - 수식 개체는 ⟦수식 스크립트⟧, 그 밖의 개체는 {gso} {tbl} {atno} {en} 같은 {이름}
편집 명령(JSON):
  {"op":"replace","n":12,"part":"sol","old":"...","new":"..."}
  {"op":"add_para","n":12,"part":"sol","after":"<기준 문단 일부>","text":"..."}  (기준 문단 바로 뒤에 새 문단)
  {"op":"add_para","n":12,"part":"sol","before":"<기준 문단 일부>","text":"..."}
  {"op":"del_para","n":12,"part":"sol","para":"<지울 문단 일부>"}
  part: q(문제 본문) / sol(미주: 정답·해설) / end(끝 정답 모음의 n번째 줄) / head(문항 1 앞) / any(문서 전체) / master(바탕쪽)
  old/para/after/before는 그 범위 안에서 정확히 한 문단, 한 곳에만 있어야 한다.
"""
import struct, random, copy, re, zlib, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hwplib import Hwp, recs, pack

HB = 16
T_PARA_HDR, T_PARA_TEXT, T_CHAR_SHAPE, T_LINE_SEG, T_RANGE_TAG, T_CTRL_HDR, T_LIST_HDR = (HB + 50, HB + 51, HB + 52,
                                                                                    HB + 53, HB + 54, HB + 55, HB + 56)
T_EQEDIT = HB + 72
CHAR1 = {0, 10, 13, 24, 25, 26, 27, 28, 29, 30, 31}
INLINE = {4, 5, 6, 7, 8, 9, 19, 20}
EXT = {1, 2, 3, 11, 12, 14, 15, 16, 17, 18, 21, 22, 23}


class EditError(Exception):
    pass


# ---------------------------------------------------------------- 문단 구조
class Para:
    """rs[hdr] 부터 rs[end-1] 까지가 이 문단의 레코드"""
    def __init__(self, doc, hdr):
        self.doc = doc
        self.hdr = hdr

    @property
    def rs(self):
        return self.doc.rs

    @property
    def level(self):
        return self.rs[self.hdr][1]

    @property
    def end(self):
        rs, L = self.rs, self.level
        j = self.hdr + 1
        while j < len(rs) and rs[j][1] > L:
            j += 1
        return j

    def child(self, tag):
        rs, L = self.rs, self.level
        for j in range(self.hdr + 1, self.end):
            if rs[j][1] == L + 1 and rs[j][0] == tag:
                return j
        return None

    def ctrls(self):
        """(시작, 끝) 레코드 범위 목록 – PARA_TEXT의 확장 제어 문자 순서와 같다"""
        rs, L = self.rs, self.level
        out = []
        j = self.hdr + 1
        e = self.end
        while j < e:
            if rs[j][1] == L + 1 and rs[j][0] == T_CTRL_HDR:
                k = j + 1
                while k < e and rs[k][1] > L + 1:
                    k += 1
                out.append((j, k))
                j = k
            else:
                j += 1
        return out

    # 글자 단위 목록: [kind, value, raw_bytes]
    #   kind 'c': 글자(value=문자열), 'n': 1칸 제어문자(value=코드), 'x': 8칸 제어(value=코드, raw=16바이트)
    def units(self):
        ti = self.child(T_PARA_TEXT)
        if ti is None:
            return []
        p = self.rs[ti][2]
        out = []
        i = 0
        while i + 1 < len(p):
            c = struct.unpack_from('<H', p, i)[0]
            if c < 32:
                if c in CHAR1:
                    out.append(['n', c, p[i:i + 2]])
                    i += 2
                else:
                    out.append(['x', c, p[i:i + 16]])
                    i += 16
            elif 0xD800 <= c < 0xDC00 and i + 3 < len(p):
                out.append(['c', p[i:i + 4].decode('utf-16le'), p[i:i + 4]])
                i += 4
            else:
                out.append(['c', chr(c), p[i:i + 2]])
                i += 2
        return out

    def render_units(self):
        """(문자열, 각 글자가 속한 unit 번호 목록)"""
        us = self.units()
        ctrls = self.ctrls()
        s = []
        owner = []
        k = 0
        for ui, u in enumerate(us):
            if u[0] == 'c':
                t = u[1]
            elif u[0] == 'n':
                t = {10: '⏎', 13: '', 0: ''}.get(u[1], '')
            else:
                if u[1] == 9:
                    t = '⇥'
                elif u[1] in EXT:
                    cid = self.doc.ctrl_id(ctrls[k][0]) if k < len(ctrls) else '?'
                    if cid == 'eqed':
                        t = '⟦' + self.doc.eq_script(ctrls[k][0]) + '⟧'
                    else:
                        t = '{' + cid.strip() + '}'
                    k += 1
                else:
                    t = ''
            s.append(t)
            owner += [ui] * len(t)
        return ''.join(s), owner, us

    def text(self):
        return self.render_units()[0]


class Doc:
    def __init__(self, path):
        self.path = path
        self.h = Hwp(path)
        self.rs = recs(self.h.stream('BodyText/Section0'))
        self.log = []

    # ---------------------------------------------------------- 기본 도우미
    def ctrl_id(self, j):
        return self.rs[j][2][:4][::-1].decode('latin1')

    def eq_rec(self, j):
        """CTRL_HDR j(수식) 아래의 EQEDIT 레코드 번호"""
        L = self.rs[j][1]
        k = j + 1
        while k < len(self.rs) and self.rs[k][1] > L:
            if self.rs[k][0] == T_EQEDIT:
                return k
            k += 1
        return None

    def eq_script(self, j):
        k = self.eq_rec(j)
        p = self.rs[k][2]
        n = struct.unpack_from('<H', p, 4)[0]
        return p[6:6 + 2 * n].decode('utf-16le', 'surrogatepass')

    def set_eq_script(self, j, s):
        k = self.eq_rec(j)
        p = self.rs[k][2]
        n = struct.unpack_from('<H', p, 4)[0]
        b = s.encode('utf-16le', 'surrogatepass')
        self.rs[k][2] = p[:4] + struct.pack('<H', len(b) // 2) + b + p[6 + 2 * n:]

    def paras(self):
        return [Para(self, i) for i, r in enumerate(self.rs) if r[0] == T_PARA_HDR]

    # ---------------------------------------------------------- 구역 나누기
    def regions(self):
        """문항별 범위: {'q': {n: [Para]}, 'sol': {n: [Para]}, 'end': {n: Para}, 'head': [Para], 'master': [Para]}"""
        rs = self.rs
        ps = self.paras()
        # 바탕쪽(구역 정의 안)
        master = set()
        for i, r in enumerate(rs):
            if r[0] == T_CTRL_HDR and r[2][:4] == b'dces':
                L = r[1]
                k = i + 1
                while k < len(rs) and rs[k][1] > L:
                    if rs[k][0] == T_PARA_HDR:
                        master.add(k)
                    k += 1
        # 미주 범위
        en_ranges = []
        for i, r in enumerate(rs):
            if r[0] == T_CTRL_HDR and r[2][:4] == b'  ne':
                L = r[1]
                k = i + 1
                while k < len(rs) and rs[k][1] > L:
                    k += 1
                en_ranges.append((i, k))
        in_en = {}
        for n, (a, b) in enumerate(en_ranges, 1):
            for k in range(a, b):
                if rs[k][0] == T_PARA_HDR:
                    in_en[k] = n
        # 미주를 가진 본문 문단 = 문항 시작
        start = {}
        for n, (a, b) in enumerate(en_ranges, 1):
            k = a
            while rs[k][0] != T_PARA_HDR or rs[k][1] >= rs[a][1]:
                k -= 1
            start[n] = k
        N = len(en_ranges)
        # 끝 정답 모음: 마지막 문항 뒤, 미주 밖에서 {atno}로 시작하는 문단
        reg = {'q': {}, 'sol': {}, 'end': {}, 'head': [], 'master': [], 'N': N}
        endlist = []
        last_start = start[N] if N else 0
        for p in ps:
            if p.hdr in master:
                reg['master'].append(p)
                continue
            if p.hdr in in_en:
                reg['sol'].setdefault(in_en[p.hdr], []).append(p)
                continue
            if N == 0 or p.hdr < start[1]:
                reg['head'].append(p)
                continue
            n = max(k for k in start if start[k] <= p.hdr)
            reg['q'].setdefault(n, []).append(p)
            if p.hdr > last_start and re.match(r'^(\s|\{gso\}|\{nwno\})*\{atno\}', p.text()):
                endlist.append(p)
        # 끝 정답 모음은 마지막 문항의 q 범위에서 떼어 낸다
        if endlist:
            first = endlist[0].hdr
            reg['q'][N] = [p for p in reg['q'][N] if p.hdr < first]
            reg['endtail'] = [p for p in ps if p.hdr >= first and p.hdr not in master and p.hdr not in in_en]
            for i, p in enumerate(endlist, 1):
                reg['end'][i] = p
        return reg

    def region_paras(self, n, part):
        reg = self.regions()
        if part == 'any':
            return [p for p in self.paras()]
        if part == 'head':
            return reg['head']
        if part == 'master':
            return reg['master']
        if part == 'end':
            if n not in reg['end']:
                raise EditError(f'끝 정답 모음에 {n}번째 줄이 없음 (모두 {len(reg["end"])}줄)')
            return [reg['end'][n]]
        if part in ('q', 'sol'):
            return reg[part].get(n, [])
        raise EditError('알 수 없는 part ' + str(part))

    def find_para(self, n, part, needle):
        hits = [p for p in self.region_paras(n, part) if needle in p.text()]
        if len(hits) != 1:
            raise EditError(f'문항 {n} {part}: "{needle}"이(가) 든 문단이 {len(hits)}개')
        return hits[0]

    # ---------------------------------------------------------- 문단 다시 쓰기
    def _owner_list(self, p):
        """p가 속한 목록의 LIST_HDR 번호 (본문이면 None)"""
        rs, L = self.rs, p.level
        k = p.hdr - 1
        while k >= 0:
            if rs[k][1] < L:
                return k if rs[k][0] == T_LIST_HDR else None
            if rs[k][1] == L and rs[k][0] == T_LIST_HDR:
                return k
            k -= 1
        return None

    def _rewrite(self, p, new_units, edits):
        """new_units: 새 글자 단위 목록(문단 끝 포함). edits: [(옛 시작, 옛 끝, 새 길이)] 위치 보정용 (wchar 단위)"""
        rs = self.rs
        data = b''.join(u[2] for u in new_units)
        nch = len(data) // 2
        hp = bytearray(rs[p.hdr][2])
        old = struct.unpack_from('<I', hp, 0)[0]
        struct.pack_into('<I', hp, 0, (old & 0x80000000) | nch)
        mask = 0
        for u in new_units:
            if u[0] in ('x', 'n') and u[1] < 32 and u[1] != 13:
                mask |= (1 << u[1])
        struct.pack_into('<I', hp, 4, mask)
        rs[p.hdr][2] = bytes(hp)
        ti = p.child(T_PARA_TEXT)
        if ti is None:
            # PARA_TEXT가 없던 문단: 문단 머리 바로 뒤에 넣는다
            rs.insert(p.hdr + 1, [T_PARA_TEXT, p.level + 1, data])
        else:
            rs[ti][2] = data

        def mp(x):
            for a, b, nl in edits:
                if x >= b:
                    x += nl - (b - a)
                elif x > a:
                    x = a
            return x
        ci = p.child(T_CHAR_SHAPE)
        if ci is not None:
            pr = rs[ci][2]
            pairs = [struct.unpack_from('<II', pr, i) for i in range(0, len(pr), 8)]
            np = []
            for pos, sid in pairs:
                q = mp(pos) if pos else 0
                if np and np[-1][0] == q:
                    np[-1] = (q, sid)
                else:
                    np.append((q, sid))
            np = [x for x in np if x[0] < nch] or [(0, pairs[0][1])]
            rs[ci][2] = b''.join(struct.pack('<II', a, b) for a, b in np)
            hp = bytearray(rs[p.hdr][2])
            struct.pack_into('<H', hp, 12, len(np))
            rs[p.hdr][2] = bytes(hp)
        li = p.child(T_LINE_SEG)
        if li is not None:
            pr = rs[li][2]
            segs = [bytearray(pr[i:i + 36]) for i in range(0, len(pr), 36)]
            out = []
            for sg in segs:
                tp = struct.unpack_from('<I', sg, 0)[0]
                q = mp(tp) if tp else 0
                if out and struct.unpack_from('<I', out[-1], 0)[0] == q:
                    continue
                if q >= nch and out:
                    continue
                struct.pack_into('<I', sg, 0, q)
                out.append(sg)
            rs[li][2] = b''.join(bytes(s) for s in out)
            hp = bytearray(rs[p.hdr][2])
            struct.pack_into('<H', hp, 16, len(out))
            rs[p.hdr][2] = bytes(hp)
        ri = p.child(T_RANGE_TAG)
        if ri is not None:
            pr = rs[ri][2]
            out = b''
            for i in range(0, len(pr), 12):
                a, b, t = struct.unpack_from('<III', pr, i)
                out += struct.pack('<III', mp(a), mp(b), t)
            rs[ri][2] = out

    # ---------------------------------------------------------- 수식 개체 만들기
    def _template_eq(self, near):
        """near 레코드에서 가장 가까운 수식 개체(CTRL_HDR 범위)"""
        best = None
        for i, r in enumerate(self.rs):
            if r[0] == T_CTRL_HDR and r[2][:4] == b'deqe':
                d = abs(i - near)
                if best is None or d < best[0]:
                    best = (d, i)
        if best is None:
            raise EditError('본보기 수식이 없음')
        i = best[1]
        L = self.rs[i][1]
        k = i + 1
        while k < len(self.rs) and self.rs[k][1] > L:
            k += 1
        return i, k

    def _eq_char_unit(self, tmpl_ctrl):
        """본보기 수식이 놓인 문단에서 그 수식의 8칸 제어 문자"""
        for p in self.paras():
            cs = p.ctrls()
            for k, (a, b) in enumerate(cs):
                if a == tmpl_ctrl:
                    us = [u for u in p.units() if u[0] == 'x' and u[1] in EXT]
                    return copy.deepcopy(us[k])
        raise EditError('수식 문자 없음')

    def _new_eq_records(self, level, script, near):
        a, b = self._template_eq(near)
        recs_ = [[t, l - self.rs[a][1] + level, pl] for t, l, pl in copy.deepcopy(self.rs[a:b])]
        hp = bytearray(recs_[0][2])
        if len(hp) >= 40:
            struct.pack_into('<I', hp, 36, random.randint(0x10000000, 0x7fffffff))
        recs_[0][2] = bytes(hp)
        for r in recs_:
            if r[0] == T_EQEDIT:
                p = r[2]
                n = struct.unpack_from('<H', p, 4)[0]
                bs = script.encode('utf-16le', 'surrogatepass')
                r[2] = p[:4] + struct.pack('<H', len(bs) // 2) + bs + p[6 + 2 * n:]
        unit = self._eq_char_unit(a)
        return recs_, unit

    # ---------------------------------------------------------- 명령
    TOK = re.compile(r'⟦(.*?)⟧|\{(gso|tbl|atno|en|nwno|cold|secd|pgnp|pghd|fn|bokm|head|foot|dloc)\}|(⏎)|(⇥)|(.)', re.S)

    def _tokens(self, s):
        out = []
        for m in self.TOK.finditer(s):
            if m.group(1) is not None:
                out.append(('eq', m.group(1)))
            elif m.group(2):
                out.append(('ctl', m.group(2)))
            elif m.group(3):
                out.append(('br', None))
            elif m.group(4):
                out.append(('tab', None))
            else:
                out.append(('t', m.group(5)))
        return out

    def replace(self, n, part, old, new, allow_ctrl_delete=False):
        if old == new:
            raise EditError('old와 new가 같음')
        p = self.find_para(n, part, old)
        self._replace_in(p, old, new, allow_ctrl_delete)
        self.log.append(('replace', n, part, old, new))

    def remove_page_numbers(self):
        """바탕쪽의 쪽 번호(자동 번호) 개체를 모두 지운다"""
        cnt = 0
        while True:
            ps = [p for p in self.regions()['master'] if '{atno}' in p.text()]
            if not ps:
                return cnt
            self._replace_in(ps[0], '{atno}', '', True)
            cnt += 1

    def _replace_in(self, p, old, new, allow_ctrl_delete=False):
        s, owner, us = p.render_units()
        if s.count(old) != 1:
            raise EditError(f'"{old}"이(가) 문단 안에 {s.count(old)}번')
        i0 = s.index(old)
        i1 = i0 + len(old)
        if i0 > 0 and owner[i0 - 1] == owner[i0]:
            raise EditError('old가 수식/개체 중간에서 시작함: 수식 전체를 ⟦…⟧로 포함하세요')
        if i1 < len(s) and owner[i1 - 1] == owner[i1]:
            raise EditError('old가 수식/개체 중간에서 끝남: 수식 전체를 ⟦…⟧로 포함하세요')
        u0, u1 = owner[i0], owner[i1 - 1] + 1
        old_units = us[u0:u1]
        ctrls = p.ctrls()
        # 이 범위 앞에 있는 확장 제어 수
        kbefore = sum(1 for u in us[:u0] if u[0] == 'x' and u[1] in EXT)
        old_ext = [(kbefore + j) for j, u in enumerate([u for u in old_units if u[0] == 'x' and u[1] in EXT])]
        old_eq = [k for k in old_ext if self.ctrl_id(ctrls[k][0]) == 'eqed']
        old_other = [k for k in old_ext if k not in old_eq]
        toks = self._tokens(new)
        new_eq = [t[1] for t in toks if t[0] == 'eq']
        new_other = [t[1] for t in toks if t[0] == 'ctl']
        if [self.ctrl_id(ctrls[k][0]).strip() for k in old_other] != new_other:
            if not (allow_ctrl_delete and not new_other):
                raise EditError('수식이 아닌 개체({gso} 등)는 old와 new에 같은 순서로 그대로 두어야 함')
        delete_recs = []
        if len(new_eq) == len(old_eq):
            for k, sc in zip(old_eq, new_eq):
                if self.eq_script(ctrls[k][0]) != sc:
                    self.set_eq_script(ctrls[k][0], sc)
            eq_units = [u for u in old_units if u[0] == 'x' and u[1] in EXT]
            keep_eq_units = [u for u, k in zip(eq_units, old_ext) if k in old_eq]
            insert_eq = []
        elif not old_eq:
            keep_eq_units = None
            insert_eq = new_eq
        elif not new_eq:
            keep_eq_units = []
            insert_eq = []
            delete_recs += [ctrls[k] for k in old_eq]
        else:
            raise EditError('수식 개수가 달라짐: 수식을 늘리거나 줄일 때는 한 명령에 한쪽만 0개가 되게 나누세요')
        other_units = [u for u, k in zip([u for u in old_units if u[0] == 'x' and u[1] in EXT], old_ext) if k in old_other]
        if allow_ctrl_delete and not new_other:
            delete_recs += [ctrls[k] for k in old_other]
            other_units = []
        # 새 글자 단위 만들기
        nu = []
        new_eq_recs = []
        ei = 0
        oi = 0
        for t in toks:
            if t[0] == 't':
                b = t[1].encode('utf-16le', 'surrogatepass')
                nu.append(['c', t[1], b])
            elif t[0] == 'br':
                nu.append(['n', 10, struct.pack('<H', 10)])
            elif t[0] == 'tab':
                tabu = next((copy.deepcopy(u) for u in us if u[0] == 'x' and u[1] == 9), None)
                if tabu is None:
                    tabu = ['x', 9, struct.pack('<H', 9) + b'\0' * 12 + struct.pack('<H', 9)]
                nu.append(tabu)
            elif t[0] == 'ctl':
                nu.append(other_units[oi])
                oi += 1
            else:
                if keep_eq_units is not None:
                    nu.append(keep_eq_units[ei])
                else:
                    recs_, unit = self._new_eq_records(p.level + 1, t[1], p.hdr)
                    nu.append(unit)
                    new_eq_recs.append(recs_)
                ei += 1
        old_len = sum(len(u[2]) for u in old_units) // 2
        a = sum(len(u[2]) for u in us[:u0]) // 2
        new_units = us[:u0] + nu + us[u1:]
        new_len = sum(len(u[2]) for u in nu) // 2
        # 개체 레코드를 새 글자 순서대로 다시 놓는다 (글자 속 확장 제어 문자 순서 = 개체 레코드 순서)
        ext_old = [u for u in us if u[0] == 'x' and u[1] in EXT]
        sub_of = {id(u): copy.deepcopy(self.rs[a_:b_]) for u, (a_, b_) in zip(ext_old, ctrls)}
        ni = 0
        for u in nu:
            if u[0] == 'x' and u[1] in EXT and id(u) not in sub_of:
                sub_of[id(u)] = new_eq_recs[ni]
                ni += 1
        ordered = []
        for u in new_units:
            if u[0] == 'x' and u[1] in EXT:
                ordered += sub_of[id(u)]
        start = ctrls[0][0] if ctrls else p.end
        self.rs[start:p.end] = ordered
        # p.hdr 위치는 그대로 (넣고 지운 레코드는 모두 p.hdr 뒤)
        self._rewrite(p, new_units, [(a, a + old_len, new_len)])

    def del_para(self, n, part, needle):
        p = self.find_para(n, part, needle)
        rs = self.rs
        a, b = p.hdr, p.end
        last = struct.unpack_from('<I', rs[a][2], 0)[0] & 0x80000000
        lh = self._owner_list(p)
        # 같은 목록의 앞 문단
        prev = None
        k = a - 1
        while k >= 0 and rs[k][1] >= p.level:
            if rs[k][0] == T_PARA_HDR and rs[k][1] == p.level:
                prev = k
                break
            k -= 1
        nxt_is_para = b < len(rs) and rs[b][0] == T_PARA_HDR and rs[b][1] == p.level
        if not nxt_is_para and prev is None:
            raise EditError('목록의 유일한 문단은 지울 수 없음')
        del rs[a:b]
        if last and prev is not None:
            hp = bytearray(rs[prev][2])
            struct.pack_into('<I', hp, 0, struct.unpack_from('<I', hp, 0)[0] | 0x80000000)
            rs[prev][2] = bytes(hp)
        if lh is not None:
            lp = bytearray(rs[lh][2])
            struct.pack_into('<h', lp, 0, struct.unpack_from('<h', lp, 0)[0] - 1)
            rs[lh][2] = bytes(lp)
        self.log.append(('del_para', n, part, needle))

    def _sol_template(self, near):
        """미주(해설)에서 가장 흔한 보통 해설 문단(정답 줄이 아닌 둘째 문단 이후)의 본보기. 같은 단계(level)만."""
        from collections import Counter
        reg = self.regions()
        cnt = Counter()
        first = {}
        for n, ps in reg['sol'].items():
            for q in ps[1:]:
                if q.level != near.level:
                    continue
                t = q.text()
                if not t.strip() or t.lstrip().startswith('{'):
                    continue
                if not any(u[0] == 'c' and u[1].strip() and not ('\u3131' <= u[1] <= '\u318e') for u in q.units()):
                    continue
                key = bytes(self.rs[q.hdr][2][8:11])
                cnt[key] += 1
                first.setdefault(key, q)
        if not cnt:
            return None
        return first[cnt.most_common(1)[0][0]]

    def add_para(self, n, part, anchor, text, before=False):
        p = self.find_para(n, part, anchor)
        rs = self.rs
        L = p.level
        last = struct.unpack_from('<I', rs[p.hdr][2], 0)[0] & 0x80000000
        # 본보기: 기준 문단의 머리·글자 모양·줄 정보.
        # 기준이 정답 줄이면 정답 줄 모양(작은 글씨·내어쓰기) 대신 보통 해설 문단 모양을 쓴다.
        tpl = p
        if re.match(r'^(\s|\{gso\}|\{nwno\})*\{atno\}', p.text()):
            tpl = self._sol_template(p) or p
        hdr = bytearray(rs[tpl.hdr][2])
        ci = tpl.child(T_CHAR_SHAPE)
        li = tpl.child(T_LINE_SEG)
        # 기준 문단 글자 모양 중 '보통 글자'에 쓰인 것: 첫 일반 글자 위치의 모양
        us = tpl.units()
        pos = 0
        first_c = None
        for u in us:
            if u[0] == 'c' and u[1].strip():
                first_c = pos
                break
            pos += len(u[2]) // 2
        pairs = [struct.unpack_from('<II', rs[ci][2], i) for i in range(0, len(rs[ci][2]), 8)]
        sid = pairs[0][1]
        if first_c is not None:
            for q, s_ in pairs:
                if q <= first_c:
                    sid = s_
        new = [[T_PARA_HDR, L, None], [T_PARA_TEXT, L + 1, b''], [T_CHAR_SHAPE, L + 1, struct.pack('<II', 0, sid)]]
        seg = bytearray(rs[li][2][:36]) if li is not None else None
        if seg is not None:
            struct.pack_into('<I', seg, 0, 0)
            new.append([T_LINE_SEG, L + 1, bytes(seg)])
        insert_at = p.hdr if before else p.end
        rs[insert_at:insert_at] = new
        np_ = Para(self, insert_at)
        # 머리: 기준 문단 복사, 마지막 표시 정리
        h2 = bytearray(hdr)
        struct.pack_into('<I', h2, 0, 1)
        struct.pack_into('<I', h2, 4, 0)
        struct.pack_into('<H', h2, 12, 1)
        struct.pack_into('<H', h2, 14, 0)
        struct.pack_into('<H', h2, 16, 1 if seg is not None else 0)
        if len(h2) >= 22:
            struct.pack_into('<I', h2, 18, 0)
        if not before and last:
            # 기준 문단이 목록의 마지막이었다면 표시를 새 문단으로 옮김
            struct.pack_into('<I', h2, 0, 0x80000000 | 1)
            ph = bytearray(rs[p.hdr][2])
            struct.pack_into('<I', ph, 0, struct.unpack_from('<I', ph, 0)[0] & 0x7fffffff)
            rs[p.hdr][2] = bytes(ph)
        rs[insert_at][2] = bytes(h2)
        # 글자 채우기: 빈 문단(문단 끝만)에 replace 방식으로 넣는다
        self._rewrite(np_, [['n', 13, struct.pack('<H', 13)]], [])
        toks = self._tokens(text)
        nu = []
        new_eq_recs = []
        for t in toks:
            if t[0] == 't':
                nu.append(['c', t[1], t[1].encode('utf-16le', 'surrogatepass')])
            elif t[0] == 'br':
                nu.append(['n', 10, struct.pack('<H', 10)])
            elif t[0] == 'tab':
                tabu = next((copy.deepcopy(u) for u in us if u[0] == 'x' and u[1] == 9), None) or \
                    ['x', 9, struct.pack('<H', 9) + b'\0' * 12 + struct.pack('<H', 9)]
                nu.append(tabu)
            elif t[0] == 'eq':
                recs_, unit = self._new_eq_records(L + 1, t[1], p.hdr)
                nu.append(unit)
                new_eq_recs.append(recs_)
            else:
                raise EditError('새 문단에는 수식 말고 다른 개체를 넣을 수 없음')
        nu.append(['n', 13, struct.pack('<H', 13)])
        if new_eq_recs:
            e = np_.end
            rs[e:e] = [r for rr in new_eq_recs for r in rr]
        self._rewrite(np_, nu, [(0, 0, sum(len(u[2]) for u in nu) // 2 - 1)])
        # 글자 모양: 새 문단 전체 한 모양
        ci2 = np_.child(T_CHAR_SHAPE)
        rs[ci2][2] = struct.pack('<II', 0, sid)
        h3 = bytearray(rs[np_.hdr][2])
        struct.pack_into('<H', h3, 12, 1)
        rs[np_.hdr][2] = bytes(h3)
        lh = self._owner_list(np_)
        if lh is not None:
            lp = bytearray(rs[lh][2])
            struct.pack_into('<h', lp, 0, struct.unpack_from('<h', lp, 0)[0] + 1)
            rs[lh][2] = bytes(lp)
        self.log.append(('add_para', n, part, anchor, text))

    def apply(self, op):
        o = op['op']
        n = op.get('n')
        part = op.get('part', 'any')
        if o == 'replace':
            self.replace(n, part, op['old'], op['new'], op.get('allow_ctrl_delete', False))
        elif o == 'del_para':
            self.del_para(n, part, op['para'])
        elif o == 'add_para':
            if 'after' in op:
                self.add_para(n, part, op['after'], op['text'])
            else:
                self.add_para(n, part, op['before'], op['text'], before=True)
        else:
            raise EditError('알 수 없는 op ' + o)

    # ---------------------------------------------------------- 저장
    def section_bytes(self):
        return pack(self.rs)

    def save(self, dst):
        import inplace, cfb
        raw = self.section_bytes()
        data = raw
        if self.h.compressed:
            c = zlib.compressobj(9, zlib.DEFLATED, -15)
            data = c.compress(raw) + c.flush()
        tmp = dst + '.tmp'
        if not inplace.replace_stream(self.path, tmp, ['BodyText', 'Section0'], data):
            root = cfb.read_tree(self.path)
            cfb.find(root, 'BodyText/Section0').data = data
            cfb.write(root, tmp)
        os.replace(tmp, dst)


def dump_regions(path, out):
    """편집 명령을 쓰기 위한 글 뽑기: 문단마다 한 줄, 구역 머리표"""
    d = Doc(path)
    reg = d.regions()
    lines = []

    def emit(p):
        t = p.text()
        if t.strip():
            lines.append('  ' * min(p.level, 6) + '¶ ' + t)
    lines.append('【head】')
    for p in reg['head']:
        emit(p)
    for n in range(1, reg['N'] + 1):
        lines.append(f'\n【문항 {n} · q】')
        for p in reg['q'].get(n, []):
            emit(p)
        lines.append(f'【문항 {n} · sol】')
        for p in reg['sol'].get(n, []):
            emit(p)
    lines.append('\n【끝 정답 모음 · end】')
    for k, p in sorted(reg['end'].items()):
        lines.append(f'[end {k}] ' + p.text())
    others = [p for p in reg.get('endtail', []) if p not in reg['end'].values()]
    if others:
        lines.append('【끝 정답 모음 사이의 다른 문단 (part any로만 고칠 수 있음)】')
        for p in others:
            emit(p)
    open(out, 'w').write('\n'.join(lines) + '\n')
    return reg['N'], len(reg['end'])
