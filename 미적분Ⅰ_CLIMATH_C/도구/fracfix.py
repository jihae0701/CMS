# -*- coding: utf-8 -*-
"""붙여 쓴 분수 정리: 'AoverB', '{A}over B', 'x-1 over{…}' → '{A} over {B}'.
한글 수식은 over 앞뒤의 '빈칸으로 끊긴 덩어리(또는 중괄호 묶음)'를 분자·분모로 읽으므로, 그 덩어리를 중괄호로 묶어 같은 모양을 지킨다.
    python3 fracfix.py 파일.hwpx 로그.json"""
import sys, os, re, html, json, zipfile, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, 'tools'))
import eqauto, eqstyle

STOP = set(' \t\r\n{}=<>~,`')
OVER = re.compile(r'(?<![A-Za-z])over(?!line)')


def grp_left(s, i):
    """s[:i] 끝의 피연산자 (시작, 끝)"""
    j = i
    while j > 0 and s[j - 1] == ' ':
        j -= 1
    if j > 0 and s[j - 1] == '}':
        d = 0
        for k in range(j - 1, -1, -1):
            if s[k] == '}':
                d += 1
            elif s[k] == '{':
                d -= 1
                if d == 0:
                    # '^{2}'·'root{3}' 같은 명령 묶음이면 그 앞 덩어리까지
                    a = k
                    while a > 0 and s[a - 1] not in STOP:
                        a -= 1
                    return a, j
        return None
    a = j
    while a > 0 and s[a - 1] not in STOP:
        a -= 1
    # 'left(1over2' 처럼 여는 괄호 명령이 덩어리에 섞이면 그 뒤부터
    for mm in re.finditer(r'(left|LEFT)\s*[(\[|]', s[a:j]):
        a2 = a + mm.end()
        if a2 < j:
            a = a2
    if s[a:j].count('(') > s[a:j].count(')'):
        a = a + s[a:j].rfind('(') + 1
    return (a, j) if a < j else None


def grp_right(s, i):
    j = i
    while j < len(s) and s[j] == ' ':
        j += 1
    if j < len(s) and s[j] == '{':
        d = 0
        for k in range(j, len(s)):
            if s[k] == '{':
                d += 1
            elif s[k] == '}':
                d -= 1
                if d == 0:
                    e = k + 1
                    # '{…}^2' 처럼 이어지면 그 덩어리까지
                    while e < len(s) and s[e] not in STOP:
                        e += 1
                    return j, e
        return None
    e = j
    pd = 0
    while e < len(s) and s[e] not in STOP:
        if s[e] == '(':
            pd += 1
        elif s[e] == ')':
            pd -= 1
            if pd < 0:   # 짝 없는 ')'에서 멈춤
                break
        if s[e] == '{':   # 'root{3}ofx' 같은 명령 묶음은 통째로
            d = 0
            for k in range(e, len(s)):
                if s[k] == '{':
                    d += 1
                elif s[k] == '}':
                    d -= 1
                    if d == 0:
                        e = k
                        break
        e += 1
    return (j, e) if j < e else None


def wrap(t):
    t = t.strip()
    if t.startswith('{') and t.endswith('}'):
        d = 0
        for k, c in enumerate(t):
            d += c == '{'
            d -= c == '}'
            if d == 0 and k < len(t) - 1:
                break
        else:
            return t
    return '{' + t + '}'


def fix(sc):
    pos = 0
    while True:
        m = OVER.search(sc, pos)
        if not m:
            return sc
        L = grp_left(sc, m.start()); R = grp_right(sc, m.end())
        if not L or not R:
            pos = m.end(); continue
        num = wrap(sc[L[0]:L[1]]); den = wrap(sc[R[0]:R[1]])
        pre, post = sc[:L[0]], sc[R[1]:]
        if pre and pre[-1] not in ' {(' and not pre.endswith('_') and not pre.endswith('^'):
            pre += ' '
        if post and post[0] not in ' })':
            post = ' ' + post
        sc = pre + num + ' over ' + den + post
        pos = len(pre) + len(num) + len(' over ')   # 분모 안의 분수도 이어서 본다
        if den.startswith('{') and not sc[R[0]:R[0]+1] == '{':
            pos += 1


def need(sc):
    return bool(re.search(r'\}over|over\{|[^\s{}]over(?![A-Za-z])|(?<![A-Za-z])over[^\s{]', sc.replace('overline', '')))


def run(path, logp):
    z = zipfile.ZipFile(path); items = [(i, z.read(i.filename)) for i in z.infolist()]; z.close()
    log = []
    out = []
    for info, data in items:
        if info.filename == 'Contents/section0.xml':
            x = data.decode('utf-8')
            plan = []
            for m in eqauto.EQPAT.finditer(x):
                sm = eqauto.SCPAT.search(m.group(0))
                if not sm:
                    continue
                sc = html.unescape(sm.group(2))
                if not need(sc):
                    continue
                new = fix(sc)
                if new != sc:
                    plan.append((m, sm, new)); log.append([sc, new])
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
    print(os.path.basename(path), 'frac', len(log))


if __name__ == '__main__':
    run(sys.argv[1], sys.argv[2])
