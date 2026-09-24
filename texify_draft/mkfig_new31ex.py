# -*- coding: utf-8 -*-
# 新第31回の例題の図を TikZ／circuitikz で自作する（原本の講義編の図はこの環境に無いため描き起こし）。
#   n31_ex35_zu … 例題35（原本36）コイルを含む直流回路（S1 と S2）
#   n31_ex36_zu … 例題36（原本39）電気振動（スイッチ a/b）
#   n31_ex37_zu / ex38_zu / ex39_zu … 例題37〜39（原本40〜42）交流電源と R / L / C
#   n31_ex36_ans / _blank … 例題36(6)(7) Q(t), I(t) のグラフ
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tikzfig import run

FIGS = {}

FIGS['n31_ex35_zu'] = r"""
\draw (0,0) to[battery1,l=$V$] (0,2.0) to[nos,l=$\mathrm{S}_1$] (1.6,2.0) -- (1.6,2.0) to[R,l=$R$] (3.6,2.0) to[L,l=$L$] (5.6,2.0) -- (5.6,0) -- (0,0);
\draw (1.6,2.0) node[circ]{} -- (1.6,0.9) to[nos,l_=$\mathrm{S}_2$] (1.6,0) node[circ]{};
\draw[cur] (5.9,1.6) -- (5.9,0.6); \node[right] at (5.9,1.1) {$I$};
"""

FIGS['n31_ex36_zu'] = r"""
\draw (0,0) to[battery1,l=$V$] (0,2.2) -- (1.2,2.2) node[circ]{} node[above]{a};
\draw (2.0,2.2) node[circ]{} node[above]{b} -- (3.6,2.2) to[L,l=$L$] (3.6,0) -- (0,0);
\draw (1.6,1.5) node[circ]{} -- (1.25,2.12); \node[left] at (1.5,1.55) {$\mathrm{S}$};
\draw (1.6,1.5) -- (1.6,1.3) to[C,l_=$C$] (1.6,0);
\node[circ] at (1.6,0) {};
"""

def ac(el, lab):
    return r"""
\draw (0,0) to[sV,l=$V(t)$] (0,2.0) -- (2.6,2.0) to[%s,l=$%s$] (2.6,0) -- (0,0);
\draw[cur] (0.8,2.35) -- (1.8,2.35); \node[above] at (1.3,2.35) {$I(t)$};
\node[left] at (-0.5,1.9) {$+$}; \node[left] at (-0.5,0.1) {$-$};
""" % (el, lab)
FIGS['n31_ex37_zu'] = ac('R', 'R')
FIGS['n31_ex38_zu'] = ac('L', 'L')
FIGS['n31_ex39_zu'] = ac('C', 'C')

GR36 = r"""
\begin{scope}
\draw[ax] (0,0) -- (5.3,0) node[right]{$t$}; \draw[ax] (0,-1.3) -- (0,1.5) node[above]{$Q$};
\node[below left] at (0,0) {O};
\draw[gd] (0,1.0) -- (4.8,1.0); \draw[gd] (0,-1.0) -- (4.8,-1.0);
\node[left] at (0,1.0) {$CV$}; \node[left] at (0,-1.0) {$-CV$};
\draw[line width=1.1pt%s] plot[domain=0:4.8,samples=80] (\x,{cos(\x*75)});
\draw[gd] (4.8,0) -- (4.8,1.0); \node[below] at (4.8,0) {$T$};
\end{scope}
\begin{scope}[yshift=-3.3cm]
\draw[ax] (0,0) -- (5.3,0) node[right]{$t$}; \draw[ax] (0,-1.3) -- (0,1.5) node[above]{$I$};
\node[below left] at (0,0) {O};
\draw[gd] (0,1.0) -- (4.8,1.0); \draw[gd] (0,-1.0) -- (4.8,-1.0);
\node[left] at (0,1.0) {$\dfrac{V\sqrt{C}}{\sqrt{L}}$}; \node[left] at (0,-1.0) {$-\dfrac{V\sqrt{C}}{\sqrt{L}}$};
\draw[line width=1.1pt%s] plot[domain=0:4.8,samples=80] (\x,{sin(\x*75)});
\node[below] at (4.8,0) {$T$};
\end{scope}
"""
FIGS['n31_ex36_ans'] = GR36 % ('', '')
FIGS['n31_ex36_ans_blank'] = GR36 % (',opacity=0', ',opacity=0')

if __name__ == '__main__':
    run(FIGS, sys.argv[1:])
