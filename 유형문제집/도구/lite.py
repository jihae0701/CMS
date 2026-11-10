# -*- coding: utf-8 -*-
"""CMS 스토리 라이트: 유형서 완성본에서 '단원 종합 문제'의 문항 몇 개만 바꿔 넣는다.

사용자 지시(2026-11-10): 유형서와 문항 수·디자인은 같게, 단원 끝 '단원 종합 문제'의 문항 중
모의고사 기출은 그대로 두고 나머지를 중·중상 난도 문항으로 바꾼다.

python lite.py 완성본.hwpx 명세.py 출력.hwpx
명세 모듈의 REPLACE = {단원종합 안의 차례(1부터): 문항, ...}
문항 = {"q": [글 | {"box": [줄, ...]} | {"ch": [보기 5개]}], "ans": 정답, "sol": [풀이 줄, ...], "src": 출처 메모}
글·풀이 줄은 '글 $수식$ 글' 꼴(공통수학1 유형서와 같은 한글 수식 스크립트).
완성본의 문단 모양을 그대로 쓴다: 번호 문단(미주 들어 있는 문단)·문제 문단·빈 문단(풀이 칸)은 그대로 두고,
문제 문단과 미주(풀이) 안의 글만 새로 쓴다. 조건 상자({"box"})는 완성본에 있는 조건 상자를 본떠 만든다.
"""
import re, sys, os, zipfile, shutil, importlib.util, html

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import eqstyle   # sizes(): 수식 크기 계산(gen.py와 같은 식, eqcache.json)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def top_paras(xml, start, end):
    """[start, end) 안의 맨 위 문단들의 (시작, 끝) 위치"""
    out, depth, st = [], 0, None
    for m in re.finditer(r"<hp:p [^>]*>|</hp:p>", xml[start:end]):
        if m.group(0).startswith("<hp:p "):
            if depth == 0:
                st = start + m.start()
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                out.append((st, start + m.end()))
    return out


class Builder:
    def __init__(self, xml):
        self.tpl = re.search(r"<hp:equation\b[^>]*>.*?</hp:equation>", xml, re.S).group(0)
        ids = [int(x) for x in re.findall(r'<hp:equation\b[^>]*\bid="(\d+)"', xml)]
        self.nid = max(ids) + 1000
        self.need = set()

    def collect(self, s):
        for m in re.finditer(r"\$(.+?)\$", s, re.S):
            self.need.add(m.group(1).strip())

    def sizes(self):
        self.EQ = eqstyle.sizes(sorted(self.need))

    def eq(self, sc):
        W, H, BL = self.EQ[sc]
        e = self.tpl
        e = re.sub(r'(<hp:equation\b[^>]*\bid=")\d+(")', lambda q: q.group(1) + str(self.nid) + q.group(2), e, count=1)
        self.nid += 1
        e = re.sub(r'(<hp:equation\b[^>]*\bbaseLine=")\d+(")', lambda q: q.group(1) + str(BL) + q.group(2), e, count=1)
        e = re.sub(r'(<hp:sz\b[^>]*\bwidth=")\d+(")', lambda q: q.group(1) + str(W) + q.group(2), e, count=1)
        e = re.sub(r'(<hp:sz\b[^>]*\bheight=")\d+(")', lambda q: q.group(1) + str(H) + q.group(2), e, count=1)
        e = re.sub(r"<hp:script[^>]*>.*?</hp:script>", lambda q: "<hp:script>" + esc(sc) + "</hp:script>", e, count=1, flags=re.S)
        return e

    def inline(self, text):
        out = []
        for i, part in enumerate(re.split(r"\$(.+?)\$", text, flags=re.S)):
            if i % 2:
                out.append(self.eq(part.strip()))
            elif part:
                out.append("<hp:t>%s</hp:t>" % esc(part))
        out.append("<hp:t/>")
        return "".join(out)

    def para(self, text, pp="3", cp="8"):
        return ('<hp:p id="0" paraPrIDRef="%s" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0">'
                '<hp:run charPrIDRef="%s">%s</hp:run></hp:p>' % (pp, cp, self.inline(text)))


PIC_DIR = os.path.join(HERE, "그림")


def png_size(path):
    import struct
    with open(path, "rb") as f:
        d = f.read(24)
    return struct.unpack(">II", d[16:24])


def pic_para(tpl, img_id, fn, width, pid):
    """그림 문단(가운데 정렬 paraPr 1). tpl: 문서 안의 아무 hp:pic"""
    pw, ph = png_size(os.path.join(PIC_DIR, fn))
    W, H = int(width), round(int(width) * ph / pw)
    x = tpl
    x = re.sub(r'binaryItemIDRef="[^"]+"', 'binaryItemIDRef="%s"' % img_id, x)
    x = re.sub(r'(<hp:pic\b[^>]*\bid=")\d+(")', lambda m: m.group(1) + str(pid) + m.group(2), x, count=1)
    x = re.sub(r'(<hp:pic\b[^>]*\binstid=")\d+(")', lambda m: m.group(1) + str(pid + 1) + m.group(2), x, count=1)
    x = re.sub(r'<hp:orgSz [^>]*/>', '<hp:orgSz width="%d" height="%d"/>' % (W, H), x)
    x = re.sub(r'<hp:curSz [^>]*/>', '<hp:curSz width="%d" height="%d"/>' % (W, H), x)
    x = re.sub(r'centerX="\d+" centerY="\d+"', 'centerX="%d" centerY="%d"' % (W // 2, H // 2), x)
    x = re.sub(r'<hc:scaMatrix [^>]*/>', '<hc:scaMatrix e1="1" e2="0" e3="0" e4="0" e5="1" e6="0"/>', x)
    x = re.sub(r'<hp:imgRect>.*?</hp:imgRect>', '<hp:imgRect><hc:pt0 x="0" y="0"/><hc:pt1 x="%d" y="0"/><hc:pt2 x="%d" y="%d"/>'
               '<hc:pt3 x="0" y="%d"/></hp:imgRect>' % (W, W, H, H), x, flags=re.S)
    x = re.sub(r'<hp:imgClip [^>]*/>', '<hp:imgClip left="0" right="%d" top="0" bottom="%d"/>' % (W, H), x)
    x = re.sub(r'<hp:imgDim [^>]*/>', '<hp:imgDim dimwidth="%d" dimheight="%d"/>' % (W, H), x)
    x = re.sub(r'<hp:sz width="\d+" widthRelTo="ABSOLUTE" height="\d+"', '<hp:sz width="%d" widthRelTo="ABSOLUTE" height="%d"' % (W, H), x)
    x = re.sub(r'<hp:pos [^>]*/>', '<hp:pos treatAsChar="1" affectLSpacing="0" flowWithText="1" allowOverlap="0" holdAnchorAndSO="0" '
               'vertRelTo="PARA" horzRelTo="PARA" vertAlign="TOP" horzAlign="LEFT" vertOffset="0" horzOffset="0"/>', x, count=1)
    if "<hp:shapeComment>" not in x:
        x = x.replace("</hp:pic>", "<hp:shapeComment>그림입니다.</hp:shapeComment></hp:pic>") if False else x
    return ('<hp:p id="0" paraPrIDRef="1" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0">'
            '<hp:run charPrIDRef="8">%s<hp:t/></hp:run></hp:p>' % x)


def choices_paras(b, ch):
    tab = '      <hp:tab width="4284" leader="0" type="1"/>'
    def line(items):
        run = []
        for k, (mark, v) in enumerate(items):
            pre = (tab if k else "") + mark + " "
            run.append("<hp:t>%s</hp:t>" % pre.replace("&", "&amp;") if not k else "<hp:t>%s</hp:t>" % (tab + mark + " "))
            run.append(b.inline(v)[:-len("<hp:t/>")] if "$" in v else b.eq(v.strip("$")))   # '(가): $1$'처럼 글이 섞인 선지
        run.append("<hp:t/>")
        return ('<hp:p id="0" paraPrIDRef="3" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0">'
                '<hp:run charPrIDRef="8">%s</hp:run></hp:p>' % "".join(run))
    marks = "①②③④⑤"
    return line(list(zip(marks[:3], ch[:3]))) + line(list(zip(marks[3:], ch[3:])))


def build(src, spec_path, out):
    sp = importlib.util.spec_from_file_location("spec", spec_path)
    spec = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(spec)
    zin = zipfile.ZipFile(src)
    items = [(i, zin.read(i.filename)) for i in zin.infolist()]
    zin.close()
    name = "Contents/section0.xml"
    xml = dict((i.filename, d) for i, d in items)[name].decode("utf-8")
    h = xml.find("단원 종합 문제")
    if h < 0:
        h = xml.find("단원종합문제")      # 3단원 완성본은 붙여 씀
    if h < 0:
        raise SystemExit("'단원 종합 문제' 제목이 없음")
    allp = top_paras(xml, 0, len(xml))
    hp = [k for k, (a, z) in enumerate(allp) if a <= h < z][0]   # 제목(그리기 개체 안 글)이 든 맨 위 문단
    paras = allp[hp + 1:]
    starts = [k for k, (a, z) in enumerate(paras) if "<hp:endNote" in xml[a:z]]
    blocks = []
    for n, k in enumerate(starts):
        k2 = starts[n + 1] if n + 1 < len(starts) else len(paras)
        blocks.append(paras[k:k2])
    print("단원 종합 문제", len(blocks), "문항")
    b = Builder(xml)
    for it in spec.REPLACE.values():
        for q in it["q"]:
            if isinstance(q, str):
                b.collect(q)
            elif "box" in q:
                for ln in q["box"]:
                    b.collect(ln)
            elif "ch" in q:
                for v in q["ch"]:
                    if "$" in v:
                        b.collect(v)
                    else:
                        b.need.add(v.strip("$"))
        for ln in it["sol"]:
            b.collect(ln)
        a = it["ans"]
        if "$" in a:
            b.collect(a)
        elif not re.match(r"[①-⑤ㄱ-ㅎ]", a):
            b.need.add(a)
    b.sizes()
    box_tpl = None
    for blk in blocks:
        for a, z in blk:
            if "<hp:tbl" in xml[a:z] and "(가)" in xml[a:z]:
                box_tpl = xml[a:z]
                break
        if box_tpl:
            break
    edits = []
    newpics = {}
    m = re.search(r"<hp:pic\b.*?</hp:pic>", xml, re.S)
    pic_tpl = m.group(0) if m else None
    for no, it in spec.REPLACE.items():
        blk = blocks[no - 1]
        first = xml[blk[0][0]:blk[0][1]]
        if re.search(r"\d{4}년 \d+월", first):
            raise SystemExit("%d번은 모의고사 문항 — 바꾸지 않는다" % no)
        # 미주(풀이) 다시 쓰기
        en = re.search(r"<hp:endNote .*?</hp:endNote>", first, re.S).group(0)
        auto = re.search(r"<hp:ctrl><hp:autoNum .*?</hp:ctrl>", en, re.S).group(0)
        head = re.match(r"<hp:endNote [^>]*><hp:subList [^>]*>", en).group(0)
        ans = it["ans"]
        if re.match(r"[①-⑤ㄱ-ㅎ]", ans):
            ans_x = "<hp:t>%s</hp:t>" % esc(ans)
        elif "$" in ans:                  # '$a=1$, $x+2y-1$'처럼 글과 수식이 섞인 답
            ans_x = b.inline(ans)[:-len("<hp:t/>")]
        else:
            ans_x = b.eq(ans)
        sp0 = ('<hp:p id="0" paraPrIDRef="23" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0">'
               '<hp:run charPrIDRef="26">%s<hp:t> [정답] </hp:t>%s<hp:t/></hp:run></hp:p>' % (auto, ans_x))
        sol = "".join(b.para(ln, pp="23", cp="26") for ln in it["sol"])
        first2 = first.replace(en, head + sp0 + sol + "</hp:subList></hp:endNote>")
        # 문제 문단: 빈 문단이 아닌 것을 모두 빼고 새 문단을 넣는다. 빈 문단(풀이 칸)은 그대로
        empties = []
        for a, z in blk[1:]:
            p = xml[a:z]
            if re.search(r"<hp:t>[^<]|<hp:equation|<hp:tbl|<hp:pic|<hp:rect", p):
                continue
            empties.append(p)
        new_q = []
        for q in it["q"]:
            if isinstance(q, str):
                new_q.append(b.para(q))
            elif "box" in q:
                if not box_tpl:
                    raise SystemExit("본뜰 조건 상자가 없음")
                inner = "".join('<hp:p id="0" paraPrIDRef="31" styleIDRef="2" pageBreak="0" columnBreak="0" merged="0">'
                                '<hp:run charPrIDRef="12">%s</hp:run></hp:p>' % b.inline(ln) for ln in q["box"])
                bx = re.sub(r'(<hp:drawText\b[^>]*><hp:subList [^>]*>).*?(</hp:subList>)', lambda m: m.group(1) + inner + m.group(2), box_tpl, count=1, flags=re.S)
                hgt = 1400 + 1250 * len(q["box"])
                bx = re.sub(r'(<hp:curSz width="\d+" height=")\d+(")', lambda m: m.group(1) + str(hgt) + m.group(2), bx)
                bx = re.sub(r'(<hp:sz width="10000" widthRelTo="COLUMN" height=")\d+(")', lambda m: m.group(1) + str(hgt) + m.group(2), bx)
                new_q.append(bx)
            elif "ch" in q:
                new_q.append(choices_paras(b, q["ch"]))
            elif "img" in q:
                fn = q["img"]
                if fn not in newpics:
                    newpics[fn] = "image%d" % (301 + len(newpics))
                new_q.append(pic_para(pic_tpl, newpics[fn], fn, q.get("w", 9000), b.nid))
                b.nid += 2
        new_blk = first2 + "".join(new_q) + "".join(empties)
        edits.append((blk[0][0], blk[-1][1], new_blk))
    for a, z, new in sorted(edits, reverse=True):
        xml = xml[:a] + new + xml[z:]
    out_items = []
    for info, data in items:
        if info.filename == name:
            data = xml.encode("utf-8")
        elif info.filename == "Contents/content.hpf" and newpics:
            hpf = data.decode("utf-8")
            k = hpf.index("/>", hpf.rindex('<opf:item id="image')) + 2
            add = "".join('<opf:item id="%s" href="BinData/%s.png" media-type="image/png" isEmbeded="1"/>' % (v, v) for v in newpics.values())
            data = (hpf[:k] + add + hpf[k:]).encode("utf-8")
        out_items.append((info, data))
    for fn, v in newpics.items():
        zi = zipfile.ZipInfo("BinData/%s.png" % v, date_time=(2026, 11, 10, 0, 0, 0))
        zi.compress_type = zipfile.ZIP_DEFLATED
        out_items.append((zi, open(os.path.join(PIC_DIR, fn), "rb").read()))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with zipfile.ZipFile(out, "w") as z:
        for info, data in out_items:
            z.writestr(info, data, compress_type=info.compress_type)
    print("바꾼 문항:", sorted(spec.REPLACE), "->", out)


if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2], sys.argv[3])
