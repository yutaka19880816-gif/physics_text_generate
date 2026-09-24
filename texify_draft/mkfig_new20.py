# -*- coding: utf-8 -*-
# 新第20回（レンズと球面鏡）で必要な図の切り出し。
# 切り出しの実体は mkfig_new16.make（PNGを純Pythonでデコード→窓の中のインクの外接矩形でトリム）。
# 座標は texify_draft/jobs_new20.py に置いてある。
#   使い方:  python3 texify_draft/mkfig_new20.py            … 全部
#            python3 texify_draft/mkfig_new20.py p57 a58    … 名前に含む図だけ
#            python3 texify_draft/mkfig_new20.py --halftone … 網点処理だけやり直す
import sys, os, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from mkfig_new16 import make

def area_down(src, out, target):
    """面積平均で縮小する。最近傍で縮めると網点が拾われてざらつくので必ずこちらを使う。"""
    from pngcrop_local import load_gray, save_gray
    W, H, g = load_gray(src)
    if target >= W:
        if src != out: subprocess.run(['cp', src, out], check=True)
        return
    sx = W / target
    nw, nh = target, max(1, int(H / sx))
    o = bytearray(nw * nh)
    for y in range(nh):
        y0 = int(y * sx); y1 = max(y0 + 1, int((y + 1) * sx))
        for x in range(nw):
            x0 = int(x * sx); x1 = max(x0 + 1, int((x + 1) * sx))
            ssum = 0; n = 0
            for yy in range(y0, min(y1, H)):
                base = yy * W
                for xx in range(x0, min(x1, W)):
                    ssum += g[base + xx]; n += 1
            o[y * nw + x] = ssum // n
    save_gray(out, nw, nh, o)

def lighten(out, mm, gamma=0.30, blur=2, floor=0, src=None, no_recut=False):
    """網点の図を明るくする（原本は fig/orig_halftone/ へ退避）。
       手順が大事：**(1) 元の解像度のまま blur+gamma → (2) 面積平均で版面幅に縮小**。
       先に縮小してから blur すると，線や文字まで灰色になって「全体が薄い」図になる
       （2026-09-05 ユーザー指摘）。src を渡すとその画像を元にする。"""
    orig = os.path.join('fig/orig_halftone', os.path.basename(out))
    if not os.path.exists(orig) and no_recut:
        raise SystemExit('  !! %s の退避元が fig/orig_halftone/ に無い．--halftone を外して切り出しからやり直すこと'
                         % os.path.basename(out))
    if not os.path.exists(orig):
        os.makedirs('fig/orig_halftone', exist_ok=True)
        subprocess.run(['cp', src if src else out, orig], check=True)
    subprocess.run(['cp', orig, out], check=True)
    subprocess.run(['python3', os.path.join(HERE, 'pnglighten.py'),
                    '--blur', str(blur), '--gamma', str(gamma), '--floor', str(floor),
                    out, out], check=True)
    target = int(round(mm / 25.4 * 360))          # 360dpi 相当
    area_down(out, out, target)
    print('  網点処理 %-26s %dpx  gamma=%.2f blur=%d floor=%d'
          % (os.path.basename(out), target, gamma, blur, floor))

if __name__ == '__main__':
    os.chdir('/Users/yutaka/Documents/入試物理基礎演習')
    args = sys.argv[1:]
    only_ht = '--halftone' in args
    only = [a for a in args if not a.startswith('--')] or None
    from jobs_new20 import jobs, halftone, lighten_from_text
    if not only_ht:
        for j in jobs:
            if only and not any(k in j[1] for k in only): continue
            make(*j)
    for out, mm, gm, bl, fl in halftone:
        if only and not any(k in out for k in only): continue
        if os.path.exists(out): lighten(out, mm, gm, bl, fl, no_recut=only_ht)
    for src, out, mm, gm, bl, fl in lighten_from_text:
        if only and not any(k in out for k in only): continue
        lighten(out, mm, gm, bl, fl, src=src)
