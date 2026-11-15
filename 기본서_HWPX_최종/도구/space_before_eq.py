# -*- coding: utf-8 -*-
"""수식 바로 앞 글이 '집합/점/직선/선분/원' 등 이름 낱말로 끝나 붙어 있으면 한 칸 띄운다.
    python3 space_before_eq.py 파일.hwpx"""
import sys, re, zipfile, shutil
WORDS = '집합|점|직선|선분|원|중점|함수|두 점|세 점'
pat = re.compile(r'(<hp:t>[^<]*?(?:^|[ ,(])(?:%s))(</hp:t>)(?=<hp:equation)' % WORDS)
pat2 = re.compile(r'(<hp:t>(?:%s))(</hp:t>)(?=<hp:equation)' % WORDS)
path = sys.argv[1]
z = zipfile.ZipFile(path); items = [(i, z.read(i.filename)) for i in z.infolist()]; z.close()
n = 0
with zipfile.ZipFile(path + '.tmp', 'w') as zo:
    for info, data in items:
        if info.filename == 'Contents/section0.xml':
            t = data.decode('utf-8')
            t, a = pat.subn(r'\1 \2', t)
            t, b = pat2.subn(r'\1 \2', t)
            n = a + b
            data = t.encode('utf-8')
        zo.writestr(info, data, compress_type=info.compress_type)
shutil.move(path + '.tmp', path)
print('수식 앞 띄움', n)
