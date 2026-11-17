# python3 big.py NN [imageX ...] → mM_NN/big.png (새 그림 원본을 크게)
import sys, io, json, zipfile
from PIL import Image, ImageDraw, ImageFont
S = '/tmp/claude-0/-home-user-CMS/7a122d51-a5b1-5def-9637-d43cb9a9b6ef/scratchpad'
u = sys.argv[1]; only = sys.argv[2:]
plan = json.load(open('%s/mfig/mM_%s/plan.json' % (S, u)))
z = zipfile.ZipFile('%s/eqw/u/mM_%s_prefig.hwpx' % (S, u))
font = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc', 22)
cells = []
for k, v in plan.items():
    if 'c_n' in v or (only and k not in only): continue
    try: im = Image.open(io.BytesIO(z.read(v['href']))).convert('RGB')
    except Exception: continue
    im.thumbnail((620, 430)); cells.append(('%s %d%s w%d' % (k, v['n'], v['part'], v['w']), im))
W, H = 640, 460; rows = (len(cells) + 1) // 2
sh = Image.new('RGB', (2 * W, max(1, rows) * H), 'white'); d = ImageDraw.Draw(sh)
for i, (n, im) in enumerate(cells):
    x, y = (i % 2) * W, (i // 2) * H
    d.text((x + 4, y + 2), n, fill='red', font=font); sh.paste(im, (x + 10, y + 28))
sh.save('%s/mfig/mM_%s/big.png' % (S, u)); print(len(cells))
