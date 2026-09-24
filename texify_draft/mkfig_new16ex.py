# -*- coding: utf-8 -*-
# 新第16回の例題の図を，原本の講義編スキャン（20161215143926.pdf の PDFページ21・22＝原本p102/103・p104/105）
# から切り出す。600dpi で描画した PNG を $S に置いてから実行する。
#
# 【傾き】原本 p105 は 1.2〜1.5度 傾いている（2026-09-04 ユーザー指摘「例題12の図が傾いている」）。
#   ・p105 は細い罫（KEY枠・まとめ枠）を texify_draft/pngslope.py で測って slope=+0.021。
#     例題枠の太い罫（1.2pt＝600dpiで約10px）は pngslope の太さフィルタ(2〜6px)から外れるので使えない。
#   ・共鳴管の図には長い水平線が無いので，**タンクの縦壁の x が y でどれだけずれるか**で検算した
#     （縦線では slope = −dx/dy）。補正前 +0.0262／+0.0250 → 補正後 +0.0062／+0.0005。
#   ・p102 は例題10の図の弦（長い水平線）を pngslope で測って slope=+0.0051／+0.0053。
import sys, os
HERE = '/Users/yutaka/Documents/入試物理基礎演習/texify_draft'
sys.path.insert(0, HERE)
from mkfig_new16 import make, make_deskew
S = '/private/tmp/claude-501/-Users-yutaka-Documents-Claude-Code----math-tex-tool/eac48c81-c173-4fc8-82ff-b0fd70232fcb/scratchpad/n16'

if __name__ == '__main__':
    os.chdir('/Users/yutaka/Documents/入試物理基礎演習')
    #        src               out                       top  left    h     w   slope
    jobs = [
     (S+'/hi21.png', 'fig/n16_ex10_z1.png',   2455, 2500,  845, 1480, 0.0051),  # 例題10 図1（音叉を横に）
     (S+'/hi21.png', 'fig/n16_ex10_z2.png',   3380, 2500,  900, 1480, 0.0053),  # 例題10 図2（音叉を立てて）
     (S+'/hi22.png', 'fig/n16_ex12_tube.png',  645, 7175, 1355,  960, 0.0210),  # 例題12 共鳴管の装置
     (S+'/hi22.png', 'fig/n16_kyoshin.png',   3930, 7150, 1330, 1000, 0.0195),  # 参考 固有振動と共鳴（振り子）
    ]
    only = sys.argv[1:] or None
    for j in jobs:
        if only and not any(k in j[1] for k in only): continue
        if j[6]: make_deskew(*j)
        else:    make(*j[:6])
