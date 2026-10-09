# -*- coding: utf-8 -*-
# 공통수학1 2단원 나머지정리 (62문항: STEP 1 46 + 고난도 16)
# 문항: unit02.py(2:), unit01.py(1:, 조립제법), unit2_extra.json(3:, 보충 문항)
import importlib.util, os, copy, json

HERE = os.path.dirname(os.path.abspath(__file__))


def _load(fn):
    sp = importlib.util.spec_from_file_location(fn[:-3], os.path.join(HERE, fn))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


A = _load("unit01.py")
B = _load("unit02.py")
X = json.load(open(os.path.join(HERE, "unit2_extra.json"), encoding="utf-8"))
UNIT = ("나머지정리", "02")
START = 62   # 1단원(1~61)에 이어지는 번호


def H(t, kind=1):
    return {"h": t, "kind": kind}


def a(v):
    it = copy.deepcopy(A.P[v] if isinstance(v, int) else getattr(A, v.upper()))
    it["v"] = "1:%s" % it["v"]
    return it


def b(v):
    it = copy.deepcopy(B.Q[v] if isinstance(v, int) else {"o25": B.O1, "o28": B.O2, "o30": B.O3}.get(v) or getattr(B, v.upper()))
    it["v"] = "2:%s" % it["v"]
    return it


def x(v):
    it = copy.deepcopy(X[v])
    it.pop("origin", None)
    it["v"] = "3:%s" % v
    return it


ITEMS = [
    H("나머지정리"), b(28), b(29), b(30), b(31), x("c2"),
    H("이차식으로 나눈 나머지"), b(32), b(34), x("c5"), x("c4"),
    H("몫과 나머지의 관계"), b(36), b(37), b(41), x("c6"),
    H("삼차 이상의 식으로 나눈 나머지"), b(35), b(39), x("c33"), b("o25"), b(47), x("c13"),
    H("xⁿ 꼴·완전제곱식으로 나눈 나머지"), x("c17"), b(44), x("c16"),
    H("수의 나머지"), x("c22"), x("c20"), x("c21"),
    H("인수정리"), b(48), b(49), b(50), b(51), b(52), b(53), b(54), b(60), b("o30"),
    H("인수정리와 다항식의 결정"), b(56), b(57), x("c32"), b(58), b(59), b(46), x("c30"),
    H("조립제법"), a(41), a(44), a(45), a(56), a("n7"),
    H("고난도", 2), x("c18"), b(61), b(62), b(65), b(66), b("m5"), b("o28"), b(71), b(75),
    x("c15"), x("c31"), b(76), b(77), b(78), b(79), b(80),
]
LEVEL = {"상": ["3:c4", "3:c6", "2:47", "3:c13", "2:44", "3:c18", "2:o30", "2:59", "3:c30", "1:n7", "1:56",
               "2:61", "2:62", "2:65", "2:66", "2:m5", "2:o28", "2:71", "2:75",
               "3:c15", "3:c31", "2:76", "2:77"],
         "최상": ["2:78", "2:79", "2:80"]}
OLYMPOS = ["1:56", "2:46", "2:47", "2:60", "2:71", "2:75", "2:o25", "2:o28", "2:o30",
           "3:c2", "3:c5", "3:c30"]
