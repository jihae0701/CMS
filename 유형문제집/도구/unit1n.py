# -*- coding: utf-8 -*-
# 공통수학1 1단원 다항식의 연산과 항등식 (59문항: STEP 1 46 + 고난도 13). 조립제법은 2단원으로 옮김
# 문항은 unit01.py(1:)·unit02.py(2:)에서 가져온다. v 앞의 "1:"/"2:"로 검산 파일을 가린다.
import importlib.util, os, copy

HERE = os.path.dirname(os.path.abspath(__file__))


def _load(fn):
    sp = importlib.util.spec_from_file_location(fn[:-3], os.path.join(HERE, fn))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


A = _load("unit01.py")
B = _load("unit02.py")
UNIT = ("다항식의 연산과 항등식", "01")


def H(t, kind=1):
    return {"h": t, "kind": kind}


def a(v):
    it = copy.deepcopy(A.P[v] if isinstance(v, int) else {"o33": A.O1, "o38": A.O2}.get(v) or getattr(A, v.upper()))
    it["v"] = "1:%s" % it["v"]
    return it


def b(v):
    it = copy.deepcopy(B.Q[v] if isinstance(v, int) else getattr(B, v.upper()))
    it["v"] = "2:%s" % it["v"]
    return it


ITEMS = [
    H("다항식의 덧셈과 뺄셈"), a(1), a(3), a(4), a(46),
    H("다항식의 곱셈"), a(7), a(8), a(10), a(11),
    H("곱셈 공식"), a(12), a(14), a(15), a("n2"),
    H("곱셈 공식의 변형 (1)"), a(19), a(20), a(23), a("n3"), a(24), a("n4"),
    H("곱셈 공식의 변형 (2)"), a("n5"), a(28), a(29), a(30), a("n9"), a(32),
    H("다항식의 나눗셈"), a(34), a(35), a(38), a(39), a(40),
    H("항등식과 미정계수법"), b(1), b(4), b(8), b(9), b(11), b(14), b(15), b("m1"),
    H("항등식의 활용"), b(16), b(17), b(21), b(24), b(25), b(26), b(27), b("m3"), b("m4"),
    H("고난도", 2), a(51), a(53), a(54), a(55), a("o33"), a(57), a(59),
    b(67), b(72), b(73), b(74), a(58), a(60),
]
LEVEL = {"상": ["1:46", "1:n2", "1:n4", "2:m3", "2:m4",
               "1:51", "1:53", "1:54", "1:55", "1:o33", "1:57", "1:59",
               "2:67", "2:72", "2:73", "2:74"],
         "최상": ["1:58", "1:60"]}
OLYMPOS = ["1:10", "1:15", "1:28", "1:29", "1:39", "1:53", "1:54", "1:55", "1:o33",
           "2:14", "2:15", "2:21", "2:26", "2:72", "2:73", "2:74"]
