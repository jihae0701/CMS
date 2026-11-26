# -*- coding: utf-8 -*-
"""CLIMATH(m) 대수: 바탕쪽 아래 흰 네모(4473×1866, 흰 채움, 글 앞) 지우기 (2026-11-26).
python drop_mp_whitebox.py <hwpx> ...   (제자리에 고쳐 씀)
- 사용자: 1단원 수정본에서 '바탕쪽 각 페이지 아래 흰 사각형 모두 지웠어' → 다른 단원·워크북 바탕쪽에서도 지움. 빌더(build_c.py·alg_wb_build.py)도 이 함수를 씀.
"""
import re, sys, zipfile

PAT = re.compile(r'<hp:rect [^>]*textWrap="IN_FRONT_OF_TEXT"[^>]*>(?:(?!</hp:rect>).)*?faceColor="#FFFFFF"(?:(?!</hp:rect>).)*?<hp:sz width="4473"(?:(?!</hp:rect>).)*?</hp:rect>', re.S)


def drop(xml):
    return PAT.subn("", xml)


if __name__ == "__main__":
    for f in sys.argv[1:]:
        z = zipfile.ZipFile(f)
        items = [(i, z.read(i.filename)) for i in z.infolist()]
        z.close()
        n = 0
        out = []
        for info, data in items:
            if re.match(r"Contents/masterpage\d+\.xml", info.filename):
                s, k = drop(data.decode("utf-8"))
                n += k
                data = s.encode("utf-8")
            out.append((info, data))
        with zipfile.ZipFile(f, "w") as w:
            for info, data in out:
                w.writestr(info, data)
        print(f, "흰 네모", n, "개 지움")
