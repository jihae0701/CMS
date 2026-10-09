# -*- coding: utf-8 -*-
"""기본서 1단원 = 다항식의 연산(A) + 항등식(B)

사용: python compose1.py 1.다항식의연산.hwpx 2.항등식.hwpx 출력.hwpx
"""
import sys, os, re, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plain, shortans, hwpxio as io, hwpxmerge as hm, fixes, numbering as nb, fixA, fixB

A, B, OUT = sys.argv[1:4]   # 다항식의 연산.hwpx, 항등식.hwpx, 출력
TITLE = "다항식의 연산과 항등식"

fa, oa = io.read(A)
fb, ob = io.read(B)
secA = fa["Contents/section0.xml"].decode("utf-8")
secB = fb["Contents/section0.xml"].decode("utf-8")
hA = fa["Contents/header.xml"].decode("utf-8")
hB = fb["Contents/header.xml"].decode("utf-8")
M = hm.Merger(hA, hB)

headA, PA, tailA = io.split(secA)
headB, PB, tailB = io.split(secB)
PA = [io.nolines(p) for p in PA]
PB = [M.body(io.nolines(p)) for p in PB]
PA, logA = fixes.apply(PA, fixA.FIX, "A")
PB, logB = fixes.apply(PB, fixB.FIX, "B")


def find(P, pat, start=0):
    for i in range(start, len(P)):
        if re.search(pat, io.text(P[i])):
            return i
    raise ValueError(pat)


a_s2 = find(PA, r"유형별 학습하기")
a_s3 = find(PA, r"단원 마무리 하기")
a_tail = len(PA) - 3            # 쪽 나눔 빈 문단, 해설 제목 상자, 쪽 번호 새로
b_s2 = find(PB, r"유형별 학습하기")
b_s3 = find(PB, r"단원 마무리 하기")
b_tail = len(PB) - 3
assert "삼각함수" in io.text(PA[a_tail + 1]) and "항등식" in io.text(PB[b_tail + 1])

# STEP 1: A의 개념 + B의 개념(첫 문단의 STEP 1 제목 상자와 끝의 빈 문단은 뺌)
def last_nonblank(P, a, b):
    k = b
    while k > a and not io.text(P[k]).strip() and "<hp:rect" not in P[k] and "<hp:tbl" not in P[k]:
        k -= 1
    return k


a1_end = last_nonblank(PA, 0, a_s2 - 1)
b1_end = last_nonblank(PB, 1, b_s2 - 1)
step1 = PA[:a1_end + 1] + PB[1:b1_end + 1] + PA[a1_end + 1:a_s2]
# STEP 2: A의 유형 01~03 + B의 유형 01~04(→04~07), B 첫 유형은 새 쪽에서
b_first = b_s2 + 1
step2 = PA[a_s2:a_s3] + [io.set_break(PB[b_first], page=1)] + PB[b_first + 1:b_s3]
# STEP 3
step3 = PA[a_s3:a_tail] + PB[b_s3 + 1:b_tail]
tail = PA[a_tail:]
tail[1] = tail[1].replace("6. 삼각함수의 그래프", "1. " + TITLE)

paras = step1 + step2 + step3 + tail
# 유형 번호 다시 매기기: B의 유형 상자 01~04 -> 04~07
n = 0
for i, p in enumerate(paras):
    t = io.text(p)
    if re.search(r"유형$", t) and re.match(r"\d\d", t):
        n += 1
        paras[i] = re.sub(r"(<hp:t>)(\d\d)(</hp:t>)", lambda m: m.group(1) + "%02d" % n + m.group(3), p, count=1)
print("유형", n)
# 설명 문단의 오타
paras = plain.rewrite(paras, plain.TABLE1, fixes.Doc(paras))
# 5지선다 -> 단답형 (003 간단히 하기, 024 삼각형 모양은 5지선다 유지)
paras, slog = shortans.convert(paras, fixes.Doc(paras), keep=(3, 24))
print("단답형", sum(1 for l in slog if l[1] == "단답형"), [l for l in slog if l[1] != "단답형"])
# 문항 번호: 대표문제 상자가 없는 번호 문단을 본보기로
tmpl = next(p for p in paras if nb.num_text(p) and "<hp:container" not in p)
paras, nprob, nins = nb.renumber(paras, tmpl)
paras = nb.note_start(paras, 1)    # 두 파일을 합쳐 뒤섞인 해설 번호를 1부터 차례로
print("문항", nprob, "번호 새로 넣음", nins)

sec = headA + "".join(paras) + tailA
fa["Contents/section0.xml"] = sec.encode("utf-8")
fa["Contents/header.xml"] = M.hA.encode("utf-8")
for mp in ("Contents/masterpage0.xml", "Contents/masterpage1.xml"):
    x = fa[mp].decode("utf-8")
    x = x.replace("<hp:t>다항식의 연산</hp:t>", "<hp:t>1. " + TITLE + "</hp:t>")
    fa[mp] = x.encode("utf-8")
io.write(OUT, fa, oa)
print("문단", len(paras), "->", OUT)
