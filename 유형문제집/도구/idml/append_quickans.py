# -*- coding: utf-8 -*-
"""사용자가 고친 CLIMATH/유형서 IDML 끝에 '빠른 정답'을 붙임 (2026-11-18).
python append_quickans.py <사용자 IDML> <빠른정답 PDF> <링크 파일 이름> <출력.idml>
- 사용자 지시: '내가 올린 파일들 빠른 정답 부분이 없어, 만들어 줄 수 없어?' — 빠른 정답 내용은 빠른정답/*.hwpx(quickans.py)를 한글에서 PDF로 저장한 것.
- 마지막 쪽(홀수) 다음 짝수 쪽에 단원 표지와 같은 모양의 '빠른 정답' 표지(사용자 IDML의 마지막 단원 표지를 복사: 색·글상자 그대로, 글만 '빠른 정답'),
  그다음 홀수 쪽부터 빠른 정답 PDF 쪽(사용자 IDML의 PDF 그림 틀을 복사: 링크 폴더·크기 맞춤은 PDF 쪽 크기에 맞게 다시 계산).
- 쪽 번호: 사용자 IDML에 쪽 번호 글상자(자동 쪽 번호만 든 글상자)가 있으면(기본서) PDF 쪽마다 같은 자리에 복사, 없으면(유형서 — PDF에 인쇄됨) 넣지 않음.
- 1쪽 차례 끝에 '빠른 정답<탭>표지 쪽' 줄을 더함(공통수학1 기본서 사용자 차례와 같은 모양).
- 사용자 IDML의 다른 것(색·링크 이름·차례·글상자)은 건드리지 않음.
"""
import sys, os, re, zipfile, subprocess
from urllib.parse import quote, unquote

src, qpdf, linkname, out = sys.argv[1:5]
z = zipfile.ZipFile(src)
files = {n: z.read(n) for n in z.namelist()}
order = z.namelist()
T = lambda n: files[n].decode("utf-8")
dm = T("designmap.xml")
used = set(re.findall(r'Self="([^"]+)"', "".join(v.decode("utf-8", "ignore") for k, v in files.items() if k.endswith(".xml"))))
cnt = [0x5b000]


def nid():
    while True:
        cnt[0] += 1
        s = "u%x" % cnt[0]
        if s not in used:
            used.add(s)
            return s


o = subprocess.check_output(["pdfinfo", qpdf]).decode()
NQ = int(re.search(r"Pages:\s+(\d+)", o).group(1))
QW, QH = map(float, re.search(r"Page size:\s+([\d.]+) x ([\d.]+)", o).groups())
QSIZE = os.path.getsize(qpdf)

spreads = re.findall(r'<idPkg:Spread src="([^"]+)"', dm)
story = lambda sid: T("Stories/Story_%s.xml" % sid)
txt = lambda sid: "".join(re.findall(r"<Content>([^<]*)</Content>", story(sid)))


def is_pn(sid):
    st = story(sid)
    return "<?ACE 18?>" in st and not re.sub(r"\s", "", txt(sid).replace("<?ACE 18?>", ""))


def blocks(s, tag):
    """맨 위(펼침면 바로 아래) 개체만: 그룹 안 개체도 쓰려면 그룹째로"""
    return [m for m in re.finditer(r"<%s Self=.*?</%s>" % (tag, tag), s, re.S)]


# ---- 틀 찾기: 마지막 단원 표지(왼쪽 쪽), PDF 그림 틀(왼쪽·오른쪽), 쪽 번호 글상자(왼쪽·오른쪽)
cover = None; rect = {}; pn = {}; page_tpl = None; last_name = None; spread_tpl = None
for f in spreads:
    s = T(f)
    pages = re.findall(r"<Page .*?</Page>", s, re.S)
    last_name = int(re.search(r' Name="(\d+)"', pages[-1]).group(1))
    if len(pages) == 2:
        page_tpl, spread_tpl = pages, s
    body = re.sub(r"<Page .*?</Page>", "", s, flags=re.S)
    tfs = list(re.finditer(r'<TextFrame Self="[^"]+" ParentStory="([^"]+)"[^>]*ItemTransform="([^"]+)".*?</TextFrame>', body, re.S))
    titles = [m for m in tfs if re.match(r"\d+\s+\S", txt(m.group(1)).strip())]
    if titles:
        # 표지: 제목 글상자 + 채운 글상자(쪽 전체). 그룹이면 그룹째로
        grp = re.search(r"<Group Self=.*?</Group>", body, re.S)
        if grp and titles[0].group(0) in grp.group(0):
            cover = ("group", grp.group(0))
        else:
            fills = [m for m in tfs if 'FillColor="Color/' in m.group(0).split(">", 1)[0] and not txt(m.group(1)).strip()]
            cover = ("frames", (fills[0].group(0) if fills else "") + titles[0].group(0))
    for r in re.finditer(r"<Rectangle Self=.*?</Rectangle>", body, re.S):
        if "<PDF " in r.group(0):
            tx = float(re.search(r'ItemTransform="1 0 0 1 (\S+)', r.group(0)).group(1))
            rect["L" if tx < 0 else "R"] = r.group(0)
    for m in tfs:
        if is_pn(m.group(1)):
            tx = float(m.group(2).split()[4])
            pn["L" if tx < 0 else "R"] = (m.group(0), m.group(1))
assert cover and rect and page_tpl, (bool(cover), list(rect), bool(page_tpl))
assert last_name % 2 == 1, "마지막 쪽이 홀수가 아님: %d" % last_name
COVER_PAGE = last_name + 1
print("마지막 쪽", last_name, "빠른 정답 표지", COVER_PAGE, "PDF", NQ, "쪽", (QW, QH), "쪽 번호", "있음" if pn else "없음(유형서)")

new_stories = []


def clone_story(sid_old, content=None):
    sid = nid()
    x = story(sid_old).replace('<Story Self="%s"' % sid_old, '<Story Self="%s"' % sid, 1)
    if content is not None:
        x = re.sub(r"<Content>.*</Content>", lambda m: content, x, count=1, flags=re.S)
    files["Stories/Story_%s.xml" % sid] = x.encode("utf-8")
    new_stories.append(sid)
    return sid


def renew_ids(x, title_story=None):
    """개체 Self를 새로 매기고, 글상자 스토리는 복제(제목 스토리는 '빠른 정답')"""
    def tf(m):
        old = m.group(2)
        content = "<Content>빠른 정답</Content>" if old == title_story else None
        return '%sSelf="%s" ParentStory="%s"' % (m.group(1), nid(), clone_story(old, content))
    x = re.sub(r'(<TextFrame )Self="[^"]+" ParentStory="([^"]+)"', tf, x)
    x = re.sub(r'(<(?:Group|Rectangle|PDF|Link|Oval|Polygon|GraphicLine|Image) )Self="[^"]+"', lambda m: '%sSelf="%s"' % (m.group(1), nid()), x)
    return x


title_sid = None
for sid in re.findall(r'ParentStory="([^"]+)"', cover[1]):
    if re.match(r"\d+\s+\S", txt(sid).strip()):
        title_sid = sid


def page_xml(tpl, num):
    x = re.sub(r'<Page Self="[^"]+"', '<Page Self="%s"' % nid(), tpl, count=1)
    x = re.sub(r' Name="\d+"', ' Name="%d"' % num, x, count=1)
    return re.sub(r'(<ListItem type="long">)\d+(</ListItem>)', lambda m: m.group(1) + str(num) + m.group(2), x)


PAGE_TOP = -403.93700787401576


def rect_xml(side, k):
    x = renew_ids(rect[side])
    w0 = float(re.search(r'<GraphicBounds [^>]*Right="([\d.]+)"', x).group(1))
    hw = 297.6099853515625                                   # 기본서 PDF 너비(595.22pt)에 맞춤 — 지금 틀과 같음
    sc = 2 * hw / QW
    hh = QH * sc / 2
    x = re.sub(r'(<PathPointType Anchor=")(-?)[\d.]+ (-?)[\d.]+(" LeftDirection=")(-?)[\d.]+ (-?)[\d.]+(" RightDirection=")(-?)[\d.]+ (-?)[\d.]+"',
               lambda m: '%s%s%r %s%r%s%s%r %s%r%s%s%r %s%r"' % (m.group(1), m.group(2), hw, m.group(3), hh, m.group(4), m.group(5), hw, m.group(6), hh,
                                                              m.group(7), m.group(8), hw, m.group(9), hh), x)
    x = re.sub(r'(<Rectangle [^>]*ItemTransform="1 0 0 1 \S+ )\S+"', lambda m: m.group(1) + repr(PAGE_TOP + hh) + '"', x, count=1)
    x = re.sub(r'(<PDF [^>]*ItemTransform=")[^"]+"', lambda m: m.group(1) + "%r 0 0 %r %r %r\"" % (sc, sc, -hw, -hh), x, count=1)
    x = re.sub(r"<GraphicBounds [^>]*/>", '<GraphicBounds Left="0" Top="0" Right="%g" Bottom="%g" />' % (QW, QH), x, count=1)
    x = re.sub(r'PageNumber="\d+"', 'PageNumber="%d"' % k, x, count=1)
    x = re.sub(r'(LinkResourceURI="file:[^"]*/)[^"/]*"', lambda m: m.group(1) + quote(linkname) + '"', x, count=1)
    x = re.sub(r'LinkResourceSize="[^"]+"', 'LinkResourceSize="0~%x"' % QSIZE, x, count=1)
    x = re.sub(r'LinkImportStamp="file (\d+) \d+"', lambda m: 'LinkImportStamp="file %s %d"' % (m.group(1), QSIZE), x, count=1)
    x = re.sub(r"<MetadataPacketPreference>.*?</MetadataPacketPreference>\s*", "", x, flags=re.S)
    return x


def pn_xml(side):
    if not pn:
        return ""
    return renew_ids(pn[side][0])


# 새 쪽: COVER_PAGE(짝수, 표지) + PDF NQ쪽, 끝이 짝수 쪽에서 끝나면 그대로(마지막 펼침면 한 쪽)
plan = [("cover",)] + [("pdf", k + 1) for k in range(NQ)]
spread_y = [float(re.search(r'<Spread [^>]*ItemTransform="1 0 0 1 0 ([^"]+)"', T(f)).group(1)) for f in spreads]
dy = spread_y[-1] - spread_y[-2]
head = spread_tpl[:spread_tpl.index("<Page ")]
new_files = []
num = COVER_PAGE
i = 0
while i < len(plan):
    pair = plan[i:i + 2]
    sid = nid()
    h = re.sub(r'<Spread Self="[^"]+"', '<Spread Self="%s"' % sid, head, count=1)
    h = re.sub(r'(<Spread [^>]*ItemTransform=")[^"]+"', lambda m: m.group(1) + "1 0 0 1 0 %r\"" % (spread_y[-1] + dy * (len(new_files) + 1)), h, count=1)
    if len(pair) == 1:
        h = re.sub(r'PageCount="\d+"', 'PageCount="1"', h, count=1)
    pages = page_xml(page_tpl[0], num) + (page_xml(page_tpl[1], num + 1) if len(pair) == 2 else "")
    items = ""
    for side, it in zip("LR", pair):
        if it[0] == "cover":
            items += renew_ids(cover[1], title_sid)
        else:
            items += rect_xml(side, it[1]) + pn_xml(side)
    name = "Spreads/Spread_%s.xml" % sid
    files[name] = (h + pages + items + "</Spread>\n</idPkg:Spread>").encode("utf-8")
    new_files.append(name)
    num += len(pair)
    i += 2
TOTAL = num - 1

# ---- 차례에 '빠른 정답' 줄
for n in list(files):
    if n.startswith("Stories/"):
        st = T(n)
        cs = re.findall(r"<Content>([^<]*)</Content>", st)
        if len(cs) >= 10 and all("\t" in c for c in cs) and not any(c.startswith("빠른 정답") for c in cs):
            last = list(re.finditer(r"<Content>[^<]*</Content>", st))[-1]
            st = st[:last.end()] + "\n\t\t\t\t<Br />\n\t\t\t\t<Content>빠른 정답\t%d</Content>" % COVER_PAGE + st[last.end():]
            files[n] = st.encode("utf-8")
            print("차례 줄 더함:", n)

# ---- designmap
last = list(re.finditer(r'<idPkg:Spread src="[^"]+" />', dm))[-1]
dm = dm[:last.end()] + "".join('\n\t<idPkg:Spread src="%s" />' % f for f in new_files) + dm[last.end():]
dm = re.sub(r'(<Section Self="[^"]+" )Length="\d+" AlternateLayoutLength="\d+"', r'\1Length="%d" AlternateLayoutLength="%d"' % (TOTAL, TOTAL), dm, count=1)
sl = re.search(r'StoryList="([^"]*)"', dm).group(1).split() + new_stories
dm = re.sub(r'StoryList="[^"]*"', 'StoryList="%s"' % " ".join(sl), dm, count=1)
lastst = list(re.finditer(r'<idPkg:Story src="[^"]+" />', dm))[-1]
dm = dm[:lastst.end()] + "".join('\n\t<idPkg:Story src="Stories/Story_%s.xml" />' % x for x in new_stories) + dm[lastst.end():]
files["designmap.xml"] = dm.encode("utf-8")

names = [n for n in order if n in files]
k = max(j for j, n in enumerate(names) if n.startswith("Spreads/")) + 1
names = names[:k] + new_files + names[k:]
names += [n for n in files if n not in names]
with zipfile.ZipFile(out, "w") as w:
    for n in names:
        info = zipfile.ZipInfo(n, date_time=(2026, 11, 18, 0, 0, 0))
        info.compress_type = zipfile.ZIP_STORED if n == "mimetype" else zipfile.ZIP_DEFLATED
        w.writestr(info, files[n])
print("총 쪽", TOTAL, "새 펼침면", len(new_files), "새 스토리", len(new_stories), "->", out)
