import re,html,sys
sys.path.insert(0,'.')
import hwpxedit as H
x=H.load(sys.argv[1])
for a in sys.argv[2:]:
    n,p=a.split(':')
    out=[]
    for s0,e0 in H.region(x,int(n),p):
        s=x[s0:e0]
        s=re.sub(r'<hp:equation (?:(?!</hp:equation>).)*?<hp:script\b[^>]*>(.*?)</hp:script></hp:equation>', lambda m:'⟦'+m.group(1)+'⟧', s, flags=re.S)
        s=re.sub(r'<hp:pic (?:(?!</hp:pic>).)*</hp:pic>','[그림]',s,flags=re.S)
        s=re.sub(r'<[^>]+>','',s)
        out.append(html.unescape(s))
    print(a, ' '.join(out)[:900]); print()
