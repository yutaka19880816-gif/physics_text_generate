# -*- coding: utf-8 -*-
# 新第33回の例題の図を TikZ で自作する（原本の講義編の例題の図はこの環境に無いため描き起こし）。
#   n33_ex3_graph … 例題3（原本3）光電管の電流－電圧グラフ a・b・c（OCR から再構成）
#   n33_ex4_zu    … 例題4（原本4）コンプトン効果の衝突の図
#   n33_ex7_level … 例題7（原本7）水素原子のエネルギー準位図
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tikzfig import run

FIGS = {}

# 例題3：a と b は阻止電圧が同じ（振動数が同じ）で飽和電流 a>b，c は阻止電圧が大きく飽和電流は b と同じ
FIGS['n33_ex3_graph'] = r"""
\draw[ax] (-3.2,0) -- (3.4,0) node[below] {$V$};
\draw[ax] (0,-0.3) -- (0,3.2) node[left] {$I$};
\node[below right] at (0,0) {O};
\draw[line width=0.9pt] plot[smooth,domain=-1.2:3.0,samples=60] (\x,{2.4/(1+exp(-3.2*(\x+0.05)))-2.4/(1+exp(-3.2*(-1.2+0.05)))});
\draw[line width=0.9pt] plot[smooth,domain=-1.2:3.0,samples=60] (\x,{1.4/(1+exp(-3.2*(\x+0.05)))-1.4/(1+exp(-3.2*(-1.2+0.05)))});
\draw[line width=0.9pt,dash pattern=on 3pt off 1.5pt] plot[smooth,domain=-2.4:3.0,samples=70] (\x,{1.4/(1+exp(-2.2*(\x+0.45)))-1.4/(1+exp(-2.2*(-2.4+0.45)))});
\node[right] at (3.0,2.35) {a};
\node[right] at (3.0,1.55) {b};
\node[right] at (3.0,1.15) {c};
\draw[gd] (-1.2,0) -- (-1.2,-0.15); \node[below] at (-1.2,-0.05) {$-V_1$};
\draw[gd] (-2.4,0) -- (-2.4,-0.15); \node[below] at (-2.4,-0.05) {$-V_2$};
"""

# 例題4：コンプトン効果
FIGS['n33_ex4_zu'] = r"""
\draw[line width=0.6pt] plot[smooth,domain=-3.2:-0.4,samples=120] (\x,{0.08*sin(\x*360/0.22)});
\draw[ax] (-0.5,0) -- (-0.22,0);
\node[above] at (-1.9,0.15) {$\lambda$};
\node[below] at (-1.9,-0.15) {入射X線};
\shade[ball color=gray!50] (0,0) circle (0.2);
\node[above] at (0,0.22) {電子};
\draw[gd] (0.2,0) -- (3.4,0);
\draw[line width=0.6pt,rotate=35] plot[smooth,domain=0.25:2.5,samples=120] (\x,{0.08*sin(\x*360/0.26)});
\draw[ax,rotate=35] (2.4,0) -- (2.8,0);
\node[above left] at ({0.2+2.2*cos(35)},{2.2*sin(35)}) {$\lambda^\prime$};
\node[right] at ({0.2+2.9*cos(35)},{2.9*sin(35)}) {散乱X線};
\draw (1.2,0) arc (0:35:1.0); \node at (1.45,0.35) {$\theta$};
\draw[frc] (0.15,-0.15) -- ({2.3*cos(-40)},{2.3*sin(-40)}); \node[right] at ({2.3*cos(-40)},{2.3*sin(-40)}) {$v$};
\draw (1.1,0) arc (0:-40:1.1); \node at (1.35,-0.42) {$\varphi$};
"""

# 例題7：水素原子のエネルギー準位
LV = [(1,-13.6),(2,-3.40),(3,-1.51),(4,-0.85),(5,-0.54),(6,-0.38)]
def y(E):  # 見やすさのため非線形に縮める
    import math
    return 8.0 - 8.0*(-E/13.6)**0.35
body = r"\draw[ax] (0,-0.3) -- (0,8.7) node[above] {エネルギー};" + "\n"
body += r"\draw (0,8.0) -- (6.6,8.0); \node[right] at (6.6,8.0) {$0\U{eV}\ (n=\infty)$};" + "\n"
for n,E in LV:
    body += r"\draw (0,%.3f) -- (6.6,%.3f); \node[right] at (6.6,%.3f) {\small $%.2f\U{eV}\ (n=%d)$};" % (y(E),y(E),y(E),E,n) + "\n"
    body = body.replace('-13.60', '-13.6')
def arrows(x0, nlow, highs, name):
    s = ""
    for i,h in enumerate(highs):
        x = x0 + 0.28*i
        s += r"\draw[cur] (%.2f,%.3f) -- (%.2f,%.3f);" % (x, y(dict(LV)[h]), x, y(dict(LV)[nlow])) + "\n"
    s += r"\node[below,align=center] at (%.2f,%.3f) {\small %s};" % (x0+0.14*(len(highs)-1), y(dict(LV)[nlow])-0.02, name) + "\n"
    return s
body += arrows(0.6, 1, [2,3,4,5,6], 'ライマン系列')
body += arrows(2.7, 2, [3,4,5,6], 'バルマー系列')
body += arrows(4.7, 3, [4,5,6], 'パッシェン系列')
FIGS['n33_ex7_level'] = body

if __name__ == '__main__':
    run(FIGS, sys.argv[1:])
