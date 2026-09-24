# -*- coding: utf-8 -*-
"""第16章の例題（例題8〜10）の図を，原本スキャンPDFから切り出す。
   §16 は原本 p74〜p77（20161215143926.pdf の PDFページ7・8）。
   スキャンの傾きは「例題の枠の上罫」の y を x をずらして測った dy/dx。
   ※ プロジェクトルートを cwd にして実行すること。"""
import subprocess, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pngdeskew import crop_deskew, save

SRC = '/Users/yutaka/Google Drive/マイドライブ/鉄緑会物理/20161215143926.pdf'
DPI = 600
BIG = '/tmp/_ch16ex_page%d.png'

SLOPE = {                      # (PDFページ, ページの左右) -> 傾き dy/dx
    (7, 'R'): +0.010500,       # 原本 p75（例題8）
    (8, 'L'): -0.014100,       # 原本 p76（例題9）
    (8, 'R'): +0.010500,       # 原本 p77（例題10）
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
 (7,'R','fig/ch16_ex8_cyl.png',  2770, 6400, 1570, 1710, 1200),  # 例題8 バネ付きシリンダー（2状態）
 (8,'L','fig/ch16_ex9_cyl.png',  4430, 3090,  700, 1160, 760),  # 例題9 ピストン固定のシリンダー
 (8,'R','fig/ch16_ex10_cyl.png', 1950, 6820,  640, 1290, 760),  # 例題10 ピストン自由のシリンダー
]
for j in jobs: make(*j)
