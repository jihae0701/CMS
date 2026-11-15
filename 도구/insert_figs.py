# -*- coding: utf-8 -*-
"""문제 속 그림을 새 그림(PNG)으로 바꿔 문제 문장 아래 가운데에 넣는다.
python3 insert_figs.py u1|u2 입력section 출력section 그림폴더 중앙정렬paraPr"""
import sys, json, copy
from PIL import Image
from hwpedit import *

HC = '{http://www.hancom.co.kr/hwpml/2011/core}'
unit, SRC, OUT, FIGDIR, CENTER_PP, HEADER = sys.argv[1:7]
d = Doc(load(SRC))
import re as _re
_h = open(HEADER, encoding='utf-8').read()
NUMBERED = set(_re.findall(r'<hh:paraPr id="(\d+)"[^>]*>(?:(?!</hh:paraPr>).)*?<hh:heading type="(?:NUMBER|BULLET|OUTLINE)"', _h, _re.S))

PLAN = {
    'u1': {4: (['image9'], ['u1_q4']), 5: (['image10'], ['u1_q5_f', 'u1_q5_g']), 6: (['image11'], ['u1_q6']),
           8: (['image12'], ['u1_q8']), 30: (['image16'], ['u1_q30_f', 'u1_q30_g']), 31: (['image17'], ['u1_q31']),
           32: (['image18', 'image19'], ['u1_q32_f', 'u1_q32_g']), 33: (['#1896706740'], ['u1_q33']),
           52: (['image20'], ['u1_q52_f', 'u1_q52_g']), 59: (['image21'], ['u1_q59'])},
    'u2': {2: (['image7'], ['u2_q2']), 4: (['image9'], ['u2_q4']), 5: (['image10'], ['u2_q5']),
           18: (['image13'], ['u2_q18_f', 'u2_q18_g']), 19: (['image14'], ['u2_q19_f', 'u2_q19_g']),
           23: (['image18'], ['u2_q23']), 29: (['image19'], ['u2_q29']), 32: (['image20'], ['u2_q32_f', 'u2_q32_g']),
           33: (['image21'], ['u2_q33_f', 'u2_q33_g']), 35: (['#1896711026'], ['u2_q35']), 38: (['image22'], ['u2_q38']),
           42: (['image25'], ['u2_q42'])},
    'u3': {6: (['image4'], ['u3_q6']), 7: (['#1896713736'], ['u3_q7']), 15: (['image7'], ['u3_q15']),
           17: (['image8'], ['u3_q17']), 31: (['image11'], ['u3_q31'])},
}[unit]

BIN = {}   # 새 그림 id -> png 경로
next_img = [101]


def find_old(key):
    if key.startswith('#'):
        hits = [c for c in d.root.iter(HP + 'container') if c.get('id') == key[1:]]
    else:
        hits = [p for p in d.root.iter(HP + 'pic')
                if p.find('.//' + HC + 'img').get('binaryItemIDRef') == key and not in_endnote(p)]
    assert len(hits) == 1, (key, len(hits))
    return hits[0]


def is_empty(p):
    if own_text(p).strip():
        return False
    for tag in ('pic', 'container', 'rect', 'tbl', 'equation', 'endNote', 'line', 'ellipse', 'curve', 'polygon'):
        if p.find('.//' + HP + tag) is not None:
            return False
    return True


def trim_edges(p, end):
    """문단 끝(end=True) 또는 앞의 줄바꿈·탭·공백 정리"""
    runs = p.findall(HP + 'run')
    seq = runs[::-1] if end else runs
    for r in seq:
        kids = list(r)
        for x in (kids[::-1] if end else kids):
            if x.tag != HP + 't':
                return
            # t 안의 조각들
            parts = list(x)
            if end:
                while len(x) and (x[-1].tag in (HP + 'lineBreak', HP + 'tab')) and not (x[-1].tail or '').strip():
                    x.remove(x[-1])
                if len(x):
                    x[-1].tail = (x[-1].tail or '').rstrip()
                    return
                x.text = (x.text or '').rstrip()
                if x.text:
                    return
            else:
                x.text = (x.text or '').lstrip()
                if x.text:
                    return
                while len(x) and x[0].tag in (HP + 'lineBreak', HP + 'tab'):
                    t = x[0].tail
                    x.remove(x[0])
                    x.text = (t or '').lstrip()
                    if x.text:
                        return
                if len(x):
                    return


def split_at(p, el):
    """문단 p를 요소 el 자리에서 둘로 나눈다(el은 지움). (앞, 뒤) 반환"""
    run = el.getparent()
    assert run.tag == HP + 'run' and run.getparent() is p
    p2 = etree.Element(HP + 'p')
    for k, v in p.attrib.items():
        p2.set(k, v)
    if p.get('paraPrIDRef') in NUMBERED:
        p2.set('paraPrIDRef', '0')
    runs = p.findall(HP + 'run')
    i = runs.index(run)
    kids = list(run)
    j = kids.index(el)
    nr = etree.SubElement(p2, HP + 'run')
    nr.set('charPrIDRef', run.get('charPrIDRef'))
    for x in kids[j + 1:]:
        nr.append(x)
    run.remove(el)
    for r in runs[i + 1:]:
        p2.append(r)
    trim_edges(p, True)
    trim_edges(p2, False)
    return p, p2


def make_pic(png, run_cp):
    im = Image.open(png)
    W, H = im.size
    cw, ch = int(round(W * 6.4)), int(round(H * 6.4))
    ow, oh = W * 75, H * 75
    iid = 'image%d' % next_img[0]
    next_img[0] += 1
    BIN[iid] = png
    pid = new_id()
    xml = f'''<hp:pic xmlns:hp="http://www.hancom.co.kr/hwpml/2011/paragraph" xmlns:hc="http://www.hancom.co.kr/hwpml/2011/core" id="{pid}" zOrder="{int(pid) % 1000 + 500}" numberingType="PICTURE" textWrap="TOP_AND_BOTTOM" textFlow="BOTH_SIDES" lock="0" dropcapstyle="None" href="" groupLevel="0" instid="{int(pid) - 1000000000}" reverse="0"><hp:offset x="0" y="0"/><hp:orgSz width="{ow}" height="{oh}"/><hp:curSz width="{cw}" height="{ch}"/><hp:flip horizontal="0" vertical="0"/><hp:rotationInfo angle="0" centerX="{cw // 2}" centerY="{ch // 2}" rotateimage="1"/><hp:renderingInfo><hc:transMatrix e1="1" e2="0" e3="0" e4="0" e5="1" e6="0"/><hc:scaMatrix e1="{cw / ow:.6f}" e2="0" e3="0" e4="0" e5="{ch / oh:.6f}" e6="0"/><hc:rotMatrix e1="1" e2="0" e3="0" e4="0" e5="1" e6="0"/></hp:renderingInfo><hc:img binaryItemIDRef="{iid}" bright="0" contrast="0" effect="REAL_PIC" alpha="0"/><hp:imgRect><hc:pt0 x="0" y="0"/><hc:pt1 x="{ow}" y="0"/><hc:pt2 x="{ow}" y="{oh}"/><hc:pt3 x="0" y="{oh}"/></hp:imgRect><hp:imgClip left="0" right="{ow}" top="0" bottom="{oh}"/><hp:inMargin left="0" right="0" top="0" bottom="0"/><hp:imgDim dimwidth="{ow}" dimheight="{oh}"/><hp:effects/><hp:sz width="{cw}" widthRelTo="ABSOLUTE" height="{ch}" heightRelTo="ABSOLUTE" protect="0"/><hp:pos treatAsChar="1" affectLSpacing="0" flowWithText="1" allowOverlap="0" holdAnchorAndSO="0" vertRelTo="PARA" horzRelTo="PARA" vertAlign="TOP" horzAlign="LEFT" vertOffset="0" horzOffset="0"/><hp:outMargin left="0" right="0" top="283" bottom="283"/><hp:shapeComment>그림입니다.</hp:shapeComment></hp:pic>'''
    return etree.fromstring(xml)


def fig_para(pngs, cp):
    p = etree.Element(HP + 'p')
    for k, v in (('id', '2147483648'), ('paraPrIDRef', CENTER_PP), ('styleIDRef', '0'), ('pageBreak', '0'),
                 ('columnBreak', '0'), ('merged', '0')):
        p.set(k, v)
    r = etree.SubElement(p, HP + 'run')
    r.set('charPrIDRef', cp)
    for i, n in enumerate(pngs):
        if i:
            t = etree.SubElement(r, HP + 't')
            t.text = '     '
        r.append(make_pic(f'{FIGDIR}/{n}.png', cp))
    etree.SubElement(r, HP + 't')
    return p


def first_text_cp(p):
    for r in p.iter(HP + 'run'):
        if r.find(HP + 't') is not None and ''.join(r.find(HP + 't').itertext()).strip() and not in_endnote(r):
            return r.get('charPrIDRef')
    return p.find(HP + 'run').get('charPrIDRef')


# ---------------------------------------------------------------- 문장 손보기(떠 있던 그림 때문에 넣은 줄바꿈 등)
if unit == 'u2':
    ps = d.problem_paras(4)
    a = [p for p in ps if own_text(p).rstrip().endswith('그래프가 구간')][0]
    b = ps[ps.index(a) + 1]
    assert own_text(b).startswith('⟦[-1,~3]⟧')
    ft = a.findall('.//' + HP + 't')
    last = [t for t in ft if not in_endnote(t)][-1]
    if len(last):
        last[-1].tail = (last[-1].tail or '') + ' '
    else:
        last.text = (last.text or '') + ' '
    for r in b.findall(HP + 'run'):
        a.append(r)
    b.getparent().remove(b)
    log(4, '문제', '줄 정리', '"…그래프가 구간 / [-1, 3]에서…" 두 문단으로 나뉨', '한 문단으로 합침')


def drop_first_break(k, contains):
    p = [p for p in d.problem_paras(k) if contains in own_text(p)][0]
    for t in p.iter(HP + 't'):
        if in_endnote(t):
            continue
        for lb in t.findall(HP + 'lineBreak'):
            prev = lb.getprevious()
            tail = lb.tail or ''
            if prev is None:
                t.text = (t.text or '') + tail
            else:
                prev.tail = (prev.tail or '') + tail
            t.remove(lb)
            return
    raise AssertionError(('줄바꿈 없음', k))


if unit == 'u1':
    drop_first_break(6, '정의역이')
if unit == 'u2':
    drop_first_break(38, '그래프가 그림과 같다')

# ---------------------------------------------------------------- 그림 바꾸기
for k, (olds, pngs) in PLAN.items():
    els = [find_old(o) for o in olds]
    para = d.top_of(els[0])
    assert all(d.top_of(e) is para for e in els)
    cp = first_text_cp(para)
    floating = els[0].find(HP + 'pos').get('treatAsChar') == '0'
    fp = fig_para(pngs, cp)
    parent = para.getparent()
    if floating:
        for e in els:
            e.getparent().remove(e)
        tb = [t for t in para.findall(HP + 'run/' + HP + 'tbl')]
        if tb:
            # 문장 안에 보기 표가 붙어 있으면 표 앞에서 나눠 그림을 표 위에 둔다
            marker = etree.Element(HP + 't')
            run = tb[0].getparent()
            run.insert(list(run).index(tb[0]), marker)
            p1, p2 = split_at(para, marker)
            i = list(parent).index(p1)
            parent.insert(i + 1, fp)
            parent.insert(i + 2, p2)
        else:
            parent.insert(list(parent).index(para) + 1, fp)
    else:
        for e in els[1:]:
            e.getparent().remove(e)
        p1, p2 = split_at(para, els[0])
        i = list(parent).index(p1)
        parent.insert(i + 1, fp)
        parent.insert(i + 2, p2)
        if is_empty(p2):
            parent.remove(p2)
        if is_empty(p1) and p1.find('.//' + HP + 'ctrl') is None:
            parent.remove(p1)
    log(k, '그림', '그림', '원본 그림' + (' (도형으로 그린 그림)' if olds[0].startswith('#') else ''),
        '그림 약속대로 다시 그림, 문제 아래 가운데에 배치')

if unit == 'u2':
    log(5, '그림', '그림 오류', '(0, -1)에 그래프와 관계없는 빈 점(○)', '새 그림에서 뺌')

save(d.tree, OUT)
json.dump({'log': LOG, 'bin': BIN}, open(OUT + '.fig.json', 'w'), ensure_ascii=False, indent=1)
print('ok', len(BIN))
