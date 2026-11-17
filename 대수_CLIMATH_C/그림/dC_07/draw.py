# -*- coding: utf-8 -*-
"""대수 C 7. 삼각함수의 활용 — 스캔 그림 다시 그리기 (iN = 문서의 imageN, i35 = 2번 해설 새 그림)"""
import sys, math
sys.path.insert(0, '/tmp/claude-0/-home-user-CMS/7a122d51-a5b1-5def-9637-d43cb9a9b6ef/scratchpad/figw')
from geo import *
OUT = sys.argv[1]
r2, r3 = math.sqrt(2), math.sqrt(3)


def tri(A, B, C, s, fill=None):
    pts = [A, B, C]; F = frame(pts, s); poly(F, pts, fill); c = cen(pts)
    for p, n in zip(pts, 'ABC'): name(F, p, n, c)
    return F, c


def i2():  # 1번 해설: b=10, c=10√3, C=120°
    B, C = (0, 0), (10, 0); A = P(10, 60, C)
    F, c = tri(A, B, C, 26)
    dim(F, A, B, '10\\sqrt{3}', c); dim(F, C, A, '10', c); dim(F, B, C, 'a', c)
    ang(F, C, B, A, 18, '120' + DEG, 40); ang(F, B, C, A, 34)
    return F.render()


def i35():  # 2번 해설: B=60°, C=45°, b=2√3, 외접원 R
    B, C = (0, 0), (4 * math.sin(math.radians(75)), 0)
    A = P(2 * r2, 60, B); O = (C[0] / 2, math.sqrt(4 - (C[0] / 2) ** 2))
    pts = [A, B, C, P(2, 90, O), P(2, 270, O), P(2, 0, O), P(2, 180, O)]
    F = frame(pts, 70); circle(F, O, 2); poly(F, [A, B, C]); c = O
    for p, n in zip((A, B, C), 'ABC'): name(F, p, n, c)
    dot(F, O); name(F, O, 'O', A, 8, (0.5, 0.7))
    clab(F, C, A, '2\\sqrt{3}', B, 34); clab(F, A, B, 'c', C, 14)
    ang(F, B, C, A, 26, '60' + DEG, 50); ang(F, C, B, A, 26, '45' + DEG, 52)
    seg(F, O, B, 1.5); F.lab(lerp(O, B, 0.5), 'R', 'cb', 0, -6)
    return F.render()


def i3():  # 16번 해설
    B, C = (0, 0), (6, 0); A = (2, 2 * r3)
    F, c = tri(A, B, C, 48)
    dim(F, A, B, '4', c); dim(F, C, A, '2\\sqrt{7}', c); dim(F, B, C, 'a', c)
    ang(F, B, C, A, 24, '60' + DEG, 44)
    return F.render()


def i4():  # 18번 해설
    a = math.sqrt(6); B, C = (0, 0), (a, 0); A = (1.932, 1.932)
    F, c = tri(A, B, C, 110)
    dim(F, A, B, '\\sqrt{3}+1', c); dim(F, C, A, '2', c); dim(F, B, C, '\\sqrt{6}', c)
    return F.render()


def i5():  # 20번 해설: AB=6, AC=4
    a = math.sqrt(28); B, C = (0, 0), (a, 0); x = 48 / (2 * a); A = (x, math.sqrt(36 - x * x))
    F, c = tri(A, B, C, 48)
    dim(F, A, B, '6', c); dim(F, C, A, '4', c); ang(F, A, B, C, 22)
    return F.render()


def i6():  # 22번 문제
    C, D = (0, 0), (5, 0); B = P(3, 120)
    # A: AB=3, AD=8 (BD 바깥쪽)
    bd = math.dist(B, D); x = (9 - 64 + bd * bd) / (2 * bd); h = math.sqrt(9 - x * x)
    ux, uy = (D[0] - B[0]) / bd, (D[1] - B[1]) / bd
    A = (B[0] + ux * x - uy * h, B[1] + uy * x + ux * h)
    pts = [A, B, C, D]; F = frame(pts, 46); poly(F, pts, PINK); seg(F, B, D); c = cen(pts)
    for p, n in zip(pts, 'ABCD'): name(F, p, n, c)
    dim(F, A, B, '3', c); dim(F, B, C, '3', c); dim(F, C, D, '5', c); dim(F, D, A, '8', c)
    ang(F, C, D, B, 20, '120' + DEG, 42)
    return F.render()


def rot_base(pts, i, j):
    """pts[i]→pts[j]가 가로가 되도록 돌린다"""
    a = math.degrees(math.atan2(pts[j][1] - pts[i][1], pts[j][0] - pts[i][0]))
    return rot(pts, -a)


def i7():  # 23번 문제: A=120°, AD 이등분, AD=4, AC=12
    A = (0, 0); D = (0, -4); C = P(12, 330); B = P(6, 210)
    A, B, C, D = rot_base([A, B, C, D], 1, 2)
    F, c = tri(A, B, C, 30); seg(F, A, D); name(F, D, 'D', A, 10)
    dim(F, C, A, '12', c); clab(F, A, D, '4', C, 12, 0.72)
    ang(F, A, B, D, 26, '60' + DEG, 50); ang(F, A, D, C, 34, '60' + DEG, 56)
    return F.render()


def i8():  # 27번 문제
    A, B = (0, 0), (4, 0); D = P(2, 60); C = P(3, 120, B)
    pts = [A, B, C, D]; F = frame(pts, 60); poly(F, pts, GREEN); seg(F, B, D); c = cen(pts)
    for p, n in zip(pts, 'ABCD'): name(F, p, n, c)
    dim(F, A, B, '4', c); dim(F, B, C, '3', c); dim(F, D, A, '2', c)
    ang(F, A, B, D, 24, '60' + DEG, 46); ang(F, B, D, C, 40, '30' + DEG, 62)
    return F.render()


def cyc(chords, start, R):
    """원 위 점들: start(도)에서 시작해 현 길이대로 시계 반대 방향"""
    pts = [P(R, start)]; a = start
    for L in chords[:-1]:
        a += math.degrees(2 * math.asin(L / (2 * R))); pts.append(P(R, a))
    return pts


def i9():  # 28번 해설
    R = 2.0026; A, B, C, D = cyc([1, 2, 3, 4], 165, R)
    F = frame([P(R, k * 90) for k in range(4)], 66); circle(F, (0, 0), R)
    poly(F, [A, B, C, D], LAVENDER); seg(F, A, C)
    for p, n in zip((A, B, C, D), 'ABCD'): name(F, p, n, (0, 0))
    c = cen([A, B, C, D])
    clab(F, A, B, '1', c); clab(F, B, C, '2', c, 12, 0.3); clab(F, C, D, '3', c); clab(F, D, A, '4', c)
    ang(F, B, A, C, 22, '\\theta', 40); ang(F, D, C, A, 30, '180' + DEG + '-\\theta', 88)
    return F.render()


def c29():
    C = (0, 0); A = P(10, 210); B = P(12, 330); D = inter(A, B, C, (0, -1))
    return rot_base([A, B, C, D], 0, 1)


def i10():  # 29번 해설
    A, B, C, D = c29(); F, c = tri(A, B, C, 26); seg(F, C, D); name(F, D, 'D', C, 10)
    dim(F, C, A, '10', c); dim(F, B, C, '12', c); clab(F, C, D, 'x', A, 12, 0.72)
    ang(F, C, A, D, 26, '60' + DEG, 52); ang(F, C, D, B, 32, '60' + DEG, 56)
    return F.render()


def i11():  # 29번 문제
    A, B, C, D = c29(); F, c = tri(A, B, C, 26); seg(F, C, D); name(F, D, 'D', C, 10)
    dim(F, C, A, '10', c); dim(F, B, C, '12', c)
    ang(F, C, A, B, 20); X0, Y0 = F.P(*C); a = _mid(F, C, D, B); F.labels.append((X0 + 52 * math.cos(a), Y0 - 52 * math.sin(a), '120' + DEG, 22, 'cc'))
    for M in (lerp(D, A, 0.04), lerp(D, B, 0.04)):
        pass
    X, Y = F.P(*C)
    for k in (-1, 1):  # 같은 두 각 표시(점)
        a = _mid(F, C, A if k < 0 else B, D)
        F.svg.append('<circle cx="%.1f" cy="%.1f" r="2.6" fill="#000"/>' % (X + 14 * math.cos(a), Y - 14 * math.sin(a)))
    return F.render()


def _mid(F, V, A, B):
    import geo
    a1, a2 = geo._dir(F, V, A), geo._dir(F, V, B)
    d = (a2 - a1 + 3 * math.pi) % (2 * math.pi) - math.pi
    return a1 + d / 2


def i12():  # 30번 해설: 평행사변형
    a = (math.sqrt(15) - r3) / 2; b = (math.sqrt(15) + r3) / 2
    B, C = (0, 0), (b, 0); A = P(a, 60); D = (A[0] + b, A[1])
    pts = [A, B, C, D]; F = frame(pts, 120); poly(F, pts, PINK); seg(F, A, C, 1.6); seg(F, B, D, 1.6); c = cen(pts)
    for p, n in zip(pts, 'ABCD'): name(F, p, n, c)
    dim(F, A, B, 'a', c); dim(F, B, C, 'b', c)
    clab(F, A, C, '\\sqrt{6}', D, 16, 0.22); clab(F, B, D, '2\\sqrt{3}', C, 18, 0.78)
    ang(F, B, C, A, 22, '60' + DEG, 44)
    return F.render()


def i13():  # 33번 문제: 대각선 4, 6, 끼인각 θ
    th = math.degrees(math.acos(1 / 3)); E = (0, 0)
    B, D = P(3.3, 200), P(2.7, 20); A, C = P(1.6, 180 - th + 20), P(2.4, 20 - th)
    pts = [A, B, C, D]; F = frame(pts, 58); poly(F, pts, YELLOW); seg(F, A, C); seg(F, B, D); c = cen(pts)
    for p, n in zip(pts, 'ABCD'): name(F, p, n, c)
    clab(F, B, D, '6', C, 14, 0.3); clab(F, A, C, '4', B, 14, 0.25)
    ang(F, E, C, D, 18, '\\theta', 36)
    return F.render()


def c36():
    R = 2.0817; return R, cyc([1, 4, 3, 3], 160, R)


def i14():  # 36번 해설
    R, (A, B, C, D) = c36(); F = frame([P(R, k * 90) for k in range(4)], 62); circle(F, (0, 0), R)
    poly(F, [A, B, C, D]); seg(F, B, D, 1.5)
    for p, n in zip((A, B, C, D), 'ABCD'): name(F, p, n, (0, 0))
    c = cen([A, B, C, D])
    clab(F, D, A, '3', c); clab(F, A, B, '1', c, 12); clab(F, C, D, '3', c); clab(F, B, C, 'x', c)
    ang(F, A, B, D, 16, '120' + DEG, 52); ang(F, C, D, B, 22, '60' + DEG, 44)
    return F.render()


def i15():  # 36번 문제
    R, (A, B, C, D) = c36(); F = frame([P(R, k * 90) for k in range(4)], 62); circle(F, (0, 0), R)
    poly(F, [A, B, C, D])
    for p, n in zip((A, B, C, D), 'ABCD'): name(F, p, n, (0, 0))
    c = cen([A, B, C, D])
    clab(F, D, A, '3', c); clab(F, A, B, '1', c, 12); clab(F, C, D, '3', c)
    ang(F, A, B, D, 16, '120' + DEG, 46)
    return F.render()


def c37():
    R = 2 * math.sqrt(7) / r3; return R, cyc([4, 6, 2, 4], 100, R)


def i16():  # 37번 해설
    R, (A, B, C, D) = c37(); F = frame([P(R, k * 90) for k in range(4)], 40); circle(F, (0, 0), R)
    poly(F, [A, B, C, D]); seg(F, A, C, 1.5)
    for p, n in zip((A, B, C, D), 'ABCD'): name(F, p, n, (0, 0))
    c = cen([A, B, C, D])
    clab(F, A, B, '4', c); clab(F, D, A, '4', c); clab(F, C, D, '2', c, 12)
    ang(F, B, C, A, 22, '60' + DEG, 44)
    return F.render()


def i17():  # 37번 문제
    R, (A, B, C, D) = c37(); F = frame([P(R, k * 90) for k in range(4)], 40); circle(F, (0, 0), R)
    poly(F, [A, B, C, D])
    for p, n in zip((A, B, C, D), 'ABCD'): name(F, p, n, (0, 0))
    c = cen([A, B, C, D])
    clab(F, A, B, '4', c); clab(F, D, A, '4', c); clab(F, C, D, '2', c, 12)
    ang(F, B, C, A, 22, '60' + DEG, 44)
    return F.render()


def i18():  # 38번 문제
    B, C, D = (0, 0), (7, 0), (2, 0); x = 33 / 14; A = (x, math.sqrt(9 - x * x))
    F, c = tri(A, B, C, 50); seg(F, A, D); name(F, D, 'D', A, 10)
    dim(F, A, B, '3', c); dim(F, C, A, '5', c); dim(F, B, D, '2', A, 10); dim(F, D, C, '5', A, 10)
    return F.render()


def i19():  # 39번 해설: 전개도
    O = (0, 0); A, B, A2 = P(3, 210), P(3, 270), P(3, 330); Pp = P(2, 270); K = P(4.05, 307)
    F = frame([O, A, A2, B, (K[0] + 1, K[1] - 1), (K[0] - 1, K[1])], 52)
    seg(F, O, A, 2.6); seg(F, O, A2, 2.6); arc(F, O, 3, 210, 330); seg(F, O, B, 2.6); seg(F, A, Pp, 1.8)
    circle(F, K, 1, 2.6); dot(F, K); seg(F, K, (K[0] + 1, K[1]), 2.0); F.lab((K[0] + 0.5, K[1]), '1', 'ct', 0, 6)
    name(F, O, 'O', B, 10); name(F, A, 'A', O, 10, (-1, 0)); name(F, A2, "A'", O, 10, (1, 0)); name(F, B, 'B', O, 8, (0, 1))
    name(F, Pp, 'P', A2, 8, (-1, 0.2))
    dim(F, O, A, '3', B, 10); dim(F, O, Pp, '2', A, 10); dim(F, Pp, B, '1', A, 6)
    ang(F, O, A, B, 26, '\\theta', 44)
    arc(F, O, 3.35, 213, 267, 1.3); F.lab(P(3.35, 240), '\\pi', 'rt', -4, 4)
    return F.render()


def i20():  # 39번 문제: 원뿔
    h = math.sqrt(8); O = (0, h); ry = 0.3
    base = lambda psi: (math.cos(psi), ry * math.sin(psi))
    A, B = base(math.pi), base(0); M = (0, 0)
    F = frame([O, A, B, (0, -ry), (0, ry)], 64, (46, 40, 46, 40))
    F.poly([A, O, B] + [base(-math.pi * i / 60) for i in range(61)][::-1], GREEN)
    pts = [base(math.pi + math.pi * i / 60) for i in range(61)]
    F.svg.append('<polyline points="%s" fill="none" stroke="#000" stroke-width="2.6"/>' % ' '.join('%.1f,%.1f' % F.P(*p) for p in pts))
    pts = [base(math.pi * i / 60) for i in range(61)]
    F.svg.append('<polyline points="%s" fill="none" stroke="#000" stroke-width="1.5" %s/>' % (' '.join('%.1f,%.1f' % F.P(*p) for p in pts), DASH))
    seg(F, O, A, 2.6); seg(F, O, B, 2.6); seg(F, M, B, 1.8); dot(F, M)
    Pp = lerp(O, B, 2 / 3); dot(F, Pp)
    # 최단 경로(전개도의 직선)
    a0, p0 = (3, 0.0), (2, math.pi / 3)
    X0, Y0 = a0[0], 0.0; X1, Y1 = 2 * math.cos(p0[1]), 2 * math.sin(p0[1])
    path = []
    for i in range(81):
        x, y = X0 + (X1 - X0) * i / 80, Y0 + (Y1 - Y0) * i / 80
        s, ph = math.hypot(x, y), math.atan2(y, x)
        q = base(math.pi + 3 * ph); path.append((O[0] + s / 3 * (q[0] - O[0]), O[1] + s / 3 * (q[1] - O[1])))
    F.svg.append('<polyline points="%s" fill="none" stroke="#000" stroke-width="1.8"/>' % ' '.join('%.1f,%.1f' % F.P(*p) for p in path))
    name(F, O, 'O', M, 8, (0, -1)); name(F, A, 'A', O, 10, (-1, 0)); name(F, B, 'B', O, 10, (1, 0)); name(F, Pp, 'P', M, 10, (1, 0))
    dim(F, A, O, '3', B, 18); F.lab(lerp(M, B, 0.5), '1', 'ct', 0, 6)
    return F.render()


def c40():
    R = 6 * r3; O = (0, 0); S, A, Pp, B, T = P(R, 120), P(R, 100), P(R, 80), P(R, 40), P(R, 0)
    Q = inter(S, T, O, A); Rr = inter(S, T, O, B)
    return O, S, A, Pp, B, T, Q, Rr


def i21():  # 40번 해설
    O, S, A, Pp, B, T, Q, Rr = c40(); R = 6 * r3
    F = frame([O, S, T, P(R, 60)], 26)
    arc(F, O, R, 0, 120); seg(F, O, S, 2.2); seg(F, O, T, 2.2); seg(F, O, A, 2.2); seg(F, O, B, 2.2); seg(F, O, Pp, 1.4)
    seg(F, S, T, 1.4); seg(F, S, Q, 2.2); seg(F, Q, Rr, 2.2); seg(F, Rr, T, 2.2); seg(F, Pp, Q, 2.2); seg(F, Pp, Rr, 2.2)
    for p, n in ((S, 'S'), (A, 'A'), (Pp, 'P'), (B, 'B'), (T, 'T')): name(F, p, n, O)
    name(F, O, 'O', P(1, 60), 10); name(F, Q, 'Q', T, 10, (-1, 0.3)); name(F, Rr, 'R', O, 10, (0.3, 1))
    omark(F, S, Q); omark(F, Pp, Q); tick(F, Pp, Rr); tick(F, Rr, T)
    ang(F, O, S, A, 40, '\\alpha', 66); ang(F, O, A, Pp, 54, '\\alpha', 84); ang(F, O, Pp, B, 40, '\\beta', 64); ang(F, O, B, T, 54, '\\beta', 82)
    dim(F, O, S, '6\\sqrt{3}', T, 12); dim(F, O, T, '6\\sqrt{3}', S, 12)
    return F.render()


def i22():  # 40번 문제
    R = 6 * r3; O = (0, 0); A, B, Pp = P(R, 60), P(R, 0), P(R, 35); Q, Rr = lerp(O, A, 0.5), lerp(O, B, 0.62)
    F = frame([O, A, B, P(R, 30)], 22)
    arc(F, O, R, 0, 60); seg(F, O, A, 2.2); seg(F, O, B, 2.2); poly(F, [Pp, Q, Rr], None, 2.2)
    name(F, O, 'O', P(1, 30), 10); name(F, A, 'A', O); name(F, B, 'B', O); name(F, Pp, 'P', O)
    name(F, Q, 'Q', B, 10, (-0.9, -0.4)); name(F, Rr, 'R', A, 10, (0, 1))
    ang(F, O, B, A, 22, '60' + DEG, 46); dim(F, O, B, '6\\sqrt{3}', A, 12)
    return F.render()


def tetra(F, O, A, B, C, Pp, Q, R, path=True):
    poly(F, [O, A, B, C], YELLOW) if False else None
    for p, q in ((O, A), (O, B), (O, C), (A, B), (B, C)): seg(F, p, q, 2.4)
    seg(F, A, C, 1.6, True)
    if path:
        seg(F, A, Pp, 2.0); seg(F, Pp, Q, 2.0); seg(F, Q, R, 1.8, True)
    c = cen([O, A, B, C])
    for p, n in ((O, 'O'), (A, 'A'), (B, 'B'), (C, 'C')): name(F, p, n, c)
    name(F, R, 'R', c, 10, (-1, -0.3)); name(F, Q, 'Q', c, 8, (1, -0.25)); name(F, Pp, 'P', c, 8, (0.7, 0.6))
    tick(F, O, R, 2); tick(F, R, A, 2)
    dim(F, O, C, '8', A, 40)


def net41():
    O = (0, 0); A, B, C, A2 = P(8, 210), P(8, 250), P(8, 290), P(8, 330); R = P(4, 330)
    Pp = inter(A, R, O, B); Q = inter(A, R, O, C)
    return O, A, B, C, A2, R, Pp, Q


def tet_pts(sh=(0, 0)):
    O, A, B, C = (0, 7.0), (-4.6, 1.3), (-0.2, -2.6), (3.4, 1.4)
    _, _, _, _, _, _, Pn, Qn = net41()
    tP, tQ = math.hypot(*Pn) / 8, math.hypot(*Qn) / 8
    Pp, Q, R = lerp(O, B, tP), lerp(O, C, tQ), lerp(O, A, 0.5)
    return [(p[0] + sh[0], p[1] + sh[1]) for p in (O, A, B, C, Pp, Q, R)]


def i23():  # 41번 해설: 정삼각뿔과 전개도
    O, A, B, C, Pp, Q, R = tet_pts((-14.5, -5.5))
    On, An, Bn, Cn, A2, Rn, Pn, Qn = net41()
    F = frame([O, A, B, C, An, A2, Bn, Cn, On], 34)
    tetra(F, O, A, B, C, Pp, Q, R)
    # 전개도
    for p in (An, Bn, Cn, A2): seg(F, On, p, 2.4)
    for p, q in ((An, Bn), (Bn, Cn), (Cn, A2)): seg(F, p, q, 2.4)
    seg(F, An, Rn, 2.0)
    c = (0, -4)
    for p, n in ((An, 'A'), (Bn, 'B'), (Cn, 'C'), (A2, "A'")): name(F, p, n, c)
    name(F, On, 'O', c, 8); name(F, Pn, 'P', c, 10, (-1, 0.6)); name(F, Qn, 'Q', c, 10, (1, 0.6)); name(F, Rn, 'R', c, 8, (0.6, -0.8))
    tick(F, On, Rn, 2); tick(F, Rn, A2, 2)
    ang(F, On, An, Bn, 26, '40' + DEG, 74); ang(F, On, Bn, Cn, 30, '40' + DEG, 76); ang(F, On, Cn, A2, 26, '40' + DEG, 74)
    dim(F, On, An, '8', Bn, 12)
    # 화살표
    X0, Y = F.P(-9.6, -2.6); X1, _ = F.P(-8.0, -2.6)
    F.svg.append('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="#bbb"/>'
                 % (X0, Y - 6, X1 - 12, Y - 6, X1 - 12, Y - 13, X1, Y, X1 - 12, Y + 13, X1 - 12, Y + 6, X0, Y + 6))
    return F.render()


def i24():  # 41번 문제
    O, A, B, C, Pp, Q, R = tet_pts()
    F = frame([O, A, B, C], 56)
    F.poly([O, A, B, C], YELLOW)
    tetra(F, O, A, B, C, Pp, Q, R)
    return F.render()


def c42():
    return (3, 3), (0, 0), (3 + r3, 0), (3, 0)


def i25():  # 42번 해설
    A, B, C, H = c42(); F, c = tri(A, B, C, 54); seg(F, A, H); name(F, H, 'H', A, 10, (-0.7, -0.7)); right_mark(F, H, A, C, 0.22)
    dim(F, A, B, 'c', c); dim(F, C, A, '2\\sqrt{3}', c); dim(F, B, C, 'a', c)
    ang(F, B, C, A, 24, '45' + DEG, 46); ang(F, C, A, B, 22, '60' + DEG, 44); ang(F, A, B, C, 20); X0, Y0 = F.P(*A); a = _mid(F, A, B, H); F.labels.append((X0 + 54 * math.cos(a), Y0 - 44 * math.sin(a), '75' + DEG, 22, 'cc'))
    return F.render()


def i26():  # 42번 문제
    A, B, C, H = c42(); F, c = tri(A, B, C, 54)
    dim(F, C, A, '2\\sqrt{3}', c)
    ang(F, B, C, A, 24, '45' + DEG, 46); ang(F, A, B, C, 20, '75' + DEG, 40)
    return F.render()


def i27():  # 43번 문제
    R = 4 * r3; O = (0, 0); B, D = (-R, 0), (R, 0); A, C = P(R, 100), P(R, -140)
    F = frame([P(R, k * 90) for k in range(4)], 18); circle(F, O, R)
    poly(F, [A, B, C, D]); seg(F, B, D, 1.5, True); seg(F, A, C, 1.6)
    for p, n in zip((A, B, C, D), 'ABCD'): name(F, p, n, O)
    ang(F, B, A, D, 30, '50' + DEG, 56); ang(F, B, D, C, 22, '70' + DEG, 46); ang(F, D, A, B, 30, '40' + DEG, 56)
    F.lab(lerp(B, D, 0.62), '8\\sqrt{3}', 'cb', 0, -8)
    return F.render()


def c44():
    B, C, E = (0, 0), (8, 0), (4, 0); D = P(3, math.degrees(math.acos(3 / 8)), E); A = (D[0] - 4, D[1])
    return A, B, C, D, E


def i28():  # 44번 문제
    A, B, C, D, E = c44(); pts = [A, B, C, D]; F = frame(pts, 46); poly(F, pts); seg(F, B, D); c = cen(pts)
    for p, n in zip(pts, 'ABCD'): name(F, p, n, c)
    dim(F, A, B, '3', c); dim(F, B, C, '8', c); dim(F, C, D, '4', c); dim(F, D, A, '4', c)
    return F.render()


def i29():  # 44번 해설
    A, B, C, D, E = c44(); pts = [A, B, C, D]; F = frame(pts, 52); poly(F, pts); seg(F, B, D); seg(F, D, E); c = cen(pts)
    for p, n in zip(pts, 'ABCD'): name(F, p, n, c)
    name(F, E, 'E', D, 10)
    dim(F, A, B, '3', c); dim(F, C, D, '4', c); dim(F, D, A, '4', c); dim(F, D, E, '3', B, 8)
    dim(F, B, E, '4', A, 10); dim(F, E, C, '4', A, 10); dim(F, B, C, '8', A, 34)
    ang(F, A, D, B, 22, '\\theta', 40); ang(F, E, D, B, 18, '\\theta', 36)
    return F.render()


def c46():
    O = (0, 0); return O, P(2, 90), P(2, 180), P(2, 300)


def i30():  # 46번 해설
    O, A, B, C = c46(); F = frame([P(2, k * 90) for k in range(4)], 70); circle(F, O, 2)
    poly(F, [A, B, C], '#e4e4f4'); seg(F, O, A, 1.5); seg(F, O, B, 1.5); seg(F, O, C, 1.5); dot(F, O)
    for p, n in zip((A, B, C), 'ABC'): name(F, p, n, O)
    name(F, O, 'O', A, 26, (0.7, -0.7))
    ang(F, O, A, B, 22, 'x', 42); ang(F, O, B, C, 30, 'y', 52); ang(F, O, C, A, 18, 'z', 36)
    return F.render()


def i31():  # 46번 문제
    O, A, B, C = c46(); F = frame([P(2, k * 90) for k in range(4)], 70); circle(F, O, 2)
    poly(F, [A, B, C], LAVENDER); seg(F, O, A, 1.5); dot(F, O)
    for p, n in zip((A, B, C), 'ABC'): name(F, p, n, O)
    name(F, O, 'O', A, 8, (0, 1)); dim(F, A, O, '2', B, 8)
    return F.render()


def i32():  # 47번 문제
    A = (0, 0); B, C = P(8, 245), P(3, 305); Pp, Q = P(2, 245), P(2, 305)
    F, c = tri(A, B, C, 38); seg(F, Pp, Q, 2.2)
    name(F, Pp, 'P', c, 8, (-1, 0.2)); name(F, Q, 'Q', c, 8, (-0.6, 0.8))
    dim(F, A, B, '8', C); dim(F, A, C, '3', B, 10)
    ang(F, A, B, C, 24, '60' + DEG, 46)
    return F.render()


def i33():  # 48번 해설
    B, C, A = (0, 0), (4, 0), (2.6, 3.8); D, E = lerp(B, A, 0.8), (5, 0)
    pts = [A, B, C, D, E]; F = frame(pts, 50); F.poly([B, E, D], '#e4e4e4'); F.poly([B, C, A], '#e4e4e4')
    poly(F, [A, B, C]); poly(F, [D, B, E])
    c = cen([A, B, C])
    for p, n in ((A, 'A'), (B, 'B')): name(F, p, n, c)
    name(F, C, 'C', A, 10, (0, 1)); name(F, D, 'D', E, 10, (0.2, 1)); name(F, E, 'E', A, 10, (1, 0))
    dim(F, B, A, 'c', C); dim(F, B, C, 'a', A, 12)
    return F.render()


def i34():  # 49번 문제
    B, C = (0, 0), (8, 0); A = (4, 4 / r3); Pp = lerp(A, C, 0.3)
    F, c = tri(A, B, C, 40); seg(F, B, Pp); dot(F, Pp); name(F, Pp, 'P', B, 8, (0.5, -0.9))
    dim(F, B, C, '8', A); ang(F, A, B, C, 20, '120' + DEG, 40)
    return F.render()


JOBS = {k: v for k, v in globals().items() if k[0] == 'i' and k[1:].isdigit()}
if __name__ == '__main__':
    run_crop(JOBS, OUT, sys.argv[2:], wide=('i23',))
