# -*- coding: utf-8 -*-
# 新第25回（コンデンサーとコンデンサー回路）で必要な図の切り出し。
# 切り出しの実体は mkfig_new16.make（PNGを純Pythonでデコード→窓の中のインクの外接矩形でトリム）。
# 座標は texify_draft/jobs_new25.py に置いてある。
#   使い方:  python3 texify_draft/mkfig_new25.py            … 全部
#            python3 texify_draft/mkfig_new25.py p16 a21    … 名前に含む図だけ
import sys, os, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from mkfig_new16 import make

def remake_xbb(paths):
    """図を作り直したら .xbb は必ず消してから extractbb（組版チェックリスト §1.5）。"""
    for p in paths:
        x = p[:-4] + '.xbb'
        if os.path.exists(x): os.remove(x)
    # extractbb は複数引数を渡すと最初の1枚しか処理しないので1枚ずつ呼ぶ
    for p in paths:
        subprocess.run(['extractbb', p], check=True)
    if paths: print('  extractbb %d 枚' % len(paths))

if __name__ == '__main__':
    os.chdir('/Users/yutaka/Documents/入試物理基礎演習')
    only = sys.argv[1:] or None
    from jobs_new25 import jobs
    done = []
    for j in jobs:
        if only and not any(k in j[1] for k in only): continue
        make(*j)
        done.append(j[1])
    remake_xbb(done)
