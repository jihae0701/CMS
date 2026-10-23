# -*- coding: utf-8 -*-
"""기본서 6단원 사용자 완성본(2026-10-23) 고치기 — 사용자 요청(2026-10-23)

python fix6u.py <입력.hwpx> <출력.hwpx>
- 213번: 출처 수식 지움, '…가 오직 하나의 실근을 갖도록 하는 양수 k의 값을 모두 구하시오.'로 바꾸고
  정답 0<k<9 또는 k=16, 해설 끝을 그래프로 실근 개수 따지기로 바꿈, (ㄴ) −7t²+10t → −7t²+20t
- 240번(조건을 모두 만족시키는 f가 없음) 삭제
- 202번 미주 새로 만듦(답 34), 해설 없던 206·207·238(첫째)·241번 해설 씀
- 216번 번호 문단이 둘(보통 번호 + 대표문제 번호)이라 보통 번호 문단을 지움
- 문항 번호를 미주 순서대로 201부터 다시 매기고 미주 번호도 맞춤
"""
import sys, re, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hwpxio as io, numbering as nb, fixes, eqsize

SRC, OUT = sys.argv[1:3]
START = 201
EN = re.compile(r"<hp:endNote .*?</hp:endNote>", re.S)
PARA = re.compile(r"<hp:p [^>]*>.*?</hp:p>", re.S)

f, o = io.read(SRC)
head, T, tail = io.split(f["Contents/section0.xml"].decode("utf-8"))
T = [io.nolines(p) for p in T]


def nums(n):
    return [i for i, p in enumerate(T) if nb.num_text(p) == n]


def en_after(i):
    return next(k for k in range(i + 1, len(T)) if "<hp:endNote " in T[k])


SOL = {
    "202": ["󰂼 $34$",
            "(가)에서 $2 leq x leq 10$일 때 $f(x)=(x-a)^{2}$의 최솟값이 $0$이므로 $2 leq a leq 10$",
            "(ⅰ) $2 leq a leq 4$일 때 $2 leq x leq 6$에서 최댓값은 $f(6)=(6-a)^{2}$, "
            "$6 leq x leq 10$에서 최솟값은 $f(6)=(6-a)^{2}$이므로 (나)를 만족시킨다.",
            "(ⅱ) $4<a<6$일 때 $2 leq x leq 6$에서 최댓값은 $f(2)=(a-2)^{2}$, "
            "$6 leq x leq 10$에서 최솟값은 $f(6)=(6-a)^{2}$이고 $(a-2)^{2}>(6-a)^{2}$이므로 (나)를 만족시키지 않는다.",
            "(ⅲ) $6 leq a leq 10$일 때 $6 leq x leq 10$에서 최솟값은 $f(a)=0$이고 "
            "$2 leq x leq 6$에서 최댓값은 $f(2)=(a-2)^{2}>0$이므로 (나)를 만족시키지 않는다.",
            "따라서 $2 leq a leq 4$이고 $f(-1)=(a+1)^{2}$이므로",
            "$a=4$일 때 최댓값 $M=25$, $a=2$일 때 최솟값 $m=9$",
            "$therefore$ $M+m=34$"],
    "206": ["󰂼 $5$",
            "(가)에서 $0 leq x leq 8$일 때 $f(x)= it-(x-a)^{2}$의 최댓값이 $0$이므로 $0 leq a leq 8$",
            "(ⅰ) $0 leq a leq 2$일 때 $0 leq x leq 2$에서 최댓값은 $f(a)=0$, "
            "$2 leq x leq 8$에서 최솟값은 $f(8)= it-(8-a)^{2}<0$이므로 (나)를 만족시킨다.",
            "(ⅱ) $2<a leq 8$일 때 $0 leq x leq 2$에서 최댓값은 $f(2)= it-(a-2)^{2}$이고, "
            "$2 leq x leq 8$에서 최솟값은 $f(2)$, $f(8)$ 중 작은 값이다.",
            "(나)를 만족시키려면 $f(8)<f(2)$, 즉 $(8-a)^{2}>(a-2)^{2}$",
            "$60-12a>0$에서 $a<5$이므로 $2<a<5$",
            "(ⅰ), (ⅱ)에서 $0 leq a<5$이므로 정수 $a$는 $0$, $1$, $2$, $3$, $4$의 $5$개이다."],
    "207": ["󰂼 $1$",
            "$f(x)=t$로 놓으면 $g(x)=t^{2}-4t=(t-2)^{2}-4$",
            "$-4 leq x<0$에서 $f(x)= it-(x+1)^{2}+6$이므로 $-3 leq f(x) leq 6$",
            "$0 leq x leq 4$에서 $f(x)=(x-2)^{2}+1$이므로 $1 leq f(x) leq 5$",
            "즉 $-3 leq t leq 6$이고 $t=2$가 이 범위에 속하므로 $g(x)$는 $f(x)=2$일 때 최솟값 $-4$를 갖는다.",
            "$x<0$일 때 $-(x+1)^{2}+6=2$에서 $(x+1)^{2}=4$이므로 $x= it-3$",
            "$x geq 0$일 때 $(x-2)^{2}+1=2$에서 $(x-2)^{2}=1$이므로 $x=1$ 또는 $x=3$",
            "따라서 모든 $alpha$의 값의 합은 $-3+1+3=1$"],
    "238": ["󰂼 $13$",
            "$y=(x-2a)^{2}+b$이므로 그래프의 축은 직선 $x=2a$이다.",
            "(ⅰ) $2a<2$, 즉 $a<1$일 때 최솟값은 $x=2$에서 $(2-2a)^{2}+b=4$이므로 $b=4-4(a-1)^{2}$",
            "$4a+b= it-4a^{2}+12a= it-4 left ( a-{3} over {2} right )^{2}+9$이고 $a<1$이므로 $4a+b<8$",
            "(ⅱ) $2 leq 2a leq 4$, 즉 $1 leq a leq 2$일 때 최솟값은 $x=2a$에서 $b=4$이므로 $4a+b=4a+4 leq 12$",
            "(ⅲ) $2a>4$, 즉 $a>2$일 때 최솟값은 $x=4$에서 $(4-2a)^{2}+b=4$이므로 $b=4-4(a-2)^{2}$",
            "$4a+b= it-4a^{2}+20a-12= it-4 left ( a-{5} over {2} right )^{2}+13$이므로 "
            "$a={5} over {2}$일 때 최댓값 $13$",
            "따라서 $M=13$"],
    "241": ["󰂼 $5$",
            "$h(x)=5x^{2}-2tx=5 left ( x-{t} over {5} right )^{2}-{t^{2}} over {5}$라 하면 "
            "$f(x)=|h(x)|$이고 $h(0)=0$, $h(1)=5-2t$",
            "(ⅰ) $t geq 5$일 때 $0 leq x leq 1$에서 $h(x) leq 0$이고 $h(x)$는 감소하므로 $g(t)=|h(1)|=2t-5 geq 5$",
            "(ⅱ) $0<t<5$일 때 꼭짓점의 $x$좌표 ${t} over {5}$가 $0$과 $1$ 사이에 있으므로 "
            "$g(t)$는 ${t^{2}} over {5}$와 $|5-2t|$ 중 작지 않은 값이다.",
            "$t geq {5} over {2}$이면 ${t^{2}} over {5}-(2t-5)={(t-5)^{2}} over {5} geq 0$이므로 "
            "$g(t)={t^{2}} over {5} geq {5} over {4}$",
            "$0<t<{5} over {2}$이면 ${t^{2}} over {5}=5-2t$에서 $t^{2}+10t-25=0$, $t= it-5+5 sqrt {2}$이므로",
            "$0<t leq -5+5 sqrt {2}$일 때 $g(t)=5-2t$, $-5+5 sqrt {2}<t<{5} over {2}$일 때 $g(t)={t^{2}} over {5}$",
            "따라서 $g(t)$는 $t= it-5+5 sqrt {2}$일 때 최솟값 $5-2(-5+5 sqrt {2})=15-10 sqrt {2}$를 갖는다.",
            "$a=15$, $b= it-10$이므로 $a+b=5$"],
}
END213 = ["따라서 $g(t)$는 $0 leq t leq 1$에서 증가하고 $t geq 1$에서 감소하며 $g(0)=9$, $g(1)=16$이다.",
          "방정식 $g(t)=k$의 실근은 직선 $y=k$와 함수 $y=g(t)$의 그래프의 교점의 $t$좌표이므로 "
          "오직 하나의 실근을 가지려면 $k=16$ 또는 $k<9$",
          "$k$는 양수이므로 $0<k<9$ 또는 $k=16$"]
ANS213 = "$0<k<9$ 또는 $k=16$"

eqsize.ensure(fixes.scripts_of([l for ls in SOL.values() for l in ls] + END213 + [ANS213, "$t GEQ 0$", "$= it -7t ^{2} +20t$"]))
doc = fixes.Doc(T)
_inst = [1996000000]


def new_inst(en):
    _inst[0] += 7
    return re.sub(r'instId="\d+"', 'instId="%d"' % _inst[0], en, count=1)


# ---- 206·207·238(첫째)·241: 해설 쓰기 (미주를 새 본문으로)
for n, k in (("206", 0), ("207", 0), ("238", 0), ("241", 0)):
    i = en_after(nums(n)[k])
    p = T[i]
    old = EN.search(p).group(0)
    assert len(PARA.findall(old)) <= 2, (n, "해설이 이미 있음")
    T[i] = p.replace(old, doc.endnote_body(old, SOL[n]), 1)

# ---- 202: 미주가 없음 → 201번의 미주를 본으로 새로 만들어 첫 문제 문단 끝에 붙임
i201 = en_after(nums("201")[0])
m = re.search(r'<hp:run charPrIDRef="(\d+)">(?:(?!</hp:run>).)*?<hp:ctrl><hp:endNote ', T[i201], re.S)
ctrl_cp = m.group(1)
en0 = EN.search(T[i201]).group(0)
i202 = nums("202")[0]
assert "<hp:endNote " not in T[i202 + 1]
en202 = new_inst(doc.endnote_body(en0, SOL["202"]))
p = T[i202 + 1]
T[i202 + 1] = p[:p.rindex("</hp:p>")] + '<hp:run charPrIDRef="%s"><hp:ctrl>%s</hp:ctrl><hp:t/></hp:run></hp:p>' % (ctrl_cp, en202)

# ---- 213: 문제 글과 해설
i = next(k for k, p in enumerate(T) if "from^2021" in p)
p = T[i]
old = EN.search(p).group(0)
body_a, body_b = p[:p.index(old)], p[p.index(old) + len(old):]
x = body_a + "\0" + body_b
x, c1 = fixes._replace_in(x, "${t GEQ 0}{{from^2021^9 고1인천^중}}$", "$t GEQ 0$", doc, mode="exact")
x, c2 = fixes._replace_in(x, "의 오직 하나의 실근을 가질 때, 양수 ", "가 오직 하나의 실근을 갖도록 하는 양수 ", doc)
x, c3 = fixes._replace_in(x, "의 값을 구하시오.", "의 값을 모두 구하시오.", doc)
assert (c1, c2, c3) == (1, 1, 1), (c1, c2, c3)
ps = PARA.findall(old)
# 정답 줄: 첫 수식을 '0<k<9 또는 k=16'으로
a0 = ps[0]
eqm = re.search(r"<hp:equation .*?</hp:equation>", a0, re.S)
a1 = a0[:eqm.start()] + doc.inline(ANS213) + a0[eqm.end():]
# (ㄴ) 줄: −7t²+10t → −7t²+20t
b_i = next(k for k, q in enumerate(ps) if "(ㄴ)" in io.text(q))
b1, cb = fixes._replace_in(ps[b_i], "$-7t ^{2} +10t$", "$-7t ^{2} +20t$", doc, mode="sub")
assert cb == 1
# 끝 줄: 그래프로 실근 개수 따지기
e_i = next(k for k, q in enumerate(ps) if "최댓값은" in io.text(q) and "따라서 함수" in io.text(q))
lh, lc = doc.line
e1 = "".join('%s<hp:run charPrIDRef="%s">%s</hp:run></hp:p>' % (lh, lc, doc.inline(l)) for l in END213)
new = old.replace(a0, a1, 1).replace(ps[b_i], b1, 1).replace(ps[e_i], e1, 1)
a, b = x.split("\0")
T[i] = a + new + b

# ---- 216: 번호 문단 둘 중 보통 번호 문단을 지움(대표문제 번호를 남김)
d = nums("216")
assert len(d) == 2 and d[1] == d[0] + 1 and 'paraPrIDRef="40"' in T[d[1]]   # 40 = 대표문제 번호 문단
del T[d[0]]

# ---- 240 삭제: 번호 문단부터 241번 번호 문단 앞까지
a, b = nums("240")[0], nums("241")[0]
assert "f LEFT ( 8 RIGHT )" in "".join(T[a:b])
del T[a:b]

# ---- 번호: 미주 순서대로 201부터, 미주 번호도 맞춤
segs = nb.segments(T)
for k, (a, e) in enumerate(segs, START):
    assert nb.num_text(T[a]) not in (None, ""), (k, io.text(T[a])[:40])
    T[a] = re.sub(r"<hp:t>\d{3}(\s*)</hp:t>", lambda m: "<hp:t>%d%s</hp:t>" % (k, m.group(1)), T[a], count=1)
T = nb.note_start(T, START)
print("문항", len(segs), "→ %d~%d" % (START, START + len(segs) - 1))

f["Contents/section0.xml"] = (head + "".join(T) + tail).encode("utf-8")
io.write(OUT, f, o)
print("->", OUT)
