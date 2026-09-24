# -*- coding: utf-8 -*-
# 新第22回（気体分子運動論と内部エネルギー）で原本から切り出す図。
#   第22回の図はほとんど旧⑮・旧⑯のもの（fig/ch15_*.png, fig/ch16_*.png）を流用するので，
#   新規に切るのは 練習［21］＝旧⑱章末[34]〈断熱変化における気体分子運動論〉の装置図1枚だけ。
#     問題図：問題編 prob_p47.png（右中ほど。シリンダー＋ピストン＋「N 個」＋x,y軸）
#   窓は texify_draft/figprobe.py で実測した
#     （col の 0 が続く帯 x=2480〜2530 と x=3520 の内側，row の 0 が続く帯 y=2070 と y=2580 の内側）。
#   sips の --cropOffset は左上原点ではないので使わない（make() が純Python）。
#   使い方:  python3 texify_draft/mkfig_new22.py        （プロジェクトルートで実行）
import sys, os, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from mkfig_new16 import make
from mkfig_new20 import area_down

# 版面での貼り付け幅[mm]（physics_new22.tex の \includegraphics の width と必ず一致させること）
WIDTH_MM = 46
DPI      = 360
TARGET   = int(WIDTH_MM / 25.4 * DPI)

OUT = 'fig/n22_a21_cyl.png'

def remake_xbb(png):
    """.xbb が .png より新しいと extractbb は黙って再生成をスキップするので，必ず消してから作る
       （組版チェックリスト §1.5）。"""
    xbb = png[:-4] + '.xbb'
    if os.path.exists(xbb): os.remove(xbb)
    subprocess.run(['extractbb', png], check=True)

# top, left, h, w（左上原点・px）
make('prob_p47.png', OUT, 2070, 2532, 515, 985, margin=16)
# 線画だけなので網点処理は不要。360dpi 相当まで面積平均で縮小するだけ。
area_down(OUT, OUT, TARGET)
remake_xbb(OUT)
print('  %s 完成' % OUT)


# ---------------------------------------------------------------------------
# 旧⑮⑯から流用している例題図のうち，窓が狭すぎて切れていた2枚を切り直す
#   （2026-09-20 ユーザー指摘「図が切れている箇所があります」）
#   ・fig/ch16_ex10_cyl.png（例題9＝原本の例題10 の定圧シリンダー）
#       mkfig_ch16ex.py の窓 left=6820 はシリンダーの左壁（x≒6860）を
#       ink_bbox の minrun=2 で拾い切れず，左壁が丸ごと落ちていた（開いた管に見える）。
#       図と本文の境（x=6760〜6835 が 0）の内側 left=6790 から切り直す。
#   ・fig/ch15_ex7_pt.png（例題7 の P-T 図）
#       mkfig_ch15ex.py の窓 w=970 が $T$ 軸の矢先とちょうど同じ位置で，
#       右に余白が無く矢先が数px欠けていた。w=1010 に広げる。
#   どちらも physics_ch15.tex / physics_ch16.tex でも使っている図なので，
#   切り直すとそちらの紙面もよくなる。
#   使い方:  python3 texify_draft/mkfig_new22.py --recut
# ---------------------------------------------------------------------------
if '--recut' in sys.argv:
    from pngdeskew import crop_deskew, save as save_deskew

    def _ink_bbox(rows, w, h, thresh=170):
        x0, y0, x1, y1 = w, h, -1, -1
        for y in range(h):
            r = rows[y]
            for x in range(w):
                if r[x] < thresh:
                    if x < x0: x0 = x
                    if x > x1: x1 = x
                    if y < y0: y0 = y
                    if y > y1: y1 = y
        return None if x1 < 0 else (x0, y0, x1, y1)

    def recut(src, out, top, left, h, w, slope, margin=18, maxw=None):
        W, H, rows = crop_deskew(src, top, left, h, w, slope)
        b = _ink_bbox(rows, W, H)
        if b is None:
            print('  !! インクなし', out); return
        x0, y0, x1, y1 = b
        x0 = max(0, x0 - margin); y0 = max(0, y0 - margin)
        x1 = min(W - 1, x1 + margin); y1 = min(H - 1, y1 + margin)
        nw, nh = x1 - x0 + 1, y1 - y0 + 1
        save_deskew(out, nw, nh, [r[x0:x1 + 1] for r in rows[y0:y1 + 1]])
        if maxw and nw > maxw:
            subprocess.run(['sips', '--resampleWidth', str(maxw), out], capture_output=True)
            nw = maxw
        remake_xbb(out)
        print('  %-24s %dx%dpx  %6.1f KB' % (os.path.basename(out), nw, nh,
                                             os.path.getsize(out) / 1000))

    SRC = '/Users/yutaka/Google Drive/マイドライブ/鉄緑会物理/20161215143926.pdf'
    for page in (6, 8):
        big = '/tmp/_recut_page%d.png' % page
        if not os.path.exists(big):
            subprocess.run(['gs', '-q', '-dNOPAUSE', '-dBATCH',
                            '-dFirstPage=%d' % page, '-dLastPage=%d' % page,
                            '-sDEVICE=png16m', '-r600', '-sOutputFile=' + big, SRC], check=True)
    # 原本 p77（PDF 8 の右ページ，傾き +0.0105）：左壁まで入る窓
    recut('/tmp/_recut_page8.png', 'fig/ch16_ex10_cyl.png', 1985, 6790, 620, 1345,
          +0.010500, maxw=760)
    # 原本 p73（PDF 6 の右ページ，傾き +0.007857）：$T$ 軸の矢先まで入る窓
    recut('/tmp/_recut_page6.png', 'fig/ch15_ex7_pt.png', 1995, 7060, 845, 1010,
          +0.007857)
