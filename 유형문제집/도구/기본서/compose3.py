# -*- coding: utf-8 -*-
"""기본서 3단원 = 인수분해 (학원 초안 '4. 인수분해(초안).hwpx'를 1·2단원 기본서 모양으로 정리)

python compose3.py <초안.hwpx> <3단원 원본 번호 본보기(2단원 원본).hwpx> <출력.hwpx>
- 검수 수정(fixD.FIX)을 초안 문항 순서(k)대로 적용한 뒤 유형을 다시 배치한다.
- 유형 순서: 01 개수 / 02 a³+b³+c³-3abc / 03 여러 문자(새 유형) / 04 복이차식(기본 2문항 보충)
             / 05 상반식 / 06 완전제곱식 / 07 배수가 될 조건 / 08 삼각형 모양 판별(새 유형)
- 유형마다 새 쪽에서 시작, 문항 번호는 2단원(042~081)에 이어 082부터.
"""
import sys, re
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
import hwpxio as io, hwpxmerge as hm, fixes, numbering as nb, shortans, addprob, fixD

SRC, NUMSRC, OUT = sys.argv[1:4]
START = 82            # 1단원 001~041, 2단원 042~081에 이어서
TITLE = "3. 인수분해"

f, o = io.read(SRC)
sec = f["Contents/section0.xml"].decode("utf-8")
head, P, tail = io.split(sec)
P = [io.nolines(p) for p in P]

# 0. 검수 수정 (초안 순서 k)
P, log = fixes.apply(P, fixD.FIX, "D")
for i, p in enumerate(P):                      # 해설의 '4. 인수분해' 같은 단원 표시
    if io.text(p).strip() == "4. 인수분해":
        P[i] = p.replace("<hp:t>4. 인수분해</hp:t>", "<hp:t>%s</hp:t>" % TITLE)


def find(pat, start=0):
    for i in range(start, len(P)):
        if re.search(pat, io.text(P[i])):
            return i
    raise ValueError(pat)


# 1. STEP 2 유형 구역 나누기
s2 = find(r"유형별 학습하기")
s3 = find(r"단원 마무리 하기")
heads = [i for i in range(s2 + 1, s3) if nb.is_heading(P[i])]
end2 = s3
while 'pageBreak="1"' in P[end2 - 1] and nb.blank(P[end2 - 1]):     # STEP 3 앞의 쪽 나눔 빈 문단
    end2 -= 1
blocks = {}
for j, a in enumerate(heads):
    b = heads[j + 1] if j + 1 < len(heads) else end2
    name = re.sub(r"^\d\d|유형$", "", io.text(P[a]).strip())
    blocks[name] = P[a:b]
key = {n: [k for k in blocks if n in k][0] for n in ("개수", "𝒂𝟯", "상반식", "완전제곱식", "배수", "복이차식")}


def retitle(hp, num, title=None):
    """유형 제목 상자: 번호(와 제목)를 바꾸고 새 쪽에서 시작"""
    hp = re.sub(r"<hp:t>\d\d</hp:t>", "<hp:t>%s</hp:t>" % num, hp, count=1)
    if title:
        t = re.findall(r"<hp:t>([^<]*)</hp:t>", hp)
        old = [x for x in t if x not in (num, "유형") and x.strip()][0]
        hp = hp.replace("<hp:t>%s</hp:t>" % old, "<hp:t>%s</hp:t>" % title, 1)
    return io.set_break(hp, page=1) if num != "01" else hp


def section(name, num):
    b = list(blocks[key[name]])
    b[0] = retitle(b[0], num)
    return b


# 새 유형 제목은 '배수가 될 조건' 제목 상자를 본으로
HEAD_TMPL = blocks[key["배수"]][0]
step2 = (section("개수", "01") + section("𝒂𝟯", "02")
         + [retitle(HEAD_TMPL, "03", "여러 문자를 포함한 식의 인수분해")]
         + section("복이차식", "04") + section("상반식", "05") + section("완전제곱식", "06")
         + section("배수", "07")
         + [retitle(HEAD_TMPL, "08", "인수분해와 삼각형의 모양")])
P = P[:s2 + 1] + step2 + P[end2:]

# 2. 문항 번호 문단 본보기(2단원 원본의 번호 문단)를 이 문서 번호 체계로
fn, on = io.read(NUMSRC)
hN = fn["Contents/header.xml"].decode("utf-8")
_, PN, _ = io.split(fn["Contents/section0.xml"].decode("utf-8"))
M = hm.Merger(f["Contents/header.xml"].decode("utf-8"), hN)
tmpl = M.body(next(io.nolines(p) for p in PN if nb.num_text(p) and "<hp:container" not in p))
P, nprob, nins = nb.renumber(P, tmpl, start=START)

# 3. 새 문항 넣기: 대표문제는 초안 k=3(대표, 문제 한 문단), 보통 문항은 k=4를 본으로
def block_of(num):
    i = next(k for k, p in enumerate(P) if nb.num_text(p) == num)
    return i


def add_after_heading(htext, items, rep_tmpl, tmpl_num):
    """유형 제목 htext 바로 뒤(또는 그 유형의 첫 문항 앞)에 items를 넣는다"""
    global P
    hi = next(i for i, p in enumerate(P) if nb.is_heading(p) and htext in io.text(p))
    new = []
    for j, it in enumerate(items):
        t = rep_tmpl if (j == 0 and it.get("rep")) else tmpl_num
        new += addprob.build(P, t, [it], blanks=it.get("blanks", 16))
    P = P[:hi + 1] + new + P[hi + 1:]


REP, NORM = "%03d" % (START + 2), "%03d" % (START + 3)      # 초안 k=3, k=4의 번호
NORM_P = P[block_of(NORM)]
add_after_heading("여러 문자를 포함한 식", fixD.NEW_MULTI, REP, NORM)
add_after_heading("복이차식", fixD.NEW_BIQ, REP, NORM)
add_after_heading("삼각형의 모양", fixD.NEW_TRI, REP, NORM)
# 복이차식 유형: 원래 첫 문항이 대표문제가 아니므로 새 대표문제가 앞에 온다

# 4. 단답형 바꾸기 (5지선다가 자연스러운 문항은 fixD.KEEP_MC의 글귀로 찾음)
def seg_pos(sub):
    segs = nb.segments(P)
    for k, (a, e) in enumerate(segs, 1):
        if sub in "".join(io.text(re.sub(r"<hp:endNote .*?</hp:endNote>", "", P[i], flags=re.S)) for i in range(a, e + 1)):
            return k
    raise ValueError(sub)


keep = tuple(seg_pos(s) for s in fixD.KEEP_MC)
P, slog = shortans.convert(P, fixes.Doc(P), keep=keep)
print("단답형", sum(1 for l in slog if l[1] == "단답형"), [l for l in slog if l[1] != "단답형"])
P, nprob, nins2 = nb.renumber(P, tmpl, start=START)
P = nb.note_start(P, START)
print("문항", nprob)

f["Contents/section0.xml"] = (head + "".join(P) + tail).encode("utf-8")
f["Contents/header.xml"] = M.hA.encode("utf-8")
for mp in [n for n in f if n.startswith("Contents/masterpage")]:
    x = re.sub(r"<hp:t>4[.,] 인수분해</hp:t>", "<hp:t>%s</hp:t>" % TITLE, f[mp].decode("utf-8"))   # 초안 머리말의 '4, 인수분해' 오타 포함
    f[mp] = x.encode("utf-8")
io.write(OUT, f, o)
print("문단", len(P), "->", OUT)
