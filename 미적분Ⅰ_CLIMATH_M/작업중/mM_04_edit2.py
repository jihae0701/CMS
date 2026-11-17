# -*- coding: utf-8 -*-
# (10·55 정답 줄은 한 번 적용함) 56 ㉤ → ㉣ (줄바꿈이 든 글 조각이라 XML에서 바로)
import sys
sys.path.insert(0, '.')
import hwpxedit as H
P = 'u_mM/mM_04.hwpx'
x = H.load(P)
old = ' ㉤<hp:lineBreak/>㉢, ㉤에서 '
assert x.count(old) == 1
H.save(P, x.replace(old, ' ㉣<hp:lineBreak/>㉢, ㉣에서 '))
