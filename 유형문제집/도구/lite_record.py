# -*- coding: utf-8 -*-
"""스토리 라이트 바뀐 문항 기록(스토리라이트/바뀐문항_기록.md)에 한 단원을 더한다.
python lite_record.py 단원번호(05) 원본.hwpx 시작번호 단원이름 "추가 설명"
명세(lite_c1_NN.py)의 REPLACE에서 바뀐 번호·새 문항·정답을, 원본 hwpx에서 원래 문항·정답·모의고사를 읽는다."""
import sys, re, html, zipfile, importlib.util, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lite import top_paras
HERE = os.path.dirname(os.path.abspath(__file__))
SUBJ = os.environ.get("LITE_SUBJ", "c1")                 # c1 공통수학1(lite_c1_NN.py), c2 공통수학2(lite_c2_NN.py)
LABEL = {"c1": "공통수학1", "c2": "공통수학2"}[SUBJ]


def txt(x, n=90):
    x = re.sub(r'<hp:equation\b.*?<hp:script[^>]*>(.*?)</hp:script>.*?</hp:equation>', lambda m: html.unescape(m.group(1)), x, flags=re.S)
    x = re.sub(r'<hp:shapeComment>.*?</hp:shapeComment>', '', x, flags=re.S)
    x = re.sub(r'<[^>]+>', ' ', x)
    x = re.sub(r'\s+', ' ', x).strip()
    return (x[:n] + '…') if len(x) > n else x


def main(nn, src, start, name, extra=""):
    sp = importlib.util.spec_from_file_location("s", os.path.join(HERE, "lite_%s_%s.py" % (SUBJ, nn)))
    S = importlib.util.module_from_spec(sp); sp.loader.exec_module(S)
    s = zipfile.ZipFile(src).read('Contents/section0.xml').decode()
    h = s.find('단원 종합 문제'); h = h if h >= 0 else s.find('단원종합문제')
    allp = top_paras(s, 0, len(s)); hp = [k for k, (a, z) in enumerate(allp) if a <= h < z][0]; ps = allp[hp + 1:]
    st = [k for k, (a, z) in enumerate(ps) if '<hp:endNote' in s[a:z]]
    blocks = [s[ps[k][0]:ps[(st[n + 1] if n + 1 < len(st) else len(ps)) - 1][1]] for n, k in enumerate(st)]
    nb = len(re.findall('<hp:endNote ', s[:h]))
    first = int(start) + nb
    mock, changed, rows = [], [], []
    for i, b in enumerate(blocks, 1):
        no = first + i - 1
        en = re.search(r'<hp:endNote .*?</hp:endNote>', b, re.S).group(0)
        body = b.replace(en, '')
        m = re.search(r'(\d{4})년 (\d+)월 고(\d)(\([가-힣]\))? (\d+)번', body)    # '고2(가)'꼴도
        a = (re.search(r'(?:\[정답\]|󰂼)\s*([①-⑤])', en) or re.search(r'(?:\[정답\]|󰂼)\s*</hp:t>(.*?)</hp:run>', en, re.S))   # 사용자 완성본은 '󰂼'인 곳도
        oans = txt(a.group(1), 30) if a else '?'
        if m and i not in S.REPLACE:          # 사용자가 바꾸라고 한 모의고사(mock_ok)는 '그대로 둔 모의고사'에서 뺀다
            mock.append('%03d (%s)' % (no, m.group(0)))
        if i in S.REPLACE:
            it = S.REPLACE[i]
            changed.append('%03d' % no)
            q = " ".join(x for x in it["q"] if isinstance(x, str))
            q = re.sub(r'\$(.*?)\$', r'\1', q)
            rows.append("| %03d | %s | %s | %s%s | 올림포스 유형편 %s | %s |" % (no, txt(body), oans, q[:90] + ('…' if len(q) > 90 else ''),
                        ' (그림)' if any(isinstance(x, dict) and 'img' in x for x in it["q"]) else '', it["src"], it["ans"].replace('$', '')))
    p = os.path.join(HERE, '..', '스토리라이트', '바뀐문항_기록.md')
    md = open(p, encoding='utf-8').read()
    summ = "| %s | %s | %s | %d | %s |" % (LABEL, name, ", ".join(changed), len(changed), ", ".join(x.split(' ')[0] for x in mock) or "없음")
    lines = md.split('\n')
    last = max(i for i, l in enumerate(lines) if l.startswith('| 공통수학1 |') or l.startswith('| %s |' % LABEL))
    lines.insert(last + 1, summ)
    md = '\n'.join(lines)
    md += "\n## %s %s (단원종합문제 %03d~%03d)\n" % (LABEL, name, first, first + len(blocks) - 1)
    md += "그대로 둔 모의고사: %s. %s\n\n" % (", ".join(mock) or "없음", extra)
    md += "| 번호 | 유형서(원래 문항) | 정답 | 라이트(새 문항) | 출처 | 정답 |\n|---|---|---|---|---|---|\n" + "\n".join(rows) + "\n"
    open(p, 'w', encoding='utf-8').write(md)
    print(summ)


if __name__ == "__main__":
    main(*sys.argv[1:])
