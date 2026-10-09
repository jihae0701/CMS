# 한글 수식 스크립트 -> LaTeX (미리보기·크기 측정용 근사 변환)
import re

WORDS = {
    "le": r"\le ", "ge": r"\ge ", "ne": r"\ne ", "TIMES": r"\times ", "times": r"\times ",
    "CDOTS": r"\cdots ", "cdots": r"\cdots ", "PLUSMINUS": r"\pm ", "notin": r"\notin ", "nin": r"\notin ",
    "in": r"\in ", "subset": r"\subset ", "nsubset": r"\not\subset ", "cap": r"\cap ", "cup": r"\cup ",
    "circ": r"\circ ", "rarrow": r"\rightarrow ", "alpha": r"\alpha ", "beta": r"\beta ", "prime": "'",
    "sim": r"\sim ", "LEFT": "left", "RIGHT": "right", "DEG": r"^\circ ",
}

def _group(s, i):
    """s[i] == '{' 일 때 짝 괄호까지의 내용과 끝 위치"""
    depth = 0
    for j in range(i, len(s)):
        if s[j] == "{":
            depth += 1
        elif s[j] == "}":
            depth -= 1
            if depth == 0:
                return s[i + 1:j], j + 1
    return s[i + 1:], len(s)

def _atom_before(s, end):
    """end 직전의 그룹 또는 토큰"""
    k = end
    while k > 0 and s[k - 1] == " ":
        k -= 1
    if k > 0 and s[k - 1] == "}":
        depth = 0
        for j in range(k - 1, -1, -1):
            if s[j] == "}":
                depth += 1
            elif s[j] == "{":
                depth -= 1
                if depth == 0:
                    return j, s[j + 1:k - 1]
    m = re.search(r"[A-Za-z0-9\.]+$", s[:k])
    if m:
        return m.start(), m.group(0)
    return k, ""

def _atom_after(s, start):
    k = start
    while k < len(s) and s[k] == " ":
        k += 1
    if k < len(s) and s[k] == "{":
        g, e = _group(s, k)
        return g, e
    m = re.match(r"[A-Za-z0-9\.]+", s[k:])
    if m:
        return m.group(0), k + m.end()
    return "", k

def convert(script):
    s = script
    s = s.replace("`", " ").replace("~", r"\ ")
    # 한글 -> \text{}
    s = re.sub(r"([가-힣]+(?:\s*[가-힣]+)*)", lambda m: r"\text{" + m.group(1) + "}", s)
    # cases / rpile(행렬)
    def env(name, body):
        rows = [r.strip() for r in body.split("#")]
        if name == "cases":
            rows = [r.replace("&&", "&").replace("& &", "&") for r in rows]
            return r"\begin{cases}" + r"\\".join(rows) + r"\end{cases}"
        rows = [re.sub(r"&&?", "&", r) for r in rows]
        return r"\begin{matrix}" + r"\\".join(rows) + r"\end{matrix}"
    for name in ("cases", "rpile", "matrix", "pmatrix"):
        while True:
            m = re.search(r"\b%s\s*\{" % name, s)
            if not m:
                break
            g, e = _group(s, m.end() - 1)
            s = s[:m.start()] + "{" + env("cases" if name == "cases" else "matrix", g) + "}" + s[e:]
    # 단어 치환
    s = re.sub(r"\b(" + "|".join(sorted(WORDS, key=len, reverse=True)) + r")\b", lambda m: WORDS[m.group(1)], s)
    # left/right 괄호
    s = re.sub(r"\bleft\s*\{", r"\\left\\{", s)
    s = re.sub(r"\bright\s*\}", r"\\right\\}", s)
    s = re.sub(r"\bleft\s*([\(\[\|\.])", r"\\left\1", s)
    s = re.sub(r"\bright\s*([\)\]\|\.])", r"\\right\1", s)
    # rm / it
    s = re.sub(r"\brm\s*\{([^{}]*)\}", r"\\mathrm{\1}", s)
    s = re.sub(r"\brm\s+([A-Za-z]+)", r"\\mathrm{\1}", s)
    s = re.sub(r"\bit\b", "", s)
    s = re.sub(r"\bbar\s*\{", r"\\overline{", s)
    s = re.sub(r"\bsqrt\s*\{", r"\\sqrt{", s)
    s = re.sub(r"\bsqrt\s+([A-Za-z0-9]+)", r"\\sqrt{\1}", s)
    # over
    while True:
        m = re.search(r"\s+over\s+", s)
        if not m:
            break
        st, num = _atom_before(s, m.start())
        den, e = _atom_after(s, m.end())
        s = s[:st] + r"\frac{" + num + "}{" + den + "}" + s[e:]
    return s

if __name__ == "__main__":
    for t in ["{1} over {3}x-1", "A`= left( rpile{ 1 && 3 # k && 5 } right)", "cases{ x^{2}-2x-8 ge 0 # x^{2}-36 < 0}",
              "{rm{A}} left(1,`4 right)", "{}_{6} rm C _{3} =20", "left{x left| x 는~ 12 의~약수 right. right}",
              "-{2a} over {15} =2", "{ bar{rm{AB}}} = sqrt{16^{2}+4^{2}}"]:
        print(t, " => ", convert(t))
