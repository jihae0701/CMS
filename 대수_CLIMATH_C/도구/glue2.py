# -*- coding: utf-8 -*-
"""수식 속 명령 뒤에 바로 붙은 글자 띄우기: times3 → times 3, timeslim → times lim, cdot5 → cdot 5, cdotscdots → cdots cdots,
leqx → leq x, ge1 → ge 1, thereforea → therefore a  (바뀐 수식 크기 다시 잼)
    python3 glue2.py 파일.hwpx"""
import sys, os, re, html, zipfile, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, 'tools'))
import eqauto, eqstyle
R = [(re.compile(r'(?<![A-Za-z])(times|TIMES|therefore|THEREFORE|leq|geq|LEQ|GEQ)(?=[0-9A-Za-z])'), r'\1 '),
     (re.compile(r'(?<![A-Za-z])(cdots|CDOTS)(?=[0-9A-Za-z])'), r'\1 '),
     (re.compile(r'(?<![A-Za-z])(cdot|CDOT)(?=[0-9])'), r'\1 '),
     (re.compile(r'(?<![A-Za-z])(le|ge)(?=[0-9])'), r'\1 '),
     (re.compile(r'(?<=[0-9])(leq|geq|LEQ|GEQ|cdot|CDOT|times|TIMES|alpha|beta|lim)(?![A-Za-z])'), r' \1'),   # 3times → 3 times
     (re.compile(r'\^\{(\d+)`\}'), r'^{\1}'),                                                      # x^{3`} → x^{3}
     (re.compile(r'ㆍ|⋅'), ' cdot '),
     (re.compile(r'(?<![A-Za-z])(DELTA|Delta|delta)(?=[A-Za-z0-9])'), r'\1 ')]   # DELTAx → DELTA x
ARR = re.compile(r'\s*`*\s*(->|(?<![A-Za-z])rarrow|(?<![A-Za-z])RARROW|→)\s*`*\s*(it\s*)?')
def arrows(sc):
    """lim 아래첨자 밖의 화살표(x→a일 때)를 'x``->``a'로, 끝의 INF → inf (bold 제목은 그대로)"""
    if re.search(r'bold', sc):
        return sc
    out = []; i = 0
    for m in re.finditer(r'lim _\{[^{}]*\}', sc):
        out.append(('t', sc[i:m.start()])); out.append(('l', m.group(0))); i = m.end()
    out.append(('t', sc[i:]))
    res = ''
    for k, t in out:
        if k == 't':
            t = ARR.sub('``->``', t)
            t = re.sub(r'(``->``\s*-?)\s*INF', r'\1inf', t)
            t = re.sub(r'``->``\s+', '``->``', t)
        res += t
    return res
def fix(sc):
    for p, r in R:
        sc = p.sub(r, sc)
    sc = arrows(sc)
    return re.sub(r'  +', ' ', sc) if '  ' in sc and False else sc
path = sys.argv[1]
z = zipfile.ZipFile(path); items = [(i, z.read(i.filename)) for i in z.infolist()]; z.close()
out = []; n = 0
for info, data in items:
    if info.filename == 'Contents/section0.xml':
        x = data.decode('utf-8'); plan = []
        for m in eqauto.EQPAT.finditer(x):
            sm = eqauto.SCPAT.search(m.group(0))
            if not sm: continue
            sc = html.unescape(sm.group(2)); new = fix(sc)
            if new != sc: plan.append((m, sm, new)); print(' ', sc[:70], '->', new[:70])
        EQ = eqstyle.sizes([p[2] for p in plan]) if plan else {}
        o = []; last = 0
        for m, sm, new in plan:
            o.append(x[last:m.start()]); el = m.group(0)
            el = el[:sm.start(2)] + eqstyle.esc(new) + el[sm.end(2):]
            o.append(eqauto.resize(el, new, EQ)); last = m.end()
        o.append(x[last:]); x = ''.join(o); n = len(plan)
        data = x.encode('utf-8')
    out.append((info, data))
with zipfile.ZipFile(path + '.tmp', 'w') as zo:
    for info, data in out: zo.writestr(info, data, compress_type=info.compress_type)
shutil.move(path + '.tmp', path); print(os.path.basename(path), 'glue', n)
