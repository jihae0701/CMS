# -*- coding: utf-8 -*-
"""수식 속 글자 기호를 명령으로: ÷→div, ±→+-, ∴→THEREFORE, ×→times, 근호 지수 자리 eqalign{n#}/pile{n#} → n
    python3 symfix.py 파일.hwpx"""
import sys, re, html, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hwpxedit as H, eqstyle
p = sys.argv[1]; x = H.load(p); cnt = {}
def f(m):
    s0 = html.unescape(m.group(2)); s = s0
    for a, b in (('÷', ' div '), ('±', ' +- '), ('∴', 'THEREFORE '), ('×', ' times '), ('∓', ' -+ '), ('≠', ' neq '), ('≥', ' geq '), ('≤', ' leq '), ('＋', '+'), ('—', '-')):
        if a in s:
            cnt[a] = cnt.get(a, 0) + s.count(a); s = s.replace(a, b)
    s3 = re.sub(r'(?<![A-Za-z])(sin|cos|tan)(theta|x|t)(?![A-Za-z])', r'\1`\2', s)
    s3 = re.sub(r'(?<![A-Za-z])piover(?![A-Za-z])', 'pi over', s3)
    s3 = re.sub(r'(?<![A-Za-z])(sin|cos|tan)([A-C])(?![A-Za-z])', r'\1`\2', s3)
    s3 = re.sub(r'(?<![A-Za-z])rm(angle|ANGLE|bar|therefore|because|THEREFORE|BECAUSE|triangle)', r'rm \1', s3)
    s3 = re.sub(r'(?<![A-Za-z])(angle|ANGLE)([A-Z])(?![a-z])', r'\1 \2', s3)
    s3 = re.sub(r'(?<![A-Za-z])RMBAR([A-Z]{1,3})(?![A-Za-z])', r'bar{rm \1}', s3)
    s3 = re.sub(r'(?<![A-Za-z])RMANGLE([A-Z]{1,3})(?![A-Za-z])', r'rm angle \1', s3)
    s3 = re.sub(r'(?<![A-Za-z])RM([A-Z]{1,4})(?![A-Za-z])', r'rm \1', s3)
    s3 = re.sub(r'(?<![A-Za-z])(bar|BAR)([A-Z]{2,3})(?![A-Za-z])', r'bar{\2}', s3)
    s3 = re.sub(r'(?<![A-Za-z])(triangle|TRIANGLE)([A-Z])', r'\1 \2', s3)
    if s3 != s:
        cnt['붙은 함수'] = cnt.get('붙은 함수', 0) + 1; s = s3
    s2 = re.sub(r'(root|sqrt)\s*\{\s*(?:eqalign|pile)\{\s*(\d+)\s*#\s*\}\s*\}', r'\1 {\2}', s)
    if s2 != s:
        cnt['지수자리'] = cnt.get('지수자리', 0) + 1; s = s2
    if s == s0:
        return m.group(0)
    return m.group(1) + eqstyle.esc(s) + m.group(3)
x = H.SC.sub(f, x)
H.save(p, x); print(p, '기호', cnt)
