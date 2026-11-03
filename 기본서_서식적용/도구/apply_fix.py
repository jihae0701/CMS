"""python3 apply_fix.py 공통수학1_03
- 원본: /home/user/CMS/기본서_서식적용/<과목>/<n>. ….hwp (읽기만 함)
- 명령: fix/spec/<KEY>.json  (명령 목록)
- 결과: fix/out/<KEY>.hwp, 결과 글: fix/out/<KEY>.txt
명령을 위에서부터 차례로 적용한다(뒤 명령의 old는 앞 명령이 바뀐 뒤의 글 기준). 실패한 명령은 번호와 이유를 출력한다."""
import sys, os, glob, json, struct, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import hwpedit as H

key = sys.argv[1]
subj, n = key.split('_')
src = [f for f in glob.glob(f'/home/user/CMS/기본서_서식적용/{subj}/*.hwp') if int(os.path.basename(f).split('.')[0]) == int(n)][0]
ops = json.load(open(f'{HERE}/fix/spec/{key}.json'))
d = H.Doc(src)
pn = d.remove_page_numbers()
fails = []
for i, op in enumerate(ops):
    try:
        d.apply(op)
    except H.EditError as e:
        fails.append((i, str(e), op))
    except Exception as e:
        fails.append((i, 'ERROR ' + type(e).__name__ + ' ' + str(e), op))
out = f'{HERE}/fix/out/{key}.hwp'
d.save(out)
# 구조 검사
d2 = H.Doc(out)
for p in d2.paras():
    us = p.units()
    nch = sum(len(u[2]) for u in us) // 2
    hn = struct.unpack_from('<I', d2.rs[p.hdr][2], 0)[0] & 0x7fffffff
    assert nch == hn or (nch == 0 and hn == 1), ('nchars', p.text()[:40])
    ext = [u for u in us if u[0] == 'x' and u[1] in H.EXT]
    cs = p.ctrls()
    assert len(cs) == len(ext), ('ctrls', p.text()[:40])
    for u, (a, _) in zip(ext, cs):
        assert u[2][2:6] == d2.rs[a][2][:4], ('ctrl order', p.text()[:60])
H.dump_regions(out, f'{HERE}/fix/out/{key}.txt')
v = subprocess.run([sys.executable, f'{HERE}/validate_pyhwp.py', out], capture_output=True, text=True).stdout.strip()
print(f'쪽 번호 지움 {pn}곳, 명령 {len(ops)}개 중 성공 {len(ops) - len(fails)}, 실패 {len(fails)}')
print('pyhwp 검사:', 'OK' if 'FAIL' not in v else v)
for i, e, op in fails:
    print(f'  실패 #{i}: {e}\n     {json.dumps(op, ensure_ascii=False)[:300]}')
sys.exit(1 if fails or 'FAIL' in v else 0)
