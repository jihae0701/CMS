# -*- coding: utf-8 -*-
"""기본서 4단원 = 복소수와 이차방정식 (학원 초안 '5. 복소수와 이차방정식(초안).hwpx'를 1~3단원 기본서 모양으로 정리)

python compose4.py <초안.hwpx> <번호 본보기(2단원 원본).hwpx> <출력.hwpx>
- 수식 안의 변환 흔적을 지우고, 검수 수정(fixE.FIX)을 초안 문항 순서(k)대로 적용한다.
- 유형: 01 i의 거듭제곱 / 02 켤레복소수 / 03 근과 계수의 관계(새 유형, 단원 마무리 4문항을 옮김) / 04 f(ax+b)=0 / 05 작성\n  / 06 두 일차식의 곱 / 07 켤레근. 그 밖의 빠진 유형은 유형서에서 다룬다. 대표문제는 단원 마무리의 √(β/α)-√(α/β) 문항. 단원 마무리는 17문항(전체 39문항).
- 유형마다 새 쪽에서 시작, 문항 번호는 3단원(082~121)에 이어 122부터.
"""
import sys, re
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from xml.sax.saxutils import escape, unescape
import hwpxio as io, hwpxmerge as hm, fixes, numbering as nb, shortans, eqsize, addprob, fixE

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


# 3-1. 새 유형 03 '이차방정식의 근과 계수의 관계': 02 유형 뒤에 두고, 단원 마무리에서 4문항을 옮겨 온다
def qtext_of(a, e):
    return "".join(io.text(re.sub(r"<hp:endNote .*?</hp:endNote>", "", P[i], flags=re.S)) for i in range(a, e + 1))


def find_seg(sub):
    for a, e in nb.segments(P):
        if sub in qtext_of(a, e):
            return a, e
    raise ValueError(sub)


def problem_block(sub):
    """번호 문단부터 다음 문항 번호 문단(또는 제목) 앞까지"""
    a, e = find_seg(sub)
    i = a if nb.num_text(P[a]) is not None else a - 1
    while nb.num_text(P[i]) is None:
        i -= 1
    j = e + 1
    while j < len(P) and nb.num_text(P[j]) is None and not nb.is_heading(P[j]) and "<hp:rect" not in P[j]:
        j += 1
    return i, j


s2 = next(i for i, p in enumerate(P) if "유형별 학습하기" in io.text(p))
s3 = next(i for i, p in enumerate(P) if "단원 마무리 하기" in io.text(p))
SPACER = next(p for p in P[s2:s3] if nb.blank(p) and 'pageBreak="1"' not in p and 'columnBreak="1"' not in p)
moved, cut = [], set()
for sub in fixE.MOVE_VIETA:
    i, j = problem_block(sub)
    body = [io.set_break(p, page=0, col=0) for p in P[i:j] if not nb.blank(p)]
    moved += body + [SPACER] * 16
    cut |= set(range(i, j))
for sub in fixE.DROP_VIETA:
    i, j = problem_block(sub)
    cut |= set(range(i, j))
heads = [i for i, p in enumerate(P) if nb.is_heading(p) and re.match(r"0\d", io.text(p).strip())]
h_make = next(i for i in heads if "작성" in io.text(P[i]))
newhead = P[h_make].replace("<hp:t>이차방정식의 작성</hp:t>", "<hp:t>이차방정식의 근과 계수의 관계</hp:t>", 1)
assert newhead != P[h_make], "작성 제목 글자를 찾지 못함"
newhead = re.sub(r"<hp:t>\d\d</hp:t>", "<hp:t>03</hp:t>", newhead, count=1)
for i in heads:                                   # 03~06 -> 04~07
    n = int(re.match(r"0(\d)", io.text(P[i]).strip()).group(1))
    if n >= 3:
        P[i] = re.sub(r"<hp:t>\d\d</hp:t>", "<hp:t>%02d</hp:t>" % (n + 1), P[i], count=1)
h03 = next(i for i in heads if "방정식" in io.text(P[i]) and "해" in io.text(P[i]))   # 원래 03 f(ax+b)=0
P = [p for i, p in enumerate(P[:h03]) if i not in cut] + [newhead] + moved + \
    [p for i, p in enumerate(P[h03:], h03) if i not in cut]
P, nprob, _ = nb.renumber(P, tmpl, start=START)
# 대표문제: 모양은 04 유형(원래 03) 대표문제(f(x-1)=0)를 본으로, 새 제목 바로 뒤에
if fixE.NEW_VIETA_REP:
    rep_num = nb.num_text(P[problem_block("f(x-1)=0")[0]])
    hn = next(i for i, p in enumerate(P) if nb.is_heading(p) and "근과 계수의 관계" in io.text(p))
    P = P[:hn + 1] + addprob.build(P, rep_num, fixE.NEW_VIETA_REP, blanks=16) + P[hn + 1:]
    P, nprob, _ = nb.renumber(P, tmpl, start=START)


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
