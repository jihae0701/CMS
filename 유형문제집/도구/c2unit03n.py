# -*- coding: utf-8 -*-
# 공통수학2 03 원의 방정식 유형서 (61문항: STEP 1 45 + 고난도 16, 127~187)
# 문항: c2unit03.py(c23:)
import importlib.util, os, copy

HERE = os.path.dirname(os.path.abspath(__file__))


def _load(fn):
    sp = importlib.util.spec_from_file_location(fn[:-3], os.path.join(HERE, fn))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


T = _load("c2unit03.py")
UNIT = ("원의 방정식", "03")
BOOK = "2"    # 머리말 '공통수학 2'
START = 127   # 2단원 유형서 071~126에 이어서


def H(t, kind=1):
    return {"h": t, "kind": kind}


def t(v):
    it = copy.deepcopy(T.P_[v])
    it["v"] = "c23:%s" % v
    return it


ITEMS = [
    H("원의 방정식"), t("f3-4"), t("o10"), t("n1622"), t("n1642"),
    H("세 점을 지나는 원"), t("f1-6"), t("o16"),
    H("좌표축에 접하는 원"), t("n1591"), t("f9-18"), t("n1666"), t("n1586"), t("n1749"),
    H("점이 나타내는 도형"), t("f2-10"), t("o12"), t("o14"),
    H("두 원의 교점을 지나는 도형"), t("n1619"), t("o05"), t("g191"),
    H("원 위의 점까지의 거리"), t("n1541"), t("o21"), t("g155"),
    H("원과 직선의 위치 관계"), t("o07"), t("n1748"), t("o17"), t("m2311"),
    H("현의 길이"), t("f3-12"), t("f9-13"), t("n1809"), t("f2-19v"),
    H("원 위의 점과 직선 사이의 거리"), t("m2209a"), t("f7-11"), t("n1648"), t("n1836"), t("n1706"),
    H("원의 접선"), t("f1-9"), t("f2-15"), t("o08"), t("m2403"), t("n1710"), t("m2410b"),
    H("원 밖의 점에서 그은 접선"), t("n1579"), t("n1644"), t("n1665"), t("f3-16"), t("f4-11"), t("n1774"),
    H("고난도", 2), t("m2410c"), t("m2410a"), t("m2603"), t("m2309c"), t("m2209b"), t("m2203"), t("n1604"), t("m2009"),
    t("m2421"), t("n1773"), t("n1715v"), t("m2109"), t("m2503b"),
    t("m2309d"), t("m2209c"), t("m2409c"),
]
LEVEL = {"상": ["c23:o17", "c23:m2311",
               "c23:m2410c", "c23:m2410a", "c23:m2603", "c23:m2309c", "c23:m2209b", "c23:m2203", "c23:n1604", "c23:m2009",
               "c23:m2421", "c23:n1773", "c23:n1715v", "c23:m2109", "c23:m2503b"],
         "최상": ["c23:m2309d", "c23:m2209c", "c23:m2409c"]}
OLYMPOS = ["c23:o10", "c23:o16", "c23:o12", "c23:o14", "c23:o05", "c23:o21", "c23:o07", "c23:o17", "c23:o08"]   # 올림포스 고난도 9문항(15%)
