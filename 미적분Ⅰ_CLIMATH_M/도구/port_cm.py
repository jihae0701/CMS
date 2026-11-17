# -*- coding: utf-8 -*-
"""C에서 고친 내용을 M의 같은 문항에 옮긴다.
    python3 port_cm.py 단원번호(02)
- C 처리본(u_mj/m1_NN_preedit.hwpx)과 M 처리본(u_mM/mM_NN.hwpx)의 문항(문제·해설 글+수식)을 맞대어
  문제 ≥0.97, 해설 ≥0.93이면 '같은 문항'으로 본다.
- C 고치기 명령(u_mj/m1_NN_edit*.json)에서 같은 문항의 명령만 번호를 바꿔 M에 적용(나머지는 목록으로 남김)."""
import sys, re, json, html, glob, difflib, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hwpxedit as H

u = sys.argv[1]
CP = 'u_mj/m1_%s_preedit.hwpx' % u
MP = 'u_mM/mM_%s.hwpx' % u

def texts(path):
    x = H.load(path); out = {}
    n = 1
    while True:
        try:
            q = H.region(x, n, 'q'); s = H.region(x, n, 'sol')
        except Exception:
            break
        if not q:
            break
        def t(spans):
            z = ''.join(x[a:b] for a, b in spans)
            z = re.sub(r'<hp:script\b[^>]*>(.*?)</hp:script>', lambda m: '⟦' + m.group(1) + '⟧', z, flags=re.S)
            z = re.sub(r'<hp:pic (?:(?!</hp:pic>).)*</hp:pic>', '[그림]', z, flags=re.S)
            z = re.sub(r'<(?!/?hp:t\b)[^>]+>', '', z)
            z = re.sub(r'</?hp:t>', '', z)
            return re.sub(r'\s+', ' ', html.unescape(z))
        out[n] = (t(q), t(s)); n += 1
    return out

C, M = texts(CP), texts(MP)
from mjedit import Ed
EC, EM = Ed(CP), Ed(MP)
nz = lambda L: [re.sub(r'[\s`~]', '', html.unescape(t)) for t in L]
sc = lambda E, n, p: nz(E.scripts(n, p))
SC = {c: (sc(EC, c, 'q'), sc(EC, c, 'sol')) for c in C}
ratio = lambda a, b: difflib.SequenceMatcher(None, a, b, autojunk=False).ratio()
mp = {}; rows = []
for m, (mq, ms) in M.items():
    q, so = sc(EM, m, 'q'), sc(EM, m, 'sol')
    best = max(C, key=lambda c: (ratio(SC[c][0], q) if q else 0) + ratio(C[c][0][:300], mq[:300]))
    rq = ratio(SC[best][0], q) if (q or SC[best][0]) else ratio(C[best][0], mq)
    rs = ratio(SC[best][1], so) if (so or SC[best][1]) else 1.0
    rt = ratio(C[best][0][:300], mq[:300])
    rows.append((m, best, round(rq, 3), round(rs, 3), round(rt, 3)))
    if rq >= 0.95 and rs >= 0.85 and rt >= 0.8:
        mp.setdefault(best, m)
ops = []
for f in sorted(glob.glob('u_mj/m1_%s_edit*.json' % u), key=lambda p: (len(p), p)):
    ops += json.load(open(f))
port, skip = [], []
for o in ops:
    if o.get('n') in mp:
        o = dict(o); o['n'] = mp[o['n']]
        for k in ('old', 'new', 'eq'):   # M 처리본은 부정적분을 int로 고친 도구를 거쳤다
            if isinstance(o.get(k), str):
                o[k] = re.sub(r'\b(int|oint|sum|prod)\s*_\s*\^\s*', r'\1 ', o[k])
        if 'like_n' in o:
            if o['like_n'] in mp:
                o['like_n'] = mp[o['like_n']]
            else:   # 본보기 문단이 있는 M 문항을 찾는다
                cand = [k for k, (q, s_) in M.items() if o['like'] in s_]
                if cand:
                    o['like_n'] = cand[0]
                else:          # 본보기가 없으면 붙일 자리 문단 모양을 따른다
                    o.pop('like_n'); o.pop('like', None)
        port.append(o)
    else:
        skip.append(o)
fails = H.apply(MP, port)
json.dump({'map_c_to_m': mp, 'rows': rows, 'ported': len(port), 'fails': [(i, msg, op) for i, msg, op in fails],
           'skipped_c_ops': skip}, open('u_mM/mM_%s_port.json' % u, 'w'), ensure_ascii=False, indent=0)
real = [f for f in fails if not f[2].get('optional')]
print('같은 문항 %d / M %d, 옮긴 명령 %d, 실패 %d, C에만 있는 문항 명령 %d' % (len(mp), len(M), len(port), len(real), len(skip)))
for i, msg, op in real[:20]:
    print('  실패', msg[:80], json.dumps(op, ensure_ascii=False)[:160])
