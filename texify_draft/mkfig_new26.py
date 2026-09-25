# -*- coding: utf-8 -*-
# 新第26回（電流・電気抵抗・抵抗の接続と計器）で必要な図の切り出し。
# 切り出しの実体は mkfig_new16.make。座標は texify_draft/jobs_new26.py。
#   使い方:  python3 texify_draft/mkfig_new26.py            … 全部
#            python3 texify_draft/mkfig_new26.py p63 a68    … 名前に含む図だけ
import sys, os, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from mkfig_new16 import make

def remake_xbb(paths):
    """.xbb は消してから1枚ずつ extractbb（組版チェックリスト §1.5）。"""
    for p in paths:
        x = p[:-4] + '.xbb'
        if os.path.exists(x): os.remove(x)
    for p in paths:
        subprocess.run(['extractbb', p], check=True)
    if paths: print('  extractbb %d 枚' % len(paths))

if __name__ == '__main__':
    os.chdir(os.path.dirname(HERE))
    only = sys.argv[1:] or None
    from jobs_new26 import jobs
    done = []
    for j in jobs:
        if only and not any(k in j[1] for k in only): continue
        make(*j)
        done.append(j[1])
    if '--noxbb' not in sys.argv: remake_xbb(done)
