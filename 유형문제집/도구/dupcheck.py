# -*- coding: utf-8 -*-
"""새 단원 기본서 문항이 앞 단원(기본서·유형서) 문항과 같은 꼴인지 찾는다.

python dupcheck.py <새 기본서.hwpx> [--min 0.45]
python dupcheck.py unit3n.py [--min 0.45]     (새 유형서 단원)
- 비교 대상: 기본서/*.hwpx 중 새 파일보다 앞 단원 파일, 유형서 단원 파일(unit*n.py)의 문항
  (새 파일이 유형서 단원이면 같은 단원 기본서까지, 유형서는 다른 단원만)
- 문제 글의 수식을 '뼈대'(숫자는 #, 문자는 그대로, 띄어쓰기·LEFT/RIGHT 없앰)로 바꾼 뒤
  뼈대 조각의 겹침(자카드)과 문장 낱말 겹침을 더해 점수를 매긴다.
- 점수가 높은 짝을 보여 줄 뿐이므로, 최종 판단은 사람이 문항을 읽고 한다.
"""
import sys, os, re, glob, json, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "기본서"))
import hwpxio as io, numbering as nb  # noqa: E402

NEW = sys.argv[1]
MIN = float(sys.argv[sys.argv.index("--min") + 1]) if "--min" in sys.argv else 0.40


def skeleton(sc):
    s = re.sub(r"\b(LEFT|RIGHT|left|right|it|rm|bold)\b|`|~|\s", "", sc)
    s = s.replace("TIMES", "times").replace("{", "(").replace("}", ")")
    s = re.sub(r"\d+", "#", s)
    s = re.sub(r"[A-Za-z]\'?\((?:x|#|a|x[+-]#)\)", "F", s)      # f(x), P(x), Q(2) 같은 흔한 표기는 하나로
    return s


def feats(text):
    eqs = [skeleton(m) for m in re.findall(r"\$([^$]+)\$", text)]
    grams = set()
    for e in eqs:
        for i in range(len(e) - 4):
            g = e[i:i + 5]
            if len(set(g) - set("F,()=#")) >= 2:           # 기호뿐인 조각은 뺌
                grams.add(g)
    words = set(w for w in re.findall(r"[가-힣]{2,}", re.sub(r"\$[^$]*\$", " ", text)))
    return grams, words


def score(a, b):
    (ga, wa), (gb, wb) = a, b
    jg = len(ga & gb) / max(1, len(ga | gb))
    jw = len(wa & wb) / max(1, len(wa | wb))
    return 0.75 * jg + 0.25 * jw


def gibon_items(path):
    fl, _ = io.read(path)
    _, P, _ = io.split(fl["Contents/section0.xml"].decode("utf-8"))
    out = []
    segs = nb.segments(P)
    for k, (a, e) in enumerate(segs):
        end = segs[k + 1][0] if k + 1 < len(segs) else len(P)      # 조건·선지 문단까지 (다음 문항 앞까지)
        rng = [i for i in range(a, end) if not nb.is_heading(P[i])]
        q = " ".join(io.text(re.sub(r"<hp:endNote .*?</hp:endNote>", "", P[i], flags=re.S)) for i in rng)
        q = re.split(r"(?:유형별 학습하기|단원 마무리 하기|개념 확인하기)", q)[0]
        out.append((nb.num_text(P[a]) or "?", q.strip()))
    return out


def unit_items(path):
    sp = importlib.util.spec_from_file_location("u", path)
    u = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(u)
    n, out = getattr(u, "START", 1) - 1, []
    for it in u.ITEMS:
        if it.get("h"):
            continue
        n += 1
        out.append((str(n), json.dumps(it["q"], ensure_ascii=False)))
    return out


IS_UNIT = NEW.endswith(".py")
new_items = unit_items(NEW) if IS_UNIT else gibon_items(NEW)
others = []
base = os.path.join(HERE, "..", "기본서")
new_unit = os.path.basename(NEW)[4] + "." if IS_UNIT else os.path.basename(NEW)
for f in sorted(glob.glob(os.path.join(base, "*.hwpx"))):
    bn = os.path.basename(f)
    if bn < new_unit or (IS_UNIT and bn.startswith(new_unit)):   # 파일 이름이 단원 번호로 시작한다
        others += [("기본서 " + bn[:2].strip(".") + "단원 " + n, q) for n, q in gibon_items(f)]
for f in sorted(glob.glob(os.path.join(HERE, "unit*n.py"))):
    if IS_UNIT and os.path.samefile(f, NEW):
        continue
    others += [("유형서 " + os.path.basename(f)[4] + "단원 " + n, q) for n, q in unit_items(f)]

F = {k: feats(q) for k, q in others}
hits = []
for n, q in new_items:
    fq = feats(q)
    for k, oq in others:
        s = score(fq, F[k])
        if s >= MIN:
            hits.append((s, n, k, q, oq))
hits.sort(reverse=True)
print("새 단원 %d문항, 비교 %d문항, 점수 %.2f 이상 %d쌍" % (len(new_items), len(others), MIN, len(hits)))
for s, n, k, q, oq in hits:
    print("\n[%.2f] %s  <->  %s" % (s, n, k))
    print("   새: " + re.sub(r"\s+", " ", q)[:160])
    print("   앞: " + re.sub(r"\s+", " ", oq)[:160])
