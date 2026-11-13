# -*- coding: utf-8 -*-
# 공통수학2 07 명제 유형서 391번(n2755, 내신 기출 모음 allc.json 2-06) — 별도 파일(2026-11-13 사용자 요청)
# 유형서는 그대로 두고, 해설만 산술평균과 기하평균의 관계로 바꾼 판을 따로 만든다. 결과 `공통수학2/유형서/07_명제_391번_해설.hwpx`.
import importlib.util, os, copy

HERE = os.path.dirname(os.path.abspath(__file__))


def _load(fn):
    sp = importlib.util.spec_from_file_location(fn[:-3], os.path.join(HERE, fn))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


T = _load("c2unit07.py")
UNIT = ("명제", "07")
BOOK = "2"
DESIGN = "c2"
START = 391


def H(t, kind=1):
    return {"h": t, "kind": kind}


it = copy.deepcopy(T.P_["n2755"])
it["v"] = "c27:n2755"
it["sol"] = [
    "명제가 거짓이면 그 부정 '모든 실수 $x$에 대하여 $x^{2} -2+ {n} over {x^{2} +1} >0$이다.'가 참이다.",
    "$x^{2} =t$ $(t geq 0)$라 하고 양변에 $t+1$을 곱하면 $(t-2)(t+1)+n>0$, 즉 $t^{2} -t+n-2>0$",
    "$t^{2} -t+n-2= LEFT ( t- {1} over {2} RIGHT ) ^{2} +n- {9} over {4}$는 $t= {1} over {2}$일 때 가장 작으므로 $n- {9} over {4} >0$  $therefore$ 정수 $n geq 3$",
    "$n-2>0$이고 $n^{2} -6n+10=(n-3)^{2} +1>0$이므로 주어진 식을 다음과 같이 나눈다.",
    "$n^{2} + {100} over {n^{2} -6n+10} + {96} over {n-2}$",
    "$= LEFT { 6(n-2)+ {96} over {n-2} RIGHT } + LEFT { (n-3)^{2} +1+ {100} over {(n-3)^{2} +1} RIGHT } +2$",
    "(참고: $n^{2} =6(n-2)+(n-3)^{2} +1+2$)",
    "산술평균과 기하평균의 관계에 의하여",
    "$6(n-2)+ {96} over {n-2} geq 2 sqrt {6(n-2) TIMES {96} over {n-2}} =2 sqrt {576} =48$ (등호는 $n-2=4$, 즉 $n=6$일 때 성립)",
    "$(n-3)^{2} +1+ {100} over {(n-3)^{2} +1} geq 2 sqrt {100} =20$ (등호는 $(n-3)^{2} +1=10$, 즉 $n=6$일 때 성립)",
    "따라서 주어진 식의 값은 $48+20+2=70$ 이상이고, 두 등호가 모두 $n=6$일 때 성립하므로 최솟값은 $70$",
]
ITEMS = [H("고난도", 2), it]
LEVEL = {"상": [], "최상": ["c27:n2755"]}
OLYMPOS = []
