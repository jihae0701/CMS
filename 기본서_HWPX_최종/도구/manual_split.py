"""수식 하나를 [('t',글자),('eq',수식)…]로 직접 나눈다. python3 manual_split.py 파일.hwpx 표.json  (표: {원래 수식: [[종류, 값], …]})"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, 'tools'))
import eqstyle
path, tab = sys.argv[1:3]
T = {k: [tuple(x) for x in v] for k, v in json.load(open(tab)).items()}
orig = eqstyle.style_script
eqstyle.style_script = lambda sc: T.get(sc, sc)
print(eqstyle.style_file(path))
