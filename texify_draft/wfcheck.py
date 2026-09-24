# -*- coding: utf-8 -*-
"""章ファイルの wrapfigure を検査する（組む前に走らせる）。

     python3 texify_draft/wfcheck.py physics_new18.tex

   図の実高は .xbb の HiResBoundingBox から  高さmm = 指定幅mm × bbH/bbW  で出す。
   jsarticle 10pt の \\baselineskip は実測 5.6mm。

   検査項目
     [1] [N] が図の実高より小さい      → 本文が図に重なる（臨界角の図で実際に発生）
     [2] 直前に \\bsNeed が無い/小さい  → ページ下端に落ちると紙面からはみ出す（ログに出ない）
                                        必要量 = 実高 − 16mm（下余白へ16mmまでの食い込みは許容）
     [3] \\bsNeed が \\subsection の後  → 見出しだけが前ページに取り残される
                                        \\subsection の前に置き，値に見出しの高さ14mmを足す
"""
import os, re, sys

BASELINE   = 5.6    # mm
MARGIN_OK  = 16.0   # 下余白への許容食い込み(mm)
SUBSEC_H   = 14.0   # \subsection 自身の高さ(mm)

def xbb_wh(img, base):
    for cand in (os.path.join(base, img),
                 os.path.join(base, 'fig', os.path.basename(img))):
        p = os.path.splitext(cand)[0] + '.xbb'
        if os.path.exists(p):
            m = re.search(r'%%HiResBoundingBox:\s*\S+\s+\S+\s+(\S+)\s+(\S+)', open(p).read())
            if m: return float(m.group(1)), float(m.group(2))
    return None

def main():
    if len(sys.argv) < 2: print(__doc__); return 1
    tex  = sys.argv[1]
    base = os.path.dirname(os.path.abspath(tex)) or '.'
    lines = open(tex, encoding='utf-8').read().split('\n')
    ng = 0
    print(f'{tex}\n')
    for i, l in enumerate(lines):
        m = re.match(r'^\s*\\begin\{wrapfigure\}\[(\d+)\]\{[rl]\}(?:\[[^\]]*\])?\{(\d+)mm\}\s*$', l)
        if not m: continue
        decl, wmm = int(m.group(1)), int(m.group(2))
        img = None
        for j in range(i, min(i+8, len(lines))):
            mm = re.search(r'\{([A-Za-z0-9_./-]+\.(?:png|pdf|jpg))\}', lines[j])
            if mm: img = mm.group(1); break
        d = xbb_wh(img, base) if img else None
        if not d:
            print(f'  行{i+1}: {img} の .xbb が見つからず判定不能'); ng += 1; continue
        hmm  = wmm * d[1] / d[0]
        need = -(-int(hmm*1000) // int(BASELINE*1000))     # ceil
        msgs = []
        if decl < need:
            msgs.append(f'[1] [{decl}] は不足。実高{hmm:.0f}mm には [{need}] が必要（本文が図に重なる）')
        # 直前の非空行をさかのぼって \bsNeed と \subsection を探す
        bs_val = bs_line = None; subsec_line = None
        k = i - 1
        while k >= 0 and i - k <= 8:
            t = lines[k].strip()
            if t and not t.startswith('%'):
                mb = re.match(r'\\bsNeed\{([\d.]+)mm\}', t)
                if mb and bs_val is None: bs_val, bs_line = float(mb.group(1)), k
                if t.startswith('\\subsection') and subsec_line is None: subsec_line = k
                if not mb and not t.startswith('\\subsection'): break
            k -= 1
        want = max(0.0, hmm - MARGIN_OK)
        if bs_val is None:
            msgs.append(f'[2] 直前に \\bsNeed が無い。\\bsNeed{{{want:.0f}mm}} を入れる')
        elif bs_val < want - 0.5:
            msgs.append(f'[2] \\bsNeed{{{bs_val:.0f}mm}} は不足。{want:.0f}mm 以上にする')
        if subsec_line is not None and bs_line is not None and bs_line > subsec_line:
            msgs.append(f'[3] \\bsNeed が \\subsection（行{subsec_line+1}）の後ろにある。'
                        f'前へ移し，値を {want+SUBSEC_H:.0f}mm にする（見出しの取り残し防止）')
        tag = 'OK ' if not msgs else 'NG '
        print(f'  {tag}行{i+1:>5}  幅{wmm}mm 実高{hmm:5.1f}mm  [{decl}]（必要[{need}]）  {os.path.basename(img)}')
        for s in msgs: print(f'         → {s}'); 
        ng += len(msgs)
    print(f'\n指摘 {ng} 件' if ng else '\n指摘なし')
    return 0

if __name__ == '__main__':
    sys.exit(main())
