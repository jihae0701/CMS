# -*- coding: utf-8 -*-
"""공통수학1 기본서 인디자인(바인더2.pdf 링크)을 단원 PDF 12개로 PDF 만들 때 쓸 '바인더2' 대신 PDF 만들기 (2026-11-19).
python c1b_binder.py <공통수학1 기본서 IDML> <단원1.pdf> … <단원12.pdf> <출력 바인더.pdf>
- 사용자가 바인더2.pdf 대신 단원 PDF 12개를 줌. 책 쪽 배치: 단원 표지 2·24·48·70·92·116·140·168·192·212·230·254, 본문은 표지 다음 쪽부터 단원 PDF 차례대로.
- IDML이 쪽마다 바인더2의 몇 쪽을 쓰는지 읽어(24쪽 ↔ 바인더 25쪽, 25쪽 ↔ 바인더 24쪽처럼 서로 바뀐 곳도 있음), 그 바인더 쪽 자리에 그 책 쪽에 올 단원 PDF 쪽을 넣음.
  본문이 아닌 쪽(표지 아래 깔리는 쪽)은 빈 A4.
"""
import sys, re, zipfile
from urllib.parse import unquote
import pymupdf

idml, units, out = sys.argv[1], sys.argv[2:14], sys.argv[14]
OPEN = [2, 24, 48, 70, 92, 116, 140, 168, 192, 212, 230, 254]
srcs = [pymupdf.open(u) for u in units]
content = {}                                         # 책 쪽 → (단원, 쪽)
for k, (o, d) in enumerate(zip(OPEN, srcs)):
    for i in range(d.page_count):
        content[o + 1 + i] = (k, i)
z = zipfile.ZipFile(idml)
dm = z.read("designmap.xml").decode()
link = {}                                            # 바인더 쪽 → 책 쪽
for f in re.findall(r'<idPkg:Spread src="([^"]+)"', dm):
    s = z.read(f).decode()
    names = re.findall(r'<Page [^>]* Name="(\d+)"', s)
    for r in re.findall(r"<Rectangle .*?</Rectangle>", s, re.S):
        if "<PDF" not in r: continue
        if not unquote(re.search(r'LinkResourceURI="([^"]+)"', r).group(1)).endswith("바인더2.pdf"): continue
        tx = float(re.search(r'ItemTransform="1 0 0 1 (\S+)', r).group(1))
        pg = int(names[0] if (tx < 0 or len(names) == 1) else names[-1])
        link[int(re.search(r'PageNumber="(\d+)"', r).group(1))] = pg
doc = pymupdf.open()
W, H = 595.22, 842
for b in range(1, max(link) + 1):
    pg = link.get(b)
    if pg in content:
        k, i = content[pg]
        doc.insert_pdf(srcs[k], from_page=i, to_page=i)
    else:
        doc.new_page(width=W, height=H)
doc.save(out, garbage=3, deflate=True)
print("바인더 쪽", doc.page_count, "본문 넣은 쪽", sum(1 for b, p in link.items() if p in content), "빈 쪽", sorted(b for b in range(1, max(link) + 1) if link.get(b) not in content))
