# -*- coding: utf-8 -*-
"""組み上がったPDFを「ページ画像のインク」で検査する。
   ログでは検出できない不具合（図の紙面はみ出し・wrapfig の折り返し持ち越し・過剰な余白）を拾う。

     python3 texify_draft/pagecheck.py 第18回のみ.pdf
     python3 texify_draft/pagecheck.py 第18回のみ.pdf --verbose

   判定基準（A4・本文領域 左25 / 右185 / 下272mm，ページ番号 288mm）:
     ・インク下端 > 290mm      → 図が紙面からはみ出している（Overfull は出ない）
     ・インク右端 > 191mm      → 右マージンを超えている（wrapfigure の overhang は190mmまで正常）
     ・上部の行の右端 < 175mm  → 前ページの wrapfigure の折り返しが持ち越され本文幅が狭い
     ・余白（272 − 本文の終わり）が25mm超のページを合計して紙面比を出す
"""
import os, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pnglighten

DPI = 72
PX  = DPI / 25.4
TEXT_RIGHT, TEXT_BOTTOM, FOLIO = 185.0, 272.0, 288.0

def render(pdf, page, out):
    subprocess.run(['gs','-q','-sDEVICE=pnggray',f'-r{DPI}',
                    f'-dFirstPage={page}',f'-dLastPage={page}',
                    '-dNOPAUSE','-dBATCH',f'-sOutputFile={out}',pdf], capture_output=True)

def npages(pdf):
    dvi = pdf[:-4] + '.dvi'
    if os.path.exists(dvi):
        r = subprocess.run(['dvipdfmx', dvi], capture_output=True, text=True)
        t = r.stderr + r.stdout
        if '[' in t:
            try: return int(t.rsplit('[',1)[1].split(']')[0])
            except Exception: pass
    n = 0
    with tempfile.TemporaryDirectory() as d:
        while n < 400:
            o = os.path.join(d, 'p.png'); render(pdf, n+1, o)
            if not os.path.exists(o) or os.path.getsize(o) == 0: break
            os.remove(o); n += 1
    return n

def dark_cols(row, bpp, w, step=3, thr=120):
    return sum(1 for x in range(0, w, step) if row[x*bpp] < thr)

def analyse(png):
    w,h,bpp,rows = pnglighten.decode(png)
    right = bottom = body_bottom = 0.0
    for y in range(h-1,-1,-1):
        if dark_cols(rows[y],bpp,w) >= 3:
            bottom = (y+1)/PX; break
    for y in range(h-1,-1,-1):
        if dark_cols(rows[y],bpp,w) >= 3 and (y+1)/PX < FOLIO-5:
            body_bottom = (y+1)/PX; break
    for y in range(h):
        r = rows[y]
        for x in range(w-1,-1,-1):
            if r[x*bpp] < 120:
                right = max(right,(x+1)/PX); break
    top_right = 0.0
    y = int(28*PX)
    while y < int(115*PX) and y < h:
        r = rows[y]
        for x in range(w-1,-1,-1):
            if r[x*bpp] < 120:
                top_right = max(top_right,(x+1)/PX); break
        y += 3
    return right, bottom, body_bottom, top_right

def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    verbose = '--verbose' in sys.argv
    if not args: print(__doc__); return 1
    pdf = args[0]
    if not os.path.exists(pdf): print('見つかりません:', pdf); return 1
    n = npages(pdf)
    print(f'{pdf}  {n}ページ\n')
    bad_over, bad_right, bad_narrow, gap_tot, gaps = [], [], [], 0.0, []
    with tempfile.TemporaryDirectory() as d:
        for p in range(1, n+1):
            o = os.path.join(d, f'{p}.png'); render(pdf, p, o)
            right, bottom, body, top_right = analyse(o)
            gap = TEXT_BOTTOM - body
            if bottom > 290: bad_over.append((p, round(bottom)))
            if right  > 191: bad_right.append((p, round(right)))
            if top_right and top_right < 175: bad_narrow.append((p, round(top_right)))
            if gap > 25: gap_tot += gap; gaps.append((p, round(gap)))
            if verbose:
                print(f'  p{p:>3}  右端{right:6.1f}  下端{bottom:6.1f}  本文終{body:6.1f}  上部右端{top_right:6.1f}')
    print('■ 紙面はみ出し（下端290mm超）  :', 'なし' if not bad_over  else bad_over)
    print('■ 右マージン超過（191mm超）    :', 'なし' if not bad_right else bad_right)
    print('■ 本文幅が狭いページ（<175mm） :', 'なし' if not bad_narrow else bad_narrow,
          '' if not bad_narrow else '← wrapfig の折り返しが持ち越された疑い')
    print(f'■ 余白（25mm超のページの合計） : {gap_tot:.0f}mm ＝ 紙面の {gap_tot/(TEXT_BOTTOM*n)*100:.0f}%')
    if gaps: print('   内訳:', gaps)
    print('\n（参考）元の archive/旧章単位の出力/第25章のみ.pdf は 17%。13%前後なら既存教材と同等。')
    return 0

if __name__ == '__main__':
    sys.exit(main())
