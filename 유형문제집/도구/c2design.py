# -*- coding: utf-8 -*-
"""공통수학2 유형서 디자인(사용자 완성본 2026-11-06)을 생성본에 입힌다.

사용자가 생성본(gen.py, 기본폼 파랑 테마)을 한글에서 고쳐 만든 완성본(01~03)은 구조는 그대로이고
글꼴·색(초록 테마)·바탕쪽(세로 구분선)·꼬리말 쪽번호 상자 색·'보 기' 라벨 등이 바뀌었다.

python c2design.py build <생성본01> <완성본01> [<생성본02> <완성본02> ...]
    → 디자인_공통수학2_유형서/ 에 header.xml, masterpage0/1.xml, idmap.json, bogi_label.xml 저장
      (마지막 쌍의 완성본 머리(header)를 기준으로 하고, 앞 쌍들에서만 나온 모양은 같은 정의를 찾거나 덧붙인다)
python c2design.py apply <gen.py 출력.hwpx> <단원 모듈.py>
    → 같은 파일에 디자인을 입힌다(gen.py가 끝에서 자동으로 부름)
"""
import sys, os, re, json, zipfile, difflib, collections, importlib.util
from lxml import etree

HERE = os.path.dirname(os.path.abspath(__file__))
DES = os.path.join(HERE, "디자인_공통수학2_유형서")
HP = "{http://www.hancom.co.kr/hwpml/2011/paragraph}"
ATTRS = ["charPrIDRef", "paraPrIDRef", "borderFillIDRef", "styleIDRef"]
KIND = {"charPrIDRef": ("charPr", "charProperties"), "paraPrIDRef": ("paraPr", "paraProperties"),
        "borderFillIDRef": ("borderFill", "borderFills"), "styleIDRef": ("style", "styles")}
# 생성본에만 글자로 박혀 있는 색 → 완성본 색 (모양 번호로 바꿀 수 없는 것)
COLOR = [('faceColor="#B9D8E5"', 'faceColor="#94DDCB"'),                       # 꼬리말 쪽번호 상자
         ('<hp:lineShape color="#0159E7" width="33" style="SOLID" endCap="FLAT" headStyle="NORMAL" tailStyle="NORMAL" '
          'headfill="1" tailfill="1" headSz="MEDIUM_MEDIUM" tailSz="MEDIUM_MEDIUM"',
          '<hp:lineShape color="#40E6ED" width="33" style="SOLID" endCap="FLAT" headStyle="NORMAL" tailStyle="NORMAL" '
          'headfill="1" tailfill="1" headSz="SMALL_SMALL" tailSz="SMALL_SMALL"'),  # 유형 제목 아래 가는 선
         ('<hp:lineShape color="#002E68" width="198"', '<hp:lineShape color="#2CB156" width="198"')]  # 유형 제목 왼쪽 굵은 막대


def unzip(path):
    z = zipfile.ZipFile(path)
    return {n: z.read(n) for n in z.namelist()}, [i.filename for i in z.infolist()], {i.filename: i.compress_type for i in z.infolist()}


def defs(head, tag):
    return {m.group(1): m.group(0) for m in re.finditer(r'<hh:%s id="(\d+)"[^>]*?(?:/>|>.*?</hh:%s>)' % (tag, tag), head, re.S)}


def fonts(head):
    out = {}
    for m in re.finditer(r'<hh:fontface lang="(\w+)" fontCnt="\d+">(.*?)</hh:fontface>', head, re.S):
        out[m.group(1)] = {f.group(1): f.group(2) for f in re.finditer(r'<hh:font id="(\d+)" face="([^"]+)"', m.group(2))}
    return out


def toks(sec):
    r = etree.fromstring(sec)
    out = []
    for e in r.iter():
        if not isinstance(e.tag, str):
            continue
        a = {k: e.get(k) for k in ATTRS if e.get(k) is not None}
        if not a:
            continue
        ln = etree.QName(e).localname
        txt = "".join(x.text or "" for x in e.iter(HP + "t"))[:20] if ln == "run" else ""
        out.append((ln + "|" + txt, a))
    return out


def vote(gen_sec, done_sec):
    A, B = toks(gen_sec), toks(done_sec)
    v = {k: collections.defaultdict(collections.Counter) for k in ATTRS}
    sm = difflib.SequenceMatcher(None, [t for t, _ in A], [t for t, _ in B], autojunk=False)
    for bl in sm.get_matching_blocks():
        for k in range(bl.size):
            a, b = A[bl.a + k][1], B[bl.b + k][1]
            for at in ATTRS:
                if at in a and at in b:
                    v[at][a[at]][b[at]] += 1
    return {at: {k: c.most_common(1)[0][0] for k, c in v[at].items()} for at in ATTRS}


def norm(x):
    return re.sub(r'\bid="\d+"', "", x, count=1)


def append_def(head, tag, plural, xml):
    cnt = int(re.search(r'<hh:%s itemCnt="(\d+)"' % plural, head).group(1))
    new = re.sub(r'\bid="\d+"', 'id="%d"' % cnt, xml, count=1)
    end = head.index("</hh:%s>" % plural)
    head = head[:end] + new + head[end:]
    head = re.sub(r'<hh:%s itemCnt="\d+"' % plural, '<hh:%s itemCnt="%d"' % (plural, cnt + 1), head, count=1)
    return head, str(cnt)


def refont(xml, src_fonts, dst_head):
    """charPr의 fontRef 번호를 글꼴 이름으로 dst 머리의 번호로 바꾼다(없으면 dst에 글꼴을 더한다)."""
    langs = ["hangul", "latin", "hanja", "japanese", "other", "symbol", "user"]
    for lang in langs:
        m = re.search(r'<hh:fontRef [^>]*\b%s="(\d+)"' % lang, xml)
        if not m:
            continue
        L = lang.upper()
        face = src_fonts.get(L, {}).get(m.group(1))
        dst = fonts(dst_head).get(L, {})
        did = next((i for i, f in dst.items() if f == face), None)
        if did is None:
            fm = re.search(r'(<hh:fontface lang="%s" fontCnt=")(\d+)(">)(.*?)(</hh:fontface>)' % L, dst_head, re.S)
            n = int(fm.group(2))
            did = str(n)
            fx = '<hh:font id="%d" face="%s" type="TTF" isEmbedded="0"><hh:typeInfo familyType="FCAT_GOTHIC" weight="6" proportion="0" contrast="0" strokeVariation="1" armStyle="1" letterform="1" midline="1" xHeight="1"/></hh:font>' % (n, face)
            dst_head = dst_head[:fm.start()] + fm.group(1) + str(n + 1) + fm.group(3) + fm.group(4) + fx + fm.group(5) + dst_head[fm.end():]
        xml = re.sub(r'(<hh:fontRef [^>]*\b%s=")\d+(")' % lang, lambda mm: mm.group(1) + did + mm.group(2), xml, count=1)
    return xml, dst_head


def build(pairs):
    os.makedirs(DES, exist_ok=True)
    gen_last, done_last = pairs[-1]
    D, _, _ = unzip(done_last)
    head = D["Contents/header.xml"].decode("utf-8")
    idmap = {at: {} for at in ATTRS}
    for gi, (g, d) in enumerate(reversed(pairs)):          # 마지막 쌍(기준 머리)부터
        G, _, _ = unzip(g)
        U, _, _ = unzip(d)
        uhead = U["Contents/header.xml"].decode("utf-8")
        m = vote(G["Contents/section0.xml"], U["Contents/section0.xml"])
        for at in ["borderFillIDRef", "charPrIDRef", "paraPrIDRef", "styleIDRef"]:
            tag, plural = KIND[at]
            for mine, theirs in m[at].items():
                if mine in idmap[at]:
                    continue
                if gi == 0:
                    idmap[at][mine] = theirs
                    continue
                x = defs(uhead, tag).get(theirs)
                if x is None:
                    continue
                if tag == "charPr":
                    x, head = refont(x, fonts(uhead), head)
                if tag == "paraPr":
                    x = re.sub(r'borderFillIDRef="(\d+)"', lambda mm: 'borderFillIDRef="%s"' % idmap["borderFillIDRef"].get(mm.group(1), mm.group(1)), x)
                if tag == "style":       # 스타일은 이름으로 찾는다
                    nm = re.search(r'name="([^"]*)"', x).group(1)
                    hit = next((i for i, y in defs(head, tag).items() if re.search(r'name="([^"]*)"', y).group(1) == nm), None)
                    if hit:
                        idmap[at][mine] = hit
                    continue
                hit = next((i for i, y in defs(head, tag).items() if norm(y) == norm(x)), None)
                if hit is None:
                    head, hit = append_def(head, tag, plural, x)
                idmap[at][mine] = hit
    open(os.path.join(DES, "header.xml"), "w", encoding="utf-8").write(head)
    title = None
    for mp in ("Contents/masterpage0.xml", "Contents/masterpage1.xml"):
        x = D[mp].decode("utf-8")
        ts = re.findall(r"<hp:t>([^<]*)</hp:t>", x)
        title = ts[ts.index("2") + 1]                       # '공통수학', ' ', '2' 다음 칸이 단원명
        x = x.replace("<hp:t>%s</hp:t>" % title, "<hp:t>{{UNIT}}</hp:t>", 1)
        open(os.path.join(DES, os.path.basename(mp)), "w", encoding="utf-8").write(x)
    # '보 기' 라벨(본문 안 글자처럼 놓인 보라색 사각형)
    sec = D["Contents/section0.xml"].decode("utf-8")
    m = re.search(r'<hp:rect [^>]*>(?:(?!</hp:rect>).)*?#997FAB.*?</hp:rect>', sec, re.S)
    open(os.path.join(DES, "bogi_label.xml"), "w", encoding="utf-8").write(m.group(0))
    json.dump(idmap, open(os.path.join(DES, "idmap.json"), "w"), indent=1)
    print("디자인 저장:", DES, {k: len(v) for k, v in idmap.items()}, "단원명 자리:", title)


def apply(path, unitfile):
    sp = importlib.util.spec_from_file_location("u", unitfile)
    U = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(U)
    F, order, ctype = unzip(path)
    ghead = F["Contents/header.xml"].decode("utf-8")
    head = open(os.path.join(DES, "header.xml"), encoding="utf-8").read()
    idmap = json.load(open(os.path.join(DES, "idmap.json")))
    sec = F["Contents/section0.xml"].decode("utf-8")
    added = collections.Counter()
    for at in ["borderFillIDRef", "charPrIDRef", "paraPrIDRef", "styleIDRef"]:
        tag, plural = KIND[at]
        for mine in sorted(set(re.findall(r'\b%s="(\d+)"' % at, sec)), key=int):
            if mine in idmap[at]:
                continue
            x = defs(ghead, tag)[mine]                       # 완성본에 없던 모양: 생성본 정의를 옮겨 온다
            if tag == "charPr":
                x, head = refont(x, fonts(ghead), head)
            if tag == "paraPr":
                x = re.sub(r'borderFillIDRef="(\d+)"', lambda mm: 'borderFillIDRef="%s"' % idmap["borderFillIDRef"].get(mm.group(1), mm.group(1)), x)
            if tag == "style":
                idmap[at][mine] = "0"
                continue
            head, idmap[at][mine] = append_def(head, tag, plural, x)
            added[tag] += 1
        sec = re.sub(r'\b(%s)="(\d+)"' % at, lambda m: '%s="%s"' % (m.group(1), idmap[at].get(m.group(2), m.group(2))), sec)
    for a, b in COLOR:
        sec = sec.replace(a, b)
    # 발문의 '<보기>' → '보 기' 라벨
    lab = open(os.path.join(DES, "bogi_label.xml"), encoding="utf-8").read()
    k = [0]

    def label(m):
        k[0] += 1
        x = re.sub(r'\bid="\d+"', 'id="%d"' % (1890000000 + k[0]), lab, count=1)
        x = re.sub(r'\binstid="\d+"', 'instid="%d"' % (1890500000 + k[0]), x, count=1)
        return "</hp:t>" + x + "<hp:t>"
    sec = re.sub(r"&lt;보기&gt;", label, sec)
    sec = sec.replace("<hp:t></hp:t>", "")
    # 문항 번호 시작: 문항 번호 문단 모양이 가리키는 번호 매기기
    start = getattr(U, "START", 1)
    pid = idmap["paraPrIDRef"]["31"]
    pdef = defs(head, "paraPr")[pid]
    nid = re.search(r'<hh:heading type="NUMBER" idRef="(\d+)"', pdef).group(1)
    head = re.sub(r'(<hh:numbering id="%s" start=")\d+(">\s*<hh:paraHead start=")\d+(")' % nid,
                  lambda m: m.group(1) + str(start) + m.group(2) + str(start) + m.group(3), head, count=1)
    F["Contents/header.xml"] = head.encode("utf-8")
    F["Contents/section0.xml"] = sec.encode("utf-8")
    for mp in ("Contents/masterpage0.xml", "Contents/masterpage1.xml"):
        x = open(os.path.join(DES, os.path.basename(mp)), encoding="utf-8").read()
        F[mp] = x.replace("{{UNIT}}", U.UNIT[0].replace("&", "&amp;")).encode("utf-8")
    with zipfile.ZipFile(path, "w") as z:
        for name in order:
            ct = zipfile.ZIP_STORED if name == "mimetype" else zipfile.ZIP_DEFLATED
            z.writestr(zipfile.ZipInfo(name, date_time=(2026, 11, 6, 0, 0, 0)), F[name], compress_type=ct)
    print("디자인 입힘:", path, "보기 라벨", k[0], "새로 옮긴 모양", dict(added))


if __name__ == "__main__":
    if sys.argv[1] == "build":
        a = sys.argv[2:]
        build(list(zip(a[0::2], a[1::2])))
    else:
        apply(sys.argv[2], sys.argv[3])
