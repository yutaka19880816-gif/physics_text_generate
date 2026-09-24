# -*- coding: utf-8 -*-
# 新第30回の例題・練習［108］の図を TikZ で自作する（原本の講義編の図はこの環境に無いため描き起こし）。
#   n30_ex30_zu … 例題30（原本32）直線電流とコイル
#   n30_ex31_zu … 例題31（原本33）回転する導体棒
#   n30_ex32_zu … 例題32（原本34）磁場中を落下する導体棒
#   n30_ex33_zu … 例題33（原本35）ソレノイドの自己インダクタンス
#   n30_ex34_zu … 例題34（原本37）鉄心に巻いた2つのコイル
#   n30_p108_zu … 練習［108］（原本の例題38）同心の2つの円形コイル
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tikzfig import run

FIGS = {}

FIGS['n30_ex30_zu'] = r"""
\draw[line width=1.0pt] (0,-0.3) -- (0,3.0); \node[left] at (0,2.8) {A};
\draw[frc] (0.25,0.6) -- (0.25,1.9); \node[right] at (0.25,1.3) {$I$};
\draw[line width=1.0pt] (2.2,1.35) circle (0.9); \node at (2.2,1.35) {B};
\draw[-{Latex[length=2mm]},line width=0.6pt] (2.2,2.45) arc (90:40:1.1); \node at (3.1,2.45) {ア};
\draw[-{Latex[length=2mm]},line width=0.6pt] (2.2,0.25) arc (-90:-40:1.1); \node at (3.1,0.25) {イ};
"""

FIGS['n30_ex31_zu'] = r"""
\foreach \x in {-1.4,-0.7,...,1.5} \foreach \y in {-1.4,-0.7,...,1.5} {\draw[line width=0.35pt,gray] (\x,\y)+(-0.06,-0.06) -- +(0.06,0.06); \draw[line width=0.35pt,gray] (\x,\y)+(-0.06,0.06) -- +(0.06,-0.06);}
\draw[eq] (0,0) circle (1.6);
\draw[line width=2.2pt] (0,0) -- (1.6,0);
\fill (0,0) circle (0.07); \node[below left] at (0,0) {P}; \node[below right] at (1.6,0) {Q};
\node[above] at (0.8,0.02) {$r$};
\draw[-{Latex[length=2mm]},line width=0.7pt] (1.9,0) arc (0:40:1.9); \node at (2.05,0.95) {$\omega$};
\node[gray] at (1.9,-1.6) {$B$};
"""

FIGS['n30_ex32_zu'] = r"""
\draw[line width=1.0pt] (0,3.4) -- (0,0) -- (3.2,0) -- (3.2,3.4);
\node[above] at (0,3.4) {C}; \node[above] at (3.2,3.4) {D};
\node[below left] at (0,0) {E}; \node[below right] at (3.2,0) {F};
\draw[line width=2.4pt,gray] (-0.2,2.4) -- (3.4,2.4); \node[right] at (3.4,2.4) {K};
\draw[frc] (1.6,2.35) -- (1.6,1.5); \node[right] at (1.6,1.7) {$v$};
\draw[dim] (-0.55,3.4) -- (-0.55,2.4); \node[lab] at (-0.55,2.9) {$x$};
\node[left] at (-0.65,3.4) {O};
\draw[dim] (0,-0.5) -- (3.2,-0.5); \node[lab] at (1.6,-0.5) {$l$};
\foreach \x in {0.6,1.6,2.6} \foreach \y in {0.5,1.3} {\draw[line width=0.4pt,gray] (\x,\y)+(-0.07,-0.07) -- +(0.07,0.07); \draw[line width=0.4pt,gray] (\x,\y)+(-0.07,0.07) -- +(0.07,-0.07);}
\node[gray] at (2.85,0.9) {$B$};
"""

FIGS['n30_ex33_zu'] = r"""
\foreach \i in {0,...,13} {
  \draw[line width=0.4pt,gray] (0.3*\i,0.75) .. controls (0.3*\i+0.2,0.75) and (0.3*\i+0.2,-0.75) .. (0.3*\i+0.15,-0.75);
  \draw[line width=0.9pt] (0.3*\i+0.15,-0.75) .. controls (0.3*\i+0.05,-0.75) and (0.3*\i+0.2,0.75) .. (0.3*\i+0.3,0.75);
}
\draw[line width=0.5pt] (0,0) ellipse (0.14 and 0.75); \draw[line width=0.5pt] (4.2,0) ellipse (0.14 and 0.75);
\draw[line width=0.9pt] (0.15,-0.75) -- (0.15,-1.4) -- (-0.4,-1.4); \draw[line width=0.9pt] (4.35,-0.75) -- (4.35,-1.4) -- (4.9,-1.4);
\draw[cur] (-1.0,-1.4) -- (-0.45,-1.4); \node[above] at (-0.75,-1.4) {$I$};
\draw[dim] (0,1.1) -- (4.2,1.1); \node[lab] at (2.1,1.1) {$l$};
\draw[line width=0.4pt] (-0.1,0.4) -- (-0.6,0.9); \node[above left] at (-0.55,0.85) {断面積 $S$};
\node[font=\small] at (2.25,-1.25) {単位長さあたり $n_0$ 巻き};
"""

FIGS['n30_ex34_zu'] = r"""
\fill[gray!30] (0,-0.35) rectangle (6.0,0.35); \draw[line width=0.6pt] (0,-0.35) rectangle (6.0,0.35);
\foreach \i in {0,...,6} \draw[line width=0.9pt] (0.5+0.25*\i,-0.45) .. controls (0.62+0.25*\i,0) .. (0.5+0.25*\i+0.12,0.45);
\foreach \i in {0,...,6} \draw[line width=0.9pt] (3.8+0.25*\i,-0.45) .. controls (3.92+0.25*\i,0) .. (3.8+0.25*\i+0.12,0.45);
\node[above] at (1.25,0.5) {A}; \node[above] at (4.55,0.5) {B};
\draw (0.5,-0.45) -- (0.5,-1.4) to[vR,l_=可変電源] (2.2,-1.4) to[nos,l_=$\mathrm{S}$] (2.8,-1.4); \draw (2.8,-1.4) -- (2.8,-0.8) -- (2.12,-0.8) -- (2.12,-0.45);
\draw (3.8,-0.45) -- (3.8,-1.1) node[circ]{} node[below]{c}; \draw (5.42,-0.45) -- (5.42,-1.1) node[circ]{} node[below]{d};
\node[below] at (0.5,-1.55) {a}; \node[below] at (2.8,-1.55) {b};
\fill (0.5,-1.4) circle (0.05); \fill (2.8,-1.4) circle (0.05);
"""

FIGS['n30_p108_zu'] = r"""
\draw[line width=1.0pt] (0,0) circle (2.0); \node at (1.2,1.8) {A};
\draw[line width=1.0pt] (0,0) circle (0.55); \node at (0.62,0.55) {B};
\fill (0,0) circle (0.04); \node[below] at (0,-0.05) {O};
\draw[line width=0.5pt] (0,0) -- (-1.414,-1.414); \node[lab] at (-0.8,-0.8) {$R$};
\draw[line width=0.5pt] (0,0) -- (-0.55,0); \node[above] at (-0.3,0) {$r$};
\draw[-{Latex[length=2.2mm]},line width=0.8pt] (2.25,-0.4) arc (-10:25:2.25); \node[right] at (2.3,0.1) {$I$};
"""

if __name__ == '__main__':
    run(FIGS, sys.argv[1:])
