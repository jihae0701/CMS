# -*- coding: utf-8 -*-
"""HWPX 문서 일관성 검사 (한글 '손상' 경고 원인 찾기)
    python3 refcheck.py 파일.hwpx
- header의 목록 itemCnt = 실제 개수, id가 빠짐없이 이어지는지
- section/masterpage의 charPrIDRef·paraPrIDRef·borderFillIDRef·styleIDRef가 header에 있는지
- charPr의 fontRef가 언어별 글꼴 개수 안인지, paraPr의 tabPrIDRef, style의 paraPr/charPr 참조
- 개체 id(tbl, pic, equation, rect, container, line, ellipse) 중복
- 줄 배치 정보 없는 문단, 빈 run 이상
"""
import sys, re, zipfile, collections

OBJ = r'<hp:(tbl|pic|equation|rect|container|line|ellipse|polygon|arc|curve|ole|textart|connectLine)\b'


def para_len(seg):
    """문단 자기 글자 수(안쪽 문단 빼고): 글자·줄바꿈 1, 탭 8, 개체·컨트롤 8"""
    # 안쪽 문단(표 칸, 글상자, 미주) 내용 지우기
    out, depth, last = [], 0, 0
    body = seg[seg.find('>') + 1:]
    for m in re.finditer(r'<(/?)hp:subList\b[^>]*?(/?)>', body):
        if m.group(2) == '/':
            continue
        if m.group(1) == '':
            if depth == 0:
                out.append(body[last:m.start()])
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                last = m.end()
    out.append(body[last:])
    b = ''.join(out)
    n = 0
    for t in re.findall(r'<hp:t>(.*?)</hp:t>', b, re.S):
        t = re.sub(r'<hp:tab\b[^>]*/>', 'X' * 8, t)
        t = re.sub(r'<hp:lineBreak/>', 'X', t)
        n += len(re.sub(r'<[^>]+>', '', re.sub(r'&[a-z]+;|&#\d+;', 'X', t)))
    n += 8 * len(re.findall(OBJ, b))
    n += 8 * len(re.findall(r'<hp:ctrl>', b))
    n += 8 * len(re.findall(r'<hp:secPr\b', b))
    return n


def lineseg_overflow(x):
    bad, stack = [], []
    for m in re.finditer(r'<(/?)hp:p\b[^>]*?(/?)>', x):
        if m.group(2) == '/':
            continue
        if m.group(1) == '':
            stack.append(m.start())
        else:
            s = stack.pop()
            seg = x[s:m.end()]
            k = seg.rfind('<hp:linesegarray>')
            if k < 0 or seg.find('</hp:run>', k) >= 0:
                continue
            tps = [int(v) for v in re.findall(r'textpos="(\d+)"', seg[k:])]
            if tps and max(tps) > 0 and max(tps) > para_len(seg[:k]):
                bad.append(s)
    return bad


def main(path):
    z = zipfile.ZipFile(path)
    h = z.read('Contents/header.xml').decode('utf-8')
    errs = []
    lists = {'borderFills': 'borderFill', 'charProperties': 'charPr', 'paraProperties': 'paraPr', 'tabProperties': 'tabPr',
             'styles': 'style', 'numberings': 'numbering', 'bullets': 'bullet'}
    ids = {}
    for L, item in lists.items():
        m = re.search(r'<hh:%s itemCnt="(\d+)">(.*?)</hh:%s>' % (L, L), h, re.S)
        if not m:
            continue
        got = re.findall(r'<hh:%s id="(\d+)"' % item, m.group(2))
        ids[item] = set(got)
        if int(m.group(1)) != len(got):
            errs.append('%s itemCnt %s ≠ 실제 %d' % (L, m.group(1), len(got)))
        nums = sorted(map(int, got))
        if nums and nums != list(range(nums[0], nums[0] + len(nums))):
            errs.append('%s id가 이어지지 않음 (%s…)' % (L, nums[:3]))
    fonts = {}
    for m in re.finditer(r'<hh:fontface lang="(\w+)" fontCnt="(\d+)">(.*?)</hh:fontface>', h, re.S):
        got = re.findall(r'<hh:font id="(\d+)"', m.group(3))
        fonts[m.group(1)] = len(got)
        if int(m.group(2)) != len(got):
            errs.append('fontface %s fontCnt %s ≠ %d' % (m.group(1), m.group(2), len(got)))
        if sorted(map(int, got)) != list(range(len(got))):
            errs.append('fontface %s id가 0부터 이어지지 않음' % m.group(1))
    LANG = {'hangul': 'HANGUL', 'latin': 'LATIN', 'hanja': 'HANJA', 'japanese': 'JAPANESE', 'other': 'OTHER', 'symbol': 'SYMBOL', 'user': 'USER'}
    for m in re.finditer(r'<hh:charPr id="(\d+)".*?</hh:charPr>', h, re.S):
        fr = re.search(r'<hh:fontRef ([^>]*)/>', m.group(0))
        for k, v in re.findall(r'(\w+)="(\d+)"', fr.group(1)):
            if int(v) >= fonts.get(LANG[k], 0):
                errs.append('charPr %s fontRef %s=%s 글꼴 없음' % (m.group(1), k, v))
        bf = re.search(r'borderFillIDRef="(\d+)"', m.group(0))
        if bf and bf.group(1) not in ids['borderFill']:
            errs.append('charPr %s borderFill %s 없음' % (m.group(1), bf.group(1)))
    for m in re.finditer(r'<hh:paraPr id="(\d+)"[^>]*tabPrIDRef="(\d+)".*?</hh:paraPr>', h, re.S):
        if m.group(2) not in ids['tabPr']:
            errs.append('paraPr %s tabPr %s 없음' % (m.group(1), m.group(2)))
        for bf in re.findall(r'borderFillIDRef="(\d+)"', m.group(0)):
            if bf not in ids['borderFill']:
                errs.append('paraPr %s borderFill %s 없음' % (m.group(1), bf))
        hd = re.search(r'<hh:heading type="(\w+)" idRef="(\d+)"', m.group(0))
        if hd and hd.group(1) in ('NUMBER', 'OUTLINE') and hd.group(2) != '0' and hd.group(2) not in ids.get('numbering', set()):
            errs.append('paraPr %s numbering %s 없음' % (m.group(1), hd.group(2)))
        if hd and hd.group(1) == 'BULLET' and hd.group(2) not in ids.get('bullet', set()):
            errs.append('paraPr %s bullet %s 없음' % (m.group(1), hd.group(2)))
    for m in re.finditer(r'<hh:style id="(\d+)"[^>]*paraPrIDRef="(\d+)" charPrIDRef="(\d+)"', h):
        if m.group(2) not in ids['paraPr'] or m.group(3) not in ids['charPr']:
            errs.append('style %s 참조 없음' % m.group(1))
    names = [n for n in z.namelist() if re.match(r'Contents/(section\d+|masterpage\d+)\.xml', n)]
    oid = collections.Counter()
    for n in names:
        x = z.read(n).decode('utf-8')
        for attr, item in (('charPrIDRef', 'charPr'), ('paraPrIDRef', 'paraPr'), ('borderFillIDRef', 'borderFill'), ('styleIDRef', 'style')):
            bad = collections.Counter(v for v in re.findall(r'\b%s="(\d+)"' % attr, x) if v not in ids[item])
            if bad:
                errs.append('%s: %s 없는 번호 %s' % (n, attr, dict(bad)))
        for m in re.finditer(r'<hp:(tbl|pic|equation|rect|container|line|ellipse|polygon|arc|curve)\b[^>]*?\bid="(\d+)"', x):
            if m.group(2) != '0':
                oid[m.group(2)] += 1
        miss = 0
        for m in re.finditer(r'<hp:p\b[^>]*>', x):
            pass
        # 문단 깊이 스택으로 줄 배치 정보 확인
        stack = []
        for m in re.finditer(r'<(/?)hp:p\b[^>]*?(/?)>', x):
            if m.group(2) == '/':
                continue
            if m.group(1) == '':
                stack.append(m.start())
            else:
                s = stack.pop()
                seg = x[s:m.end()]
                inner = seg.rfind('</hp:run>')
                if '<hp:linesegarray>' not in seg[inner if inner > 0 else 0:]:
                    miss += 1
        if miss:
            errs.append('%s: 줄 배치 정보 없는 문단 %d' % (n, miss))
        bad = lineseg_overflow(x)
        if bad:
            errs.append('%s: 줄 배치 정보의 글자 위치가 문단 글자 수를 넘는 문단 %d (첫 위치 %d)' % (n, len(bad), bad[0]))
    d = {k: v for k, v in oid.items() if v > 1}
    if d:
        errs.append('개체 id 중복 %d개 (%s)' % (len(d), list(d.items())[:5]))
    hp = z.read('Contents/content.hpf').decode('utf-8')
    for href in re.findall(r'href="([^"]+)"', hp):
        if href not in z.namelist():
            errs.append('content.hpf의 %s 파일 없음' % href)
    for e in errs:
        print('  ', e)
    print(path.split('/')[-1], '문제', len(errs))
    return errs


if __name__ == '__main__':
    for p in sys.argv[1:]:
        main(p)
