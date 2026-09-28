# python3 sheet.py <outdir> <prefix> [cols] [scale]: join screen shots <prefix>NN.png side by side into sheets
import sys, glob
from PIL import Image
d, pre = sys.argv[1], sys.argv[2]; cols = int(sys.argv[3]) if len(sys.argv) > 3 else 4; sc = float(sys.argv[4]) if len(sys.argv) > 4 else .5
fs = sorted(glob.glob(f'{d}/{pre}[0-9][0-9].png'))
for k in range(0, len(fs), cols):
    ims = [Image.open(f).convert('RGB') for f in fs[k:k + cols]]
    w, h = ims[0].size; W, H = int(w * sc), int(h * sc); g = 14
    s = Image.new('RGB', (len(ims) * (W + g) - g, H), (38, 38, 38))
    for j, im in enumerate(ims):
        s.paste(im.resize((W, int(im.size[1] * sc))), (j * (W + g), 0))
    s.save(f'{d}/{pre}sheet{k // cols}.png'); print(f'{d}/{pre}sheet{k // cols}.png')
