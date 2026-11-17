#!/bin/bash
# 사용: inv.sh 03 → 그림 목록과 보기 시트(v1.png …)
S=/tmp/claude-0/-home-user-CMS/7a122d51-a5b1-5def-9637-d43cb9a9b6ef/scratchpad; u=dC_$1
mkdir -p $S/figw/$u/src $S/figw/$u/out; cd $S/figw/$u/src && rm -rf BinData && unzip -oq $S/eqw/u/$u.hwpx 'BinData/*'
cd $S/eqw; python3 figcheck.py $S/in2/$u.hwpx u/$u.hwpx $S/figw/$u/sheet.png | grep '번' | grep -v 'image1 \|image2 ' > $S/figw/$u/map.txt
cat $S/figw/$u/map.txt
cd $S/figw/$u/src/BinData
L=$(ls | grep -v -E '^image(1|2)\.png$' | grep -iE 'bmp|jpg|gif' | sort -V)
i=1; set -- $L
while [ $# -gt 0 ]; do python3 ../../../sheet2.py ../../v$i.png ${@:1:6}; shift 6 2>/dev/null || shift $#; i=$((i+1)); done
echo sheets $((i-1))
