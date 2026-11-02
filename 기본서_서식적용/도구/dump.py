import sys,struct,glob,os; sys.path.insert(0,__import__('os').path.dirname(__file__))
from hwplib import *
HB=16
def para_text(p, ctrls):
    out=[]; i=0; k=0
    while i+1<len(p):
        c=struct.unpack_from('<H',p,i)[0]
        if c<32:
            if c in (0,10,13,24,25,26,27,28,29,30,31):
                if c==10: out.append(' / ')
                if c==9: out.append('\t')
                i+=2; continue
            if c==9: out.append(' '); i+=16; continue
            cid=p[i+2:i+6][::-1].decode('latin1','ignore')
            out.append('{%s}'%cid.strip()); i+=16; continue
        out.append(chr(c) if not 0xD800<=c<0xE000 else '?'); i+=2
    return ''.join(out)
def dump(fn):
    rs=recs(Hwp(fn).stream('BodyText/Section0'))
    # pass: attach equation scripts into the paragraph text that owns the ctrl
    lines=[]
    stack=[]  # (level, kind)
    cur=None
    eqs=[]
    for idx,(t,l,p) in enumerate(rs):
        if t==HB+51:
            lines.append([l, para_text(p,None)])
        elif t==HB+72:  # EQEDIT
            n=struct.unpack_from('<H',p,4)[0]; s=p[6:6+2*n].decode('utf-16le','replace')
            # find nearest preceding paragraph text at level < l containing {eqed}
            for L in reversed(lines):
                if '{eqed}' in L[1] and L[0]<l:
                    L[1]=L[1].replace('{eqed}','⟦'+s+'⟧',1); break
            else: lines.append([l,'[EQ '+s+']'])
        elif t==HB+55 and p[:4]==b'  ne':
            lines.append([l,'<<미주>>'])
    return lines
if __name__=='__main__':
    for l,s in dump(sys.argv[1]):
        s=s.strip()
        if s: print('  '*min(l,6)+s)
