import sys
sys.path.insert(0, '.')
from mjedit import Ed
ed = Ed('u_dC/dC_10.hwpx')
# 19 정답 줄: '5' 지우고 180만
ed.op({'op': 'del_eq', 'n': 19, 'part': 'sol', 'old': '180'})
ed.op({'op': 'eq', 'n': 19, 'part': 'sol', 'old': '5', 'new': '180', 'first': True})
# 4 ⑴ 해설: 첫째항 1, 공비 4
ed.op({'op': 'eq', 'n': 4, 'part': 'sol', 'old': '3', 'new': '1', 'nth': 1})
ed.op({'op': 'eq', 'n': 4, 'part': 'sol', 'old': '3', 'new': '4', 'nth': 1})
ed.run('u_dC/dC_10_edit2.json')
