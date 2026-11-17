#!/bin/bash
# 사용: run_mM.sh 번호(02) "단원 이름" — CLIMATH(M): C 1단원 완성본의 틀(머리말 CLIMATH ⓜ) + 자동 수식 정리 + 검사
S=/tmp/claude-0/-home-user-CMS/7a122d51-a5b1-5def-9637-d43cb9a9b6ef/scratchpad; cd $S/eqw
n=$1; name=$2; u=mM_$n; F=u_mM/$u.hwpx
python3 mk_mj.py u/m1_01.hwpx $S/mM/in/$u.hwpx $F ${n#0} "$name" > u_mM/${u}_mk.json
python3 - $F <<'PY'
import zipfile, shutil, sys
p = sys.argv[1]; t = p + '.tmp'; zi = zipfile.ZipFile(p); zo = zipfile.ZipFile(t, 'w'); c = 0
for i in zi.infolist():
    d = zi.read(i.filename)
    if 'masterpage' in i.filename:
        s = d.decode(); c += s.count('ⓒ'); d = s.replace('ⓒ', 'ⓜ').encode()
    zo.writestr(i, d, compress_type=i.compress_type)
zo.close(); shutil.move(t, p); print('ⓒ→ⓜ', c)
PY
python3 limfix.py $F u_mM/${u}_lim.json
python3 eqauto.py $F u_mM/${u}_eq.json
python3 fracfix.py $F u_mM/${u}_frac.json
python3 glue2.py $F | tail -1
python3 emptygrp.py $F
python3 eqauto.py $F u_mM/${u}_eq2.json
python3 style_ida.py $F | tail -1; python3 space_before_eq.py $F | tail -1; python3 setglue.py $F | tail -1; python3 fix_lsa.py $F $F | tail -1
python3 wordfix.py $F | tail -1
cp $F u/$u.hwpx; cp $S/mM/in/$u.hwpx $S/in2/$u.hwpx
bash final_check.sh $u 2>&1 | tail -7
