import sys
sys.path.insert(0, '/home/user/CMS/.claude/skills/math-figure-rules'); sys.path.insert(0, sys.argv[2])
from mathfig import fit_shoot
from nl import numline
OUT = sys.argv[1]
# 21번 해설: -1 ≤ a < 3 과 1 ≤ a ≤ 4 의 공통 범위 1 ≤ a < 3
f = lambda: numline([(-1, '-1', True), (1, '1', True), (3, '3', False), (4, '4', True)], [(-1, 3, 1), (1, 4, 2)], -2.2, 5.6, 'a', shade=(1, 3, 1))
print('폭', fit_shoot(OUT + '/c1_05_21.png', f))
