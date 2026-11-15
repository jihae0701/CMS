# -*- coding: utf-8 -*-
"""수식 약속(hwp-equation-rules) 중 기계적으로 고칠 수 있는 것을 hwpx에 한꺼번에 적용한다.
    python eqauto.py [--prop] 파일.hwpx 로그.json
1) eqfix: '<-' → '< it-'
2) eqstyle: 여집합 ^{∁}, 조건제시법 left|, 조건 속 한글 나누기, 줄임표, 수식 뒤 '이하·또는…' 앞 빈칸 (+ --prop: 명제 화살표 빈칸·소문자 집합 기호)
3) 이 파일의 규칙: 중괄호 짝, rm 뒤 빈칸, 붙여 쓴 명령 띄우기, 분수 over 앞뒤 빈칸, 계승 뒤 등호, 쉼표 뒤 ~, 관계 기호 뒤 음수 it-, 소문자 집합 기호
바뀐 수식은 KaTeX로 크기를 다시 재어 넣는다(문단 글자 크기 baseUnit에 맞춰 비례).
"""
import sys, os, re, html, json, zipfile, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'tools'))
import eqstyle, eqfix

EQPAT = re.compile(r"<hp:equation\b[^>]*>.*?</hp:equation>", re.S)
SCPAT = re.compile(r"(<hp:script\b[^>]*>)(.*?)(</hp:script>)", re.S)
GLUE = r"(overline|alpha|beta|gamma|delta|theta|omega|pi|pmatrix|sqrt|times|TIMES|leq|geq|circ|rarrow)"
SETMODE = False
MULTI = re.compile(r"\b(cases|pile|lpile|rpile|matrix|pmatrix|eqalign)\b|#")


def balance(sc):
    """LEFT/RIGHT/left/right 괄호와 따옴표 속 글자를 빼고 { } 짝을 맞춘다: 남는 '}'는 지우고 모자란 '}'는 끝에 붙인다."""
    out = []
    i = 0
    depth = 0
    n = len(sc)
    while i < n:
        m = re.match(r'(LEFT|RIGHT|left|right)\s*(\{|\}|\||\(|\)|\[|\]|\.)', sc[i:])
        if m and (i == 0 or not sc[i - 1].isalpha()):
            out.append(m.group(0)); i += m.end(); continue
        if sc[i] == '"':
            j = sc.find('"', i + 1)
            j = n - 1 if j < 0 else j
            out.append(sc[i:j + 1]); i = j + 1; continue
        c = sc[i]
        if c == '{':
            depth += 1; out.append(c)
        elif c == '}':
            if depth == 0:
                pass  # 남는 닫는 괄호는 지운다
            else:
                depth -= 1; out.append(c)
        else:
            out.append(c)
        i += 1
    s = ''.join(out)
    if depth > 0:
        s = s.rstrip() + '}' * depth
    return s


def rules(sc):
    s = sc
    if not s.strip():
        return s
    # rm 뒤 빈칸
    s = re.sub(r'\brm(?=[A-Z])', 'rm ', s)
    # 분수 over 앞뒤 빈칸
    s = re.sub(r'\}\s*over\b', '} over', s)
    s = re.sub(r'\bover\s*\{', 'over {', s)
    # 수·문자 바로 뒤의 over (1over x → 1 over x)
    s = re.sub(r'(?<![A-Za-z\\])([0-9]+|[A-Za-z])over\b', r'\1 over', s)
    # 붙여 쓴 명령: 수·문자 바로 뒤 (rm/it 뒤나 낱말 안이 아닐 때)
    def glue(m):
        pre = s_[:m.start()]
        if re.search(r'\b(rm|it|bold|LEFT|RIGHT|left|right)\s*$', pre):
            return m.group(0)
        return m.group(1) + ' ' + m.group(2)
    s_ = s
    s = re.sub(r'(?<![A-Za-z\\])([0-9]+|[A-Za-z])' + GLUE + r'\b', glue, s)
    # alpha beta 처럼 명령끼리 붙은 것
    s = re.sub(r'\b(alpha|beta|gamma|delta|theta|omega)(alpha|beta|gamma|delta|theta|omega)\b', r'\1 \2', s)
    # 계승 뒤 등호
    s = re.sub(r'([0-9A-Za-z)])\s*!\s*=(?=\s*[0-9(])', lambda m: m.group(1) + '! =', s) if re.search(r'[0-9]!=', s) else s
    # 대문자 집합 기호 → 소문자
    for a, b in (('NSUBSET', 'nsubset'), ('SUBSET', 'subset'), ('SMALLINTER', 'cap'), ('SMALLUNION', 'cup'), ('CUP', 'cup'), ('SIM', 'sim')):
        s = re.sub(r'\b%s(?![a-z])' % a, b + ' ', s)
        s = re.sub(r'\b%s  +' % b, b + ' ', s)
    if SETMODE:
        # 따옴표 괄호 "{" "}" → LEFT { … RIGHT }
        s = re.sub(r'\s*"\{"\s*', ' LEFT { ', s)
        s = re.sub(r'\s*"\}"\s*', ' RIGHT } ', s)
        # 조건제시법 세로줄: LEFT { 안의 하나뿐인 '|' (절댓값 LEFT | … RIGHT | 이 아닌 것) → left|
        if re.search(r'\bLEFT\s*\{', s) and 'left|' not in s and not re.search(r'\bRIGHT\s*\|', s):
            s = re.sub(r'\s*\bLEFT\s*\|\s*', ' left| ', s, count=1)
            if 'left|' not in s and s.count('|') == 1:
                s = re.sub(r'[\s`~]*\|[\s`~]*', ' left| ', s)
        # 조건 속 한글의 띄어쓰기 기호 정리 (x는 `` 10의 ``` 약수 → x는 10의 약수)
        s = re.sub(r'(?<=[가-힣0-9A-Za-z])[\s`~]+(?=[가-힣])|(?<=[가-힣])[\s`~]+(?=[0-9A-Za-z가-힣])', ' ', s) if re.search(r'left\|', s) else s
        # 여집합 A^c, A^{c}, A^{ C} → A^{∁}
        s = re.sub(r'\^\s*\{\s*`?\s*[cC]\s*\}|\^\s*[cC](?![A-Za-z])', '^{∁}', s)
        s = re.sub(r'\^\s*∁(?!\})', '^{∁}', s)
    if not MULTI.search(s):
        # 쉼표 뒤 ~ (따옴표 안 제외)
        parts = re.split(r'("[^"]*")', s)
        parts = [p if p.startswith('"') else re.sub(r',\s*(?=[0-9A-Za-z(\-])', ',~', p) for p in parts]
        s = ''.join(parts)
    # 관계 기호 바로 뒤 음수는 it-
    s = re.sub(r'(=|<|>|\bleq\b|\bgeq\b|\bLEQ\b|\bGEQ\b)(\s*)-(?=\s*[0-9A-Za-z(\\{])', lambda m: m.group(1) + ' it-', s)
    s = re.sub(r'\bit\s+it-', 'it-', s)
    s = balance(s)
    return s


def resize(el, sc, EQ):
    W, H, BL = EQ[sc]
    bu = re.search(r'\bbaseUnit="(\d+)"', el)
    f = int(bu.group(1)) / 1000 if bu else 1.0
    W, H = int(W * f), int(H * f)
    el = re.sub(r'(<hp:equation\b[^>]*\bbaseLine=")\d+(")', lambda q: q.group(1) + str(BL) + q.group(2), el, count=1)
    el = re.sub(r'(<hp:sz\b[^>]*\bwidth=")\d+(")', lambda q: q.group(1) + str(W) + q.group(2), el, count=1)
    el = re.sub(r'(<hp:sz\b[^>]*\bheight=")\d+(")', lambda q: q.group(1) + str(H) + q.group(2), el, count=1)
    return el


def apply_rules_xml(xml, log):
    plan = []
    for m in EQPAT.finditer(xml):
        sm = SCPAT.search(m.group(0))
        if not sm:
            continue
        sc = html.unescape(sm.group(2))
        new = rules(sc)
        if new != sc:
            plan.append((m, sm, sc, new))
    EQ = eqstyle.sizes([p[3] for p in plan]) if plan else {}
    out, last = [], 0
    for m, sm, sc, new in plan:
        out.append(xml[last:m.start()])
        el = m.group(0)
        el = el[:sm.start(2)] + eqstyle.esc(new) + el[sm.end(2):]
        out.append(resize(el, new, EQ))
        last = m.end()
        log.append([sc, new])
    out.append(xml[last:])
    return ''.join(out)


def main():
    args = sys.argv[1:]
    global SETMODE
    prop = False
    while args[0].startswith('--'):
        if args[0] == '--prop': prop = True
        if args[0] == '--set': SETMODE = True
        args = args[1:]
    path, logp = args
    eqstyle.PROP = prop
    # 1) eqfix
    nfix = eqfix.fix_file(path)
    # 2) 이 파일의 규칙
    zin = zipfile.ZipFile(path)
    items = [(i, zin.read(i.filename)) for i in zin.infolist()]
    zin.close()
    log = []
    out = []
    for info, data in items:
        if info.filename.startswith('Contents/') and info.filename.endswith('.xml') and ('section' in info.filename or 'masterpage' in info.filename):
            data = apply_rules_xml(data.decode('utf-8'), log).encode('utf-8')
        out.append((info, data))
    tmp = path + '.tmp'
    with zipfile.ZipFile(tmp, 'w') as zo:
        for info, data in out:
            zo.writestr(info, data, compress_type=info.compress_type)
    shutil.move(tmp, path)
    # 3) eqstyle: 조건 속 한글 나누기, 수식 뒤 빈칸 등 (그 자리에서)
    st = eqstyle.style_file(path)
    json.dump({'eqfix': nfix, 'eqstyle': st, 'rules': log}, open(logp, 'w'), ensure_ascii=False, indent=0)
    print(os.path.basename(path), 'eqfix', nfix, 'eqstyle', st, 'rules', len(log))


if __name__ == '__main__':
    main()
