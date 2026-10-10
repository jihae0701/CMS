# -*- coding: utf-8 -*-
"""기본서 4단원 = 복소수와 이차방정식 (학원 초안 '5. 복소수와 이차방정식(초안).hwpx'를 1~3단원 기본서 모양으로 정리)

python compose4.py <초안.hwpx> <번호 본보기(2단원 원본).hwpx> <출력.hwpx>
- 수식 안의 변환 흔적을 지우고, 검수 수정(fixE.FIX)을 초안 문항 순서(k)대로 적용한다.
- 유형 순서는 초안 그대로(01 i의 거듭제곱 ~ 06 켤레근의 활용). 빠진 유형은 유형서에서 다룬다.
- 유형마다 새 쪽에서 시작, 문항 번호는 3단원(082~121)에 이어 122부터.
"""
import sys, re
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from xml.sax.saxutils import escape, unescape
import hwpxio as io, hwpxmerge as hm, fixes, numbering as nb, shortans, eqsize, fixE

SRC, NUMSRC, OUT = sys.argv[1:4]
START = 122           # 1단원 001~041, 2단원 042~081, 3단원 082~121에 이어서
TITLE = "4. 복소수와 이차방정식"

f, o = io.read(SRC)
sec = f["Contents/section0.xml"].decode("utf-8")
head, P, tail = io.split(sec)
P = [io.nolines(p) for p in P]

# 0. 수식 안의 변환 흔적·오타 (바뀐 수식은 크기를 다시 잰다)
doc0 = fixes.Doc(P)


def clean_eq(m):
    eq = m.group(0)
    sm = re.search(r"(<hp:script[^>]*>)(.*?)(</hp:script>)", eq, re.S)
    if not sm:
        return eq
    sc = unescape(sm.group(2))
    new = sc
    for pat, rep in fixE.SCRIPT_FIX:
        new = re.sub(pat, rep, new.strip() if pat.startswith("^") else new)
    new = new.strip() if new != sc else sc
    if new == sc:
        return eq
    eq = eq[:sm.start()] + sm.group(1) + escape(new) + sm.group(3) + eq[sm.end():]
    return fixes.resize_eq(eq, doc0.base)


P = [re.sub(r"<hp:equation .*?</hp:equation>", clean_eq, p, flags=re.S) for p in P]

# 개념 정리: √a√b=-√(ab)의 조건 'a=0, b=0' -> 'a=0 또는 b=0'
ci = next(i for i, p in enumerate(P) if "⇨" in io.text(p) and "rootb" in io.text(p) and "b=0" in io.text(p))
k = P[ci].rfind("<hp:t>, </hp:t>")
P[ci] = P[ci][:k] + "<hp:t> 또는 </hp:t>" + P[ci][k + len("<hp:t>, </hp:t>"):]

# 1. 검수 수정 (초안 순서 k)
P, log = fixes.apply(P, fixE.FIX, "E")

# 2. 유형마다 새 쪽 (01은 'STEP 2' 제목 바로 뒤라 그대로)
s2 = next(i for i, p in enumerate(P) if "유형별 학습하기" in io.text(p))
s3 = next(i for i, p in enumerate(P) if "단원 마무리 하기" in io.text(p))
for i in range(s2 + 1, s3):
    if nb.is_heading(P[i]) and not re.match(r"01", io.text(P[i]).strip()):
        P[i] = io.set_break(P[i], page=1)

# 3. 문항 번호 문단 본보기(2단원 원본의 번호 문단)를 이 문서 번호 체계로
fn, on = io.read(NUMSRC)
hN = fn["Contents/header.xml"].decode("utf-8")
_, PN, _ = io.split(fn["Contents/section0.xml"].decode("utf-8"))
M = hm.Merger(f["Contents/header.xml"].decode("utf-8"), hN)
tmpl = M.body(next(io.nolines(p) for p in PN if nb.num_text(p) and "<hp:container" not in p))
P, nprob, nins = nb.renumber(P, tmpl, start=START)


# 4. 단답형 바꾸기 (보기 ㄱㄴㄷ 문항은 5지선다로 남김)
def seg_pos(sub):
    for kk, (a, e) in enumerate(nb.segments(P), 1):
        if sub in "".join(io.text(re.sub(r"<hp:endNote .*?</hp:endNote>", "", P[i], flags=re.S)) for i in range(a, e + 1)):
            return kk
    raise ValueError(sub)


keep = tuple(seg_pos(s) for s in fixE.KEEP_MC)
P, slog = shortans.convert(P, fixes.Doc(P), keep=keep)
print("단답형", sum(1 for l in slog if l[1] == "단답형"), [l for l in slog if l[1] != "단답형"])
P, nprob, _ = nb.renumber(P, tmpl, start=START)
P = nb.note_start(P, START)
print("문항", nprob)

f["Contents/section0.xml"] = (head + "".join(P) + tail).encode("utf-8")
f["Contents/header.xml"] = M.hA.encode("utf-8")
io.write(OUT, f, o)
print("문단", len(P), "->", OUT)
