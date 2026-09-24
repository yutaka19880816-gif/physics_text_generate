# -*- coding: utf-8 -*-
# 新第19回の例題23・24・25 の図を，講義編 第2冊の原本スキャンPDFから切り出す。
#   /Users/yutaka/Google Drive/マイドライブ/鉄緑会物理/20161215144626.pdf
#     PDFページ n ＝ 原本 p(2n+2)|p(2n+3)（見開き）
#     PDFページ4 = 原本 p10|p11 … §26.1 くさびガラス と 例題23
#     PDFページ5 = 原本 p12|p13 … §26.2 ニュートンリング と 例題24
#     PDFページ6 = 原本 p14|p15 … §26.3 の続き と 例題25
#   gs で 400dpi にしてから，窓の中のインクの外接矩形でトリムする。
#   傾きは pngslope で測ったところ p14 で +0.0031（＝0.18度）とほぼ0だったので補正しない。
#   例題25 の図は網点なので pnglighten をかける。
import subprocess, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from pngtrim import ink_bbox
from pngcrop_local import load_gray, save_gray

SRCPDF = '/Users/yutaka/Google Drive/マイドライブ/鉄緑会物理/20161215144626.pdf'
CACHE  = '/tmp/_new19ex_p%d_r%d.png'

def page(n, dpi=400):
    f = CACHE % (n, dpi)
    if not os.path.exists(f):
        subprocess.run(['gs', '-q', '-dNOPAUSE', '-dBATCH', '-sDEVICE=png16m', '-r%d' % dpi,
                        '-dFirstPage=%d' % n, '-dLastPage=%d' % n, '-sOutputFile=' + f, SRCPDF],
                       check=True)
    return f

_cache = {}
def load(n, dpi=400):
    f = page(n, dpi)
    if f not in _cache:
        _cache[f] = load_gray(f)
        print('  (loaded %s %dx%d)' % (os.path.basename(f), _cache[f][0], _cache[f][1]))
    return _cache[f]

def make(pg, out, top, left, h, w, dpi=400, margin=16, thresh=150):
    """座標は 400dpi 基準で書き，dpi を上げるとその比で自動的に換算する。
       網点の図は 700dpi で切ると，明るくしたあとも線と文字が黒く残る（下記 lighten 参照）。"""
    W, H, g = load(pg, dpi)
    k = dpi / 400.0
    top = int(top * k); left = int(left * k); h = int(h * k); w = int(w * k); margin = int(margin * k)
    top = max(0, top); left = max(0, left); h = min(h, H - top); w = min(w, W - left)
    x0, y0, x1, y1 = w, h, -1, -1
    for y in range(h):
        row = g[(top + y) * W + left:(top + y) * W + left + w]
        for x in range(w):
            if row[x] < thresh:
                if x < x0: x0 = x
                if x > x1: x1 = x
                if y < y0: y0 = y
                if y > y1: y1 = y
    if x1 < 0:
        print('  !! インクなし', out); return
    L = max(0, left + x0 - margin); T = max(0, top + y0 - margin)
    Wc = min((x1 - x0 + 1) + 2 * margin, W - L); Hc = min((y1 - y0 + 1) + 2 * margin, H - T)
    c = bytearray(Wc * Hc)
    for y in range(Hc):
        c[y * Wc:(y + 1) * Wc] = g[(T + y) * W + L:(T + y) * W + L + Wc]
    save_gray(out, Wc, Hc, c)
    print('  %-26s %dx%dpx  %6.1f KB  (left=%d top=%d)'
          % (os.path.basename(out), Wc, Hc, os.path.getsize(out) / 1000, L, T))

from mkfig_new19 import lighten   # 「元の解像度で blur+gamma → 面積平均で縮小」の実装

# 座標は 400dpi 基準。最後の値は切り出すときの dpi。
# 網点の図は 700dpi で切る（明るくしたあとに面積平均で縮めるので，線と文字が黒く残る）。
jobs = [
 (4, 'fig/n19_ex23.png',  930, 4220,  480, 1120, 400),   # 例題23 くさびガラス（n1,n2,n3・d・l）
 (5, 'fig/n19_ex24.png',  360, 4540,  900,  880, 400),   # 例題24 平凸レンズとガラス平板（R・d・r）
 (6, 'fig/n19_ex25.png', 2010, 1720,  830,  950, 700),   # 例題25 水面上の油膜（網点）
]

if __name__ == '__main__':
    os.chdir('/Users/yutaka/Documents/入試物理基礎演習')
    only = sys.argv[1:] or None
    for j in jobs:
        if only and not any(k in j[1] for k in only): continue
        make(*j)
    if not only or any('ex25' in k for k in only):
        lighten('fig/n19_ex25.png', 56, gamma=0.30, blur=2, floor=0)   # .tex の width と一致させる
