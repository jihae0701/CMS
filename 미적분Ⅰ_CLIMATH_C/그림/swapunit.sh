#!/bin/bash
# 사용: swapunit.sh 02   (figw/m1_02/out/widths.json의 iN → imageN 으로 u/m1_02.hwpx 그림 바꾸기, 결과 u/m1_02.hwpx; 전 파일은 u/m1_02_prefig.hwpx)
S=/tmp/claude-0/-home-user-CMS/7a122d51-a5b1-5def-9637-d43cb9a9b6ef/scratchpad; u=m1_$1
cd $S/eqw
[ -f u/${u}_prefig.hwpx ] || cp u/$u.hwpx u/${u}_prefig.hwpx
args=$(python3 -c "
import json;W=json.load(open('$S/figw/$u/out/widths.json'))
print(' '.join('image%s=$S/figw/$u/out/%s.png@%d'%(k[1:],k,w) for k,w in W.items() if k[1:].isdigit()))")
python3 /home/user/CMS/.claude/skills/math-figure-rules/hwpx_swapimg.py u/${u}_prefig.hwpx u/$u.hwpx $args
python3 fix_lsa.py u/$u.hwpx >/dev/null
bash final_check.sh $u
python3 figcheck.py $S/in2/$u.hwpx u/$u.hwpx $S/figw/$u/sheet_after.png | grep -c 바꿈
