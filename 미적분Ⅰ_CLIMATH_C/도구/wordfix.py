# -*- coding: utf-8 -*-
"""문항(문제·해설) 글의 표현 통일: 구하여라→구하시오, 만족할→만족시킬, 만족하는→만족시키는, 만족하도록→만족시키도록,
닫힌 구간→닫힌구간, 열린 구간→열린구간, 풀이참조→풀이 참조, 사잇값의 정리→사잇값 정리 (줄 배치 위치도 맞춤)
    python3 wordfix.py 파일.hwpx"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hwpxedit as H
W = [('구하여라', '구하시오'), ('만족할 때', '만족시킬 때'), ('만족하는', '만족시키는'), ('만족하도록', '만족시키도록'), ('만족한다', '만족시킨다'),
     ('닫힌 구간', '닫힌구간'), ('열린 구간', '열린구간'), ('풀이참조', '풀이 참조')]
path = sys.argv[1]
x = H.load(path)
cnt = {}
for n in range(1, len(H.endnotes(x)) + 1):
    for part in ('q', 'sol'):
        for old, new in W:
            try:
                x = H.op_text(x, H.region(x, n, part), old, new, None, False, True, None)
                cnt[old] = cnt.get(old, 0) + 1
            except Exception:
                pass
H.save(path, x)
print(os.path.basename(path), cnt)
