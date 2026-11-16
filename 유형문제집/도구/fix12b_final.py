# -*- coding: utf-8 -*-
"""공통수학2 기본서 12단원(무리식과 무리함수) 사용자 완성본(2026-11-16) 등록.  python fix12b_final.py <입력.hwpx> <출력.hwpx>  (환경변수 S: swapimg.py 위치)
- 숫자를 직접 쓴 문항 번호 문단 5곳(글자 '448'·'449'·'458'·'457'·'477', 문단 모양 26)을 자동 번호 문단(다른 문항과 같은 번호 상자 문단)으로
  → 문항 번호 436~477(42문항, 11단원 435에 이어짐)
- 미주 시작 438 → 436(번호 매기기 시작값 436과 같게), 미주 번호 값도 436~477로
- 붙여 넣은 스캔 그림 4장을 다시 그린 그림(도구/그림/draw2_12.py)으로: image2·3(개념 y=√(ax), y=−√(ax)), image5·6(470번 해설)
- 해설 첫 줄 '[정답]' 3곳 → '󰂼'(다른 문항과 같은 10pt)
"""
import sys, os, re, zipfile, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from lite import top_paras
G = os.path.join(HERE, "그림")
src, out = sys.argv[1:3]
z = zipfile.ZipFile(src)
items = [(i, z.read(i.filename)) for i in z.infolist()]
s = z.read("Contents/section0.xml").decode()

P = top_paras(s, 0, len(s))
T = lambda i: s[P[i][0]:P[i][1]]
num_tpl = next(T(i) for i in range(len(P)) if re.match(r'<hp:p [^>]*paraPrIDRef="49"', T(i)) and "<hp:container" in T(i))
lit = [i for i in range(len(P)) if re.match(r'<hp:p [^>]*paraPrIDRef="26"', T(i))
       and re.fullmatch(r"\s*\d{3}\s*", "".join(re.findall(r"<hp:t>([^<]*)</hp:t>", re.sub(r"<hp:endNote .*?</hp:endNote>", "", T(i), flags=re.S))))]
assert len(lit) == 5, lit


def bump(x, k):
    x = re.sub(r'(<hp:container id=")(\d+)', lambda m: m.group(1) + str(1997000000 + 100 * k), x, count=1)
    x = re.sub(r'\b(id)="(199\d{7})"', lambda m: '%s="%d"' % (m.group(1), int(m.group(2)) % 1000000 + 1997100000 + 1000 * k), x)
    x = re.sub(r'\b(instid)="(99\d{7})"', lambda m: '%s="%d"' % (m.group(1), int(m.group(2)) % 1000000 + 997100000 + 1000 * k), x)
    return x


for k, i in enumerate(sorted(lit, reverse=True)):
    s = s[:P[i][0]] + bump(num_tpl, k + 1) + s[P[i][1]:]

# 미주 번호
s = re.sub(r'(<hp:endNotePr>.*?newNum=")(\d+)(")', lambda m: m.group(1) + "436" + m.group(3), s, count=1, flags=re.S)
k = [435]


def ren(m):
    k[0] += 1
    e = m.group(0)
    e = re.sub(r'(<hp:endNote number=")\d+', lambda q: q.group(1) + str(k[0]), e, count=1)
    e = re.sub(r'(<hp:autoNum num=")\d+(" numType="ENDNOTE")', lambda q: q.group(1) + str(k[0]) + q.group(2), e, count=1)
    return e


s = re.sub(r"<hp:endNote .*?</hp:endNote>", ren, s, flags=re.S)
print("미주", 436, "~", k[0])

# 정답 표시
n = [0]


def ans(m):
    n[0] += 1
    return m.group(0).replace('<hp:run charPrIDRef="%s">' % m.group(1), '<hp:run charPrIDRef="18">', 1).replace("<hp:t> [정답] </hp:t>", "<hp:t> 󰂼 </hp:t>", 1)


s = re.sub(r'<hp:run charPrIDRef="(\d+)"><hp:ctrl><hp:autoNum num="\d+" numType="ENDNOTE">(?:(?!</hp:ctrl>).)*</hp:ctrl><hp:t> \[정답\] </hp:t>', ans, s, flags=re.S)
print("[정답] → 󰂼:", n[0], "남은 [정답]:", s.count("[정답]"))

tmp = out + ".tmp.hwpx"
with zipfile.ZipFile(tmp, "w") as zo:
    for info, data in items:
        if info.filename == "Contents/section0.xml":
            data = s.encode("utf-8")
        zo.writestr(info, data, compress_type=info.compress_type)
W = {"image2": ("c2b12_c1.png", 9600), "image3": ("c2b12_c2.png", 9600), "image5": ("c2b12_470a.png", 13000), "image6": ("c2b12_470b.png", 14000)}
subprocess.check_call([sys.executable, "-I", os.path.join(os.environ["S"], "swapimg.py"), tmp, out] +
                      ["%s=%s@%d" % (k_, os.path.join(G, f), w) for k_, (f, w) in W.items()])
os.remove(tmp)
print("->", out)
