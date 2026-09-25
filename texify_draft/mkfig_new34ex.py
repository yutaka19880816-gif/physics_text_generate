# -*- coding: utf-8 -*-
# 新第34回の例題の図を TikZ で自作する（原本の講義編の例題の図はこの環境に無いため描き起こし）。
#   n34_ex8_zu  … 例題8（原本8）加速電圧 60 kV のX線スペクトル（OCR から再構成：横軸 ×10^{-11} m，目盛 5・10）
#   n34_ex8_ans … 例題8 の解答：加速電圧を半分にしたときのスペクトル（破線）
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tikzfig import run

FIGS = {}
# 連続X線：I(λ) = K (1/λmin − 1/λ)/λ^2（λmin=hc/eV）．特性X線は λ=6.3, 7.1（×10^{-11} m）に鋭いピーク
K, SX = 120.0, 0.55
def f(lmin, l):
    k = K if lmin < 3 else 2.2*K   # 30 kV は見やすさのため縦を拡大（60 kV より低いことは保つ）
    return max(0.0, k*(1/lmin - 1/l)/l**2)
def cont(lmin, style):
    pts = []
    l = lmin
    while l <= 10.8:
        pts.append('(%.3f,%.3f)' % (l*SX, f(lmin, l)))
        l += 0.1
    return r"\draw[%s] plot[smooth] coordinates {%s};" % (style, ' '.join(pts)) + "\n"
def peaks(lmin, hs, style):
    s = ""
    for lam, h in zip((6.3, 7.1), hs):
        b1, b2 = f(lmin, lam-0.09), f(lmin, lam+0.09)
        s += r"\draw[%s] (%.3f,%.3f) -- (%.3f,%.3f) -- (%.3f,%.3f);" % (style, (lam-0.09)*SX, b1, lam*SX, f(lmin, lam)+h, (lam+0.09)*SX, b2) + "\n"
    return s
AX = r"""
\draw[ax] (0,0) -- (6.4,0);
\node[right,align=left] at (6.4,0) {\small 波長\\\small ($\times 10^{-11}\U{m}$)};
\draw[ax] (0,0) -- (0,3.6) node[left] {\small X線強度};
\foreach \x in {5,10} {\draw (\x*0.55,0) -- (\x*0.55,-0.08) node[below] {\small \x};}
\node[below left] at (0,0) {O};
"""
S1 = 'line width=0.9pt'
S2 = 'line width=0.9pt,dash pattern=on 3pt off 1.5pt'
FIGS['n34_ex8_zu'] = AX + cont(2.07, S1) + peaks(2.07, (1.5, 1.2), S1)
FIGS['n34_ex8_ans'] = FIGS['n34_ex8_zu'] + cont(4.14, S2) + peaks(4.14, (0.6, 0.5), S2) + \
    r"\draw[gd] (2.07*0.55,0) -- (2.07*0.55,-0.1) node[below] {\small 2.1};" + "\n" + \
    r"\draw[gd] (4.14*0.55,0) -- (4.14*0.55,-0.1) node[below] {\small 4.1};" + "\n" + \
    r"\node[above] at (1.9,2.05) {\small 60\,kV}; \node[right] at (3.9,0.2) {\small 30\,kV（破線）};" + "\n"

if __name__ == '__main__':
    run(FIGS, sys.argv[1:])
