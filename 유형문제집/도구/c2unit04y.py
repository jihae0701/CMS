# -*- coding: utf-8 -*-
# 기본서 4단원 문항을 따로 만든 파일: 156번(고쟁이 259, 정사각형 종이 접기) — c2unit04z.py는 122·123번 (2026-11-08 사용자 요청). 문항은 기본서2/data04.py에서 그대로 가져온다.
import os, sys, copy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "기본서2"))
import data04

UNIT = ("도형의 이동", "04")
BOOK = "2"
DESIGN = "c2"
START = 156   # 사용자 기본서 파일의 번호


def _it(src):
    p = [q for _, _, ps in data04.TYPES for q in ps] + data04.STEP3
    p = copy.deepcopy([q for q in p if q["src"] == src][0])
    return {"v": "b4:" + src, "q": p["q"], "ans": p["ans"], "sol": p["sol"], "src": ""}


ITEMS = [{"h": "대칭이동의 활용(종이 접기)", "kind": 1}, _it("g259")]
LEVEL = {"상": ["b4:g259"], "최상": []}
OLYMPOS = []
