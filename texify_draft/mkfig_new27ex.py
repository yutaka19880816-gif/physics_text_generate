# -*- coding: utf-8 -*-
# 新第27回の例題の図を TikZ／circuitikz で自作する（原本の講義編の図はこの環境に無いため描き起こし）。
#     n27_ex16_zu        … 例題16（原本17）3本の枝をもつ回路
#     n27_ex17_zu2       … 例題17(2)（原本20）メートルブリッジ
#     n27_ex18_zu        … 例題18（原本21）RC 直列回路
#     n27_ex18_ans / _blank … 例題18(5) Q-t グラフ（\AnaFig 用の補助図は曲線を opacity=0）
#     n27_ex19_zu        … 例題19（原本22）抵抗・コンデンサー複合回路（OCR から回路を再構成）
#     n27_ex20_zu / _graph … 例題20（原本23）豆電球と抵抗，豆電球の I-V 特性
#     n27_ex20_ans       … 例題20(3) 特性曲線と直線の交点
#   使い方:  python3 texify_draft/mkfig_new27ex.py [名前の一部…]
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tikzfig import run

FIGS = {}

FIGS['n27_ex16_zu'] = r"""
\draw (0,0) to[battery1,l=$E_1$] (0,1.6) to[R,l=$R_1$] (0,3.4) -- (2.2,3.4) node[circ]{} node[above]{A} -- (4.4,3.4)
      to[R,l_=$R_2$] (4.4,1.6) to[battery1,l_=$E_2$] (4.4,0) -- (2.2,0) node[circ]{} node[below]{B} -- (0,0);
\draw (2.2,3.4) to[R,l=$R_3$] (2.2,0);
"""

FIGS['n27_ex17_zu2'] = r"""
\fill[gray!55] (0,0) rectangle (5,0.16); \draw[line width=0.6pt] (0,0) rectangle (5,0.16);
\node[above left] at (-0.3,0.08) {A}; \node[above right] at (5.3,0.08) {B};
\draw (0,0.08) -- (-0.3,0.08) -- (-0.3,1.6) to[R,l=$R_0$] (2.5,1.6) to[R,l=$R$] (5.3,1.6) -- (5.3,0.08) -- (5,0.08);
\draw (2.5,1.6) -- (2.5,1.25) node[draw,circle,fill=white,inner sep=1.2pt,anchor=north]{\small G};
\draw[-{Latex[length=2mm]}] (2.5,0.78) .. controls (2.5,0.5) and (1.9,0.55) .. (1.9,0.2);
\node[below right] at (1.9,0.0) {C};
\draw[gd] (0,0) -- (0,-0.95); \draw[gd] (1.9,0) -- (1.9,-0.95); \draw[gd] (5,0) -- (5,-0.95);
\draw[dim] (0,-0.85) -- (1.9,-0.85); \node[lab] at (0.95,-0.85) {$l_1$};
\draw[dim] (1.9,-0.85) -- (5,-0.85); \node[lab] at (3.45,-0.85) {$l_2$};
\draw (-0.3,0.08) -- (-0.3,-1.5) to[battery1,l_=$E$] (5.3,-1.5) -- (5.3,0.08);
"""

FIGS['n27_ex18_zu'] = r"""
\draw (0,0) to[R,l=$R$] (2.4,0) to[C,l=$C$] (4.2,0) -- (4.2,-1.8) to[battery1,l=$V$,invert] (2.1,-1.8) to[nos,l=$\mathrm{S}$] (0,-1.8) -- (0,0);
"""

GR18 = r"""
\draw[ax] (0,0) -- (5.2,0) node[right]{$t$};
\draw[ax] (0,0) -- (0,2.9) node[above]{$Q$};
\node[below left] at (0,0) {O};
\draw[gd] (0,2.2) -- (5.0,2.2); \node[left] at (0,2.2) {$CV$};
\draw[line width=1.1pt%s] plot[domain=0:4.9,samples=60] (\x,{2.2*(1-exp(-\x/1.0))});
\draw[gd%s] (0,0) -- (1.0,2.2);
\node[font=\small,anchor=west%s] at (1.35,0.75) {傾き$I_0=\dfrac{V}{R}$};
"""
FIGS['n27_ex18_ans'] = GR18 % ('', '', '')
FIGS['n27_ex18_ans_blank'] = GR18 % (',opacity=0', ',opacity=0', ',opacity=0')

FIGS['n27_ex19_zu'] = r"""
\draw (0,0) to[battery1,l=$E$] (0,4) -- (5.4,4);
\draw (2,4) to[R,l_=$R_1$] (2,2) node[circ]{} node[left]{B} to[C,l_=$C_1$] (2,0);
\draw (2,2) -- (3.3,2) node[circ]{} to[C,l=$C_2$] (5.4,2) node[circ]{} node[right]{D};
\draw (3.3,2) to[nos,l=$\mathrm{S}_1$] (3.3,1.1) to[R,l=$R_2$] (3.3,0);
\draw (5.4,4) to[nos,l=$\mathrm{S}_2$] (5.4,3.1) to[R,l=$R_3$] (5.4,2) to[R,l=$R_4$] (5.4,0) -- (0,0);
\node[circ] at (0,0) {}; \node[below left] at (0,0) {A};
\draw (0,0) -- (0,-0.3) node[ground]{};
"""

GR20 = r"""
\begin{scope}[xscale=0.5,yscale=8]
\foreach \x in {1,...,10} \draw[gd] (\x,0) -- (\x,0.5);
\foreach \y in {0.1,0.2,0.3,0.4,0.5} \draw[gd] (0,\y) -- (10,\y);
\draw[line width=0.6pt] (0,0) rectangle (10,0.5);
\foreach \x in {2,4,6,8,10} \node[below,font=\small] at (\x,0) {$\x$};
\foreach \y in {0.1,0.2,0.3,0.4,0.5} \node[left,font=\small] at (0,\y) {$\y$};
\node[below left,font=\small] at (0,0) {O};
\node[font=\small] at (8.6,-0.075) {$V\U{V}$};
\node[font=\small,anchor=south west] at (-1.6,0.515) {$I\U{A}$};
\draw[line width=1.1pt] plot[domain=0:10,samples=60] (\x,{0.2*pow(\x/2,0.55)});
%s
\end{scope}
"""
FIGS['n27_ex20_graph'] = GR20 % ''
FIGS['n27_ex20_ans'] = GR20 % r"""\draw[line width=0.8pt,dash pattern=on 3pt off 2pt] (0,0.4) -- (4,0);
\fill (2,0.2) circle (0.06 and 0.004);
\draw[gd] (2,0) -- (2,0.2) -- (0,0.2);
\node[font=\small,anchor=west,lab] at (3.3,0.13) {$I=0.4-\dfrac{V}{10}$};"""

FIGS['n27_ex20_zu'] = r"""
\draw (0,0) node[ocirc]{} node[left]{P} to[R,l=$30\,\Omega$] (2.6,0) -- (2.6,0.8) to[lamp,l=豆電球] (4.8,0.8) -- (4.8,0) -- (5.6,0) node[ocirc]{} node[right]{Q};
\draw (2.6,0) -- (2.6,-0.8) to[R,l_=$15\,\Omega$] (4.8,-0.8) -- (4.8,0);
\draw[dim] (0,-1.5) -- (5.6,-1.5); \node[lab] at (2.8,-1.5) {$12\U{V}$};
"""

if __name__ == '__main__':
    run(FIGS, sys.argv[1:])
