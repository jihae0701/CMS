#!/bin/bash
# 사용: final_check.sh 단원코드  (u/단원.hwpx 를 원본과 비교 검사)
S=/tmp/claude-0/-home-user-CMS/7a122d51-a5b1-5def-9637-d43cb9a9b6ef/scratchpad; u=$1
cd $S/eqw
python3 figcheck.py $S/in2/$u.hwpx u/$u.hwpx $S/figs_$u.png | tail -1
python3 refcheck.py u/$u.hwpx | tail -2
python3 tools/eqcheck.py --all u/$u.hwpx | tail -4
cp u/$u.hwpx $S/chk_$u.hwpx; cp $S/in2/$u.hwpx $S/chk_o_$u.hwpx
r=$(cd $S/h2x && java -cp .:hwp2hwpx/target/lib/hwpxlib-1.0.9.jar ReadX $S/chk_$u.hwpx 2>&1 | grep -v JAVA_TOOL | awk '{print $1}')
o=$(cd $S/h2x && java -cp .:hwp2hwpx/target/lib/hwpxlib-1.0.9.jar ReadX $S/chk_o_$u.hwpx 2>&1 | grep -v JAVA_TOOL | awk '{print $1}')
echo "hwpxlib: 결과 $r (원본 $o)"
python3 -I -c "
import zipfile;from xml.dom import minidom
z=zipfile.ZipFile('u/$u.hwpx');[minidom.parseString(z.read(n)) for n in z.namelist() if n.endswith(('.xml','.hpf'))];print('xml ok')"
