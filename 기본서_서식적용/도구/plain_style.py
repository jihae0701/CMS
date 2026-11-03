"""해설(미주)의 존댓말 끝맺음(-입니다/-합니다 …)을 -이다/-한다 체로 바꾼다. python3 plain_style.py 파일.hwp ... (제자리)"""
import sys, re, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hwpedit as H
RULES = [('입니다', '이다'), ('않습니다', '않는다'), ('같습니다', '같다'), ('있습니다', '있다'), ('없습니다', '없다'),
         ('합니다', '한다'), ('됩니다', '된다'), ('지납니다', '지난다'), ('가집니다', '가진다'), ('만납니다', '만난다'),
         ('나옵니다', '나온다'), ('구합니다', '구한다')]
WORD = re.compile('(' + '|'.join(re.escape(a) for a, _ in RULES) + ')')
def conv(s):
    return WORD.sub(lambda m: dict(RULES)[m.group(1)], s)
SEG = re.compile(r'⟦.*?⟧|\{[a-z ]+\}')
log = []
for f in sys.argv[1:]:
    d = H.Doc(f)
    cnt = 0
    while True:
        hit = None
        for n, ps in d.regions()['sol'].items():
            for p in ps:
                t = p.text()
                # 수식·개체 밖의 글 조각
                pos = 0
                for piece in SEG.split(t):
                    if WORD.search(piece):
                        hit = (n, p, t, piece)
                        break
                if hit:
                    break
            if hit:
                break
        if not hit:
            break
        n, p, t, piece = hit
        old = piece
        if t.count(old) != 1:
            # 조각이 여러 번 나오면 문단 전체를 수식 그대로 두고 통째로 바꾼다
            old = t
            new = SEG.sub(lambda m: m.group(0), t)
            parts = SEG.split(t); toks = SEG.findall(t)
            new = ''.join(conv(a) + (toks[i] if i < len(toks) else '') for i, a in enumerate(parts))
        else:
            new = conv(piece)
        d._replace_in(p, old, new)
        log.append((os.path.basename(f), n, piece.strip()[-40:], conv(piece).strip()[-40:]))
        cnt += 1
    d.save(f)
    print(os.path.basename(f), cnt)
import json
json.dump(log, open(os.environ.get('STYLE_LOG', '/dev/null'), 'w'), ensure_ascii=False, indent=0)
