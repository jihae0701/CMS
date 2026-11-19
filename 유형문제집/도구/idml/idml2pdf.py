# -*- coding: utf-8 -*-
"""우리가 만든 인디자인(IDML) 책을 PDF로 (인디자인 없이) (2026-11-19).
python idml2pdf.py <책.idml> <출력.pdf> <Pretendard 폴더> <링크파일이름=PDF경로> ...
- 사용자: '위에 만든 인디자인 파일들 PDF로 만들어 줄 수 있어?'(링크가 끊겨 있어서).
- IDML에서 쪽마다 읽어 그대로 그림: 놓인 PDF 쪽(링크 이름 → 받은 단원 PDF, 쪽 번호·크기·자리 그대로), 단원 표지(채운 글상자 색 + 'N 단원명'),
  1쪽 '이 책의 차례'와 차례 글상자(탭 오른쪽 맞춤 + 가운뎃점 채움), 쪽 번호 글상자(자동 쪽 번호 → 그 쪽 번호).
- 글꼴: 인디자인 글꼴(a파도소리·아는체·HY울릉도M)이 여기 없어 Pretendard로 바꿔 씀 — 제목 ExtraBold(흰 글자 + 검은 테두리), 차례 Bold, 쪽 번호 SemiBold.
  크기·자리는 IDML 값 그대로.
"""
import sys, os, re, zipfile
from urllib.parse import unquote
import pymupdf

idml, out, pdir = sys.argv[1:4]
LINK = dict(a.split("=", 1) for a in sys.argv[4:])
F_TITLE = os.path.join(pdir, "Pretendard-ExtraBold.otf")
F_TOC = os.path.join(pdir, "Pretendard-Bold.otf")
F_PN = os.path.join(pdir, "Pretendard-SemiBold.otf")

z = zipfile.ZipFile(idml)
T = lambda n: z.read(n).decode("utf-8")
dm = T("designmap.xml")
gr = T("Resources/Graphic.xml")
COLORS = {m.group(1): m for m in re.finditer(r'<Color Self="(Color/[^"]+)"[^>]*>', gr)}


def rgb(name):
    if name == "Color/Paper": return (1, 1, 1)
    if name == "Color/Black": return (0, 0, 0)
    m = COLORS.get(name)
    if not m: return (0, 0, 0)
    tag = m.group(0)
    v = list(map(float, re.search(r'ColorValue="([^"]+)"', tag).group(1).split()))
    if 'Space="RGB"' in tag:
        return tuple(x / 255 for x in v)
    c, mm, y, k = [x / 100 for x in v]
    return ((1 - c) * (1 - k), (1 - mm) * (1 - k), (1 - y) * (1 - k))


def story(sid):
    return T("Stories/Story_%s.xml" % sid)


def box(el):
    """요소의 펼침면 좌표 상자 (ItemTransform이 이동만 있다고 봄)"""
    tr = list(map(float, re.search(r'ItemTransform="([^"]+)"', el.split(">", 1)[0]).group(1).split()))
    pts = [tuple(map(float, a.split())) for a in re.findall(r'PathPointType Anchor="([^"]+)"', el)]
    xs = [tr[0] * x + tr[2] * y + tr[4] for x, y in pts]
    ys = [tr[1] * x + tr[3] * y + tr[5] for x, y in pts]
    return min(xs), min(ys), max(xs), max(ys)


def text_white_stroke(page, rect, text, size, fill, stroke, sw, font, fontname, align_center=True):
    tw = font.text_length(text, size)
    x = (rect.x0 + rect.x1) / 2 - tw / 2 if align_center else rect.x0
    y = rect.y0 + size * 0.9 + 4
    page.insert_text((x, y), text, fontsize=size, fontname=fontname, fontfile=None, color=stroke, fill=fill,
                     render_mode=2, border_width=sw / size)


doc = pymupdf.open()
src = {}
fonts = {}
for key, path in (("T", F_TITLE), ("C", F_TOC), ("P", F_PN)):
    fonts[key] = pymupdf.Font(fontfile=path)
PH = None
for f in re.findall(r'<idPkg:Spread src="([^"]+)"', dm):
    s = T(f)
    pages = re.findall(r"<Page .*?</Page>", s, re.S)
    plist = []
    for p in pages:
        gb = list(map(float, re.search(r'GeometricBounds="([^"]+)"', p).group(1).split()))
        tr = list(map(float, re.search(r'ItemTransform="([^"]+)"', p).group(1).split()))
        name = re.search(r' Name="([^"]+)"', p).group(1)
        x0, y0 = tr[4] + gb[1], tr[5] + gb[0]
        plist.append(dict(name=name, x0=x0, y0=y0, x1=tr[4] + gb[3], y1=tr[5] + gb[2], items=[]))
    body = re.sub(r"<Page .*?</Page>", "", s, flags=re.S)

    def page_of(bx):
        cx = (bx[0] + bx[2]) / 2
        for pg in plist:
            if pg["x0"] - 1 <= cx <= pg["x1"] + 1:
                return pg
        return plist[0]
    for m in re.finditer(r"<Rectangle Self=.*?</Rectangle>", body, re.S):
        r = m.group(0)
        if "<PDF " not in r: continue
        lk = unquote(re.search(r'LinkResourceURI="([^"]+)"', r).group(1)).rsplit("/", 1)[1]
        pn = int(re.search(r'PageNumber="(\d+)"', r).group(1))
        bx = box(r)
        page_of(bx)["items"].append(("pdf", bx, lk, pn))
    for m in re.finditer(r'<TextFrame Self="[^"]+" ParentStory="([^"]+)"[^>]*>.*?</TextFrame>', body, re.S):
        el, sid = m.group(0), m.group(1)
        st = story(sid)
        bx = box(el)
        fill = re.search(r'FillColor="([^"]+)"', el.split(">", 1)[0])
        page_of(bx)["items"].append(("text", bx, st, fill.group(1) if fill else None))
    for pg in plist:
        W, H = pg["x1"] - pg["x0"], pg["y1"] - pg["y0"]
        page = doc.new_page(width=W, height=H)
        for key, path in (("T", F_TITLE), ("C", F_TOC), ("P", F_PN)):
            page.insert_font(fontname="f" + key, fontfile=path)
        loc = lambda bx: pymupdf.Rect(bx[0] - pg["x0"], bx[1] - pg["y0"], bx[2] - pg["x0"], bx[3] - pg["y0"])
        # 그리는 차례: PDF → 채운 글상자 → 글
        for it in pg["items"]:
            if it[0] == "pdf":
                _, bx, lk, pn = it
                if lk not in LINK:
                    raise SystemExit("PDF 없음: %s" % lk)
                if lk not in src: src[lk] = pymupdf.open(LINK[lk])
                page.show_pdf_page(loc(bx), src[lk], pn - 1, keep_proportion=True)
        for it in pg["items"]:
            if it[0] == "text" and it[3] and it[3] not in ("Swatch/None",):
                page.draw_rect(loc(it[1]), color=None, fill=rgb(it[3]), overlay=True)
        for it in pg["items"]:
            if it[0] != "text": continue
            _, bx, st, _f = it
            R = loc(bx)
            cs = re.findall(r"<Content>([^<]*)</Content>", st)
            if "<?ACE 18?>" in st and not "".join(cs).replace("<?ACE 18?>", "").strip():
                size = float(re.search(r'PointSize="([\d.]+)"', st).group(1)) if 'PointSize="' in st else 11
                t = pg["name"]
                tw = fonts["P"].text_length(t, size)
                page.insert_text(((R.x0 + R.x1) / 2 - tw / 2, (R.y0 + R.y1) / 2 + size * 0.36), t, fontsize=size, fontname="fP", color=(0, 0, 0))
                continue
            if not cs: continue
            size = float(re.search(r'PointSize="([\d.]+)"', st).group(1)) if 'PointSize="' in st else 12
            fillc = re.search(r'<CharacterStyleRange [^>]*FillColor="([^"]+)"', st)
            strk = re.search(r'<CharacterStyleRange [^>]*StrokeColor="([^"]+)"', st)
            swm = re.search(r'<CharacterStyleRange [^>]*StrokeWeight="([\d.]+)"', st)
            if "\t" in "".join(cs):                                    # 차례: 왼쪽 글 + 오른쪽 맞춤 탭(가운뎃점 채움)
                tab = float(re.search(r"<Position type=\"unit\">([\d.]+)</Position>", st).group(1)) if "<Position" in st else R.width
                after = float(re.search(r'SpaceAfter="([\d.]+)"', st).group(1)) if "SpaceAfter" in st else 0
                lead = size * 1.2 + after
                y = R.y0 + size
                for line in cs:
                    left, right = line.split("\t", 1)
                    page.insert_text((R.x0, y), left, fontsize=size, fontname="fC", color=(0, 0, 0))
                    rw = fonts["C"].text_length(right, size)
                    xr = R.x0 + tab
                    page.insert_text((xr - rw, y), right, fontsize=size, fontname="fC", color=(0, 0, 0))
                    lw = fonts["C"].text_length(left, size)
                    dot = fonts["C"].text_length("·", size)
                    xd = R.x0 + lw + 4
                    while xd + dot < xr - rw - 4:
                        page.insert_text((xd, y), "·", fontsize=size, fontname="fC", color=(0.25, 0.25, 0.25))
                        xd += dot * 1.6
                    y += lead
                continue
            t = "".join(cs)
            fill = rgb(fillc.group(1)) if fillc else (0, 0, 0)
            if strk:
                sw = float(swm.group(1)) if swm else 1
                tw = fonts["T"].text_length(t, size)
                x = (R.x0 + R.x1) / 2 - tw / 2
                yb = R.y0 + size * 0.95
                page.insert_text((x, yb), t, fontsize=size, fontname="fT", color=rgb(strk.group(1)), fill=fill,
                                 render_mode=2, border_width=sw / size * 0.7)   # 테두리 굵기는 글자 크기에 대한 비율(InDesign 2pt 테두리 ≈ 바깥 1pt)
            else:
                tw = fonts["T"].text_length(t, size)
                page.insert_text(((R.x0 + R.x1) / 2 - tw / 2, R.y0 + size), t, fontsize=size, fontname="fT", color=fill)
doc.save(out, garbage=3, deflate=True)
print("쪽", doc.page_count, "->", out)
