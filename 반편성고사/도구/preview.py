# 시험지 내용 미리보기(PDF): KaTeX로 수식 렌더링, 2단 A4
import sys, os, re, html
from playwright.sync_api import sync_playwright
from problems import M1, M2, PTS
from hwp2latex import convert
HERE=os.path.dirname(os.path.abspath(__file__)); K=os.path.join(HERE,'npmk/node_modules/katex/dist')
FIG=os.path.join(HERE,'figs'); CIRC="①②③④⑤"
def rich(t):
    out=[]
    for i,p in enumerate(re.split(r"\$(.+?)\$",t)):
        out.append('<span class="m" data-t="%s"></span>'%html.escape(convert(p)) if i%2 else html.escape(p))
    return "".join(out)
def prob(p):
    tag=" [%d점]"%PTS[p['level']]; body=list(p['body']); b2=list(p.get('body2',[]))
    if b2: b2[-1]+=tag
    else: body[-1]+=tag
    h=['<div class="q"><div class="no">%d.</div>'%p['no']]
    h+=['<p>%s</p>'%rich(l) for l in body]
    box='<div class="box">%s</div>'%"".join('<p>%s</p>'%rich(l) for l in p['box']) if p.get('box') else ''
    if p.get('fig'):
        h.append('<div class="fig"><img src="file://%s/%s"></div>'%(FIG,p['fig'])); h+=['<p>%s</p>'%rich(l) for l in b2]; h.append(box)
    else:
        h.append(box); h+=['<p>%s</p>'%rich(l) for l in b2]
    if p['choices']:
        h.append('<div class="ch">%s</div>'%"".join('<span>%s %s</span>'%(CIRC[i],rich('$'+c+'$')) for i,c in enumerate(p['choices'])))
    h.append('</div>'); return "".join(h)
def sol(p):
    a=CIRC[p['ans']-1] if p['choices'] else p['ans']
    return '<div class="s"><b>%d. [정답] %s</b> <small>(%s · %s · %d점 · 변형: %s)</small>%s</div>'%(p['no'],a,p['unit'],p['level'],PTS[p['level']],p['src'],"".join('<p>%s</p>'%rich(l) for l in p['sol']))
def page(M,subj,out):
    doc='''<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="file://%s/katex.min.css"><script src="file://%s/katex.min.js"></script>
<style>@page{size:A4;margin:14mm 12mm} body{font-family:"Noto Sans KR",sans-serif;font-size:10.5pt;line-height:1.75}
h1{text-align:center;font-size:20pt;margin:0 0 2mm;border-bottom:2px solid #000;padding-bottom:2mm} .sub{text-align:center;margin-bottom:4mm}
.cols{column-count:2;column-gap:10mm;column-rule:1px solid #000} .q{break-inside:avoid;margin-bottom:22mm;position:relative;padding-left:7mm}
.no{position:absolute;left:0;top:0;font-weight:700;font-size:12pt} .q p{margin:0 0 1mm}
.box{border:1px solid #000;padding:2mm 3mm;margin:2mm 0} .box p{margin:0} .fig{text-align:center;margin:2mm 0} .fig img{width:60%%}
.ch{display:grid;grid-template-columns:repeat(3,1fr);row-gap:1mm;margin-top:2mm} .katex{font-size:1.05em}
.s{break-inside:avoid;margin-bottom:5mm} .s p{margin:0 0 0 4mm} h2{break-before:page}
</style></head><body><h1>%s</h1><div class="sub">예비고1 반편성고사 · 20문항(객관식 14, 단답형 6) · 60분 · 100점</div>
<div class="cols">%s</div><h2>%s 정답 및 해설</h2><div class="cols">%s</div>
<script>document.querySelectorAll('.m').forEach(e=>{try{katex.render(e.dataset.t,e,{throwOnError:true,strict:false})}catch(x){e.textContent='[[ERR '+e.dataset.t+']]';e.style.color='red'}});</script></body></html>'''%(K,K,subj,"".join(prob(p) for p in M),subj,"".join(sol(p) for p in M))
    hp=out.replace('.pdf','.html'); open(hp,'w').write(doc)
    with sync_playwright() as pw:
        b=pw.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome"); pg=b.new_page()
        pg.goto('file://'+hp); pg.wait_for_timeout(500)
        errs=pg.evaluate("Array.from(document.querySelectorAll('.m')).filter(e=>e.textContent.startsWith('[[ERR')).map(e=>e.textContent)")
        pg.pdf(path=out,format='A4',print_background=True); b.close()
    print(out,'수식 오류',len(errs),errs[:5])
OUT=os.path.abspath(sys.argv[1]); page(M1,'공통수학1',OUT+'/미리보기_공통수학1.pdf'); page(M2,'공통수학2',OUT+'/미리보기_공통수학2.pdf')
