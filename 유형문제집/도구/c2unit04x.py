# -*- coding: utf-8 -*-
# 공통수학2 04 도형의 이동 — 별도 파일(2026-11-08 사용자 요청): 유형서 193번(f4-17, 그림 넣음)과 '도형 f(x, y)=0의 이동' 내신 4문항
# 문항: c2unit04.py(c24:). 결과 `공통수학2/유형서/04_도형의 이동_추가문항.hwpx`, 번호 1~5.
import importlib.util, os, copy

HERE = os.path.dirname(os.path.abspath(__file__))


def _load(fn):
    sp = importlib.util.spec_from_file_location(fn[:-3], os.path.join(HERE, fn))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


T = _load("c2unit04.py")
UNIT = ("도형의 이동", "04")
BOOK = "2"
DESIGN = "c2"
START = 1


def H(t, kind=1):
    return {"h": t, "kind": kind}


def t(v):
    it = copy.deepcopy(T.P_[v])
    it["v"] = "c24:%s" % v
    return it


ITEMS = [
    H("이동한 도형과 넓이"), t("f4-17"),
    H("도형 f(x, y)=0의 이동"), t("n1795"), t("n1933"), t("e10-7"), t("n1862"),
]
LEVEL = {"상": ["c24:f4-17", "c24:e10-7", "c24:n1862"], "최상": []}
OLYMPOS = []
