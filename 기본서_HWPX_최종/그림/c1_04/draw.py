import sys
sys.path.insert(0, '/home/user/CMS/.claude/skills/math-figure-rules')
from mathfig import Frame, fit_shoot, dim_arc
OUT = sys.argv[1]

def fig_tri():
    # 14번: 삼각형 ABC, 세 변 a=BC, b=CA, c=AB 를 점선 호로 표시 (원본 배치 그대로)
    F = Frame((-1.0, 7.7), (-1.75, 4.9), 40, 40, (16, 16, 16, 16))
    B, C, A = (0, 0), (6.7, 0), (4.5, 4.1)
    F.seg(A, B, 3.2); F.seg(B, C, 3.2); F.seg(C, A, 3.2)
    F.pt(A, r"A", "cb", 0, -8); F.pt(B, r"B", "rc", -8, 0); F.pt(C, r"C", "lc", 8, 0)
    dim_arc(F, B, C, "a", 1, 22)
    dim_arc(F, B, A, "c", -1, 22)
    dim_arc(F, A, C, "b", -1, 22)
    return F.render()

print('폭', fit_shoot(OUT + '/c1_04_14.png', fig_tri))
