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
    def char(self, pt, color="#1d2433", bold=False, shade=None):
        key = ("c", pt, color, bold, shade)
        for i, k in enumerate(self.cs):
            if k[0] == key:
                return self.cs0 + i
        attrs = ('BorderFillId="1" Height="%d" Id="%d" ShadeColor="%d" SymMark="0" TextColor="%d" UseFontSpace="false" UseKerning="false"'
                 % (int(pt * 100), self.cs0 + len(self.cs), rgb(shade) if shade else 4294967295, rgb(color)))
        f = "FONTID_PLACEHOLDER"
        body = ('<CHARSHAPE %s>%s<RATIO Hangul="100" Hanja="100" Japanese="100" Latin="100" Other="100" Symbol="100" User="100"/>'
                '<CHARSPACING Hangul="0" Hanja="0" Japanese="0" Latin="0" Other="0" Symbol="0" User="0"/>'
                '<RELSIZE Hangul="100" Hanja="100" Japanese="100" Latin="100" Other="100" Symbol="100" User="100"/>'
                '<CHAROFFSET Hangul="0" Hanja="0" Japanese="0" Latin="0" Other="0" Symbol="0" User="0"/>%s</CHARSHAPE>'
                % (attrs, f, "<BOLD/>" if bold else ""))
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

    def build_head(self, title):
        h = self.head
        # 글꼴: 맑은 고딕을 각 언어 글꼴 목록에 추가
        def addfont(m):
            n = int(m.group(2))
            self.font_id = n
            font = ('<FONT Id="%d" Name="맑은 고딕" Type="ttf"><TYPEINFO ArmStyle="1" Contrast="0" FamilyType="2" Letterform="1" Midline="1" Proportion="0" StrokeVariation="1" Weight="6" XHeight="1"/></FONT>' % n)
            return m.group(0).replace('Count="%d"' % n, 'Count="%d"' % (n + 1)) + font
        h = re.sub(r'(<FONTFACE Count="(\d+)" Lang="\w+">)', addfont, h)
        fid = ('<FONTID Hangul="{0}" Hanja="{0}" Japanese="{0}" Latin="{0}" Other="{0}" Symbol="{0}" User="{0}"/>').format(self.font_id)
        cs = "".join(b.replace("FONTID_PLACEHOLDER", fid) for _, b in self.cs)
        h = re.sub(r'<CHARSHAPELIST Count="\d+">', '<CHARSHAPELIST Count="%d">' % (self.cs0 + len(self.cs)), h)
        h = h.replace("</CHARSHAPELIST>", cs + "</CHARSHAPELIST>")
        h = re.sub(r'<BORDERFILLLIST Count="\d+">', '<BORDERFILLLIST Count="%d">' % (self.bf0 - 1 + len(self.bf)), h)
        h = h.replace("</BORDERFILLLIST>", "".join(b for _, b in self.bf) + "</BORDERFILLLIST>")
        h = re.sub(r'<PARASHAPELIST Count="\d+">', '<PARASHAPELIST Count="%d">' % (self.ps0 + len(self.ps)), h)
        h = h.replace("</PARASHAPELIST>", "".join(b for _, b in self.ps) + "</PARASHAPELIST>")
        h = re.sub(r"<BINDATALIST.*?</BINDATALIST>", "", h, flags=re.S)
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
        body = "".join('<TEXT CharShape="%d"><CHAR>%s</CHAR></TEXT>' % (cs, escape(t)) for t, cs in runs if t)
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

    def bar(self, rate, avg, width, show_avg):
        """색칠한 표 칸 막대(평균 위치는 굵은 왼쪽 선)"""
        S = self.st
        FILL, TRACK, DARK = "#2F5597", "#E3E8F2", "#1d2433"
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
            bf = S.border(col, left=("0.6", DARK) if tick else None)
            ws.append(w)
            cells.append(("", bf))
        if not ws:
            ws, cells = [width], [("", S.border(TRACK))]
        ws[-1] += width - sum(ws)
        empty = '<P ParaShape="%d" Style="0"><TEXT CharShape="%d"/></P>' % (self.P_TINY, self.C_TINY)
        row = [(empty, bf, "Center") for _, bf in cells]
        return self.table([row], ws, heights=[620], margin=(0, 0, 0, 0))


# ---------------- 보고서 ----------------
LVCOL = {"매우 우수": "#1F3864", "우수": "#2F5597", "양호": "#3f8a6b", "보완 필요": "#c27b2c", None: "#9aa3b5"}


def build(students, cfg, exams, stats, SUBJ, level, opinion, out_path, recommended=lambda s, c: None):
    base = open(BASE_HML, encoding="utf-8").read()
    head = base[:base.index("<BODY>")]
    S = Styles(head)
    D = Doc(S)
    C = dict(
        brand=S.char(10, "#2F5597", True), title=S.char(19, "#1F3864", True), meta=S.char(9, "#5b6577"),
        label=S.char(8, "#6b7588"), val=S.char(10.5, "#1d2433", True), valn=S.char(10.5, "#1d2433"),
        secmark=S.char(11.5, "#2F5597", True), sec=S.char(11.5, "#1F3864", True),
        sub=S.char(9.5, "#44506a", True), score=S.char(24, "#1F3864", True), scoreu=S.char(10, "#6b7588"),
        miss=S.char(16, "#9aa3b5", True), cap=S.char(8.5, "#5b6577"),
        us=S.char(8.5, "#6b7588"), uu=S.char(9.5, "#1d2433", True), pct=S.char(9.5, "#1F3864", True),
        leg=S.char(8, "#6b7588"), legb=S.char(8, "#2F5597", True), legd=S.char(8, "#1d2433", True),
        gno=S.char(8, "#44506a"), glab=S.char(8.5, "#44506a", True),
        o=S.char(10, "#2F5597", True), x=S.char(10, "#c0504d", True), n=S.char(10, "#9aa3b5"),
        body=S.char(9.5, "#1d2433"), bodyb=S.char(9.5, "#1F3864", True), bul=S.char(9.5, "#2F5597", True),
        recol=S.char(11, "#ffffff", True), recoc=S.char(20, "#1F3864", True), recod=S.char(9, "#44506a"), foot=S.char(8.5, "#5b6577"), footb=S.char(8.5, "#1F3864", True),
    )
    BADGE = {k: S.char(8.5, "#ffffff", True, shade=v) for k, v in LVCOL.items()}
    BF = dict(
        none=1, box=S.box(), card=S.box(fill="#f7f9fd"), head=S.border(bottom=("0.7", "#1F3864")),
        row=S.border(bottom=("0.12", "#e6eaf2")), grid=S.box("#d5dced"), grids=S.box("#d5dced", fill="#f4f1fa"),
        navy=S.box("#1F3864", "0.4", fill="#1F3864"), write=S.box("#1F3864", "0.4"),
        writeL=S.border(None, None, ("0.12", "#d5dced"), ("0.4", "#1F3864"), ("0.4", "#1F3864")),
        writeR=S.border(None, None, ("0.4", "#1F3864"), ("0.4", "#1F3864"), ("0.4", "#1F3864")), foot=S.border(top=("0.12", "#d5dced")),
    )

    def badge(lv):
        return (" %s " % (lv or "미응시"), BADGE.get(lv, BADGE[None]))

    def sec(title, first=False):
        return D.p([("┃ ", C["secmark"]), (title, C["sec"])], D.P_SEC)

    pages = []
    show = cfg["show_avg"]
    subjects = " · ".join(n for _, n in SUBJ)
    for idx, s in enumerate(students):
        x = []
        brk = ' ColumnBreak="false" PageBreak="true"' if idx else ""
        # 머리말
        left = D.p([(cfg["academy"], C["brand"])]) + D.p([(cfg["title"], C["title"])], D.P_TIGHT)
        right = D.p([("시험일 %s" % cfg["date"], C["meta"])], D.P_R) + D.p([("평가 영역 %s" % subjects, C["meta"])], D.P_R)
        x.append(D.table([[(left, BF["head"], "Bottom"), (right, BF["head"], "Bottom")]], [33000, 18000], margin=(0, 300, 0, 0), extra=brk))
        x.append(D.p([("", D.C_TINY)], D.P_GAP))
        # 학생 정보
        took = " · ".join(n for k, n in SUBJ if s["took"][k]) or "-"
        info = [(D.p([("이름", C["label"])]) + D.p([(s["name"], C["val"])]), BF["box"]),
                (D.p([("학교", C["label"])]) + D.p([(str(s["school"]), C["valn"])]), BF["box"]),
                (D.p([("응시 과목", C["label"])]) + D.p([(took, C["valn"])]), BF["box"])]
        x.append(D.table([info], [17000, 17000, 17000], margin=(250, 250, 500, 500)))
        # 과목별 결과
        x.append(sec("과목별 결과"))
        cards = []
        for key, nm in SUBJ:
            full = stats[("full", key)]
            if not s["took"][key]:
                c = D.p([(nm, C["sub"])]) + D.p([("미응시", C["miss"])])
            else:
                sc = s["score"][key]
                avg = stats[("avg", key)]
                lv = level(sc / full if full else 0, cfg)
                cap = "20문항 중 %d문항 정답" % sum(s["ok"][key]) + (" · 전체 평균 %.1f점" % avg if show and avg is not None else "")
                c = (D.p([(nm, C["sub"])]) +
                     D.p([("%g" % sc, C["score"]), (" / %d점    " % full, C["scoreu"]), badge(lv)]) +
                     D.bar(sc / full if full else 0, (avg / full) if (avg is not None and full) else None, 22600, show) +
                     D.p([(cap, C["cap"])]))
            cards.append((c, BF["card"], "Top"))
        x.append(D.table([[cards[0], ("", BF["none"]), cards[1]]], [25000, 1000, 25000], margin=(300, 300, 700, 700)))
        # 단원별 성취도
        x.append(sec("단원별 성취도"))
        rows = []
        for key, nm in SUBJ:
            for u in cfg["units"][key]:
                r = s["unit"][(key, u)]
                rows.append([(D.p([(nm, C["us"])]), BF["row"]),
                             (D.p([(u, C["uu"])]), BF["row"]),
                             (D.bar(r, stats[("uavg", key, u)], 20500, show), BF["row"]),
                             (D.p([("-" if r is None else "%d%%" % round(r * 100), C["pct"])], D.P_R), BF["row"]),
                             (D.p([badge(level(r, cfg))], D.P_C), BF["row"])])
        x.append(D.table(rows, [6200, 11000, 21300, 4800, 7700], margin=(170, 170, 200, 200)))
        leg = [("■ ", C["legb"]), ("학생 득점률    ", C["leg"])]
        if show:
            leg += [("┃ ", C["legd"]), ("전체 평균    ", C["leg"])]
        leg += [("성취 수준: 매우 우수 %g%% 이상 · 우수 %g%% 이상 · 양호 %g%% 이상" % tuple(cfg["lv"]), C["leg"])]
        x.append(D.p(leg))
        # 문항별 결과
        x.append(sec("문항별 결과"))
        grows = []
        for key, nm in SUBJ:
            row = [(D.p([(nm, C["glab"])]), BF["none"], "Center")]
            for q, ok in zip(exams[key], s["ok"][key]):
                mark = ("-", C["n"]) if not s["took"][key] else (("○", C["o"]) if ok else ("×", C["x"]))
                row.append((D.p([(str(q["no"]), C["gno"])], D.P_C) + D.p([mark], D.P_C), BF["grids"] if q["no"] > 14 else BF["grid"]))
            grows.append(row)
        x.append(D.table(grows, [5400] + [2280] * 20, margin=(60, 60, 0, 0)))
        x.append(D.p([("○ 정답 · × 오답      1~14번 객관식 · 15~20번 단답형(음영)", C["leg"])]))
        # 종합 의견
        x.append(sec("종합 의견"))
        text, tips = opinion(s, cfg, stats)
        op = D.p([(text, C["body"])], D.P_L)
        for u, t in tips:
            if t:
                op += D.p([("•  ", C["bul"]), (u, C["bodyb"]), (" — " + t, C["body"])], D.P_BUL)
        x.append(D.table([[(op, BF["box"], "Top")]], [51000], margin=(500, 500, 700, 700)))
        # 추천 반: 최종반(수동조정 우선), 보류·미정이면 직접 쓰는 빈칸
        x.append(sec("추천 반"))
        rc = recommended(s, cfg)
        if rc:
            right = [(D.p([(rc, C["recoc"])], D.P_C), BF["writeL"], "Center"),
                     (D.p([(cfg["class_desc"].get(rc, ""), C["recod"])], D.P_L), BF["writeR"], "Center")]
            widths = [9000, 12000, 30000]
        else:
            right = [("".join(D.p([("", C["body"])]) for _ in range(3)), BF["write"], "Center")]
            widths = [9000, 42000]
        x.append(D.table([[(D.p([("추천 반", C["recol"])], D.P_C), BF["navy"], "Center")] + right],
                         widths, heights=[6200], margin=(300, 300, 600, 600)))
        # 꼬리말
        x.append(D.p([("", D.C_TINY)], D.P_GAP))
        x.append(D.table([[(D.p([(cfg["notice"], C["foot"])]), BF["foot"], "Center"),
                           (D.p([(cfg["academy"] + " ", C["footb"]), (str(cfg["contact"]), C["foot"])], D.P_R), BF["foot"], "Center")]],
                         [35000, 16000], margin=(250, 0, 0, 0)))
        pages.append("".join(x))

    # 구역 정의(A4, 1단, 머리말·바탕쪽 없음)
    secdef = re.search(r"<SECDEF.*?</SECDEF>", base, re.S).group(0)
    secdef = re.sub(r"<MASTERPAGE.*?</MASTERPAGE>", "", secdef, flags=re.S)
    secdef = re.sub(r'<PAGEDEF [^>]*>.*?</PAGEDEF>',
                    '<PAGEDEF GutterType="LeftOnly" Height="84188" Landscape="0" Width="59528">'
                    '<PAGEMARGIN Bottom="2268" Footer="0" Gutter="0" Header="0" Left="3969" Right="3969" Top="3118"/></PAGEDEF>', secdef, flags=re.S)
    secdef = secdef.replace('MasterPage="true"', 'MasterPage="false"')
    first = ('<P ParaShape="%d" Style="0"><TEXT CharShape="%d"><COLDEF Count="1" Layout="Left" SameGap="0" SameSize="true" Type="Newspaper"/>%s</TEXT></P>'
             % (D.P_TINY, D.C_TINY, secdef))
    head_xml = S.build_head(cfg["title"])
    tail = re.sub(r"<BINDATASTORAGE>.*?</BINDATASTORAGE>", "", base[base.index("<TAIL>"):], flags=re.S)
    doc = head_xml + '<BODY><SECTION Id="0">' + first + "".join(pages) + "</SECTION></BODY>" + tail
    open(out_path, "w", encoding="utf-8").write(doc)
    return out_path
