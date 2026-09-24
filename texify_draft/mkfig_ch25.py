# -*- coding: utf-8 -*-
# 第25回（光波の干渉(1)）の図の切り出し
#   広めに切る → インクの外接矩形を測る → 余白付きで切り直す
#   網点（グレーの塗り）を含む図は，貼付幅に対して 360dpi 相当まで縮小してから
#   pnglighten でモアレを潰す（落とし穴13・21b）
import subprocess, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pngtrim import ink_bbox
TMP = '/tmp/_mkfig_ch25_tmp.png'
def sips(a): subprocess.run(['sips']+a, capture_output=True)
def make(src, out, top, left, h, w, margin=14, mm=None, halftone=False):
    sips(['-c',str(h),str(w),'--cropOffset',str(top),str(left),src,'--out',TMP])
    b = ink_bbox(TMP)
    if b is None: print('  !! インクなし', out); return
    x0,y0,x1,y1,cw,ch = b
    L=max(0,left+x0-margin); T=max(0,top+y0-margin)
    W=(x1-x0+1)+2*margin;    H=(y1-y0+1)+2*margin
    sips(['-c',str(H),str(W),'--cropOffset',str(T),str(L),src,'--out',out])
    note=''
    if halftone and mm:
        target = int(round(mm/25.4*360))
        if target < W:
            sips(['--resampleWidth',str(target),out])
            subprocess.run(['python3',os.path.join(os.path.dirname(os.path.abspath(__file__)),'pnglighten.py'),
                            '--blur','1','--gamma','0.45',out,out],capture_output=True)
            note=f'  →網点処理 {target}px'
    print(f'  {os.path.basename(out):24s} {W}x{H}px  {os.path.getsize(out)/1000:6.1f} KB  (left={L} top={T}){note}')

jobs = [
 # ---- 練習問題ページ ----
 ('prob2_p2.png', 'fig/ch25_p2_young1.png',   990, 2110, 1120, 1400, 14, 62, True ),  # [46] ヤングの実験 装置図
 ('prob2_p2.png', 'fig/ch25_p2_young2.png',  2040, 2140,  990, 1560, 14, 66, False),  # [46] 経路差の拡大図
 ('prob2_p3.png', 'fig/ch25_p3_glass.png',    150, 2110,  900, 1570, 14, 66, True ),  # [47] ガラスGを置いたヤングの実験
 ('prob2_p3.png', 'fig/ch25_p3_grating.png', 2250, 2300, 1000, 1400, 14, 58, False),  # [48] 回折格子
 ('prob2_p4.png', 'fig/ch25_p4_lloyd.png',    260, 2090,  880, 1560, 14, 66, True ),  # [49] ロイドの鏡
 ('prob2_p4.png', 'fig/ch25_p4_foucault.png',1980, 2330, 1010, 1330, 14, 58, True ),  # [50] フーコーの実験
 ('prob2_p5.png', 'fig/ch25_p5_young.png',    140, 2250, 1000, 1400, 14, 60, False),  # [51] 装置図
 ('prob2_p5.png', 'fig/ch25_p5_int.png',     1220, 2240,  790, 1420, 14, 60, False),  # [51] 干渉縞の強度分布
 # ---- 解答ページ ----
 ('prob2_p72.png','fig/ch25_a47_1.png',       780,  180,  850, 1400, 14, 68, False),  # [47](1) 経路差の図
 ('prob2_p72.png','fig/ch25_a47_2.png',      2080,  470,  700, 1160, 14, 46, True ),  # [47](2) ガラスG内の光路長
 ('prob2_p72.png','fig/ch25_a49_1.png',      4500, 2180,  708, 1330, 14, 68, True ),  # [49](1) 二つの経路
 ('prob2_p73.png','fig/ch25_a49_2.png',       430,  200,  810, 1400, 14, 68, True ),  # [49](2) 鏡に対する折り返し
 ('prob2_p73.png','fig/ch25_a50_1.png',      2900, 2400,  680,  800, 14, 44, False),  # [50](1) 回転鏡の反射角
 ('prob2_p74.png','fig/ch25_a51_1.png',      1510,  200,  860, 1400, 14, 68, False),  # [51](1) 経路差の図
 ('prob2_p74.png','fig/ch25_a51_2.png',      4520,  200,  830, 1400, 14, 68, False),  # [51](2) 単スリットを動かした図
]
for j in jobs: make(*j)
