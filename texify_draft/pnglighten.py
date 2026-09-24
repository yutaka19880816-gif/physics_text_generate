# -*- coding: utf-8 -*-
"""原本スキャンの網点（ハーフトーン）の図を，文字が読めるように明るくする。
   PIL / numpy / ImageMagick が無い環境用の純Python実装。

なぜ2段階なのか
---------------
網点は「黒い点」と「白い地」の2値でできている。そのままガンマ補正をかけても
0→0，255→255 で何も変わらない。先に**近傍を平均して連続階調のグレーに直し**，
そのうえで**ガンマで持ち上げる**必要がある。

  1. box 平均（半径 r）  … 網点 → 濃度に応じたグレー
  2. ガンマ γ<1         … グレーを明るくする。真っ黒(0)は0のままなので
                          線画や文字の芯は黒く残り，塗りだけが薄くなる

使い方
------
  python3 pnglighten.py --blur 1 --gamma 0.55 in.png out.png
  python3 pnglighten.py --blur 1 --gamma 0.55 --floor 40 in.png out.png

  --floor N  … 平均後の値が N 未満（＝ベタに近い線・文字）はガンマをかけず
               そのまま黒く残す。文字を黒いまま塗りだけ薄くしたいときに使う。

出力は8bitグレースケールPNG。使う前に extractbb で .xbb を作り直すこと
（.xbb が無いと dvipdfmx が画像を埋め込まず，図が消える）。
"""
import zlib, struct, sys, os
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from imgpath import resolve   # 画像は img/scan・img/text に移動（2026-09-05）

# ---------------------------------------------------------------- 読み込み
def decode(path):
    """8bit の RGB(2)/RGBA(6)/Gray(0)/GrayA(4) PNG を (w,h,bpp,rows) で返す"""
    d = open(resolve(path), 'rb').read()
    assert d[:8] == b'\x89PNG\r\n\x1a\n', path
    pos = 8; w = h = bd = ct = None; idat = []
    while pos < len(d):
        ln = struct.unpack('>I', d[pos:pos+4])[0]; typ = d[pos+4:pos+8]
        if typ == b'IHDR':
            w, h, bd, ct, comp, filt, inter = struct.unpack('>IIBBBBB', d[pos+8:pos+21])
            assert bd == 8 and inter == 0, (bd, inter)
        elif typ == b'IDAT':
            idat.append(d[pos+8:pos+8+ln])
        elif typ == b'IEND':
            break
        pos += 12 + ln
    raw = zlib.decompress(b''.join(idat))
    bpp = {0: 1, 2: 3, 4: 2, 6: 4}[ct]
    stride = w * bpp
    out = []; prev = bytearray(stride); off = 0
    for _ in range(h):
        f = raw[off]; off += 1
        line = bytearray(raw[off:off+stride]); off += stride
        if f == 1:
            for x in range(bpp, stride): line[x] = (line[x] + line[x-bpp]) & 255
        elif f == 2:
            for x in range(stride): line[x] = (line[x] + prev[x]) & 255
        elif f == 3:
            for x in range(stride):
                a = line[x-bpp] if x >= bpp else 0
                line[x] = (line[x] + ((a + prev[x]) >> 1)) & 255
        elif f == 4:
            for x in range(stride):
                a = line[x-bpp] if x >= bpp else 0
                b = prev[x]; c = prev[x-bpp] if x >= bpp else 0
                p = a + b - c; pa, pb, pc = abs(p-a), abs(p-b), abs(p-c)
                pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                line[x] = (line[x] + pr) & 255
        out.append(bytes(line)); prev = line
    return w, h, bpp, out

# ---------------------------------------------------------------- 書き出し
def write_gray(path, w, h, rows):
    """8bit グレースケール(type 0) PNG を書く。各行の先頭にフィルタ0を置くだけ。"""
    raw = bytearray()
    for r in rows:
        raw.append(0); raw += r
    def chunk(typ, data):
        c = struct.pack('>I', len(data)) + typ + data
        return c + struct.pack('>I', zlib.crc32(typ + data) & 0xffffffff)
    png = b'\x89PNG\r\n\x1a\n'
    png += chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 0, 0, 0, 0))
    png += chunk(b'IDAT', zlib.compress(bytes(raw), 9))
    png += chunk(b'IEND', b'')
    open(path, 'wb').write(png)

# ---------------------------------------------------------------- 本体
def lighten(src, dst, blur=1, gamma=0.55, floor=0):
    w, h, bpp, rows = decode(src)
    # まずグレー1chに落とす（RGB でも実質グレーなので先頭成分でよい）
    g = [bytearray(r[i*bpp] for i in range(w)) for r in rows]

    # 1) box 平均で網点を連続階調に直す
    if blur > 0:
        k = blur
        # 横方向
        tmp = []
        for r in g:
            o = bytearray(w)
            acc = sum(r[0:k+1]) + r[0]*k
            n = 2*k + 1
            for x in range(w):
                o[x] = acc // n
                left = r[max(x-k, 0)]
                right = r[min(x+k+1, w-1)]
                acc += right - left
            tmp.append(o)
        # 縦方向
        out = []
        for y in range(h):
            o = bytearray(w)
            for x in range(w):
                s = 0
                for dy in range(-k, k+1):
                    s += tmp[min(max(y+dy, 0), h-1)][x]
                o[x] = s // (2*k + 1)
            out.append(o)
        g = out

    # 2) ガンマで持ち上げる（0 は 0 のまま＝線画の芯は黒く残る）
    lut = bytearray(256)
    for v in range(256):
        if v < floor:
            lut[v] = v                      # ベタに近い部分はそのまま黒く残す
        else:
            lut[v] = min(255, int(255.0 * (v / 255.0) ** gamma + 0.5))
    g = [bytearray(lut[v] for v in r) for r in g]

    write_gray(dst, w, h, g)
    return w, h

if __name__ == '__main__':
    a = sys.argv[1:]
    blur, gamma, floor = 1, 0.55, 0
    while a and a[0].startswith('--'):
        k = a.pop(0)
        if k == '--blur':   blur = int(a.pop(0))
        elif k == '--gamma': gamma = float(a.pop(0))
        elif k == '--floor': floor = int(a.pop(0))
        else: sys.exit('不明なオプション: ' + k)
    src, dst = a
    w, h = lighten(src, dst, blur, gamma, floor)
    print('%s → %s  (%dx%d, blur=%d, gamma=%.2f, floor=%d, %d B)'
          % (src, dst, w, h, blur, gamma, floor, os.path.getsize(dst)))
