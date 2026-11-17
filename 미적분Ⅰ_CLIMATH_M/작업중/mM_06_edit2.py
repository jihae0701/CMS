# -*- coding: utf-8 -*-
# 수식 속 한글(단위 '/초', '(단, …)')을 수식 밖 글로 (C와 같은 꼴)
import sys
sys.path.insert(0, '.')
from mjedit import Ed
ed = Ed('u_mM/mM_06.hwpx')
op = ed.op
op({'op': 'eq', 'n': 21, 'part': 'q', 'old': 'rmcm^2 /초', 'new': 'rm cm^2'})
op({'op': 'append', 'n': 21, 'part': 'q', 'after_eq': 'rm cm^2', 'text': '/초'})
op({'op': 'eq', 'n': 22, 'part': 'sol', 'old': '= {pi} over {50} (t-100)^2 (t+10)`````(단, ``0 leq t leq 100)', 'new': '= {pi} over {50} (t-100)^2 (t+10)'})
op({'op': 'append', 'n': 22, 'part': 'sol', 'after_eq': '= {pi} over {50} (t-100)^2 (t+10)', 'text': ' (단, 0 leq t leq 100)'})
op({'op': 'text_eq', 'n': 22, 'part': 'sol', 'old': '0 leq t leq 100', 'pre': '', 'eq': '0 leq t leq 100', 'post': '', 'sub': True})
op({'op': 'eq', 'n': 36, 'part': 'q', 'old': 'a`rmcm^3 /초', 'new': 'a`rm cm^3'})
op({'op': 'append', 'n': 36, 'part': 'q', 'after_eq': 'a`rm cm^3', 'text': '/초'})
op({'op': 'eq', 'n': 36, 'part': 'sol', 'old': '{40} over {3} pi times 9=120 pi``(rmcm^3 /초)', 'new': '{40} over {3} pi times 9=120 pi'})
op({'op': 'append', 'n': 36, 'part': 'sol', 'after_eq': '{40} over {3} pi times 9=120 pi', 'text': ' (rm cm^3/초)'})
op({'op': 'text_eq', 'n': 36, 'part': 'sol', 'old': 'rm cm^3', 'pre': '', 'eq': 'rm cm^3', 'post': '', 'sub': True})
ed.run('u_mM/mM_06_edit2.json')
