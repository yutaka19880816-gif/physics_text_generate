# -*- coding: utf-8 -*-
"""第17章の例題（例題11〜14）の図を，原本スキャンPDFから切り出す。
   §17 は原本 p78〜p81（20161215143926.pdf の PDFページ9・10）。
   スキャンの傾きは「例題の枠の上罫」の y を x をずらして測った dy/dx。
   ※ プロジェクトルートを cwd にして実行すること。"""
import subprocess, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pngdeskew import crop_deskew, save

SRC = '/Users/yutaka/Google Drive/マイドライブ/鉄緑会物理/20161215143926.pdf'
DPI = 600
BIG = '/tmp/_ch17ex_page%d.png'

SLOPE = {                      # (PDFページ, ページの左右) -> 傾き dy/dx
    ( 9, 'L'): -0.009500,      # 原本 p78（例題11）
    (10, 'L'): +0.001700,      # 原本 p80（例題13）
    (10, 'R'): +0.021000,      # 原本 p81（例題14）
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
 ( 9,'L','fig/ch17_ex11_cyl.png', 1160, 2780,  650, 1340, 900),  # 例題11 温度一定のシリンダー
 (10,'L','fig/ch17_ex13_cyl.png', 1580, 2800, 1360, 1530, 860),  # 例題13 断熱変化の前後（2状態）
 (10,'R','fig/ch17_ex14_box1.png',2600, 7220,  650, 1010, 800),  # 例題14(1) 左に気体・右は真空
 (10,'R','fig/ch17_ex14_box2.png',3400, 7220,  690, 1020, 800),  # 例題14(2) 左右に異なる気体
]
for j in jobs: make(*j)
