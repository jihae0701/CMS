# -*- coding: utf-8 -*-
"""두 단원에 공통으로 쓰는 고치기: 단답형 바꾸기, bold 없애기, 괄호 정리, 빠른 정답 지우기"""
import re, copy
from hwpedit import *


def set_answer(d, k, ans):
    """미주 첫 문단 '[정답] ②'를 값으로. ans: '$수식$' 또는 글"""
    note = d.endnote(k)
    p0 = note.findall('.//' + HP + 'p')[0]
    old = own_text(p0)
    hit = None
    for r in p0.findall(HP + 'run'):
        for t in r.findall(HP + 't'):
            txt = ''.join(t.itertext())
            m = re.search(r'\[정답\]\s*([①②③④⑤])', txt)
            if m:
                hit = (r, t, m)
    assert hit, ('정답 찾기 실패', k, old)
    r, t, m = hit
    t.text = (t.text or '').replace(m.group(1), '')
    segs = seg_parse(ans)
    tmpl_eq = next(d.root.iter(HP + 'equation'))
    pos = list(r).index(t) + 1
    for s in segs:
        if isinstance(s, str):
            t.text = (t.text or '') + s
        else:
            e = make_eq(tmpl_eq, s[1])
            r.insert(pos, e)
            pos += 1
    log(k, '정답', '단답형', m.group(1), ans.replace('$', ''))


def drop_choices(d, k):
    """문항 k의 보기(①~⑤) 문단 지우기"""
    n = 0
    for p in d.problem_paras(k):
        t = own_text(p).lstrip()
        if t[:1] and (t[:1] in '①②③④⑤' or t.startswith('㈎')):
            assert '[미주' not in t
            if p.find('.//' + HP + 'endNote') is not None:
                raise AssertionError(('보기 문단에 미주', k))
            p.getparent().remove(p)
            n += 1
    assert n >= 1, ('보기 없음', k)


def to_short(d, k, ans, subs):
    """subs: [(옛 글, 새 글)] 문제 글 바꾸기"""
    scope = d.problem_paras(k)
    for old, new in subs:
        text_sub(scope, k, '문제', '단답형', old, new, problem_only=True, quiet=True)
    drop_choices(d, k)
    set_answer(d, k, ans)


def strip_bold_and_braces(d, unit_log):
    """모든 수식에서 bold 지우고 괄호 짝 맞추기. 바뀐 문항 번호를 모은다"""
    ens = d.endnotes()
    bold_q, brace_q = set(), set()
    k = 0
    for el in d.root.iter():
        if el.tag == HP + 'endNote':
            k = ens.index(el) + 1
        if el.tag != HP + 'equation':
            continue
        sc = el.find(HP + 'script').text or ''
        new = re.sub(r'(?i)bold', '', sc)
        where = ('해설' if in_endnote(el) else '문제/개념')
        q = k if in_endnote(el) else None
        if new != sc:
            bold_q.add(q if q else '개념·문제')
        b2 = fix_braces(new)
        if b2 != new:
            brace_q.add((k if in_endnote(el) else '본문', ))
        if b2 != sc:
            set_script(el, b2)
    unit_log['bold'] = bold_q
    unit_log['brace'] = brace_q


def drop_quick_answers(d):
    """본문 끝(단원 제목 뒤)의 빠른 정답 문단 지우기. 쪽 번호 새로 매기기(newNum)는 남김"""
    top = d.top()
    n = 0
    for p in top:
        if p.find('.//' + HP + 'endNote') is not None:
            continue
        has_auto = any(a.get('numType') == 'ENDNOTE' for a in p.iter(HP + 'autoNum'))
        if not has_auto:
            continue
        if p.find('.//' + HP + 'newNum') is not None:
            for r in p.findall(HP + 'run'):
                keep = [x for x in r if x.tag == HP + 'ctrl' and x.find(HP + 'newNum') is not None]
                for x in list(r):
                    if x not in keep:
                        r.remove(x)
            n += 1
        else:
            d.root.remove(p)
            n += 1
    return n


def find_para(scope_el, starts=None, contains=None):
    hits = []
    for p in scope_el.iter(HP + 'p'):
        t = own_text(p)
        if starts and t.lstrip().startswith(starts) or contains and contains in t:
            hits.append(p)
    assert len(hits) == 1, ('문단 찾기 실패', starts, contains, len(hits))
    return hits[0]


def replace_para(d, k, p, lines, tmpl_p=None):
    """문단 p를 새 문단들로 바꿈. lines: seg 문자열 리스트"""
    note = d.endnote(k)
    body, cp, eq = note_templates(note)
    tp = tmpl_p if tmpl_p is not None else p
    if eq is None:
        eq = next(d.root.iter(HP + 'equation'))
    parent = p.getparent()
    i = list(parent).index(p)
    parent.remove(p)
    for j, ln in enumerate(lines):
        parent.insert(i + j, make_para(tp, eq, cp, seg_parse(ln)))


def add_paras(d, k, after_p, lines, tmpl_p=None, cp=None):
    note = d.endnote(k)
    body, cp0, eq = note_templates(note)
    if eq is None:
        eq = next(d.root.iter(HP + 'equation'))
    tp = tmpl_p if tmpl_p is not None else body
    cp = cp or cp0
    parent = after_p.getparent()
    i = list(parent).index(after_p)
    for j, ln in enumerate(lines):
        parent.insert(i + 1 + j, make_para(tp, eq, cp, seg_parse(ln)))


def eq_edit(scope, q, where, kind_, contains, old_sub, new_sub, show=None, **kw):
    hits = [e for e in iter_scope(scope, 'equation', kw.get('problem_only', False))
            if contains in (e.find(HP + 'script').text or '')
            and (not kw.get('solution_only') or in_endnote(e))]
    assert len(hits) == 1, ('수식 찾기 실패', contains, len(hits))
    e = hits[0]
    sc = e.find(HP + 'script').text
    assert old_sub in sc, (old_sub, sc)
    set_script(e, sc.replace(old_sub, new_sub, 1))
    log(q, where, kind_, show[0] if show else old_sub, show[1] if show else new_sub)
