import sys, re, zipfile, glob, os
D='/home/user/CMS/미적분Ⅰ_CLIMATH_C'; DM='/home/user/CMS/미적분Ⅰ_CLIMATH_M'
def load(p):
    z=zipfile.ZipFile(p); h=z.read('Contents/header.xml').decode()
    fonts={}
    for lang,body in re.findall(r'<hh:fontface lang="(\w+)"[^>]*>(.*?)</hh:fontface>',h,re.S):
        for i,n in re.findall(r'<hh:font id="(\d+)" face="([^"]+)"',body): fonts[(lang,i)]=n
    def defs(tag):
        return {m.group(1):m.group(0) for m in re.finditer(r'<hh:%s id="(\d+)".*?</hh:%s>'%(tag,tag),h,re.S)}
    return z,h,fonts,defs('charPr'),defs('paraPr'),defs('borderFill')
def norm_char(s,fonts):
    m=re.search(r'<hh:fontRef ([^/]*)/>',s)
    if m:
        langs=dict(re.findall(r'(\w+)="(\d+)"',m.group(1)))
        rep=' '.join('%s=%s'%(k,fonts.get((k.upper(),v),'?')) for k,v in sorted(langs.items()))
        s=s.replace(m.group(0),'<FONTS %s/>'%rep)
    return re.sub(r' id="\d+"','',s)
bad=0
for u in range(1,11):
    n=[f for f in os.listdir(D) if f.startswith('%d. '%u) and f.endswith('.hwpx')][0]
    zc,hc,fc,cc,pc,bc=load(D+'/'+n); zm,hm,fm,cm,pm,bm=load(DM+'/'+n)
    for k in (0,1):
        a=zc.read('Contents/masterpage%d.xml'%k).decode(); b=zm.read('Contents/masterpage%d.xml'%k).decode()
        ra=re.findall(r'(charPrIDRef|paraPrIDRef|borderFillIDRef)="(\d+)"',a); rb=re.findall(r'(charPrIDRef|paraPrIDRef|borderFillIDRef)="(\d+)"',b)
        if len(ra)!=len(rb): print(u,k,'참조 수 다름'); bad+=1; continue
        for (t,x),(_,y) in zip(ra,rb):
            if t=='charPrIDRef': e=norm_char(cc[x],fc)==norm_char(cm[y],fm)
            elif t=='paraPrIDRef': e=re.sub(r' id="\d+"','',pc[x])==re.sub(r' id="\d+"','',pm[y])
            else: e=re.sub(r' id="\d+"','',bc[x])==re.sub(r' id="\d+"','',bm[y])
            if not e: bad+=1; print(u,k,t,x,y,'다름')
        sa=re.sub(r'(IDRef|id)="\d+"','',a).replace('ⓒ','ⓜ'); sb=re.sub(r'(IDRef|id)="\d+"','',b)
        if sa!=sb: print(u,k,'구조 다름'); bad+=1
    # 바탕쪽 그림
    for img in re.findall(r'binaryItemIDRef="(\w+)"', zc.read('Contents/masterpage1.xml').decode()):
        hc_=re.search(r'<opf:item id="%s" href="([^"]+)"'%img,zc.read('Contents/content.hpf').decode()).group(1)
        hm_=re.search(r'<opf:item id="%s" href="([^"]+)"'%img,zm.read('Contents/content.hpf').decode()).group(1)
        if zc.read(hc_)!=zm.read(hm_): print(u,'바탕쪽 그림 다름',img); bad+=1
print('다른 곳',bad)
