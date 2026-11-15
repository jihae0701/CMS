# -*- coding: utf-8 -*-
"""작업을 마치기 전 그림·구조 검사 (원본과 비교).
    python3 figcheck.py 원본.hwpx 결과.hwpx [그림목록.png]
- 그림 개수: 문제(q)·해설(sol)마다 원본과 같은지 (그림이 없어지면 실패)
- 그림 파일: content.hpf 등록, zip 안에 있음, 열림, 확장자와 형식이 맞음
- 바꿔 넣은 그림: 이동 값(offset·transMatrix)이 0인지 (남아 있으면 그림이 밖으로 밀려 안 보임)
- 크기: sz = curSz(글자처럼 취급), 0보다 큼, imgClip이 imgDim 안
- 문단: 모든 문단에 줄 배치 정보(linesegarray)가 있는지
- 압축: 원본과 같은 압축 방식인지 (mimetype은 맨 앞·무압축)
그림목록.png를 주면 모든 그림을 문항 번호와 함께 한 장에 모아 그린다(눈으로 확인용).
"""
import sys, os, re, io, zipfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hwpxedit import endnotes, all_paras
from PIL import Image, ImageDraw, ImageFont

PIC = re.compile(r'<hp:pic\b.*?</hp:pic>', re.S)
FMT = {'png': 'PNG', 'jpg': 'JPEG', 'jpeg': 'JPEG', 'bmp': 'BMP', 'gif': 'GIF'}


def signed(v):
    v = int(v)
    return v - (1 << 32) if v >= (1 << 31) else v


def pics(z):
    x = z.read('Contents/section0.xml').decode('utf-8')
    ens = endnotes(x)
    out = []
    for m in PIC.finditer(x):
        p = m.group(0)
        pos = m.start()
        k = sum(1 for s, e in ens if s <= pos)
        inside = any(s <= pos < e for s, e in ens)
        out.append({'pos': pos, 'n': k, 'part': 'sol' if inside else 'q', 'xml': p,
                    'img': (re.search(r'binaryItemIDRef="([^"]+)"', p) or [None, None])[1]})
    return x, out


def check(orig, res, sheet=None):
    zo, zr = zipfile.ZipFile(orig), zipfile.ZipFile(res)
    errs, notes = [], []
    xo, po = pics(zo)
    xr, pr = pics(zr)
    # 1) 개수
    from collections import Counter
    co = Counter((p['n'], p['part']) for p in po)
    cr = Counter((p['n'], p['part']) for p in pr)
    for key in sorted(set(co) | set(cr)):
        if co[key] != cr[key]:
            errs.append('그림 개수 다름: %d번 %s 원본 %d → 결과 %d' % (key[0], key[1], co[key], cr[key]))
    # 2) 그림 파일
    hpf = zr.read('Contents/content.hpf').decode('utf-8')
    names = set(zr.namelist())
    items = dict(re.findall(r'<opf:item id="([^"]+)" href="([^"]+)"', hpf))
    ohpf = zo.read('Contents/content.hpf').decode('utf-8')
    oitems = dict(re.findall(r'<opf:item id="([^"]+)" href="([^"]+)"', ohpf))
    for p in pr:
        k = p['img']
        if k is None:
            errs.append('%d번 %s: 그림 파일 참조 없음' % (p['n'], p['part'])); continue
        if k not in items or items[k] not in names:
            errs.append('%d번 %s: %s 파일 없음' % (p['n'], p['part'], k)); continue
        data = zr.read(items[k])
        try:
            im = Image.open(io.BytesIO(data)); im.load()
        except Exception as e:
            errs.append('%d번 %s: %s 열리지 않음 (%s)' % (p['n'], p['part'], k, e)); continue
        ext = items[k].rsplit('.', 1)[-1].lower()
        if FMT.get(ext) and FMT[ext] != im.format:
            errs.append('%d번 %s: %s 확장자 %s인데 형식 %s' % (p['n'], p['part'], k, ext, im.format))
        p['im'] = im
        changed = k not in oitems or oitems[k] != items[k] or zo.read(oitems[k]) != data
        p['changed'] = changed
        xml = p['xml']
        off = re.search(r'<hp:offset x="(\d+)" y="(\d+)"', xml)
        tm = re.search(r'<hc:transMatrix e1="[^"]*" e2="[^"]*" e3="([^"]*)" e4="[^"]*" e5="[^"]*" e6="([^"]*)"', xml)
        sca = re.search(r'<hc:scaMatrix e1="([^"]*)" e2="[^"]*" e3="([^"]*)" e4="[^"]*" e5="([^"]*)" e6="([^"]*)"', xml)
        ident = sca and float(sca.group(1)) == 1 and float(sca.group(3)) == 1 and float(sca.group(2)) == 0 and float(sca.group(4)) == 0
        grouped = re.search(r'groupLevel="(\d+)"', xml).group(1) != '0'
        if ident and not grouped:
            if off and (signed(off.group(1)) or signed(off.group(2))):
                errs.append('%d번 %s: %s 이동 값 offset=(%d,%d) 남음 → 그림이 밀려 안 보임' % (p['n'], p['part'], k, signed(off.group(1)), signed(off.group(2))))
            if tm and (float(tm.group(1)) or float(tm.group(2))):
                errs.append('%d번 %s: %s transMatrix 이동 (%s,%s) 남음 → 그림이 밀려 안 보임' % (p['n'], p['part'], k, tm.group(1), tm.group(2)))
        sz = re.search(r'<hp:sz width="(\d+)"[^>]*height="(\d+)"', xml)
        cs = re.search(r'<hp:curSz width="(\d+)" height="(\d+)"', xml)
        tac = 'treatAsChar="1"' in xml
        if sz and (int(sz.group(1)) <= 0 or int(sz.group(2)) <= 0) and not grouped:
            errs.append('%d번 %s: %s 크기 0' % (p['n'], p['part'], k))
        if tac and not grouped and sz and cs and sz.groups() != cs.groups():
            errs.append('%d번 %s: %s sz %s ≠ curSz %s' % (p['n'], p['part'], k, sz.groups(), cs.groups()))
        clip = re.search(r'<hp:imgClip left="(\d+)" right="(\d+)" top="(\d+)" bottom="(\d+)"', xml)
        dim = re.search(r'<hp:imgDim dimwidth="(\d+)" dimheight="(\d+)"', xml)
        if clip and dim and (int(clip.group(2)) > int(dim.group(1)) or int(clip.group(4)) > int(dim.group(2))):
            errs.append('%d번 %s: %s imgClip이 imgDim 밖' % (p['n'], p['part'], k))
        notes.append('%d번 %-3s %-7s %s %s %s' % (p['n'], p['part'], k, '바꿈' if changed else '    ', 'x'.join(sz.groups()) if sz else '?', '묶음' if grouped else ''))
    # 3) 문단 줄 배치 정보
    for name, zz in (('결과', zr),):
        for fn in [n for n in zz.namelist() if re.match(r'Contents/(section\d+|masterpage\d+)\.xml', n)]:
            x = zz.read(fn).decode('utf-8')
            miss = sum(1 for s, e in all_paras(x) if '<hp:linesegarray>' not in x[s:e] and x.find('<hp:p ', s + 5, e) < 0)
            if miss:
                errs.append('%s: 줄 배치 정보 없는 문단 %d개' % (fn, miss))
    # 4) 압축
    il = zr.infolist()
    if il[0].filename != 'mimetype' or il[0].compress_type != 0:
        errs.append('mimetype이 맨 앞·무압축이 아님')
    oc = {i.filename: i.compress_type for i in zo.infolist()}
    for i in il:
        exp = oc.get(i.filename, 0 if i.filename.startswith('BinData/') else 8)
        if i.compress_type != exp:
            errs.append('압축 방식 다름: %s (원본 %s, 결과 %s)' % (i.filename, exp, i.compress_type))
    # 그림 모음
    if sheet:
        cells = [p for p in pr if 'im' in p]
        W, cols, th = 1800, 3, 560
        cw = W // cols
        rows = (len(cells) + cols - 1) // cols
        S = Image.new('RGB', (W, max(1, rows) * (th + 40)), 'white')
        d = ImageDraw.Draw(S)
        try:
            font = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc', 26)
        except Exception:
            font = ImageFont.load_default()
        for i, p in enumerate(cells):
            r, c = divmod(i, cols)
            im = p['im'].convert('RGB')
            im.thumbnail((cw - 20, th - 10))
            S.paste(im, (c * cw + 10, r * (th + 40) + 36))
            d.text((c * cw + 10, r * (th + 40) + 4), '%d번 %s %s%s' % (p['n'], '문제' if p['part'] == 'q' else '해설', p['img'], ' (새로 그림)' if p.get('changed') else ''), fill='black', font=font)
        S.save(sheet)
    return errs, notes


if __name__ == '__main__':
    errs, notes = check(*sys.argv[1:4])
    for n in notes:
        print('  ', n)
    for e in errs:
        print('실패:', e)
    print('그림 검사', '통과' if not errs else '실패 %d' % len(errs))
    sys.exit(1 if errs else 0)
