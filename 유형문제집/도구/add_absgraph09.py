# -*- coding: utf-8 -*-
"""공통수학2 기본서 9단원(함수) 사용자 수정본에 '절댓값 기호를 포함한 식의 그래프' 유형을 넣는다(2026-11-14 사용자 요청).
python add_absgraph09.py <입력.hwpx> <출력.hwpx>
- STEP 1 '함수'에 ⑸ 절댓값 기호를 포함한 식의 그래프(참고 4줄)를 넣고, 아래 빈 줄 6개를 줄여 쪽 배치를 지킨다.
- STEP 2 '04 함수의 대칭성과 주기' 다음에 새 05 유형(대표문제 1 + 2문항, 미주 풀이). 04 유형의 틀(머리 상자·대표문제 상자·빈 줄)을 그대로 본뜬다.
- 뒤 유형 번호 05→06, 06→07(08·09는 그대로 맞게 된다).
- 숫자를 직접 쓴 문항 번호 문단 6곳을 자동 번호 문단(다른 문항과 같은 paraPr 19)으로 바꾸고, 미주 번호를 312부터 다시 매긴다.
"""
import sys, re, zipfile
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from lite import top_paras, Builder, esc

src, out = sys.argv[1:3]
z = zipfile.ZipFile(src)
items = [(i, z.read(i.filename)) for i in z.infolist()]
s = z.read("Contents/section0.xml").decode()
P = top_paras(s, 0, len(s))
T = lambda i: s[P[i][0]:P[i][1]]


def find(pred):
    return [i for i in range(len(P)) if pred(T(i))]


def txt(p):
    p = re.sub(r"<hp:endNote.*?</hp:endNote>", "", p, flags=re.S)
    return "".join(re.sub(r"<[^>]+>", "", m) for m in re.findall(r"<hp:t>(.*?)</hp:t>", p, re.S))


H04 = find(lambda p: re.sub(r"\s", "", txt(p)).startswith("04함수의대칭성과주기"))[0]
H05 = find(lambda p: re.sub(r"\s", "", txt(p)).startswith("05일대일함수"))[0]
H06 = find(lambda p: re.sub(r"\s", "", txt(p)).startswith("06항등함수"))[0]
G4 = find(lambda p: "⑷ 함수의 그래프" in txt(p))[0]
assert txt(T(H04 + 1)).strip() == "대표문제"
NUMP = T(H04 + 45 + 1) if False else None
# 본뜰 문단
num_para = [T(i) for i in range(H04, H05) if 'paraPrIDRef="19"' in T(i)[:200] and "<hp:rect" not in T(i)][0]
blank9 = [T(i) for i in range(H04, H05) if 'paraPrIDRef="9"' in T(i)[:200] and not txt(T(i)).strip()][0]
blank37 = next(T(i) for i in range(len(P)) if 'paraPrIDRef="37" styleIDRef="16"' in T(i)[:200] and len(T(i)) < 400)
qtpl = T(H04 + 2)                       # 대표문제 문항 문단(미주 포함)
en_tpl = re.search(r"<hp:endNote .*?</hp:endNote>", qtpl, re.S).group(0)
ans_head = re.search(r"(<hp:p [^>]*><hp:run charPrIDRef=\"\d+\"><hp:ctrl><hp:autoNum .*?</hp:ctrl><hp:t>)([^<]*)(</hp:t>)", en_tpl, re.S)
sol_pp = re.search(r'<hp:p [^>]*paraPrIDRef="(\d+)"[^>]*><hp:run charPrIDRef="(\d+)">', en_tpl[ans_head.end():]).groups()

OFF = [0]


def bump(x, add):
    x = re.sub(r'\b(id)="(1996\d{6})"', lambda m: '%s="%d"' % (m.group(1), int(m.group(2)) + add), x)
    x = re.sub(r'\b(instid)="(996\d{6})"', lambda m: '%s="%d"' % (m.group(1), int(m.group(2)) + add), x)
    return x


B = Builder(s)
Q = [
    ("함수 $y= LEFT | x+2 RIGHT | + LEFT | x-3 RIGHT |$의 그래프와 직선 $y=k$로 둘러싸인 부분의 넓이가 $12$일 때, 상수 $k$의 값을 구하시오.",
     "7",
     ["$x<-2$일 때 $y= it-2x+1$, $-2 leq x<3$일 때 $y=5$, $x geq 3$일 때 $y=2x-1$",
      "둘러싸인 부분이 있으려면 $k>5$이고, 직선 $y=k$와 만나는 두 점의 $x$좌표는 ${1-k} over {2}$, ${k+1} over {2}$이다.",
      "둘러싸인 부분은 윗변의 길이가 $k$, 아랫변의 길이가 $5$, 높이가 $k-5$인 사다리꼴이므로 넓이는",
      "${1} over {2} (k+5)(k-5)= {k^{2} -25} over {2} =12$  $therefore$ $k^{2} =49$",
      "$k>5$이므로 $k=7$"]),
    ("함수 $y= LEFT | x^{2} -4x RIGHT |$의 그래프와 직선 $y=k$가 서로 다른 네 점에서 만나도록 하는 정수 $k$의 개수를 구하시오.",
     "3",
     ["$y= LEFT | x^{2} -4x RIGHT |$의 그래프는 $y=x^{2} -4x=(x-2)^{2} -4$의 그래프에서 $x$축 아랫부분 $(0<x<4)$을 $x$축 위로 접어 올린 것이다.",
      "접어 올린 부분의 꼭짓점이 $(2,~4)$이므로 직선 $y=k$와 서로 다른 네 점에서 만나려면 $0<k<4$",
      "따라서 정수 $k$는 $1$, $2$, $3$의 $3$개"]),
    ("함수 $y=x^{2} -4 LEFT | x RIGHT | +3$의 그래프와 직선 $y=k$가 서로 다른 네 점에서 만날 때, 실수 $k$의 값의 범위는 $a<k<b$이다. $b-a$의 값을 구하시오.",
     "4",
     ["$x geq 0$일 때 $y=x^{2} -4x+3=(x-2)^{2} -1$",
      "$y=f( LEFT | x RIGHT | )$ 꼴이므로 그래프는 $x geq 0$인 부분과 이를 $y$축에 대하여 대칭이동한 부분으로 이루어진다.",
      "꼭짓점은 $(2,~-1)$, $(-2,~-1)$이고 $x=0$일 때 $y=3$이므로 서로 다른 네 점에서 만나려면 $-1<k<3$",
      "$a= it-1$, $b=3$이므로 $b-a=4$"]),
]
CONCEPT = ["⑸ 절댓값 기호를 포함한 식의 그래프",
           "$y= LEFT | f(x) RIGHT |$ : $y=f(x)$의 그래프에서 $x$축 아랫부분을 $x$축 위로 접어 올린다.",
           "$y=f( LEFT | x RIGHT | )$ : $x geq 0$인 부분을 그리고, 이를 $y$축에 대하여 대칭이동한 부분을 더한다.",
           "$LEFT | y RIGHT | =f(x)$ : $y geq 0$인 부분을 그리고, 이를 $x$축에 대하여 대칭이동한 부분을 더한다.",
           "$y= LEFT | x-a RIGHT | + LEFT | x-b RIGHT |$ : 절댓값 안이 $0$이 되는 $x$의 값을 기준으로 구간을 나누어 그린다."]
for q, a, sol in Q:
    B.collect(q); B.collect("$" + a + "$"); [B.collect(x) for x in sol]
[B.collect(x) for x in CONCEPT]
B.sizes()


def inl(t):
    return B.inline(t)[:-len("<hp:t/>")]


def qpara(k, q, a, sol):
    en = en_tpl
    en = re.sub(r'instId="\d+"', 'instId="%d"' % (1996009100 + k), en, count=1)
    head = ans_head.group(1) + ans_head.group(2) + ans_head.group(3)
    ans_x = B.eq(a)
    sols = "".join('<hp:p id="2147483648" paraPrIDRef="%s" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0">'
                   '<hp:run charPrIDRef="%s">%s<hp:t/></hp:run></hp:p>' % (sol_pp[0], sol_pp[1], inl(x)) for x in sol)
    sub_open = re.match(r"<hp:endNote [^>]*><hp:subList [^>]*>", en).group(0)
    en_new = sub_open + head + ans_x + "<hp:t/></hp:run></hp:p>" + sols + "</hp:subList></hp:endNote>"
    p_open = re.match(r"<hp:p [^>]*><hp:run charPrIDRef=\"\d+\">", qtpl).group(0)
    return p_open + inl(q) + "<hp:ctrl>" + en_new + "</hp:ctrl><hp:t/></hp:run></hp:p>"


head_new = bump(T(H04), 700)
head_new = head_new.replace("<hp:t>04</hp:t>", "<hp:t>05</hp:t>").replace("<hp:t>함수의 대칭성과 주기</hp:t>", "<hp:t>절댓값 기호를 포함한 식의 그래프</hp:t>")
head_new = re.sub(r'pageBreak="1" columnBreak="0"', 'pageBreak="0" columnBreak="1"', head_new, count=1)
assert "절댓값" in head_new
rep_new = bump(T(H04 + 1), 720)
block = (head_new + rep_new + qpara(1, *Q[0]) + blank9 * 45 + num_para + qpara(2, *Q[1]) + blank37 * 16 + num_para + qpara(3, *Q[2]))

# STEP 1 개념 ⑸
g = T(G4)
c_open = re.match(r"<hp:p [^>]*><hp:run charPrIDRef=\"\d+\">", g).group(0)
lines = [inl(x) for x in CONCEPT]
concept = c_open + "<hp:t><hp:lineBreak/></hp:t>".join(lines) + "</hp:run></hp:p>"
blanks1 = [i for i in range(G4, H04) if 'paraPrIDRef="26" styleIDRef="15"' in T(i)[:200] and len(T(i)) < 400 and not txt(T(i)).strip()]
drop = set(blanks1[-7:-1])      # STEP 1 아래 빈 줄 6개를 줄인다(마지막 하나는 남김)

# 다시 조립
outp = []
for i in range(len(P)):
    p = T(i)
    if i in drop:
        continue
    if i == H05:
        p = p.replace("<hp:t>05</hp:t>", "<hp:t>06</hp:t>", 1)
    if i == H06:
        p = p.replace("<hp:t>06</hp:t>", "<hp:t>07</hp:t>", 1)
    if re.fullmatch(r"\s*\d{3}\s*", txt(p)) and "<hp:endNote" not in p and 'paraPrIDRef="27"' in p[:200]:
        p = num_para                     # 숫자를 직접 쓴 번호 → 자동 번호 문단
    outp.append(p)
    if i == G4:
        outp.append(concept)
    if i == H05 - 1:
        outp.append(block)
body = "".join(outp)
x = s[:P[0][0]] + body + s[P[-1][1]:]
# 미주 번호 다시 매기기
k = [311]


def ren(m):
    k[0] += 1
    e = m.group(0)
    e = re.sub(r'(<hp:endNote number=")\d+', lambda q: q.group(1) + str(k[0]), e, count=1)
    e = re.sub(r'(<hp:autoNum num=")\d+(" numType="ENDNOTE")', lambda q: q.group(1) + str(k[0]) + q.group(2), e, count=1)
    return e


x = re.sub(r"<hp:endNote .*?</hp:endNote>", ren, x, flags=re.S)
with zipfile.ZipFile(out, "w") as zo:
    for info, data in items:
        if info.filename == "Contents/section0.xml":
            data = x.encode("utf-8")
        zo.writestr(info, data, compress_type=info.compress_type)
print("미주", 312, "~", k[0], "->", out)
