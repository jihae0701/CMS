# -*- coding: utf-8 -*-
"""문단번호(미주) 줄 바로 옆에서 문제 시작 (2026-11-26 사용자).
- 미주만 있는 번호 문단(출처 글자 없음) 다음의 첫 문제 문단을 번호 문단에 이어 붙임.
- 모의고사 기출(번호 문단 오른쪽에 출처 '2025년 6월 고2 19번')은 그대로 둠.
- 다음 문단이 그림·표·글상자이거나 '(단'으로 시작하면 붙이지 않음.
python num_inline.py <입력.hwpx> <출력.hwpx>
"""
import re, sys, zipfile

LSA = re.compile(r"<hp:linesegarray>.*?</hp:linesegarray>", re.S)


def plain(x):
    x = re.sub(r"<hp:endNote .*?</hp:endNote>", "", x, flags=re.S)
    x = re.sub(r"<hp:equation .*?</hp:equation>", "E", x, flags=re.S)
    return "".join(re.findall(r"<hp:t>(.*?)</hp:t>", x, re.S))


def convert(s):
    out, pos, n = [], 0, 0
    for m in re.finditer(r"</hp:endNote>", s):
        e = m.end()
        if e < pos:
            continue
        a = s.rfind("<hp:p ", 0, s.rfind("<hp:endNote ", 0, e))
        pe = s.find("</hp:p>", e)
        en = s[a:pe]
        if re.sub(r"<[^>]+>", "", re.sub(r"<hp:endNote .*?</hp:endNote>", "", en, flags=re.S)).strip():
            continue                                   # 출처 글자 있음 = 모의고사
        qa = pe + len("</hp:p>")
        if not s.startswith("<hp:p ", qa):
            continue
        qe = s.find("</hp:p>", qa)
        q = s[qa:qe]
        if "<hp:p " in q[5:] or re.search(r"<hp:(pic|tbl|rect|container|ctrl|drawText)\b", q):
            continue
        if plain(q).lstrip().startswith("(단") or not plain(q).strip():
            continue
        body = re.sub(r"^<hp:p [^>]*>", "", LSA.sub("", q))
        en2 = LSA.sub("", en)
        en2 = re.sub(r"</hp:ctrl><hp:t/></hp:run>", "</hp:ctrl></hp:run>", en2)
        en2 = re.sub(r"(</hp:ctrl></hp:run>)<hp:run charPrIDRef=\"\d+\"><hp:t/></hp:run>", r"\1", en2)
        out.append(s[pos:a] + en2 + body + "</hp:p>")
        pos = qe + len("</hp:p>")
        n += 1
    out.append(s[pos:])
    return "".join(out), n


def convert_file(src, dst):
    zi = zipfile.ZipFile(src)
    items = [(i, zi.read(i.filename)) for i in zi.infolist()]
    zi.close()
    tot = 0
    with zipfile.ZipFile(dst, "w") as zo:
        for i, d in items:
            if re.match(r"Contents/section\d+\.xml", i.filename):
                x, k = convert(d.decode("utf-8")); tot += k; d = x.encode("utf-8")
            zo.writestr(i, d, compress_type=zipfile.ZIP_STORED if i.filename == "mimetype" else zipfile.ZIP_DEFLATED)
    return tot


if __name__ == "__main__":
    print(convert_file(sys.argv[1], sys.argv[2]))
