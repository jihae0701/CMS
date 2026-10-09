# KaTeX(Chromium)로 수식을 렌더링해 폭·높이·기준선(px)을 측정
import json, os
from playwright.sync_api import sync_playwright
from hwp2latex import convert

HERE = os.path.dirname(os.path.abspath(__file__))
KATEX = os.environ.get("KATEX_DIR", os.path.join(HERE, "npmk", "node_modules", "katex", "dist"))  # npm install katex 위치
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

PAGE = """<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="file://%s/katex.min.css">
<script src="file://%s/katex.min.js"></script>
<style>body{font-size:%spx;font-family:serif} .katex{font-size:1em} span.m{display:inline-block;white-space:nowrap}</style>
</head><body><div id="root"></div></body></html>"""

def measure(scripts, px=16):
    """scripts -> [(w, h, depth)] px 단위"""
    latex = [convert(s) for s in scripts]
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME)
        pg = b.new_page()
        path = os.path.join(HERE, "_measure.html")
        open(path, "w").write(PAGE % (KATEX, KATEX, px))
        pg.goto("file://" + path)
        res = pg.evaluate("""(L) => {
          const root = document.getElementById('root'); const out = [];
          for (const t of L) {
            const s = document.createElement('span'); s.className='m';
            try { katex.render(t, s, {throwOnError:true, strict:false}); } catch(e) { out.push([0,0,0,String(e)]); continue; }
            const mk = document.createElement('span'); mk.style.display='inline-block'; mk.style.width='0'; mk.style.height='0';
            s.appendChild(mk);
            root.appendChild(s);
            const r = s.getBoundingClientRect();
            const mr = mk.getBoundingClientRect();
            const base = s.querySelector('.katex-html');
            const strut = s.querySelector('.strut');
            // 기준선: 높이 - 깊이
            let depth = 0; const st = s.querySelectorAll('.strut');
            const bb = s.querySelector('.base');
            out.push([r.width, r.height, mr.bottom - r.top, null]);
            root.removeChild(s);
          }
          return out; }""", latex)
        b.close()
    return res, latex

if __name__ == "__main__":
    import sys, re
    import xml.etree.ElementTree as ET
    t = ET.parse(sys.argv[1]).getroot()
    data = []
    for e in t.find("BODY").iter("EQUATION"):
        sz = e.find("SHAPEOBJECT/SIZE"); sc = e.find("SCRIPT")
        if sz is None or sc is None or not sc.text:
            continue
        data.append((sc.text, int(sz.get("Width")), int(sz.get("Height")), int(e.get("BaseLine"))))
    res, latex = measure([d[0] for d in data])
    rows = []
    for d, r, l in zip(data, res, latex):
        if r[3]:
            print("ERR", d[0], "|", l, "|", r[3][:80]); continue
        rows.append((d[0], d[1], d[2], d[3], r[0], r[1], r[2]))
    json.dump(rows, open(os.path.join(HERE, "calib.json"), "w"), ensure_ascii=False)
    import statistics
    rw = [a[1] / a[4] for a in rows if a[4] > 5]
    rh = [a[2] / a[5] for a in rows if a[5] > 5]
    print("n", len(rows), "width ratio median", statistics.median(rw), "p10", sorted(rw)[len(rw)//10], "p90", sorted(rw)[9*len(rw)//10])
    print("height ratio median", statistics.median(rh))
