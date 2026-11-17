# -*- coding: utf-8 -*-
"""묶지 않은 위 첨자 묶기: '^' 뒤(빈칸 하나 허용) 빈칸·=·<·>·,·`·~·짝 없는 ')' '}'까지를 지수로 본다.
supchk 무늬가 있는 수식만. python3 supfix.py 파일 [--dry] [--skip n:part:번호,...]"""
import sys, re, os, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hwpxedit as H, eqstyle
from supchk import P
PS = re.compile(r'_\s?(-[\w(]|[A-Za-z0-9.]+[+\-(][\w(]|[A-Za-z]_)')
STOPS = set(' \t\n=<>,`~')
def fix(s, mark='^'):
    s = s.replace('＋', '+')
    if mark == '_':
        s = re.sub(r'_(\w)\+1it\^2', r'_{\1+1} ^{2}', s)
    out, i = [], 0
    while i < len(s):
        c = s[i]
        if c == mark and i + 1 < len(s):
            j = i + 1
            if s[j] == ' ' and j + 1 < len(s) and s[j + 1] not in '{ ':
                j += 1
            if s[j] == '{':
                out.append(s[i:j]); i = j; continue
            k, d = j, 0
            while k < len(s):
                ch = s[k]
                if ch in '({':
                    d += 1
                elif ch in ')}':
                    if d == 0:
                        break
                    d -= 1
                elif ch in STOPS and d == 0:
                    break
                elif ch in '^_' and d == 0 and k > j and (mark == '_' or ch == '_'):
                    break
                k += 1
            run = s[j:k]
            if run and re.search(r'[+\-(^]|[0-9][A-Za-z]|[A-Za-z][0-9]', run) and not re.fullmatch(r'\d+', run):
                # 끝이 연산자면 그 앞까지
                run2 = run.rstrip('+-')
                out.append(mark + '{' + run2 + '}'); i = j + len(run2); continue
            out.append(s[i:j]); i = j; continue
        out.append(c); i += 1
    return ''.join(out)
if __name__ == '__main__':
    p = sys.argv[1]; dry = '--dry' in sys.argv
    x = H.load(p); cnt = 0
    def f(m):
        global cnt
        s0 = html.unescape(m.group(2))
        if not P.search(s0.replace('^{', '^@')) and not PS.search(s0.replace('_{', '_@')):
            return m.group(0)
        s = fix(fix(s0), '_') if PS.search(s0.replace('_{', '_@')) else fix(s0)
        if s == s0:
            return m.group(0)
        cnt += 1
        if dry or '-v' in sys.argv:
            print('  ', s0[:110], '\n=>', s[:110])
        return m.group(1) + eqstyle.esc(s) + m.group(3)
    x2 = H.SC.sub(f, x)
    if not dry:
        H.save(p, x2)
    print(p, '위 첨자 묶음', cnt)
