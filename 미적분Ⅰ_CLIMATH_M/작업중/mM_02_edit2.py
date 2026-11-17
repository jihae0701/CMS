# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '.')
from mjedit import Ed
ed = Ed('u_mM/mM_02.hwpx')
ed.op({'op': 'eq', 'n': 9, 'part': 'sol', 'old': '(2,~-2)', 'new': '(-2,~2)'})
ed.run('u_mM/mM_02_edit2.json')
