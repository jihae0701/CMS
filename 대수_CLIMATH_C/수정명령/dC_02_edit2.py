import sys
sys.path.insert(0, '.')
from mjedit import Ed
ed = Ed('u_dC/dC_02.hwpx')
t = '이때 판별식 ⟦D over 4 =9-2>0⟧이고 ⟦alpha + beta >0⟧, ⟦alpha beta >0⟧이므로 ⟦alpha⟧, ⟦beta⟧는 서로 다른 두 양의 실근이다.'
ed.op({'op': 'del_para', 'n': 39, 'part': 'sol', 'anchor': '서로 다른 두 양의 실근'})
ed.op({'op': 'add_para', 'n': 39, 'part': 'sol', 'after': '⟦alpha + beta =6,~alpha beta =2⟧', 'text': t})
ed.T(55, 'sol', '이 때, ', '이때, ', optional=True)
ed.run('u_dC/dC_02_edit2.json')
