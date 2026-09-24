# -*- coding: utf-8 -*-
# 第18回（光の屈折と光波の干渉）で新規に必要な図5枚の切り出し
import subprocess, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from pngtrim import ink_bbox
TMP = '/private/tmp/claude-501/-Users-yutaka-Documents-Claude-Code----math-tex-tool/3114164b-5b30-473b-9efe-12838b682091/scratchpad/tmpcrop18.png'
def sips(a): subprocess.run(['sips']+a, capture_output=True)
def make(src, out, top, left, h, w, margin=14):
    sips(['-c',str(h),str(w),'--cropOffset',str(top),str(left),src,'--out',TMP])
    b = ink_bbox(TMP)
    if b is None: print('  !! インクなし', out); return
    x0,y0,x1,y1,cw,ch = b
    L=max(0,left+x0-margin); T=max(0,top+y0-margin)
    W=(x1-x0+1)+2*margin;    H=(y1-y0+1)+2*margin
    sips(['-c',str(H),str(W),'--cropOffset',str(T),str(L),src,'--out',out])
    print(f'  {os.path.basename(out):26s} {W}x{H}px  {os.path.getsize(out)/1000:6.1f} KB  (left={L} top={T})')

jobs = [
 # 例題17 屈折の法則（旧練習[45]）：問題図と解答図
 ('prob_p62.png',  'fig/ch18_ex_refract.png',      140, 2560,  660, 1080),
 ('prob_p173.png', 'fig/ch18_ex_refract_ans.png',  500,  380,  720, 1180),
 # 練習［45］水中の光源を隠す円板の半径（旧[46]）：問題図と解答図
 ('prob_p62.png',  'fig/ch18_p45_disk.png',       1320, 2560,  640, 1080),
 ('prob_p173.png', 'fig/ch18_p45_disk_ans.png',    600, 1950,  880, 1560),
 # 練習［46］光ファイバーの原理（旧[47]）：問題図
 ('prob_p62.png',  'fig/ch18_p46_fiber.png',      2390, 2530,  820, 1110),
]
for j in jobs: make(*j)
