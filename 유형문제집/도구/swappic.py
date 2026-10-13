# -*- coding: utf-8 -*-
"""문서(hwpx) 안의 그림을 도구/그림/의 새 PNG로 바꾸고 크기를 1픽셀=6.4 HWPUNIT로 맞춘다(문서는 다시 만들지 않음).
python 도구/swappic.py 문서.hwpx BinData/image201.png=u5_n1090.png [...]
그림을 다시 그린 뒤 문서를 통째로 다시 만들기 어려울 때(사용자가 고친 문서 등) 쓴다.
"""
import os, re, sys, struct, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
PIC_DIR = os.path.join(HERE, "그림")
K_HWP = 6.4


def png_size(path):
    with open(path, "rb") as f:
        return struct.unpack(">II", f.read(24)[16:24])


def resize_pic(x, W, H):
    x = re.sub(r'<hp:orgSz [^>]*/>', '<hp:orgSz width="%d" height="%d"/>' % (W, H), x)
    x = re.sub(r'<hp:curSz [^>]*/>', '<hp:curSz width="%d" height="%d"/>' % (W, H), x)
    x = re.sub(r'centerX="\d+" centerY="\d+"', 'centerX="%d" centerY="%d"' % (W // 2, H // 2), x)
    x = re.sub(r'<hc:scaMatrix [^>]*/>', '<hc:scaMatrix e1="1" e2="0" e3="0" e4="0" e5="1" e6="0"/>', x)
    x = re.sub(r'<hp:imgRect>.*?</hp:imgRect>', '<hp:imgRect><hc:pt0 x="0" y="0"/><hc:pt1 x="%d" y="0"/>'
               '<hc:pt2 x="%d" y="%d"/><hc:pt3 x="0" y="%d"/></hp:imgRect>' % (W, W, H, H), x, flags=re.S)
    x = re.sub(r'<hp:imgClip [^>]*/>', '<hp:imgClip left="0" right="%d" top="0" bottom="%d"/>' % (W, H), x)
    x = re.sub(r'<hp:imgDim [^>]*/>', '<hp:imgDim dimwidth="%d" dimheight="%d"/>' % (W, H), x)
    x = re.sub(r'<hp:sz width="\d+" widthRelTo="ABSOLUTE" height="\d+"',
               '<hp:sz width="%d" widthRelTo="ABSOLUTE" height="%d"' % (W, H), x)
    return x


def swap(doc, pairs):
    """pairs: {BinData 경로: 새 PNG 경로}"""
    tmp = doc + ".tmp"
    with zipfile.ZipFile(doc) as zin, zipfile.ZipFile(tmp, "w") as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            if info.filename in pairs:
                data = open(pairs[info.filename], "rb").read()
            elif re.match(r"Contents/section\d+\.xml$", info.filename):
                sec = data.decode("utf-8")
                for bin_name, png in pairs.items():
                    img = os.path.splitext(os.path.basename(bin_name))[0]
                    pw, ph = png_size(png)
                    W, H = round(pw * K_HWP), round(ph * K_HWP)
                    pos = 0
                    while True:
                        i = sec.find('binaryItemIDRef="%s"' % img, pos)
                        if i < 0:
                            break
                        a = sec.rindex("<hp:pic ", 0, i)
                        b = sec.index("</hp:pic>", i) + len("</hp:pic>")
                        x = resize_pic(sec[a:b], W, H)
                        sec = sec[:a] + x + sec[b:]
                        pos = a + len(x)
                data = sec.encode("utf-8")
            zout.writestr(info, data)
    os.replace(tmp, doc)


if __name__ == "__main__":
    doc = sys.argv[1]
    pairs = {}
    for a in sys.argv[2:]:
        k, v = a.split("=")
        pairs[k] = v if os.path.isabs(v) else os.path.join(PIC_DIR, v)
    swap(doc, pairs)
    print("그림", len(pairs), "->", doc)
