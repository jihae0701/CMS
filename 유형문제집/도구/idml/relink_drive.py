# -*- coding: utf-8 -*-
"""IDML 링크의 드라이브 글자 바꾸기 (2026-11-19).
python relink_drive.py <원래 드라이브> <새 드라이브> <IDML> ...   예) relink_drive.py H E a.idml b.idml
- 사용자 화면(탐색기)에서 자료가 'Toshiba Canvio Hard Drive (E:)\\수학자료[최지혜]\\2027 예비고1 교재'에 있음 → 링크 'file:H:/…'를 'file:E:/…'로.
  폴더·파일 이름은 그대로(사용자 탭의 '1. 평면좌표.pdf', '01_평면좌표.pdf'와 같음).
"""
import sys, re, zipfile, os

old, new = sys.argv[1], sys.argv[2]
for path in sys.argv[3:]:
    z = zipfile.ZipFile(path)
    names = z.namelist()
    files = {n: z.read(n) for n in names}
    cnt = 0
    for n in names:
        if n.endswith(".xml"):
            s = files[n].decode("utf-8")
            s2, k = re.subn(r'file:%s:/' % old, 'file:%s:/' % new, s)   # 링크 + 링크 정보(라벨)의 경로 모두
            if k:
                files[n] = s2.encode("utf-8"); cnt += k
    tmp = path + ".tmp"
    with zipfile.ZipFile(tmp, "w") as w:
        for n in names:
            info = z.getinfo(n)
            info2 = zipfile.ZipInfo(n, date_time=info.date_time)
            info2.compress_type = zipfile.ZIP_STORED if n == "mimetype" else zipfile.ZIP_DEFLATED
            w.writestr(info2, files[n])
    os.replace(tmp, path)
    print(os.path.basename(path), "링크", cnt, "개", old, "→", new)
