# -*- coding: utf-8 -*-
"""단원별 기본서·유형서 완성본 파일 목록 (공통수학1·2 각 12단원)"""
import os, re, glob

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _num(f):
    return int(re.match(r"(\d+)", os.path.basename(f)).group(1))


def units(book):
    if book == 1:
        B = [f for f in glob.glob(os.path.join(ROOT, "기본서", "[0-9]*.hwpx"))]
        Y = [f for f in glob.glob(os.path.join(ROOT, "공통수학1", "[0-9][0-9]_*.hwpx")) if not re.search(r"교체후보|추가|_\d+번", f)]
    else:
        B = [f for f in glob.glob(os.path.join(ROOT, "공통수학2", "기본서", "[0-9]*.hwpx")) if not re.search(r"_\d+(_\d+)?번", f)]
        Y = [f for f in glob.glob(os.path.join(ROOT, "공통수학2", "유형서", "[0-9][0-9]_*.hwpx")) if not re.search(r"추가|_\d+번", f)]
    B, Y = sorted(B, key=_num), sorted(Y, key=_num)
    assert [_num(f) for f in B] == list(range(1, 13)) == [_num(f) for f in Y], (B, Y)
    name = lambda f: re.sub(r"^\d+[._]\s*", "", os.path.splitext(os.path.basename(f))[0]).replace("_", " ")
    return [(i + 1, name(b), b, y) for i, (b, y) in enumerate(zip(B, Y))]
