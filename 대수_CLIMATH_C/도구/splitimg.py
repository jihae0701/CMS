# -*- coding: utf-8 -*-
"""한 그림 파일을 여러 그림 개체가 같이 쓰면(잘라 쓴 경우) 2번째부터 새 그림 파일로 나눈다.
    python3 splitimg.py 입력.hwpx 출력.hwpx image8 [image9 ...]
새 이름(imageN)을 출력한다. 나눈 뒤 hwpx_swapimg.py로 하나씩 바꿀 수 있다."""
import zipfile, re, sys
src, out = sys.argv[1:3]
z = zipfile.ZipFile(src); items = [(i, z.read(i.filename)) for i in z.infolist()]
hpf = z.read('Contents/content.hpf').decode(); sec = z.read('Contents/section0.xml').decode()
used = set(int(n) for n in re.findall(r'id="image(\d+)"', hpf))
nxt = max(used) + 1
add = []
for k in sys.argv[3:]:
    line = re.search(r'<opf:item id="%s" href="([^"]+)"[^>]*/>' % k, hpf)
    href = line.group(1); ext = href.rsplit('.', 1)[1]
    data = z.read(href)
    cnt = [0]
    def fix(m):
        global nxt
        p = m.group(0)
        if 'binaryItemIDRef="%s"' % k not in p:
            return p
        cnt[0] += 1
        if cnt[0] == 1:
            print(k, '1번째 그대로'); return p
        nk = 'image%d' % nxt; nxt += 1
        nl = line.group(0).replace('id="%s"' % k, 'id="%s"' % nk).replace(href, 'BinData/%s.%s' % (nk, ext))
        add.append((nl, 'BinData/%s.%s' % (nk, ext), data))
        print(k, '%d번째 ->' % cnt[0], nk)
        return p.replace('binaryItemIDRef="%s"' % k, 'binaryItemIDRef="%s"' % nk)
    sec = re.sub(r'<hp:pic\b.*?</hp:pic>', fix, sec, flags=re.S)
for nl, _, _ in add:
    hpf = hpf.replace(line.group(0) if False else '</opf:manifest>', nl + '</opf:manifest>', 1)
with zipfile.ZipFile(out, 'w') as zo:
    for info, data in items:
        if info.filename == 'Contents/content.hpf': data = hpf.encode()
        elif info.filename == 'Contents/section0.xml': data = sec.encode()
        zo.writestr(info, data, compress_type=info.compress_type)
    for _, fn, data in add:
        zi = zipfile.ZipInfo(fn, date_time=(2026, 11, 15, 0, 0, 0)); zi.compress_type = zipfile.ZIP_STORED
        zo.writestr(zi, data)
