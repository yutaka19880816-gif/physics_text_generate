# -*- coding: utf-8 -*-
"""スキャンの傾きを「本来水平な長い線」から自動で測る。
   使い方:  slope_of_band(png, thickness=(2,6))
   各列で太さ 2〜6px の暗い塊の中心を拾い，その y のモード付近だけを最小二乗で直線近似する。
   （曲線の頂点など，別の水平っぽい塊を拾ってしまうのを避けるため）
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pnglighten import decode

def slope_of_band(path, thickness=(2,6), step=6, tol=25):
    W,H,bpp,rows = decode(path)
    cands=[]
    for x in range(0,W,step):
        runs=[]; cur=[]
        for y in range(H):
            if rows[y][x*bpp] < 128: cur.append(y)
            elif cur: runs.append(cur); cur=[]
        if cur: runs.append(cur)
        for r in runs:
            if thickness[0] <= len(r) <= thickness[1]:
                cands.append((x,(r[0]+r[-1])/2.0))
    if len(cands) < 20: return None, 0
    # y のモード（tol 幅のヒストグラムで最多のビン）に属する点だけ使う
    best=None
    for c in cands:
        grp=[p for p in cands if abs(p[1]-c[1]) <= tol]
        if best is None or len(grp) > len(best): best=grp
    # 1列に2点以上ある x は捨てる（曲線と軸を同時に拾っている）
    from collections import Counter
    cnt=Counter(p[0] for p in best)
    pts=[p for p in best if cnt[p[0]]==1]
    if len(pts) < 20: return None, len(pts)
    n=len(pts); sx=sum(p[0] for p in pts); sy=sum(p[1] for p in pts)
    sxx=sum(p[0]**2 for p in pts); sxy=sum(p[0]*p[1] for p in pts)
    return (n*sxy-sx*sy)/(n*sxx-sx*sx), n

if __name__ == '__main__':
    for f in sys.argv[1:]:
        s,n = slope_of_band(f)
        print('%-40s slope=%s 点数=%d' % (os.path.basename(f),
              ('%.5f (%.3f度)'%(s,math.degrees(math.atan(s)))) if s else 'NG', n))
