# -*- coding: utf-8 -*-
# 新第26回の例題の図を TikZ／circuitikz で自作する。
#   原本の講義編（第2冊 20161215144626.pdf）はこの作業環境に無く，Google Drive からは
#   OCR テキストしか取れなかった（2026-09-24）。例題の問題文は OCR から復元し，図は描き起こした。
#     n26_ex12_zu   … 例題12（原本の例題15）抵抗モデル：導線と電池
#     n26_ex13_zu   … 例題13（原本の例題18）合成抵抗：R1 と（R2∥R3）
#     n26_ex14_zu   … 例題14（原本の例題16）内部抵抗：A,B,C,D と接地
#     n26_ex15_ans1 … 例題15(1) 分流器（解答の図）
#     n26_ex15_ans2 … 例題15(3) 倍率器（解答の図）
#     n26_ex14_ans  … 例題14(2) 電位の変化（解答の図）
#   使い方:  python3 texify_draft/mkfig_new26ex.py [名前の一部…]
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tikzfig import run

FIGS = {}

FIGS['n26_ex12_zu'] = r"""
% 導線（円柱）
\draw[line width=0.8pt] (0,0) ellipse (0.25 and 0.55);
\draw[line width=0.8pt] (0,0.55) -- (4.2,0.55);
\draw[line width=0.8pt] (0,-0.55) -- (4.2,-0.55);
\draw[line width=0.8pt] (4.2,-0.55) arc (-90:90:0.25 and 0.55);
\draw[gd] (4.2,0.55) arc (90:270:0.25 and 0.55);
\node at (-0.55,0.75) {$S$};
\draw[line width=0.4pt] (-0.35,0.6) -- (-0.12,0.3);
% 電場と電子
\draw[frc] (1.0,0.18) -- (2.4,0.18) node[right] {$E$};
\draw[line width=0.6pt,fill=white] (3.0,-0.22) circle (0.1);
\draw[frc] (2.85,-0.22) -- (1.85,-0.22);
\node[font=\small,anchor=west] at (3.1,-0.22) {電子};
% 長さ
\draw[dim] (0,-0.95) -- (4.2,-0.95); \node[lab] at (2.1,-0.95) {$l$};
% 電池
\draw[line width=0.8pt] (-0.25,0) -- (-0.8,0) -- (-0.8,-1.9) -- (1.6,-1.9);
\draw[line width=0.8pt] (4.45,0) -- (5.0,0) -- (5.0,-1.9) -- (2.6,-1.9);
\draw[line width=0.8pt] (1.6,-1.9) to[battery1] (2.6,-1.9);
\node at (2.1,-2.45) {$V$};
"""

FIGS['n26_ex13_zu'] = r"""
\draw (0,0) node[circ]{} node[left]{a} to[R,l=$R_1$] (2.4,0) -- (2.4,0.7) to[R,l=$R_2$] (4.4,0.7) -- (4.4,0);
\draw (2.4,0) -- (2.4,-0.7) to[R,l_=$R_3$] (4.4,-0.7) -- (4.4,0) -- (5.2,0) node[circ]{} node[right]{b};
\draw (0,0) -- (0,-2.0) to[battery1,l_=$E$] (5.2,-2.0) -- (5.2,0);
"""

FIGS['n26_ex14_zu'] = r"""
% D（接地）→起電力→A→内部抵抗→B→R1→C→R2→D
\draw (0,0) to[battery1,invert,l=$E$] (0,1.6) node[circ]{} node[left]{A}
      to[R,l=$r$] (0,3.4) node[circ]{} node[left]{B} -- (1.6,3.4) to[R,l=$R_1$] (3.8,3.4)
      node[circ]{} node[above]{C} -- (4.6,3.4) to[R,l=$R_2$] (4.6,0) -- (0,0) node[circ]{} node[below]{D};
\draw (2.3,0) node[ground]{};
\draw[gd,line width=0.5pt] (-1.05,0.3) rectangle (0.6,2.95);
\node[font=\small,anchor=east] at (-1.1,2.7) {電池};
"""

FIGS['n26_ex14_ans'] = r"""
\draw[ax] (0,0) -- (6.4,0) node[right] {位置};
\draw[ax] (0,0) -- (0,3.3) node[above] {電位};
\draw[line width=1.0pt] (0.3,0) -- (0.3,2.8) -- (1.3,2.5) -- (3.3,1.2) -- (5.6,0);
\foreach \x/\t in {0.3/D,0.3/A,1.3/B,3.3/C,5.6/D} {}
\draw[gd] (0.3,2.8) -- (0,2.8) node[left] {$E$};
\draw[gd] (1.3,2.5) -- (1.3,0); \draw[gd] (3.3,1.2) -- (3.3,0);
\node[below] at (0.3,0) {D\,A}; \node[below] at (1.3,0) {B}; \node[below] at (3.3,0) {C}; \node[below] at (5.6,0) {D};
\node[font=\small,anchor=west] at (0.45,3.05) {$rI$ だけ下がる};
\node[font=\small] at (2.6,2.25) {$R_1I$};
\node[font=\small] at (4.75,0.95) {$R_2I$};
"""

FIGS['n26_ex15_ans1'] = r"""
\draw (0,0) node[circ]{} -- (0.6,0) -- (0.6,0.7) to[R,l=$1.8\,\Omega$] (2.6,0.7) -- (3.3,0.7) node[draw,circle,fill=white,inner sep=1.6pt]{\small M} -- (3.9,0.7) -- (3.9,0) -- (4.5,0) node[circ]{};
\draw (0.6,0) -- (0.6,-0.8) to[R,l_=$R_{\mathrm{s}}$] (3.9,-0.8) -- (3.9,0);
\draw[cur] (-0.6,0) -- (-0.05,0); \node[above] at (-0.4,0) {$I$};
\draw[cur] (1.1,0.35) -- (2.1,0.35); \node[right] at (2.1,0.35) {$i$};
\draw[cur] (1.1,-0.42) -- (2.1,-0.42); \node[right] at (2.1,-0.42) {$I-i$};
\draw[gd,line width=0.5pt] (0.4,0.2) rectangle (4.1,1.45);
\node[font=\small,anchor=west] at (4.15,1.3) {元の電流計};
"""

FIGS['n26_ex15_ans2'] = r"""
\draw (0,0) node[circ]{} to[R,l=$5.0\,\mathrm{k}\Omega$] (2.2,0) -- (2.8,0) node[draw,circle,inner sep=1.6pt]{\small M} -- (3.4,0) to[R,l=$R_{\mathrm{m}}$] (5.6,0) node[circ]{};
\draw[gd,line width=0.5pt] (-0.25,-0.45) rectangle (3.55,0.9);
\node[font=\small] at (1.65,-0.75) {元の電圧計（$100\U{V}$まで）};
\draw[cur] (-0.7,0) -- (-0.1,0); \node[above] at (-0.5,0) {$i$};
"""

if __name__ == '__main__':
    run(FIGS, sys.argv[1:])
