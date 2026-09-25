# -*- coding: utf-8 -*-
# 新第32回の例題の図を TikZ／circuitikz で自作する（原本の講義編の図はこの環境に無いため描き起こし）。
#   n32_ex40_zu / ex41_zu / ex42_zu … 例題40〜42（原本43〜45）RL / RC / RLC 直列回路
#   n32_ex40_ans / ex41_ans / ex42_ans … 各例題の電流・電圧のベクトル図（解答）
#   n32_ex43_zu / ex43_graph … 例題43（原本46）複雑な交流回路と V_BC のグラフ（OCR から再構成）
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tikzfig import run

FIGS = {}

def series(els):
    s = r"\draw (0,0) to[sV,l=$V(t)$] (0,2.0) -- (%.1f,2.0) -- (%.1f,0)" % (1.8*len(els), 1.8*len(els))
    x = 1.8*len(els)
    for e, lab in els:
        s += r" to[%s,l_=$%s$] (%.1f,0)" % (e, lab, x-1.8)
        x -= 1.8
    s += ";\n"
    s += r"\draw[cur] (0.9,2.35) -- (2.0,2.35); \node[above] at (1.45,2.35) {$I(t)$};" + "\n"
    s += r"\node[left] at (-0.5,1.9) {$+$}; \node[left] at (-0.5,0.1) {$-$};" + "\n"
    return s
FIGS['n32_ex40_zu'] = series([('L','L'),('R','R')])
FIGS['n32_ex41_zu'] = series([('C','C'),('R','R')])
FIGS['n32_ex42_zu'] = series([('C','C'),('L','L'),('R','R')])

VEC = r"""
\draw[ax] (-2.2,0) -- (3.2,0); \draw[ax] (0,-1.6) -- (0,3.0);
\node[below left] at (0,0) {O};
\draw[frc,gray] (0,0) -- (1.6,0.75); \node[below right,gray] at (1.6,0.75) {$\overrightarrow{I}$};
\draw (0.9,0) arc (0:25:0.9); \node at (1.15,0.2) {\small$\omega t-\varphi$};
%s
"""
# 電流の方向ベクトル (cos25, sin25)=(0.906,0.423)，垂直 (-0.423,0.906)
FIGS['n32_ex40_ans'] = VEC % r"""
\draw[frc] (0,0) -- (2.4,1.12); \node[below right] at (2.4,1.1) {$RI_0$};
\draw[frc] (0,0) -- (-0.8,1.72); \node[left] at (-0.8,1.72) {$\omega LI_0$};
\draw[gd] (2.4,1.12) -- (1.6,2.84) -- (-0.8,1.72);
\draw[frc,line width=1.4pt] (0,0) -- (1.6,2.84); \node[above] at (1.6,2.84) {$V_0$};
\draw (0.6,1.06) arc (60.6:25:1.22); \node at (1.25,1.25) {$\varphi$};
"""
FIGS['n32_ex41_ans'] = VEC % r"""
\draw[frc] (0,0) -- (2.4,1.12); \node[above right] at (2.4,1.1) {$RI_0$};
\draw[frc] (0,0) -- (0.8,-1.72); \node[left] at (0.7,-1.72) {$\dfrac{I_0}{\omega C}$};
\draw[gd] (2.4,1.12) -- (3.2,-0.6) -- (0.8,-1.72);
\draw[frc,line width=1.4pt] (0,0) -- (3.2,-0.6); \node[right] at (3.2,-0.6) {$V_0$};
"""
FIGS['n32_ex42_ans'] = VEC % r"""
\draw[frc] (0,0) -- (2.4,1.12); \node[below right] at (2.4,1.1) {$RI_0$};
\draw[frc] (0,0) -- (-1.1,2.36); \node[left] at (-1.1,2.36) {$\omega LI_0$};
\draw[frc] (0,0) -- (0.5,-1.07); \node[left] at (0.45,-1.1) {$\dfrac{I_0}{\omega C}$};
\draw[gd] (0,0) -- (-0.6,1.29) -- (1.8,2.41) -- (2.4,1.12);
\draw[frc,line width=1.4pt] (0,0) -- (1.8,2.41); \node[above] at (1.8,2.41) {$V_0$};
\node[font=\small,anchor=east] at (3.3,-1.35) {（$\omega L>\dfrac{1}{\omega C}$ の場合）};
"""

FIGS['n32_ex43_zu'] = r"""
\draw (0,2.4) node[circ]{} node[above]{A} to[R,l=$R$] (2.4,2.4) node[circ]{} node[above]{B} -- (3.2,2.4);
\draw (3.2,2.4) -- (3.2,3.1) to[L,l=$L$] (5.4,3.1) -- (5.4,2.4);
\draw (3.2,2.4) -- (3.2,1.7) to[C,l_=$C$] (5.4,1.7) -- (5.4,2.4) -- (6.2,2.4) node[circ]{} node[above]{C};
\draw (6.2,2.4) -- (6.2,0) -- (3.4,0) node[circ]{} node[below]{D};
\draw (0,2.4) -- (0,0) to[sV] (3.4,0);
"""
FIGS['n32_ex43_graph'] = r"""
\draw[ax] (0,0) -- (5.2,0) node[right]{$t\U{s}$}; \draw[ax] (0,-1.5) -- (0,1.7) node[above]{$V_{\mathrm{BC}}\U{V}$};
\node[below left] at (0,0) {O};
\draw[gd] (0,1.2) -- (4.8,1.2); \draw[gd] (0,-1.2) -- (4.8,-1.2);
\node[left] at (0,1.2) {$12$}; \node[left] at (0,-1.2) {$-12$};
\draw[line width=1.1pt] plot[domain=0:4.8,samples=80] (\x,{1.2*sin(\x*75)});
\draw[gd] (4.8,0) -- (4.8,-0.05); \node[below] at (4.8,0) {$\dfrac{1}{60}$};
\node[below] at (2.4,0) {$\dfrac{1}{120}$};
"""

if __name__ == '__main__':
    run(FIGS, sys.argv[1:])
