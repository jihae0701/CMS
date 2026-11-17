# python3 sheet.py NN  → mfig/mM_NN/match.png (M 원본 | C 다시 그린 것), new.png (새 그림)
import sys, io, json, zipfile, glob, os
from PIL import Image, ImageDraw, ImageFont
S = '/tmp/claude-0/-home-user-CMS/7a122d51-a5b1-5def-9637-d43cb9a9b6ef/scratchpad'
u = sys.argv[1]
D = '/home/user/CMS/미적분Ⅰ_CLIMATH_C'
cf = [f for f in glob.glob(D + '/*.hwpx') if os.path.basename(f).startswith('%d. ' % int(u))][0]
plan = json.load(open('%s/mfig/mM_%s/plan.json' % (S, u)))
zm = zipfile.ZipFile('%s/eqw/u/mM_%s.hwpx' % (S, u)); zf = zipfile.ZipFile(cf)
try: font = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc', 18)
except Exception: font = ImageFont.load_default()
def th(z, h, size=260):
    try:
        im = Image.open(io.BytesIO(z.read(h))).convert('RGB')
    except Exception:
        im = Image.new('RGB', (200, 100), (255, 200, 200)); ImageDraw.Draw(im).text((5, 40), 'unreadable ' + h, fill='black')
    im.thumbnail((size, size)); return im
def grid(cells, out, cols):
    W, Hh = 560 if cols == 2 else 280, 300
    rows = (len(cells) + cols - 1) // cols
    sh = Image.new('RGB', (cols * W, max(1, rows) * Hh), 'white'); d = ImageDraw.Draw(sh)
    for i, (lab, ims) in enumerate(cells):
        x0, y0 = (i % cols) * W, (i // cols) * Hh
        d.text((x0 + 4, y0 + 2), lab, fill='red', font=font)
        x = x0 + 4
        for im in ims:
            sh.paste(im, (x, y0 + 26)); x += 276
    sh.save(out)
mc = [(f"{k} {v['n']}{v['part']} d{v['d']} {'↺' if v.get('redrawn') else '='}", [th(zm, v['href']), th(zf, v['f_href'])]) for k, v in plan.items() if 'f_href' in v]
nw = [(f"{k} {v['n']}{v['part']} {v['w']}", [th(zm, v['href'])]) for k, v in plan.items() if 'c_n' not in v]
grid(mc, '%s/mfig/mM_%s/match.png' % (S, u), 2)
grid(nw, '%s/mfig/mM_%s/new.png' % (S, u), 4)
print(u, len(mc), len(nw))
