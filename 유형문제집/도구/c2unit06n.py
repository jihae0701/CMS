# -*- coding: utf-8 -*-
# 공통수학2 06 집합의 연산 유형서 (43문항: STEP 1 31 + 고난도 12, 272~314)
# 쎈처럼 집합을 두 단원으로 나눈 뒤 단원(2026-11-06 사용자 지시). 문항: c2unit06.py(c26:)
import importlib.util, os, copy

HERE = os.path.dirname(os.path.abspath(__file__))


def _load(fn):
    sp = importlib.util.spec_from_file_location(fn[:-3], os.path.join(HERE, fn))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


T = _load("c2unit06.py")
UNIT = ("집합의 연산", "06")
BOOK = "2"    # 머리말 '공통수학 2'
DESIGN = "c2"  # 공통수학2 유형서 완성본 디자인(c2design.py)
START = 272   # 5단원 유형서 242~271에 이어서


def H(t, kind=1):
    return {"h": t, "kind": kind}


def t(v):
    it = copy.deepcopy(T.P_[v])
    it["v"] = "c26:%s" % v
    return it


ITEMS = [
    H("합집합과 교집합"), t("o11"), t("n1893"), t("n1570"),
    H("여집합과 차집합"), t("o13"), t("o22"), t("n2370"),
    H("조건을 만족시키는 집합 구하기"), t("n1772"), t("o36"), t("e10-22"),
    H("집합의 연산과 미지수"), t("o12"), t("g330"), t("g311"),
    H("집합의 연산의 성질"), t("n1909"), t("n2376"),
    H("집합의 연산 법칙"), t("g281"), t("g283"), t("g315"),
    H("집합의 연산과 집합의 개수"), t("m2203x2"), t("g334"), t("n1841"), t("g339"),
    H("배수와 약수의 집합"), t("g285"), t("n1564"), t("e10-12"),
    H("새롭게 정의된 연산"), t("g323"), t("g347"),
    H("유한집합의 원소의 개수"), t("o19"), t("n1938"),
    H("원소의 개수의 최댓값과 최솟값"), t("n1915"), t("e13-13"), t("g332"),
    H("고난도", 2), t("g360"), t("g355"), t("m2203x1"), t("m2311x"), t("m2011x1"), t("m2410-27"),
    t("m2403-28"), t("m2603-19"), t("m2211x"),
    t("m2503-29"), t("m2011x2"), t("m2410-30"),
]
LEVEL = {"상": ["c26:g339", "c26:e13-13",
               "c26:g360", "c26:g355", "c26:m2203x1", "c26:m2311x", "c26:m2011x1", "c26:m2410-27",
               "c26:m2403-28", "c26:m2603-19", "c26:m2211x"],
         "최상": ["c26:m2503-29", "c26:m2011x2", "c26:m2410-30"]}
OLYMPOS = ["c26:o11", "c26:o13", "c26:o22", "c26:o36", "c26:o12", "c26:o19"]   # 올림포스 고난도 6문항(14%)
