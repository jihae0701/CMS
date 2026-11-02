"""정답·해설(미주)과 정답 모음 수식의 bold를 없앤다. python3 apply_unbold.py 파일.hwp ... (제자리에서 고침)"""
import sys, os, zlib, shutil, tempfile
sys.path.insert(0, os.path.dirname(__file__))
from hwplib import Hwp, recs
import unbold, inplace, cfb

def main(path):
    h = Hwp(path)
    raw = h.stream('BodyText/Section0')
    new, changed, other = unbold.process(raw)
    h.ole.close()
    if not changed:
        return 0, other, 'none'
    data = new
    if h.compressed:
        c = zlib.compressobj(9, zlib.DEFLATED, -15); data = c.compress(new) + c.flush()
    tmp = path + '.tmp'
    if inplace.replace_stream(path, tmp, ['BodyText', 'Section0'], data):
        mode = 'inplace'
    else:
        root = cfb.read_tree(path); cfb.find(root, 'BodyText/Section0').data = data; cfb.write(root, tmp); mode = 'rewrite'
    os.replace(tmp, path)
    return len(changed), other, mode

if __name__ == '__main__':
    for p in sys.argv[1:]:
        print(p, *main(p))
