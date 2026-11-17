# -*- coding: utf-8 -*-
"""M 단원 그림 바꾸기: C에서 다시 그린 같은 그림(plan.json) + 새로 그린 그림(mM_NN/out/widths.json, 키 iN=imageN)
   python3 apply.py NN   (u/mM_NN_prefig.hwpx → u/mM_NN.hwpx)"""
import sys, json, zipfile, glob, os, shutil, subprocess
S = '/tmp/claude-0/-home-user-CMS/7a122d51-a5b1-5def-9637-d43cb9a9b6ef/scratchpad'
u = sys.argv[1]; E = S + '/eqw'; W = '%s/mfig/mM_%s' % (S, u)
D = '/home/user/CMS/미적분Ⅰ_CLIMATH_C'
cf = [f for f in glob.glob(D + '/*.hwpx') if os.path.basename(f).startswith('%d. ' % int(u))][0]
pre = '%s/u/mM_%s_prefig.hwpx' % (E, u)
if not os.path.exists(pre):
    shutil.copy('%s/u/mM_%s.hwpx' % (E, u), pre)
plan = json.load(open(W + '/plan.json'))
os.makedirs(W + '/c', exist_ok=True)
zf = zipfile.ZipFile(cf)
args = []; used = {}
for k, v in plan.items():
    if v.get('redrawn') and v['f_href'].endswith('.png'):
        p = '%s/c/%s.png' % (W, k)
        open(p, 'wb').write(zf.read(v['f_href']))
        args.append('%s=%s@%d' % (k, p, v['f_w'])); used[k] = 'C'
nw = W + '/out/widths.json'
if os.path.exists(nw):
    for kk, w in json.load(open(nw)).items():
        k = 'image' + kk[1:]
        if k in used: print('!! 겹침', k)
        args = [a for a in args if not a.startswith(k + '=')]
        args.append('%s=%s/out/%s.png@%d' % (k, W, kk, w)); used[k] = 'new'
r = subprocess.run(['python3', '/home/user/CMS/.claude/skills/math-figure-rules/hwpx_swapimg.py', pre, '%s/u/mM_%s.hwpx' % (E, u)] + args, cwd=E, capture_output=True, text=True)
print(r.stdout[-500:], r.stderr[-500:])
subprocess.run(['python3', 'fix_lsa.py', 'u/mM_%s.hwpx' % u], cwd=E, capture_output=True)
print(u, '바꾼 그림: C', sum(1 for v in used.values() if v == 'C'), '새', sum(1 for v in used.values() if v == 'new'),
      '남은 새 그림', [k for k, v in plan.items() if 'c_n' not in v and k not in used])
