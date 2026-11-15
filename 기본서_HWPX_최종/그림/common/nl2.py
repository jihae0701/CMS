# -*- coding: utf-8 -*-
"""범위 꺾쇠 수직선: ranges=[(a, b, level, '㉠')] (a=None → -∞, b=None → +∞, 무한 쪽은 화살표),
   pts=[(x, '라벨', filled)], ticks=[x], shade=[(a, b, level)] (연노랑)"""
import sys
sys.path.insert(0, '/home/user/CMS/.claude/skills/math-figure-rules')
from mathfig import Frame, dot
YEL = '#fff3bf'
H = 0.62

def numline2(x0, x1, ranges, pts, ticks=(), shade=(), name='x', unit=40, hstep=None, bottom=-1.0):
    global H
    H = hstep or 0.62
    top = max(r[2] for r in ranges)
    F = Frame((x0, x1), (bottom, H * top + 0.5), unit, unit, (16, 16, 26, 16))
    for a, b, lv in shade:
        F.poly([(a, 0), (b, 0), (b, H * lv), (a, H * lv)], YEL)
    F.xaxis(x0, x1, name)
    F.svg.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#000" stroke-width="2" marker-end="url(#ar)"/>'
                 % (F.P(x0 + 0.6, 0) + F.P(x0, 0)))
    for t in ticks:
        X, Y = F.P(t, 0)
        F.svg.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#000" stroke-width="1.6"/>' % (X, Y - 5, X, Y + 5))
    for a, b, lv, lab in ranges:
        h = H * lv
        L = a if a is not None else x0 + 0.25
        R = b if b is not None else x1 - 0.25
        if a is not None:
            F.seg((a, 0), (a, h), 2.4)
        if b is not None:
            F.seg((b, 0), (b, h), 2.4)
        # 가운데를 끊고 ㉠ 글자
        mid = (L + R) / 2 if (a is not None and b is not None) else ((R - 1.6) if a is not None else (L + 1.6))
        g = 0.32
        if a is None:
            F.svg.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#000" stroke-width="2.4" marker-end="url(#ar)"/>' % (F.P(mid - g, h) + F.P(L, h)))
        else:
            F.seg((L, h), (mid - g, h), 2.4)
        if b is None:
            F.svg.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#000" stroke-width="2.4" marker-end="url(#ar)"/>' % (F.P(mid + g, h) + F.P(R, h)))
        else:
            F.seg((mid + g, h), (R, h), 2.4)
        F.labels.append(F.P(mid, h) + (r'\text{%s}' % lab, 22, 'cc', 'dim'))
    for x, lab, filled in pts:
        X, Y = F.P(x, 0)
        if filled:
            dot(F, (x, 0), 5)
        else:
            F.svg.append('<circle cx="%.1f" cy="%.1f" r="5" fill="#fff" stroke="#000" stroke-width="2"/>' % (X, Y))
        if lab:
            F.lab((x, 0), lab, 'ct', 0, 12)
    return F
