# -*- coding: utf-8 -*-
"""한글(hwpx) 문서 속 그림을 PNG로 바꿔 넣는다(스캔 그림을 다시 그린 뒤 교체할 때).
    python hwpx_swapimg.py 입력.hwpx 출력.hwpx image3=새그림.png@10000 image5=그림2.png ...
- imageN: 문서 안 그림 이름(Contents/content.hpf의 opf:item id, 그림 개체의 binaryItemIDRef)
- @폭: 문서에 넣을 폭(HWPUNIT). 빼면 지금 폭을 그대로 두고 높이만 PNG 비율로 맞춘다.
  mathfig.fit_shoot가 돌려준 폭을 그대로 쓰면 1픽셀=6.4 HWPUNIT 약속이 지켜진다.
- 원래 BMP 등은 지우고 BinData/imageN.png로 넣으며, 크기 정보(orgSz·curSz·imgRect·imgClip·imgDim·sz)를 모두 새로 맞춘다.
"""
import zipfile,re,sys,os
from PIL import Image
src,out=sys.argv[1:3]
rep={}
for a in sys.argv[3:]:
    k,v=a.split('=',1); fn,_,w=v.partition('@'); rep[k]=(fn,int(w) if w else None)
z=zipfile.ZipFile(src); items=[(i,z.read(i.filename)) for i in z.infolist()]
hpf=z.read('Contents/content.hpf').decode(); sec=z.read('Contents/section0.xml').decode()
old={k:re.search(r'<opf:item id="%s" href="([^"]+)"'%k,hpf).group(1) for k in rep}
for k,(fn,w) in rep.items():
    hpf=re.sub(r'(<opf:item id="%s" href=")[^"]+(" media-type=")[^"]+(")'%k, r'\g<1>BinData/%s.png\g<2>image/png\g<3>'%k, hpf)
    pw,ph=Image.open(fn).size
    def fix(m):
        p=m.group(0)
        if 'binaryItemIDRef="%s"'%k not in p: return p
        cw=int(re.search(r'<hp:curSz width="(\d+)"',p).group(1))
        W=w or cw; H=round(W*ph/pw)
        p=re.sub(r'<hp:orgSz [^>]*/>','<hp:orgSz width="%d" height="%d"/>'%(W,H),p)
        p=re.sub(r'<hp:curSz [^>]*/>','<hp:curSz width="%d" height="%d"/>'%(W,H),p)
        p=re.sub(r'centerX="\d+" centerY="\d+"','centerX="%d" centerY="%d"'%(W//2,H//2),p)
        p=re.sub(r'<hc:scaMatrix [^>]*/>','<hc:scaMatrix e1="1" e2="0" e3="0" e4="0" e5="1" e6="0"/>',p)
        p=re.sub(r'<hp:imgRect>.*?</hp:imgRect>','<hp:imgRect><hc:pt0 x="0" y="0"/><hc:pt1 x="%d" y="0"/><hc:pt2 x="%d" y="%d"/><hc:pt3 x="0" y="%d"/></hp:imgRect>'%(W,W,H,H),p,flags=re.S)
        p=re.sub(r'<hp:imgClip [^>]*/>','<hp:imgClip left="0" right="%d" top="0" bottom="%d"/>'%(W,H),p)
        p=re.sub(r'<hp:imgDim [^>]*/>','<hp:imgDim dimwidth="%d" dimheight="%d"/>'%(W,H),p)
        p=re.sub(r'(<hp:sz width=")\d+(" widthRelTo="ABSOLUTE" height=")\d+(")',lambda q:q.group(1)+str(W)+q.group(2)+str(H)+q.group(3),p)
        p=re.sub(r'(<hp:shapeComment>).*?(</hp:shapeComment>)',r'\1그림입니다.\2',p,flags=re.S)
        print(k,fn.split('/')[-1],'->',W,H); return p
    sec=re.sub(r'<hp:pic\b.*?</hp:pic>',fix,sec,flags=re.S)
outs=[]
drop=set(old.values())
for info,data in items:
    if info.filename in drop: continue
    if info.filename=='Contents/content.hpf': data=hpf.encode()
    elif info.filename=='Contents/section0.xml': data=sec.encode()
    outs.append((info,data))
for k,(fn,w) in rep.items():
    zi=zipfile.ZipInfo('BinData/%s.png'%k,date_time=(2026,11,13,0,0,0)); zi.compress_type=zipfile.ZIP_DEFLATED
    outs.append((zi,open(fn,'rb').read()))
with zipfile.ZipFile(out,'w') as zo:
    for info,data in outs: zo.writestr(info,data,compress_type=info.compress_type)
