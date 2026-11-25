import sys, numpy as np, potrace
from PIL import Image
src, out = sys.argv[1], sys.argv[2]
im = Image.open(src).convert('RGBA')
bg = Image.new('RGBA', im.size, 'white'); bg.alpha_composite(im)
g = bg.convert('L')
S = 3  # upscale for smoother curves
g = g.resize((g.width*S, g.height*S), Image.LANCZOS)
a = np.array(g)
B = 20*S
a = np.pad(a, B, constant_values=255)
mask = a >= 128           # potracer inverts: trace the white area
bm = potrace.Bitmap(mask)
plist = bm.trace(turdsize=10, alphamax=1.0, opticurve=True, opttolerance=0.2)
d = []
f = lambda p: f"{(p.x-B)/S:.2f},{(p.y-B)/S:.2f}"
for c in plist:
    d.append("M" + f(c.start_point))
    for s in c.segments:
        if s.is_corner: d.append("L"+f(s.c)+" L"+f(s.end_point))
        else: d.append("C"+f(s.c1)+" "+f(s.c2)+" "+f(s.end_point))
    d.append("Z")
W, H = im.size
svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"><path fill="#000" fill-rule="evenodd" d="{" ".join(d)}"/></svg>'
open(out,'w').write(svg); print(len(plist), "paths")
