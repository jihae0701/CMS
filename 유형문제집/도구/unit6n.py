# -*- coding: utf-8 -*-
# 공통수학1 6단원 이차함수의 최대, 최소 (51문항: STEP 1 40 + 고난도 11)
# 문항: unit06.py(7:)
import importlib.util, os, copy

HERE = os.path.dirname(os.path.abspath(__file__))


def _load(fn):
    sp = importlib.util.spec_from_file_location(fn[:-3], os.path.join(HERE, fn))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


T = _load("unit06.py")
UNIT = ("이차함수의 최대, 최소", "06")
START = 305   # 5단원(242~304)에 이어지는 번호


def H(t, kind=1):
    return {"h": t, "kind": kind}


def t(v):
    it = copy.deepcopy(T.P[v])
    it["v"] = "7:%s" % v
    return it


ITEMS = [
    H("이차함수의 최댓값과 최솟값"), t("w1"), t("w4"), t("n1174"), t("n1104"),
    H("제한된 범위에서의 최대·최소"), t("n1276"), t("o41"), t("w5"),
    H("조건을 이용한 이차함수의 최대·최소"), t("o39"), t("o55"), t("o46"), t("n989"), t("n1498"), t("n3107"), t("o57"), t("n1126"),
    H("축에 문자가 있을 때의 최대·최소"), t("o42"), t("n3000"), t("n21"), t("n1435"), t("n1393"),
    H("범위에 문자가 있을 때의 최대·최소"), t("n61"), t("o40"), t("n1338"), t("n1488"), t("n3043"), t("n2933"), t("n1108"),
    H("공통부분이 있는 함수의 최대·최소"), t("o19"), t("n1102"), t("w3"),
    H("이차식의 최대·최소"), t("w2"), t("o21"), t("n1132"),
    H("이차함수의 최대·최소의 활용"), t("n1095"), t("n1319"), t("n1069"), t("o44"), t("n1151"), t("n711"), t("n1169"),
    H("고난도", 2), t("m3285"), t("m3335"), t("n1260"), t("o56"), t("n1281"), t("n1023"), t("m3313"), t("n705"),
    t("n1045"), t("n16"), t("n1027"),
]
LEVEL = {"상": ["7:n1435", "7:n1393", "7:o57", "7:n1169",
               "7:m3285", "7:m3335", "7:n1260", "7:o56", "7:n1281", "7:n1023", "7:m3313", "7:n705"],
         "최상": ["7:n1045", "7:n16", "7:n1027"]}
OLYMPOS = ["7:o39", "7:o41", "7:o55", "7:o46", "7:o57", "7:o42", "7:o40", "7:o19", "7:o21", "7:o44", "7:o56"]
