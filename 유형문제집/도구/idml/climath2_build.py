# -*- coding: utf-8 -*-
"""기본서 공통수학2 CLIMATH(m) IDML 만들기 (2026-11-18).
python climath2_build.py <공통수학2 틀.idml> <공통수학1 v2.idml> <단원 PDF 폴더> <출력.idml> [c2b|c2y|c1y]
- c1y·c2y(유형서, 2026-11-18 사용자 '유형서는 PDF 자체에 쪽 번호가 있으니 쪽 번호 넣는 작업만 빼고', '기본서와 같은 틀 사용'):
  쪽 번호 글상자 없음, 링크 파일 '01 평면좌표.pdf' 꼴(사용자 파일 이름), 링크 폴더 …/유형서/,
  B4(257×364mm) PDF를 기본서 PDF와 같은 너비(595.22pt)로 줄여(약 81.6%) 쪽 위에 맞춤 → 높이 약 842.6pt(기본서 A4 PDF와 같음), 인쇄된 쪽 번호(아래에서 약 75pt)는 쪽 안에 들어옴.
- 틀: 사용자가 준 'CLIMATH(m) 공통수학2.indd' IDML(바인더1.pdf 264쪽을 쪽마다 놓은 것). 1쪽 펼침면(쪽 uf1, 섹션 시작)과 마스터·스타일은 그대로 두고
  나머지 펼침면은 새로 만든다.
- 사용자 지시: 바인더1.pdf 대신 단원별 PDF('N. 단원명.pdf', 사용자 파일 이름 그대로), 1쪽은 PDF 없이 흰 쪽에 '이 책의 차례'와 차례만(3번),
  단원마다 보라색 단원 표지 쪽(짝수 쪽)을 넣고 단원 PDF는 홀수 쪽부터, 모자라면 빈 쪽(이번엔 단원 쪽수가 모두 홀수라 빈 쪽 없음), 빠른정답 없음.
- 디자인은 공통수학1 v2(사용자 수정본)에서 복사: 1쪽 제목 글상자(u13a)·차례 글상자(u150), 단원 표지의 보라 글상자(u19a, RGB 145 102 165)·단원명 글상자(u1b0),
  쪽 번호(HY울릉도M 11pt, 2단 가운데 줄 기준 오른쪽 쪽 +10pt·왼쪽 쪽 −10pt, 1쪽·표지 쪽 없음).
- 차례: 'N. 단원명<탭>표지 쪽' (대단원·빠른정답 줄 없음).
"""
import sys, os, re, zipfile, subprocess
from urllib.parse import quote

tpl, c1, pdfdir, out = sys.argv[1:5]
BOOK = sys.argv[5] if len(sys.argv) > 5 else "c2b"
YU = BOOK.endswith("y")                                   # 유형서: 쪽 번호 없음
UNITS = {"2": ["평면좌표", "직선의 방정식", "원의 방정식", "도형의 이동", "집합의 뜻과 표현", "집합의 연산",
               "명제", "절대부등식", "함수", "합성함수와 역함수", "유리함수", "무리함수"],
         "1": ["다항식의 연산과 항등식", "나머지정리", "인수분해", "복소수와 이차방정식", "이차함수와 이차방정식의 관계", "이차함수의 최대·최소",
               "여러 가지 방정식", "이차부등식", "연립부등식", "경우의 수와 순열", "조합", "행렬"]}[BOOK[1]]
if BOOK == "c1c":   # 2026-11-19 CLIMATH ⓒ 공통수학1 (14단원, 사용자 단원 PDF 머리말·파일 이름)
    UNITS = ["다항식의 연산", "항등식", "나머지정리", "인수분해", "복소수", "이차함수와 이차방정식의 관계", "이차함수의 최대·최소",
             "고차방정식", "연립방정식", "연립부등식과 이차부등식", "연립이차부등식", "순열", "조합", "행렬"]
NU = len(UNITS)
# 링크 파일 이름 = 사용자 PDF 이름(기본서 '1. 평면좌표.pdf', 유형서 '01 평면좌표.pdf'), 단원명은 PDF 머리말과 같게
FILES = [("%02d %s.pdf" if YU else "%d. %s.pdf") % (i + 1, u) for i, u in enumerate(UNITS)]
# 2026-11-18 사용자 수정본(유형서 공통수학1 IDML)을 따름: 유형서 링크 이름은 밑줄('01_다항식의_연산과_항등식.pdf', '06_이차함수의_최대_최소.pdf'),
# 단원 표지 색은 주황(RGB 243 134 35). 기본서는 보라(145 102 165).
if YU:   # 사용자 실제 파일 이름(탐색기 화면, 2026-11-19): 공통수학1은 모두 밑줄, 공통수학2는 번호 뒤만 밑줄('02_직선의 방정식.pdf')
    FILES = [(re.sub(r"[ ·]", "_", f[:-4]) if BOOK == "c1y" else re.sub(r"^(\d\d) ", r"\1_", f[:-4])) + ".pdf" for f in FILES]
COVER_RGB = {"c1y": "243 134 35", "c2y": "32 123 77"}.get(BOOK, "145 102 165")   # 2026-11-19: 유형서는 그 책 메인색(표지와 같게) — 공통수학1 주황, 공통수학2 초록 #207B4D
OFF = 10.0
PW, PH = 595.2755905509999, 807.8740157480315
SPREAD_DY = 987.8740157480315

zt, zc = zipfile.ZipFile(tpl), zipfile.ZipFile(c1)
files = {n: zt.read(n) for n in zt.namelist()}
order = zt.namelist()
T = lambda n: files[n].decode("utf-8")
C = lambda n: zc.read(n).decode("utf-8")
dm = T("designmap.xml")
layer = re.search(r'<Layer Self="([^"]+)"', dm).group(1)
used = set(re.findall(r'Self="([^"]+)"', "".join(v.decode("utf-8", "ignore") for k, v in files.items() if k.endswith(".xml"))))

# 단원 쪽수
def npages(p):
    o = subprocess.check_output(["pdfinfo", p]).decode()
    return int(re.search(r"Pages:\s+(\d+)", o).group(1))

counts = [npages(os.path.join(pdfdir, "u%02d.pdf" % (i + 1))) for i in range(NU)]
sizes = [os.path.getsize(os.path.join(pdfdir, "u%02d.pdf" % (i + 1))) for i in range(NU)]
def psize(p):
    o = subprocess.check_output(["pdfinfo", p]).decode()
    return tuple(map(float, re.search(r"Page size:\s+([\d.]+) x ([\d.]+)", o).groups()))
psz = [psize(os.path.join(pdfdir, "u%02d.pdf" % (i + 1))) for i in range(NU)]

# 쪽 배치: 1=차례, 단원마다 짝수 표지 + 홀수부터 본문(+필요하면 빈 쪽)
plan = {1: ("toc",)}
starts, p = [], 2
for u, n in enumerate(counts):
    if p % 2 == 1:
        plan[p] = ("blank",); p += 1
    starts.append(p)
    plan[p] = ("cover", u); p += 1
    for k in range(n):
        plan[p] = ("pdf", u, k + 1); p += 1
    if n % 2 == 0:
        plan[p] = ("blank",); p += 1
TOTAL = p - 1
if TOTAL % 2 == 0:
    plan[TOTAL + 1] = ("blank",); TOTAL += 1
print("총 쪽수", TOTAL, "표지 쪽", starts, "빈 쪽", [k for k, v in plan.items() if v[0] == "blank"])

cnt = [0x3a000]
def nid():
    while True:
        cnt[0] += 1
        s = "u%x" % cnt[0]
        if s not in used:
            used.add(s)
            return s

# ---- 공통수학1 v2에서 디자인 가져오기
c1sp = {f: C(f) for f in zc.namelist() if f.startswith("Spreads/")}
def c1_item(tag, sid):
    for s in c1sp.values():
        m = re.search(r'<%s Self="%s".*?</%s>' % (tag, sid, tag), s, re.S)
        if m:
            return m.group(0)
    raise KeyError(sid)

def clone_frame(xml, fid, stid):
    x = re.sub(r'^<TextFrame Self="[^"]+" ParentStory="[^"]+"', '<TextFrame Self="%s" ParentStory="%s"' % (fid, stid), xml)
    x = re.sub(r' BeforeGroupingLayerReference="[^"]*"', "", x)
    x = re.sub(r' BeforeGroupingLayerPosition="[^"]*"', ' BeforeGroupingLayerPosition="-1"', x, count=1)
    if "ItemLayer=" in x.split(">", 1)[0]:
        x = re.sub(r'ItemLayer="[^"]*"', 'ItemLayer="%s"' % layer, x, count=1)
    else:
        x = x.replace(' LocalDisplaySetting=', ' ItemLayer="%s" Locked="false" LocalDisplaySetting=' % layer, 1)
    return x

def clone_story(sid_old, sid_new, content=None):
    x = C("Stories/Story_%s.xml" % sid_old).replace('<Story Self="%s"' % sid_old, '<Story Self="%s"' % sid_new, 1)
    if content is not None:
        x = re.sub(r"<Content>.*</Content>", lambda m: content, x, count=1, flags=re.S)
    return x

PURPLE = nid()
fr_title, fr_toc = c1_item("TextFrame", "u13a"), c1_item("TextFrame", "u150")
fr_purple, fr_unit = c1_item("TextFrame", "u19a"), c1_item("TextFrame", "u1b0")
fr_purple = fr_purple.replace('FillColor="Color/uf1"', 'FillColor="Color/%s"' % PURPLE)
pn_story_src = "u1ca"

new_stories = []
def add_story(xml, sid):
    files["Stories/Story_%s.xml" % sid] = xml.encode("utf-8")
    new_stories.append(sid)

esc = lambda t: t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

# ---- 템플릿 조각
sp1_name = re.findall(r'<idPkg:Spread src="([^"]+)"', dm)
s2 = T(sp1_name[1])
page_tpl = re.findall(r"<Page .*?</Page>", s2, re.S)[0]
rect_tpl = re.search(r"<Rectangle .*?</Rectangle>", s2, re.S).group(0)
rect_tpl = re.sub(r"<MetadataPacketPreference>.*?</MetadataPacketPreference>\s*", "", rect_tpl, flags=re.S)
head_tpl = s2[:s2.index("<Page ")]
link_dir = re.search(r'LinkResourceURI="(file:[^"]*/)[^"/]*"', rect_tpl).group(1)
if YU:                                                     # 사용자: '공통수학1 유형서 PDF 위치 H:/…/공통수학1_기본서_유형서/유형서/'
    link_dir = link_dir.replace(quote("/기본서/"), quote("/유형서/"))
link_dir = link_dir.replace(quote("공통수학2_기본서_유형서"), quote("공통수학%s_기본서_유형서" % BOOK[1]))
if BOOK == "c1c":                                          # 사용자 자료 폴더(탐색기 화면): E:\…\2027 예비고1 교재\CLIMATH 공통수학1 (C) 2027년\
    link_dir = link_dir.replace(quote("공통수학2_기본서_유형서/기본서/"), quote("CLIMATH 공통수학1 (C) 2027년/")).replace("file:H:/", "file:E:/")
PAGE_TY = -403.93700787401576

def page_xml(num, left):
    x = re.sub(r'<Page Self="[^"]+"', '<Page Self="%s"' % nid(), page_tpl, count=1)
    x = re.sub(r'ItemTransform="[^"]+"', 'ItemTransform="1 0 0 1 %s %s"' % (repr(-PW) if left else "0", repr(PAGE_TY)), x, count=1)
    x = re.sub(r' Name="\d+"', ' Name="%d"' % num, x, count=1)
    x = re.sub(r'(<ListItem type="long">)\d+(</ListItem>)', lambda m: m.group(1) + str(num) + m.group(2), x)
    return x

def rect_xml(u, k, left):
    x = rect_tpl
    x = re.sub(r'<Rectangle Self="[^"]+"', '<Rectangle Self="%s"' % nid(), x, count=1)
    x = re.sub(r'<PDF Self="[^"]+"', '<PDF Self="%s"' % nid(), x, count=1)
    x = re.sub(r'<Link Self="[^"]+"', '<Link Self="%s"' % nid(), x, count=1)
    x = re.sub(r'(<Rectangle [^>]*ItemTransform=")[^"]+"', lambda m: m.group(1) + "1 0 0 1 %s 17.062992125984238\"" % ("-297.66560519943744" if left else "297.6099853515625"), x, count=1)
    x = re.sub(r'PageNumber="\d+"', 'PageNumber="%d"' % k, x, count=1)
    w, h = psz[u]
    if abs(w - 595.22) > 0.5 or abs(h - 842) > 0.5:          # 크기가 다른 PDF(유형서 B4): 너비 595.22pt로 줄여 쪽 위에 맞춤
        sc = 595.219970703125 / w
        hw, hh = 297.6099853515625, h * sc / 2
        x = re.sub(r'<PathPointType Anchor="(-?)297.6099853515625 (-?)421" LeftDirection="-?297.6099853515625 -?421" RightDirection="-?297.6099853515625 -?421" />',
                   lambda m: '<PathPointType Anchor="{0}{1} {2}{3}" LeftDirection="{0}{1} {2}{3}" RightDirection="{0}{1} {2}{3}" />'.format(m.group(1), hw, m.group(2), hh), x)
        x = re.sub(r'(<Rectangle [^>]*ItemTransform="1 0 0 1 \S+ )\S+"', lambda m: m.group(1) + repr(PAGE_TY + hh) + '"', x, count=1)
        x = re.sub(r'(<PDF [^>]*ItemTransform=")[^"]+"', lambda m: m.group(1) + "%r 0 0 %r %r %r\"" % (sc, sc, -hw, -hh), x, count=1)
        x = re.sub(r'<GraphicBounds [^>]*/>', '<GraphicBounds Left="0" Top="0" Right="%g" Bottom="%g" />' % (w, h), x, count=1)
    x = re.sub(r'LinkResourceURI="[^"]+"', 'LinkResourceURI="%s%s"' % (link_dir, quote(FILES[u])), x, count=1)
    x = re.sub(r'LinkImportStamp="file (\d+) \d+"', lambda m: 'LinkImportStamp="file %s %d"' % (m.group(1), sizes[u]), x, count=1)
    x = re.sub(r'LinkResourceSize="[^"]+"', 'LinkResourceSize="0~%x"' % sizes[u], x, count=1)
    return x

def pn_frame(left):
    a, b = (-PW, 0) if left else (0, PW)
    cx = (a + b) / 2 + (-OFF if left else OFF)
    bottom = PAGE_TY + PH
    sid, fid = nid(), nid()
    add_story(clone_story(pn_story_src, sid), sid)
    x0, y0, x1, y1 = cx - 30, bottom - 30, cx + 30, bottom - 12
    hw, hh = 30.0, 9.0
    pts = "".join('<PathPointType Anchor="%.4f %.4f" LeftDirection="%.4f %.4f" RightDirection="%.4f %.4f" />' % (x, y, x, y, x, y)
                  for x, y in ((-hw, -hh), (-hw, hh), (hw, hh), (hw, -hh)))
    return ('<TextFrame Self="%s" ParentStory="%s" PreviousTextFrame="n" NextTextFrame="n" ContentType="TextType" ItemLayer="%s" Locked="false" '
            'AppliedObjectStyle="ObjectStyle/$ID/[Normal Text Frame]" Visible="true" Name="$ID/" ItemTransform="1 0 0 1 %.4f %.4f">'
            '<Properties><PathGeometry><GeometryPathType PathOpen="false"><PathPointArray>%s</PathPointArray></GeometryPathType></PathGeometry></Properties>'
            '<TextFramePreference TextColumnCount="1" TextColumnFixedWidth="60" VerticalJustification="CenterAlign"><Properties><InsetSpacing type="list">'
            '<ListItem type="unit">0</ListItem><ListItem type="unit">0</ListItem><ListItem type="unit">0</ListItem><ListItem type="unit">0</ListItem>'
            '</InsetSpacing></Properties></TextFramePreference></TextFrame>' % (fid, sid, layer, (x0 + x1) / 2, (y0 + y1) / 2, pts))

def cover_items(u):
    s_p, f_p, s_t, f_t = nid(), nid(), nid(), nid()
    add_story(clone_story("u188", s_p), s_p)
    add_story(clone_story("u19e", s_t, "<Content>%d %s</Content>" % (u + 1, esc(UNITS[u]))), s_t)
    return clone_frame(fr_purple, f_p, s_p) + clone_frame(fr_unit, f_t, s_t)

def page_items(num, left):
    kind = plan[num]
    if kind[0] == "pdf":
        return rect_xml(kind[1], kind[2], left) + ("" if YU else pn_frame(left))
    if kind[0] == "cover":
        return cover_items(kind[1])
    if kind[0] == "blank":
        return "" if YU else pn_frame(left)
    return ""

# ---- 1쪽 펼침면: PDF 지우고 제목·차례
f1 = sp1_name[0]
s1 = T(f1)
s1 = re.sub(r"\s*<Rectangle .*?</Rectangle>", "", s1, flags=re.S)
st_title, fid_title, st_toc, fid_toc = nid(), nid(), nid(), nid()
add_story(clone_story("u128", st_title), st_title)
lines = "<Br />".join("<Content>%d. %s\t%d</Content>" % (i + 1, esc(UNITS[i]), starts[i]) for i in range(NU))
add_story(clone_story("u13e", st_toc, lines), st_toc)
s1 = s1.replace("</Spread>", clone_frame(fr_title, fid_title, st_title) + clone_frame(fr_toc, fid_toc, st_toc) + "</Spread>", 1)
files[f1] = s1.encode("utf-8")

# ---- 나머지 펼침면 새로
for f in sp1_name[1:]:
    files.pop(f)
    order.remove(f)
new_spreads = []
for i, left_num in enumerate(range(2, TOTAL + 1, 2)):
    sid = nid()
    head = re.sub(r'<Spread Self="[^"]+"', '<Spread Self="%s"' % sid, head_tpl, count=1)
    head = re.sub(r'(<Spread [^>]*ItemTransform=")[^"]+"', lambda m: m.group(1) + "1 0 0 1 0 %s\"" % repr(SPREAD_DY * (i + 1)), head, count=1)
    body = page_xml(left_num, True) + page_xml(left_num + 1, False) + page_items(left_num, True) + page_items(left_num + 1, False)
    name = "Spreads/Spread_%s.xml" % sid
    files[name] = (head + body + "</Spread>\n</idPkg:Spread>").encode("utf-8")
    new_spreads.append(name)

# ---- 색·글꼴
g = T("Resources/Graphic.xml")
g = g.replace("<Color ", '<Color Self="Color/%s" Model="Process" Space="RGB" ColorValue="%s" ColorOverride="Normal" ConvertToHsb="false" '
              'AlternateSpace="NoAlternateColor" AlternateColorValue="" Name="$ID/" ColorEditable="true" ColorRemovable="true" Visible="false" '
              'SwatchCreatorID="7937" SwatchColorGroupReference="n" />\n\t<Color ' % (PURPLE, COVER_RGB), 1)
files["Resources/Graphic.xml"] = g.encode("utf-8")
fx, fc = T("Resources/Fonts.xml"), C("Resources/Fonts.xml")
add = ""
for n in ("a파도소리", "HY울릉도M", "아는체"):
    if 'Name="%s"' % n not in fx:
        add += re.search(r'<FontFamily Self="[^"]*" Name="%s">.*?</FontFamily>' % n, fc, re.S).group(0) + "\n\t"
i = fx.rindex("</FontFamily>") + len("</FontFamily>")
fx = fx[:i] + "\n\t" + add.rstrip() + fx[i:]
files["Resources/Fonts.xml"] = fx.encode("utf-8")

# ---- designmap
dm = re.sub(r'(<idPkg:Spread src="[^"]+" />\s*)+',
            lambda m: "".join('<idPkg:Spread src="%s" />\n\t' % x for x in [f1] + new_spreads), dm, count=1)
if YU or BOOK == "c1c":                                    # 문서 이름(틀은 'CLIMATH(m) 공통수학2.indd')
    dm = re.sub(r'(<Document [^>]*?) Name="[^"]*"', lambda m: m.group(1) + ' Name="%s"' % (os.path.splitext(os.path.basename(out))[0] + ".indd"), dm, count=1)
dm = re.sub(r'(<Section Self="[^"]+" )Length="\d+" AlternateLayoutLength="\d+"', r'\1Length="%d" AlternateLayoutLength="%d"' % (TOTAL, TOTAL), dm, count=1)
sl = re.search(r'StoryList="([^"]*)"', dm).group(1).split() + new_stories
dm = re.sub(r'StoryList="[^"]*"', 'StoryList="%s"' % " ".join(sl), dm, count=1)
b = dm.index('<idPkg:BackingStory src="XML/BackingStory.xml" />') + len('<idPkg:BackingStory src="XML/BackingStory.xml" />')
dm = dm[:b] + "".join('\n\t<idPkg:Story src="Stories/Story_%s.xml" />' % x for x in new_stories) + dm[b:]
files["designmap.xml"] = dm.encode("utf-8")

names = [n for n in order if n in files]
i = max(k for k, n in enumerate(names) if n.startswith("Spreads/")) + 1
names = names[:i] + new_spreads + names[i:]
names += [n for n in files if n not in names]
with zipfile.ZipFile(out, "w") as w:
    for n in names:
        info = zipfile.ZipInfo(n, date_time=(2026, 11, 18, 0, 0, 0))
        info.compress_type = zipfile.ZIP_STORED if n == "mimetype" else zipfile.ZIP_DEFLATED
        w.writestr(info, files[n])
print("펼침면", 1 + len(new_spreads), "새 스토리", len(new_stories), "->", out)
print("차례:", [(i + 1, UNITS[i], starts[i]) for i in range(NU)])
