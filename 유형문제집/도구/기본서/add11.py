# -*- coding: utf-8 -*-
"""기본서 11단원(사용자 완성본) 단원 마무리에 6문항 넣기 — 사용자 요청(2026-10-25): 34 → 40문항

python add11.py <입력.hwpx> <출력.hwpx>
- 고등수매씽 유형(조합의 성질과 이차방정식, 대각선의 교점, 평행사변형의 개수, 크기가 엇갈리는 네 자리 수,
  꼭짓점에서 그은 선분으로 만든 삼각형, 조건이 있는 조 나누기)을 숫자를 바꿔 새로 만듦
- 문항 번호는 문단 자동 번호(번호 정의 4, start 403)라 번호 문단(45)만 복제하면 번호가 이어진다
- 모양은 STEP 3의 425번(번호 문단 + 문제 한 문단 + 빈 문단)을 본으로 쓴다
"""
import sys, re, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hwpxio as io, fixes, eqsize

SRC, OUT = sys.argv[1:3]
EN = re.compile(r"<hp:endNote .*?</hp:endNote>", re.S)
NUMP = {"43", "45", "46"}          # 자동 번호 문단(대표문제 43·46, 보통 45)

NEW = {
    "A": {"q": "$x$에 대한 이차방정식 ${}_{n} rm C _{3} x^{2}-{}_{n} rm C _{4} x+{}_{n} rm C _{5} =0$의 두 근을 "
               "$alpha$, $beta$라 하자. $alpha beta =1$일 때, $alpha + beta$의 값을 구하시오. (단, $n geq 5$)",
          "ans": "󰂼 ${5} over {4}$",
          "sol": ["이차방정식의 근과 계수의 관계에 의하여 $alpha + beta ={{}_{n} rm C _{4}} over {{}_{n} rm C _{3}}$, "
                  "$alpha beta ={{}_{n} rm C _{5}} over {{}_{n} rm C _{3}}$",
                  "$alpha beta =1$이므로 ${}_{n} rm C _{5} ={}_{n} rm C _{3}$",
                  "${}_{n} rm C _{r} ={}_{n} rm C _{n-r}$이고 $5 ne 3$이므로 $n=5+3=8$",
                  "$therefore$ $alpha + beta ={{}_{8} rm C _{4}} over {{}_{8} rm C _{3}} ={70} over {56} ={5} over {4}$"]},
    "B": {"q": "볼록 $n$각형의 대각선 중 어느 세 대각선도 다각형의 내부의 한 점에서 만나지 않는다. "
               "대각선끼리 다각형의 내부에서 만나는 점의 개수가 $70$일 때, 이 다각형의 대각선의 개수를 구하시오.",
          "ans": "󰂼 $20$",
          "sol": ["다각형의 네 꼭짓점을 택하면 이 네 점을 꼭짓점으로 하는 사각형의 두 대각선이 다각형의 내부에서 한 번 만난다.",
                  "어느 세 대각선도 한 점에서 만나지 않으므로 교점 하나에 네 꼭짓점이 하나씩 대응하고, "
                  "교점의 개수는 ${}_{n} rm C _{4}$이다.",
                  "${}_{n} rm C _{4} =70$에서 $n=8$",
                  "따라서 팔각형의 대각선의 개수는 ${}_{8} rm C _{2} -8=28-8=20$"]},
    "C": {"q": "한 평면 위에 방향이 서로 다른 세 종류의 평행선이 각각 $5$개, $4$개, $3$개 있다. "
               "어느 세 직선도 한 점에서 만나지 않을 때, 이 $12$개의 직선으로 만들어지는 평행사변형의 개수를 구하시오.",
          "ans": "󰂼 $108$",
          "sol": ["평행사변형은 방향이 다른 두 종류의 평행선에서 각각 $2$개씩 택하면 하나 만들어진다.",
                  "(ⅰ) $5$개, $4$개인 평행선에서 택할 때 ${}_{5} rm C _{2} times {}_{4} rm C _{2} =10 times 6=60$",
                  "(ⅱ) $5$개, $3$개인 평행선에서 택할 때 ${}_{5} rm C _{2} times {}_{3} rm C _{2} =10 times 3=30$",
                  "(ⅲ) $4$개, $3$개인 평행선에서 택할 때 ${}_{4} rm C _{2} times {}_{3} rm C _{2} =6 times 3=18$",
                  "따라서 구하는 평행사변형의 개수는 $60+30+18=108$"]},
    "D": {"q": "$0$ 이상 $9$ 이하의 서로 다른 네 정수 $a$, $b$, $c$, $d$에 대하여 천의 자리의 수, 백의 자리의 수, "
               "십의 자리의 수, 일의 자리의 수가 각각 $a$, $b$, $c$, $d$인 네 자리 자연수 중 "
               "$a>b$, $b<c$, $c>d$를 만족시키는 자연수의 개수를 구하시오.",
          "ans": "󰂼 $1050$",
          "sol": ["$a>b$이므로 $a ne 0$이다. 서로 다른 네 수를 먼저 택한 다음 조건에 맞게 놓는 방법의 수를 센다.",
                  "택한 네 수를 $p<q<r<s$라 하면 $a>b$, $c>d$이므로 가장 작은 수 $p$는 $b$ 또는 $d$ 자리에 온다.",
                  "(ⅰ) $b=p$일 때 $a$를 정하는 방법은 $3$가지이고, 남은 두 수는 $c>d$가 되도록 한 가지로 놓이므로 $3$가지",
                  "(ⅱ) $d=p$일 때 $a>b$, $c>b$이므로 $b=q$이고, $a$, $c$에 $r$, $s$를 놓는 방법은 $2$가지",
                  "즉 택한 네 수마다 $3+2=5$가지씩이므로 구하는 개수는 ${}_{10} rm C _{4} times 5=210 times 5=1050$"]},
    "E": {"q": "삼각형 $rm ABC$의 변 $rm BC$ 위에 두 점 $rm B$, $rm C$가 아닌 서로 다른 $5$개의 점을 잡아 "
               "꼭짓점 $rm A$와 각각 선분으로 이었다. 또, 변 $rm AB$와 변 $rm AC$ 위의 점을 이어 "
               "변 $rm BC$와 평행한 선분 $2$개를 그었다. 이 도형의 선분들로 만들 수 있는 삼각형의 개수를 구하시오.",
          "ans": "󰂼 $63$",
          "sol": ["점 $rm A$를 지나는 선분은 변 $rm AB$, $rm AC$와 새로 그은 $5$개를 합하여 $7$개이고, "
                  "변 $rm BC$와 평행한 선분은 변 $rm BC$를 포함하여 $3$개이다.",
                  "평행한 두 선분은 한 삼각형의 두 변이 될 수 없고, 점 $rm A$를 지나는 세 선분으로는 삼각형을 만들 수 없으므로 "
                  "삼각형은 점 $rm A$를 지나는 선분 $2$개와 변 $rm BC$에 평행한 선분 $1$개로 만들어진다.",
                  "따라서 구하는 삼각형의 개수는 ${}_{7} rm C _{2} times {}_{3} rm C _{1} =21 times 3=63$"]},
    "F": {"q": "어른 $7$명과 어린이 $3$명을 $5$명씩 두 조로 나눌 때, 각 조에 적어도 한 명의 어린이가 포함되도록 "
               "나누는 경우의 수를 구하시오.",
          "ans": "󰂼 $105$",
          "sol": ["$10$명을 $5$명, $5$명의 두 조로 나누는 경우의 수는 "
                  "${}_{10} rm C _{5} times {}_{5} rm C _{5} times {1} over {2!} =252 times 1 times {1} over {2} =126$",
                  "어린이가 한 명도 없는 조가 생기는 경우는 어른 $7$명 중 $5$명을 택하여 한 조로 만드는 경우이므로 "
                  "${}_{7} rm C _{5} =21$",
                  "따라서 구하는 경우의 수는 $126-21=105$"]},
}
# 넣을 자리: 문제 글에 이 말이 든 STEP 3 문항 뒤
AFTER = [("조합의 수에 관한 등식", ["A"]),               # 조합의 수에 관한 등식 설명 뒤에 조합의 성질
         ("네 자리 자연수 중", ["D"]),                   # 네 자리 3의 배수 뒤
         ("서로 다른 종류의 인형", ["F"]),               # 분배 뒤에 조 나누기
         ("정사면체", ["B", "C", "E"])]                  # 도형의 개수 뒤
BLANKS = 18

f, o = io.read(SRC)
head, T, tail = io.split(f["Contents/section0.xml"].decode("utf-8"))
T = [io.nolines(p) for p in T]
eqsize.ensure(fixes.scripts_of([x for it in NEW.values() for x in [it["q"], it["ans"]] + it["sol"]]))


def pid(p):
    return re.search(r'paraPrIDRef="(\d+)"', p).group(1)


i_s3 = next(i for i, p in enumerate(T) if "단원 마무리 하기" in io.text(p))
nums = [i for i, p in enumerate(T) if pid(p) in NUMP]


def block(i):
    j = next((k for k in nums if k > i), None)
    if j is None:                                   # 마지막 문항: 단원 이름 상자 앞까지
        j = next(k for k in range(i + 1, len(T)) if 'pageBreak="1"' in T[k][:200])
    return i, j


def find(key):
    hit = [i for i in nums if i > i_s3 and key in io.text(EN.sub("", T[i + 1]))]
    assert len(hit) == 1, (key, hit)
    return hit[0]


# 본보기: STEP 3의 '6개의 숫자 … 3의 배수' 문항
ti = next(i for i in nums if i > i_s3 and "의 배수" in io.text(EN.sub("", T[i + 1])) and "네 자리" in io.text(T[i + 1]))
num_p, q_p = T[ti], T[ti + 1]
q_open = re.match(r"<hp:p [^>]*>", q_p).group(0)
run_cp = re.search(r'<hp:run charPrIDRef="(\d+)">', q_p).group(1)
m = re.search(r'<hp:run charPrIDRef="(\d+)">(?:(?!</hp:run>).)*?<hp:ctrl><hp:endNote ', q_p, re.S)
ctrl_cp = m.group(1)
en0 = EN.search(q_p).group(0)
blank = next(p for p in T[ti + 2:ti + 6] if not io.text(p).strip() and "<hp:" in p and "<hp:tbl" not in p)
doc = fixes.Doc(T)
qdoc = fixes.Doc(T)
qeq = re.search(r"<hp:equation [^>]*>", q_p).group(0)
qdoc.eq_open = re.sub(r'\bid="\d+"', 'id="0"', re.sub(r'zOrder="\d+"', 'zOrder="0"', qeq))
qdoc.base = int(re.search(r'baseUnit="(\d+)"', qeq).group(1))
_id = [1997000000]


def nid():
    _id[0] += 1
    return _id[0]


def make(key):
    it = NEW[key]
    en = doc.endnote_body(en0, [it["ans"]] + it["sol"])
    q = ('%s<hp:run charPrIDRef="%s">%s</hp:run><hp:run charPrIDRef="%s"><hp:ctrl>%s</hp:ctrl><hp:t/></hp:run></hp:p>'
         % (q_open, run_cp, qdoc.inline(it["q"]), ctrl_cp, en))
    q = re.sub(r'(<hp:equation id=")\d+(")', lambda m: m.group(1) + str(nid()) + m.group(2), q)
    return [num_p, q] + [blank] * BLANKS


ins = {}
for start, keys in AFTER:
    i, j = block(find(start))
    ins[j] = [p for k in keys for p in make(k)]
out = []
for i, p in enumerate(T):
    if i in ins:
        out += ins[i]
    out.append(p)
T = out

# 미주 번호(구역 안 차례)를 처음부터 다시
n = [0]


def renum(p):
    def num(m):
        n[0] += 1
        return m.group(1) + str(n[0]) + m.group(2)
    p = re.sub(r'(<hp:endNote number=")\d+(")', lambda m: m.group(1) + str(n[0] + 1) + m.group(2), p)
    return re.sub(r'(<hp:autoNum num=")\d+(" numType="ENDNOTE")', num, p)


T = [renum(p) for p in T]
nn = sum(1 for p in T if pid(p) in NUMP)
ne = sum(p.count("<hp:endNote ") for p in T)
print("문항(자동 번호 문단)", nn, "미주", ne)
f["Contents/section0.xml"] = (head + "".join(T) + tail).encode("utf-8")
io.write(OUT, f, o)
print("->", OUT)
