# -*- coding: utf-8 -*-
# 新第24回（静電気力・電場・電位）で必要な図をすべて作る。
#   座標は texify_draft/jobs_new24.py。切り出しの実体は mkfig_new16.make（純Python）。
#   使い方:  python3 texify_draft/mkfig_new24.py            … 全部
#            python3 texify_draft/mkfig_new24.py p44 a46    … 名前に含む図だけ
#            python3 texify_draft/mkfig_new24.py --halftone … 網点処理だけやり直す
#   ※ .xbb は必ず消してから extractbb する（組版チェックリスト §1.5）。
import sys, os, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from mkfig_new16 import make
from mkfig_new20 import area_down, lighten

ROOT   = '/Users/yutaka/Documents/入試物理基礎演習'
SRCPDF = '/Users/yutaka/Google Drive/マイドライブ/鉄緑会物理/20161215144626.pdf'
TMPD   = ('/private/tmp/claude-501/-Users-yutaka-Documents-Claude-Code----math-tex-tool/'
          '59bca349-8945-456d-922e-8c5753c43468/scratchpad/hi')
DPI    = 600

def render(pg):
    """講義編PDFの1ページを 600dpi の PNG にする（見開き1枚＝原本2ページ分）。"""
    out = '%s/pdf%d.png' % (TMPD, pg)
    if not os.path.exists(out):
        os.makedirs(TMPD, exist_ok=True)
        subprocess.run(['gs', '-q', '-dNOPAUSE', '-dBATCH', '-sDEVICE=pnggray',
                        '-r%d' % DPI, '-dFirstPage=%d' % pg, '-dLastPage=%d' % pg,
                        '-sOutputFile=' + out, SRCPDF], check=True)
    return out

def remake_xbb(png):
    xbb = png[:-4] + '.xbb'
    if os.path.exists(xbb): os.remove(xbb)
    subprocess.run(['extractbb', png], check=True)

if __name__ == '__main__':
    os.chdir(ROOT)
    args   = sys.argv[1:]
    only_ht = '--halftone' in args
    only   = [a for a in args if not a.startswith('--')] or None
    from jobs_new24 import pdf_jobs, jobs, text_jobs, widths, halftone
    hits = lambda out: (not only) or any(k in out for k in only)

    if not only_ht:
        for pg, out, top, left, h, w in pdf_jobs:
            if hits(out): make(render(pg), out, top, left, h, w, margin=18)
        for j in jobs:
            src, out, top, left, h, w = j[:6]
            mg = j[6] if len(j) > 6 else 16      # 本文が近い図は margin を小さくする
            if hits(out): make(src, out, top, left, h, w, margin=mg)
        # 講義編の既存の図は原本を書き換えず fig/ にコピーしてから処理する
        for src, out, win in text_jobs:
            if not hits(out): continue
            if win is None:
                subprocess.run(['cp', 'img/text/' + src, out], check=True)
                print('  %-26s コピー' % os.path.basename(out))
            else:
                make('img/text/' + src, out, *win, margin=10)

    ht = dict((n, (g, b)) for n, g, b in halftone)
    for name, mm in sorted(widths.items()):
        out = 'fig/%s.png' % name
        if not hits(out) or not os.path.exists(out): continue
        if name in ht:
            g, b = ht[name]
            lighten(out, mm, gamma=g, blur=b, floor=0, no_recut=only_ht)
        else:
            target = int(round(mm / 25.4 * 360))       # 360dpi 相当
            area_down(out, out, target)
        remake_xbb(out)
    print('完了')
