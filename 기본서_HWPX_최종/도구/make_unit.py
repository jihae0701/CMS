# -*- coding: utf-8 -*-
"""기준 문서(1. 다항식의 연산, 사용자가 한글로 만든 HWPX)의 틀을 다른 단원 HWPX에 입힌다.
    python3 make_unit.py 기준.hwpx 단원.hwpx 출력.hwpx
- 용지 여백: 기준 문서와 같게
- 바탕쪽: 개체 위치·글 영역 높이를 기준 문서와 같게, 쪽 번호(자동 번호) 지움
- 맨 앞에 가로줄 노트 표 12개(6쪽): 기준 문서의 표를 그대로 복사(표가 쓰는 테두리·글꼴·글자·문단 모양은 같은 것이 있으면 쓰고 없으면 덧붙임)
- 쪽 번호 새로 시작: STEP 2 첫 제목 문단과 문서 끝 문단에도 넣음(기준 문서와 같은 자리). 값은 structfix.py가 1로 맞춘다.
"""
import sys, re, copy, zipfile, random
from lxml import etree

NS = {'hh': 'http://www.hancom.co.kr/hwpml/2011/head', 'hp': 'http://www.hancom.co.kr/hwpml/2011/paragraph',
      'hc': 'http://www.hancom.co.kr/hwpml/2011/core'}
HH = '{%s}' % NS['hh']; HP = '{%s}' % NS['hp']
LANGS = {'hangul': 'HANGUL', 'latin': 'LATIN', 'hanja': 'HANJA', 'japanese': 'JAPANESE', 'other': 'OTHER', 'symbol': 'SYMBOL', 'user': 'USER'}


def canon(el):
    e = copy.deepcopy(el)
    e.attrib.pop('id', None)
    return etree.tostring(e)


class HeaderImport:
    def __init__(self, bh, th):
        self.B, self.T = bh, th
        self.maps = {'borderFill': {}, 'charPr': {}, 'paraPr': {}, 'tabPr': {}, 'font': {}}

    def lst(self, root, name):
        return root.find('.//hh:%s' % name, NS)

    def _import(self, kind, listname, bid, fix):
        if bid in self.maps[kind]:
            return self.maps[kind][bid]
        src = self.lst(self.B, listname).find('hh:%s[@id="%s"]' % (kind, bid), NS)
        new = copy.deepcopy(src)
        fix(new)
        tl = self.lst(self.T, listname)
        c = canon(new)
        for e in tl.findall('hh:%s' % kind, NS):
            if canon(e) == c:
                self.maps[kind][bid] = e.get('id')
                return e.get('id')
        nid = str(max(int(e.get('id')) for e in tl.findall('hh:%s' % kind, NS)) + 1)
        new.set('id', nid)
        tl.append(new)
        tl.set('itemCnt', str(len(tl.findall('hh:%s' % kind, NS))))
        self.maps[kind][bid] = nid
        return nid

    def borderFill(self, bid):
        return self._import('borderFill', 'borderFills', bid, lambda e: None)

    def font(self, lang, fid):
        key = (lang, fid)
        if key in self.maps['font']:
            return self.maps['font'][key]
        bf = self.B.find('.//hh:fontface[@lang="%s"]/hh:font[@id="%s"]' % (lang, fid), NS)
        tff = self.T.find('.//hh:fontface[@lang="%s"]' % lang, NS)
        for f in tff.findall('hh:font', NS):
            if f.get('face') == bf.get('face'):
                self.maps['font'][key] = f.get('id'); return f.get('id')
        new = copy.deepcopy(bf)
        nid = str(len(tff.findall('hh:font', NS)))
        new.set('id', nid); tff.append(new); tff.set('fontCnt', str(len(tff.findall('hh:font', NS))))
        self.maps['font'][key] = nid
        return nid

    def charPr(self, cid):
        def fix(e):
            fr = e.find('hh:fontRef', NS)
            for k, lang in LANGS.items():
                if fr is not None and fr.get(k) is not None:
                    fr.set(k, self.font(lang, fr.get(k)))
            if e.get('borderFillIDRef'):
                e.set('borderFillIDRef', self.borderFill(e.get('borderFillIDRef')))
        return self._import('charPr', 'charProperties', cid, fix)

    def tabPr(self, tid):
        return self._import('tabPr', 'tabProperties', tid, lambda e: None)

    def paraPr(self, pid):
        def fix(e):
            if e.get('tabPrIDRef') is not None:
                e.set('tabPrIDRef', self.tabPr(e.get('tabPrIDRef')))
            for b in e.iter(HH + 'border'):
                if b.get('borderFillIDRef'):
                    b.set('borderFillIDRef', self.borderFill(b.get('borderFillIDRef')))
            h = e.find('hh:heading', NS)
            assert h is None or h.get('type') == 'NONE', 'paraPr에 번호 문단(heading)이 있음'
        return self._import('paraPr', 'paraProperties', pid, fix)


def remap_refs(s, hi):
    s = re.sub(r'borderFillIDRef="(\d+)"', lambda m: 'borderFillIDRef="%s"' % hi.borderFill(m.group(1)), s)
    s = re.sub(r'paraPrIDRef="(\d+)"', lambda m: 'paraPrIDRef="%s"' % hi.paraPr(m.group(1)), s)
    s = re.sub(r'charPrIDRef="(\d+)"', lambda m: 'charPrIDRef="%s"' % hi.charPr(m.group(1)), s)
    s = re.sub(r'styleIDRef="\d+"', 'styleIDRef="0"', s)
    s = re.sub(r'(<hp:tbl\b[^>]*\bid=")\d+(")', lambda m: m.group(1) + str(random.randint(1000000000, 2000000000)) + m.group(2), s)
    return s


def top_paras(x):
    """section0의 최상위 <hp:p> 범위 목록"""
    out, depth, start = [], 0, None
    for m in re.finditer(r'<(/?)hp:p\b[^>]*?(/?)>', x):
        if m.group(2) == '/':
            continue
        if m.group(1) == '':
            if depth == 0:
                start = m.start()
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                out.append((start, m.end()))
    return out


SECRUN = r'<hp:run charPrIDRef="\d+"><hp:secPr\b.*?</hp:secPr><hp:ctrl><hp:colPr[^>]*/></hp:ctrl></hp:run>'
LSA = r'<hp:linesegarray>.*?</hp:linesegarray>'


def note_tables(bx):
    """기준 문서 맨 앞 노트 표: (첫 문단 틀 — 구역 설정 자리 {SEC}, 표 1개),
    (둘째 문단의 표 11개 run, 둘째 문단 linesegarray). 둘째 문단에는 STEP 1 제목 상자가 함께 있다."""
    paras = top_paras(bx)
    p0 = bx[paras[0][0]:paras[0][1]]
    p1 = bx[paras[1][0]:paras[1][1]]
    assert len(re.findall(r'<hp:tbl\b[^>]*rowCnt="28" colCnt="1"', p0)) == 1
    p0 = re.sub(SECRUN, '{SEC}', p0, count=1, flags=re.S)
    assert '{SEC}' in p0
    m = re.match(r'<hp:p\b[^>]*>(<hp:run charPrIDRef="\d+">(?:<hp:tbl\b.*?</hp:tbl>)+</hp:run>)', p1, re.S)
    run = m.group(1)
    assert len(re.findall(r'<hp:tbl\b[^>]*rowCnt="28" colCnt="1"', run)) == 11
    assert '<hp:container' in p1[m.end():]
    return p0, run, re.search(LSA, p1, re.S).group(0)


def build(base, target, out):
    bz, tz = zipfile.ZipFile(base), zipfile.ZipFile(target)
    bx = bz.read('Contents/section0.xml').decode('utf-8')
    tx = tz.read('Contents/section0.xml').decode('utf-8')
    bh = etree.fromstring(bz.read('Contents/header.xml'))
    th = etree.fromstring(tz.read('Contents/header.xml'))
    hi = HeaderImport(bh, th)
    log = {}
    # 1) 여백
    bm = re.search(r'<hp:margin [^>]*/>', bx).group(0)
    tx, n = re.subn(r'<hp:margin [^>]*/>', bm, tx, count=1); log['margin'] = n
    # 2) 노트 표: 대상 첫 문단의 secPr·colPr run을 떼어 노트 표 첫 문단으로 옮김
    m = re.search(SECRUN, tx, flags=re.S)
    assert m, '대상 첫 문단의 구역 설정을 찾지 못함'
    secrun = m.group(0)
    tx = tx[:m.start()] + tx[m.end():]
    a, b = top_paras(tx)[0]
    first = tx[a:b]
    assert '<hp:container' in first, '대상 첫 문단에 STEP 1 제목 상자가 없음'
    p0, run, lsa1 = note_tables(bx)
    p0 = remap_refs(p0, hi).replace('{SEC}', secrun)
    run = remap_refs(run, hi)
    head = re.match(r'<hp:p\b[^>]*>', first).group(0)
    first = head + run + first[len(head):]
    first = re.sub(LSA, lambda _: lsa1, first, count=1, flags=re.S)
    tx = tx[:a] + p0 + first + tx[b:]
    tables = [1] * len(re.findall(r'<hp:tbl\b[^>]*rowCnt="28" colCnt="1"', p0 + run))
    log['note_tables'] = len(tables)
    # 3) 쪽 번호 새로 시작: STEP 2 첫 제목 문단, 문서 끝 문단 (없을 때만)
    NEW = '<hp:ctrl><hp:newNum num="1" numType="PAGE"/></hp:ctrl>'
    paras = top_paras(tx)
    steps = [mm.start() for mm in re.finditer(r'<hp:t>STEP</hp:t>', tx)]
    added = 0
    targets = []
    if len(steps) >= 2:
        k = next(i for i, (a, b) in enumerate(paras) if a <= steps[1] < b)
        if k + 1 < len(paras):
            targets.append(paras[k + 1])
    targets.append(paras[-1])
    for a, b in sorted(targets, reverse=True):
        p = tx[a:b]
        if 'numType="PAGE"' in p:
            continue
        r = re.search(r'<hp:run charPrIDRef="\d+">', p)
        if r:
            p = p[:r.end()] + NEW + p[r.end():]
        else:
            p = re.sub(r'(<hp:p\b[^>]*>)', r'\1<hp:run charPrIDRef="0">' + NEW + '</hp:run>', p, count=1)
        tx = tx[:a] + p + tx[b:]
        added += 1
    log['newnum_added'] = added
    # 4) 바탕쪽
    mps = {}
    for name in [n for n in tz.namelist() if re.match(r'Contents/masterpage\d+\.xml', n)]:
        tr = etree.fromstring(tz.read(name))
        br = etree.fromstring(bz.read(name))
        def objs(r):
            sl = r.find(HP + 'subList'); res = []
            for p in sl.findall(HP + 'p'):
                for run in p.findall(HP + 'run'):
                    for o in run:
                        if etree.QName(o).localname in ('tbl', 'line', 'rect', 'container', 'pic', 'ellipse', 'polygon', 'curve', 'arc'):
                            res.append(o)
            return sl, res
        bsl, bo = objs(br); tsl, to = objs(tr)
        bpos = {}
        for o in bo:
            sz = o.find(HP + 'sz'); bpos[(etree.QName(o).localname, sz.get('width'), sz.get('height'))] = o.find(HP + 'pos')
        moved = 0
        for o in to:
            sz = o.find(HP + 'sz'); key = (etree.QName(o).localname, sz.get('width'), sz.get('height'))
            if key in bpos:
                pos = o.find(HP + 'pos')
                for att in ('vertOffset', 'horzOffset', 'vertRelTo', 'horzRelTo', 'vertAlign', 'horzAlign'):
                    pos.set(att, bpos[key].get(att))
                moved += 1
        for att in ('textWidth', 'textHeight'):
            tsl.set(att, bsl.get(att))
        removed = 0
        for c in list(tr.iter(HP + 'ctrl')):
            if c.find(HP + 'autoNum') is not None and c.find(HP + 'autoNum').get('numType') == 'PAGE':
                c.getparent().remove(c); removed += 1
        mps[name] = etree.tostring(tr, xml_declaration=True, encoding='UTF-8', standalone=True)
        log[name] = {'moved': moved, 'objs': len(to), 'pagenum_removed': removed}
    # 쓰기
    items = [(i, tz.read(i.filename)) for i in tz.infolist()]
    with zipfile.ZipFile(out, 'w') as zo:
        for info, data in items:
            if info.filename == 'Contents/section0.xml':
                data = tx.encode('utf-8')
            elif info.filename == 'Contents/header.xml':
                data = etree.tostring(th, xml_declaration=True, encoding='UTF-8', standalone=True)
            elif info.filename in mps:
                data = mps[info.filename]
            zo.writestr(info, data, compress_type=info.compress_type)
    log['header_imports'] = {k: {str(a): b for a, b in v.items()} for k, v in hi.maps.items() if v}
    return log


if __name__ == '__main__':
    import json
    print(json.dumps(build(*sys.argv[1:4]), ensure_ascii=False, default=str))
