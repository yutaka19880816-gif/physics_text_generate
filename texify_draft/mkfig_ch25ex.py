# -*- coding: utf-8 -*-
# 第25回の例題21・22の図を，原本スキャンPDFから切り出す
#   /Users/yutaka/Google Drive/マイドライブ/鉄緑会物理/20161215144626.pdf
#     PDFページ1 = 原本 p4|p5（§25.1 と 例題21）
#     PDFページ3 = 原本 p8|p9（§25.3〜25.4 と 例題22）
#   gs で 400dpi にしてから ink_bbox でトリム．網点の図は pnglighten をかける．
import subprocess, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from pngtrim import ink_bbox
SRCPDF = '/Users/yutaka/Google Drive/マイドライブ/鉄緑会物理/20161215144626.pdf'
CACHE  = '/tmp/_ch25ex_p%d.png'
TMP    = '/tmp/_mkfig_ch25ex_tmp.png'
def sips(a): subprocess.run(['sips']+a, capture_output=True)
def page(n):
    f = CACHE % n
    if not os.path.exists(f):
        subprocess.run(['gs','-q','-dNOPAUSE','-dBATCH','-sDEVICE=png16m','-r400',
                        '-dFirstPage=%d'%n,'-dLastPage=%d'%n,'-sOutputFile='+f, SRCPDF],
                       capture_output=True)
    return f
def make(pg, out, top, left, h, w, margin=14, mm=None, halftone=False):
    src = page(pg)
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
            subprocess.run(['python3',os.path.join(HERE,'pnglighten.py'),
                            '--blur','1','--gamma','0.45',out,out],capture_output=True)
            note=f'  →網点処理 {target}px'
    print(f'  {os.path.basename(out):24s} {W}x{H}px  {os.path.getsize(out)/1000:6.1f} KB  (left={L} top={T}){note}')

jobs = [
 (1, 'fig/ch25_ex21_young.png',   2060, 4180, 680, 1140, 14, 78, True ),  # 例題21 ヤングの実験の装置図
 (3, 'fig/ch25_ex22_grating.png', 1700, 4400, 690,  960, 14, 70, True ),  # 例題22 水槽の底の回折格子（2図）
]
for j in jobs: make(*j)
