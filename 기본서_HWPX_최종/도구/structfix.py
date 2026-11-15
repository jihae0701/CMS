"""기준 문서 약속: 첫 STEP 제목 '개념 확인하기', 쪽 번호 1로 시작, 미주(정답·해설) 수식 bold 제거.
python3 structfix.py 파일.hwpx 로그.json"""
import sys, os, re, html, json, zipfile, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, 'tools'))
import eqauto, eqstyle
path, logp = sys.argv[1:3]
z = zipfile.ZipFile(path); items = [(i, z.read(i.filename)) for i in z.infolist()]; z.close()
log = {'step': 0, 'newnum': 0, 'bold': []}
out = []
for info, data in items:
    if info.filename == 'Contents/section0.xml':
        x = data.decode('utf-8')
        # 1) STEP 제목: 첫 번째 STEP 상자의 제목은 '개념 확인하기', 두 번째는 '유형별 학습하기'
        steps = [m for m in re.finditer(r'<hp:t>STEP</hp:t>', x)]
        titles = [m for m in re.finditer(r'<hp:t>(유형별 학습하기|개념 확인하기)</hp:t>', x)]
        if titles and titles[0].group(1) != '개념 확인하기':
            m = titles[0]; x = x[:m.start()] + '<hp:t>개념 확인하기</hp:t>' + x[m.end():]; log['step'] += 1
        # 2) 쪽 번호 새로 시작 → 1
        x, n = re.subn(r'(<hp:newNum num=")\d+(" numType="PAGE"/>)', r'\g<1>1\2', x); log['newnum'] = n
        # 3) 미주 안 수식의 bold 제거
        ends = [(m.start(), x.find('</hp:endNote>', m.start())) for m in re.finditer(r'<hp:endNote\b', x)]
        plan = []
        for m in eqauto.EQPAT.finditer(x):
            if not any(a < m.start() < b for a, b in ends):
                continue
            sm = eqauto.SCPAT.search(m.group(0)); sc = html.unescape(sm.group(2))
            if re.search('bold', sc, re.I):
                new = re.sub(r'\s*bold\s*', ' ', sc, flags=re.I).strip()
                plan.append((m, sm, sc, new))
        EQ = eqstyle.sizes([p[3] for p in plan]) if plan else {}
        o = []; last = 0
        for m, sm, sc, new in plan:
            o.append(x[last:m.start()]); el = m.group(0)
            el = el[:sm.start(2)] + eqstyle.esc(new) + el[sm.end(2):]
            o.append(eqauto.resize(el, new, EQ)); last = m.end(); log['bold'].append([sc, new])
        o.append(x[last:]); x = ''.join(o)
        data = x.encode('utf-8')
    out.append((info, data))
tmp = path + '.tmp'
with zipfile.ZipFile(tmp, 'w') as zo:
    for info, data in out:
        zo.writestr(info, data, compress_type=(zipfile.ZIP_STORED if info.filename == 'mimetype' else zipfile.ZIP_DEFLATED))
shutil.move(tmp, path)
json.dump(log, open(logp, 'w'), ensure_ascii=False, indent=0)
print(os.path.basename(path), 'step', log['step'], 'newnum', log['newnum'], 'bold', len(log['bold']))
