# 단원 파일 개요: 최상위 문단 단위로 텍스트+수식, 도형/그림/미주 요약
import sys, xml.etree.ElementTree as ET
HP='{http://www.hancom.co.kr/hwpml/2011/paragraph}'
HH='{http://www.hancom.co.kr/hwpml/2011/head}'
hdr=ET.parse(sys.argv[2]).getroot()
styles={s.get('id'):s.get('name') for s in hdr.iter(HH+'style')}
def sh(t): return t.split('}')[1]
def ptext(p, notes):
    out=[]
    for r in p.findall(HP+'run'):
        for x in r:
            t=sh(x.tag)
            if t=='t':
                for y in x.iter():
                    if y is x:
                        out.append(x.text or '')
                    else:
                        tt=sh(y.tag)
                        if tt=='lineBreak': out.append('⏎')
                        elif tt=='tab': out.append('⇥')
                        out.append(y.tail or '')
            elif t=='equation': out.append('⟦'+(x.find(HP+'script').text or '').replace('\n',' ')+'⟧')
            elif t=='ctrl':
                for c in x:
                    ct=sh(c.tag)
                    if ct=='endNote':
                        notes.append(c); out.append(f'[미주{c.get("number") or ""}]')
                    elif ct=='footNote': notes.append(c); out.append('[각주]')
                    elif ct in('autoNum','newNum'): out.append(f'[{ct}:{c.get("numType")}]')
                    elif ct in('colPr','pageNum','header','footer','bookmark','pageHiding'): out.append(f'[{ct}]')
                    else: out.append(f'[{ct}]')
            elif t=='tbl': out.append(f'[표 {x.get("rowCnt")}x{x.get("colCnt")}: '+' | '.join(' '.join(ptext(pp,[]) for pp in tc.iter(HP+'p')) for tc in x.iter(HP+'tc'))+']')
            elif t=='pic':
                img=x.find('.//{http://www.hancom.co.kr/hwpml/2011/core}img')
                sz=x.find(HP+'sz')
                out.append(f'[그림 {img.get("binaryItemIDRef")} {sz.get("width")}x{sz.get("height")}]')
            elif t in('container','rect','line','curve','ellipse','polygon','arc','connectLine'):
                inner=[ptext(pp,[]) for pp in x.iter(HP+'p')]
                kinds={}
                for y in x.iter():
                    k=sh(y.tag)
                    if k in('line','curve','ellipse','polygon','arc','rect','pic','container'): kinds[k]=kinds.get(k,0)+1
                sz=x.find(HP+'sz')
                out.append(f'[도형:{t} {sz.get("width") if sz is not None else ""}x{sz.get("height") if sz is not None else ""} {kinds} 글:'+' / '.join(i for i in inner if i.strip())[:300]+']')
            elif t in('secPr','fieldBegin','fieldEnd'): pass
            else: out.append(f'[{t}]')
    return ''.join(out)
root=ET.parse(sys.argv[1]).getroot()
for i,p in enumerate(root.findall(HP+'p')):
    notes=[]
    txt=ptext(p,notes)
    st=styles.get(p.get('styleIDRef'))
    if txt.strip() or True:
        print(f'#{i} [{st}|pp{p.get("paraPrIDRef")}] {txt}')
    for n in notes:
        for q in n.iter(HP+'p'):
            print(f'      └미주: {ptext(q,[])}')
