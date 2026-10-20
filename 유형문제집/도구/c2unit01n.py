# -*- coding: utf-8 -*-
# 공통수학2 01 평면좌표 유형서 (57문항: STEP 1 44 + 고난도 13, 001~057)
# 문항: c2unit01.py(c21:)
import importlib.util, os, copy

HERE = os.path.dirname(os.path.abspath(__file__))


def _load(fn):
    sp = importlib.util.spec_from_file_location(fn[:-3], os.path.join(HERE, fn))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


T = _load("c2unit01.py")
UNIT = ("평면좌표", "01")
BOOK = "2"    # 머리말 '공통수학 2'
START = 1     # 공통수학2는 따로 한 권이므로 001부터


def H(t, kind=1):
    return {"h": t, "kind": kind}


def t(v):
    it = copy.deepcopy(T.P_[v])
    it["v"] = "c21:%s" % v
    return it


ITEMS = [
    H("두 점 사이의 거리"), t("f9-1"), t("g002"), t("g019"),
    H("두 점에서 같은 거리에 있는 점"), t("n1885"), t("g004"), t("g023"),
    H("삼각형의 모양"), t("g005"), t("g006"), t("w1"),
    H("삼각형의 외심"), t("n1815"), t("b040"), t("f2-13"),
    H("두 점 사이의 거리의 활용"), t("g020"), t("b067"), t("f3-17"), t("n1621"),
    H("선분의 내분점"), t("f3-3"), t("f2-4"), t("g012"), t("f8-14"), t("f9-5"),
    H("선분의 내분점의 위치"), t("f7-4"), t("g014"), t("g038"),
    H("삼각형의 무게중심"), t("f9-3"), t("f6-7"), t("g018"), t("b045"), t("n1528"),
    H("평행사변형과 마름모"), t("g017a"), t("g017b"),
    H("각의 이등분선과 삼각형의 내심"), t("n1802"), t("b018"), t("n1879"), t("n1840"),
    H("중선정리"), t("g016"), t("b055"), t("n1937"),
    H("중선정리의 확장"), t("g029"), t("g030"),
    H("거리의 제곱의 합의 최솟값"), t("g021"), t("g037"),
    H("삼각형의 넓이의 비"), t("g035"), t("g040"),
    H("고난도", 2), t("g044v"), t("w2"), t("w3"), t("m2410"), t("n1796"), t("b060"), t("n1919"), t("f6-16"), t("g053"), t("g050"),
    t("g049"), t("f7-17"), t("g051"),
]
LEVEL = {"상": ["c21:f2-13", "c21:n1621", "c21:f9-5", "c21:n1840", "c21:g029", "c21:g037",
               "c21:g044v", "c21:w2", "c21:w3", "c21:m2410", "c21:n1796", "c21:b060", "c21:n1919", "c21:f6-16", "c21:g053", "c21:g050"],
         "최상": ["c21:g049", "c21:f7-17", "c21:g051"]}
OLYMPOS = []   # 올림포스 고난도 공통수학2는 아직 받지 않음
