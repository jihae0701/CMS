# -*- coding: utf-8 -*-
"""해설·문제의 "-입니다/-습니다" 끝맺음을 "-이다/-다"로 맞춘다 (줄 배치 위치도 맞춤).
    python3 style_ida.py 파일.hwpx"""
import sys, re, zipfile, shutil, html
import hwpxedit as H

MAP = [('일대일 대응', '일대일대응'), ('개다.', '개이다.'), ('일치합니다', '일치한다'), ('있습니다', '있다'), ('않습니다', '않는다'), ('같습니다', '같다'),
       ('합니다', '한다'), ('지납니다', '지난다'), ('가집니다', '가진다'), ('됩니다', '된다'), ('입니다', '이다')]


def run(x):
    log = []
    for old, new in MAP:
        while True:
            ms = [m for m in H.TPAT.finditer(x) if old in m.group(1)]
            if not ms:
                break
            m = ms[0]
            ctx = html.unescape(re.sub(r'<[^>]+>', '', m.group(1)))
            x = H.op_text(x, [(m.start(), m.end())], old, new) if m.group(1).count(old) == 1 else \
                x[:m.start()] + '<hp:t>' + m.group(1).replace(old, new) + '</hp:t>' + x[m.end():]
            H._PCACHE.clear()
            log.append(ctx.strip()[-30:])
    return x, log


if __name__ == '__main__':
    path = sys.argv[1]
    z = zipfile.ZipFile(path)
    items = [(i, z.read(i.filename)) for i in z.infolist()]
    z.close()
    with zipfile.ZipFile(path + '.tmp', 'w') as zo:
        for info, data in items:
            if info.filename == 'Contents/section0.xml':
                t, log = run(data.decode('utf-8'))
                data = t.encode('utf-8')
                for l in log:
                    print('  ', l)
                print('끝맺음 고침', len(log))
            zo.writestr(info, data, compress_type=info.compress_type)
    shutil.move(path + '.tmp', path)
