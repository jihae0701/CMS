# -*- coding: utf-8 -*-
"""M 단원의 그림을 C 원본 그림과 맞대어, C에서 다시 그린 그림을 그대로 쓸 수 있는지 찾는다.
   python3 figmatch.py NN  → mfig/mM_NN/plan.json"""
import sys, re, io, json, zipfile, glob, os
sys.path.insert(0, '/tmp/claude-0/-home-user-CMS/7a122d51-a5b1-5def-9637-d43cb9a9b6ef/scratchpad/eqw')
import hwpxedit as H
from PIL import Image
S = '/tmp/claude-0/-home-user-CMS/7a122d51-a5b1-5def-9637-d43cb9a9b6ef/scratchpad'
u = sys.argv[1]
D = '/home/user/CMS/미적분Ⅰ_CLIMATH_C'
cfinal = [f for f in glob.glob(D + '/*.hwpx') if os.path.basename(f).startswith('%d. ' % int(u))][0]
PIC = re.compile(r'<hp:pic\b.*?</hp:pic>', re.S)

def pics(path):
    x = H.load(path); z = zipfile.ZipFile(path)
    hpf = z.read('Contents/content.hpf').decode()
    href = dict(re.findall(r'<opf:item id="([^"]+)" href="([^"]+)"', hpf))
    out = []
    n = 1
    while True:
        try:
            q = H.region(x, n, 'q')
        except Exception:
            break
        if not q: break
        for part in ('q', 'sol'):
            k = 0
            for a, b in H.region(x, n, part):
                for m in PIC.finditer(x, a, b):
                    p = m.group(0)
                    iid = re.search(r'binaryItemIDRef="([^"]+)"', p).group(1)
                    cw = int(re.search(r'<hp:curSz width="(\d+)"', p).group(1)) or int(re.search(r'<hp:sz width="(\d+)"', p).group(1))
                    if '정답.png' in p: continue
                    out.append(dict(n=n, part=part, k=k, id=iid, w=cw, href=href.get(iid)))
                    k += 1
        n += 1
    return out, z

def sig(z, href):
    try:
        im = Image.open(io.BytesIO(z.read(href))).convert('L')
    except Exception:
        return None
    w, h = im.size
    return (w / h, list(im.resize((24, 24)).getdata()))

def dist(a, b):
    if a is None or b is None: return 9e9
    ar = abs(a[0] - b[0]) / max(a[0], b[0])
    return sum(abs(p - q) for p, q in zip(a[1], b[1])) / 576 + 200 * ar

M, zm = pics(("%s/eqw/u/mM_%s_prefig.hwpx" if os.path.exists("%s/eqw/u/mM_%s_prefig.hwpx" % (S, u)) else "%s/eqw/u/mM_%s.hwpx") % (S, u))
C, zc = pics('%s/in2/m1_%s.hwpx' % (S, u))
F, zf = pics(cfinal)
cs = [(c, sig(zc, c['href'])) for c in C]
fpos = {(f['n'], f['part'], f['k']): f for f in F}
plan = {}
for m in M:
    if m['id'] in plan: continue
    s = sig(zm, m['href'])
    best = min(cs, key=lambda t: dist(s, t[1])) if cs else None
    d = dist(s, best[1]) if best else 9e9
    ent = dict(n=m['n'], part=m['part'], href=m['href'], w=m['w'], d=round(d, 1))
    if best and d < 5:
        c = best[0]; f = fpos.get((c['n'], c['part'], c['k']))
        ent.update(c_n=c['n'], c_part=c['part'], c_href=c['href'])
        if f:
            ent.update(f_href=f['href'], f_w=f['w'], redrawn=f['href'] != c['href'] or f['href'].endswith('.png'))
    plan[m['id']] = ent
os.makedirs('%s/mfig/mM_%s' % (S, u), exist_ok=True)
json.dump(plan, open('%s/mfig/mM_%s/plan.json' % (S, u), 'w'), ensure_ascii=False, indent=0)
nm = sum(1 for v in plan.values() if 'c_n' in v); nr = sum(1 for v in plan.values() if v.get('redrawn'))
print(u, 'M 그림', len(plan), 'C와 같음', nm, '그중 C에서 다시 그림', nr, '새 그림', len(plan) - nm)
