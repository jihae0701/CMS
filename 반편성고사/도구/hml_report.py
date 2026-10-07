# -*- coding: utf-8 -*-
"""학부모 보고서를 수정 가능한 한글 문서(HML)로 만든다.
막대그래프는 색칠한 표 칸, 성취 수준 배지는 글자 음영으로 표현한다(그림 없음).
서식 정의(HEAD)는 같은 폴더 구조의 시험지 HML에서 가져와 필요한 모양을 덧붙인다.
"""
import os, re, random
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.abspath(__file__))
BASE_HML = os.path.join(HERE, "..", "시험지", "예비고1_반편성고사_공통수학1.hml")
MM = 283.465  # 1mm (HWPUNIT)
CONTENT_W = 51000  # A4 210mm - 좌우 여백 14mm*2 ≈ 182mm(51590) 보다 조금 작게


def rgb(h):
    h = h.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return r + (g << 8) + (b << 16)


# ---------------- 스타일 정의 ----------------
class Styles:
    def __init__(self, head):
        self.head = head
        self.cs0 = int(re.search(r'<CHARSHAPELIST Count="(\d+)"', head).group(1))
        self.bf0 = int(re.search(r'<BORDERFILLLIST Count="(\d+)"', head).group(1)) + 1  # BorderFill Id는 1부터
        self.ps0 = int(re.search(r'<PARASHAPELIST Count="(\d+)"', head).group(1))
        self.cs, self.bf, self.ps = [], [], []
        self.font_id = None

    # 글자 모양
    def char(self, pt, color="#1d2433", bold=False, shade=None, mono=False, italic=False, underline=False, spacing=0):
        key = ("c", pt, color, bold, shade, mono, italic, underline, spacing)
        for i, k in enumerate(self.cs):
            if k[0] == key:
                return self.cs0 + i
        attrs = ('BorderFillId="1" Height="%d" Id="%d" ShadeColor="%d" SymMark="0" TextColor="%d" UseFontSpace="false" UseKerning="false"'
                 % (int(pt * 100), self.cs0 + len(self.cs), rgb(shade) if shade else 4294967295, rgb(color)))
        f = "FONTID_MONO" if mono else "FONTID_PLACEHOLDER"
        sp = ('<CHARSPACING Hangul="{0}" Hanja="{0}" Japanese="{0}" Latin="{0}" Other="{0}" Symbol="{0}" User="{0}"/>').format(int(spacing))
        extra = ("<ITALIC/>" if italic else "") + ("<BOLD/>" if bold else "") + \
                ('<UNDERLINE Color="%d" Shape="Solid" Type="Bottom"/>' % rgb(color) if underline else "")
        body = ('<CHARSHAPE %s>%s<RATIO Hangul="100" Hanja="100" Japanese="100" Latin="100" Other="100" Symbol="100" User="100"/>'
                '%s<RELSIZE Hangul="100" Hanja="100" Japanese="100" Latin="100" Other="100" Symbol="100" User="100"/>'
                '<CHAROFFSET Hangul="0" Hanja="0" Japanese="0" Latin="0" Other="0" Symbol="0" User="0"/>%s</CHARSHAPE>'
                % (attrs, f, sp, extra))
        self.cs.append((key, body))
        return self.cs0 + len(self.cs) - 1

    # 테두리/배경
    def border(self, fill=None, left=None, right=None, top=None, bottom=None):
        """각 변: None 또는 (굵기mm, 색)"""
        key = (fill, left, right, top, bottom)
        for i, k in enumerate(self.bf):
            if k[0] == key:
                return self.bf0 + i
        def side(tag, v):
            if not v:
                return '<%s Type="None" Width="0.12mm"/>' % tag
            return '<%s Type="Solid" Width="%smm" Color="%d"/>' % (tag, v[0], rgb(v[1]))
        body = ('<BORDERFILL BackSlash="0" BreakCellSeparateLine="0" CenterLine="0" CounterBackSlash="0" CounterSlash="0" CrookedSlash="0" Id="%d" Shadow="false" Slash="0" ThreeD="false">%s%s%s%s%s</BORDERFILL>'
                % (self.bf0 + len(self.bf), side("LEFTBORDER", left), side("RIGHTBORDER", right), side("TOPBORDER", top), side("BOTTOMBORDER", bottom),
                   '<FILLBRUSH><WINDOWBRUSH Alpha="0" FaceColor="%d" HatchColor="0"/></FILLBRUSH>' % rgb(fill) if fill else ""))
        self.bf.append((key, body))
        return self.bf0 + len(self.bf) - 1

    def box(self, color="#d5dced", w="0.12", fill=None):
        v = (w, color)
        return self.border(fill, v, v, v, v)

    # 문단 모양
    def para(self, align="Left", spacing=150, prev=0, nxt=0, left=0, indent=0):
        key = (align, spacing, prev, nxt, left, indent)
        for i, k in enumerate(self.ps):
            if k[0] == key:
                return self.ps0 + i
        body = ('<PARASHAPE Align="%s" AutoSpaceEAsianEng="false" AutoSpaceEAsianNum="false" BreakLatinWord="KeepWord" BreakNonLatinWord="false" Condense="0" FontLineHeight="false" HeadingType="None" Id="%d" KeepLines="false" KeepWithNext="false" Level="0" LineWrap="Break" PageBreakBefore="false" SnapToGrid="false" TabDef="0" VerAlign="Baseline" WidowOrphan="false">'
                '<PARAMARGIN Indent="%d" Left="%d" LineSpacing="%d" LineSpacingType="Percent" Next="%d" Prev="%d" Right="0"/><PARABORDER BorderFill="1" Connect="false" IgnoreMargin="false"/></PARASHAPE>'
                % (align, self.ps0 + len(self.ps), indent, left, spacing, nxt, prev))
        self.ps.append((key, body))
        return self.ps0 + len(self.ps) - 1

    def build_head(self, title, bins=()):
        h = self.head
        # 글꼴: 맑은 고딕을 각 언어 글꼴 목록에 추가
        def addfont(m):
            n = int(m.group(2))
            self.font_id = n
            font = ('<FONT Id="%d" Name="맑은 고딕" Type="ttf"><TYPEINFO ArmStyle="1" Contrast="0" FamilyType="2" Letterform="1" Midline="1" Proportion="0" StrokeVariation="1" Weight="6" XHeight="1"/></FONT>' % n +
                    '<FONT Id="%d" Name="Consolas" Type="ttf"><TYPEINFO ArmStyle="1" Contrast="0" FamilyType="2" Letterform="1" Midline="1" Proportion="9" StrokeVariation="1" Weight="6" XHeight="1"/></FONT>' % (n + 1))
            return m.group(1).replace('Count="%d"' % n, 'Count="%d"' % (n + 2)) + m.group(3) + font + m.group(4)
        h = re.sub(r'(<FONTFACE Count="(\d+)" Lang="\w+">)(.*?)(</FONTFACE>)', addfont, h, flags=re.S)
        fid = ('<FONTID Hangul="{0}" Hanja="{0}" Japanese="{0}" Latin="{0}" Other="{0}" Symbol="{0}" User="{0}"/>').format(self.font_id)
        fmono = ('<FONTID Hangul="{0}" Hanja="{0}" Japanese="{0}" Latin="{1}" Other="{0}" Symbol="{0}" User="{0}"/>').format(self.font_id, self.font_id + 1)
        cs = "".join(b.replace("FONTID_PLACEHOLDER", fid).replace("FONTID_MONO", fmono) for _, b in self.cs)
        h = re.sub(r'<CHARSHAPELIST Count="\d+">', '<CHARSHAPELIST Count="%d">' % (self.cs0 + len(self.cs)), h)
        h = h.replace("</CHARSHAPELIST>", cs + "</CHARSHAPELIST>")
        h = re.sub(r'<BORDERFILLLIST Count="\d+">', '<BORDERFILLLIST Count="%d">' % (self.bf0 - 1 + len(self.bf)), h)
        h = h.replace("</BORDERFILLLIST>", "".join(b for _, b in self.bf) + "</BORDERFILLLIST>")
        h = re.sub(r'<PARASHAPELIST Count="\d+">', '<PARASHAPELIST Count="%d">' % (self.ps0 + len(self.ps)), h)
        h = h.replace("</PARASHAPELIST>", "".join(b for _, b in self.ps) + "</PARASHAPELIST>")
        items = "".join('<BINITEM BinData="%d" Format="png" Type="Embedding"/>' % (i + 1) for i in range(len(bins)))
        h = re.sub(r"<BINDATALIST.*?</BINDATALIST>", ('<BINDATALIST Count="%d">%s</BINDATALIST>' % (len(bins), items)) if bins else "", h, flags=re.S)
        h = re.sub(r"<DOCSUMMARY>.*?</DOCSUMMARY>", "<DOCSUMMARY><TITLE>%s</TITLE></DOCSUMMARY>" % escape(title), h, flags=re.S)
        return h


# ---------------- 문서 조각 ----------------
_z = [900000]


def zo():
    _z[0] += 1
    return _z[0]


class Doc:
    def __init__(self, st):
        self.st = st
        S = st
        self.P_L = S.para("Left", 150)
        self.P_C = S.para("Center", 130)
        self.P_R = S.para("Right", 150)
        self.P_TIGHT = S.para("Left", 120)
        self.P_TINY = S.para("Left", 100)
        self.P_SEC = S.para("Left", 150, prev=1100, nxt=250)
        self.P_GAP = S.para("Left", 100)
        self.P_BUL = S.para("Left", 155, left=1100, indent=-1100)
        self.C_TINY = S.char(1)

    # 글자 조각: [(텍스트, charshape)]
    def p(self, runs, ps=None, extra=""):
        ps = self.P_L if ps is None else ps
        body = "".join(('<TEXT CharShape="%d">%s<CHAR></CHAR></TEXT>' % (cs, t[1])) if isinstance(t, tuple) else
                       ('<TEXT CharShape="%d"><CHAR>%s</CHAR></TEXT>' % (cs, escape(t))) for t, cs in runs if t)
        if not body:
            body = '<TEXT CharShape="%d"/>' % runs[0][1] if runs else '<TEXT CharShape="%d"/>' % self.C_TINY
        return '<P ParaShape="%d" Style="0"%s>%s</P>' % (ps, extra, body)

    def table(self, rows, widths, bf_table=1, heights=None, margin=(141, 141, 283, 283), ps=None, extra=""):
        """rows: [[(내용P들 문자열, borderfill, valign, colspan), ...], ...]"""
        W = sum(widths)
        nrow = len(rows)
        out = []
        for ri, row in enumerate(rows):
            ci = 0
            cells = []
            for cell in row:
                content, bf, va = cell[0], cell[1], cell[2] if len(cell) > 2 else "Center"
                if not content:
                    content = '<P ParaShape="%d" Style="0"><TEXT CharShape="%d"/></P>' % (self.P_TINY, self.C_TINY)
                span = cell[3] if len(cell) > 3 else 1
                w = sum(widths[ci:ci + span])
                h = heights[ri] if heights else 282
                cells.append('<CELL BorderFill="%d" ColAddr="%d" ColSpan="%d" Dirty="false" Editable="false" HasMargin="true" Header="false" Height="%d" Protect="false" RowAddr="%d" RowSpan="1" Width="%d">'
                             '<CELLMARGIN Bottom="%d" Left="%d" Right="%d" Top="%d"/>'
                             '<PARALIST LineWrap="Break" LinkListID="0" LinkListIDNext="0" TextDirection="0" VertAlign="%s">%s</PARALIST></CELL>'
                             % (bf, ci, span, h, ri, w, margin[1], margin[2], margin[3], margin[0], va, content))
                ci += span
            out.append("<ROW>%s</ROW>" % "".join(cells))
        Ht = sum(heights) if heights else 282 * nrow
        tbl = ('<TABLE BorderFill="%d" CellSpacing="0" ColCount="%d" PageBreak="Cell" RepeatHeader="false" RowCount="%d">'
               '<SHAPEOBJECT InstId="%d" Lock="false" NumberingType="Table" TextWrap="TopAndBottom" ZOrder="%d">'
               '<SIZE Height="%d" HeightRelTo="Absolute" Protect="false" Width="%d" WidthRelTo="Absolute"/>'
               '<POSITION AffectLSpacing="false" AllowOverlap="false" FlowWithText="true" HoldAnchorAndSO="false" HorzAlign="Left" HorzOffset="0" HorzRelTo="Para" TreatAsChar="true" VertAlign="Top" VertOffset="0" VertRelTo="Para"/>'
               '<OUTSIDEMARGIN Bottom="0" Left="0" Right="0" Top="0"/></SHAPEOBJECT>'
               '<INSIDEMARGIN Bottom="0" Left="0" Right="0" Top="0"/>%s</TABLE>'
               % (bf_table, len(widths), nrow, random.randint(10 ** 7, 10 ** 8), zo(), Ht, W, "".join(out)))
        return '<P ParaShape="%d" Style="0"%s><TEXT CharShape="%d">%s<CHAR></CHAR></TEXT></P>' % (self.P_TINY if ps is None else ps, extra, self.C_TINY, tbl)

    def picture(self, tpl, binid, px_w, px_h, width):
        """시험지 HML의 그림 개체를 틀로 삼아 글자처럼 취급되는 그림 생성"""
        oriW, oriH = px_w * 75, px_h * 75
        curW, curH = int(width), int(width * px_h / px_w)
        x = tpl
        x = re.sub(r'<SHAPECOMMENT>.*?</SHAPECOMMENT>', '<SHAPECOMMENT>CLIMATH 로고</SHAPECOMMENT>', x, flags=re.S)
        x = re.sub(r'InstId="\d+"', 'InstId="%d"' % random.randint(10 ** 7, 10 ** 8), x, count=1)
        x = re.sub(r'InstID="\d+"', 'InstID="%d"' % random.randint(10 ** 7, 10 ** 8), x, count=1)
        x = re.sub(r'ZOrder="\d+"', 'ZOrder="%d"' % zo(), x, count=1)
        x = re.sub(r'<SIZE Height="\d+"', '<SIZE Height="%d"' % curH, x, count=1)
        x = re.sub(r'Width="\d+" WidthRelTo', 'Width="%d" WidthRelTo' % curW, x, count=1)
        x = re.sub(r'CurHeight="\d+" CurWidth="\d+"', 'CurHeight="%d" CurWidth="%d"' % (curH, curW), x)
        x = re.sub(r'OriHeight="\d+" OriWidth="\d+"', 'OriHeight="%d" OriWidth="%d"' % (oriH, oriW), x)
        x = re.sub(r'CenterX="\d+" CenterY="\d+"', 'CenterX="%d" CenterY="%d"' % (curW // 2, curH // 2), x)
        x = re.sub(r'(<RENDERINGINFO>.*?)<SCAMATRIX E1="[\d.]+"( E2="[\d.]+" E3="[\d.]+" E4="[\d.]+") E5="[\d.]+"',
                   lambda m: '%s<SCAMATRIX E1="%.5f"%s E5="%.5f"' % (m.group(1), curW / oriW, m.group(2), curH / oriH), x, count=1, flags=re.S)
        x = re.sub(r'<IMAGERECT [^>]*/>', '<IMAGERECT X0="0" X1="%d" X2="%d" X3="0" Y0="0" Y1="0" Y2="%d" Y3="%d"/>' % (oriW, oriW, oriH, oriH), x)
        x = re.sub(r'<IMAGECLIP [^>]*/>', '<IMAGECLIP Bottom="%d" Left="0" Right="%d" Top="0"/>' % (oriH, oriW), x)
        x = re.sub(r'<IMAGEDIM [^>]*/>', '<IMAGEDIM Height="%d" Width="%d"/>' % (oriH, oriW), x)
        x = re.sub(r'BinItem="\d+"', 'BinItem="%d"' % binid, x)
        return x

    def bar(self, rate, avg, width, show_avg, FILL="#1a1a1a", TRACK="#DEDBCF", DARK="#B3202E", height=420):
        """색칠한 표 칸 막대(평균 위치는 굵은 왼쪽 선)"""
        S = self.st
        if rate is None:
            segs = [(1.0, TRACK, False)]
        else:
            r = max(0.0, min(1.0, rate))
            if not show_avg or avg is None:
                segs = [(r, FILL, False), (1 - r, TRACK, False)]
            else:
                a = max(0.0, min(1.0, avg))
                if a <= r:
                    segs = [(a, FILL, False), (r - a, FILL, True), (1 - r, TRACK, False)]
                else:
                    segs = [(r, FILL, False), (a - r, TRACK, False), (1 - a, TRACK, True)]
        # 너무 좁은 칸 정리
        ws, cells = [], []
        for frac, col, tick in segs:
            w = int(round(frac * width))
            if w < 120:
                if tick and cells:  # 평균선이 끝에 붙은 경우: 마지막 칸 오른쪽 선으로
                    pass
                continue
            bf = S.border(col, left=("1.0", DARK) if tick else None)
            ws.append(w)
            cells.append(("", bf))
        if not ws:
            ws, cells = [width], [("", S.border(TRACK))]
        ws[-1] += width - sum(ws)
        empty = '<P ParaShape="%d" Style="0"><TEXT CharShape="%d"/></P>' % (self.P_TINY, self.C_TINY)
        row = [(empty, bf, "Center") for _, bf in cells]
        return self.table([row], ws, heights=[height], margin=(0, 0, 0, 0))


# ---------------- 보고서 (CMS CLIMATH 스타일, 학생당 2쪽) ----------------
PB = {"매우 우수": "#B3202E", "우수": "#2B2B2B", "양호": "#C49A3A", "보완 필요": "#8A8F7A", None: "#B9B6A8"}
RED, INK, GREY, CREAM = "#B3202E", "#1a1a1a", "#555555", "#FBF8F1"


def build(students, cfg, exams, stats, SUBJ, level, opinion, out_path, recommended=lambda s, c: None,
          recommended2=lambda s, c: None, strengths_weaknesses=None, basis=None):
    base = open(BASE_HML, encoding="utf-8").read()
    head = base[:base.index("<BODY>")]
    S = Styles(head)
    D = Doc(S)
    ch = S.char
    C = dict(
        logo=ch(14, "#1B2A4A", True), logosep=ch(10, "#9a9a9a"), logo2=ch(7, "#1B2A4A", True, italic=True, underline=True),
        kicker=ch(7.5, GREY, mono=True, spacing=30), title=ch(24, RED, True), subt=ch(11, "#222222"),
        code=ch(12, "#8b8b8b", True, mono=True, spacing=45), nm=ch(9.5, "#111111", True), nmr=ch(9.5, "#333333"),
        sh=ch(12, "#111111", True), shr=ch(7, GREY, mono=True, spacing=20),
        body=ch(9.5, "#222222"), bodyb=ch(9.5, "#111111", True), tag=ch(7.5, "#3c3c33", mono=True, shade="#E2E0D2", spacing=5),
        cnm=ch(10.5, "#111111", True), big=ch(22, "#111111", True), bigs=ch(9, "#9b9b9b"), miss=ch(16, "#B9B6A8", True),
        cap=ch(8, "#666666"), us=ch(7.6, "#888888"), uu=ch(8.6, "#222222"), up=ch(8.6, "#111111", True), uph=ch(8.6, RED, True),
        leg=ch(7.4, "#777777"), legk=ch(7.4, INK, True), legr=ch(7.4, RED, True),
        gno=ch(7.4, "#777777"), glab=ch(8.4, "#222222", True), o=ch(9.6, INK, True), x=ch(9.6, RED, True), n=ch(9.6, "#B9B6A8"),
        mini=ch(9, "#333333"), minib=ch(9, "#111111", True),
        gh=ch(9.8, "#3f5f49", True), wh=ch(9.8, RED, True), gm=ch(9, "#5E7F68", True), wm=ch(9, RED, True),
        bx=ch(8.8, "#222222"), bxb=ch(8.8, "#111111", True),
        bh=ch(12, "#111111", True), bd=ch(8.6, GREY), rno=ch(10, "#ffffff", True), rcls=ch(12.5, "#111111", True),
        rtag=ch(7.6, "#2F6FD0", True), rtx=ch(8.8, "#444444"), why=ch(7.8, "#2F6FD0"), whyb=ch(7.8, "#2F6FD0", True),
        nx=ch(8.8, "#333333"), nxb=ch(8.8, "#111111", True), pf=ch(7, "#9a9a9a", mono=True, spacing=5),
    )
    BADGE = {k: ch(7.6, "#ffffff", True, shade=v) for k, v in PB.items()}
    BF = dict(
        none=1, rule=S.border(bottom=("0.7", INK)), sh=S.border(bottom=("0.12", "#c9c6b8")),
        olive=S.box("#cfcdbd", fill="#EFEEE3"), card=S.box("#d8d5c8", fill="#ffffff"),
        grid=S.box("#d8d5c8", fill="#ffffff"), grids=S.box("#d8d5c8", fill="#F1F0E6"),
        good=S.border("#F3F4F0", ("1.0", "#5E7F68"), ("0.12", "#d6d8cf"), ("0.12", "#d6d8cf"), ("0.12", "#d6d8cf")),
        warn=S.border("#FCF0F1", ("1.0", RED), ("0.12", "#ecd2d5"), ("0.12", "#ecd2d5"), ("0.12", "#ecd2d5")),
        note=S.box("#d8d5c8", fill="#ffffff"), blue=S.border("#F3F7FC", ("1.0", "#2F6FD0")),
        rno=S.box("#2F6FD0", fill="#2F6FD0"), rc1=S.box("#2F6FD0", "0.4", fill="#ffffff"), rc2=S.box("#d6dbe6", fill="#ffffff"),
        cream=S.border(CREAM),
    )
    P_SH = S.para("Left", 140)
    P_C = S.para("Center", 140)
    P_C2 = S.para("Center", 140, prev=500)
    P_R = S.para("Right", 140)
    P_B = S.para("Left", 165)
    P_IT = S.para("Left", 150, prev=250, left=900, indent=-900)
    gap = lambda h=1: "".join(D.p([("", D.C_TINY)], D.P_GAP) for _ in range(h))

    def badge(lv):
        return (" %s " % (lv or "미응시"), BADGE.get(lv, BADGE[None]))

    def sec(kr, en, first=False):
        return (D.p([("", C["body"])], S.para("Left", 100, prev=0 if first else 700)) +
                D.table([[(D.p([(kr, C["sh"])], P_SH), BF["sh"], "Bottom"), (D.p([(en, C["shr"])], P_R), BF["sh"], "Bottom")]],
                        [30000, 21000], margin=(0, 250, 0, 0)) + gap())

    LOGO = os.path.join(HERE, "assets", "climath_logo_cream.png")
    bins = []
    pic_tpl = re.search(r"<PICTURE .*?</PICTURE>", base, re.S)
    if os.path.exists(LOGO) and pic_tpl:
        from PIL import Image
        bins.append(LOGO)
        lw, lh = Image.open(LOGO).size

    def logo(width=3700):
        if bins:
            return [("CMS", C["logo"]), ("  │  ", C["logosep"]), (("pic", D.picture(pic_tpl.group(0), 1, lw, lh, width)), C["logo"])]
        return [("CMS", C["logo"]), ("  │ ", C["logosep"]), ("CLIMATH", C["logo2"])]

    def footer(n):
        return (gap(2) + D.table([[(D.p([("CMS CLIMATH", C["pf"])]), BF["none"], "Center"),
                                   (D.p([("%d / 2" % n, C["pf"])], P_R), BF["none"], "Center")]], [36000, 15000], margin=(0, 0, 0, 0)))

    show = cfg["show_avg"]
    subjects = " · ".join(n for _, n in SUBJ)
    title = cfg["title"] or "예비고1 진단평가 결과 보고서"
    pages = []
    for idx, s in enumerate(students):
        x = []
        brk = ' ColumnBreak="false" PageBreak="true"'
        text, tips = opinion(s, cfg, stats)
        strong, weak = strengths_weaknesses(s, cfg) if strengths_weaknesses else ([], [])
        first_sent = text.split(". ")[0].rstrip(".") + "."
        # ---- 1쪽 ----
        x.append(D.p(logo(), P_C, extra=brk if idx else ""))
        x.append(D.p([(title, C["title"])], P_C2))
        x.append(D.p([("%s 학습 진단 리포트" % subjects, C["subt"])], P_C))
        x.append(D.p([("PRE-HIGH 1", C["code"])], P_C2))
        x.append(D.p([(s["name"] + "  ", C["nm"]), ("중3 · %s" % s["school"] if s["school"] else "중3", C["nmr"])], P_C))
        x.append(D.table([[("", BF["rule"])]], [51000], heights=[300], margin=(0, 0, 0, 0)))
        x.append(sec("진단 요약", "SUMMARY"))
        tg = []
        for _, u, _ in strong:
            tg += [(" ✓ 강점 %s " % u, C["tag"]), ("  ", C["body"])]
        for _, u, _ in weak:
            tg += [(" ✓ 보완 %s " % u, C["tag"]), ("  ", C["body"])]
        x.append(D.table([[(D.p([(first_sent, C["body"])], P_B) + (D.p(tg, P_B) if tg else ""), BF["olive"], "Center")]],
                         [51000], margin=(400, 400, 700, 700)))
        x.append(sec("과목별 결과", "SUBJECT SCORE"))
        cards = []
        for key, nm in SUBJ:
            full = stats[("full", key)]
            if not s["took"][key]:
                c = D.p([(nm + "    ", C["cnm"]), badge(None)]) + D.p([("미응시", C["miss"])])
            else:
                sc = s["score"][key]; avg = stats[("avg", key)]
                lv = level(sc / full if full else 0, cfg)
                cap = "20문항 중 %d문항 정답" % sum(s["ok"][key]) + (" · 전체 평균 %.1f점" % avg if show and avg is not None else "")
                c = (D.p([(nm + "    ", C["cnm"]), badge(lv)]) + D.p([("%g" % sc, C["big"]), (" / %d" % full, C["bigs"])]) +
                     D.bar(sc / full if full else 0, (avg / full) if (avg is not None and full) else None, 22400, show) +
                     D.p([(cap, C["cap"])]))
            cards.append((c, BF["card"], "Top"))
        x.append(D.table([[cards[0], ("", BF["none"]), cards[1]]], [25000, 1000, 25000], margin=(400, 400, 700, 700)))
        x.append(sec("단원별 성취도", "UNIT PROFILE"))
        rows = []
        for key, nm in SUBJ:
            for u in cfg["units"][key]:
                r = s["unit"][(key, u)]
                lv = level(r, cfg)
                pct = "-" if r is None else "%d%%" % round(r * 100)
                rows.append([(D.p([(nm + "  ", C["us"]), (u, C["uu"])]), BF["none"], "Bottom"),
                             (D.p([(pct + "  ", C["uph"] if lv == "매우 우수" else C["up"]), badge(lv)], P_R), BF["none"], "Bottom")])
                rows.append([(D.bar(r, stats[("uavg", key, u)], 50400, show), BF["none"], "Top", 2)])
        x.append(D.table(rows, [33000, 18000], margin=(120, 230, 0, 0)))
        leg = [("■ ", C["legk"]), ("학생 득점률     ", C["leg"])]
        if show:
            leg += [("┃ ", C["legr"]), ("전체 평균     ", C["leg"])]
        leg += [("매우 우수 %g%%↑ · 우수 %g%%↑ · 양호 %g%%↑" % tuple(cfg["lv"]), C["leg"])]
        x.append(D.p(leg))
        x.append(footer(1))
        # ---- 2쪽 ----
        x.append(D.table([[(D.p(logo(3200)), BF["rule"], "Bottom"),
                           (D.p([(title + "  ", C["mini"]), (s["name"], C["minib"])], P_R), BF["rule"], "Bottom")]],
                         [24000, 27000], margin=(0, 250, 0, 0), extra=brk))
        x.append(sec("문항별 결과", "ITEM CHECK"))
        grows = []
        for key, nm in SUBJ:
            row = [(D.p([(nm, C["glab"])]), BF["none"], "Center")]
            for q, ok in zip(exams[key], s["ok"][key]):
                mark = ("-", C["n"]) if not s["took"][key] else (("○", C["o"]) if ok else ("×", C["x"]))
                row.append((D.p([(str(q["no"]), C["gno"])], D.P_C) + D.p([mark], D.P_C), BF["grids"] if q["no"] > 14 else BF["grid"]))
            grows.append(row)
        x.append(D.table(grows, [5400] + [2280] * 20, margin=(60, 60, 0, 0)))
        x.append(D.p([("○ 정답 · × 오답      1~14번 객관식 · 15~20번 단답형(음영)", C["leg"])]))
        x.append(sec("강점과 보완점", "TOP 2 EACH"))
        gi = "".join(D.p([("✓  ", C["gm"]), (u, C["bxb"]), (" %d%% · %s" % (round(r * 100), level(r, cfg)), C["bx"])], P_IT) for _, u, r in strong) \
            or D.p([("✓  ", C["gm"]), ("기본 개념을 차근차근 쌓아 가는 중입니다. 꾸준한 복습으로 강점 단원을 만들어 갈 수 있습니다.", C["bx"])], P_IT)
        wi = "".join(D.p([("!  ", C["wm"]), (u, C["bxb"]), (" — " + cfg["advice"].get(u, ""), C["bx"])], P_IT) for _, u, _ in weak) \
            or D.p([("!  ", C["wm"]), ("전 단원이 고르게 우수합니다. 고난도 문항으로 실력의 폭을 넓혀 보세요.", C["bx"])], P_IT)
        x.append(D.table([[(D.p([("✓ 강점 단원", C["gh"])]) + gi, BF["good"], "Top"), ("", BF["none"]),
                           (D.p([("! 보완할 단원", C["wh"])]) + wi, BF["warn"], "Top")]],
                         [25000, 1000, 25000], margin=(350, 350, 700, 600)))
        x.append(sec("종합 의견", "OVERALL COMMENT"))
        x.append(D.table([[(D.p([(text, C["body"])], P_B), BF["note"], "Center")]], [51000], margin=(400, 400, 700, 700)))
        x.append(sec("수강 추천 반", "RECOMMENDED CLASSES"))
        r1, r2 = recommended(s, cfg), recommended2(s, cfg)
        b1, b2 = basis(s, cfg) if basis else ("", "")

        def rcard(n, kind, std, c, desc, why, first):
            if c:
                body = (D.p([(c + "      ", C["rcls"]), ("%s · %s" % (kind, std), C["rtag"])]) +
                        D.p([(desc, C["rtx"])], P_B) + D.p([("추천 근거  ", C["whyb"]), (why, C["why"])]))
            else:
                body = (D.p([("", C["rcls"]), ("%s · %s" % (kind, std), C["rtag"])], P_R) + D.p([("", C["rtx"])]) + D.p([("", C["rtx"])]))
            return D.table([[(D.p([(str(n), C["rno"])], P_C), BF["rno"], "Center"),
                             (body, BF["rc1"] if first else BF["rc2"], "Center")]],
                           [2600, 44800], heights=[2600], margin=(300, 300, 600, 600))
        inner = (D.p([("진단평가 결과에 따른 ", C["bd"]), ("공통수학반 1개", C["bxb"]), ("와 현재 학습 진도에 맞춘 ", C["bd"]),
                      ("선행 과목반 1개", C["bxb"]), (", 총 2개 반을 함께 수강합니다.", C["bd"])]) +
                 gap() + rcard(1, "공통수학반", "진단평가 결과 기준", r1, cfg["class_desc"].get(r1 or "", ""), b1, True) + gap() +
                 rcard(2, "선행 과목반", "학습 진도 기준", r2, cfg.get("pre_desc", {}).get(r2 or "", ""), b2, False))
        x.append(D.table([[(inner, BF["blue"], "Top")]], [51000], margin=(500, 500, 900, 700)))
        x.append(gap(2))
        x.append(D.table([[(D.p([("상담 안내", C["nxb"])]) + D.p([(cfg["notice"], C["nx"])], P_B), BF["olive"], "Center"),
                           (D.p([(cfg["academy"], C["nxb"])], P_R) + D.p([(str(cfg["contact"]), C["nx"])], P_R), BF["olive"], "Center")]],
                         [37000, 14000], margin=(350, 350, 700, 700)))
        x.append(footer(2))
        pages.append("".join(x))

    # 구역 정의(A4, 1단, 바탕쪽 없음, 크림색 종이)
    secdef = re.search(r"<SECDEF.*?</SECDEF>", base, re.S).group(0)
    secdef = re.sub(r"<MASTERPAGE.*?</MASTERPAGE>", "", secdef, flags=re.S)
    secdef = re.sub(r'<PAGEDEF [^>]*>.*?</PAGEDEF>',
                    '<PAGEDEF GutterType="LeftOnly" Height="84188" Landscape="0" Width="59528">'
                    '<PAGEMARGIN Bottom="2551" Footer="0" Gutter="0" Header="0" Left="3969" Right="3969" Top="3402"/></PAGEDEF>', secdef, flags=re.S)
    secdef = secdef.replace('MasterPage="true"', 'MasterPage="false"')
    secdef = re.sub(r'<PAGEBORDERFILL BorferFill="\d+" FillArea="\w+"', '<PAGEBORDERFILL BorferFill="%d" FillArea="Paper"' % BF["cream"], secdef)
    first = ('<P ParaShape="%d" Style="0"><TEXT CharShape="%d"><COLDEF Count="1" Layout="Left" SameGap="0" SameSize="true" Type="Newspaper"/>%s</TEXT></P>'
             % (D.P_TINY, D.C_TINY, secdef))
    head_xml = S.build_head(title, bins)
    store = ""
    for i, pth in enumerate(bins):
        raw = open(pth, "rb").read()
        b64 = __import__("base64").b64encode(raw).decode()
        b64 = "\n".join(b64[k:k + 76] for k in range(0, len(b64), 76))
        store += '<BINDATA Encoding="Base64" Id="%d" Size="%d">%s</BINDATA>' % (i + 1, len(raw), b64)
    tail = re.sub(r"<BINDATASTORAGE>.*?</BINDATASTORAGE>", ("<BINDATASTORAGE>%s</BINDATASTORAGE>" % store) if store else "",
                  base[base.index("<TAIL>"):], flags=re.S)
    doc = head_xml + '<BODY><SECTION Id="0">' + first + "".join(pages) + "</SECTION></BODY>" + tail
    open(out_path, "w", encoding="utf-8").write(doc)
    return out_path
