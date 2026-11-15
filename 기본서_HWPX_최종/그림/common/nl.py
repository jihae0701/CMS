# -*- coding: utf-8 -*-
"""수직선 그림 공통: 축(오른쪽 화살표), 점(채운/빈), 아래 숫자, 범위 꺾쇠(높이별), 겹친 부분 연한 색"""
import sys
sys.path.insert(0, '/home/user/CMS/.claude/skills/math-figure-rules')
from mathfig import Frame, dot, SKY

def numline(pts, ranges, x0, x1, name='x', shade=None, unit=46, levels=None):
    """pts: [(x, '라벨', filled)], ranges: [(a, b, level)] — level 1,2,… 높이의 꺾쇠, shade: (a, b, level) 연한 색 칠"""
    top = max([r[2] for r in ranges] + [0])
    F = Frame((x0, x1), (-0.9, 0.55 * top + 0.35), unit, unit, (16, 14, 26, 14))
    if shade:
        a, b, lv = shade
        F.poly([(a, 0), (b, 0), (b, 0.55 * lv), (a, 0.55 * lv)], SKY)
    F.xaxis(x0, x1, name)
    for a, b, lv in ranges:
        h = 0.55 * lv
        F.svg.append('<polyline points="%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="none" stroke="#000" stroke-width="3.2" stroke-linejoin="round"/>'
                     % (F.P(a, 0) + F.P(a, h) + F.P(b, h) + F.P(b, 0)))
    for x, lab, filled in pts:
        X, Y = F.P(x, 0)
        if filled:
            dot(F, (x, 0), 5)
        else:
            F.svg.append('<circle cx="%.1f" cy="%.1f" r="5" fill="#fff" stroke="#000" stroke-width="2"/>' % (X, Y))
        F.lab((x, 0), lab, 'ct', 0, 12)
    return F.render()
