# -*- coding: utf-8 -*-
# 新第21回（気体の状態方程式と熱力学第一法則）で必要な図の切り出し。
#   第21回の図は旧⑭の7枚（fig/ch14_*.png）をそのまま流用するので，
#   新規に切るのは練習［9］＝旧⑱章末[33]〈ジュールの実験〉の装置図1枚だけ。
#     問題図：問題編 prob_p47.png（右上。断熱容器＋羽根車＋滑車＋おもり）
#   窓は texify_draft/figprobe.py で実測した（col の 0 が続く帯 x=2560 と x=3540、
#   row の 0 が続く帯 y=300 と y=1410 の内側）。
#   sips の --cropOffset は左上原点ではないので使わない（mkfig_new16.make が純Python）。
#   使い方:  python3 texify_draft/mkfig_new21.py        （プロジェクトルートで実行）
#            python3 texify_draft/mkfig_new21.py --light  … 網点処理だけやり直す
import sys, os, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from mkfig_new16 import make
from mkfig_new20 import area_down, lighten

# 版面での貼り付け幅[mm]（physics_new21.tex の \includegraphics の width と必ず一致させること）
WIDTH_MM = 52
DPI      = 360
TARGET   = int(WIDTH_MM / 25.4 * DPI)      # 737px

OUT = 'fig/n21_a09_joule.png'

def remake_xbb(png):
    """.xbb が .png より新しいと extractbb は黙って再生成をスキップするので，必ず消してから作る
       （組版チェックリスト §1.5）。"""
    xbb = png[:-4] + '.xbb'
    if os.path.exists(xbb): os.remove(xbb)
    subprocess.run(['extractbb', png], check=True)

if '--light' not in sys.argv:
    # top, left, h, w（左上原点・px）
    make('prob_p47.png', OUT, 290, 2555, 1125, 990, margin=16)

# 容器の壁と地面が網点なので薄くする。線画に近い網点なので gamma は高め・blur は 1。
lighten(OUT, WIDTH_MM, gamma=0.55, blur=1)
area_down(OUT, OUT, TARGET)
remake_xbb(OUT)
print('  %s 完成' % OUT)
