# -*- coding: utf-8 -*-
# 공통수학2 05 집합의 뜻과 표현 유형서 (44문항: STEP 1 34 + 고난도 10, 242~285) — 2026-11-06 2026 중간 17개교 반영 30 → 42, 기본서에서 옮긴 2문항 → 44
# 쎈처럼 집합을 두 단원으로 나눈 앞 단원(2026-11-06 사용자 지시). 문항: c2unit05.py(c25:)
import importlib.util, os, copy

HERE = os.path.dirname(os.path.abspath(__file__))


def _load(fn):
    sp = importlib.util.spec_from_file_location(fn[:-3], os.path.join(HERE, fn))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


T = _load("c2unit05.py")
UNIT = ("집합의 뜻과 표현", "05")
BOOK = "2"    # 머리말 '공통수학 2'
DESIGN = "c2"  # 공통수학2 유형서 완성본 디자인(c2design.py)
START = 242   # 4단원 유형서 185~241에 이어서


def H(t, kind=1):
    return {"h": t, "kind": kind}


def t(v):
    it = copy.deepcopy(T.P_[v])
    it["v"] = "c25:%s" % v
    return it


ITEMS = [
    H("집합과 원소"), t("j2-1"), t("n1743"), t("e14-5"), t("j12-9"),
    H("집합의 표현과 새로운 집합"), t("e10-4"), t("j6-7"), t("e5-13"),
    H("집합의 원소의 개수"), t("g265"), t("g300"), t("n1902"),
    H("원소에 대한 조건이 주어진 집합"), t("o44"), t("o25"),
    H("집합 사이의 포함 관계"), t("g269"), t("g272"), t("f4-5"), t("j9-8"), t("n1932"), t("o05"),
    H("서로 같은 집합"), t("g304"), t("g271"), t("j6-4"), t("e1-3"), t("j3-13"),
    H("부분집합의 개수"), t("f4-12"), t("j5-6"), t("g295"), t("g296"), t("f4-8"), t("j9-7"),
    H("조건을 만족시키는 부분집합의 개수"), t("e11-18"), t("n1682"),
    H("부분집합의 원소의 합"), t("n1894"), t("g358"), t("e7-13"),
    H("고난도", 2), t("o24"), t("e2-12"), t("g303"), t("n2761"), t("m81"), t("m2303x"), t("j7-20"),
    t("e12-20"), t("m87"), t("m88"),
]
LEVEL = {"상": ["c25:n1932", "c25:o05", "c25:e7-13", "c25:o24", "c25:e2-12", "c25:g303", "c25:n2761", "c25:m81", "c25:m2303x", "c25:j7-20"],
         "최상": ["c25:e12-20", "c25:m87", "c25:m88"]}
OLYMPOS = ["c25:o24", "c25:o44", "c25:o25", "c25:o05"]   # 올림포스 고난도 4문항(10%)
