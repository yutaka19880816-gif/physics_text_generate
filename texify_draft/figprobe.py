# -*- coding: utf-8 -*-
"""スキャンページの「図と本文の境目」を実測する（切り出し窓を目分量で決めないための道具）。

    python3 texify_draft/figprobe.py row prob_p160.png 4350 650 430 1100
        → 行方向のインク量を10行ごとに出す。0 が続く帯が図と本文の境目。
    python3 texify_draft/figprobe.py col prob_p56.png 50 724 1800 1800
        → 列方向のインク量を20列ごとに出す。段の間の空白（＝本文の右端）が分かる。

    引数は共通で <png> <top> <height> <left> <width>（左上原点・px）。

なぜ要るか：切り出し窓を目で決めると，ほぼ必ず隣の本文を1行巻き込む（第16回では
9枚のうち7枚で発生した）。mkfig_new*.py の make() はインクの外接矩形で自動トリムするので，
窓の中に本文が1文字でも入っていると，その本文まで含めた矩形が出力される。
"""
import sys
sys.path.insert(0, '/Users/yutaka/Documents/入試物理基礎演習/texify_draft')
from pngcrop_local import load_gray

THRESH = 150


def rows(g, W, H, top, h, left, w, bin=10):
    out = []
    for y0 in range(top, min(top + h, H), bin):
        n = 0
        for y in range(y0, min(y0 + bin, H)):
            row = g[y * W:(y + 1) * W]
            for x in range(left, min(left + w, W), 2):
                if row[x] < THRESH: n += 1
        out.append('%d:%d' % (y0, n))
    return out


def cols(g, W, H, top, h, left, w, bin=20):
    out = []
    for x0 in range(left, min(left + w, W), bin):
        n = 0
        for y in range(top, min(top + h, H), 3):
            row = g[y * W:(y + 1) * W]
            for x in range(x0, min(x0 + bin, W)):
                if row[x] < THRESH: n += 1
        out.append('%d:%d' % (x0, n))
    return out


if __name__ == '__main__':
    if len(sys.argv) < 7:
        print(__doc__); sys.exit(1)
    mode, src = sys.argv[1], sys.argv[2]
    top, h, left, w = (int(a) for a in sys.argv[3:7])
    W, H, g = load_gray(src)
    print('W=%d H=%d' % (W, H))
    print(' '.join((rows if mode == 'row' else cols)(g, W, H, top, h, left, w)))
