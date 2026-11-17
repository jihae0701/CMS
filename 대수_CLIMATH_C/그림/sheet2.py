# 사용: sheet2.py 출력.png 그림파일... (2열, 큰 칸)
import sys
from PIL import Image, ImageDraw, ImageFont, ImageChops
out, fs = sys.argv[1], sys.argv[2:]
cw, ch = 900, 760
S = Image.new('RGB', (cw * 2, ch * ((len(fs) + 1) // 2)), 'white'); d = ImageDraw.Draw(S)
font = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc', 30)
for i, f in enumerate(fs):
    im = Image.open(f).convert('RGB')
    bg = Image.new('RGB', im.size, 'white'); bb = ImageChops.difference(im, bg).getbbox()
    if bb: im = im.crop(bb)
    im.thumbnail((cw - 20, ch - 50))
    r, c = divmod(i, 2)
    S.paste(im, (c * cw + 10, r * ch + 45)); d.text((c * cw + 10, r * ch + 5), f.split('/')[-1], fill='red', font=font)
S.save(out)
