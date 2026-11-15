"""HWPX에서 문항(미주 번호 순)마다 문제 글·수식과 정답 줄을 뽑는다."""
import zipfile, re, html
def norm_eq(s):
    s = html.unescape(s)
    s = re.sub(r'\b(bold|rm|it)\b', '', s, flags=re.I)
    return re.sub(r'[\s`~{}]', '', s)
def problems(path):
    x = zipfile.ZipFile(path).read('Contents/section0.xml').decode()
    # 미주 위치
    ens = [m for m in re.finditer(r'<hp:endNote\b.*?</hp:endNote>', x, re.S)]
    out = []
    for k, m in enumerate(ens):
        # 문제: 이 미주가 든 최상위 문단 시작 ~ 다음 미주 앞 (미주 내용 제외)
        a = x.rfind('<hp:p ', 0, m.start())
        b = ens[k + 1].start() if k + 1 < len(ens) else len(x)
        seg = x[m.end():b]
        seg = re.sub(r'<hp:endNote\b.*?</hp:endNote>', '', seg, flags=re.S)
        eqs = [norm_eq(s) for s in re.findall(r'<hp:script[^>]*>(.*?)</hp:script>', seg, re.S)]
        txt = ''.join(html.unescape(t) for t in re.findall(r'<hp:t>([^<]*)</hp:t>', seg))
        ans = m.group(0)
        ans_eq = [norm_eq(s) for s in re.findall(r'<hp:script[^>]*>(.*?)</hp:script>', ans, re.S)[:3]]
        out.append({'n': k + 1, 'text': txt, 'eqs': eqs, 'sig': re.sub(r'\s', '', txt) + '|' + '|'.join(eqs), 'ans': ans_eq})
    return out
