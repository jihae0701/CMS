import sys, xml.etree.ElementTree as ET
HH='{http://www.hancom.co.kr/hwpml/2011/head}'
def load(path):
    r=ET.parse(path).getroot()
    faces={}
    for ff in r.iter(HH+'fontface'):
        lang=ff.get('lang'); faces[lang]={f.get('id'):f.get('face') for f in ff.findall(HH+'font')}
    cps={}
    for c in r.iter(HH+'charPr'):
        fr=c.find(HH+'fontRef'); ra=c.find(HH+'ratio'); sp=c.find(HH+'spacing')
        d=dict(h=c.get('height'),color=c.get('textColor'),han=faces['HANGUL'].get(fr.get('hangul')),lat=faces['LATIN'].get(fr.get('latin')),
               ratio=ra.get('hangul'),sp=sp.get('hangul'),bold=c.find(HH+'bold') is not None,italic=c.find(HH+'italic') is not None,
               shade=c.get('shadeColor'),bf=c.get('borderFillIDRef'),ul=(c.find(HH+'underline').get('type') if c.find(HH+'underline') is not None else None))
        cps[c.get('id')]=d
    pps={}
    for p in r.iter(HH+'paraPr'):
        al=p.find(HH+'align'); ls=p.find('.//'+HH+'lineSpacing'); mg=p.find('.//'+HH+'margin')
        m={}
        if mg is not None:
            for x in mg: m[x.tag.split('}')[1]]=x.get('value')
        pps[p.get('id')]=dict(align=al.get('horizontal'),ls=(ls.get('type'),ls.get('value')) if ls is not None else None,m=m,heading=p.find(HH+'heading').get('type') if p.find(HH+'heading') is not None else None)
    return faces,cps,pps,r
if __name__=='__main__':
    faces,cps,pps,_=load(sys.argv[1])
    kind=sys.argv[2]
    for i in sys.argv[3:]:
        print(i, (cps if kind=='c' else pps)[i])
