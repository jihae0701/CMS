#!/bin/bash
# 사용: run_mj.sh 번호(02) "단원 이름"  — 틀 + 자동 수식 정리 + 검사
S=/tmp/claude-0/-home-user-CMS/7a122d51-a5b1-5def-9637-d43cb9a9b6ef/scratchpad; cd $S/eqw
n=$1; name=$2; u=m1_$n; F=u_mj/$u.hwpx
python3 mk_mj.py u/m1_01.hwpx $S/mj/in/$u.hwpx $F ${n#0} "$name" > u_mj/${u}_mk.json
python3 limfix.py $F u_mj/${u}_lim.json
python3 eqauto.py $F u_mj/${u}_eq.json
python3 fracfix.py $F u_mj/${u}_frac.json
python3 glue2.py $F | tail -1
python3 emptygrp.py $F
python3 eqauto.py $F u_mj/${u}_eq2.json
python3 style_ida.py $F | tail -1; python3 space_before_eq.py $F | tail -1; python3 setglue.py $F | tail -1; python3 fix_lsa.py $F $F | tail -1
cp $F u/$u.hwpx; cp $S/mj/in/$u.hwpx $S/in2/$u.hwpx
bash final_check.sh $u 2>&1 | tail -7
