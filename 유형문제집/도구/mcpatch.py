# 사용자가 고친 유형서(예: 08)를 다시 만들지 않고, mcorig 표의 객관식 문항만 고친다(발문 끝, 보기 문단, 정답 번호).
# 사용: python mcpatch.py 사용자문서.hwpx 같은단원을_gen으로_새로_만든.hwpx
import sys, zipfile, re, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hwpxitems import top_paras, text
import mcorig
doc, gen = sys.argv[1], sys.argv[2]
sec = zipfile.ZipFile(doc).read("Contents/section0.xml").decode()
gsec = zipfile.ZipFile(gen).read("Contents/section0.xml").decode()
h, P, t = top_paras(sec)
_, G, _ = top_paras(gsec)
nid = [max(int(x) for x in re.findall(r'<hp:(?:equation|tbl|pic|rect) id="(\d+)"', sec)) + 1000]
def renum(x):
    def f(m):
        nid[0] += 1; return m.group(1) + str(nid[0]) + m.group(2)
    return re.sub(r'(<hp:equation id=")\d+(")', f, x)
def en_text(p):
    return text(p)
done = []
for src, (ch, mark, edits) in mcorig.TABLE.items():
    ks = [k for k, p in enumerate(P) if "<hp:endNote" in p and (src + " [4점]") in p]
    if not ks:
        continue
    k = ks[0]
    if re.search(r'\[정답\] [①-⑤]', P[k]):
        continue      # 이미 고침
    # 정답
    new, n = re.subn(r'<hp:t> \[정답\] </hp:t><hp:equation .*?</hp:equation>', '<hp:t> [정답] %s</hp:t>' % mark, P[k], count=1, flags=re.S)
    assert n == 1, src
    P[k] = new
    # 발문
    j = k + 1
    while not re.search(r"<hp:t>[^<]*(을|를) 구하시오\.[^<]*</hp:t>", P[j]):
        assert "<hp:endNote" not in P[j]; j += 1
    q = P[j]
    for a, b in (edits or []):
        assert q.count("<hp:t>" + a) + q.count(a) >= 1, (src, a)
        q = q.replace(a, b, 1)
    q, n = re.subn(r"(<hp:t>[^<]*)(을|를) 구하시오\.", lambda m: m.group(1) + ("은?" if m.group(2) == "을" else "는?"), q)
    assert n == 1
    q = re.sub(r"<hp:linesegarray>.*?</hp:linesegarray>", "", q, flags=re.S)
    # 보기 문단: 새로 만든 문서의 같은 문항에서
    gk = [i for i, p in enumerate(G) if "<hp:endNote" in p and (src + " [4점]") in p][0]
    chp = []
    i = gk + 1
    while "<hp:endNote" not in G[i]:
        if text(G[i]).startswith(("① ", "④ ")): chp.append(renum(G[i]))
        i += 1
        if i >= len(G): break
    assert len(chp) == 2, (src, len(chp))
    P[j] = q
    P[j + 1:j + 1] = chp
    done.append(src)
out = h + "".join(P) + t
tmp = doc + ".tmp"
with zipfile.ZipFile(doc) as zin, zipfile.ZipFile(tmp, "w") as zout:
    for info in zin.infolist():
        data = zin.read(info.filename)
        if info.filename == "Contents/section0.xml":
            data = out.encode()
        zout.writestr(info, data)
os.replace(tmp, doc)
print(len(done), done)
