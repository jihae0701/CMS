# -*- coding: utf-8 -*-
"""기본서·유형서 문항 닮은 정도(쌍둥이 후보) — 수식 뼈대(숫자→#) 조각 겹침 + 낱말 겹침 (dupcheck.py와 같은 방식)"""
import re


def skeleton(sc):
    s = re.sub(r"\b(LEFT|RIGHT|left|right|it|rm|rmbold|bold|cdots|CDOTS)\b|`|~|\s", "", sc)
    s = s.replace("TIMES", "times").replace("{", "(").replace("}", ")")
    s = re.sub(r"\d+", "#", s)
    s = re.sub(r"[A-Za-z]'?\((?:x|#|a|x[+-]#)\)", "F", s)
    return s


def feats(text):
    eqs = [skeleton(m) for m in re.findall(r"\$([^$]+)\$", text)]
    grams = set()
    for e in eqs:
        for i in range(len(e) - 4):
            g = e[i:i + 5]
            if len(set(g) - set("F,()=#")) >= 2:
                grams.add(g)
    body = re.sub(r"\$[^$]*\$", " ", text)
    body = re.sub(r"\d{4}년 \d+월 고\d.*?\[\d점\]|대표문제|\d{3}\s", " ", body)
    words = set(re.findall(r"[가-힣]{2,}", body))
    nums = set(re.findall(r"\d+", " ".join(re.findall(r"\$([^$]+)\$", text))))
    return grams, words, nums


def score(a, b):
    (ga, wa, na), (gb, wb, nb) = a, b
    jg = len(ga & gb) / max(1, len(ga | gb))
    jw = len(wa & wb) / max(1, len(wa | wb))
    return 0.75 * jg + 0.25 * jw


def numsame(a, b):
    na, nb = a[2], b[2]
    return len(na & nb) / max(1, len(na | nb))


def numseq(text):
    """식 속 숫자를 차례대로(같은 문제 판단용)"""
    return re.findall(r"\d+", " ".join(re.findall(r"\$([^$]+)\$", text)))
