# -*- coding: utf-8 -*-
"""글 조각 하나뿐인 함수 이름(g, f, h)과 바로 뒤 수식 '(t)=…', \"'(t)…\"가 갈라진 것을 한 수식으로 합친다: T'g' E'(t)=…' → E'g(t)=…'
    python3 mergeletter.py 파일.hwpx"""
import sys, os, re, html
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, 'tools'))
import hwpxedit as H, eqauto, eqstyle
path = sys.argv[1]
x = H.load(path)
pat = re.compile(r'<hp:t>([fgh])</hp:t>(<hp:equation\b[^>]*>.*?</hp:equation>)', re.S)
plan = []
def rep(m):
    el = m.group(2); sm = H.SC.search(el)
    sc = html.unescape(sm.group(2)) if sm else ''
    if not re.match(r"\s*[('`]", sc):
        return m.group(0)
    new = m.group(1) + sc.lstrip()
    plan.append(new)
    return '<hp:t/>' + el[:sm.start(2)] + eqstyle.esc(new) + el[sm.end(2):]
x2 = pat.sub(rep, x)
if plan:
    EQ = eqstyle.sizes(plan)
    x2 = H.EQ.sub(lambda m: eqauto.resize(m.group(0), html.unescape(H.SC.search(m.group(0)).group(2)), EQ) if H.SC.search(m.group(0)) and html.unescape(H.SC.search(m.group(0)).group(2)) in plan else m.group(0), x2)
H.save(path, x2)
print(os.path.basename(path), '글자+수식 합침', len(plan), plan[:4])
