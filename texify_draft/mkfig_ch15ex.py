# -*- coding: utf-8 -*-
"""第15章の例題（例題5〜7）の図を，原本スキャンPDFから切り出す。
   2026-09-02 改訂：原本スキャンは1度弱傾いているので，切り出す前に
   pngdeskew で傾きを打ち消す（図が斜めに見える／枠に対して曲がって見える対策）。

   傾き slope は「本来水平な長い線」（例題の枠の上罫）の y を x をずらして2点測り，
   dy/dx で求めた値。見開きの左ページと右ページで違うので分けてある。
   ※ プロジェクトルートを cwd にして実行すること。"""
import subprocess, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pngdeskew import crop_deskew, save

SRC = '/Users/yutaka/Google Drive/マイドライブ/鉄緑会物理/20161215143926.pdf'
DPI = 600
BIG = '/tmp/_ch15ex_page%d.png'

SLOPE = {                      # (PDFページ, ページの左右) -> 傾き dy/dx
    (5, 'L'): -0.018125,       # 原本 p70（例題5）
    (6, 'L'): -0.015556,       # 原本 p72（例題6）
    (6, 'R'): +0.007857,       # 原本 p73（例題7）
}

def sips(a): subprocess.run(['sips']+a, capture_output=True)

def render(page):
    out = BIG % page
    if os.path.exists(out): return out
    subprocess.run(['gs','-q','-dNOPAUSE','-dBATCH',
                    '-dFirstPage=%d'%page,'-dLastPage=%d'%page,
                    '-sDEVICE=png16m','-r%d'%DPI,'-sOutputFile='+out, SRC],
                   capture_output=True)
    print('  PDF p%d を %ddpi で描画' % (page, DPI))
    return out

def ink_bbox_rows(rows, w, h, thresh=170, minrun=2):
    """連続 minrun 画素以上の暗い並びだけをインクとみなす（点ノイズ除け）"""
    x0,y0,x1,y1 = w,h,-1,-1
    for y in range(h):
        r = rows[y]; run = 0
        for x in range(w):
            if r[x] < thresh:
                run += 1
                if run >= minrun:
                    if x-run+1 < x0: x0 = x-run+1
                    if x > x1: x1 = x
                    if y < y0: y0 = y
                    if y > y1: y1 = y
            else: run = 0
    return None if x1 < 0 else (x0,y0,x1,y1)

def make(page, side, out, top, left, h, w, maxw=None, margin=16):
    src = render(page)
    W,H,rows = crop_deskew(src, top, left, h, w, SLOPE[(page,side)])
    b = ink_bbox_rows(rows, W, H)
    if b is None: print('  !! インクなし', out); return
    x0,y0,x1,y1 = b
    x0 = max(0,x0-margin); y0 = max(0,y0-margin)
    x1 = min(W-1,x1+margin); y1 = min(H-1,y1+margin)
    nw, nh = x1-x0+1, y1-y0+1
    save(out, nw, nh, [r[x0:x1+1] for r in rows[y0:y1+1]])
    if maxw and nw > maxw:      # 網点は面積平均で縮小するとなめらかな階調になる
        sips(['--resampleWidth',str(maxw),out]); nw = maxw
    print(f'  {os.path.basename(out):26s} {nw}x{nh}px  {os.path.getsize(out)/1000:6.1f} KB')

# 窓は「隣の文字を拾わない」ところで止める（ink_bbox は窓の中しか見ないため）
jobs = [
 (5,'L','fig/ch15_ex5_cube.png',   540, 2820,  860, 1320,  650),  # 立方体容器と気体分子
 (5,'L','fig/ch15_ex5_hane.png',  1408, 2950,  975, 1350,  700),  # 注目する面での反射
 (5,'L','fig/ch15_ex5_Ft.png',    3225, 2800,  945, 1530,  800),  # 力-時間グラフ
 (6,'L','fig/ch15_ex6_cock.png',  3690, 3080,  815, 1120,  760),  # 断熱容器A・BとコックK
 (6,'R','fig/ch15_ex7_pt.png',    1995, 7060,  845,  970, None),  # P-T 図
]
for j in jobs: make(*j)
