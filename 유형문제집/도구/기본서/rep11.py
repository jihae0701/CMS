# -*- coding: utf-8 -*-
"""기본서 11단원 단원 마무리의 대진표 문항(족구 대회, 5040)을 체험 프로그램 분배 문항으로 바꾸기 — 사용자 요청(2026-10-25)

python rep11.py <입력.hwpx> <출력.hwpx>
- 새 문항은 고등수매씽 서술형 1951(7명, 3개 프로그램, 최대 4명)을 숫자·조건을 바꿔 만듦: 6명, 4개 프로그램, 최대 2명 → 1080
- 모양은 add11.py와 같이 STEP 3의 '네 자리 자연수 중 3의 배수' 문항(번호 문단 + 문제 한 문단 + 빈 문단)을 본으로 쓴다
"""
import sys, re, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hwpxio as io, fixes, eqsize

SRC, OUT = sys.argv[1:3]
EN = re.compile(r"<hp:endNote .*?</hp:endNote>", re.S)
NUMP = {"43", "45", "46"}
NEW = {"q": "$6$명의 학생이 $4$개의 체험 프로그램 $rm A$, $rm B$, $rm C$, $rm D$ 중에서 한 개씩 선택하여 체험하려고 한다. "
            "한 명도 선택하지 않는 프로그램은 없고, 각 프로그램은 최대 $2$명까지 선택할 수 있을 때, "
            "$6$명이 프로그램을 선택하는 경우의 수를 구하시오.",
       "ans": "󰂼 $1080$",
       "sol": ["한 명도 선택하지 않는 프로그램이 없고 각 프로그램은 최대 $2$명까지 선택할 수 있으므로 "
               "$6$명을 $2$명, $2$명, $1$명, $1$명의 $4$개의 조로 나누어 $4$개의 프로그램에 배정하면 된다.",
               "$6$명을 $2$명, $2$명, $1$명, $1$명으로 나누는 경우의 수는 "
               "${}_{6} rm C _{2} times {}_{4} rm C _{2} times {1} over {2!} times {}_{2} rm C _{1} times {}_{1} rm C _{1} "
               "times {1} over {2!} =45$",
               "$4$개의 조를 $4$개의 프로그램에 배정하는 경우의 수는 $4!=24$",
               "따라서 구하는 경우의 수는 $45 times 24=1080$"]}
BLANKS = 18

f, o = io.read(SRC)
head, T, tail = io.split(f["Contents/section0.xml"].decode("utf-8"))
T = [io.nolines(p) for p in T]
eqsize.ensure(fixes.scripts_of([NEW["q"], NEW["ans"]] + NEW["sol"]))


def pid(p):
    return re.search(r'paraPrIDRef="(\d+)"', p).group(1)


i_s3 = next(i for i, p in enumerate(T) if "단원 마무리 하기" in io.text(p))
nums = [i for i, p in enumerate(T) if pid(p) in NUMP]
old = [i for i in nums if i > i_s3 and "족구 대회" in io.text(EN.sub("", T[i + 1]))]
assert len(old) == 1
a = old[0]
b = next(k for k in nums if k > a)

ti = next(i for i in nums if i > i_s3 and "네 자리 자연수 중" in io.text(EN.sub("", T[i + 1])) and "의 배수" in io.text(T[i + 1]))
num_p, q_p = T[ti], T[ti + 1]
q_open = re.match(r"<hp:p [^>]*>", q_p).group(0)
run_cp = re.search(r'<hp:run charPrIDRef="(\d+)">', q_p).group(1)
ctrl_cp = re.search(r'<hp:run charPrIDRef="(\d+)">(?:(?!</hp:run>).)*?<hp:ctrl><hp:endNote ', q_p, re.S).group(1)
en0 = EN.search(q_p).group(0)
blank = next(p for p in T[ti + 2:ti + 6] if not io.text(p).strip() and "<hp:tbl" not in p)
doc = fixes.Doc(T)
qdoc = fixes.Doc(T)
qeq = re.search(r"<hp:equation [^>]*>", q_p).group(0)
qdoc.eq_open = re.sub(r'\bid="\d+"', 'id="0"', re.sub(r'zOrder="\d+"', 'zOrder="0"', qeq))
qdoc.base = int(re.search(r'baseUnit="(\d+)"', qeq).group(1))
_id = [1998000000]


def nid():
    _id[0] += 1
    return _id[0]


en = doc.endnote_body(en0, [NEW["ans"]] + NEW["sol"])
q = ('%s<hp:run charPrIDRef="%s">%s</hp:run><hp:run charPrIDRef="%s"><hp:ctrl>%s</hp:ctrl><hp:t/></hp:run></hp:p>'
     % (q_open, run_cp, qdoc.inline(NEW["q"]), ctrl_cp, en))
q = re.sub(r'(<hp:equation id=")\d+(")', lambda m: m.group(1) + str(nid()) + m.group(2), q)
T = T[:a] + [num_p, q] + [blank] * BLANKS + T[b:]

n = [0]


def renum(p):
    def num(m):
        n[0] += 1
        return m.group(1) + str(n[0]) + m.group(2)
    p = re.sub(r'(<hp:endNote number=")\d+(")', lambda m: m.group(1) + str(n[0] + 1) + m.group(2), p)
    return re.sub(r'(<hp:autoNum num=")\d+(" numType="ENDNOTE")', num, p)


T = [renum(p) for p in T]
print("문항(자동 번호 문단)", sum(1 for p in T if pid(p) in NUMP), "미주", sum(p.count("<hp:endNote ") for p in T))
f["Contents/section0.xml"] = (head + "".join(T) + tail).encode("utf-8")
io.write(OUT, f, o)
print("->", OUT)
