import olefile, zlib, struct
def recs(data):
    i=0; out=[]
    while i<len(data):
        h=struct.unpack_from('<I',data,i); h=h[0]; i+=4
        tag=h&0x3ff; lvl=(h>>10)&0x3ff; sz=h>>20
        if sz==0xfff: sz=struct.unpack_from('<I',data,i)[0]; i+=4
        out.append([tag,lvl,data[i:i+sz]]); i+=sz
    return out
def pack(rs):
    b=bytearray()
    for tag,lvl,p in rs:
        sz=len(p)
        if sz>=0xfff: b+=struct.pack('<II',tag|(lvl<<10)|(0xfff<<20),sz)
        else: b+=struct.pack('<I',tag|(lvl<<10)|(sz<<20))
        b+=p
    return bytes(b)
class Hwp:
    def __init__(s,path):
        s.ole=olefile.OleFileIO(path); s.path=path
        fh=s.ole.openstream('FileHeader').read(); s.flags=struct.unpack_from('<I',fh,36)[0]
        s.compressed=bool(s.flags&1)
    def stream(s,name):
        d=s.ole.openstream(name).read()
        return zlib.decompress(d,-15) if s.compressed else d
    def sections(s):
        return sorted(['/'.join(e) for e in s.ole.listdir() if e[0]=='BodyText'], key=lambda x:int(x.split('Section')[1]))
def text_of(p):
    # PARA_TEXT utf16 with ctrl chars
    out=[]; i=0
    while i+1<len(p):
        c=struct.unpack_from('<H',p,i)[0]
        if c<32:
            if c in (0,10,13,24,25,26,27,28,29,30,31): i+=2; 
            else: i+=16
            if c==10: out.append('\n')
            continue
        out.append(chr(c)); i+=2
    return ''.join(out)

def objprops(p):
    # CTRL_HDR of gso/tbl common object
    cid=p[:4][::-1].decode('latin1')
    attr,vo,ho,w,hgt,z=struct.unpack_from('<IiiIIi',p,4)
    return dict(id=cid,attr=attr,vo=vo,ho=ho,w=w,h=hgt,
        treat=attr&1, vrel=(attr>>3)&3, valign=(attr>>5)&7, hrel=(attr>>8)&3, halign=(attr>>10)&7)
