# -*- coding: utf-8 -*-
# 第16回（気体の状態変化(1)）の図の切り出し
#   広めに切る → インクの外接矩形を測る → 余白付きで切り直す
import subprocess, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pngtrim import ink_bbox
TMP = '/tmp/_mkfig_ch16_tmp.png'
def sips(a): subprocess.run(['sips']+a, capture_output=True)
def make(src, out, top, left, h, w, margin=16):
    sips(['-c',str(h),str(w),'--cropOffset',str(top),str(left),src,'--out',TMP])
    b = ink_bbox(TMP)
    if b is None: print('  !! インクなし', out); return
    x0,y0,x1,y1,cw,ch = b
    L=max(0,left+x0-margin); T=max(0,top+y0-margin)
    W=(x1-x0+1)+2*margin;    H=(y1-y0+1)+2*margin
    sips(['-c',str(H),str(W),'--cropOffset',str(T),str(L),src,'--out',out])
    print(f'  {os.path.basename(out):22s} {W}x{H}px  {os.path.getsize(out)/1000:6.1f} KB  (left={L} top={T})')

jobs = [
 # ---- 練習問題ページ ----
 ('prob_p40.png',  'fig/ch16_p40_pv6.png',  1684,   70, 1360, 3560, 14),  # [18] p-V図6枚（(1)〜(6)）
 ('prob_p40.png',  'fig/ch16_p40_cyl.png',  3080, 2670,  470, 1001, 12),  # [19] 水平シリンダー（ピストン自由）
 ('prob_p41.png',  'fig/ch16_p41_cyl.png',   130, 2590,  460, 1010, 12),  # [20] 水平シリンダー（ピストン固定）
 ('prob_p41.png',  'fig/ch16_p41_vcyl.png', 2670, 2680,  900,  760, 12),  # [22] 鉛直シリンダー
 ('prob_p42.png',  'fig/ch16_p42_vcyl.png',  280, 2600, 1060,  760, 12),  # [23] 鉛直シリンダー＋ストッパー
 # ---- 解答ページ ----
 ('prob_p126_2.png','fig/ch16_a18_1.png',   4570, 2300,  620,  880, 16),  # [18](1) 長方形
 ('prob_p127.png', 'fig/ch16_a18_2.png',      30,  530,  620,  850, 16),  # [18](2) 台形
 ('prob_p127.png', 'fig/ch16_a18_4.png',    1220,  530,  640,  850, 16),  # [18](4) 双曲線（膨張）
 ('prob_p127.png', 'fig/ch16_a18_5.png',    2520,  530,  600,  850, 16),  # [18](5) 長方形（圧縮）
 ('prob_p127.png', 'fig/ch16_a18_6.png',    3580,  530,  600,  850, 16),  # [18](6) 双曲線（圧縮）
 ('prob_p128.png', 'fig/ch16_a19_pv.png',   1980,  280,  590, 1030, 16),  # [19](3) 定圧変化の p-V 図
 ('prob_p128.png', 'fig/ch16_a20_pv.png',   4660, 2200,  600, 1000, 16),  # [20](2) 定積変化の p-V 図
 ('prob_p129.png', 'fig/ch16_a21_pv.png',   4290,  240,  620, 1050, 16),  # [21](1) 等温変化の p-V 図
 ('prob_p129.png', 'fig/ch16_a22_f1.png',   1550, 2400,  750,  880, 16),  # [22](1) ピストンの力の作用図
 ('prob_p129.png', 'fig/ch16_a22_f2.png',   3860, 2300,  760,  980, 16),  # [22](2) 変化中の力の作用図
 ('prob_p130.png', 'fig/ch16_a22_pv.png',   1020,  260,  590, 1280, 16),  # [22](3) 定圧変化の p-V 図
 ('prob_p130.png', 'fig/ch16_a23_f1.png',   3540, 2230,  700, 1150, 16),  # [23](2) ストッパーからの力を含む作用図
]
for j in jobs: make(*j)
