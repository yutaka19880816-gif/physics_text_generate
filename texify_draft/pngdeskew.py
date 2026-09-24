# -*- coding: utf-8 -*-
"""原本スキャンの傾き（1度弱）を直してから図を切り出すための小道具。
   PIL / numpy 無しの純Python。バイリニアで回すのでモアレは増えない。

   傾きの測り方：例題の枠の上罫のように「本来水平な長い線」の y 座標を
   x をずらして2点測り，slope = dy/dx を出す（画面座標なので y は下向き）。
   その slope をそのまま crop_deskew の引数に渡す。
"""
import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pnglighten import decode, write_gray

def crop_deskew(src, top, left, h, w, slope):
    """src の (left,top) から w×h を切り出し，slope を打ち消すように回して
       8bit グレースケールの (w,h,rows) を返す。外側は白で埋める。"""
    W, H, bpp, rows = decode(src)
    phi = math.atan(slope)
    cs, sn = math.cos(phi), math.sin(phi)
    cx, cy = left + w / 2.0, top + h / 2.0
    out = []
    for yo in range(h):
        dy = (top + yo + 0.5) - cy
        line = bytearray(w)
        for xo in range(w):
            dx = (left + xo + 0.5) - cx
            xs = cx + dx * cs - dy * sn
            ys = cy + dx * sn + dy * cs
            x0, y0 = int(math.floor(xs)), int(math.floor(ys))
            fx, fy = xs - x0, ys - y0
            v = 0.0; tot = 0.0
            for (xx, yy, wt) in ((x0,y0,(1-fx)*(1-fy)), (x0+1,y0,fx*(1-fy)),
                                 (x0,y0+1,(1-fx)*fy), (x0+1,y0+1,fx*fy)):
                if 0 <= xx < W and 0 <= yy < H:
                    v += rows[yy][xx*bpp] * wt; tot += wt
            line[xo] = 255 if tot == 0 else min(255, max(0, int(v / tot + 0.5)))
        out.append(line)
    return w, h, out

def save(path, w, h, rows):
    write_gray(path, w, h, rows)
