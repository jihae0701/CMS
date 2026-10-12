import sys, zipfile, re, collections
from lxml import etree
HP='{http://www.hancom.co.kr/hwpml/2011/paragraph}'; HH='{http://www.hancom.co.kr/hwpml/2011/head}'; HC='{http://www.hancom.co.kr/hwpml/2011/core}'
path, ref = sys.argv[1], sys.argv[2]
z=zipfile.ZipFile(path)
names=z.namelist()
assert names[0]=='mimetype' and z.getinfo('mimetype').compress_type==0
X={n:etree.fromstring(z.read(n)) for n in names if n.endswith(('.xml','.hpf'))}
h=X['Contents/header.xml']
ids={}
for tag in ('charPr','paraPr','style','borderFill','tabPr','numbering'):
    ids[tag]=set(e.get('id') for e in h.iter(HH+tag))
fonts={ff.get('lang'):set(f.get('id') for f in ff.findall(HH+'font')) for ff in h.iter(HH+'fontface')}
LANG={'hangul':'HANGUL','latin':'LATIN','hanja':'HANJA','japanese':'JAPANESE','other':'OTHER','symbol':'SYMBOL','user':'USER'}
for c in h.iter(HH+'charPr'):
    fr=c.find(HH+'fontRef')
    for a,l in LANG.items(): assert fr.get(a) in fonts[l],(c.get('id'),a)
    assert c.get('borderFillIDRef') in ids['borderFill']
for p in h.iter(HH+'paraPr'):
    assert p.get('tabPrIDRef') in ids['tabPr']
    hd=p.find(HH+'heading')
    if hd.get('type')=='NUMBER': assert hd.get('idRef') in ids['numbering'],p.get('id')
for n in h.iter(HH+'numbering'):
    for ph in n.iter(HH+'paraHead'):
        c=ph.get('charPrIDRef'); assert c=='4294967295' or c in ids['charPr']
for lst in h.find(HH+'refList'):
    assert int(lst.get('itemCnt'))==len(lst), lst.tag
bad=collections.Counter()
for n in ('Contents/section0.xml','Contents/masterpage0.xml','Contents/masterpage1.xml'):
    for el in X[n].iter():
        if not isinstance(el.tag,str): continue
        for a,t in (('charPrIDRef','charPr'),('paraPrIDRef','paraPr'),('styleIDRef','style'),('borderFillIDRef','borderFill')):
            v=el.get(a)
            if v is not None and v not in ids[t]: bad[(n,a,v)]+=1
print('bad refs',dict(bad))
man={it.get('id'):it.get('href') for it in X['Contents/content.hpf'].iter('{http://www.idpf.org/2007/opf/}item')}
for n in X:
    for img in X[n].iter(HC+'img'):
        i=img.get('binaryItemIDRef'); assert i in man and man[i] in names,(n,i)
print('images ok', sum(1 for k in man if k.startswith('image')))
sec=X['Contents/section0.xml']
def text(root):
    out=[]
    for el in root.iter():
        if el.tag==HP+'t': out.append(''.join(el.itertext()))
        elif el.tag==HP+'script': out.append(el.text or '')
    return ''.join(out)
r=etree.parse(ref).getroot()
print('text same:', text(r)==text(sec), len(text(sec)))
print('endnotes', len(list(sec.iter(HP+'endNote'))), 'pics', len(list(sec.iter(HP+'pic'))), 'eqs', len(list(sec.iter(HP+'equation'))))
print('linesegs', len(list(sec.iter(HP+'linesegarray'))))
mp=''.join(''.join(t.itertext()) for t in X['Contents/masterpage1.xml'].iter(HP+'t'))
print('master1 text:', mp)
