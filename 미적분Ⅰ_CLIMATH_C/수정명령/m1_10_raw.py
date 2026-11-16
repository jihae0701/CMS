# -*- coding: utf-8 -*-
"""10단원 수식 도구로 안 되는 곳: 12 문제 쉼표·괄호, 26 문제 겹친 S"""
import zipfile, shutil, re, sys
p = sys.argv[1]
EQ = r'<hp:equation (?:(?!</hp:equation>).)*?<hp:script>%s</hp:script></hp:equation>'
zi = zipfile.ZipFile(p); t = p + '.tmp'; zo = zipfile.ZipFile(t, 'w')
for i in zi.infolist():
    d = zi.read(i.filename)
    if i.filename == 'Contents/section0.xml':
        s = d.decode()
        def rep(pat, new, flags=re.S):
            global s
            m = list(re.finditer(pat, s, flags))
            assert len(m) == 1, (pat[:80], len(m))
            s = s[:m[0].start()] + m[0].expand(new) + s[m[0].end():]
        rep(r'(-ax  \^\{2\}</hp:script></hp:equation>)<hp:t> </hp:t>', r'\1<hp:t>, </hp:t>')
        rep(r'(의 값을 구하시오\. )</hp:t>' + EQ % r'\(' + r'<hp:t>단, ', r'\1(단, ')
        rep(r'(<hp:script>0&lt;a&lt;1</hp:script></hp:equation>)' + EQ % r'\)', r'\1<hp:t>)</hp:t>')
        rep(r'(<hp:t>가 </hp:t>)' + EQ % '`S' + r'(?=<hp:equation (?:(?!</hp:equation>).)*?<hp:script>\{q\} over \{p\})', r'\1')
        d = s.encode()
    zo.writestr(i, d, compress_type=i.compress_type)
zo.close(); shutil.move(t, p)
print('raw ok')
