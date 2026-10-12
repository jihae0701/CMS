import sys, collections, xml.etree.ElementTree as ET
sys.path.insert(0, sys.argv[3])
from hdr import load
HP='{http://www.hancom.co.kr/hwpml/2011/paragraph}'
faces,cps,pps,_=load(sys.argv[2])
root=ET.parse(sys.argv[1]).getroot()
ctx=collections.Counter()
def walk(el, where):
    for ch in el:
        tag=ch.tag.split('}')[1]
        w=where
        if tag=='endNote': w='미주'
        elif tag in('rect','container','tbl') and where=='본문': w='도형/표'
        if tag=='run':
            n=sum(len(''.join(t.itertext())) for t in ch.findall(HP+'t'))+5*len(ch.findall(HP+'equation'))
            if n: ctx[(w,ch.get('charPrIDRef'))]+=n
        walk(ch,w)
walk(root,'본문')
for (w,c),n in sorted(ctx.items(), key=lambda x:-x[1])[:40]:
    print(w,c,n,cps[c])
