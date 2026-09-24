# -*- coding: utf-8 -*-
"""列ストリップを空白帯で切って「ブロック」に分け，図の候補を探す（2026-09-05 作成）。

    python3 texify_draft/blocks.py img/scan/prob2_p77.png 120 1600
        → <png> <left> <width>。空白が40px以上続いたところで区切る。

「密度」は 1行あたりのインク量で，**13〜40 なら線画の図，70以上は本文か枠**が目安。
解答編は2段組なので 左段 x=120〜1720／右段 x=2000〜3650 を目安に2回かける。
切り出し窓の y はここで出たブロックの範囲をそのまま使えばよい（x は段の全幅でよい）。
""" 
import sys
sys.path.insert(0,'/Users/yutaka/Documents/入試物理基礎演習/texify_draft')
from pngcrop_local import load_gray
src=sys.argv[1]; left=int(sys.argv[2]); w=int(sys.argv[3])
bin=10; gapmin=4   # 空白が 40px 以上続いたら区切り
W,H,g=load_gray(src)
prof=[]
for y0 in range(0,H,bin):
    n=0
    for y in range(y0,min(y0+bin,H)):
        row=g[y*W:(y+1)*W]
        for x in range(left,min(left+w,W),2):
            if row[x]<150: n+=1
    prof.append(n)
blocks=[];cur=None;gap=0
for i,n in enumerate(prof):
    if n>=3:
        if cur is None: cur=[i,i]
        else: cur[1]=i
        gap=0
    else:
        if cur is not None:
            gap+=1
            if gap>=gapmin:
                blocks.append(cur);cur=None;gap=0
if cur: blocks.append(cur)
for a,b in blocks:
    tot=sum(prof[a:b+1]); hh=(b-a+1)*bin
    print('y %5d - %5d  (h=%4d)  ink=%7d  密度=%5.0f' % (a*bin,(b+1)*bin,hh,tot,tot/hh))
