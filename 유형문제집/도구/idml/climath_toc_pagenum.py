# -*- coding: utf-8 -*-
"""기본서 공통수학1 CLIMATH(m) 인디자인(IDML)에 차례와 쪽 번호 넣기 (2026-11-18 사용자 요청).
python climath_toc_pagenum.py <입력.idml> <출력.idml>
- 1쪽 '이 책의 차례' 아래에 차례 글상자: 단원명 + 시작 쪽(대단원 없음). 시작 쪽은 문서에서 단원 표지 글상자('1 다항식의 연산과 항등식' 등)가
  놓인 쪽 이름(Page Name)을 직접 읽는다. 단원명은 우리 기본서 단원명을 쓴다(표지 '10 경우의 순열'은 '경우의 수와 순열'로).
- 쪽 번호: 쪽마다 아래 가운데에 자동 쪽 번호 글상자(그 쪽의 PDF 위에). 마스터에 넣은 판은 PDF의 흰 바탕에 가려 보이지 않았음.
"""
import sys, re, zipfile, os

src, out = sys.argv[1:3]
z = zipfile.ZipFile(src)
files = {n: z.read(n) for n in z.namelist()}
dec = lambda n: files[n].decode("utf-8")
UNITS = {1: "다항식의 연산과 항등식", 2: "나머지정리", 3: "인수분해", 4: "복소수와 이차방정식", 5: "이차함수와 이차방정식의 관계",
         6: "이차함수의 최대, 최소", 7: "여러 가지 방정식", 8: "이차부등식", 9: "연립부등식", 10: "경우의 수와 순열", 11: "조합", 12: "행렬"}
FONT = "HY울릉도M"

# ---------------------------------------------------------------- 단원 시작 쪽 읽기
dm = dec("designmap.xml")
starts = {}
for f in re.findall(r'<idPkg:Spread src="([^"]+)"', dm):
    s = dec(f)
    pages = [(re.search(r'Name="([^"]*)"', p).group(1), float(re.search(r'ItemTransform="([^"]+)"', p).group(1).split()[4]))
             for p in re.findall(r"<Page [^>]*>", s)]
    for m in re.finditer(r'<TextFrame [^>]*ParentStory="([^"]+)"[^>]*ItemTransform="([^"]+)"[^>]*>(.*?)</TextFrame>', s, re.S):
        t = "".join(re.findall(r"<Content>([^<]*)</Content>", dec("Stories/Story_%s.xml" % m.group(1)))).strip()
        mm = re.match(r"(\d+)\s+\S", t)
        if not mm and t != "빠른 정답":
            continue
        xs = [float(a.split()[0]) + float(m.group(2).split()[4]) for a in re.findall(r'<PathPointType Anchor="([^"]+)"', m.group(3))]
        cx = sum(xs) / len(xs)
        pg = pages[0][0] if len(pages) == 1 else (pages[0][0] if cx < 0 else pages[1][0])
        starts[int(mm.group(1)) if mm else 99] = int(pg)
assert sorted(k for k in starts if k != 99) == list(range(1, 13)), starts
print("단원 시작 쪽:", starts)

# ---------------------------------------------------------------- 차례 글(스토리)
def csr(text, size, color="Color/Black", style="Regular"):
    return ('<CharacterStyleRange AppliedCharacterStyle="CharacterStyle/$ID/[No character style]" FillColor="%s" FontStyle="%s" PointSize="%s">'
            '<Properties><AppliedFont type="string">%s</AppliedFont></Properties><Content>%s</Content></CharacterStyleRange>' % (color, style, size, FONT, text))

W = 393.07
TAB = ('<Properties><TabList type="list"><ListItem type="record"><Alignment type="enumeration">RightAlign</Alignment>'
       '<AlignmentCharacter type="string">.</AlignmentCharacter><Leader type="string">·</Leader><Position type="unit">%.2f</Position></ListItem></TabList></Properties>' % W)
paras = []
rows = [("%d. %s" % (k, UNITS[k]), starts[k]) for k in range(1, 13)] + ([("빠른 정답", starts[99])] if 99 in starts else [])
for i, (name, pg) in enumerate(rows):
    br = "" if i == len(rows) - 1 else "<Br/>"
    paras.append('<ParagraphStyleRange AppliedParagraphStyle="ParagraphStyle/$ID/NormalParagraphStyle" Justification="LeftAlign" SpaceAfter="6" Leading="19">%s%s%s%s</ParagraphStyleRange>'
                 % (TAB, csr(name, 13), csr("\t" + str(pg), 13), br))


def story(self_, body):
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<idPkg:Story xmlns:idPkg="http://ns.adobe.com/AdobeInDesign/idml/1.0/packaging" DOMVersion="21.5">'
            '<Story Self="%s" AppliedTOCStyle="n" UserText="true" IsEndnoteStory="false" TrackChanges="false" StoryTitle="$ID/" AppliedNamedGrid="n">'
            '<StoryPreference OpticalMarginAlignment="false" OpticalMarginSize="12" FrameType="TextFrameType" StoryOrientation="Horizontal" StoryDirection="LeftToRightDirection" />'
            '%s</Story></idPkg:Story>' % (self_, body))


def frame(self_, story_id, layer, x0, y0, x1, y1, valign="TopAlign"):
    cx, cy, hw, hh = (x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) / 2, (y1 - y0) / 2
    pts = "".join('<PathPointType Anchor="%.4f %.4f" LeftDirection="%.4f %.4f" RightDirection="%.4f %.4f" />' % (x, y, x, y, x, y)
                  for x, y in ((-hw, -hh), (-hw, hh), (hw, hh), (hw, -hh)))
    return ('<TextFrame Self="%s" ParentStory="%s" PreviousTextFrame="n" NextTextFrame="n" ContentType="TextType" ItemLayer="%s" Locked="false" '
            'AppliedObjectStyle="ObjectStyle/$ID/[Normal Text Frame]" Visible="true" Name="$ID/" ItemTransform="1 0 0 1 %.4f %.4f">'
            '<Properties><PathGeometry><GeometryPathType PathOpen="false"><PathPointArray>%s</PathPointArray></GeometryPathType></PathGeometry></Properties>'
            '<TextFramePreference TextColumnCount="1" TextColumnFixedWidth="%.4f" VerticalJustification="%s"><Properties><InsetSpacing type="list">'
            '<ListItem type="unit">0</ListItem><ListItem type="unit">0</ListItem><ListItem type="unit">0</ListItem><ListItem type="unit">0</ListItem>'
            '</InsetSpacing></Properties></TextFramePreference></TextFrame>' % (self_, story_id, layer, cx, cy, pts, 2 * hw, valign))


files["Stories/Story_uqT1.xml"] = story("uqT1", "".join(paras)).encode("utf-8")
# 1쪽(Spread_uec): '이 책의 차례' 글상자(x 101~494, y −150~13) 아래
sp1 = [f for f in re.findall(r'<idPkg:Spread src="([^"]+)"', dm) if 'Name="1"' in dec(f)][0]
s = dec(sp1)
s = s.replace("</Spread>", frame("uqF1", "uqT1", "ue9", 297.64 - W / 2, 30, 297.64 + W / 2, 365) + "</Spread>", 1)
files[sp1] = s.encode("utf-8")

# ---------------------------------------------------------------- 쪽 번호
# 처음에는 마스터(맨 위 레이어)에 넣었으나, 쪽마다 놓인 PDF가 아래쪽을 흰색으로 덮어 보이지 않았다(사용자 확인 2026-11-18).
# 그래서 쪽마다 직접, 그 쪽의 PDF보다 뒤(위)에 자동 쪽 번호 글상자를 놓는다. 쪽을 옮겨도 번호는 자동으로 바뀐다.
pn = ('<ParagraphStyleRange AppliedParagraphStyle="ParagraphStyle/$ID/NormalParagraphStyle" Justification="CenterAlign">'
      '<CharacterStyleRange AppliedCharacterStyle="CharacterStyle/$ID/[No character style]" FillColor="Color/Black" FontStyle="Regular" PointSize="11">'
      '<Properties><AppliedFont type="string">%s</AppliedFont></Properties><Content><?ACE 18?></Content></CharacterStyleRange></ParagraphStyleRange>' % FONT)
new_stories = []
k = 0
for f in re.findall(r'<idPkg:Spread src="([^"]+)"', dm):
    s = files[f].decode("utf-8")
    add = []
    for p in re.findall(r"<Page [^>]*>", s):
        y0, x0, y1, x1 = map(float, re.search(r'GeometricBounds="([^"]+)"', p).group(1).split())
        tx, ty = map(float, re.search(r'ItemTransform="([^"]+)"', p).group(1).split()[4:6])
        cx, bottom = tx + (x0 + x1) / 2, ty + y1
        k += 1
        sid, fid = "u1fa%03x" % k, "u1fb%03x" % k
        files["Stories/Story_%s.xml" % sid] = story(sid, pn).encode("utf-8")
        new_stories.append(sid)
        add.append(frame(fid, sid, "ue9", cx - 30, bottom - 30, cx + 30, bottom - 12, "CenterAlign"))
    s = s.replace("</Spread>", "".join(add) + "</Spread>", 1)      # 쪽의 다른 개체(PDF)보다 뒤에 = 위에 보임
    files[f] = s.encode("utf-8")
print("쪽 번호 글상자", k)

# ---------------------------------------------------------------- designmap: 스토리 등록
dm = re.sub(r'(StoryList=")([^"]*)"', lambda m: '%s%s %s"' % (m.group(1), m.group(2), " ".join(["uqT1"] + new_stories)), dm, count=1)
last_story = list(re.finditer(r'<idPkg:Story src="[^"]+" />', dm))[-1]
dm = dm[:last_story.end()] + "".join('<idPkg:Story src="Stories/Story_%s.xml" />' % x for x in ["uqT1"] + new_stories) + dm[last_story.end():]
files["designmap.xml"] = dm.encode("utf-8")

with zipfile.ZipFile(out, "w") as w:
    names = z.namelist() + [n for n in files if n not in z.namelist()]
    for n in names:
        info = zipfile.ZipInfo(n, date_time=(2026, 11, 18, 0, 0, 0))
        info.compress_type = zipfile.ZIP_STORED if n == "mimetype" else zipfile.ZIP_DEFLATED
        w.writestr(info, files[n])
print("->", out)
