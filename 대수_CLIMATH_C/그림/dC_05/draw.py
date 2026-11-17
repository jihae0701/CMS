# -*- coding: utf-8 -*-
"""대수 C 5. 삼각함수 — 스캔 그림 다시 그리기 (iN = 문서의 imageN)"""
import sys, math
sys.path.insert(0, '/tmp/claude-0/-home-user-CMS/7a122d51-a5b1-5def-9637-d43cb9a9b6ef/scratchpad/figw')
from dcommon import *
from mathfig import right_mark, dim_arc
OUT = sys.argv[1]
M = (16, 16, 16, 16)
r3 = math.sqrt(3)


def dirpt(deg, L=1.0):
    a = math.radians(deg); return (L * math.cos(a), L * math.sin(a))


def gen(total, final, lab_total, lab_final, turns_r=14):
    F = Frame((-1.25, 1.25), (-1.05, 1.05), 120, 120, M)
    F.axes(); O(F, 'rt', -6, 4)
    ray(F, (0, 0), dirpt(final, 1.1))
    e = spiral(F, total, r0=12, dr=6)
    return F


def i2():
    F = gen(510, 150, '', '')
    F.lab(angpt(F, 120, 44), '150^{\\circ}', 'lb', 6, -2); F.lab(angpt(F, -60, 34), '510^{\\circ}', 'lt', 2, 2)
    return F.render()


def i3():
    F = gen(1290, 210, '', '')
    F.lab(angpt(F, 150, 50), '210^{\\circ}', 'rb', -4, -2); F.lab(angpt(F, -40, 46), '1290^{\\circ}', 'lt', 4, 2)
    return F.render()


def i4():
    F = gen(-750, -30, '', '')
    F.lab(angpt(F, 40, 40), '-750^{\\circ}', 'lb', 4, -2); F.lab(angpt(F, -60, 40), '-30^{\\circ}', 'lt', 6, 2)
    return F.render()


def i5():
    F = gen(-1050, 30, '', '')
    F.lab(angpt(F, 150, 50), '-1050^{\\circ}', 'rb', -2, -2); F.lab(angpt(F, 10, 46), '30^{\\circ}', 'lc', 8, 0)
    return F.render()


def ox(deg, name):
    F = Frame((-1.0, 1.4), (-1.0, 1.1), 110, 110, M)
    ray(F, (0, 0), (1.25, 0)); ray(F, (0, 0), dirpt(deg, 1.05))
    spiral(F, deg, r0=22, dr=0)
    F.pt((0, 0), 'O', 'rt', -4, 6 if deg < 180 else -14)
    F.pt((1.25, 0), 'X', 'lc', 6, 0); F.pt(dirpt(deg, 1.05), 'P', 'rc' if deg < 180 else 'rt', -6, 0 if deg < 180 else 2)
    F.lab(angpt(F, deg / 2, 30), name, 'lb', 4, -4)
    return F


def i6(): return ox(120, '120^{\\circ}').render()
def i7(): return ox(230, '230^{\\circ}').render()


def tri(F, P, legs=True):
    F.seg((0, 0), P); F.dashed(P, (P[0], 0)); F.dashed(P, (0, P[1]))
    fdot(F, P)


def i8():  # 16번 P(-4,3), r=5
    F = Frame((-6.4, 6.4), (-6.2, 6.4), 22, 22, M)
    F.axes(); O(F, 'rt', -4, 4); circ(F, (0, 0), 5)
    P = (-4, 3); tri(F, P); F.seg((-4, 0), (0, 0), 2.0); F.seg((-4, 0), P, 2.0)
    right_mark(F, (-4, 0), (0, 0), P)
    spiral(F, math.degrees(math.atan2(3, -4)), r0=16, dr=0)
    F.pt(P, 'P', 'rb', -4, -4); F.lab((-2, 1.5), '5', 'cb', 0, -4)
    F.lab((0, 3), '3', 'lc', 6, 0); F.lab((-4, 0), '-4', 'ct', 4, 6); F.lab((5, 0), '5', 'lt', 4, 4); F.lab((-5, 0), '-5', 'rt', -2, 4)
    F.lab((0, 5), '5', 'lb', 6, -2); F.lab((0, -5), '-5', 'rt', -6, 4); F.lab(angpt(F, 60, 24), '\\theta', 'lb', 2, -2)
    return F.render()


def i9():  # 19번 다른 풀이 P(-4,-3)
    F = Frame((-5.4, 2.2), (-4.2, 2.2), 34, 34, M)
    F.axes(); O(F, 'lt', 4, 4)
    P = (-4, -3); F.seg((0, 0), P); F.seg((-4, 0), P, 2.0); F.seg((-4, 0), (0, 0), 2.0)
    right_mark(F, (-4, 0), (0, 0), P)
    spiral(F, 360 + math.degrees(math.atan2(-3, -4)), r0=18, dr=0)
    dim_arc(F, (-4, 0), (0, 0), '4', -1); dim_arc(F, (-4, -3), (-4, 0), '3', -1); dim_arc(F, (0, 0), (-4, -3), '5', -1)
    F.lab(angpt(F, 60, 22), '\\theta', 'lb', 2, -2)
    return F.render()


def i10():  # 20번 P(-5,12), r=13
    F = Frame((-16, 16), (-15.5, 16), 9, 9, M)
    F.axes(); O(F, 'lt', 4, 4); circ(F, (0, 0), 13)
    P = (-5, 12); F.poly([(0, 0), (-5, 0), P], PINK); F.seg((0, 0), P); F.seg((-5, 0), P, 2.0); F.seg((-5, 0), (0, 0), 2.0)
    right_mark(F, (-5, 0), (0, 0), P); fdot(F, P)
    spiral(F, math.degrees(math.atan2(12, -5)), r0=14, dr=0)
    F.lab(P, '\\mathrm{P}(-5,\\,12)', 'rb', -4, -4); F.lab((-2.5, 6), '13', 'lc', 6, 0); F.lab((-5, 6), '12', 'rc', -6, 0)
    F.lab((-5, 0), '-5', 'ct', 0, 6); F.lab((13, 0), '13', 'lt', 4, 4); F.lab((-13, 0), '-13', 'rt', -2, 4)
    F.lab((0, 13), '13', 'lb', 6, -2); F.lab((0, -13), '-13', 'rt', -6, 4); F.lab(angpt(F, 55, 20), '\\theta', 'lb', 2, -2)
    return F.render()


def i11():  # 21번 P(1,-√3), r=2
    F = Frame((-2.7, 2.9), (-2.7, 2.6), 56, 56, M)
    F.axes(); O(F, 'rb', -6, -4); circ(F, (0, 0), 2)
    P = (1, -r3); F.poly([(0, 0), (1, 0), P], PINK); F.seg((0, 0), P); F.seg((1, 0), P, 2.0)
    right_mark(F, (1, 0), (0, 0), P); fdot(F, P)
    spiral(F, -60, r0=24, dr=0)
    F.lab(P, '\\mathrm{P}(1,\\,-\\sqrt{3})', 'lt', 6, 2); F.lab((0.5, -0.9), '2', 'rc', -6, 0)
    F.lab((1, 0), '1', 'lb', 4, -2); F.lab((2, 0), '2', 'lt', 4, 4); F.lab((-2, 0), '-2', 'rt', -2, 4)
    F.lab((0, 2), '2', 'lb', 6, -2); F.lab((0, -2), '-2', 'rt', -6, 4); F.lab((1.05, -0.87), '-\\sqrt{3}', 'lc', 8, 0)
    F.lab(angpt(F, -120, 30), '-\\dfrac{\\pi}{3}', 'rt', 0, 0)
    return F.render()


def i12():  # 42번 θ=2π/3, 7θ
    F = Frame((-1.25, 1.25), (-1.05, 1.15), 120, 120, M)
    F.axes(); O(F, 'rt', -6, 4)
    ray(F, (0, 0), dirpt(120, 1.15)); spiral(F, 120, r0=34, dr=0); spiral(F, 840, r0=12, dr=6)
    F.lab(angpt(F, 70, 40), '\\theta', 'lb', 4, -2); F.lab(angpt(F, -50, 34), '7\\theta', 'lt', 4, 2)
    return F.render()


def i13():  # 43번 θ=9π/5(324°), 6θ(1944°)
    F = Frame((-1.25, 1.25), (-1.15, 1.05), 120, 120, M)
    F.axes(); O(F, 'rt', -6, 4)
    ray(F, (0, 0), dirpt(324, 1.15)); ray(F, (0, 0), dirpt(144, 1.15))
    spiral(F, 324, r0=48, dr=0); spiral(F, 1944, r0=10, dr=6)
    F.lab(angpt(F, 270, 50), '\\theta', 'ct', 0, 6); F.lab(angpt(F, 100, 44), '6\\theta', 'rb', -2, -2)
    return F.render()


def i14():  # 45번 α, β (y=x 대칭)
    F = Frame((-0.3, 1.5), (-0.3, 1.5), 140, 140, (16, 16, 60, 16))
    F.axes(); O(F, 'rt', -6, 4)
    F.seg((-0.25, -0.25), (1.4, 1.4)); F.seg((0, 0), dirpt(20, 1.45), 2.0); F.seg((0, 0), dirpt(70, 1.45), 2.0)
    spiral(F, 20, r0=40, dr=0); spiral(F, 70, r0=62, dr=0)
    F.lab(angpt(F, 10, 42), '\\alpha', 'lc', 4, 0); F.lab(angpt(F, 55, 64), '\\beta', 'lb', 4, -2)
    F.lab((1.4, 1.4), 'y=x', 'lc', 6, 0)
    return F.render()


def i15():  # 49번 P(-√2,-1)
    F = Frame((-2.2, 0.9), (-1.9, 0.8), 90, 90, (90, 16, 30, 16))
    F.axes(); O(F, 'lt', 4, 4)
    P = (-math.sqrt(2), -1); ray(F, (0, 0), (P[0] * 1.25, P[1] * 1.25)); fdot(F, P)
    F.dashed(P, (P[0], 0)); F.dashed(P, (0, -1))
    spiral(F, 360 + math.degrees(math.atan2(-1, -math.sqrt(2))), r0=20, dr=0)
    F.lab(P, '\\mathrm{P}(-\\sqrt{2},\\,-1)', 'lt', 8, 10); F.lab((P[0], 0), '-\\sqrt{2}', 'cb', 0, -6)
    F.lab((0, -1), '-1', 'lc', 8, 0); F.lab((-0.7, -0.5), '\\sqrt{3}', 'lt', 6, 4); F.lab(angpt(F, 120, 24), '\\theta', 'rb', -2, -2)
    return F.render()


def i16():  # 51번 P(-2,1)
    F = Frame((-2.9, 0.8), (-0.5, 1.6), 90, 90, (16, 16, 30, 16))
    F.axes(); O(F, 'rt', -6, 4)
    P = (-2, 1); ray(F, (0, 0), (-2.5, 1.25)); fdot(F, P)
    F.dashed(P, (-2, 0)); F.dashed(P, (0, 1))
    spiral(F, math.degrees(math.atan2(1, -2)), r0=20, dr=0)
    F.lab(P, '\\mathrm{P}(-2,\\,1)', 'lb', 4, -6); F.lab((-2, 0), '-2', 'ct', 0, 6); F.lab((0, 1), '1', 'lc', 8, 0)
    F.lab((-1, 0.5), '\\sqrt{5}', 'lb', 6, -2); F.lab(angpt(F, 60, 22), '\\theta', 'lb', 2, -2)
    return F.render()


def i17():  # 54번 단위원 10등분
    F = Frame((-1.4, 1.5), (-1.35, 1.35), 120, 120, M)
    F.axes(); O(F, 'rt', -6, 4); circ(F, (0, 0), 1)
    for k in range(10):
        p = dirpt(36 * k); fdot(F, p)
        a = 36 * k; X, Y = math.cos(math.radians(a)), math.sin(math.radians(a))
        anc = ('l' if X > 0.3 else 'r' if X < -0.3 else 'c') + ('b' if Y > 0.3 else 't' if Y < -0.3 else 'c')
        F.lab(p, '\\mathrm{P}_{%d}' % k, anc, 8 * (X > 0.3) - 8 * (X < -0.3) + (6 if k == 0 else 0), -8 * (Y > 0.3) + 8 * (Y < -0.3) + (-12 if k == 0 else 0))
    F.seg((0, 0), dirpt(36), 2.0); spiral(F, 36, r0=26, dr=0)
    F.lab(angpt(F, 18, 28), '\\theta', 'lc', 4, 0)
    F.lab((1, 0), '1', 'lt', 4, 6); F.lab((-1, 0), '-1', 'rt', -4, 6); F.lab((0, 1), '1', 'lb', 4, -4); F.lab((0, -1), '-1', 'rt', -4, 4)
    return F.render()


def i18():  # 58번 P(-3,4), r=5
    F = Frame((-6.6, 6.4), (-6.2, 6.4), 22, 22, (90, 16, 16, 16))
    F.axes(); O(F, 'rt', -4, 4); circ(F, (0, 0), 5)
    F.seg((-4.8, 6.4), (4.65, -6.2), 2.0)
    P = (-3, 4); F.dashed(P, (-3, 0)); F.dashed(P, (0, 4)); fdot(F, P)
    right_mark(F, (0, 4), (0, 0), P)
    spiral(F, math.degrees(math.atan2(4, -3)), r0=16, dr=0)
    F.lab(P, '\\mathrm{P}(-3,\\,4)', 'rc', -8, 0); F.lab((-4.8, 6.4), 'y=-\\dfrac{4}{3}x', 'rc', -4, 8)
    F.lab((-1.5, 2), '5', 'rc', -6, 0); F.lab((0, 4), '4', 'lc', 6, 0); F.lab((-3, 0), '-3', 'ct', 2, 6)
    F.lab((5, 0), '5', 'lt', 4, 4); F.lab((-5, 0), '-5', 'rt', -2, 4); F.lab((0, 5), '5', 'lb', 6, -2); F.lab((0, -5), '-5', 'rt', -6, 4)
    F.lab(angpt(F, 70, 24), '\\theta', 'lb', 2, -2)
    return F.render()


def rect(sol):
    F = Frame((-1.5, 1.6), (-1.35, 1.35), 120, 120, (16 if not sol else 110, 16, 110 if sol else 30, 16))
    F.axes(); O(F, 'rt', -6, 4); circ(F, (0, 0), 1)
    A, B = dirpt(20), dirpt(170); C, D = (-A[0], -A[1]), (-B[0], -B[1])
    F.polyline([A, B, C, D, A]); F.seg((0, 0), A, 2.0); F.seg(A, C, 2.0)
    spiral(F, 20, r0=40, dr=0); F.lab(angpt(F, 8, 42), '\\theta', 'lc', 4, 0)
    F.lab((1, 0), '1', 'lt', 4, 6); F.lab((-1, 0), '-1', 'rt', -4, 6); F.lab((0, 1), '1', 'lb', 4, -4); F.lab((0, -1), '-1', 'rt', -4, 4)
    if sol:
        F.lab(A, '\\mathrm{A}(x,\\,y)', 'lb', 6, -2); F.lab(C, '\\mathrm{C}(-x,\\,-y)', 'rt', -6, 2)
    else:
        F.pt(A, 'A', 'lb', 6, -2); F.pt(C, 'C', 'rt', -6, 2)
    F.pt(B, 'B', 'rb', -6, -2); F.pt(D, 'D', 'lt', 6, 2)
    return F


def i19(): return rect(True).render()
def i20(): return rect(False).render()


JOBS = {k: v for k, v in globals().items() if k[0] == 'i' and k[1:].isdigit()}
if __name__ == '__main__':
    run(JOBS, OUT, sys.argv[2:])
