# -*- coding: utf-8 -*-
# 新第14回（正弦波の表式と縦波）で必要な図の切り出し
#   問題図：問題編 prob_p48/49（旧第19回）, prob_p50/51（旧第20回）
#   解答図：問題編 prob_p143〜148（旧第19回）, prob_p149/152（旧第20回）
# 座標は確定値（切り出し後に組版して目視確認済み・2026-09-04）
import subprocess, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pngtrim import ink_bbox
TMP = '/private/tmp/claude-501/-Users-yutaka-Documents-Claude-Code----math-tex-tool/1df6deb5-316e-4f0f-a56b-76b9376dca13/scratchpad/tmpcrop14.png'
def sips(a): subprocess.run(['sips']+a, capture_output=True)
def make(src, out, top, left, h, w, margin=14):
    sips(['-c',str(h),str(w),'--cropOffset',str(top),str(left),src,'--out',TMP])
    b = ink_bbox(TMP)
    if b is None: print('  !! インクなし', out); return
    x0,y0,x1,y1,cw,ch = b
    L=max(0,left+x0-margin); T=max(0,top+y0-margin)
    W=(x1-x0+1)+2*margin;    H=(y1-y0+1)+2*margin
    sips(['-c',str(H),str(W),'--cropOffset',str(T),str(L),src,'--out',out])
    print(f'  {os.path.basename(out):26s} {W}x{H}px  {os.path.getsize(out)/1000:6.1f} KB  (left={L} top={T})')

jobs = [
 # ---------- 問題図 ----------
 ('prob_p48.png', 'fig/n14_p2_wave.png',   1330, 2680,  560,  920),  # ［2］横波と媒質の振動
 ('prob_p48.png', 'fig/n14_p3_wave.png',   2250, 2680,  560,  920),  # ［3］正弦波のグラフ
 ('prob_p48.png', 'fig/n14_p4_yx.png',     3290, 2700,  520,  950),  # ［4］y-xグラフ
 ('prob_p49.png', 'fig/n14_p5_yt.png',       80, 2600,  520, 1040),  # ［5］y-tグラフ
 ('prob_p49.png', 'fig/n14_p6_conv.png',   1270, 2560,  590, 1080),  # ［6］相互変換
 ('prob_p50.png', 'fig/n14_p7_long.png',   2320, 2600,  420, 1090),  # ［7］（旧[10]）縦波の横波表示
 ('prob_p49.png', 'fig/n14_p9_phase.png',  3650, 2600,  520, 1040),  # ［9］（旧[8]）波の位相
 ('prob_p51.png', 'fig/n14_p10_fig1.png',  3300, 2500,  610, 1140),  # ［10］（旧[14]）図1
 ('prob_p51.png', 'fig/n14_p10_fig2.png',  3930, 2500,  640, 1140),  # ［10］（旧[14]）図2
 # ---------- 解答図 ----------
 ('prob_p143.png','fig/n14_a2_wave.png',    140,  380,  500, 1100),  # ［2］次の瞬間の波形
 ('prob_p143.png','fig/n14_a3_right.png',  4150,  620,  560, 1060),  # ［3］(1)右へ進む場合
 ('prob_p143.png','fig/n14_a3_left.png',   4700,  620,  490, 1060),  # ［3］(1)左へ進む場合
 ('prob_p143.png','fig/n14_a3_15T.png',    2260, 2230,  500, 1100),  # ［3］(3)1.5周期後
 ('prob_p143.png','fig/n14_a3_bekkai.png', 4330, 2160,  480, 1250),  # ［3］別解
 ('prob_p144.png','fig/n14_a4_daihyo.png', 2140,  350,  600, 1150),  # ［4］(2)代表点
 ('prob_p144.png','fig/n14_a4_shift.png',    30, 2080, 1150, 1500),  # ［4］(4)時刻0／時刻t
 ('prob_p144.png','fig/n14_a5_daihyo.png', 3390, 2250,  540, 1100),  # ［5］(1)代表点
 ('prob_p145.png','fig/n14_a5_shift.png',    30,  100, 1030, 1350),  # ［5］(3)時刻t／時刻t+x/v
 ('prob_p145.png','fig/n14_a6_1a.png',       60, 2220,  480, 1080),  # ［6］(1)次の瞬間の波形
 ('prob_p145.png','fig/n14_a6_1b.png',     1190, 2280,  460, 1020),  # ［6］(1)y-tグラフ
 ('prob_p145.png','fig/n14_a6_2a.png',     2230, 2220,  440, 1080),  # ［6］(2)次の瞬間の波形
 ('prob_p145.png','fig/n14_a6_2b.png',     3330, 2280,  460, 1020),  # ［6］(2)y-tグラフ
 ('prob_p145.png','fig/n14_a6_3a.png',     4380, 2320,  530, 1000),  # ［6］(3)y-x代表値
 ('prob_p146.png','fig/n14_a6_3b.png',      560,  100, 1060, 1400),  # ［6］(3)時刻0／時刻t
 ('prob_p146.png','fig/n14_a8_yx.png',     5060, 2260,  470,  850),  # ［8］(2)y-xグラフ
 ('prob_p147.png','fig/n14_a8_yt.png',     3270,  360,  470,  900),  # ［8］(2)y-tグラフ
 ('prob_p149.png','fig/n14_a7_disp.png',   4050,  100,  460, 1400),  # ［7］(1)変位
 ('prob_p149.png','fig/n14_a7_yoko.png',    750, 2050,  500, 1560),  # ［7］(3)横波表示
 ('prob_p149.png','fig/n14_a7_jissai.png', 2000, 2050,  500, 1560),  # ［7］(3)実際の変位
 ('prob_p152.png','fig/n14_a10_p.png',     3245,  200,  500, 1500),  # ［10］(1)+x向き
 ('prob_p152.png','fig/n14_a10_m.png',     4260,  200,  560, 1500),  # ［10］(1)-x向き
 ('prob_p152.png','fig/n14_a10_dense.png', 1130, 2100,  500, 1470),  # ［10］(2)波形
 ('prob_p152.png','fig/n14_a10_chu.png',   2830, 2160,  480, 1400),  # ［10］(2)注
 ('prob_p152.png','fig/n14_a10_34T.png',   3790, 2100,  500, 1470),  # ［10］(3)波形
]
for j in jobs: make(*j)
