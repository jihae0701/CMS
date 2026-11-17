# -*- coding: utf-8 -*-
"""C 원본과 M 원본의 문항을 단원별로 맞대어 본다. python3 compare.py C.hwpx M.hwpx"""
import sys, re, html, difflib, json
sys.path.insert(0, '/tmp/claude-0/-home-user-CMS/7a122d51-a5b1-5def-9637-d43cb9a9b6ef/scratchpad/eqw')
import hwpxedit as H

def probs(path):
    x = H.load(path)
    # STEP 경계: 본문에서 'STEP 2', 'STEP 3' 글이 나오는 위치
    body = re.sub(r'<hp:endNote.*?</hp:endNote>', lambda m: ' ' * len(m.group(0)), x, flags=re.S)
    steps = [(m.start(), '2') for m in re.finditer('유형별 학습하기', body)] + [(m.start(), '3') for m in re.finditer('단원 마무리', body)]
    steps.sort()
    out = []
    n = 1
    while True:
        try:
            q = H.region(x, n, 'q'); sol = H.region(x, n, 'sol')
        except Exception:
            break
        if not q:
            break
        def txt(spans):
            s = ''.join(x[a:b] for a, b in spans)
            s = re.sub(r'<hp:equation (?:(?!</hp:equation>).)*?<hp:script>(.*?)</hp:script></hp:equation>', lambda m: ' ' + html.unescape(m.group(1)) + ' ', s, flags=re.S)
            s = re.sub(r'<hp:pic (?:(?!</hp:pic>).)*</hp:pic>', ' [그림] ', s, flags=re.S)
            s = re.sub(r'<[^>]+>', '', s)
            return html.unescape(s)
        qs = txt(q); ss = txt(sol)
        pos = q[0][0]
        st = '1'
        for p, k in steps:
            if p < pos:
                st = k
        ans = re.search(r'\[정답\]\s*(.{0,40})', ss)
        out.append({'n': n, 'step': st, 'q': re.sub(r'\s+', ' ', qs).strip(), 'ans': ans.group(1).strip() if ans else '', 'sol_len': len(ss)})
        n += 1
    return out

def norm(s):
    s = re.sub(r'수식입니다\.|그림입니다\.|원본 그림의 이름:\S+|원본 그림의 크기:[^ ]+ [^ ]+', '', s)
    return re.sub(r'[\s`~{}]|LEFT|RIGHT|left|right', '', s)

C, M = probs(sys.argv[1]), probs(sys.argv[2])
res = []
for m in M:
    best = max(C, key=lambda c: difflib.SequenceMatcher(None, norm(c['q']), norm(m['q'])).ratio())
    r = difflib.SequenceMatcher(None, norm(best['q']), norm(m['q'])).ratio()
    res.append({'m': m['n'], 'mstep': m['step'], 'c': best['n'], 'cstep': best['step'], 'r': round(r, 2), 'mq': m['q'][:160], 'cq': best['q'][:160], 'msol': m['sol_len'], 'csol': best['sol_len']})
json.dump({'C': C, 'M': M, 'match': res}, open(sys.argv[3], 'w'), ensure_ascii=False, indent=0)
same = sum(1 for r in res if r['r'] >= 0.9); mod = sum(1 for r in res if 0.6 <= r['r'] < 0.9); new = sum(1 for r in res if r['r'] < 0.6)
from collections import Counter
print('C', len(C), dict(Counter(c['step'] for c in C)), '| M', len(M), dict(Counter(m['step'] for m in M)), '| 같음', same, '바뀜', mod, '새 문항', new)
