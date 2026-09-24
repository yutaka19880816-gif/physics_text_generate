# -*- coding: utf-8 -*-
import subprocess, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from pngtrim import ink_bbox
TMP = '/tmp/_mkfig_ch2_tmp.png'
def sips(a): subprocess.run(['sips']+a, capture_output=True)
def make(src, out, top, left, h, w, margin=20):
    sips(['-c',str(h),str(w),'--cropOffset',str(top),str(left),src,'--out',TMP])
    b = ink_bbox(TMP)
    if b is None: print('  !! インクなし', out); return
    x0,y0,x1,y1,cw,ch = b
    L=max(0,left+x0-margin); T=max(0,top+y0-margin)
    W=(x1-x0+1)+2*margin;    H=(y1-y0+1)+2*margin
    sips(['-c',str(H),str(W),'--cropOffset',str(T),str(L),src,'--out',out])
    print(f'  {os.path.basename(out):22s} {W}x{H}px  {os.path.getsize(out)/1000:6.1f} KB  (left={L} top={T})')

jobs = [
 ('prob_p5.png','fig/ch2_p5_up.png',    2910, 2462,  770, 1206),  # [11] 鉛直投げ上げ
 ('prob_p5.png','fig/ch2_p5_hor.png',   3845, 2462,  730, 1206),  # [12] 水平投射
 ('prob_p6.png','fig/ch2_p6_obl.png',    165, 2520,  630, 1167),  # [13] 斜方投射
 ('prob_p6.png','fig/ch2_p6_bldg.png',  1335, 2520,  760, 1167),  # [14] ビルから斜方投射
 ('prob_p7.png','fig/ch2_p7_cart.png',   165, 2520,  415, 1158),  # [17] 台車
 ('prob_p7.png','fig/ch2_p7_monkey.png',1590, 2520,  905, 1158),  # [18] モンキーハンティング
]
for j in jobs: make(*j)
