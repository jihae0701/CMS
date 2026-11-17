# -*- coding: utf-8 -*-
"""글꼴을 CLIMATH 기준으로: 문제 본문 글꼴 나눔명조 → 하는체 Regular(글자 모양의 글꼴 참조를 바꿈), 수식 글꼴 → HancomEQN
   python3 fontfix.py 파일.hwpx 기준.hwpx"""
import sys, re, zipfile, shutil
P, BASE = sys.argv[1], sys.argv[2]
FROM, TO = '나눔명조', '하는체 Regular'
bh = zipfile.ZipFile(BASE).read('Contents/header.xml').decode()
z = zipfile.ZipFile(P); items = [(i, z.read(i.filename)) for i in z.infolist()]; z.close()
D = {i.filename: d for i, d in items}
h = D['Contents/header.xml'].decode(); s = D['Contents/section0.xml'].decode()
LANGS = re.findall(r'<hh:fontface lang="(\w+)"', h)
def face_body(hh, lang):
    m = re.search(r'(<hh:fontface lang="%s" fontCnt=")(\d+)("[^>]*>)(.*?)(</hh:fontface>)' % lang, hh, re.S); return m
fid_from, fid_to = {}, {}
for lang in LANGS:
    m = face_body(h, lang)
    ids = dict((n, i) for i, n in re.findall(r'<hh:font id="(\d+)" face="([^"]+)"', m.group(4)))
    if FROM in ids: fid_from[lang] = ids[FROM]
    if TO not in ids:
        bm = face_body(bh, lang)
        bdef = re.search(r'<hh:font id="\d+" face="%s".*?</hh:font>' % re.escape(TO), bm.group(4), re.S)
        if not bdef: continue
        new = int(m.group(2))
        el = re.sub(r'id="\d+"', 'id="%d"' % new, bdef.group(0), count=1)
        h = h[:m.start()] + m.group(1) + str(new + 1) + m.group(3) + m.group(4) + el + m.group(5) + h[m.end():]
        ids[TO] = str(new)
    fid_to[lang] = ids[TO]
cnt = 0
def fix_cp(mm):
    global cnt
    cp = mm.group(0)
    fr = re.search(r'<hh:fontRef ([^/]*)/>', cp)
    refs = dict(re.findall(r'(\w+)="(\d+)"', fr.group(1)))
    changed = False
    for lang in LANGS:
        k = lang.lower()
        if k in refs and lang in fid_from and refs[k] == fid_from[lang] and lang in fid_to:
            refs[k] = fid_to[lang]; changed = True
    if not changed: return cp
    cnt += 1
    newfr = '<hh:fontRef %s/>' % ' '.join('%s="%s"' % (k, v) for k, v in refs.items())
    return cp.replace(fr.group(0), newfr)
h = re.sub(r'<hh:charPr id="\d+".*?</hh:charPr>', fix_cp, h, flags=re.S)
s, neq = re.subn(r'(<hp:equation [^>]*font=")(?!HancomEQN")[^"]*(")', r'\1HancomEQN\2', s)
D['Contents/header.xml'] = h.encode(); D['Contents/section0.xml'] = s.encode()
tmp = P + '.tmp'
with zipfile.ZipFile(tmp, 'w') as zo:
    for i, _ in items:
        zo.writestr(i, D[i.filename], compress_type=i.compress_type)
shutil.move(tmp, P)
print(P.split('/')[-1], '글자 모양 %s→%s %d개, 수식 글꼴→HancomEQN %d개' % (FROM, TO, cnt, neq))
