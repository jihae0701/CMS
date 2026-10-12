# -*- coding: utf-8 -*-
# 공통수학1 8단원 이차부등식 (45문항: STEP 1 38 + 고난도 7)
# 문항: unit08.py(9:)
import importlib.util, os, copy

HERE = os.path.dirname(os.path.abspath(__file__))


def _load(fn):
    sp = importlib.util.spec_from_file_location(fn[:-3], os.path.join(HERE, fn))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


T = _load("unit08.py")
UNIT = ("이차부등식", "08")
START = 415   # 7단원(355~414)에 이어지는 번호


def H(t, kind=1):
    return {"h": t, "kind": kind}


def t(v):
    it = copy.deepcopy(T.P[v])
    it["v"] = "9:%s" % v
    return it


ITEMS = [
    H("이차부등식의 풀이"), t("n541"), t("n961"), t("y75"), t("o40"), t("w8"),
    H("이차함수의 그래프와 이차부등식"), t("y72"), t("y73"), t("w1"), t("n471"), t("o39"), t("w9"),
    H("해가 주어진 이차부등식"), t("o16"), t("n157"), t("n310"), t("n957"), t("y82"), t("n725"),
    H("이차부등식이 해를 가질 조건"), t("n556"), t("n598"), t("n250"), t("n164"),
    H("이차부등식이 해를 갖지 않을 조건"), t("o18"), t("n315"),
    H("모든 실수에 대하여 성립하는 이차부등식"), t("o17"), t("n130"), t("n209"), t("n817"),
    H("제한된 범위에서 항상 성립하는 이차부등식"), t("n462"), t("n945"), t("n728"),
    H("이차방정식의 근의 판별과 이차부등식"), t("y104"), t("y106"),
    H("두 이차함수와 이차부등식"), t("n954"), t("n282"),
    H("이차부등식의 활용"), t("w5"), t("w6"), t("w7"),
    H("이차식의 최대·최소"), t("w10"),
    H("고난도", 2), t("n2512"), t("o41"), t("n980"), t("o57"), t("n913"), t("n640"), t("n495"),
]
LEVEL = {"상": ["9:w9", "9:n817", "9:n728", "9:n164", "9:n315", "9:n954", "9:n282", "9:n2512", "9:o41", "9:n980", "9:o57"],
         "최상": ["9:n913", "9:n640", "9:n495"]}
OLYMPOS = ["9:o40", "9:o39", "9:o16", "9:o18", "9:o17", "9:o41", "9:o57"]
