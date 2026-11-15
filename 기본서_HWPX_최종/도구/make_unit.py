# -*- coding: utf-8 -*-
"""기준 문서(1. 다항식의 연산, 사용자가 한글로 만든 HWPX)의 틀을 다른 단원 HWPX에 입힌다.
    python3 make_unit.py 기준.hwpx 단원.hwpx 출력.hwpx
- 용지 여백: 기준 문서와 같게
- 바탕쪽: 기준 문서의 바탕쪽을 그대로 쓰고 단원 번호·제목, 과목(공통수학1/2)만 바꿈 (기준 문서에는 쪽 번호가 없음)
- 맨 앞에 가로줄 노트 표 12개(6쪽): 기준 문서의 표를 그대로 복사(표가 쓰는 테두리·글꼴·글자·문단 모양은 같은 것이 있으면 쓰고 없으면 덧붙임)
- 끝의 정답 모음(정답 줄을 모아 놓은 부분)은 지운다(기준 문서에는 없음)
- 쪽 번호 새로 시작: STEP 2 첫 제목 문단과 문서 끝 문단에도 넣음(기준 문서와 같은 자리). 값은 structfix.py가 1로 맞춘다.
"""
import sys, re, copy, zipfile, random
from xml.sax.saxutils import escape as eqesc
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
        self.added = []  # (목록 이름, 언어, 새 요소) — header.xml 글에 그대로 끼워 넣는다

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
        self.added.append((listname, None, new))
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
        self.added.append(('fontface', lang, new))
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


def write_header(text, added):
    """header.xml을 다시 쓰지 않고 원래 글에 새 항목만 끼워 넣고 개수를 고친다(한글이 쓴 형식 그대로 유지)"""
    ITEM = {'borderFills': 'borderFill', 'charProperties': 'charPr', 'paraProperties': 'paraPr', 'tabProperties': 'tabPr'}
    for listname, lang, el in added:
        frag = etree.tostring(el, encoding='unicode')
        frag = re.sub(r'\s+xmlns:\w+="[^"]*"', '', frag)
        if listname == 'fontface':
            m = re.search(r'<hh:fontface lang="%s" fontCnt="\d+">' % lang, text)
            end = text.index('</hh:fontface>', m.end())
        else:
            end = text.index('</hh:%s>' % listname)
        text = text[:end] + frag + text[end:]
    for listname, item in ITEM.items():
        m = re.search(r'(<hh:%s itemCnt=")\d+(">)(.*?)</hh:%s>' % (listname, listname), text, re.S)
        if m:
            n = len(re.findall(r'<hh:%s id=' % item, m.group(3)))
            text = text[:m.start()] + m.group(1) + str(n) + m.group(2) + text[m.end(2):]
    for m in list(re.finditer(r'(<hh:fontface lang="\w+" fontCnt=")\d+(">)(.*?)</hh:fontface>', text, re.S)):
        pass
    out, last = [], 0
    for m in re.finditer(r'(<hh:fontface lang="\w+" fontCnt=")\d+(">)(.*?)(</hh:fontface>)', text, re.S):
        out.append(text[last:m.start()]); out.append(m.group(1) + str(len(re.findall(r'<hh:font id=', m.group(3)))) + m.group(2) + m.group(3) + m.group(4)); last = m.end()
    out.append(text[last:])
    return ''.join(out)


def shift_own_lineseg(p, delta, after=0):
    """문단 p 자기 줄 배치 정보(맨 끝 linesegarray)에서 글자 위치 > after 인 줄을 delta만큼 민다"""
    k = p.rfind('<hp:linesegarray>')
    if k < 0 or p.find('</hp:run>', k) >= 0:
        return p
    tail = re.sub(r'textpos="(\d+)"', lambda m: 'textpos="%d"' % (int(m.group(1)) + delta if int(m.group(1)) > after else int(m.group(1))), p[k:])
    return p[:k] + tail


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
    k = p1.rfind('<hp:linesegarray>')
    own = p1[k:p1.index('</hp:linesegarray>', k) + len('</hp:linesegarray>')]
    assert own.count('<hp:lineseg ') == 12, own.count('<hp:lineseg ')
    return p0, run, own


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
    k = first.rfind('<hp:linesegarray>')
    k2 = first.index('</hp:linesegarray>', k) + len('</hp:linesegarray>')
    assert first.find('</hp:run>', k) < 0
    first = first[:k] + lsa1 + first[k2:]   # 문단 자기 줄 배치 정보(표 11개 + 제목 상자 = 줄 12개)
    tx = tx[:a] + p0 + first + tx[b:]
    tables = [1] * len(re.findall(r'<hp:tbl\b[^>]*rowCnt="28" colCnt="1"', p0 + run))
    log['note_tables'] = len(tables)
    # 2b) 끝의 정답 모음(제목 상자 뒤 "번호 󰂼 정답" 줄들) 지우기 — 기준 문서에는 없음. 빈 문단 하나로 바꾼다
    paras = top_paras(tx)
    ans = [i for i, (a, b) in enumerate(paras) if re.search(r'<hp:autoNum num="\d+" numType="ENDNOTE"', tx[a:b]) and '<hp:endNote' not in tx[a:b]]
    # 정답 모음 = 맨 끝까지 이어지는 '미주 번호가 붙은 문단' 묶음 (정답 기호가 󰂼, [정답], 없음 어느 것이든)
    while ans and ans[-1] == len(paras) - 1 and len(ans) >= 2 and ans[-2] == ans[-1] - 1:
        break
    tail = []
    for i in reversed(range(len(paras))):
        if i in ans:
            tail.append(i)
        else:
            break
    ans = sorted(tail)
    log['answer_list_removed'] = 0
    if ans:
        i0 = ans[0]
        assert ans == list(range(i0, len(paras))), ('정답 모음 뒤에 다른 문단이 있음', ans[:3], len(paras))
        pa = tx[paras[i0 - 1][0]:paras[i0 - 1][1]]   # 바로 앞 = 제목 상자 문단
        head = re.match(r'<hp:p\b[^>]*>', pa).group(0)
        head = re.sub(r'pageBreak="1"', 'pageBreak="0"', head)
        cp = re.findall(r'<hp:run charPrIDRef="(\d+)">', pa)[-1]
        ls = re.search(r'<hp:lineseg\b[^>]*/>', tx[paras[i0][0]:paras[i0][1]]).group(0)
        empty = head + '<hp:run charPrIDRef="%s"><hp:t/></hp:run><hp:linesegarray>%s</hp:linesegarray></hp:p>' % (cp, re.sub(r'textpos="\d+"', 'textpos="0"', ls))
        tx = tx[:paras[i0][0]] + empty + tx[paras[-1][1]:]
        log['answer_list_removed'] = len(ans)
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
        r = re.match(r'<hp:p\b[^>]*><hp:run charPrIDRef="\d+">', p)
        if r:
            p = p[:r.end()] + NEW + p[r.end():]
        else:
            p = re.sub(r'(<hp:p\b[^>]*>)', r'\1<hp:run charPrIDRef="0">' + NEW + '</hp:run>', p, count=1)
        p = shift_own_lineseg(p, 8, after=0)  # 맨 앞에 8글자(컨트롤)가 늘어남
        tx = tx[:a] + p + tx[b:]
        added += 1
    log['newnum_added'] = added
    # 4) 바탕쪽: 기준 문서의 바탕쪽을 통째로 쓰고, 단원 번호·제목과 과목(공통수학1/2)만 바꾼다
    t0 = re.findall(r'<hp:t>([^<]*)</hp:t>', tz.read('Contents/masterpage0.xml').decode('utf-8'))
    i0 = t0.index('HF') + 1 if 'HF' in t0 else 0
    i1 = next(i for i in range(i0, len(t0)) if t0[i].startswith('공통수학'))
    title = ''.join(t0[i0:i1]).strip()
    num, _, name = title.partition(' ')
    subj = '2' if any('공통수학2' in t for t in t0) or (t0[i1:i1 + 3] == ['공통수학', ' ', '2']) else '1'
    log['title'] = [num, name, '공통수학' + subj]
    mps = {}
    for mname in [n for n in bz.namelist() if re.match(r'Contents/masterpage\d+\.xml', n)]:
        m = bz.read(mname).decode('utf-8')
        m = remap_refs(m, hi)
        n1 = m.count('<hp:t>1.</hp:t>'); n2 = m.count('<hp:t>다항식의 연산</hp:t>')
        assert n1 == 1 and n2 == 1, (mname, n1, n2)
        m = m.replace('<hp:t>1.</hp:t>', '<hp:t>%s</hp:t>' % eqesc(num)).replace('<hp:t>다항식의 연산</hp:t>', '<hp:t>%s</hp:t>' % eqesc(name))
        if subj == '2':
            m = m.replace('<hp:t>공통수학1</hp:t>', '<hp:t>공통수학2</hp:t>')
            m = re.sub(r'(<hp:t>공통수학</hp:t></hp:run><hp:run charPrIDRef="\d+"><hp:t> </hp:t></hp:run><hp:run charPrIDRef="\d+"><hp:t>)1(</hp:t>)', r'\g<1>2\2', m)
        assert '<hp:autoNum' not in m
        mps[mname] = m.encode('utf-8')
        log[mname] = re.findall(r'<hp:t>([^<]*)</hp:t>', m)
    # 쓰기
    items = [(i, tz.read(i.filename)) for i in tz.infolist()]
    with zipfile.ZipFile(out, 'w') as zo:
        for info, data in items:
            if info.filename == 'Contents/section0.xml':
                data = tx.encode('utf-8')
            elif info.filename == 'Contents/header.xml':
                data = write_header(tz.read('Contents/header.xml').decode('utf-8'), hi.added).encode('utf-8')
            elif info.filename in mps:
                data = mps[info.filename]
            zo.writestr(info, data, compress_type=info.compress_type)
    log['header_imports'] = {k: {str(a): b for a, b in v.items()} for k, v in hi.maps.items() if v}
    return log


if __name__ == '__main__':
    import json
    print(json.dumps(build(*sys.argv[1:4]), ensure_ascii=False, default=str))
