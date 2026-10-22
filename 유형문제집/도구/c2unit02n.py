# -*- coding: utf-8 -*-
# 공통수학2 02 직선의 방정식 유형서 (56문항: STEP 1 43 + 고난도 13, 071~126)
# 문항: c2unit02.py(c22:), '점이 나타내는 도형의 방정식'의 수매씽 0111~0115는 c2unit01.py(c21:)에서 옮겨 옴(사용자 지시 2026-10-22)
import importlib.util, os, copy

HERE = os.path.dirname(os.path.abspath(__file__))


def _load(fn):
    sp = importlib.util.spec_from_file_location(fn[:-3], os.path.join(HERE, fn))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


T1 = _load("c2unit01.py")
T = _load("c2unit02.py")
UNIT = ("직선의 방정식", "02")
BOOK = "2"    # 머리말 '공통수학 2'
START = 71    # 1단원 유형서 001~070에 이어서


def H(t, kind=1):
    return {"h": t, "kind": kind}


def t(v):
    it = copy.deepcopy(T.P_[v])
    it["v"] = "c22:%s" % v
    return it


def t1(v):
    it = copy.deepcopy(T1.P_[v])
    it["v"] = "c21:%s" % v
    return it


ITEMS = [
    H("직선의 방정식"), t("w6"), t("n1780"), t("m0903"),
    H("넓이를 이등분하는 직선"), t("w1"), t("b012"), t("n1929"), t("n1708"),
    H("정점을 지나는 직선"), t("b034"), t("g077"), t("o14"), t("o36"),
    H("두 직선의 평행과 수직"), t("f2-7"), t("f3-18"), t("m2503"), t("m2303"),
    H("수선의 발과 선분의 수직이등분선"), t("n1816"), t("n1891"), t("o17"), t("b019"), t("n1920"), t("g097"),
    H("세 직선의 위치 관계"), t("f4-14"), t("b024"), t("f4-10"), t("g116"),
    H("점과 직선 사이의 거리"), t("f1-7"), t("g109"), t("m2309a"),
    H("거리의 최대, 최소"), t("b047"), t("o42"), t("o21"),
    H("평행한 두 직선 사이의 거리"), t("b052"), t("o20"), t("m2409a"),
    H("각의 이등분선"), t("b057"), t("g121"), t("o46"),
    H("점이 나타내는 도형의 방정식"), t1("sm0111"), t1("sm0112"), t1("sm0113"), t1("sm0114"), t1("sm0115"), t("w5"),
    H("고난도", 2), t("m2309b"), t("g113"), t("w3"), t("n1607"), t("n1917"), t("g083"), t("w2"), t("f8-11"), t("w7"), t("m2311"),
    t("m18"), t("m2409b"), t("w4"),
]
LEVEL = {"상": ["c22:n1708", "c22:o36", "c22:m2303", "c22:g116",
               "c22:m2309b", "c22:g113", "c22:w3", "c22:n1607", "c22:n1917", "c22:g083", "c22:w2", "c22:f8-11", "c22:w7", "c22:m2311"],
         "최상": ["c22:m18", "c22:m2409b", "c22:w4"]}
OLYMPOS = ["c22:o14", "c22:o36", "c22:o17", "c22:o42", "c22:o21", "c22:o20", "c22:o46"]   # 올림포스 고난도 7문항(13%)
