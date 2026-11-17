# -*- coding: utf-8 -*-
"""표·그림의 숨은 설명(shapeComment)에 남은 사람 이름을 기본 설명으로: python3 shapecmt.py 파일.hwpx 이름"""
import sys
sys.path.insert(0, '.')
import hwpxedit as H
P, name = sys.argv[1], sys.argv[2]
x = H.load(P)
old = '<hp:shapeComment>%s</hp:shapeComment>' % name
n = x.count(old)
if n:
    H.save(P, x.replace(old, '<hp:shapeComment>표입니다.</hp:shapeComment>'))
print(P, '숨은 설명', n)
