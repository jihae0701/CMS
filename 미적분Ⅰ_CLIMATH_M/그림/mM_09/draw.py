# -*- coding: utf-8 -*-
"""미적분Ⅰ M 9. 정적분으로 정의된 함수 — C에 없던 스캔 그림 다시 그리기 (iN = 문서의 imageN).  python3 draw.py 출력폴더 [이름...]"""
import sys, math
sys.path.insert(0, '/home/user/CMS/.claude/skills/math-figure-rules'); sys.path.insert(0, '/tmp/claude-0/-home-user-CMS/7a122d51-a5b1-5def-9637-d43cb9a9b6ef/scratchpad/figw')
from mathfig import Frame, SKY, PINK
from mjcommon import odot, fdot, plot, axes2, O, run, herm
OUT = sys.argv[1]
M = (16, 16, 16, 16)

fp = lambda x: x * (x + 1) * (x - 2)                       # f'(x) 꼴
G = lambda x: x ** 4 / 4 - x ** 3 / 3 - x * x               # 그 원시함수(원점 지남)


def i6():   # 25번 문제 f(x)=-x(x-4)
    F = Frame((-0.8, 5.4), (-0.9, 4.8), 55, 55, M)
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, lambda x: -x * (x - 4), -0.2, 4.2)
    F.dashed((2, 0), (2, 4)); F.dashed((0, 4), (2, 4))
    F.lab((2, 0), '2', 'ct', 0, 8); F.lab((4, 0), '4', 'rt', -4, 6); F.lab((0, 4), '4', 'rc', -8, 0)
    F.lab((2.6, 3.64), 'y=f(x)', 'lb', 6, -4)
    return F.render()


def i7():   # 26번 문제 f(x)=k(x+1)(x-3)
    f = lambda x: 0.5 * (x + 1) * (x - 3)
    F = Frame((-2.0, 5.8), (-2.4, 2.4), 55, 55, M)
    F.axes(); O(F, 'lt', 4, 4)
    plot(F, f, -1.6, 3.75)
    F.lab((-1, 0), '-1', 'rt', -4, 6); F.lab((3, 0), '3', 'lt', 4, 6)
    F.lab((3.75, f(3.75)), 'y=f(x)', 'lc', 8, 0)
    return F.render()


def i12():  # 43번 문제 y=|f'(x)|
    s = 0.9
    F = Frame((-1.9, 4.0), (-0.6, 3.4), 65, 65, M)
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, lambda x: s * abs(fp(x)), -1.42, 2.4, n=400)
    F.lab((-1, 0), '-1', 'ct', 0, 8); F.lab((2, 0), '2', 'ct', 0, 8)
    F.lab((2.4, s * abs(fp(2.4))), "y=|f'(x)|", 'lc', 8, 0)
    return F.render()


def two(f1, f2, lab1, lab2, yr, s1, s2, marks=None):
    F = Frame((-1.9, 9.2), yr, 55, 55, M)
    ox = 5.3
    axes2(F, 0, -1.9, 3.1, yr[0], yr[1]); O(F, 'rt', -6, 4)
    axes2(F, ox, ox - 1.9, ox + 2.6, yr[0], yr[1]); F.pt((ox, 0), 'O', 'rt', -6, 4)
    for o, f, lab, (a, b) in ((0, f1, lab1, s1), (ox, f2, lab2, s2)):
        plot(F, lambda x: f(x - o), o + a, o + b, n=300)
        F.lab((o - 1, 0), '-1', 'cb', -6, -8); F.lab((o + 2, 0), '2', 'cb', 6, -8)
        F.lab((o + b, f(b)), lab, 'lc' if f(b) > 0 else 'rc', 6 if f(b) > 0 else -10, 0)
    return F


def i9():   # 43번 해설 y=f'(x) 두 가지
    F = two(lambda x: 0.8 * fp(x), lambda x: -0.8 * fp(x), "y=f'(x)", "y=f'(x)", (-2.4, 2.6), (-1.45, 2.35), (-1.45, 2.35))
    return F.render()


def i10():  # 43번 해설 y=g(x) 두 가지 (원점 지남)
    F = two(lambda x: 0.9 * G(x), lambda x: -0.9 * G(x), 'y=g(x)', 'y=g(x)', (-2.8, 2.8), (-1.55, 3.0), (-1.55, 2.95))
    F.dashed((2, 0), (2, 0.9 * G(2))); F.dashed((5.3 + 2, 0), (5.3 + 2, -0.9 * G(2)))
    return F.render()


def i11():  # 43번 해설 y=g'(x), y=g(x)와 직선 y=g(-1)
    ox = 5.3
    F = two(lambda x: -0.8 * fp(x), lambda x: -0.9 * G(x), "y=g'(x)", 'y=g(x)', (-2.4, 2.8), (-1.45, 2.35), (-1.55, 2.95))
    c = -0.9 * G(-1)
    F.seg((ox - 1.8, c), (ox + 3.0, c), 2.0)
    F.dashed((ox + 2, 0), (ox + 2, -0.9 * G(2)))
    F.lab((ox - 1.8, c), 'g(-1)', 'lb', 0, -6)
    return F.render()


fa = lambda x, a=math.sqrt(6): 0.45 * (x + 1) * (x - 1) * (x - a)


def i14():  # 45번 해설 f(x)=(x+1)(x-1)(x-a)
    a = math.sqrt(6)
    F = Frame((-1.9, 3.6), (-1.9, 2.6), 70, 70, M)
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, fa, -1.45, 3.05)
    F.lab((-1, 0), '-1', 'rb', -4, -4); F.lab((1, 0), '1', 'lt', 4, 6); F.lab((a, 0), 'a', 'rt', -4, 6)
    F.lab((3.05, fa(3.05)), 'y=f(x)', 'rc', -10, 0)
    return F.render()


def i15():  # 45번 해설 넓이 ∫_0^1 f, ∫_1^a f
    a = math.sqrt(6); n = 60
    F = Frame((-1.9, 3.6), (-2.6, 2.6), 70, 70, M)
    F.poly([(0, 0)] + [(i / n, fa(i / n)) for i in range(n + 1)], SKY)
    F.poly([(1, 0)] + [(1 + (a - 1) * i / n, fa(1 + (a - 1) * i / n)) for i in range(n + 1)], PINK)
    F.axes(); O(F, 'rt', -6, 4)
    plot(F, fa, -1.45, 3.05)
    F.lab((-1, 0), '-1', 'rb', -4, -4); F.lab((1, 0), '1', 'cb', 4, -8); F.lab((a, 0), 'a', 'lb', 6, -4)
    F.lab((3.05, fa(3.05)), 'y=f(x)', 'rc', -10, 0)
    F.leader((0.4, 0.25), (0.25, -1.4)); F.lab((0.25, -1.4), '\\displaystyle\\int_0^1 f(x)\\,dx', 'rt', 10, 0)
    F.leader((1.8, -0.35), (2.0, 1.0)); F.lab((2.0, 1.0), '\\displaystyle\\int_1^a f(x)\\,dx', 'rb', 10, -2)
    return F.render()


JOBS = {k: v for k, v in globals().items() if k[0] == 'i' and k[1:].isdigit()}
if __name__ == '__main__':
    run(JOBS, OUT, sys.argv[2:], wide=('i9', 'i10', 'i11'))
