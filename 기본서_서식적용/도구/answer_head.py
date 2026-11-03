"""정답 줄 머리의 정답 기호(U+F00BC)를 글자 [정답]으로 바꾼다. python3 answer_head.py 파일.hwp ... (제자리)"""
import sys, re, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hwpedit as H
SYM = '\U000f00bc'
PAT = re.compile(r'^((?:\s|\{gso\}|\{nwno\})*\{atno\}\s*)' + SYM)
for f in sys.argv[1:]:
    d = H.Doc(f)
    done = 0; left = []
    while True:
        reg = d.regions()
        ps = [ps_[0] for ps_ in reg['sol'].values() if ps_] + list(reg['end'].values())
        target = None
        for p in ps:
            m = PAT.match(p.text())
            if m:
                target = (p, m.group(0), m.group(1) + '[정답]')
                break
        if not target:
            break
        d._replace_in(*target)
        done += 1
    reg = d.regions()
    for n, ps_ in reg['sol'].items():
        if ps_ and '[정답]' not in ps_[0].text():
            left.append(('sol', n, ps_[0].text()[:40]))
    for n, p in reg['end'].items():
        if '[정답]' not in p.text():
            left.append(('end', n, p.text()[:40]))
    d.save(f)
    print(os.path.basename(f), '바꿈', done, '남은 줄', len(left), left[:4])
