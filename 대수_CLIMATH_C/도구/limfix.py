# -*- coding: utf-8 -*-
"""미적분 약속: lim 아래첨자를 'lim _{x `->` a}' 꼴로 맞추고(화살표 앞뒤 ` 하나씩, inf 소문자),
미주(정답·해설) 수식의 bold를 뺀다.
    python3 limfix.py 파일.hwpx 로그.json [--nobold]
알아보는 꼴: lim _{…}, lim_{…}, lim from {…}, lim_x->a(괄호 없이 빈칸·{·(·`까지), lim_ x→a
화살표: ->, rarrow, →  /  끝 값: INF → inf, - INF → -inf, 0+ · 1- 그대로
"""
import sys, os, re, html, json, zipfile, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, 'tools'))
import eqauto, eqstyle

ARROW = re.compile(r'\s*`*\s*(->|(?<![A-Za-z])rarrow|(?<![A-Za-z])RARROW|→)\s*`*\s*')


def norm_sub(sub):
    """아래첨자 속 'x -> a'를 'x `->` a'로. 화살표가 없으면 None"""
    sub = sub.strip()
    m = ARROW.search(sub)
    if not m:
        return None
    left = re.sub(r'\s+', ' ', re.sub(r'`', ' ', sub[:m.start()])).strip()   # 'DELTA x'처럼 명령 뒤 빈칸은 남긴다
    left = re.sub(r'\s*([+\-])\s*', r'\1', left)
    right = re.sub(r'[`\s]+', '', sub[m.end():])
    right = re.sub(r'INF', 'inf', right)
    if not left or not right:
        return None
    return '%s `->` %s' % (left, right)


def find_brace(s, i):
    """s[i]=='{' 일 때 짝 '}' 위치"""
    d = 0
    for j in range(i, len(s)):
        if s[j] == '{':
            d += 1
        elif s[j] == '}':
            d -= 1
            if d == 0:
                return j
    return -1


def fix_script(sc):
    out = []
    i = 0
    n = len(sc)
    changed = False
    while i < n:
        m = re.compile(r'(?<![A-Za-z])lim(?![A-Za-z])').search(sc, i)
        if not m:
            out.append(sc[i:]); break
        out.append(sc[i:m.start()])
        if m.start() > 0 and (sc[m.start() - 1].isalnum() or sc[m.start() - 1] in ')}]'):
            out.append(' ')   # '3lim' → '3 lim'
        j = m.end()
        k = j
        while k < n and sc[k] in ' `':
            k += 1
        sub = None
        end = None
        if sc.startswith('from', k):
            k2 = k + 4
            while k2 < n and sc[k2] in ' `':
                k2 += 1
            if k2 < n and sc[k2] == '{':
                e = find_brace(sc, k2)
                if e > 0:
                    sub, end = sc[k2 + 1:e], e + 1
        elif k < n and sc[k] == '_':
            k2 = k + 1
            while k2 < n and sc[k2] in ' `':
                k2 += 1
            if k2 < n and sc[k2] == '{':
                e = find_brace(sc, k2)
                if e > 0:
                    sub, end = sc[k2 + 1:e], e + 1
            else:   # 괄호 없는 아래첨자: 빈칸·{·(·[·`·LEFT 앞까지
                mm = re.compile(r'[^\s{(\[`]+').match(sc, k2)
                if mm:
                    tok = mm.group(0)
                    # '->a+' 뒤 바로 이어지는 식(예: 'x->1{f(x)}')은 위에서 끊김. 'x->0-x' 같은 경우는 드묾
                    sub, end = tok, mm.end()
        new = norm_sub(sub) if sub is not None and not re.search(r'eqalign|#', sub) else None
        if new is None:
            out.append(sc[m.start():j]); i = j; continue
        rep = 'lim _{%s}' % new
        if rep != sc[m.start():end]:
            changed = True
        out.append(rep)
        if end < n and sc[end] not in ' `':
            out.append(' ')
            changed = True
        i = end
    return ''.join(out), changed


def run(path, logp, bold=True):
    z = zipfile.ZipFile(path); items = [(i, z.read(i.filename)) for i in z.infolist()]; z.close()
    log = {'lim': [], 'bold': []}
    out = []
    for info, data in items:
        if info.filename == 'Contents/section0.xml':
            x = data.decode('utf-8')
            ends = [(m.start(), x.find('</hp:endNote>', m.start())) for m in re.finditer(r'<hp:endNote\b', x)]
            plan = []
            for m in eqauto.EQPAT.finditer(x):
                sm = eqauto.SCPAT.search(m.group(0))
                if not sm:
                    continue
                sc = html.unescape(sm.group(2))
                new, ch = fix_script(sc)
                if ch:
                    log['lim'].append([sc, new])
                if bold and any(a < m.start() < b for a, b in ends) and re.search(r'\bbold\b|bold', new, re.I):
                    nb = re.sub(r'\s*\bbold\b\s*', ' ', new, flags=re.I).strip()
                    nb = re.sub(r'bold(?=[{(0-9a-z])', '', nb)
                    if nb != new:
                        log['bold'].append([new, nb]); new = nb
                if new != sc:
                    plan.append((m, sm, new))
            EQ = eqstyle.sizes([p[2] for p in plan]) if plan else {}
            o = []; last = 0
            for m, sm, new in plan:
                o.append(x[last:m.start()]); el = m.group(0)
                el = el[:sm.start(2)] + eqstyle.esc(new) + el[sm.end(2):]
                o.append(eqauto.resize(el, new, EQ)); last = m.end()
            o.append(x[last:]); x = ''.join(o)
            data = x.encode('utf-8')
        out.append((info, data))
    tmp = path + '.tmp'
    with zipfile.ZipFile(tmp, 'w') as zo:
        for info, data in out:
            zo.writestr(info, data, compress_type=info.compress_type)
    shutil.move(tmp, path)
    json.dump(log, open(logp, 'w'), ensure_ascii=False, indent=0)
    print(os.path.basename(path), 'lim', len(log['lim']), 'bold', len(log['bold']))


if __name__ == '__main__':
    run(sys.argv[1], sys.argv[2], '--nobold' not in sys.argv)
