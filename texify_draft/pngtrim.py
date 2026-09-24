# -*- coding: utf-8 -*-
"""PNGを純Pythonでデコードして、インク（暗い画素）の外接矩形を返す。
   PIL が無い環境用。8bit の RGB(type2)/RGBA(type6)/Gray(type0) に対応。"""
import zlib, struct, sys
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from imgpath import resolve   # 画像は img/scan・img/text に移動（2026-09-05）

def decode(path):
    d = open(resolve(path),'rb').read()
    assert d[:8]==b'\x89PNG\r\n\x1a\n', path
    pos=8; w=h=None; bd=ct=None; idat=[]
    while pos < len(d):
        ln = struct.unpack('>I', d[pos:pos+4])[0]; typ=d[pos+4:pos+8]
        if typ==b'IHDR':
            w,h,bd,ct,comp,filt,inter = struct.unpack('>IIBBBBB', d[pos+8:pos+21])
            assert bd==8 and inter==0, (bd,inter)
        elif typ==b'IDAT': idat.append(d[pos+8:pos+8+ln])
        elif typ==b'IEND': break
        pos += 12+ln
    raw = zlib.decompress(b''.join(idat))
    bpp = {0:1, 2:3, 4:2, 6:4}[ct]
    stride = w*bpp
    out=[]; prev=bytearray(stride); off=0
    for y in range(h):
        f = raw[off]; off+=1
        line = bytearray(raw[off:off+stride]); off+=stride
        if f==1:
            for x in range(bpp,stride): line[x]=(line[x]+line[x-bpp])&255
        elif f==2:
            for x in range(stride): line[x]=(line[x]+prev[x])&255
        elif f==3:
            for x in range(stride):
                a=line[x-bpp] if x>=bpp else 0
                line[x]=(line[x]+((a+prev[x])>>1))&255
        elif f==4:
            for x in range(stride):
                a=line[x-bpp] if x>=bpp else 0
                b=prev[x]; c=prev[x-bpp] if x>=bpp else 0
                p=a+b-c; pa,pb,pc=abs(p-a),abs(p-b),abs(p-c)
                pr = a if (pa<=pb and pa<=pc) else (b if pb<=pc else c)
                line[x]=(line[x]+pr)&255
        out.append(bytes(line)); prev=line
    return w,h,bpp,out

def ink_bbox(path, thresh=170, minrun=2):
    w,h,bpp,rows = decode(path)
    xs_min, xs_max, ys = w, -1, []
    for y,r in enumerate(rows):
        lo, hi = None, None
        for x in range(w):
            v = r[x*bpp]  # 赤成分（グレー/RGB/RGBAとも先頭）
            if v < thresh:
                if lo is None: lo = x
                hi = x
        if lo is not None:
            ys.append(y)
            xs_min = min(xs_min, lo); xs_max = max(xs_max, hi)
    if not ys: return None
    return xs_min, ys[0], xs_max, ys[-1], w, h

if __name__=='__main__':
    for p in sys.argv[1:]:
        b = ink_bbox(p)
        print(p, '→ bbox', b)
