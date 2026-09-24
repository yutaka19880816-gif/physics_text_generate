# -*- coding: utf-8 -*-
import subprocess, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pngtrim import ink_bbox
TMP = '/tmp/_mkfig_ch14_tmp.png'
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
 ('prob_p35.png', 'fig/ch14_p35_cyl.png',   2780, 2566,  600, 1110),  # [3] 断熱ピストンCで仕切られた容器
 ('prob_p36.png', 'fig/ch14_p36_flask.png', 1830, 2600,  680, 1076),  # [8] 細管でつながれた二つの容器
 ('prob_p119.png','fig/ch14_p119_dU1.png',  1900,  450,  580,  980),  # [7](1) 熱Q・仕事W の収支
 ('prob_p119.png','fig/ch14_p119_dU2.png',  3000,  450,  580,  980),  # [7](2) 仕事W'・熱Q' の収支
]
for j in jobs: make(*j)
