# 수정한 26번(사차방정식) 문제·해설을 양식 글꼴로 담은 HWPX 만들기
import sys, os, copy, zipfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hwpedit import *

FD, OUT = sys.argv[1], sys.argv[2]
sec_tree = load(f'{FD}/Contents/section0.xml')
root = sec_tree.getroot()
paras = root.findall(HP + 'p')
first = paras[0]
tmpl_eq = next(root.iter(HP + 'equation'))
tmpl_eq = copy.deepcopy(tmpl_eq)
# 첫 문단: 용지·단 설정만 남기기
for r in first.findall(HP + 'run'):
    for x in list(r):
        keep = x.tag == HP + 'secPr' or (x.tag == HP + 'ctrl' and x.find(HP + 'colPr') is not None)
        if not keep:
            r.remove(x)
for p in paras[1:]:
    root.remove(p)
for la in list(root.iter(HP + 'linesegarray')):
    la.getparent().remove(la)

PB, PS = '0', '0'           # 문단 모양
CP_Q, CP_S = '50', '24'     # 문제 글자(하는체), 해설 글자(나눔고딕)
tp = etree.Element(HP + 'p')
tp.set('paraPrIDRef', PB); tp.set('styleIDRef', '0'); tp.set('merged', '0')

lines = [
    (CP_Q, '[수정 문제]'),
    (CP_Q, '26. 사차방정식 $x^4 -(3n+2)x^2 +n^2 =0$의 서로 다른 두 양의 실근을 $alpha ,~beta$라 할 때, $beta =3 alpha$가 되도록 하는 정수 $n$의 값을 구하시오. (단, $alpha < beta$)'),
    (CP_Q, ''),
    (CP_S, '[정답] $6$'),
    (CP_S, '$x^2 =t$로 놓으면'),
    (CP_S, '$t^2 -(3n+2)t+n^2 =0$ …… ㉠'),
    (CP_S, '주어진 방정식이 서로 다른 두 양의 실근 $alpha ,~beta$를 가지므로 ㉠은 서로 다른 두 양의 실근 $alpha ^2 ,~beta ^2$을 갖는다.'),
    (CP_S, '$beta =3 alpha$이므로 ㉠의 두 근은 $alpha ^2 ,~9 alpha ^2$이고, 근과 계수의 관계에 의하여'),
    (CP_S, '$alpha ^2 +9 alpha ^2 =10 alpha ^2 =3n+2$ …… ㉡'),
    (CP_S, '$alpha ^2 TIMES 9 alpha ^2 =9 alpha ^4 =n^2$ …… ㉢'),
    (CP_S, '㉢에서 $3 alpha ^2 = LEFT | n RIGHT |$'),
    (CP_S, '(ⅰ) $n>0$일 때, $alpha ^2 = {n} over {3}$을 ㉡에 대입하면 ${10n} over {3} =3n+2$    ∴ $n=6$'),
    (CP_S, '(ⅱ) $n<0$일 때, $alpha ^2 =- {n} over {3}$을 ㉡에 대입하면 $- {10n} over {3} =3n+2$    ∴ $n=- {6} over {19}$ (정수가 아니다.)'),
    (CP_S, '따라서 구하는 정수 $n$의 값은 $6$이다.'),
    (CP_S, '(확인) $n=6$이면 $x^4 -20x^2 +36=(x^2 -2)(x^2 -18)=0$에서 양의 실근은 $sqrt {2} ,~3 sqrt {2}$이므로 $beta =3 alpha$를 만족시킨다.'),
    (CP_Q, ''),
    (CP_S, '※ 원래 문제(β=2α)는 조건을 만족시키는 정수 n이 없다.'),
    (CP_S, '   $t_2 =4t_1$에서 $5t_1 =3n+2$, $4{t_1}^2 =n^2$ ⇒ $n>0$이면 $n=-4$(모순), $n<0$이면 $n=- {4} over {11}$(정수 아님)'),
]
for cp, txt in lines:
    root.append(make_para(tp, tmpl_eq, cp, seg_parse(txt) if txt else []))
sec_out = OUT + '.section0.xml'
save(sec_tree, sec_out)

with zipfile.ZipFile(OUT, 'w') as z:
    z.writestr(zipfile.ZipInfo('mimetype'), open(f'{FD}/mimetype', 'rb').read(), compress_type=zipfile.ZIP_STORED)
    def add(n, data):
        z.writestr(n, data, compress_type=zipfile.ZIP_DEFLATED)
    for n in ('version.xml', 'Contents/header.xml', 'Contents/content.hpf', 'settings.xml', 'BinData/image1.png',
              'META-INF/container.xml', 'META-INF/container.rdf', 'META-INF/manifest.xml',
              'Preview/PrvText.txt', 'Preview/PrvImage.png'):
        add(n, open(f'{FD}/{n}', 'rb').read())
    for mp in ('masterpage0.xml', 'masterpage1.xml'):
        s = open(f'{FD}/Contents/{mp}', encoding='utf-8').read()
        s = s.replace('1. 수열의 극한', '수정 문항').replace('수열의 극한', '수정 문항')
        add(f'Contents/{mp}', s.encode('utf-8'))
    add('Contents/section0.xml', open(sec_out, 'rb').read())
print('ok', OUT)
