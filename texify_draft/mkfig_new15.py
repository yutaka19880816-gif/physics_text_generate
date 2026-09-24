# -*- coding: utf-8 -*-
# 新第15回（波の重ね合わせ・干渉・定常波と反射）で必要な図の切り出し。
#   問題図：問題編 prob_p50/51/52（旧第20回）, prob_p53/54（旧第21回）
#   解答図：問題編 prob_p150/151/153（旧第20回）, prob_p154〜158（旧第21回）
#   例題図：講義編 第1冊 20161215143926.pdf（原本 p94/95/98/99）
# sips の --cropOffset は左上原点ではない（中心基準）ので使わない。
# ここでは PNG を純Pythonでデコードして自前で切り出す（pngcrop_local.py）。
import sys, os, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from pngtrim import ink_bbox

def load(path):
    from pngcrop_local import load_gray
    return load_gray(path)

_cache = {}
def page(src):
    if src not in _cache:
        _cache[src] = load(src)
        print('  (loaded %s %dx%d)' % (os.path.basename(src), _cache[src][0], _cache[src][1]))
    return _cache[src]

def make(src, out, top, left, h, w, margin=14, thresh=150):
    from pngcrop_local import save_gray
    W,H,g = page(src)
    top=max(0,top); left=max(0,left); h=min(h,H-top); w=min(w,W-left)
    # インクの外接矩形を求める
    x0,y0,x1,y1 = w,h,-1,-1
    for y in range(h):
        row = g[(top+y)*W+left:(top+y)*W+left+w]
        for x in range(w):
            if row[x] < thresh:
                if x<x0: x0=x
                if x>x1: x1=x
                if y<y0: y0=y
                if y>y1: y1=y
    if x1 < 0:
        print('  !! インクなし', out); return
    L=max(0,left+x0-margin); T=max(0,top+y0-margin)
    Wc=min((x1-x0+1)+2*margin, W-L); Hc=min((y1-y0+1)+2*margin, H-T)
    c = bytearray(Wc*Hc)
    for y in range(Hc):
        c[y*Wc:(y+1)*Wc] = g[(T+y)*W+L:(T+y)*W+L+Wc]
    save_gray(out, Wc, Hc, c)
    print('  %-26s %dx%dpx  %6.1f KB  (left=%d top=%d)'
          % (os.path.basename(out), Wc, Hc, os.path.getsize(out)/1000, L, T))


def make_deskew(src, out, top, left, h, w, slope, margin=14, pad=60, thresh=150):
    """slope を打ち消してから切り出す（原本スキャンの傾き対策）。"""
    from pngdeskew import crop_deskew
    from pngcrop_local import save_gray
    W,H,rowsd = crop_deskew(src, top-pad, left-pad, h+2*pad, w+2*pad, slope)
    g = bytearray()
    for r in rowsd: g += r
    # 回転後の座標系で (pad,pad) から w x h をインク基準でトリム
    x0,y0,x1,y1 = w,h,-1,-1
    for y in range(h):
        row = g[(pad+y)*W+pad:(pad+y)*W+pad+w]
        for x in range(w):
            if row[x] < thresh:
                if x<x0: x0=x
                if x>x1: x1=x
                if y<y0: y0=y
                if y>y1: y1=y
    if x1 < 0:
        print('  !! インクなし', out); return
    L=max(0,pad+x0-margin); T=max(0,pad+y0-margin)
    Wc=min((x1-x0+1)+2*margin, W-L); Hc=min((y1-y0+1)+2*margin, H-T)
    c = bytearray(Wc*Hc)
    for y in range(Hc):
        c[y*Wc:(y+1)*Wc] = g[(T+y)*W+L:(T+y)*W+L+Wc]
    save_gray(out, Wc, Hc, c)
    print('  %-26s %dx%dpx  %6.1f KB  slope=%+.5f' % (os.path.basename(out), Wc, Hc, os.path.getsize(out)/1000, slope))

if __name__ == '__main__':
    os.chdir('/Users/yutaka/Documents/入試物理基礎演習')
    only = sys.argv[1:] or None
    from jobs_new15 import jobs
    for j in jobs:
        if only and not any(k in j[1] for k in only): continue
        make(*j)
