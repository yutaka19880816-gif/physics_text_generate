# -*- coding: utf-8 -*-
"""第14章の例題の図を、原本スキャンPDF（Googleドライブのローカルマウント）から切り出す。
   mkfig_ch14.py と同じ2段階方式（広く切る→ink_bboxで外接矩形→切り直す）だが、
   入力がPDFなので先に gs で 600dpi の PNG にする。
   ※ プロジェクトルートを cwd にして実行すること。"""
import subprocess, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pngtrim import ink_bbox

SRC  = '/Users/yutaka/Google Drive/マイドライブ/鉄緑会物理/20161215143926.pdf'
PAGE = 2          # 見開き（原本 p64 | p65）
DPI  = 600
BIG  = '/tmp/_ch14ex_page.png'
TMP  = '/tmp/_ch14ex_tmp.png'

def sips(a): subprocess.run(['sips']+a, capture_output=True)

def render():
    subprocess.run(['gs','-q','-dNOPAUSE','-dBATCH',
                    '-dFirstPage=%d'%PAGE,'-dLastPage=%d'%PAGE,
                    '-sDEVICE=png16m','-r%d'%DPI,'-sOutputFile='+BIG, SRC],
                   capture_output=True)
    w = subprocess.run(['sips','-g','pixelWidth','-g','pixelHeight',BIG],
                       capture_output=True, text=True).stdout
    print('  見開きを %ddpi で描画: %s' % (DPI, ' '.join(w.split()[-3:])))

def make(out, top, left, h, w, maxw=None, margin=24):
    sips(['-c',str(h),str(w),'--cropOffset',str(top),str(left),BIG,'--out',TMP])
    b = ink_bbox(TMP)
    if b is None: print('  !! インクなし', out); return
    x0,y0,x1,y1,cw,ch = b
    L=max(0,left+x0-margin); T=max(0,top+y0-margin)
    W=(x1-x0+1)+2*margin;    H=(y1-y0+1)+2*margin
    sips(['-c',str(H),str(W),'--cropOffset',str(T),str(L),BIG,'--out',out])
    if maxw and W > maxw:            # 網点の図は面積平均で縮小するとなめらかな階調になる
        sips(['--resampleWidth',str(maxw),out]); W = maxw
    print(f'  {os.path.basename(out):24s} {W}x{H}px  {os.path.getsize(out)/1000:6.1f} KB  (left={L} top={T})')

# w は例題の枠線（右端の太い縦罫）を拾わないところで止める
jobs = [
 # 出力,                          top,  left,   h,     w,  maxw
 ('fig/ch14_ex1_cyl.png',        1370,  3715,  820,   555, None),  # 例題1 シリンダー＋ピストン
 ('fig/ch14_ex1_water.png',      2280,  3115,  915,  1170,  600),  # 例題1 水中の直方体
 ('fig/ch14_ex2_cock.png',       2900,  7030,  790,  1110,  900),  # 例題2 容器A・B＋コック
]

render()
for j in jobs: make(*j)
