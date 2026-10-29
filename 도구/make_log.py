# 수정기록.md 단원 부분 만들기
import sys, json, re
sys.path.insert(0,'.')
from hwpedit import *
S='/tmp/claude-0/-home-user-CMS/6e5852ae-cc0e-5adb-9ab3-0e789dd16949/scratchpad'
UNITS=[('u1','1. 함수의 극한','올려 준 단원 파일 1, 59문항'),('u2','2. 함수의 연속','올려 준 단원 파일 2, 48문항')]
if len(sys.argv) > 1:
    UNITS=[tuple(sys.argv[1:4])]
OUTP = sys.argv[4] if len(sys.argv) > 4 else S+'/log_section.md'
DATE = sys.argv[5] if len(sys.argv) > 5 else '2026-10-12'

def where_map(u):
    """원본에서 bold·괄호 정리가 일어난 수식의 문항 번호 모으기"""
    d=Doc(load(f'{S}/{u}/Contents/section0.xml'))
    ens=d.endnotes(); n=len(ens)
    owner={}
    for k in range(1,n+1):
        for p in d.problem_paras(k):
            for e in p.iter(HP+'equation'):
                owner[e]=(k, '해설' if in_endnote(e) else '문제')
    bold=set(); brace=set()
    for e in d.root.iter(HP+'equation'):
        sc=e.find(HP+'script').text or ''
        k,w=owner.get(e,('개념',''))
        concept=any(a.tag==HP+'rect' and a.find(HP+'lineShape') is not None and a.find(HP+'lineShape').get('width')=='198' for a in e.iterancestors())
        top=d.top_of(e)
        quick=(not in_endnote(e)) and top.find('.//'+HP+'endNote') is None and any(a.get('numType')=='ENDNOTE' for a in top.iter(HP+'autoNum'))
        title=any(a.tag==HP+'container' for a in e.iterancestors())
        if concept or title: k='개념'
        if quick: continue
        lab=f'{k}' if k=='개념' else f'{k}번 {w}'
        nb=re.sub(r'(?i)bold','',sc)
        if nb!=sc: bold.add(lab)
        if fix_braces(nb)!=nb: brace.add(lab)
    return bold, brace

def key(lab):
    m=re.match(r'(\d+)',lab); return (0,0,lab) if not m else (1,int(m.group(1)),lab)

NICE={('는 두 점','는 두 점 '):('두 점(a, f(a))','두 점 (a, f(a))'),
      ('이다. 함수','이다. 함수 '):('함수f(x)가','함수 f(x)가'),
      ('다항함수','다항함수 '):('다항함수f(x)가','다항함수 f(x)가'),
      ('극한 문제는 항상 ','극한 문제는 '):('대부분의 경우 극한 문제는 항상 (우극한)=(좌극한)','\'항상\' 삭제 (\'대부분\'과 모순)'),
      ('이므로 (분모)','이고, 0이 아닌 극한값이 존재하므로 (분모)'):('(분자)→0이므로 (분모)→0','(분자)→0이고, 0이 아닌 극한값이 존재하므로 (분모)→0'),
      ('ㄷ. ','ㄴ. '):('둘째 항목 번호 ㄷ.','ㄴ.'),
      ('이다. 이때, ','개이다. 이때, '):('점의 개수는 b이다','점의 개수는 b개이다'),
      ('    되어있고 즉 ','    되어 있고, 즉 '):('정의 되어있고 즉','정의되어 있고, 즉'),
      ('의 불연속인','가 불연속인'):('(f∘f)(x)의 불연속인','(f∘f)(x)가 불연속인'),
      ('에서 연속이어야한다.','에서 연속인지만 조사하면 된다.'):('…x=1에서 연속이어야한다.','…x=1에서 연속인지만 조사하면 된다.')}
def tidy(v):
    v=str(v)
    v=re.sub(r'\{\s*([^{}]+?)\s*\}\s*over\s*\{\s*([^{}]+?)\s*\}', r'\1/\2', v)
    return v.replace('- ','-').replace('$','')
def esc(s): return tidy(s).replace('|','\\|').replace('\n',' ')

out=[]
for u,title,src in UNITS:
    a=json.load(open(f'{S}/work/{u}_section0.xml.log.json')); b=json.load(open(f'{S}/work/{u}_fig.xml.fig.json'))
    logs=a['log']+b['log']
    short=[l for l in logs if l[2]=='단답형']
    figs=[l for l in logs if l[2]=='그림']
    rest=[l for l in logs if l[2] not in ('단답형','그림')]
    def sk(l):
        q=str(l[0]); m=re.match(r'개념(\d+)',q)
        if m: return (0,int(m.group(1)))
        if q.isdigit(): return (1,int(q))
        return (2,0)
    rest.sort(key=sk)
    out.append(f'\n## {title} ({src}) — 검토일 {DATE}\n')
    out.append('결과 파일: `완성/%s.hwpx` · 문항 번호는 원본과 같음(문항을 더하거나 빼지 않음)\n' % title)
    out.append('### 오타·오류\n')
    out.append('| # | 문항 | 위치 | 종류 | 원래 | 고친 내용 |')
    out.append('|---|------|------|------|------|-----------|')
    for i,l in enumerate(rest,1):
        l=list(l); l[3],l[4]=NICE.get((l[3],l[4]),(l[3],l[4]))
        q=l[0]; q=f'{q}번' if str(q).isdigit() else q
        out.append(f'| {i} | {esc(q)} | {esc(l[1])} | {esc(l[2])} | {esc(l[3])} | {esc(l[4])} |')
    out.append('\n### 단답형으로 바꾼 문항 (보기 지우고, 정답을 번호 → 값으로)\n')
    out.append('| 문항 | 원래 정답 | 새 정답 |')
    out.append('|------|-----------|---------|')
    for l in sorted(short,key=lambda l:int(l[0])):
        out.append(f'| {l[0]}번 | {esc(l[3])} | {esc(l[4])} |')
    out.append('\n문장 끝은 "~의 값은?" → "~의 값을 구하시오.", "옳은 것을 모두 고른 것은?" → "옳은 것만을 있는 대로 고르시오." 식으로 바꿈.\n')
    out.append('### 그림\n')
    out.append('| 문항 | 내용 |')
    out.append('|------|------|')
    for l in sorted(figs,key=lambda l:int(l[0])):
        out.append(f'| {l[0]}번 | {esc(l[3])} → {esc(l[4])} |')
    bold,brace=where_map(u)
    out.append('\n### 수식 정리 (화면 모양은 거의 그대로, 수식 문법만 바로잡음)\n')
    out.append('- **bold 지움**(빠른 정답 목록은 통째로 지워서 뺌, "개념"은 개념 상자·유형 제목): ' + ', '.join(sorted(bold,key=key)))
    out.append('- **짝이 맞지 않는 중괄호 정리**(남는 `} { }` 지우기, 빠진 `}` 채우기): ' + ', '.join(sorted(brace,key=key)))
    out.append('')
open(OUTP,'w').write('\n'.join(out))
print('\n'.join(out)[:3000])
