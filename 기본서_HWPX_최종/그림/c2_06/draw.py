import sys
sys.path.insert(0, '/home/user/CMS/.claude/skills/math-figure-rules')
sys.path.insert(0, '/tmp/claude-0/-home-user-CMS/7a122d51-a5b1-5def-9637-d43cb9a9b6ef/scratchpad/figw/common')
from mathfig import fit_shoot
from nl2 import numline2
OUT = sys.argv[1]

def f21():   # P={x | x≥a}, Q={x | 1≤x<3}
    F = numline2(-1.4, 5.0, [(0, None, 2, '$P$'), (1.6, 3.6, 1, '$Q$')],
                 [(0, '\\mathit{a}', True), (1.6, '1', True), (3.6, '3', False)], unit=70, hstep=0.75, bottom=-1.0)
    return F.render()

print('21', fit_shoot(OUT + '/c2_06_21.png', f21))
