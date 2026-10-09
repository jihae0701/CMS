import sys,zipfile,re,collections
from lxml import etree
z=zipfile.ZipFile(sys.argv[1])
names=z.namelist()
assert names[0]=='mimetype' and z.getinfo('mimetype').compress_type==0, 'mimetype first/stored'
for n in names:
    if n.endswith('.xml') or n.endswith('.hpf') or n.endswith('.rdf'):
        etree.fromstring(z.read(n))
sec=z.read('Contents/section0.xml').decode()
root=etree.fromstring(sec.encode())
HP='{http://www.hancom.co.kr/hwpml/2011/paragraph}'
ids=collections.Counter()
for tag in ['tbl','rect','pic','equation','line','container']:
    for e in root.iter(HP+tag): ids[e.get('id')]+=1
dup=[k for k,v in ids.items() if v>1]
print('objects',sum(ids.values()),'dup ids',len(dup))
en=list(root.iter(HP+'endNote')); print('endnotes',len(en))
# every image ref exists in manifest
hpf=z.read('Contents/content.hpf').decode()
refs=set(re.findall(r'binaryItemIDRef="([^"]+)"',sec))
for r in refs:
    m=re.search(r'<opf:item id="%s" href="([^"]+)"'%r,hpf); assert m, r; assert m.group(1) in names, m.group(1)
print('images ok',sorted(refs))
# hpf items exist
for m in re.finditer(r'href="([^"]+)"',hpf):
    assert m.group(1) in names, m.group(1)
# equations empty?
empty=[e for e in root.iter(HP+'script') if not (e.text or '').strip()]
print('empty scripts',len(empty))
# paragraphs direct children only p
print('top-level children',collections.Counter(etree.QName(c).localname for c in root))
# compare tag vocabulary with form
form=etree.fromstring(zipfile.ZipFile(sys.argv[2]).read('Contents/section0.xml'))
ft=set(etree.QName(e).localname for e in form.iter()); nt=set(etree.QName(e).localname for e in root.iter())
print('new tags not in form:',nt-ft)
