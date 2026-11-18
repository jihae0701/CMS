# -*- coding: utf-8 -*-
"""기본서 공통수학1 CLIMATH(m) IDML 쪽 번호 다시 놓기 (2026-11-18 사용자 수정본 기준).
python climath_pagenum_v2.py <입력.idml> <출력.idml>
- 사용자 지시: 쪽 번호는 PDF가 2단이라 가운데 세로줄을 중심으로(쪽 가운데가 아님), 1쪽(차례)과 보라색 단원 표지 쪽에는 붙이지 않음.
  사용자가 1~5쪽을 고쳐 둠 → 가운데 세로줄은 오른쪽(홀수) 쪽에서 쪽 가운데보다 10pt 오른쪽, 왼쪽(짝수) 쪽에서 10pt 왼쪽(바깥쪽)
  (3쪽 +10.0, 4쪽 −10.0으로 놓여 있음; 5쪽은 +11.4로 손으로 옮긴 것으로 보고 +10으로 맞춤).
- 이미 있는 쪽 번호 글상자(자동 쪽 번호만 든 글상자)를 모두 지우고, 표지·1쪽을 뺀 쪽마다 다시 놓는다. 높이(아래 가장자리에서 12~30pt)는 그대로.
- 1쪽 차례·제목 등 사용자가 고친 다른 개체는 건드리지 않는다.
"""
import sys, re, zipfile

src, out = sys.argv[1:3]
OFF = 10.0
z = zipfile.ZipFile(src)
files = {n: z.read(n) for n in z.namelist()}
dec = lambda n: files[n].decode("utf-8")
FONT = "HY울릉도M"
dm = dec("designmap.xml")
layer = re.search(r'<Layer Self="([^"]+)"', dm).group(1)


def story_text(sid):
    return dec("Stories/Story_%s.xml" % sid)


def is_pn(sid):
    st = story_text(sid)
    return "<?ACE 18?>" in st and not re.sub(r"\s", "", "".join(re.findall(r"<Content>([^<]*)</Content>", st)).replace("<?ACE 18?>", ""))


def story(self_, body):
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<idPkg:Story xmlns:idPkg="http://ns.adobe.com/AdobeInDesign/idml/1.0/packaging" DOMVersion="21.5">'
            '<Story Self="%s" AppliedTOCStyle="n" UserText="true" IsEndnoteStory="false" TrackChanges="false" StoryTitle="$ID/" AppliedNamedGrid="n">'
            '<StoryPreference OpticalMarginAlignment="false" OpticalMarginSize="12" FrameType="TextFrameType" StoryOrientation="Horizontal" StoryDirection="LeftToRightDirection" />'
            '%s</Story></idPkg:Story>' % (self_, body))


def frame(self_, story_id, x0, y0, x1, y1):
    cx, cy, hw, hh = (x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) / 2, (y1 - y0) / 2
    pts = "".join('<PathPointType Anchor="%.4f %.4f" LeftDirection="%.4f %.4f" RightDirection="%.4f %.4f" />' % (x, y, x, y, x, y)
                  for x, y in ((-hw, -hh), (-hw, hh), (hw, hh), (hw, -hh)))
    return ('<TextFrame Self="%s" ParentStory="%s" PreviousTextFrame="n" NextTextFrame="n" ContentType="TextType" ItemLayer="%s" Locked="false" '
            'AppliedObjectStyle="ObjectStyle/$ID/[Normal Text Frame]" Visible="true" Name="$ID/" ItemTransform="1 0 0 1 %.4f %.4f">'
            '<Properties><PathGeometry><GeometryPathType PathOpen="false"><PathPointArray>%s</PathPointArray></GeometryPathType></PathGeometry></Properties>'
            '<TextFramePreference TextColumnCount="1" TextColumnFixedWidth="%.4f" VerticalJustification="CenterAlign"><Properties><InsetSpacing type="list">'
            '<ListItem type="unit">0</ListItem><ListItem type="unit">0</ListItem><ListItem type="unit">0</ListItem><ListItem type="unit">0</ListItem>'
            '</InsetSpacing></Properties></TextFramePreference></TextFrame>' % (self_, story_id, layer, cx, cy, pts, 2 * hw))


PN = ('<ParagraphStyleRange AppliedParagraphStyle="ParagraphStyle/$ID/NormalParagraphStyle" Justification="CenterAlign">'
      '<CharacterStyleRange AppliedCharacterStyle="CharacterStyle/$ID/[No character style]" FillColor="Color/Black" FontStyle="Regular" PointSize="11">'
      '<Properties><AppliedFont type="string">%s</AppliedFont></Properties><Content><?ACE 18?></Content></CharacterStyleRange></ParagraphStyleRange>' % FONT)

removed, new_stories, skipped, k = [], [], [], 0
for f in re.findall(r'<idPkg:Spread src="([^"]+)"', dm):
    s = dec(f)
    # 1) 기존 쪽 번호 글상자 지우기
    def drop(m):
        if is_pn(m.group(1)):
            removed.append(m.group(1))
            return ""
        return m.group(0)
    s = re.sub(r'<TextFrame Self="[^"]+" ParentStory="([^"]+)"[^>]*>.*?</TextFrame>', drop, s, flags=re.S)
    # 2) 쪽마다: 표지(단원명 글상자·쪽 전체 글상자)와 1쪽 빼기
    pages = []
    for p in re.findall(r"<Page [^>]*>", s):
        y0, x0, y1, x1 = map(float, re.search(r'GeometricBounds="([^"]+)"', p).group(1).split())
        tx, ty = map(float, re.search(r'ItemTransform="([^"]+)"', p).group(1).split()[4:6])
        pages.append((re.search(r'Name="([^"]*)"', p).group(1), tx + x0, tx + x1, ty + y1))
    cover = set()
    for m in re.finditer(r'<TextFrame [^>]*ParentStory="([^"]+)"[^>]*ItemTransform="([^"]+)"[^>]*>(.*?)</TextFrame>', s, re.S):
        tr = [float(v) for v in m.group(2).split()]
        xs = [float(a.split()[0]) * tr[0] + tr[4] for a in re.findall(r'<PathPointType Anchor="([^"]+)"', m.group(3))]
        cx = sum(xs) / len(xs)
        t = "".join(re.findall(r"<Content>([^<]*)</Content>", story_text(m.group(1)))).strip()
        if re.match(r"\d+\s+\S", t) or t == "빠른 정답" or (max(xs) - min(xs) > 500):
            for name, a, b, bottom in pages:
                if a <= cx <= b:
                    cover.add(name)
    add = []
    for name, a, b, bottom in pages:
        if name == "1" or name in cover:
            skipped.append(name)
            continue
        left = a < -1                                  # 왼쪽 쪽(짝수)
        cx = (a + b) / 2 + (-OFF if left else OFF)
        k += 1
        sid, fid = "u1fc%03x" % k, "u1fd%03x" % k
        files["Stories/Story_%s.xml" % sid] = story(sid, PN).encode("utf-8")
        new_stories.append(sid)
        add.append(frame(fid, sid, cx - 30, bottom - 30, cx + 30, bottom - 12))
    s = s.replace("</Spread>", "".join(add) + "</Spread>", 1)
    files[f] = s.encode("utf-8")

# designmap: 지운 스토리 빼고 새 스토리 넣기
for sid in removed:
    files.pop("Stories/Story_%s.xml" % sid, None)
    dm = dm.replace('<idPkg:Story src="Stories/Story_%s.xml" />' % sid, "")
sl = re.search(r'StoryList="([^"]*)"', dm).group(1).split()
sl = [x for x in sl if x not in set(removed)] + new_stories
dm = re.sub(r'StoryList="[^"]*"', 'StoryList="%s"' % " ".join(sl), dm, count=1)
last = list(re.finditer(r'<idPkg:Story src="[^"]+" />', dm))[-1]
dm = dm[:last.end()] + "".join('<idPkg:Story src="Stories/Story_%s.xml" />' % x for x in new_stories) + dm[last.end():]
files["designmap.xml"] = dm.encode("utf-8")
names = [n for n in z.namelist() if n in files] + [n for n in files if n not in z.namelist()]
with zipfile.ZipFile(out, "w") as w:
    for n in names:
        info = zipfile.ZipInfo(n, date_time=(2026, 11, 18, 0, 0, 0))
        info.compress_type = zipfile.ZIP_STORED if n == "mimetype" else zipfile.ZIP_DEFLATED
        w.writestr(info, files[n])
print("지운 쪽 번호", len(removed), "새 쪽 번호", k, "번호 없는 쪽", skipped)
