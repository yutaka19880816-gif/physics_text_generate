# -*- coding: utf-8 -*-
"""純Pythonの PNG 切り出し／縮小。sips の cropOffset 仕様に依存しないため自前で持つ。"""
import zlib, struct, sys, os
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from imgpath import resolve   # 画像は img/scan・img/text に移動（2026-09-05）
sys.path.insert(0, '/Users/yutaka/Documents/入試物理基礎演習/texify_draft')
from pngtrim import decode   # decode(path) -> ?

def load_gray(path):
    """(w, h, bytearray gray) を返す"""
    d = open(resolve(path),'rb').read()
    assert d[:8]==b'\x89PNG\r\n\x1a\n', path
    pos=8; idat=[]; w=h=bd=ct=None; plte=None; trns=None
    while pos < len(d):
        ln = struct.unpack('>I', d[pos:pos+4])[0]; typ=d[pos+4:pos+8]
        if typ==b'IHDR':
            w,h,bd,ct,comp,filt,inter = struct.unpack('>IIBBBBB', d[pos+8:pos+21])
        elif typ==b'PLTE': plte = d[pos+8:pos+8+ln]
        elif typ==b'IDAT': idat.append(d[pos+8:pos+8+ln])
        elif typ==b'IEND': break
        pos += 12+ln
    assert bd==8 and inter==0, (path,bd,inter)
    raw = zlib.decompress(b''.join(idat))
    bpp = {0:1,2:3,3:1,4:2,6:4}[ct]
    stride = w*bpp
    out = bytearray(h*stride); prev = bytearray(stride); p=0
    for y in range(h):
        f = raw[p]; p+=1
        line = bytearray(raw[p:p+stride]); p+=stride
        if f==1:
            for i in range(bpp,stride): line[i]=(line[i]+line[i-bpp])&255
        elif f==2:
            for i in range(stride): line[i]=(line[i]+prev[i])&255
        elif f==3:
            for i in range(stride):
                a = line[i-bpp] if i>=bpp else 0
                line[i]=(line[i]+((a+prev[i])>>1))&255
        elif f==4:
            for i in range(stride):
                a = line[i-bpp] if i>=bpp else 0
                b = prev[i]; c = prev[i-bpp] if i>=bpp else 0
                pa=abs(b-c); pb=abs(a-c); pc=abs(a+b-2*c)
                pr = a if (pa<=pb and pa<=pc) else (b if pb<=pc else c)
                line[i]=(line[i]+pr)&255
        out[y*stride:(y+1)*stride]=line; prev=line
    g = bytearray(w*h)
    if ct==0:
        g[:] = out
    elif ct in (2,6):
        n = 3 if ct==2 else 4
        for i in range(w*h):
            r=out[i*n]; gg=out[i*n+1]; b=out[i*n+2]
            g[i]=(r*299+gg*587+b*114)//1000
    elif ct==4:
        for i in range(w*h): g[i]=out[i*2]
    elif ct==3:
        for i in range(w*h):
            idx=out[i]; r=plte[idx*3]; gg=plte[idx*3+1]; b=plte[idx*3+2]
            g[i]=(r*299+gg*587+b*114)//1000
    return w,h,g

def save_gray(path,w,h,g):
    raw = bytearray()
    for y in range(h):
        raw.append(0); raw += g[y*w:(y+1)*w]
    def chunk(t,data):
        c = struct.pack('>I',len(data))+t+data
        return c+struct.pack('>I', zlib.crc32(t+data)&0xffffffff)
    png = b'\x89PNG\r\n\x1a\n'
    png += chunk(b'IHDR', struct.pack('>IIBBBBB',w,h,8,0,0,0,0))
    png += chunk(b'IDAT', zlib.compress(bytes(raw),6))
    png += chunk(b'IEND', b'')
    open(path,'wb').write(png)

def crop(src, out, top, left, h, w, scale=None):
    W,H,g = load_gray(src)
    top=max(0,top); left=max(0,left)
    h=min(h,H-top); w=min(w,W-left)
    c = bytearray(w*h)
    for y in range(h):
        c[y*w:(y+1)*w] = g[(top+y)*W+left:(top+y)*W+left+w]
    if scale and scale<1:
        nw=int(w*scale); nh=int(h*scale)
        s=bytearray(nw*nh)
        for y in range(nh):
            sy=int(y/scale)
            for x in range(nw):
                s[y*nw+x]=c[sy*w+int(x/scale)]
        w,h,c = nw,nh,s
    save_gray(out,w,h,c)
    return w,h

def rowprofile(src, thresh=140):
    W,H,g = load_gray(src)
    prof=[]
    for y in range(H):
        row=g[y*W:(y+1)*W]
        prof.append(sum(1 for v in row if v<thresh))
    return W,H,prof

if __name__=='__main__':
    a=sys.argv[1:]
    if a[0]=='prof':
        W,H,p = rowprofile(a[1])
        print(W,H)
        # 100行ごとの平均
        for y in range(0,H,100):
            print(y, sum(p[y:y+100])//100)
    else:
        src,out,top,left,h,w = a[0],a[1],int(a[2]),int(a[3]),int(a[4]),int(a[5])
        sc = float(a[6]) if len(a)>6 else None
        print(crop(src,out,top,left,h,w,sc))
