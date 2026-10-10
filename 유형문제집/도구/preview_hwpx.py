# -*- coding: utf-8 -*-
"""생성한 hwpx를 읽어 내용 확인용 미리보기 PDF를 만든다(KaTeX 수식, 2단).
사용: python preview_hwpx.py <입력.hwpx> <출력.pdf>
"""
import sys, os, re, html, zipfile, base64, io
from lxml import etree
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from hwp2latex import convert  # noqa
from playwright.sync_api import sync_playwright

SRC, OUT = sys.argv[1:3]
K = os.environ.get("KATEX_DIR", os.path.join(HERE, "npmk", "node_modules", "katex", "dist"))
z = zipfile.ZipFile(SRC)
root = etree.fromstring(z.read("Contents/section0.xml"))
HP = "{http://www.hancom.co.kr/hwpml/2011/paragraph}"
hpf = z.read("Contents/content.hpf").decode()
IMG = {m.group(1): m.group(2) for m in re.finditer(r'<opf:item id="(image\d+)" href="([^"]+)"', hpf)}


def ln(e):
    return etree.QName(e).localname


def img_src(ref, w):
    data = z.read(IMG[ref])
    try:
        im = Image.open(io.BytesIO(data)).convert("RGB")
    except Exception:
        return '<div class="noimg">[그림 %s]</div>' % ref
    b = io.BytesIO(); im.save(b, "PNG")
    return '<img style="width:%.1fmm" src="data:image/png;base64,%s">' % (w / 283.46, base64.b64encode(b.getvalue()).decode())


def inline(el):
    out = []
    for r in el.findall(HP + "run"):
        for c in r:
            t = ln(c)
            if t == "t":
                out.append(html.escape(c.text or ""))
                for cc in c:
                    if ln(cc) == "lineBreak":
                        out.append("<br>")
                    elif ln(cc) == "tab":
                        out.append("&emsp;")
                    if cc.tail:
                        out.append(html.escape(cc.tail))
            elif t == "equation":
                sc = c.find(HP + "script").text or ""
                m = re.match(r"\s*(.*?)=\s*pile\{.*\}\s*right\{\s*$", sc, re.S)
                if m:   # 두 줄 식 왼쪽 칸: 'h(x)= pile{ # # } right{' -> h(x)= 와 두 줄 높이의 왼쪽 중괄호
                    lx = convert(m.group(1)) + r"=\left\{\rule{0pt}{2.2em}\right."
                else:
                    lx = convert(sc)
                out.append('<span class="m" data-t="%s"></span>' % html.escape(lx))
            elif t == "tbl":
                out.append(table(c))
            elif t == "pic":
                ref = c.find(".//{*}img").get("binaryItemIDRef")
                w = int(c.find(HP + "sz").get("width"))
                if ref == "image9":
                    out.append('<span class="bogilab">보기</span>')
                elif ref != "image2":
                    out.append('<div class="fig">%s</div>' % img_src(ref, w))
            elif t == "rect":
                ls = c.find(HP + "lineShape")
                if ls is not None and ls.get("style") == "NONE":
                    # 표 칸 안의 선 없는 글상자(보기·조건 상자): 문단마다 한 줄, 안쪽 여백만 둔다
                    sub = c.find(HP + "drawText").find(HP + "subList")
                    txt = "".join("<div>%s</div>" % inline(p) for p in sub.findall(HP + "p"))
                    out.append('<div class="inbox">%s</div>' % txt)
                else:
                    txt = "".join(inline(p) for p in c.iter(HP + "p"))
                    out.append('<div class="head">%s</div>' % txt)
    return "".join(out)


def table(tb):
    texts = [inline(p) for p in tb.iter(HP + "p")]
    if any("다항식의 연산" in t or "나머지정리" in t for t in texts) and tb.get("rowCnt") == "4" and tb.get("colCnt") == "4":
        return '<div class="banner">%s</div>' % " ".join(t for t in texts if t)
    rows = []
    syn = tb.get("borderFillIDRef") == "40"
    pw = any("pile{" in (e.text or "") for e in tb.iter(HP + "script"))
    for tr in tb.findall(HP + "tr"):
        cells = []
        for tc in tr.findall(HP + "tc"):
            bf = tc.get("borderFillIDRef")
            inner = "".join("<div>%s</div>" % inline(p) for p in tc.find(HP + "subList").findall(HP + "p"))
            st = ""
            if syn:
                st = {"42": "border-right:1px solid #000", "44": "border-top:1px solid #000",
                      "43": "border-left:1px solid #000;border-top:1px solid #000"}.get(bf, "")
            sp = tc.find(HP + "cellSpan")
            rs = ' rowspan="%s"' % sp.get("rowSpan") if sp is not None and sp.get("rowSpan") != "1" else ""
            cells.append('<td%s style="%s">%s</td>' % (rs, st, inner))
        rows.append("<tr>%s</tr>" % "".join(cells))
    cls = "syn" if syn else "pw" if pw else "box"
    return '<table class="%s">%s</table>' % (cls, "".join(rows))


body, sols = [], []
n = 0
for p in root:
    en = p.find(".//" + HP + "endNote")
    if en is not None:
        n += 1
        src = "".join(c.text or "" for r in p.findall(HP + "run") if r.get("charPrIDRef") == "34" for c in r if ln(c) == "t")
        cb = p.get("columnBreak") == "1"
        body.append('<div class="q%s"><span class="no">%d</span> <span class="src">%s</span>' % (" cb" if cb else "", n, html.escape(src)))
        sol = "".join("<p>%s</p>" % inline(sp) for sp in en.find(HP + "subList").findall(HP + "p"))
        sols.append('<div class="s"><b>%d</b> %s</div>' % (n, sol))
        continue
    txt = inline(p)
    if p.get("pageBreak") == "1":
        body.append('<div class="pb"></div>')
    elif p.get("columnBreak") == "1":
        body.append('<div class="cb"></div>')
    body.append("<p>%s</p>" % txt)

doc = """<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="file://%s/katex.min.css">
<script src="file://%s/katex.min.js"></script><style>
@page{size:A4;margin:12mm 11mm} body{font-family:"WenQuanYi Zen Hei","Noto Sans CJK KR",sans-serif;font-size:9.6pt;line-height:1.7}
.cols{column-count:2;column-gap:8mm;column-rule:1px solid #9bb} p{margin:0 0 1mm}
.head{border:2px solid #002E68;padding:1.5mm 3mm;font-weight:700;margin:2mm 0;break-after:avoid}
.banner{background:#ECF2FA;padding:2mm;font-weight:700;margin-bottom:2mm}
.no{font-weight:800;font-size:13pt;color:#002E68} .src{font-size:8pt;color:#555}
.q{margin-top:5mm} .cb{break-before:column} .pb{break-before:page}
table.box{border:1px solid #787878;border-collapse:collapse;margin:2mm 0;width:100%%} table.box td{padding:0}
.inbox{padding:1mm 1.5mm 2mm 1.5mm} .inbox div{padding-left:2.2em;text-indent:-2.2em}
table.syn{border-collapse:collapse;margin:2mm auto} table.syn td{padding:.5mm 3mm;text-align:center;min-width:8mm} table.pw{border-collapse:collapse;margin:1mm 0 1mm 4mm;display:inline-table;vertical-align:middle} table.pw td{padding:0 1.5mm;text-align:center;white-space:nowrap}
.bogilab{background:#8e6fb3;color:#fff;font-size:8pt;padding:0 2mm}
.fig{text-align:center;margin:2mm 0} .s{margin-bottom:3mm;break-inside:avoid} h2{column-span:all}
.noimg{border:1px dashed #999;padding:4mm;text-align:center;color:#999}
</style></head><body><div class="cols">%s</div><h2>정답 및 풀이</h2><div class="cols">%s</div>
<script>document.querySelectorAll('.m').forEach(e=>{try{katex.render(e.dataset.t,e,{throwOnError:true,strict:false})}catch(x){e.textContent='⟦'+e.dataset.t+'⟧';e.style.color='red'}});</script>
</body></html>""" % (K, K, "".join(body), "".join(sols))
path = OUT + ".html"
open(path, "w", encoding="utf-8").write(doc)
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
    pg = b.new_page()
    pg.goto("file://" + os.path.abspath(path))
    pg.wait_for_timeout(500)
    bad = pg.evaluate("document.querySelectorAll('.m[style]').length")
    pg.pdf(path=OUT, format="A4", print_background=True)
    b.close()
print("미리보기:", OUT, "수식 변환 실패", bad)
