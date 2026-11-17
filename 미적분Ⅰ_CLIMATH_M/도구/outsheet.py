import sys, glob, os
from PIL import Image, ImageDraw, ImageFont
d = sys.argv[1]; names = sys.argv[2:]
fs = sorted(glob.glob(d + '/out/i*.png'), key=lambda p: int(os.path.basename(p)[1:-4]))
if names: fs = [f for f in fs if os.path.basename(f)[:-4] in names]
font = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc', 22)
cells = []
for f in fs:
    im = Image.open(f).convert('RGB'); im.thumbnail((520, 360)); cells.append((os.path.basename(f), im))
cols = 2; W, H = 540, 390; rows = (len(cells) + 1) // 2
sh = Image.new('RGB', (cols * W, rows * H), 'white'); dr = ImageDraw.Draw(sh)
for i, (n, im) in enumerate(cells):
    x, y = (i % cols) * W, (i // cols) * H
    dr.text((x + 4, y + 2), n, fill='red', font=font); sh.paste(im, (x + 10, y + 28))
sh.save(d + '/outsheet.png'); print(len(cells))
