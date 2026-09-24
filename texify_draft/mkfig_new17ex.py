# -*- coding: utf-8 -*-
# 新第17回の例題の図を，原本の講義編スキャン（20161215143926.pdf の PDFページ23・25・26・27
# ＝原本 p106/107・p110/111・p112/113・p114/115）から切り出す。600dpi の PNG を $S に置いてから実行。
#
#   gs -q -dNOPAUSE -dBATCH -sDEVICE=pnggray -r600 -dFirstPage=N -dLastPage=N -sOutputFile=hiN.png <原本.pdf>
#
# 【傾き】texify_draft/pngslope.py で KEY 枠・まとめ枠の細罫（0.4pt）を測った。
#   見開きでもページごとに違う：p107=+0.0203／p110=+0.0050／p111=+0.0198／
#   p112=-0.0026／p113=+0.0190／p114=+0.0163
# 【例題15の図は例題13の図と同一】（原本でも同じ4つの配置を再掲している）ので，
#   n17_ex13_z.png を例題15でもそのまま使う。切り出しは1回だけ。
import sys, os
HERE = '/Users/yutaka/Documents/入試物理基礎演習/texify_draft'
sys.path.insert(0, HERE)
from mkfig_new16 import make_deskew
S = ('/private/tmp/claude-501/-Users-yutaka-Documents-Claude-Code----math-tex-tool'
     '/70e8f740-74db-42e9-b903-6a74517c90df/scratchpad/n17')

if __name__ == '__main__':
    os.chdir('/Users/yutaka/Documents/入試物理基礎演習')
    #        src              out                      top  left    h     w   slope
    jobs = [
     (S+'/hi23.png', 'fig/n17_ex13_z.png', 2590, 5280, 1460, 2520,  0.0203),  # 例題13・15 の4配置
     (S+'/hi25.png', 'fig/n17_ex16_z.png', 2870, 5180,  600, 2560,  0.0198),  # 例題16 風がある場合
     (S+'/hi26.png', 'fig/n17_ex17_z.png', 2320, 2620,  690, 1380, -0.0026),  # 例題17 壁R・音源S・観測者O
     (S+'/hi26.png', 'fig/n17_ex18_z.png', 2510, 6440,  610, 1740,  0.0190),  # 例題18 円運動する音源
     (S+'/hi27.png', 'fig/n17_ex19_z.png', 1000, 2940,  980,  960,  0.0163),  # 例題19 O・O′・P
    ]
    only = sys.argv[1:] or None
    for j in jobs:
        if only and not any(k in j[1] for k in only): continue
        make_deskew(*j)
