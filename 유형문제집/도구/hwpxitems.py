import re, zipfile
def top_paras(sec):
    """section xml -> (head, [top-level <hp:p> strings], tail)"""
    tok = re.compile(r"<hp:p[ >]|</hp:p>")
    i = sec.index("<hp:p "); head = sec[:i]; out = []; depth = 0; start = None; last = i
    for m in tok.finditer(sec, i):
        if m.group(0).startswith("<hp:p"):
            if depth == 0: start = m.start()
            depth += 1
        else:
            depth -= 1
            if depth == 0: out.append(sec[start:m.end()]); last = m.end()
    return head, out, sec[last:]
def text(x):
    return "".join(a or b for a, b in re.findall(r"<hp:t>([^<]*)</hp:t>|<hp:script>([^<]*)</hp:script>", x))
def items(P):
    """[(start, end, src)] : 미주 문단부터 다음 미주/제목 전까지"""
    res = []; cur = None
    for k, p in enumerate(P):
        if "<hp:endNote " in p:
            if cur: res.append(cur)
            m = re.findall(r'<hp:run charPrIDRef="34"><hp:t>([^<]*)</hp:t>', p)
            cur = [k, k + 1, m[-1] if m else ""]
        elif cur and "<hp:tbl " in p and "<hp:endNote" not in p and not text(p).strip().startswith(("(", "①", "④")) and False:
            pass
        elif cur:
            cur[1] = k + 1
    if cur: res.append(cur)
    return res
