# -*- coding: utf-8 -*-
"""HWPX 문항 단위 편집 (section0.xml 글 기준).
문항 n = n번째 미주. 'q' 범위 = 미주 n이 든 최상위 문단부터 미주 n+1이 든 최상위 문단 앞까지(미주 내용 제외),
'sol' 범위 = 미주 n의 내용.
명령(JSON 목록):
  {"op":"eq","n":6,"part":"sol","old":"수식 스크립트(그대로)","new":"새 스크립트"}   — 그 범위에서 정확히 하나여야 함
  {"op":"text","n":25,"part":"q","old":"개수의 합","new":"계수의 합"}                 — <hp:t> 하나 안에서, 범위에서 정확히 하나 (줄바꿈은 ⏎)
     "after_eq":"x=2" 를 더하면 그 수식 바로 뒤의 글에서만 찾는다(조사 고치기). eq·text에 "all":true면 모두 바꾼다. text에 "exact":true면 <hp:t> 글 전체가 old와 같을 때만.
  {"op":"add_para","n":22,"part":"sol","after":"<기준 문단에 있는 글 또는 ⟦수식⟧>","text":"글과 ⟦수식⟧ 섞어서"}
     기준 문단 바로 뒤에 같은 문단·글자 모양으로 새 문단을 넣는다.
  {"op":"del_eq","n":8,"part":"sol","old":"스크립트"}  {"op":"del_para","n":51,"part":"sol","anchor":"글"}  add_para에서 "after"를 빼면 범위 맨 끝에 넣는다.
python3 hwpxedit.py list 파일.hwpx n [n...]      문항의 q/sol 문단을 보여 줌
python3 hwpxedit.py apply 파일.hwpx 명령.json    그 자리에서 고침
"""
import sys, os, re, json, html, zipfile, shutil, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, 'tools'))
import eqauto, eqstyle

EQ = re.compile(r'<hp:equation\b[^>]*>.*?</hp:equation>', re.S)
SC = re.compile(r'(<hp:script\b[^>]*>)(.*?)(</hp:script>)', re.S)


def top_paras(x):
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


def endnotes(x):
    res = []
    for m in re.finditer(r'<hp:endNote\b', x):
        e = x.find('</hp:endNote>', m.start()) + len('</hp:endNote>')
        res.append((m.start(), e))
    return res


_PCACHE = {}


def all_paras(x):
    key = (len(x), hash(x))
    if key not in _PCACHE:
        spans, stack = [], []
        for m in re.finditer(r'<(/?)hp:p\b[^>]*?(/?)>', x):
            if m.group(2) == '/':
                continue
            if m.group(1) == '':
                stack.append(m.start())
            else:
                spans.append((stack.pop(), m.end()))
        _PCACHE.clear(); _PCACHE[key] = sorted(spans)
    return _PCACHE[key]


def inner_para(x, pos):
    best = None
    for s, e in all_paras(x):
        if s <= pos < e and (best is None or s > best[0]):
            best = (s, e)
    return best


def region(x, n, part):
    ens = endnotes(x)
    a, b = ens[n - 1]
    if part == 'sol':
        return [(a, b)]
    start = inner_para(x, a)[0]
    end = inner_para(x, ens[n][0])[0] if n < len(ens) else len(x)
    spans, cur = [], start
    for s, e in ens:
        if cur <= s < end:
            spans.append((cur, s)); cur = e
    spans.append((cur, end))
    return [sp for sp in spans if sp[0] < sp[1]]


def paras_in(x, spans):
    """범위 안의 문단(<hp:p>…</hp:p>) — 미주 범위면 그 안의 문단들"""
    out = []
    for a, b in spans:
        for m in re.finditer(r'<hp:p\b[^>]*>', x[a:b]):
            s = a + m.start()
            # 같은 깊이의 닫는 태그 찾기
            depth = 0
            for t in re.finditer(r'<(/?)hp:p\b[^>]*?(/?)>', x[s:]):
                if t.group(2) == '/':
                    continue
                depth += 1 if t.group(1) == '' else -1
                if depth == 0:
                    e = s + t.end(); break
            out.append((s, e))
    # 겹치는(안쪽) 문단 빼기
    res = []
    for s, e in out:
        if not any(s2 < s and e <= e2 for s2, e2 in out):
            res.append((s, e))
    return res


def render(p):
    p = re.sub(r'<hp:endNote\b.*?</hp:endNote>', '{미주}', p, flags=re.S)
    p = EQ.sub(lambda m: '⟦' + html.unescape(SC.search(m.group(0)).group(2)) + '⟧', p)
    p = re.sub(r'<hp:lineBreak/>', '⏎', p)
    p = re.sub(r'<hp:t>([^<]*)</hp:t>', lambda m: html.unescape(m.group(1)), p)
    p = re.sub(r'<hp:(tbl|pic|rect|container|ellipse|line)\b', lambda m: '{%s}' % m.group(1), p)
    return re.sub(r'<[^>]+>', '', p)


def find_unique(x, spans, pat, what):
    hits = []
    for a, b in spans:
        for m in pat.finditer(x, a, b):
            hits.append(m)
    if len(hits) != 1:
        raise ValueError('%s: %d곳' % (what, len(hits)))
    return hits[0]


def op_eq(x, spans, old, new, all_=False, first=False):
    cands = []
    for a, b in spans:
        for m in EQ.finditer(x, a, b):
            sm = SC.search(m.group(0))
            if html.unescape(sm.group(2)) == old:
                cands.append((m, sm))
    if first and cands:
        cands = cands[:1]
    if not cands or (len(cands) != 1 and not all_):
        raise ValueError('수식 "%s": %d곳' % (old, len(cands)))
    EQS = eqstyle.sizes([new])
    for m, sm in sorted(cands, key=lambda c: -c[0].start()):
        el = m.group(0)
        el = el[:sm.start(2)] + eqstyle.esc(new) + el[sm.end(2):]
        el = eqauto.resize(el, new, EQS)
        x = x[:m.start()] + el + x[m.end():]
    return x


TPAT = re.compile(r'<hp:t>((?:[^<]|<hp:lineBreak/>|<hp:tab\b[^>]*/>)*)</hp:t>')


def op_text(x, spans, old, new, after_eq=None, exact=False, all_=False, before_eq=None):
    """<hp:t> 하나 안의 글 바꾸기. 줄바꿈은 ⏎로 쓴다. after_eq를 주면 그 스크립트의 수식 바로 뒤 <hp:t>만 본다."""
    enc = lambda s: eqstyle.esc(s).replace('⏎', '<hp:lineBreak/>')
    o, nw = enc(old), enc(new)
    cands = []
    for a, b in spans:
        for m in TPAT.finditer(x, a, b):
            if o not in m.group(1) or (exact and m.group(1) != o):
                continue
            if after_eq is not None:
                pre = x[:m.start()]
                if not pre.endswith('</hp:equation>'):
                    continue
                e0 = pre.rfind('<hp:equation')
                sm = SC.search(pre[e0:])
                if not sm or html.unescape(sm.group(2)) != after_eq:
                    continue
            if before_eq is not None:
                rest = x[m.end():m.end() + 4000]
                sm = SC.search(rest) if rest.startswith('<hp:equation') else None
                if not sm or html.unescape(sm.group(2)) != before_eq:
                    continue
            cands.append(m)
    tot = sum(m.group(1).count(o) for m in cands)
    if all_ and tot >= 1:
        for m in sorted(cands, key=lambda c: -c.start()):
            x = op_text(x, [(m.start(), m.end())], old, new)
        return x
    if tot != 1:
        raise ValueError('글 "%s": %d곳' % (old, tot))
    m = cands[0]
    x2 = x[:m.start()] + '<hp:t>' + m.group(1).replace(o, nw) + '</hp:t>' + x[m.end():]
    # 글자 수가 바뀌면 그 문단 자기 줄 배치 정보의 뒤쪽 줄 위치를 맞춘다
    delta = len(new.replace('⏎', 'X')) - len(old.replace('⏎', 'X'))
    if delta:
        import refcheck, make_unit
        s0, e0 = inner_para(x2, m.start())
        p = x2[s0:e0]
        pre_t = m.group(1)[:m.group(1).find(o)]
        off = refcheck.para_len(x2[s0:m.start()] + '</hp:p>') + len(re.sub(r'<hp:tab\b[^>]*/>', 'X' * 8, pre_t.replace('<hp:lineBreak/>', 'X')))
        _PCACHE.clear()
        p2 = make_unit.shift_own_lineseg(p, delta, after=off)
        if delta < 0:
            p2 = trim_lineseg(p2)
        x2 = x2[:s0] + p2 + x2[e0:]
        _PCACHE.clear()
    return x2


def trim_lineseg(p):
    """문단 자기 줄 배치 정보에서 글자 수를 넘는 줄 기록을 지운다(첫 줄은 남김) — 글을 줄였을 때"""
    import refcheck
    k = p.rfind('<hp:linesegarray>')
    if k < 0 or p.find('</hp:run>', k) >= 0:
        return p
    L = refcheck.para_len(p[:k] + '</hp:p>')
    segs = re.findall(r'<hp:lineseg\b[^>]*/>', p[k:])
    keep = [sg for i, sg in enumerate(segs) if i == 0 or int(re.search(r'textpos="(\d+)"', sg).group(1)) < L]
    if len(keep) == len(segs):
        return p
    e = p.index('</hp:linesegarray>', k)
    return p[:k] + '<hp:linesegarray>' + ''.join(keep) + p[e:]


def op_del_eq(x, spans, old):
    """수식 하나 지우기 (그 문단 줄 배치 위치도 8글자 당김)"""
    cands = []
    for a, b in spans:
        for m in EQ.finditer(x, a, b):
            sm = SC.search(m.group(0))
            if sm and html.unescape(sm.group(2)) == old:
                cands.append(m)
    if len(cands) != 1:
        raise ValueError('지울 수식 "%s": %d곳' % (old, len(cands)))
    m = cands[0]
    import refcheck, make_unit
    s0, e0 = inner_para(x, m.start())
    off = refcheck.para_len(x[s0:m.start()] + '</hp:p>')
    p = x[s0:m.start()] + x[m.end():e0]
    p = trim_lineseg(make_unit.shift_own_lineseg(p, -8, after=off))
    _PCACHE.clear()
    return x[:s0] + p + x[e0:]


def op_del_para(x, spans, anchor):
    """기준 글이 든 문단 하나 지우기"""
    ps = [(s, e) for s, e in paras_in(x, spans) if anchor in render(x[s:e])]
    if len(ps) != 1:
        raise ValueError('지울 문단 "%s": %d개' % (anchor, len(ps)))
    s, e = ps[0]
    _PCACHE.clear()
    return x[:s] + x[e:]


def op_add_para(x, spans, after, text, like=None):
    if after is None:   # 범위의 맨 끝 문단 뒤
        ps = paras_in(x, spans)[-1:]
    else:
        ps = [(s, e) for s, e in paras_in(x, spans) if after in render(x[s:e])]
    if len(ps) != 1:
        raise ValueError('기준 문단 "%s": %d개' % (after, len(ps)))
    s, e = ps[0]
    p = x[s:e]
    if like is not None:
        ln, lt = like
        lp = [(a, b) for a, b in paras_in(x, region(x, ln, 'sol')) if lt in render(x[a:b])]
        if len(lp) != 1:
            raise ValueError('본보기 문단 "%s": %d개' % (lt, len(lp)))
        p = x[lp[0][0]:lp[0][1]]
    head = re.match(r'<hp:p\b[^>]*>', p).group(0)
    head = re.sub(r'\bid="\d+"', 'id="0"', head)
    head = re.sub(r'pageBreak="1"', 'pageBreak="0"', head)
    # 글자 모양: 기준 문단에서 글자가 있는 첫 run의 모양
    cp = re.search(r'<hp:run charPrIDRef="(\d+)">(?:(?!</hp:run>).)*?<hp:t>[^<]', p, re.S)
    cp = cp.group(1) if cp else re.search(r'charPrIDRef="(\d+)"', p).group(1)
    tmpl = EQ.search(x[spans[0][0]:]) or EQ.search(x)
    tmpl = tmpl.group(0)
    parts = re.split(r'⟦(.*?)⟧', text)
    eqs = [parts[i] for i in range(1, len(parts), 2)]
    EQS = eqstyle.sizes(eqs) if eqs else {}
    inner = []
    zmax = max(int(z) for z in re.findall(r'\bzOrder="(\d+)"', x))
    for i, piece in enumerate(parts):
        if i % 2 == 0:
            if piece:
                inner.append('<hp:t>%s</hp:t>' % eqstyle.esc(piece).replace('⏎', '<hp:lineBreak/>'))
        else:
            el = re.sub(r'(<hp:equation\b[^>]*\bid=")\d+(")', lambda q: q.group(1) + str(random.randint(1000000000, 2100000000)) + q.group(2), tmpl, count=1)
            zmax += 1
            el = re.sub(r'(<hp:equation\b[^>]*\bzOrder=")\d+(")', lambda q: q.group(1) + str(zmax) + q.group(2), el, count=1)
            sm = SC.search(el)
            el = el[:sm.start(2)] + eqstyle.esc(piece) + el[sm.end(2):]
            inner.append(eqauto.resize(el, piece, EQS))
    # 줄 배치 정보: 한글 문서의 모든 문단에 있어야 한다(없으면 '손상' 경고). 기준 문단의 첫 줄을 본떠 넣으면 한글이 다시 계산한다.
    ls = re.search(r'<hp:lineseg\b[^>]*/>', p).group(0)
    ls = re.sub(r'\btextpos="\d+"', 'textpos="0"', ls)
    newp = head + '<hp:run charPrIDRef="%s">%s</hp:run><hp:linesegarray>%s</hp:linesegarray></hp:p>' % (cp, ''.join(inner) or '<hp:t/>', ls)
    s, e = ps[0]
    return x[:e] + newp + x[e:]


def load(path):
    return zipfile.ZipFile(path).read('Contents/section0.xml').decode('utf-8')


def save(path, x):
    z = zipfile.ZipFile(path); items = [(i, z.read(i.filename)) for i in z.infolist()]; z.close()
    tmp = path + '.tmp'
    with zipfile.ZipFile(tmp, 'w') as zo:
        for info, data in items:
            if info.filename == 'Contents/section0.xml':
                data = x.encode('utf-8')
            zo.writestr(info, data, compress_type=info.compress_type)
    shutil.move(tmp, path)


def apply(path, ops):
    x = load(path)
    fails = []
    for i, op in enumerate(ops):
        try:
            spans = region(x, op['n'], op.get('part', 'q'))
            if op['op'] == 'eq':
                x = op_eq(x, spans, op['old'], op['new'], op.get('all', False), op.get('first', False))
            elif op['op'] == 'text':
                x = op_text(x, spans, op['old'], op['new'], op.get('after_eq'), op.get('exact', False), op.get('all', False), op.get('before_eq'))
            elif op['op'] == 'add_para':
                x = op_add_para(x, spans, op.get('after'), op['text'], (op['like_n'], op['like']) if 'like' in op else None)
            elif op['op'] == 'del_eq':
                x = op_del_eq(x, spans, op['old'])
            elif op['op'] == 'del_para':
                x = op_del_para(x, spans, op['anchor'])
            else:
                raise ValueError('op?')
        except Exception as e:
            fails.append((i, str(e), op))
    save(path, x)
    return fails


if __name__ == '__main__':
    cmd, path = sys.argv[1:3]
    if cmd == 'list':
        x = load(path)
        for n in map(int, sys.argv[3:]):
            for part in ('q', 'sol'):
                print('【%d %s】' % (n, part))
                for s, e in paras_in(x, region(x, n, part)):
                    t = render(x[s:e]).strip()
                    if t:
                        print('  ¶', t[:400])
    else:
        fails = apply(path, json.load(open(sys.argv[3])))
        for f in fails:
            print('실패', f)
        print('완료, 실패', len(fails))
