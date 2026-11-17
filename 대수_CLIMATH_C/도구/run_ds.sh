#!/bin/bash
# 사용: run_ds.sh 번호(02) "단원 이름" — 대수 CLIMATH(C): 미적분Ⅰ C 1단원 완성본의 틀(바탕쪽 '미적분Ⅰ'→'대수', CLIMATH 로고) + 글꼴 + 자동 수식 정리 + 검사
S=/tmp/claude-0/-home-user-CMS/7a122d51-a5b1-5def-9637-d43cb9a9b6ef/scratchpad; cd $S/eqw
BASE="/home/user/CMS/미적분Ⅰ_CLIMATH_C/1. 함수의 극한.hwpx"
n=$1; name=$2; u=dC_$n; F=u_dC/$u.hwpx
python3 mk_mj.py "$BASE" $S/ds/in/$u.hwpx $F ${n#0} "$name" > u_dC/${u}_mk.json || exit 1
python3 - $F "$BASE" <<'PY'
import zipfile, shutil, sys, re
p, base = sys.argv[1], sys.argv[2]; logo = zipfile.ZipFile(base).read('BinData/image1.png')
t = p + '.tmp'; zi = zipfile.ZipFile(p); zo = zipfile.ZipFile(t, 'w'); c = 0
hpf = zi.read('Contents/content.hpf').decode(); href = re.search(r'<opf:item id="image1" href="([^"]+)"', hpf).group(1)
for i in zi.infolist():
    d = zi.read(i.filename)
    if 'masterpage' in i.filename:
        s = d.decode(); c += s.count('미적분')
        s = s.replace('<hp:t>미적분Ⅰ</hp:t>', '<hp:t>대수</hp:t>').replace('<hp:t>미적분</hp:t>', '<hp:t>대수</hp:t>').replace('<hp:t>Ⅰ</hp:t>', '<hp:t/>')
        d = s.encode()
    if i.filename == href: d = logo
    zo.writestr(i, d, compress_type=i.compress_type)
zo.close(); shutil.move(t, p); print('바탕쪽 미적분Ⅰ→대수', c, '로고', href)
PY
python3 fontfix.py $F "$BASE"
python3 limfix.py $F u_dC/${u}_lim.json
python3 eqauto.py $F u_dC/${u}_eq.json
python3 fracfix.py $F u_dC/${u}_frac.json
python3 glue2.py $F | tail -1
python3 emptygrp.py $F
python3 eqauto.py $F u_dC/${u}_eq2.json
python3 negsub.py $F
python3 style_ida.py $F | tail -1; python3 space_before_eq.py $F | tail -1; python3 setglue.py $F | tail -1; python3 fix_lsa.py $F $F | tail -1
python3 wordfix.py $F | tail -1
python3 ansnorm.py $F 2>&1 | tail -2
python3 fix_lsa.py $F $F | tail -1
cp $F u/$u.hwpx; cp $S/ds/in/$u.hwpx $S/in2/$u.hwpx
bash final_check.sh $u 2>&1 | tail -7
