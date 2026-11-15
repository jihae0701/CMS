import sys
sys.path.insert(0, '/home/user/CMS/.claude/skills/math-figure-rules'); sys.path.insert(0, sys.argv[2])
from mathfig import fit_shoot
from qp import qplot
OUT = sys.argv[1]
R = lambda F: F.render()
fr = lambda a, b: r"\dfrac{%s}{%s}" % (a, b)
figs = {
 'img2': lambda: R(qplot(lambda x: -3*x*x+2*x, (0, 1), (-0.45, 1.5), (-1.55, 0.75), 150, 150, pts=[(0, 0), (1/3, 1/3), (1, -1)],
                         xt=[(1/3, fr(1, 3)), (1, '1')], yt=[(1/3, fr(1, 3)), (-1, '-1')], label=(r'y=f(x)', 0.6, 'lb', 16, -10), m=(16, 16, 90, 16))),
 'img3': lambda: R(qplot(lambda x: x*x-4*x+1, (0, 1), (-0.7, 4.3), (-3.8, 2.4), 52, 52, pts=[(0, 1), (1, -2), (2, -3)],
                         xt=[(1, '1'), (2, '2')], yt=[(1, '1'), (-2, '-2'), (-3, '-3')], label=(r'y=f(x)', 3.9, 'rb', -10, -2), crange=(-0.15, 4.0))),
 'img4': lambda: R(qplot(lambda x: -2*x*x-4*x+1, (-3, 0), (-3.8, 1.3), (-6.0, 4.0), 46, 34, pts=[(-3, -5), (-1, 3), (0, 1)],
                         xt=[(-3, '-3'), (-1, '-1')], yt=[(3, '3'), (1, '1'), (-5, '-5')], crange=(-3.25, 0.65), origin=True)),
 'img5': lambda: R(qplot(lambda x: x*x-2*x+5, (-2, 0), (-2.8, 3.3), (-1.0, 16.5), 50, 12, pts=[(0, 5), (1, 4)], opens=[(-2, 13)],
                         xt=[(-2, '-2'), (1, '1')], yt=[(13, '13'), (5, '5'), (4, '4')], crange=(-2.2, 3.0))),
 'img6': lambda: R(qplot(lambda x: x*x-2*x+2, (0, 3), (-0.8, 4.2), (-0.6, 6.4), 48, 40, yname='t', pts=[(0, 2), (1, 1), (3, 5)],
                         xt=[(1, '1'), (3, '3')], yt=[(5, '5'), (2, '2'), (1, '1')], label=(r't=x^2-2x+2', 3.25, 'lb', 6, -2), crange=(-0.6, 3.25), m=(16, 16, 120, 16))),
 'img7': lambda: R(qplot(lambda t: t*t-2*t+1, (1, 5), (-1.2, 6.2), (-1.5, 19), 34, 9, xname='t', pts=[(1, 0), (5, 16)],
                         xt=[(1, '1'), (5, '5')], yt=[(16, '16')], label=(r'y=t^2-2t+1', 5.3, 'lc', 8, 0), crange=(-1.6, 5.3), m=(16, 16, 170, 16))),
 'img8': lambda: R(qplot(lambda x: x*x-2*x+3, (-1, 2), (-1.6, 3.1), (-0.6, 7.6), 48, 30, yname='t', pts=[(-1, 6), (1, 2), (2, 3)],
                         xt=[(-1, '-1'), (1, '1'), (2, '2')], yt=[(6, '6'), (3, '3'), (2, '2')], crange=(-1.4, 2.9))),
 'img9': lambda: R(qplot(lambda t: t*t-4*t-2, (2, 6), (-3.0, 7.4), (-7.5, 12.0), 34, 14, xname='t', pts=[(2, -6), (6, 10)],
                         xt=[(2, '2'), (6, '6')], yt=[(10, '10'), (-2, '-2'), (-6, '-6')], crange=(-0.6, 6.25))),
 'img10': lambda: R(qplot(lambda x: -(x-3)**2+5, (0, 2), (-0.8, 6.6), (-5.0, 6.2), 44, 30, yname='t', pts=[(0, -4), (2, 4), (3, 5)],
                          xt=[(2, '2'), (3, '3')], yt=[(5, '5'), (4, '4'), (-4, '-4')], label=(r't=-(x-3)^2+5', 4.6, 'lc', 12, 0), crange=(0, 5.3), m=(16, 16, 150, 16))),
 'img11': lambda: R(qplot(lambda x: x*x-2*x-1, (0, 3), (-1.3, 4.0), (-2.7, 3.6), 52, 44, pts=[(0, -1), (1, -2), (3, 2)],
                          xt=[(1, '1'), (3, '3')], yt=[(2, '2'), (-1, '-1'), (-2, '-2')], label=(r'y=x^2-2x-1', 3.45, 'lb', 6, -2), crange=(-0.9, 3.45), m=(16, 16, 140, 16))),
 'img12': lambda: R(qplot(lambda x: -x*x+4*x-3, (2, 4), (-0.8, 5.0), (-4.8, 2.0), 50, 44, pts=[(2, 1), (4, -3)],
                          xt=[(2, '2'), (4, '4')], yt=[(1, '1'), (-3, '-3')], label=(r'y=-x^2+4x-3', 4.3, 'lc', 10, 0), crange=(0.1, 4.3), m=(16, 16, 215, 16))),
 'img15': lambda: R(qplot(lambda t: -2*(t-3)**2+15, (-2, 5.75), (-3.2, 5.6), (-38, 21), 40, 3.2, xname='t', pts=[(-2, -35), (3, 15)],
                          guides={(-2, -35): (True, False), (3, 15): (True, True)}, xt=[(-2, '-2'), (3, '3')], yt=[(15, '18-k')], crange=(-2.3, 5.75))),
}
def case28(a, ticks):
    f = lambda x: -0.25*(x-a)**2 + 3.6
    w = ((3.6 - 0.3) / 0.25) ** 0.5
    lo, hi = max(a - w, min(a, -1) - 1.0), min(a + w, max(a, 1) + 1.0)
    def g():
        F = qplot(f, (-1, 1), (min(a, -1)-1.3, max(a, 1)+1.3), (-0.4, 4.2), 52, 52, pts=[(-1, f(-1)), (1, f(1))], yaxis=False,
                  xt=ticks, crange=(lo, hi), origin=False)
        F.dashed((a, f(a)), (a, 0))
        return F.render()
    return g
figs['img16'] = case28(-2.2, [(-2.2, 'a'), (-1, '-1'), (1, '1')])
figs['img17'] = case28(0.0, [(-1, '-1'), (0, 'a'), (1, '1')])
figs['img18'] = case28(2.2, [(-1, '-1'), (1, '1'), (2.2, 'a')])
for k, fn in figs.items():
    print(k, '폭', fit_shoot(OUT + '/c1_07_%s.png' % k, fn))
