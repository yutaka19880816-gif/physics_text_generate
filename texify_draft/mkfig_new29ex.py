# -*- coding: utf-8 -*-
# 新第29回の例題・講義の図を TikZ で自作する（原本の講義編の図はこの環境に無いため描き起こし）。
#   n29_ex25_zu … 例題25（原本7）点電荷に近づく荷電粒子
#   n29_ex26_zu … 例題26（原本30）トムソンの実験（電場偏向）
#   n29_ex27_zu … 例題27（原本28）磁場中の半円運動
#   n29_ex28_zu … 例題28（原本29）らせん運動
#   n29_ex29_zu … 例題29（原本31）磁場偏向
#   n29_zu_sokudo … 29.5 速度選別器
#   n29_zu_hall   … 29.5 ホール効果
#   n29_zu_cyclo  … 29.5 サイクロトロン（上から見た図）
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tikzfig import run

FIGS = {}

FIGS['n29_ex25_zu'] = r"""
\draw[gd] (-0.5,0) -- (5.2,0);
\shade[ball color=gray!40] (0,0) circle (0.22); \node at (0,0) {\small $+$};
\node[below] at (0,-0.25) {O}; \node[above] at (0,0.25) {$+Ze$};
\fill (4.2,0) circle (0.09); \node[below] at (4.2,-0.12) {A}; \node[above] at (4.35,0.15) {$m,\ +q$};
\draw[frc] (4.1,0.0) -- (3.0,0.0); \node[above] at (3.3,0.02) {$v_0$};
\draw[dim] (0,-0.75) -- (4.2,-0.75); \node[lab] at (2.1,-0.75) {$r_0$};
"""

FIGS['n29_ex26_zu'] = r"""
\draw[line width=1.2pt] (0,1.0) -- (2.4,1.0); \node[left] at (0,1.0) {A};
\draw[line width=1.2pt] (0,-0.2) -- (2.4,-0.2); \node[left] at (0,-0.2) {B};
\foreach \x in {0.4,1.0,1.6,2.2} \draw[-{Latex[length=1.6mm]},line width=0.5pt] (\x,-0.15) -- (\x,0.95);
\node[right] at (2.45,0.75) {$E$};
\draw[ax] (-1.4,0.4) -- (6.8,0.4) node[right] {$x$};
\draw[line width=1.0pt] (6.2,-1.0) -- (6.2,2.4); \node[above] at (6.2,2.4) {スクリーン};
\draw[ax] (6.2,0.4) -- (6.2,2.0); \node[right] at (6.2,1.9) {$y$};
\node[below right] at (6.2,0.4) {O};
\draw[frc] (-1.4,0.4) -- (-0.6,0.4); \node[above] at (-1.0,0.45) {$v_0$};
\draw[line width=0.8pt,dash pattern=on 2pt off 1.5pt] (0,0.4) .. controls (1.4,0.4) and (2.0,0.2) .. (2.4,0.0) -- (6.2,-0.95);
\draw[gd] (0,1.6) -- (0,1.1); \draw[gd] (2.4,1.6) -- (2.4,1.1);
\draw[dim] (0,1.5) -- (2.4,1.5); \node[lab] at (1.2,1.5) {$l$ \small ①};
\draw[dim] (2.4,1.5) -- (6.2,1.5); \node[lab] at (4.3,1.5) {$L$ \small ②};
\node[font=\small] at (-1.0,-0.2) {電子};
"""

FIGS['n29_ex27_zu'] = r"""
\draw[eq] (-2.6,0) rectangle (2.6,-2.9);
\foreach \x in {-2.2,-1.4,...,2.2} \foreach \y in {-0.5,-1.3,-2.1} {\draw[line width=0.4pt] (\x,\y)+(-0.07,-0.07) -- +(0.07,0.07); \draw[line width=0.4pt] (\x,\y)+(-0.07,0.07) -- +(0.07,-0.07);}
\node[font=\small] at (2.1,-2.65) {$B$};
\draw[line width=1.2pt] (-2.6,0) -- (0.9,0); \draw[line width=1.2pt] (1.5,0) -- (2.6,0);
\draw[line width=1.2pt] (0.3,0.8) -- (0.9,0.8); \draw[line width=1.2pt] (1.5,0.8) -- (2.2,0.8);
\node[right] at (2.2,0.8) {$\mathrm{S}_1$}; \node[right] at (2.6,0.0) {$\mathrm{S}_2$};
\draw[frc] (1.2,1.6) -- (1.2,0.3); \node[right] at (1.25,1.4) {$v$};
\draw[line width=0.9pt,-{Latex[length=2mm]}] (1.2,0) arc (0:-180:1.3);
\draw[gd] (-0.1,0) -- (-0.1,-0.25);
"""

FIGS['n29_ex28_zu'] = r"""
\draw[ax] (0,0) -- (0,3.0) node[above]{$z$};
\draw[ax] (0,0) -- (3.0,0) node[right]{$y$};
\draw[ax] (0,0) -- (-1.3,-1.1) node[below left]{$x$};
\node[below right] at (0,0) {O};
\foreach \x in {1.4,2.4} \draw[-{Latex[length=2mm]},line width=0.5pt,gray] (\x,-0.2) -- (\x,2.6);
\node[right,gray] at (2.4,2.4) {$B$};
\draw[frc] (0,0) -- (-0.8,1.6); \node[left] at (-0.8,1.6) {$v$};
\draw (0,0.8) arc (90:117:0.8); \node at (-0.2,1.05) {$\theta$};
"""

FIGS['n29_ex29_zu'] = r"""
\draw[eq] (0,-0.9) rectangle (2.4,1.8);
\foreach \x in {0.4,1.2,2.0} \foreach \y in {-0.5,0.9,1.5} {\draw[line width=0.4pt] (\x,\y) circle (0.07); \fill (\x,\y) circle (0.022);}
\node[font=\small] at (2.15,-0.1) {$B$};
\draw[ax] (-1.4,0.4) -- (6.8,0.4) node[right] {$x$};
\draw[line width=1.0pt] (6.2,-1.0) -- (6.2,2.4); \node[above] at (6.2,2.4) {スクリーン};
\draw[ax] (6.2,0.4) -- (6.2,2.0); \node[right] at (6.2,1.9) {$y$};
\node[below right] at (6.2,0.4) {O};
\draw[frc] (-1.4,0.4) -- (-0.6,0.4); \node[above] at (-1.0,0.45) {$v$};
\draw[line width=0.8pt,dash pattern=on 2pt off 1.5pt] (0,0.4) arc (-90:-73:8.0) -- (6.2,1.95);
\draw[dim] (0,-1.25) -- (2.4,-1.25); \node[lab] at (1.2,-1.25) {$l$ \small ①};
\draw[dim] (2.4,-1.25) -- (6.2,-1.25); \node[lab] at (4.3,-1.25) {$L$ \small ②};
\node[font=\small] at (-1.0,-0.2) {電子};
"""

FIGS['n29_zu_sokudo'] = r"""
\draw[line width=1.2pt] (-1.4,-0.3) -- (-1.4,3.2); \node[left] at (-1.4,2.9) {$+$};
\draw[line width=1.2pt] (1.4,-0.3) -- (1.4,3.2); \node[right] at (1.4,2.9) {$-$};
\foreach \y in {0.2,2.6} \draw[-{Latex[length=1.6mm]},line width=0.5pt] (-1.35,\y) -- (1.35,\y);
\node[above] at (-0.8,2.6) {$E$};
\foreach \x in {-0.9,0.9} \foreach \y in {0.7,2.1} {\draw[line width=0.5pt] (\x,\y)+(-0.08,-0.08) -- +(0.08,0.08); \draw[line width=0.5pt] (\x,\y)+(-0.08,0.08) -- +(0.08,-0.08);}
\node[right] at (0.95,2.1) {$B$};
\draw[frc] (0,-0.9) -- (0,3.6); \node[above] at (0,3.6) {$v$};
\fill (0,1.4) circle (0.07);
\draw[frc] (0,1.4) -- (0.9,1.4); \node[above] at (0.55,1.42) {$qE$};
\draw[frc] (0,1.4) -- (-0.9,1.4); \node[above] at (-0.55,1.42) {$qvB$};
"""

FIGS['n29_zu_hall'] = r"""
\draw[line width=0.8pt] (0,0) -- (3.0,0) -- (3.0,1.6) -- (0,1.6) -- cycle;
\draw[line width=0.8pt] (3.0,0) -- (3.8,0.6) -- (3.8,2.2) -- (0.8,2.2) -- (0,1.6);
\draw[line width=0.8pt] (3.0,1.6) -- (3.8,2.2);
\foreach \x in {0.4,1.2,2.0,2.8} \node at (\x,1.4) {\small $-$};
\foreach \x in {0.4,1.2,2.0,2.8} \node at (\x,0.2) {\small $+$};
\draw[frc] (-1.1,0.8) -- (-0.1,0.8); \node[above] at (-0.7,0.85) {$I$};
\draw[-{Latex[length=2mm]},line width=0.6pt,gray] (1.8,3.6) -- (1.0,3.0); \node[right,gray] at (1.8,3.6) {$B$（手前向き）};
\fill[gray] (1.5,0.9) circle (0.08); \draw[frc] (1.5,0.9) -- (2.3,0.9); \node[above] at (2.1,0.9) {$\bar v$};
\draw[frc] (1.5,0.85) -- (1.5,0.35);
\node[right] at (1.55,0.55) {\small $q\bar vB$};
"""

FIGS['n29_zu_cyclo'] = r"""
\draw[line width=1.0pt] (-0.12,-2.2) -- (-0.12,2.2) arc (90:270:2.2);
\draw[line width=1.0pt] (0.12,2.2) -- (0.12,-2.2) arc (-90:90:2.2);
\node at (-1.6,2.0) {$\mathrm{D}_1$}; \node at (1.6,2.0) {$\mathrm{D}_2$};
\draw[line width=0.8pt] (0,0.5) arc (90:-90:0.5) arc (-90:-270:0.7) arc (90:-90:0.9) arc (-90:-270:1.1) arc (90:-90:1.3) arc (-90:-270:1.5) arc (90:-90:1.7);
\draw[-{Latex[length=2mm]},line width=0.8pt] (0,-1.7) -- (-2.6,-1.7);
\fill (0,0.5) circle (0.05);
\node[font=\small,anchor=west] at (2.4,0.3) {磁場は紙面に垂直};
\node[font=\small,anchor=north] at (0,-2.3) {すき間で交流電圧により加速};
"""

if __name__ == '__main__':
    run(FIGS, sys.argv[1:])
