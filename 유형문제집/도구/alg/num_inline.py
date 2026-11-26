# -*- coding: utf-8 -*-
"""문단번호(미주) 줄 바로 옆에서 문제 시작 (2026-11-26 사용자).
- 미주만 있는 번호 문단(출처 글자 없음) 다음의 첫 문제 문단을 번호 문단에 이어 붙임.
- 모의고사 기출(번호 문단 오른쪽에 출처 '2025년 6월 고2 19번')은 그대로 둠.
- 다음 문단이 그림·표·글상자이거나 '(단'으로 시작하면 붙이지 않음.
- 둘째 줄부터 내어 쓰기(사용자 '두 번째 줄이 칸 띄기 되었으면').
  처음엔 문단번호 '자동 내어 쓰기'(autoIndent=1, 번호 뒤 글자 자리)로 했으나 사용자 '내어 쓰기가 좀 적게' →
  자동 내어 쓰기를 끄고(autoIndent=0) 붙인 문단 모양에 고정 내어 쓰기 HANG을 줌
  (hp:case 값 = HANG, hp:default 값 = 2×HANG — 이 파일들의 다른 내어 쓰기 문단 모양과 같은 짝).
  (중간에 미주 표시를 1pt로 줄인 것은 사용자 '아니'로 되돌림.)
python num_inline.py <입력.hwpx> <출력.hwpx>
"""
import re, sys, zipfile

HANG = 1500          # 내어 쓰기 폭(HWPUNIT, 1000 ≈ 10pt 글자 하나)
LSA = re.compile(r"<hp:linesegarray>.*?</hp:linesegarray>", re.S)


def plain(x):
    x = re.sub(r"<hp:endNote .*?</hp:endNote>", "", x, flags=re.S)
    x = re.sub(r"<hp:equation .*?</hp:equation>", "E", x, flags=re.S)
    return "".join(re.findall(r"<hp:t>(.*?)</hp:t>", x, re.S))


def convert(s, used=None):
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
        if used is not None:
            used.add(re.search(r'paraPrIDRef="(\d+)"', en).group(1))
        pos = qe + len("</hp:p>")
        n += 1
    out.append(s[pos:])
    return "".join(out), n


def hang(h, used):
    """used 문단 모양: 내어 쓰기 HANG, 그 문단번호(1수준)는 자동 내어 쓰기 끔"""
    nums = set()
    for pid in used:
        m = re.search(r'<hh:paraPr id="%s" .*?</hh:paraPr>' % pid, h, re.S)
        blk = m.group(0)
        nums |= set(re.findall(r'<hh:heading type="NUMBER" idRef="(\d+)"', blk))
        blk = re.sub(r'(<hp:case [^>]*><hh:margin>)<hc:intent value="-?\d+"', r'\1<hc:intent value="-%d"' % HANG, blk, count=1)
        blk = re.sub(r'(<hp:default><hh:margin>)<hc:intent value="-?\d+"', r'\1<hc:intent value="-%d"' % (2 * HANG), blk, count=1)
        h = h[:m.start()] + blk + h[m.end():]
    for nid in nums:
        m = re.search(r'<hh:numbering id="%s" .*?</hh:numbering>' % nid, h, re.S)
        blk = re.sub(r'(<hh:paraHead [^>]*level="1"[^>]*?)autoIndent="1"', r'\1autoIndent="0"', m.group(0), count=1)
        h = h[:m.start()] + blk + h[m.end():]
    return h


def convert_file(src, dst):
    zi = zipfile.ZipFile(src)
    items = [(i, zi.read(i.filename)) for i in zi.infolist()]
    zi.close()
    tot, used = 0, set()
    for j, (i, d) in enumerate(items):
        if re.match(r"Contents/section\d+\.xml", i.filename):
            x, k = convert(d.decode("utf-8"), used); tot += k; items[j] = (i, x.encode("utf-8"))
    j = next(j for j, (i, _) in enumerate(items) if i.filename == "Contents/header.xml")
    items[j] = (items[j][0], hang(items[j][1].decode("utf-8"), used).encode("utf-8"))
    with zipfile.ZipFile(dst, "w") as zo:
        for i, d in items:
            zo.writestr(i, d, compress_type=zipfile.ZIP_STORED if i.filename == "mimetype" else zipfile.ZIP_DEFLATED)
    return tot


if __name__ == "__main__":
    print(convert_file(sys.argv[1], sys.argv[2]))
