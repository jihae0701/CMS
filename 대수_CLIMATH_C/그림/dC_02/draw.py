# -*- coding: utf-8 -*-
"""대수 C 2. 로그 — 4번 해설 수직선 다시 그리기"""
import sys
sys.path.insert(0, '/tmp/claude-0/-home-user-CMS/7a122d51-a5b1-5def-9637-d43cb9a9b6ef/scratchpad/figw')
sys.path.insert(0, '/tmp/claude-0/-home-user-CMS/7a122d51-a5b1-5def-9637-d43cb9a9b6ef/scratchpad/figw/common')
from nl2 import numline2
from dcommon import run
OUT = sys.argv[1]


def i2():
    F = numline2(-0.4, 4.6, [(1, 2, 1, '㉠'), (2, None, 1, '㉠'), (None, 3, 2, '㉡')], [(1, '1', False), (2, '2', False), (3, '3', False)],
                 shade=[(1, 2, 1), (2, 3, 1)], unit=70)
    return F.render()


JOBS = {'i2': i2}
if __name__ == '__main__':
    run(JOBS, OUT, sys.argv[2:])
