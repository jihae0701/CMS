# -*- coding: utf-8 -*-
# 기본서 4단원 122번(내신 n1713)·123번(고쟁이 261, 평행이동한 도형의 공통부분)만 따로 만든 파일 (2026-11-08 사용자 요청) (2026-11-08 사용자 요청). 문항은 기본서2/data04.py에서 그대로 가져온다.
import os, sys, copy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "기본서2"))
import data04

UNIT = ("도형의 이동", "04")
BOOK = "2"
DESIGN = "c2"
START = 122   # 사용자 기본서 파일의 번호(평행이동한 도형의 공통부분 122·123)


def _it(src):
    p = [q for _, _, ps in data04.TYPES for q in ps] + data04.STEP3
    p = copy.deepcopy([q for q in p if q["src"] == src][0])
    return {"v": "b4:" + src, "q": p["q"], "ans": p["ans"], "sol": p["sol"], "src": ""}


ITEMS = [{"h": "평행이동한 도형의 공통부분", "kind": 1}, _it("n1713"), _it("g261")]
LEVEL = {"상": ["b4:n1713", "b4:g261"], "최상": []}
OLYMPOS = []
