# -*- coding: utf-8 -*-
"""한글 수식에서 '<-'는 왼쪽 화살표(←) 명령이라 'x<-1'이 'x←1'로 보인다.
수식 스크립트 안의 '<-'를 '< it-'로 바꾼다(사용자가 쓰는 방식, 학원 초안도 같음).

python eqfix.py 파일.hwpx [...]   (그 자리에서 고친다)
gen.py와 기본서/applyform.py가 저장할 때 자동으로 부른다.
"""
import re, sys, zipfile, os, shutil

PAT = re.compile(r"(<hp:script[^>]*>)(.*?)(</hp:script>)", re.S)


def fix_script(sc):
    """이스케이프된 스크립트(&lt;) 기준"""
    return re.sub(r"&lt;\s*-(?!&gt;)", "&lt; it-", sc)


def fix_xml(xml):
    n = [0]

    def rep(m):
        new = fix_script(m.group(2))
        if new != m.group(2):
            n[0] += 1
        return m.group(1) + new + m.group(3)
    return PAT.sub(rep, xml), n[0]


def fix_file(path):
    zin = zipfile.ZipFile(path)
    items = [(i, zin.read(i.filename)) for i in zin.infolist()]
    zin.close()
    total = 0
    out = []
    for info, data in items:
        if info.filename.startswith("Contents/section") and info.filename.endswith(".xml"):
            xml, n = fix_xml(data.decode("utf-8"))
            total += n
            data = xml.encode("utf-8")
        out.append((info, data))
    if total:
        tmp = path + ".tmp"
        with zipfile.ZipFile(tmp, "w") as z:
            for info, data in out:
                z.writestr(info, data, compress_type=info.compress_type)
        shutil.move(tmp, path)
    return total


if __name__ == "__main__":
    for p in sys.argv[1:]:
        print(fix_file(p), p)
