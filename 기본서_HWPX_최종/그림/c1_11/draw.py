import sys
sys.path.insert(0, '/home/user/CMS/.claude/skills/math-figure-rules'); sys.path.insert(0, sys.argv[2])
from mathfig import Frame, fit_shoot, dot
from nl2 import numline2
OUT = sys.argv[1]
figs = {}
# 28번: ㉠ x≤1, ㉡ x>3-a (-4≤3-a<-3) → 3-a<x≤1
base28 = lambda: numline2(-5.6, 2.6, [(None, 1, 1, '㉠'), (-3.55, None, 2, '㉡')],
                              [(-3.55, '', False), (1, '1', True)], ticks=[-4, -3, -2, -1, 0],
                              shade=[(-3.55, 1, 1)], hstep=0.8, bottom=-1.7)
def f28():
    F = base28()
    for x, l in ((-4, '-4'), (-3, '-3')):
        F.lab((x, 0), l, 'ct', 0, 12)
    F.lab((-3.55, 0), '3-a', 'ct', 0, 44)
    return F.render()
figs['28'] = f28
def lab_ticks(F, xs):
    for x, l in xs:
        F.lab((x, 0), l, 'ct', 0, 44 if 'k' in l else 12)
    return F
# 41번: ㉠ k-5≤x≤k+5, ㉡ x<-3 또는 x>4
def c41(k, xs):
    def g():
        F = numline2(min(k - 5, -3) - 3.6, max(k + 5, 4) + 3.4, [(k - 5, k + 5, 2, '㉠'), (None, -3, 1, '㉡'), (4, None, 1, '㉡')],
                     [(k - 5, None, True), (k + 5, None, True), (-3, None, False), (4, None, False)], ticks=[],
                     shade=([(k - 5, min(k + 5, -3), 1)] if k - 5 < -3 else []) + ([(max(k - 5, 4), k + 5, 1)] if k + 5 > 4 else []), unit=46, hstep=0.9, bottom=-2.7)
        return lab_ticks(F, xs).render()
    return g
figs['41a'] = c41(-3.4, [(-8.4, 'k-5'), (-3, '-3'), (1.6, 'k+5'), (4, '4')])
figs['41b'] = c41(0.4, [(-4.6, 'k-5'), (-3, '-3'), (4, '4'), (5.4, 'k+5')])
figs['41c'] = c41(3.6, [(-3, '-3'), (-1.4, 'k-5'), (4, '4'), (8.6, 'k+5')])
def f46():
    F = Frame((-0.6, 5.6), (-1.6, 6.6), 52, 44, (16, 16, 120, 16))
    F.xaxis(-0.6, 5.6)
    f = lambda x: 0.8 * (x - 2) * (x - 4)
    F.curve(f, 0.45, 5.55)
    F.dashed((1, f(1)), (1, 0)); F.dashed((3, f(3)), (3, 0))
    F.dashed((3, 0), (3, f(5.55)))
    F.lab((1, 0), '1', 'ct', 0, 8)
    F.lab((3, f(3)), 'x=a', 'ct', 0, 10)
    F.lab((5.55, f(5.55)), r'y=f(x)', 'lc', 8, 0)
    return F.render()
figs['46'] = f46
for k, fn in figs.items():
    print(k, '폭', fit_shoot(OUT + '/c1_11_%s.png' % k, fn))
