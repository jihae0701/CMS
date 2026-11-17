# -*- coding: utf-8 -*-
"""묶지 않은 위 첨자가 길게 이어진 곳 찾기(2^x+3 +1, 4^-(x+2), a^2x, a^x^3 …): python3 supchk.py 파일 [n...]"""
import sys, re, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mjedit import Ed
P = re.compile(r'\^\s?(-[\w(]|[A-Za-z0-9.]+[+\-(][\w(]|[0-9]+[A-Za-z]|[A-Za-z]\^|[A-Za-z0-9]+\{)')
if __name__ == '__main__':
  e = Ed(sys.argv[1])
  ns = list(map(int, sys.argv[2:])) or range(1, 90)
  for n in ns:
      for part in ('q', 'sol'):
          try:
              sc = e.scripts(n, part)
          except Exception:
              continue
          for s in sc:
              if P.search(s.replace('^{', '^@')):
                  print(n, part, '|', s[:160])
