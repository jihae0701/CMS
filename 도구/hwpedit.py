# -*- coding: utf-8 -*-
"""HWPX section0.xml 편집 도구 (lxml). 고친 내용은 LOG에 모아 수정기록을 만든다."""
import re, copy, random
from lxml import etree
from eqwidth import em

HP = '{http://www.hancom.co.kr/hwpml/2011/paragraph}'
NS = {'hp': 'http://www.hancom.co.kr/hwpml/2011/paragraph'}
LOG = []          # (문항, 위치, 종류, 원래, 고친 내용)
K_EM = 1.048      # em -> 폭(baseUnit 배수) 보정값 (원본 수식으로 맞춘 값)


def load(path):
    return etree.parse(path, etree.XMLParser(remove_blank_text=False, huge_tree=True))


def save(tree, path):
    data = etree.tostring(tree.getroot(), encoding='UTF-8', xml_declaration=False)
    with open(path, 'wb') as f:
        f.write(b"<?xml version='1.0' encoding='UTF-8' standalone='yes'?>")
        f.write(data)


def log(q, where, kind, before, after):
    LOG.append((q, where, kind, before, after))


# ------------------------------------------------------------------ 범위
class Doc:
    def __init__(self, tree):
        self.tree = tree
        self.root = tree.getroot()

    def top(self):
        return self.root.findall(HP + 'p')

    def endnotes(self):
        return list(self.root.iter(HP + 'endNote'))

    def endnote(self, k):
        return self.endnotes()[k - 1]

    def top_of(self, el):
        while el.getparent() is not self.root:
            el = el.getparent()
        return el

    def problem_paras(self, k):
        """문항 k의 본문 문단들(미주 k를 품은 문단부터 다음 미주를 품은 문단 직전까지)"""
        ens = self.endnotes()
        start = self.top_of(ens[k - 1])
        stop = self.top_of(ens[k]) if k < len(ens) else None
        out, on = [], False
        for p in self.top():
            if p is start:
                on = True
            if p is stop:
                break
            if on:
                out.append(p)
        return out


def in_endnote(el):
    return any(a.tag == HP + 'endNote' for a in el.iterancestors())


def iter_scope(scope, tag, problem_only=False):
    """scope: 요소 리스트. problem_only면 미주 안은 건너뜀"""
    for s in scope:
        for el in s.iter(HP + tag):
            if problem_only and in_endnote(el):
                continue
            yield el


# ------------------------------------------------------------------ 수식
SHAPE = {  # (높이, baseLine) 종류별 대표값 (원본 통계)
    '': (1125, 85), 'frac': (2580, 65), 'lim': (2100, 51), 'limfrac': (2768, 62),
    'sqrt': (1290, 87), 'limsqrt': (2340, 56), 'fracsqrt': (2910, 64), 'limfracsqrt': (2933, 64)}


def kind(sc):
    return (('lim' if re.search(r'lim', sc) else '') + ('frac' if re.search(r'over', sc, re.I) else '')
            + ('sqrt' if re.search(r'sqrt|root', sc) else ''))


def set_script(eq, new):
    sc = eq.find(HP + 'script')
    old = sc.text or ''
    sc.text = new
    sz = eq.find(HP + 'sz')
    bu = int(eq.get('baseUnit'))
    eo, en = em(old), em(new)
    w = int(sz.get('width'))
    if eo >= 1.0 and kind(old) == kind(new):
        nw = int(round(w * en / eo))
    else:
        nw = int(round(en * K_EM * bu))
    sz.set('width', str(max(nw, 300)))
    if kind(old) != kind(new):
        h, bl = SHAPE.get(kind(new), (1125, 85))
        sz.set('height', str(int(h * bu / 1100)))
        eq.set('baseLine', str(bl))
    return old


def eq_find(scope, old, problem_only=False, solution_only=False, n=None):
    hits = []
    for eq in iter_scope(scope, 'equation', problem_only):
        if solution_only and not in_endnote(eq):
            continue
        if (eq.find(HP + 'script').text or '').strip() == old.strip():
            hits.append(eq)
    if n is None:
        assert len(hits) == 1, ('수식 찾기 실패', old, len(hits))
        return hits[0]
    assert len(hits) > n, ('수식 찾기 실패', old, len(hits))
    return hits[n]


def eq_fix(scope, q, where, kind_, old, new, show_old=None, show_new=None, **kw):
    eq = eq_find(scope, old, **kw)
    set_script(eq, new)
    if show_old is not None or show_new is not None or kind_:
        if kind_:
            log(q, where, kind_, show_old or old, show_new or new)
    return eq


# ------------------------------------------------------------------ 글자
def t_nodes(scope, problem_only=False, solution_only=False):
    """(소유 요소, 'text'|'tail') 단위로 글자 조각을 돌려준다"""
    for t in iter_scope(scope, 't', problem_only):
        if solution_only and not in_endnote(t):
            continue
        yield t, 'text'
        for ch in t:
            yield ch, 'tail'


def _get(el, which):
    return (el.text if which == 'text' else el.tail) or ''


def _set(el, which, v):
    if which == 'text':
        el.text = v
    else:
        el.tail = v


def text_sub(scope, q, where, kind_, old, new, count=1, problem_only=False, solution_only=False, quiet=False):
    hits = [(el, w) for el, w in t_nodes(scope, problem_only, solution_only) if old in _get(el, w)]
    assert len(hits) == count, ('글자 찾기 실패', old, len(hits))
    for el, w in hits:
        _set(el, w, _get(el, w).replace(old, new))
    if not quiet:
        log(q, where, kind_, old, new)


def para_text(p):
    out = []
    for el in p.iter():
        if el.tag == HP + 't':
            out.append(el.text or '')
        elif el.getparent() is not None and el.getparent().tag == HP + 't':
            out.append(el.tail or '')
        elif el.tag == HP + 'equation':
            out.append('⟦' + (el.find(HP + 'script').text or '') + '⟧')
    return ''.join(out)


def own_text(p):
    """문단 자기 글(미주/도형 안 제외)"""
    out = []
    for r in p.findall(HP + 'run'):
        for x in r:
            if x.tag == HP + 't':
                out.append(''.join(x.itertext()))
            elif x.tag == HP + 'equation':
                out.append('⟦' + (x.find(HP + 'script').text or '') + '⟧')
    return ''.join(out)


# ------------------------------------------------------------------ 문단 만들기
_ids = set()


def new_id():
    while True:
        i = random.randint(1900000000, 2100000000)
        if i not in _ids:
            _ids.add(i)
            return str(i)


def make_eq(template_eq, script):
    eq = copy.deepcopy(template_eq)
    eq.set('id', new_id())
    sc = eq.find(HP + 'script')
    sc.text = 'x'
    sz = eq.find(HP + 'sz')
    sz.set('width', '1000')
    set_script(eq, script)
    bu = int(eq.get('baseUnit'))
    h, bl = SHAPE.get(kind(script), (1125, 85))
    sz.set('height', str(int(h * bu / 1100)))
    eq.set('baseLine', str(bl))
    sz.set('width', str(max(300, int(round(em(script) * K_EM * bu)))))
    return eq


def make_para(template_p, template_eq, text_cp, segs):
    """segs: 'text' 또는 ('eq', script) 또는 ('br',) 의 리스트"""
    p = etree.Element(HP + 'p', nsmap=None)
    for k in ('id', 'paraPrIDRef', 'styleIDRef', 'pageBreak', 'columnBreak', 'merged'):
        if template_p.get(k) is not None:
            p.set(k, template_p.get(k))
    p.set('id', '2147483648')
    p.set('pageBreak', '0')
    p.set('columnBreak', '0')
    run = etree.SubElement(p, HP + 'run')
    run.set('charPrIDRef', text_cp)
    cur_t = None
    for s in segs:
        if isinstance(s, str):
            if cur_t is None:
                cur_t = etree.SubElement(run, HP + 't')
                cur_t.text = s
            else:
                if len(cur_t):
                    cur_t[-1].tail = (cur_t[-1].tail or '') + s
                else:
                    cur_t.text = (cur_t.text or '') + s
        elif s[0] == 'eq':
            run.append(make_eq(template_eq, s[1]))
            cur_t = None
        elif s[0] == 'br':
            if cur_t is None:
                cur_t = etree.SubElement(run, HP + 't')
            etree.SubElement(cur_t, HP + 'lineBreak')
    if cur_t is None:
        etree.SubElement(run, HP + 't')
    return p


def seg_parse(s):
    """'글 $수식$ 글 | 다음 줄' 꼴의 문자열을 segs로. |는 줄바꿈"""
    segs = []
    for i, part in enumerate(re.split(r'(\$[^$]*\$|\|)', s)):
        if not part:
            continue
        if part == '|':
            segs.append(('br',))
        elif part.startswith('$'):
            segs.append(('eq', part[1:-1]))
        else:
            segs.append(part)
    return segs


def note_templates(note):
    """미주 안의 본문 문단·글자모양·수식 본보기"""
    ps = note.findall('.//' + HP + 'p')
    body = ps[1] if len(ps) > 1 else ps[0]
    cp = None
    for r in body.findall(HP + 'run'):
        if r.find(HP + 't') is not None and ''.join(r.find(HP + 't').itertext()).strip():
            cp = r.get('charPrIDRef')
            break
    if cp is None:
        cp = body.find(HP + 'run').get('charPrIDRef')
    eq = next(note.iter(HP + 'equation'), None)
    return body, cp, eq


# ------------------------------------------------------------------ 괄호 정리
def _strip_delims(s):
    s = re.sub(r'"[^"]*"', '', s)
    return re.sub(r'(?i)\b(left|right)\s*[{}.\[\]()|]', '', s)


def balance(s):
    d, neg = 0, False
    for ch in _strip_delims(s):
        if ch == '{':
            d += 1
        elif ch == '}':
            d -= 1
            if d < 0:
                neg = True
    return d, neg


def fix_braces(sc):
    """짝 없는 } 지우고 모자란 } 채움. 'left/right' 구분자는 건드리지 않음"""
    d, neg = balance(sc)
    if d == 0 and not neg:
        return sc
    s = sc
    # 끝의 '} { }' 찌꺼기 반복 제거
    while True:
        d, neg = balance(s)
        if not neg and d >= 0:
            break
        m = re.search(r'\}\s*\{\s*\}\s*$', s)
        if not m:
            break
        s = s[:m.start()].rstrip()
    # 남은 짝 없는 } 제거
    d, neg = balance(s)
    if neg:
        out, depth, i = [], 0, 0
        prot = [(m.start(), m.end()) for m in re.finditer(r'(?i)\b(left|right)\s*[{}]|"[^"]*"', s)]
        def protected(i):
            return any(a <= i < b for a, b in prot)
        for i, ch in enumerate(s):
            if ch == '{' and not protected(i):
                depth += 1
            elif ch == '}' and not protected(i):
                if depth == 0:
                    continue
                depth -= 1
            out.append(ch)
        s = ''.join(out)
    d, neg = balance(s)
    if d > 0:
        s = s.rstrip() + '}' * d
    return s
