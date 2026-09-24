# -*- coding: utf-8 -*-
# 新第17回（ドップラー効果と衝撃波）で必要な図の切り出し。
# 切り出しの実体は mkfig_new16.make（PNGを純Pythonでデコード→窓の中のインクの外接矩形でトリム）。
# 座標は texify_draft/jobs_new17.py に置いてある。
#   使い方:  python3 texify_draft/mkfig_new17.py            … 全部
#            python3 texify_draft/mkfig_new17.py p42 a40    … 名前に含む図だけ
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from mkfig_new16 import make

if __name__ == '__main__':
    os.chdir('/Users/yutaka/Documents/入試物理基礎演習')
    only = sys.argv[1:] or None
    from jobs_new17 import jobs
    for j in jobs:
        if only and not any(k in j[1] for k in only): continue
        make(*j)
