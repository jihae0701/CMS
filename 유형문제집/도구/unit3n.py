# -*- coding: utf-8 -*-
# 공통수학1 3단원 인수분해 (54문항: STEP 1 41 + 고난도 13, 상 15 + 최상 3)
# 문항: unit03.py(4:), unit01.py(1:), unit02.py(2:), unit2_extra.json(3:)
import importlib.util, os, copy, json

HERE = os.path.dirname(os.path.abspath(__file__))


def _load(fn):
    sp = importlib.util.spec_from_file_location(fn[:-3], os.path.join(HERE, fn))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


A = _load("unit01.py")
B = _load("unit02.py")
T = _load("unit03.py")
X = json.load(open(os.path.join(HERE, "unit2_extra.json"), encoding="utf-8"))
UNIT = ("인수분해", "03")
START = 120   # 2단원(59~119)에 이어지는 번호


def H(t, kind=1):
    return {"h": t, "kind": kind}


def a(v):
    it = copy.deepcopy(A.P[v] if isinstance(v, int) else getattr(A, v.upper()))
    it["v"] = "1:%s" % it["v"]
    return it


def b(v):
    it = copy.deepcopy(B.Q[v])
    it["v"] = "2:%s" % it["v"]
    return it


def x(v):
    it = copy.deepcopy(X[v])
    it.pop("origin", None)
    it["v"] = "3:%s" % v
    return it


def t(v):
    it = copy.deepcopy(T.P[v])
    it["v"] = "4:%s" % v
    return it


ITEMS = [
    H("인수분해 공식"), t("n1052"), t("o01"), t("w1"), t("o13"),
    H("공통부분이 있는 식의 인수분해"), t("n1355"), t("n1037"), t("o04"), b(13), t("w17"),
    H("복이차식의 인수분해"), t("w3"), t("o06"), t("w16"),
    H("상반식의 인수분해"), t("w13"), t("w14"),
    H("여러 개의 문자를 포함한 식의 인수분해"), t("n1103"), t("n1251"), t("n993"), t("n1401"), t("w9"), t("n1131"), t("n1234"),
    H("a³+b³+c³−3abc를 이용한 인수분해"), t("w2"), t("w5"), t("w10"), a(48),
    H("인수정리를 이용한 인수분해"), t("o08"), t("w11"), t("n1146"), t("n1370"), t("n3099"), t("o20"),
    H("인수분해의 조건"), t("m3212"), t("n1059"), t("n1464"), t("m3185"),
    H("인수분해의 활용"), t("w12"), t("n3017"), t("n1082"), t("w15"), t("w7"), t("n1167"), t("n3037"),
    H("고난도", 2), t("o23"), t("o25"), t("k30"), a("n4"), t("n1323"), t("n2951"), t("o33"), t("o29"), t("o36"), t("w8"), t("n1452"), t("n1243"), t("n553"),
]
LEVEL = {"상": ["2:13", "4:n1234", "1:48", "4:m3185", "4:w15", "4:n3037",
               "4:k30", "1:n4", "4:w16", "4:w17", "4:n1323", "4:n2951", "4:o29", "4:o36", "4:w8"],
         "최상": ["4:n1452", "4:n1243", "4:n553"]}
OLYMPOS = ["4:o01", "4:o13", "4:o04", "4:o06", "4:o08", "4:o20",
           "4:o23", "4:o25", "4:o33", "4:o29", "4:o36"]
