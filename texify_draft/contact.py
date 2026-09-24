# -*- coding: utf-8 -*-
"""切り出した図を縦に並べた確認用シートを作る（目視チェックを1回で済ませるため）。
    python3 texify_draft/contact.py /tmp/sheet.png 900 fig/a.png fig/b.png ...
        → <出力> <1枚あたりの幅px> <入力...>。各図の間に黒い区切り線を入れる。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pngcrop_local import load_gray, save_gray

def down(W, H, g, target):
    if target >= W: return W, H, g
    sx = W / target; nw = target; nh = max(1, int(H / sx))
    o = bytearray(nw * nh)
    for y in range(nh):
        y0 = int(y*sx); y1 = max(y0+1, int((y+1)*sx))
        for x in range(nw):
            x0 = int(x*sx); x1 = max(x0+1, int((x+1)*sx))
            s = 0; n = 0
            for yy in range(y0, min(y1, H)):
                b = yy*W
                for xx in range(x0, min(x1, W)): s += g[b+xx]; n += 1
            o[y*nw+x] = s//n
    return nw, nh, o

out = sys.argv[1]; wid = int(sys.argv[2]); srcs = sys.argv[3:]
imgs = []
for s in srcs:
    W,H,g = load_gray(s)
    imgs.append(down(W,H,g,wid))
TH = sum(h for _,h,_ in imgs) + 6*len(imgs)
sheet = bytearray(b'\xff'*(wid*TH))
y0 = 0
for w,h,g in imgs:
    for y in range(h):
        sheet[(y0+y)*wid:(y0+y)*wid+w] = g[y*w:(y+1)*w]
    y0 += h
    for y in range(y0, y0+3): sheet[y*wid:(y+1)*wid] = b'\x00'*wid
    y0 += 6
save_gray(out, wid, TH, sheet)
print(out, wid, TH, '/', len(imgs), 'figs')
