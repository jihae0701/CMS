# 1단원 5번(고난도 3) 해설: 줄글로 풀린 곱셈표를 3×5 표로 되살림
import zipfile, re, sys
SRC, DST = sys.argv[1:3]
zi = zipfile.ZipFile(SRC); items = [(i, zi.read(i.filename)) for i in zi.infolist()]; zi.close()
k = next(j for j, (i, _) in enumerate(items) if i.filename == "Contents/section0.xml")
s = items[k][1].decode("utf-8")
i = s.find('<hp:endNote number="5"'); e = s.find("</hp:endNote>", i)
E_ = s[i:e]
a = E_.find("<hp:t>곱</hp:t>"); pa = E_.rfind("<hp:p ", 0, a)
paras = []; pos = pa
for n in range(15):
    q = E_.find("</hp:p>", pos) + 7
    paras.append(E_[pos:q]); pos = q
assert re.sub(r"<[^>]+>", "", paras[0]) == "곱", paras[0][:200]
eqs = []
for p in paras[1:]:
    m = re.findall(r"<hp:equation .*?</hp:equation>", p, re.S)
    assert len(m) == 1 and not re.sub(r"<hp:equation .*?</hp:equation>|<[^>]+>", "", p).strip(), p[:300]
    eqs.append(m[0])
scr = [re.search(r"<hp:script>(.*?)</hp:script>", x).group(1) for x in eqs]
assert scr == ["-2i", "2i", "-2", "2", "-2i", "-4", "4", "4i", "-4i", "2i", "4", "-4", "-4i", "4i"], scr
cells = [["<hp:t>곱</hp:t>"] + eqs[0:4], [eqs[4]] + eqs[5:9], [eqs[9]] + eqs[10:14]]
CW, CH, BF = 4800, 1900, 9
tr = []
for r, row in enumerate(cells):
    tcs = []
    for c, x in enumerate(row):
        run = x if x.startswith("<hp:t>") else x + "<hp:t/>"
        tcs.append('<hp:tc name="" header="0" hasMargin="0" protect="0" editable="0" dirty="0" borderFillIDRef="%d"><hp:subList id="" textDirection="HORIZONTAL" lineWrap="BREAK" vertAlign="CENTER" linkListIDRef="0" linkListNextIDRef="0" textWidth="0" textHeight="0" hasTextRef="0" hasNumRef="0"><hp:p id="0" paraPrIDRef="10" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0"><hp:run charPrIDRef="25">%s</hp:run></hp:p></hp:subList><hp:cellAddr colAddr="%d" rowAddr="%d"/><hp:cellSpan colSpan="1" rowSpan="1"/><hp:cellSz width="%d" height="%d"/><hp:cellMargin left="510" right="510" top="141" bottom="141"/></hp:tc>' % (BF, run, c, r, CW, CH))
    tr.append("<hp:tr>%s</hp:tr>" % "".join(tcs))
tbl = ('<hp:tbl id="2500000501" zOrder="0" numberingType="TABLE" textWrap="TOP_AND_BOTTOM" textFlow="BOTH_SIDES" lock="0" dropcapstyle="None" pageBreak="CELL" repeatHeader="1" rowCnt="3" colCnt="5" cellSpacing="0" borderFillIDRef="%d" noAdjust="0">'
       '<hp:sz width="%d" widthRelTo="ABSOLUTE" height="%d" heightRelTo="ABSOLUTE" protect="0"/>'
       '<hp:pos treatAsChar="1" affectLSpacing="0" flowWithText="1" allowOverlap="0" holdAnchorAndSO="0" vertRelTo="PARA" horzRelTo="PARA" vertAlign="TOP" horzAlign="LEFT" vertOffset="0" horzOffset="0"/>'
       '<hp:outMargin left="0" right="0" top="283" bottom="283"/><hp:inMargin left="510" right="510" top="141" bottom="141"/>%s</hp:tbl>') % (BF, 5 * CW, 3 * CH, "".join(tr))
new_p = '<hp:p id="0" paraPrIDRef="10" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0"><hp:run charPrIDRef="25">%s<hp:t/></hp:run></hp:p>' % tbl
E2 = E_[:pa] + new_p + E_[pos:]
s = s[:i] + E2 + s[e:]
items[k] = (items[k][0], s.encode("utf-8"))
with zipfile.ZipFile(DST, "w") as zo:
    for it, d in items:
        zo.writestr(it, d, compress_type=zipfile.ZIP_STORED if it.filename == "mimetype" else zipfile.ZIP_DEFLATED)
print("5번 해설 표 3×5 넣음")
