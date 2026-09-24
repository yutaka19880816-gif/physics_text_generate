# -*- coding: utf-8 -*-
# 新第25回の例題の図を，原本の講義編スキャン（20161215144626.pdf の PDFページ17〜20
# ＝原本 p36/p37・p38/p39・p40/p41・p42/p43）から切り出す。600dpi の PNG を $S に置いてから実行。
#
#   gs -q -dNOPAUSE -dBATCH -sDEVICE=pnggray -r600 -dFirstPage=N -dLastPage=N -sOutputFile=hiN.png <原本.pdf>
#
# 【傾き】texify_draft/pngslope.py で KEY 枠・まとめ枠の細罫（0.4pt）を測った。
#   見開きでもページごとに違う：p36=-0.0095／p37=+0.0040／p38=+0.0001／p39=-0.0006／
#   p40=-0.0041／p41=+0.0009／p42=-0.0036／p43=+0.0001
# 【練習［22］は原本の例題13】なので，その図もここで切り出す（再編案で例題→練習へ格下げ）。
import sys, os, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from mkfig_new16 import make_deskew
S = ('/private/tmp/claude-501/-Users-yutaka-Documents-Claude-Code----math-tex-tool'
     '/bcd43292-8d06-445f-97d9-7e46546ccfa9/scratchpad/r25')

if __name__ == '__main__':
    os.chdir('/Users/yutaka/Documents/入試物理基礎演習')
    #        src            out                     top  left    h     w   slope
    jobs = [
     (S+'/hi17.png', 'fig/n25_ex6_zu.png',  4255, 6690,  610, 1500,  0.0040),  # 例題6（原本8）
     (S+'/hi18.png', 'fig/n25_ex7_zu.png',  1620, 4850,  660, 3240, -0.0006),  # 例題7（原本9）(1)(2)(3)
     (S+'/hi19.png', 'fig/n25_ex8_zu.png',  4660, 3400,  850,  850, -0.0041),  # 例題8（原本10）並列
     (S+'/hi19.png', 'fig/n25_ex9_zu.png',  1440, 7280,  730,  830,  0.0009),  # 例題9（原本11）直列
     (S+'/hi20.png', 'fig/n25_ex10_zu.png',  600, 2960,  950, 1215, -0.0036),  # 例題10（原本12）回路
     (S+'/hi20.png', 'fig/n25_p55_zu.png',  3270, 4840,  750, 3225,  0.0001),  # 練習［22］（原本の例題13）
    ]
    only = sys.argv[1:] or None
    done = []
    for j in jobs:
        if only and not any(k in j[1] for k in only): continue
        make_deskew(*j)
        done.append(j[1])
    for p in done:
        x = p[:-4] + '.xbb'
        if os.path.exists(x): os.remove(x)
    for p in done:
        subprocess.run(['extractbb', p], check=True)
    if done: print('  extractbb %d 枚' % len(done))
