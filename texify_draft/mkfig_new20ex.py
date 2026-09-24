# -*- coding: utf-8 -*-
# 新第20回の例題28・29 の図を，講義編 第2冊の原本スキャンPDFから切り出す。
#   /Users/yutaka/Google Drive/マイドライブ/鉄緑会物理/20161215144626.pdf
#     PDFページ n ＝ 原本 p(2n+2)|p(2n+3)（見開き）
#     PDFページ8 = 原本 p18|p19 … 例題28〈レンズによる像の作図〉
#     PDFページ9 = 原本 p20|p21 … 例題29〈レンズによる像〉（虚光源）
#   例題26・27 の図は 練習㉗[60][61] と同一なので問題編スキャン（prob2_p11）から切ってある
#   （jobs_new20.py の n20_ex26 / n20_ex27）。
#   レンズは網点なので 700dpi で切ってから pnglighten をかける。
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from mkfig_new19ex import make, load, page   # 400dpi 基準の座標→dpi 換算つき切り出し
from mkfig_new19 import lighten

jobs = [
 (8, 'fig/n20_ex28a.png', 690, 540,  430, 1900, 700),  # 例題28 (1)(2) 凸レンズ
 (8, 'fig/n20_ex28b.png',1390, 540,  420, 1900, 700),  # 例題28 (3)(4) 凹レンズ
 (9, 'fig/n20_ex29a.png', 700, 560,  420, 1930, 700),  # 例題29 (1)(2)
 (9, 'fig/n20_ex29b.png',1160, 560,  400, 1930, 700),  # 例題29 (3)
]

if __name__ == '__main__':
    os.chdir('/Users/yutaka/Documents/入試物理基礎演習')
    only = sys.argv[1:] or None
    for j in jobs:
        if only and not any(k in j[1] for k in only): continue
        make(*j)
    if not only or any('ex28' in k for k in only):
        lighten('fig/n20_ex28a.png', 128, gamma=0.28, blur=1, floor=0)
        lighten('fig/n20_ex28b.png', 128, gamma=0.28, blur=1, floor=0)
    if not only or any('ex29' in k for k in only):
        lighten('fig/n20_ex29a.png', 128, gamma=0.28, blur=1, floor=0)
        lighten('fig/n20_ex29b.png', 99, gamma=0.28, blur=1, floor=0)
