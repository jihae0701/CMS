# -*- coding: utf-8 -*-
# 공통수학2 01 평면좌표 유형서 (44문항: STEP 1 34 + 고난도 10, 001~044)
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
    H("두 점 사이의 거리"), t("o01"), t("g019"), t("g023"),
    H("삼각형의 모양"), t("g006"), t("m2109"),
    H("삼각형의 외심"), t("o02"), t("f2-13"),
    H("두 점 사이의 거리의 활용"), t("g020"), t("b067"), t("f3-17"), t("n1621"),
    H("선분의 내분점"), t("o06"), t("f8-14"), t("f9-5"), t("m2103"),
    H("선분의 내분점의 위치"), t("f7-4"), t("g038"),
    H("삼각형의 무게중심"), t("g018"), t("b045"), t("n1528"),
    H("평행사변형"), t("o54"),
    H("각의 이등분선과 삼각형의 내심"), t("n1879"), t("n1840"),
    H("중선정리"), t("b055"), t("o27"),
    H("중선정리의 확장"), t("g029"), t("g030"),
    H("거리의 제곱의 합의 최솟값"), t("g021"), t("g037"),
    H("좌표를 이용한 도형의 성질"), t("n1937"), t("m0809"),
    H("삼각형의 넓이의 비"), t("g035"), t("g040"), t("o32"),
    H("고난도", 2), t("w3"), t("m2410"), t("m0911"), t("n1796"), t("o48"), t("f6-16"), t("g050"),
    t("g049"), t("f7-17"), t("g051"),
]
LEVEL = {"상": ["c21:f2-13", "c21:m2109", "c21:n1840", "c21:o32",
               "c21:w3", "c21:m2410", "c21:m0911", "c21:n1796", "c21:o48", "c21:f6-16", "c21:g050"],
         "최상": ["c21:g049", "c21:f7-17", "c21:g051"]}
OLYMPOS = ["c21:o01", "c21:o02", "c21:o06", "c21:o54", "c21:o27", "c21:o32", "c21:o48"]   # 올림포스 고난도 7문항(16%, 사용자 기준 15% 내외)
