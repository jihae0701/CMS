# -*- coding: utf-8 -*-
"""수식 속 붙여 쓴 집합·명제 기호 띄우기: capB → cap B, smallunionB → smallunion B, inA → in A, subsetQ → subset Q
    python3 setglue.py 파일.hwpx"""
import sys, re, zipfile, shutil
R = [(re.compile(r'\b(smallinter|smallunion)(?=[A-Za-z])'), r'\1 '),
     (re.compile(r'(?<=[0-9)])(right|RIGHT)(?=[^A-Za-z])'), r' \1'),
     (re.compile(r'\b(cap|cup|subset|supset|notin|in|IN|NOTIN|SUBSET|SUPSET|CAP|CUP)(?=[A-Z])'), r'\1 ')]
path = sys.argv[1]
z = zipfile.ZipFile(path); items = [(i, z.read(i.filename)) for i in z.infolist()]; z.close()
tot = 0
def fix(m):
    global tot
    s = m.group(2)
    if '\ue04d' in s:   # 글꼴 전용 문자(세로선) → |
        s = s.replace('\ue04d', '|'); tot += 1
    for r, rep in R:
        s, n = r.subn(rep, s); tot += n
    return m.group(1) + s + m.group(3)
with zipfile.ZipFile(path + '.tmp', 'w') as zo:
    for info, data in items:
        if re.match(r'Contents/(section\d+|masterpage\d+)\.xml', info.filename):
            data = re.sub(r'(<hp:script\b[^>]*>)(.*?)(</hp:script>)', fix, data.decode('utf-8'), flags=re.S).encode('utf-8')
        zo.writestr(info, data, compress_type=info.compress_type)
shutil.move(path + '.tmp', path)
print('기호 띄움', tot)
