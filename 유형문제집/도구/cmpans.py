# 단원 파일의 정답과 검산 파일의 계산 결과를 맞춰 본다.
# 사용: python cmpans.py unit02.py verify02.py
#       python cmpans.py unit1n.py 1=verify01.py 2=verify02.py   (문항 v가 "1:…", "2:…"일 때)
import sys, re, io, contextlib, importlib.util
from sympy import sympify, simplify, sqrt


def load(path):
    spec = importlib.util.spec_from_file_location(path.replace("/", "_")[:-3], path)
    m = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(m)
    return m


U = load(sys.argv[1])
R = []
for arg in sys.argv[2:]:
    pre, path = (arg.split("=", 1) + [None])[:2] if "=" in arg else ("", arg)
    if path is None:
        pre, path = "", arg
    for no, ok, got, exp in load(path).R:
        R.append(("%s:%s" % (pre, no) if pre else no, ok, got, exp))

items = [it for it in U.ITEMS if not it.get("h")]
ans = {it.get("v", i): it["ans"] for i, it in enumerate(items, 1)}


def conv(s):
    s = s.strip().strip("$")
    if re.match(r"^[①-⑤ㄱ-ㅎ]", s):
        return s
    s = re.sub(r"\{([^{}]*)\}\s*over\s*\{([^{}]*)\}", r"((\1)/(\2))", s)
    s = re.sub(r"(\d+)\s*over\s*(\d+)", r"((\1)/(\2))", s)
    s = re.sub(r"sqrt\s*\{\s*([^{}]*)\}", r"sqrt(\1)", s)
    s = re.sub(r"root\s*\{?(\d+)\}?", r"sqrt(\1)", s)
    s = re.sub(r"(\d)\s*sqrt", r"\1*sqrt", s).replace(" ", "")
    return sympify(s)


bad = 0
seen = set()
for no, ok, got, exp in R:
    if no not in ans:
        continue  # 이 단원에 없는 문항
    seen.add(no)
    a = conv(ans[no])
    same = (a == exp) if isinstance(a, str) else simplify(a - sympify(exp)) == 0
    if not same or not ok:
        bad += 1
        print("MISMATCH", no, ans[no], exp, got, ok)
miss = [k for k in ans if k not in seen]
if miss:
    bad += len(miss)
    print("검산 없음", miss)
print("문항", len(ans), "검산", len(seen), "불일치", bad)
