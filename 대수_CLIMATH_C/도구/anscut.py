# -*- coding: utf-8 -*-
"""끝의 정답 모음(마지막 미주 뒤 '[정답]' 문단들)을 지우고, 첫 문단의 쪽 번호 새로 시작(newNum)만 남긴 빈 문단 하나로 바꾼다
(기준 1단원 끝과 같은 모양). 끝 제목 상자의 단원 이름도 맞춘다.
    python3 anscut.py 파일.hwpx "N. 단원 이름" """
import sys, re
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
import hwpxedit as H
path, title = sys.argv[1:3]
x = H.load(path); ps = H.top_paras(x)
last = max(i for i, (s, e) in enumerate(ps) if '<hp:endNote' in x[s:e])
ans = [i for i in range(last + 1, len(ps)) if '[정답]' in x[ps[i][0]:ps[i][1]]]
n = 0
if ans:
    # 정답 모음 사이의 이어진 줄('⑶ …')은 정답 모음에 넣고, 정답 모음 뒤의 끝 제목 상자는 남긴다
    keep = ''
    if any('<hp:rect' in x[ps[i][0]:ps[i][1]] for i in range(ans[-1] + 1, len(ps))):
        keep = x[ps[ans[-1] + 1][0]:ps[-1][1]]
        ans = list(range(ans[0], ans[-1] + 1))
    rest = [i for i in range(ans[0], len(ps)) if i not in ans] if not keep else []
    assert all(not H.render(x[ps[i][0]:ps[i][1]]).strip() and '<hp:rect' not in x[ps[i][0]:ps[i][1]] and '<hp:pic' not in x[ps[i][0]:ps[i][1]] for i in rest), ('정답 모음 뒤에 다른 문단', rest)
    s, e = ps[ans[0]]; p = x[s:e]
    head = re.match(r'<hp:p\b[^>]*>', p).group(0)
    cp = re.search(r'<hp:run charPrIDRef="(\d+)"', p).group(1)
    nn = re.search(r'<hp:ctrl><hp:newNum [^>]*/></hp:ctrl>', p)
    ls = re.sub(r'textpos="\d+"', 'textpos="0"', re.search(r'<hp:lineseg\b[^>]*/>', p).group(0))
    newp = head + '<hp:run charPrIDRef="%s">%s<hp:t/></hp:run><hp:linesegarray>%s</hp:linesegarray></hp:p>' % (cp, nn.group(0) if nn else '', ls)
    x = x[:s] + newp + keep + x[ps[-1][1]:]
    n = len(ans)
# 끝 제목 상자(마지막 rect 글)
ps = H.top_paras(x)
k = None
for i in range(len(ps) - 1, last, -1):
    if '<hp:rect' in x[ps[i][0]:ps[i][1]]:
        k = i; break
fixed = 0
if k is not None:
    s, e = ps[k]; p = x[s:e]
    ts = re.findall(r'<hp:t>([^<]*)</hp:t>', p)
    if len(ts) == 1 and ts[0] != title:
        p = p.replace('<hp:t>%s</hp:t>' % ts[0], '<hp:t>%s</hp:t>' % H.eqstyle.esc(title)); fixed = ts[0]
        x = x[:s] + p + x[e:]
H.save(path, x)
print(path, '정답 모음 지움', n, '끝 제목', fixed or '그대로')
