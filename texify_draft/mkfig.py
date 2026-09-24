# -*- coding: utf-8 -*-
import subprocess, sys, os
sys.path.insert(0,'/tmp')
from pngtrim import ink_bbox
TMP='/private/tmp/claude-501/-Users-yutaka-Documents-Claude-Code----math-tex-tool/710841d1-c0ec-48e6-bdcc-a046c6fd35e9/scratchpad/tmpcrop.png'
def sips(args):
    subprocess.run(['sips']+args, capture_output=True)
def make(src, out, top, left, h, w, margin=20):
    # 1) 広めに切る
    sips(['-c',str(h),str(w),'--cropOffset',str(top),str(left),src,'--out',TMP])
    # 2) インクの外接矩形を測る
    b = ink_bbox(TMP)
    if b is None: print('  !! インクなし',out); return
    x0,y0,x1,y1,cw,ch = b
    # 3) 原寸座標に直して余白付きで切り直す
    L = max(0, left + x0 - margin); T = max(0, top + y0 - margin)
    W = (x1-x0+1) + 2*margin; H = (y1-y0+1) + 2*margin
    sips(['-c',str(H),str(W),'--cropOffset',str(T),str(L),src,'--out',out])
    print(f'  {os.path.basename(out):24s} {W}x{H}px  {os.path.getsize(out)/1000:6.1f} KB   (原寸 left={L} top={T})')

jobs=[
 ('prob_p3.png','fig/ch1_p3_vt.png',     100,2560, 700,1089),
 ('prob_p3.png','fig/ch1_p3_boat.png',  2150,2565, 900,1084),
 ('prob_p3.png','fig/ch1_p3_river.png', 3050,2590, 800,1059),
 ('prob_p4.png','fig/ch1_p4_vt.png',     150,2140, 980,1414),
 ('prob_p64.png','fig/ch1_p64_at.png',  2480,2250, 640,1000),
 ('prob_p65.png','fig/ch1_p65_river.png',1730,2260, 620,1200),
]
for j in jobs: make(*j)
