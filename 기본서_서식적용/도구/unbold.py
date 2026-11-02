"""정답 줄(자동 번호로 시작하는 문단: 해설 첫 줄·끝 정답 모음)의 수식에서 bold를 없앤다."""
import sys, struct, re
sys.path.insert(0, __import__('os').path.dirname(__file__))
from hwplib import recs, pack
import dump
HB = 16
BOLD = re.compile(r'bold', re.I)

def is_answer_para(txt):
    t = re.sub(r'^(\{gso\}|\{tbl\}|\{nwno\}|\s)+', '', txt)
    return t.startswith('{atno}')

def eq_script(p):
    n = struct.unpack_from('<H', p, 4)[0]
    return n, p[6:6 + 2 * n].decode('utf-16le', 'surrogatepass')

def set_script(p, s):
    n = struct.unpack_from('<H', p, 4)[0]
    b = s.encode('utf-16le', 'surrogatepass')
    return p[:4] + struct.pack('<H', len(b) // 2) + b + p[6 + 2 * n:]

def process(data, apply=True):
    """미주(정답·해설) 안의 모든 수식과, 미주 밖에서 자동 번호로 시작하는 정답 모음 문단의 수식."""
    rs = recs(data)
    ans_level = None; changed = []; other = 0; en_level = None; cur_level = 0
    for r in rs:
        t, l, p = r
        if en_level is not None and l <= en_level:
            en_level = None
        if t == HB + 55 and p[:4] == b'  ne':   # 미주
            en_level = l
        if t == HB + 50:   # PARA_HDR
            ans_level = None
            cur_level = l
        elif t == HB + 51 and l == cur_level + 1:
            if is_answer_para(dump.para_text(p, None)):
                ans_level = cur_level
        elif t == HB + 72:
            n, s = eq_script(p)
            if BOLD.search(s):
                if en_level is not None or (ans_level is not None and l > ans_level):
                    ns = BOLD.sub('', s)
                    changed.append((s, ns))
                    if apply: r[2] = set_script(p, ns)
                else:
                    other += 1
    return pack(rs), changed, other
