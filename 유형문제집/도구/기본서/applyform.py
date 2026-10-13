# -*- coding: utf-8 -*-
"""기본서 양식(기본서/원본/기본서_form.hwpx)의 바탕쪽(머리말·꼬리말)과 쪽 여백을 기본서 단원 파일에 입힌다.

python applyform.py <양식.hwpx> <기본서 단원.hwpx> [<출력.hwpx>]
- 양식의 masterpage0(짝수 쪽)·masterpage1(홀수 쪽)을 그대로 가져오고, 단원 제목 글자만 바꾼다
  (masterpage1 '1. 수열의 극한' → '7. 여러 가지 방정식', masterpage0 '(문단 번호 1.) 수열의 극한' → '7. 여러 가지 방정식').
- 바탕쪽이 쓰는 글자 모양·문단 모양·테두리·탭·글꼴은 단원 파일 header.xml에 같은 것이 있으면 그것을 쓰고,
  없으면 새 번호로 덧붙인다(여러 번 돌려도 늘어나지 않음).
- 쪽 여백(<hp:margin>)은 양식 값으로 바꾼다. 본문 단 너비는 양식과 같다(29,620).
"""
import re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hwpxio as io

FORM = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "기본서", "원본", "기본서_form.hwpx")
LANGS = ["HANGUL", "LATIN", "HANJA", "JAPANESE", "OTHER", "SYMBOL", "USER"]
FR_KEYS = ["hangul", "latin", "hanja", "japanese", "other", "symbol", "user"]


def _elem_at(h, start, tag):
    """start 위치의 <hh:tag ...> 요소 전체(스스로 닫히는 요소 포함)"""
    gt = h.index(">", start)
    if h[gt - 1] == "/":
        return h[start:gt + 1]
    return h[start:h.index("</hh:%s>" % tag, gt) + len("</hh:%s>" % tag)]


def _elem(h, tag, i):
    m = re.search(r'<hh:%s id="%s"[ >/]' % (tag, i), h)
    return _elem_at(h, m.start(), tag)


def _block(h, tag):
    """<hh:tags itemCnt="n"> ... </hh:tags> 블록"""
    return re.search(r'<hh:%s itemCnt="\d+">.*?</hh:%s>' % (tag, tag), h, re.S)


def _items(block, tag):
    return [_elem_at(block, m.start(), tag) for m in re.finditer(r'<hh:%s id="\d+"[ >/]' % tag, block)]


def _norm(e):
    return re.sub(r'\bid="\d+"', 'id=""', e, count=1)


class Merger:
    def __init__(self, src_h, dst_h):
        self.src, self.dst = src_h, dst_h
        self.font_map = {}

    # ---- 글꼴: 언어별로 이름이 같은 글꼴을 찾고, 없으면 덧붙인다
    def font(self, lang, fid):
        key = (lang, fid)
        if key in self.font_map:
            return self.font_map[key]
        sblk = re.search(r'<hh:fontface lang="%s" fontCnt="\d+">.*?</hh:fontface>' % lang, self.src, re.S).group(0)
        fe = re.search(r'<hh:font id="%s" .*?</hh:font>' % fid, sblk, re.S).group(0)
        face = re.search(r'face="([^"]*)"', fe).group(1)
        m = re.search(r'<hh:fontface lang="%s" fontCnt="(\d+)">.*?</hh:fontface>' % lang, self.dst, re.S)
        dblk = m.group(0)
        hit = re.search(r'<hh:font id="(\d+)" face="%s"' % re.escape(face), dblk)
        if hit:
            nid = hit.group(1)
        else:
            nid = str(int(m.group(1)))
            new_fe = re.sub(r'id="\d+"', 'id="%s"' % nid, fe, count=1)
            nblk = dblk.replace("</hh:fontface>", new_fe + "</hh:fontface>")
            nblk = re.sub(r'fontCnt="\d+"', 'fontCnt="%d"' % (int(nid) + 1), nblk, count=1)
            self.dst = self.dst.replace(dblk, nblk, 1)
        self.font_map[key] = nid
        return nid

    # ---- 같은 정의가 있으면 그 번호, 없으면 새 번호로 덧붙인다
    def put(self, blocktag, tag, elem, first_id):
        m = _block(self.dst, blocktag)
        blk = m.group(0)
        items = _items(blk, tag)
        for it in items:
            if _norm(it) == _norm(elem):
                return re.search(r'id="(\d+)"', it).group(1)
        ids = [int(re.search(r'id="(\d+)"', it).group(1)) for it in items]
        nid = max(ids) + 1 if ids else first_id
        ne = re.sub(r'\bid="\d+"', 'id="%d"' % nid, elem, count=1)
        nblk = blk[:blk.rindex("</hh:%s>" % blocktag)] + ne + "</hh:%s>" % blocktag
        nblk = re.sub(r'itemCnt="\d+"', 'itemCnt="%d"' % (len(items) + 1), nblk, count=1)
        self.dst = self.dst[:m.start()] + nblk + self.dst[m.end():]
        return str(nid)

    def border_fill(self, i):
        e = _elem(self.src, "borderFill", i)
        return self.put("borderFills", "borderFill", e, 1)

    def tab(self, i):
        e = _elem(self.src, "tabPr", i)
        return self.put("tabProperties", "tabPr", e, 0)

    def char(self, i):
        e = _elem(self.src, "charPr", i)
        fr = re.search(r"<hh:fontRef [^>]*/>", e).group(0)
        nfr = fr
        for lang, k in zip(LANGS, FR_KEYS):
            v = re.search(r'%s="(\d+)"' % k, fr).group(1)
            nfr = re.sub(r'\b%s="\d+"' % k, '%s="%s"' % (k, self.font(lang, v)), nfr)
        e = e.replace(fr, nfr)
        e = re.sub(r'borderFillIDRef="(\d+)"', lambda m: 'borderFillIDRef="%s"' % self.border_fill(m.group(1)), e)
        return self.put("charProperties", "charPr", e, 0)

    def para(self, i):
        e = _elem(self.src, "paraPr", i)
        e = re.sub(r'tabPrIDRef="(\d+)"', lambda m: 'tabPrIDRef="%s"' % self.tab(m.group(1)), e)
        e = re.sub(r'borderFillIDRef="(\d+)"', lambda m: 'borderFillIDRef="%s"' % self.border_fill(m.group(1)), e)
        # 짝수 쪽 제목 상자는 문단 번호(^1.)로 '1.'을 붙이므로, 번호를 끄고 단원 번호를 글자로 쓴다
        e = re.sub(r'<hh:heading type="\w+" idRef="\d+" level="\d+"/>', '<hh:heading type="NONE" idRef="0" level="0"/>', e)
        return self.put("paraProperties", "paraPr", e, 0)


def remap_master(x, mg):
    x = re.sub(r'charPrIDRef="(\d+)"', lambda m: 'charPrIDRef="%s"' % mg.char(m.group(1)), x)
    x = re.sub(r'paraPrIDRef="(\d+)"', lambda m: 'paraPrIDRef="%s"' % mg.para(m.group(1)), x)
    x = re.sub(r'borderFillIDRef="(\d+)"', lambda m: 'borderFillIDRef="%s"' % mg.border_fill(m.group(1)), x)
    assert not re.search(r'styleIDRef="[1-9]', x), "바탕쪽은 바탕글 스타일만 쓴다"
    return x


def apply(form_path, unit_path, out_path, unit_no, unit_title):
    F, _ = io.read(form_path)
    U, order = io.read(unit_path)
    assert F["BinData/image1.png"] == U["BinData/image1.png"], "로고 그림(image1)이 다르다"
    mg = Merger(F["Contents/header.xml"].decode("utf-8"), U["Contents/header.xml"].decode("utf-8"))
    for name in ("Contents/masterpage0.xml", "Contents/masterpage1.xml"):
        x = F[name].decode("utf-8")
        x = remap_master(x, mg)
        x = x.replace("<hp:t>1. 수열의 극한</hp:t>", "<hp:t>%s %s</hp:t>" % (unit_no, unit_title))
        x = x.replace("<hp:t>수열의 극한</hp:t>", "<hp:t>%s %s</hp:t>" % (unit_no, unit_title))
        assert "수열의 극한" not in x
        U[name] = x.encode("utf-8")
    U["Contents/header.xml"] = mg.dst.encode("utf-8")
    sec = U["Contents/section0.xml"].decode("utf-8")
    fmargin = re.search(r"<hp:margin [^>]*/>", F["Contents/section0.xml"].decode("utf-8")).group(0)
    sec = re.sub(r"<hp:margin [^>]*/>", fmargin, sec, count=1)
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import eqfix   # 한글 수식의 '<-'(← 명령)를 '< it-'로
    sec = eqfix.fix_xml(sec)[0]
    U["Contents/section0.xml"] = sec.encode("utf-8")
    io.write(out_path, U, order)


def unit_of(path):
    m = re.match(r"(\d+)\. (.+)\.hwpx$", os.path.basename(path))
    return m.group(1) + ".", m.group(2)


if __name__ == "__main__":
    form, unit = sys.argv[1], sys.argv[2]
    out = sys.argv[3] if len(sys.argv) > 3 else unit
    no, title = unit_of(out)
    apply(form, unit, out, no, title)
    print("양식 적용:", out)
