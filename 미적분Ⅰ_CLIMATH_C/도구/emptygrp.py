# -*- coding: utf-8 -*-
"""수식 속 빈 묶음 정리: lim 아래첨자 뒤 '{}', 끝에 남은 '{ }' 지움 (eqauto 괄호 짝 맞춤 뒤에 남는 것)
    python3 emptygrp.py 파일.hwpx"""
import sys, os, re, html, zipfile, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, 'tools'))
import eqauto, eqstyle
path = sys.argv[1]
z = zipfile.ZipFile(path); items = [(i, z.read(i.filename)) for i in z.infolist()]; z.close()
out = []; n = 0
for info, data in items:
    if info.filename == 'Contents/section0.xml':
        x = data.decode(); plan = []
        for m in eqauto.EQPAT.finditer(x):
            sm = eqauto.SCPAT.search(m.group(0))
            if not sm: continue
            sc = html.unescape(sm.group(2))
            new = re.sub(r'lim _\{eqalign\{([^{}#]*)#\r?\n\}\}', r'lim _{\1}', sc)
            new = re.sub(r'(lim _\{[^{}]*\})\s*\{\s*\}\s*', r'\1 ', new)
            new = re.sub(r'\s*\{\s*\}(?=\s*(\}|$|=|\s))', '', new)
            if new != sc:
                new = re.sub(r'  +', ' ', new).strip(); plan.append((m, sm, new))
        EQ = eqstyle.sizes([p[2] for p in plan]) if plan else {}
        o = []; last = 0
        for m, sm, new in plan:
            o.append(x[last:m.start()]); el = m.group(0); el = el[:sm.start(2)] + eqstyle.esc(new) + el[sm.end(2):]
            o.append(eqauto.resize(el, new, EQ)); last = m.end()
        o.append(x[last:]); data = ''.join(o).encode(); n = len(plan)
    out.append((info, data))
with zipfile.ZipFile(path + '.tmp', 'w') as zo:
    for info, data in out: zo.writestr(info, data, compress_type=info.compress_type)
shutil.move(path + '.tmp', path); print(os.path.basename(path), 'empty groups', n)
