# -*- coding: utf-8 -*-
"""기본서 수업에서 꼭 풀어 줄 문항 고르기 (2026-11-19 사용자 '교재 수업 가이드 할 거야. 기본서 대표문제 외 유형서와 비교하여 쌍둥이 문제 등
기본서 수업 시 반드시 풀어 줘야 할 것들 만들어 줘').
python analyze.py <1|2> <출력.json>
- 기본서 문항마다 유형서(Core) 문항과 닮은 정도를 잼: 식 뼈대 겹침(jg, 숫자→#)과 문장 낱말 겹침(jw).
  · 쌍둥이: jg≥0.35·jw≥0.45·평균≥0.45, 또는 평균≥0.60(둘 다 0.15 이상) — 숫자만 바꾸거나 거의 같은 문제.
  · 같은 문제: 평균≥0.75이고 식 속 숫자가 차례까지 모두 같음(숫자까지 같은 문제).
  · 같은 틀: jw≥0.70이고 기본서 문장 낱말 8개 이상 — 묻는 방식·조건 문장이 같고 식만 다른 문제.
- 꼭 풀 문항 = 대표문제 전부 + 유형서에 쌍둥이·같은 틀이 있는 기본서 문항.
- 대표문제는 쌍둥이가 없어도, 이어지는 유형서 유형 안에서 가장 닮은 문항 1~2개를 '이어 풀기'로 적음(평균≥0.25).
- 유형 연계: 유형서 유형마다 기본서 유형과의 이름 닮음(글자 2개 묶음) + 문항 닮음 합으로 가장 가까운 기본서 유형.
- Lite: 같은 번호의 Lite 문항이 Core와 같은지(단원종합문제는 Lite에서 바뀐 문항이 있음).
"""
import sys, os, re, json, glob
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from extract import book, read, ptext
from match import feats, numseq

bookno, out = int(sys.argv[1]), sys.argv[2]
ROOT = os.path.dirname(os.path.dirname(HERE))
J = lambda a, b: len(a & b) / max(1, len(a | b))
bi = lambda s: set(s[i:i + 2] for i in range(len(s) - 1))


def lite_items(u):
    fs = [f for f in glob.glob(os.path.join(ROOT, "스토리라이트", "공통수학%d" % bookno, "%02d_*.hwpx" % u)) if not re.search(r"추가|_\d+번", f)]
    return read(fs[0], "y") if fs else None


def mock(q):
    m = re.match(r"\s*(\d{4}년 \d+월 고\d[^\[]*?\d+번)", q)
    return m.group(1).strip() if m else ""


# 공통수학2 기본서 대표문제 번호: 사용자가 2026-11-18에 준 단원 PDF(인디자인용)에서 '대표문제' 딱지가 붙은 번호.
# 4~12단원 한글 파일은 번호가 자동 번호라 글자로 안 남고, 인쇄에 안 나오는 '대표문제' 상자가 남은 문항(445·446·449·457·477 등)이 있어 PDF를 따름.
REP2 = {1: [1, 4, 8, 10, 12, 14, 16, 19, 21, 23], 2: [39, 42, 45, 47, 50, 53, 57, 59, 63], 3: [78, 80, 83, 86, 89, 92, 96, 99, 102, 105],
        4: [119, 122, 124, 127, 130, 132, 135, 138, 140, 142, 143], 5: [161, 164, 167, 170, 173, 177, 179, 182],
        6: [200, 203, 206, 209, 211, 213, 216, 219, 221, 224], 7: [237, 240, 242, 245, 248, 250, 253, 256, 258, 260],
        8: [275, 277, 283, 285, 287, 288, 290, 292, 294, 296, 298, 300], 9: [312, 315, 318, 321, 323, 328, 332, 336, 339, 343],
        10: [355, 358, 360, 363, 366, 369, 372, 375, 378, 381], 11: [395, 397, 402, 405, 407, 409, 411, 414, 416, 418, 420],
        12: [436, 439, 442, 444, 447, 450, 452, 456, 458, 461, 463, 465, 467]}

res = []
for u, name, B, Y, bf, yf in book(bookno):
    if bookno == 2:
        for it in B: it["rep"] = it["n"] in REP2[u]
    FB = [feats(it["q"]) for it in B]
    FY = [feats(it["q"]) for it in Y]
    NB = [numseq(it["q"]) for it in B]
    NY = [numseq(it["q"]) for it in Y]
    L = lite_items(u)
    ystart = Y[0]["n"]
    if L:
        for i, it in enumerate(L): it["n"] = ystart + i
    def lite_same(n):
        if not L: return None                                  # Lite 없음(유형서에서 읽음)
        k = n - ystart
        if k >= len(L): return False
        a, b = feats(Y[k]["q"]), feats(L[k]["q"])
        return (0.5 * J(a[0], b[0]) + 0.5 * J(a[1], b[1])) > 0.8
    # 짝 점수
    S = {}
    for i in range(len(B)):
        for j in range(len(Y)):
            jg, jw = J(FB[i][0], FY[j][0]), J(FB[i][1], FY[j][1])
            S[i, j] = (jg, jw, 0.5 * jg + 0.5 * jw)
    def kind(i, j):
        jg, jw, s = S[i, j]
        if s >= 0.75 and NB[i] and NB[i] == NY[j]:
            return "같은 문제"
        if (jg >= 0.35 and jw >= 0.45 and s >= 0.45) or (s >= 0.60 and min(jg, jw) >= 0.15):
            return "쌍둥이"
        if jw >= 0.70 and len(FB[i][1]) >= 8:
            return "같은 틀"
        return None
    # 유형 연계
    btypes = []
    for it in B:
        if it["type"] and it["type"] not in btypes: btypes.append(it["type"])
    ytypes = []
    for it in Y:
        if it["type"] and it["type"] not in ytypes: ytypes.append(it["type"])
    tmap = {}
    for yt in ytypes:
        best = None
        for bt in btypes:
            name_s = J(bi(re.sub(r"\s|[^가-힣A-Za-z]", "", yt[1])), bi(re.sub(r"\s|[^가-힣A-Za-z]", "", bt[1])))
            prob_s = 0
            for j, iy in enumerate(Y):
                if iy["type"] != yt: continue
                prob_s += max([S[i, j][2] for i, ib in enumerate(B) if ib["type"] == bt] or [0])
            nY = sum(1 for iy in Y if iy["type"] == yt)
            v = 0.6 * name_s + 0.4 * prob_s / max(1, nY)
            if best is None or v > best[0]: best = (v, bt, name_s)
        tmap[yt] = best
    # 꼭 풀 문항
    must = []
    for i, ib in enumerate(B):
        twins = []
        for j, iy in enumerate(Y):
            k = kind(i, j)
            if k: twins.append(dict(n=iy["n"], kind=k, score=round(S[i, j][2], 2), stage=iy["stage"], mock=mock(iy["q"]), lite=lite_same(iy["n"])))
        twins.sort(key=lambda t: -t["score"])
        if not (ib["rep"] or twins):
            continue
        follow = []
        if ib["rep"] and not twins:
            yts = [yt for yt, v in tmap.items() if v and v[1] == ib["type"]]
            cand = sorted([(S[i, j][2], j) for j, iy in enumerate(Y) if iy["type"] in yts], reverse=True)
            follow = [dict(n=Y[j]["n"], score=round(s, 2)) for s, j in cand[:2] if s >= 0.25]
        must.append(dict(n=ib["n"], stage=ib["stage"], type=ib["type"], rep=ib["rep"], twins=twins[:3], follow=follow,
                         q=re.sub(r"\s+", " ", re.sub(r"\$[^$]*\$", "□", ib["q"]))[:80]))
    yr = lambda yt: [iy["n"] for iy in Y if iy["type"] == yt]
    res.append(dict(unit=u, name=name, b_range=[B[0]["n"], B[-1]["n"]], y_range=[Y[0]["n"], Y[-1]["n"]],
                    btypes=[dict(no=bt[0], title=bt[1], nums=[ib["n"] for ib in B if ib["type"] == bt], reps=[ib["n"] for ib in B if ib["type"] == bt and ib["rep"]]) for bt in btypes],
                    ytypes=[dict(no=yt[0], title=yt[1], range=[yr(yt)[0], yr(yt)[-1]], btype=(tmap[yt][1][0] if tmap[yt] else None), fit=round(tmap[yt][0], 2) if tmap[yt] else 0) for yt in ytypes],
                    y_mix=[iy["n"] for iy in Y if iy["stage"] == "종합"],
                    lite=(L is not None), must=must))
    print("%d단원 %s: 꼭 풀 %d문항 (대표 %d, 쌍둥이·같은 틀 있는 문항 %d)" % (u, name, len(must), sum(m["rep"] for m in must), sum(1 for m in must if m["twins"])))
json.dump(res, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
