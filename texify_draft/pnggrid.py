# -*- coding: utf-8 -*-
"""元画像の座標グリッドを重ねた縮小PNGを作る（切り出し窓を目で読むため。2026-09-05 作成）。

    python3 texify_draft/pnggrid.py img/scan/prob2_p7.png /tmp/g_p7.png 200
        → <src> <out> [grid間隔px]。幅1560pxに縮小し，200pxごとに罫と座標ラベルを描く。

ラベルは**元画像の座標**なので，そのまま jobs_new*.py の (top,left,h,w) に使える。""" 
import sys, os
sys.path.insert(0,'/Users/yutaka/Documents/入試物理基礎演習/texify_draft')
from pngcrop_local import load_gray, save_gray

# 5x7 の極小数字フォント
F = {
'0':["111","101","101","101","111"],'1':["010","110","010","010","111"],
'2':["111","001","111","100","111"],'3':["111","001","111","001","111"],
'4':["101","101","111","001","001"],'5':["111","100","111","001","111"],
'6':["111","100","111","101","111"],'7':["111","001","010","010","010"],
'8':["111","101","111","101","111"],'9':["111","101","111","001","111"],
}
def put(g,W,H,x,y,s,sc=2):
    for ch in s:
        pat=F.get(ch)
        if pat:
            for r,row in enumerate(pat):
                for c,v in enumerate(row):
                    if v=='1':
                        for dy in range(sc):
                            for dx in range(sc):
                                X,Y=x+c*sc+dx,y+r*sc+dy
                                if 0<=X<W and 0<=Y<H: g[Y*W+X]=0
        x+=4*sc

src,out,step = sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv)>3 else 200
W,H,g = load_gray(src)
sc = 1560.0/W
nw,nh = int(W*sc), int(H*sc)
s = bytearray(nw*nh)
for y in range(nh):
    sy=int(y/sc)
    base=sy*W
    row=g[base:base+W]
    for x in range(nw):
        s[y*nw+x]=row[int(x/sc)]
# グリッド線
for X in range(0,W,step):
    x=int(X*sc)
    if x<nw:
        for y in range(nh):
            if (y//4)%2==0: s[y*nw+x]=120
for Y in range(0,H,step):
    y=int(Y*sc)
    if y<nh:
        for x in range(nw):
            if (x//4)%2==0: s[y*nw+x]=120
# ラベル
for X in range(0,W,step*2):
    x=int(X*sc)
    if x<nw-30: put(s,nw,nh,x+2,2,str(X))
for Y in range(0,H,step*2):
    y=int(Y*sc)
    if y<nh-12: put(s,nw,nh,2,y+2,str(Y))
save_gray(out,nw,nh,s)
print(out,nw,nh,'orig',W,H)
