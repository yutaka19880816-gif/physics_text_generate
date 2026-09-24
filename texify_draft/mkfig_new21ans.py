# -*- coding: utf-8 -*-
# 新第21回（気体の状態方程式と熱力学第一法則）の解説図を TikZ で自作する。
#   21.1「圧力」で力のつり合いの式を立てる2か所に，力の作用図を添えるためのもの。
#   （2026-09-20 ユーザー指摘「力のつり合いの式を立てる時は，力の作用図を入れた方がわかりやすい」）
#     n21_zu_piston … シリンダーをふさぐピストンにはたらく3力（P_0S・mg・PS）
#     n21_zu_water  … 水中の水柱にはたらく3力（P_0S・ρhSg・p(h)S）
#   図中に和文を書くので uplatex → dvipdfmx → gs（mkfig_new20ans.build_ja と同じ方式）。
#   使い方:  python3 texify_draft/mkfig_new21ans.py     （プロジェクトルートで実行）
import os, sys, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

TMPD = '/private/tmp/claude-501/-Users-yutaka-Documents-Claude-Code----math-tex-tool/7cb07582-9078-4f1f-991f-872effaa8d88/scratchpad/tikz21'
os.makedirs(TMPD, exist_ok=True)

HEAD = r"""\documentclass[border=3pt,dvipdfmx]{standalone}
\usepackage{amsmath}
\usepackage{tikz}
\usetikzlibrary{arrows.meta}
\begin{document}
\begin{tikzpicture}[line join=round,line cap=round,
   wall/.style={line width=1.1pt},
   thin/.style={line width=0.5pt},
   frc/.style={-{Latex[length=2.2mm,width=1.8mm]},line width=1.0pt},
   dim/.style={{Latex[length=1.6mm]}-{Latex[length=1.6mm]},line width=0.5pt}]
"""
TAIL = "\\end{tikzpicture}\n\\end{document}\n"


def remake_xbb(png):
    """.xbb は .png より新しいと extractbb が黙ってスキップするので必ず消してから作る（§1.5）。"""
    xbb = png[:-4] + '.xbb'
    if os.path.exists(xbb):
        os.remove(xbb)
    subprocess.run(['extractbb', png], capture_output=True)


def build(name, body):
    tex = os.path.join(TMPD, name + '.tex')
    open(tex, 'w', encoding='utf-8').write(HEAD + body + TAIL)
    for _ in range(2):                      # 和文なので uplatex を2回
        r = subprocess.run(['uplatex', '-interaction=nonstopmode', '-output-directory', TMPD, tex],
                           capture_output=True, text=True)
    dvi = os.path.join(TMPD, name + '.dvi')
    if not os.path.exists(dvi):
        print('  !! コンパイル失敗', name)
        print('\n'.join(l for l in r.stdout.splitlines() if l.startswith('!'))[:800]); return
    pdf = os.path.join(TMPD, name + '.pdf')
    subprocess.run(['dvipdfmx', '-o', pdf, dvi], capture_output=True)
    out = 'fig/%s.png' % name
    subprocess.run(['gs', '-sDEVICE=pnggray', '-r600', '-dNOPAUSE', '-dBATCH', '-o', out, pdf],
                   capture_output=True)
    remake_xbb(out)
    import struct
    w, h = struct.unpack('>II', open(out, 'rb').read(64)[16:24])
    print('  %-22s %5dx%-5d (縦横比 %.2f)  %6.1f KB' % (os.path.basename(out), w, h, h / w,
                                                      os.path.getsize(out) / 1000))


# ---------------------------------------------------------------- ピストン
# シリンダー（内壁 x=0.9〜4.5，底 y=0.3）＋ ピストン（y=2.9〜3.35）
piston = r"""
%% 気体（塗りを先に。あとから壁を描かないと壁が塗りで隠れる）
\fill[gray!12] (0.9,0.3) rectangle (4.5,2.9);
%% ピストン
\fill[gray!50] (0.9,2.9) rectangle (4.5,3.35);
%% シリンダー（側壁と底）
\draw[wall] (0.9,4.3) -- (0.9,0.3) -- (4.5,0.3) -- (4.5,4.3);
\draw[wall] (0.9,2.9) rectangle (4.5,3.35);
%% 3力
\draw[frc] (2.7,4.95) -- (2.7,3.45);   \node[above] at (2.7,4.95) {$P_0S$};
\draw[frc] (1.75,2.88) -- (1.75,1.75); \node[right] at (1.82,2.32) {$mg$};
\draw[frc] (3.65,1.75) -- (3.65,2.88); \node[left]  at (3.58,2.32) {$PS$};
%% ラベル
\node[left]  at (0.80,3.12) {ピストン};
\node at (2.7,1.15) {気体 $P$};
\node at (2.7,0.62) {断面積 $S$};
"""

# ---------------------------------------------------------------- 水柱
water = r"""
%% 水面と水
\fill[gray!8] (0,0.15) rectangle (7.0,4.5);
\draw[wall] (0,4.5) -- (7.0,4.5);
\node[above right] at (0.05,4.55) {水面};
%% 水柱
\fill[gray!28] (1.95,1.0) rectangle (4.15,4.5);
\draw[thin] (1.95,1.0) rectangle (4.15,4.5);
%% 深さ h
\draw[dim] (1.40,4.5) -- (1.40,1.0); \node[left] at (1.33,2.75) {$h$};
%% 3力
\draw[frc] (3.05,5.35) -- (3.05,4.60); \node[right] at (3.15,5.02) {$P_0S$};
\draw[frc] (3.05,3.55) -- (3.05,2.35); \node[right] at (3.15,2.95) {$\rho hSg$};
\draw[frc] (3.05,0.35) -- (3.05,0.95); \node[right] at (3.15,0.62) {$p(h)S$};
%% ラベル
\node at (3.05,4.08) {断面積 $S$};
\node[right] at (4.25,1.45) {密度 $\rho$ の水};
"""

build('n21_zu_piston', piston)
build('n21_zu_water',  water)
