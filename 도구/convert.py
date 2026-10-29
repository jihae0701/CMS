# -*- coding: utf-8 -*-
"""고친 단원(section0)을 기본 양식(header·쪽 머리말·용지 설정)으로 옮겨 HWPX로 묶는다.
python3 convert.py 원본폴더 고친section 그림json 양식폴더 출력.hwpx 단원번호 단원이름"""
import sys, os, re, copy, json, zipfile
from lxml import etree

HP = '{http://www.hancom.co.kr/hwpml/2011/paragraph}'
HH = '{http://www.hancom.co.kr/hwpml/2011/head}'
HC = '{http://www.hancom.co.kr/hwpml/2011/core}'
OPF = '{http://www.idpf.org/2007/opf/}'

ODIR, SEC, FIGJSON, FDIR, OUT, UNO, UNAME = sys.argv[1:8]
FONT_SUB = {'나눔명조': '하는체 Regular'}       # 문제 본문 글꼴: 양식 글꼴로
SUBTITLE_COLOR = '#315F97'                      # 개념 소제목 글자색(양식)

P = etree.XMLParser(remove_blank_text=False, huge_tree=True)
oh = etree.parse(f'{ODIR}/Contents/header.xml', P).getroot()
fh_tree = etree.parse(f'{FDIR}/Contents/header.xml', P)
fh = fh_tree.getroot()
sec_tree = etree.parse(SEC, P)
sec = sec_tree.getroot()


def canon(el):
    e = copy.deepcopy(el)
    e.attrib.pop('id', None)
    return etree.tostring(e, encoding='unicode')


def lst(root, name):
    return root.find(f'{HH}refList/{HH}{name}')


# ---------------------------------------------------------------- 글꼴
LANG = {'hangul': 'HANGUL', 'latin': 'LATIN', 'hanja': 'HANJA', 'japanese': 'JAPANESE', 'other': 'OTHER',
        'symbol': 'SYMBOL', 'user': 'USER'}
ffo = {ff.get('lang'): ff for ff in lst(oh, 'fontfaces')}
fff = {ff.get('lang'): ff for ff in lst(fh, 'fontfaces')}
font_map = {}   # (lang, oid) -> fid


def font_id(lang, face, src_el=None):
    ff = fff[lang]
    for f in ff.findall(HH + 'font'):
        if f.get('face') == face:
            return f.get('id')
    # 양식에 없으면 원본 정의를 복사해 붙임
    if src_el is None:
        for l2, ff2 in fff.items():
            for f in ff2.findall(HH + 'font'):
                if f.get('face') == face:
                    src_el = f
        assert src_el is not None, face
    n = copy.deepcopy(src_el)
    nid = str(len(ff.findall(HH + 'font')))
    n.set('id', nid)
    ff.append(n)
    ff.set('fontCnt', str(len(ff.findall(HH + 'font'))))
    return nid


for lang, ff in ffo.items():
    for f in ff.findall(HH + 'font'):
        face = FONT_SUB.get(f.get('face'), f.get('face'))
        font_map[(lang, f.get('id'))] = font_id(lang, face, f if face == f.get('face') else None)


# ---------------------------------------------------------------- 공통 매핑 도우미
def merge(name, child, translate):
    """원본 목록 name의 항목을 양식 목록으로: 같은 것이 있으면 그 id, 없으면 덧붙임"""
    fl = lst(fh, name)
    have = {}
    for e in fl.findall(HH + child):
        have.setdefault(canon(e), e.get('id'))
    m = {}
    for e in lst(oh, name).findall(HH + child):
        t = translate(copy.deepcopy(e))
        c = canon(t)
        if c in have:
            m[e.get('id')] = have[c]
        else:
            nid = str(max([int(x.get('id')) for x in fl.findall(HH + child)] + [-1]) + 1)
            t.set('id', nid)
            fl.append(t)
            have[c] = nid
            m[e.get('id')] = nid
    fl.set('itemCnt', str(len(fl.findall(HH + child))))
    return m


bf_map = merge('borderFills', 'borderFill', lambda e: e)


def tr_char(e):
    fr = e.find(HH + 'fontRef')
    for a, lang in LANG.items():
        fr.set(a, font_map[(lang, fr.get(a))])
    if e.get('borderFillIDRef') is not None:
        e.set('borderFillIDRef', bf_map[e.get('borderFillIDRef')])
    # 개념 소제목(나눔스퀘어 굵게 검정 10pt) -> 양식 색
    han = fff['HANGUL'].find(f"{HH}font[@id='{fr.get('hangul')}']").get('face')
    if han == '나눔스퀘어' and e.find(HH + 'bold') is not None and e.get('textColor') == '#000000' and e.get('height') == '1000':
        e.set('textColor', SUBTITLE_COLOR)
    return e


cp_map = merge('charProperties', 'charPr', tr_char)
tab_map = merge('tabProperties', 'tabPr', lambda e: e)


def tr_num(e):
    for ph in e.iter(HH + 'paraHead'):
        c = ph.get('charPrIDRef')
        if c in cp_map:
            ph.set('charPrIDRef', cp_map[c])
    return e


num_map = merge('numberings', 'numbering', tr_num)
bul_map = merge('bullets', 'bullet', tr_num) if lst(oh, 'bullets') is not None and lst(fh, 'bullets') is not None else {}


def tr_para(e):
    e.set('tabPrIDRef', tab_map[e.get('tabPrIDRef')])
    h = e.find(HH + 'heading')
    if h is not None and h.get('type') == 'NUMBER':
        h.set('idRef', num_map[h.get('idRef')])
    elif h is not None and h.get('type') == 'BULLET':
        h.set('idRef', bul_map[h.get('idRef')])
    for b in e.iter(HH + 'border'):
        if b.get('borderFillIDRef') is not None:
            b.set('borderFillIDRef', bf_map[b.get('borderFillIDRef')])
    return e


pp_map = merge('paraProperties', 'paraPr', tr_para)

# 스타일: 이름으로 맞추고 없으면 덧붙임
fst = lst(fh, 'styles')
fnames = {s.get('name'): s.get('id') for s in fst.findall(HH + 'style')}
st_map = {}
for s in lst(oh, 'styles').findall(HH + 'style'):
    if s.get('name') in fnames:
        st_map[s.get('id')] = fnames[s.get('name')]
    else:
        n = copy.deepcopy(s)
        nid = str(len(fst.findall(HH + 'style')))
        n.set('id', nid)
        n.set('paraPrIDRef', pp_map[s.get('paraPrIDRef')])
        n.set('charPrIDRef', cp_map[s.get('charPrIDRef')])
        n.set('nextStyleIDRef', nid)
        fst.append(n)
        fnames[s.get('name')] = nid
        st_map[s.get('id')] = nid
fst.set('itemCnt', str(len(fst.findall(HH + 'style'))))

# ---------------------------------------------------------------- 본문 id 바꾸기
MAPS = {'charPrIDRef': cp_map, 'paraPrIDRef': pp_map, 'styleIDRef': st_map, 'borderFillIDRef': bf_map}
for el in sec.iter():
    if not isinstance(el.tag, str):
        continue
    for a, m in MAPS.items():
        v = el.get(a)
        if v is not None:
            assert v in m, (el.tag, a, v)
            el.set(a, m[v])

# 줄 배치 정보(옛 글꼴 기준)는 지워서 한글이 다시 계산하게 한다
for la in list(sec.iter(HP + 'linesegarray')):
    la.getparent().remove(la)

# 용지·여백·머리말 설정은 양식 것으로
fsec = etree.parse(f'{FDIR}/Contents/section0.xml', P).getroot()
f_secpr = next(fsec.iter(HP + 'secPr'))
o_secpr = next(sec.iter(HP + 'secPr'))
o_secpr.getparent().replace(o_secpr, copy.deepcopy(f_secpr))

# 책갈피 이름(정답 위치)
for bm in sec.iter(HP + 'bookmark'):
    bm.set('name', f'답{UNO}.{UNAME}')

# ---------------------------------------------------------------- 쪽 머리말(바탕쪽)
masters = {}
for mp in ('masterpage0.xml', 'masterpage1.xml'):
    s = open(f'{FDIR}/Contents/{mp}', encoding='utf-8').read()
    s = s.replace('1. 수열의 극한', f'{UNO}. {UNAME}').replace('수열의 극한', UNAME)
    masters[mp] = s

# ---------------------------------------------------------------- 그림 파일
fig = json.load(open(FIGJSON))
used = set(e.get('binaryItemIDRef') for e in sec.iter(HC + 'img'))
bins = {}   # id -> (경로, 확장자)
for f in os.listdir(f'{ODIR}/BinData'):
    iid, ext = os.path.splitext(f)
    if iid in used:
        bins[iid] = (f'{ODIR}/BinData/{f}', ext[1:])
for iid, path in fig['bin'].items():
    assert iid in used, iid
    bins[iid] = (path, 'png')
bins['image1'] = (f'{FDIR}/BinData/image1.png', 'png')   # 양식 로고(쪽 머리말)
missing = used - set(bins)
assert not missing, missing

# content.hpf: 양식 것에 그림 목록만 바꿔 넣기
hpf = etree.parse(f'{FDIR}/Contents/content.hpf', P).getroot()
man = hpf.find(OPF + 'manifest')
for it in list(man):
    if it.get('id', '').startswith('image'):
        man.remove(it)
MT = {'png': 'image/png', 'bmp': 'image/bmp', 'jpg': 'image/jpeg', 'gif': 'image/gif'}
anchor = [it for it in man if it.get('id') == 'masterpage1'][0]
for iid in sorted(bins, key=lambda x: int(x[5:])):
    path, ext = bins[iid]
    it = etree.Element(OPF + 'item')
    it.set('id', iid)
    it.set('href', f'BinData/{iid}.{ext}')
    it.set('media-type', MT[ext])
    it.set('isEmbeded', '1')
    man.insert(list(man).index(anchor), it)
title = hpf.find(f'{OPF}metadata/{OPF}title')
if title is not None:
    title.text = f'{UNO}. {UNAME}'


def xml_bytes(root):
    return b"<?xml version='1.0' encoding='UTF-8' standalone='yes'?>" + etree.tostring(root, encoding='UTF-8')


# ---------------------------------------------------------------- 묶기
with zipfile.ZipFile(OUT, 'w') as z:
    z.writestr(zipfile.ZipInfo('mimetype'), open(f'{FDIR}/mimetype', 'rb').read(), compress_type=zipfile.ZIP_STORED)
    def add(name, data):
        z.writestr(name, data, compress_type=zipfile.ZIP_DEFLATED)
    add('version.xml', open(f'{FDIR}/version.xml', 'rb').read())
    add('Contents/header.xml', xml_bytes(fh))
    for mp, s in masters.items():
        add(f'Contents/{mp}', s.encode('utf-8'))
    add('Contents/section0.xml', xml_bytes(sec))
    add('Contents/content.hpf', xml_bytes(hpf))
    for iid, (path, ext) in bins.items():
        z.writestr(f'BinData/{iid}.{ext}', open(path, 'rb').read(), compress_type=zipfile.ZIP_DEFLATED)
    add('settings.xml', open(f'{FDIR}/settings.xml', 'rb').read())
    for f in ('META-INF/container.xml', 'META-INF/container.rdf', 'META-INF/manifest.xml',
              'Preview/PrvText.txt', 'Preview/PrvImage.png'):
        add(f, open(f'{FDIR}/{f}', 'rb').read())

print('ok', OUT, 'charPr+', len(lst(fh, 'charProperties')), 'paraPr+', len(lst(fh, 'paraProperties')), 'bins', len(bins))
