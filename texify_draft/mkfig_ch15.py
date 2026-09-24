# -*- coding: utf-8 -*-
# 第15回（気体分子運動論）の図の切り出し
#   広めに切る → インクの外接矩形を測る → 余白付きで切り直す
import subprocess, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pngtrim import ink_bbox
TMP = '/tmp/_mkfig_ch15_tmp.png'
def sips(a): subprocess.run(['sips']+a, capture_output=True)
def make(src, out, top, left, h, w, margin=20):
    sips(['-c',str(h),str(w),'--cropOffset',str(top),str(left),src,'--out',TMP])
    b = ink_bbox(TMP)
    if b is None: print('  !! インクなし', out); return
    x0,y0,x1,y1,cw,ch = b
    L=max(0,left+x0-margin); T=max(0,top+y0-margin)
    W=(x1-x0+1)+2*margin;    H=(y1-y0+1)+2*margin
    sips(['-c',str(H),str(W),'--cropOffset',str(T),str(L),src,'--out',out])
    print(f'  {os.path.basename(out):24s} {W}x{H}px  {os.path.getsize(out)/1000:6.1f} KB  (left={L} top={T})')

jobs = [
 ('prob_p37.png', 'fig/ch15_p37_cube.png',   1400, 2600, 900, 920),  # [11] 一辺 l の立方体容器・壁A
 ('prob_p38.png', 'fig/ch15_p38_box.png',    1650, 2700, 830, 950),  # [14] 断熱材の箱とヒーター
 ('prob_p38.png', 'fig/ch15_p38_tv.png',     2650, 2680, 750, 800),  # [15] T-V 図（A→B→C→A）
 ('prob_p39.png', 'fig/ch15_p39_sphere.png',  230, 2620, 800, 900),  # [16] 球形容器内の分子の軌跡
 ('prob_p124.png','fig/ch15_p124_pv.png',    1400, 2330, 750, 850),  # [15]解答 A,B,C の p-V 図上の位置
 ('prob_p125.png','fig/ch15_p125_pv.png',     250,  580, 750, 750),  # [15]解答 完成した p-V 図
]
for j in jobs: make(*j)
