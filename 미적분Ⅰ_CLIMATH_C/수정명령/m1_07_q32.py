# -*- coding: utf-8 -*-
"""7단원 32번: 31번과 같은 문제였던 것을 다른 문제로 (f'(x)=3x(x-2), 극솟값 -1 → 극댓값 3, 단답형)"""
import sys
sys.path.insert(0, '.')
from mjedit import Ed
for f in sys.argv[1:]:
    ed = Ed(f)
    E, T, SA, op = ed.E, ed.T, ed.SA, ed.op
    op({'op': 'eq', 'n': 32, 'part': 'q', 'old': "f`'(x)=3x(x-4)", 'new': "f`'(x)=3x(x-2)"})
    op({'op': 'eq', 'n': 32, 'part': 'q', 'old': '5', 'new': '-1'})
    SA(32, '3', '④', ending='극솟값은?', new_ending='극댓값을 구하시오.')
    T(32, 'q', '극댓값이', '극솟값이')
    op({'op': 'eq', 'n': 32, 'part': 'sol', 'old': 'x=4', 'new': 'x=2', 'all': True})
    op({'op': 'eq', 'n': 32, 'part': 'sol', 'old': '4', 'new': '2'})
    op({'op': 'eq', 'n': 32, 'part': 'sol', 'old': 'f(x)= int f` prime (x)dx= int 3x(x-4)dx', 'new': 'f(x)= int f` prime (x)dx= int 3x(x-2)dx'})
    op({'op': 'eq', 'n': 32, 'part': 'sol', 'old': '= int {(3x ^{2} -12x)dx} =x ^{3} -6x ^{2} +C', 'new': '= int {(3x ^{2} -6x)dx} =x ^{3} -3x ^{2} +C'})
    T(32, 'sol', '극댓값이', '극솟값이')
    op({'op': 'eq', 'n': 32, 'part': 'sol', 'old': '5', 'new': '-1'})
    op({'op': 'eq', 'n': 32, 'part': 'sol', 'old': 'f(0)=C=5', 'new': 'f(2)=8-12+C= it-1'})
    T(32, 'sol', '=5', '=3')
    op({'op': 'eq', 'n': 32, 'part': 'sol', 'old': ' f(x)=x^3 -6x^2 +5', 'new': ' f(x)=x^3 -3x^2 +3'})
    T(32, 'sol', '극솟값은', '극댓값은')
    op({'op': 'eq', 'n': 32, 'part': 'sol', 'old': 'f(4)=64-96+5= it-27', 'new': 'f(0)=3'})
    ed.run()
