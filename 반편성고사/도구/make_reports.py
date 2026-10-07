# -*- coding: utf-8 -*-
"""채점 엑셀(입력값)을 읽어 학부모 보고서와 상담 카드(PDF)를 만든다.

사용: python make_reports.py 채점파일.xlsx 출력폴더
  - 학부모보고서_전체.pdf, 학부모보고서/번호_이름.pdf : 석차·백분위 없이 성취 수준, (선택)전체 평균, 추천 반
  - 상담카드_전체.pdf : 내부용. 석차, 반 컷과의 차이, 경계 여부, 오답 분석
엑셀의 수식 결과(캐시)에 의존하지 않고 입력값으로 직접 계산한다.
필요: openpyxl, playwright(Chromium)
"""
import sys, os, html, re
from openpyxl import load_workbook

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from problems import M1, M2
    POINT = {("공수1", p["no"]): p["point"] for p in M1}
    POINT.update({("공수2", p["no"]): p["point"] for p in M2})
except Exception:
    POINT = {}

FIRST, LAST = 7, 86
QCOLS = list(range(4, 24))  # D..W
SUBJ = [("공수1", "공통수학1"), ("공수2", "공통수학2")]
CHROME = os.environ.get("CHROME_PATH", "/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
CIRC = "①②③④⑤"


def num(v):
    if v is None or v == "":
        return None
    if isinstance(v, str):
        v = v.strip()
        try:
            f = float(v)
            return int(f) if f.is_integer() else f
        except ValueError:
            return v
    return int(v) if isinstance(v, float) and v.is_integer() else v


def read(path):
    wb = load_workbook(path)  # 입력 칸만 읽으므로 수식 캐시 불필요
    s = wb["설정"]
    val = lambda ref: s[ref].value
    cfg = {
        "classes": [val("B6"), val("B7"), val("B8")],
        "caps": [int(val("C6") or 0), int(val("C7") or 0), int(val("C8") or 0)],
        "w": [float(val("C13") or 1), float(val("C14") or 1)],
        "border": float(val("C15") or 0),
        "academy": val("B32") or "", "title": val("B33") or "", "date": val("B34") or "",
        "show_avg": (val("B35") or "표시") != "숨김",
        "lv": [float(val("B36") or 85), float(val("B37") or 70), float(val("B38") or 50)],
        "notice": val("B39") or "", "contact": val("B40") or "",
        "class_desc": {val("B%d" % (6 + i)): (val("B%d" % (45 + i)) or "") for i in range(3)},
    }
    units = {"공수1": [], "공수2": []}
    r = 19
    for key in ("공수1", "공수2"):
        while s["B%d" % r].value != "합계":
            units[key].append(s["B%d" % r].value)
            r += 1
        r += 1
    cfg["units"] = units
    order = units["공수1"] + units["공수2"]
    cfg["advice"] = {u: (s["B%d" % (51 + i)].value or "") for i, u in enumerate(order)}

    exams = {}
    for key, _ in SUBJ:
        ws = wb[key]
        exams[key] = [dict(no=i + 1, key=num(ws.cell(2, c).value), pts=num(ws.cell(3, c).value) or 0,
                           unit=ws.cell(4, c).value, level=ws.cell(5, c).value, col=c) for i, c in enumerate(QCOLS)]

    st, b = wb["학생명단"], wb["반배정"]
    students = []
    for r in range(FIRST, LAST + 1):
        name = st.cell(r, 2).value
        resp = {key: [num(wb[key].cell(r, c).value) for c in QCOLS] for key, _ in SUBJ}
        if not name and not any(v is not None for key in resp for v in resp[key]):
            continue
        if name and "(예시)" in str(name):
            continue
        students.append(dict(row=r, no=r - FIRST + 1, name=str(name or "(이름 없음)"), school=st.cell(r, 3).value or "",
                             kind=st.cell(r, 4).value or "", phone=st.cell(r, 5).value or "", memo=st.cell(r, 6).value or "",
                             comment=st.cell(r, 7).value or "", manual=b.cell(r, 11).value, resp=resp))
    return cfg, exams, students


def compute(cfg, exams, students):
    for s in students:
        s["took"], s["score"], s["ok"], s["unit"] = {}, {}, {}, {}
        for key, _ in SUBJ:
            resp = s["resp"][key]
            took = any(v is not None for v in resp)
            s["took"][key] = took
            ok = [took and v is not None and q["key"] is not None and v == q["key"] for v, q in zip(resp, exams[key])]
            s["ok"][key] = ok
            s["score"][key] = sum(q["pts"] for q, o in zip(exams[key], ok) if o) if took else None
            for u in cfg["units"][key]:
                full = sum(q["pts"] for q in exams[key] if q["unit"] == u)
                got = sum(q["pts"] for q, o in zip(exams[key], ok) if o and q["unit"] == u)
                s["unit"][(key, u)] = (got / full if full and took else None)
        if not any(s["took"].values()):
            s["total"] = None
        else:
            s["total"] = sum((s["score"][k] or 0) * w for (k, _), w in zip(SUBJ, cfg["w"]))
    ranked = [s for s in students if s["total"] is not None]
    c1, c2 = cfg["caps"][0], cfg["caps"][0] + cfg["caps"][1]
    for s in ranked:
        s["rank"] = 1 + sum(1 for t in ranked if t["total"] > s["total"])
        s["auto"] = cfg["classes"][0] if s["rank"] <= c1 else cfg["classes"][1] if s["rank"] <= c2 else cfg["classes"][2]
        s["final"] = s["manual"] or s["auto"]
    for s in students:
        s.setdefault("rank", None); s.setdefault("auto", None); s.setdefault("final", s["manual"])
    cuts = {}
    for i in range(2):
        g = [s["total"] for s in ranked if s["auto"] == cfg["classes"][i]]
        cuts[i] = min(g) if g else None
    stats = {"n": len(ranked), "cuts": cuts}
    for key, _ in SUBJ:
        takers = [s for s in students if s["took"][key]]
        stats[("avg", key)] = sum(s["score"][key] for s in takers) / len(takers) if takers else None
        stats[("full", key)] = sum(q["pts"] for q in exams[key])
        for u in cfg["units"][key]:
            v = [s["unit"][(key, u)] for s in takers if s["unit"][(key, u)] is not None]
            stats[("uavg", key, u)] = sum(v) / len(v) if v else None
            for cname in cfg["classes"]:
                vv = [s["unit"][(key, u)] for s in takers if s["final"] == cname and s["unit"][(key, u)] is not None]
                stats[("cavg", key, u, cname)] = sum(vv) / len(vv) if vv else None
        for q in exams[key]:
            n = len(takers)
            q["rate"] = sum(1 for s in takers if s["ok"][key][q["no"] - 1]) / n if n else None
    return stats


def level(rate, cfg):
    if rate is None:
        return None
    p = rate * 100
    a, b, c = cfg["lv"]
    return "매우 우수" if p >= a else "우수" if p >= b else "양호" if p >= c else "보완 필요"


LVCLS = {"매우 우수": "l0", "우수": "l1", "양호": "l2", "보완 필요": "l3"}


def josa(word, pair):  # pair=("과","와") 등: 받침 있으면 앞
    ch = word.strip()[-1]
    code = ord(ch) - 0xAC00
    has = 0 <= code <= 11171 and code % 28 != 0
    return word + (pair[0] if has else pair[1])


def opinion(s, cfg, stats):
    name = s["name"]
    took = [k for k, _ in SUBJ if s["took"][k]]
    full = sum(stats[("full", k)] for k in took)
    rate = sum(s["score"][k] for k in took) / full if full else 0
    lv = level(rate, cfg)
    first = {
        "매우 우수": f"{name} 학생은 공통수학 전반에 걸쳐 개념 이해와 문제 해결력이 매우 뛰어납니다. 고난도 문항에서도 안정적으로 풀이 과정을 이어 가는 힘이 돋보였습니다.",
        "우수": f"{name} 학생은 공통수학의 핵심 개념을 잘 이해하고 있으며, 안정적인 문제 해결력을 보여 주었습니다. 일부 단원을 보완하면 한 단계 더 성장할 수 있습니다.",
        "양호": f"{name} 학생은 공통수학의 기본 개념을 갖추고 있습니다. 단원별 이해도의 차이를 줄여 나가면 실력이 더욱 단단해질 것으로 기대됩니다.",
        "보완 필요": f"{name} 학생은 이번 진단평가를 통해 앞으로 다져야 할 부분을 분명히 확인할 수 있었습니다. 핵심 개념부터 차근차근 쌓아 가면 충분히 성장할 수 있습니다.",
    }[lv]
    units = [(k, u, s["unit"][(k, u)]) for k, _ in SUBJ for u in cfg["units"][k] if s["unit"][(k, u)] is not None]
    strong = sorted([x for x in units if x[2] * 100 >= cfg["lv"][1]], key=lambda x: -x[2])[:2]
    weak = sorted([x for x in units if x[2] * 100 < cfg["lv"][1]], key=lambda x: x[2])[:2]
    parts = [first]
    if len(strong) == 2:
        parts.append(f"특히 {josa(strong[0][1], ('과', '와'))} {strong[1][1]} 단원에서 강점을 보였습니다.")
    elif len(strong) == 1:
        parts.append(f"특히 {strong[0][1]} 단원에서 강점을 보였습니다.")
    missing = [n for k, n in SUBJ if not s["took"][k]]
    if missing:
        parts.append(f"{'·'.join(missing)}는 응시하지 않아 응시한 과목을 중심으로 분석하였습니다.")
    tips = [(u, cfg["advice"].get(u, "")) for _, u, _ in weak]
    return " ".join(parts), tips


CSS = """
@page{size:A4;margin:0}
*{box-sizing:border-box}
body{margin:0;font-family:"Noto Sans KR","Malgun Gothic","Apple SD Gothic Neo",sans-serif;color:#1d2433;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:210mm;height:297mm;padding:12mm 14mm 9mm;position:relative;page-break-after:always;overflow:hidden;display:flex;flex-direction:column}
.top{display:flex;justify-content:space-between;align-items:flex-end;border-bottom:2.5px solid #1F3864;padding-bottom:3.5mm}
.brand{font-size:10pt;color:#2F5597;font-weight:700;letter-spacing:.5px}
h1{margin:1.2mm 0 0;font-size:19pt;color:#1F3864;font-weight:800;letter-spacing:-.5px}
.meta{text-align:right;font-size:9pt;color:#5b6577;line-height:1.6}
.who{display:flex;gap:0;margin:3.5mm 0 3.8mm;border:1px solid #d5dced;border-radius:2.5mm;overflow:hidden}
.who div{flex:1;padding:2mm 4mm;font-size:10.5pt;border-right:1px solid #d5dced}
.who div:last-child{border-right:none}
.who span{display:block;font-size:8pt;color:#6b7588;margin-bottom:.5mm}
h2{font-size:11.5pt;color:#1F3864;margin:0 0 1.8mm;display:flex;align-items:center;gap:2mm}
h2:before{content:"";width:1.2mm;height:4.2mm;background:#2F5597;border-radius:.6mm}
.sec{margin-bottom:3.6mm}
.cards{display:flex;gap:4mm}
.card{flex:1;border:1px solid #d5dced;border-radius:2.5mm;padding:2.6mm 4mm;background:#f7f9fd}
.card .sub{font-size:9.5pt;color:#44506a;font-weight:700}
.card .sc{display:flex;align-items:baseline;gap:1.5mm;margin:1mm 0 .6mm}
.card .sc b{font-size:25pt;color:#1F3864;font-weight:800;line-height:1}
.card .sc i{font-style:normal;color:#6b7588;font-size:10pt}
.card .sc .badge{margin-left:auto}
.card .cap{font-size:8.5pt;color:#5b6577}
.track{position:relative;height:2.6mm;background:#e3e8f2;border-radius:1.3mm;margin:2mm 0 1.4mm}
.fill{position:absolute;left:0;top:0;bottom:0;background:#2F5597;border-radius:1.3mm}
.avg{position:absolute;top:-1mm;bottom:-1mm;width:.6mm;background:#1d2433}
.badge{display:inline-block;font-size:8.5pt;font-weight:700;padding:.6mm 2.4mm;border-radius:3mm;color:#fff;white-space:nowrap}
.l0{background:#1F3864}.l1{background:#2F5597}.l2{background:#3f8a6b}.l3{background:#c27b2c}.lx{background:#9aa3b5}
table.units{width:100%;border-collapse:collapse;font-size:9.5pt}
table.units td{padding:1.05mm 1.5mm;border-bottom:1px solid #e6eaf2;vertical-align:middle}
table.units td.s{width:19mm;color:#6b7588;font-size:8.5pt}
table.units td.u{width:33mm;font-weight:600}
table.units td.b{width:auto}
table.units td.p{width:13mm;text-align:right;font-weight:700;color:#1F3864}
table.units td.l{width:21mm;text-align:center}
table.units .track{margin:0}
.legend{font-size:8pt;color:#6b7588;margin-top:1.4mm;display:flex;gap:4mm;align-items:center}
.legend .k{display:inline-block;width:5mm;height:2mm;background:#2F5597;border-radius:1mm;vertical-align:middle;margin-right:1mm}
.legend .t{display:inline-block;width:.6mm;height:3mm;background:#1d2433;vertical-align:middle;margin-right:1mm}
.grid{display:flex;align-items:center;gap:2mm;margin-bottom:1.2mm}
.grid .gl{width:19mm;font-size:8.5pt;color:#44506a;font-weight:700}
.grid .cells{display:grid;grid-template-columns:repeat(20,1fr);flex:1;border:1px solid #d5dced;border-radius:1.5mm;overflow:hidden}
.grid .cells div{text-align:center;font-size:8pt;border-right:1px solid #e6eaf2;padding:.5mm 0;line-height:1.35}
.grid .cells div:last-child{border-right:none}
.grid .cells div.sa{background:#f4f1fa}
.grid .cells b{display:block;font-size:10pt}
.o{color:#2F5597}.x{color:#c0504d}.n{color:#9aa3b5}
.two{display:flex;gap:4mm}
.reco{width:60mm;border-radius:2.5mm;background:#1F3864;color:#fff;padding:4mm}
.reco .t{font-size:9pt;opacity:.85}
.reco .c{font-size:21pt;font-weight:800;margin:1.5mm 0 2mm}
.reco .d{font-size:8.8pt;line-height:1.6;opacity:.95}
.op{flex:1;border:1px solid #d5dced;border-radius:2.5mm;padding:3mm 4mm;font-size:9pt;line-height:1.6}
.op ul{margin:1.5mm 0 0;padding-left:4.5mm}
.op li{margin-bottom:.6mm}
.op .tc{margin-top:2mm;padding-top:2mm;border-top:1px dashed #cfd6e4}
.op .tc b{color:#1F3864}
.foot{margin-top:auto;border-top:1px solid #d5dced;padding-top:2.4mm;font-size:8.5pt;color:#5b6577;display:flex;justify-content:space-between;gap:6mm}
.foot b{color:#1F3864}
/* 상담 카드 */
.int{position:absolute;top:8mm;right:14mm;font-size:8pt;color:#c0504d;font-weight:700;border:1px solid #c0504d;padding:.6mm 2mm;border-radius:1mm}
.kpi{display:grid;grid-template-columns:repeat(4,1fr);gap:2.5mm;margin-bottom:4mm}
.kpi div{border:1px solid #d5dced;border-radius:2mm;padding:2mm 3mm;font-size:8.5pt;color:#6b7588}
.kpi b{display:block;font-size:14pt;color:#1d2433;margin-top:.5mm}
.kpi .warn{border-color:#e3a35b;background:#fff6ea}
table.t{width:100%;border-collapse:collapse;font-size:8.8pt}
table.t th{background:#eef2f9;color:#1F3864;font-weight:700;padding:1.3mm;border:1px solid #d5dced}
table.t td{padding:1.2mm 1.5mm;border:1px solid #e1e6ef;text-align:center}
table.t td.L{text-align:left}
.flag{color:#c0504d;font-weight:700}
.memo{border:1px solid #d5dced;border-radius:2mm;height:40mm;padding:2mm 3mm;font-size:8.5pt;color:#9aa3b5;
 background:repeating-linear-gradient(#fff 0 7.6mm,#e6eaf2 7.6mm 7.9mm)}
"""


def pct(v):
    return "-" if v is None else "%d%%" % round(v * 100)


def bar(rate, avg, show):
    if rate is None:
        return '<div class="track"></div>'
    a = '<div class="avg" style="left:%.1f%%"></div>' % (avg * 100) if (show and avg is not None) else ""
    return '<div class="track"><div class="fill" style="width:%.1f%%"></div>%s</div>' % (rate * 100, a)


def badge(lv):
    return '<span class="badge %s">%s</span>' % (LVCLS.get(lv, "lx"), lv or "미응시")


def parent_page(s, cfg, exams, stats):
    e = html.escape
    show = cfg["show_avg"]
    subjects = " · ".join(n for _, n in SUBJ)
    cards = []
    for key, nm in SUBJ:
        full = stats[("full", key)]
        if not s["took"][key]:
            cards.append('<div class="card"><div class="sub">%s</div><div class="sc"><b style="font-size:16pt;color:#9aa3b5">미응시</b></div></div>' % nm)
            continue
        sc = s["score"][key]
        n_ok = sum(s["ok"][key])
        avg = stats[("avg", key)]
        lv = level(sc / full if full else 0, cfg)
        cap = "20문항 중 %d문항 정답" % n_ok + (" · 전체 평균 %.1f점" % avg if show and avg is not None else "")
        cards.append('<div class="card"><div class="sub">%s</div><div class="sc"><b>%s</b><i>/ %d점</i>%s</div>%s<div class="cap">%s</div></div>'
                     % (nm, ("%g" % sc), full, badge(lv), bar(sc / full if full else 0, (avg / full) if (avg is not None and full) else None, show), cap))
    rows = []
    for key, nm in SUBJ:
        for u in cfg["units"][key]:
            r = s["unit"][(key, u)]
            rows.append('<tr><td class="s">%s</td><td class="u">%s</td><td class="b">%s</td><td class="p">%s</td><td class="l">%s</td></tr>'
                        % (nm, e(u), bar(r, stats[("uavg", key, u)], show), pct(r) if r is not None else "-", badge(level(r, cfg))))
    legend = '<div class="legend"><span><i class="k"></i>학생 득점률</span>%s<span>성취 수준: 매우 우수 %g%% 이상 · 우수 %g%% 이상 · 양호 %g%% 이상</span></div>' % (
        '<span><i class="t"></i>전체 평균</span>' if show else "", *cfg["lv"])
    grids = []
    for key, nm in SUBJ:
        cells = []
        for q, o in zip(exams[key], s["ok"][key]):
            if not s["took"][key]:
                mark = '<b class="n">-</b>'
            else:
                mark = '<b class="o">○</b>' if o else '<b class="x">×</b>'
            cells.append('<div class="%s">%d%s</div>' % ("sa" if q["no"] > 14 else "", q["no"], mark))
        grids.append('<div class="grid"><div class="gl">%s</div><div class="cells">%s</div></div>' % (nm, "".join(cells)))
    text, tips = opinion(s, cfg, stats)
    tip_html = "".join("<li><b>%s</b> — %s</li>" % (e(u), e(t)) for u, t in tips if t)
    tc = '<div class="tc"><b>선생님 한마디</b> &nbsp;%s</div>' % e(s["comment"]) if s["comment"] else ""
    cls = s["final"] or "-"
    desc = cfg["class_desc"].get(cls, "")
    return f"""<div class="page">
<div class="top"><div><div class="brand">{e(cfg['academy'])}</div><h1>{e(cfg['title'])}</h1></div>
<div class="meta">시험일 {e(str(cfg['date']))}<br>평가 영역 {subjects}</div></div>
<div class="who"><div><span>이름</span><b>{e(s['name'])}</b></div><div><span>학교</span>{e(str(s['school']))}</div><div><span>응시 과목</span>{' · '.join(n for k, n in SUBJ if s['took'][k]) or '-'}</div></div>
<div class="sec"><h2>과목별 결과</h2><div class="cards">{''.join(cards)}</div></div>
<div class="sec"><h2>단원별 성취도</h2><table class="units">{''.join(rows)}</table>{legend}</div>
<div class="sec"><h2>문항별 결과</h2>{''.join(grids)}<div class="legend"><span>○ 정답 · × 오답</span><span>1~14번 객관식 · 15~20번 단답형(음영)</span></div></div>
<div class="sec two"><div class="reco"><div class="t">추천 반</div><div class="c">{e(cls)}</div><div class="d">{e(desc)}</div></div>
<div class="op"><h2 style="margin-bottom:1.5mm">종합 의견</h2>{e(text)}{('<ul>' + tip_html + '</ul>') if tip_html else ''}{tc}</div></div>
<div class="foot"><div>{e(cfg['notice'])}</div><div style="white-space:nowrap"><b>{e(cfg['academy'])}</b> {e(str(cfg['contact']))}</div></div>
</div>"""


def counsel_page(s, cfg, exams, stats):
    e = html.escape
    cls = cfg["classes"]
    gap = []
    if s["total"] is not None:
        for i in range(2):
            c = stats["cuts"][i]
            if c is not None:
                gap.append("%s 컷 %g점 대비 %+g점" % (cls[i], c, s["total"] - c))
    near = s["total"] is not None and any(c is not None and abs(s["total"] - c) <= cfg["border"] for c in stats["cuts"].values())
    manual = s["manual"] and s["manual"] != s["auto"]
    kpi = [("공통수학1", "-" if s["score"]["공수1"] is None else "%g점" % s["score"]["공수1"], False),
           ("공통수학2", "-" if s["score"]["공수2"] is None else "%g점" % s["score"]["공수2"], False),
           ("환산총점 / 석차", "-" if s["total"] is None else "%g점 · %d/%d" % (s["total"], s["rank"], stats["n"]), False),
           ("자동배정 → 최종반", "%s → %s%s" % (s["auto"] or "-", s["final"] or "-", " (수동)" if manual else ""), near)]
    kp = "".join('<div class="%s">%s<b>%s</b></div>' % ("warn" if w else "", e(a), e(b)) for a, b, w in kpi)
    urows = []
    for key, nm in SUBJ:
        for u in cfg["units"][key]:
            r = s["unit"][(key, u)]
            urows.append("<tr><td>%s</td><td class='L'>%s</td><td><b>%s</b></td><td>%s</td><td>%s</td><td>%s</td></tr>" % (
                nm, e(u), pct(r), pct(stats[("uavg", key, u)]), pct(stats[("cavg", key, u, s["final"])]) if s["final"] else "-", level(r, cfg) or "미응시"))
    wrong = []
    easy_miss = 0
    for key, nm in SUBJ:
        if not s["took"][key]:
            continue
        for q, o, v in zip(exams[key], s["ok"][key], s["resp"][key]):
            if o:
                continue
            flag = q["rate"] is not None and q["rate"] >= 0.7
            easy_miss += flag
            ans = CIRC[q["key"] - 1] if q["no"] <= 14 and isinstance(q["key"], int) and 1 <= q["key"] <= 5 else q["key"]
            mine = "무응답" if v is None else (CIRC[v - 1] if q["no"] <= 14 and isinstance(v, int) and 1 <= v <= 5 else v)
            wrong.append("<tr><td>%s</td><td>%d</td><td>%s</td><td>%s</td><td class='L'>%s</td><td>%s</td><td>%s</td><td class='%s'>%s</td></tr>" % (
                nm, q["no"], e(str(q["unit"])), q["level"], e(POINT.get((key, q["no"]), "")), mine, ans, "flag" if flag else "", pct(q["rate"])))
    pts = []
    if near:
        pts.append("반 경계 점수대입니다. 단원별 성취와 학습 태도를 함께 보고 반을 확정하세요.")
    if easy_miss:
        pts.append("정답률 70%% 이상인 문항에서 %d문항 오답 — 개념 누락 또는 계산 실수 여부를 확인하세요." % easy_miss)
    weak = sorted([(u, s["unit"][(k, u)]) for k, _ in SUBJ for u in cfg["units"][k] if s["unit"][(k, u)] is not None], key=lambda x: x[1])[:2]
    if weak:
        pts.append("상대적 취약 단원: " + ", ".join("%s(%s)" % (u, pct(r)) for u, r in weak))
    if manual:
        pts.append("수동 조정됨: 자동배정 %s → %s" % (s["auto"], s["final"]))
    if s["memo"]:
        pts.append("비고: %s" % s["memo"])
    return f"""<div class="page"><div class="int">내부용 · 외부 유출 금지</div>
<div class="top"><div><div class="brand">{e(cfg['academy'])} · 개별 상담 카드</div><h1>{e(s['name'])} <span style="font-size:11pt;color:#5b6577;font-weight:500">{e(str(s['school']))} · {e(str(s['kind']))} · {e(str(s['phone']))}</span></h1></div>
<div class="meta">{e(cfg['title'])}<br>{' / '.join(gap) if gap else ''}</div></div>
<div style="height:4mm"></div><div class="kpi">{kp}</div>
<div class="sec"><h2>상담 포인트</h2><ul style="margin:0;padding-left:5mm;font-size:9.3pt;line-height:1.7">{''.join('<li>%s</li>' % e(p) for p in pts) or '<li>특이 사항 없음</li>'}</ul></div>
<div class="sec"><h2>단원별 득점률</h2><table class="t"><tr><th>과목</th><th>단원</th><th>학생</th><th>전체 평균</th><th>최종반 평균</th><th>수준</th></tr>{''.join(urows)}</table></div>
<div class="sec"><h2>오답 문항 <span style="font-size:8.5pt;color:#6b7588;font-weight:400">(빨간 정답률 = 70% 이상이 맞힌 문항)</span></h2>
<table class="t"><tr><th>과목</th><th>번호</th><th>단원</th><th>난도</th><th>평가 요소</th><th>학생 답</th><th>정답</th><th>전체 정답률</th></tr>{''.join(wrong) or '<tr><td colspan=8>오답 없음</td></tr>'}</table></div>
<div class="sec"><h2>상담 메모</h2><div class="memo"></div></div>
</div>"""


def render(pages, out_pdf):
    from playwright.sync_api import sync_playwright
    doc = '<!doctype html><html><head><meta charset="utf-8"><style>%s</style></head><body>%s</body></html>' % (CSS, "".join(pages))
    tmp = os.path.abspath(out_pdf) + ".html"
    open(tmp, "w", encoding="utf-8").write(doc)
    with sync_playwright() as p:
        kw = {"executable_path": CHROME} if os.path.exists(CHROME) else {}
        b = p.chromium.launch(args=["--disable-background-networking", "--no-pings"], **kw)
        pg = b.new_page()
        pg.goto("file://" + tmp)
        pg.pdf(path=out_pdf, format="A4", print_background=True, margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
        b.close()
    os.remove(tmp)


def main(xlsx, outdir):
    cfg, exams, students = read(xlsx)
    stats = compute(cfg, exams, students)
    os.makedirs(os.path.join(outdir, "학부모보고서"), exist_ok=True)
    targets = [s for s in students if s["total"] is not None]
    pages = [parent_page(s, cfg, exams, stats) for s in targets]
    render(pages, os.path.join(outdir, "학부모보고서_전체.pdf"))
    for s, pgx in zip(targets, pages):
        safe = re.sub(r'[\\/:*?"<>|]', "_", s["name"])
        render([pgx], os.path.join(outdir, "학부모보고서", "%02d_%s.pdf" % (s["no"], safe)))
    render([counsel_page(s, cfg, exams, stats) for s in targets], os.path.join(outdir, "상담카드_전체.pdf"))
    print("학생 %d명: 학부모 보고서·상담 카드 생성 완료 → %s" % (len(targets), outdir))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
