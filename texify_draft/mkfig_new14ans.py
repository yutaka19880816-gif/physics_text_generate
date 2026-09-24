# -*- coding: utf-8 -*-
# 新第14回の例題の「解答図」をTikZで自作する。
# 原本の例題には解答が載っていないため解答図も存在しない（組版チェックリスト 2. の方針）。
# pdflatex を使うので図中に日本語は書けない。ラベルはすべて数式記号にしてある。
import subprocess, os, sys
TMPD = '/private/tmp/claude-501/-Users-yutaka-Documents-Claude-Code----math-tex-tool/1df6deb5-316e-4f0f-a56b-76b9376dca13/scratchpad/tikz14'
os.makedirs(TMPD, exist_ok=True)
HEAD = r'''\documentclass[border=3pt]{standalone}
\usepackage{amsmath}
\usepackage{tikz}
\usetikzlibrary{arrows.meta}
\begin{document}
\begin{tikzpicture}[x=0.42cm,y=0.42cm,line join=round,
   ax/.style={-{Latex[length=2mm]},line width=0.5pt},
   cv/.style={line width=1.0pt},
   gd/.style={line width=0.4pt,densely dashed},
   ref/.style={line width=0.7pt,densely dashed}]
'''
TAIL = r'''\end{tikzpicture}
\end{document}
'''

# 波長8単位・振幅2単位に正規化して，どの図も同じ見た目にそろえる
FIGS = {}

# --- 例題1(4) t=1.4[s] の波形（実線）と t=0 の波形（参考・破線） -------------
FIGS['n14_ex1_ans'] = r'''
\draw[gd] (0.2,2)--(14.6,2);  \draw[gd] (0.2,-2)--(14.6,-2);
\draw[ax] (-2.6,0)--(15.4,0) node[below right=-1pt]{$x$};
\draw[ax] (0,-3.4)--(0,3.4) node[above right=-2pt]{$y$};
\node[below left=-2pt,fill=white,inner sep=0.5pt] at (0,0) {$\mathrm{O}$};
\node[left,fill=white,inner sep=1pt] at (0,2) {$2$}; \node[left,fill=white,inner sep=1pt] at (0,-2) {$-2$};
\foreach \n in {2,4,6,8,10,12} \node[below,fill=white,inner sep=1pt] at (\n,-0.15) {$\n$};
\draw[ref] plot[domain=-2:14.6,samples=160] (\x,{-2*sin(pi*\x/4 r)});
\draw[cv]  plot[domain=-2:14.6,samples=160] (\x,{ 2*sin(pi*\x/4 r)});
'''
# --- 例題3(1) グラフ(1)の代表点 --------------------------------------------
FIGS['n14_ex3_d1'] = r'''
\draw[gd] (0.2,2)--(10.4,2);  \draw[gd] (0.2,-2)--(10.4,-2);
\draw[ax] (-1.6,0)--(11.2,0) node[below right=-1pt]{$x$};
\draw[ax] (0,-3.4)--(0,3.4) node[above right=-2pt]{$y$};
\node[below left=-2pt] at (0,0) {$\mathrm{O}$};
\node[left] at (0,2) {$A$}; \node[left] at (0,-2) {$-A$};
\node[above,fill=white,inner sep=1pt] at (2,0.15) {$\frac{vT}{4}$};
\node[below,fill=white,inner sep=1pt] at (4,-0.15) {$\frac{vT}{2}$};
\node[above,fill=white,inner sep=1pt] at (6,0.15) {$\frac{3vT}{4}$};
\node[below] at (8,-0.15) {$vT$};
\draw[cv] plot[domain=-1:10.4,samples=140] (\x,{2*sin(pi*\x/4 r)});
'''
# --- 例題3(1) グラフ(2)の代表点 --------------------------------------------
FIGS['n14_ex3_d2'] = r'''
\draw[gd] (0.2,2)--(10.4,2);  \draw[gd] (0.2,-2)--(10.4,-2);
\draw[ax] (-1.6,0)--(11.2,0) node[below right=-1pt]{$x$};
\draw[ax] (0,-3.4)--(0,3.4) node[above right=-2pt]{$y$};
\node[above left=-2pt] at (0,0) {$\mathrm{O}$};
\node[left] at (0,2) {$A$}; \node[left] at (0,-2) {$-A$};
\node[below,fill=white,inner sep=1pt] at (2,-0.15) {$\frac{vT}{4}$};
\node[above,fill=white,inner sep=1pt] at (4,0.15) {$\frac{vT}{2}$};
\node[below,fill=white,inner sep=1pt] at (6,-0.15) {$\frac{3vT}{4}$};
\node[above] at (8,0.15) {$vT$};
\draw[cv] plot[domain=-1:10.4,samples=140] (\x,{-2*cos(pi*\x/4 r)});
'''
# --- 例題3(2) 原点の y-t グラフ（(1)のグラフに対応） ------------------------
FIGS['n14_ex3_a1'] = r'''
\draw[gd] (0.2,2)--(10.4,2);  \draw[gd] (0.2,-2)--(10.4,-2);
\draw[ax] (-1.6,0)--(11.2,0) node[below right=-1pt]{$t$};
\draw[ax] (0,-3.4)--(0,3.4) node[above right=-2pt]{$y$};
\node[above left=-2pt] at (0,0) {$\mathrm{O}$};
\node[left] at (0,2) {$A$}; \node[left] at (0,-2) {$-A$};
\node[above,fill=white,inner sep=1pt] at (4,0.15) {$\frac{T}{2}$};
\node[above] at (8,0.15) {$T$};
\draw[cv] plot[domain=-1:10.4,samples=140] (\x,{-2*sin(pi*\x/4 r)});
'''
# --- 例題3(2) 原点の y-t グラフ（(2)のグラフに対応） ------------------------
FIGS['n14_ex3_a2'] = r'''
\draw[gd] (0.2,2)--(10.4,2);  \draw[gd] (0.2,-2)--(10.4,-2);
\draw[ax] (-1.6,0)--(11.2,0) node[below right=-1pt]{$t$};
\draw[ax] (0,-3.4)--(0,3.4) node[above right=-2pt]{$y$};
\node[above left=-2pt] at (0,0) {$\mathrm{O}$};
\node[left] at (0,2) {$A$}; \node[left] at (0,-2) {$-A$};
\node[below,fill=white,inner sep=1pt] at (2,-0.15) {$\frac{T}{4}$};
\node[above,fill=white,inner sep=1pt] at (4,0.15) {$\frac{T}{2}$};
\node[below] at (8,-0.15) {$T$};
\draw[cv] plot[domain=-1:10.4,samples=140] (\x,{-2*cos(pi*\x/4 r)});
'''
# --- 例題4(1) 与えられた y-t グラフの代表点 ---------------------------------
FIGS['n14_ex4_ans'] = r'''
\draw[gd] (0.2,2)--(10.4,2);  \draw[gd] (0.2,-2)--(10.4,-2);
\draw[ax] (-1.6,0)--(11.2,0) node[below right=-1pt]{$t$};
\draw[ax] (0,-3.4)--(0,3.4) node[above right=-2pt]{$y$};
\node[above left=-2pt] at (0,0) {$\mathrm{O}$};
\node[left] at (0,2) {$A$}; \node[left] at (0,-2) {$-A$};
\node[above,fill=white,inner sep=1pt] at (2,0.15) {$\frac{T}{4}$};
\node[above,fill=white,inner sep=1pt] at (4,0.15) {$\frac{T}{2}$};
\node[above,fill=white,inner sep=1pt] at (6,0.15) {$\frac{3T}{4}$};
\node[above] at (8,0.15) {$T$};
\draw[cv] plot[domain=-1:10.4,samples=140] (\x,{-2*sin(pi*\x/4 r)});
'''

# --- 例題5(2)(3) 縦波の実際の媒質の位置（横波表示を元に戻したもの） ---------
#  実長 2.5 ごとに媒質をとり，変位 y=-3sin(pi x/10) を x 方向の変位として置き直す。
#  作図単位 ＝ 実長/2.5（波長20 → 8単位。他の図と縮尺をそろえる）
_eq  = [0,1,2,3,4,5,6,7,8,9,10,11,12]
_dsp = [0.000,0.152,0.800,2.152,4.000,5.848,7.200,7.848,8.000,8.152,8.800,10.152,12.000]
_lab = {2:'A',4:'B',6:'C',8:'D',10:'E'}
def ex5(hide=False):
    """hide=True … 変位後の媒質・点線・B/D の矢印を \path にして「変位を描き込む前」の
       補助図にする（バウンディングボックスは完全版と同じ）。"""
    D = '\\path' if hide else '\\draw'
    F = '\\path' if hide else '\\fill'
    _b  = r'\draw[line width=0.5pt] (-0.6,2.6)--(12.6,2.6);' + '\n'
    _b += r'\draw[line width=0.5pt] (-0.6,0)--(12.6,0);' + '\n'
    for k in _eq:
        _b += r'\fill (%g,2.6) circle (1.5pt);' % k + '\n'
    for k,v in _lab.items():
        _b += r'\node[above=1pt] at (%g,2.6) {$\mathrm{%s}$};' % (k,v) + '\n'
    for k,d in zip(_eq,_dsp):
        _b += F + r' (%g,0) circle (1.5pt);' % d + '\n'
        _b += D + r'[line width=0.3pt,densely dotted] (%g,2.45)--(%g,0.15);' % (k,d) + '\n'
    # 疎になる点（B）と密になる点（D）だけを矢印で示す（ラベルは記号のみ：pdflatex のため）
    _b += D + r'[line width=0.6pt,-{Latex[length=2mm]}] (4,-1.6)--(4,-0.35);' + '\n'
    _b += r'\node[below,fill=white,inner sep=1pt] at (4,-1.6) {%s};' % (r'\phantom{$\mathrm{B}$}' if hide else r'$\mathrm{B}$') + '\n'
    _b += D + r'[line width=0.6pt,-{Latex[length=2mm]}] (8,-1.6)--(8,-0.35);' + '\n'
    _b += r'\node[below,fill=white,inner sep=1pt] at (8,-1.6) {%s};' % (r'\phantom{$\mathrm{D}$}' if hide else r'$\mathrm{D}$') + '\n'
    return _b
FIGS['n14_ex5_ans']   = ex5(False)
FIGS['n14_ex5_ans_blank'] = ex5(True)

# ---- 穴埋め版（生徒用）の補助図：答えの線・値だけを消し，寸法は完全版と同じ ----
import re as _re
def _ph(body, *targets):
    """\node の中身を \phantom にして，見えないが同じ寸法にする"""
    for t in targets:
        body = body.replace('{%s}' % t, '{\\phantom{%s}}' % t)
    return body
def _nodraw(body, *styles):
    """\draw[style] を \path[style] にする（描かれないが bbox は同じ）"""
    for st in styles:
        body = _re.sub(r'\\draw\[' + _re.escape(st) + r'\]', r'\\path[' + st + r']', body)
    return body

# 例題1(4)：実線（＝求める t=1.4s の波形）を消す。破線（t=0）は残す
FIGS['n14_ex1_ans_blank'] = _nodraw(FIGS['n14_ex1_ans'], 'cv')
# 例題3(1)：代表点の値だけを消す（曲線と軸は残す＝値を書き込む図）
_d = ('$A$','$-A$',r'$\frac{vT}{4}$',r'$\frac{vT}{2}$',r'$\frac{3vT}{4}$','$vT$')
FIGS['n14_ex3_d1_blank'] = _ph(FIGS['n14_ex3_d1'], *_d)
FIGS['n14_ex3_d2_blank'] = _ph(FIGS['n14_ex3_d2'], *_d)
# 例題3(2)：y-t グラフそのものが答えなので曲線も値も消す（軸だけ残す）
_t = ('$A$','$-A$',r'$\frac{T}{4}$',r'$\frac{T}{2}$',r'$\frac{3T}{4}$','$T$')
FIGS['n14_ex3_a1_blank'] = _nodraw(_ph(FIGS['n14_ex3_a1'], *_t), 'cv')
FIGS['n14_ex3_a2_blank'] = _nodraw(_ph(FIGS['n14_ex3_a2'], *_t), 'cv')
# 例題4(1)：代表点の値だけを消す
FIGS['n14_ex4_ans_blank'] = _ph(FIGS['n14_ex4_ans'], *_t)

# --------------------------------------------------------------------------
def build(name, body):
    tex = os.path.join(TMPD, name + '.tex')
    open(tex,'w',encoding='utf-8').write(HEAD + body + TAIL)
    r = subprocess.run(['pdflatex','-interaction=nonstopmode','-output-directory',TMPD,tex],
                       capture_output=True, text=True)
    pdf = os.path.join(TMPD, name + '.pdf')
    if not os.path.exists(pdf):
        print('  !! コンパイル失敗', name)
        print('\n'.join(l for l in r.stdout.splitlines() if l.startswith('!'))[:400]); return
    out = 'fig/%s.png' % name
    subprocess.run(['gs','-sDEVICE=pnggray','-r600','-dNOPAUSE','-dBATCH','-o',out,pdf],
                   capture_output=True)
    subprocess.run(['extractbb', out], capture_output=True)
    print(f'  {os.path.basename(out):22s} {os.path.getsize(out)/1000:6.1f} KB')

if __name__ == '__main__':
    for n,b in FIGS.items(): build(n,b)
