# -*- coding: utf-8 -*-
# 新第14回の例題1〜5の図を，原本（講義編 第1冊）から切り出す。
#   原本: Google ドライブ同期フォルダ 鉄緑会物理/20161215143926.pdf（29ページ＝見開き）
#   PDFページ n ＝ 原本 p(60+2n)/p(61+2n)  →  p86/87=13, p88/89=14, p92/93=16
import subprocess, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pngtrim import ink_bbox
from pngdeskew import crop_deskew, save as save_gray
from pngslope import slope_of_band

SRC = '/Users/yutaka/Library/CloudStorage/GoogleDrive-y-kobayashi@seiryo-js.com/マイドライブ/鉄緑会物理/20161215143926.pdf'
TMPD = '/private/tmp/claude-501/-Users-yutaka-Documents-Claude-Code----math-tex-tool/1df6deb5-316e-4f0f-a56b-76b9376dca13/scratchpad'
TMP  = TMPD + '/tmpcrop14ex.png'
DPI  = 500

def render(pg):
    out = f'{TMPD}/gen_p{pg}.png'
    if not os.path.exists(out):
        subprocess.run(['gs','-sDEVICE=png16m','-r%d'%DPI,'-dFirstPage=%d'%pg,'-dLastPage=%d'%pg,
                        '-o',out,SRC], capture_output=True)
    return out

def sips(a): subprocess.run(['sips']+a, capture_output=True)
TMP2 = TMPD + '/tmpcrop14ex_2.png'
TMPR = TMPD + '/tmpcrop14ex_r.png'

def make(pg, out, top, left, h, w, margin=14, slope=0.0, pad=48):
    """slope を与えると，余裕をもって切り出してから傾きを打ち消してトリムする。
       slope は pngslope.slope_of_band（本来水平な長い線＝グラフの x 軸）で実測した値。"""
    src = render(pg)
    if slope:
        sips(['-c',str(h+2*pad),str(w+2*pad),'--cropOffset',str(top-pad),str(left-pad),src,'--out',TMP2])
        rw, rh, rows = crop_deskew(TMP2, 0, 0, h+2*pad, w+2*pad, slope)
        save_gray(TMPR, rw, rh, rows)
        base, bx, by = TMPR, pad, pad
    else:
        base, bx, by = src, left, top
    sips(['-c',str(h),str(w),'--cropOffset',str(by),str(bx),base,'--out',TMP])
    b = ink_bbox(TMP)
    if b is None: print('  !! インクなし', out); return
    x0,y0,x1,y1,cw,ch = b
    L=max(0,bx+x0-margin); T=max(0,by+y0-margin)
    W=(x1-x0+1)+2*margin;  H=(y1-y0+1)+2*margin
    sips(['-c',str(H),str(W),'--cropOffset',str(T),str(L),base,'--out',out])
    print(f'  {os.path.basename(out):24s} {W}x{H}px  {os.path.getsize(out)/1000:6.1f} KB  slope={slope:+.5f}')

jobs = [
 (13, 'fig/n14_ex1_wave.png',  1345, 1690,  590, 1590, 14, 0.00806),  # 例題1 実線・破線の波形（原本 p86）
 (14, 'fig/n14_ex3_g1.png',    1700, 2010,  590, 1260),   # 傾き0.04度＝実質なし  # 例題3 グラフ\MARU{1}（原本 p88）
 (14, 'fig/n14_ex3_g2.png',    2340, 2010,  520, 1260),  # 例題3 グラフ\MARU{2}
 (14, 'fig/n14_ex4_yt.png',    2745, 5400,  535, 1290, 14, 0.01994),  # 例題4 原点の y-t グラフ（原本 p89）
 (16, 'fig/n14_ex5_long.png',   885, 2010,  505, 1290, 14, 0.01056),  # 例題5 縦波の横波表示（原本 p92）
]
for j in jobs: make(*j)
