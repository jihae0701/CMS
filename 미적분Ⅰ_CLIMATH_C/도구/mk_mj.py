# -*- coding: utf-8 -*-
"""미적분Ⅰ: 기준(1단원 완성본)의 틀을 다른 단원에 입힌다.
    python3 mk_mj.py 기준.hwpx 단원.hwpx 출력.hwpx 번호 "단원 이름"
- 맨 앞 가로줄 노트 표 12개(6쪽): 기준 첫 문단(구역 설정 + 표 12개)을 그대로 복사하고 구역 설정만 대상 것으로.
  대상의 첫 문단(STEP 1 제목 상자)은 구역 설정을 떼고 새 쪽에서 시작(기준과 같게)
- 용지 여백: 기준과 같게
- 바탕쪽: 기준 바탕쪽을 통째로 쓰고 '1. 함수의 극한'만 '번호. 이름'으로
- 쪽 번호 새로 시작 값: 모두 1
표·바탕쪽이 쓰는 테두리·글자·문단 모양은 대상 header에 같은 것이 있으면 쓰고 없으면 덧붙인다(make_unit.HeaderImport)."""
import sys, re, zipfile
from xml.sax.saxutils import escape as esc
from lxml import etree
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from make_unit import HeaderImport, write_header, remap_refs, top_paras, SECRUN


def build(base, target, out, num, name):
    bz, tz = zipfile.ZipFile(base), zipfile.ZipFile(target)
    bx = bz.read('Contents/section0.xml').decode('utf-8')
    tx = tz.read('Contents/section0.xml').decode('utf-8')
    hi = HeaderImport(etree.fromstring(bz.read('Contents/header.xml')), etree.fromstring(tz.read('Contents/header.xml')))
    log = {}
    # 여백
    bm = re.search(r'<hp:margin [^>]*/>', bx).group(0)
    tx, log['margin'] = re.subn(r'<hp:margin [^>]*/>', bm, tx, count=1)
    # 노트 표
    if len(re.findall(r'<hp:tbl\b[^>]*rowCnt="28" colCnt="1"', tx)) >= 12:
        log['note_tables'] = 'already'
    else:
        bp = top_paras(bx)
        p0 = bx[bp[0][0]:bp[0][1]]
        assert len(re.findall(r'<hp:tbl\b[^>]*rowCnt="28" colCnt="1"', p0)) == 12, '기준 첫 문단에 노트 표 12개가 없음'
        assert len(re.findall(SECRUN, p0, flags=re.S)) == 1
        p0 = re.sub(SECRUN, '{SEC}', p0, count=1, flags=re.S)
        p0 = remap_refs(p0, hi)
        m = re.search(SECRUN, tx, flags=re.S)
        assert m, '대상 첫 문단의 구역 설정을 찾지 못함'
        sec = m.group(0)
        tx = tx[:m.start()] + tx[m.end():]
        a, b = top_paras(tx)[0]
        first = tx[a:b]
        assert '<hp:container' in first, '대상 첫 문단에 STEP 1 제목 상자가 없음'
        first = re.sub(r'(<hp:p\b[^>]*?)pageBreak="0"', r'\1pageBreak="1"', first, count=1)
        tx = tx[:a] + p0.replace('{SEC}', sec) + first + tx[b:]
        log['note_tables'] = 12
    # 쪽 번호
    tx, log['newnum'] = re.subn(r'(<hp:newNum num=")\d+(" numType="PAGE"/>)', r'\g<1>1\2', tx)
    # 바탕쪽
    mps = {}
    for mname in [n for n in bz.namelist() if re.match(r'Contents/masterpage\d+\.xml', n)]:
        m = remap_refs(bz.read(mname).decode('utf-8'), hi)
        assert m.count('<hp:t>1. 함수의 극한</hp:t>') == 1, mname
        m = m.replace('<hp:t>1. 함수의 극한</hp:t>', '<hp:t>%s</hp:t>' % esc('%s. %s' % (num, name)))
        mps[mname] = m.encode('utf-8')
        log[mname] = re.findall(r'<hp:t>([^<]*)</hp:t>', m)
    items = [(i, tz.read(i.filename)) for i in tz.infolist()]
    tnames = set(tz.namelist())
    with zipfile.ZipFile(out, 'w') as zo:
        for info, data in items:
            if info.filename == 'Contents/section0.xml':
                data = tx.encode('utf-8')
            elif info.filename == 'Contents/header.xml':
                data = write_header(tz.read('Contents/header.xml').decode('utf-8'), hi.added).encode('utf-8')
            elif info.filename in mps:
                data = mps[info.filename]
            zo.writestr(info, data, compress_type=info.compress_type)
        for mname in mps:
            assert mname in tnames, ('대상에 바탕쪽 파일이 없음', mname)
    log['header_imports'] = {k: len(v) for k, v in hi.maps.items() if v}
    return log


if __name__ == '__main__':
    import json
    print(json.dumps(build(*sys.argv[1:6]), ensure_ascii=False))
