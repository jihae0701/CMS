# 라이트 파일과 유형서 완성본의 '단원종합문제' 블록을 비교해 그대로인 번호를 알려 준다.
# 사용: python3 lite_same.py <단원 파일 이름(확장자 없이)> <단원종합 첫 번호>
import zipfile, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lite import top_paras
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
def blocks(f):
    s = zipfile.ZipFile(f).read("Contents/section0.xml").decode()
    h = s.find("단원 종합 문제"); h = h if h >= 0 else s.find("단원종합문제")
    allp = top_paras(s, 0, len(s)); hp = [k for k, (a, z) in enumerate(allp) if a <= h < z][0]; ps = allp[hp + 1:]
    st = [k for k, (a, z) in enumerate(ps) if "<hp:endNote" in s[a:z]]
    return [s[ps[k][0]:ps[(st[n + 1] if n + 1 < len(st) else len(ps)) - 1][1]] for n, k in enumerate(st)]
u, first = sys.argv[1], int(sys.argv[2])
A = blocks(os.path.join(ROOT, "공통수학1", u + ".hwpx")); B = blocks(os.path.join(ROOT, "스토리라이트", "공통수학1", u + ".hwpx"))
print(len(A), len(B), "그대로:", [first + i for i, (a, b) in enumerate(zip(A, B)) if a == b])
