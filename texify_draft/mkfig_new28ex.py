# -*- coding: utf-8 -*-
# 新第28回の例題の図を TikZ で自作する（原本の講義編の図はこの環境に無いため描き起こし）。
#     n28_ex21_zu   … 例題21（原本24）ソレノイドコイル
#     n28_ex22_zu   … 例題22（原本25）円形電流と，それに接する垂直な直線電流
#     n28_ex22_ans  … 例題22(3) 点O の合成磁場（真上から見た図と，断面の図）
#     n28_ex23_zu   … 例題23（原本26）逆向きの平行電流と座標軸
#     n28_ex24_zu   … 例題24（原本27）平行導線（断面）
#     n28_ex24_ans  … 例題24(2) B が受ける力
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tikzfig import run

FIGS = {}

FIGS['n28_ex21_zu'] = r"""
\foreach \i in {0,...,13} {
  \draw[line width=0.4pt,gray] (0.3*\i,0.75) .. controls (0.3*\i+0.2,0.75) and (0.3*\i+0.2,-0.75) .. (0.3*\i+0.15,-0.75);
  \draw[line width=0.9pt] (0.3*\i+0.15,-0.75) .. controls (0.3*\i+0.05,-0.75) and (0.3*\i+0.2,0.75) .. (0.3*\i+0.3,0.75);
}
\draw[line width=0.5pt] (0,0) ellipse (0.14 and 0.75); \draw[line width=0.5pt] (4.2,0) ellipse (0.14 and 0.75);
\draw[line width=0.9pt] (0.15,-0.75) -- (0.15,-1.4) -- (-0.4,-1.4); \draw[line width=0.9pt] (4.35,-0.75) -- (4.35,-1.4) -- (4.9,-1.4);
\draw[cur] (-1.0,-1.4) -- (-0.45,-1.4); \node[above] at (-0.75,-1.4) {$I$};
\draw[dim] (0,1.1) -- (4.2,1.1); \node[lab] at (2.1,1.1) {$l$};
\draw[line width=0.4pt] (-0.1,0.4) -- (-0.6,0.9); \node[above left] at (-0.55,0.85) {断面積 $S$};
\node[font=\small] at (2.25,-1.25) {巻き数 $N$};
"""

FIGS['n28_ex22_zu'] = r"""
% 円（xy 平面，斜めから見た楕円）
\draw[line width=1.0pt] (0,0) ellipse (1.6 and 0.6);
\fill (0,0) circle (0.04); \node[below left] at (0,0) {O};
\draw[gd] (0,0) -- (1.6,0); \node[below] at (0.8,0) {$a$};
\draw[-{Latex[length=2.4mm]},line width=0.8pt] (-0.4,-0.58) -- (0.15,-0.6); \node[below] at (-0.1,-0.62) {$I_1$};
% 直線電流（円に接して鉛直）
\draw[line width=1.0pt] (1.6,-1.8) -- (1.6,-0.08); \draw[line width=1.0pt] (1.6,0.08) -- (1.6,1.9);
\draw[-{Latex[length=2.4mm]},line width=0.8pt] (1.85,0.6) -- (1.85,1.5); \node[right] at (1.85,1.05) {$I_2$};
% 座標軸
\draw[ax] (0,0) -- (0,1.9) node[above]{$z$};
\draw[ax] (0,0) -- (-1.1,-1.3) node[below left]{$x$};
\draw[gd] (-1.6,0) -- (-2.3,0);
\draw[ax] (-1.6,0) -- (-2.6,0) node[left]{$y$};
"""

FIGS['n28_ex22_ans'] = r"""
\draw[ax] (0,0) -- (3.2,0) node[right] {$-x$};
\draw[ax] (0,0) -- (0,2.6) node[above] {$-z$};
\fill (0,0) circle (0.05); \node[below left] at (0,0) {O};
\draw[frc] (0,0) -- (2.4,0); \node[below] at (1.6,0) {$H_2=\dfrac{I_2}{2\pi a}$};
\draw[frc] (0,0) -- (0,1.8); \node[left] at (0,1.2) {$H_1=\dfrac{I_1}{2a}$};
\draw[gd] (2.4,0) -- (2.4,1.8) -- (0,1.8);
\draw[frc,line width=1.4pt] (0,0) -- (2.4,1.8); \node[above right] at (2.4,1.8) {$H$};
\draw (0.7,0) arc (0:36.87:0.7); \node at (0.95,0.3) {$\theta$};
"""

FIGS['n28_ex23_zu'] = r"""
\draw[ax] (-2.6,0) -- (2.8,0) node[right]{$x$};
\draw[ax] (0,-0.6) -- (0,2.3) node[above]{$y$};
\node[below left] at (0,0) {O};
\draw[line width=0.8pt,fill=white] (-1.4,0) circle (0.14); \fill (-1.4,0) circle (0.045);
\draw[line width=0.8pt,fill=white] (1.4,0) circle (0.14);
\draw (1.4,0)+(-0.1,-0.1) -- +(0.1,0.1); \draw (1.4,0)+(-0.1,0.1) -- +(0.1,-0.1);
\node[above] at (-1.4,0.15) {A}; \node[above] at (1.4,0.15) {B};
\node[below] at (-1.4,-0.15) {$-a$}; \node[below] at (1.4,-0.15) {$a$};
\node[font=\small,anchor=north] at (-1.4,-0.55) {$I_{\mathrm{A}}$（手前向き）};
\node[font=\small,anchor=north] at (1.4,-0.55) {$I_{\mathrm{B}}$（奥向き）};
\fill (0,1.5) circle (0.05); \node[right] at (0,1.5) {$\mathrm{P}(0,b)$};
\draw[gd] (-1.4,0) -- (0,1.5) -- (1.4,0);
"""

FIGS['n28_ex24_zu'] = r"""
\draw[line width=0.8pt,fill=white] (0,0) circle (0.16); \fill (0,0) circle (0.05);
\draw[line width=0.8pt,fill=white] (2.6,0) circle (0.16); \fill (2.6,0) circle (0.05);
\node[above] at (0,0.2) {A}; \node[above] at (2.6,0.2) {B};
\node[below] at (0,-0.2) {$I_1$}; \node[below] at (2.6,-0.2) {$I_2$};
\draw[dim] (0.2,-0.75) -- (2.4,-0.75); \node[lab] at (1.3,-0.75) {$r$};
"""

FIGS['n28_ex24_ans'] = r"""
\draw[eq] (0,0) circle (2.6);
\draw[line width=0.8pt,fill=white] (0,0) circle (0.16); \fill (0,0) circle (0.05);
\draw[line width=0.8pt,fill=white] (2.6,0) circle (0.16); \fill (2.6,0) circle (0.05);
\node[below left] at (0,-0.1) {A}; \node[below right] at (2.65,-0.12) {B};
\draw[frc] (2.6,0.2) -- (2.6,1.4); \node[right] at (2.6,1.2) {$B_1=\dfrac{\mu_0I_1}{2\pi r}$};
\draw[frc,line width=1.3pt] (2.4,0) -- (1.2,0); \node[above] at (1.5,0.02) {$F$};
\node[font=\small] at (-1.2,1.9) {A の磁場（磁力線）};
"""

if __name__ == '__main__':
    run(FIGS, sys.argv[1:])
