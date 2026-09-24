# -*- coding: utf-8 -*-
# 第17回（気体の状態変化(2)）の図の切り出し
#   広めに切る → インクの外接矩形を測る → 余白付きで切り直す
import subprocess, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pngtrim import ink_bbox
TMP = '/tmp/_mkfig_ch17_tmp.png'
def sips(a): subprocess.run(['sips']+a, capture_output=True)
def make(src, out, top, left, h, w, margin=16):
    sips(['-c',str(h),str(w),'--cropOffset',str(top),str(left),src,'--out',TMP])
    b = ink_bbox(TMP)
    if b is None: print('  !! インクなし', out); return
    x0,y0,x1,y1,cw,ch = b
    L=max(0,left+x0-margin); T=max(0,top+y0-margin)
    W=(x1-x0+1)+2*margin;    H=(y1-y0+1)+2*margin
    sips(['-c',str(H),str(W),'--cropOffset',str(T),str(L),src,'--out',out])
    print(f'  {os.path.basename(out):24s} {W}x{H}px  {os.path.getsize(out)/1000:6.1f} KB  (left={L} top={T})')

jobs = [
 # ---- 練習問題ページ ----
 ('prob_p43.png',  'fig/ch17_p43_cyl.png',   2600, 2600,  340, 1160, 12),  # [26] 水平シリンダー（棒つき）
 ('prob_p44.png',  'fig/ch17_p44_cyl.png',    160, 2620,  300, 1045, 12),  # [27] 水平シリンダー（断熱・棒つき）
 ('prob_p44.png',  'fig/ch17_p44_ab.png',    1740, 2620,  720, 1045, 12),  # [28] 断熱容器A・B（コックK）
 ('prob_p44.png',  'fig/ch17_p44_valve.png', 2700, 2650,  340, 1015, 12),  # [29] 隔壁バルブつきシリンダー
 ('prob_p45.png',  'fig/ch17_p45_spring.png', 250, 2380,  880, 1300, 12),  # [30] バネつきシリンダー（2段）
 # ---- 解答ページ ----
 ('prob_p132.png', 'fig/ch17_a25_pv.png',    2480, 2400,  640, 1060, 16),  # [25](3)【注】等温曲線
 ('prob_p133.png', 'fig/ch17_a27_pv.png',    4790, 2080,  640, 1390, 16),  # [27](3) 断熱曲線の p-V 図
 ('prob_p135.png', 'fig/ch17_a29_1.png',       60,  340,  380, 1150, 16),  # [29](1) 初状態（右は真空）
 ('prob_p135.png', 'fig/ch17_a29_2.png',     1860,  300,  390,  900, 16),  # [29](1) 拡散後
 ('prob_p135.png', 'fig/ch17_a29_3.png',     3060,  350,  380,  880, 16),  # [29](2) 途中（右側の体積 V）
 ('prob_p135.png', 'fig/ch17_a29_4.png',     3820,  350,  760,  880, 16),  # [29](2) V0 → 2V0（矢印つき）
 ('prob_p135.png', 'fig/ch17_a29_ref.png',   2380, 2280,  380,  850, 16),  # [29]【参考】拡散途中の濃淡
]
for j in jobs: make(*j)
