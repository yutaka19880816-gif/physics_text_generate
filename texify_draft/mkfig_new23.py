# -*- coding: utf-8 -*-
# 新第23回（気体の状態変化と熱機関）の図を TikZ で自作する。
#   ・練習［31］［32］（旧⑱[31][32]）は physics_ch18.tex がページ画像の貼り込みの
#     ままだったので，問題の p-V 図・解答の T-V 図・面積図を新規に起こす。
#   ・23.5 熱機関は原本の図が網点1枚（text_p84_fig1）しか無く，エネルギーの流れが
#     どこにも図示されていなかったので加筆する。
#
#     n23_p31_pv    … 練習［31］問題の p-V 図（長方形サイクル ABCD）
#     n23_p32_pv    … 練習［32］問題の p-V 図（A→B は定積，B→C は等温，C→A は定圧）
#     n23_a31_tv    … 練習［31］(2) の T-V 図（解答）
#     n23_a31_area  … 練習［31］参考の面積図3枚（w2／−w4／W_total）
#     n23_a32_pv    … 練習［32］の p-V 図（吸熱・放熱過程と囲む面積）【加筆】
#     n23_zu_netu   … 23.5 熱機関のエネルギーの流れ図【加筆】
#     n23_zu_cycle  … 23.5 サイクルが囲む面積＝正味の仕事（text_p84_fig1 の描き直し）
#     n23_zu_jiyuu  … 23.4 準静的断熱膨張と断熱自由膨張の対比【加筆】
#
#   図中に和文を書くので uplatex → dvipdfmx → gs（mkfig_new21ans.py / 22ans.py と同じ）。
#   使い方:  python3 texify_draft/mkfig_new23.py            （全部作り直す）
#            python3 texify_draft/mkfig_new23.py netu tv    （名前の一部を指定して作る）
import os, sys, subprocess, struct

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

TMPD = ('/private/tmp/claude-501/-Users-yutaka-Documents-Claude-Code----math-tex-tool/'
        '7b99dda4-47d0-4d34-b337-983ef0b7c514/scratchpad/tikz23')
os.makedirs(TMPD, exist_ok=True)

HEAD = r"""\documentclass[border=3pt,dvipdfmx]{standalone}
\usepackage{amsmath}
\usepackage{tikz}
\usetikzlibrary{arrows.meta,decorations.pathmorphing,patterns}
\begin{document}
\begin{tikzpicture}[line join=round,line cap=round,
   ax/.style={line width=0.6pt,-{Latex[length=2.2mm,width=1.8mm]}},
   cv/.style={line width=1.0pt},
   thn/.style={line width=0.5pt},
   wall/.style={line width=1.1pt},
   frc/.style={-{Latex[length=2.2mm,width=1.8mm]},line width=1.0pt},
   gd/.style={line width=0.4pt,dash pattern=on 1.2pt off 1.2pt},
   lead/.style={line width=0.4pt}]
"""
TAIL = "\\end{tikzpicture}\n\\end{document}\n"


def remake_xbb(png):
    """図を作り直したら .xbb は必ず消してから作る（組版チェックリスト §1.5）"""
    xbb = png[:-4] + '.xbb'
    if os.path.exists(xbb):
        os.remove(xbb)
    subprocess.run(['extractbb', png], capture_output=True)


def build(name, body):
    tex = os.path.join(TMPD, name + '.tex')
    open(tex, 'w', encoding='utf-8').write(HEAD + body + TAIL)
    r = None
    for _ in range(2):                      # 和文なので uplatex を2回
        r = subprocess.run(['uplatex', '-interaction=nonstopmode',
                            '-output-directory', TMPD, tex],
                           capture_output=True, text=True)
    dvi = os.path.join(TMPD, name + '.dvi')
    if not os.path.exists(dvi):
        print('  !! コンパイル失敗', name)
        print('\n'.join(l for l in r.stdout.splitlines() if l.startswith('!'))[:1500])
        return
    pdf = os.path.join(TMPD, name + '.pdf')
    subprocess.run(['dvipdfmx', '-o', pdf, dvi], capture_output=True)
    out = 'fig/%s.png' % name
    subprocess.run(['gs', '-sDEVICE=pnggray', '-r600', '-dNOPAUSE', '-dBATCH', '-o', out, pdf],
                   capture_output=True)
    remake_xbb(out)
    w, h = struct.unpack('>II', open(out, 'rb').read(64)[16:24])
    print('  %-16s %5dx%-5d (縦横比 %.2f)  %6.1f KB'
          % (os.path.basename(out), w, h, h / w, os.path.getsize(out) / 1000))


FIGS = {}

# =====================================================================
#  練習［31］問題の p-V 図：長方形サイクル A→B→C→D→A
#   A(V0,p0) B(V0,2p0) C(3V0,2p0) D(3V0,p0)
# =====================================================================
FIGS['n23_p31_pv'] = r"""
\draw[gd] (0,1.0) -- (1.25,1.0);  \draw[gd] (0,2.0) -- (1.25,2.0);
\draw[gd] (1.25,0) -- (1.25,1.0); \draw[gd] (3.65,0) -- (3.65,1.0);
\draw[ax] (0,0) -- (5.40,0);  \node[below] at (5.10,-0.06) {$V\,[\mathrm{m^3}]$};
\draw[ax] (0,0) -- (0,2.75);  \node[above] at (0.02,2.72) {$p\,[\mathrm{Pa}]$};
\node[below left] at (0,0) {$\mathrm{O}$};
\node[left] at (-0.05,1.0) {$p_0$};  \node[left] at (-0.05,2.0) {$2p_0$};
\node[below] at (1.25,-0.06) {$V_0$}; \node[below] at (3.65,-0.06) {$3V_0$};
%% サイクル本体
\draw[cv] (1.25,1.0) -- (1.25,2.0) -- (3.65,2.0) -- (3.65,1.0) -- cycle;
%% 進行方向の矢印
\draw[frc] (1.25,1.40) -- (1.25,1.62);
\draw[frc] (2.32,2.0) -- (2.58,2.0);
\draw[frc] (3.65,1.60) -- (3.65,1.38);
\draw[frc] (2.58,1.0) -- (2.32,1.0);
%% 頂点のラベル（線から離す）
\node[below right,inner sep=1.5pt] at (1.25,1.0) {$\mathrm{A}$};
\node[above right,inner sep=1.5pt] at (1.25,2.0) {$\mathrm{B}$};
\node[above left ,inner sep=1.5pt] at (3.65,2.0) {$\mathrm{C}$};
\node[below left ,inner sep=1.5pt] at (3.65,1.0) {$\mathrm{D}$};
"""

# =====================================================================
#  練習［32］問題の p-V 図：A→B 定積，B→C 等温（pV=2p0V0），C→A 定圧
# =====================================================================
_ISO = r"plot[domain=1.25:2.50,samples=60] (\x,{3.125/\x})"
FIGS['n23_p32_pv'] = (r"""
\draw[gd] (0,1.25) -- (1.25,1.25);  \draw[gd] (0,2.50) -- (1.25,2.50);
\draw[gd] (1.25,0) -- (1.25,1.25);  \draw[gd] (2.50,0) -- (2.50,1.25);
\draw[ax] (0,0) -- (3.75,0);  \node[below] at (3.45,-0.06) {$V\,[\mathrm{m^3}]$};
\draw[ax] (0,0) -- (0,3.25);  \node[above] at (0.02,3.22) {$p\,[\mathrm{Pa}]$};
\node[below left] at (0,0) {$\mathrm{O}$};
\node[left] at (-0.05,1.25) {$p_0$};  \node[left] at (-0.05,2.50) {$2p_0$};
\node[below] at (1.25,-0.06) {$V_0$}; \node[below] at (2.50,-0.06) {$2V_0$};
\draw[cv] (1.25,1.25) -- (1.25,2.50);
\draw[cv] """ + _ISO + r""";
\draw[cv] (2.50,1.25) -- (1.25,1.25);
\draw[frc] (1.25,1.75) -- (1.25,1.97);
\draw[frc] (1.80,{3.125/1.80}) -- (1.95,{3.125/1.95});
\draw[frc] (1.98,1.25) -- (1.77,1.25);
\node[below right,inner sep=1.5pt] at (1.25,1.25) {$\mathrm{A}$};
\node[above right,inner sep=1.5pt] at (1.25,2.50) {$\mathrm{B}$};
\node[right,inner sep=2.5pt]       at (2.50,1.25) {$\mathrm{C}$};
""")

# =====================================================================
#  練習［31］(2) の T-V 図
#   A(V0,T0) B(V0,2T0) C(3V0,6T0) D(3V0,3T0)
#   B→C は T=(2T0/V0)V，D→A は T=(T0/V0)V の直線
# =====================================================================
FIGS['n23_a31_tv'] = r"""
\draw[gd] (0,0.55) -- (1.30,0.55);  \draw[gd] (0,1.10) -- (1.30,1.10);
\draw[gd] (0,1.65) -- (3.40,1.65);  \draw[gd] (0,3.30) -- (3.40,3.30);
\draw[gd] (1.30,0) -- (1.30,0.55);  \draw[gd] (3.40,0) -- (3.40,1.65);
\draw[ax] (0,0) -- (5.20,0);  \node[below] at (4.90,-0.06) {$V\,[\mathrm{m^3}]$};
\draw[ax] (0,0) -- (0,3.85);  \node[above] at (0.02,3.82) {$T\,[\mathrm{K}]$};
\node[below left] at (0,0) {$\mathrm{O}$};
\node[left] at (-0.05,0.55) {$T_0$};  \node[left] at (-0.05,1.10) {$2T_0$};
\node[left] at (-0.05,1.65) {$3T_0$}; \node[left] at (-0.05,3.30) {$6T_0$};
\node[below] at (1.30,-0.06) {$V_0$}; \node[below] at (3.40,-0.06) {$3V_0$};
%% 4つの過程
\draw[cv] (1.30,0.55) -- (1.30,1.10);
\draw[cv] (1.30,1.10) -- (3.40,3.30);
\draw[cv] (3.40,3.30) -- (3.40,1.65);
\draw[cv] (3.40,1.65) -- (1.30,0.55);
%% 進行方向の矢印
\draw[frc] (1.30,0.76) -- (1.30,0.95);
\draw[frc] (2.15,1.99) -- (2.32,2.17);
\draw[frc] (3.40,2.70) -- (3.40,2.48);
\draw[frc] (2.45,1.05) -- (2.26,0.95);
\node[below right,inner sep=2pt] at (1.30,0.55) {$\mathrm{A}$};
\node[above left,inner sep=2.5pt] at (1.30,1.10) {$\mathrm{B}$};   % 破線に乗らないよう上へ
\node[above left,inner sep=1.5pt] at (3.40,3.30) {$\mathrm{C}$};
\node[right,inner sep=3pt]       at (3.40,1.65) {$\mathrm{D}$};
"""

# =====================================================================
#  練習［31］参考の面積図（縦3枚）
#   上：w2（B→C の膨張でした仕事）／中：−w4（D→A で外界からされた仕事）
#   下：W_total＝サイクルが囲む面積
# =====================================================================
_PANEL = r"""
\begin{scope}[yshift=%(dy)scm]
  %(fill)s
  \draw[gd] (0,0.75) -- (1.05,0.75);  \draw[gd] (0,1.50) -- (1.05,1.50);
  \draw[gd] (1.05,0) -- (1.05,0.75);  \draw[gd] (3.00,0) -- (3.00,0.75);
  %% 3V_0 の目盛ラベルと軸ラベルがくっつくので軸を伸ばして離す（2026-09-21）
  \draw[ax] (0,0) -- (4.55,0);  \node[below] at (4.28,-0.05) {\scriptsize $V\,[\mathrm{m^3}]$};
  \draw[ax] (0,0) -- (0,2.10);  \node[above] at (0.02,2.06) {\scriptsize $p\,[\mathrm{Pa}]$};
  \node[below left,inner sep=1pt] at (0,0) {\scriptsize $\mathrm{O}$};
  \node[left,inner sep=2pt] at (0,0.75) {\scriptsize $p_0$};
  \node[left,inner sep=2pt] at (0,1.50) {\scriptsize $2p_0$};
  \node[below,inner sep=2pt] at (1.05,-0.05) {\scriptsize $V_0$};
  \node[below,inner sep=2pt] at (3.00,-0.05) {\scriptsize $3V_0$};
  \draw[cv] (1.05,0.75) -- (1.05,1.50) -- (3.00,1.50) -- (3.00,0.75) -- cycle;
  \draw[frc] (1.05,1.04) -- (1.05,1.21);
  \draw[frc] (1.93,1.50) -- (2.12,1.50);
  \draw[frc] (3.00,1.21) -- (3.00,1.04);
  \draw[frc] (2.12,0.75) -- (1.93,0.75);
  \node[below right,inner sep=1pt] at (1.05,0.75) {\scriptsize $\mathrm{A}$};
  \node[above right,inner sep=1pt] at (1.05,1.50) {\scriptsize $\mathrm{B}$};
  \node[above left ,inner sep=1pt] at (3.00,1.50) {\scriptsize $\mathrm{C}$};
  \node[below left ,inner sep=1pt] at (3.00,0.75) {\scriptsize $\mathrm{D}$};
  %(lab)s
\end{scope}
"""


def _panel(dy, fill, lab):
    return _PANEL % {'dy': dy, 'fill': fill, 'lab': lab}


FIGS['n23_a31_area'] = (
    _panel('6.10',
           r'\fill[black!18] (1.05,0) rectangle (3.00,1.50);',
           r'\node[fill=white,inner sep=1.5pt] at (2.02,0.35) {\scriptsize $w_2$};')
    + _panel('3.05',
             r'\fill[black!38] (1.05,0) rectangle (3.00,0.75);',
             r'\node[fill=white,inner sep=1.5pt] at (2.02,0.36) '
             r'{\scriptsize $-w_4\,(=W_4)$};')
    + _panel('0',
             r'\fill[black!55] (1.05,0.75) rectangle (3.00,1.50);',
             r'\node[fill=white,inner sep=1.5pt] at (2.02,1.12) '
             r'{\scriptsize $W_{\mathrm{total}}$};')
)

# =====================================================================
#  練習［32］の p-V 図（加筆）：吸熱過程・放熱過程と，囲む面積＝w_total
# =====================================================================
#  【2026-09-21 ユーザー指摘】等温曲線がラベルの上を通っていたので図全体を1.35倍に広げ，
#   ・「囲む面積＝w_total」の囲み文字は外し（注の本文が同じことを述べている），
#     $w_{\mathrm{total}}$ だけを引き出し線で網かけの中へ引く
#   ・「吸熱」（B→C）は曲線の右上の空きへ出して短い引き出し線を添える
#   ・「放熱」は C→A の線の下・A のラベルから十分離す
#   引き出し線の端点は「曲線のどちら側か」を y=5.78/x で計算してから置くこと。
_ISO2 = r"plot[domain=1.70:3.40,samples=80] (\x,{5.78/\x})"
FIGS['n23_a32_pv'] = (r"""
\fill[black!25] (1.70,1.70) -- (1.70,3.40) --
   plot[domain=1.70:3.40,samples=80] (\x,{5.78/\x}) -- cycle;
\draw[gd] (0,1.70) -- (1.70,1.70);  \draw[gd] (0,3.40) -- (1.70,3.40);
\draw[gd] (1.70,0) -- (1.70,1.70);  \draw[gd] (3.40,0) -- (3.40,1.70);
\draw[ax] (0,0) -- (5.25,0);  \node[below] at (4.90,-0.06) {\small $V\,[\mathrm{m^3}]$};
\draw[ax] (0,0) -- (0,4.40);  \node[above] at (0.02,4.36) {\small $p\,[\mathrm{Pa}]$};
\node[below left] at (0,0) {\small $\mathrm{O}$};
\node[left] at (-0.05,1.70) {\small $p_0$};  \node[left] at (-0.05,3.40) {\small $2p_0$};
\node[below] at (1.70,-0.06) {\small $V_0$}; \node[below] at (3.40,-0.06) {\small $2V_0$};
\draw[cv] (1.70,1.70) -- (1.70,3.40);
\draw[cv] """ + _ISO2 + r""";
\draw[cv] (3.40,1.70) -- (1.70,1.70);
%% 進行方向の矢印（B→C は曲線上の点と接線方向で引く）
\draw[frc] (1.70,2.35) -- (1.70,2.68);
\draw[frc] (2.021,2.855) -- (2.179,2.649);
\draw[frc] (2.70,1.70) -- (2.42,1.70);
\node[below right,inner sep=1.5pt] at (1.70,1.70) {\small $\mathrm{A}$};
\node[above right,inner sep=1.5pt] at (1.70,3.40) {\small $\mathrm{B}$};
\node[right,inner sep=2.5pt]       at (3.40,1.70) {\small $\mathrm{C}$};
%% 吸熱・放熱
\node[left ,inner sep=3pt] at (1.62,2.55) {\scriptsize 吸熱};
\node[inner sep=1pt] at (2.60,2.95) {\scriptsize 吸熱};
\draw[lead] (2.58,2.79) -- (2.46,2.40);
\node[below,inner sep=2pt] at (2.55,1.62) {\scriptsize 放熱};
%% 網かけ＝正味の仕事
\node[right,inner sep=2pt] at (3.72,2.60) {\scriptsize $w_{\mathrm{total}}$};
\draw[lead] (3.70,2.52) -- (3.08,1.87);
""")

# =====================================================================
#  23.5 熱機関のエネルギーの流れ図（加筆）
# =====================================================================
#  版面では 88mm 幅で貼る。縦長にすると 23.5 の途中で改ページが起きるので，
#  横長（縦横比 0.45 前後）になるよう矢印を短く・注記を1行に収めてある。
FIGS['n23_zu_netu'] = r"""
%% 高熱源（上）・低熱源（下）
\draw[wall] (0.20,2.75) rectangle (4.00,3.45);
\node at (2.10,3.10) {高熱源（温度 $T_1$）};
\draw[wall] (0.20,-0.95) rectangle (4.00,-0.25);
\node at (2.10,-0.60) {低熱源（温度 $T_2$）};
%% 熱機関
\draw[wall] (2.10,1.25) circle (0.82);
\node at (2.10,1.45) {熱};
\node at (2.10,1.00) {機関};
%% 高熱源 → 機関（吸熱）
\draw[frc,line width=1.4pt] (2.10,2.70) -- (2.10,2.15);
\node[right,inner sep=4pt] at (2.14,2.44) {$Q_{\mathrm{in}}$};
%% 機関 → 低熱源（放熱）
\draw[frc,line width=1.4pt] (2.10,0.38) -- (2.10,-0.20);
\node[right,inner sep=4pt] at (2.14,0.10) {$Q_{\mathrm{out}}$};
%% 機関 → 外界（仕事）
\draw[frc,line width=1.4pt] (3.00,1.25) -- (4.40,1.25);
\node[right,inner sep=4pt] at (4.40,1.25)
  {$W_{\mathrm{total}}=Q_{\mathrm{in}}-Q_{\mathrm{out}}$\ （外界にする仕事）};
"""

# =====================================================================
#  23.5 サイクルが囲む面積＝正味の仕事（text_p84_fig1 の描き直し）
#   上の曲線（膨張）でする仕事 − 下の曲線（圧縮）でされる仕事 ＝ 囲む面積
# =====================================================================
_UP = (r"(0.65,2.15) .. controls (1.35,2.05) and (1.75,1.35) .. (2.55,0.95)")
_LO = (r"(2.55,0.95) .. controls (1.90,0.70) and (1.25,0.80) .. (0.65,2.15)")

_CYCPANEL = r"""
\begin{scope}[xshift=%(dx)scm]
  %(fill)s
  \draw[gd] (0.65,0) -- (0.65,2.25);  \draw[gd] (2.55,0) -- (2.55,1.05);
  \draw[ax] (0,0) -- (3.15,0);  \node[below] at (3.00,-0.05) {\scriptsize $V$};
  \draw[ax] (0,0) -- (0,2.70);  \node[left]  at (0.03,2.62) {\scriptsize $p$};
  \node[below left,inner sep=1pt] at (0,0) {\scriptsize $\mathrm{O}$};
  \draw[cv] %(up)s;
  \draw[cv] %(lo)s;
  %% 矢印は曲線上の t=0.5 の点と，その点での接線方向で引く（浮かせない）
  \draw[frc] (1.493,1.720) -- (1.632,1.605);
  \draw[frc] (1.662,0.909) -- (1.501,0.991);
  \node[align=center,font=\scriptsize] at (1.58,-0.72) {%(cap)s};
\end{scope}
"""


def _cyc(dx, fill, cap):
    return _CYCPANEL % {'dx': dx, 'fill': fill, 'up': _UP, 'lo': _LO, 'cap': cap}


FIGS['n23_zu_cycle'] = (
    _cyc('0',
         r'\fill[black!22] (0.65,0) -- (0.65,2.15) ' + _UP.replace('(0.65,2.15) ..', '..')
         + r' -- (2.55,0) -- cycle;',
         r'膨張の過程で\\外界にする仕事')
    + r'\node at (3.55,1.10) {\Large $-$};' + '\n'
    + _cyc('3.95',
           r'\fill[black!22] (2.55,0) -- ' + _LO.replace('(2.55,0.95) ..', '(2.55,0.95) ..')
           + r' -- (0.65,0) -- cycle;',
           r'圧縮の過程で\\外界からされる仕事')
    + r'\node at (7.50,1.10) {\Large $=$};' + '\n'
    + _cyc('7.90',
           r'\fill[black!45] ' + _UP + r' ' + _LO.replace('(2.55,0.95) ..', '..') + r' -- cycle;',
           r'差し引き\\外界にする正味の仕事')
)

# =====================================================================
#  23.4 準静的な断熱膨張と断熱自由膨張の対比（加筆）
# =====================================================================
FIGS['n23_zu_jiyuu'] = r"""
%% ---------------- 左：準静的な断熱膨張（ピストンをゆっくり引く）
\begin{scope}
  \fill[black!15] (0.15,0.20) rectangle (2.75,2.00);
  \draw[wall] (2.75,0.20) -- (0.15,0.20) -- (0.15,2.00) -- (2.75,2.00);
  \fill[black!45] (2.75,0.14) rectangle (2.92,2.06);   % ピストン
  \draw[wall] (2.88,1.10) -- (3.60,1.10);              % 取っ手
  %% 「ゆっくり引く」は矢印の上に置くとシリンダーの上辺・ピストンに重なるので，
  %%   矢印の右へ出す（2026-09-21 ユーザー指摘）
  \draw[frc] (3.05,1.72) -- (3.80,1.72);
  \node[right,inner sep=3pt] at (3.80,1.72) {\small ゆっくり引く};
  \node at (1.45,1.10) {\small 圧力 $P$ が一様};
  \node[below,align=center] at (1.95,0.05)
    {\small 準静的な断熱膨張\\[0.8mm]\small $PV^\gamma=$（一定）が使える\\[0.8mm]\small 外へ仕事をするので温度が下がる};
\end{scope}
%% ---------------- 右：断熱自由膨張（真空へ噴き出す）
\begin{scope}[xshift=7.60cm]
  \fill[black!28] (0.15,0.20) rectangle (1.65,2.00);
  \fill[black!6]  (1.65,0.20) rectangle (3.75,2.00);
  \draw[wall] (0.15,0.20) rectangle (3.75,2.00);
  \draw[wall] (1.65,0.20) -- (1.65,0.90);            % 仕切り（下半分）
  \draw[wall] (1.65,1.30) -- (1.65,2.00);            % 仕切り（上半分）
  \draw[frc] (1.40,1.10) -- (2.30,1.10);
  \node at (0.85,1.10) {\small 密};
  \node at (2.95,1.10) {\small 疎};
  \node[below,align=center] at (1.95,0.05)
    {\small 断熱自由膨張\\[0.8mm]\small 圧力が一様でないので$PV^\gamma=$（一定）は使えない\\[0.8mm]\small 仕事も熱も $0$ なので温度は変わらない};
\end{scope}
"""



# =====================================================================
#  【2026-09-21 レビュー対応】
#  ch16_ex8_pv / _blank … 例題10（原本の例題8）の p-V 図。
#    原本（physics_ch16.tex）の本文・図とも終状態の圧力が P_0+ka/S^2 になっていたが，
#    P(x)=P_0+kx/S に x=a を入れれば P_0+ka/S。同じ装置の練習［33］も P_0+ka/S。
#    図にも誤植が載っていたので作り直す（physics_ch16.tex も同時に訂正した）。
#    完全版と穴埋め版の補助図は同じ bbox になるよう，同じ座標で中身だけ空にする。
#  n23_zu_rei    … 23.5「手順の確認」の三角形サイクル（加筆）。
# =====================================================================
_EX8 = r"""
%(g1)s
\draw[gd] (0,1.05) -- (1.30,1.05);  \draw[gd] (0,2.70) -- (4.10,2.70);
\draw[gd] (1.30,0) -- (1.30,1.05);  \draw[gd] (4.10,0) -- (4.10,2.70);
\node[left] at (-0.05,1.05) {$P_0$};
\node[left] at (-0.05,2.70) {$P_0+\dfrac{ka}{S}$};
\node[below] at (1.30,-0.06) {$V_0$};  \node[below] at (4.10,-0.06) {$V_0+aS$};
\draw[cv] (1.30,1.05) -- (4.10,2.70);
\draw[frc] (2.55,1.79) -- (2.85,1.97);
\fill (1.30,1.05) circle (0.055);  \fill (4.10,2.70) circle (0.055);
\node[inner sep=1pt] at (2.70,0.52) {$w$};
%(g2)s
\draw[ax] (0,0) -- (5.55,0);  \node[below] at (5.30,-0.06) {$V$};
\draw[ax] (0,0) -- (0,3.45);  \node[above] at (0.02,3.42) {$p$};
\node[below left] at (0,0) {$\mathrm{O}$};
"""
#  穴埋め版は「軸だけ残して中身を消した」図。消す要素は opacity=0 にして
#  bbox を完全版と1ptも変えない（組版チェックリスト §4.5）。
FIGS['ch16_ex8_pv'] = _EX8 % {
    'g1': r'\fill[black!18] (1.30,0) -- (1.30,1.05) -- (4.10,2.70) -- (4.10,0) -- cycle;'
          + '\n\\begin{scope}',
    'g2': r'\end{scope}'}
FIGS['ch16_ex8_pv_blank'] = _EX8 % {
    'g1': r'\begin{scope}[opacity=0]', 'g2': r'\end{scope}'}

# ---------------------------------------------------------------------
#  23.5「手順の確認」の三角形サイクル
#   A(V0,P0) →定積→ B(V0,2P0) →直線→ C(3V0,P0) →定圧→ A（単原子分子理想気体）
#   この数値なら B→C の途中でも吸熱のまま（過程ごとに Q の符号が一定）になる。
# ---------------------------------------------------------------------
FIGS['n23_zu_rei'] = r"""
\fill[black!22] (1.40,1.20) -- (1.40,2.40) -- (4.20,1.20) -- cycle;
\draw[gd] (0,1.20) -- (1.40,1.20);  \draw[gd] (0,2.40) -- (1.40,2.40);
\draw[gd] (1.40,0) -- (1.40,1.20);  \draw[gd] (4.20,0) -- (4.20,1.20);
\draw[ax] (0,0) -- (5.70,0);  \node[below] at (5.40,-0.06) {$V\,[\mathrm{m^3}]$};
\draw[ax] (0,0) -- (0,3.15);  \node[above] at (0.02,3.12) {$p\,[\mathrm{Pa}]$};
\node[below left] at (0,0) {$\mathrm{O}$};
\node[left] at (-0.05,1.20) {$P_0$};  \node[left] at (-0.05,2.40) {$2P_0$};
\node[below] at (1.40,-0.06) {$V_0$}; \node[below] at (4.20,-0.06) {$3V_0$};
\draw[cv] (1.40,1.20) -- (1.40,2.40) -- (4.20,1.20) -- cycle;
\draw[frc] (1.40,1.62) -- (1.40,1.90);
\draw[frc] (2.60,1.89) -- (2.90,1.76);
\draw[frc] (3.20,1.20) -- (2.85,1.20);
\node[below right,inner sep=2pt] at (1.40,1.20) {$\mathrm{A}$};
\node[above left ,inner sep=1.5pt] at (1.40,2.40) {$\mathrm{B}$};
\node[right,inner sep=3pt]        at (4.20,1.20) {$\mathrm{C}$};
\node[inner sep=1pt] at (2.25,1.45) {\small $W_{\mathrm{total}}$};
"""


def main():
    want = [a for a in sys.argv[1:]]
    names = [n for n in FIGS if (not want or any(w in n for w in want))]
    for n in sorted(names):
        build(n, FIGS[n])


if __name__ == '__main__':
    main()
